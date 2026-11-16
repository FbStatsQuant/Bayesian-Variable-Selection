"""Sanity checks for Lemma T (T.md). DRAFT helper, stream B. Run: python3 check_T.py > check_T_out.txt"""
import numpy as np
from math import comb, log, e, exp, sqrt
from scipy import stats

rng = np.random.default_rng(7)

# 1. constants of Prop. R and of the ratio route
kappa = 2 * (0.5 - 0.2) * (1 - 0.2) / (1.5 - 0.2) ** 2
print(f"[1] kappa(1/5) = {kappa:.6f} = 48/169 = {48/169:.6f} >= 1/4: {kappa >= 0.25}")
print(f"    lower bound for n*eta^2 in Lemma T: 4(1+4log(2e)+log4) = {4*(1+4*log(2*e)+log(4)):.3f} (>= 25 needed)")
print(f"    ratio route, theta=1/7, prefactor 6: n theta^2 eta^2 >= {6*(1+4*log(2*e)+log(4))/49:.3f} (>=1), (1-theta)^2*6/4 = {(6/7)**2*1.5:.4f} (>=1)")

# 2. grid: n*eta^2 >= 25 and all bracket terms >= 0, and Sauer-type bounds
mn = np.inf
for n in [2, 3, 5, 10, 50, 200, 1000]:
    for P in [1, 2, 5, 50, 10**4]:
        for d in range(1, min(P, n - 1) + 1):
            for delta in [0.999, 0.5, 1e-3, 1e-12]:
                L = d * log(e * P / d) + 2 * (d + 1) * log(2 * e * n / (d + 1))
                neta2 = 4 * (L + log(4 / delta))
                mn = min(mn, neta2)
print(f"[2] min n*eta^2 over grid = {mn:.3f} (>= 25 required)")
ok = True
for m in range(1, 60):
    for k in range(1, m + 1):
        Phi = sum(comb(m, i) for i in range(k + 1))
        ok &= Phi <= (e * m / k) ** k * (1 + 1e-12)
print(f"    Phi_k(m) <= (em/k)^k for 1<=k<=m<60: {ok}")

# 3. Monte Carlo of Prop. R on R^1, d = 1, class {|a+ux|>r}: complements of closed intervals (plus empty set / R).
#    sup_A [nu(A) - 2 P_n(A)] = -1 + max_{i<=j} [2(j-i+1)/n - nu[x_(i), x_(j)]]  (continuous law; atoms handled by CDF)
def sup_stat(xs, cdf, cdf_left):
    xs = np.sort(xs); n = len(xs)
    F = cdf(xs); Fl = cdf_left(xs)
    best = -np.inf
    for i in range(n):
        j = np.arange(i, n)
        val = 2 * (j - i + 1) / n - (F[j] - Fl[i])
        best = max(best, val.max())
    return -1 + best

def run(name, sampler, cdf, cdf_left, n, eta2, reps):
    fails = 0
    for _ in range(reps):
        fails += sup_stat(sampler(n), cdf, cdf_left) > eta2
    # growth function of complements of intervals on m points (traces): <= 1 + m + C(m,2) + ... crude S(2n) <= (2n)^2+1
    S2n = (2 * n) ** 2 + 1
    print(f"    {name:8s} n={n:4d} eta^2={eta2:.4f} (n eta^2={n*eta2:5.1f}): empirical P(fail) = {fails/reps:.4f}; Prop.R bound = {min(1,2*S2n*exp(-n*eta2/4)):.3g}")

print("[3] Monte Carlo of the multiplicative inequality (worst set over the class, exact):")
cauchy = (lambda n: rng.standard_cauchy(n), stats.cauchy.cdf, stats.cauchy.cdf)
pois = (lambda n: rng.poisson(0.7, n).astype(float), stats.poisson(0.7).cdf, lambda x: stats.poisson(0.7).cdf(x - 1))
for n in [50, 200]:
    for c in [1.0, 3.0, 6.0, 25.0, 60.0]:
        eta2 = c / n
        run("Cauchy", *cauchy, n, eta2, 300)
        run("Pois0.7", *pois, n, eta2, 300)
