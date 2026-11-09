"""W2-UNI numerics N1: falsification probe for the metric toolkit (CT_M) and Lemma LOCL.

For Psi in LOC_M (three geometries: 2-D jittered sites with exponential covariance (Sigma-branch), 2-D grid GMRF
(Theta-branch), random geometric graph with graph distance (Sigma-branch, exp of graph distance)), compute for many
(T, l) and radii r:
  Delta(r) = || beta_T(l) - beta_{T cap B(l,r)}(l) ||_1   (zero-padded; beta_A(l) = Psi_AA^{-1} Psi_{A l})
and record max over (T, l) as a function of r (must decay to 0, roughly exponentially), plus fitted exponential decay
slopes of the observed inverse-entry envelopes of principal submatrices.
[R05a-13] The fitted slopes are exploratory observations only: this script does NOT construct the CT_M constants or t*
and does NOT test the analytic CT_M ratio |(A^{-1})_ij| / ((2/alpha) e^{-t* d_ij}) <= 1. That ratio check is in
n2_metric.py (-> n2_metric_out.txt). (Docstring corrected after the R05a sweep; code and n1_out.txt unchanged.)
T: random subsets of densities 0.1/0.5/0.9 and 'greedy' sets = all of [p] minus a random small set.
Observations only (a falsification probe; the proofs are the certificate).
Run: py -3.13 -B n1_metric.py > n1_out.txt
"""
import numpy as np
from scipy.sparse.csgraph import shortest_path

rng = np.random.default_rng(20261109)


def sites_2d(m, jitter=0.25):
    g = np.array([(i, j) for i in range(m) for j in range(m)], float)
    g += rng.uniform(-jitter, jitter, g.shape)
    return g


def dist_euclid(x):
    return np.sqrt(((x[:, None, :] - x[None, :, :]) ** 2).sum(-1))


def design_exp2d(m=14, phi=1.0, rho=0.8):
    x = sites_2d(m)
    d = dist_euclid(x)
    psi = rho * np.exp(-d / phi)
    np.fill_diagonal(psi, 1.0)
    return psi, d, "exp2d(m=%d,phi=%.1f)" % (m, phi)


def design_gmrf(m=14, kappa=0.22):
    p = m * m
    th = np.eye(p)
    idx = lambda i, j: i * m + j
    for i in range(m):
        for j in range(m):
            for di, dj in ((1, 0), (0, 1)):
                if i + di < m and j + dj < m:
                    a, b = idx(i, j), idx(i + di, j + dj)
                    th[a, b] = th[b, a] = -kappa
    psi = np.linalg.inv(th)
    s = np.sqrt(np.diag(psi))
    psi = psi / s[:, None] / s[None, :]
    x = np.array([(i, j) for i in range(m) for j in range(m)], float)
    d = np.abs(x[:, None, :] - x[None, :, :]).sum(-1)  # graph (l1) distance on the grid
    return psi, d, "gmrf(m=%d,k=%.2f)" % (m, kappa)


def design_rgg(p=196, radius=0.12, rho=0.7, a=1.0):
    x = rng.uniform(0, 1, (p, 2))
    e = dist_euclid(x)
    adj = (e < radius) & (e > 0)
    d = shortest_path(adj.astype(float), unweighted=True)
    d[np.isinf(d)] = 1e6
    psi = rho * np.exp(-a * d)
    np.fill_diagonal(psi, 1.0)
    # make PD with spectrum floor: shrink if needed
    lo = np.linalg.eigvalsh(psi).min()
    if lo < 0.05:
        psi = (psi + (0.05 - lo) * np.eye(p)) / (1 + 0.05 - lo)
    return psi, d, "rgg(p=%d,r=%.2f)" % (p, radius)


def beta(psi, A, l):
    A = np.asarray(A, int)
    out = np.zeros(psi.shape[0])
    if len(A) == 0:
        return out
    out[A] = np.linalg.solve(psi[np.ix_(A, A)], psi[A, l])
    return out


def probe(psi, d, name, n_pairs=120, radii=(0, 1, 2, 3, 4, 6, 8)):
    p = psi.shape[0]
    ev = np.linalg.eigvalsh(psi)
    print(f"== {name}: p={p} spectrum=[{ev.min():.3f},{ev.max():.3f}]")
    worst = {r: 0.0 for r in radii}
    for it in range(n_pairs):
        l = int(rng.integers(p))
        kind = it % 4
        others = np.setdiff1d(np.arange(p), [l])
        if kind < 3:
            dens = (0.1, 0.5, 0.9)[kind]
            T = others[rng.uniform(size=others.size) < dens]
        else:
            drop = rng.choice(others, size=5, replace=False)
            T = np.setdiff1d(others, drop)
        bT = beta(psi, T, l)
        for r in radii:
            Tp = T[d[l, T] <= r]
            worst[r] = max(worst[r], np.abs(bT - beta(psi, Tp, l)).sum())
    for r in radii:
        print(f"   r={r:>2}  max ||Delta beta||_1 = {worst[r]:.3e}")
    # empirical L0: max ||beta_T(l)||_1
    L0 = 0.0
    for it in range(60):
        l = int(rng.integers(p))
        others = np.setdiff1d(np.arange(p), [l])
        T = others[rng.uniform(size=others.size) < (0.2 + 0.7 * rng.uniform())]
        L0 = max(L0, np.abs(beta(psi, T, l)).sum())
    print(f"   sampled max ||beta_T(l)||_1 = {L0:.3f}")
    # empirical inverse-decay rate over submatrices: fit log|(A^-1)_ij| vs d
    rates = []
    for it in range(10):
        A = np.sort(rng.choice(p, size=int(p * (0.3 + 0.6 * rng.uniform())), replace=False))
        inv = np.linalg.inv(psi[np.ix_(A, A)])
        dd = d[np.ix_(A, A)]
        mask = (dd > 0) & (dd < 1e5)
        y = np.log(np.abs(inv[mask]) + 1e-300)
        # envelope rate: max over distance bins
        bins = np.floor(dd[mask]).astype(int)
        env = [y[bins == b].max() for b in range(1, min(10, bins.max() + 1)) if np.any(bins == b)]
        if len(env) >= 3:
            rates.append(-(np.polyfit(np.arange(len(env)), env, 1)[0]))
    print(f"   inverse-entry envelope decay rate per unit distance (min over 10 submatrices) = {min(rates):.3f}")


if __name__ == "__main__":
    for psi, d, name in (design_exp2d(), design_exp2d(phi=2.0), design_gmrf(), design_rgg()):
        probe(psi, d, name)
