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

cases = ['both_lips/2k30', 'front_lip/2k30', 'back_lip/2k30', 'no_lips/2k30']

cp_objs = [
    rodney.SurfacePressureData(folder, maindir / folder)
    for folder in cases
]

times = numpy.round(
    numpy.arange(start=100, stop=200 + 1e-3, step=0.05),
    decimals=2
)

for cp_obj in cp_objs:
    if args.compute:
        cp_obj.compute(times, from_tarball=True)
        cp_obj.save('surface_pressure_coefficient_100_200.txt')
    else:
        cp_obj.load('surface_pressure_coefficient_100_200.txt')

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot the surface pressure coefficient.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('$x / c$')
ax.set_ylabel('$C_p$')
for cp_obj in cp_objs:
    ax.plot(cp_obj.x, cp_obj.values, label=cp_obj.label)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 1.0, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'surface_pressure_coefficient_2k30.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
