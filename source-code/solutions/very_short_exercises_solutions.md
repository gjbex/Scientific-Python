# Example Solutions for Very Short Exercises

These are concise example solutions for the exercises in `very_short_exercises.md`. They are intended as worked examples, not as the only acceptable answers.

## NumPy

### 1. Creating a simple array

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(a)
print(np.mean(a))
print(np.std(a))
```

### 2. Building a diagonal matrix

```python
import numpy as np

A = np.zeros((3, 3))
np.fill_diagonal(A, 1)
print(A)
```

### 3. Vector operations

```python
import numpy as np

u = np.array([1, 2, 3])
v = np.array([4, 5, 6])

print(u + v)
print(u * v)
print(np.dot(u, v))
```

### 4. Reshaping and slicing

```python
import numpy as np

A = np.arange(16).reshape(4, 4)
print(A)
print(A[1, :])
print(A[:, 2])
```

### 5. Sampling a function

```python
import numpy as np

x = np.linspace(0.0, 1.0, 100)
y = np.sin(x)
print(x[:5])
print(y[:5])
```

### 6. Maximum and location

```python
import numpy as np

A = np.random.rand(5, 5)
idx = np.argmax(A)
pos = np.unravel_index(idx, A.shape)

print(A)
print(np.max(A))
print(pos)
```

### 7. Boolean masking

```python
import numpy as np

a = np.array([0.2, 1.7, -0.3, 2.4, 0.8])
mask = a > 0.5

print(mask)
print(a[mask])
```

### 8. Stacking arrays

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.vstack((a, b)))
print(np.column_stack((a, b)))
```

## SciPy

### 9. Numerical integration

```python
import numpy as np
from scipy.integrate import quad

f = lambda x: np.exp(-x**2)
value, error = quad(f, 0.0, 1.0)

print(value)
print(error)
```

### 10. Root finding

```python
import numpy as np
from scipy.optimize import root

f = lambda x: np.cos(x) - x
sol = root(f, 1.0)

print(sol.x[0])
print(f(sol.x[0]))
```

### 11. Simple minimization

```python
from scipy.optimize import minimize

f = lambda x: (x[0] - 2.0)**2 + 1.0
sol = minimize(f, [0.0])

print(sol.x[0])
print(sol.fun)
```

### 12. One-dimensional interpolation

```python
import numpy as np
from scipy.interpolate import interp1d

x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([1.0, 3.0, 2.0, 4.0])
f = interp1d(x, y, kind="linear")

x_new = np.array([0.5, 1.5, 2.5])
print(f(x_new))
```

### 13. Numerical eigenvalues

```python
import numpy as np
from scipy.linalg import eig

A = np.array([[2.0, 1.0], [1.0, 2.0]])
values, vectors = eig(A)

print(values)
print(vectors)
```

### 14. Solving a linear system

```python
import numpy as np
from scipy.linalg import solve

A = np.array([[2.0, 1.0], [1.0, 3.0]])
b = np.array([1.0, 2.0])
x = solve(A, b)

print(x)
print(A @ x)
```

### 15. Discrete Fourier transform

```python
import numpy as np
from scipy.fft import fft, fftfreq

n = 100
dt = 0.01
t = np.arange(n) * dt
signal = np.sin(2.0 * np.pi * 5.0 * t)

spec = fft(signal)
freq = fftfreq(n, dt)
dominant = freq[np.argmax(np.abs(spec[:n // 2]))]

print(dominant)
```

### 16. Linear regression

```python
import numpy as np
from scipy.stats import linregress

rng = np.random.default_rng(1234)
x = np.linspace(0.0, 10.0, 20)
y = 2.0 * x + 1.0 + 0.5 * rng.normal(size=x.size)

fit = linregress(x, y)
print(fit.slope)
print(fit.intercept)
```

## SymPy

### 17. Simplifying an expression

```python
import sympy as sp

x = sp.symbols("x")
expr = (x**2 - 1) / (x - 1)

print(expr)
print(sp.simplify(expr))
```

### 18. Symbolic differentiation and integration

```python
import sympy as sp

x = sp.symbols("x")
expr = sp.sin(x) * sp.exp(x)

print(sp.diff(expr, x))
print(sp.integrate(expr, x))
```

### 19. Solving a quadratic equation

```python
import sympy as sp

x = sp.symbols("x")
solutions = sp.solve(x**2 - 5*x + 6, x)

print(solutions)
```

### 20. Symbolic matrix operations

```python
import sympy as sp

A = sp.Matrix([[1, 2], [3, 4]])

print(A.det())
print(A.eigenvals())
```
