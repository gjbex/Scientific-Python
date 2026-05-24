# Short Exercises

These exercises are based on the same notebooks and directories as the longer exercise sheet, but are scoped to take approximately 30 minutes each. The emphasis is on a single concept, a short implementation step, and a brief interpretation.

This sheet is intended for tutorials, short labs, or preparatory work. Several of these problems can be used as stepping stones toward the longer assignments collected in `exercises_challenging.md`. For an overview of all exercise sheets, see `exercises.md`.

## 1. Empirical scaling of matrix multiplication

In `matrices/numpy_matmul.py`, time `np.dot(A, B)` for three matrix sizes and estimate the empirical scaling exponent from a log-log plot.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Choose matrix sizes that differ by a factor of about 2.
  - Plot `log(time)` versus `log(n)`.
  - Compare the slope with the theoretical cubic scaling.

## 2. Checking a matrix product by hand

In the pure Python matrix-multiplication code, replace random initialization by a constant matrix and verify the product against a hand-computed `2 x 2` example.

- Estimated effort: 15-25 minutes
- Optional hints:
  - Use very small matrices first.
  - Compute one entry of the product explicitly on paper.
  - Make sure the code and the manual calculation use the same convention.

## 3. Sensitivity to time step in the heat equation

In the heat-equation notebook, halve the time step while keeping the grid fixed and compare the final temperature field visually and with an `L2` difference.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Use the same initial condition in both runs.
  - Compare the final states at the same physical time.
  - A small difference does not necessarily imply full convergence.

## 4. Changing the initial condition in diffusion

In the heat-equation notebook, change the initial condition from a hot square to a hot Gaussian and describe how the transient evolution differs.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Keep the domain and time step unchanged.
  - Compare symmetry and smoothness during the evolution.
  - A Gaussian is already smooth, unlike the sharp-edged square.

## 5. Nearby trajectories in the logistic map

In `numpy/logistic_map.ipynb`, compute trajectories for two nearby initial conditions at one chaotic value of `r` and one non-chaotic value, then compare the divergence.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Pick one `r` in the stable regime and one in the chaotic regime.
  - Plot the absolute difference versus iteration number.
  - Use the same initial separation in both cases.

## 6. Fixed point or periodic orbit?

In the logistic-map notebook, determine numerically whether a given `r` value leads to a fixed point, a period-2 orbit, or more complicated behavior.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Discard transient iterations first.
  - Compare the last several values of the trajectory.
  - Use a small numerical tolerance when testing equality.

## 7. Identifying frequencies with the FFT

In `numpy/fft_experiments.ipynb`, generate a signal with two cosines and identify their frequencies from the power spectrum.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Start with frequencies that align with the sampling grid.
  - Use the positive-frequency half of the spectrum.
  - Check whether the largest peaks match the input frequencies.

## 8. Noise and spectral peaks

Add Gaussian noise to the FFT signal and determine how the dominant peaks change as the noise amplitude increases.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Keep the clean signal fixed and vary only the noise level.
  - Compare peak heights and visibility.
  - A small table of results is enough.

## 9. Replacing loops by broadcasting

In the broadcasting notebook, replace a simple nested-loop array scaling operation by a broadcasting-based expression and verify equality.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Start from a case with one array and one 1D scaling factor.
  - Check shapes before writing the final expression.
  - Use `np.allclose` to verify the result.

## 10. Slicing a 2D array

In `numpy/indexing_arrays.ipynb`, extract every second row and the last three columns of a 2D array without using loops.

- Estimated effort: 10-20 minutes
- Optional hints:
  - Use slice notation only.
  - Print the shape of the extracted array.
  - Check one example by hand.

## 11. Reshape versus copy

In `numpy/numpy.ipynb`, reshape a 1D array into a matrix and explain the difference between `reshape`, slicing, and copying for one concrete example.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Modify one element after reshaping.
  - Check whether the original array changes.
  - Use `np.shares_memory` if helpful.

## 12. Working with structured arrays

In `numpy/structured_arrays.ipynb`, create a small structured array with fields such as `mass` and `charge`, then sort by one field.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Use three to five entries only.
  - Print the array before and after sorting.
  - Check that field access works by name.

## 13. Comparing NumPy data types

In `numpy/numpy_datatypes.ipynb`, compare the memory usage of the same array stored as `float64` and `float32`.

- Estimated effort: 15-25 minutes
- Optional hints:
  - Use the same shape and values.
  - Compare `itemsize` and total bytes.
  - Briefly comment on the precision-memory tradeoff.

## 14. A period-2 oscillator in the Game of Life

In the Game of Life notebook, initialize a blinker and verify that the period is 2.

- Estimated effort: 15-25 minutes
- Optional hints:
  - Start from a very small grid.
  - Save the world at successive time steps.
  - Check when the initial pattern reappears.

## 15. Magnetization of simple Ising configurations

In the Ising notebook, compute magnetization for one random configuration and one fully aligned configuration, then explain the sign and magnitude.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Use spins `+1` and `-1`.
  - Normalize by the number of lattice sites.
  - A fully aligned state should give the extremal value.

## 16. Variability in diffusion-limited aggregation

In the diffusion-limited aggregation notebook, run a very small simulation twice with different seeds and compare the resulting cluster shapes.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Keep grid size and particle count fixed.
  - Use a small system so the run is quick.
  - Focus on qualitative differences between the two clusters.

## 17. Solving a symbolic linear system

In `sympy/sympy.ipynb`, solve a `2 x 2` linear system symbolically and verify the result by substitution.

- Estimated effort: 15-25 minutes
- Optional hints:
  - Use symbolic coefficients or a simple numerical example.
  - Substitute the solution back into both equations.
  - Compare symbolic and numerical evaluation.

## 18. Checking an eigenvalue-eigenvector pair

In the SymPy notebook, compute eigenvalues and eigenvectors of a simple `2 x 2` matrix and check the eigenvector relation explicitly.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Choose a matrix with real eigenvalues first.
  - Compute `A v` and `lambda v` separately.
  - Compare the two expressions exactly or numerically.

## 19. Small-angle pendulum equation

In `sympy/pendulums.ipynb`, derive the small-angle equation of motion for a simple pendulum and compare it with the full nonlinear equation.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Use `sin(theta) ~ theta` for small angles.
  - Identify the resulting equation as a harmonic oscillator.
  - State when the approximation is expected to fail.

## 20. Short string alignment by dynamic programming

In `numpy/dynamic_programming.ipynb`, fill in the alignment table for two very short strings and recover one optimal alignment by backtracking.

- Estimated effort: 20-30 minutes
- Optional hints:
  - Use strings of length 3 or 4.
  - Keep the scoring system simple.
  - Mark the predecessor direction in each cell while filling the table.
