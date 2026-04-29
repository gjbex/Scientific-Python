# 15. Magnetization of simple Ising configurations

## Example solution

For a spin array `s` with values `+1` and `-1`, a common definition is

```python
import numpy as np

def magnetization(s):
    return np.sum(s) / s.size

aligned = np.ones((4, 4), dtype=int)
random_state = np.array([
    [ 1, -1,  1,  1],
    [-1, -1,  1, -1],
    [ 1,  1, -1, -1],
    [ 1, -1, -1,  1],
])

print(magnetization(aligned))
print(magnetization(random_state))
```

## Discussion

The aligned state has magnetization `1.0`. The random state has a value nearer `0`, because positive and negative spins partially cancel.
