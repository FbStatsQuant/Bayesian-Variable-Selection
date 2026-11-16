#!/usr/bin/env python3
"""N1 (W3-MISR-R): boundary numerics for CorG-min (STATEMENT.md §2).

Exact enumeration of the coded target pi_C of [W3P] §0 (Theory_work/Wave3/W3-POST/STATEMENT.md:16-29):
X = standardised candidate design (centred, ||x_j||^2 = n-1), y = C y^r / s_y, G_S = X_S'X_S, H_S = (n+1)G_S + I,
D_S = det H_S / det(G_S + I), Q_S = y'y - n z_S' H_S^{-1} z_S, nu = 0.01 + n/2,
log m(S) = -1/2 log D_S - nu log(2 b0 + Q_S), b0 = 0.01, prior w(k) = 1/2 / C(2p-1, k), K = min(p, floor(n/2)).

Candidate design (p = 5): binary entries x_ij = 1{h_i + u_ij > 0}, h an AR(1) process over i (rho = 0.6), u_ij iid N(0,1):
rows are dependent and non-Gaussian (outside BASE Cor-G, inside CorG-min). One omitted column x_M, beta_M = 1;
beta_C = (1, 0.8, 0, 0, 0); epsilon ~ N(0, 1).
Scenarios for the omitted column (Z ~ N(0,1) unless said otherwise):
  IN      x_M = 0.6 x_4 + Z                         (OV) holds: gamma = 0.6 e_4, target {1,2,4}
  OUT-het x_M = 0.6 x_4 + sqrt(2 x_1) Z             conditional covariance not scalar; mean linear; target {1,2,4}
  OUT-rad x_M = 0.6 x_4 + R, R Rademacher           non-Gaussian omitted part (Cramer: GR^c fails); target {1,2,4}
  OUT-nl  x_M = 1.2 x_1 x_2 + Z                     conditional mean not linear in the candidates (no gamma)
For OUT-nl the 'target' is the support of the population best linear predictor of x_M on (1, x_C), estimated once
from 2e6 rows (reported); the theorem says nothing there.
Output: E delta = E[1 - pi(target)] and P(HPM != target), Monte Carlo, R replications per (scenario, n).
"""
import itertools
import math
import sys

import numpy as np

P = 5
BETA_C = np.array([1.0, 0.8, 0.0, 0.0, 0.0])
RHO = 0.6


def design(n, rng):
    h = np.empty(n)
    h[0] = rng.standard_normal()
    e = rng.standard_normal(n) * math.sqrt(1 - RHO ** 2)
    for i in range(1, n):
        h[i] = RHO * h[i - 1] + e[i]
    u = rng.standard_normal((n, P))
    return (h[:, None] + u > 0).astype(float)


def omitted(x, scen, rng):
    n = x.shape[0]
    z = rng.standard_normal(n)
    if scen == "IN":
        return 0.6 * x[:, 3] + z
    if scen == "OUT-het":
        return 0.6 * x[:, 3] + np.sqrt(2.0 * x[:, 0]) * z
    if scen == "OUT-rad":
        return 0.6 * x[:, 3] + rng.choice([-1.0, 1.0], size=n)
    if scen == "OUT-nl":
        return 1.2 * x[:, 0] * x[:, 1] + z
    raise ValueError(scen)


MODELS = [S for k in range(P + 1) for S in itertools.combinations(range(P), k)]


def posterior(x, yr):
    n = x.shape[0]
    xc = x - x.mean(axis=0)
    sd = np.sqrt((xc ** 2).sum(axis=0) / (n - 1))
    if np.any(sd == 0):
        return None
    X = xc / sd
    yc = yr - yr.mean()
    y = yc / math.sqrt((yc ** 2).sum() / (n - 1))
    K = min(P, n // 2)
    nu = 0.01 + n / 2
    b0 = 0.01
    G = X.T @ X
    zf = X.T @ y
    yty = y @ y
    logpost = {}
    for S in MODELS:
        k = len(S)
        if k > K:
            continue
        logw = math.log(0.5) - (math.lgamma(2 * P) - math.lgamma(k + 1) - math.lgamma(2 * P - k))
        if k == 0:
            logD, Q = 0.0, yty
        else:
            idx = list(S)
            GS = G[np.ix_(idx, idx)]
            H = (n + 1) * GS + np.eye(k)
            logD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(GS + np.eye(k))[1]
            z = zf[idx]
            Q = yty - n * z @ np.linalg.solve(H, z)
        logpost[S] = logw - 0.5 * logD - nu * math.log(2 * b0 + Q)
    m = max(logpost.values())
    tot = sum(math.exp(v - m) for v in logpost.values())
    return {S: math.exp(v - m) / tot for S, v in logpost.items()}


def blp_support(rng):
    x = design(2_000_000, rng)
    xm = omitted(x, "OUT-nl", rng)
    A = np.column_stack([np.ones(len(xm)), x])
    coef = np.linalg.lstsq(A, xm, rcond=None)[0][1:]
    bc = BETA_C + coef
    return bc, tuple(j for j in range(P) if abs(bc[j]) > 0.02)


def main():
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    rng = np.random.default_rng(20261115)
    bc_nl, tgt_nl = blp_support(rng)
    print(f"# N1 W3-MISR-R, R = {R} replications, seed 20261115")
    print(f"# OUT-nl population best-linear-predictor coefficient (1e-2 rounding): {np.round(bc_nl, 2).tolist()}; "
          f"support (|coef| > 0.02) = {[j + 1 for j in tgt_nl]}")
    print("scenario  n     E_delta   P(HPM!=target)  r_n")
    for scen in ["IN", "OUT-het", "OUT-rad", "OUT-nl"]:
        tgt = tgt_nl if scen == "OUT-nl" else (0, 1, 3)
        for n in [100, 400, 1600]:
            dl, miss, done = 0.0, 0, 0
            while done < R:
                x = design(n, rng)
                yr = x @ BETA_C + omitted(x, scen, rng) + rng.standard_normal(n)
                post = posterior(x, yr)
                if post is None:
                    continue
                dl += 1 - post.get(tgt, 0.0)
                miss += max(post, key=post.get) != tgt
                done += 1
            print(f"{scen:8s}  {n:5d} {dl / R:9.4f}   {miss / R:9.4f}       {math.sqrt(math.log(n) / n):.4f}")


if __name__ == "__main__":
    main()
