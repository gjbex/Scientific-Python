# Source code

This is source code that is either used in the presentation, or was developed
to create it.  There is some material not covered in the presentation as well.

## Exercise sheets

* [`exercises.md`](exercises.md): overview of the available exercise sheets.
* [`exercises_very_short.md`](exercises_very_short.md): 5-10 minute warm-up
  exercises covering small NumPy, SciPy, and SymPy tasks.
* [`exercises_short.md`](exercises_short.md): approximately 30-minute exercises
  based on the notebooks and example code in this repository.
* [`exercises_challenging.md`](exercises_challenging.md): longer, more
  sophisticated assignments and mini-projects for advanced practice.

## Requirements

The preferred way to run the examples is through the Pixi environments defined
in [`../pixi.toml`](../pixi.toml).

To start Jupyter Lab with the default training environment, run this from the
repository root:

```bash
pixi run lab
```

Examples that need additional packages can be run with a named environment.
For example, the NetCDF examples can be run either from the repository root:

```bash
pixi run -e netcdf netcdf-write
```

or from their own directory:

```bash
cd source-code/netcdf
pixi run -e netcdf python write_netcdf.py
```

The default environment contains:
  * numpy
  * scipy
  * matplotlib
  * bokeh
  * sympy
  * ipywidgets
  * pandas
  * seaborn
  * networkx
  * Jupyter Lab

Optional named environments provide:
  * opencv
  * numexpr
  * pytables
  * h5py
  * scikit-image
  * xarray
  * netcdf4
  * vpython
  * manim

## What is it?
* [`birdsong`](birdsong): illustration of signal processing with scipy, reading
  and writing of a WAV file, computing the amplitude spectrum using FFT,
  applying a high-pass filter.
* [`bokeh`](bokeh): illustrations of how to create plots using bokeh, including
  interactive plots.
* [`hdf5`](hdf5): illustrations of how to create and access HDF5 files.
* [`image-processing`](image-processing): illustrations of image processing
  using scikit-image and video processing using OpenCV.
* [`matplotlib`](matplotlib): illustrations of how to create plots using
  matplotlib.
* [`matrices`](matrices): some numpy illustrations.
* [`numpy`](numpy): some numpy and scipy illustrations.
* [`sympy`](sympy): some illustrations of doing symbolic computations using
  sympy.
* [`xarray`](xarray): introduction to `xarray`, a library for indexed, labeled
  N-dimensional arrays.
* [`netcdf`](netcdf): sample code for reading and writing NetCDF data.
* [`vpython`]: illustrations of using VPython for physics and mathematics
  animations.
* [`manim`](manim): sample code for illustrating manim, a framework to create
  mathematical animations.
* [`cannon.ipynb`](cannon.ipynb): Jupyter notebook illustrating the use of
  numpy, scipy, sympy and bokeh.
* [`cellular_automata.ipynb`](cellular_automata.ipynb): Jupyter notebook
  illustrating the use of matplotlib.
* [`diffusion_limited_aggregation.ipynb`](diffusion_limited_aggregation.ipynb):
  Jupyter notebook illustrating the use of numpy and matplotlib.
* [`ising_model.ipynb`](ising_model.ipynb): Jupyter notebook illustrating the
  use of numpy and dependency injection in simulation design.
* [`lennard_jones.ipynb`](lennard_jones.ipynb): Jupyter notebook illustrating
  the use of numpy, scipy, sympy and matplotlib.
* [`prison_guard.ipynb`](prison_guard.ipynb): Jupyter notebook illustrating the
  use of numpy and matplotlib.
