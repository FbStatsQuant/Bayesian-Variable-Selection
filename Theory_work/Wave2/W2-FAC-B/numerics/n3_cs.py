"""N3: compound symmetry, exact Gram, LS0 path from [p] (closed form). Records: pure deletion, final=S0, NA margin,
truth-move margin, swap-vs-delete margin, interval-hole property of the deletion order, ties.
Output N3_raw.jsonl"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import json, math, sys, time
import numpy as np
from multiprocessing import Pool
import cs_core as cc, cs_gain as cg

def layouts(p, s0, c, kind):
    th = np.zeros(p)
    idx = np.linspace(2, p - 3, s0).astype(int)
    if kind == "mixed":
        vals = np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])[np.arange(s0) % 6]
    else:  # aligned signs (strong factor signal)
        vals = np.array([1.4, 1.0, 1.8, 1.2, 0.8, 1.6])[np.arange(s0) % 6]
    th[idx] = c * vals
    return th

def run(job):
    rho, n, p, s0, c, kind, seed = job
    rng = np.random.default_rng(10007 * seed + 13)
    th = layouts(p, s0, c, kind)
    P = cc.CS(rho, th, n, rng=rng)
    t0 = time.time()
    out = cg.ls0_path_gain(P)
    mv = out["moves"]
    S0 = set(P.S0)
    pure = all(m[0] == "-N" for m in mv)
    # interval-hole check over null xi values
    nulls = np.array([j for j in range(p) if j not in S0])
    order = np.argsort(P.xi[nulls]); rank = np.empty(len(nulls), int); rank[order] = np.arange(len(nulls))
    pos = {int(j): int(rank[i]) for i, j in enumerate(nulls)}
    lo = hi = None; interval = True
    for m in mv:
        if m[0] != "-N": interval = False; break
        r = pos[m[1]]
        if lo is None: lo = hi = r
        elif r == lo - 1: lo = r
        elif r == hi + 1: hi = r
        else: interval = False; break
    inf = out["info"]
    return dict(rho=rho, n=n, p=p, s0=s0, c=c, kind=kind, seed=seed, A=math.log(p) / math.log(n),
                moves=len(mv), pure_deletion=pure, final_is_S0=out["final_is_S0"], interval_hole=interval,
                max_add_gain_over_logn=inf["max_add_gain_over_logn"], max_swap_minus_del=inf["max_swap_minus_del"],
                min_del_gain=inf["min_del_gain"], max_truth_move=inf["max_truth_move"], ties=inf["ties"],
                t=round(time.time() - t0, 1))

if __name__ == "__main__":
    J = []
    for rho in [0.3, 0.7, 0.95]:
        for s0 in [1, 4]:
            for kind in ["mixed", "aligned"]:
                if s0 == 1 and kind == "aligned": continue
                for n, p in [(10**4, 100), (10**4, 4999), (10**5, 1000), (10**5, 20000), (10**6, 5000), (10**8, 2000), (10**8, 20000), (4001, 2000)]:
                    for c in ([1.0] if p >= 20000 else [1.0, 0.25]):
                        for seed in range(2 if p >= 20000 else 4):
                            J.append((rho, n, p, s0, c, kind, seed))
    J.sort(key=lambda j: -j[2])
    print(len(J), "jobs", flush=True)
    with Pool(7) as pool:
        for r in pool.imap_unordered(run, J):
            with open("N3_raw.jsonl", "a") as f:
                f.write(json.dumps(r) + "\n")
    print("done", flush=True)
