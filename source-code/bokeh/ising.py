#!/usr/bin/env python

from argparse import ArgumentParser
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import curdoc, figure
import numpy as np


x = np.linspace(-3.0, 3.0, 301)
y = x.copy()
default_beta = 4.0
y_tanh = np.tanh(default_beta*x)

source = ColumnDataSource(data=dict(x=x, y=y_tanh))

def callback(attr, old_value, new_value):
    beta = new_value
    new_data = {
        'x': source.data['x'],
        'y': np.tanh(beta*source.data['x']),
    }
    source.data = new_data

plot = figure(width=300, height=300)
plot.line(x, y, line_width=0.5, line_dash='3 3')
plot.line('x', 'y', source=source)

plot.xaxis.axis_label = '$$x$$'
plot.yaxis.axis_label = r'$$\tanh \beta x$$'

slider = Slider(start=0.2, end=6.0, value=default_beta, step=0.01,
                title=r'$$\beta$$')
slider.on_change('value', callback)

layout = column(children=[plot, slider])

curdoc().add_root(layout)
