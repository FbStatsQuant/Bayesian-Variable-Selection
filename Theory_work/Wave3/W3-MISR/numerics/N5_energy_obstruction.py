"""W3-MISR numerics N5: the energy condition (E^sigma) cannot simply be dropped (obstruction proposed in
reviews/BT1_better_theorem_astra.md, "Limits"). Local only.

p = 2, exactly orthogonal centred columns (G = N I), v = 1, S0 = {0, 1}. theta_1 = n^a (a huge first signal when a = 1),
theta_2 = sqrt(c log n / n), c = 200 > c_0(2, 1) = 192 (the beta-min threshold); c_1(2, 1) is approximately 258.9.
In the obstruction arm a = 1, all hypotheses of MIS-R(i) except (E^sigma) hold eventually: p = s, so (OS) is void; (F0)
holds; and every underfit has ridge loss exceeding any fixed multiple of log n: with h = (n-1)/n the smoother
eigenvalue, L_{0} = (n-1) n + 200 (n-1) log(n)/n for the model keeping the huge signal, and the other two underfits
have loss at least (n-1) n^2. The arms a = 0 and a = 1/2 are numerical controls, not verified instances of the
ridge-margin class with c = 200 > c_1.
Observation: with a = 1 the posterior mass of S0 decreases towards 0 over the sampled n (it moves to {0}); in the control
arms it is 1.0000 at every sampled n.

Run:  py -3.13 -I Theory_work/Wave3/W3-MISR/numerics/N5_energy_obstruction.py > Theory_work/Wave3/W3-MISR/numerics/N5_out.txt
"""
import math
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
A0 = B0 = 0.01
REPS = 200
C_MARGIN = 200.0


def post_p2(X, yr):
    """Exact posterior over the 4 models for a standardised 2-column design X (n x 2) and raw response yr."""
    n = X.shape[0]
    yc = yr - yr.mean()
    y = yc / math.sqrt((yc ** 2).sum() / (n - 1))
    G = X.T @ X
    z = X.T @ y
    yy = float(y @ y)
    nu = A0 + n / 2.0
    p = 2
    logw = [math.log(0.5) - (math.lgamma(2 * p) - math.lgamma(k + 1) - math.lgamma(2 * p - k)) for k in range(3)]
    models = [(), (0,), (1,), (0, 1)]
    lp = []
    for S in models:
        k = len(S)
        if k == 0:
            lp.append(logw[0] - nu * math.log(2 * B0 + yy)); continue
        idx = list(S)
        GS = G[np.ix_(idx, idx)]
        H = (n + 1) * GS + np.eye(k)
        Q = yy - n * float(z[idx] @ np.linalg.solve(H, z[idx]))
        lp.append(logw[k] - 0.5 * (np.linalg.slogdet(H)[1] - np.linalg.slogdet(GS + np.eye(k))[1]) - nu * math.log(2 * B0 + Q))
    lp = np.array(lp); lp -= lp.max()
    w = np.exp(lp)
    return dict(zip(models, w / w.sum()))


def orth_design(rng, n):
    z = rng.standard_normal((n, 2))
    z -= z.mean(0)
    q, _ = np.linalg.qr(z)                    # orthonormal, centred columns
    return q * math.sqrt(n - 1)               # standardised: ||x_j||^2 = n - 1, x_1' x_2 = 0


print(f"N5  p = 2 orthogonal design, v = 1, theta_1 = n^a, theta_2^2 = {C_MARGIN:g} log n / n; reps = {REPS}")
for a in [0.0, 0.5, 1.0]:
    for n in [100, 400, 1600, 6400, 25600, 102400]:
        rng = np.random.default_rng(1000 * n + int(10 * a))
        m01, m0, energy, margin = [], [], 0.0, 0.0
        for _ in range(REPS):
            X = orth_design(rng, n)
            th1, th2 = float(n) ** a, math.sqrt(C_MARGIN * math.log(n) / n)
            mu = X @ np.array([th1, th2])
            post = post_p2(X, 2.0 + mu + rng.standard_normal(n))
            m01.append(post[(0, 1)]); m0.append(post[(0,)])
        energy = (th1 ** 2 + th2 ** 2) * (n - 1) / n          # ||mu||^2 / (n v)
        margin = th2 ** 2 * (n - 1) / math.log(n)             # projection margin Delta_{0} / (v log n)
        print(f"  a={a:<4} n={n:<6d} ||mu||^2/(n v)={energy:<10.3g} Delta_{{0}}/(v log n)={margin:6.1f}  "
              f"E pi(S0)={np.mean(m01):.4f}  E pi({{0}})={np.mean(m0):.4f}")
print("DONE")
