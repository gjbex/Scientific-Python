# NetCDF Python API examples

Code samples of how to read and write NetCDF files using the netCDF4
module for Python (not part of the standard library).


## Requirements

The NetCDF library is required, as wel as tne `netcdf4` python package.  The
recommended environment is the `netcdf` Pixi environment defined in the
repository root:

```bash
pixi run -e netcdf netcdf-write
pixi run -e netcdf netcdf-read
```

From this directory, the scripts can also be run directly:

```bash
pixi run -e netcdf python write_netcdf.py
pixi run -e netcdf python read_netcdf.py
```

For compatibility, Conda environment definitions are also available:

* `environment.yml`
* `netcdf_linux64_conda_specs.txt`


## What is it?

1. `write_netcdf.py`: writes an NetCDF 3 file that has three dimensions
   x, y, and z.  The grid points are stored in variables 'x', 'y', and 'z'
   respectively, and the field is stored in a 3D variable 'field'.
   NetCDF 3 as well as NetCDF 4 can be generated since ParaView prior
   to version 4.1.x seems not to be able to deal with NetCDF 4.
1. `read_netcdf.py`: read a NetCDF file that was created `write_netcdf.py`.
1. `test.nc`: sample NetCDF file.
