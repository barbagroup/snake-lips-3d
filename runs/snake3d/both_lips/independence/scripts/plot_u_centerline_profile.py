"""Plot the centerline mean streamwise velocity."""

import pathlib

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
        'Base grid', maindir / '2k35_nominal',
        plt_kwargs=dict(color='C0', zorder=1)
    ),
    rodney.UxCenterlineData(
        'Fine grid', maindir / '2k35_fine',
        plt_kwargs=dict(color='black', zorder=0)
    )
]

times = numpy.round(
    numpy.arange(start=50, stop=100 + 1e-3, step=0.05),
    decimals=2
)

for vel_obj in vel_objs:
    if args.compute:
        vel_obj.compute(times, from_tarball=True)
        vel_obj.save('u_centerline_profile_50_100.txt')
    else:
        vel_obj.load('u_centerline_profile_50_100.txt')

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$x / D$')
ax.set_ylabel(r'$<u> / U_\infty$')
U_inf, D = 1.0, 1.0
for vel_obj in vel_objs:
    ax.plot(vel_obj.x / D, vel_obj.values / U_inf,
            label=vel_obj.label, **vel_obj.plt_kwargs)
ax.axhline(y=0.0, color='gray', linestyle='--')
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
