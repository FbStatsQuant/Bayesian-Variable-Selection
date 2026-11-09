"""N3b: hard corners for L4 (s0 small, rho near 1, p = n/2 - 1, large n), production tie rule, records the best swap
gain relative to F(T) (max_swap_gain) and the NA margin. Output N3b_raw.jsonl"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import json, math
from multiprocessing import Pool
import n3_cs
import cs_core as cc, cs_gain as cg
import numpy as np

def run(job):
    r = n3_cs.run(job)
    # rerun to fetch max_swap_gain (n3_cs.run does not export it)
    rho, n, p, s0, c, kind, seed = job
    rng = np.random.default_rng(10007 * seed + 13)
    P = cc.CS(rho, n3_cs.layouts(p, s0, c, kind), n, rng=rng)
    out = cg.ls0_path_gain(P)
    r["max_swap_gain"] = out["info"].get("max_swap_gain")
    r["ties_lexrule"] = out["info"]["ties"]
    return r

if __name__ == "__main__":
    J = []
    for (rho, s0) in [(0.95, 1), (0.9, 2), (0.99, 1)]:
        for (n, p) in [(100001, 50000), (20001, 10000)]:
            for seed in range(2):
                J.append((rho, n, p, s0, 1.0, "mixed", seed))
    with Pool(6) as pool:
        for r in pool.imap_unordered(run, J):
            with open("N3b_raw.jsonl", "a") as f: f.write(json.dumps(r) + "\n")
