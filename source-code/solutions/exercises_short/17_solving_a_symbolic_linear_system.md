# 17. Solving a symbolic linear system

## Example solution

```python
import sympy as sp

x, y = sp.symbols("x y")
sol = sp.solve([2*x + y - 5, x - y - 1], [x, y])

print(sol)
print(2*sol[x] + sol[y] - 5)
print(sol[x] - sol[y] - 1)
```

## Discussion

The residuals should evaluate to zero, confirming the symbolic solution.
