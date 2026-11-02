"""Population PGD on the study's designs (gen_dev_data.R: scenario_covariance, truth; theta = c*beta, PGD is
invariant to c).  Deterministic.  Writes results/study_pop.json and results/eta_block.txt.

Part A (S1, S3, S4, S6; block-orthogonal at population level, one truth per group of 5, D = the 56 mates):
  eta*(d), d = 1, 2, 3, by (i) Cor P2' closed form, (ii) direct enumeration of (B1)-(B3) on Sigma,
  (iii) brute-force scan of PGD on R_{a,d}(D) over an exact reduced column set (the 70 truth-group columns + one
  pure-null representative: every other null is orthogonal to all of them, so its add/swap reductions equal
  those of the representative).  (iii) for (a,d) in {(1,1),(2,1),(1,2),(2,2),(1,3)}.
Part B (S2 AR(1), S5 common factor; not block-orthogonal): PGD, GERC (on R_{3,2}(D)) and TRC on R_{2,2}(D) with
  D = the 56 mates; S5 on the exact reduction 70 + 1 pure null (pure-null groups are exchangeable given any state
  without pure nulls); S2 on all 500 columns (no reduction).
Part C (p = 30, the generator's small configuration, s0 = 5): all six scenarios, D = ALL nulls, R_{2,2}, exact.
"""
import json, sys, time
import numpy as np
from popcheck import scenario_covariance, truth, mates, scan
from check_P2_bruteforce import eta_B123, eta_formula

out = {}
lines = []


def reduced(scen, p):
    act, beta = truth(p)
    mt = mates(act, p)
    tg = set(int(a) // 5 for a in act)
    pure = next(x for x in range(p) if x // 5 not in tg)
    cols = sorted(set(map(int, act)) | set(mt) | {pure})
    pos = {c: i for i, c in enumerate(cols)}
    Sig = scenario_covariance(scen, p)[np.ix_(cols, cols)]
    th = np.zeros(len(cols)); th[[pos[int(a)] for a in act]] = beta
    return Sig, th, [pos[int(a)] for a in act], [pos[m] for m in mt], cols


def group_rhos(scen, act):
    g = np.array(act) // 5 + 1
    if scen == 1: return [0.0] * len(act)
    if scen == 3: return [0.7] * len(act)
    if scen == 4: return [0.85] * len(act)
    if scen == 6: return list(0.4 + 0.1 * ((g - 1) % 6))


p = 500
which = sys.argv[1] if len(sys.argv) > 1 else 'ABC'
if 'A' in which:
    for scen in (1, 3, 4, 6):
        act, beta = truth(p)
        Sig, th, tp, mp, cols = reduced(scen, p)
        groups = {}; truth_of = {}
        for i, cidx in enumerate(cols):
            groups.setdefault(cidx // 5, []).append(i)
        for g, mem in groups.items():
            tt = [i for i in mem if i in tp]
            truth_of[g] = tt[0] if tt else None
        rec = {}
        for d in (1, 2, 3):
            ef = eta_formula(group_rhos(scen, act), list(beta), 5, d)
            eb = eta_B123(Sig, th, groups, truth_of, set(mp), d)
            rec[f'd={d}'] = dict(formula=ef, B123=eb)
        for (a, d) in ((1, 1), (2, 1), (1, 2), (2, 2), (1, 3)):
            t0 = time.time()
            sc = scan(Sig, th, tp, mp, a, d)
            rec[f'scan a={a} d={d}'] = dict(eta=sc['eta'], states=sc['states'], binding=sc['worst_type'],
                                            worst=[cols[i] for i in sc['worst']], trc_min=sc['trc_min'], secs=round(time.time() - t0, 1))
        out[f'S{scen}'] = rec
        ln = f"S{scen}: " + "; ".join(f"d={d}: formula {rec[f'd={d}']['formula']:.4f}, (B1-B3) {rec[f'd={d}']['B123']:.4f}" for d in (1, 2, 3))
        ln += " | scan: " + "; ".join(f"R_{{{a},{d}}} {rec[f'scan a={a} d={d}']['eta']:.4f} ({rec[f'scan a={a} d={d}']['binding']})" for (a, d) in ((1, 1), (2, 1), (1, 2), (2, 2), (1, 3)))
        print(ln, flush=True); lines.append(ln)
        json.dump(out, open('../results/study_pop_A.json', 'w'), indent=1)

if 'B' in which:
    for scen in (5, 2):
        act, beta = truth(p)
        if scen == 5:
            Sig, th, tp, mp, cols = reduced(5, p)
        else:
            cols = list(range(p)); Sig = scenario_covariance(2, p)
            th = np.zeros(p); th[act] = beta; tp = list(map(int, act)); mp = mates(act, p)
        t0 = time.time()
        sc = scan(Sig, th, tp, mp, 2, 2, gerc_a=3, verbose=True)
        rec = dict(eta=sc['eta'], states=sc['states'], binding=sc['worst_type'], worst=[cols[i] for i in sc['worst']],
                   trc_min=sc['trc_min'], trc_state=[cols[i] for i in sc['trc_state']] if sc['trc_state'] else None,
                   gerc_max=sc['gerc_max'], gerc_state=[cols[i] for i in sc['gerc_state']] if sc['gerc_state'] else None,
                   rho_plus_min=sc['rho_plus_min'], secs=round(time.time() - t0, 1), columns=len(cols))
        out[f'S{scen}'] = rec
        ln = (f"S{scen} (p=500, R_{{2,2}}(D), {len(cols)} cols): eta_hat={rec['eta']:.4f} binding {rec['binding']} at {rec['worst']}; "
              f"TRC_min={rec['trc_min']:.4f}; GERC_max(R_{{3,2}})={rec['gerc_max']:.4f} => GERC eta1={1 - rec['gerc_max'] ** 2:.4f}")
        print(ln, flush=True); lines.append(ln)
        json.dump(out, open('../results/study_pop_B.json', 'w'), indent=1)

if 'C' in which:
    p30 = 30
    for scen in range(1, 7):
        act, beta = truth(p30)
        Sig = scenario_covariance(scen, p30); th = np.zeros(p30); th[act] = beta
        nulls = [x for x in range(p30) if x not in set(act)]
        sc = scan(Sig, th, list(map(int, act)), nulls, 2, 2, gerc_a=3)
        rec = dict(eta=sc['eta'], binding=sc['worst_type'], worst=sc['worst'], trc_min=sc['trc_min'], gerc_max=sc['gerc_max'], states=sc['states'])
        if scen in (1, 3, 4, 6):
            rec['formula_d2'] = eta_formula(group_rhos(scen, act), list(beta), 5, 2)
        out[f'p30 S{scen}'] = rec
        ln = (f"p=30 S{scen} (D = all nulls, R_{{2,2}}): eta_hat={rec['eta']:.4f} ({rec['binding']}); TRC_min={rec['trc_min']:.4f}; "
              f"GERC_max={rec['gerc_max']:.4f}" + (f"; Cor P2' formula d=2: {rec['formula_d2']:.4f}" if 'formula_d2' in rec else ''))
        print(ln, flush=True); lines.append(ln)
        json.dump(out, open('../results/study_pop_C.json', 'w'), indent=1)

open(f'../results/study_pop_{which}.txt', 'w').write('\n'.join(lines) + '\n')
