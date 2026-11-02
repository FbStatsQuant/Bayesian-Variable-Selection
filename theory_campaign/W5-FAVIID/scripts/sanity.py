"""Sanity and lemma checks for W5-FAVIID. Seed 20261102. Output: results/sanity.txt
(1) FastTables == pxn_core.Tables; brute-force pi0 == convolution pi0 (p = 12).
(2) Lemma X+ (one-sided chain-free table bound): R+ := log r(A) - log r(U) + (j/2)log(n+1) + nu log(RSS_A/RSS_U)
    satisfies R+ <= kappa+ := j(1+phi^-2)/(2 phi^2 (n-1)) + nu/((n+1) phi^2 RSS^y_U), phi^2 = lambda_min(R_A).
(3) Lemma M (Mittag-Leffler constant): min_c c E_{1/2}(1/c).
(4) Lemma S (subspace-sum inequality) on random near-orthogonal subspaces.
(5) Lemma B' (exact Beta law, conditioning set = own-group truth + a co-blocked truth W): KS test.
"""
import itertools, math, sys
import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar
from scipy.special import logsumexp
import pxn_core as pc
import fav_core as fc

rng = np.random.default_rng(20261102)
out = []
P = lambda *a: out.append(" ".join(str(x) for x in a))

# (1)
n, p = 40, 12
X = rng.standard_normal((n, p)) @ np.linalg.cholesky(0.5 * np.eye(p) + 0.5 * np.ones((p, p))).T
y = X[:, :3] @ np.array([1.0, -0.7, 0.5]) + rng.standard_normal(n)
D = pc.Data(X, y)
blocks = [list(range(0, 5)), list(range(5, 9)), list(range(9, 12))]
T1, T2 = pc.Tables(D, blocks), fc.FastTables(D, blocks)
P("(1) max|FastTables - Tables| =", max(np.abs(a - b).max() for a, b in zip(T1.lr, T2.lr)))
SL = pc.StartLaw(T2)
allS = [S for k in range(D.K + 1) for S in itertools.combinations(range(p), k)]
lg = np.array([pc.log_w(len(S), p) + T2.log_r(S) for S in allS])
lZ = logsumexp(lg)
P("(1) |logZ brute - logZ conv| =", abs(lZ - SL.logZ))

# (2) Lemma X+
worst, cnt = -np.inf, 0
for rep in range(300):
    n = int(rng.choice([30, 60, 200]))
    p = 10
    rho = rng.uniform(0, 0.9)
    X = rng.standard_normal((n, p)) * math.sqrt(1 - rho) + math.sqrt(rho) * rng.standard_normal((n, 1))
    th = rng.standard_normal(p) * rng.choice([0.1, 1, 5]) * (rng.uniform(size=p) < 0.4)
    y = X @ th + rng.standard_normal(n) * rng.choice([0.2, 1.0])
    D = pc.Data(X, y)
    G = D.X.T @ D.X
    for _ in range(20):
        k = rng.integers(0, 6)
        U = sorted(rng.choice(p, size=k, replace=False).tolist())
        rest = [j for j in range(p) if j not in U]
        j = int(rng.integers(1, min(5, len(rest)) + 1))
        A = sorted(U + rng.choice(rest, size=j, replace=False).tolist())
        lrA, lrU = pc.log_bf_sets(D, [A, U])
        def rss(S):
            if not S:
                return float(D.y @ D.y)
            XS = D.X[:, S]
            b = np.linalg.lstsq(XS, D.y, rcond=None)[0]
            r = D.y - XS @ b
            return float(r @ r)
        rA, rU = rss(A), rss(U)
        Rp = lrA - lrU + 0.5 * j * math.log(n + 1) + D.nu * math.log(rA / rU)
        phi2 = np.linalg.eigvalsh(G[np.ix_(A, A)] / (n - 1)).min()
        kap = j * (1 + 1 / phi2) / (2 * phi2 * (n - 1)) + D.nu / ((n + 1) * phi2 * rU)
        worst = max(worst, Rp - kap)
        cnt += 1
P("(2) Lemma X+: max over %d (U,A) pairs of R+ - kappa+ =" % cnt, worst, "(must be <= 0)")

# (3)
res = minimize_scalar(fc.ml_const, bounds=(0.5, 5), method="bounded")
P("(3) min_c c*E_{1/2}(1/c) = %.4f at c = %.3f; at c=1.7: %.4f" % (res.fun, res.x, fc.ml_const(1.7)))
# brute check of the scalar inequality max_j Y_j <= lam(1+sum (Y_j/lam)^j)
Ys = rng.exponential(size=(10000, 6)) * 3
lam = 1.3
lhs = Ys.max(1)
rhs = lam * (1 + ((Ys / lam) ** np.arange(1, 7)).sum(1))
P("(3) scalar inequality violations:", int((lhs > rhs + 1e-12).sum()))

# (4) Lemma S
viol = 0
for rep in range(2000):
    nn, m = 50, int(rng.integers(2, 5))
    dims = rng.integers(1, 4, size=m)
    bases = [np.linalg.qr(rng.standard_normal((nn, d)))[0] for d in dims]
    # make them near-orthogonal sometimes
    if rep % 2:
        Q = np.linalg.qr(rng.standard_normal((nn, int(dims.sum()))))[0]
        o = 0
        for i, d in enumerate(dims):
            bases[i] = np.linalg.qr(Q[:, o:o + d] + 0.1 * rng.standard_normal((nn, d)))[0]
            o += d
    c = max(np.linalg.norm(bases[i].T @ bases[k], 2) for i in range(m) for k in range(m) if i != k)
    if (m - 1) * c >= 1:
        continue
    r = rng.standard_normal(nn)
    Ball = np.linalg.qr(np.hstack(bases))[0]
    lhs = np.sum((Ball.T @ r) ** 2)
    rhs = sum(np.sum((Bq.T @ r) ** 2) for Bq in bases) / (1 - (m - 1) * c)
    viol += lhs > rhs * (1 + 1e-10)
P("(4) Lemma S violations:", viol)

# (5) Lemma B': group K = {0..4} with truth 0, W = {5} truth of another group; V = {1,2}; S3-like
for (Vset, Wset, lab) in [([1, 2], [5], "own truth + co-blocked truth"), ([11, 12, 13], [0, 5], "null group, two co-blocked truths"),
                          ([3], [], "own truth only")]:
    vals = []
    n = 120
    for rep in range(1500):
        X = fc.gen_raw_X(3, n, 20, rng)
        th = np.zeros(20); th[[0, 5, 16]] = [1.4, -1.0, 1.8]
        # generator convention: signal on standardised columns
        Xs = (X - X.mean(0)) / X.std(0, ddof=1)
        yr = Xs @ th + rng.standard_normal(n)
        Y = yr - yr.mean()
        Xc = X - X.mean(0)
        U = ([0] if lab != "null group, two co-blocked truths" else []) + Wset
        def rss(S):
            if not S:
                return float(Y @ Y)
            b = np.linalg.lstsq(Xc[:, S], Y, rcond=None)[0]
            r = Y - Xc[:, S] @ b
            return float(r @ r)
        vals.append(1 - rss(U + Vset) / rss(U))
    a, b = len(Vset) / 2, (n - 1 - len(U) - len(Vset)) / 2
    P("(5) Lemma B' (%s): KS p-value vs Beta(%.1f, %.1f) = %.3f" % (lab, a, b, stats.kstest(vals, stats.beta(a, b).cdf).pvalue))

open("../results/sanity.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
