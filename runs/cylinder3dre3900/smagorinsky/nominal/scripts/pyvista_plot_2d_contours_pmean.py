import pathlib

import numpy
import pyvista

import rodney


def slice_z_center(mesh):
    slice_mesh = mesh.slice(normal='z')
    slice_mesh.translate((0, 0, -slice_mesh.center[-1]), inplace=True)
    return slice_mesh


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
datadir = maindir / 'output' / 'LES-tmp'
figdir = maindir / 'figures'

reader = pyvista.OpenFOAMReader(str(datadir / 'case.foam'))
reader.set_active_time_value(150.0)

mesh = reader.read()
internal_mesh = mesh['internalMesh']

slice_internal_mesh = slice_z_center(internal_mesh)

slice_internal_mesh.set_active_scalars('pMean')

contours = slice_internal_mesh.contour(
    isosurfaces=numpy.linspace(-0.7, 0.5, 20), scalars='pMean'
)

p = pyvista.Plotter(off_screen=not args.show_figures)
p.add_mesh(slice_internal_mesh.outline(), color='k')
p.add_mesh(contours, scalars='pMean', opacity=1.0, cmap='viridis')
p.view_xy()
p.enable_parallel_projection()

kwargs = dict()
if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'pyvista_2d_contours_pmean.png'
    kwargs['screenshot'] = filepath

p.show(**kwargs)
