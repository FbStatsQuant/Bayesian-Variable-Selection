"""W5-B2ENV s2b: NB' and D2's inputs on a large-p exact-Gram LH (c = 1), where the pilot does NOT draw S0.  Seed 20261102.

Design: groups of g = 4 (rho = 0.7); group 0 = a (hub 0), group 1 = b (hub 4, psi = 0.5), group 2 visible (hub 8), all other
groups null (independent).  beta_a = 1.4, beta_h = 1.8, sigma = 1 (configuration A plus null groups).  X'X = (n-1)Sigma exactly;
X'y is drawn from its exact law block by block (Sigma is block diagonal apart from the linked pair).  B = 16 >= g, and complete
linkage gives blocks = groups here except that 4 groups may be packed together only if g <= B/... -- NOTE: with B = 16 and
g = 4, next-fit packing would merge groups; we therefore use the *group partition* (the LH theorem's setting g <= B < 2g has
g >= 9 at B = 16).  The statistics of the theorem (pi0 structure, d, ESS) are computed for the group partition.
pi0 sampling: exact backward sampler over blocks with the total size truncated at kmax = 40 (pi0(|S| > 40) is below 1e-100
here; a negligible EX-A deviation).
Reported per n: pi0(S°), H*pi0(S0), the d-jump of a proxy draw, the fraction of pilot repetitions with NB'^c, with S0 drawn,
the pilot's first temperature phi_1 (and whether forced), the weighted share of S°, Dep at S° (exact sum over all l), beta,
and D2's bound.
"""
import sys, time
from math import ceil, log, sqrt, lgamma
import numpy as np

out = []
pr = lambda s: (out.append(s), print(s, flush=True))
RSTAR = (11 + 2 * sqrt(10)) / 9
g, rho, psi, ba, bh, sig = 4, 0.7, 0.5, 1.4, 1.8, 1.0
a0 = b0 = 0.01


def group_corr():
    E = np.full((g, g), rho); np.fill_diagonal(E, 1.0); return E


def build(n, G, rng):
    p = G * g
    E = group_corr()
    # pair block (groups 0,1), 8x8
    P = np.zeros((2 * g, 2 * g)); P[:g, :g] = E; P[g:, g:] = E
    cross = psi * np.outer(E[:, 0], E[0, :]); P[:g, g:] = cross; P[g:, :g] = cross.T
    blocks = [(P, [0, 1])] + [(E, [h]) for h in range(2, G)]
    theta = np.zeros(p); theta[0] = ba; theta[4] = -psi * ba; theta[8] = bh
    # exact law of X'Y and Y'Y:  X'Y = (n-1) Sigma theta + sqrt(n-1) L xi, Y'Y = (n-1) th'Sig th + 2 sqrt(n-1) th' L xi + xi'xi + chi2
    XtY = np.zeros(p); cross_term = 0.0; xx = 0.0; tSt = 0.0
    for (Sb, grs) in blocks:
        idx = np.concatenate([np.arange(h * g, (h + 1) * g) for h in grs])
        L = np.linalg.cholesky(Sb)
        xi = rng.standard_normal(len(idx)) * sig
        tb = theta[idx]
        XtY[idx] = (n - 1) * Sb @ tb + sqrt(n - 1) * L @ xi
        cross_term += tb @ L @ xi; xx += xi @ xi; tSt += tb @ Sb @ tb
    YtY = (n - 1) * tSt + 2 * sqrt(n - 1) * cross_term + xx + sig ** 2 * rng.chisquare(n - 1 - p)
    sy = sqrt(YtY / (n - 1))
    z = XtY / sy                         # X'y for standardised y; y'y = n-1
    return p, blocks, theta, z


