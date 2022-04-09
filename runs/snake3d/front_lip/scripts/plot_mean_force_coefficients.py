"""Plot the history of the force coefficients."""

import pathlib

import numpy
from matplotlib import markers, pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

cases = {
    '1k': [25, 30, 35, 40],
    '2k': [20, 25, 30, 35, 40],
}

cd, cl = dict(), dict()
for Re, angles in cases.items():
    cd[Re], cl[Re] = [], []
    for AoA in angles:
        coeff_obj = rodney.ForceCoefficientsData(None, maindir / f'{Re}{AoA}')
        if args.compute:
            coeff_obj.compute(Lz=numpy.pi, from_tarball=True)
            coeff_obj.save('force_coefficients.txt')
        else:
            coeff_obj.load('force_coefficients.txt')
        coeff_stats = coeff_obj.get_stats(time_limits=(100.0, 200.0))
        cd[Re].append(coeff_stats[0]['mean'])
        cl[Re].append(coeff_stats[1]['mean'])


# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot history of the force coefficients.
fig, (ax1, ax2) = pyplot.subplots(figsize=(4.0, 6.0), nrows=2, sharex=True)

ax1.set_ylabel('Lift coefficient')
for i, Re in enumerate(cases.keys()):
    ax1.plot(cases[Re], cl[Re], label=f'Re={Re}',
             marker='o', color=f'C{i}', linestyle='-')
ax1.set_ylim(0.5, 1.7)
ax1.legend(loc='upper left', frameon=False, prop={'size': 12})
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

ax2.set_xlabel('Angle of attack (deg)')
ax2.set_ylabel('Drag coefficient')
for i, Re in enumerate(cases.keys()):
    ax2.plot(cases[Re], cd[Re], label=f'Re={Re}',
             marker='o', color=f'C{i}', linestyle='-')
ax2.set_ylim(0.3, 1.4)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'mean_force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
