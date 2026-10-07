# Very Short Exercises

These exercises are intended to take approximately 10 minutes each and start from scratch. They focus on core `numpy`, `scipy`, and `sympy` functionality rather than on the repository material. Each problem targets a small number of functions and is suitable for a quick practice session, a warm-up exercise, or a short tutorial.

This sheet is intended as an entry point before moving on to `exercises_short.md` and `exercises_challenging.md`. For an overview of all exercise sheets, see `exercises.md`.

## NumPy

### 1. Creating a simple array

Create a 1D NumPy array containing the integers 1 through 10, then compute its mean and standard deviation.

- Estimated effort: 5-10 minutes
- Target functions: `np.array`, `np.mean`, `np.std`
- Optional hints:
  - Store the values in a single array first.
  - Print both the array and the computed quantities.
  - Compare the result with a manual check for one of the quantities.

### 2. Building a diagonal matrix

Create a `3 x 3` matrix filled with zeros, then replace the diagonal by ones.

- Estimated effort: 5-10 minutes
- Target functions: `np.zeros`, `np.fill_diagonal`
- Optional hints:
  - Print the matrix before and after changing the diagonal.
  - Check that only diagonal entries were modified.

### 3. Vector operations

Create two vectors and compute their elementwise sum, elementwise product, and dot product.

- Estimated effort: 5-10 minutes
- Target functions: `np.array`, `+`, `*`, `np.dot`
- Optional hints:
  - Use short vectors so the result is easy to check by hand.
  - Compare elementwise multiplication with the dot product.

### 4. Reshaping and slicing

Create a `4 x 4` array with values from 0 to 15 and extract the second row and the third column.

- Estimated effort: 5-10 minutes
- Target functions: `np.arange`, `reshape`, slicing
- Optional hints:
  - Print the full array first.
  - Remember that Python indexing starts at 0.

### 5. Sampling a function

Generate 100 evenly spaced points between 0 and 1 and evaluate `sin(x)` on them.

- Estimated effort: 5-10 minutes
- Target functions: `np.linspace`, `np.sin`
- Optional hints:
  - Store the sample points and function values in separate arrays.
  - Print the first few values to verify the result.

### 6. Maximum and location

Create a random `5 x 5` array and find its maximum value and the index where it occurs.

- Estimated effort: 5-10 minutes
- Target functions: `np.random.rand`, `np.max`, `np.argmax`, `np.unravel_index`
- Optional hints:
  - First find the flat index with `argmax`.
  - Then convert it to row and column indices.

### 7. Boolean masking

Given a 1D array, select only the entries larger than a chosen threshold.

- Estimated effort: 5-10 minutes
- Target functions: comparison operators, boolean masks
- Optional hints:
  - Print the boolean mask before applying it.
  - Try two different threshold values.

### 8. Stacking arrays

Stack two 1D arrays as rows of a `2 x n` matrix, then as columns of an `n x 2` matrix.

- Estimated effort: 5-10 minutes
- Target functions: `np.vstack`, `np.column_stack`
- Optional hints:
  - Use small arrays so the shapes are easy to verify.
  - Print the shape of each result.

## SciPy

### 9. Numerical integration

Compute the integral of `exp(-x^2)` from 0 to 1 numerically.

- Estimated effort: 5-10 minutes
- Target functions: `scipy.integrate.quad`
- Optional hints:
  - Define the integrand as a Python function.
  - Print both the estimated integral and the error estimate.

### 10. Root finding

Solve the equation `cos(x) - x = 0` numerically starting from an initial guess.

- Estimated effort: 5-10 minutes
- Target functions: `scipy.optimize.root` or `scipy.optimize.fsolve`
- Optional hints:
  - Start from an initial guess near 1.
  - Substitute the result back into the equation to check it.

### 11. Simple minimization

Minimize the function `(x - 2)^2 + 1`.

- Estimated effort: 5-10 minutes
- Target functions: `scipy.optimize.minimize`
- Optional hints:
  - Use a one-dimensional initial guess.
  - Compare the numerical minimum with the exact answer.

### 12. One-dimensional interpolation

Interpolate a small set of data points with a 1D linear interpolant and evaluate it at intermediate points.

- Estimated effort: 5-10 minutes
- Target functions: `scipy.interpolate.interp1d`
- Optional hints:
  - Use 4 or 5 sample points only.
  - Evaluate the interpolant at values that were not in the original data.

### 13. Numerical eigenvalues

Compute the eigenvalues of a `2 x 2` matrix numerically.

- Estimated effort: 5-10 minutes
- Target functions: `scipy.linalg.eig`
- Optional hints:
  - Start with a simple matrix with real eigenvalues.
  - Print the eigenvalues clearly.

### 14. Solving a linear system

Solve a `2 x 2` linear system numerically.

- Estimated effort: 5-10 minutes
- Target functions: `scipy.linalg.solve`
- Optional hints:
  - Write the system in matrix form first.
  - Verify the solution by multiplying back.

### 15. Discrete Fourier transform

Compute the discrete Fourier transform of a short sampled signal and identify the dominant frequency.

- Estimated effort: 5-10 minutes
- Target functions: `scipy.fft.fft`, `scipy.fft.fftfreq`
- Optional hints:
  - Use a simple sine wave as the signal.
  - Compare the frequency you recover with the one you used to build the signal.

### 16. Linear regression

Generate a noisy straight line and fit it with linear regression.

- Estimated effort: 5-10 minutes
- Target functions: `scipy.stats.linregress`
- Optional hints:
  - Use a known slope and intercept.
  - Compare the fitted parameters with the exact ones.

## SymPy

### 17. Simplifying an expression

Define a symbolic variable `x` and simplify the expression `(x^2 - 1)/(x - 1)`.

- Estimated effort: 5-10 minutes
- Target functions: `symbols`, `simplify`
- Optional hints:
  - Print the expression before and after simplification.
  - Check where the original expression is not defined.

### 18. Symbolic differentiation and integration

Differentiate and integrate `sin(x) * exp(x)` symbolically.

- Estimated effort: 5-10 minutes
- Target functions: `diff`, `integrate`
- Optional hints:
  - Use the same symbolic variable for both operations.
  - Verify one result by differentiating the integral.

### 19. Solving a quadratic equation

Solve the quadratic equation `x^2 - 5x + 6 = 0` symbolically.

- Estimated effort: 5-10 minutes
- Target functions: `solve`
- Optional hints:
  - Check the solutions by substitution.
  - Compare with factorization by hand.

### 20. Symbolic matrix operations

Define a `2 x 2` symbolic matrix and compute its determinant and eigenvalues.

- Estimated effort: 5-10 minutes
- Target functions: `Matrix`, `det`, `eigenvals`
- Optional hints:
  - Begin with a matrix containing small integers.
  - Compare determinant and eigenvalues with what you expect from linear algebra.
