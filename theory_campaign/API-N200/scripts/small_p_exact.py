#!/usr/bin/env python3
"""API-N200: exact small-p enumeration of the one non-rigorous step of Thm N200.

Thm N200 bounds the posterior-miss term by P(S-dagger != S0 | X).  O-SWAP computes the ONE-MOVE event
L = {some add/drop/swap neighbour of S0 beats S0}, which is a rigorous lower bound (L implies S-dagger != S0).
Here, at p = 12 (|Omega| = 2^12 = 4096, all feasible since K = min(p, n/2) = 12), we enumerate Omega exactly and
measure, over R noise draws given X:
    P_post = P(S-dagger != S0 | X)   (exact argmax over Omega, exact score F of 00_COMMON.md)
    P_L    = P(L | X)
    excess = P_post - P_L            (the multi-move-only posterior misses)
    P_L2   = P(some model within Hamming distance 2 beats S0)
and the brackets max_e p_e <= P_L <= sum_e p_e (exact-score, one-move events).
Designs: iid Gaussian; equicorrelated 0.3 (S5-like); look-alike blocks with r = 0.85 (S4-like).
Fixed seed. Output: results/small_p_exact.txt
"""
import itertools, os, sys, time
import numpy as np
from scipy.special import gammaln

A0 = B0 = 0.01
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results")
os.makedirs(OUT, exist_ok=True)

def log_prior_table(p, n):
    K = min(p, n // 2)
    k = np.arange(K + 1)
    lw = np.log(0.5) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
    lC = gammaln(p + 1) - gammaln(k + 1) - gammaln(p - k + 1)
    lWK = np.logaddexp.reduce(lC + lw)
    return lw - lWK, K

def standardise_X(X):
    n = X.shape[0]
    Xc = X - X.mean(0)
    return Xc / np.sqrt((Xc ** 2).sum(0) / (n - 1))

def make_design(kind, n, p, rng):
    if kind == "iid":
        Sigma = np.eye(p)
    elif kind == "equi0.3":
        Sigma = 0.3 * np.ones((p, p)) + 0.7 * np.eye(p)
    elif kind == "lookalike0.85":   # blocks of 3: (truth, proxy, proxy) with r = 0.85 within block
        Sigma = np.eye(p)
        for b in range(0, p, 3):
            idx = list(range(b, min(b + 3, p)))
            for i in idx:
                for j in idx:
                    if i != j: Sigma[i, j] = 0.85
    else:
        raise ValueError(kind)
    Lc = np.linalg.cholesky(Sigma)
    return standardise_X(rng.standard_normal((n, p)) @ Lc.T)

def all_models(p):
    models = []
    for k in range(p + 1):
        for S in itertools.combinations(range(p), k):
            models.append(S)
    return models

def run(kind, c, n=40, p=12, R=2000, seed=20261102):
    rng = np.random.default_rng(seed)
    X = make_design(kind, n, p, rng)
    s0 = 3
    S0 = (0, 3, 6)                       # one truth per look-alike block in the block design
    beta = np.array([1.4, -1.0, 1.8]) * c
    mu = X[:, list(S0)] @ beta
    lprior, K = log_prior_table(p, n)
    nu = A0 + n / 2
    logC = A0 * np.log(2 * B0) + gammaln(nu) - (n / 2) * np.log(np.pi) - gammaln(A0)
    models = [S for S in all_models(p) if len(S) <= K]
    M = len(models)
    # noise draws, standardise y as the method does (y = C y / s_y)
    Eps = rng.standard_normal((n, R))
    Y = mu[:, None] + Eps
    Y = Y - Y.mean(0)
    Y = Y / np.sqrt((Y ** 2).sum(0) / (n - 1))
    yy = (Y ** 2).sum(0)
    Fm = np.empty((M, R))
    for m, S in enumerate(models):
        k = len(S)
        if k == 0:
            Fm[m] = lprior[0] + logC - nu * np.log(2 * B0 + yy); continue
        XS = X[:, list(S)]
        G = XS.T @ XS
        H = (n + 1) * G + np.eye(k)
        ldD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(k))[1]
        A = XS @ np.linalg.solve(H, XS.T)            # n x n
        Q = yy - n * np.einsum("ir,ir->r", Y, A @ Y)
        Fm[m] = lprior[k] + logC - 0.5 * ldD - nu * np.log(2 * B0 + Q)
    idx = {S: m for m, S in enumerate(models)}
    m0 = idx[S0]
    F0 = Fm[m0]
    # S-dagger: total order = larger F, then smaller size, then lexicographic (ties have prob 0 here)
    arg = Fm.argmax(0)
    post_miss = arg != m0
    # Hamming distances
    sets = [set(S) for S in models]
    S0s = set(S0)
    dist = np.array([len(s ^ S0s) for s in sets])
    one = [m for m in range(M) if dist[m] == 1 or (dist[m] == 2 and len(sets[m]) == s0)]   # adds, drops, swaps
    two = [m for m in range(M) if 1 <= dist[m] <= 2]
    beats = Fm > F0[None, :]
    L1 = beats[one].any(0)
    L2 = beats[two].any(0)
    pe = beats[one].mean(1)
    # exact posterior mass of S0 over Omega (log-sum-exp), hence delta1 = 1 - pi(S0) and T21's Markov term 2 E delta1
    Fmax = Fm.max(0)
    logZ = Fmax + np.log(np.exp(Fm - Fmax[None, :]).sum(0))
    piS0 = np.exp(F0 - logZ)
    delta1 = 1 - piS0
    res = dict(kind=kind, c=c, n=n, p=p, R=R, M=M,
               P_post=post_miss.mean(), P_L=L1.mean(), P_L2=L2.mean(),
               excess=(post_miss & ~L1).mean(), excess2=(post_miss & ~L2).mean(),
               max_pe=pe.max(), sum_pe=min(1.0, pe.sum()),
               E_delta1=delta1.mean(), two_E_delta1=min(2 * delta1.mean(), 9.99), P_half=(piS0 <= 0.5).mean(),
               mean_dist_of_Sdagger_on_miss=(dist[arg][post_miss].mean() if post_miss.any() else float("nan")),
               max_dist_of_Sdagger=int(dist[arg].max()))
    # sanity: L implies post miss (deterministic inclusion), never violated
    assert not (L1 & ~post_miss).any()
    return res

