#!/usr/bin/env python3
"""W3-VT38E: independent implementation of the method objects needed to referee W1-T38E's CF(c) family and D2.

Written from METHODOLOGY_v3.md / 00_COMMON.md and the engine (Scripts/SMC_BVS/core/cpp), NOT from W1's code.
Objects: standardisation, log m(S) and F(S); complete linkage with the engine's R13 tie rule (pair with the
lexicographically smallest UNION among exactly equal distances), top-down cut, next-fit packing; tables r_b;
pi0 normaliser by size-profile convolution; joint (size, #extras) profile for pi0(R_d); exact pi0 sampler
(total size, then block sizes backwards, then a sub-model within the block's size class); start mode by max-plus
convolution; neighbour graph (M 6.4); local search (M 6.10, engine order); the pilot rule (engine pilot_next_phi);
one random-order round with the four step types (engine step_gibbs / step_uswap / step_nswap / step_indep).

Design CF(c) (from W1 PROOF.md section 8, re-implemented): contrast-orthonormal f_1..f_{c+1}, e_1, ...;
x_1 = f_1, x_j = rho f_1 + sqrt(1-rho^2) f_j (j=2..c+1); each truth gets B-1 copies 0.9 x_j + sqrt(.19) e;
other columns orthonormal nulls; mu = theta1 x_1 + t sum_{j>=2} x_j with t = -theta1 rho/(1+(c-1) rho^2)
so x_j' mu = 0 for j >= 2; p = floor(n^{3/4}); eps ~ N(0, I); y = mu + eps, then standardised.
"""
import itertools, math
import numpy as np
from math import lgamma, log

def lchoose(a, b):
    return lgamma(a + 1) - lgamma(b + 1) - lgamma(a - b + 1)

def lse(a):
    a = np.asarray(a, float)
    if a.size == 0: return -np.inf
    m = np.max(a)
    return -np.inf if m == -np.inf else m + np.log(np.exp(a - m).sum())

# ------------------------------------------------------------------ design
def build_cf(n, c, seed, A=0.75, rho=0.5, theta1=1.0):
    rng = np.random.default_rng(seed)
    p = int(math.floor(n ** A))
    B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
    s0 = c + 1
    G = rng.standard_normal((n, p + 5)); G -= G.mean(0)
    Q, _ = np.linalg.qr(G)
    f = Q[:, :s0]; e = Q[:, s0:]
    xs = [f[:, 0]] + [rho * f[:, 0] + math.sqrt(1 - rho ** 2) * f[:, j] for j in range(1, s0)]
    cols, cl = list(xs), list(range(s0)); k = 0
    for j in range(s0):
        for _ in range(B - 1):
            cols.append(0.9 * xs[j] + math.sqrt(0.19) * e[:, k]); k += 1; cl.append(j)
    while len(cols) < p:
        cols.append(e[:, k]); k += 1; cl.append(-1)
    X = np.array(cols).T
    t = -theta1 * rho / (1 + (c - 1) * rho ** 2)
    beta = np.zeros(p); beta[0] = theta1; beta[1:s0] = t
    mu = math.sqrt(n - 1) * (X @ beta)            # columns below get norm sqrt(n-1)
    y = mu + rng.standard_normal(n)
    return standardise(X, y) + (dict(n=n, p=p, B=B, S0=tuple(range(s0)), cl=np.array(cl), c=c, mu=mu),)

def standardise(Xr, yr):
    n = Xr.shape[0]
    X = Xr / np.abs(Xr).max(0); X = X - X.mean(0); X = X / X.std(0, ddof=1)
    y = yr / np.abs(yr).max(); y = y - y.mean(); y = y / y.std(ddof=1)
    return X, y

