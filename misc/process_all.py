"""Run post-processing scripts."""

import os
import subprocess
from pathlib import Path

pwd = Path(__file__).absolute().parent
os.environ['DISPLAY'] = ':0'

rootdir = pwd.parent

scripts = list((rootdir / 'runs').glob('**/process_all.py'))
scripts += list((rootdir / 'data').glob('**/process_all.py'))

for script in scripts:
    print(f'[INFO] Running script {script} ...')
    p = subprocess.Popen(
        f'python {script}', shell=True
    )
    p.communicate()
