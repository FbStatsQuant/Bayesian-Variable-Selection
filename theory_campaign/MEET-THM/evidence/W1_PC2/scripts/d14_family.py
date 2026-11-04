"""PC2: non-vacuity check of R1_C §E IC3 exhibit (D14) at its own sizes.
Design: p = 9 floor(n^{1/3}/9); groups of nine, within corr 1/4, every cross corr eps_n = 1/(n p); exact centred Gram
X'X = (n-1) Sigma_n; model G with sigma^2 = 1, one coefficient n^{-1/4} in each of two groups (standardised scale).
Exact sufficient statistics are simulated (bvs_common.exact_gram_suff).  Reports B, K, whether the exact branch fires,
whether complete linkage + cut + next-fit gives blocks = groups (checked analytically: strict separation, 9 <= B < 18),
lambda_min, a, dA, dH, r, nu a^2, K(dA+dH), nu r, D_*.  Also a variant with larger cross correlation eps = c n^{-1/2}/p
to probe how far the bound stays O(1).  10 seeds per n; < 1 minute."""
import math
import numpy as np
from math import comb
from bvs_common import exact_gram_suff, card_Dstar, A0


def sigma_E(p, eps, rho=0.25, g=9):
    gid = np.arange(p) // g
    S = np.where(gid[:, None] == gid[None, :], rho, eps)
    np.fill_diagonal(S, 1.0)
    return S, gid


def exact_branch(n, p):
    K = min(p, n // 2)
    N0 = max(2500, n, p)
    H0 = math.ceil(512 * N0 / 2500)
    E = sum(comb(p, k) for k in range(K + 1))
    return E <= (5 * H0 + 4 * N0) * p


for label, epsf in (("eps=1/(np) [card]", lambda n, p: 1.0 / (n * p)),
                    ("eps=n^-1/2/p", lambda n, p: n ** -0.5 / p),
                    ("eps=0.01 fixed", lambda n, p: 0.01)):
    print(f"=== {label}")
    for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 2 * 10 ** 7, 10 ** 8):
        p = 9 * int(n ** (1 / 3) / 9 + 1e-12)
        if p < 18:
            print(f"n={n}: p={p} (fewer than two groups; design undefined/degenerate)")
            continue
        K = min(p, n // 2)
        B = min(math.isqrt(n), math.isqrt(p), 16)
        eps = epsf(n, p)
        Sig, gid = sigma_E(p, eps)
        lmin = float(np.linalg.eigvalsh(Sig).min())
        sep = (1 - 0.25) < (1 - abs(eps))
        blocks_eq_groups = sep and 9 <= B < 18
        Ds = []
        for seed in range(10):
            rng = np.random.default_rng(1000 + seed)
            theta = np.zeros(p)
            theta[0] = theta[9] = n ** -0.25
            G, z, Y, nn = exact_gram_suff(Sig, theta, n, 1.0, rng)
            blocks = [list(np.where(gid == g)[0]) for g in range(p // 9)]
            cs = card_Dstar(G, z, Y, n, blocks, K)
            Ds.append(cs)
        D = np.array([c['Dstar'] for c in Ds])
        a = np.array([c['a'] for c in Ds])
        nua2 = np.array([c['nu'] * c['a'] ** 2 for c in Ds])
        Kd = np.array([K * (c['dA'] + c['dH']) for c in Ds])
        nur = np.array([c['nu'] * c.get('r', np.nan) for c in Ds])
        print(f"n={n:>9} p={p:>3} K={K:>3} B={B:>2} exact_branch={exact_branch(n, p)} blocks=groups={blocks_eq_groups}"
              f" lmin={lmin:.4f} a~{np.median(a):.3g} nu*a^2~{np.median(nua2):.3g} K(dA+dH)~{np.median(Kd):.3g}"
              f" nu*r~{np.median(nur):.3g} D*: med {np.median(D):.3g} max {D.max():.3g}")
