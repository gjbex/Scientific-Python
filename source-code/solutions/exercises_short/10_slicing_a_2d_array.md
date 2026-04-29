# 10. Slicing a 2D array

## Example solution

```python
import numpy as np

A = np.arange(30).reshape(5, 6)
sub = A[::2, -3:]

print(A)
print(sub)
print(sub.shape)
```

## Discussion

`::2` selects every second row, while `-3:` selects the last three columns.
