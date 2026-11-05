This two-part training introduces the core Python tools used in scientific
computing.  It is intended for participants who already have basic Python
programming experience and want to work with numerical algorithms,
multidimensional data, visualization, symbolic computation, and scientific
file formats.


## Learning outcomes

When you complete this training, you will be able to

* interpret NumPy array shapes, axes, dtypes, views, and copies, and express
  multidimensional computations using broadcasting, reductions, reshaping,
  and basic linear algebra;
* diagnose common numerical-reliability and resource risks involving
  precision, non-finite values, comparisons, randomness, memory use, and I/O;
* select suitable SciPy routines and assess their results using diagnostics,
  residuals, or error estimates;
* create and interpret scientific visualizations with Matplotlib;
* connect symbolic SymPy expressions to numerical calculations;
* represent and select labeled multidimensional data with xarray;
* choose a scientific data format based on fidelity, metadata, access pattern,
  and scale, and perform fundamental HDF5 operations with h5py;
* combine these tools in a scientific investigation and distinguish numerical
  cross-checking from validation of the scientific model.


## Schedule

The training has a **seven-hour scheduled duration**, delivered as two parts of
3.5 hours.  Each part includes one 15-minute short break.

The parts can be scheduled on separate days.  Participants are encouraged to
practise and work on exercises between them; this independent work is optional
and is not included in the seven-hour duration.  Part 2 starts with a recap and
questions arising from that practice, but does not require participants to have
completed the exercises.

If both parts are delivered on one day, schedule a one-hour lunch between them.
Lunch is not included in the course duration, so the total elapsed time is eight
hours.

### Part 1 — Numerical foundations

| Subject | Duration |
|---|---:|
| Objectives, logistics, and ecosystem boundaries | 10 min |
| NumPy block 1: array model | 45 min |
| NumPy block 2: multidimensional computation | 45 min |
| Short break | 15 min |
| NumPy block 3: reliability, performance, and I/O | 45 min |
| SciPy numerical workflows | 50 min |
| **Part 1 total** | **210 min** |

### Part 2 — Interpretation, scientific data, and integration

| Subject | Duration |
|---|---:|
| Recap and questions arising from Part 1 practice | 15 min |
| Matplotlib | 35 min |
| SymPy and symbolic-to-numerical work | 25 min |
| Short break | 15 min |
| xarray core | 40 min |
| Scientific formats and h5py fundamentals | 25 min |
| Integrated instructor-led pendulum investigation | 45 min |
| Synthesis, limitations, and related training | 10 min |
| **Part 2 total** | **210 min** |


## Training materials

Slides are available in the
 [GitHub repository](https://github.com/gjbex/Scientific-Python),
as well as example code and hands-on material.


## Target audience

This training is for researchers and technical users who already know basic
Python and want to apply it to numerical computation, scientific data,
visualization, and reproducible analysis.


## Prerequisites

You will need experience programming in Python.  This is not a training that starts
from scratch.

If you plan to do Python programming in a Linux or HPC environment you should
be familiar with these as well.

More concretely, participants should already be comfortable with the following:

* running Python code in Jupyter or from the command line;
* variables, numbers, strings, booleans, and basic containers such as lists and dictionaries;
* `if`/`else` statements and `for` loops;
* writing and calling simple functions with arguments and a return value;
* indexing and slicing sequences;
* importing modules and calling functions from them;
* reading short Python scripts without needing every line explained.

You do not need prior experience with NumPy, SciPy, Matplotlib, SymPy, xarray,
or HDF5.  Those are taught in the training.

### Quick self-assessment

If you can do most of the tasks below without looking up basic Python syntax, you are likely ready for this training.

* write a function that returns `sin(x)` for a given input `x`;
* loop over a list of numbers and compute their average;
* use `if`/`else` to classify a value as negative, zero, or positive;
* extract every second element from a list or array using slicing;
* read a short function with nested loops and understand what it computes;
* import a module such as `math` and call `math.cos`;
* store a few values in a dictionary and retrieve one by key;
* make a small change to an example script and run it again.

If several of these items still feel difficult, the training will probably move too fast. In that case, it is better to first take a short introductory Python course or refresh the basics.

### Software and access requirements

To follow along, you need

* a laptop or desktop with internet access;
* a Python environment that can run JupyterLab, or access to Google
  Colaboratory.

An account on a Linux or HPC system is not required.  Access to one is useful
if you want to adapt the I/O examples to that environment.


## Level of the Material

For participants who already have basic Python programming experience, the material in this training is approximately

* Introductory: 30 %
* Intermediate: 40 %
* Advanced: 30 %

These percentages describe the level of the scientific Python topics covered in the training, not the required entry level in Python itself.


## Trainer(s)

  * Geert Jan Bex ([geertjan.bex@uhasselt.be](mailto:geertjan.bex@uhasselt.be))
