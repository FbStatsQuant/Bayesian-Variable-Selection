"""Lemma B (W3-PXN): exact Beta laws of start statistics on LH-iid, independent of y. KS tests with 2000 reps each,
plus two negative controls that the lemma does NOT cover (must be rejected: power check), plus the same tests at
psi = 0.9 > rho (Lemma B's population identities do not need |psi| < rho; only the partition does).

Design: G = 8 groups of g = 10, rho = 0.7; pairs (0,1) and (2,3) with betas (1, -1); visible group 4 (beta 1);
groups 5-7 null; n = 120; sigma = 1. Seed 9100 + 1000*psi_index.
Statistics (RSS-based, standardised columns, centred y; U = conditioning set):
  B1  b-group, U = {}, V = {j_b, k}                       ~ Beta(1, (n-1-2)/2)
  B2  a-group, U = {j_a}, V = 3 non-hubs                   ~ Beta(3/2, (n-1-1-3)/2)
  B3  visible, U = {j_h}, V = 2 non-hubs                   ~ Beta(1, (n-1-1-2)/2)
  B4  null group, U = {}, V = all 10                       ~ Beta(5, (n-1-10)/2)
  B5  case beta: A = S° u {a1 non-hub, vis non-hub, null}, l = another a1 non-hub ~ Beta(1/2, (n-2-|A|)/2)
  B6  case beta: same A, l = a non-hub of the OTHER pair's a-group               ~ Beta(1/2, (n-2-|A|)/2)
  B7  masked hub j_b1: r^2(j_b1, y)                         ~ Beta(1/2, (n-2)/2); and independence of the two
      masked hubs (chi-square test on 5x5 quantile cells of (r1^2, r2^2))
  N1  CONTROL a-group non-hub, U = {} (signal-correlated)   tested against Beta(1/2, (n-2)/2): should reject
  N2  CONTROL proxy l in C_b1 minus j_b1 given A = S°       tested against Beta(1/2, (n-2-|S°|)/2): should reject
Output: ../results/ks_lemmaB.txt
"""
import math
import numpy as np
from scipy import stats
from vm_core import lh_spec, gen_lh_iid, standardise


def rss(X, y, T):
    if not T:
        return float(y @ y)
    XT = X[:, T]
    b, *_ = np.linalg.lstsq(XT, y, rcond=None)
    r = y - XT @ b
    return float(r @ r)


def frac(X, y, U, V):
    return 1 - rss(X, y, U + V) / rss(X, y, U)


n, G, g, reps = 120, 8, 10, 2000
lines = []
for pi, psi in enumerate([0.5, 0.9]):
    units, theta, S0, Sref, M, groups = lh_spec(G, g, 0.7, [psi, psi], [1.0, -1.0], [1.0])
    rng = np.random.default_rng(9100 + 1000 * pi)
    ja1, jb1, ja2, jb2, jh = 0, 10, 20, 30, 40
    A = Sref + [1, 41, 51]
    stat = {k: [] for k in ["B1", "B2", "B3", "B4", "B5", "B6", "B7a", "B7b", "N1", "N2"]}
    for r in range(reps):
        Xr, yr = gen_lh_iid(n, G, g, units, theta, rng)
        X, y = standardise(Xr, yr)
        stat["B1"].append(frac(X, y, [], [jb1, 11]))
        stat["B2"].append(frac(X, y, [ja1], [2, 3, 4]))
        stat["B3"].append(frac(X, y, [jh], [42, 43]))
        stat["B4"].append(frac(X, y, [], list(range(50, 60))))
        stat["B5"].append(frac(X, y, A, [5]))
        stat["B6"].append(frac(X, y, A, [25]))
        stat["B7a"].append(np.corrcoef(X[:, jb1], y)[0, 1] ** 2)
        stat["B7b"].append(np.corrcoef(X[:, jb2], y)[0, 1] ** 2)
        stat["N1"].append(frac(X, y, [], [6]))
        stat["N2"].append(frac(X, y, Sref, [12]))
    laws = {"B1": (1, (n - 3) / 2), "B2": (1.5, (n - 5) / 2), "B3": (1, (n - 4) / 2), "B4": (5, (n - 11) / 2),
            "B5": (0.5, (n - 2 - len(A)) / 2), "B6": (0.5, (n - 2 - len(A)) / 2), "B7a": (0.5, (n - 2) / 2),
            "B7b": (0.5, (n - 2) / 2), "N1": (0.5, (n - 2) / 2), "N2": (0.5, (n - 2 - len(Sref)) / 2)}
    lines.append(f"psi = {psi} (rho = 0.7), n = {n}, {reps} reps per statistic")
    for k, (a, b) in laws.items():
        pv = stats.kstest(stat[k], stats.beta(a, b).cdf).pvalue
        tag = "CONTROL (should reject)" if k.startswith("N") else "Lemma B"
        lines.append(f"  {k:4s} Beta({a}, {b}): KS p = {pv:.3g}   [{tag}]  mean {np.mean(stat[k]):.4f} vs {a/(a+b):.4f}")
    q1 = np.searchsorted(np.quantile(stat["B7a"], [.2, .4, .6, .8]), stat["B7a"])
    q2 = np.searchsorted(np.quantile(stat["B7b"], [.2, .4, .6, .8]), stat["B7b"])
    tab = np.zeros((5, 5))
    for i, j in zip(q1, q2):
        tab[i, j] += 1
    chi = stats.chi2_contingency(tab)
    lines.append(f"  B7 independence of the two masked hubs' r^2: chi-square p = {chi.pvalue:.3g}")
txt = "\n".join(lines)
print(txt)
open("../results/ks_lemmaB.txt", "w").write(txt + "\n")
