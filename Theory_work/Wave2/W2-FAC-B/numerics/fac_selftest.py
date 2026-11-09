"""fac_selftest.py -- checks (a) ExactGram sufficient statistics reproduce bvs_core.Problem on an actual exact-Gram
X (same g, chi); (b) closed-form scan() equals direct scoring for every neighbour on random T."""
import math, numpy as np, itertools
import bvs_core as bc, fac_core as fc

rng = np.random.default_rng(1)
n, p = 60, 20
Sigma, Lam, Psi = fc.s5_sigma(p)
th, S0 = fc.study_layout(p, 1.0, s0=3, step=1)
# (a) actual design
X = bc.exact_gram_design(Sigma, n, rng)
eps = rng.standard_normal(n)
e = eps - eps.mean()
mu = X @ th
yr = mu + e
y = bc.standardize_y(yr)
Pd = bc.Problem(X, y)
g = X.T @ e / math.sqrt(n - 1)
chi = float(e @ e - g @ np.linalg.solve(Sigma, g))
class R:  # fake rng returning g then chi
    def standard_normal(self, k): return np.linalg.solve(np.linalg.cholesky(Sigma), g)
    def chisquare(self, df): return chi
Pe = fc.ExactGram(Sigma, th, n, R())
maxd = 0
for k in range(0, 5):
    for S in itertools.islice(itertools.combinations(range(p), k), 200):
        maxd = max(maxd, abs(Pd.F(S) - Pe.F(S)))
print("(a) max |F_direct - F_exactgram| =", maxd)
# (b) scan vs direct
P = fc.ExactGram(Sigma, th, 400, np.random.default_rng(3), Lam=Lam, Psi=Psi)
worst = 0
for trial in range(30):
    k = int(rng.integers(0, p))
    T = tuple(sorted(rng.choice(p, k, replace=False).tolist()))
    sc = fc.scan(P, T)
    worst = max(worst, abs(sc["FT"] - P.F(T)))
    O = sc["O"]
    if sc["add"] is not None:
        for i, l in enumerate(O):
            worst = max(worst, abs(sc["add"][i] - P.F(tuple(sorted(T + (int(l),))))))
    for i, j in enumerate(T):
        worst = max(worst, abs(sc["del"][i] - P.F(tuple(t for t in T if t != j))))
        for jj, l in enumerate(O):
            ns = tuple(sorted([t for t in T if t != j] + [int(l)]))
            worst = max(worst, abs(sc["swap"][i, jj] - P.F(ns)))
print("(b) max |scan - direct| over all neighbours of 30 random T =", worst)
