"""Plot the history of the force coefficients."""

import pathlib

import numpy
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

cases = {
    'both_lips': {
        '2k': [25]
    },
    'front_lip': {
        '2k': [25]
    },
    'back_lip': {
        '2k': [25]
    },
    'no_lips': {
        '2k': [25]
    }
}

data = dict()
for lip_cfg in cases.keys():
    for Re, angles in cases[lip_cfg].items():
        for AoA in angles:
            coeff_obj = rodney.ForceCoefficientsData(
                None, maindir / lip_cfg / f'{Re}{AoA}'
            )
            if args.compute:
                coeff_obj.compute(Lz=numpy.pi, from_tarball=True)
                coeff_obj.save('force_coefficients.txt')
            else:
                coeff_obj.load('force_coefficients.txt')
            data[f'{lip_cfg}_{Re}{AoA}'] = coeff_obj

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot history of the force coefficients.
fig, (ax1, ax2) = pyplot.subplots(figsize=(8.0, 6.0), nrows=2)

ax1.set_ylabel('Lift coefficient')
for key, d in data.items():
    ax1.plot(d.times, d.values[1], label=key)
ax1.set_xlim(100.0, 200.0)
ax1.set_ylim(0.4, 2.2)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

ax2.set_xlabel('Non-dimensional time')
ax2.set_ylabel('Drag coefficient')
for key, d in data.items():
    ax2.plot(d.times, d.values[0], label=key)
ax2.set_xlim(100.0, 200.0)
ax2.set_ylim(0.4, 1.2)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

handles, labels = ax1.get_legend_handles_labels()
labels = ['both', 'front', 'back', 'none']
fig.legend(handles=handles, labels=labels, loc='upper center',
           ncol=len(labels), frameon=False, fontsize=12)

fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients_2k25.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
