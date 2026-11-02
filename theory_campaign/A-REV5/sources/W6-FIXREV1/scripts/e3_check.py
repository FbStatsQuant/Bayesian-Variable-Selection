"""E3(ii) and the q < 1 hypothesis of locked T22(i-a).  Seed 20261103.

Part A: reproduce A-REV1 Sec. 3.3 independently (n = 20, p = 2, orthogonal centred columns, y = x_2,
        singleton blocks, reference {1}).  Uses mpmath at 60 digits for the start law.
Part B: random small instances (p = 2..5, random partitions, every reference S° in Omega):
        (B1) whenever q < 1, check pi0(S°) >= (1-q)^{s+1}/(1+e)^s and 1 - pi0(S°) <= (s+1)q/(1-q) + s e;
        (B2) count cases with q >= 1 in which the unrestricted formula exceeds the true mass (E3(ii) as printed
             would be false there) and cases in which it exceeds 1/2 while pi0(S°) <= 1/2 (the E3 conclusion fails).
"""
import itertools
import json
import math
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from bvs_core import Target, standardise, all_models  # noqa: E402

mp.mp.dps = 60
OUT = {}


def start_law(T):
    models = list(all_models(T.p, T.K))
    lg = [mp.mpf(T.logg0(S)) for S in models]
    m = max(lg)
    Z = mp.fsum(mp.e ** (v - m) for v in lg)
    return {S: mp.e ** (v - m) / Z for S, v in zip(models, lg)}


def agg_quantities(T, ref):
    """q and e of locked T22 (STATEMENT Sec. 1, 'Reference quantities') for the reference ref."""
    p = T.p
    s = len(ref)
    refset = set(ref)
    Ds = []
    emax = 0.0
    for C in T.blocks:
        Ub = sorted(refset & set(C))
        rest = [j for j in C if j not in refset]
        r_Ub = mp.e ** mp.mpf(T.logBF(tuple(Ub)))
        # D_b
        Db = mp.mpf(0)
        for j in range(1, len(rest) + 1):
            a = mp.fsum(mp.e ** mp.mpf(T.logBF(tuple(sorted(Ub + list(V))))) / r_Ub
                        for V in itertools.combinations(rest, j))
            Db = max(Db, (mp.factorial(j) * a) ** (mp.mpf(1) / j))
        Ds.append(Db)
        # e
        for k in range(len(C) + 1):
            for U in itertools.combinations(C, k):
                a = len(set(Ub) - set(U))
                if a == 0:
                    continue
                num = mp.e ** mp.mpf(T.logBF(tuple(sorted(U))))
                den = mp.e ** mp.mpf(T.logBF(tuple(sorted(set(U) | set(Ub)))))
                emax = max(emax, (num / den) ** (mp.mpf(1) / a))
    q = mp.fsum(Ds) / (p - s) if s < p else mp.mpf(0)
    e = 2 * p * emax
    return q, e


# ---------------- Part A ----------------
n, p = 20, 2
rng = np.random.default_rng(20261103)
Z = rng.standard_normal((n, 2))
Z -= Z.mean(axis=0)
Qm, _ = np.linalg.qr(Z)
X = math.sqrt(n - 1) * Qm
y = X[:, 1].copy()
X, y = standardise(X, y)
T = Target(X, y)
pi0 = start_law(T)
q, e = agg_quantities(T, (0,))
s = 1
formula = (1 - q) ** (s + 1) / (1 + e) ** s
mode = max(pi0, key=lambda S: pi0[S])
OUT['partA'] = dict(n=n, p=p, K=T.K, r1=float(mp.e ** T.logBF((0,))), r2=float(mp.e ** T.logBF((1,))),
                    q=float(q), e=float(e), unrestricted_formula=float(formula),
                    pi0_ref=float(pi0[(0,)]), start_mode=[j + 1 for j in mode],
                    x1_dot_x2=float(X[:, 0] @ X[:, 1]))
print('Part A', json.dumps(OUT['partA'], indent=1))

# ---------------- Part B ----------------
rng = np.random.default_rng(20261104)
stats = dict(instances=0, refs=0, q_lt_1=0, ia_viol=0, ia_tail_viol=0, q_ge_1=0,
             q_ge_1_formula_exceeds_mass=0, q_ge_1_formula_gt_half_mass_le_half=0, worst_ia_ratio=None)
worst = math.inf
for it in range(300):
    p = int(rng.integers(2, 6))
    n = int(rng.integers(8, 40))
    Xr = rng.standard_normal((n, p))
    if rng.random() < 0.5:   # correlated designs
        Xr[:, 1:] += rng.uniform(0, 1.5) * Xr[:, [0]]
    beta = rng.standard_normal(p) * rng.uniform(0, 2) * (rng.random(p) < 0.6)
    yr = Xr @ beta + rng.standard_normal(n)
    Xs, ys = standardise(Xr, yr)
    perm = list(rng.permutation(p))
    cuts = sorted(set(int(c) for c in rng.integers(1, p, size=int(rng.integers(0, p)))))
    blocks, prev = [], 0
    for c in cuts + [p]:
        if c > prev:
            blocks.append(sorted(perm[prev:c]))
        prev = c
    T = Target(Xs, ys, blocks=blocks)
    pi0 = start_law(T)
    stats['instances'] += 1
    for ref in all_models(p, T.K):
        stats['refs'] += 1
        q, e = agg_quantities(T, ref)
        s = len(ref)
        f = (1 - q) ** (s + 1) / (1 + e) ** s
        if q < 1:
            stats['q_lt_1'] += 1
            if pi0[ref] < f * (1 - mp.mpf(10) ** -40):
                stats['ia_viol'] += 1
            tail = (s + 1) * q / (1 - q) + s * e
            if 1 - pi0[ref] > tail * (1 + mp.mpf(10) ** -40) + mp.mpf(10) ** -50:
                stats['ia_tail_viol'] += 1
            if f > 0:
                worst = min(worst, float(pi0[ref] / f))
        else:
            stats['q_ge_1'] += 1
            if f > pi0[ref]:
                stats['q_ge_1_formula_exceeds_mass'] += 1
            if f > 0.5 and pi0[ref] <= 0.5:
                stats['q_ge_1_formula_gt_half_mass_le_half'] += 1
stats['worst_ia_ratio'] = worst
OUT['partB'] = stats
print('Part B', json.dumps(stats, indent=1))
with open(__file__.rsplit('/', 2)[0] + '/results/e3_check.json', 'w') as fh:
    json.dump(OUT, fh, indent=1)
