# Scientific Python training revision TODO

## Goal

Refocus the training on the core libraries and workflows that Python
programmers need for scientific computing.  The emphasis should be on choosing
and using tools effectively, while retaining enough numerical concepts to use
those tools correctly.

The four-hour version should remain a focused overview.  A six-hour workshop
version can add hands-on practice and depth without introducing many more
libraries.

## Status audit (2026-10-07)

This checklist was re-audited against the current `development` branch, using
commit `65f59e7` (which added this file) as the baseline.  Checked items below
are satisfied by the current materials.  Unchecked items may be wholly
unaddressed or only partially addressed; the latter are called out here so
that completed work is not lost and remaining work is not understated.

### Confirmed progress

- Removed uses of the removed scalar aliases `np.int`, `np.float`,
  `np.complex`, and `np.bool` from the current slides and sources.
- Added `default_rng` and reproducible seeding to the main slide deck, and
  modernized selected examples.  A repository-wide conversion is not yet
  complete.
- Modernized the core ODE examples and slides to use `solve_ivp`.
- Linked the expanded broadcasting notebook from the main deck; the notebook
  now covers broadcasting rules, diagnosis, memory use, and performance
  pitfalls.
- Added explicit teaching material for aggregation axes, views versus copies,
  and NumPy linear algebra, including `solve`, least squares, and numerical
  comparisons.
- Modernized the histogram and principal 3D surface-plot examples.
- The SymPy pendulum material now demonstrates `lambdify`, a symbolic
  Jacobian, and its use with a SciPy solver.

### Remaining issues found during the audit

- `source-code/vpython/pendulum.ipynb` still uses
  `scipy.integrate.ode`; `source-code/birdsong/analyse.py` still calls
  `sp.fft(...)`; and `source-code/numpy/target_function_plot.py` still uses
  `figure.gca(projection="3d")`.
- Legacy global `np.random.*` calls remain in exercises, notebooks, and
  scripts.  Some are harmless for throwaway data, but examples that teach
  reproducibility or serve as models for new code should use a `Generator`.
- The dtype slide now warns that extended precision is not portable, but
  `source-code/numpy/numpy_datatypes.ipynb` still presents `np.float96` as if
  it were generally available.
- Slide 22 contains `np.arrange(24)` instead of `np.arange(24)`.
- Stored error or interrupt output remains in
  `source-code/sympy/triple_six_puzzle.ipynb`,
  `source-code/sympy/griffith_chapter_01.ipynb`, and
  `source-code/diffusion_limited_aggregation.ipynb`.  Several other notebooks
  contain unexecuted code cells without a documented output policy.
- The Bokeh README still says its notebooks do not work in JupyterLab, while
  the repository's preferred command launches JupyterLab.  This needs a
  current, tested statement rather than an environment assumption.
- The live course structure is still the old one: xarray is absent from the
  schedule and deck, while PyTables, Bokeh, and image/video processing remain
  in the core path.
- `docs/README.md` labels the course as 240 minutes but its schedule sums to
  245 minutes.  `training.toml` sums to 240 minutes by assigning 5 rather than
  10 minutes to the wrap-up.  These sources must be reconciled when the revised
  schedule is adopted.

## Agreed scope boundaries

- Scientific Python should own:
  - NumPy arrays and numerical computation;
  - SciPy numerical algorithms;
  - core Matplotlib visualization;
  - SymPy and symbolic-to-numerical workflows;
  - xarray and labeled multidimensional scientific data;
  - basic scientific data-format selection and serial h5py usage;
  - numerical reliability and reproducibility.
- Refer participants to **Python for Data Science** for pandas, Polars,
  statistical/exploratory visualization, databases, web data, and GIS.
- Refer participants to **Python for HPC** for profiling, Numba, Cython,
  compiled-language interoperability, parallel execution, and computing at
  scale.
- Refer participants to **Machine Learning with Python** for scikit-learn and
  machine-learning workflows.
- GPU-oriented libraries and parallel execution remain out of scope.
- Bokeh, PyTables, OpenCV/video processing, VPython, and Manim should be
  optional or specialist material rather than part of the core four-hour path.

## Priority 0: modernize and validate existing material

- [x] Replace removed NumPy aliases such as `np.int`, `np.float`,
  `np.complex`, and `np.bool` in the slides, notebooks, and scripts.
- [ ] Review dtype examples for portability, especially extended-precision
  types on supported Linux, macOS, and Windows platforms.
- [ ] Replace legacy global `np.random.*` examples with
  `np.random.default_rng()` where reproducibility or new code is being taught.
- [ ] Replace `scipy.integrate.ode` examples with `scipy.integrate.solve_ivp`.
- [ ] Replace calls such as `sp.fft(signal)` with the modern
  `scipy.fft.fft(signal)` API.
- [ ] Update the signal-filtering example to use second-order sections where
  appropriate, e.g. `output="sos"` and `sosfiltfilt`.
