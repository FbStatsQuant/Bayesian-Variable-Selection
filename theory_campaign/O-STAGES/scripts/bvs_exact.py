"""Exact enumeration of the SMC-BVS v3 target, start law and bridge at small p.

Implements, from Docs/Theory/theorems/00_COMMON.md and Docs/Methodology/METHODOLOGY_v3.md:
  standardisation; log m(S) (up to the constant c_n, which cancels); BB(1,p) size prior capped at K;
  the method's block partition (complete linkage on 1-|r|, top-down cut at B, next-fit packing in leaf order);
  tables r_b = BF; gamma_0, d, bridge q_phi; the neighbour graph; the elementary kernels at phi = 1 evaluated
  at S0 (for the departure bound of Lemma 2).
All models are bitmasks over p <= 20 columns.
Deviations (documented): merge ties in complete linkage are broken by scipy, not lexicographically
(irrelevant for continuous random designs).
"""
import numpy as np
from itertools import combinations
from math import lgamma, log, comb, floor, sqrt, ceil
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform
from scipy.special import logsumexp

A0 = B0 = 0.01


def standardise(Xr, yr):
    n = Xr.shape[0]
    Xc = Xr - Xr.mean(0)
    X = Xc / Xc.std(0, ddof=1)
    yc = yr - yr.mean()
    y = yc / yc.std(ddof=1)
    return X, y


def popcount(a):
    a = a.astype(np.int64)
    c = np.zeros_like(a)
    while np.any(a):
        c += a & 1
        a >>= 1
    return c


def all_log_m(X, y):
    """log m(S) - log c_n for every bitmask S (|S| <= K), -inf for infeasible."""
    n, p = X.shape
    K = min(p, n // 2)
    G = X.T @ X
    z = X.T @ y
    yy = float(y @ y)
    nu = A0 + n / 2
    out = np.full(1 << p, -np.inf)
    out[0] = -nu * log(2 * B0 + yy)
    for k in range(1, K + 1):
        idx = np.array(list(combinations(range(p), k)), dtype=np.int64)
        masks = (1 << idx).sum(1)
        Gs = G[idx[:, :, None], idx[:, None, :]]
        zs = z[idx]
        I = np.eye(k)
        H = (n + 1) * Gs + I
        _, ldH = np.linalg.slogdet(H)
        _, ldG = np.linalg.slogdet(Gs + I)
        sol = np.linalg.solve(H, zs[:, :, None])[:, :, 0]
        Q = yy - n * np.einsum('ij,ij->i', zs, sol)
        out[masks] = -0.5 * (ldH - ldG) - nu * np.log(2 * B0 + Q)
    return out


def log_prior_size(p, K):
    """log w(k), k = 0..p (uncapped weights; cap applied through feasibility)."""
    return np.array([log(0.5) - (lgamma(2 * p) - lgamma(k + 1) - lgamma(2 * p - k)) for k in range(p + 1)])


def method_blocks(X, B):
    """Complete linkage on 1-|r|, top-down cut at B, next-fit packing in leaf order."""
    p = X.shape[1]
    if p == 1:
        return [[0]]
    R = np.corrcoef(X, rowvar=False)
    D = 1 - np.abs(R)
    np.fill_diagonal(D, 0)
    D = np.clip((D + D.T) / 2, 0, None)
    Z = linkage(squareform(D, checks=False), method='complete')
    root = to_tree(Z)

    def leaves(node):
        return node.pre_order()

    clusters = []

    def cut(node):
        lv = leaves(node)
        if len(lv) <= B:
            clusters.append(lv)
            return
        kids = [node.get_left(), node.get_right()]
        kids.sort(key=lambda c: min(leaves(c)))  # visit smallest index first
        for c in kids:
            cut(c)

    cut(root)
    # leaf order of the dendrogram
    order = root.pre_order()
    pos = {j: i for i, j in enumerate(order)}
    clusters.sort(key=lambda c: min(pos[j] for j in c))
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) <= B:
            cur = cur + c
        else:
            blocks.append(cur)
            cur = list(c)
    if cur:
        blocks.append(cur)
    return [sorted(b) for b in blocks]


def neighbour_graph(X, B):
    n, p = X.shape
    if p == 1:
        return [set()]
    R = np.corrcoef(X, rowvar=False)
    rn = sqrt(2 * log(p) / n)
    nb = [set() for _ in range(p)]
    for j in range(p):
        a = np.abs(R[j]).copy()
        a[j] = -1
        order = sorted(range(p), key=lambda l: (-a[l], l))
        part = [l for l in order if l != j and a[l] > rn]
        if order[0] not in part:
            part = [order[0]] + part
        part = sorted(part, key=lambda l: (-a[l], l))[:B]
        nb[j] |= set(part)
    sym = [set() for _ in range(p)]
    for j in range(p):
        for l in nb[j]:
            sym[j].add(l)
            sym[l].add(j)
    return sym


