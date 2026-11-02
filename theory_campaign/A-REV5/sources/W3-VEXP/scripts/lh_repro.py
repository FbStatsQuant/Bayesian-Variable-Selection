"""Independent reproduction of W1-EXP Thm 5 / Thm 1 / Thm 3-4 evidence on the linked-hub family LH.

Design realisation differs from W1's on purpose: an EXPLICIT n x p design X with X'X = (n-1) Sigma exactly
(X = sqrt(n-1) Q L', Q an orthonormal frame orthogonal to 1, L = chol(Sigma)), and an explicit noise vector
eps ~ N_n(0, I) per replicate; Y = mu + C eps, y = Y/s_y. (W1 simulated sufficient statistics.)
Also an iid-Gaussian design variant (rows iid N(0, Sigma), fresh X per replicate, standardised).

Config A (W1): p = 16, 4 groups of 4, rho = 0.7; link hubs of groups 0,1 with psi = 0.5;
theta: hub0 = 1.4, hub1 = -0.7 (= -psi*1.4, suppressor), hub2 = 1.8; S0 = {0,4,8}, M = {4}, S° = {0,8}.
Outputs per n: quantiles of Mstat = log pi0(S0) + log p + 0.5 log n, sqrt(n)(1 - pi0(S°)), pi0(R_0), pi(S0),
max|R| (EXP' remainder over all within-block additions) vs kappa_EXP, the T22(i) bound check, blocks = groups.
Usage: python3 lh_repro.py [gram|iid] [reps] [npi]   (seed 20261102 + n)
"""
import itertools, math, sys, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import vcore as V

