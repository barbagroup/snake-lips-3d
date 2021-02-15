"""Plot the history of the force coefficients."""

from matplotlib import pyplot
import numpy
import pathlib

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
casedir = maindir / 'output' / 'LES'
figdir = maindir / 'figures'

# Load forces from file.
filepath = casedir / 'postProcessing' / 'forces' / '0' / 'forces.dat'
t, fx, fy, fz = rodney.load_forces_3d(filepath)

# Compute force coefficients.
rho, U_inf, D = 1.0, 1.0, 1.0
Lz = numpy.pi * D  # spanwise length
p_dyn = 0.5 * rho * U_inf * D * Lz  # dynamic pressure
cd, cl, cz = fx / p_dyn, fy / p_dyn, fz / p_dyn

# Compute statistics about force coefficients.
time_limits = (50.0, 150.0)
cd_stats = rodney.get_stats(t, cd, limits=time_limits, verbose=True)
cl_stats = rodney.get_stats(t, cl, limits=time_limits, verbose=True)
cz_stats = rodney.get_stats(t, cz, limits=time_limits, verbose=True)

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot history of the force coefficients.
fig, ax = pyplot.subplots(figsize=(8.0, 6.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.plot(t, cd, label='$C_D$')
ax.plot(t, cl, label='$C_L$')
ax.plot(t, cz, label='$C_Z$')
ax.legend(ncol=3, frameon=False)
ax.set_ylim(-2.0, 2.0)
fig.tight_layout()

if args.save_figures:
    # Save Matplotlib figures.
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    # Display Matplotlib figures.
    pyplot.show()