class Problem:
    def __init__(self, Xr, yr, S0):
        X, y = standardise(Xr, yr)
        self.X, self.y = X, y
        n, p = X.shape
        self.n, self.p = n, p
        self.K = min(p, n // 2)
        self.B = min(floor(sqrt(n)), floor(sqrt(p)), 16)
        self.L = max(4, ceil(log(n + 1, 2)))
        self.ell = ceil(log(n + p + 1, 2))
        self.T0 = max(1000, self.ell ** 2)
        self.Tmax = 4 * self.T0
        self.masks = np.arange(1 << p, dtype=np.int64)
        self.size = popcount(self.masks)
        self.feas = self.size <= self.K
        lm = all_log_m(X, y)
        self.logBF = lm - lm[0]
        lw = log_prior_size(p, self.K)
        self.logw = np.where(self.feas, lw[np.minimum(self.size, p)], -np.inf)
        self.blocks = method_blocks(X, self.B)
        self.bmask = [int(sum(1 << j for j in b)) for b in self.blocks]
        sum_logr = np.zeros(1 << p)
        for M in self.bmask:
            sum_logr += self.logBF[self.masks & M]
        self.lg0 = np.where(self.feas, self.logw + sum_logr, -np.inf)
        self.d = np.where(self.feas, self.logBF - sum_logr, 0.0)
        self.lg1 = np.where(self.feas, self.logw + self.logBF, -np.inf)
        self.S0 = int(sum(1 << j for j in S0))
        self.s0 = len(S0)
        self.nbr = neighbour_graph(X, self.B)
        self.pi0 = np.exp(self.lg0 - logsumexp(self.lg0))
        self.pi = np.exp(self.lg1 - logsumexp(self.lg1))

    def logZbar(self, phi):
        return logsumexp(self.lg0 + phi * self.d)

    def q(self, phi, S):
        return float(np.exp(self.lg0[S] + phi * self.d[S] - self.logZbar(phi)))

    # ---- premise quantities ----
    def premise(self, phis=None):
        S0 = self.S0
        out = {}
        if not self.feas[S0]:
            return dict(feasible=False)
        p0 = self.pi0[S0]
        p1 = self.pi[S0]
        out['one_minus_pi0'] = 1 - p0
        out['delta1'] = 1 - p1
        out['u_pi'] = (1 - p1) / p1
        out['rho_star'] = min(1.0, (self.B + 3) * out['u_pi'])
        if phis is None:
            phis = np.linspace(0, 1, 201)
        qs = np.array([self.q(f, S0) for f in phis])
        out['Delta_grid'] = 1 - qs.min()
        out['Delta'] = max(1 - p0, 1 - p1)  # Lemma 1
        out['rho_bar_bound'] = self.departure_sum()
        out['rho_bar'] = self.rho_bar_exact
        return out

    def departure_sum(self):
        """Sum over the m = p+B+2 elementary kernels at phi=1 of K_e(S0, Omega minus S0) (Lemma 2 middle term)."""
        S0, p, K = self.S0, self.p, self.K
        lg = self.lg1
        tot = 0.0
        logstay = 0.0  # log prod_e (1 - k_e): exact rho_bar = 1 - exp(logstay)
        # Gibbs: heat bath on coordinate j
        for j in range(p):
            Sj = S0 ^ (1 << j)
            if not self.feas[Sj]:
                continue
            a, b = lg[S0], lg[Sj]
            ke = 1.0 / (1.0 + np.exp(min(a - b, 700.0)))  # prob of moving to Sj
            tot += ke; logstay += np.log1p(-min(ke, 1 - 1e-300))
        k = self.s0
        ins = [j for j in range(p) if S0 >> j & 1]
        outs = [j for j in range(p) if not S0 >> j & 1]
        # uniform swap
        if 0 < k < p:
            s = 0.0
            for i in ins:
                for l in outs:
                    Sp = S0 ^ (1 << i) ^ (1 << l)
                    s += min(1.0, np.exp(lg[Sp] - lg[S0]))
            ke = s / (k * (p - k)); tot += ke; logstay += np.log1p(-min(ke, 1 - 1e-300))
        # neighbour swap (B copies)
        if k > 0:
            s = 0.0
            for j in ins:
                cand = [l for l in self.nbr[j] if not S0 >> l & 1]
                if not cand:
                    continue
                for l in cand:
                    Sp = S0 ^ (1 << j) ^ (1 << l)
                    rev = [jj for jj in self.nbr[l] if not Sp >> jj & 1]
                    hast = len(cand) / len(rev)
                    s += (1.0 / len(cand)) * min(1.0, np.exp(lg[Sp] - lg[S0]) * hast)
            ke = s / k; tot += self.B * ke; logstay += self.B * np.log1p(-min(ke, 1 - 1e-300))
        # independence proposal from pi0, accept 1 ^ exp(d(S') - d(S0))
        mv = self.pi0 * np.minimum(1.0, np.exp(np.where(self.feas, self.d - self.d[S0], -np.inf)))
        ke = float(mv.sum() - mv[S0]); tot += ke; logstay += np.log1p(-min(ke, 1 - 1e-300))
        self.rho_bar_exact = float(-np.expm1(logstay))
        return tot

    def ideal_grid(self, thr=0.9, halvings=60):
        """Full-space ESS grid: from u, the largest v with Zbar_v^2/(Zbar_u Zbar_{2v-u}) >= thr (bisection).
        A proxy for the method's T (the method uses the pilot plus the restricted candidate-set ESS)."""
        grid = [0.0]
        u = 0.0
        while u < 1.0:
            def ok(v):
                return 2 * self.logZbar(v) - self.logZbar(u) - self.logZbar(2 * v - u) >= log(thr)
            if ok(1.0):
                v = 1.0
            else:
                lo, hi = u, 1.0
                for _ in range(halvings):
                    mid = (lo + hi) / 2
                    if ok(mid):
                        lo = mid
                    else:
                        hi = mid
                v = lo
                if v <= u:
                    return None
            grid.append(v)
            u = v
            if len(grid) > 100000:
                return None
        return grid
