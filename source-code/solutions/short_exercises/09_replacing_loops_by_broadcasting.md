# 9. Replacing loops by broadcasting

## Example solution

Suppose each row of a matrix should be scaled by a different factor.

```python
import numpy as np

A = np.arange(12).reshape(3, 4)
scale = np.array([1.0, 10.0, 100.0])

B_loop = np.empty_like(A, dtype=float)
for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        B_loop[i, j] = scale[i] * A[i, j]

B_broadcast = scale[:, np.newaxis] * A

print(np.allclose(B_loop, B_broadcast))
print(B_broadcast)
```

## Discussion

The key point is the inserted axis in `scale[:, np.newaxis]`, which allows NumPy to broadcast the row factors across columns.
