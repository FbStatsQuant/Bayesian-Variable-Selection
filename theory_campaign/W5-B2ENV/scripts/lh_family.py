"""Copied verbatim from W1-EXP scripts/family.py (branch theory/W1-EXP) for self-containment."""
"""The linked-hub equicorrelated-group design family LH(g, rho, psi, links) of W1-EXP.

Population covariance (correlation) Sigma on p = G*g variables:
  * G groups of size g; within group h, equicorrelation rho_h (S3: 0.7, S4: 0.85, S6: 0.4..0.9);
  * each group has a hub position (index of its potential true variable);
  * groups are independent (S3/S4/S6 structure) EXCEPT for disjoint linked pairs (a, b, psi):
        Sigma[C_a, C_b] = psi * Sigma[C_a, j_a] Sigma[j_b, C_b]     (rank one, through the hubs)
    i.e. corr(j_a, j_b) = psi, corr(j_a, k in C_b) = psi*rho_b, corr(k in C_a, k' in C_b) = psi*rho_a*rho_b.
    PSD for |psi| < 1 (Schur complement Sigma_aa - psi^2 a a^T, a = Sigma_aa e_{j_a}).
Truth: theta[j_a] = beta_a, theta[j_b] = -psi*beta_a for each linked pair (j_b is a suppressor: Cov(x_{j_b}, mu) = 0,
in fact Cov(X_{C_b}, mu) = 0 exactly), and theta[j_h] = beta_h for unlinked "visible" groups.
"""
import math
import numpy as np


def lh_sigma(G, g, rho, hub, links):
    rho = np.broadcast_to(np.asarray(rho, float), (G,))
    hub = np.broadcast_to(np.asarray(hub, int), (G,))
    p = G * g
    S = np.zeros((p, p))
    C = [list(range(h * g, (h + 1) * g)) for h in range(G)]
    for h in range(G):
        blk = np.full((g, g), rho[h])
        np.fill_diagonal(blk, 1.0)
        S[np.ix_(C[h], C[h])] = blk
    for (a, b, psi) in links:
        ja, jb = C[a][hub[a]], C[b][hub[b]]
        cross = psi * np.outer(S[C[a], ja], S[jb, C[b]])
        S[np.ix_(C[a], C[b])] = cross
        S[np.ix_(C[b], C[a])] = cross.T
    return S, C


def lh_truth(G, g, hub, links, visible):
    """links: list (a,b,psi); visible: dict group->beta for unlinked true groups; linked pairs use
    beta_a given in visible[a] as well (a must be a key).  Returns theta, S0, masked set M, S_ref = S0 minus M."""
    hub = np.broadcast_to(np.asarray(hub, int), (G,))
    p = G * g
    th = np.zeros(p)
    M = []
    for h, bet in visible.items():
        th[h * g + hub[h]] = bet
    for (a, b, psi) in links:
        jb = b * g + hub[b]
        th[jb] = -psi * visible[a]
        M.append(int(jb))
    S0 = [int(j) for j in sorted(np.flatnonzero(th).tolist())]
    Sref = sorted(set(S0) - set(M))
    return th, S0, sorted(M), Sref


def suff_exact_gram(Sigma, theta, n, sigma, rng):
    """Exact-Gram fixed design X'X = (n-1) Sigma (requires p <= n-1).
    Returns (R, r) = (X'X/(n-1), X'y/(n-1)) for the standardised response, simulated exactly via
    xi = Q'eps ~ N_p(0, I) and an independent chi^2_{n-1-p} (Q = orthonormal centred basis of span X)."""
    p = Sigma.shape[0]
    assert p <= n - 1
    L = np.linalg.cholesky(Sigma)
    xi = rng.standard_normal(p) * sigma
    chi = sigma ** 2 * (rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0)
    XtY = (n - 1) * Sigma @ theta + math.sqrt(n - 1) * L @ xi
    YtY = (n - 1) * theta @ Sigma @ theta + 2 * math.sqrt(n - 1) * theta @ L @ xi + xi @ xi + chi
    sy = math.sqrt(YtY / (n - 1))
    return Sigma.copy(), XtY / ((n - 1) * sy)


def suff_random_design(Sigma, theta, n, sigma, rng):
    """iid Gaussian rows x ~ N(0, Sigma), y = x'theta + eps (raw scale), standardised; via Bartlett Wishart."""
    p = Sigma.shape[0]
    J = np.zeros((p + 1, p + 1))
    J[:p, :p] = Sigma
    J[:p, p] = J[p, :p] = Sigma @ theta
    J[p, p] = theta @ Sigma @ theta + sigma ** 2
    Lj = np.linalg.cholesky(J)
    m = n - 1  # centred cross products ~ Wishart(n-1, J)
    A = np.zeros((p + 1, p + 1))
    for i in range(p + 1):
        A[i, i] = math.sqrt(rng.chisquare(m - i))
        A[i, :i] = rng.standard_normal(i)
    W = Lj @ A @ A.T @ Lj.T
    d = np.sqrt(np.diag(W))
    Rfull = W / np.outer(d, d)
    return Rfull[:p, :p], Rfull[:p, p]
