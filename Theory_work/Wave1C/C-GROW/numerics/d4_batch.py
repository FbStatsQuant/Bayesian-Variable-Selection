"""Run D4 fits: python d4_batch.py <workers> <ns> <seeds> ; skips fits whose sum_*.json exists"""
import sys, os, subprocess, time
from concurrent.futures import ThreadPoolExecutor
R = "C:/Program Files/R/R-4.4.1/bin/Rscript.exe"
w = int(sys.argv[1]); ns = [int(x) for x in sys.argv[2].split(",")]; seeds = int(sys.argv[3])
jobs = [(s, n, sd) for sd in range(seeds) for n in ns for s in (2, 5)]
def go(j):
    s, n, sd = j
    if os.path.exists("d4_out/sum_S%d_n%d_s%d.json" % j):
        return
    t = time.time()
    r = subprocess.run([R, "d4_run.R", str(s), str(n), str(sd)], capture_output=True, text=True)
    print(j, round(time.time() - t), "s", r.returncode, (r.stdout.strip().splitlines() or [""])[0], flush=True)
    if r.returncode != 0:
        print("ERR", r.stderr[-500:], flush=True)
with ThreadPoolExecutor(w) as ex:
    list(ex.map(go, jobs))
print("D4 batch done", flush=True)
