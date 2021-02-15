"""Compare the history of the force coefficients."""

from matplotlib import pyplot
import numpy
import pathlib

import rodney


rootdir = pathlib.Path(__file__).absolute().parents[1]

case1 = rootdir / 'snake3d2k35_both'
datadir1 = case1 / 'output' / 'LES' / 'postProcessing' / 'forces' / '0'
filepath = datadir1 / 'forces.dat'
t1, fx1, fy1, fz1 = rodney.load_forces_3d(filepath)

case2 = rootdir / 'snake3d2k35_both_fine'
datadir2 = case2 / 'output' / 'LES' / 'postProcessing' / 'forces' / '0'
filepath = datadir2 / 'forces.dat'
t2, fx2, fy2, fz2 = rodney.load_forces_3d(filepath)

# Compute force coefficients.
rho, U_inf, D = 1.0, 1.0, 1.0
Lz = numpy.pi * D  # spanwise length
p_dyn = 0.5 * rho * U_inf * D * Lz  # dynamic pressure
cd1, cl1, cz1 = fx1 / p_dyn, fy1 / p_dyn, fz1 / p_dyn
cd2, cl2, cz2 = fx2 / p_dyn, fy2 / p_dyn, fz2 / p_dyn

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot history of the force coefficients.
fig, ax = pyplot.subplots(figsize=(8.0, 6.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.plot(t1, cd1, label='$C_D$')
ax.plot(t1, cl1, label='$C_L$')
ax.plot(t1, cz1, label='$C_Z$')
ax.plot(t2, cd2, label='$C_D$', linestyle='--')
ax.plot(t2, cl2, label='$C_L$', linestyle='--')
ax.plot(t2, cz2, label='$C_Z$', linestyle='--')
ax.legend(ncol=3, frameon=False)
ax.set_ylim(-2.0, 2.0)
fig.tight_layout()

pyplot.show()
