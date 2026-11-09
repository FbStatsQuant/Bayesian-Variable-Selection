"""Validate pathsim: (1) Model.F against dense marginal-likelihood formulas on an explicit exact-CS design;
(2) pathsim.run best-move reduction against a brute-force complete flip/swap scan (all moves, incl. truth)."""
import math, json, sys
import numpy as np
from pathsim import Model, run

out = {}

# (1) dense check
def dense_F(X, y, U, n, p):
    k = len(U)
    lw = -math.log(2) - (math.lgamma(2 * p) - math.lgamma(k + 1) - math.lgamma(2 * p - k))
    if k == 0:
        return lw - (0.01 + n / 2) * math.log(0.02 + y @ y)
    XU = X[:, U]; G = XU.T @ XU; z = XU.T @ y
    H = (n + 1) * G + np.eye(k)
    Q = y @ y - n * z @ np.linalg.solve(H, z)
    L = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(k))[1]
    return lw - L / 2 - (0.01 + n / 2) * math.log(0.02 + Q)

errs = []
for (n, c, s0, seed) in [(60, .7, 1, 0), (60, .7, 2, 1), (80, .9, 2, 2)]:
    m = Model(n, c, s0, seed); p = m.p; h = n - 1
    rng = np.random.default_rng(100 + seed)
    A = rng.standard_normal((n, n)); A -= A.mean(0)
    Qm, _ = np.linalg.qr(np.column_stack([np.ones(n), A[:, :n - 1]]))
    B = Qm[:, 1:p + 1]; R = Qm[:, p + 1:]
    Sig = 0.5 * np.eye(p) + 0.5 * np.ones((p, p))
    ev, V = np.linalg.eigh(Sig); Sh = V @ np.diag(np.sqrt(ev)) @ V.T
    X = math.sqrt(h) * B @ Sh
    g = (m.eta + m.xi) / math.sqrt(2)
    u = R @ rng.standard_normal(R.shape[1]); u *= math.sqrt(m.r) / np.linalg.norm(u)
    e = X @ np.linalg.solve(Sig, g) / math.sqrt(h) + u
    theta = np.zeros(p); theta[:s0] = 1
    Y = X @ theta + e; s = math.sqrt(Y @ Y / h); y = Y / s
    assert abs(s - m.s) < 1e-9 * s, (s, m.s)
    for trial in range(30):
        k = int(rng.integers(0, m.K + 1))
        U = sorted(rng.choice(p, size=k, replace=False).tolist())
        W1 = float(m.w[U].sum()); W2 = float((m.w[U] ** 2).sum())
        errs.append(abs(dense_F(X, y, U, n, p) - m.F(k, W1, W2)))
out['dense_max_abs_err'] = max(errs)

# (2) brute-force path comparison
def brute(m):
    s0, K, p = m.s0, m.K, m.p
    T = sorted(m.start()); moves = []
    Fc = m.F(len(T), m.w[T].sum(), (m.w[T] ** 2).sum())
    while True:
        k = len(T); Tset = set(T); outs = [j for j in range(p) if j not in Tset]
        W1 = m.w[T].sum(); W2 = (m.w[T] ** 2).sum()
        best = (0.0, None)
        for j in T:
            v = m.F(k - 1, W1 - m.w[j], W2 - m.w[j] ** 2) - Fc
            if v > best[0]: best = (v, ('d' if j >= s0 else 'D_truth', j, None))
        if k < K:
            for l in outs:
                v = m.F(k + 1, W1 + m.w[l], W2 + m.w[l] ** 2) - Fc
                if v > best[0]: best = (v, ('a', None, l))
        wo = m.w[outs]
        for j in T:
            vals = np.array([m.F(k, W1 - m.w[j] + x, W2 - m.w[j] ** 2 + x * x) for x in wo]) - Fc
            i = int(np.argmax(vals))
            if vals[i] > best[0]: best = (vals[i], ('s' if j >= s0 else 'S_truth', j, outs[i]))
        if best[1] is None: break
        typ, j, l = best[1]; moves.append((typ, j, l, best[0]))
        if j is not None: T.remove(j)
        if l is not None: T.append(l)
        T.sort(); Fc = m.F(len(T), m.w[T].sum(), (m.w[T] ** 2).sum())
    return moves

cmp = []
for (n, c, s0, seed) in [(120, .6, 1, 0), (120, .85, 2, 1), (160, .75, 1, 2), (160, .95, 2, 3), (200, .7, 2, 4), (200, .9, 1, 5)]:
    m = Model(n, c, s0, seed)
    bm = brute(m)
    r = run(m)
    fm = [(e[1], ) for e in r['events']]
    same = len(bm) == len(r['events']) and all(a[0] == b[1] and abs(a[3] - b[5]) < 1e-6 for a, b in zip(bm, r['events']))
    cmp.append(dict(n=n, c=c, s0=s0, seed=seed, brute_moves=len(bm), sim_moves=r['moves'], identical=bool(same),
                    brute_types={t: sum(1 for x in bm if x[0] == t) for t in set(x[0] for x in bm)}))
out['brute_vs_sim'] = cmp
print(json.dumps(out, indent=1))