- [ ] Replace obsolete Matplotlib usage, including `hist(..., normed=...)` and
  `figure.gca(projection="3d")`.
- [ ] Check all slide code fragments for syntax errors, misspelled names, and
  inconsistencies with the corresponding source files.
- [ ] Re-execute every instructional notebook from a clean kernel in its
  documented environment.
- [ ] Remove stored exceptions and `KeyboardInterrupt` outputs from notebooks
  intended for participants.
- [ ] Clearly label deliberately unexecuted exercise notebooks; otherwise ship
  notebooks with a clean, sequential execution state.
- [ ] Resolve the Bokeh/JupyterLab setup inconsistency if Bokeh remains in the
  distributed optional material.

## Priority 1: rebalance the four-hour core

Use the following schedule as the target, including the break:

| Topic | Time |
|---|---:|
| Introduction and ecosystem/course boundaries | 5 min |
| NumPy | 65 min |
| SciPy | 45 min |
| Break | 10 min |
| Matplotlib | 30 min |
| SymPy and the symbolic-to-numerical bridge | 20 min |
| xarray and scientific data-format choices | 25 min |
| h5py fundamentals | 15 min |
| Integrated hands-on exercise | 15 min |
| Wrap-up and pointers to related trainings | 10 min |
| **Total** | **240 min** |

- [ ] Update `docs/README.md` with the revised schedule and learning outcomes.
- [ ] Restructure `scientific_python.pptx` to match the revised teaching path.
- [ ] Add an early “which tool should I use?” overview covering Python
  containers, NumPy, pandas, xarray, SciPy, and SymPy without teaching pandas.
- [ ] Add a final course-navigation slide pointing to the data-science, HPC,
  machine-learning, GPU, and parallel-computing trainings.
- [ ] Remove PyTables from the core presentation.
- [ ] Move detailed Bokeh and image/video-processing material to optional
  sections or separate modules.

## NumPy coverage

- [x] Retain array creation, shapes, dtypes, indexing, slicing, vectorized
  operations, and views versus copies.
- [x] Promote broadcasting from the optional notebook material into the main
  teaching path.
- [x] Teach reductions and the meaning of `axis` explicitly.
- [ ] Cover reshaping, stacking, and concatenation using practical examples.
- [x] Explain when basic slicing returns a view and when advanced/Boolean
  indexing creates a copy.
- [x] Introduce reproducible random generation with `default_rng`.
- [x] Add numerical-comparison examples with `isclose` and `allclose`.
- [ ] Cover integer overflow, floating-point precision, NaNs, and dtype choices
  at a practical level.
- [ ] Teach `solve` and least-squares before explicit matrix inversion.
- [ ] Temper the “never use vanilla Python” message: Python should orchestrate
  computations, while bulk numerical work should use compiled array/library
  operations.
- [ ] Explain the performance and memory costs of temporary arrays and when
  vectorization is not a good fit; refer deeper optimization work to Python for
  HPC.

## SciPy coverage

- [ ] Expand the section beyond SVD, basic regression, one optimizer, an ODE,
  and signal filtering.
- [ ] Add concise examples of:
  - [ ] numerical quadrature with `integrate.quad`;
  - [ ] scalar and multidimensional root finding;
  - [ ] interpolation;
  - [ ] `minimize`, `least_squares`, and `curve_fit`;
  - [x] ODE integration with `solve_ivp`;
  - [ ] statistical distributions and selected hypothesis tests;
  - [ ] sparse arrays and sparse solvers;
  - [ ] selected special functions.
- [ ] Teach how to inspect SciPy result objects, convergence status, warnings,
  and error estimates.
- [ ] Include a scientific fitting example with weighted observations,
  parameter covariance, residuals, and uncertainty estimates.
- [ ] Clarify the difference between scientific parameter estimation and the
  predictive regression workflows taught in Machine Learning with Python.

## Matplotlib coverage

- [ ] Teach the object-oriented pattern using `fig, ax = plt.subplots()` as the
  default interface.
- [ ] Add subplots, shared axes, legends, and constrained layout.
- [ ] Add error bars and uncertainty bands.
- [ ] Cover logarithmic scales and appropriate limits.
- [ ] Explain color maps and normalization for sequential, diverging, and
  categorical data.
- [ ] Demonstrate publication-quality raster and vector export.
- [ ] Prefer these broadly useful topics over detailed 3D plotting.
- [ ] Keep statistical and interactive visualization libraries in Python for
  Data Science, with cross-references where useful.

## SymPy coverage

- [x] Retain symbols, assumptions, equation solving, differentiation,
  integration, simplification, and basic matrix operations.
- [ ] Explain the distinction between exact and floating-point input.
- [x] Add `lambdify` to convert symbolic expressions into NumPy-callable
  functions.
