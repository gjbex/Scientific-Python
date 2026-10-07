#!/usr/bin/env python3

'''Create a GIF illustrating the mean-field Ising phase transition.

The inverse temperature is denoted by beta, the temperature by T = 1 / beta,
and the magnetization by m. Natural units with the Boltzmann constant equal
to one are used.
'''

from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from pathlib import Path
import shutil
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from numpy.typing import NDArray


CRITICAL_BETA = 0.25
BETA_STEP = 0.025
FRAME_DELAY_CENTISECONDS = 100


def mean_field_response(
    magnetization: float | NDArray[np.float64], beta: float
) -> np.float64 | NDArray[np.float64]:
    '''Return tanh(4 beta m) for magnetization m.'''
    return np.tanh(4.0 * beta * magnetization)


def find_magnetizations(beta: float) -> NDArray[np.float64]:
    '''Find the three mean-field fixed points for an inverse temperature.'''
    if beta <= CRITICAL_BETA:
        return np.zeros(3)

    def residual(magnetization: float) -> float:
        response = mean_field_response(magnetization, beta)
        return float(response - magnetization)

    solution = opt.root_scalar(
        residual,
        bracket=(np.finfo(float).eps, 1.0),
        method='brentq',
    )
    if not solution.converged:
        raise RuntimeError(f'root finding failed for beta = {beta:.5f}')

    positive_root = solution.root
    return np.array([-positive_root, 0.0, positive_root])


def frame_path(file_base: Path, index: int) -> Path:
    '''Return the output path for a numbered PNG frame.'''
    return file_base.parent / f'{file_base.name}-{index:04d}.png'


def movie_path(file_base: Path) -> Path:
    '''Return the output path for the GIF animation.'''
    return file_base.parent / f'{file_base.name}.gif'


def create_plot(
    beta: float,
    index: int,
    beta_history: list[float],
    magnetization_history: list[list[float]],
    options: Namespace,
) -> Path:
    '''Create one animation frame and return its path.'''
    magnetizations = np.linspace(
        -options.x_max, options.x_max, options.points
    )
    responses = mean_field_response(magnetizations, beta)
    roots = find_magnetizations(beta)

    beta_history.append(beta)
    for branch, root in zip(magnetization_history, roots, strict=True):
        branch.append(float(root))

    output_path = frame_path(options.file_base, index)
    figure, main_axes = plt.subplots()
    try:
        main_axes.plot(magnetizations, responses)
        main_axes.plot(magnetizations, magnetizations)
        main_axes.plot(roots, mean_field_response(roots, beta), 'ro')
        main_axes.set(
            xlabel=r'$m$',
            ylabel=r'$\tanh(4\beta m)$',
            xlim=(-options.x_max, options.x_max),
            ylim=(-1.1, 1.1),
        )
        main_axes.text(
            0.05,
            0.75,
            rf'$\beta = {beta:.5f}$',
            fontsize=16,
            transform=main_axes.transAxes,
        )

        inset_axes = figure.add_axes((0.6, 0.2, 0.35, 0.35))
        temperatures = np.reciprocal(np.asarray(beta_history))
        for branch in magnetization_history:
            inset_axes.plot(temperatures, branch, 'b-')
        inset_axes.set(
            xlabel=r'$T$',
            ylabel=r'$m$',
            xlim=(0.0, 1.0 / options.beta_min),
            ylim=(-1.1, 1.1),
        )

        figure.savefig(output_path)
    finally:
        plt.close(figure)

    return output_path


def create_beta_schedule(options: Namespace) -> list[float]:
    '''Return inverse temperatures used for the animation frames.'''
    beta_values: list[float] = []
    beta = options.beta_max
    while (
        beta >= CRITICAL_BETA + 1.0e-5
        and len(beta_values) < options.steps
    ):
        beta_values.append(beta)
        beta = CRITICAL_BETA + (beta - CRITICAL_BETA) / options.alpha

    beta = CRITICAL_BETA
    while (
        beta >= options.beta_min
        and len(beta_values) < 2 * options.steps
    ):
        beta_values.append(beta)
        beta -= BETA_STEP

    return beta_values


