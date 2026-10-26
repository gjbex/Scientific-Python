"""Execute manifest notebooks and apply their committed-output policies."""

from __future__ import annotations

import argparse
import os
import stat
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

OUTPUT_POLICY_PRESERVE = "preserve_source"
OUTPUT_POLICY_STRIP = "strip"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PIXI_ENVIRONMENT = "full"
SKIP_EXECUTION_TAG = "skip-execution"
SUPPORTED_OUTPUT_POLICIES = {OUTPUT_POLICY_PRESERVE, OUTPUT_POLICY_STRIP}


class RefreshError(RuntimeError):
    """Raised when the manifest cannot define a safe output-refresh run."""


@dataclass(frozen=True)
class NotebookSpec:
    path: Path
    output_policy: str


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("validation/manifest.toml"),
    )
    return parser


def load_notebook_specs(repository: Path, manifest_path: Path) -> list[NotebookSpec]:
    """Load and validate manifest notebook paths and output policies."""
    repository = repository.resolve()
    manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest.get("notebooks")
    if not isinstance(entries, list) or not entries:
        raise RefreshError("manifest contains no notebook entries")

    specs: list[NotebookSpec] = []
    seen_paths: set[Path] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise RefreshError("manifest contains an invalid notebook entry")
        relative_text = entry.get("path")
        properties = entry.get("properties")
        if not isinstance(relative_text, str) or not isinstance(properties, dict):
            raise RefreshError("manifest notebook entry lacks path or properties")
        relative = Path(relative_text)
        if relative.is_absolute() or ".." in relative.parts:
            raise RefreshError(f"unsafe notebook path in manifest: {relative_text}")
        if relative.suffix != ".ipynb":
            raise RefreshError(f"manifest path is not a notebook: {relative_text}")
        if relative in seen_paths:
            raise RefreshError(f"duplicate notebook path in manifest: {relative_text}")
        seen_paths.add(relative)

        output_policy = properties.get("output_policy")
        if output_policy not in SUPPORTED_OUTPUT_POLICIES:
            raise RefreshError(
                f"unsupported output policy for {relative_text}: {output_policy!r}"
            )
        path = (repository / relative).resolve()
        try:
            path.relative_to(repository)
        except ValueError as error:
            raise RefreshError(
                f"notebook path resolves outside repository: {relative_text}"
            ) from error
        if not path.is_file():
            raise RefreshError(f"manifest notebook does not exist: {relative_text}")
        specs.append(NotebookSpec(path=path, output_policy=output_policy))

    return sorted(specs, key=lambda spec: spec.path.as_posix())


def execute_and_write_notebook(path: Path, output_policy: str) -> None:
    """Execute one notebook and replace it atomically after successful completion."""
    if output_policy not in SUPPORTED_OUTPUT_POLICIES:
        raise RefreshError(f"unsupported output policy: {output_policy!r}")

    import nbformat
    from nbclient import NotebookClient

    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=None,
        resources={"metadata": {"path": str(path.parent)}},
        skip_cells_with_tag=SKIP_EXECUTION_TAG,
    )
    client.execute()
    if output_policy == OUTPUT_POLICY_STRIP:
        strip_notebook_outputs(notebook)
    write_notebook_atomic(notebook, path, nbformat)


def strip_notebook_outputs(notebook: Any) -> None:
    """Remove code outputs and execution state from an executed notebook."""
    notebook.metadata.pop("widgets", None)
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        cell.outputs = []
        cell.execution_count = None
        cell.metadata.pop("execution", None)
        cell.metadata.pop("ExecuteTime", None)


def write_notebook_atomic(notebook: Any, path: Path, nbformat_module: Any) -> None:
    """Replace a notebook without exposing a partially written destination."""
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.stem}-",
        suffix=".ipynb",
    )
    os.close(descriptor)
    temporary_path = Path(temporary_name)
    try:
        nbformat_module.write(notebook, temporary_path)
        temporary_path.chmod(stat.S_IMODE(path.stat().st_mode))
        temporary_path.replace(path)
    finally:
        temporary_path.unlink(missing_ok=True)


def main(arguments: list[str] | None = None) -> int:
    namespace = create_parser().parse_args(arguments)
    repository = namespace.repository.resolve()
    if not repository.is_dir():
        print(f"error: repository is not a directory: {repository}", file=sys.stderr)
        return 2
    manifest_path = namespace.manifest
    if not manifest_path.is_absolute():
        manifest_path = repository / manifest_path

    environment = os.environ.get("PIXI_ENVIRONMENT_NAME")
    if environment != REQUIRED_PIXI_ENVIRONMENT:
        print(
            "error: output refresh requires the full Pixi environment; run "
            "'pixi run -e full refresh-notebook-outputs'",
            file=sys.stderr,
        )
        return 2

    try:
        specs = load_notebook_specs(repository, manifest_path)
    except (OSError, RefreshError, tomllib.TOMLDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ["EXEC_BENCHMARKS"] = "1"
    total = len(specs)
    for index, spec in enumerate(specs, start=1):
        relative = spec.path.relative_to(repository)
        print(
            f"[{index}/{total}] executing {relative} "
            f"(outputs: {spec.output_policy})",
            flush=True,
        )
        try:
            execute_and_write_notebook(spec.path, spec.output_policy)
        except Exception as error:  # noqa: BLE001 - show the failing notebook
            print(
                f"error: {spec.path} failed: {type(error).__name__}: {error}",
                file=sys.stderr,
            )
            return 1

    print(f"Executed and updated {total} notebooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
