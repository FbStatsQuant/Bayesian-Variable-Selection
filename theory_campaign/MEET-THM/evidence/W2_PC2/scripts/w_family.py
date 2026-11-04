"""W2_PC2: R2_C §R3 IC3 exhibit W, checked with the method's OWN partition actually computed.
W: p = 9 floor(n^{1/3}/9); groups of 9, within corr 1/4, every cross corr eps_n = 1/(n p); exact centred Gram
X'X = (n-1) Sigma; sigma^2 = 1; one coefficient n^{-1/4} in each of two groups.  Partition = complete linkage on
1-|r| (scipy, then the coded top-down size cut at B and next-fit packing, M §6.3 / v3_blocks.h), B = min(isqrt n,
isqrt p, 16) (v3_preprocess.R:22).  Reports blocks == groups, eps > 0, a, dA, dH, r, C_sigma, b_X, D_*, the
§R5 proxy eps_hat, kappa and the C16 proxy bounds on dA, dH.  Also fixed-eps and n^{-1/2}/p variants.  10 seeds.
"""
import math, sys
import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
from bvs_common import exact_gram_suff, card_Dstar, next_fit


def sigma_W(p, eps, rho=0.25, g=9):
    gid = np.arange(p) // g
    S = np.where(gid[:, None] == gid[None, :], rho, eps)
    np.fill_diagonal(S, 1.0)
    return S, gid


def method_partition(Sig, B):
    p = Sig.shape[0]
    Dm = 1 - np.abs(Sig)
    np.fill_diagonal(Dm, 0)
    Z = linkage(squareform(Dm, checks=False), method='complete')
    kids = {i: i for i in range(p)}
    for k, (a, b, h, c) in enumerate(Z):
        kids[p + k] = (kids[int(a)], kids[int(b)])
    root = kids[2 * p - 2]

    def lv(t):
        return [t] if isinstance(t, (int, np.integer)) else lv(t[0]) + lv(t[1])

    def cut(t):
        L = lv(t)
        if len(L) <= B:
            return [sorted(L)]
        c0, c1 = t
        if min(lv(c0)) > min(lv(c1)):
            c0, c1 = c1, c0
        return cut(c0) + cut(c1)
    return next_fit(cut(root), B)


def proxy(G, blocks, n):
    p = G.shape[0]
    bid = np.empty(p, int)
    for b, C in enumerate(blocks):
        bid[C] = b
    cross = bid[:, None] != bid[None, :]
    eh = float(np.max(np.abs(G[cross])) / (n - 1)) if cross.any() else 0.0
    kap = min(float(np.linalg.eigvalsh(G[np.ix_(C, C)] / (n - 1)).min()) for C in blocks)
    bA = (n - 1) * (p - 1) * eh / (1 + (n - 1) * kap)
    bH = (n * n - 1) * (p - 1) * eh / (1 + (n * n - 1) * kap)
    return eh, kap, bA, bH


ns = [531440, 531441, 10 ** 6, 2 * 10 ** 7, 10 ** 8]
for label, epsf in (("W card eps=1/(np)", lambda n, p: 1.0 / (n * p)),
                    ("eps=n^-1/2/p", lambda n, p: n ** -0.5 / p),
                    ("eps=0.01 fixed", lambda n, p: 0.01)):
    print("===", label)
    for n in ns:
        p = 9 * int(n ** (1 / 3) / 9 + 1e-12)
        K = min(p, n // 2)
        B = min(math.isqrt(n), math.isqrt(p), 16)
        eps = epsf(n, p)
        Sig, gid = sigma_W(p, eps)
        groups = [list(np.where(gid == g)[0]) for g in range(p // 9)]
        blocks = method_partition(Sig, B)
        beq = sorted(map(sorted, blocks)) == sorted(map(sorted, groups))
        lmin = float(np.linalg.eigvalsh(Sig).min())
        rows = []
        for seed in range(10):
            rng = np.random.default_rng(2000 + seed)
            th = np.zeros(p); th[0] = th[9] = n ** -0.25
            G, z, Y, _ = exact_gram_suff(Sig, th, n, 1.0, rng)
            cs = card_Dstar(G, z, Y, n, blocks, K)
            eh, kap, bA, bH = proxy(G, blocks, n)
            rows.append((cs, eh, kap, bA, bH))
        D = np.array([r[0]['Dstar'] for r in rows])
        ok = all(r[0]['ok'] for r in rows)
        proxy_ok = all(r[3] >= r[0]['dA'] - 1e-15 and r[4] >= r[0]['dH'] - 1e-15 for r in rows)
        r0 = rows[0]
        print(f"n={n:>9} p={p:>3} K={K:>3} B={B:>2} blocks==groups={beq} nblocks={len(blocks)} eps={eps:.3g} "
              f"lmin={lmin:.4f} domain_ok(10/10)={ok} "
              f"a~{np.median([r[0]['a'] for r in rows]):.3g} dA={r0[0]['dA']:.3g} dH={r0[0]['dH']:.3g} "
              f"Csig~{np.median([r[0].get('shared', np.nan) for r in rows]):.3g} "
              f"bX~{np.median([r[0].get('bX', np.nan) for r in rows]):.3g} D*: med {np.median(D):.3g} max {D.max():.3g} | "
              f"eps_hat={r0[1]:.3g} kappa={r0[2]:.4f} proxy_bA={r0[3]:.3g} proxy_bH={r0[4]:.3g} proxy>=delta:{proxy_ok}")
