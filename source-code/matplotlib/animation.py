#!/usr/bin/env python3

'''Create an MP4 animation of a decaying cosine function.

Frame i shows f_i(x) = cos(2 pi x) exp(-0.005 x^2 i), where x is the
horizontal coordinate and i is the zero-based frame index.
'''

from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation, writers
from matplotlib.axes import Axes
from matplotlib.lines import Line2D


FRAME_COUNT = 300
FRAMES_PER_SECOND = 2


class CosineDecay:
    '''Update a line plot with successive decaying cosine curves.'''

    def __init__(
        self,
        axes: Axes,
        x_min: float,
        x_max: float,
        num_points: int = 200,
    ) -> None:
        axes.set(xlim=(x_min, x_max), ylim=(-1.0, 1.0))
        (self._line,) = axes.plot([], [])
        self._x = np.linspace(x_min, x_max, num_points)
        self._cosine = np.cos(2.0 * np.pi * self._x)
        self._x_squared = self._x**2

    def initialize(self) -> tuple[Line2D]:
        '''Clear the animated line before drawing the first frame.'''
        self._line.set_data([], [])
        return (self._line,)

    def update(self, frame_index: int) -> tuple[Line2D]:
        '''Update the line for a zero-based frame index.'''
        decay = np.exp(-0.005 * self._x_squared * frame_index)
        self._line.set_data(self._x, self._cosine * decay)
        return (self._line,)


def parse_args(argv: Sequence[str] | None = None) -> Namespace:
    '''Parse command-line arguments.'''
    parser = ArgumentParser(
        description='create an MP4 animation of a decaying cosine'
    )
    parser.add_argument('file', type=Path, help='MP4 output path')
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    '''Create and save the animation.'''
    options = parse_args(argv)
    if not writers.is_available('ffmpeg'):
        raise RuntimeError('ffmpeg is required to create the MP4 animation')

    options.file.parent.mkdir(parents=True, exist_ok=True)

    figure, axes = plt.subplots()
    cosine_decay = CosineDecay(
        axes,
        x_min=-6.0 * np.pi,
        x_max=6.0 * np.pi,
        num_points=2000,
    )
    animation = FuncAnimation(
        figure,
        cosine_decay.update,
        init_func=cosine_decay.initialize,
        frames=FRAME_COUNT,
        blit=True,
    )

    try:
        writer = FFMpegWriter(fps=FRAMES_PER_SECOND)
        animation.save(str(options.file), writer=writer)
    finally:
        plt.close(figure)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
