"""Run post-processing scripts."""

import os
import subprocess
from pathlib import Path

pwd = Path(__file__).absolute().parent

scripts = [
    'plot_force_coefficients.py',
    'plot_velocity_profiles.py',
    'plot_surface_pressure_coefficient.py',
    'plot_u_centerline_profile.py'
]

for script in scripts:
    print(f'[INFO] Running script {script} ...')
    script = str(pwd / script)
    p = subprocess.Popen(
        f'python {script} --no-compute --no-show', shell=True
    )
    p.communicate()