mode = sys.argv[1] if len(sys.argv) > 1 else 'gram'
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 100
NPI = int(sys.argv[3]) if len(sys.argv) > 3 else 30
p, g, rho, psi = 16, 4, 0.7, 0.5
groups = [list(range(h * g, (h + 1) * g)) for h in range(p // g)]
Sigma = np.zeros((p, p))
for G_ in groups:
    for i in G_:
        for j in G_:
            Sigma[i, j] = 1.0 if i == j else rho
a, b = groups[0], groups[1]
ca = Sigma[a, a[0]]; cb = Sigma[b[0], b]
Sigma[np.ix_(a, b)] = psi * np.outer(ca, cb); Sigma[np.ix_(b, a)] = Sigma[np.ix_(a, b)].T
theta = np.zeros(p); theta[0] = 1.4; theta[4] = -psi * 1.4; theta[8] = 1.8
S0 = (0, 4, 8); Sdeg = (0, 8); s = 2; c = 1
sig2 = 1.0
v0 = sig2 + theta @ Sigma @ theta
pred = math.log((s + 1) * p / (2 * p - s - 1))
Lc = np.linalg.cholesky(Sigma)
print('lambda_min(Sigma) =', np.linalg.eigvalsh(Sigma).min(), ' bound (1-psi)(1-rho) =', (1 - psi) * (1 - rho))
print('v_empty =', v0, ' predicted Mstat law (gram): %.3f + chi2_1/(2v)' % pred)


def subsets_mask(Sset):
    out = []
    for r in range(len(Sset) + 1):
        for t in itertools.combinations(Sset, r):
            out.append(V.mask_of(t))
    return out


def run_n(n, rng):
    res = dict(M=[], spi=[], R0=[], piS0=[], maxR=[], kap=[], t22=[], bg=[])
    if mode == 'gram':
        Zm = rng.standard_normal((n, p)); Zm -= Zm.mean(0)
        Q, _ = np.linalg.qr(Zm)
        Xf = math.sqrt(n - 1) * Q @ Lc.T
    for r in range(REPS):
        if mode == 'gram':
            X = Xf
        else:
            Z = rng.standard_normal((n, p)) @ Lc.T
            X = Z - Z.mean(0); X /= X.std(0, ddof=1)
        mu = X @ theta
        eps = rng.standard_normal(n) * math.sqrt(sig2); eps -= eps.mean()
        Y = mu + eps
        y = Y / math.sqrt(Y @ Y / (n - 1))
        G = X.T @ X
        sf = V.Suff(G, X.T @ y, y @ y, n)
        R = G / (n - 1)
        B = V.B_rule(n, p)
        blocks = V.make_blocks(R, B)
        res['bg'].append(sorted(map(tuple, blocks)) == sorted(map(tuple, groups)))
        logr = V.tables(sf, blocks)
        Sm, k, lg = V.log_gamma0_all(sf, blocks, logr)
        pi0 = V.normalise(lg)
        res['M'].append(math.log(pi0[V.mask_of(S0)]) + math.log(p) + 0.5 * math.log(n))
        res['spi'].append(math.sqrt(n) * (1 - pi0[V.mask_of(Sdeg)]))
        res['R0'].append(pi0[subsets_mask(S0)].sum())
        # EXP' remainder over every within-block addition and kappa_EXP (Thm 1 constants, sigma^2 = 1)
        phi2 = min(np.linalg.eigvalsh(R[np.ix_(C, C)]).min() for C in blocks)
        Mn = (mu @ mu) / n
        cst = sig2 / (8 * (Mn + 2 * sig2))
        kap = (1 + 1 / phi2) / (2 * phi2 * (n - 1)) + (n / 2 + 0.01) * (1.02 + 1 / (n * phi2)) / (cst * n)
        mx = 0.0
        for C, t in zip(blocks, logr):
            m = len(C)
            rss = np.zeros(1 << m)
            for code in range(1 << m):
                U = [C[i] for i in range(m) if code >> i & 1]
                rss[code] = sf.yty - (sf.z[U] @ np.linalg.solve(G[np.ix_(U, U)], sf.z[U]) if U else 0.0)
            for code in range(1 << m):
                for i in range(m):
                    if code >> i & 1:
                        continue
                    c2 = code | (1 << i)
                    x = (rss[code] - rss[c2]) / rss[code]
                    Rm = t[c2] - t[code] + 0.5 * math.log(n + 1) + sf.nu * math.log1p(-x)
                    mx = max(mx, abs(Rm))
        res['maxR'].append(mx); res['kap'].append(kap)
        # T22(i) bound at S°: (1-u)^{s+1}/(1+e)^s <= pi0(S°) when u < 1
        bl = {j: bi for bi, C in enumerate(blocks) for j in C}
        pos = {j: C.index(j) for C in blocks for j in C}
        us = []
        for l in range(p):
            if l in Sdeg:
                continue
            bi = bl[l]; C = blocks[bi]; t = logr[bi]
            Ub = sum(1 << pos[j] for j in Sdeg if bl[j] == bi)
            best = -np.inf
            for code in range(1 << len(C)):
                if (code & Ub) == Ub and not (code >> pos[l] & 1):
                    best = max(best, t[code | (1 << pos[l])] - t[code])
            us.append(math.exp(best))
        u = sum(us) / (p - s)
        ee = 0.0
        for bi, C in enumerate(blocks):
            t = logr[bi]
            Ub = sum(1 << pos[j] for j in Sdeg if bl[j] == bi)
            for code in range(1 << len(C)):
                aa = bin(Ub & ~code).count('1')
                if aa > 0:
                    ee = max(ee, math.exp((t[code] - t[code | Ub]) / aa))
        e = 2 * p * ee
        if u < 1:
            res['t22'].append(pi0[V.mask_of(Sdeg)] >= (1 - u) ** (s + 1) / (1 + e) ** s - 1e-12)
        if r < NPI:
            Sm2, k2, lp = V.log_post_all(sf)
            res['piS0'].append(V.normalise(lp)[V.mask_of(S0)])
    return res


out = {}
for n in [100, 400, 1600, 6400, 25600, 102400]:
    rng = np.random.default_rng(20261102 + n)
    rs = run_n(n, rng)
    q = np.quantile(rs['M'], [0.05, 0.5, 0.95])
    line = dict(n=n, Mstat=list(np.round(q, 3)), sqrtn_1mpi0Sdeg_med=round(float(np.median(rs['spi'])), 3),
                pi0R0_med=round(float(np.median(rs['R0'])), 4), piS0_med=round(float(np.median(rs['piS0'])), 4),
                maxR_max=round(float(max(rs['maxR'])), 3), maxR_med=round(float(np.median(rs['maxR'])), 3),
                kappa_med=round(float(np.median(rs['kap'])), 2), t22_ok=f"{sum(rs['t22'])}/{len(rs['t22'])}",
                blocks_eq_groups=f"{sum(rs['bg'])}/{len(rs['bg'])}",
                med_log10_pi0S0=round(float(np.median(np.array(rs['M']) - math.log(p) - 0.5 * math.log(n)) / math.log(10)), 3))
    print(json.dumps(line), flush=True)
    out[n] = line
if mode == 'gram':
    sim = pred + rng.chisquare(1, 200000) * sig2 / (2 * v0)
else:
    sim = pred + rng.chisquare(1, 200000) / 2
print('predicted Mstat quantiles (5/50/95):', np.round(np.quantile(sim, [0.05, 0.5, 0.95]), 3))
json.dump(out, open(__file__.rsplit('/', 2)[0] + f'/results/lh_{mode}.json', 'w'), indent=1)
