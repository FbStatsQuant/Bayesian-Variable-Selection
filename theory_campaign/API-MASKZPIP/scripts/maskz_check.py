"""API-MASKZPIP numerical checks at p = 18 (exact scores by enumeration; engine-faithful final-run simulator
vendored from theory/F-MASKPIP (scripts/vendor/, round kernel unchanged from W2-T26)).

Checks, per design (masked, masked8) and n:
  (S)  Theorem E1 (two-phase sandwich, deterministic): for every island, with t = first stage index such that all
       particles of stages t..T-1 equal S0 (if any), x° = start mode, eta = max_{x visited at stages < t}|d(x)-d(x°)|,
       the realised log W lies in [pred - phi_t*eta, pred + phi_t*eta] (eta' = 0 because phase 2 is at S0 exactly),
       pred = log q_t(x°) - log q_t(S0) + log pi(S0) - log pi0(x°).
  (U)  Theorem E2 (miss bound): E[W 1{no stage-(t-1) particle in A}] <= kappa_t(A); empirical mean reported.
       A = {x : 3 in x} (models containing the masked variable x3).
  (H)  The hockey stick: grid (0, phi_a, 1), log W vs  min(0, log-odds_{phi_a}(A^c : A)) (two-state prediction).
  (P)  Theorem P1 (PIP bias <= TV): |mean_r PIPhat_rj - PIP_j| vs TV(nubar, pi), nubar = mean empirical
       end-of-stage-T law.
Usage: python maskz_check.py design n N reps outfile     (seeds fixed; see code)
"""
import sys, os, json, time
import numpy as np
from scipy.special import logsumexp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendor'))
from bvs_exact import Problem
from masked_sim import design, DESIGNS, restricted_grid
from smc_sim import Sim

HUB = 3


class CSim(Sim):
    def island(self, grid, N, L, rng):
        pr = self.pr
        S = self.draw0(N, rng)
        pops = [S.copy()]                     # population of stage t (post-mutation), t = 0..T-1 used by increments
        logW = logsumexp(pr.lg0) - logsumexp(pr.lg1)
        for t in range(1, len(grid)):
            lw = (grid[t] - grid[t - 1]) * pr.d[S]
            logW += logsumexp(lw) - np.log(N)
            prob = np.exp(lw - logsumexp(lw))
            S = S[np.searchsorted(np.cumsum(prob) / prob.sum(), rng.random(N), side='right').clip(0, N - 1)]
            S = self.round(S, grid[t], rng)
            pops.append(S.copy())
        endT = S.copy()
        for _ in range(L):
            S = self.round(S, 1.0, rng)
        rec = np.zeros((N, self.p))
        for _ in range(4):
            S = self.round(S, 1.0, rng, record=rec)
        return float(logW), pops, endT, rec.sum(0) / (4 * N)


