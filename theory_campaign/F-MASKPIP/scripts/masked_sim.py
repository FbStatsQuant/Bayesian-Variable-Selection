"""F-MASKPIP: exact-score simulation of the SMC-BVS v3 FINAL RUN on masked designs at p = 18.

Adapted from W2-T26 smc_sim.py (the round kernel `Sim.round` is reused unchanged). Per island r it records
  logW_r      = log(Zhat_r / Z)                          (evidence ratio, exact Z by enumeration)
  f_r         = fraction of particles != S0 at the end of stage T (after the stage-T round)
  g_r[0..3]   = fraction != S0 at the start of each of the 4 measured rounds
  Bbar_r      = fraction of (particle, measured round) pairs whose within-round path, INCLUDING its start,
                visits a state != S0 (track initialised to S != S0, then OR-ed after every elementary step)
  err_r       = max_j |PIPhat_rj - 1{j in S0}|   (Rao-Blackwell PIP of island r over the 4 measured rounds)
and per rep: primary pooled PIP error (equal-weight mean of the 4 island PIPs) and MPM correctness.

Grids (all frozen before the final run):
  G1: (0, 1)                                   one-shot importance sampling, then L burn-in + 4 measured rounds.
  G2: bvs_exact.ideal_grid (full-space ESS 0.9 bisection).
  G3: "blind" grid: ESS 0.9 bisection RESTRICTED to the set V of distinct states in a pilot of N iid pi0 draws
      (rho_V(u,v) = Zbar_v(V)^2 / (Zbar_u(V) Zbar_{2v-u}(V))), mimicking the candidate-set restriction (T13).
      One pilot per setting, seed default_rng(3*10**6 + 7919*n + N + 100*design_index).

Designs: 'masked' = premise_scan.design('masked') (corr(x3, x0) = 0.6, beta = (1, -0.6, 0.6) on {0, 3, 12});
         'masked8' = same construction with corr(x3, x0) = 0.8 and beta_3 = -0.8 (so cov(x3, mu) = 0 exactly in
         population: 1*0.8 - 0.8*1 = 0), i.e. stronger masking. Data rng: default_rng(1000*di + dseed + 7919*n)
         with di = 2 (masked) or 3 (masked8).
SMC seeds: default_rng(10**6 + 1000*dseed + rep + 10**5*grid_index + 7*N) per rep (4 islands drawn sequentially).

Usage: python masked_sim.py design n N grid reps outfile
"""
import sys, os, json, time
import numpy as np
from math import log
from scipy.special import logsumexp
sys.path.insert(0, os.path.dirname(__file__))
from bvs_exact import Problem
from premise_scan import design as design_base, P
from smc_sim import Sim

DESIGNS = ['fav_iid', 'fav_cor', 'masked', 'masked8']
GRIDS = ['G1', 'G2', 'G3']


