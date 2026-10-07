#!/usr/bin/env python

import sys
import numpy as np
from scipy.integrate import solve_ivp


#
# f[0] = d theta1/dt = omega1
# f[1] = d theata2/dt = omega2
# f[2] = d omega1/dt = -(g/l1)*theta1 - k*(theta1 - theta2)
# f[3] = d omega2/dt = -(g/l2)*theta2 - k*(theta2 - theta1)
#
# y[0] = theta1
# y[1] = theta2
# y[2] = omega1
# y[3] = omega2
#
def functions(t, y, l1, l2, k):
    g = 9.81
    return (
        y[2],
        y[3],
        -(g/l1)*y[0] - k*(y[0] - y[1]),
        -(g/l2)*y[1] - k*(y[1] - y[0])
    )


if __name__ == '__main__':
    from argparse import ArgumentParser
    arg_parser = ArgumentParser(description='solved coupled pendulums')
    arg_parser.add_argument('--theta0_1', type=float, default=0.0,
                            help='initial theta of first pendulum')
    arg_parser.add_argument('--theta0_2', type=float, default=0.0,
                            help='initial theta of second pendulum')
    arg_parser.add_argument('--l1', type=float, default=1.0,
                            help='length of first pendulum')
    arg_parser.add_argument('--l2', type=float, default=1.0,
                            help='length of second pendulum')
    arg_parser.add_argument('--k', type=float, default=0.5,
                            help="Hooke's constant")
    arg_parser.add_argument('--t_max', type=float, default=10*2*np.pi,
                            help='maximum time')
    arg_parser.add_argument('--delta_t', type=float, default=0.01,
                            help='delta t')
    options = arg_parser.parse_args()
    solution = solve_ivp(
            functions,
            t_span=(0.0, options.t_max),
            y0=(options.theta0_1, options.theta0_2, 0.0, 0.0),
            args=(options.l1, options.l2, options.k),
            t_eval=np.arange(0.0, options.t_max, options.delta_t),
            rtol=1.0e-6, atol=1.0e-6,
            method='RK45'
    )
    if not solution.success:
        print('Integration failed: {0}'.format(solution.message), file=sys.stderr)
        sys.exit(1)
    for t, theta1, theta2 in zip(solution.t, solution.y[0], solution.y[1]):
        print(f'{t:.3f}\t{theta1:.5f}\t{theta2:.5f}')
