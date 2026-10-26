"""Execute every source notebook and write successful outputs back in place."""

from __future__ import annotations

import argparse
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any

CHECKPOINT_DIRECTORY = ".ipynb_checkpoints"
REQUIRED_PIXI_ENVIRONMENT = "full"
SKIP_EXECUTION_TAG = "skip-execution"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("source-code"))
    return parser


def discover_notebooks(root: Path) -> list[Path]:
    """Return source notebooks in deterministic order, excluding checkpoints."""
    return sorted(
        path
        for path in root.rglob("*.ipynb")
        if CHECKPOINT_DIRECTORY not in path.parts
    )


def execute_and_write_notebook(path: Path) -> None:
    """Execute one notebook and replace it atomically after successful completion."""
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
    write_notebook_atomic(notebook, path, nbformat)


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
    root = namespace.root.resolve()
    if not root.is_dir():
        print(f"error: notebook root is not a directory: {root}", file=sys.stderr)
        return 2

    environment = os.environ.get("PIXI_ENVIRONMENT_NAME")
    if environment != REQUIRED_PIXI_ENVIRONMENT:
        print(
            "error: output refresh requires the full Pixi environment; run "
            "'pixi run -e full refresh-notebook-outputs'",
            file=sys.stderr,
        )
        return 2

    notebooks = discover_notebooks(root)
    if not notebooks:
        print(f"error: no notebooks found below {root}", file=sys.stderr)
        return 2

    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ["EXEC_BENCHMARKS"] = "1"
    total = len(notebooks)
    for index, path in enumerate(notebooks, start=1):
        print(f"[{index}/{total}] executing {path.relative_to(root)}", flush=True)
        try:
            execute_and_write_notebook(path)
        except Exception as error:  # noqa: BLE001 - show the failing notebook
            print(
                f"error: {path} failed: {type(error).__name__}: {error}",
                file=sys.stderr,
            )
            return 1

    print(f"Executed and updated {total} notebooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
