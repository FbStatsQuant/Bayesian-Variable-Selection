"""N4 (falsification for L2/(C1)): exact-Gram compound symmetry, coded partition (bvs_core), start mode vs
S* = [p] minus N0 (N0 = nulls in a block containing all truths). Also checks (FS) for each layout.
Output N4_out.txt"""
import math, json, itertools, numpy as np
import bvs_core as bc, fac_core as fc

def fs_ok(vartheta, rho):
    s0 = len(vartheta); worst = np.inf
    for r in range(1, s0 + 1):
        for V in itertools.combinations(range(s0), r):
            tv = sum(vartheta[i] for i in V); worst = min(worst, abs(tv))
            for l in V:
                for u in range(16):
                    worst = min(worst, abs(vartheta[l] + rho * tv / (1 + (u - 1) * rho)))
    return worst

rows = []
cases = []
for rho in [0.3, 0.7]:
    for (p, n) in [(100, 10**5), (100, 10**7), (200, 10**7), (400, 10**8)]:
        cases.append((rho, p, n, "spread", (2, 26, 53, 75), (1.4, -1.0, 1.8, -1.2)))
        cases.append((rho, p, n, "oneblock", (0, 1, 2, 3), (1.4, -1.0, 1.8, -1.2)))
        cases.append((rho, p, n, "s0=1", (40,), (1.0,)))
for (rho, p, n, name, S0, vals) in cases:
    th = np.zeros(p); th[list(S0)] = vals
    Sigma, Lam, Psi = fc.factor_sigma(p, math.sqrt(rho) * np.ones(p), (1 - rho) * np.ones(p))
    for seed in range(3):
        P = fc.ExactGram(Sigma, th, n, np.random.default_rng(seed + 100), Lam=Lam, Psi=Psi)
        blocks = bc.partition_from_corr(Sigma, bc.block_size(n, p))
        info = bc.start_mode(P, blocks)
        N0 = set()
        for C in blocks:
            if set(S0) <= set(C): N0 |= set(C) - set(S0)
        Sstar = tuple(j for j in range(p) if j not in N0)
        r = dict(rho=rho, p=p, n=n, layout=name, seed=seed, fs_min=round(fs_ok(vals, rho), 4), nblocks=len(blocks),
                 N0=len(N0), start_size=len(info.mode), start_equals_Sstar=(tuple(info.mode) == Sstar), n_optimal=info.n_optimal)
        rows.append(r); print(json.dumps(r), flush=True)
print("start == S*:", sum(r["start_equals_Sstar"] for r in rows), "/", len(rows))
