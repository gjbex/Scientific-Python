# 16. Variability in diffusion-limited aggregation

## Example solution

Run the same small simulation twice with different seeds.

```python
np.random.seed(1)
cluster1 = run_dla(grid_size=31, nr_particles=50)

np.random.seed(2)
cluster2 = run_dla(grid_size=31, nr_particles=50)
```

## Discussion

Both clusters should show branched growth, but the exact arms and asymmetries differ because the aggregation process is stochastic. The purpose of the exercise is to observe variability, not to obtain identical shapes.
