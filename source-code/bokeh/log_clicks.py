#!/usr/bin/env python

from bokeh.events import Tap
from bokeh.io import curdoc, show
from bokeh.plotting import figure
import numpy as np

fig = figure(title='test plot', toolbar_location=None)

x = np.linspace(0.0, 1.0, 101)
y = np.sqrt(x)

fig.line(x, y)

def log_press(event):
    with open('my_log.txt', 'a') as file:
        print(f'{event.sx},{event.sy}: {event.x},{event.y}', file=file)

fig.on_event(Tap, log_press)
curdoc().add_root(fig)
