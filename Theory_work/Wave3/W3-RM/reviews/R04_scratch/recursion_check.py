"""R04 sanity check: partial-correlation recursion and |z_U - z0| = O(g_n^2) (L3_SANDR s4, L3b).
Design: U0 (3 vars), V (5 remote vars, equicorrelated rho_V = 0.9 -> floor 0.1, NO small v-v' covariance),
l and truth j each with population covariance r with every v in V given U0, Cov(l, j | U0) = gain.
Y = theta * W_j / t_j + eps (centred).  Compare max |z_U - z0| with g^2, g = r + sqrt(log n / n)."""
import numpy as np

def pcorr_given(Z, x, y):
    """sample partial correlation of columns x,y given columns Z (all centred)."""
    if Z.shape[1] == 0:
        rx, ry = x, y
    else:
        Q, _ = np.linalg.qr(Z)
        rx = x - Q @ (Q.T @ x); ry = y - Q @ (Q.T @ y)
    return rx @ ry / np.sqrt((rx @ rx) * (ry @ ry))

def build_sigma(r, gain, rhoV=0.9, kU0=3, kV=5):
    # order: U0 (kU0), V (kV), l, j ; U0 independent of everything (so conditioning on U0 is trivial in population)
    p = kU0 + kV + 2
    S = np.eye(p)
    iV = np.arange(kU0, kU0 + kV); il = kU0 + kV; ij = il + 1
    for a in iV:
        for b in iV:
            if a != b: S[a, b] = rhoV
    for v in iV:
        S[il, v] = S[v, il] = r
        S[ij, v] = S[v, ij] = r
    S[il, ij] = S[ij, il] = gain
    return S, np.arange(kU0), iV, il, ij

rng = np.random.default_rng(20261109)
theta, sigma = 1.0, 1.0
print(f"{'n':>6} {'r':>9} {'g^2':>9} {'max|zU-z0|':>11} {'ratio':>7} {'max n|zU^2-z0^2|':>16} {'check_identity':>14}")
for n in [500, 2000, 8000, 32000]:
    hn = np.sqrt(np.log(n) / n)
    for r in [n**-2.0, hn, n**(-1/3), n**-0.25]:
        S, iU0, iV, il, ij = build_sigma(r, gain=n**-0.5)
        if np.linalg.eigvalsh(S).min() <= 0: continue
        L = np.linalg.cholesky(S)
        worst, worsth, worst_id = 0.0, 0.0, 0.0
        for rep in range(40):
            W = rng.standard_normal((n, S.shape[0])) @ L.T
            W = W - W.mean(0)
            t = np.linalg.norm(W, axis=0) / np.sqrt(n - 1)
            eps = rng.standard_normal(n) * sigma; eps -= eps.mean()
            Y = theta * W[:, ij] / t[ij] + eps
            Z0 = W[:, iU0]; ZU = W[:, np.r_[iU0, iV]]
            z0 = pcorr_given(Z0, W[:, il], Y)
            zU = pcorr_given(ZU, W[:, il], Y)
            # recursion ingredients (all given U0)
            a = np.array([pcorr_given(Z0, W[:, il], W[:, v]) for v in iV])
            d = np.array([pcorr_given(Z0, Y, W[:, v]) for v in iV])
            R = np.array([[pcorr_given(Z0, W[:, v], W[:, w]) if v != w else 1.0 for w in iV] for v in iV])
            Ri = np.linalg.inv(R)
            zrec = (z0 - a @ Ri @ d) / np.sqrt((1 - a @ Ri @ a) * (1 - d @ Ri @ d))
            worst_id = max(worst_id, abs(zrec - zU))
            worst = max(worst, abs(zU - z0)); worsth = max(worsth, n * abs(zU**2 - z0**2))
        g2 = (r + hn) ** 2
        print(f"{n:6d} {r:9.2e} {g2:9.2e} {worst:11.3e} {worst/g2:7.2f} {worsth:16.3e} {worst_id:14.1e}")
