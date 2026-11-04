#!/usr/bin/env python3
# Seat A, Round 2 local check. Exact-Gram family, p=16, four groups of 4, within rho, cross eps.
# Method partition: complete linkage on 1-|r|, size cut B=min(floor(sqrt n), floor(sqrt p), 16)=4, next-fit packing.
# Computes, over ALL 2^16 models (K=min(p,n/2)=16): d, d_sigma (WS3), eta_S (WS4), eta_Omega;
# checks |d-d_sigma|<=eta_S, the transfer ratio at v in {phi_1, .25, .5, 1} vs exp(4 v eta),
# the corrected stage-count sandwich T_sig(.9e^{-4eta}) <= T(.9) <= T_sig(.9e^{4eta}) (full-space greedy, 60 halvings, no pilot targets),
# and the fixed-eps growth of sup|d-d_sigma| in n (necessity scale).
import numpy as np, math, sys, time
from scipy.special import logsumexp, betaln
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

p, g = 16, 4
groups = [list(range(4*b, 4*b+4)) for b in range(4)]

def make(n, rho, eps, seed, beta_idx=(0, 8), beta=(0.8, 0.6), sigma=1.0):
    rng = np.random.default_rng(seed)
    Sig = np.full((p, p), eps)
    for G in groups:
        for i in G:
            for j in G:
                Sig[i, j] = rho if i != j else 1.0
    L = np.linalg.cholesky(Sig)
    A = rng.normal(size=(n, p)); A -= A.mean(0)
    U, _ = np.linalg.qr(A)                      # orthonormal centred columns
    X = math.sqrt(n-1) * U @ L.T                # X'X = (n-1) Sig exactly
    y = sum(b * X[:, j] for j, b in zip(beta_idx, beta)) + sigma * rng.normal(size=n)
    y -= y.mean(); y /= y.std(ddof=1)
    return X, y, Sig

def partition(X, n):
    r = np.corrcoef(X.T); D = 1 - np.abs(r); np.fill_diagonal(D, 0)
    B = min(int(math.sqrt(n)), int(math.sqrt(p)), 16)
    Z = linkage(squareform(D, checks=False), method='complete')
    # size cut: smallest number of clusters with all sizes <= B
    for k in range(1, p+1):
        lab = fcluster(Z, k, criterion='maxclust')
        sizes = np.bincount(lab)[1:]
        if sizes.max() <= B: break
    clusters = [sorted(np.where(lab == c)[0].tolist()) for c in range(1, lab.max()+1)]
    clusters.sort(key=lambda c: c[0])
    # next-fit packing
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) <= B: cur += c
        else: blocks.append(cur); cur = list(c)
    if cur: blocks.append(cur)
    return B, [sorted(b) for b in blocks]

def all_models(X, y, n, blocks):
    a0 = b0 = 0.01; nu = a0 + n/2; Qbar = 2*b0 + y @ y
    G = X.T @ X; z = X.T @ y
    M = 1 << p
    masks = np.arange(M)
    size = np.array([bin(m).count('1') for m in range(M)])
    logBF = np.zeros(M); xS = np.zeros(M); eps_S = np.zeros(M); F_S = np.zeros(M)
    blk_of = np.zeros(p, int)
    for b, Bk in enumerate(blocks):
        for j in Bk: blk_of[j] = b
    for k in range(1, p+1):
        idx = masks[size == k]
        cols = np.array([[j for j in range(p) if (m >> j) & 1] for m in idx])   # (m,k)
        Gs = G[cols[:, :, None], cols[:, None, :]]                               # (m,k,k)
        zs = z[cols]
        Hs = (n+1)*Gs + np.eye(k)
        t = n * np.einsum('mi,mi->m', zs, np.linalg.solve(Hs, zs[..., None])[..., 0])
        D = np.linalg.slogdet(Hs)[1] - np.linalg.slogdet(Gs + np.eye(k))[1]
        x = t / Qbar
        logBF[idx] = -0.5*D - nu*np.log1p(-x); xS[idx] = x
        if k >= 2:
            R = Gs/(n-1)
            same = (blk_of[cols][:, :, None] == blk_of[cols][:, None, :])
            A = np.where(same, R, 0.0); E = R - A
            w, V = np.linalg.eigh(A)
            Ah = V @ (V.transpose(0, 2, 1) / np.sqrt(w)[:, :, None])   # A^{-1/2}
            Mx = Ah @ E @ Ah
            ev = np.linalg.eigvalsh(Mx)
            eps_S[idx] = np.abs(ev).max(1); F_S[idx] = (ev**2).sum(1)
    # block parts
    lr_sum = np.zeros(M); xbar = np.zeros(M); dsig = np.zeros(M)
    for Bk in blocks:
        mb = sum(1 << j for j in Bk)
        sub = masks & mb
        lr_sum += logBF[sub]; xbar += xS[sub]; dsig -= -nu*np.log1p(-xS[sub])  # accumulate sum_b log(1-x_b) * (-nu)... fix below
    # d_sigma = -nu[log(1 - xbar) - sum_b log(1 - x_b)]
    sum_log1mxb = np.zeros(M)
    for Bk in blocks:
        mb = sum(1 << j for j in Bk); sum_log1mxb += np.log1p(-xS[masks & mb])
    dsig = -nu*(np.log1p(-xbar) - sum_log1mxb)
    d = logBF - lr_sum
    ok = (eps_S < 1 - xbar)
    eta_S = np.where(ok, nu*eps_S*xbar/(1 - eps_S - xbar) + F_S/(4*(1-eps_S)), np.inf)
    # prior BB(1,p), no cap (K=p)
    lprior = betaln(1 + size, p + p - size) - betaln(1, p)
    lg0 = lprior + lr_sum
    return dict(d=d, dsig=dsig, eta_S=eta_S, lg0=lg0, xbar=xbar, nu=nu, size=size, eps_S=eps_S)

