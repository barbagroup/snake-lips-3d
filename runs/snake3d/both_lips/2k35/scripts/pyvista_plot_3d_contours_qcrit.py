import pathlib

import numpy
import pyvista

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
datadir = maindir / 'output' / 'LES'
figdir = maindir / 'figures'

reader = pyvista.OpenFOAMReader(str(datadir / 'case.foam'))
reader.set_active_time_value(150.0)

mesh = reader.read()
internal_mesh = mesh['internalMesh']
internal_mesh.set_active_scalars('U')

internal_mesh = internal_mesh.compute_derivative(
    qcriterion=True, vorticity=True, faster=True, progress_bar=True
)

contours = internal_mesh.contour(
    isosurfaces=(0.1,), scalars='qcriterion', preference='point'
)

filepath = maindir / 'RANS' / 'constant' / 'triSurface' / 'snake.obj'
body = pyvista.get_reader(str(filepath)).read()

p = pyvista.Plotter(off_screen=not args.show_figures)
p.add_mesh(internal_mesh.outline(), color='black')
p.add_mesh(
    contours, scalars='vorticity', component=0,
    opacity=0.25, cmap='viridis', clim=[-5.0, 5.0],
    scalar_bar_args=dict(title='wx')
)
p.add_mesh(body, color='black', opacity=0.5)
p.view_xy()
p.enable_parallel_projection()

kwargs = dict()
if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'pyvista_3d_contours_qcrit.png'
    kwargs['screenshot'] = filepath

p.show(**kwargs)
