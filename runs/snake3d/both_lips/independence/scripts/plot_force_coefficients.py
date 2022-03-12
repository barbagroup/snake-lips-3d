"""Plot the history of the force coefficients."""

import pathlib

import numpy
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

coeff_objs = [
    rodney.ForceCoefficientsData('nominal', maindir / '2k35_nominal'),
    rodney.ForceCoefficientsData('fine', maindir / '2k35_fine')
]

for coeff_obj in coeff_objs:
    coeff_obj.compute(Lz=numpy.pi)
    _ = coeff_obj.get_stats(time_limits=(50.0, 100.0), verbose=True)

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot history of the force coefficients.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
for coeff_obj in coeff_objs:
    t, (cd, cl, cz) = coeff_obj.times, coeff_obj.values
    ax.plot(t, cd, label=f'$C_D$ ({coeff_obj.label})')
    ax.plot(t, cl, label=f'$C_L$ ({coeff_obj.label})')
ax.legend(ncol=2, frameon=False)
ax.set_xlim(0.0, 100.0)
ax.set_ylim(-1.5, 2.5)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
