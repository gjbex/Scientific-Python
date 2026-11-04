# Xarray

xarray is a Python package to represent numerical data with metadata.  In that respect it is
a hybrid between numpy and pandas.

## Requirements

The recommended environment is the `xarray` Pixi environment defined in the
repository root:

```bash
pixi run -e xarray lab
```

From this directory, the notebook can also be opened with:

```bash
pixi run -e xarray jupyter lab .
```

## What is it?

- [`xarray_intro.ipynb`](xarray_intro.ipynb): introductory tutorial on labeled
  multidimensional data, coordinate-aware computation, plotting, and NetCDF.
- [`xarray_combining.ipynb`](xarray_combining.ipynb): optional tutorial on
  concatenating, merging, filling, and assembling labeled data while making
  coordinate and conflict policies explicit.
- [`xarray_zarr.ipynb`](xarray_zarr.ipynb): optional tutorial on storing an
  xarray dataset in Zarr and choosing storage chunks from expected access
  patterns.
