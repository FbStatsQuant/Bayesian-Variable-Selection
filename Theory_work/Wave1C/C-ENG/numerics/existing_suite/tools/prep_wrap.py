# Windows shim for Scripts/SMC_BVS/tests/prepare.py: os.getpriority does not exist, lscpu missing.
import os, sys, runpy, subprocess
os.getpriority = lambda *a, **k: 0          # nice level not available on Windows
os.PRIO_PROCESS = 0
_run = subprocess.run
def run(cmd, *a, **k):
    try: return _run(cmd, *a, **k)
    except FileNotFoundError:
        k.get('stdout') and k['stdout'].write(f'(command not found on Windows: {cmd[0]})\n')
subprocess.run = run
script = sys.argv[1]; sys.argv = [script] + sys.argv[2:]
runpy.run_path(script, run_name='__main__')
