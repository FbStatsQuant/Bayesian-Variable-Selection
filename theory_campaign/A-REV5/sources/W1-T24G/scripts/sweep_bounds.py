"""
Exact computation of the sweep-theorem constants (PROOF.md, Theorems S2 and S1) at phi = 1.

Phase 2 (superset family  S_a = {S0 u P : P subset S0^c, |P| <= a}):
  eps2(a) = tau2 + kappa2 + sum_{e in NG} nu_e,
    tau2   = sum_{i in S0}  max_{W in S_a} (1 - o_i(W))
    kappa2 = sum_{l notin S0} max_{W in S_a} o_l(W)
    nu_e   = max_W P_W(e -> outside S_a)  +  1/2 sum_{l'} max_W P_W(e accepted, introduces l')
  eps2out(a) = tau2 + kappa2_out + sum_e max_W P_W(e -> outside S_a)  (first-exit bound),
    kappa2_out = sum_{l notin S0} max_{W in S_a, |P(W)| = a, l notin W} o_l(W).
Phase 1 (truth completion family Z(x,A) = {U u P : x cap S0 subset U subset S0, P subset A}):
  eps1(x,A) = tau1 + lambda1 + sum_e nu1_e,
    tau1    = sum_{i in S0} max_{W in Z} (1 - o_i(W))
    lambda1 = sum_{l notin S0 u A} max_{W in Z} o_l(W)
    nu1_e   = max_{W in Z} P_W(e accepted to W' with W' notin Z or W' cap S0 not superset of W cap S0)
"""
import math
import numpy as np
from bvs_engine import *


def bits_of(x, p):
    return [j for j in range(p) if x >> j & 1]


def gibbs_o(M, W, j):
    """vectorised o_j(W) for an array W."""
    bit = np.int64(1 << j)
    xp = W | bit; xm = W & ~bit
    o = 1.0 / (1.0 + np.exp(M.F[xm] - M.F[xp]))
    o = np.where(M.size[xp] > M.K, 0.0, o)
    return o


def swap_moves(M, W, kind):
    """For array W (all same family), yield (j, l, prob_accepted_move) arrays per (j,l) pair:
    prob = P(label proposes W - j + l and accepts). kind in {'U','N'}."""
    p = M.p
    k = M.size[W].astype(float)
    Nb = np.array(M.Nb, dtype=np.int64)
    out = []
    for j in range(p):
        hasj = (W >> j) & 1 == 1
        if not hasj.any():
            continue
        if kind == 'N':
            cand = Nb[j] & ~W
            nc = popcnt(cand)
        for l in range(p):
            if l == j:
                continue
            okl = hasj & (((W >> l) & 1) == 0)
            if kind == 'N':
                okl = okl & (((Nb[j] >> l) & 1) == 1)
            if not okl.any():
                continue
            dest = (W & ~np.int64(1 << j)) | np.int64(1 << l)
            ratio = np.exp(M.F[dest] - M.F[W])
            if kind == 'U':
                pr = np.where(okl, 1.0 / (k * (p - k)) * np.minimum(1, ratio), 0.0)
            else:
                rev = popcnt(Nb[l] & ~dest)
                pr = np.where(okl, (1.0 / k) * (1.0 / np.maximum(nc, 1)) *
                              np.minimum(1, ratio * nc / np.maximum(rev, 1)), 0.0)
            out.append((j, l, dest, pr))
    return out


def popcnt(a):
    a = np.asarray(a, dtype=np.int64).copy(); c = np.zeros_like(a)
    while a.any():
        c += a & 1; a >>= 1
    return c


class SortedAcc:
    """for a set S of models: f(dx) = sum_{S' in S} pi0(S') min(1, exp(d(S') - dx))."""
    def __init__(self, M, sel):
        dd = M.d[sel]; w = M.pi0[sel]
        o = np.argsort(dd); self.dd = dd[o]; w = w[o]
        self.cw = np.concatenate([[0], np.cumsum(w)])
        with np.errstate(divide='ignore'):
            lw = np.log(w) + self.dd
        self.lc = np.concatenate([[-np.inf], np.logaddexp.accumulate(lw)]) if len(dd) else np.array([-np.inf])
        self.empty = len(dd) == 0

    def __call__(self, dx):
        if self.empty:
            return np.zeros_like(dx)
        i = np.searchsorted(self.dd, dx, side='left')
        return (self.cw[-1] - self.cw[i]) + np.exp(self.lc[i] - dx)