# ------------------------------------------------------------------ scores
class Model:
    def __init__(self, X, y, info):
        self.X, self.y, self.info = X, y, info
        self.n, self.p = X.shape
        self.G = X.T @ X; self.z = X.T @ y; self.yy = float(y @ y)
        self.nu = 0.01 + self.n / 2; self.b0 = 0.01
        self.K = min(self.p, self.n // 2)
        self.lw = np.array([log(0.5) - lchoose(2 * self.p - 1, k) for k in range(self.K + 1)])
        self.lWK = lse(np.array([lchoose(self.p, k) for k in range(self.K + 1)]) + self.lw)
        self.lprior = self.lw - self.lWK
        self.cache = {}
        self.lm0 = self._logm_batch(np.zeros((1, 0), int))[0]
    def _logm_batch(self, idx):
        num, k = idx.shape
        if k == 0: return np.full(num, -self.nu * log(2 * self.b0 + self.yy))
        Gs = self.G[idx[:, :, None], idx[:, None, :]]; zs = self.z[idx]
        H = (self.n + 1) * Gs + np.eye(k)
        LH = np.linalg.cholesky(H); LG = np.linalg.cholesky(Gs + np.eye(k))
        ldH = 2 * np.log(np.diagonal(LH, axis1=1, axis2=2)).sum(1)
        ldG = 2 * np.log(np.diagonal(LG, axis1=1, axis2=2)).sum(1)
        v = np.linalg.solve(H, zs[:, :, None])[:, :, 0]
        Q = self.yy - self.n * np.einsum('ij,ij->i', zs, v)
        return -0.5 * (ldH - ldG) - self.nu * np.log(2 * self.b0 + Q)
    def logm(self, S):
        S = tuple(sorted(S))
        v = self.cache.get(S)
        if v is None:
            v = self._logm_batch(np.array(S, int).reshape(1, len(S)))[0]; self.cache[S] = v
        return v
    def logm_many(self, Ss):
        out = np.empty(len(Ss)); todo = {}
        for i, S in enumerate(Ss):
            v = self.cache.get(S)
            if v is None: todo.setdefault(len(S), []).append(i)
            else: out[i] = v
        for k, ii in todo.items():
            idx = np.array([Ss[i] for i in ii], int).reshape(len(ii), k)
            vals = self._logm_batch(idx)
            for i, v in zip(ii, vals): self.cache[Ss[i]] = v; out[i] = v
        return out
    def F(self, S): return self.lprior[len(S)] + self.logm(S)
    def F_many(self, Ss): return np.array([self.lprior[len(S)] for S in Ss]) + self.logm_many(Ss)

# ------------------------------------------------------------------ blocks (engine R13 rule)
def complete_linkage_blocks(X, B):
    p = X.shape[1]
    G = X.T @ X; s = np.sqrt(np.diag(G)); R = G / np.outer(s, s)
    Dm = 1.0 - np.abs(R); np.fill_diagonal(Dm, np.inf)
    mem = {i: (i,) for i in range(p)}; node = {i: i for i in range(p)}
    left, right, minidx, size = {}, {}, {i: i for i in range(p)}, {i: 1 for i in range(p)}
    active = list(range(p)); nxt = p
    D = Dm.copy()
    while len(active) > 1:
        sub = D[np.ix_(active, active)]
        mval = sub.min()
        cand = np.argwhere(sub == mval)
        best = None
        for a, b in cand:
            if a >= b: continue
            i, j = active[a], active[b]
            u = tuple(sorted(mem[i] + mem[j]))
            if best is None or u < best[0]: best = (u, i, j)
        u, i, j = best
        na, nb = node[i], node[j]
        L, Rr = (na, nb) if minidx[na] < minidx[nb] else (nb, na)
        left[nxt], right[nxt] = L, Rr; minidx[nxt] = min(minidx[na], minidx[nb]); size[nxt] = size[na] + size[nb]
        newrow = np.maximum(D[i], D[j]); D[i, :] = newrow; D[:, i] = newrow; D[i, i] = np.inf
        D[j, :] = np.inf; D[:, j] = np.inf
        mem[i] = u; node[i] = nxt; active.remove(j); nxt += 1
    root = nxt - 1
    def leaves(x):
        if x < p: return [x]
        return leaves(left[x]) + leaves(right[x])
    retained = []
    def cut(x):
        if size[x] <= B: retained.append(leaves(x)); return
        cut(left[x]); cut(right[x])
    import sys; sys.setrecursionlimit(10000)
    cut(root)
    blocks, cur = [], []
    for c in retained:
        if len(cur) + len(c) <= B: cur += c
        else: blocks.append(tuple(sorted(cur))); cur = list(c)
    if cur: blocks.append(tuple(sorted(cur)))
    return blocks, R

# ------------------------------------------------------------------ start law
class Start:
    def __init__(self, M, blocks, S0):
        self.M, self.blocks, self.S0 = M, blocks, set(S0)
        self.bof = {j: b for b, C in enumerate(blocks) for j in C}
        self.tab = []          # dict subset -> log r_b
        self.prof = []         # per block: log e_b(j)
        self.byk = []          # per block: list (per size) of (subsets, log r)
        for C in blocks:
            t = {}; byk = []
            for k in range(len(C) + 1):
                subs = list(itertools.combinations(C, k))
                v = M.logm_many(subs) - M.lm0
                for S, val in zip(subs, v): t[S] = val
                byk.append((subs, np.array(v)))
            self.tab.append(t); self.byk.append(byk)
            self.prof.append(np.array([lse(v) for _, v in byk]))
        K = M.K
        # forward convolution of size profiles, E[b][k] = log sum over first b blocks
        E = [np.full(K + 1, -np.inf)]; E[0][0] = 0.0
        for b in range(len(blocks)):
            prev = E[-1]; new = np.full(K + 1, -np.inf); pr = self.prof[b]
            for j in range(len(pr)):
                if j > K: break
                sh = np.full(K + 1, -np.inf); sh[j:] = prev[:K + 1 - j] + pr[j]
                new = np.logaddexp(new, sh)
            E.append(new)
        self.E = E
        self.lsize = E[-1] + M.lprior          # log of unnormalised pi0 size marginal
        self.lZ0 = lse(self.lsize)
    def lg0(self, S):
        v = self.M.lprior[len(S)]
        parts = {}
        for j in S: parts.setdefault(self.bof[j], []).append(j)
        for b, U in parts.items(): v += self.tab[b][tuple(sorted(U))]
        return v
    def lpi0(self, S): return self.lg0(S) - self.lZ0
    def d(self, S): return (self.M.logm(S) - self.M.lm0) - (self.lg0(S) - self.M.lprior[len(S)])
    def mass_by_extras(self, NMAX):
        K = self.M.K
        tot = np.full((K + 1, NMAX + 1), -np.inf); tot[0, 0] = 0.0
        for b, C in enumerate(self.blocks):
            pr = np.full((len(C) + 1, NMAX + 1), -np.inf)
            for S, v in self.tab[b].items():
                ne = min(sum(1 for j in S if j not in self.S0), NMAX)
                pr[len(S), ne] = np.logaddexp(pr[len(S), ne], v)
            new = np.full((K + 1, NMAX + 1), -np.inf)
            for k2 in range(len(C) + 1):
                for e2 in range(NMAX + 1):
                    if pr[k2, e2] == -np.inf: continue
                    for e1 in range(NMAX + 1):
                        ee = min(e1 + e2, NMAX)
                        sh = np.full(K + 1, -np.inf); sh[k2:] = tot[:K + 1 - k2, e1] + pr[k2, e2]
                        new[:, ee] = np.logaddexp(new[:, ee], sh)
            tot = new
        return np.array([math.exp(lse(tot[:, e] + self.M.lprior) - self.lZ0) for e in range(NMAX + 1)])
    def mode(self):
        K = self.M.K
        best = np.full(K + 1, -np.inf); best[0] = 0.0; arg = [()] + [None] * K
        for b, C in enumerate(self.blocks):
            bk = []
            for k, (subs, v) in enumerate(self.byk[b]):
                i = int(np.argmax(v)); bk.append((v[i], subs[i]))
            nb = np.full(K + 1, -np.inf); na = [None] * (K + 1)
            for k1 in range(K + 1):
                if best[k1] == -np.inf: continue
                for k2, (v, S) in enumerate(bk):
                    if k1 + k2 > K: break
                    if best[k1] + v > nb[k1 + k2]: nb[k1 + k2] = best[k1] + v; na[k1 + k2] = tuple(sorted(arg[k1] + S))
            best, arg = nb, na
        tot = best + self.M.lprior; k = int(np.argmax(tot))
        return arg[k], tot[k] - self.lZ0
    def draw(self, rng):
        K = self.M.K
        ps = np.exp(self.lsize - self.lZ0); k = int(rng.choice(K + 1, p=ps / ps.sum()))
        S = []
        for b in range(len(self.blocks) - 1, -1, -1):
            pr = self.prof[b]; prev = self.E[b]
            js = np.arange(min(len(pr) - 1, k) + 1)
            lp = pr[js] + prev[k - js]
            w = np.exp(lp - lse(lp)); j = int(rng.choice(js, p=w / w.sum()))
            if j > 0:
                subs, v = self.byk[b][j]
                ww = np.exp(v - lse(v)); S += list(subs[int(rng.choice(len(subs), p=ww / ww.sum()))])
            k -= j
        return tuple(sorted(S))

# ------------------------------------------------------------------ neighbour graph (M 6.4)
def neighbour_graph(R, n, B):
    p = R.shape[0]; rn = math.sqrt(2 * math.log(p) / n)
    A = np.abs(R.copy()); np.fill_diagonal(A, -1)
    nb = [set() for _ in range(p)]
    for j in range(p):
        order = sorted(range(p), key=lambda l: (-A[j, l], l))
        order = [l for l in order if l != j]
        keep = [l for l in order if A[j, l] > rn]
        if order[0] not in keep: keep = [order[0]] + keep
        keep = sorted(keep, key=lambda l: (-A[j, l], l))[:B]
        for l in keep: nb[j].add(l); nb[l].add(j)
    return [sorted(s) for s in nb]

# ------------------------------------------------------------------ local search (M 6.10, engine order)
def flips_swaps(S, p, K):
    S = tuple(sorted(S)); out = []
    Sset = set(S)
    for j in range(p):
        if j in Sset: out.append(tuple(x for x in S if x != j))
        elif len(S) < K: out.append(tuple(sorted(S + (j,))))
    for j in S:
        for l in range(p):
            if l in Sset: continue
            out.append(tuple(sorted(tuple(x for x in S if x != j) + (l,))))
    return out

def local_search(M, centre, ell):
    C = tuple(sorted(centre)); FC = M.F(C); scored = {C}; path = [C]; moves = 0
    while True:
        nb = flips_swaps(C, M.p, M.K); Fv = M.F_many(nb); scored.update(nb)
        mx = Fv.max(); best = min(nb[i] for i in np.flatnonzero(Fv == mx))
        if mx > FC:
            if moves >= ell: return path, scored, 'move_limit'
            C, FC = best, mx; moves += 1; path.append(C)
        else:
            return path, scored, 'no_improvement'
