"""iid_selftest.py: (1) incremental PathState gains == direct closed-form scan (fac_core.scan) along a path,
(2) Bartlett sufficient statistics == explicit n x p simulation in law (moments), (3) xi = u'eps/||eps|| check."""
import math, numpy as np
import iid_core as ic, fac_core as fc

rng = np.random.default_rng(1)
worst = 0.0
for trial in range(4):
    n, p = [(200, 30), (5000, 60), (10 ** 6, 40), (10 ** 7, 25)][trial]
    rho = [0.3, 0.6, 0.5, 0.8][trial]
    beta = np.zeros(p); beta[[3, 11, 20]] = [1.2, -0.8, 1.5]
    P = ic.IidData(math.sqrt(rho) * np.ones(p), beta, n, rng)
    st = ic.PathState(P, range(p))
    for step in range(p - 5):
        Gd, Ga, Gs, _ = st.gains()
        sc = fc.scan(P, tuple(st.T))
        FT = sc["FT"]
        e = max(np.max(np.abs(Gd - (sc["del"] - FT))),
                np.max(np.abs(Ga - (sc["add"] - FT))) if len(Ga) else 0.0,
                np.max(np.abs(Gs - (sc["swap"] - FT))) if Gs.size else 0.0)
        worst = max(worst, e)
        # delete a pseudo-random element (not necessarily the best) to exercise the downdate
        i = int(rng.integers(len(st.T)))
        st.delete(i)
    print(f"trial {trial} n={n} p={p}: max |incremental - direct| gain = {e:.3e}")
print(f"WORST over all steps: {worst:.3e}")

# (2) law check at small n against explicit rows
n, p, rho = 50, 6, 0.4
beta = np.zeros(p); beta[1] = 1.0
M_b = []; M_e = []
for r in range(4000):
    P = ic.IidData(math.sqrt(rho) * np.ones(p), beta, n, rng)
    M_b.append(P.XtX[0, 2] / (n - 1)); M_b.append(P.XtX[3, 4] / (n - 1))
    f = rng.standard_normal(n); U = rng.standard_normal((n, p))
    Xr = math.sqrt(rho) * f[:, None] + math.sqrt(1 - rho) * U
    Xc = Xr - Xr.mean(0); Xs = Xc / Xc.std(0, ddof=1)
    R = Xs.T @ Xs / (n - 1)
    M_e.append(R[0, 2]); M_e.append(R[3, 4])
print(f"law check (sample corr): Bartlett mean {np.mean(M_b):.4f} sd {np.std(M_b):.4f} | explicit mean {np.mean(M_e):.4f} sd {np.std(M_e):.4f}")
P = ic.IidData(math.sqrt(0.5) * np.ones(500), np.r_[1.0, np.zeros(499)], 10 ** 6, rng)
print(f"xi: mean {P.xi.mean():.3f} sd {P.xi.std():.3f} (iid N(0,1) by construction)")
