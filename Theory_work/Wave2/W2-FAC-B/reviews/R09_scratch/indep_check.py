# R09 (Claude Opus council seat) independent check: general D0 scorer (no CS closed form),
# explicit exact-Gram X (moderate n) or Gram-level sufficient statistics (large n),
# block-DP start mode, coded local-search loop (flips j asc, swaps j in S asc x l out asc, lex ties, strict).
import numpy as np, math, sys, itertools
from math import lgamma

def logw(k, p):  # w(k) = 1/(2 C(2p-1,k))
    return -math.log(2) - (lgamma(2*p) - lgamma(k+1) - lgamma(2*p-k))

class Scorer:
    def __init__(s, G, z, yy, n):
        s.G, s.z, s.yy, s.n = G, z, yy, n; s.nu = 0.01 + n/2; s.cache = {}
    def logm(s, A):
        A = tuple(sorted(A))
        if A in s.cache: return s.cache[A]
        n = s.n
        if len(A) == 0:
            v = -s.nu*math.log(0.02 + s.yy)
        else:
            idx = np.array(A); GA = s.G[np.ix_(idx, idx)]; zA = s.z[idx]
            H = (n+1)*GA + np.eye(len(A)); Gi = GA + np.eye(len(A))
            L = np.linalg.cholesky(H); w = np.linalg.solve(L, zA)
            ld_H = 2*np.log(np.diag(L)).sum(); ld_G = np.linalg.slogdet(Gi)[1]
            Q = s.yy - n*(w@w)
            v = -0.5*(ld_H - ld_G) - s.nu*math.log(0.02 + Q)
        s.cache[A] = v; return v
    def F(s, A, p): return logw(len(A), p) + s.logm(A)

def make_data(n, p, rho, theta, sigma, rng, explicit):
    Sig = (1-rho)*np.eye(p) + rho*np.ones((p, p))
    if explicit:
        Z = rng.standard_normal((n, p)); Z -= Z.mean(0)
        Q, _ = np.linalg.qr(Z); Lc = np.linalg.cholesky(Sig)
        X = math.sqrt(n-1)*Q@Lc.T
        eps = sigma*rng.standard_normal(n)
        Y = X@theta + eps; Y -= Y.mean()
        G = X.T@X; zY = X.T@Y; YY = Y@Y
    else:
        G = (n-1)*Sig
        g = rng.multivariate_normal(np.zeros(p), Sig)       # X'eps/(sigma sqrt(n-1))
        r = rng.chisquare(n-1-p)
        Xe = sigma*math.sqrt(n-1)*g
        e2 = sigma**2*(g@np.linalg.solve(Sig, g) + r)       # ||C eps||^2
        mu2 = (n-1)*theta@Sig@theta
        zY = G@theta + Xe; YY = mu2 + 2*theta@Xe + e2
    s = math.sqrt(YY/(n-1))
    return G, zY/s, (n-1.0)

def start_mode(sc, p, blocks):
    # gamma0(S) = w(|S|) prod_b r_b(S cap C_b); DP over sizes; return argmax and whether unique (by brute tie count)
    lm0 = sc.logm(())
    best_b = []
    for C in blocks:
        tab = {}
        for k in range(len(C)+1):
            vals = []
            for U in itertools.combinations(C, k):
                vals.append((sc.logm(U) - lm0, U))
            vals.sort(key=lambda t: -t[0])
            tab[k] = vals
        best_b.append(tab)
    # DP: f[k] = (value, list of chosen U)
    f = {0: (0.0, [])}
    for tab in best_b:
        g = {}
        for k0, (v0, ch) in f.items():
            for j, vals in tab.items():
                v = v0 + vals[0][0]; kk = k0 + j
                if kk not in g or v > g[kk][0]: g[kk] = (v, ch + [vals[0][1]])
        f = g
    tot = {k: v + logw(k, p) for k, (v, ch) in f.items()}
    kbest = max(tot, key=lambda k: tot[k])
    S = tuple(sorted(itertools.chain.from_iterable(f[kbest][1])))
    # margin: second best overall = best over (other sizes) or (same size, one block 2nd best)
    ordered = sorted(tot.values(), reverse=True)
    margin_size = ordered[0] - ordered[1] if len(ordered) > 1 else float('inf')
    # within size kbest: replace one block's choice by its 2nd best of same size
    within = float('inf')
    for b, U in enumerate(f[kbest][1]):
        vals = best_b[b][len(U)]
        if len(vals) > 1: within = min(within, vals[0][0] - vals[1][0])
    return S, min(margin_size, within)

