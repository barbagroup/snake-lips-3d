"""Run post-processing scripts."""

import os
import subprocess
from pathlib import Path

pwd = Path(__file__).absolute().parent
os.environ['DISPLAY'] = ':0'

scripts = [
    'pyvista_plot_2d_contours_wz.py',
]

for script in scripts:
    print(f'[INFO] Running script {script} ...')
    script = str(pwd / script)
    p = subprocess.Popen(
        f'python {script} --no-show', shell=True
    )
    p.communicate()
