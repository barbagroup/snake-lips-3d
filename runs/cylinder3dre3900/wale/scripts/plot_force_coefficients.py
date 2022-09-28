"""Plot the history of the force coefficients."""

import pathlib

import numpy
import pandas
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

coeff_objs = [
    rodney.ForceCoefficientsData('Base grid',
                                 maindir / 'fine',
                                 plt_kwargs=dict(color='C0', zorder=1)),
    rodney.ForceCoefficientsData('Coarse grid',
                                 maindir / 'nominal',
                                 plt_kwargs=dict(color='black', zorder=0))
]

df = pandas.DataFrame(columns=['Case', '<C_D>', 'rms(C_L)'])

for coeff_obj in coeff_objs:
    coeff_obj.compute(Lz=numpy.pi)
    data = coeff_obj.get_stats(time_limits=(50.0, 150.0))
    df.loc[len(df)] = [coeff_obj.label, data[0]['mean'], data[1]['rms']]

print(df.set_index('Case').round(decimals=2))

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot history of the force coefficients.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
for coeff_obj in coeff_objs:
    t, (cd, cl, cz) = coeff_obj.times, coeff_obj.values
    ax.plot(t, cd, label=coeff_obj.label, **coeff_obj.plt_kwargs)
    ax.plot(t, cl, label=None, **coeff_obj.plt_kwargs)
ax.annotate('$C_D$', xy=(90.0, 1.2), xytext=(100.0, 1.5),
            arrowprops=dict(arrowstyle='->'))
ax.annotate('$C_L$', xy=(90.0, 0.5), xytext=(100.0, 0.75),
            arrowprops=dict(arrowstyle='->'))
ax.legend(frameon=False, fontsize=12)
ax.set_xlim(0.0, 150.0)
ax.set_ylim(-2.0, 2.0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
