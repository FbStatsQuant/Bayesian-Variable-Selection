# Copied verbatim from W4-SHARE scripts/bvs_core.py (branch theory/W4-SHARE) for self-containment.
"""W4-SHARE bvs_core: a small-p, exact-score, faithful re-implementation of the SMC-BVS v3 final run.

Written from METHODOLOGY_v3.md §§4-6 (not copied from earlier runs).  p <= 20; states are bitmasks.
- Designs are specified by an exact sample correlation matrix R (so G = (n-1) R), coefficients theta (standardised
  scale) and sigma; the sufficient statistics (X'y, y'y) are drawn from their exact law (requires n - 1 > p), and y is
  standardised (y'y = n - 1).  This allows any n, including n >> p, with exact scores.
- Target (M §5): g = n, tau = 1, IG(0.01, 0.01), BB(1, p) capped at K = min(p, floor(n/2)).
- Blocks (M §6.3): complete linkage on 1 - |r| with lexicographic tie rule, top-down cut at B, next-fit packing in
  leaf order (children visited smallest index first); tables r_b(U) = BF(U); gamma_0, d, Zbar_0 exact by enumeration.
- Neighbour graph (M §6.4).  Round (M §6.5): p Gibbs labels, 1 uniform swap, B neighbour swaps, 1 independence
  proposal, uniformly random order per particle and round; multinomial resampling after every reweighting (M §6.6);
  final island = N iid pi_0 draws, grid stages, L burn-in + 4 measured rounds at phi = 1 (M §6.8).
- Grid: idealised calibration (documented in REPORT): pilot temperatures from the *exact-law* ESS rule
  (largest phi' with ESS fraction of e^{(phi'-phi)d} under q_phi >= 0.9; 60 bisections; floor 1/T_e), candidate set
  V = top-20p by log gamma_0 U top-20p by log gamma_1 U {empty} computed over all of Omega, then the candidate-grid
  construction of M §6.7 with rho_V.  Optionally a particle pilot (H particles, adaptive rule on the population).
"""
import numpy as np
from math import comb, lgamma, log, sqrt, floor

POP16 = np.array([bin(i).count("1") for i in range(1 << 16)], dtype=np.int8)


def popcount(a):
    a = np.asarray(a, dtype=np.int64)
    return (POP16[a & 0xFFFF] + POP16[(a >> 16) & 0xFFFF]).astype(np.int64)


def lse(a, axis=None):
    a = np.asarray(a, dtype=float)
    m = np.max(a, axis=axis, keepdims=True)
    m = np.where(np.isfinite(m), m, 0.0)
    r = m + np.log(np.sum(np.exp(a - m), axis=axis, keepdims=True))
    return np.squeeze(r, axis=axis) if axis is not None else float(r.squeeze())


# ---------------------------------------------------------------- design
def suff_stats(R, theta, sigma, n, rng):
    """Exact law of (z = X'y, y'y) for centred X with X'X = (n-1)R and y = X theta + C eps; returns standardised."""
    p = R.shape[0]
    G = (n - 1) * R
    L = np.linalg.cholesky(G)
    xe = sigma * (L @ rng.standard_normal(p))            # X' eps ~ N(0, sigma^2 G)
    ee = xe @ np.linalg.solve(G, xe) + sigma ** 2 * rng.chisquare(n - 1 - p)   # eps' C eps
    z = G @ theta + xe
    yy = theta @ G @ theta + 2 * theta @ xe + ee
    sy = sqrt(yy / (n - 1))
    return z / sy, yy / sy ** 2   # standardised: y'y = n - 1


