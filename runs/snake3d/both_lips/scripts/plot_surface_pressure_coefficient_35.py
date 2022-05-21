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

cases = {'Re=1000': '1k35', 'Re=2000': '2k35', 'Re=3000': '3k35'}

cp_objs = [
    rodney.SurfacePressureData(label, maindir / folder)
    for label, folder in cases.items()
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
pyplot.rc('font', family='serif', size=12)

# Plot the surface pressure coefficient.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$x / c$')
ax.set_ylabel('$C_p$')
wrap = lambda arr: numpy.append(arr, arr[0])
for cp_obj in cp_objs:
    ax.plot(wrap(cp_obj.x), wrap(cp_obj.values), label=cp_obj.label)
ax.legend(loc='lower right', frameon=False, fontsize=12)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'surface_pressure_coefficient_35.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
