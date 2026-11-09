"""n4_start.py -- N4 (falsification for L2/(C1)): exact-Gram S5 (block CS a=.3,b=.4,c=.3,q=5), coded partition
(bvs_core.partition_from_corr), start mode (bvs_core.start_mode) vs S* = [p] minus N0. Layouts: study (truths in
different groups), 'onegroup' (all truths in one group, N0 may be nonempty), s0=1. Uses FAC-B's fac_core.ExactGram
(general scorer) so the block tables are the production ones. Output N4_out.txt"""
import sys, os, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "W2-FAC-B", "numerics"))
import bvs_core as bc, fac_core as fc

rows = []
cases = []
for (p, n) in [(100, 10 ** 6), (100, 10 ** 8), (200, 10 ** 8), (400, 10 ** 8), (400, 10 ** 10)]:
    cases.append((p, n, "study", (2, 26, 53, 75), (1.4, -1.0, 1.8, -1.2)))
    cases.append((p, n, "onegroup", (0, 1, 2, 3), (1.4, -1.0, 1.8, -1.2)))
    cases.append((p, n, "s0=1", (40,), (1.0,)))
    cases.append((p, n, "twoingroup", (5, 6, 53), (1.4, -1.0, 1.8)))
out = []
for (p, n, name, S0, vals) in cases:
    th = np.zeros(p); th[list(S0)] = vals
    Sigma, Lam, Psi = fc.s5_sigma(p)
    for seed in range(3):
        P = fc.ExactGram(Sigma, th, n, np.random.default_rng(seed + 100), Lam=Lam, Psi=Psi)
        blocks = bc.partition_from_corr(Sigma, bc.block_size(n, p))
        info = bc.start_mode(P, blocks)
        N0 = set()
        for C in blocks:
            if set(S0) <= set(C):
                N0 |= set(C) - set(S0)
        Sstar = tuple(j for j in range(p) if j not in N0)
        r = dict(p=p, n=n, layout=name, seed=seed, nblocks=len(blocks), block_sizes=sorted(set(len(C) for C in blocks)),
                 N0=len(N0), start_size=len(info.mode), start_equals_Sstar=(tuple(info.mode) == Sstar), n_optimal=info.n_optimal,
                 missing_from_start=len(set(Sstar) - set(info.mode)), extra_in_start=len(set(info.mode) - set(Sstar)))
        rows.append(r)
        line = json.dumps(r); print(line, flush=True); out.append(line)
summ = f"start == S*: {sum(r['start_equals_Sstar'] for r in rows)} / {len(rows)}; by n: " + \
       ", ".join(f"n={n:.0e}: {sum(r['start_equals_Sstar'] for r in rows if r['n']==n)}/{sum(1 for r in rows if r['n']==n)}" for n in sorted(set(r['n'] for r in rows)))
print(summ); out.append(summ)
open(os.path.join(HERE, "N4_out.txt"), "w").write("\n".join(out) + "\n")