def main():
    name, n, N, reps, outfile = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    di = DESIGNS.index(name)
    t0 = time.time()
    X, y, S0 = design(name, n, np.random.default_rng(1000 * di + 0 + 7919 * n))   # data seed 0 as F-MASKPIP
    pr = Problem(X, y, S0)
    sim = CSim(pr)
    s0 = pr.S0
    xo = int(np.argmax(pr.lg0))
    inA = ((pr.masks >> HUB) & 1) == 1
    lg0n = pr.lg0 - logsumexp(pr.lg0)                       # log pi0
    lpi = pr.lg1 - logsumexp(pr.lg1)                        # log pi
    feas = pr.feas
    dmax = pr.d[feas].max(); xm = int(np.argmax(np.where(feas, pr.d, -np.inf)))
    pip_exact = np.array([pr.pi[(pr.masks >> j) & 1 == 1].sum() for j in range(pr.p)])

    def lq(phi):          # log q_phi over Omega
        a = pr.lg0 + phi * pr.d
        return a - logsumexp(a)

    def log_kappa(phi_t):   # kappa_t(A) = sum_{A^c} gamma0 e^{phi_t d + (1-phi_t) dmax} / Zbar_1
        sel = (~inA) & feas
        return float(logsumexp(pr.lg0[sel] + phi_t * pr.d[sel] + (1 - phi_t) * dmax) - logsumexp(pr.lg1))

    def two_state_pred(phi):  # min(0, log q_phi(A^c)/q_phi(A)) -- hockey-stick prediction for grid (0, phi, 1)
        l = lq(phi)
        return min(0.0, float(logsumexp(l[(~inA) & feas]) - logsumexp(l[inA & feas])))

    setting = dict(kind='setting', design=name, n=n, N=N, S0=s0, start_mode=xo, start_mode_bits=[j for j in range(pr.p) if xo >> j & 1],
                   xm=xm, xm_is_S0=bool(xm == s0), log_pi0_S0=float(lg0n[s0]), log_pi_S0=float(lpi[s0]),
                   log_pi0_xo=float(lg0n[xo]), log_pi_xo=float(lpi[xo]), pi0_A=float(np.exp(logsumexp(lg0n[inA & feas]))),
                   pi_A=float(np.exp(logsumexp(lpi[inA & feas]))), dmax=float(dmax), d_S0=float(pr.d[s0]),
                   d_xo=float(pr.d[xo]), D=float(dmax - pr.d[(~inA) & feas].max()), delta1=float(1 - pr.pi[s0]),
                   pip_exact=pip_exact.tolist())
    a = float(lg0n[xo] - lg0n[s0]); Lam = float(lpi[s0] - lpi[xo])
    setting.update(a=a, Lambda=Lam, phi_star=a / (a + Lam) if a + Lam > 0 else None)
    grids = {}
    for phia in np.logspace(-4, 0, 13)[:-1]:
        grids[f'J{phia:.2e}'] = [0.0, float(phia), 1.0]
    grids['G1'] = [0.0, 1.0]
    grids['G2'] = pr.ideal_grid()
    prng = np.random.default_rng(3 * 10 ** 6 + 7919 * n + N + 100 * di)
    grids['G3'] = restricted_grid(pr, np.unique(sim.draw0(N, prng)))
    out = open(outfile, 'w')
    out.write(json.dumps(setting) + '\n')
    for gi, (gname, grid) in enumerate(grids.items()):
        T = len(grid) - 1
        lqs = [lq(f) for f in grid]
        rng = np.random.default_rng(5 * 10 ** 6 + 7919 * n + 13 * gi + N + 100 * di)
        rows = []
        pip_sum = np.zeros(pr.p); nu = {}
        for rep in range(reps):
            lW, pops, endT, pip = sim.island(grid, N, pr.L, rng)
            # (S) sandwich: t = first index with all stages t..T-1 at S0
            t_sw = None
            for t in range(T):
                if all(np.all(pops[k] == s0) for k in range(t, T)):
                    t_sw = t; break
            sand = None
            if t_sw is not None and t_sw >= 1:
                vis = np.unique(np.concatenate(pops[:t_sw]))
                eta = float(np.abs(pr.d[vis] - pr.d[xo]).max())
                ph = grid[t_sw]
                pred = float(lqs[t_sw][xo] - lqs[t_sw][s0] + lpi[s0] - lg0n[xo])
                sand = dict(t=t_sw, phi_t=ph, eta=eta, pred=pred, lo=pred - ph * eta, hi=pred + ph * eta,
                            ok=bool(pred - ph * eta - 1e-8 <= lW <= pred + ph * eta + 1e-8))
            elif t_sw == 0:
                sand = dict(t=0, pred=float(lpi[s0] - lpi[s0] + lqs[T][s0] - lqs[0][s0]))  # W = pi(S0)/pi0(S0) exactly
                sand['ok'] = bool(abs(lW - (lpi[s0] - lg0n[s0])) < 1e-8)
            # (U) miss events: E_t := no particle of stage t-1 in A, t = 1..T
            miss = [bool(not np.any(inA[pops[t - 1]])) for t in range(1, T + 1)]
            rows.append(dict(logW=lW, sand=sand, miss=miss, f_endT=float(np.mean(endT != s0)),
                             frac_S0_stage=[float(np.mean(P == s0)) for P in pops],
                             err_post=float(np.abs(pip - pip_exact).max())))
            pip_sum += pip
            u, c = np.unique(endT, return_counts=True)
            for uu, cc in zip(u, c):
                nu[int(uu)] = nu.get(int(uu), 0.0) + cc / N / reps
        pip_mean = pip_sum / reps
        nu_vec = np.zeros(len(pr.pi)); nu_vec[list(nu.keys())] = list(nu.values())
        TV = 0.5 * float(np.abs(nu_vec - pr.pi).sum())
        lWs = np.array([r['logW'] for r in rows])
        lk = [log_kappa(grid[t]) for t in range(1, T + 1)]
        EWmiss = [float(np.mean([np.exp(r['logW']) * r['miss'][t] for r in rows])) for t in range(T)]
        summ = dict(kind='grid', design=name, n=n, N=N, grid_name=gname, T=T, grid=[float(v) for v in grid],
                    reps=reps, median_logW=float(np.median(lWs)), q05_logW=float(np.quantile(lWs, .05)),
                    q95_logW=float(np.quantile(lWs, .95)), sd_logW=float(lWs.std()), mean_W=float(np.exp(lWs).mean()),
                    two_state_pred=two_state_pred(grid[1]) if T == 2 else None,
                    sandwich_applicable=int(sum(r['sand'] is not None for r in rows)),
                    sandwich_ok=int(sum(bool(r['sand'] and r['sand']['ok']) for r in rows)),
                    sandwich_pred_median=float(np.median([r['sand']['pred'] for r in rows if r['sand']])) if any(r['sand'] for r in rows) else None,
                    sandwich_maxwidth=float(max([r['sand']['hi'] - r['sand']['lo'] for r in rows if r['sand'] and 'hi' in r['sand']], default=0.0)),
                    log_kappa=lk, P_miss=[float(np.mean([r['miss'][t] for r in rows])) for t in range(T)],
                    E_W_miss=EWmiss, U_ok=bool(all(EWmiss[t] <= np.exp(lk[t]) * 1.0 + 3 * np.sqrt(np.exp(2 * lk[t]) / reps) + 1e-300 for t in range(T))),
                    mean_f_endT=float(np.mean([r['f_endT'] for r in rows])), TV_nubar_pi=TV,
                    bias_max=float(np.abs(pip_mean - pip_exact).max()), mean_err_post=float(np.mean([r['err_post'] for r in rows])),
                    delta1=setting['delta1'])
        out.write(json.dumps(summ) + '\n'); out.flush()
        print(gname, T, 'medlogW=%.3f' % summ['median_logW'], 'pred2=', summ['two_state_pred'],
              'sand %d/%d' % (summ['sandwich_ok'], summ['sandwich_applicable']), 'U_ok', summ['U_ok'],
              'TV=%.4f bias=%.4f' % (TV, summ['bias_max']), flush=True)
    print('done %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
