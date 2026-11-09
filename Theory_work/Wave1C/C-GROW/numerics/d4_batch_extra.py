"""targeted D4 fits on the p = 100 data sets where the Python search found a model better than S0 (S2 n=200 seed 19; S5 n=200 seed 12)"""
import subprocess
from concurrent.futures import ThreadPoolExecutor
R = "C:/Program Files/R/R-4.4.1/bin/Rscript.exe"
J = [(2, 200, 19), (5, 200, 12)]
def go(j):
    r = subprocess.run([R, "d4_run.R"] + [str(x) for x in j], capture_output=True, text=True)
    print(j, r.returncode, (r.stdout.strip().splitlines() or [""])[:2], flush=True)
with ThreadPoolExecutor(2) as ex:
    list(ex.map(go, J))
