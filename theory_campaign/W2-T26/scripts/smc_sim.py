"""Simulate the SMC-BVS v3 FINAL RUN (potential uninterrupted run) at p = 18 with exact precomputed scores,
and compare the realised errors with Theorem A (A-0) bounds.

Final run per METHODOLOGY 6.5, 6.6, 6.8, 6.11, 6.12: N iid pi0 draws; for each stage reweight by exp(Dphi d),
multinomial resampling, one round at phi_t (m = p + B + 2 labelled steps in a fresh uniform random order per particle:
p Gibbs heat-bath flips with additions at |S| = K excluded, one uniform swap, B neighbour swaps with the Hastings
ratio |N(j)\\S| / |N(l)\\S'|, one independence proposal from pi0); then L burn-in and 4 measured rounds at phi = 1
recording o_j before each Gibbs step j. Grid: the ideal full-space ESS grid of bvs_exact.ideal_grid (a proxy for the
calibrated grid; the bounds hold for ANY frozen grid, so the proxy does not affect validity of the comparison).

Usage: python smc_sim.py design n data_seed reps N
Seeds: data rng as in premise_scan.py; SMC rng default_rng(10**6 + 1000*data_seed + rep).
"""
import sys, os, json
import numpy as np
from scipy.special import logsumexp
sys.path.insert(0, os.path.dirname(__file__))
from bvs_exact import Problem
from premise_scan import design


def popc(a, p):
    return ((a[:, None] >> np.arange(p)) & 1).sum(1)


def rand_bit(S, p, rng, want_set=True, allowed=None):
    bits = (S[:, None] >> np.arange(p)) & 1
    ok = bits == 1 if want_set else bits == 0
    if allowed is not None:
        ok &= ((allowed[:, None] >> np.arange(p)) & 1) == 1
    keys = rng.random(ok.shape)
    keys[~ok] = -1.0
    return keys.argmax(1), ok.any(1)


class Sim:
    def __init__(self, pr):
        self.pr = pr
        self.p, self.B, self.K = pr.p, pr.B, pr.K
        self.m = pr.p + pr.B + 2
        self.nbmask = np.array([sum(1 << l for l in pr.nbr[j]) for j in range(pr.p)], dtype=np.int64)
        self.cdf0 = np.cumsum(pr.pi0)
        self.cdf0 /= self.cdf0[-1]

    def draw0(self, N, rng):
        return np.searchsorted(self.cdf0, rng.random(N), side='right').astype(np.int64)

    def lg(self, S, phi):
        return self.pr.lg0[S] + phi * self.pr.d[S]

    def round(self, S, phi, rng, record=None, track=None):
        pr, p, B, K = self.pr, self.p, self.B, self.K
        N = len(S)
        order = rng.random((N, self.m)).argsort(1)
        for k in range(self.m):
            lab = order[:, k]
            # Gibbs
            g = np.nonzero(lab < p)[0]
            if g.size:
                j = lab[g]; s = S[g]
                sin = s | (1 << j); sout = s & ~(1 << j)
                a = self.lg(sin, phi); b = self.lg(sout, phi)
                feas_in = pr.feas[sin]
                o = np.where(feas_in, 1.0 / (1.0 + np.exp(np.clip(b - a, -700, 700))), 0.0)
                if record is not None:
                    np.add.at(record, (g, j), o)
                S[g] = np.where(rng.random(g.size) < o, sin, sout)
            # uniform swap
            u = np.nonzero(lab == p)[0]
            if u.size:
                s = S[u]; k_ = popc(s, p)
                act = (k_ > 0) & (k_ < p)
                i_out, _ = rand_bit(s, p, rng, True)
                l_in, _ = rand_bit(s, p, rng, False)
                sp = s ^ (1 << i_out) ^ (1 << l_in)
                acc = act & (np.log(rng.random(u.size)) < self.lg(sp, phi) - self.lg(s, phi))
                S[u] = np.where(acc, sp, s)
            # neighbour swaps
            v = np.nonzero((lab > p) & (lab <= p + B))[0]
            if v.size:
                s = S[v]
                nonempty = s != 0
                jdel, _ = rand_bit(s, p, rng, True)
                cand = self.nbmask[jdel] & ~s
                l_add, has = rand_bit(s, p, rng, False, allowed=cand)
                sp = s ^ (1 << jdel) ^ (1 << l_add)
                ncand = popc(cand, p)
                nrev = popc(self.nbmask[l_add] & ~sp, p)
                ok = nonempty & has & pr.feas[sp]
                lr = np.where(ok, self.lg(sp, phi) - self.lg(s, phi) + np.log(np.maximum(ncand, 1))
                              - np.log(np.maximum(nrev, 1)), -np.inf)
                acc = ok & (np.log(rng.random(v.size)) < lr)
                S[v] = np.where(acc, sp, s)
            # independence
            w = np.nonzero(lab == p + B + 1)[0]
            if w.size:
                s = S[w]; sp = self.draw0(w.size, rng)
                acc = np.log(rng.random(w.size)) < phi * (pr.d[sp] - pr.d[s])
                S[w] = np.where(acc, sp, s)
            if track is not None:
                track |= S != self.pr.S0
        return S

    def island(self, grid, N, L, rng):
        pr = self.pr
        S = self.draw0(N, rng)
        logW = logsumexp(pr.lg0) - logsumexp(pr.lg1)  # log(Zbar0 / Zbar1); W = Zhat_r / Z
        for t in range(1, len(grid)):
            dphi = grid[t] - grid[t - 1]
            lw = dphi * pr.d[S]
            logW += logsumexp(lw) - np.log(N)
            prob = np.exp(lw - logsumexp(lw))
            S = S[np.searchsorted(np.cumsum(prob) / prob.sum(), rng.random(N), side='right').clip(0, N - 1)]
            S = self.round(S, grid[t], rng)
        f = float(np.mean(S != pr.S0))
        for _ in range(L):
            S = self.round(S, 1.0, rng)
        rec = np.zeros((N, self.p))
        g = []
        for _ in range(4):
            g.append(float(np.mean(S != pr.S0)))
            S = self.round(S, 1.0, rng, record=rec)
        pip = rec.sum(0) / (4 * N)
        self.last_g = g
        return float(np.exp(logW)), f, pip


