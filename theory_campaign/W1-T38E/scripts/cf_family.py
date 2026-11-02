#!/usr/bin/env python3
"""W1-T38E compatibility family CF(c): c cross-block cancelled true variables.

Design (contrast coordinates, every column norm sqrt(n-1)):
  x_1 = f_1 ; x_j = rho f_1 + sqrt(1-rho^2) f_j (j = 2..c+1) ;  S0 = {1..c+1}
  mu = theta1 x_1 + t sum_{j>=2} x_j,  t = -theta1 rho / (1 + (c-1) rho^2)  =>  x_j' mu = 0 exactly (j >= 2)
  each true x_j gets B-1 "copies" 0.9 x_j/|x_j| + sqrt(.19) e  (cluster of size B) ; remaining columns orthonormal nulls.
Method objects computed exactly: blocks (complete linkage on 1-|r|, lexicographic ties, top-down cut, next-fit packing),
tables r_b, pi_0 (size-profile convolution with the capped BB(1,p) prior), pi_0 of S0, of S^(0) = {1}, of R_d,
start mode S~0 (max-plus convolution), TD(d,0) (T37 definition) on R_d, and the production local search from S~0 (LS0).
Also the D2 (pilot one-flip) bound for c = 1.  Fixed seeds.  Usage: python3 cf_family.py n c [dmax]
"""
import sys, itertools, math
import numpy as np
from math import lgamma, log

def lchoose(a, b):
    return lgamma(a + 1) - lgamma(b + 1) - lgamma(a - b + 1)

def build(n, c, A=0.75, rho=0.5, theta1=1.0, sigma=1.0, seed=0):
    rng = np.random.default_rng(seed)
    p = int(math.floor(n ** A))
    B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
    s0 = c + 1
    ncl = s0 * B
    assert p >= ncl + 2, "p too small for the clusters"
    G = rng.standard_normal((n, p)); G -= G.mean(0)
    Qm, _ = np.linalg.qr(G)                  # orthonormal, orthogonal to 1
    f = Qm[:, :s0]; e = Qm[:, s0:]
    X = np.zeros((n, p)); k = 0
    xs = [f[:, 0]] + [rho * f[:, 0] + math.sqrt(1 - rho ** 2) * f[:, j] for j in range(1, s0)]
    order = []
    for j in range(s0):
        X[:, j] = xs[j]
    col = s0
    for j in range(s0):
        for r in range(B - 1):
            X[:, col] = 0.9 * xs[j] + math.sqrt(0.19) * e[:, k]; k += 1; col += 1
    while col < p:
        X[:, col] = e[:, k]; k += 1; col += 1
    X *= math.sqrt(n - 1)
    t = -theta1 * rho / (1 + (c - 1) * rho ** 2)
    beta = np.zeros(p); beta[0] = theta1; beta[1:s0] = t
    mu = X @ beta
    eps = np.random.default_rng(seed + 1000).standard_normal(n) * sigma
    yr = mu + eps
    y = yr - yr.mean(); y = y / math.sqrt((y @ y) / (n - 1))
    # cluster membership (for reporting)
    cl = np.full(p, -1)
    for j in range(s0):
        cl[j] = j; cl[s0 + j * (B - 1): s0 + (j + 1) * (B - 1)] = j
    return dict(n=n, p=p, B=B, s0=s0, X=X, y=y, S0=tuple(range(s0)), beta=beta, mu=mu, cl=cl, c=c)