class Model:
    def __init__(self, n, G, rng):
        self.n, self.G = n, G
        self.p, self.blocks, self.theta, self.z = build(n, G, rng)
        p = self.p
        self.K = min(p, n // 2)
        self.nu = a0 + n / 2
        self.yy = n - 1.0
        self.base = -self.nu * log(2 * b0 + self.yy)
        E = group_corr()
        self.Sfull_pair = self.blocks[0][0]
        # log w(k) - normalisation irrelevant for ratios; we need W_K only for absolute pi0 (computed via DP)
        self.lw = lambda k: log(0.5) - (lgamma(2 * p) - lgamma(k + 1) - lgamma(2 * p - k))
        # per-group tables over the 16 subsets (group partition; the pair is two blocks of the start)
        self.tab = np.zeros((G, 16))
        for h in range(G):
            for U in range(16):
                idx = [h * g + j for j in range(g) if (U >> j) & 1]
                self.tab[h, U] = self.logBF(idx)
        self.size16 = np.array([bin(U).count("1") for U in range(16)])

    def corr(self, idx):
        idx = np.asarray(idx)
        gr = idx // g
        R = np.zeros((len(idx), len(idx)))
        E = group_corr(); P = self.Sfull_pair
        for a in range(len(idx)):
            for b in range(len(idx)):
                ga, gb = gr[a], gr[b]
                if ga <= 1 and gb <= 1:
                    R[a, b] = P[idx[a], idx[b]]
                elif ga == gb:
                    R[a, b] = E[idx[a] % g, idx[b] % g]
        return R

    def logBF(self, idx):
        if len(idx) == 0: return 0.0
        n = self.n
        Gs = (n - 1) * self.corr(idx); zs = self.z[list(idx)]
        H = (n + 1) * Gs + np.eye(len(idx))
        ldH = np.linalg.slogdet(H)[1]; ldG = np.linalg.slogdet(Gs + np.eye(len(idx)))[1]
        Q = self.yy - n * zs @ np.linalg.solve(H, zs)
        return -0.5 * (ldH - ldG) - self.nu * log(2 * b0 + Q) - self.base

    def d(self, S):
        S = sorted(S)
        lt = 0.0
        for h in set(j // g for j in S):
            U = sum(1 << (j % g) for j in S if j // g == h); lt += self.tab[h, U]
        return self.logBF(S) - lt

    def prepare_sampler(self, kmax=40):
        # forward DP over groups: F[h][k] = log sum over subsets of groups >= h with total size k of prod tables
        G = self.G
        self.kmax = kmax
        poly = np.full((G, g + 1), -np.inf)
        for h in range(G):
            for k in range(g + 1):
                sel = self.size16 == k
                m = self.tab[h, sel].max(); poly[h, k] = m + log(np.exp(self.tab[h, sel] - m).sum())
        self.poly = poly
        F = np.full((G + 1, kmax + 1), -np.inf); F[G, 0] = 0.0
        for h in range(G - 1, -1, -1):
            acc = np.full((g + 1, kmax + 1), -np.inf)
            for j in range(g + 1):
                acc[j, j:] = poly[h, j] + F[h + 1, :kmax + 1 - j]
            m = acc.max(0); mm = np.where(np.isfinite(m), m, 0)
            F[h] = mm + np.log(np.exp(acc - mm).sum(0))
        self.F = F
        lwk = np.array([self.lw(k) for k in range(kmax + 1)])
        self.logmass_k = lwk + F[0]          # unnormalised log pi0(|S| = k)
        self.logZ0 = np.logaddexp.reduce(self.logmass_k)

    def draw(self, N, rng):
        G, g_ = self.G, g
        pk = np.exp(self.logmass_k - self.logZ0)
        ks = rng.choice(len(pk), size=N, p=pk / pk.sum())
        states = []
        # vectorised over draws: sequential over groups
        rem = ks.copy(); sel = [[] for _ in range(N)]
        for h in range(G):
            # P(group h has j | remaining r) ∝ poly[h,j] + F[h+1, r-j]
            lp = np.full((N, g_ + 1), -np.inf)
            for j in range(g_ + 1):
                ok = rem >= j
                lp[ok, j] = self.poly[h, j] + self.F[h + 1, rem[ok] - j]
            lp -= lp.max(1, keepdims=True); pr_ = np.exp(lp); pr_ /= pr_.sum(1, keepdims=True)
            u = rng.random(N); js = (pr_.cumsum(1) < u[:, None]).sum(1)
            nz = np.nonzero(js)[0]
            for i in nz:
                j = js[i]
                cand = np.nonzero(self.size16 == j)[0]
                w = np.exp(self.tab[h, cand] - self.tab[h, cand].max()); w /= w.sum()
                U = cand[min(np.searchsorted(w.cumsum(), rng.random()), len(cand) - 1)]
                sel[i] += [h * g_ + b for b in range(g_) if (U >> b) & 1]
            rem -= js
        return [tuple(sorted(s)) for s in sel]

    def logpi0(self, S):
        lt = 0.0
        for h in set(j // g for j in S):
            U = sum(1 << (j % g) for j in S if j // g == h); lt += self.tab[h, U]
        return self.lw(len(S)) + lt - self.logZ0


def ess_frac(dv, delta):
    lw = delta * dv; w = np.exp(lw - lw.max()); return w.sum() ** 2 / (len(w) * (w ** 2).sum())


def pilot_first_phi(dv, Te):
    if ess_frac(dv, 1.0) >= 0.9: return 1.0, False
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if ess_frac(dv, mid) >= 0.9: lo = mid
        else: hi = mid
    return (1.0 / Te, True) if lo < 1.0 / Te else (lo, False)


def gfun(f): return f - np.sqrt(f * (1 - f)) / 3


def run(n, G, reps, rng):
    t0 = time.time()
    m = Model(n, G, rng); m.prepare_sampler()
    p = m.p; Sref = (0, 8); S0 = (0, 4, 8)
    l_ = ceil(log(n + p + 1, 2)); T0 = max(1000, l_ * l_); H = ceil(512 * max(2500, n, p) / 2500)
    lp_ref = m.logpi0(Sref); lp_S0 = m.logpi0(S0)
    dref = m.d(Sref)
    dprox = m.d((0, 5, 8)) - dref
    # Dep at S°: all l except the masked group's proxies (D = {5,6,7}) and j_b = 4
    s = 2
    lw1 = m.lw(s + 1) - m.lw(s); lwm = m.lw(s - 1) - m.lw(s)
    lBFref = m.logBF(list(Sref))
    dep = 0.0
    for l in range(p):
        if l in (4, 5, 6, 7): continue
        if l in Sref:
            S_ = [j for j in Sref if j != l]
            k0 = lwm + sum(m.tab[j // g, 0] for j in [l]) - m.tab[l // g, 1 << (l % g)]
            k1 = lwm + m.logBF(S_) - lBFref
        else:
            h = l // g; U = sum(1 << (j % g) for j in Sref if j // g == h)
            k0 = lw1 + m.tab[h, U | (1 << (l % g))] - m.tab[h, U]
            k1 = lw1 + m.logBF(sorted(list(Sref) + [l])) - lBFref
        dep += np.exp(min(max(k0, k1), 50))
    beta = max(0.0, 1 - dep) / (3 + 16 + 3)       # k_D = g-1 = 3, B = 16
    pr(f"n={n} p={p} G={G}: pi0(S°)={np.exp(lp_ref):.4f}  pi0(S0)={np.exp(lp_S0):.2e}  H={H}  H*pi0(S0)={H*np.exp(lp_S0):.3f}  "
       f"sqrt(n)/p={sqrt(n)/p:.4f}  d(S°+proxy)-d(S°)={dprox:.0f} vs T0 log r*={T0*log(RSTAR):.0f}  Dep={dep:.4f} beta={beta:.4f}  "
       f"(setup {time.time()-t0:.0f}s)")
    nbfail = s0d = forced = 0; phis = []; shares = []; drs = []; proxy_draws = 0
    for rep in range(reps):
        X = m.draw(H, rng)
        dv = np.array([m.d(S) if len(S) else 0.0 for S in X])
        has = any(S == S0 for S in X); s0d += has
        proxy_draws += sum(1 for S in X if any(j in (5, 6, 7) for j in S) or (4 in S and S != S0))
        nb = has or ess_frac(dv, 1.0 / T0) >= 0.9; nbfail += not nb
        phi1, f = pilot_first_phi(dv, T0); forced += f; phis.append(phi1)
        lw = phi1 * dv; w = np.exp(lw - lw.max())
        at = np.array([S == Sref for S in X]); shares.append(w[at].sum() / w.sum())
        good = np.array([S == Sref or (set(Sref) <= set(S) and not set(S) & {4, 5, 6, 7} and len(S) <= 4) for S in X])
        drs.append(dv[good].max() - dv[good].min())
    sh = np.array(shares)
    bound = min(np.exp(-2 * H * t ** 2) + np.exp(-H * beta * gfun(np.exp(lp_ref) - t)) for t in np.linspace(0.01, np.exp(lp_ref) - 0.11, 50))
    pr(f"    {reps} pilots: P(NB'^c)={nbfail/reps:.3f}  P(S0 drawn)={s0d/reps:.3f}  draws touching C_b (not S0): {proxy_draws} in total  "
       f"phi_1: median {np.median(phis):.4f} (forced {forced})  share of S° after weighting: min {sh.min():.3f}  "
       f"d-range on G: max {max(drs):.2f}  D2 bound (t optimised, excl. NB'): {bound:.2e}")


if __name__ == "__main__":
    rng = np.random.default_rng(20261102)
    for n, G, reps in [(10000, 1000, 20), (40000, 5000, 10)]:
        run(n, G, reps, rng)
    open(__file__.replace(".py", ".txt"), "w").write("\n".join(out) + "\n")
