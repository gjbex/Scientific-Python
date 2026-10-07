#!/usr/bin/env python

from math import ceil, floor
import numpy as np
import scipy.stats


def gamma_distr(x, params):
    k = params['k']
    theta = params['theta']
    return scipy.stats.gamma.pdf(x, k, scale=theta)


def gauss_distr(x, params):
    mu = params['mu']
    sigma = params['sigma']
    return scipy.stats.norm.pdf(x - mu)/sigma


distributions = {
    'gamma': gamma_distr,
    'gauss': gauss_distr,
}


if __name__ == '__main__':
    from argparse import ArgumentParser
    from warnings import warn
    import matplotlib.pyplot as plt
# set up command line argument parser, and evaluate arguments
    arg_parser = ArgumentParser(description="plot given distribution")
    arg_parser.add_argument('file', help='data file')
    arg_parser.add_argument('-o', dest='output', help='output file')
    arg_parser.add_argument('--bins', type=int, default=50,
                            help='number of bins')
    arg_parser.add_argument('--distr',
                            help='distribution and parameters, '
                                 'e.g., --distr=gamma:k=2.0,theta=3.0'
                                 '      --distr=gauss:mu=1.0,sigma=0.5')
    options = arg_parser.parse_args()

# read data from text file
    values = np.loadtxt(options.file)

# create histogram of data
    figure, axis = plt.subplots(figsize=(8, 6))
    axis.set(
            xlabel='$x$',
            ylabel='$P(x)$',
    )
    axis.hist(values, options.bins, density=True, color='red', alpha=0.6)

# compute theoretical distribution
    if options.distr:
        name, param_str = options.distr.split(':')
        if name not in distributions:
            warn_msg = f"unknown distribution '{name}'"
            warn(warn_msg)
        else:
            param_list = param_str.split(',')
            params = {}
            for param in param_list:
                key, value = param.split('=')
                params[key] = float(value)
            x = np.linspace(floor(np.min(values)), ceil(np.max(values)),
                            200)

            try:
                y = distributions[name](x, params)
                axis.plot(x, y, linewidth=2.0, color='black')
            except KeyError as e:
                param_name = e.args[0]
                warn_msg = "missing parameter '{0}' for distribution {1}"
                warn(warn_msg.format(param_name, name))

# if output file given, create plot, otherise, show it
    if options.output:
        figure.savefig(options.output)
    else:
        plt.show()
