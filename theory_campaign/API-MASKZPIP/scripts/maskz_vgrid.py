"""API-MASKZPIP: final-run evidence with a METHOD-LIKE candidate set V (METHODOLOGY_v3 §6.6-6.7), p = 18.

Pilot (§6.6): H particles iid pi0; next phi = largest phi' with particle ESS of e^{(phi'-phi)d} >= 0.9 H (60 halvings),
floor 1/T_e (T_e = 1000); multinomial resampling; one engine round at phi'. "Scored" set := every state occupied
during the pilot plus all single-flip neighbours of every occupied state (proxy for SR: both Gibbs configurations
are scored). V := top 20p scored by log gamma0  U  top 20p scored by log gamma1  U  {empty}  (§6.7).
Grid: restricted-ESS bisection on V from u = 0 (bvs: masked_sim.restricted_grid; pilot targets omitted, they only add
points). One rebuild is NOT done (single construction). Final run: N particles, 4 islands per rep.
Compared with: blind V0 = distinct states of N iid pi0 draws (F-MASKPIP G3).
Usage: python maskz_vgrid.py design n N reps outfile
"""
import sys, os, json, time
import numpy as np
from scipy.special import logsumexp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendor'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bvs_exact import Problem
from masked_sim import design, DESIGNS, restricted_grid
from maskz_check import CSim


def pilot(sim, H, Te, rng):
    pr = sim.pr
    S = sim.draw0(H, rng)
    occ = set(np.unique(S).tolist())
    phi, phis = 0.0, [0.0]
    while phi < 1.0:
        def ess_ok(v):
            lw = (v - phi) * pr.d[S]
            return 2 * logsumexp(lw) - logsumexp(2 * lw) >= np.log(0.9 * H)
        if ess_ok(1.0):
            v = 1.0
        else:
            lo, hi = phi, 1.0
            for _ in range(60):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if ess_ok(mid) else (lo, mid)
            v = max(lo, min(1.0, phi + 1.0 / Te))
        lw = (v - phi) * pr.d[S]
        prob = np.exp(lw - logsumexp(lw))
        S = S[np.searchsorted(np.cumsum(prob) / prob.sum(), rng.random(H), side='right').clip(0, H - 1)]
        S = sim.round(S, v, rng)
        occ |= set(np.unique(S).tolist())
        phi = v; phis.append(v)
    for _ in range(pr.L + 4):
        S = sim.round(S, 1.0, rng)
        occ |= set(np.unique(S).tolist())
    occ = np.array(sorted(occ), dtype=np.int64)
    nb = (occ[:, None] ^ (1 << np.arange(pr.p))[None, :]).ravel()
    scored = np.unique(np.concatenate([occ, nb]))
    scored = scored[pr.feas[scored]]
    return phis, scored


def main():
    name, n, N, reps, outfile = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    di = DESIGNS.index(name)
    t0 = time.time()
    X, y, S0 = design(name, n, np.random.default_rng(1000 * di + 0 + 7919 * n))
    pr = Problem(X, y, S0)
    sim = CSim(pr)
    s0 = pr.S0
    lpi = pr.lg1 - logsumexp(pr.lg1)
    out = open(outfile, 'w')
    for prep in range(3):                                   # three independent pilots -> three grids
        rng = np.random.default_rng(9 * 10 ** 6 + 7919 * n + 100 * di + prep)
        phis, scored = pilot(sim, N, 1000, rng)
        k = 20 * pr.p
        top0 = scored[np.argsort(-pr.lg0[scored])[:k]]
        top1 = scored[np.argsort(-pr.lg1[scored])[:k]]
        V = np.unique(np.concatenate([top0, top1, [0]]))
        grid = restricted_grid(pr, V)
        V0 = np.unique(sim.draw0(N, rng))
        grid0 = restricted_grid(pr, V0)
        for gname, g, VV in [('Vmethod', grid, V), ('Vblind', grid0, V0)]:
            lWs = []
            for rep in range(reps):
                lW, pops, endT, pip = sim.island(g, N, pr.L, rng)
                lWs.append(lW)
            lWs = np.array(lWs)
            row = dict(design=name, n=n, N=N, pilot=prep, grid_name=gname, T=len(g) - 1, pilot_T=len(phis) - 1,
                       S0_in_V=bool(np.any(VV == s0)), V_size=int(len(VV)), pi_V=float(np.exp(logsumexp(lpi[VV]))),
                       median_logW=float(np.median(lWs)), q05=float(np.quantile(lWs, .05)),
                       q95=float(np.quantile(lWs, .95)), grid=[float(v) for v in g])
            out.write(json.dumps(row) + '\n'); out.flush()
            print(name, n, prep, gname, 'T=%d S0inV=%s piV=%.3f medlogW=%.3f [%.3f, %.3f]' % (
                row['T'], row['S0_in_V'], row['pi_V'], row['median_logW'], row['q05'], row['q95']), flush=True)
    print('done %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