def phase2(M, a):
    p, S0 = M.p, M.S0
    allidx = np.arange(1 << p, dtype=np.int64)
    extra = popcnt(allidx & ~np.int64(S0))
    fam = ((allidx & S0) == S0) & (extra <= a)
    W = allidx[fam]
    s0b = bits_of(S0, p)
    res = {}
    tau = sum(np.max(1 - gibbs_o(M, W, i)) for i in s0b)
    kap = 0.0; kap_out = 0.0
    bd = extra[W] == a
    for l in range(p):
        if l in s0b:
            continue
        o = gibbs_o(M, W, l)
        kap += o.max()
        sel = bd & (((W >> l) & 1) == 0)
        if sel.any():
            kap_out += o[sel].max()
    res.update(tau2=tau, kappa2=kap, kappa2_out=kap_out)
    # swaps
    for kind in ('U', 'N'):
        out_w = np.zeros(len(W)); intro = np.zeros((p, len(W)))
        for j, l, dest, pr in swap_moves(M, W, kind):
            if j in s0b:
                out_w += pr                    # truth removed -> outside S_a
            else:
                intro[l] += pr                 # extra j replaced by null l (same count, stays in S_a)
        res['nu_' + kind] = out_w.max() + 0.5 * intro.max(axis=1).sum()
        res['out_' + kind] = out_w.max()
    # independence
    outside = SortedAcc(M, ~fam)
    dW = M.d[W]
    out_ind = outside(dW)
    intro_max = 0.0
    for l in range(p):
        if l in s0b:
            continue
        has_l = fam & (((allidx >> l) & 1) == 1)
        f = SortedAcc(M, has_l)(dW)
        f = np.where(((W >> l) & 1) == 1, 0.0, f)     # introduces l only if l notin W
        intro_max += f.max()
    res['nu_I'] = out_ind.max() + 0.5 * intro_max
    res['out_I'] = out_ind.max()
    nnb = M.n_nb
    res['eps2'] = tau + kap + res['nu_U'] + nnb * res['nu_N'] + res['nu_I']
    res['eps2out'] = tau + kap_out + res['out_U'] + nnb * res['out_N'] + res['out_I']
    res['famsize'] = int(fam.sum())
    return res


def lookalikes(M, x):
    S0 = M.S0
    miss = bits_of(S0 & ~x, M.p)
    A = x & ~S0
    for j in miss:
        A |= M.Nb[j] & ~S0
    return A


def phase1(M, x, A):
    p, S0 = M.p, M.S0
    s0b = bits_of(S0, p)
    U0 = x & S0
    allidx = np.arange(1 << p, dtype=np.int64)
    fam = ((allidx & U0) == U0) & ((allidx & ~np.int64(S0) & ~np.int64(A)) == 0)
    W = allidx[fam]
    tau = sum(np.max(1 - gibbs_o(M, W, i)) for i in s0b)
    lam = 0.0
    for l in range(p):
        if l in s0b or (A >> l) & 1:
            continue
        lam += gibbs_o(M, W, l).max()
    res = dict(tau1=tau, lambda1=lam)
    for kind in ('U', 'N'):
        fail = np.zeros(len(W))
        for j, l, dest, pr in swap_moves(M, W, kind):
            if j in s0b:
                fail += pr
            elif (l not in s0b) and not ((A >> l) & 1):
                fail += pr
        res['nu1_' + kind] = fail.max()
    # independence: good destinations are S' in Z with S' cap S0 superset of W cap S0
    dW = M.d[W]
    tot = SortedAcc(M, np.ones(1 << p, bool))(dW)
    good = np.zeros(len(W))
    Upat = W & S0
    for u in np.unique(Upat):
        selW = Upat == u
        gset = fam & ((allidx & u) == u)
        good[selW] = SortedAcc(M, gset)(dW[selW])
    res['nu1_I'] = (tot - good - M.pi0[W] * 0).max()   # includes self-proposal? see note
    res['eps1'] = tau + lam + res['nu1_U'] + M.n_nb * res['nu1_N'] + res['nu1_I']
    res['famsize'] = int(fam.sum()); res['A_size'] = bin(A).count('1')
    return res
