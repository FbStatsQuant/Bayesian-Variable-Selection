#!/usr/bin/env python3
"""W5-LOCKBOOK: independent reproduction of W2-T26's p = 18 premise scan at three sizes (n = 160, 2560, 40960).

Independent of W2-T26's bvs_exact.py except for the DATA GENERATOR, which is copied verbatim from W2-T26
scripts/premise_scan.py (function `design` and the seed rule default_rng(1000*design_index + seed + 7919*n)) so that
the same data sets are scored. Everything else is re-implemented from 00_COMMON / METHODOLOGY_v3 / the engine:
  * log BF(S) for all 2^18 models by batched Cholesky (W2-T26 used slogdet + solve);
  * the block partition by my own complete linkage with the engine's R13 rules (cpp/v3_blocks.h: lexicographic merge
    ties, left child = smaller minimum index, left-first leaf order, top-down cut, next-fit packing);
    W2-T26 used scipy's linkage/to_tree, whose left/right convention is not R13's;
  * the neighbour graph per cpp/v3_blocks.h:149-173;
  * pi_0, pi, d; Delta via Lemma 1 and on a 201-point phi grid; the exact one-round departure
    rho_bar = 1 - prod_e (1 - K_e(S0, Omega minus S0)) computed from explicit per-label kernels, and the sum bound;
  * the full-space-ESS "ideal" grid (proxy for T) by bisection.
Output: results/premise_indep.csv and a comparison with W2-T26's CSVs (results/premise_compare.txt) if the W2-T26
CSVs are given as arguments.  Deterministic given the data seeds.
"""
import sys, os, csv, math, itertools
import numpy as np

P = 18
A0 = B0 = 0.01

