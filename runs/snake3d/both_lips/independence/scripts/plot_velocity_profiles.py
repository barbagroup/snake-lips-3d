"""Compare velocity profiles."""

from matplotlib import pyplot
import numpy
import pathlib


rootdir = pathlib.Path(__file__).absolute().parents[1]

xlocs = [1.06, 1.54, 2.02, 4.0, 7.0, 10.0]

case1 = rootdir / 'snake3d2k35_both'
profiles1 = dict()
for xloc in xlocs:
    filepath = case1 / 'data' / f'velocity_profile_x{xloc}.txt'
    with open(filepath, 'r') as infile:
        profiles1[xloc] = numpy.loadtxt(infile, unpack=True)

case2 = rootdir / 'snake3d2k35_both_fine'
profiles2 = dict()
for xloc in xlocs:
    filepath = case2 / 'data' / f'velocity_profile_x{xloc}.txt'
    with open(filepath, 'r') as infile:
        profiles2[xloc] = numpy.loadtxt(infile, unpack=True)

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=10)

# Plot vertical profiles of the mean streamwise velocity.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('y / D')
ax.set_ylabel(r'$<u> / U_\infty$')
y_offsets = {1.06: 4.5, 1.54: 3.1, 2.02: 2.1,
             4.0: 1.0, 7.0: 0.75, 10.0: 0.21}
for xloc in xlocs:
    y, ux, _ = profiles1[xloc]
    ax.plot(y, y_offsets[xloc] + ux - 1.0, color='black')
    y, ux, _ = profiles2[xloc]
    ax.plot(y, y_offsets[xloc] + ux - 1.0, color='C0')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

# Plot vertical profiles of the mean transversal velocity.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('y / D')
ax.set_ylabel(r'$<v> / U_\infty$')
y_scale = {1.06: -0.7, 1.54: -1.4, 2.02: -2.1,
           4.0: -2.5, 7.0: -2.75, 10.0: -2.9}
for xloc in xlocs:
    y, _, uy = profiles1[xloc]
    ax.plot(y, y_offsets[xloc] + uy, color='black')
    y, _, uy = profiles2[xloc]
    ax.plot(y, y_offsets[xloc] + uy, color='C0')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

pyplot.show()
