#!/usr/bin/env python3
"""LIT-PAR G4 demo: SaM-style split-and-merge vs exact posterior on an LH-like masked design.
Design (LH-like, our own construction; NOT the exact W1-EXP family): p = 16, groups {0..3},{5,6,7},{8..11},{12..15} with equicorrelation
rho; variable 4 is a singleton linked only to hub 0 with corr psi; all other correlations 0. Population masking: cov(x4, y) = 0. Truth: theta_0 = beta, theta_4 = -psi*beta (suppressor,
marginally uncorrelated with y in population), theta_8 = beta (visible hub). S0 = {0,4,8}.
Score: Zellner g-prior, g = n, sigma^2 integrated with 1/sigma^2 prior, BB(1,p) size prior, cap K. Exact enumeration.
SaM (Song-Liang 2015 as described in Liang's slides): split predictors into 2 halves; Stage I: exact posterior on each half, keep PIP > 0.5;
Stage II: exact posterior on the merged set, report HPM. Compare: full-posterior HPM; correlation-clustered split {0..7},{8..15}.
Seed fixed (20261103)."""
import itertools, sys
import numpy as np
from math import lgamma

def bb_logprior(k, p):  # BB(1,p) model prior for a specific model of size k: B(k+1, p-k+p)/B(1,p)
    a, b = 1.0, float(p)
    return (lgamma(k + a) + lgamma(p - k + b) - lgamma(p + a + b)) - (lgamma(a) + lgamma(b) - lgamma(a + b))

def enumerate_post(X, y, idx, K, g):
    n = len(y); p_tot = X.shape[1]
    yc = y - y.mean(); Xc = X - X.mean(0)
    yy = yc @ yc
    G = Xc.T @ Xc; z = Xc.T @ yc
    models, lps = [], []
    for k in range(0, min(K, len(idx)) + 1):
        for S in itertools.combinations(idx, k):
            if k == 0:
                R2 = 0.0
            else:
                S_ = list(S)
                b = np.linalg.solve(G[np.ix_(S_, S_)], z[S_])
                R2 = float(z[S_] @ b) / yy
            lm = 0.5 * (n - 1 - k) * np.log1p(g) - 0.5 * (n - 1) * np.log1p(g * (1 - R2))
            models.append(frozenset(S)); lps.append(lm + bb_logprior(k, p_tot))
    lps = np.array(lps); w = np.exp(lps - lps.max()); w /= w.sum()
    pip = {j: 0.0 for j in idx}
    for M, wi in zip(models, w):
        for j in M: pip[j] += wi
    return models[int(np.argmax(lps))], pip

def make_sigma(p=16, gsize=4, rho=0.7, psi=0.5):
    S = np.zeros((p, p))
    for g0 in range(0, p, gsize):
        S[g0:g0+gsize, g0:g0+gsize] = rho
    np.fill_diagonal(S, 1.0)
    S[4, :] = 0.0; S[:, 4] = 0.0; S[4, 4] = 1.0   # partner 4 is a singleton (removed from group {4..7})
    S[0, 4] = S[4, 0] = psi                       # linked only to hub 0
    assert np.linalg.eigvalsh(S).min() > 0
    return S

def main(n=200, beta=0.6, rho=0.7, psi=0.5, reps=20, splits=30, K=6, seed=20261103):
    rng = np.random.default_rng(seed)
    p = 16; Sig = make_sigma(p, 4, rho, psi); L = np.linalg.cholesky(Sig)
    theta = np.zeros(p); theta[0] = beta; theta[4] = -psi * beta; theta[8] = beta
    S0 = frozenset({0, 4, 8}); g = float(n)
    res = dict(full=0, clus=0, sam=0, sam_sep=0, n_sep=0, sam_tog=0, n_tog=0, pip4_sep=[], pip4_tog=[])
    for r in range(reps):
        X = rng.standard_normal((n, p)) @ L.T
        y = X @ theta + rng.standard_normal(n)
        hpm, _ = enumerate_post(X, y, list(range(p)), K, g)
        res['full'] += (hpm == S0)
        def sam(parts):
            keep, pips = [], {}
            for part in parts:
                _, pip = enumerate_post(X, y, sorted(part), K, g)
                pips.update(pip); keep += [j for j in part if pip[j] > 0.5]
            h, _ = enumerate_post(X, y, sorted(keep), K, g) if keep else (frozenset(), None)
            return h, pips
        h, _ = sam([range(0, 8), range(8, 16)])
        res['clus'] += (h == S0)
        for s in range(splits):
            perm = rng.permutation(p); parts = [perm[:8], perm[8:]]
            h, pips = sam(parts)
            sep = (0 in parts[0]) != (4 in parts[0])
            ok = (h == S0)
            res['sam'] += ok
            if sep: res['n_sep'] += 1; res['sam_sep'] += ok; res['pip4_sep'].append(pips[4])
            else: res['n_tog'] += 1; res['sam_tog'] += ok; res['pip4_tog'].append(pips[4])
    print(f"n={n} beta={beta} rho={rho} psi={psi} reps={reps} splits/rep={splits} cap K={K} seed={seed}")
    print(f"full exact posterior: HPM == S0 in {res['full']}/{reps}")
    print(f"SaM, correlation-clustered split {{0..7}},{{8..15}}: HPM == S0 in {res['clus']}/{reps}")
    print(f"SaM, random halves: HPM == S0 in {res['sam']}/{reps*splits}")
    print(f"   splits separating hub pair (0,4): {res['sam_sep']}/{res['n_sep']} recover S0; median Stage-I PIP of x4 = {np.median(res['pip4_sep']):.3g}")
    print(f"   splits keeping pair together:     {res['sam_tog']}/{res['n_tog']} recover S0; median Stage-I PIP of x4 = {np.median(res['pip4_tog']):.3g}")

if __name__ == '__main__':
    b = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
    main(beta=b)