class Scorer:
    def __init__(s, D):
        s.n = D['n']; s.p = D['p']; X = D['X']; y = D['y']
        s.G = X.T @ X; s.z = X.T @ y; s.yy = y @ y
        s.nu = 0.01 + s.n / 2; s.b0 = 0.01
        s.K = min(s.p, s.n // 2)
        p = s.p
        s.lw = np.array([log(0.5) - lchoose(2 * p - 1, k) for k in range(s.K + 1)])
        s.logWK = np.logaddexp.reduce(np.array([lchoose(p, k) for k in range(s.K + 1)]) + s.lw)
        s.cache = {}
    def logm_batch(s, idx):           # idx: (num, k) int array; returns log m(S) up to the common constant
        num, k = idx.shape
        if k == 0:
            return np.full(num, -s.nu * log(2 * s.b0 + s.yy))
        Gs = s.G[idx[:, :, None], idx[:, None, :]]
        zs = s.z[idx]
        I = np.eye(k)
        H = (s.n + 1) * Gs + I
        _, ldH = np.linalg.slogdet(H); _, ldG = np.linalg.slogdet(Gs + I)
        sol = np.linalg.solve(H, zs[:, :, None])[:, :, 0]
        Q = s.yy - s.n * np.einsum('ij,ij->i', zs, sol)
        return -0.5 * (ldH - ldG) - s.nu * np.log(2 * s.b0 + Q)
    def F(s, S):
        S = tuple(sorted(S))
        if S not in s.cache:
            v = s.logm_batch(np.array([S], dtype=int).reshape(1, len(S)))[0]
            s.cache[S] = s.lw[len(S)] - s.logWK + v
        return s.cache[S]
    def F_many(s, Ss):
        out = np.empty(len(Ss)); todo = {}
        for i, S in enumerate(Ss):
            S = tuple(sorted(S)); Ss[i] = S
            if S in s.cache: out[i] = s.cache[S]
            else: todo.setdefault(len(S), []).append(i)
        for k, ii in todo.items():
            idx = np.array([Ss[i] for i in ii], dtype=int).reshape(len(ii), k)
            v = s.logm_batch(idx)
            for j, i in enumerate(ii):
                s.cache[Ss[i]] = s.lw[k] - s.logWK + v[j]; out[i] = s.cache[Ss[i]]
        return out

def blocks_complete_linkage(X, B):
    p = X.shape[1]
    R = np.corrcoef(X.T); Dm = 1 - np.abs(R)
    clusters = {i: (i,) for i in range(p)}       # id -> sorted tuple
    children = {}
    dist = {}
    ids = list(range(p))
    for a in range(p):
        for b in range(a + 1, p):
            dist[(a, b)] = Dm[a, b]
    nxt = p
    import heapq
    heap = [(Dm[a, b], (a,), (b,), a, b) for a in range(p) for b in range(a + 1, p)]
    heapq.heapify(heap)
    alive = set(range(p))
    cd = {}  # (id1,id2)->dist
    for a in range(p):
        for b in range(a + 1, p): cd[(a, b)] = Dm[a, b]
    while len(alive) > 1:
        while True:
            dd, la, lb, a, b = heapq.heappop(heap)
            if a in alive and b in alive: break
        new = nxt; nxt += 1
        children[new] = (a, b) if min(clusters[a]) < min(clusters[b]) else (b, a)
        clusters[new] = tuple(sorted(clusters[a] + clusters[b]))
        alive.discard(a); alive.discard(b)
        for o in alive:
            dn = max(cd[(min(a, o), max(a, o))], cd[(min(b, o), max(b, o))])
            cd[(min(o, new), max(o, new))] = dn
            lo, hi = (clusters[o], clusters[new]) if clusters[o] < clusters[new] else (clusters[new], clusters[o])
            heapq.heappush(heap, (dn, lo, hi, min(o, new), max(o, new)))
        alive.add(new)
    root = alive.pop()
    # top-down cut, children visited smallest index first; leaf order = DFS order
    retained = []
    def cut(node):
        if len(clusters[node]) <= B: retained.append(clusters[node]); return
        a, b = children[node]; cut(a); cut(b)
    cut(root)
    blocks = []; cur = []
    for cl in retained:                     # next-fit packing of whole clusters
        if len(cur) + len(cl) <= B: cur += list(cl)
        else: blocks.append(tuple(sorted(cur))); cur = list(cl)
    if cur: blocks.append(tuple(sorted(cur)))
    return blocks

def tables(sc, blocks):
    T = []
    lm0 = sc.logm_batch(np.zeros((1, 0), dtype=int))[0]
    for C in blocks:
        tab = {}
        for k in range(len(C) + 1):
            subs = list(itertools.combinations(C, k))
            idx = np.array(subs, dtype=int).reshape(len(subs), k)
            v = sc.logm_batch(idx) - lm0
            for S, val in zip(subs, v): tab[S] = val
        T.append(tab)
    return T

def main():
    n = int(sys.argv[1]); c = int(sys.argv[2]); dmax = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    D = build(n, c); sc = Scorer(D)
    p, B, s0, S0 = D['p'], D['B'], D['s0'], D['S0']
    print(f"== CF(c={c}) n={n} p={p} B={B} s0={s0} K={sc.K}; beta_S0={D['beta'][:s0].round(3)}")
    print("x_j'mu for j in S0 (scaled):", (D['X'][:, :s0].T @ D['mu'] / (n - 1)).round(12))
    blocks = blocks_complete_linkage(D['X'], B)
    bof = {j: b for b, C in enumerate(blocks) for j in C}
    print("blocks of true variables:", [bof[j] for j in S0], " sizes:", sorted(set(len(C) for C in blocks)), " J=", len(blocks))
    print("truth-cluster blocks pure:", all(set(blocks[bof[j]]) == set(np.where(D['cl'] == j)[0]) for j in S0))
    T = tables(sc, blocks)
    nulls = [j for j in range(p) if j not in S0]
    # --- pi_0 via convolution: profiles e_b(k) and two-variable profiles (size, #nulls) ---
    K = sc.K; lw = sc.lw
    def lse(a): 
        a = np.asarray(a); m = np.max(a)
        return -np.inf if m == -np.inf else m + np.log(np.exp(a - m).sum())
    # two-variable profile: dims (size, nulls), cap nulls at NMAX (bucket NMAX = ">= NMAX")
    NMAX = 4
    tot = np.full((K + 1, NMAX + 1), -np.inf); tot[0, 0] = 0.0
    best = np.full(K + 1, -np.inf); best[0] = 0.0; arg = [()] + [None] * K
    for b, C in enumerate(blocks):
        prof = np.full((len(C) + 1, NMAX + 1), -np.inf)
        bestb = {}
        for S, v in T[b].items():
            k = len(S); nn = min(sum(1 for j in S if j not in S0), NMAX)
            prof[k, nn] = np.logaddexp(prof[k, nn], v)
            if k not in bestb or v > bestb[k][0] or (v == bestb[k][0] and S < bestb[k][1]): bestb[k] = (v, S)
        new = np.full((K + 1, NMAX + 1), -np.inf)
        for k1 in range(K + 1):
            for n1 in range(NMAX + 1):
                if tot[k1, n1] == -np.inf: continue
                for k2 in range(len(C) + 1):
                    if k1 + k2 > K: break
                    for n2 in range(NMAX + 1):
                        if prof[k2, n2] == -np.inf: continue
                        nn = min(n1 + n2, NMAX)
                        new[k1 + k2, nn] = np.logaddexp(new[k1 + k2, nn], tot[k1, n1] + prof[k2, n2])
        tot = new
        nb = np.full(K + 1, -np.inf); na = [None] * (K + 1)
        for k1 in range(K + 1):
            if best[k1] == -np.inf: continue
            for k2, (v, S) in bestb.items():
                if k1 + k2 > K: continue
                if best[k1] + v > nb[k1 + k2]: nb[k1 + k2] = best[k1] + v; na[k1 + k2] = tuple(sorted(arg[k1] + S))
        best, arg = nb, na
    logZ0 = lse((tot + lw[:, None]).ravel())
    def lg0(S):
        S = tuple(sorted(S)); v = lw[len(S)]
        for b, C in enumerate(blocks):
            v += T[b][tuple(j for j in S if j in C)]
        return v
    lpi0 = lambda S: lg0(S) - logZ0
    mode_val = best + lw; kstar = int(np.argmax(mode_val)); S0t = arg[kstar]
    mass_by_nulls = [math.exp(lse(tot[:, m] + lw) - logZ0) for m in range(NMAX + 1)]
    Sref = (0,)
    print("pi0(S0)=%.3e  pi0({1})=%.4f  pi0(R_d), d=0..3: %s  start mode S~0=%s (in R_0: %s)" % (
        math.exp(lpi0(S0)), math.exp(lpi0(Sref)),
        [round(sum(mass_by_nulls[:d + 1]), 6) for d in range(4)], tuple(j + 1 for j in S0t), set(S0t) <= set(S0)))
    # budgets (tier 0)
    N0 = max(2500, n, p); ell = math.ceil(math.log2(n + p + 1)); T0 = max(1000, ell ** 2); L = max(4, math.ceil(math.log2(n + 1)))
    Qmin, Qmax = 4 * N0 * (L + 6), 4 * N0 * (T0 + L + 5)
    print("ell=%d L=%d N0=%d: Q_min*pi0(S0)=%.3g  Q_max*pi0(S0)=%.3g  (iid-discovery miss >= exp(-Q_max pi0/(1-pi0)) ~ %.3g)" % (
        ell, L, N0, Qmin * math.exp(lpi0(S0)), Qmax * math.exp(lpi0(S0)), math.exp(-Qmax * math.exp(lpi0(S0)))))
    # --- moves ---
    def moves(S):
        S = tuple(sorted(S)); out = []
        for j in range(p):
            if j in S: out.append(tuple(x for x in S if x != j))
            elif len(S) < K: out.append(tuple(sorted(S + (j,))))
        for j in S:
            for l in range(p):
                if l not in S: out.append(tuple(sorted(tuple(x for x in S if x != j) + (l,))))
        return out
    # --- local search (production rule) from S~0 ---
    def local_search(centre, ell):
        scored = set(); cur = tuple(sorted(centre)); Fc = sc.F(cur); scored.add(cur); path = [cur]
        for mv in range(ell + 1):
            nb = moves(cur); Fv = sc.F_many(nb); scored.update(nb)
            i = int(np.argmax(Fv)); best_nb = nb[i]
            ties = [nb[k] for k in range(len(nb)) if Fv[k] == Fv[i]]; best_nb = min(ties)
            if Fv[i] > Fc and mv < ell: cur, Fc = best_nb, Fv[i]; path.append(cur)
            else: break
        return path, scored
    path, scored = local_search(S0t, ell)
    print("LS0 from S~0: path", [tuple(j + 1 for j in s) for s in path], " S0 scored:", S0 in scored)
    # --- TD(d,0) on R_d ---
    for d in range(dmax + 1):
        worst = np.inf; nstates = 0; fails = 0
        for k in range(s0 + 1):
            for U in itertools.combinations(S0, k):
                for m in range(d + 1):
                    for P in itertools.combinations(nulls, m):
                        S = tuple(sorted(U + P)); nstates += 1
                        nb = moves(S); Fv = sc.F_many(nb) - sc.F(S)
                        if S == S0:
                            marg = -np.max(Fv)
                        elif not set(S0) <= set(S):
                            good = [i for i, x in enumerate(nb) if len(x) == len(S) + 1 and set(x) - set(S) <= set(S0)]
                            gb = max(Fv[i] for i in good); other = max(Fv[i] for i in range(len(nb)) if i not in good or Fv[i] < gb)
                            # margin: best missing-true addition minus best other move
                            oth = np.max(np.delete(Fv, good)) if len(good) < len(nb) else -np.inf
                            marg = gb - oth
                        else:
                            good = [i for i, x in enumerate(nb) if len(x) == len(S) - 1 and set(S) - set(x) <= set(nulls)]
                            gb = max(Fv[i] for i in good)
                            oth = np.max(np.delete(Fv, good))
                            marg = gb - oth
                        worst = min(worst, marg); fails += marg <= 0
        print("TD(%d,0): states=%d  min margin (nats)=%.2f  failures=%d" % (d, nstates, worst, fails))
        # GP(d): greedy progress -- the production best move (max F, lexicographic ties) from every S in R_d \ {S0}
        # strictly improves F, stays in R_d and strictly reduces |S delta S0|; at S0 no strict improvement.
        gp_fail = 0; kinds = {}
        for k in range(s0 + 1):
            for U in itertools.combinations(S0, k):
                for m in range(d + 1):
                    for P in itertools.combinations(nulls, m):
                        S = tuple(sorted(U + P)); nb = moves(S); Fv = sc.F_many(nb); FS = sc.F(S)
                        i = int(np.argmax(Fv)); bnb = min(nb[q] for q in range(len(nb)) if Fv[q] == Fv[i])
                        dist = lambda x: len(set(x) ^ set(S0))
                        if S == S0:
                            ok = Fv[i] <= FS
                        else:
                            inR = len(set(bnb) - set(S0)) <= d
                            ok = Fv[i] > FS and inR and dist(bnb) < dist(S)
                            kind = ("add" if len(bnb) > len(S) else "del" if len(bnb) < len(S) else "swap")
                            kinds[kind] = kinds.get(kind, 0) + 1
                        gp_fail += (not ok)
        print("GP(%d): failures=%d ; best-move types over R_d minus S0: %s" % (d, gp_fail, kinds))
    # --- D2 pilot one-flip bound (meaningful when S0 \\ {1} ... reference x0 = {1} is one flip from S0 iff c = 1) ---
    if c == 1:
        x0 = (0,); j = 1
        Dset = [l for l in range(p) if D['cl'][l] == 1 and l != j]   # copies of the cancelled variable
        dep = 0.0; big = []
        for l in range(p):
            if l == j or l in Dset: continue
            y = tuple(sorted(set(x0) ^ {l}))
            o0 = math.exp(lg0(y) - lg0(x0)); o1 = math.exp(sc.F(y) - sc.F(x0)); dep += max(o0, o1)
            if max(o0, o1) > 1e-2: big.append((l + 1, o0, o1))
        H0 = math.ceil(512 * N0 / 2500)
        f0 = math.exp(lpi0(x0)); g = f0 - math.sqrt(f0 * (1 - f0) / 9)
        beta_lb = max(0.0, 1 - dep) / (len(Dset) + B + 3)
        print("D2: x0={1}, |D|=%d, Dep_rest^max=%.3e, beta_lb=%.4f, pi0(x0)=%.4f, share_lb=%.4f, H0=%d, miss bound exp(-H beta share)=%.3e; large-odds labels outside D: %s" % (
            len(Dset), dep, beta_lb, f0, g, H0, math.exp(-H0 * beta_lb * g), big[:5]))

if __name__ == '__main__':
    main()
