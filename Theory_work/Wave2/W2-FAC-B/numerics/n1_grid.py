"""N1 grid driver (parallel). Output N1_raw.csv (one row per data set)."""
import os
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import csv, json, sys, time
from multiprocessing import Pool
import n1_run

def jobs():
    J = []
    for name in ["S5", "F10.3", "F10.6", "F2"]:
        for p in [100, 200, 400]:
            for n in [int(1.5 * p), 2 * p, 3200, 10000, 100000, 1000000, 100000000]:
                if n < p + 2: continue
                for c in [1.0, 0.5]:
                    ns = 5 if p < 400 else 3
                    if p == 400 and name not in ("S5", "F10.3"): ns = 2
                    for sd in range(ns):
                        J.append((name, p, c, n, sd))
    J.sort(key=lambda j: -j[1])  # big first
    return J

def one(j):
    try:
        return n1_run.run(*j)
    except Exception as e:
        return dict(design=j[0], p=j[1], c=j[2], n=j[3], seed=j[4], error=repr(e))

if __name__ == "__main__":
    out = "N1_raw.csv"
    J = jobs()
    print(len(J), "jobs", flush=True)
    rows = []
    t0 = time.time()
    with Pool(7) as pool:
        for r in pool.imap_unordered(one, J):
            rows.append(r)
            with open("N1_raw.jsonl", "a") as f:
                f.write(json.dumps(r) + "\n")
    keys = []
    for r in rows:
        for k in r:
            if k not in keys: keys.append(k)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    print("done", time.time() - t0, flush=True)
