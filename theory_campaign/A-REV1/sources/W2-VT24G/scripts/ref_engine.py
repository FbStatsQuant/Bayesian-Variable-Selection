"""
W2-VT24G independent reference engine (written from METHODOLOGY_v3 §§5, 6.3-6.5 and the production C++
Scripts/SMC_BVS/core/cpp/v3_engine.h / v3_blocks.h; it does NOT import or copy W1-T24G's bvs_engine.py).

Exact enumeration of all 2^p models (p <= 20) at phi = 1:
  F(S) = log varpi(|S|) + log m(S)   (target, up to log Z)
  log gamma_0(S) = log varpi(|S|) + sum_b log r_b(S n C_b),  r_b(U) = m(U)/m(empty)
  d(S) = log BF(S) - sum_b log r_b(S n C_b)
Blocks: explicit complete linkage on 1-|r| (left child = child with smaller min index), DFS top-down cut at B,
next-fit packing in left-to-right leaf order (as v3_blocks.h).  Neighbour graph as v3_blocks.h.
Round simulation: vectorised over replicate particles; uniform permutation of the m = p+B+2 labels per particle.

Bitmask convention: S <-> sum_{j in S} 2^j.
"""
import math
import numpy as np
from scipy.special import gammaln

A0 = B0 = 0.01


def scenario_cov(scen, p):
    g = np.ceil(np.arange(1, p + 1) / 5.0)
    H = (g[:, None] == g[None, :]).astype(float)
    I = np.eye(p)
    idx = np.arange(1, p + 1)
    if scen == 1:
        return I
    if scen == 2:
        return 0.5 ** np.abs(idx[:, None] - idx[None, :])
    if scen == 3:
        return 0.7 * H + 0.3 * I
    if scen == 4:
        return 0.85 * H + 0.15 * I
    if scen == 5:
        return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    if scen == 6:
        rho = 0.4 + 0.1 * ((g - 1) % 6)
        S = H * rho[None, :]   # R: H * matrix(rho, p, p) fills column-wise -> entry (i,j) gets rho[j]; symmetric on H
        np.fill_diagonal(S, 1.0)
        return S
    raise ValueError(scen)


def truth(p):
    """gen_dev_data.R::truth pattern with step 1 (one truth per group of 5), s0 = p/5."""
    s0 = p // 5
    pos = [3, 2, 4, 1, 5, 3]
    pat = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    act = [5 * k + pos[k % 6] - 1 for k in range(s0)]
    beta = [pat[k % 6] for k in range(s0)]
    return np.array(act), np.array(beta)


def make_data(scen, c, p=20, n=200, seed=1):
    """Same draw convention as W1-T24G (numpy default_rng(seed): X then eps) so their numbers can be checked
    on the same datasets; other seeds give fresh replicates."""
    rng = np.random.default_rng(seed)
    U = np.linalg.cholesky(scenario_cov(scen, p)).T
    Xr = rng.standard_normal((n, p)) @ U
    eps = rng.standard_normal(n)
    # method preprocessing (M §4): divide by max abs, centre, divide by sd (ddof 1)
    X = Xr / np.abs(Xr).max(0)
    X = X - X.mean(0)
    X = X / X.std(0, ddof=1)
    act, beta = truth(p)
    b = np.zeros(p); b[act] = beta
    # generator: X0 = scale(raw); y = c * X0 b + eps.  X (method) equals X0 exactly up to rounding.
    X0 = (Xr - Xr.mean(0)) / Xr.std(0, ddof=1)
    yr = c * (X0 @ b) + eps
    yc = yr - yr.mean()
    y = yc / math.sqrt(yc @ yc / (n - 1))
    S0 = int(sum(1 << int(j) for j in act))
    return X, y, S0


def popcounts(N):
    a = np.arange(N, dtype=np.int64)
    c = np.zeros(N, dtype=np.int16)
    for _ in range(64):
        if not a.any():
            break
        c += (a & 1).astype(np.int16)
        a >>= 1
    return c


def all_logm(X, y):
    """log m(S) - log m(empty) for every S (Cholesky of H_S and of G_S + I; batched by size)."""
    n, p = X.shape
    G = X.T @ X; z = X.T @ y; yy = float(y @ y); nu = A0 + n / 2.0
    N = 1 << p
    sizes = popcounts(N)
    out = np.empty(N)
    lm0 = -nu * math.log(2 * B0 + yy)
    out[0] = 0.0
    bitsel = np.arange(p)
    for k in range(1, p + 1):
        masks = np.nonzero(sizes == k)[0]
        for s in range(0, len(masks), 50000):
            mm = masks[s:s + 50000]
            bits = ((mm[:, None] >> bitsel[None, :]) & 1).astype(bool)
            idx = np.nonzero(bits)[1].reshape(len(mm), k)
            Gs = G[idx[:, :, None], idx[:, None, :]]
            Hs = (n + 1) * Gs + np.eye(k)
            LH = np.linalg.cholesky(Hs)
            LG = np.linalg.cholesky(Gs + np.eye(k))
            ldH = 2 * np.log(np.diagonal(LH, axis1=1, axis2=2)).sum(1)
            ldG = 2 * np.log(np.diagonal(LG, axis1=1, axis2=2)).sum(1)
            w = np.linalg.solve(LH, z[idx][:, :, None])[:, :, 0]      # L^{-1} z
            Q = yy - n * (w * w).sum(1)
            out[mm] = -0.5 * (ldH - ldG) - nu * np.log(2 * B0 + Q) - lm0
    return out, sizes


