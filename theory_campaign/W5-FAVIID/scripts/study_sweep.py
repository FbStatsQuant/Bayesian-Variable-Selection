"""W5-FAVIID study sweep: exact start law on S1/S3/S4/S6, p in {500,1000}, scale in {0.5,1}, n in {200,...,3200}.
Seed: 5000000 + 100000*scen + 1000*(p//500) + 10*nidx + rep  (one X and one eps per (scen,p,n,rep), shared by both
scales, as in gen_dev_data.R). Output: results/sweep.jsonl (one line per design x scale).

Per design and scale it records:
  B, #blocks, Q_n (blocks are unions of groups), max # truth-carrying groups per block (m_real), co-blocked group pairs;
  log10 pi0(S0) (exact, capped convolution); T22(i) q and log e at reference S0 and the bound (s0+1)q/(1-q) + s0 e;
  N_add = sum_{l not in S0} pi0(S0+l)/pi0(S0) (exact);
  per truth j: LO0(j) = log pi0(S0) - log pi0(S0 - j); best same-group proxy swap log-odds max_l log pi0(S0-j+l)/pi0(S0);
  Theorem B check: Q_real = (p-s0)^-1 sum_K D'_{K,W(K)} at the realised truth contexts W(K), Q_0 = same with W = {} for all K.
Usage: python3 study_sweep.py [reps] [nproc]
"""
import json, math, sys, itertools
import numpy as np
from multiprocessing import Pool
from scipy.special import gammaln, logsumexp
import pxn_core as pc
import fav_core as fc

NS = [200, 400, 800, 1600, 3200]


def rss_y(D, T):
    """RSS^y_T = y'(I-P_T)y for the standardised data."""
    if len(T) == 0:
        return float(D.y @ D.y)
    G = D.X[:, T].T @ D.X[:, T]
    z = D.z[T]
    return float(D.y @ D.y - z @ np.linalg.solve(G, z))


def dprime(D, K, U, nfree_idx):
    """D'_{K,W} with U = truths(K) u W: max_j (j! a'_j)^{1/j}, a'_j = sum_{|V|=j} (n+1)^{-j/2}(1-X')^{-nu} (no truncation)."""
    n, nu = D.n, D.nu
    rU = rss_y(D, U)
    la = {}
    for j in range(1, len(nfree_idx) + 1):
        vals = []
        for V in itertools.combinations(nfree_idx, j):
            rA = rss_y(D, sorted(U + list(V)))
            vals.append(-0.5 * j * math.log(n + 1) - nu * math.log(rA / rU))
        la[j] = logsumexp(vals)
    return max(math.exp((gammaln(j + 1) + la[j]) / j) for j in la)


def run(args):
    scen, p, nidx, rep = args
    n = NS[nidx]
    seed = 5000000 + 100000 * scen + 1000 * (p // 500) + 10 * nidx + rep
    rng = np.random.default_rng(seed)
    X = fc.gen_raw_X(scen, n, p, rng)
    eps = rng.standard_normal(n)
    active, beta, tgrp = fc.truth(p)
    Xs = X[:, active] - X[:, active].mean(0)
    Xs /= np.sqrt((Xs ** 2).sum(0) / (n - 1))
    signal = Xs @ beta
    S0 = sorted(active.tolist())
    groups = fc.groups_of(p, scen)
    gid = np.repeat(np.arange(p // 5), 5) if scen != 1 else np.arange(p)
    D0 = pc.Data(X, signal + eps)
    blocks = pc.v3_blocks(D0)
    unions = fc.blocks_are_unions(blocks, groups)
    tg = set(gid[S0].tolist())
    m_real = max(len(set(gid[C].tolist()) & tg) for C in blocks)
    max_truths = max(len(set(C) & set(S0)) for C in blocks)
    pairs = []
    if scen != 1:
        for C in blocks:
            hs = sorted(set(gid[C].tolist()))
            pairs += [list(x) for x in itertools.combinations(hs, 2)]
    out = []
    for scale in (0.5, 1.0):
        D = pc.Data(X, scale * signal + eps)
        T = fc.FastTables(D, blocks)
        SL = pc.StartLaw(T)
        lp0 = SL.log_pi0(S0)
        q, loge = pc.agg_q_e(T, S0)
        s0 = len(S0)
        bound = (s0 + 1) * q / (1 - q) + s0 * math.exp(loge) if q < 1 else float("inf")
        # exact one-change odds
        lw = lambda k: float(pc.log_w(k, p))
        base_r = T.log_r(S0)
        S0set = set(S0)
        ladd = []
        for b, C in enumerate(blocks):
            um = T.mask(b, S0)
            for t, l in enumerate(C):
                if l in S0set:
                    continue
                ladd.append(T.lr[b][um | (1 << t)] - T.lr[b][um])
        log_Nadd = lw(s0 + 1) - lw(s0) + logsumexp(ladd)
        LO, LSW = [], []
        for j in S0:
            b, t = T.where[j]
            um = T.mask(b, S0)
            LO.append(lw(s0) - lw(s0 - 1) + T.lr[b][um] - T.lr[b][um & ~(1 << t)])
            best = -np.inf
            for l in groups[gid[j]]:
                if l == j or l in S0set:
                    continue
                b2, t2 = T.where[l]
                if b2 != b:
                    continue
                best = max(best, T.lr[b][(um & ~(1 << t)) | (1 << t2)] - T.lr[b][um])
            LSW.append(best)
        # Theorem B factorisation check (block-diagonal scenarios with groups of 5 only; cheap there)
        Qreal = Q0 = None
        if scen != 1:
            sreal = s0_ = 0.0
            for C in blocks:
                hs = sorted(set(gid[C].tolist()))
                Ub = sorted(set(C) & S0set)
                for h in hs:
                    K = groups[h]
                    TK = [j for j in K if j in S0set]
                    free = [j for j in K if j not in S0set]
                    sreal += dprime(D, K, Ub, free)
                    s0_ += dprime(D, K, TK, free)
            Qreal, Q0 = sreal / (p - s0), s0_ / (p - s0)
        out.append(dict(scen=scen, p=p, n=n, rep=rep, scale=scale, B=D.B, J=len(blocks), unions=bool(unions),
                        m_real=int(m_real), max_truths=int(max_truths), n_pairs=len(pairs),
                        pairs=pairs if (scale == 0.5 and rep < 4) else None,
                        log10_pi0_S0=lp0 / math.log(10), q=q, log10_e=loge / math.log(10), T22i_bound=bound,
                        log_Nadd=log_Nadd, LO=LO, LSW=LSW, Qreal=Qreal, Q0=Q0, theta=(scale * beta).tolist()))
    return out


if __name__ == "__main__":
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    jobs = [(s, p, ni, r) for s in (1, 3, 4, 6) for p in (500, 1000) for ni in range(len(NS)) for r in range(reps)]
    jobs.sort(key=lambda j: -NS[j[2]])
    with Pool(nproc) as pool, open("../results/sweep.jsonl", "w") as f:
        for res in pool.imap_unordered(run, jobs):
            for row in res:
                f.write(json.dumps(row) + "\n")
            f.flush()