def main():
    name, n, dseed, reps, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    di = ['fav_iid', 'fav_cor', 'masked'].index(name)
    rng = np.random.default_rng(1000 * di + dseed + 7919 * n)
    X, y, S0 = design(name, n, rng)
    pr = Problem(X, y, S0)
    q = pr.premise()
    grid = pr.ideal_grid()
    T = len(grid) - 1
    sim = Sim(pr)
    truth = np.array([1.0 if j in S0 else 0.0 for j in range(pr.p)])
    pip_exact = np.array([pr.pi[(pr.masks >> j) & 1 == 1].sum() for j in range(pr.p)])
    Delta = q['Delta']
    b = 2 * (T + 1) * Delta / (1 - Delta)
    fbound = min(1.0, 2 * q['delta1'] + 2 * b)
    pipbound = fbound + min(1.0, q['rho_bar_bound']) + q['u_pi']          # Theorem A (A-0)(c), Lemma 3
    pipbound_old = fbound + (pr.L + 2.5) * min(1.0, q['rho_bar_bound']) + q['u_pi']  # end-of-stage-T route (Remark 3.1)
    Ws, fs, perr, pooled, primerr, mpm_wrong, gs = [], [], [], [], [], 0, []
    for rep in range(reps):
        srng = np.random.default_rng(10 ** 6 + 1000 * dseed + rep)
        isl = []
        for _ in range(4):
            isl.append(sim.island(grid, N, pr.L, srng)); gs.extend(sim.last_g)
        for W, f, pip in isl:
            Ws.append(W); fs.append(f); perr.append(np.abs(pip - truth).max())
        pooled.append(np.mean([w for w, _, _ in isl]))
        prim = np.mean([pp for _, _, pp in isl], axis=0)
        primerr.append(np.abs(prim - truth).max())
        mpm_wrong += int(not np.array_equal(prim > 0.5, truth > 0.5))
    Ws = np.array(Ws)
    out = dict(design=name, n=n, data_seed=dseed, reps=reps, N=N, T=T, L=pr.L, Delta=Delta, delta1=q['delta1'],
               one_minus_pi0=q['one_minus_pi0'], u_pi=q['u_pi'], rho_bar_bound=q['rho_bar_bound'],
               rho_star=q['rho_star'],
               bound_b=b, mean_abs_W_minus_1=float(np.abs(Ws - 1).mean()), mean_W=float(Ws.mean()),
               mean_abs_pooled_minus_1=float(np.abs(np.array(pooled) - 1).mean()),
               bound_f=fbound, mean_f=float(np.mean(fs)),
               bound_pip=pipbound, bound_pip_old=pipbound_old, max_round_start_f=float(np.max(gs)) if gs else None, mean_round_start_f=float(np.mean(gs)) if gs else None, mean_island_pip_err=float(np.mean(perr)), mean_primary_pip_err=float(np.mean(primerr)),
               exact_pip_err=float(np.abs(pip_exact - truth).max()), mpm_wrong_frac=mpm_wrong / reps)
    print(json.dumps(out))


if __name__ == '__main__':
    main()
