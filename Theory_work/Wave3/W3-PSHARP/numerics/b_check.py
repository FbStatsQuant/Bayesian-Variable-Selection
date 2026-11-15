"""W3-PSHARP numerics (b) + Lemma S: falsification search by exact enumeration on small designs, and tables.

F1  Lemma S items 1-2 on random / correlated / rank-deficient designs: the Schur formulas for D_{S+j}/D_S and
    Q_S - Q_{S+j} against generic linear algebra; D ratio <= n (the equality case is not tested here).
F2  Corollary B: for every S0 with 0 <= s0 <= K-1 (S0 need not be a true support) and adversarial data,
    odds := delta/(1-delta) >= O_lb >= c(p,s0)/sqrt(n). Reports the minimum of odds/O_lb (must be >= 1).
T1  Table of the bound: sqrt(n) O_lb/(s0+1), c(p,s0)/(s0+1), and the cap on pi(S0) for s0 = lambda sqrt(n).
Run: py -3.13 -I b_check.py > b_check_out.txt
"""
import sys, os, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script directory
sys.dont_write_bytecode = True
import numpy as np
from core import B0, standardise, log_score, enumerate_posterior, odds_against, c_const, O_lb, logsumexp


def make_design(kind, n, p, rng):
    Z = rng.standard_normal((n, p))
    if kind == "iid":
        Xr = Z
    elif kind == "corr":                      # strong equicorrelation
        Xr = Z + 3.0 * rng.standard_normal((n, 1))
    elif kind == "dup":                       # exact duplicate and an exact linear dependence
        Xr = Z.copy(); Xr[:, 1] = Xr[:, 0]; Xr[:, 2] = Xr[:, 3] + Xr[:, 4]
    elif kind == "near":                      # near-duplicates
        Xr = Z.copy(); Xr[:, 1] = Xr[:, 0] + 1e-4 * rng.standard_normal(n)
    elif kind == "orth":
        Q, _ = np.linalg.qr(Z - Z.mean(0)); Xr = Q if n - 1 >= p else Z   # orthogonal centred columns need p <= n-1
    elif kind == "binary":
        Xr = (Z > 0.3).astype(float)
        for j in range(p):
            if Xr[:, j].std() == 0: Xr[0, j] = 1 - Xr[0, j]
    return Xr


def make_y(kind, Xr, rng):
    n, p = Xr.shape
    if kind == "null":
        return rng.standard_normal(n)
    if kind == "sparse":
        b = np.zeros(p); b[:2] = [1.0, -0.7]; return Xr @ b + rng.standard_normal(n)
    if kind == "dense":
        return Xr @ rng.standard_normal(p) + 0.5 * rng.standard_normal(n)
    if kind == "exact":                       # y almost exactly in the column space (near-perfect fits)
        return Xr @ rng.standard_normal(p) + 1e-6 * rng.standard_normal(n)
    if kind == "heavy":
        return rng.standard_cauchy(n)


