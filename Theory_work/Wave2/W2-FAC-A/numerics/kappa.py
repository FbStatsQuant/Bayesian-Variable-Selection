"""kappa.py -- kappa(Sigma), c_min, alpha0 for the factor class (STATEMENT §2). usage: py -3.13 kappa.py"""
import itertools, numpy as np
def kappa(lam, Psi, groups):
    cmin = np.inf; kap = 0.0
    for g in groups:
        g = list(g)
        for r in range(1, len(g) + 1):
            for U in itertools.combinations(g, r):
                U = list(U); s = lam[U] @ np.linalg.solve(Psi[np.ix_(U, U)], lam[U]); cmin = min(cmin, s)
    for g in groups:
        g = list(g)
        for l in g:
            rest = [j for j in g if j != l]
            for r in range(0, len(rest) + 1):
                for U in itertools.combinations(rest, r):
                    U = list(U)
                    if U:
                        c = np.linalg.solve(Psi[np.ix_(U, U)], Psi[U, l]); lt = lam[l] - c @ lam[U]; ps = Psi[l, l] - Psi[l, U] @ c
                    else:
                        lt, ps = lam[l], Psi[l, l]
                    kap = max(kap, abs(lt) / np.sqrt(ps))
    return kap / np.sqrt(cmin), cmin
def alpha0(k):
    s = np.linspace(0, 1, 100001); return 1 / (2 * ((1 + k * s) ** 2 - s ** 2).max())
for a in (0.1, 0.3, 0.5, 0.9):
    p = 6; lam = np.full(p, np.sqrt(a)); Psi = (1 - a) * np.eye(p)
    k, c = kappa(lam, Psi, [[j] for j in range(p)]); print("CS a=%.1f kappa=%.6f cmin=%.4f alpha0=%.5f" % (a, k, c, alpha0(k)))
for rb, rw, gs in ((0.3, 0.7, 5), (0.1, 0.8, 5), (0.5, 0.6, 3), (0.2, 0.9, 4)):
    G = 2; p = G * gs; lam = np.full(p, np.sqrt(rb)); H = np.kron(np.eye(G), np.ones((gs, gs))); Psi = (rw - rb) * H + (1 - rw) * np.eye(p)
    groups = [list(range(i * gs, (i + 1) * gs)) for i in range(G)]
    Sig = np.outer(lam, lam) + Psi; assert np.allclose(np.diag(Sig), 1)
    k, c = kappa(lam, Psi, groups); print("BCS rb=%.1f rw=%.1f g=%d kappa=%.6f cmin=%.4f alpha0=%.5f" % (rb, rw, gs, k, c, alpha0(k)))
