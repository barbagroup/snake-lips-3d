"""Create 3D snake cylinder coordinates and output in OBJ format."""

import pathlib

import petibmpy
from rodney import DATADIR

# Set directories.
casedir = pathlib.Path(__file__).absolute().parents[1]
outdir = casedir / 'RANS' / 'constant' / 'triSurface'
outdir.mkdir(parents=True, exist_ok=True)

# Load input coordinates from file.
filepath = DATADIR / 'snake_nofrontlip.txt'
x, y = petibmpy.read_body(filepath, skiprows=1)

# Regularize and rotate geometry.
x, y = petibmpy.regularize2d(x, y, N=500)
x, y = petibmpy.rotate2d(x, y, center=(0.0, 0.0), angle=-25.0)

num = x.size

filepath = outdir / 'snake.obj'
header = ('# Wavefront OBJ file\n'
          f'# points: {2 * num}\n'
          f'# faces: {2 * num}\n'
          '# zones: 1\n'
          '# Regions: 0 snake\n')

zlims = (-1.6, 1.6)

with open(filepath, 'w') as outfile:
    outfile.write(header)
    # Write vertices.
    for zi in zlims:
        for xi, yi in zip(x, y):
            outfile.write(f'v {xi} {yi} {zi}\n')
    # Write group name.
    outfile.write('g snake\n')
    # Write faces.
    for i in range(1, num):
        i1, i2, i3, i4 = i, i + 1, num + i, num + i + 1
        outfile.write(f'f {i} {num + i} {i + 1}\n')
        outfile.write(f'f {i + 1} {num + i} {num + i + 1}\n')
    outfile.write(f'f {num} {2 * num} {1}\n')
    outfile.write(f'f {1} {2 * num} {num + 1}\n')
