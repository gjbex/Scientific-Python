#!/usr/bin/env python

from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt

arg_parser = ArgumentParser(description='plots damped pendulum amplitude')
arg_parser.add_argument('--mu', type=float, default=0.2,
                        help='damping coefficient')
arg_parser.add_argument('--alpha', type=float, default=0.8,
                        help='alpha factor for envelope curves')
arg_parser.add_argument('--width', type=float, default=1.0,
                        help='line width for envelope curves')
arg_parser.add_argument('file', nargs='?', help='output file name')
options = arg_parser.parse_args()

eq = (r'$\frac{d^2 \theta}{dt^2} = - \frac{g}{l} \theta ' +
      r'- \mu \frac{d\theta}{dt}$')
x = np.linspace(0.0, 20.0, 500)
y = np.exp(-options.mu*x)*np.cos(2.0*np.pi*x)
y_plus = np.exp(-options.mu*x)
y_min = -np.exp(-options.mu*x)

figure, axis = plt.subplots(figsize=(8, 4))
axis.plot(x, y)
axis.plot(x, y_plus, ':', alpha=options.alpha, color='red',
          linewidth=options.width)
axis.plot(x, y_min, ':', alpha=options.alpha, color='red',
          linewidth=options.width)
axis.set(
        xlabel=r'$t$', ylabel=r'$\theta(t)$',
        title='Damped pendulum',
)
axis.text(10.0, 0.65, eq, fontsize=18)

if options.file:
    figure.savefig(options.file)
else:
    plt.show()
