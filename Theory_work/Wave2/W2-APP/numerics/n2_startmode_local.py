"""n2_startmode_local.py -- start-mode sandwich and LS0 on local designs L1-L4.
n in {800,3200}, p in {200,400}, seeds 1..6, theta c=1, s0=3 (truths at round(p*(.15,.5,.85)), theta=(1,-.8,1.2)).
Per data set: partition (bc.partition), start mode (bc.start_mode), LS0 = local search from start mode with cap ell_cap(n,p)+|start| (bc.neighbours scoring; ls_timed == bc.local_search + 600s deadline)."""
import sys, os, time, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n0_common import *
from multiprocessing import Pool

DESIGNS = ("L1", "L2", "L3", "L4")
NS = (800, 3200)
PS = (200, 400)
SEEDS = (1, 2, 3, 4, 5, 6)


def job(args):
    did, n, p, seed = args
    t0 = time.time()
    D = build_data(did, n, p, seed, s0=3, tag=3)
    out, mode, blocks, prob = start_and_ls(D, tmax=600.0)
    out = dict(design=did, seed=seed, S0=json.dumps(list(D["S0"])), **out)
    out["mode"] = json.dumps(list(out["mode"]))
    out["extras"] = json.dumps(out["extras"])
    out["secs"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    t00 = time.time()
    jobs = [(d, n, p, s) for n in NS[::-1] for p in PS[::-1] for d in DESIGNS for s in SEEDS]
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        jobs = [("L1", 800, 200, 1)]
    with Pool(7) as pool:
        out = []
        for r in pool.imap_unordered(job, jobs):
            out.append(r)
            print(r["design"], r["n"], r["p"], r["seed"], "S0in", r["S0_in_mode"], "extra", r["n_extra"], "maxd", r["maxdist_extra"],
                  "LS: S0scored", r["ls_S0_scored"], "final==S0", r["ls_final_eq_S0"], "cert", r["ls_certified"], "moves", r["ls_moves"],
                  "secs", r["secs"], flush=True)
    here = os.path.dirname(os.path.abspath(__file__))
    fn = os.path.join(here, "n2_test.csv" if len(sys.argv) > 1 else "n2_results.csv")
    out.sort(key=lambda r: (r["design"], r["n"], r["p"], r["seed"]))
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print("total secs", round(time.time() - t00, 1))
