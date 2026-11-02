"""API-POS check: is the masking of LH a property of the start law pi_0 only, or also of the
target posterior pi?  Concretely, on the exact-Gram LH family and the PAPER'S OWN target
(ridge g-prior g = n, IG(0.01, 0.01), BB(1, p) capped at K = min(p, n/2)), compute by exact enumeration:

  * c1(cap) := min over underfitted gamma (S0 not subset of gamma, |gamma| < cap) of
               max_{j in S0 minus gamma} log_p [pi(gamma + j)/pi(gamma)]          (ZYVR Condition (1b))
  * c1s(cap): the same for |gamma| = cap with swap moves (j in S0 minus gamma, k in gamma minus S0)   (1c)
  * c0(cap) := -max over overfitted gamma (S0 subset gamma, |gamma| < cap), j not in gamma, of
               log_p [pi(gamma + j)/pi(gamma)]                                   (ZYVR Condition (1a))
  * number of local modes of pi w.r.t. add/delete/swap on M(K) (whole space) and on M(cap);
  * log pi_0(S0) (start, masked) and pi(S0) (target);
  * hitting time of S0 for the Yang-Wainwright-Jordan symmetric RW-MH chain (their eq. (3)) on M(K),
    started at the empty model and at the start mode, 40 replicates each.

Seed fixed (20261102).  Uses W1-EXP's verified LH constructor and exact v3 score code (copied verbatim).
Usage: python cond1_lh.py
"""
import math
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lh_family_W1EXP import lh_sigma, lh_truth, suff_exact_gram  # noqa: E402
import bvs_exact_W1EXP as bx  # noqa: E402
import itertools  # noqa: E402

SEED = 20261102


