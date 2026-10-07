#!/usr/bin/env python
# borrowed from John D. Cook, posted on
# https://www.johndcook.com/blog/2017/02/14/recreating-the-vertigo-poster/
# ------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

i = np.arange(5000)
x1 = 1.0*np.cos(i/10.0)*np.exp(-i/2500.0)
y1 = 1.4*np.sin(i/10.0)*np.exp(-i/2500.0)
d = 450.0
vx = np.cos(i/d)*x1 - np.sin(i/d)*y1
vy = np.sin(i/d)*x1 + np.cos(i/d)*y1

h = max(vy) - min(vy)
w = max(vx) - min(vx)

figure, axis = plt.subplots()
axis.plot(vx, vy, "k")
axis.set_aspect(w/h)
plt.show()
