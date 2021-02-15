"""Compare the mean streamwise velocity along centerline."""

from matplotlib import pyplot
import numpy
import pathlib

rootdir = pathlib.Path(__file__).absolute().parents[1]

case1 = rootdir / 'snake3d2k35_both'
filepath = case1 / 'data' / 'u_centerline_profile.txt'
with open(filepath, 'r') as infile:
    x1, ux1 = numpy.loadtxt(infile, unpack=True)

case2 = rootdir / 'snake3d2k35_both_fine'
filepath = case2 / 'data' / 'u_centerline_profile.txt'
with open(filepath, 'r') as infile:
    x2, ux2 = numpy.loadtxt(infile, unpack=True)

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('x / c')
ax.set_ylabel(r'$<u> / U_\infty$')
ax.plot(x1, ux1, color='black')
ax.plot(x2, ux2, color='C0')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

pyplot.show()