"""Plot the mean Strouhal number versus the angle of attack."""

import pathlib

import numpy
from matplotlib import pyplot, text

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

strouhal = dict()
for lip_cfg in cases.keys():
    strouhal[lip_cfg] = dict()
    for Re, angles in cases[lip_cfg].items():
        _strouhal = []
        for AoA in angles:
            coeff_obj = rodney.ForceCoefficientsData(
                None, maindir / lip_cfg / f'{Re}{AoA}'
            )
            if args.compute:
                coeff_obj.compute(Lz=numpy.pi, from_tarball=True)
                coeff_obj.save('force_coefficients.txt')
            else:
                coeff_obj.load('force_coefficients.txt')

            _strouhal.append(coeff_obj.get_strouhal(
                L=1.0, U=1.0, time_limits=(100.0, 200.0), order=100
            ))
        strouhal[lip_cfg][Re] = _strouhal

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot history of the force coefficients.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))

lip_labels = {'both_lips': 'both', 'back_lip': 'back',
              'front_lip': 'front', 'no_lips': 'none'}

ax.set_xlabel('Angle of attack (deg)')
ax.set_ylabel('Strouhal number')
for lip_cfg in cases.keys():
    for Re in cases[lip_cfg].keys():
        label = f'Re={Re}'.replace('k', '000')
        ax.plot(
            cases[lip_cfg][Re], strouhal[lip_cfg][Re], label=label,
            marker='o', markersize=4
        )
ax.set_ylim(0.2, 0.6)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()


class LegendTitle:
    def __init__(self, text_props=None):
        self.text_props = text_props or {}

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        title = text.Text(x0, y0, orig_handle, **self.text_props)
        handlebox.add_artist(title)
        return title


handles_org, labels_org = ax.get_legend_handles_labels()
handles, labels, idx = [], [], 0
for lip_cfg in cases.keys():
    handles.append('\n' + lip_labels[lip_cfg] + ':')
    labels.append('')
    for Re in cases[lip_cfg].keys():
        handles.append(handles_org[idx])
        labels.append(labels_org[idx])
        idx += 1

fig.legend(handles, labels, handler_map={str: LegendTitle()},
           frameon=False, loc='center right')

fig.subplots_adjust(right=0.7)

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'mean_strouhal.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
