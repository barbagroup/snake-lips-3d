"""Compare surface pressure coefficients."""

from matplotlib import pyplot
import numpy
import pathlib


rootdir = pathlib.Path(__file__).absolute().parents[1]

case1 = rootdir / 'snake3d2k35_both'
filepath = case1 / 'data' / 'surface_pressure_coefficient.txt'
with open(filepath, 'r') as infile:
    x1, cp1 = numpy.loadtxt(infile, usecols=(0, 2), unpack=True)

case2 = rootdir / 'snake3d2k35_both_fine'
filepath = case2 / 'data' / 'surface_pressure_coefficient.txt'
with open(filepath, 'r') as infile:
    x2, cp2 = numpy.loadtxt(infile, usecols=(0, 2), unpack=True)

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot the surface pressure coefficient.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$x / c$')
ax.set_ylabel('$C_p$')
ax.plot(x1, cp1, color='black')
ax.plot(x2, cp2, color='C0')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

pyplot.show()