def F1(rng):
    print("F1: Lemma S items 1-2 (Schur formulas, D ratio <= n)")
    worst_f, worst_q, max_ratio, cnt = 0.0, 0.0, 0.0, 0
    for kind in ("iid", "corr", "dup", "near", "orth", "binary"):
        for n in (6, 9, 15, 40):
            p = 7
            Xr = make_design(kind, n, p, rng); yr = make_y("dense", Xr, rng)
            X, y = standardise(Xr, yr)
            for k in range(0, min(p, n // 2)):
                for S in itertools.combinations(range(p), k):
                    S = list(S)
                    _, logD_S, Q_S = log_score(X, y, S)
                    for j in range(p):
                        if j in S: continue
                        _, logD_Sj, Q_Sj = log_score(X, y, S + [j])
                        xj = X[:, j]
                        if k:
                            XS = X[:, S]; G = XS.T @ XS; H = (n + 1) * G + np.eye(k)
                            g = XS.T @ xj
                            s = n * n - (n + 1) ** 2 * g @ np.linalg.solve(H, g)
                            den = n - g @ np.linalg.solve(G + np.eye(k), g)
                            rho = y - (n + 1) * XS @ np.linalg.solve(H, XS.T @ y)
                        else:
                            s, den, rho = float(n * n), float(n), y
                        ratio = math.exp(logD_Sj - logD_S)
                        worst_f = max(worst_f, abs(ratio - s / den) / ratio)
                        gain = Q_S - Q_Sj
                        worst_q = max(worst_q, abs(gain - n * (xj @ rho) ** 2 / s) / max(Q_S, 1e-12))
                        max_ratio = max(max_ratio, ratio / n)
                        assert 0 < s <= n * n * (1 + 1e-12) and gain >= -1e-9 * max(Q_S, 1e-9) and Q_Sj >= -1e-9
                        assert gain >= (xj @ rho) ** 2 / n - 1e-8 * max(Q_S, 1.0)
                        cnt += 1
    print(f"  {cnt} (S, j) pairs: max rel error D-ratio formula {worst_f:.1e}; max error of the Q-gain formula (rel. to Q_S) {worst_q:.1e};"
          f" max of (D_Sj/D_S)/n = {max_ratio:.12f} (must be <= 1)")
    print(f"  {'PASS' if worst_f < 1e-6 and worst_q < 1e-6 and max_ratio <= 1 + 1e-9 else 'FAIL'}")


def F2(rng):
    print("F2: Corollary B falsification: min over cases of odds/O_lb and of odds/(c/sqrt n) (both must be >= 1)")
    mn, mn1, cnt, arg = np.inf, np.inf, 0, None
    for kind in ("iid", "corr", "dup", "near", "orth", "binary"):
        for ykind in ("null", "sparse", "dense", "exact", "heavy"):
            for (n, p) in ((6, 5), (8, 8), (12, 7), (25, 8), (60, 8), (400, 7), (5000, 6)):
                for rep in range(2):
                    Xr = make_design(kind, n, p, rng); yr = make_y(ykind, Xr, rng)
                    X, y = standardise(Xr, yr)
                    post = enumerate_posterior(X, y)
                    K = min(p, n // 2)
                    lz = logsumexp(list(post.values()))
                    for S0, l0 in post.items():
                        s0 = len(S0)
                        if s0 > K - 1: continue
                        d = lz - l0                    # log(1 + odds); work in logs (odds can be astronomically large)
                        if d > 30: lodds = d
                        elif d > 1e-6: lodds = math.log(math.expm1(d))
                        else: lodds = math.log(odds_against(post, S0))   # no cancellation
                        ob = O_lb(n, p, s0); c1 = c_const(p, s0) / math.sqrt(n)
                        assert ob >= c1 * (1 - 1e-12)
                        r, r1 = math.exp(min(lodds - math.log(ob), 50)), math.exp(min(lodds - math.log(c1), 50))
                        cnt += 1
                        if r < mn: mn, arg = r, (kind, ykind, n, p, sorted(S0))
                        mn1 = min(mn1, r1)
    print(f"  {cnt} (design, data, S0) cases: min odds/O_lb = {mn:.6f} at {arg}; min odds/(c/sqrt n) = {mn1:.6f}")
    print(f"  {'PASS' if mn >= 1 - 1e-9 else 'FAIL'}")
    # orthogonal design, y orthogonal to all columns -> every fit factor is 1 and every D ratio is n: equality
    n, p = 12, 6
    M = rng.standard_normal((n, p + 1)); M = M - M.mean(0); Qm, _ = np.linalg.qr(M); Qm = Qm - Qm.mean(0); Qm, _ = np.linalg.qr(Qm)
    X = math.sqrt(n - 1) * Qm[:, :p]; y = math.sqrt(n - 1) * Qm[:, p]
    post = enumerate_posterior(X, y)
    for s0 in (0, 1, 3):
        odds = odds_against(post, range(s0))
        sup = math.exp(logsumexp([v - post[frozenset(range(s0))] for S, v in post.items() if S > frozenset(range(s0))]))
        print(f"  equality case (orthogonal X, y orthogonal to col X), n={n} p={p} s0={s0}: superset odds/O_lb = {sup / O_lb(n, p, s0):.12f}"
              f" (all odds/O_lb = {odds / O_lb(n, p, s0):.4f}; for s0 > 0 the non-superset models add mass)")


def T1():
    print("T1: the bound. (i) fixed s0: sqrt(n) O_lb/(s0+1) and c(p,s0)/(s0+1) (limit 1/2 as s0/p -> 0)")
    for (n, p) in ((100, 50), (1000, 1000), (10 ** 4, 10 ** 6), (10 ** 6, 10 ** 8)):
        row = []
        for s0 in (0, 1, 5, 20):
            if s0 <= min(p, n // 2) - 1:
                row.append(f"s0={s0}: {math.sqrt(n) * O_lb(n, p, s0) / (s0 + 1):.4f}/{c_const(p, s0) / (s0 + 1):.4f}")
        print(f"  n={n:.0e} p={p:.0e}: " + "; ".join(row))
    print("    (ii) s0 = round(lambda sqrt n), p = 10 n: cap on pi(S0): 1/(1+O_lb) [full sum], 1/(1+c/sqrt n) [j=1 term], and e^{-lambda/2}")
    for lam in (0.25, 1.0, 4.0, 16.0):
        row = []
        for n in (10 ** 2, 10 ** 4, 10 ** 6):
            s0 = int(round(lam * math.sqrt(n))); p = 10 * n
            if s0 <= n // 2 - 1:
                row.append(f"n={n:.0e}: {1 / (1 + O_lb(n, p, s0)):.4f} [{1 / (1 + c_const(p, s0) / math.sqrt(n)):.4f}]")
        print(f"  lambda={lam}: " + "; ".join(row) + f";  e^(-lambda/2) = {math.exp(-lam / 2):.4f}")


if __name__ == "__main__":
    rng = np.random.default_rng(20261112)
    F1(rng); F2(rng); T1()
