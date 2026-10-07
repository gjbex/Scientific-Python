# 4. Changing the initial condition in diffusion

## Example solution

Replace the hot square by a Gaussian profile.

```python
x = np.linspace(-1.0, 1.0, nx)
y = np.linspace(-1.0, 1.0, ny)
X, Y = np.meshgrid(x, y, indexing="ij")

u0_square = np.zeros((nx, ny))
u0_square[(np.abs(X) < 0.2) & (np.abs(Y) < 0.2)] = 1.0

u0_gauss = np.exp(-(X**2 + Y**2) / 0.05)
```

## Discussion

The Gaussian starts smooth and remains smooth, while the square starts with sharp gradients that are quickly rounded off by diffusion. The square therefore shows stronger early-time smoothing.
