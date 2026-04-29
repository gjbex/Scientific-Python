# 8. Noise and spectral peaks

## Example solution

```python
import numpy as np

rng = np.random.default_rng(123)
dt = 0.01
t = np.arange(0.0, 2.0, dt)
clean = np.cos(2*np.pi*8*t)

for sigma in [0.0, 0.2, 0.5, 1.0]:
    noisy = clean + sigma * rng.normal(size=t.size)
    spec = np.fft.rfft(noisy)
    freq = np.fft.rfftfreq(t.size, dt)
    peak = freq[np.argmax(np.abs(spec))]
    print(f"sigma={sigma:.1f}, dominant frequency={peak:.2f}")
```

## Discussion

As the noise level grows, the main peak usually remains near the correct frequency but becomes less pronounced relative to the background.
