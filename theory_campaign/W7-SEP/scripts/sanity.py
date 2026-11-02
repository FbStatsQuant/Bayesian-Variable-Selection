"""W7-SEP sanity: (1) DFS scorer vs dense formula (W4-T38FULL Scorer.logm) on random masks, both designs;
(2) vectorised successor map vs a direct scan for random centres. Seed fixed. Output: sanity.txt"""
import math, numpy as np
from sep_core import *

def dense_logm(d, S):
    n, GX, z, yy = d["n"], d["GX"], d["z"], d["yy"]; nu = 0.01 + n / 2
    if not S: return -nu * math.log(0.02 + yy)
    idx = list(S); GS = GX[np.ix_(idx, idx)]; H = (n + 1) * GS + np.eye(len(idx)); zS = z[idx]
    Q = yy - n * float(zS @ np.linalg.solve(H, zS))
    logD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(GS + np.eye(len(idx)))[1]
    return -0.5 * logD - nu * math.log(0.02 + Q)

rng = np.random.default_rng(7)
lines = []
for design in ("gram", "iid"):
    d = build(make_config("A1"), 400, rng, design)
    lm = all_logm(d); p = d["p"]
    err = max(abs(lm[m] - dense_logm(d, set_of(m, p))) for m in rng.integers(0, 1 << p, 300))
    lines.append(f"{design}: max |DFS - dense| log m over 300 random masks = {err:.2e}")
    sc = scores(d); F = sc["F"]; K = sc["K"]; pc = sc["pc"]
    succ = successor(F, p, K, pc)
    bad = 0
    for C in rng.integers(0, 1 << p, 300):
        S = set(set_of(C, p)); best, bF = C, F[C]
        nbs = [mask_of(S ^ {j}) for j in range(p)] + [mask_of((S - {i}) | {j}) for i in S for j in range(p) if j not in S]
        for m in nbs:
            if pc[m] <= K and F[m] > bF: best, bF = m, F[m]
        bad += best != succ[C]
    lines.append(f"{design}: successor map mismatches over 300 random centres = {bad}")
    # start law sanity: pi0 sums to one and factorises
    lines.append(f"{design}: sum pi0 = {np.exp(sc['log_pi0']).sum():.12f}, sum pi = {np.exp(sc['log_pi']).sum():.12f}")
print("\n".join(lines)); open("sanity.txt", "w").write("\n".join(lines) + "\n")
