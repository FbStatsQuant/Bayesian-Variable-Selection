"""Monte Carlo of the ACTUAL v3 partition (fast port, validated against the compiled engine in check_port.py)
at the study sizes n = 200, p in {500, 1000} (B = 14), and in the counterexample regimes.
Per replicate: blocks == groups; blocks are unions of whole groups; dendrogram laminar; local margin (M) holds.
Seeds: 20261102 + hash of the config + rep (fixed). Output: results/sim_partition.jsonl and results/sim_partition.txt
Usage: python3 sim_partition.py [NPROC]"""
import json, math, sys, time, zlib
import numpy as np
from multiprocessing import Pool
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
from scipy.stats import beta as Beta
from part_core import *


def one(args):
    (cfg, rep) = args
    n, p, g, rho, psi, kind, nlink = cfg["n"], cfg["p"], cfg["g"], cfg["rho"], cfg["psi"], cfg["kind"], cfg.get("nlink")
    seed = 20261102 + zlib.crc32(json.dumps(cfg, sort_keys=True).encode()) % 1000003 * 1000 + rep
    rng = np.random.default_rng(seed)
    G = p // g
    X, groups = gen_groups(n, G, g, rho, psi, kind, rng, nlink=nlink)
    p = X.shape[1]  # = G*g (may be < cfg p when g does not divide p)
    B = block_size(n, p)
    r = correlation(X)
    d = 1.0 - np.abs(r); np.fill_diagonal(d, 0.0); d = np.maximum(d, 0.0)
    Z = linkage(squareform(d, checks=False), method="complete")
    T = tree_from_scipy(Z, p)
    blocks, clusters = cut_and_pack(T, p, B)
    lam = laminar(T, p, groups)
    mloc, mglob = margins(r, groups)
    return dict(beq=blocks_equal_groups(blocks, groups), union=blocks_are_group_unions(blocks, groups), lam=lam,
                M=mloc > 0, nblocks=len(blocks), maxblock=max(map(len, blocks)))


CONFIGS = []
def add(reps, **c):
    CONFIGS.append((c, reps))

for p in (500, 1000):
    # the task's family at the study size (B = 14 at n = 200: g in [8, 14])
    for g in (8, 10, 14):
        add(2000 if g == 10 else 500, n=200, p=p, g=g, rho=0.7, psi=0.0, kind="indep")
    for rho in (0.3, 0.35, 0.4, 0.5, 0.85):
        add(300, n=200, p=p, g=10, rho=rho, psi=0.0, kind="indep")
    for c in (1, 2):
        add(2000, n=200, p=p, g=10, rho=0.7, psi=0.5, kind="lh", nlink=c)
    for psi in (0.6, 0.65, 0.7, 0.75):
        add(300, n=200, p=p, g=10, rho=0.7, psi=psi, kind="lh", nlink=2)
    add(1000, n=200, p=p, g=10, rho=0.7, psi=0.5, kind="lh", nlink=None)  # every group linked (G/2 pairs)
    for (rho, psi) in ((0.7, 0.1), (0.7, 0.2), (0.7, 0.3), (0.5, 0.1), (0.5, 0.2)):
        add(300, n=200, p=p, g=10, rho=rho, psi=psi, kind="global")
    # counterexample regimes
    for g in (15, 16):
        add(50, n=200, p=p - p % g, g=g, rho=0.7, psi=0.0, kind="indep")
    add(200, n=200, p=p, g=5, rho=0.7, psi=0.0, kind="indep")   # 2g <= B (study's group size)
# asymptotic direction: LH near the boundary, p ~ n^1.25
for (n, p) in ((200, 750), (400, 1790), (800, 4260)):
    add(200 if n < 800 else 60, n=n, p=p - p % 10, g=10, rho=0.7, psi=0.65, kind="lh", nlink=2)
    add(200 if n < 800 else 60, n=n, p=p - p % 10, g=10, rho=0.4, psi=0.0, kind="indep")


def cp(k, N):
    lo = Beta.ppf(0.025, k, N - k + 1) if k > 0 else 0.0
    hi = Beta.ppf(0.975, k + 1, N - k) if k < N else 1.0
    return lo, hi


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    t0 = time.time()
    lines = ["Actual v3 partition, Monte Carlo. fail = blocks != groups; 95% Clopper-Pearson interval for P(fail).",
             "kind      c   n     p     g   B   rho   psi  | reps | fail (95% CI)               | not union | not laminar | margin(M) fails"]
    with open("../results/sim_partition.jsonl", "w") as fj, Pool(nproc) as pool:
        for (cfg, reps) in CONFIGS:
            res = pool.map(one, [(cfg, r) for r in range(reps)], chunksize=10)
            k = sum(not x["beq"] for x in res); nu = sum(not x["union"] for x in res)
            nl = sum(not x["lam"] for x in res); nm = sum(not x["M"] for x in res)
            lo, hi = cp(k, reps)
            pa = (cfg["p"] // cfg["g"]) * cfg["g"]
            B = block_size(cfg["n"], pa)
            rec = dict(cfg=cfg, reps=reps, B=B, fail=k, not_union=nu, not_laminar=nl, margin_fail=nm, ci=[lo, hi])
            fj.write(json.dumps(rec) + "\n"); fj.flush()
            c = cfg.get("nlink"); c = ("all" if c is None else c) if cfg["kind"] == "lh" else "-"
            lines.append(f"{cfg['kind']:8s} {str(c):3s} {cfg['n']:4d} {pa:6d} {cfg['g']:3d} {B:3d} {cfg['rho']:5.2f} {cfg['psi']:5.2f} | "
                         f"{reps:4d} | {k:4d} ({lo:.2e}, {hi:.2e})   | {nu:4d}      | {nl:4d}        | {nm:4d}")
            print(lines[-1], f"[{time.time()-t0:.0f}s]", flush=True)
    open("../results/sim_partition.txt", "w").write("\n".join(lines) + "\n")
