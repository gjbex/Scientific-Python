from __future__ import annotations

import struct
import tempfile
import unittest
import zlib
from pathlib import Path

import nbformat
from nbclient.exceptions import CellExecutionError

from validation.assertions import parse_assertion_records
from validation.refresh_notebook_outputs import (
    OUTPUT_POLICY_PRESERVE,
    OUTPUT_POLICY_STRIP,
    execute_and_write_notebook,
    load_notebook_specs,
)
from validation.run_validation import (
    BENCHMARK_CELL_TAG,
    NotebookTimeoutError,
    ValidationError,
    clear_skipped_execution_state,
    execute_entry,
    execute_notebook,
    infrastructure_error_entry,
    load_toml,
    safe_relative_path,
    validate_configuration,
    validate_png,
)

ROOT = Path(__file__).resolve().parents[1]


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def _one_pixel_png() -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"
    header = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    pixels = zlib.compress(b"\x00\x00\x00\x00")
    return (
        signature
        + _png_chunk(b"IHDR", header)
        + _png_chunk(b"IDAT", pixels)
        + _png_chunk(b"IEND", b"")
    )


class ConfigurationTests(unittest.TestCase):
    def test_profiles_match_reviewed_required_manifest_entries(self) -> None:
        configuration = load_toml(ROOT / "validation" / "execution.toml")
        manifest = load_toml(ROOT / "validation" / "manifest.toml")
        required_ids = {
            notebook["id"]
            for notebook in manifest["notebooks"]
            if notebook["properties"].get("validation_tier") == "required"
        }

        validate_configuration(configuration)

        self.assertEqual(
            set(configuration["profiles"]["required"]["notebook_ids"]),
            required_ids,
        )
        self.assertEqual(len(configuration["profiles"]["smoke"]["notebook_ids"]), 4)
        self.assertTrue(
            all("path" not in notebook for notebook in configuration["notebooks"])
        )

    def test_interrupted_worker_is_an_error_not_a_pass(self) -> None:
        entry = {
            "notebook_id": "fixture",
            "path": "fixture.ipynb",
            "current_blob": "0" * 40,
        }

        result = infrastructure_error_entry(
            entry, "default", "worker_process_error", "interrupted"
        )

        self.assertEqual(result["outcome"], "error")
        self.assertEqual(result["checks"][0]["outcome"], "error")

    def test_missing_environment_is_an_error_not_a_pass(self) -> None:
        entry = {
            "notebook_id": "fixture",
            "path": "fixture.ipynb",
            "current_blob": "0" * 40,
        }

        result = infrastructure_error_entry(
            entry,
            "missing",
            "environment_setup_error",
            "Pixi environment setup failed",
        )

        self.assertEqual(result["outcome"], "error")
        self.assertEqual(result["reason_code"], "environment_setup_error")
        self.assertIsNone(result["observed_environment"])


