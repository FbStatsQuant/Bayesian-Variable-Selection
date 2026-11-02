"""
Vectorised simulation of the actual terminal round K_1 (phi = 1) from a fixed start, with exact scores.
Each replicate draws a fresh uniform order of the m = p + 1 + n_nb + 1 labels every round (METHODOLOGY s6.5).
Records, per replicate: first round in which S0 is scored (SR: both Gibbs configurations, every swap and
independence proposal, accepted or not), and per round: progress (V_end < V_start or S0 scored), any
non-fatal V-increase, any exit from R.
"""
import numpy as np
from bvs_engine import *


def popcount_vec(a):
    a = a.copy(); c = np.zeros_like(a)
    while a.any():
        c += a & 1; a >>= 1
    return c


def kth_set_bit(a, k, p):
    """position of the k-th (0-based) set bit of a (vectorised)."""
    pos = np.full(a.shape, -1, dtype=np.int64)
    cnt = np.zeros_like(a)
    for j in range(p):
        bit = (a >> j) & 1
        hit = (bit == 1) & (cnt == k) & (pos < 0)
        pos[hit] = j
        cnt += bit
    return pos


def simulate(M, x0, H, reps, rng, inR=None, V=None):
    p = M.p; S0 = M.S0; F = M.F; full = (1 << p) - 1
    m = M.m_labels
    X = np.full(reps, x0, dtype=np.int64)
    scored = np.zeros(reps, bool)
    first = np.full(reps, -1)
    cum0 = np.cumsum(M.pi0); cum0 /= cum0[-1]
    Nb = np.array(M.Nb, dtype=np.int64)
    NbSize = None
    prog = np.zeros((H, reps), bool); incr = np.zeros((H, reps), bool); exitr = np.zeros((H, reps), bool)
    alive_exit = np.zeros(reps, bool)
    for h in range(H):
        Vstart = V[X] if V is not None else None
        orders = np.argsort(rng.random((reps, m)), axis=1)   # uniform permutations
        for t in range(m):
            lab = orders[:, t]
            Xold = X.copy()
            # Gibbs labels 0..p-1
            g = lab < p
            if g.any():
                j = lab[g]; bit = (1 << j).astype(np.int64)
                xs = X[g]; xp = xs | bit; xm = xs & ~bit
                scored[g] |= (xp == S0) | (xm == S0)
                sz = popcount_vec(xp)
                o = 1.0 / (1.0 + np.exp(F[xm] - F[xp]))
                o[sz > M.K] = 0.0
                u = rng.random(g.sum())
                X[g] = np.where(u < o, xp, xm)
            # uniform swap label p
            us = lab == p
            if us.any():
                xs = X[us]; k = popcount_vec(xs)
                ok = (k > 0) & (k < p)
                jj = kth_set_bit(xs, (rng.random(us.sum()) * np.maximum(k, 1)).astype(np.int64), p)
                comp = (~xs) & full
                ll = kth_set_bit(comp, (rng.random(us.sum()) * np.maximum(p - k, 1)).astype(np.int64), p)
                prop = (xs & ~(1 << np.maximum(jj, 0))) | (1 << np.maximum(ll, 0))
                prop = np.where(ok, prop, xs)
                scored[us] |= ok & (prop == S0)
                acc = np.minimum(1.0, np.exp(F[prop] - F[xs]))
                X[us] = np.where(ok & (rng.random(us.sum()) < acc), prop, xs)
            # neighbour swaps labels p+1 .. p+n_nb
            ns = (lab > p) & (lab <= p + M.n_nb)
            if ns.any():
                xs = X[ns]; k = popcount_vec(xs)
                ok = k > 0
                jj = kth_set_bit(xs, (rng.random(ns.sum()) * np.maximum(k, 1)).astype(np.int64), p)
                jj0 = np.maximum(jj, 0)
                cand = Nb[jj0] & ~xs
                nc = popcount_vec(cand)
                ok2 = ok & (nc > 0)
                ll = kth_set_bit(cand, (rng.random(ns.sum()) * np.maximum(nc, 1)).astype(np.int64), p)
                ll0 = np.maximum(ll, 0)
                prop = (xs & ~(1 << jj0)) | (1 << ll0)
                prop = np.where(ok2, prop, xs)
                scored[ns] |= ok2 & (prop == S0)
                rev = popcount_vec(Nb[ll0] & ~prop)
                ratio = np.exp(F[prop] - F[xs]) * nc / np.maximum(rev, 1)
                acc = np.where(ok2, np.minimum(1.0, ratio), 0.0)
                X[ns] = np.where(ok2 & (rng.random(ns.sum()) < acc), prop, xs)
            # independence label m-1
            ind = lab == m - 1
            if ind.any():
                prop = np.searchsorted(cum0, rng.random(ind.sum()), side='right').astype(np.int64)
                prop = np.minimum(prop, full)
                scored[ind] |= prop == S0
                xs = X[ind]
                acc = np.minimum(1.0, np.exp(M.d[prop] - M.d[xs]))
                X[ind] = np.where(rng.random(ind.sum()) < acc, prop, xs)
            if V is not None:
                ch = X != Xold
                inr = inR[X]
                exitr[h] |= ch & ~inr & inR[Xold]
                incr[h] |= ch & inr & inR[Xold] & (V[X] > V[Xold])
        newly = scored & (first < 0)
        first[newly] = h
        if V is not None:
            prog[h] = (V[X] < Vstart) | newly
    return dict(first=first, prog=prog, incr=incr, exit=exitr, final=X)
