# Master-Level Exercises

These exercises are based on the Jupyter notebooks in this repository, together with the material in the `matrices`, `numpy`, and `sympy` directories. The intended audience is Master students in Physics, Chemistry, Mathematics, and Engineering.

Effort estimates are approximate and assume that students are already comfortable with Python, NumPy, plotting, and basic scientific computing.

This sheet is intended for longer assignments or mini-projects. For shorter in-class or tutorial work based on the same material, see `short_exercises.md`.

## 1. Blocked matrix multiplication and performance analysis

Implement blocked matrix multiplication in NumPy and compare it to naive Python and `np.dot`.

- Estimated effort: 4-6 hours
- Optional hints:
  - Start from the scripts in `matrices/`.
  - Benchmark across several matrix sizes.
  - Interpret the results using cache locality, BLAS usage, and arithmetic intensity.

## 2. Loop ordering in dense matrix multiplication

Measure the impact of loop ordering on dense matrix multiplication in pure Python, C, and Fortran. Implement at least two loop nest orderings such as `ijk`, `ikj`, and `kij`, benchmark them over increasing matrix sizes, and explain the results in terms of memory layout, cache reuse, and language/runtime overhead.

- Estimated effort: 4-6 hours
- Optional hints:
  - Compare row-major and column-major effects carefully.
  - Keep the mathematical operation fixed while varying only the loop structure.
  - Plot runtime versus matrix dimension on linear and log scales.

## 3. Stability study for the 2D heat equation

Solve the 2D heat equation with an explicit finite-difference scheme and determine the CFL stability limit experimentally. Perform a convergence study against an analytical separable solution.

- Estimated effort: 5-7 hours
- Optional hints:
  - Use `numpy/diffusion.ipynb` as a starting point.
  - Check both qualitative blow-up behavior and quantitative error norms.
  - Compare at least two grid resolutions.

## 4. Anisotropic diffusion

Extend the heat-equation notebook to anisotropic diffusion with different diffusivities in the `x` and `y` directions. Interpret the physical meaning and discuss when a rotated diffusion tensor would require a different discretization strategy.

- Estimated effort: 4-6 hours
- Optional hints:
  - Begin with diagonal anisotropy before considering mixed derivatives.
  - Visualize isotherms to show directional effects.
  - Relate the model to transport in layered or crystalline media.

## 5. Spectral versus finite-difference diffusion solver

Build a spectral solver for the diffusion equation using FFTs and compare it against the finite-difference method. Quantify accuracy, runtime, and the limitations imposed by boundary conditions.

- Estimated effort: 6-8 hours
- Optional hints:
  - Periodic boundaries are the natural starting point for FFT methods.
  - Compare wall-clock time and error for the same initial condition.
  - Discuss when an FFT-based solver is a poor fit.

## 6. Bifurcation diagram and Feigenbaum scaling

For the logistic map, compute a bifurcation diagram and estimate the Feigenbaum ratio from successive period doublings. Comment on numerical sensitivity and finite-resolution effects.

- Estimated effort: 4-5 hours
- Optional hints:
  - Use `numpy/logistic_map.ipynb`.
  - Discard transients before estimating asymptotic behavior.
  - Track period-doubling points consistently across runs.

## 7. Largest Lyapunov exponent of the logistic map

Compute the largest Lyapunov exponent of the logistic map as a function of `r`. Use it to classify parameter regions and compare with the visual structure in the bifurcation or heatmap plots.

- Estimated effort: 4-6 hours
- Optional hints:
  - Use the tangent-map formula rather than finite-difference perturbations if possible.
  - Average over sufficiently long trajectories.
  - Mark regions with negative, zero, and positive exponents.

## 8. Spectral leakage and windowing

Reconstruct noisy multitone signals from the FFT notebook and study spectral leakage. Compare rectangular, Hann, and Blackman windows quantitatively.

- Estimated effort: 4-6 hours
- Optional hints:
  - Use peak widths and amplitude errors as comparison metrics.
  - Keep sampling frequency and record length explicit.
  - Test both commensurate and incommensurate frequencies.

## 9. Aliasing and sampling design

Design a sampling strategy that avoids aliasing for a target band-limited signal, then deliberately undersample it and identify the aliased frequencies. Explain the results using the Nyquist criterion.

- Estimated effort: 3-5 hours
- Optional hints:
  - Start from a simple sum of sinusoids.
  - Predict the aliased frequencies analytically before computing them.
  - Show the time-domain and frequency-domain views side by side.

## 10. Broadcasting as a replacement for loops

Reimplement one slow image or array-processing pattern from the broadcasting notebook using broadcasting only. Report both speedups and memory tradeoffs.

- Estimated effort: 3-5 hours
- Optional hints:
  - Use `numpy/broadcast.ipynb`.
  - Verify that the vectorized result is numerically identical to the loop-based version.
  - Temporary arrays may dominate memory usage even when runtime improves.

