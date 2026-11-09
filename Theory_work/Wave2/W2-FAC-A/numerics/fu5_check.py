"""fu5_check.py -- F-U5 (R01 optional): adversarial class members for Lemma U(a),(b): tiny loadings (small c_min),
sign-changing heterogeneous loadings, negative within-group correlations (Psi PD), bounded p; checks the exact identity
and the deterministic bound (1.2) on random / one-sided sets (no greedy sets here; those are in fu_check.py).  -> FU5_out.txt"""
import math, numpy as np
from fu_check import innov, decomp
rng = np.random.default_rng(77)
maxerr = 0.0; viol = 0; nt = 0
cases = []
for rep in range(60):
    G = int(rng.integers(1, 6)); gs = int(rng.integers(1, 5)); p = G * gs
    groups = [list(range(i * gs, (i + 1) * gs)) for i in range(G)]
    lam = rng.uniform(0.01, 0.9, size=p) * rng.choice([-1, 1], size=p)
    if rep % 3 == 0: lam[rng.integers(0, p)] = 1e-3      # tiny loading -> tiny c_min
    Psi = np.zeros((p, p))
    for g in groups:
        A = rng.standard_normal((len(g), len(g)))
        B = A @ A.T
        d = np.sqrt(np.diag(B)); C = B / np.outer(d, d)      # correlation with possibly negative entries
        C = 0.85 * C + 0.15 * np.eye(len(g))
        Psi[np.ix_(g, g)] = C
    dd = np.sqrt(lam ** 2 + np.diag(Psi)); lam /= dd; Psi /= np.outer(dd, dd)
    gid = np.repeat(np.arange(G), gs); Sig = np.outer(lam, lam) + Psi
    for _ in range(5):
        xi0 = rng.standard_normal(); zeta = np.linalg.cholesky(Psi) @ rng.standard_normal(p); gv = lam * xi0 + zeta
        sets = [[]] + [sorted(rng.choice(p, size=int(rng.integers(0, p)), replace=False).tolist()) for _ in range(20)]
        o = np.argsort(-zeta); sets += [sorted(o[:m].tolist()) for m in range(1, p)]
        for T in sets:
            for l in [j for j in range(p) if j not in T]:
                z1 = innov(Sig, gv, T, l); z2, b, _ = decomp(lam, Psi, gid, groups, xi0, zeta, T, l)
                maxerr = max(maxerr, abs(z1 - z2)); nt += 1; viol += (abs(z1) > b + 1e-9)
txt = "F-U5 adversarial members (tiny loadings, sign changes, negative within-group corr, p<=20): tests %d, max identity error %.2e, bound violations %d" % (nt, maxerr, viol)
print(txt); open("FU5_out.txt", "w").write(txt + "\n")
