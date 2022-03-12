"""Plot the surface pressure coefficient."""

import pathlib

import numpy
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

cp_obj = rodney.SurfacePressureData('Present', maindir,
                                    plt_kwargs=dict(color='black'))

if args.compute:
    cp_obj.compute(time_limits=(50.0, 100.0))
    cp_obj.save('surface_pressure_coefficient_50_100.txt')
else:
    cp_obj.load('surface_pressure_coefficient_50_100.txt')

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot the surface pressure coefficient.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$x / c$')
ax.set_ylabel('$C_p$')
ax.plot(cp_obj.x, cp_obj.values, **cp_obj.plt_kwargs)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'surface_pressure_coefficient.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