def Lam(lg0, dd, phi): return logsumexp(lg0 + phi*dd) - logsumexp(lg0)
def log1chi(lg0, dd, u, v): return Lam(lg0, dd, 2*v-u) - 2*Lam(lg0, dd, v) + Lam(lg0, dd, u)
def greedy(lg0, dd, thr):
    u, T, pts = 0.0, 0, []
    while u < 1:
        if math.exp(-log1chi(lg0, dd, u, 1.0)) >= thr: return T+1, pts+[1.0]
        lo, hi = u, 1.0
        for _ in range(60):
            mid = (lo+hi)/2
            if math.exp(-log1chi(lg0, dd, u, mid)) >= thr: lo = mid
            else: hi = mid
        u = lo; T += 1; pts.append(u)
    return T, pts

t0 = time.time()
print("A) IC3 exhibit p=16, n=64, rho=0.5, groups of 4; method partition; all 65536 models")
print("eps seed | blocks=groups SIZE | eta_Om  max|d-ds| perS_ok | phi1 ratio1 bnd1 | v=.5 ratio bnd | v=1 ratio bnd | T(.9) Tsig(.9e^-4eta) Tsig(.9e^4eta) order_ok")
viol = 0
for eps in (1e-4, 1e-3, 1e-2):
    for seed in (0, 1, 2):
        n = 64
        X, y, Sig = make(n, 0.5, eps, seed)
        B, blocks = partition(X, n)
        bg = (sorted(map(sorted, blocks)) == groups); SIZE = (max(map(len, blocks)) <= B < 2*min(map(len, blocks)))
        R = all_models(X, y, n, blocks)
        d, ds, etaS, lg0 = R['d'], R['dsig'], R['eta_S'], R['lg0']
        eta = etaS.max(); dev = np.abs(d-ds)
        perS = bool((dev <= etaS + 1e-9).all())
        T, pts = greedy(lg0, d, 0.9); phi1 = pts[0]
        out = []
        for v in (phi1, 0.5, 1.0):
            ratio = math.exp(log1chi(lg0, d, 0, v) - log1chi(lg0, ds, 0, v)); bnd = math.exp(4*v*eta)
            out += [ratio, bnd]
            if not (1/bnd - 1e-9 <= ratio <= bnd + 1e-9): viol += 1
        if 0.9*math.exp(4*eta) < 1:
            Tlo, _ = greedy(lg0, ds, 0.9*math.exp(-4*eta)); Thi, _ = greedy(lg0, ds, 0.9*math.exp(4*eta))
            order = (Tlo <= T <= Thi)
        else:
            Tlo = Thi = -1; order = None
        print(f"{eps:.0e} {seed} | {bg} {SIZE} | {eta:7.3f} {dev.max():7.3f} {perS} | {phi1:.3f} {out[0]:.3f} {out[1]:.3f} | {out[2]:.3f} {out[3]:.3f} | {out[4]:.3f} {out[5]:.3f} | {T} {Tlo} {Thi} {order}")
print("transfer violations:", viol)

print("\nB) necessity scale: fixed eps=0.05, rho=0.5, seed 0; sup|d-d_sigma| vs n, with |d_fit(S0)| and the 2x2 prediction nu*2*eps*c1*c2/(1-xbar)")
print("n   nu    sup|d-ds|  |d(S0)-ds(S0)|  pred  eta_Om")
for n in (32, 64, 128, 256):
    X, y, Sig = make(n, 0.5, 0.05, 0)
    B, blocks = partition(X, n)
    R = all_models(X, y, n, blocks)
    d, ds, etaS, nu = R['d'], R['dsig'], R['eta_S'], R['nu']
    S0 = (1 << 0) | (1 << 8)
    c = (X.T @ y)/(n-1); pred = nu*2*0.05*abs(c[0]*c[8])/(1 - R['xbar'][S0])
    print(f"{n:4d} {nu:6.1f} {np.abs(d-ds).max():9.3f} {abs(d[S0]-ds[S0]):9.3f} {pred:9.3f} {etaS.max():9.3f}")
print(f"elapsed {time.time()-t0:.1f}s")
