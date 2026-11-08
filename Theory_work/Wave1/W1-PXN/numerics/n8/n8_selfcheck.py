"""Self-checks for n8_route.py: scorer vs naive, start-mode DP/pi0 vs brute force, partition code path."""
import itertools
import math
import numpy as np
import n8_route as R

rng = np.random.default_rng(1)
n, p = 40, 12
X = rng.standard_normal((n, p))
X[:, 1] += 0.8 * X[:, 0]
X[:, 5] += 0.8 * X[:, 4]
y = 3 * X[:, 0] - 3 * X[:, 4] + 2 * X[:, 9] + rng.standard_normal(n)
Xs, ys = R.standardise(X, y)
sc = R.Scorer(Xs, ys)


def naive_F(S):
    S = list(S)
    k = len(S)
    nn = n
    if k:
        G = Xs[:, S].T @ Xs[:, S]
        z = Xs[:, S].T @ ys
        H = (nn + 1) * G + np.eye(k)
        D = np.linalg.det(H) / np.linalg.det(G + np.eye(k))
        Q = ys @ ys - nn * z @ np.linalg.inv(H) @ z
    else:
        D, Q = 1.0, ys @ ys
    nu = 0.01 + nn / 2
    lm = -0.5 * math.log(D) - nu * math.log(2 * 0.01 + Q)
    lw = math.log(0.5) - (math.lgamma(2 * p) - math.lgamma(k + 1) - math.lgamma(2 * p - k))
    return lw + lm


subs = [tuple(c) for k in range(0, 6) for c in itertools.combinations(range(p), k)]
err = max(abs(sc.F_sets([S])[0] - naive_F(S)) for S in subs[:400])
# F is log w + log m with constants dropped; naive uses the same dropping
print("scorer vs naive max abs err (400 sets):", err)

blocks = [tuple(range(0, 4)), tuple(range(4, 8)), tuple(range(8, 12))]
tables = [R.BlockTable(sc, b, 12) for b in blocks]
S0t, logZ, lw = R.pi0_machinery(sc, tables)
tof = {j: bi for bi, b in enumerate(blocks) for j in b}
K = sc.K
best, bestS, Zs = -np.inf, None, []
allv = {}
for k in range(0, K + 1):
    for S in itertools.combinations(range(p), k):
        lp = lw[k] + sum(tables[tof_b].lookup[tuple(sorted(j for j in S if tof[j] == tof_b))] for tof_b in range(3))
        allv[S] = lp
Zb = np.logaddexp.reduce(list(allv.values()))
Sb = min((S for S, v in allv.items() if v == max(allv.values())), key=lambda s: (len(s), s))
print("DP start mode:", S0t, " brute:", Sb, " same:", S0t == Sb)
print("logZ DP vs brute:", logZ, Zb, " diff", logZ - Zb)
print("log pi0 lookup check:", R.log_pi0(sc, tof, tables, lw, logZ, Sb), allv[Sb] - Zb)
# block table vs scorer (r_b(U) = m(U)/m(empty))
U = (1, 2)
print("table r_b vs scorer:", tables[0].lookup[U], sc.F_sets([U])[0] - sc.F_sets([()])[0] - (R.log_w(2, p) - R.log_w(0, p)))

# partition code path with blocks != groups (g=5 violates SIZE) and truncation
r = R.one_fit(150, 270, 5, 1, 0, 0.7, (0.5,), [1.0], [], 1.0, 0)
print("g=5 path: blocks==groups", r["blocks_eq_groups"], "nblocks", r["nblocks"], "maxblock", r["maxblock"], "trunc", r["truncated"])
