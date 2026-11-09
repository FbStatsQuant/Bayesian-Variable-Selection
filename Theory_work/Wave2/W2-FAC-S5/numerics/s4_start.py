"""S4 (falsification for L2/(C1) on block compound symmetry): exact-Gram S5 (and a second BCS), the coded partition and
start-mode routine of FACB numerics (bvs_core, copied unchanged from C-GROW), start mode vs S* = [p] minus N0."""
import sys, math, json, numpy as np
sys.path.insert(0, "../../W2-FAC-B/numerics")
import bvs_core as bc, fac_core as fc

def bcs_sigma(p, q, rb, rw):
    grp = np.arange(p) // q
    S = rb + (rw - rb) * (grp[:, None] == grp[None, :]) + (1 - rw) * np.eye(p)
    Lam = math.sqrt(rb) * np.ones((p, 1)); Psi = S - Lam @ Lam.T
    return S, Lam, Psi

rows = []
for (q, rb, rw) in [(5, .3, .7), (3, .2, .6)]:
    for (p, n) in [(100, 10**6), (200, 10**8), (400, 10**8)]:
        for name, S0, vals in [("spread", (2, 26, 53, 75), (1.4, -1.0, 1.8, -1.2)),
                               ("onegroup", (0, 1), (1.4, -1.0)), ("s0=1", (40,), (1.0,))]:
            th = np.zeros(p); th[list(S0)] = vals
            Sigma, Lam, Psi = bcs_sigma(p, q, rb, rw)
            for seed in range(2):
                P = fc.ExactGram(Sigma, th, n, np.random.default_rng(seed + 200), Lam=Lam, Psi=Psi)
                blocks = bc.partition_from_corr(Sigma, bc.block_size(n, p))
                info = bc.start_mode(P, blocks)
                N0 = set()
                for C in blocks:
                    if set(S0) <= set(C): N0 |= set(C) - set(S0)
                Sstar = tuple(j for j in range(p) if j not in N0)
                r = dict(q=q, rb=rb, rw=rw, p=p, n=n, layout=name, seed=seed, nblocks=len(blocks), N0=len(N0),
                         start_size=len(info.mode), start_equals_Sstar=(tuple(info.mode) == Sstar), n_optimal=info.n_optimal)
                rows.append(r); print(json.dumps(r), flush=True)
print("start == S*:", sum(r["start_equals_Sstar"] for r in rows), "/", len(rows))