class BVS:
    def __init__(self, R, z, yy, n, S0, B=None, Te=1000):
        self.R = np.asarray(R, float); self.p = p = R.shape[0]; self.n = n
        self.z = np.asarray(z, float); self.yy = float(yy)
        self.K = min(p, n // 2)
        self.B = B if B is not None else min(int(floor(sqrt(n))), int(floor(sqrt(p))), 16)
        self.S0 = sum(1 << j for j in S0); self.S0list = sorted(S0)
        self.Te = Te
        self.L = max(4, int(np.ceil(np.log2(n + 1))))
        self.nstates = 1 << p
        self._scores()
        self._blocks()
        self._start()
        self._neighbours()

    # exact log BF for every state (vectorised by size)
    def _logm_rel(self, masks):
        n, a0, b0 = self.n, 0.01, 0.01
        nu = a0 + n / 2
        out = np.empty(len(masks))
        sizes = popcount(masks)
        base = -nu * np.log(2 * b0 + self.yy)
        for k in np.unique(sizes):
            sel = np.where(sizes == k)[0]
            if k == 0:
                out[sel] = base; continue
            idx = np.array([[j for j in range(self.p) if (m >> j) & 1] for m in masks[sel]])
            Gs = (n - 1) * self.R[idx[:, :, None], idx[:, None, :]]
            zs = self.z[idx]
            I = np.eye(k)
            H = (n + 1) * Gs + I
            ldH = np.linalg.slogdet(H)[1]; ldG = np.linalg.slogdet(Gs + I)[1]
            sol = np.linalg.solve(H, zs[:, :, None])[:, :, 0]
            Q = self.yy - n * np.sum(zs * sol, axis=1)
            out[sel] = -0.5 * (ldH - ldG) - nu * np.log(2 * b0 + Q)
        return out - base   # log BF

    def _scores(self):
        p = self.p
        masks = np.arange(self.nstates, dtype=np.int64)
        self.size = popcount(masks)
        self.logBF = self._logm_rel(masks)
        lw = np.array([log(0.5) - (lgamma(2 * p) - lgamma(k + 1) - lgamma(2 * p - k)) for k in range(p + 1)])
        WK = lse([log(comb(p, k)) + lw[k] for k in range(self.K + 1)])
        self.logprior = np.where(self.size <= self.K, lw[np.minimum(self.size, p)] - WK, -np.inf)
        self.lg1 = self.logprior + self.logBF
        self.logZbar1 = lse(self.lg1)
        self.post = np.exp(self.lg1 - self.logZbar1)

    def _blocks(self):
        p, B = self.p, self.B
        D = 1 - np.abs(self.R)
        clusters = {i: [i] for i in range(p)}; children = {}; nid = p
        active = list(range(p))
        while len(active) > 1:
            best = None
            for ia in range(len(active)):
                for ib in range(ia + 1, len(active)):
                    a, b = active[ia], active[ib]
                    dist = max(D[i, j] for i in clusters[a] for j in clusters[b])
                    key = (dist, sorted(clusters[a]) if min(clusters[a]) < min(clusters[b]) else sorted(clusters[b]),
                           sorted(clusters[b]) if min(clusters[a]) < min(clusters[b]) else sorted(clusters[a]))
                    if best is None or key < best[0]:
                        best = (key, a, b)
            _, a, b = best
            clusters[nid] = sorted(clusters[a] + clusters[b]); children[nid] = (a, b)
            active = [x for x in active if x not in (a, b)] + [nid]; nid += 1
        root = active[0]
        retained = []

        def visit(node):
            if len(clusters[node]) <= B:
                retained.append(clusters[node]); return
            a, b = children[node]
            first, second = (a, b) if min(clusters[a]) < min(clusters[b]) else (b, a)
            visit(first); visit(second)
        visit(root)
        blocks, cur = [], []
        for c in retained:
            if len(cur) + len(c) <= B:
                cur = cur + c
            else:
                blocks.append(cur); cur = list(c)
        if cur: blocks.append(cur)
        self.blocks = [sorted(b) for b in blocks]
        self.blockmask = [sum(1 << j for j in b) for b in self.blocks]

    def _start(self):
        masks = np.arange(self.nstates, dtype=np.int64)
        logtab = np.zeros(self.nstates)
        for bm in self.blockmask:
            logtab += self.logBF[masks & bm]   # r_b(S cap C_b) = BF(S cap C_b)
        self.logtab = logtab
        self.lg0 = self.logprior + logtab
        self.d = np.where(np.isfinite(self.lg0), self.logBF - logtab, 0.0)
        self.logZbar0 = lse(self.lg0)
        self.pi0 = np.exp(self.lg0 - self.logZbar0)
        self.cum0 = np.cumsum(self.pi0); self.cum0[-1] = 1.0
        self.start_mode = int(np.argmax(self.lg0))

    def _neighbours(self):
        p, n, B = self.p, self.n, self.B
        rn = sqrt(2 * log(p) / n) if p > 1 else np.inf
        Nb = [set() for _ in range(p)]
        A = np.abs(self.R)
        for j in range(p):
            others = [l for l in range(p) if l != j]
            if not others: continue
            order = sorted(others, key=lambda l: (-A[j, l], l))
            part = [l for l in order if A[j, l] > rn]
            if order[0] not in part: part = [order[0]] + part
            part = sorted(part, key=lambda l: (-A[j, l], l))[:B]
            for l in part:
                Nb[j].add(l); Nb[l].add(j)
        self.nbmask = np.array([sum(1 << l for l in Nb[j]) for j in range(p)], dtype=np.int64)

    # ------------------------------------------------------------ bridge laws
    def logq(self, phi):
        lg = self.lg0 + phi * self.d
        return lg - lse(lg)

    def F(self, t, V=None):
        lg = self.lg0 + t * self.d
        return lse(lg if V is None else lg[V])

    def rho(self, u, v, V=None):
        return np.exp(2 * self.F(v, V) - self.F(u, V) - self.F(2 * v - u, V))

    def pilot_exact(self, thr=0.9):
        phis = [0.0]; phi = 0.0; forced = 0
        while phi < 1.0:
            if self.rho(phi, 1.0) >= thr:
                nxt = 1.0
            else:
                lo, hi = phi, 1.0
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    if self.rho(phi, mid) >= thr: lo = mid
                    else: hi = mid
                nxt = lo
                if nxt < phi + 1.0 / self.Te:
                    nxt = min(1.0, phi + 1.0 / self.Te); forced += 1
            phis.append(nxt); phi = nxt
        return np.array(phis), forced

    def candidate_V(self):
        top = 20 * self.p
        fin = np.where(np.isfinite(self.lg0))[0]
        V0 = fin[np.lexsort((fin, -self.lg0[fin]))][:top]
        V1 = fin[np.lexsort((fin, -self.lg1[fin]))][:top]
        return np.unique(np.r_[V0, V1, 0])

    def candidate_grid(self, pilot, V, thr=0.9):
        grid = [0.0]; u = 0.0
        for b in pilot[1:]:
            while u < b:
                if self.rho(u, b, V) >= thr:
                    grid.append(b); u = b
                else:
                    lo, hi = u, b
                    for _ in range(60):
                        mid = 0.5 * (lo + hi)
                        if self.rho(u, mid, V) >= thr: lo = mid
                        else: hi = mid
                    if lo <= u: raise RuntimeError("grid construction: non-progress")
                    grid.append(lo); u = lo
                if len(grid) - 1 > self.Te: raise RuntimeError("grid construction: > Te intervals")
        return np.array(grid)

    def method_grid(self):
        pil, forced = self.pilot_exact()
        V = self.candidate_V()
        return self.candidate_grid(pil, V), pil, forced

    # ------------------------------------------------------------ particle system
    def draw_pi0(self, size, rng):
        return np.searchsorted(self.cum0, rng.random(size), side="left").astype(np.int64)

    def _rand_bit(self, masks, rng):
        """uniform random set bit of each mask (masks > 0 assumed)."""
        keys = rng.random((len(masks), self.p))
        bits = ((masks[:, None] >> np.arange(self.p)) & 1).astype(bool)
        keys[~bits] = -1.0
        return np.argmax(keys, axis=1)

    def one_round(self, S, phi, rng, rec):
        """One round for every particle in S (int64 array), in place semantics returned."""
        p, B = self.p, self.B
        N = len(S); m = p + B + 2
        order = np.argsort(rng.random((N, m)), axis=1)   # uniform random permutation per particle
        lg = self.lg0 + phi * self.d
        allmask = (1 << p) - 1
        for pos in range(m):
            lab = order[:, pos]
            # Gibbs
            gi = np.where(lab < p)[0]
            if len(gi):
                j = lab[gi]; s = S[gi]; bit = (np.int64(1) << j)
                inn = (s & bit) != 0
                s_add = s | bit; s_del = s & ~bit
                other = np.where(inn, s_del, s_add)
                feas = inn | (self.size[s] < self.K)
                rec(other[feas], "gibbs")
                a = lg[s_add] - lg[s_del]
                o = np.where(feas | inn, 1 / (1 + np.exp(-np.clip(a, -700, 700))), 0.0)
                o = np.where(self.size[s_del] >= self.K, 0.0, o)
                inc = rng.random(len(gi)) < o
                S[gi] = np.where(inc, s_add, s_del)
            # uniform swap
            ui = np.where(lab == p)[0]
            if len(ui):
                s = S[ui]; k = self.size[s]
                ok = (k > 0) & (k < p)
                ui, s = ui[ok], s[ok]
                if len(ui):
                    j = self._rand_bit(s, rng); l = self._rand_bit(allmask & ~s, rng)
                    sp = (s & ~(np.int64(1) << j)) | (np.int64(1) << l)
                    rec(sp, "uswap")
                    acc = np.log(rng.random(len(ui))) < (lg[sp] - lg[s])
                    S[ui] = np.where(acc, sp, s)
            # neighbour swaps
            ni = np.where((lab > p) & (lab <= p + B))[0]
            if len(ni):
                s = S[ni]; ok = s > 0
                ni, s = ni[ok], s[ok]
                if len(ni):
                    j = self._rand_bit(s, rng)
                    cand = self.nbmask[j] & ~s
                    ok2 = cand > 0
                    ni, s, j, cand = ni[ok2], s[ok2], j[ok2], cand[ok2]
                    if len(ni):
                        l = self._rand_bit(cand, rng)
                        sp = (s & ~(np.int64(1) << j)) | (np.int64(1) << l)
                        back = popcount(self.nbmask[l] & ~sp)
                        rec(sp, "nswap")
                        la = lg[sp] - lg[s] + np.log(popcount(cand)) - np.log(back)
                        acc = np.log(rng.random(len(ni))) < la
                        S[ni] = np.where(acc, sp, s)
            # independence proposal
            ii = np.where(lab == p + B + 1)[0]
            if len(ii):
                s = S[ii]; sp = self.draw_pi0(len(ii), rng)
                rec(sp, "indep")
                acc = np.log(rng.random(len(ii))) < phi * (self.d[sp] - self.d[s])
                S[ii] = np.where(acc, sp, s)
        return S

    def island(self, N, grid, rng, sets=None, n_term=None, track_S0=True):
        """Final-run island.  sets: dict name -> boolean array over states (counted after every stage).
        Returns dict with counts per stage, realised r_t and P_t for each set (h = indicator), log Zhat/Z,
        first stage/mechanism at which S0 was scored."""
        sets = sets or {}
        n_term = self.L + 4 if n_term is None else n_term
        S = self.draw_pi0(N, rng)
        info = {"first_S0": None}
        stage = [0]

        def rec(states, mech):
            if info["first_S0"] is None and track_S0 and np.any(states == self.S0):
                info["first_S0"] = (stage[0], mech)
        rec(S, "init")
        counts = {k: [int(v[S].sum())] for k, v in sets.items()}
        logr = {k: [] for k in sets}
        logZ = self.logZbar0
        for t in range(1, len(grid)):
            stage[0] = t
            dphi = grid[t] - grid[t - 1]
            lw = dphi * self.d[S]
            L = lse(lw)
            logZ += L - np.log(N)
            for k, v in sets.items():
                inW = v[S]
                if inW.any():
                    logGW = lse(lw[inW]) - np.log(inW.sum())
                    logr[k].append(logGW - (L - np.log(N)))
                else:
                    logr[k].append(0.0)
            w = np.exp(lw - L)
            anc = np.searchsorted(np.cumsum(w), rng.random(N) * np.sum(w), side="left")
            anc = np.minimum(anc, N - 1)
            S = S[anc].copy()
            rec(S, "held")
            S = self.one_round(S, grid[t], rng, rec)
            rec(S, "held")
            for k, v in sets.items():
                counts[k].append(int(v[S].sum()))
        stage[0] = len(grid)  # terminal rounds
        for h in range(n_term):
            S = self.one_round(S, 1.0, rng, rec)
            rec(S, "held")
        info["final_counts"] = {k: int(v[S].sum()) for k, v in sets.items()}
        info["counts"] = {k: np.array(c) for k, c in counts.items()}
        info["logr"] = {k: np.array(c) for k, c in logr.items()}
        info["logZhat_over_Z"] = logZ - self.logZbar1
        info["final_states"] = S
        return info

    # ------------------------------------------------------------ helpers
    def extras(self, masks=None):
        masks = np.arange(self.nstates) if masks is None else masks
        return popcount(masks & ~self.S0)

    def missing(self, masks=None):
        masks = np.arange(self.nstates) if masks is None else masks
        return popcount(self.S0 & ~masks)

    def R_d(self, d):
        return (self.extras() <= d) & np.isfinite(self.lg0)

    def fmt(self, m):
        return "{" + ",".join(str(j) for j in range(self.p) if (m >> j) & 1) + "}"
