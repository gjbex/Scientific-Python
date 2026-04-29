# 3. Sensitivity to time step in the heat equation

## Example solution

Run the same solver twice to the same physical end time, once with `dt` and once with `dt/2`.

```python
u1 = solve_diffusion(dt=1.0e-4, t_end=0.01)
u2 = solve_diffusion(dt=5.0e-5, t_end=0.01)

l2 = np.sqrt(np.mean((u1 - u2)**2))
print("L2 difference =", l2)
```

## Discussion

If the scheme is stable and the time step is already reasonably small, the two final fields should look similar and the `L2` difference should be modest. A large discrepancy indicates poor temporal resolution or instability.