def log_varpi(p, K):
    k = np.arange(p + 1)
    lw = -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
    lC = gammaln(p + 1) - gammaln(k + 1) - gammaln(p - k + 1)
    lWK = np.logaddexp.reduce((lC + lw)[k <= K])
    lw = lw - lWK
    lw[k > K] = -np.inf
    return lw


def complete_linkage_blocks(X, B):
    n, p = X.shape
    G = X.T @ X
    s = np.sqrt(np.diag(G))
    R = G / np.outer(s, s)
    dist = 1 - np.abs(R)
    mem = {j: [j] for j in range(p)}      # active cluster id -> members
    node = {j: j for j in range(p)}       # active cluster id -> tree node
    left, right, minidx, size = {}, {}, {j: j for j in range(p)}, {j: 1 for j in range(p)}
    D = {(a, b): dist[a, b] for a in range(p) for b in range(p) if a != b}
    nxt = p
    active = set(range(p))
    while len(active) > 1:
        best = None
        for a in active:
            for b in active:
                if a < b:
                    key = (D[(a, b)], sorted(mem[a] + mem[b]))
                    if best is None or key < best[0]:
                        best = (key, a, b)
        _, a, b = best
        na, nb = node[a], node[b]
        L, Rr = (na, nb) if minidx[na] < minidx[nb] else (nb, na)
        left[nxt], right[nxt] = L, Rr
        minidx[nxt] = min(minidx[na], minidx[nb]); size[nxt] = size[na] + size[nb]
        mem[a] = sorted(mem[a] + mem[b]); del mem[b]; active.remove(b); node[a] = nxt
        for x in active:
            if x != a:
                v = max(D[(x, a)], D[(x, b)])
                D[(x, a)] = D[(a, x)] = v
        nxt += 1
    root = nxt - 1

    def leaves(nd):
        if nd < p:
            return [nd]
        return leaves(left[nd]) + leaves(right[nd])

    clusters, st = [], [root]
    while st:
        x = st.pop()
        if size[x] <= B:
            clusters.append(leaves(x)); continue
        st.append(right[x]); st.append(left[x])
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) > B:
            blocks.append(sorted(cur)); cur = []
        cur += c
    if cur:
        blocks.append(sorted(cur))
    return blocks, R


def neighbour_graph(R, n, B):
    p = R.shape[0]
    rn = math.sqrt(2 * math.log(p) / n)
    chosen = []
    for j in range(p):
        cand = sorted([l for l in range(p) if l != j], key=lambda l: (-abs(R[j, l]), l))
        keep = [l for l in cand if abs(R[j, l]) > rn][:B]
        if not keep:
            keep = [cand[0]]
        if cand[0] not in keep:
            keep = [cand[0]] + keep[:B - 1]
        chosen.append(keep)
    N = [set() for _ in range(p)]
    for j in range(p):
        for l in chosen[j]:
            N[j].add(l); N[l].add(j)
    return [sorted(s) for s in N]


