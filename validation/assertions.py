"""Target-owned post-execution assertions for selected training notebooks."""

from __future__ import annotations

import json

RESULT_PREFIX = "__SCIENTIFIC_PYTHON_VALIDATION__="

_ASSERTION_EXPRESSIONS = {
    "root-residuals": """
_residual_norms = [float(np.linalg.norm(_result.fun)) for _result in results]
_maximum_residual = max(_residual_norms)
_threshold = 1.0e-8
_validation_records.append({
    "name": "root-residuals",
    "outcome": "pass" if _maximum_residual < _threshold else "fail",
    "message": (
        f"maximum residual norm {_maximum_residual:.3e}; "
        f"required < {_threshold:.1e}"
    ),
})
""",
    "pendulum-route-agreement": """
_maximum_discrepancy = float(np.max(relative_discrepancies))
_threshold = 1.0e-8
_validation_records.append({
    "name": "pendulum-route-agreement",
    "outcome": "pass" if _maximum_discrepancy < _threshold else "fail",
    "message": (
        f"maximum relative ODE/quadrature discrepancy "
        f"{_maximum_discrepancy:.3e}; required < {_threshold:.1e}"
    ),
})
""",
}


def assertion_cell(names: list[str]) -> str | None:
    """Return one cell that records assertions without masking their values."""

    if not names:
        return None
    unknown = sorted(set(names) - set(_ASSERTION_EXPRESSIONS))
    if unknown:
        raise ValueError(f"unknown assertion: {', '.join(unknown)}")
    body = ["import json as _validation_json", "_validation_records = []"]
    body.extend(_ASSERTION_EXPRESSIONS[name] for name in names)
    body.append(
        f"print({RESULT_PREFIX!r} + _validation_json.dumps(_validation_records))"
    )
    return "\n".join(body)


def parse_assertion_records(notebook, names: list[str]) -> list[dict[str, str]]:
    """Extract exactly one result record for every configured assertion."""

    if not names:
        return []
    records: list[dict[str, str]] = []
    for output in notebook.cells[-1].get("outputs", []):
        if output.get("output_type") != "stream":
            continue
        for line in output.get("text", "").splitlines():
            if line.startswith(RESULT_PREFIX):
                records.extend(json.loads(line.removeprefix(RESULT_PREFIX)))
    observed_names = [record.get("name") for record in records]
    if observed_names != names:
        raise RuntimeError(
            "assertion result names do not match configuration: "
            f"expected {names}, observed {observed_names}"
        )
    return records
