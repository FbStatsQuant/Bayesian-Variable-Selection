"""
Driver: per design (scenario S1-S6, scale c, n), compute exact constants and simulated round behaviour.
Usage: python3 run_designs.py OUT.json n [scen,...] [c,...] [reps]
Fixed seeds: design seed 1 (numpy default_rng), simulation seed 20261102 + 100*scen + int(10*c).
"""
import sys, json, math, time
import numpy as np
from bvs_engine import *
from progress_bounds import phase2_B, phase1_B, binom_lt
from round_analysis import classify, pstar, cpoly, IndTables
from simulate import simulate


def design_summary(scen, c, n, reps=3000, H=None, p=20, nphase1=12, amax=4):
    X, y, S0, b = gen_design(scen, p=p, n=n, c=c, seed=1)
    M = Model(X, y, S0)
    L = max(4, math.ceil(math.log2(n + 1)))
    H = L + 4 if H is None else H
    out = dict(scen=scen, c=c, n=n, p=p, B=M.B, m=M.m_labels, H=H,
               pi_S0=float(np.exp(M.logpi[S0])), pi0_S0=float(M.pi0[S0]),
               blocks=M.blocks, S0=[int(j) for j in range(p) if S0 >> j & 1])
    inR, V, miss, extra = region_arrays(M, 20, 4)
    # phase-2 constants
    out['phase2'] = []
    for a in range(1, amax + 1):
        r = phase2_B(M, a); r.pop('eta_parts')
        out['phase2'].append(r)
    # exact first-change progress P* over the superset families (min) for a = 1..amax
    T = IndTables(M, inR, V)
    allidx = np.arange(1 << p, dtype=np.int64)
    sup = ((allidx & S0) == S0) & (extra <= amax) & (allidx != S0)
    ps = []
    for x in allidx[sup]:
        st, bt, inc, ex = classify(M, int(x), inR, V, T)
        ps.append((int(extra[x]), pstar(st, bt), cpoly(st, bt)))
    ps = np.array(ps)
    out['pstar_superset'] = {int(a): dict(min=float(ps[ps[:, 0] <= a, 1].min()), min_cpoly=float(ps[ps[:, 0] <= a, 2].min()))
                             for a in range(1, amax + 1)}
    # starts: iid pi0 draws, not S0
    rng = np.random.default_rng(20261102 + 100 * scen + int(10 * c) + n)
    starts = np.searchsorted(np.cumsum(M.pi0), rng.random(int(reps * 1.2)) * M.pi0.sum()).astype(np.int64)
    starts = starts[starts != S0][:reps]
    out['start_comp'] = dict(mean_miss=float(miss[starts].mean()), mean_extra=float(extra[starts].mean()),
                             frac_superset=float((miss[starts] == 0).mean()))
    # phase-1 constants for a few incomplete starts (most pi0-probable distinct)
    inc_states = [int(x) for x in np.argsort(-M.pi0) if (int(x) & S0) != S0 and int(x) != S0][:nphase1]
    out['phase1'] = []
    for x in inc_states:
        if M.pi0[x] < 1e-4:
            break
        r1 = phase1_B(M, x); r1.pop('parts')
        st, bt, inc, ex = classify(M, x, inR, V, T)
        r1.update(x=[j for j in range(p) if x >> j & 1], pi0=float(M.pi0[x]), pstar=pstar(st, bt),
                  miss=int(miss[x]), extra=int(extra[x]))
        r1['A'] = [j for j in range(p) if r1['A'] >> j & 1]
        out['phase1'].append(r1)
    # simulation
    t = time.time()
    res = simulate(M, starts, H, len(starts), rng, inR, V)
    f = res['first']
    out['sim'] = dict(reps=int(len(starts)),
                      scored_by_round=[float(((f >= 0) & (f <= h)).mean()) for h in range(H)],
                      progress_round1=float(res['prog'][0].mean()),
                      progress_rate_while_unscored=float(np.mean([res['prog'][h][(f < 0) | (f >= h)].mean()
                                                                   for h in range(min(H, 3))])),
                      incr_round1=float(res['incr'][0].mean()),
                      time=time.time() - t)
    # simulated per-round progress from the worst superset states for P* (a<=2)
    return out


if __name__ == '__main__':
    outp = sys.argv[1]; n = int(sys.argv[2])
    scens = [int(s) for s in sys.argv[3].split(',')] if len(sys.argv) > 3 else [1, 2, 3, 4, 5, 6]
    cs = [float(s) for s in sys.argv[4].split(',')] if len(sys.argv) > 4 else [1.0, 0.5]
    reps = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
    allres = []
    for s in scens:
        for c in cs:
            t = time.time()
            r = design_summary(s, c, n, reps=reps)
            r['wall'] = time.time() - t
            allres.append(r)
            print('S%d c=%.2f n=%d done %.0fs  c2(a=1)=%.3f eta2(a=1)=%.3f  P*min(a=1)=%.3f sim r1=%.3f' % (
                s, c, n, r['wall'], r['phase2'][0]['c2'], r['phase2'][0]['eta2'], r['pstar_superset'][1]['min'],
                r['sim']['scored_by_round'][0]), flush=True)
            json.dump(allres, open(outp, 'w'), indent=1, default=float)
