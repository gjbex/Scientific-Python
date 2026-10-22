# Notebook validation pilot

This directory contains the Scientific Python–owned execution policy layered on
top of the reviewed notebook classifications in `manifest.toml`. The shared
`notebook-classifier` in Training-sessions owns plan and result semantics; this
repository owns environments, timeouts, notebook execution, scientific
assertions, generated-artifact checks, budgets, and CI policy.

Only Linux is supported, including Linux under WSL. Notebook source and its
committed outputs are never rewritten: every execution uses a temporary copy,
sets Matplotlib's backend to `Agg`, and stores evidence outside the checkout.

## Local commands

Run the contract tests first:

```bash
pixi run --locked validation-contract
```

Run the four-notebook pilot selected in `VALIDATION_DESIGN.md`:

```bash
pixi run --locked validation-smoke
```

Run all 19 notebooks classified as `required`, grouped into their declared
`default`, `hdf5`, and `xarray` Pixi environments:

```bash
pixi run --locked validation-required
```

By default the runner creates a fresh directory under `/tmp` and prints its
location. Pass `--output-directory /absolute/new/path` after the task name when
a stable location is needed. The directory contains the exact plan, result
document, JSON assessment, Markdown and JSON summaries, run metrics, logs,
executed notebook copies, and declared generated artifacts.

The runner needs version 0.3 or later of the Training-sessions classifier. It
uses `NOTEBOOK_CLASSIFIER_ROOT` when set, otherwise tries the normal sibling
checkout `../Training-sessions/tools/notebook-classifier`, and finally an
installed `notebook-classifier` executable. The plan is a run artifact rather
than a committed file: embedding the repository commit in a plan committed to
that same commit would create an impossible self-reference.

## What is checked

Every selected notebook must finish within its explicit timeout. Successful
kernel exit is reported as `notebook_execution`; it is not described as proof
that the teaching or science is correct.

Two target-owned numerical checks are appended only to the temporary notebook:

- `root-residuals` requires the maximum Euclidean residual norm of the two
  successful circle–parabola solves to be below `1e-8`. The notebook itself
  classifies roots with that residual threshold, so this checks the scientific
  acceptance criterion rather than exact solver internals.
- `pendulum-route-agreement` requires the largest relative discrepancy between
  ODE-event and quadrature period estimates to be below `1e-8`. The ODE uses
  `rtol=1e-10` and `atol=1e-12`, while quadrature requests `1e-12`; the looser
  cross-method bound accommodates accumulated event-location and integration
  error without accepting a visibly different period.

`multiple_plots.ipynb` must generate a PNG of at least 1000 bytes. The runner
checks the PNG signature, required chunks, positive dimensions, chunk bounds,
and CRCs before retaining it. This is an artifact-integrity smoke check, not a
visual or pedagogical assessment of the plot.

The contract test creates a defective temporary notebook whose ODE/quadrature
discrepancy is `1e-3` and verifies that the numerical check reports `fail`.
Neither the source notebook nor a tracked fixture is mutated.

Failed executions retain the partially executed notebook and a per-notebook
log in the external evidence directory. This is intentional: a failure must
remain diagnosable without writing outputs back into instructional material.

## Current pilot result

The 2026-10-21 required-profile pilot accounted for all 47 manifest entries
and attempted all 19 required notebooks. Fifteen passed and four produced
actionable execution errors:

- `source-code-numpy-fft-experiments` declares an unavailable historical
  `conda-env-py35-py` kernel;
- `source-code-numpy-io-performance` is assigned to `default` but imports
  `h5py`;
- `source-code-numpy-numpy-linear-algebra` refers to undefined name `y`;
- `source-code-xarray-xarray-intro` uses pandas frequency `6H`, which the
  locked pandas version rejects in favour of `6h`.

These findings are not suppressed or reclassified as passes. Fixing notebook
content or changing a reviewed manifest environment is a separate maintainer
decision. The run completed in 463.726 seconds, below the provisional
720-second budget. The four-notebook smoke profile passed in 29.135 seconds.

## Profiles and maintenance

`execution.toml` refers to notebooks only by stable manifest ID. Paths and
environment names come from the generated plan. Consequently, a pure notebook
move requires a manifest path/blob update but no execution-registry path edit.
The `smoke` profile selects four IDs; the `required` profile accounts for all
19 reviewed required IDs. Missing results, stale blobs, environment setup
errors, worker interruption, failed assertions, and invalid artifacts have
distinct non-passing states.

The workflow under `ci/` is deliberately not active yet. It is manual plus
monthly, has read-only permissions, and runs repository-owned Pixi tasks. Move
it to `.github/workflows` only after the current Training-sessions tool is
committed and its checkout and external actions are pinned to reviewed commit
hashes. No ordinary pull-request trigger should be added.

The delivery tag `20261023` is not present yet. A baseline plan, results, and
report can only be frozen for that tag after it exists; do not represent a run
of the evolving branch as delivery-tag evidence.
