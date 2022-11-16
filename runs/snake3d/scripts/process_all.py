"""Run post-processing scripts."""

import os
import subprocess
from pathlib import Path

pwd = Path(__file__).absolute().parent

scripts = [
    'plot_mean_force_coefficients.py',
    'plot_mean_lift_drag_ratio.py',
    'plot_mean_strouhal.py',
    'plot_force_coefficients_2k25.py',
    'plot_force_coefficients_2k35.py',
    'plot_surface_pressure_coefficient_2k25.py',
    'plot_surface_pressure_coefficient_2k35.py',
    'plot_u_centerline_profile_2k25.py',
    'plot_u_centerline_profile_2k35.py',
    'plot_velocity_profiles_2k25.py',
    'plot_velocity_profiles_2k35.py'
]

for script in scripts:
    print(f'[INFO] Running script {script} ...')
    script = str(pwd / script)
    p = subprocess.Popen(
        f'python {script} --no-compute --no-show', shell=True
    )
    p.communicate()