class Model:
    def __init__(self, X, y, S0):
        self.X, self.y, self.S0 = X, y, S0
        n, p = X.shape
        self.n, self.p = n, p
        self.K = min(p, n // 2)
        self.B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
        self.m = p + self.B + 2
        self.L = max(4, math.ceil(math.log2(n + 1)))
        self.logbf, self.sizes = all_logm(X, y)
        lv = log_varpi(p, self.K)
        self.F = lv[self.sizes] + self.logbf                    # log gamma_1 up to a constant
        self.blocks, self.R = complete_linkage_blocks(X, self.B)
        self.Nb = neighbour_graph(self.R, n, self.B)
        self.nbmask = np.array([sum(1 << l for l in self.Nb[j]) for j in range(p)], dtype=np.int64)
        N = 1 << p
        ar = np.arange(N, dtype=np.int64)
        comp = np.zeros(N)
        for bl in self.blocks:
            # table: log r_b(U) for every U subset of the block, from logbf of the sub-model
            sub = np.zeros(N, dtype=np.int64)
            for t, j in enumerate(bl):
                sub |= ((ar >> j) & 1) << j
            comp += self.logbf[sub]
        self.lg0 = lv[self.sizes] + comp
        self.d = self.logbf - comp
        lse = np.logaddexp.reduce(self.F)
        self.post = np.exp(self.F - lse)
        l0 = np.logaddexp.reduce(self.lg0)
        self.pi0 = np.exp(self.lg0 - l0)
        self.cdf0 = np.cumsum(self.pi0); self.cdf0 /= self.cdf0[-1]
        self.lse = lse

    # ------------------------------------------------------------- vectorised round at phi = 1
    def kth_bit(self, S, k):
        """index of the k-th (0-based) set bit of S (vectorised)."""
        out = np.full(S.shape, -1, dtype=np.int64)
        cnt = np.zeros(S.shape, dtype=np.int64)
        for b in range(self.p):
            bit = (S >> b) & 1
            hit = (bit == 1) & (cnt == k) & (out < 0)
            out[hit] = b
            cnt += bit
        return out

    def popc(self, S):
        return self.sizes[S].astype(np.int64)

    def round(self, S, rng, target=None, region=None):
        """One round of the m labels for every particle in S (int64 array, modified in place).
        Returns (S, scored, exited): scored[i] = particle i's round evaluated `target` (SR: both Gibbs
        configurations, every swap / independence proposal); exited[i] = some elementary state of the round
        lies outside `region` (boolean array over masks)."""
        p, B, m = self.p, self.B, self.m
        R = len(S)
        scored = np.zeros(R, dtype=bool); exited = np.zeros(R, dtype=bool)
        if target is not None:
            scored |= S == target
        order = np.argsort(rng.random((R, m)), axis=1)   # uniform permutation per particle
        for t in range(m):
            lab = order[:, t]
            k = self.popc(S)
            # Gibbs
            g = lab < p
            if g.any():
                j = lab[g]
                Sg = S[g]
                with_ = Sg | (np.int64(1) << j)
                without = Sg & ~(np.int64(1) << j)
                feas = self.sizes[with_] <= self.K
                lw = np.where(feas, self.F[with_], -np.inf)
                lo = self.F[without]
                o = 1.0 / (1.0 + np.exp(lo - lw))
                inc = rng.random(len(j)) < o
                S[g] = np.where(inc, with_, without)
                if target is not None:
                    scored[g] |= ((with_ == target) & feas) | (without == target)
            # uniform swap
            u = lab == p
            if u.any():
                Su = S[u]; ku = k[u]
                ok = (ku > 0) & (ku < p)
                jj = self.kth_bit(Su, np.floor(rng.random(len(Su)) * np.maximum(ku, 1)).astype(np.int64))
                comp = (~Su) & ((np.int64(1) << p) - 1)
                ll = self.kth_bit(comp, np.floor(rng.random(len(Su)) * np.maximum(p - ku, 1)).astype(np.int64))
                Sp = np.where(ok, (Su & ~(np.int64(1) << np.maximum(jj, 0))) | (np.int64(1) << np.maximum(ll, 0)), Su)
                acc = ok & (np.log(rng.random(len(Su))) < self.F[Sp] - self.F[Su])
                S[u] = np.where(acc, Sp, Su)
                if target is not None:
                    scored[u] |= ok & (Sp == target)
            # neighbour swaps
            nb = (lab > p) & (lab <= p + B)
            if nb.any():
                Sn = S[nb]; kn = k[nb]
                ok = kn > 0
                jj = self.kth_bit(Sn, np.floor(rng.random(len(Sn)) * np.maximum(kn, 1)).astype(np.int64))
                jj0 = np.maximum(jj, 0)
                cand = self.nbmask[jj0] & ~Sn
                nc = self.popc(cand)
                ok &= nc > 0
                ll = self.kth_bit(cand, np.floor(rng.random(len(Sn)) * np.maximum(nc, 1)).astype(np.int64))
                ll0 = np.maximum(ll, 0)
                Sp = (Sn & ~(np.int64(1) << jj0)) | (np.int64(1) << ll0)
                back = self.popc(self.nbmask[ll0] & ~Sp)
                la = self.F[Sp] - self.F[Sn] + np.log(np.maximum(nc, 1)) - np.log(np.maximum(back, 1))
                acc = ok & (np.log(rng.random(len(Sn))) < la)
                S[nb] = np.where(acc, Sp, Sn)
                if target is not None:
                    scored[nb] |= ok & (Sp == target)
            # independence
            iv = lab == p + B + 1
            if iv.any():
                Si = S[iv]
                Sp = np.searchsorted(self.cdf0, rng.random(len(Si)), side='right').astype(np.int64)
                Sp = np.minimum(Sp, (1 << p) - 1)
                acc = np.log(rng.random(len(Si))) < self.d[Sp] - self.d[Si]
                S[iv] = np.where(acc, Sp, Si)
                if target is not None:
                    scored[iv] |= Sp == target
            if region is not None:
                exited |= ~region[S]
        return S, scored, exited


def mask_to_list(S):
    return [j for j in range(64) if (S >> j) & 1]
