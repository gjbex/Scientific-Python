# Bokeh
Bokeh is a library to create interactive plots easily from a number of
programming languages, including Python.  The result is saved to an HTML
page that can be viewed with any modern browser.

Note: out of the box, these notebooks work with Jupyter Notebook, *not*
Jupyter Lab!


## What is it?
1. `bokeh_intro.ipynb`: Jupyter notebook showing some basic plotting
    capabilities of Bokeh.
1. `function_plot.py`: a simple script to plot multiple functions on the
    same figure.
1. `HIVseries.csv`: data set to use with `viral_load.py`.
1. `ising.py`: Visualizes the graphical solution to the equation of the
    magnetization of the 2D Ising model in the mean field approximation.
    The temperature (i.e., beta = 1/T) can be varied using a slider. *Note:*
    this is intended to be run using Bokeh server, see below.
1. `pendulum.ipynb`: Jupyter notebook illustrating interactive plots with
    widgets, linked plots and a hover tool.
1. `viral_load.ipynb`: Jupyter notebook to interactively adjust the
    parameters of a model for HIV viral load to fit experimental data.

## How to use it?

To use `ising.py`, run it with the Bokeh server, i.e.,
```bash
$ bokeh serve  --show  ising.py
```
