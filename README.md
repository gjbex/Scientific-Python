# Scientific Python

GitHub repository for participants of the "Scientific Python" training.
For information on the training, see the website
[https://gjbex.github.io/Scientific-Python/](https://gjbex.github.io/Scientific-Python/)

## Environment

This repository uses [Pixi](https://pixi.sh/) to define the Python
environments for the training examples.

Make sure the installed `pixi` command is the Prefix.dev Pixi tool:

```bash
pixi --version
```

To start Jupyter Lab with the default training environment, run:

```bash
pixi run lab
```

Some examples use additional packages that are not needed for the main
training path.  These are available as named Pixi environments, for example:

```bash
pixi run -e image lab
pixi run -e netcdf netcdf-write
pixi run -e manim manim-square
```

The existing `environment.yml` and topic-specific Conda environment files are
kept for compatibility, but `pixi.toml` is the preferred environment
definition.

## What is it?

1. [`scientific_python.pptx`](scientific_python.pptx): PowerPoint
   presentation used for the training.
1. [`source-code`](source-code): directory that contains sample code written to
   develop the slides and illustrate concepts.
1. [License](LICENSE): license information for the material in this repository.
1. [Contributing](CONTRIBUTING.md): information on how to contribute to this
   repository.
1. docs: directory containing the website for this repository.
1. [Code of conduct](CODE_OF_CONDUCT.md): when participating in this training
   you accept to abide by the code of conduct.
