"""Create 3D snake cylinder coordinates and output in OBJ format.

* Inputs: None
* Outputs: RANS/constant/triSurface/snake.obj

"""

import numpy
import pathlib

import petibmpy


casedir = pathlib.Path(__file__).absolute().parents[1]
outdir = casedir / 'RANS' / 'constant' / 'triSurface'
outdir.mkdir(parents=True, exist_ok=True)

# Create circle.
R = 0.5  # radius
xc, yc = 0.0, 0.0  # center
theta = numpy.linspace(0.0, 2 * numpy.pi, num=500)[:-1]
x, y = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

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