# ---------------- data generator: verbatim from W2-T26 scripts/premise_scan.py ----------------
def design(name, n, rng):
    if name == 'fav_iid':
        X = rng.standard_normal((n, P))
        beta = np.zeros(P); S0 = [0, 6, 12]; beta[S0] = 0.6
    else:
        rho = 0.5
        Zg = rng.standard_normal((n, 6))
        E = rng.standard_normal((n, P))
        X = np.empty((n, P))
        for j in range(P):
            X[:, j] = np.sqrt(rho) * Zg[:, j // 3] + np.sqrt(1 - rho) * E[:, j]
        beta = np.zeros(P)
        if name == 'fav_cor':
            S0 = [0, 6, 12]; beta[S0] = 0.6
        else:  # masked
            X[:, 3] = 0.6 * X[:, 0] + np.sqrt(1 - 0.36) * X[:, 3]
            S0 = [0, 3, 12]; beta[0] = 1.0; beta[3] = -0.6; beta[12] = 0.6
    y = X @ beta + rng.standard_normal(n)
    return X, y, S0
# ------------------------------------------------------------------------------------------------

def lse(v):
    m = np.max(v)
    return m + np.log(np.sum(np.exp(v - m)))

class Exact:
    def __init__(self, Xr, yr, S0):
        n, p = Xr.shape
        X = Xr - Xr.mean(axis=0); X = X / np.sqrt((X ** 2).sum(axis=0) / (n - 1))
        y = yr - yr.mean(); y = y / np.sqrt((y ** 2).sum() / (n - 1))
        self.n, self.p = n, p
        self.K = min(p, n // 2)
        self.B = min(math.isqrt(n), math.isqrt(p), 16)
        self.L = max(4, math.ceil(math.log2(n + 1)))
        self.ell = math.ceil(math.log2(n + p + 1))
        self.Tmax = 4 * max(1000, self.ell ** 2)
        G = X.T @ X; z = X.T @ y; yy = float(y @ y); nu = A0 + n / 2
        N = 1 << p
        size = np.array([bin(s).count('1') for s in range(N)])
        self.size = size
        logm = np.full(N, -np.inf)
        logm[0] = -nu * math.log(2 * B0 + yy)
        for k in range(1, min(p, self.K) + 1):
            idx = np.array(list(itertools.combinations(range(p), k)))
            masks = (np.left_shift(1, idx)).sum(axis=1)
            Gs = G[idx[:, :, None], idx[:, None, :]]
            H = (n + 1) * Gs + np.eye(k)
            A = Gs + np.eye(k)
            LH = np.linalg.cholesky(H); LA = np.linalg.cholesky(A)
            ldH = 2 * np.log(np.diagonal(LH, axis1=1, axis2=2)).sum(axis=1)
            ldA = 2 * np.log(np.diagonal(LA, axis1=1, axis2=2)).sum(axis=1)
            zs = z[idx]
            # z' H^{-1} z = || LH^{-1} z ||^2
            w = np.linalg.solve(LH, zs[:, :, None])[:, :, 0]
            Q = yy - n * (w ** 2).sum(axis=1)
            logm[masks] = -0.5 * (ldH - ldA) - nu * np.log(2 * B0 + Q)
        self.logBF = logm - logm[0]
        feas = size <= self.K
        lw = np.array([math.log(0.5) - (math.lgamma(2 * p) - math.lgamma(k + 1) - math.lgamma(2 * p - k)) for k in range(p + 1)])
        self.logw = np.where(feas, lw[size], -np.inf)
        R = G / np.sqrt(np.outer(np.diag(G), np.diag(G)))
        self.R = R
        self.blocks = self.make_blocks(R, self.B)
        self.nbr = self.neighbours(R, self.B, n)
        comp = np.zeros(N)
        for b in self.blocks:
            M = sum(1 << j for j in b)
            comp += self.logBF[np.arange(N) & M]
        self.lg0 = np.where(feas, self.logw + comp, -np.inf)
        self.d = np.where(feas, self.logBF - comp, 0.0)
        self.lg1 = np.where(feas, self.logw + self.logBF, -np.inf)
        self.pi0 = np.exp(self.lg0 - lse(self.lg0)); self.pi = np.exp(self.lg1 - lse(self.lg1))
        self.S0 = sum(1 << j for j in S0); self.s0 = len(S0)
        self.feas = feas

    @staticmethod
    def make_blocks(R, B):
        p = R.shape[0]
        dist = 1 - np.abs(R)
        mem = {j: [j] for j in range(p)}
        node = {j: ('leaf', j) for j in range(p)}
        D = {(i, j): dist[i, j] for i in range(p) for j in range(p) if i != j}
        active = set(range(p))
        while len(active) > 1:
            best = None
            for i in active:
                for j in active:
                    if i >= j: continue
                    key = (D[(i, j)], sorted(mem[i] + mem[j]))
                    if best is None or key < best[0]:
                        best = (key, i, j)
            _, a, b = best
            na, nb = node[a], node[b]
            L, Rr = (na, nb) if min(mem[a]) < min(mem[b]) else (nb, na)
            for x in active:
                if x in (a, b): continue
                v = max(D[(x, a)], D[(x, b)])
                D[(x, a)] = D[(a, x)] = v
            mem[a] = sorted(mem[a] + mem[b]); del mem[b]; active.discard(b)
            node[a] = ('node', L, Rr, len(mem[a]))
        root = node[next(iter(active))]
        def leaves(t):
            return [t[1]] if t[0] == 'leaf' else leaves(t[1]) + leaves(t[2])
        def sz(t):
            return 1 if t[0] == 'leaf' else t[3]
        clusters = []
        def cut(t):
            if sz(t) <= B: clusters.append(leaves(t)); return
            cut(t[1]); cut(t[2])
        cut(root)
        blocks, cur = [], []
        for c in clusters:
            if len(cur) + len(c) > B:
                blocks.append(cur); cur = []
            cur = cur + c
        if cur: blocks.append(cur)
        return [sorted(b) for b in blocks]

    @staticmethod
    def neighbours(R, B, n):
        p = R.shape[0]
        rn = math.sqrt(2 * math.log(p) / n)
        N = [set() for _ in range(p)]
        for j in range(p):
            cand = sorted([l for l in range(p) if l != j], key=lambda l: (-abs(R[j, l]), l))
            above = 0
            for l in cand:
                if abs(R[j, l]) > rn: above += 1
                else: break
            keep = min(B, max(1, above))
            for l in cand[:keep]:
                N[j].add(l); N[l].add(j)
        return N

    def q(self, phi, S):
        v = self.lg0 + phi * self.d
        return math.exp(v[S] - lse(v))

    def kernels_at_S0(self):
        """K_e(S0, Omega minus S0) for each of the m = p + B + 2 labels at phi = 1."""
        S0, p, lg = self.S0, self.p, self.lg1
        ks = []
        for j in range(p):                         # Gibbs j (heat bath between S0 and S0 xor j)
            Sj = S0 ^ (1 << j)
            if not self.feas[Sj]: ks.append(0.0); continue
            ks.append(1.0 / (1.0 + math.exp(min(lg[S0] - lg[Sj], 700))))
        ins = [j for j in range(p) if S0 >> j & 1]; outs = [l for l in range(p) if not S0 >> l & 1]
        k = len(ins)
        us = 0.0                                   # uniform swap
        if 0 < k < p:
            for i in ins:
                for l in outs:
                    Sp = S0 ^ (1 << i) ^ (1 << l)
                    us += min(1.0, math.exp(lg[Sp] - lg[S0])) / (k * (p - k))
        ks.append(us)
        ns = 0.0                                   # neighbour swap (one label; B copies)
        if k > 0:
            for j in ins:
                cand = sorted(l for l in self.nbr[j] if not S0 >> l & 1)
                for l in cand:
                    Sp = S0 ^ (1 << j) ^ (1 << l)
                    back = sum(1 for x in self.nbr[l] if not Sp >> x & 1)
                    ns += (1.0 / k) * (1.0 / len(cand)) * min(1.0, math.exp(lg[Sp] - lg[S0]) * len(cand) / back)
        ks += [ns] * self.B
        acc = self.pi0 * np.minimum(1.0, np.exp(np.where(self.feas, self.d - self.d[S0], -np.inf)))
        ks.append(float(acc.sum() - acc[S0]))     # independence proposal
        return ks

    def ideal_T(self, thr=0.9):
        def lz(phi): return lse(self.lg0 + phi * self.d)
        u, T = 0.0, 0
        while u < 1.0:
            ok = lambda v: 2 * lz(v) - lz(u) - lz(2 * v - u) >= math.log(thr)
            if ok(1.0): v = 1.0
            else:
                lo, hi = u, 1.0
                for _ in range(60):
                    mid = (lo + hi) / 2
                    if ok(mid): lo = mid
                    else: hi = mid
                v = lo
                if v <= u: return -1
            u = v; T += 1
            if T > 100000: return -1
        return T

def run(ns=(160, 2560, 40960)):
    rows = []
    for di, name in enumerate(['fav_iid', 'fav_cor', 'masked']):
        for n in ns:
            seeds = range(8) if n <= 5120 else range(6)
            for seed in seeds:
                rng = np.random.default_rng(1000 * di + seed + 7919 * n)
                X, y, S0 = design(name, n, rng)
                E = Exact(X, y, S0)
                p0, p1 = E.pi0[E.S0], E.pi[E.S0]
                Delta = max(1 - p0, 1 - p1)
                grid_min = min(E.q(f, E.S0) for f in np.linspace(0, 1, 201))
                ks = E.kernels_at_S0()
                rho_bar = 1 - float(np.prod([1 - k for k in ks]))
                u_pi = (1 - p1) / p1
                T = E.ideal_T()
                rows.append(dict(design=name, n=n, seed=seed, blocks='|'.join(','.join(map(str, b)) for b in E.blocks),
                                 one_minus_pi0=1 - p0, delta1=1 - p1, Delta=Delta, Delta_grid=1 - grid_min,
                                 u_pi=u_pi, rho_bar=rho_bar, rho_bar_sum=sum(ks), rho_star=min(1.0, (E.B + 3) * u_pi),
                                 T_ideal=T, P1_Tideal=(T + 1) * Delta, P1_Tmax=(E.Tmax + 1) * Delta,
                                 S0_is_HPM=int(np.argmax(E.lg1) == E.S0)))
                r = rows[-1]
                print(name, n, seed, "1-pi0=%.3e d1=%.3e Dgrid-D=%.1e rhobar=%.3e sum=%.3e T=%d" %
                      (r['one_minus_pi0'], r['delta1'], r['Delta_grid'] - r['Delta'], r['rho_bar'], r['rho_bar_sum'], T), flush=True)
    return rows

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    res = os.path.join(here, '..', 'results')
    rows = run()
    with open(os.path.join(res, 'premise_indep.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    if len(sys.argv) > 1:
        theirs = {}
        for path in sys.argv[1:]:
            with open(path) as fh:
                for r in csv.DictReader(fh):
                    theirs[(r['design'], int(r['n']), int(r['seed']))] = r
        out = []
        same_blocks = 0; tot = 0; maxrel = {}
        for r in rows:
            t = theirs.get((r['design'], r['n'], r['seed']))
            if t is None: continue
            tot += 1
            sb = t['blocks'] == r['blocks']; same_blocks += sb
            for key, tk in [('one_minus_pi0', 'one_minus_pi0'), ('delta1', 'delta1'), ('Delta', 'Delta'), ('rho_bar_sum', 'rho_bar_bound'), ('T_ideal', 'T_ideal')]:
                a, b = float(r[key]), float(t[tk])
                rel = abs(a - b) / max(abs(b), 1e-300)
                kk = (key, sb)
                maxrel[kk] = max(maxrel.get(kk, 0), rel)
            out.append("%s n=%d seed=%d same_blocks=%s  1-pi0 mine %.6e theirs %.6e | delta1 %.6e %.6e | rhobar_sum %.6e %.6e | T %s %s" %
                       (r['design'], r['n'], r['seed'], sb, r['one_minus_pi0'], float(t['one_minus_pi0']), r['delta1'], float(t['delta1']),
                        r['rho_bar_sum'], float(t['rho_bar_bound']), r['T_ideal'], t['T_ideal']))
        out.append(f"rows compared: {tot}; identical partitions: {same_blocks}")
        for k, v in sorted(maxrel.items()):
            out.append(f"max relative difference {k[0]} (same partition = {k[1]}): {v:.3e}")
        with open(os.path.join(res, 'premise_compare.txt'), 'w') as fh:
            fh.write('\n'.join(out) + '\n')
        print('\n'.join(out[-12:]))
