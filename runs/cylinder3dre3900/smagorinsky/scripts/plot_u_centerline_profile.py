"""Plot the centerline mean streamwise velocity."""

import pathlib
from dataclasses import dataclass

from matplotlib import pyplot
import numpy

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

vel_objs = [
    rodney.UxCenterlineData(
        'Present (Smagorinsky, nominal)', maindir / 'nominal',
        plt_kwargs=dict(color='C0', zorder=1)
    ),
    rodney.UxCenterlineData(
        'Present (Smagorinsky, fine)', maindir / 'fine',
        plt_kwargs=dict(color='black', zorder=0)
    )
]

times = numpy.round(
    numpy.arange(start=50, stop=150 + 1e-3, step=0.05),
    decimals=2
)

for vel_obj in vel_objs:
    if args.compute:
        vel_obj.compute(times)
        vel_obj.save('u_centerline_profile_50_150.txt')
    else:
        vel_obj.load('u_centerline_profile_50_150.txt')

# Load data from literature.
data = rodney.load_u_centerline_profiles_literature()

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$x / D$')
ax.set_ylabel(r'$<u> / U_\infty$')
U_inf, D = 1.0, 1.0
for vel_obj in vel_objs:
    ax.plot(vel_obj.x / D, vel_obj.values / U_inf,
            label=vel_obj.label, **vel_obj.plt_kwargs)
for i, (label, subdata) in enumerate(data.items(), start=1):
    ax.scatter(*subdata, label=label, s=5, color=f'C{i}', marker='o')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.legend(frameon=False, fontsize=12)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_centerline_profile.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
