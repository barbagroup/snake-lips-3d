"""Plot the time-averaged the force coefficients."""

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
        '1k': [25, 30, 35, 40],
        '2k': [20, 25, 30, 35, 40],
        '3k': [20, 25, 30, 35, 40]
    },
    'back_lip': {
        '1k': [25, 30, 35, 40],
        '2k': [20, 25, 30, 35, 40]
    },
    'front_lip': {
        '1k': [25, 30, 35, 40],
        '2k': [20, 25, 30, 35, 40]
    },
    'no_lips': {
        '1k': [25, 30, 35, 40],
        '2k': [20, 25, 30, 35, 40]
    }
}

cd, cl = dict(), dict()
for lip_cfg in cases.keys():
    cd[lip_cfg], cl[lip_cfg] = dict(), dict()
    for Re, angles in cases[lip_cfg].items():
        _cd, _cl = [], []
        for AoA in angles:
            coeff_obj = rodney.ForceCoefficientsData(
                None, maindir / lip_cfg / f'{Re}{AoA}'
            )
            if args.compute:
                coeff_obj.compute(Lz=numpy.pi, from_tarball=True)
                coeff_obj.save('force_coefficients.txt')
            else:
                coeff_obj.load('force_coefficients.txt')
            coeff_stats = coeff_obj.get_stats(time_limits=(100.0, 200.0))
            _cd.append(coeff_stats[0]['mean'])
            _cl.append(coeff_stats[1]['mean'])
        cd[lip_cfg][Re] = _cd
        cl[lip_cfg][Re] = _cl

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot history of the force coefficients.
fig, (ax1, ax2) = pyplot.subplots(figsize=(6.0, 6.0), nrows=2, sharex=True)

labels = {'both_lips': 'both', 'back_lip': 'back',
          'front_lip': 'front', 'no_lips': 'none'}

ax1.set_ylabel('Lift coefficient')
for lip_cfg in cases.keys():
    for Re in cases[lip_cfg].keys():
        label = f'{labels[lip_cfg]}: Re={Re}'
        ax1.plot(
            cases[lip_cfg][Re], cl[lip_cfg][Re], label=label, marker='o'
        )
ax1.set_ylim(0.5, 1.7)
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 1.0, box.height])
ax1.legend(loc='upper left', bbox_to_anchor=(1, 1),
           frameon=False, prop=dict(size=12))
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

ax2.set_xlabel('Angle of attack (deg)')
ax2.set_ylabel('Drag coefficient')
for lip_cfg in cases.keys():
    for Re in cases[lip_cfg].keys():
        label = f'{labels[lip_cfg]}: Re={Re}'
        ax2.plot(
            cases[lip_cfg][Re], cd[lip_cfg][Re], label=label, marker='o'
        )
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
