# 13. Comparing NumPy data types

## Example solution

```python
import numpy as np

a64 = np.ones((1000, 1000), dtype=np.float64)
a32 = np.ones((1000, 1000), dtype=np.float32)

print(a64.itemsize, a64.nbytes)
print(a32.itemsize, a32.nbytes)
```

## Discussion

`float32` uses half the storage of `float64`, at the cost of reduced precision.
