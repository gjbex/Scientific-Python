# 11. Reshape versus copy

## Example solution

```python
import numpy as np

a = np.arange(6)
b = a.reshape(2, 3)
c = a.copy()

b[0, 0] = 99
print("a =", a)
print("b =", b)
print("c =", c)
print(np.shares_memory(a, b))
print(np.shares_memory(a, c))
```

## Discussion

`reshape` often returns a view sharing memory with the original array, while `copy` creates independent storage.
