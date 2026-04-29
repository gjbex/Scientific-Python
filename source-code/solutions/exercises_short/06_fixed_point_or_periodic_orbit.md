# 6. Fixed point or periodic orbit?

## Example solution

```python
def classify(r, x0=0.2, n_burn=200, n_keep=20, tol=1.0e-8):
    x = x0
    for _ in range(n_burn):
        x = r * x * (1.0 - x)
    values = []
    for _ in range(n_keep):
        x = r * x * (1.0 - x)
        values.append(x)
    rounded = np.round(values, 8)
    return len(np.unique(rounded))

for r in [2.8, 3.2, 3.5, 3.9]:
    print(r, classify(r))
```

## Discussion

One distinct long-time value suggests a fixed point, two values suggest a period-2 orbit, and more distinct values indicate higher-period or chaotic behavior.