class AssertionTests(unittest.TestCase):
    def test_skipped_benchmark_state_is_cleared(self) -> None:
        benchmark = nbformat.v4.new_code_cell(
            "raise RuntimeError('benchmark must not execute')",
            execution_count=17,
            outputs=[nbformat.v4.new_output("stream", name="stdout", text="stale\n")],
            metadata={
                "tags": [BENCHMARK_CELL_TAG],
                "execution": {"iopub.status.busy": "stale"},
                "ExecuteTime": {"start_time": "stale", "end_time": "stale"},
            },
        )
        notebook = nbformat.v4.new_notebook(cells=[benchmark])

        clear_skipped_execution_state(notebook, BENCHMARK_CELL_TAG)

        self.assertEqual(
            benchmark.source,
            "raise RuntimeError('benchmark must not execute')",
        )
        self.assertEqual(benchmark.metadata["tags"], [BENCHMARK_CELL_TAG])
        self.assertEqual(benchmark.outputs, [])
        self.assertIsNone(benchmark.execution_count)
        self.assertNotIn("execution", benchmark.metadata)
        self.assertNotIn("ExecuteTime", benchmark.metadata)

    def test_benchmark_cell_is_skipped_during_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "benchmark.ipynb"
            notebook = nbformat.v4.new_notebook(
                cells=[
                    nbformat.v4.new_code_cell("value = 42"),
                    nbformat.v4.new_code_cell(
                        "raise RuntimeError('benchmark must not execute')",
                        metadata={"tags": [BENCHMARK_CELL_TAG]},
                    ),
                    nbformat.v4.new_code_cell("assert value == 42"),
                ]
            )
            nbformat.write(notebook, path)

            executed = execute_notebook(path, 60, [])

        self.assertIsNotNone(executed.cells[0].execution_count)
        self.assertIsNone(executed.cells[1].execution_count)
        self.assertEqual(executed.cells[1].outputs, [])
        self.assertIsNotNone(executed.cells[2].execution_count)

    def test_output_refresh_executes_benchmark_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "benchmark.ipynb"
            notebook = nbformat.v4.new_notebook(
                cells=[
                    nbformat.v4.new_code_cell(
                        "print('benchmark executed')",
                        metadata={"tags": [BENCHMARK_CELL_TAG]},
                    )
                ]
            )
            nbformat.write(notebook, path)

            execute_and_write_notebook(path, OUTPUT_POLICY_PRESERVE)
            refreshed = nbformat.read(path, as_version=4)

        self.assertIsNotNone(refreshed.cells[0].execution_count)
        self.assertEqual(refreshed.cells[0].outputs[0].text, "benchmark executed\n")

    def test_failed_output_refresh_preserves_source_notebook(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "failure.ipynb"
            notebook = nbformat.v4.new_notebook(
                cells=[nbformat.v4.new_code_cell("raise RuntimeError('defect')")]
            )
            nbformat.write(notebook, path)
            original = path.read_bytes()

            with self.assertRaises(CellExecutionError):
                execute_and_write_notebook(path, OUTPUT_POLICY_PRESERVE)

            self.assertEqual(path.read_bytes(), original)

    def test_output_refresh_executes_then_strips_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "exercise.ipynb"
            notebook = nbformat.v4.new_notebook(
                cells=[
                    nbformat.v4.new_code_cell(
                        "from pathlib import Path\n"
                        "Path('benchmark-ran').write_text('yes')\n"
                        "print('discard this output')",
                        metadata={"tags": [BENCHMARK_CELL_TAG]},
                    )
                ],
                metadata={
                    "widgets": {
                        "application/vnd.jupyter.widget-state+json": {
                            "state": {},
                            "version_major": 2,
                            "version_minor": 0,
                        }
                    }
                },
            )
            nbformat.write(notebook, path)

            execute_and_write_notebook(path, OUTPUT_POLICY_STRIP)
            refreshed = nbformat.read(path, as_version=4)
            self.assertEqual((root / "benchmark-ran").read_text(), "yes")
            self.assertIsNone(refreshed.cells[0].execution_count)
            self.assertEqual(refreshed.cells[0].outputs, [])
            self.assertNotIn("execution", refreshed.cells[0].metadata)
            self.assertNotIn("ExecuteTime", refreshed.cells[0].metadata)
            self.assertNotIn("widgets", refreshed.metadata)

    def test_temporary_numerical_defect_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "defect.ipynb"
            notebook = nbformat.v4.new_notebook(
                cells=[
                    nbformat.v4.new_code_cell(
                        "import numpy as np\n"
                        "relative_discrepancies = np.array([1.0e-3])"
                    )
                ]
            )
            nbformat.write(notebook, path)

            executed = execute_notebook(path, 60, ["pendulum-route-agreement"])
            records = parse_assertion_records(executed, ["pendulum-route-agreement"])

        self.assertEqual(records[0]["outcome"], "fail")
        self.assertIn("required < 1.0e-08", records[0]["message"])

    def test_stale_blob_is_reported_as_execution_error(self) -> None:
        entry = {
            "notebook_id": "source-code-numpy-axes",
            "path": "source-code/numpy/axes.ipynb",
            "current_blob": "0" * 40,
        }
        policy = {"timeout_seconds": 30}
        with tempfile.TemporaryDirectory() as directory:
            result = execute_entry(ROOT, entry, "default", policy, Path(directory))

        self.assertEqual(result["outcome"], "error")
        self.assertIn("does not match the plan", result["checks"][0]["message"])

    def test_failed_execution_retains_the_partial_notebook(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "failure.ipynb"
            executed = root / "executed.ipynb"
            nbformat.write(
                nbformat.v4.new_notebook(
                    cells=[nbformat.v4.new_code_cell("raise RuntimeError('defect')")]
                ),
                source,
            )

            with self.assertRaises(CellExecutionError):
                execute_notebook(source, 60, [], executed)

            retained = nbformat.read(executed, as_version=4)

        self.assertIn("RuntimeError", retained.cells[0].outputs[0]["ename"])

    def test_timeout_limits_the_whole_notebook_and_retains_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "slow.ipynb"
            executed = root / "executed.ipynb"
            nbformat.write(
                nbformat.v4.new_notebook(
                    cells=[
                        nbformat.v4.new_code_cell(
                            "import time\ntime.sleep(2)\nprint('too late')"
                        )
                    ]
                ),
                source,
            )

            with self.assertRaisesRegex(
                NotebookTimeoutError, "total execution timeout"
            ):
                execute_notebook(source, 1, [], executed)

            self.assertTrue(executed.is_file())


class ArtifactAndPathTests(unittest.TestCase):
    def test_output_refresh_uses_only_manifest_notebooks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source-code"
            source.mkdir()
            (source / "classified.ipynb").touch()
            (source / "unclassified.ipynb").touch()
            manifest = root / "manifest.toml"
            manifest.write_text(
                "[[notebooks]]\n"
                "path = 'source-code/classified.ipynb'\n"
                "[notebooks.properties]\n"
                "output_policy = 'strip'\n"
            )

            specs = load_notebook_specs(root, manifest)

        self.assertEqual(
            [spec.path.relative_to(root).as_posix() for spec in specs],
            ["source-code/classified.ipynb"],
        )
        self.assertEqual([spec.output_policy for spec in specs], ["strip"])

    def test_png_validator_checks_structure_and_checksum(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "figure.png"
            path.write_bytes(_one_pixel_png())
            validate_png(path, 1)
            damaged = bytearray(path.read_bytes())
            damaged[-5] ^= 1
            path.write_bytes(damaged)
            with self.assertRaisesRegex(ValidationError, "checksum"):
                validate_png(path, 1)

    def test_relative_path_cannot_escape_root(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            self.assertRaisesRegex(ValidationError, "unsafe relative path"),
        ):
            safe_relative_path(Path(directory), "../outside")


if __name__ == "__main__":
    unittest.main()
