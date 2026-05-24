# manim

`manim` is a framework to create mathematical animation in the style of
[3Blue1Brown](https://www.3blue1brown.com/).  This directory contains
a few examples.


## What is it?

1. `square_and_circle.py`: a square is rendered, flips and rotates, and
   is transformed into a circle.
1. `environment.yml`: conda environment description to use `manim`.


## How to use it?

The recommended environment is the `manim` Pixi environment defined in the
repository root.  From the repository root, use:

```bash
pixi run -e manim manim-square
```

From this directory, the example can also be rendered directly:

```bash
pixi run -e manim manim -pql square_and_circle.py SquareAndCircle
```
