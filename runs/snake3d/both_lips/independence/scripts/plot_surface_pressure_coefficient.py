"""Plot the surface pressure coefficient."""

import pathlib

import numpy
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

cp_objs = [
    rodney.SurfacePressureData('Base grid',
                               maindir / '2k35_nominal',
                               plt_kwargs=dict(color='C0', zorder=1)),
    rodney.SurfacePressureData('Fine grid',
                               maindir / '2k35_fine',
                               plt_kwargs=dict(color='black', zorder=0))
]

times = numpy.round(
    numpy.arange(start=50, stop=100 + 1e-3, step=0.05),
    decimals=2
)

for cp_obj in cp_objs:
    if args.compute:
        cp_obj.compute(times, from_tarball=True)
        cp_obj.save('surface_pressure_coefficient_50_100.txt')
    else:
        cp_obj.load('surface_pressure_coefficient_50_100.txt')

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot the surface pressure coefficient.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$x / c$')
ax.set_ylabel('$C_p$')
for cp_obj in cp_objs:
    ax.plot(cp_obj.x, cp_obj.values, label=cp_obj.label,
            **cp_obj.plt_kwargs)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.legend(frameon=False, fontsize=12)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'surface_pressure_coefficient.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