def create_gif(frame_paths: Sequence[Path], output_path: Path) -> None:
    '''Create a GIF from PNG frames with ImageMagick.'''
    image_magick = shutil.which('magick') or shutil.which('convert')
    if image_magick is None:
        raise FileNotFoundError(
            'ImageMagick is required, but neither magick nor convert was found'
        )

    subprocess.run(
        [
            image_magick,
            '-set',
            'delay',
            str(FRAME_DELAY_CENTISECONDS),
            *(str(path) for path in frame_paths),
            str(output_path),
        ],
        check=True,
    )


def remove_frames(
    frame_paths: Sequence[Path], *, keep_last: bool, keep_all: bool
) -> None:
    '''Remove temporary PNG frames according to the retention options.'''
    if keep_all:
        return

    paths_to_remove = frame_paths[:-1] if keep_last else frame_paths
    for path in paths_to_remove:
        path.unlink()


def parse_args(argv: Sequence[str] | None = None) -> Namespace:
    '''Parse and validate command-line arguments.'''
    parser = ArgumentParser(
        description='create a GIF for the Ising mean-field equation'
    )
    parser.add_argument(
        '--x-max',
        '--x_max',
        dest='x_max',
        type=float,
        default=1.5,
        help='maximum absolute magnetization shown on the x-axis',
    )
    parser.add_argument(
        '--points',
        type=int,
        default=200,
        help='number of points in each mean-field curve',
    )
    parser.add_argument(
        '--beta-min',
        '--beta_min',
        dest='beta_min',
        type=float,
        default=1.0 / 6.0,
        help='minimum inverse temperature beta',
    )
    parser.add_argument(
        '--beta-max',
        '--beta_max',
        dest='beta_max',
        type=float,
        default=3.0,
        help='maximum inverse temperature beta',
    )
    parser.add_argument(
        '--alpha',
        type=float,
        default=2.0,
        help=(
            'approach factor alpha in beta(i+1) = 1/4 '
            '+ (beta(i) - 1/4)/alpha'
        ),
    )
    parser.add_argument(
        '--file-base',
        '--file_base',
        dest='file_base',
        type=Path,
        default=Path('ising_magnetization'),
        help='base path for PNG frames and the GIF',
    )
    parser.add_argument(
        '--steps',
        type=int,
        default=20,
        help='maximum number of frames on each side of the transition',
    )
    parser.add_argument(
        '--keep-last',
        '--keep_last',
        dest='keep_last',
        action='store_true',
        help='keep the last PNG frame',
    )
    parser.add_argument(
        '--keep-all',
        '--keep_all',
        dest='keep_all',
        action='store_true',
        help='keep all PNG frames',
    )
    arguments = parser.parse_args(argv)

    if arguments.x_max <= 0.0:
        parser.error('--x-max must be positive')
    if arguments.points < 2:
        parser.error('--points must be at least 2')
    if not 0.0 < arguments.beta_min <= CRITICAL_BETA:
        parser.error('--beta-min must be in the interval (0, 0.25]')
    if arguments.beta_max < CRITICAL_BETA:
        parser.error('--beta-max must be at least 0.25')
    if arguments.alpha <= 1.0:
        parser.error('--alpha must be greater than 1')
    if arguments.steps < 1:
        parser.error('--steps must be positive')

    return arguments


def main(argv: Sequence[str] | None = None) -> int:
    '''Create all frames, assemble the GIF, and clean up temporary files.'''
    options = parse_args(argv)
    options.file_base.parent.mkdir(parents=True, exist_ok=True)

    beta_history: list[float] = []
    magnetization_history: list[list[float]] = [[], [], []]
    frame_paths: list[Path] = []

    for index, beta in enumerate(create_beta_schedule(options), start=1):
        print(
            f'creating plot {index} for beta = {beta:.5f}',
            file=sys.stderr,
        )
        frame_paths.append(
            create_plot(
                beta,
                index,
                beta_history,
                magnetization_history,
                options,
            )
        )

    output_path = movie_path(options.file_base)
    print(f'creating GIF {output_path}', file=sys.stderr)
    try:
        create_gif(frame_paths, output_path)
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f'error: {error}', file=sys.stderr)
        print('PNG frames were retained', file=sys.stderr)
        return 1

    remove_frames(
        frame_paths,
        keep_last=options.keep_last,
        keep_all=options.keep_all,
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
