"""LH discrepancy check: at S = S0 - {a_1, a_2} (two hubs a missing, their partners b present), the neutral swap
b_2 -> a_1 ties 'add a_1' at population level; with the exact score the swap wins w.p. -> 1, so D_S fails and
TD'_P(R_{2,0}) fails, while D_S holds on Lat(S°).  LH case 0 of lh_pgd.py, exact Gram X'X = (n-1) Sigma
(X = sqrt(n-1) Q chol(Sigma)', Q with orthonormal columns orthogonal to 1).  Seeds 0..199 per n."""
import numpy as np
from lh_pgd import build
from engine import Scorer
Sig, th = build(5, 3, [.7] * 5, [(0, 1, .5, 1.4), (2, 3, -.4, -1.0)], [(4, 1.0)])
p = len(th); S0 = sorted(np.nonzero(th)[0].tolist())   # hubs: a1=0, b1=3, a2=6, b2=9, h=12
L = np.linalg.cholesky(Sig)
is_t = np.zeros(p, bool); is_t[S0] = True
out = []
for n in (200, 2000, 20000):
    fails = 0; fails_lat = 0; R = 200
    for seed in range(R):
        rng = np.random.default_rng(seed)
        Z = rng.standard_normal((n, p + 1)); Z -= Z.mean(0)
        Q, _ = np.linalg.qr(Z)
        X = np.sqrt(n - 1) * Q[:, :p] @ L.T
        y = X @ th + rng.standard_normal(n)
        y = (y - y.mean()) / y.std(ddof=1)
        Sc = Scorer(X, y)
        for S, tag in (([3, 9, 12], 'R20'), ([0, 6, 12], 'lat')):   # S0-{a1,a2}  and  S° = S0-{b1,b2}
            o = Sc.eval(np.array([S]))
            inS = o['inS'][0]; tS = is_t[S]
            add = np.where(inS, -np.inf, o['add'][0, :, 0])
            prog = max(add[is_t].max(), np.where(~tS, o['del'][0, :, 0], -np.inf).max(),
                       np.where((~tS)[:, None] & is_t[None, :] & ~inS[None, :], o['swap'][0, :, :, 0], -np.inf).max())
            non = max(o['F'][0, 0], add[~is_t].max(), np.where(tS, o['del'][0, :, 0], -np.inf).max(),
                      np.where(~((~tS)[:, None] & is_t[None, :]) & ~inS[None, :], o['swap'][0, :, :, 0], -np.inf).max())
            if prog <= non:
                if tag == 'R20': fails += 1
                else: fails_lat += 1
    out.append(f"n={n}: D_S fails at S0-{{a1,a2}} (in R_(2,0), not in Lat(S°)): {fails}/{R};  at S° = S0-{{b1,b2}} (in Lat(S°)): {fails_lat}/{R}")
print('\n'.join(out)); open('../results/lh_tie.txt', 'w').write('\n'.join(out) + '\n')
