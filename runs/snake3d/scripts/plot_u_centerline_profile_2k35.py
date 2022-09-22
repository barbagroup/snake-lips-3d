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

cases = {
    'both_lips': {'2k': [35]},
    'front_lip': {'2k': [35]},
    'back_lip': {'2k': [35]},
    'no_lips': {'2k': [35]}
}

times = numpy.round(
    numpy.arange(start=100, stop=200 + 1e-3, step=0.05),
    decimals=2
)

data = dict()
body = dict()
for lip_cfg in cases.keys():
    for Re, angles in cases[lip_cfg].items():
        for AoA in angles:
            vel_obj = rodney.UxCenterlineData(
                None, maindir / lip_cfg / f'{Re}{AoA}'
            )

            if args.compute:
                vel_obj.compute(times, from_tarball=True)
                vel_obj.save('u_centerline_profile_100_200.txt')
            else:
                vel_obj.load('u_centerline_profile_100_200.txt')

            data[f'{lip_cfg}_{Re}{AoA}'] = vel_obj

            filepath = (maindir / lip_cfg / f'{Re}{AoA}' /
                        'RANS' / 'constant' / 'triSurface' / 'snake.obj')
            _body = pyvista.get_reader(str(filepath)).read()
            _body = _body.slice(normal='z')
            xb, yb = _body.points[:, 0], _body.points[:, 1]

            body[f'{lip_cfg}_{Re}{AoA}'] = (xb, yb)

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

plt_kwargs = {
    'both_lips_2k35': dict(label='Both', color='C0', linestyle='-'),
    'front_lip_2k35': dict(label='Front', color='C1', linestyle='-'),
    'back_lip_2k35': dict(label='Back', color='C2', linestyle='-'),
    'no_lips_2k35': dict(label='None', color='C3', linestyle='-')
}

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('$x / c$')
ax.set_ylabel(r'$<u> / U_\infty$')
U_inf, D = 1.0, 1.0
ax.axhline(0.0, color='gray', linestyle='--')
for label, vel_obj in data.items():
    ax.plot(vel_obj.x / D, vel_obj.values / U_inf, **plt_kwargs[label])
    plt_kwargs[label]['label'] = None
    if label != 'both_lips_2k35':
        ax.plot(*body[label], **plt_kwargs[label])
ax.axis('scaled')
ax.axis([-0.6, 3.0, -0.5, 1.0])
ax.set_yticks([-0.5, 0.0, 0.5, 1.0])
ax.legend(frameon=False, loc='upper left', fontsize=12)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_centerline_profile_2k35.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
