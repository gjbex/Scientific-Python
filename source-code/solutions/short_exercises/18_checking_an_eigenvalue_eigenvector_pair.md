# 18. Checking an eigenvalue-eigenvector pair

## Example solution

```python
import sympy as sp

A = sp.Matrix([[2, 1], [1, 2]])
eigs = A.eigenvects()

lam = eigs[0][0]
v = eigs[0][2][0]

print("lambda =", lam)
print("v =", v)
print("A v =", A * v)
print("lambda v =", lam * v)
```

## Discussion

The two printed vectors should match exactly, verifying the eigenvalue relation.
