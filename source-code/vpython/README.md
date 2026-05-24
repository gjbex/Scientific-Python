# VPython

VPython is a framework to create 3D animations in Python.  It can be used
to visualize physics simulations.

## Requirements

The recommended environment is the `vpython` Pixi environment defined in the
repository root.  To start Jupyter Lab with VPython available, run:

```bash
pixi run -e vpython lab
```

From this directory, notebooks or scripts can also be opened with:

```bash
pixi run -e vpython jupyter lab .
```

## What is it?

1. `pendulum.ipynb`: Jupyter notebook illustrating VPython on a non-linear frictionless
   pendulum, using scipy to solve the set of ODEs that describes it.  The second system
   is a double pendulum.
1. `double_pendulum.py`: module that computes the ODEs and the corresponding Jacobian
   for the double pendulum using sympy.
1. `spring.ipynb`: Jupyter notebook visualizing a mass subject to gravity and suspended
   from a spring.
1. `elastic_collistion.ipynb`: Jupyter notebook visualizing two spherical objects colliding.
1. `environment.yml`: conda environment defintion requred to run the notebook.