def all_logpost(R, r, n, p):
    """log pi over all 2^p bitmasks (models above the cap K get -inf)."""
    K = min(p, n // 2)
    lp = np.full(1 << p, -np.inf)
    for k in range(K + 1):
        combs = np.array(list(itertools.combinations(range(p), k)), dtype=int)
        if k == 0:
            combs = np.zeros((1, 0), dtype=int)
        lm = bx.log_m_batch(combs, R, r, n) + bx.log_w(k, p)
        masks = (np.left_shift(1, combs)).sum(axis=1) if k > 0 else np.array([0])
        lp[masks] = lm
    finite = np.isfinite(lp)
    lz = np.logaddexp.reduce(lp[finite])
    lp[finite] -= lz
    return lp


def popcount(a):
    return np.array([bin(x).count("1") for x in a]) if False else np.unpackbits(
        a.astype(">u4").view(np.uint8).reshape(-1, 4), axis=1).sum(axis=1)


def analyse(lp, p, S0, cap):
    N = 1 << p
    masks = np.arange(N, dtype=np.int64)
    size = popcount(masks.astype(np.uint32))
    s0m = sum(1 << j for j in S0)
    over = (masks & s0m) == s0m
    inside = size <= cap
    logp = math.log(p)
    best_add_true = np.full(N, -np.inf)   # max over j in S0\gamma of log ratio
    best_add_any = np.full(N, -np.inf)    # max over j notin gamma
    nbr_best = np.full(N, -np.inf)         # best neighbour (add/del/swap) within M(cap)
    for j in range(p):
        bit = 1 << j
        notin = (masks & bit) == 0
        tgt = masks | bit
        ok = notin & inside & (size + 1 <= cap)
        d = np.where(ok, lp[tgt] - lp, -np.inf)
        best_add_any = np.maximum(best_add_any, d)
        if bit & s0m:
            best_add_true = np.maximum(best_add_true, d)
        nbr_best = np.maximum(nbr_best, np.where(ok, lp[tgt], -np.inf))
        okd = (~notin) & inside
        nbr_best = np.maximum(nbr_best, np.where(okd, lp[masks ^ bit], -np.inf))
    # swaps (only needed for local-mode count and (1c))
    best_swap_true = np.full(N, -np.inf)
    for j in range(p):
        for k in range(p):
            if j == k:
                continue
            bj, bk = 1 << j, 1 << k
            ok = ((masks & bj) == 0) & ((masks & bk) != 0) & inside
            tgt = (masks | bj) ^ bk
            nbr_best = np.maximum(nbr_best, np.where(ok, lp[tgt], -np.inf))
            if (bj & s0m) and not (bk & s0m):
                best_swap_true = np.maximum(best_swap_true, np.where(ok, lp[tgt] - lp, -np.inf))
    under = (~over) & inside
    u_lt = under & (size < cap)
    u_eq = under & (size == cap)
    c1 = best_add_true[u_lt].min() / logp
    c1s = best_swap_true[u_eq].min() / logp if u_eq.any() else float("nan")
    o_lt = over & inside & (size < cap)
    c0 = -best_add_any[o_lt].max() / logp if o_lt.any() else float("nan")
    modes = np.flatnonzero(inside & np.isfinite(lp) & (lp >= nbr_best))
    return dict(c1=c1, c1s=c1s, c0=c0, n_modes=len(modes), modes=modes[:5].tolist())


def rwmh_hit(lp, p, start_mask, target_mask, rng, maxit=200000):
    """YWJ chain (3): w.p. 1/2 single flip (uniform j), w.p. 1/2 double flip (uniform (k,l) in S x S^c)."""
    g = start_mask
    for t in range(maxit):
        if g == target_mask:
            return t
        if rng.random() < 0.5:
            j = int(rng.integers(p))
            h = g ^ (1 << j)
        else:
            ins = [i for i in range(p) if g >> i & 1]
            if not ins:
                continue
            outs = [i for i in range(p) if not g >> i & 1]
            k = ins[int(rng.integers(len(ins)))]
            l = outs[int(rng.integers(len(outs)))]
            h = g ^ (1 << k) ^ (1 << l)
        a = lp[h] - lp[g]
        if np.isfinite(lp[h]) and (a >= 0 or rng.random() < math.exp(a)):
            g = h
    return maxit


def run(name, G, g, rho, psi_links, visible, ns, cap, sigma=1.0):
    rng = np.random.default_rng(SEED)
    hub = 0
    Sigma, C = lh_sigma(G, g, rho, hub, psi_links)
    th, S0, M, Sref = lh_truth(G, g, hub, psi_links, visible)
    p = G * g
    print(f"## {name}: p={p}, G={G}, g={g}, rho={rho}, links={psi_links}, S0={S0}, masked={M}, S°={Sref}, cap={cap}")
    print("| n | log10 pi0(S0) | pi(S0) | c1 (1b) | c1s (1c) | c0 (1a) | #local modes M(cap) | modes(K) | YWJ hit from empty: median / max | from start mode: median / max |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    s0m = sum(1 << j for j in S0)
    for n in ns:
        R, r = suff_exact_gram(Sigma, th, n, sigma, rng)
        lp = all_logpost(R, r, n, p)
        B = bx.block_size_B(n, p)
        blocks = bx.make_blocks(R, B)
        tabs = bx.tables(blocks, R, r, n)
        sm = bx.start_masses(blocks, tabs, p, n, S0)
        l0S0 = bx.start_logmass(blocks, tabs, p, n, S0, sm["logZ0"])
        # start mode by enumeration of the product form
        best, bestS = -np.inf, None
        for k in range(0, 7):
            for S in itertools.combinations(range(p), k):
                v = bx.start_logmass(blocks, tabs, p, n, S, sm["logZ0"])
                if v > best:
                    best, bestS = v, S
        a = analyse(lp, p, S0, cap)
        aK = analyse(lp, p, S0, min(p, n // 2))
        smask = sum(1 << j for j in bestS)
        h0 = [rwmh_hit(lp, p, 0, s0m, rng) for _ in range(40)]
        h1 = [rwmh_hit(lp, p, smask, s0m, rng) for _ in range(40)]
        print(f"| {n} | {l0S0/math.log(10):.2f} | {math.exp(lp[s0m]):.4f} | {a['c1']:.2f} | {a['c1s']:.2f} | {a['c0']:.2f} | "
              f"{a['n_modes']} | {aK['n_modes']} | {int(np.median(h0))} / {max(h0)} | {int(np.median(h1))} / {max(h1)} |",
              flush=True)
        print(f"<!-- n={n}: blocks={blocks}; start mode={bestS}; modes(cap)={a['modes']}; c1(K)={aK['c1']:.2f}, c0(K)={aK['c0']:.2f} -->", flush=True)


if __name__ == "__main__":
    ns = [200, 1600, 12800, 102400]
    run("LH c=1", 4, 4, 0.7, [(0, 1, 0.5)], {0: 1.0, 2: 1.0}, ns, cap=6)
    run("LH c=2", 5, 4, 0.85, [(0, 1, 0.5), (2, 3, 0.5)], {0: 1.0, 2: 1.0, 4: 1.0}, ns, cap=8)