if __name__ == "__main__":
    t0 = time.time()
    out = []
    hdr = "kind | c | P_post=P(S-dagger!=S0) | P_L (one-move) | P_L2 (Hamming<=2) | excess=P_post-P_L | excess2 | max_e p_e | sum_e p_e | mean/max dist of S-dagger | P(pi(S0)<=1/2) | 2 E delta1 (T21 term)"
    out.append(hdr)
    for kind in ("iid", "equi0.3", "lookalike0.85"):
        for c in (0.35, 0.5, 0.75, 1.0):
            r = run(kind, c)
            out.append(f"{kind} | {c} | {r['P_post']:.4f} | {r['P_L']:.4f} | {r['P_L2']:.4f} | {r['excess']:.4f} | {r['excess2']:.4f} | {r['max_pe']:.4f} | {r['sum_pe']:.4f} | {r['mean_dist_of_Sdagger_on_miss']:.2f}/{r['max_dist_of_Sdagger']} | {r['P_half']:.4f} | {r['two_E_delta1']:.3f}")
            print(out[-1], flush=True)
    out.append(f"(n = 40, p = 12, s0 = 3, beta = c*(1.4,-1,1.8), sigma = 1, R = 2000 noise draws per design, one design per kind, seed 20261102; {time.time()-t0:.0f} s)")
    with open(os.path.join(OUT, "small_p_exact.txt"), "w") as f:
        f.write("\n".join(out) + "\n")