def design(name, n, rng):
    if name != 'masked8':
        return design_base(name, n, rng)
    rho = 0.5
    Zg = rng.standard_normal((n, 6))
    E = rng.standard_normal((n, P))
    X = np.empty((n, P))
    for j in range(P):
        X[:, j] = np.sqrt(rho) * Zg[:, j // 3] + np.sqrt(1 - rho) * E[:, j]
    X[:, 3] = 0.8 * X[:, 0] + 0.6 * X[:, 3]
    beta = np.zeros(P)
    S0 = [0, 3, 12]; beta[0] = 1.0; beta[3] = -0.8; beta[12] = 0.6
    y = X @ beta + rng.standard_normal(n)
    return X, y, S0


def restricted_grid(pr, V, thr=0.9, halvings=60):
    lg0, d = pr.lg0[V], pr.d[V]

    def lZ(v):
        return logsumexp(lg0 + v * d)
    grid, u = [0.0], 0.0
    while u < 1.0:
        def ok(v):
            return 2 * lZ(v) - lZ(u) - lZ(2 * v - u) >= log(thr)
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
        grid.append(v); u = v
        if len(grid) > 100000:
            return None
    return grid


class MSim(Sim):
    def island(self, grid, N, L, rng):
        pr = self.pr
        S = self.draw0(N, rng)
        logW = logsumexp(pr.lg0) - logsumexp(pr.lg1)  # log(Zbar0/Zbar1)
        for t in range(1, len(grid)):
            lw = (grid[t] - grid[t - 1]) * pr.d[S]
            logW += logsumexp(lw) - np.log(N)
            prob = np.exp(lw - logsumexp(lw))
            S = S[np.searchsorted(np.cumsum(prob) / prob.sum(), rng.random(N), side='right').clip(0, N - 1)]
            S = self.round(S, grid[t], rng)
        f = float(np.mean(S != pr.S0))
        for _ in range(L):
            S = self.round(S, 1.0, rng)
        rec = np.zeros((N, self.p))
        g, bb = [], 0.0
        for _ in range(4):
            g.append(float(np.mean(S != pr.S0)))
            track = S != pr.S0
            S = self.round(S, 1.0, rng, record=rec, track=track)
            bb += track.mean()
        return float(logW), f, g, bb / 4, rec.sum(0) / (4 * N)


def main():
    name, n, N, gname, reps, outfile = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], \
        int(sys.argv[5]), sys.argv[6]
    dseed = 0
    di, gi = DESIGNS.index(name), GRIDS.index(gname)
    t0 = time.time()
    X, y, S0 = design(name, n, np.random.default_rng(1000 * di + dseed + 7919 * n))
    pr = Problem(X, y, S0)
    q = pr.premise(phis=np.linspace(0, 1, 3))
    sim = MSim(pr)
    truth = np.array([1.0 if j in S0 else 0.0 for j in range(pr.p)])
    pip_exact = np.array([pr.pi[(pr.masks >> j) & 1 == 1].sum() for j in range(pr.p)])
    if gname == 'G1':
        grid = [0.0, 1.0]
    elif gname == 'G2':
        grid = pr.ideal_grid()
    else:
        prng = np.random.default_rng(3 * 10 ** 6 + 7919 * n + N + 100 * di)
        V = np.unique(sim.draw0(N, prng))
        grid = restricted_grid(pr, V)
    T = len(grid) - 1
    pil = dict(design=name, n=n, N=N, grid_name=gname, T=T, grid=[float(v) for v in grid], L=pr.L, B=pr.B,
               blocks=pr.blocks, delta1=float(q['delta1']), u_pi=float(q['u_pi']), rho_bar=float(q['rho_bar']),
               pi0_S0=float(pr.pi0[pr.S0]), pi_S0=float(pr.pi[pr.S0]),
               exact_pip_err=float(np.abs(pip_exact - truth).max()), pip_exact=pip_exact.tolist(),
               S0_is_HPM=int(np.argmax(pr.lg1) == pr.S0), start_mode=int(np.argmax(pr.lg0)), S0=pr.S0)
    if gname == 'G3':
        pil['V_size'] = int(len(V)); pil['S0_in_V'] = bool(np.any(V == pr.S0))
        pil['V_has_x3'] = bool(np.any((V >> 3) & 1))
    with open(outfile, 'w') as fh:
        fh.write(json.dumps(dict(kind='setting', **pil)) + '\n')
        for rep in range(reps):
            srng = np.random.default_rng(10 ** 6 + 1000 * dseed + rep + 10 ** 5 * gi + 7 * N)
            isl = [sim.island(grid, N, pr.L, srng) for _ in range(4)]
            prim = np.mean([x[4] for x in isl], axis=0)
            prim_err = float(np.abs(prim - truth).max())
            mpm_ok = bool(np.array_equal(prim > 0.5, truth > 0.5))
            for r, (lW, f, g, bb, pip) in enumerate(isl):
                fh.write(json.dumps(dict(kind='island', design=name, n=n, N=N, grid_name=gname, T=T, rep=rep,
                                         island=r, logW=lW, f=f, g=g, Bbar=float(bb),
                                         err=float(np.abs(pip - truth).max()), pip=pip.tolist(),
                                         primary_err=prim_err, mpm_correct=mpm_ok)) + '\n')
            fh.flush()
    print(f'done {name} n={n} N={N} {gname} T={T} reps={reps} {time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
