# 12. Working with structured arrays

## Example solution

```python
import numpy as np

particles = np.array(
    [(1.0, -1), (12.0, 6), (16.0, 8)],
    dtype=[("mass", "f8"), ("charge", "i4")]
)

print(particles)
print(particles["mass"])
print(np.sort(particles, order="mass"))
```

## Discussion

Structured arrays store heterogeneous fields under names while still supporting NumPy operations such as sorting.
