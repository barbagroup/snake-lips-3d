"""Plot the centerline mean streamwise velocity."""

import pathlib

import numpy
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

vel_obj = rodney.UxCenterlineData('Present', maindir)

if args.compute:
    times = numpy.round(numpy.arange(start=50, stop=100 + 1e-3, step=0.05),
                        decimals=2)
    vel_obj.compute(times, from_tarball=True)
    vel_obj.save('u_centerline_profile_50_100.txt')
else:
    vel_obj.load('u_centerline_profile_50_100.txt')

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('x / D')
ax.set_ylabel(r'$<u> / U_\infty$')
U_inf, D = 1.0, 1.0
ax.plot(vel_obj.x / D, vel_obj.values / U_inf, color='black')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_centerline_profile.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
