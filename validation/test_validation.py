from __future__ import annotations

import struct
import tempfile
import unittest
import zlib
from pathlib import Path

import nbformat
from nbclient.exceptions import CellExecutionError

from validation.assertions import parse_assertion_records
from validation.run_validation import (
    NotebookTimeoutError,
    ValidationError,
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
