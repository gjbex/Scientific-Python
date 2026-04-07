# 7. Identifying frequencies with the FFT

## Example solution

```python
import numpy as np

dt = 0.01
t = np.arange(0.0, 2.0, dt)
signal = 1.2*np.cos(2*np.pi*5*t) + 0.8*np.cos(2*np.pi*12*t)

spec = np.fft.rfft(signal)
freq = np.fft.rfftfreq(t.size, dt)

peak_ids = np.argsort(np.abs(spec))[-2:]
print(np.sort(freq[peak_ids]))
```

## Discussion

The dominant peaks should lie near `5 Hz` and `12 Hz`, matching the frequencies used to construct the signal.
