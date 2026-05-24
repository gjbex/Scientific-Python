# Plotting

Illustration of various plots in sympy, also illustrating the
use of alternative backends such as Bokeh.  Also some examples
of interactive plots implemented either using sympy plotting
backends package or ipywidgets.

## Requirements

The recommended environment is the `sympy-plotting` Pixi environment defined
in the repository root:

```bash
pixi run -e sympy-plotting lab
```

From this directory, the notebook can also be opened with:

```bash
pixi run -e sympy-plotting jupyter lab .
```

## What is it?

1. `plotting_backends.ipynb`: Jupyter notebook illustrating the
   use of the sympy plotting backends package, as well as various
   types of (interactive) plots.
1. `environment.yml`: conda environment that contains the packages
   to run the notebooks and scripts.