def local_search(sc, p, K, centre, cap):
    C = tuple(sorted(centre)); FC = sc.F(C, p); moves = 0; path = [C]; scored = {C}
    while True:
        best = None; bestF = -np.inf
        cand = []
        Cs = set(C)
        for j in range(p):
            if j in Cs: Q = tuple(x for x in C if x != j)
            else:
                if len(C) >= K: continue
                Q = tuple(sorted(C + (j,)))
            cand.append(Q)
        for j in C:
            for l in range(p):
                if l in Cs: continue
                cand.append(tuple(sorted([x for x in C if x != j] + [l])))
        for Q in cand:
            FQ = sc.F(Q, p); scored.add(Q)
            if best is None or FQ > bestF or (FQ == bestF and list(Q) < list(best)): best, bestF = Q, FQ
        if best is not None and bestF > FC:
            if moves >= cap: return dict(path=path, moves=moves, limit=True, returned=best, scored=scored)
            C, FC = best, bestF; moves += 1; path.append(C)
        else:
            return dict(path=path, moves=moves, limit=False, returned=C, scored=scored)

def run(n, p, rho, S0, vt, sigma, seed, explicit, bsize):
    rng = np.random.default_rng(seed)
    theta = np.zeros(p); theta[list(S0)] = vt
    G, z, yy = make_data(n, p, rho, theta, sigma, rng, explicit)
    sc = Scorer(G, z, yy, n)
    blocks = [tuple(range(i, min(i+bsize, p))) for i in range(0, p, bsize)]
    S0s = set(S0)
    N0 = set()
    for C in blocks:
        if S0s <= set(C): N0 |= set(C) - S0s
    Sstar = tuple(sorted(set(range(p)) - N0))
    St, marg = start_mode(sc, p, blocks)
    K = min(p, n//2)
    ell = math.ceil(math.log2(n+p+1))
    res = local_search(sc, p, K, St, ell + len(St))
    # check pure null deletion path
    pure = all(len(res['path'][i+1]) == len(res['path'][i]) - 1 and set(res['path'][i+1]) <= set(res['path'][i])
               and (set(res['path'][i]) - set(res['path'][i+1])).isdisjoint(S0s) for i in range(len(res['path'])-1))
    end = res['returned']; m0 = len(Sstar) - len(S0)
    legacy = local_search(sc, p, K, St, ell)
    return dict(n=n, p=p, rho=rho, start_is_Sstar=(St == Sstar), start_margin=round(marg, 2), moves=res['moves'], m0=m0,
                pure_deletion=pure, ends_S0=(tuple(sorted(end)) == tuple(sorted(S0)) and not res['limit']),
                legacy_scores_S0=(tuple(sorted(S0)) in legacy['scored']), ell=ell)

if __name__ == '__main__':
    out = []
    cfgs = [
        # (n, p, rho, S0, values, explicit, bsize)
        (10**5, 40, 0.5, (3, 17, 30), (1.0, -0.6, 0.8), True, 8),
        (10**5, 40, 0.3, (0, 1, 2), (1.0, 1.0, 1.0), True, 8),      # all truths in block 0 -> N0 = 5 nulls
        (10**8, 48, 0.7, (5, 20, 41), (0.5, -0.5, 0.9), False, 8),
        (10**8, 48, 0.5, (2, 9), (1.0, -2.0), False, 8),           # masked truth: (1-rho)*1 + rho*(-1) = 0
        (10**8, 60, 0.95, (10,), (0.3,), False, 8),
        (10**8, 48, 0.5, (0, 1, 2, 3), (1.0, -1.0, 0.7, 0.4), False, 16),
    ]
    for (n, p, rho, S0, vt, ex, bs) in cfgs:
        for seed in range(2):
            r = run(n, p, rho, S0, np.array(vt), 1.0, 1000+seed, ex, bs); r['seed'] = seed; r['S0'] = S0; r['bsize'] = bs
            print(r, flush=True)
