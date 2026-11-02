"""W6-FIXREV2: two further T37 checks (seed 20261102).

(A) A-REV2 §4.2 production-table-compatible suppressor variant: n = 100, p = 20, B = 4, groups a = {0..3}, b = {4..7}
    (within-group correlation .99), hub cross-correlation .95 through the hubs 0 and 4
    (Sigma[a,b] = .95 Sigma[a,0] Sigma[4,b]), twelve orthogonal nulls, mu = 3 x0 - 2.8 x4, exact Gram (n-1)Sigma,
    noise orthogonal to all columns with ||e||^2 = n-1 (the noise is not specified in A-REV2; this is my choice).
    Checks: blocks = groups (complete-linkage margins); every nonempty within-block (table) model has F below F(empty);
    the start mode argmax pi_0 is empty (exact, by max-plus convolution over block size profiles); every flip at
    empty is non-improving; F({0,4}) > F(empty); the local search from empty certifies empty (category II).
(B) PHI-REACH without TD'_P (W3-VT37R R3, rebuilt independently): search random small designs for a centre S whose
    greedy path reaches S0 within Phi(S) moves although its first move is not a progress move.
"""
import itertools, json, sys
from math import log
import numpy as np
from core import BVS, frame, phi, is_progress, region

OUT = {}


def variant():
    n, p = 100, 20
    Sig = np.eye(p)
    a, b = list(range(0, 4)), list(range(4, 8))
    for g in (a, b):
        for i in g:
            for j in g:
                if i != j:
                    Sig[i, j] = 0.99
    cross = 0.95 * np.outer(Sig[a, 0], Sig[4, b])
    Sig[np.ix_(a, b)] = cross; Sig[np.ix_(b, a)] = cross.T
    lam = np.linalg.eigvalsh(Sig).min()
    N = n - 1
    G = N * Sig
    th = np.zeros(p); th[0] = 3.0; th[4] = -2.8
    # contrast scale: Y = X th + e, e ⟂ col X, ||e||^2 = N:  X'Y = G th, ||Y||^2 = th'G th + N
    Y2 = float(th @ G @ th) + N
    sy = np.sqrt(Y2 / N)
    m = BVS(G, G @ th / sy, N, n)
    F0 = m.F(())
    # complete-linkage margins: within-group distance 1-.99; minimum cross distance
    d_in = 1 - 0.99
    d_cross = min(1 - abs(Sig[i, j]) for i in a for j in b)
    blocks = [a, b, list(range(8, 12)), list(range(12, 16)), list(range(16, 20))]
    worst_table = -np.inf
    for C in blocks:
        for k in range(1, len(C) + 1):
            for A in itertools.combinations(C, k):
                worst_table = max(worst_table, m.F(A) - F0)
    # start mode: gamma_0(S) = w(|S|) prod_b r_b(S ∩ C_b); r_b = BF. Max-plus over blocks of best log r_b per size.
    best = {0: (0.0, ())}
    for C in blocks:
        per = {}
        for k in range(0, len(C) + 1):
            for A in itertools.combinations(C, k):
                v = m.logBF(A) if A else 0.0
                if k not in per or v > per[k][0]:
                    per[k] = (v, A)
        nb = {}
        for s, (v, S) in best.items():
            for k, (u, A) in per.items():
                if s + k <= m.K and (s + k not in nb or v + u > nb[s + k][0]):
                    nb[s + k] = (v + u, tuple(sorted(S + A)))
        best = nb
    mode = max(best.items(), key=lambda kv: m.lw[kv[0]] + kv[1][0])
    flips = max(m.F(T) - F0 for T in m.neighbours(()) if len(T) == 1)
    ls = m.local_search((), 10)
    res = dict(lambda_min_Sigma=lam, d_within=d_in, d_cross_min=d_cross, blocks_equal_groups=bool(d_cross > d_in),
               max_table_model_gain_over_empty=worst_table, start_mode=list(mode[1][1]),
               best_flip_gain_at_empty=flips, truth_gain_over_empty=m.F((0, 4)) - F0,
               search_from_empty=dict(returned=list(ls['returned']), certified=ls['certified']))
    OUT['production_table_variant'] = res
    return res


def phi_reach(seed=20261102, ndesign=400):
    rng = np.random.default_rng(seed)
    for d in range(ndesign):
        n = int(rng.choice([25, 40])); p = 7
        E = frame(n, p + 1, rng)
        A = rng.standard_normal((p, p)) * 0.7 + np.eye(p)
        X = E[:, :p] @ A.T
        S0 = (0, 1, 2)
        th = rng.choice([-1, 1], 3) * rng.uniform(0.3, 1.0, 3)
        y = X[:, :3] @ th + rng.uniform(0.5, 2.0) * E[:, p]
        m = BVS.from_data(X, y)
        for S in region(p, S0, 2, 2, m.K):
            if S == S0:
                continue
            path = [S]; C = S
            while True:
                T = m.M(C)
                if T is None:
                    break
                path.append(T); C = T
            if C == S0 and len(path) - 1 <= phi(S, S0) and not is_progress(S, path[1], S0):
                res = dict(design=d, n=n, centre=list(S), Phi=phi(S, S0), path=[list(t) for t in path],
                           moves=len(path) - 1, first_move_progress=False,
                           Phi_along_path=[phi(t, S0) for t in path])
                OUT['phi_reach_without_TDP'] = res
                return res
    OUT['phi_reach_without_TDP'] = None
    return None


if __name__ == '__main__':
    for f in (variant, phi_reach):
        r = f(); print(f.__name__, json.dumps(r, default=str))
    with open(sys.argv[1] if len(sys.argv) > 1 else 't37_extra.json', 'w') as fh:
        json.dump(OUT, fh, indent=1, default=str)