## 11. When NumPy helps and when it does not

Compare pure Python loops, naive NumPy loops, vectorized NumPy, and `numpy.vectorize()` on the Julia-set style workload from `numpy/to_numpy_or_not_to_numpy.ipynb`. Explain why some apparently NumPy-based code is still slow.

- Estimated effort: 4-5 hours
- Optional hints:
  - Distinguish clearly between Python-level loops and array-level operations.
  - Benchmark repeated runs, not just a single execution.
  - Include a brief discussion of interpreter overhead and temporary allocations.

## 12. Statistical study of the Game of Life

Extend the Game of Life notebook with periodic boundary conditions and measure the lifetime distribution of random initial states. Perform a statistical analysis over many seeds and grid sizes.

- Estimated effort: 5-7 hours
- Optional hints:
  - Use summary statistics, not only example runs.
  - Define carefully what counts as termination or recurrence.
  - Consider whether finite-size scaling appears in the data.

## 13. Estimating the critical temperature in the Ising model

Using the Ising model notebook, estimate the critical temperature from magnetization, susceptibility, or heat capacity. Compare Glauber and Metropolis-Hastings dynamics and discuss finite-size effects.

- Estimated effort: 6-8 hours
- Optional hints:
  - Use ensemble averages after equilibration.
  - Compare at least two lattice sizes.
  - Expect the apparent critical point to shift with system size.

## 14. Autocorrelation and equilibration in Monte Carlo simulation

Add autocorrelation-time estimation to the Ising simulation and use it to define an evidence-based equilibration criterion. Treat this as a Monte Carlo methodology exercise rather than only a simulation task.

- Estimated effort: 5-7 hours
- Optional hints:
  - Record time series of energy or magnetization.
  - Compare naive averaging to block-averaged estimates.
  - Explain why correlated samples reduce the effective sample size.

## 15. Fractal dimension in diffusion-limited aggregation

For diffusion-limited aggregation, estimate the fractal dimension of the cluster using a box-counting method. Test the sensitivity to seed geometry, particle count, and lattice size.

- Estimated effort: 5-7 hours
- Optional hints:
  - Use several box sizes and justify the fitting range.
  - Compare single-seed and multi-seed growth.
  - Report uncertainty in the fitted slope.

## 16. Symbolic derivation and numerical generation for the double pendulum

Use SymPy to derive the Euler-Lagrange equations for a double pendulum, then generate numerical right-hand sides automatically and compare them with a hand-derived implementation.

- Estimated effort: 6-8 hours
- Optional hints:
  - Start from `sympy/pendulums.ipynb`.
  - Simplify expressions before converting them to numerical functions.
  - Compare trajectories over short and moderate times, not only at one instant.

## 17. Normal modes of coupled pendulums

Starting from the pendulum material in `sympy/pendulums.ipynb` and `numpy/coupled_pendulums.py`, derive the small-angle normal modes of two coupled pendulums symbolically. Compare modal predictions against numerical time integration for increasing amplitudes.

- Estimated effort: 5-7 hours
- Optional hints:
  - Linearize first, then solve the eigenvalue problem.
  - Use symmetric and antisymmetric initial conditions as diagnostic tests.
  - Quantify when the linear approximation begins to fail.

## 18. Parameter-dependent eigenvalue problems

Use SymPy linear algebra to diagonalize a parameter-dependent matrix and identify parameter values where eigenvalue degeneracy occurs. Explain what becomes numerically delicate near defective or nearly defective cases.

- Estimated effort: 4-6 hours
- Optional hints:
  - Use `sympy/sympy.ipynb` for symbolic matrix operations.
  - Track both eigenvalues and eigenvectors as the parameter varies.
  - Distinguish exact degeneracy from near-degeneracy.

## 19. Symbolic quantum-mechanics calculations

From `sympy/griffith_chapter_01.ipynb`, formulate a symbolic quantum-mechanics problem: normalize a wavefunction, compute expectation values, and verify uncertainty relations numerically for selected parameters.

- Estimated effort: 4-6 hours
- Optional hints:
  - Keep the symbolic derivation and numerical evaluation clearly separated.
  - Check dimensions and normalization carefully.
  - A Gaussian wave packet is a good baseline test case.

## 20. Dynamic programming for scientific data comparison

Turn the string-alignment notebook into a scientific-data exercise by aligning two symbolic or molecular strings with custom scoring. Justify the recurrence relation, analyze computational complexity, and propose a vectorized or memory-reduced implementation.

- Estimated effort: 4-6 hours
- Optional hints:
  - Use `numpy/dynamic_programming.ipynb`.
  - Separate the scoring model from the dynamic-programming engine.
  - Compare full-table storage with reduced-memory variants.
