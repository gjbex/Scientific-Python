# 5. Nearby trajectories in the logistic map

## Example solution

```python
import numpy as np

def step(x, r):
    return r * x * (1.0 - x)

def trajectory(x0, r, n=50):
    xs = [x0]
    x = x0
    for _ in range(n):
        x = step(x, r)
        xs.append(x)
    return np.array(xs)

for r in [3.2, 3.9]:
    a = trajectory(0.2, r)
    b = trajectory(0.200001, r)
    print(r, np.abs(a - b)[-5:])
```

## Discussion

For `r = 3.2`, the trajectories remain close after transients. For `r = 3.9`, the difference typically grows quickly, reflecting sensitive dependence on initial conditions.
