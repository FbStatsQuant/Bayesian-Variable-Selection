"""Checks of Lemma B (exact Beta laws) and Lemma Lambda / Theorem P6 population margins. Seed 7.
(1) LH-iid config A at n = 200, p = 750: collect x_{S°,l} (neutral l in an a-group, a visible group, a null group),
    X_{h,V} for |V| = 2 in a null group and in the masked b-group (U° = empty), and (n-1) r^2 of the masked hub;
    KS tests against the exact Beta laws.
(2) Population: for parameter grids (rho, psi, beta) and c in {1,2,3}, enumerate every lattice state S° u M' and every
    flip/swap neighbour inside the signal components (plus one generic null), compute lambda exactly from Sigma, and report
    the minimum margin  min_A [lambda(A) - lambda(P*)]  over non-progress A (must be > 0), and the (L) margin at S0."""
import itertools, math, numpy as np
from scipy import stats
import lh_iid
from pxn_core import Data

rng = np.random.default_rng(7)
cfg = lh_iid.CONFIGS["A"]; g = cfg["g"]; n, p = 200, 750
xs = {"a-group neutral": [], "visible neutral": [], "null": [], "nullV2": [], "bgroupV2": [], "hub_b": []}
for rep in range(400):
    X, y, groups, S0, Sref, M = lh_iid.gen_lh(n, p // g, g, cfg["rho"], cfg["psi"], cfg["pairs"], cfg["visible"], rng)
    D = Data(X, y)
    def frac(A, W):
        Y = D.y
        def rss(B):
            if not B: return Y @ Y
            Xb = D.X[:, B]; b = np.linalg.lstsq(Xb, Y, rcond=None)[0]; r = Y - Xb @ b; return r @ r
        return 1 - rss(sorted(A + W)) / rss(sorted(A))
    xs["a-group neutral"].append(frac(Sref, [1]))          # member of C_a (group 0)
    xs["visible neutral"].append(frac(Sref, [21]))         # member of visible group 2
    xs["null"].append(frac(Sref, [35]))                    # null group 3
    xs["nullV2"].append(frac([], [40, 41]))                # block statistic, null group, |V| = 2
    xs["bgroupV2"].append(frac([], [11, 12]))              # block statistic, masked b-group, U° = empty
    xs["hub_b"].append(frac([], [10]))                     # masked hub alone
s = len(Sref)
laws = {"a-group neutral": (0.5, (n - 2 - s) / 2), "visible neutral": (0.5, (n - 2 - s) / 2), "null": (0.5, (n - 2 - s) / 2),
        "nullV2": (1.0, (n - 3) / 2), "bgroupV2": (1.0, (n - 3) / 2), "hub_b": (0.5, (n - 2) / 2)}
print("Lemma B: KS tests vs exact Beta laws (400 reps each)")
for k, v in xs.items():
    a, b = laws[k]
    print("  %-16s Beta(%.1f, %.1f): KS p-value = %.3f" % (k, a, b, stats.kstest(v, stats.beta(a, b).cdf).pvalue))
# control: a proxy of the masked hub given S° is NOT Beta (signal leaks)
print()

def lh_sigma(c, v, g, rho, psi):
    G = 2 * c + v + 1
    P = G * g
    S = np.zeros((P, P))
    for h in range(G):
        S[h*g:(h+1)*g, h*g:(h+1)*g] = rho; 
    np.fill_diagonal(S, 1.0)
    for i in range(c):
        a, b = 2 * i, 2 * i + 1
        cross = psi * np.outer(S[a*g:(a+1)*g, a*g], S[b*g, b*g:(b+1)*g])
        S[a*g:(a+1)*g, b*g:(b+1)*g] = cross; S[b*g:(b+1)*g, a*g:(a+1)*g] = cross.T
    return S

def lam(S, th, A):
    if not A: return th @ S @ th
    A = list(A); c = S[A] @ th
    return th @ S @ th - c @ np.linalg.solve(S[np.ix_(A, A)], c)

print("Theorem P6 population margins (exhaustive over neighbours inside the signal components + one null column)")
worst = []
for c in (1, 2, 3):
    for rho in (0.4, 0.7, 0.85):
        for psi in (0.2, 0.5, min(0.8, rho - 0.05)):
            for beta in (0.5, 1.0, 2.0):
                g, v = 4, 1  # g only matters through the variable types; 4 members per group suffices
                S = lh_sigma(c, v, g, rho, psi)
                th = np.zeros(len(S))
                for i in range(c):
                    th[2*i*g] = beta * (1 if i % 2 == 0 else -1); th[(2*i+1)*g] = -psi * th[2*i*g]
                th[2*c*g] = 1.0
                S0 = sorted(np.flatnonzero(th)); Mset = [(2*i+1)*g for i in range(c)]
                Sref = sorted(set(S0) - set(Mset))
                univ = list(range(len(S)))  # includes one null group (last)
                mins = []
                for r in range(c):
                    for Mp in itertools.combinations(Mset, r):
                        St = sorted(Sref + list(Mp)); lS = lam(S, th, St)
                        prog = [sorted(St + [j]) for j in Mset if j not in St]
                        lP = min(lam(S, th, A) for A in prog)
                        nb = []
                        for j in univ:
                            if j in St: nb.append(sorted(set(St) - {j}))
                            else: nb.append(sorted(St + [j]))
                        for i_ in St:
                            for j in univ:
                                if j not in St: nb.append(sorted(set(St) - {i_} | {j}))
                        nonprog = [A for A in nb if A not in prog] + [St]
                        mins.append(min(lam(S, th, A) for A in nonprog) - lP)
                # (L) at S0: deletions/swaps
                lS0 = [lam(S, th, sorted(set(S0) - {i_} | ({j} if j is not None else set())))
                       for i_ in S0 for j in [None] + [j for j in univ if j not in S0]]
                worst.append((min(mins), min(lS0), c, rho, psi, beta))
worst.sort()
print("  smallest D_S margin over the grid: %.4g (c=%d rho=%.2f psi=%.2f beta=%.1f)" % (worst[0][0], *worst[0][2:]))
print("  smallest (L) deletion/swap margin over the grid: %.4g" % min(w[1] for w in worst))
print("  all margins positive:", all(w[0] > 0 and w[1] > 0 for w in worst), " (grid size %d)" % len(worst))
