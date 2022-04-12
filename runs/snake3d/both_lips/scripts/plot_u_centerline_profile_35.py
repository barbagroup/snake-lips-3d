"""Plot the centerline mean streamwise velocity."""

import pathlib

import numpy
import pyvista
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

cases = {'1k': 'Re=1000', '2k': 'Re=2000', '3k': 'Re=3000'}

times = numpy.round(
    numpy.arange(start=100, stop=200 + 1e-3, step=0.05),
    decimals=2
)

data = dict()
body = dict()
for Re in cases.keys():
    vel_obj = rodney.UxCenterlineData(
        None, maindir / f'{Re}35'
    )

    if args.compute:
        vel_obj.compute(times, from_tarball=True)
        vel_obj.save('u_centerline_profile_100_200.txt')
    else:
        vel_obj.load('u_centerline_profile_100_200.txt')

    data[Re] = vel_obj

    filepath = (maindir / f'{Re}35' /
                'RANS' / 'constant' / 'triSurface' / 'snake.obj')
    _body = pyvista.get_reader(str(filepath)).read()
    _body = _body.slice(normal='z')
    xb, yb = _body.points[:, 0], _body.points[:, 1]

    body[Re] = (xb, yb)

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('x / D')
ax.set_ylabel(r'$<u> / U_\infty$')
U_inf, D = 1.0, 1.0
ax.axhline(0.0, color='gray', linestyle='--')
for key, vel_obj in data.items():
    ax.plot(vel_obj.x / D, vel_obj.values / U_inf, label=cases[key])
ax.set_xlim(0.0, 4.0)
inset_ax = fig.add_axes([0.1, 0.6, 0.3, 0.3])
for label, vel_obj in data.items():
    inset_ax.plot(*body[label], color='black')
    inset_ax.axhline(0.0, xmin=0.6, xmax=1.0, color='gray', linestyle='--')
inset_ax.axis('scaled')
inset_ax.axis('off')
ax.legend(frameon=False, loc='center right')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_centerline_profile_35.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
