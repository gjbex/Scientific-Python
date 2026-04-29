# 19. Small-angle pendulum equation

## Example solution

The full equation is

```text
theta'' + (g / l) sin(theta) = 0
```

For small angles, use `sin(theta) ≈ theta`. This gives

```text
theta'' + (g / l) theta = 0
```

## Discussion

This is the equation of a simple harmonic oscillator with angular frequency

```text
omega = sqrt(g / l)
```

The approximation is good only when `|theta|` remains small enough that `sin(theta)` and `theta` are close.
