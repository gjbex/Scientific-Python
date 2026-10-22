"""Execute manifest-selected notebooks in locked Pixi environments.

The orchestrator delegates classification and reporting to the shared
Training-sessions tool. This repository owns timeouts, assertions, artifacts,
environment invocation, and the decision about which profile to execute.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
import zlib
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from .assertions import assertion_cell, parse_assertion_records
except ImportError:
    from assertions import assertion_cell, parse_assertion_records

RUNNER_NAME = "scientific-python-notebook-runner"
RUNNER_VERSION = "1"


class ValidationError(RuntimeError):
    """Raised for unsafe or inconsistent validation configuration."""


@dataclass(frozen=True)
class ClassifierCommand:
    """A shell-free command and environment for the shared classifier."""

    arguments: tuple[str, ...]
    environment: dict[str, str]


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run")
    run.add_argument("--profile", choices=("smoke", "required"), default="smoke")
    run.add_argument("--repository", type=Path, default=Path.cwd())
    run.add_argument("--output-directory", type=Path)

    worker = subparsers.add_parser("worker")
    worker.add_argument("--repository", type=Path, required=True)
    worker.add_argument("--plan", type=Path, required=True)
    worker.add_argument("--configuration", type=Path, required=True)
    worker.add_argument("--notebook-id", required=True)
    worker.add_argument("--environment", required=True)
    worker.add_argument("--artifact-root", type=Path, required=True)
    worker.add_argument("--result", type=Path, required=True)
    return parser


def main(arguments: list[str] | None = None) -> int:
    namespace = create_parser().parse_args(arguments)
    try:
        if namespace.command == "run":
            return run_profile(
                namespace.repository,
                namespace.profile,
                namespace.output_directory,
            )
        return run_worker(namespace)
    except (OSError, ValidationError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


def run_profile(
    repository: Path, profile_name: str, output_directory: Path | None
) -> int:
    repository = git_root(repository)
    configuration_path = repository / "validation" / "execution.toml"
    configuration = load_toml(configuration_path)
    validate_configuration(configuration)
    profile = configuration["profiles"][profile_name]
    selected_ids = profile["notebook_ids"]
    output = prepare_output_directory(repository, output_directory)
    artifact_root = output / "artifacts"
    artifact_root.mkdir()
    fragments = output / "fragments"
    fragments.mkdir()
    plan_path = output / "plan.json"
    results_path = output / "results.json"
    report_path = output / "report.md"
    summary_path = output / "summary.json"
    metadata_path = output / "run-metadata.json"
    classifier = discover_classifier(repository)

    create_plan_arguments = [
        *classifier.arguments,
        "create-validation-plan",
        "--repository",
        str(repository),
        "--include-tier",
        "required",
    ]
    for notebook_id in selected_ids:
        create_plan_arguments.extend(("--include-id", notebook_id))
    create_plan_arguments.extend(("--output", str(plan_path)))
    plan_process = subprocess.run(
        create_plan_arguments,
        check=False,
        cwd=repository,
        env=classifier.environment,
        text=True,
        capture_output=True,
    )
    if plan_process.returncode != 0:
        raise ValidationError(
            plan_process.stderr.strip()
            or plan_process.stdout.strip()
            or "validation plan creation failed"
        )

    plan = load_json(plan_path)
    candidates = [entry for entry in plan["entries"] if entry["action"] == "candidate"]
    candidate_ids = {entry["notebook_id"] for entry in candidates}
    if candidate_ids != set(selected_ids):
        raise ValidationError(
            "planned candidates differ from the target-owned profile: "
            f"planned={sorted(candidate_ids)}, configured={sorted(selected_ids)}"
        )

    start = time.monotonic()
    environment_metrics: dict[str, dict[str, Any]] = {}
    result_entries: list[dict[str, Any]] = []
    by_environment: dict[str, list[dict[str, Any]]] = {}
    for entry in candidates:
        environment = str(entry["properties"]["environment"])
        by_environment.setdefault(environment, []).append(entry)

    for environment, entries in sorted(by_environment.items()):
        setup_started = time.monotonic()
        setup_process = run_in_environment(
            repository,
            environment,
            ["python", "-c", "import sys; print(sys.version.split()[0])"],
        )
        setup_duration = time.monotonic() - setup_started
        environment_metrics[environment] = {
            "setup_seconds": round(setup_duration, 9),
            "setup_returncode": setup_process.returncode,
            "python_version": setup_process.stdout.strip() or None,
            "notebook_count": len(entries),
        }
        if setup_process.returncode != 0:
            for entry in entries:
                result_entries.append(
                    infrastructure_error_entry(
                        entry,
                        environment,
                        "environment_setup_error",
                        setup_process.stderr.strip() or "Pixi environment setup failed",
                    )
                )
            continue

        for entry in entries:
            notebook_id = entry["notebook_id"]
            fragment_path = fragments / f"{notebook_id}.json"
            worker_arguments = [
                "python",
                "-B",
                "validation/run_validation.py",
                "worker",
                "--repository",
                str(repository),
                "--plan",
                str(plan_path),
                "--configuration",
                str(configuration_path),
                "--notebook-id",
                notebook_id,
                "--environment",
                environment,
                "--artifact-root",
                str(artifact_root),
                "--result",
                str(fragment_path),
            ]
            worker_process = run_in_environment(
                repository, environment, worker_arguments
            )
            log_relative = f"logs/{notebook_id}.log"
            log_path = safe_relative_path(artifact_root, log_relative)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text(
                worker_process.stdout + worker_process.stderr,
                encoding="utf-8",
            )
            if fragment_path.is_file():
                result_entry = load_json(fragment_path)
            else:
                result_entry = infrastructure_error_entry(
                    entry,
                    environment,
                    "worker_process_error",
                    f"worker exited with status {worker_process.returncode}",
                )
            result_entry["artifacts"].append(
                {
                    "kind": "log",
                    "path": log_relative,
                    "digest": file_digest(log_path),
                }
            )
            result_entries.append(result_entry)

    results = {
        "schema_version": 1,
        "runner": {"name": RUNNER_NAME, "version": RUNNER_VERSION},
        "plan_digest": plan["plan_digest"],
        "repository": {
            "id": plan["repository"]["id"],
            "commit": git_text(repository, "rev-parse", "HEAD"),
            "platform": "linux-64",
        },
        "entries": sorted(result_entries, key=lambda item: item["notebook_id"]),
    }
    write_json_atomic(results_path, results)

    validation_process = run_classifier(
        classifier,
        repository,
        [
            "validate-validation-results",
            "--plan",
            str(plan_path),
            "--results",
            str(results_path),
            "--artifact-root",
            str(artifact_root),
            "--json",
        ],
    )
    (output / "validation-assessment.json").write_text(
        validation_process.stdout, encoding="utf-8"
    )
    if validation_process.stderr:
        (output / "validation-diagnostics.log").write_text(
            validation_process.stderr, encoding="utf-8"
        )

    markdown_process = run_classifier(
        classifier,
        repository,
        [
            "summarize-validation",
            "--plan",
            str(plan_path),
            "--results",
            str(results_path),
            "--artifact-root",
            str(artifact_root),
            "--output",
            str(report_path),
        ],
    )
    json_process = run_classifier(
        classifier,
        repository,
        [
            "summarize-validation",
            "--plan",
            str(plan_path),
            "--results",
            str(results_path),
            "--artifact-root",
            str(artifact_root),
            "--format",
            "json",
            "--output",
            str(summary_path),
        ],
    )

    elapsed = time.monotonic() - start
    budget = configuration["policy"]["required_budget_seconds"]
    metadata = {
        "schema_version": 1,
        "profile": profile_name,
        "plan_digest": plan["plan_digest"],
        "repository_commit": plan["repository"]["commit"],
        "repository_dirty": plan["repository"]["dirty"],
        "total_seconds": round(elapsed, 9),
        "budget_seconds": budget,
        "budget_exceeded": elapsed > budget,
        "environment_metrics": environment_metrics,
        "pixi_version": command_output(["pixi", "--version"]),
        "lockfile_sha256": file_digest(repository / "pixi.lock"),
        "reproduction_command": f"pixi run --locked validation-{profile_name}",
    }
    write_json_atomic(metadata_path, metadata)
    print(f"validation evidence: {output}")
    print(f"human report: {report_path}")

    outcomes_ok = all(entry["outcome"] == "pass" for entry in result_entries)
    reports_ok = all(
        process.returncode == 0
        for process in (validation_process, markdown_process, json_process)
    )
    return int(not outcomes_ok or not reports_ok or elapsed > budget)


def run_worker(namespace: argparse.Namespace) -> int:
    repository = git_root(namespace.repository)
    artifact_root = namespace.artifact_root.resolve()
    result_path = namespace.result.resolve()
    require_outside_repository(repository, artifact_root, "artifact root")
    require_outside_repository(repository, result_path, "result path")
    artifact_root.mkdir(parents=True, exist_ok=True)
    plan = load_json(namespace.plan)
    configuration = load_toml(namespace.configuration)
    validate_configuration(configuration)
    entry = next(
        (
            item
            for item in plan["entries"]
            if item["notebook_id"] == namespace.notebook_id
        ),
        None,
    )
    if entry is None or entry["action"] != "candidate":
        raise ValidationError("worker notebook is not a plan candidate")
    expected_environment = str(entry["properties"]["environment"])
    if namespace.environment != expected_environment:
        raise ValidationError("worker environment does not match the plan")
    policies = {item["id"]: item for item in configuration["notebooks"]}
    policy = policies[namespace.notebook_id]
    result = execute_entry(
        repository,
        entry,
        namespace.environment,
        policy,
        artifact_root,
    )
    write_json_atomic(result_path, result)
    if result["outcome"] != "pass":
        print(f"{result['notebook_id']}: {result['outcome']} ({result['reason_code']})")
        for check in result["checks"]:
            if check["outcome"] != "pass":
                print(f"{check['name']}: {check['message']}")
    return int(result["outcome"] != "pass")


def execute_entry(
    repository: Path,
    entry: dict[str, Any],
    environment: str,
    policy: dict[str, Any],
    artifact_root: Path,
) -> dict[str, Any]:
    notebook_id = entry["notebook_id"]
    before = git_status(repository)
    started_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    started = time.monotonic()
    checks: list[dict[str, str]] = []
    artifacts: list[dict[str, str]] = []
    outcome = "pass"
    reason_code = "declared_checks_passed"
    observed_blob = entry["current_blob"]
    executed_relative = f"executed-notebooks/{notebook_id}.ipynb"
    executed_path = safe_relative_path(artifact_root, executed_relative)
    executed_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        source = safe_relative_path(repository, entry["path"])
        observed_blob = git_text(repository, "hash-object", "--", str(source))
        if observed_blob != entry["current_blob"]:
            raise ValidationError("source notebook blob does not match the plan")
        with temporary_repository_copy(repository) as temporary_repository:
            temporary_notebook = safe_relative_path(temporary_repository, entry["path"])
            notebook = execute_notebook(
                temporary_notebook,
                policy["timeout_seconds"],
                policy.get("assertions", []),
                executed_path,
            )
            checks.append(
                {
                    "name": "notebook_execution",
                    "outcome": "pass",
                    "message": "kernel completed in an isolated repository copy",
                }
            )
            assertion_records = parse_assertion_records(
                notebook, policy.get("assertions", [])
            )
            checks.extend(assertion_records)
            checks.extend(
                collect_declared_artifacts(
                    temporary_notebook.parent,
                    notebook_id,
                    policy.get("artifacts", []),
                    artifact_root,
                    artifacts,
                )
            )
        if any(check["outcome"] == "fail" for check in checks):
            outcome = "fail"
            reason_code = "declared_check_failed"
    except Exception as error:  # noqa: BLE001 - runner errors are result evidence
        outcome = "error"
        reason_code = "notebook_execution_error"
        checks.append(
            {
                "name": "notebook_execution",
                "outcome": "error",
                "message": f"{type(error).__name__}: {error}",
            }
        )
    finally:
        if executed_path.is_file():
            artifacts.append(
                {
                    "kind": "executed_notebook",
                    "path": executed_relative,
                    "digest": file_digest(executed_path),
                }
            )

    unchanged = git_status(repository) == before
    return {
        "notebook_id": notebook_id,
        "path": entry["path"],
        "source_blob": observed_blob,
        "environment": environment,
        "observed_environment": {
            "name": environment,
            "python_version": platform.python_version(),
        },
        "outcome": outcome,
        "reason_code": reason_code,
        "started_at": started_at,
        "duration_seconds": round(time.monotonic() - started, 9),
        "timeout_seconds": policy["timeout_seconds"],
        "artifacts": artifacts,
        "checks": checks,
        "worktree_unchanged": unchanged,
    }


def execute_notebook(
    path: Path,
    timeout: int,
    assertion_names: list[str],
    executed_path: Path | None = None,
):
    import nbformat
    from nbclient import NotebookClient

    os.environ.setdefault("MPLBACKEND", "Agg")
    notebook = nbformat.read(path, as_version=4)
    source = assertion_cell(assertion_names)
    if source is not None:
        notebook.cells.append(
            nbformat.v4.new_code_cell(
                source=source,
                metadata={"tags": ["validation-only"]},
            )
        )
    client = NotebookClient(
        notebook,
        timeout=timeout,
        resources={"metadata": {"path": str(path.parent)}},
    )
    try:
        client.execute()
    finally:
        if executed_path is not None:
            executed_path.parent.mkdir(parents=True, exist_ok=True)
            nbformat.write(notebook, executed_path)
    return notebook


def collect_declared_artifacts(
    working_directory: Path,
    notebook_id: str,
    declarations: list[dict[str, Any]],
    artifact_root: Path,
    artifacts: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    for declaration in declarations:
        relative = declaration["path"]
        source = safe_relative_path(working_directory, relative)
        check_name = f"artifact:{relative}"
        if not source.is_file():
            checks.append(
                {
                    "name": check_name,
                    "outcome": "fail",
                    "message": "declared generated file is missing",
                }
            )
            continue
        try:
            if declaration["validator"] == "png":
                validate_png(source, declaration["minimum_bytes"])
            else:
                raise ValidationError(
                    f"unsupported artifact validator: {declaration['validator']}"
                )
        except ValidationError as error:
            checks.append(
                {"name": check_name, "outcome": "fail", "message": str(error)}
            )
            continue
        stored_relative = f"generated/{notebook_id}/{relative}"
        destination = safe_relative_path(artifact_root, stored_relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        artifacts.append(
            {
                "kind": declaration["kind"],
                "path": stored_relative,
                "digest": file_digest(destination),
            }
        )
        checks.append(
            {
                "name": check_name,
                "outcome": "pass",
                "message": (f"valid PNG artifact, {source.stat().st_size} bytes"),
            }
        )
    return checks


def validate_png(path: Path, minimum_bytes: int) -> None:
    content = path.read_bytes()
    if len(content) < minimum_bytes:
        raise ValidationError(
            f"PNG is {len(content)} bytes; required at least {minimum_bytes}"
        )
    if content[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValidationError("file does not have a PNG signature")
    offset = 8
    chunk_types: list[bytes] = []
    width = 0
    height = 0
    while offset < len(content):
        if offset + 12 > len(content):
            raise ValidationError("PNG contains a truncated chunk header")
        length = int.from_bytes(content[offset : offset + 4], "big")
        chunk_type = content[offset + 4 : offset + 8]
        end = offset + 12 + length
        if end > len(content):
            raise ValidationError("PNG contains a truncated chunk")
        chunk_data = content[offset + 8 : offset + 8 + length]
        expected_crc = int.from_bytes(content[offset + 8 + length : end], "big")
        observed_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if observed_crc != expected_crc:
            raise ValidationError("PNG chunk checksum is invalid")
        chunk_types.append(chunk_type)
        if chunk_type == b"IHDR":
            if length != 13 or len(chunk_types) != 1:
                raise ValidationError("PNG has an invalid IHDR chunk")
            width = int.from_bytes(chunk_data[:4], "big")
            height = int.from_bytes(chunk_data[4:8], "big")
        offset = end
        if chunk_type == b"IEND":
            break
    if not {b"IHDR", b"IDAT", b"IEND"} <= set(chunk_types):
        raise ValidationError("PNG is missing a required chunk")
    if offset != len(content):
        raise ValidationError("PNG contains trailing bytes after IEND")
    if width <= 0 or height <= 0:
        raise ValidationError("PNG dimensions must be positive")


def validate_configuration(configuration: dict[str, Any]) -> None:
    if configuration.get("schema_version") != 1:
        raise ValidationError("unsupported execution configuration schema")
    if configuration["policy"]["platform"] != "linux-64":
        raise ValidationError("only linux-64 is supported")
    notebooks = configuration.get("notebooks", [])
    ids = [item["id"] for item in notebooks]
    if len(ids) != len(set(ids)):
        raise ValidationError("execution configuration contains duplicate IDs")
    for item in notebooks:
        timeout = item.get("timeout_seconds")
        if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout <= 0:
            raise ValidationError(f"invalid timeout for {item['id']}")
        assertion_cell(item.get("assertions", []))
        for artifact in item.get("artifacts", []):
            safe_relative_parts(artifact["path"])
    configured = set(ids)
    for name, profile in configuration.get("profiles", {}).items():
        profile_ids = profile["notebook_ids"]
        if len(profile_ids) != len(set(profile_ids)):
            raise ValidationError(f"profile {name} contains duplicate IDs")
        missing = sorted(set(profile_ids) - configured)
        if missing:
            raise ValidationError(
                f"profile {name} lacks notebook configuration: {', '.join(missing)}"
            )


def infrastructure_error_entry(
    entry: dict[str, Any], environment: str, reason_code: str, message: str
) -> dict[str, Any]:
    return {
        "notebook_id": entry["notebook_id"],
        "path": entry["path"],
        "source_blob": entry["current_blob"],
        "environment": environment,
        "observed_environment": None,
        "outcome": "error",
        "reason_code": reason_code,
        "started_at": None,
        "duration_seconds": None,
        "timeout_seconds": None,
        "artifacts": [],
        "checks": [
            {"name": "runner_infrastructure", "outcome": "error", "message": message}
        ],
        "worktree_unchanged": True,
    }


def discover_classifier(repository: Path) -> ClassifierCommand:
    explicit = os.environ.get("NOTEBOOK_CLASSIFIER_ROOT")
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    candidates.append(
        repository.parent / "Training-sessions" / "tools" / "notebook-classifier"
    )
    for candidate in candidates:
        root = candidate.expanduser().resolve()
        source = root / "src"
        python = root / ".pixi" / "envs" / "default" / "bin" / "python"
        if source.is_dir() and python.is_file():
            environment = os.environ.copy()
            previous = environment.get("PYTHONPATH")
            environment["PYTHONPATH"] = (
                f"{source}{os.pathsep}{previous}" if previous else str(source)
            )
            return ClassifierCommand(
                arguments=(str(python), "-B", "-m", "notebook_classifier"),
                environment=environment,
            )
    executable = shutil.which("notebook-classifier")
    if executable:
        return ClassifierCommand(arguments=(executable,), environment=os.environ.copy())
    raise ValidationError(
        "notebook-classifier is unavailable; install the pinned Training-sessions "
        "tool or set NOTEBOOK_CLASSIFIER_ROOT"
    )


def run_classifier(
    classifier: ClassifierCommand, repository: Path, arguments: list[str]
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*classifier.arguments, *arguments],
        check=False,
        cwd=repository,
        env=classifier.environment,
        text=True,
        capture_output=True,
    )


def run_in_environment(
    repository: Path, environment: str, arguments: list[str]
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "pixi",
            "run",
            "--locked",
            "--manifest-path",
            str(repository / "pixi.toml"),
            "--environment",
            environment,
            *arguments,
        ],
        check=False,
        cwd=repository,
        text=True,
        capture_output=True,
    )


def prepare_output_directory(repository: Path, requested: Path | None) -> Path:
    if requested is None:
        return Path(tempfile.mkdtemp(prefix="scientific-python-validation-"))
    output = requested.expanduser().resolve()
    require_outside_repository(repository, output, "output directory")
    if output.exists():
        raise ValidationError(f"output directory already exists: {output}")
    if not output.parent.is_dir():
        raise ValidationError(f"output parent does not exist: {output.parent}")
    output.mkdir()
    return output


@contextmanager
def temporary_repository_copy(repository: Path) -> Iterator[Path]:
    with tempfile.TemporaryDirectory(prefix="scientific-python-notebook-") as directory:
        destination = Path(directory) / "repository"
        destination.mkdir()
        for relative in git_tracked_paths(repository):
            source = safe_relative_path(repository, relative)
            target = destination.joinpath(*safe_relative_parts(relative))
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target, follow_symlinks=False)
        yield destination


def git_tracked_paths(repository: Path) -> tuple[str, ...]:
    process = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repository), "ls-files", "-z"],
        check=False,
        capture_output=True,
    )
    if process.returncode != 0:
        raise ValidationError(
            process.stderr.decode(errors="replace").strip()
            or "unable to enumerate tracked files"
        )
    return tuple(
        path.decode(errors="surrogateescape")
        for path in process.stdout.split(b"\0")
        if path
    )


def safe_relative_parts(relative: str) -> tuple[str, ...]:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        raise ValidationError(f"unsafe relative path: {relative}")
    return pure.parts


def safe_relative_path(root: Path, relative: str) -> Path:
    candidate = root.joinpath(*safe_relative_parts(relative)).resolve()
    resolved_root = root.resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValidationError(f"path escapes its declared root: {relative}")
    return candidate


def require_outside_repository(repository: Path, path: Path, label: str) -> None:
    resolved_repository = repository.resolve()
    resolved_path = path.resolve()
    if (
        resolved_path == resolved_repository
        or resolved_repository in resolved_path.parents
    ):
        raise ValidationError(f"{label} must be outside the source repository")


def git_root(path: Path) -> Path:
    return Path(git_text(path.resolve(), "rev-parse", "--show-toplevel")).resolve()


def git_status(repository: Path) -> str:
    return git_text(
        repository,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    )


def git_text(repository: Path, *arguments: str) -> str:
    process = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repository), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        raise ValidationError(process.stderr.strip() or "Git command failed")
    return process.stdout.strip()


def command_output(arguments: list[str]) -> str | None:
    process = subprocess.run(arguments, check=False, capture_output=True, text=True)
    return process.stdout.strip() if process.returncode == 0 else None


def load_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValidationError(f"JSON document must be an object: {path}")
    return document


def load_toml(path: Path) -> dict[str, Any]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json_atomic(path: Path, document: dict[str, Any]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, text=True
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=2, sort_keys=True)
            handle.write("\n")
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
