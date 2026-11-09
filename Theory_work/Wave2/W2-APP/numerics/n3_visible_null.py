r"""n3_visible_null.py -- visible-null obstruction: V1 (star), V2 (growing equicorrelated blocks), V3 (equicorrelation rho=.3; theta-sum !=0 (V3a) and =0 (V3b)).
n in {800,3200,12800}, p=200, seeds 1..4.  Deviation: V2 n=12800 (block size 113) has only 1 full block at p=200, so the s0=3 'one truth per block' needs p=400:
run V2 n=12800 at p=400 (main) and additionally at p=200 with s0=2 (extra rows, flagged).
Reports start mode, |start \ S0|, #visible nulls in the start mode vs lemma bound min(K-s0, |visible|-16 s0), K=min(p, n//2); LS0 from start with cap ell_cap(n,p)+|start|."""
import sys, os, time, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n0_common import *
from multiprocessing import Pool

NS = (800, 3200, 12800)
SEEDS = (1, 2, 3, 4)
P = 200


def visible_set(did, n, p, S0):
    info = sigma_of(did, n, p)[1]
    if did == "V1":
        return set(info["leaves"])
    if did == "V2":
        sizes = block_sizes(p, info["g"])
        starts = np.cumsum([0] + sizes)
        vis = set()
        for t in S0:
            b = int(np.searchsorted(starts, t, side="right") - 1)
            vis |= set(range(int(starts[b]), int(starts[b + 1])))
        return vis - set(S0)
    return set(range(p)) - set(S0)


def job(args):
    did, n, p, seed, s0 = args
    t0 = time.time()
    D = build_data(did, n, p, seed, s0=s0, tag=4)
    out, mode, blocks, prob = start_and_ls(D, tmax=600.0)
    S0 = D["S0"]
    vis = visible_set(did, n, p, S0)
    nvis_in = len(vis & set(mode))
    K = prob.K
    bound = min(K - len(S0), len(vis) - 16 * len(S0))
    out = dict(design=did, seed=seed, s0=len(S0), S0=json.dumps(list(S0)), n_visible=len(vis), n_visible_in_mode=nvis_in,
               K=K, lemma_bound=bound, bound_met=(nvis_in >= bound), frac_visible_in_mode=nvis_in / max(1, len(vis)),
               **{k: v for k, v in out.items() if k != "K"})
    out["mode"] = json.dumps(list(out["mode"]))
    out["extras"] = json.dumps(out["extras"])
    out["secs"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    t00 = time.time()
    jobs = []
    for n in NS[::-1]:
        for did in ("V1", "V2", "V3a", "V3b"):
            for s in SEEDS:
                if did == "V2" and n == 12800:
                    jobs.append((did, n, 400, s, 3))
                    jobs.append((did, n, 200, s, 2))
                else:
                    jobs.append((did, n, P, s, 1 if did == "V1" else 3))
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        jobs = [("V3a", 800, 200, 1, 3), ("V1", 800, 200, 1, 1)]
    with Pool(7) as pool:
        out = []
        for r in pool.imap_unordered(job, jobs):
            out.append(r)
            print(r["design"], r["n"], r["p"], r["seed"], "mode", r["mode_size"], "extra", r["n_extra"], "vis_in", r["n_visible_in_mode"], "/", r["n_visible"],
                  "bound", r["lemma_bound"], "LS: S0scored", r["ls_S0_scored"], "final==S0", r["ls_final_eq_S0"], "cert", r["ls_certified"],
                  "lim", r["ls_limit"], "TO", r["ls_timed_out"], "moves", r["ls_moves"], "secs", r["secs"], flush=True)
    here = os.path.dirname(os.path.abspath(__file__))
    fn = os.path.join(here, "n3_test.csv" if len(sys.argv) > 1 else "n3_results.csv")
    out.sort(key=lambda r: (r["design"], r["n"], r["p"], r["seed"]))
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print("total secs", round(time.time() - t00, 1))
