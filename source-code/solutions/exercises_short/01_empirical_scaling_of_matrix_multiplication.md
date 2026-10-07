# 1. Empirical scaling of matrix multiplication

## Example solution

Use three matrix sizes, time `np.dot`, then estimate the slope of a log-log fit.

```python
import time
import numpy as np

sizes = np.array([100, 200, 400], dtype=float)
times = []

for n in sizes.astype(int):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    t0 = time.perf_counter()
    np.dot(A, B)
    times.append(time.perf_counter() - t0)

times = np.array(times)
alpha, beta = np.polyfit(np.log(sizes), np.log(times), 1)
print("sizes =", sizes)
print("times =", times)
print("estimated exponent =", alpha)
```

## Discussion

The fitted slope should be near 3 for large enough matrices, although BLAS implementation details and cache effects often distort the estimate for small systems.
