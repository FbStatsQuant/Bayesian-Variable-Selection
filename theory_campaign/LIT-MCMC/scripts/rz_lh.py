"""LIT-MCMC check: do the landscape hypotheses of the published rapid-mixing theorems hold for the PAPER'S OWN target
on the exact-Gram linked-hub (LH) family, at n = 200 and beyond?

Chang & Zhou (arXiv:2404.03867, Thm 1): with M = max_x |N(x)| and R = min_{x != x*} max_{y in N(x)} pi(y)/pi(x),
random-walk MH has Gap^{-1} <= c(rho) M when rho = R/M > 1; informed MH (Thm 2) needs R > M^2.
Zhou & Smith (AISTATS 2022) Assumption 1 is the same with R >= p^nu, M <= p^alpha, nu > alpha.
We compute log_p R, log_p M on (a) the whole capped space M(K), K = min(p, n//2), and (b) the restricted space
X0 = M(s) (Chang-Zhou Thm 4 / ZYVR use a sparse cap s), N = add/delete/swap within the space.
Also: the minimising state x (where the landscape is flattest) and pi(X0^c).
Uses API-POS's copies of W1-EXP's LH constructor and exact v3 score code (unchanged). Seed 20261102 + n.
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lh_family_W1EXP import lh_sigma, lh_truth, suff_exact_gram  # noqa
from cond1_lh import all_logpost, popcount  # noqa

SEED = 20261102


def landscape(lp, p, cap):
    N = 1 << p
    masks = np.arange(N, dtype=np.int64)
    size = popcount(masks.astype(np.uint32))
    inside = (size <= cap) & np.isfinite(lp)
    best = np.full(N, -np.inf)
    for j in range(p):
        bit = 1 << j
        notin = (masks & bit) == 0
        t = masks ^ bit
        ok = inside & inside[t]
        best = np.maximum(best, np.where(ok, lp[t], -np.inf))
    for j in range(p):
        for k in range(p):
            if j == k:
                continue
            bj, bk = 1 << j, 1 << k
            ok0 = ((masks & bj) == 0) & ((masks & bk) != 0)
            t = (masks | bj) & ~bk
            ok = ok0 & inside
            best = np.maximum(best, np.where(ok, lp[t], -np.inf))
    xstar = int(np.argmax(np.where(inside, lp, -np.inf)))
    sel = inside.copy(); sel[xstar] = False
    ratio = np.where(sel, best - lp, np.inf)
    xmin = int(np.argmin(ratio))
    logR = ratio[xmin]
    ks = np.arange(0, cap + 1)
    nb = (np.where(ks < cap, p - ks, 0) + ks + ks * (p - ks))
    M = int(nb.max())
    n_modes = int(np.sum(sel & (ratio <= 0)))
    mass_out = float(np.exp(np.logaddexp.reduce(lp[np.isfinite(lp) & ~inside]))) if np.any(np.isfinite(lp) & ~inside) else 0.0
    return dict(logR=logR, M=M, xstar=xstar, xmin=xmin, n_modes=n_modes, mass_out=mass_out, size_min=int(size[xmin]))


def fmt(m, p):
    return "{" + ",".join(str(j) for j in range(p) if m >> j & 1) + "}"


def run(name, G, g, rho, links, visible, ns, s_small):
    Sigma, C = lh_sigma(G, g, rho, 0, links)
    th, S0, Mk, Sref = lh_truth(G, g, 0, links, visible)
    p = G * g
    s0m = sum(1 << j for j in S0)
    lp_ = math.log(p)
    print(f"## {name}: p={p}, S0={S0}, masked={Mk}")
    print("| n | space | log_p R | log_p M | rho=R/M | R>M (RW-MH, CZ Thm1) | R>M^2 (informed, CZ Thm2) | x* = S0? | argmin x (size) | #local modes | pi(outside) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for n in ns:
        rng = np.random.default_rng(SEED + n)
        R, r = suff_exact_gram(Sigma, th, n, 1.0, rng)
        lp = all_logpost(R, r, n, p)
        for lab, cap in (("M(K)", min(p, n // 2)), (f"M({s_small})", s_small)):
            a = landscape(lp, p, cap)
            lR, lM = a["logR"] / lp_, math.log(a["M"]) / lp_
            print(f"| {n} | {lab} | {lR:.2f} | {lM:.2f} | {math.exp(a['logR'] - math.log(a['M'])):.3g} | "
                  f"{'yes' if lR > lM else 'NO'} | {'yes' if lR > 2 * lM else 'NO'} | {'yes' if a['xstar'] == s0m else 'NO'} | "
                  f"{fmt(a['xmin'], p)} ({a['size_min']}) | {a['n_modes']} | {a['mass_out']:.2e} |", flush=True)


if __name__ == "__main__":
    ns = [200, 1600, 12800, 102400]
    run("LH c=1", 4, 4, 0.7, [(0, 1, 0.5)], {0: 1.0, 2: 1.0}, ns, 6)
    run("LH c=2", 5, 4, 0.85, [(0, 1, 0.5), (2, 3, 0.5)], {0: 1.0, 2: 1.0, 4: 1.0}, ns, 8)