- [x] Demonstrate passing a symbolic derivative or Jacobian to a SciPy solver.
- [ ] Move expression-tree internals to optional/advanced material if time is
  needed elsewhere.

## xarray and scientific data formats

- [ ] Promote `source-code/xarray/xarray_intro.ipynb` into the live teaching
  path, reducing it to a concise core version if necessary.
- [ ] Cover `DataArray`, `Dataset`, named dimensions, coordinates, attributes,
  and label-based selection.
- [ ] Demonstrate reductions and grouping by named dimension.
- [ ] Show how xarray interoperates with NumPy and Matplotlib.
- [ ] Include a small NetCDF read/write example.
- [ ] Add a practical format-selection guide:
  - tables: CSV or Parquet, covered further in Python for Data Science;
  - simple NumPy arrays: `.npy` or `.npz`;
  - labeled multidimensional scientific data: xarray and NetCDF;
  - hierarchical binary data: HDF5/h5py.

## h5py coverage

- [ ] Reduce HDF5 from a 40-minute dual-API section to approximately 15 minutes
  of h5py fundamentals.
- [ ] Cover context managers, groups, datasets, attributes, and slicing.
- [ ] Briefly explain chunking, compression, and extensible datasets without
  turning the section into an I/O-performance lecture.
- [ ] Refer large-data, performance, and parallel-HDF5 topics to Python for HPC.
- [ ] Keep PyTables examples available only as optional legacy/specialist
  material, or remove them if they no longer serve a clear audience.

## Hands-on material and exercises

- [ ] Create one short, integrated core exercise that follows this workflow:

  ```text
  load scientific data
  -> inspect shape, dtype, coordinates, and metadata
  -> select or transform the data
  -> fit, optimize, or solve with SciPy
  -> inspect errors and residuals
  -> create a publication-quality Matplotlib figure
  -> save a structured result
  ```

- [ ] Ensure every core learning outcome has at least one approachable
  exercise, not only a slide example.
- [ ] Add short exercises for Matplotlib, xarray, h5py, fitting, and
  uncertainty.
- [ ] Separate notebooks into clearly documented groups:
  1. core guided labs;
  2. optional library demonstrations;
  3. extended scientific applications.
- [ ] Prefer small, tool-oriented exercises in the core over examples that
  require substantial understanding of Ising models, diffusion-limited
  aggregation, chaos, or dynamic programming.
- [ ] Retain the richer scientific applications as optional projects and
  examples of how the tools combine.
- [ ] Add expected runtimes and environment names to notebooks that are slow or
  require optional dependencies.

## Optional six-hour workshop

Keep the four-hour course as the focused overview.  Offer an additional
two-hour block when the goal is practical competence:

| Additional activity | Time |
|---|---:|
| Extended integrated scientific workflow exercise | 45 min |
| SciPy fitting, uncertainty, and diagnostics | 30 min |
| xarray/NetCDF hands-on exercise | 25 min |
| Numerical reliability and reproducibility | 15 min |
| Review | 5 min |
| **Additional time** | **120 min** |

- [ ] Prepare the extended integrated exercise with starter and completed
  versions.
- [ ] Decide whether to offer the extension as a continuous six-hour workshop
  or as two shorter sessions; prefer two sessions when scheduling permits.
- [ ] Keep optional tracks modular so they can be selected for a particular
  audience:
  - numerical methods with SciPy;
  - scientific data with xarray, NetCDF, h5py, metadata, and units;
  - scientific visualization;
  - symbolic-to-numerical workflows;
  - image analysis with scikit-image/OpenCV.
- [ ] Consider a brief Pint/physical-units example in the scientific-data
  track; do not make it a core dependency without a concrete use case.

## Documentation and quality assurance

- [ ] Update `README.md`, `source-code/README.md`, and topic READMEs so the core
  and optional paths are immediately visible.
- [ ] Document the relationships and expected prerequisites among the
  Scientific Python, Python for Data Science, Python for HPC, Machine Learning
  with Python, GPU, and parallel-computing trainings.
- [ ] Ensure the default environment contains everything required by the core
  path; keep specialist dependencies in named optional environments.
- [ ] Add a repeatable notebook-validation procedure that executes core
  notebooks from clean kernels.
- [ ] Run the complete core path on every supported platform or document any
  platform-specific exclusions.
- [ ] Perform a final slide-to-notebook-to-environment consistency check before
  releasing the revised training.

## Completion criteria

- [ ] The four-hour schedule totals exactly four hours including its break.
- [ ] Every core library has a stated learning outcome and at least one exercise.
- [ ] All core examples run with the documented environment and current APIs.
- [ ] Participants can identify when to use NumPy, SciPy, SymPy, Matplotlib,
  xarray, and h5py.
- [ ] The material clearly redirects pandas, Numba, scikit-learn, GPU, and
  parallel-computing topics to the appropriate related trainings.
- [ ] Optional material is clearly separated and does not obscure the core
  learning path.
