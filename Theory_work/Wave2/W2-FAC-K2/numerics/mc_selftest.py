"""mc_selftest.py -- validates mc_core (k-dim closed forms) against fac_core.scan / ExactGram (general exact-Gram scorer)
on the same data set: F on random sets, every deletion/addition, best swap, full swap matrix."""
import sys, math, itertools, numpy as np
sys.path.insert(0, r"C:\Users\felip\Bayesian-Variable-Selection\Theory_work\Wave2\W2-FAC-B\numerics")
import fac_core as fc, mc_core as mc
rng = np.random.default_rng(7)
for trial, (k, n, p) in enumerate([(2, 400, 30), (3, 2000, 45), (2, 10**6, 40)]):
    R = np.array([[0.5, 0.2], [0.2, 0.7]]) if k == 2 else np.array([[0.4, 0.1, 0.25], [0.1, 0.6, 0.0], [0.25, 0.0, 0.5]])
    cls = np.arange(p) % k
    D = mc.MCDesign(cls, R)
    th = np.zeros(p); th[[0, 5, 11]] = [1.4, -1.0, 1.8]
    P = mc.MCData(D, th, n, rng)
    Sigma = D.Sigma()
    class FakeR:
        def standard_normal(self, m): return np.linalg.solve(np.linalg.cholesky(Sigma), P.g)
        def chisquare(self, df): return P.chi
    Pe = fc.ExactGram(Sigma, th, n, FakeR())
    assert abs(Pe.scale_s - P.s) < 1e-9 * P.s
    worst = 0.0
    for sz in range(0, 7):
        for S in itertools.islice(itertools.combinations(range(p), sz), 60):
            worst = max(worst, abs(P.F(S) - Pe.F(S)))
    wsc = 0.0
    for t in range(12):
        kk = int(rng.integers(0, min(p, P.K)))
        T = tuple(sorted(rng.choice(p, kk, replace=False).tolist()))
        a = P.scan(T, full_swaps=True); b = fc.scan(Pe, T)
        wsc = max(wsc, abs(a["FT"] - b["FT"]))
        if kk: wsc = max(wsc, np.max(np.abs(a["del"] - b["del"])))
        if kk < P.K and len(a["O"]): wsc = max(wsc, np.max(np.abs(a["add"] - b["add"])))
        if kk and len(a["O"]):
            wsc = max(wsc, np.max(np.abs(a["swap"] - b["swap"])))
            wsc = max(wsc, abs(a["best_swap"] - b["swap"].max()))
            a2 = P.scan(T)  # convexity shortcut
            wsc = max(wsc, abs(a2["best_swap"] - b["swap"].max()))
    print(f"k={k} n={n} p={p}: max|F_mc - F_exactgram| = {worst:.3e}; max scan discrepancy (incl. full swaps, "
          f"convexity best swap) = {wsc:.3e}; |F| scale ~ {abs(P.F(()))::.3e}" if False else
          f"k={k} n={n} p={p}: max|F_mc - F_exactgram| = {worst:.3e}; max scan discrepancy (del/add/full swap/convexity best swap) = {wsc:.3e}; |F(empty)| = {abs(P.F(())):.3e}")
