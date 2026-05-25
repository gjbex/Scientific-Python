# Setup

This repository supports two ways to create a Python environment for the
training examples:

* Pixi, the preferred setup for this repository.
* Mamba, a compatibility setup based on the existing Conda environment file.

Both approaches assume that you run commands from a terminal.

## Pixi

Pixi uses the checked-in `pixi.toml` and `pixi.lock` files.  This is the
recommended setup.

Install Pixi following the instructions at <https://pixi.sh/>.

Check that the `pixi` command is the Prefix.dev Pixi tool:

```bash
pixi --version
```

Create the default environment from the repository root:

```bash
pixi install
```

On systems with a small home directory quota, set `PIXI_HOME` to a location
with enough space before installing environments:

```bash
export PIXI_HOME=/path/to/scratch/pixi
```

Pixi and its dependencies may also use the system temporary directory.  On HPC
systems where the default temporary directory is unsuitable, set `TMPDIR` to a
site-appropriate location:

```bash
export TMPDIR=/path/to/scratch/tmp
```

See the root `README.md` and the `source-code` subdirectory READMEs for usage
commands.

## Mamba

The repository also contains a Conda-style `environment.yml` file that can be
used with Mamba.  This environment is broader than the default Pixi
environment and includes several optional packages.

Install Mamba or a Mamba-compatible Conda distribution, then create the
environment from the repository root:

```bash
mamba env create -f environment.yml
```

Activate the environment:

```bash
mamba activate scientific_python
```

On systems with a small home directory quota, configure Conda/Mamba to store
environments and package caches on a filesystem with enough space.  For
example:

```bash
conda config --add envs_dirs /path/to/scratch/conda/envs
conda config --add pkgs_dirs /path/to/scratch/conda/pkgs
```

Mamba reads the same Conda configuration, so this also affects `mamba env
create` and `mamba env update`.

If the environment already exists and `environment.yml` changes, update it with:

```bash
mamba env update -f environment.yml --prune
```

Topic-specific Conda environment files are still present in a few
subdirectories for compatibility with older versions of the training material.
See the root `README.md` and the `source-code` subdirectory READMEs for usage
commands.
