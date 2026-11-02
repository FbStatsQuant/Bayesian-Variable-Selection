"""
Task 4: per-round progress probability (actual round, exact scores, Monte Carlo over orders and draws) versus
the proven constants: c2 (Prop. B2), P* (Lemma P), c_poly (Lemma P, D = optimal top-q set), 1/(B+3) floor,
and for incomplete starts c1 (Prop. B1).
For each design (S1-S6, c in {1, .5}, n = 200, p = 20):
  - phase 2: the state W in S_a (a = 1, 2) with the smallest P*; and the most pi0-probable superset start;
  - phase 1: the most pi0-probable incomplete start.
Simulation: 20000 single rounds per state, seed 11 + design index.
"""
import sys, json, math
import numpy as np
from bvs_engine import *
from round_analysis import classify, pstar, cpoly, IndTables
from progress_bounds import phase2_B, phase1_B
from simulate import simulate

REPS = 20000


def one_round_stats(M, x, inR, V, rng):
    r = simulate(M, np.full(REPS, x, dtype=np.int64), 1, REPS, rng, inR, V)
    prog = r['prog'][0]; inc = r['incr'][0] | r['exit'][0]
    sc = r['first'] == 0
    return dict(p_progress=float(prog.mean()), p_prog_or_bad=float((prog | inc).mean()),
                p_scored=float(sc.mean()), se=float(math.sqrt(max(prog.mean() * (1 - prog.mean()), 1e-12) / REPS)))


def main(outp):
    res = []
    k = 0
    for scen in [1, 2, 3, 4, 5, 6]:
        for c in [1.0, 0.5]:
            k += 1
            rng = np.random.default_rng(11 + k)
            X, y, S0, b = gen_design(scen, p=20, n=200, c=c, seed=1)
            M = Model(X, y, S0)
            inR, V, miss, extra = region_arrays(M, 20, 4)
            T = IndTables(M, inR, V)
            rec = dict(scen=scen, c=c, floor=1 / (M.B + 3), phase2=[], phase1=None)
            allidx = np.arange(1 << M.p, dtype=np.int64)
            for a in [1, 2]:
                b2 = phase2_B(M, a)
                fam = np.nonzero(((allidx & S0) == S0) & (extra <= a) & (allidx != S0))[0]
                best = None
                for x in fam:
                    st, bt, inc, ex = classify(M, int(x), inR, V, T)
                    v = pstar(st, bt)
                    if best is None or v < best[0]:
                        best = (v, int(x), cpoly(st, bt))
                sim = one_round_stats(M, best[1], inR, V, rng)
                rec['phase2'].append(dict(a=a, c2=b2['c2'], epsdel=b2['epsdel'], Hmax=b2['Hmax'], eta2=b2['eta2'],
                                          worst_state=[j for j in range(M.p) if best[1] >> j & 1],
                                          pstar=best[0], cpoly=best[2], sim=sim))
            # most probable superset start (any a) and incomplete start under pi0
            order = np.argsort(-M.pi0)
            xs = next(int(x) for x in order if (int(x) & S0) == S0 and int(x) != S0)
            st, bt, inc, ex = classify(M, xs, inR, V, T)
            rec['pi0_superset_start'] = dict(x=[j for j in range(M.p) if xs >> j & 1], pi0=float(M.pi0[xs]),
                                             pstar=pstar(st, bt), sim=one_round_stats(M, xs, inR, V, rng))
            xi = next((int(x) for x in order if (int(x) & S0) != S0), None)
            if xi is not None and M.pi0[xi] > 1e-6:
                b1 = phase1_B(M, xi)
                st, bt, inc, ex = classify(M, xi, inR, V, T)
                rec['phase1'] = dict(x=[j for j in range(M.p) if xi >> j & 1], pi0=float(M.pi0[xi]), c1=b1['c1'],
                                     eta1=b1['eta1'], a=b1['a'], pstar=pstar(st, bt), cpoly=cpoly(st, bt),
                                     sim=one_round_stats(M, xi, inR, V, rng))
            res.append(rec)
            print(json.dumps(rec, default=float), flush=True)
            json.dump(res, open(outp, 'w'), indent=1, default=float)


if __name__ == '__main__':
    main(sys.argv[1])
