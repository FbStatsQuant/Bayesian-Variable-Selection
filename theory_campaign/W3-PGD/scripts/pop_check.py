"""Population-level check of PGD / GERC / TRC for the study's scenarios S1-S6 (p = 500, 1000; s0 = 14).

Population design: rows of raw X ~ N(0, Sigma), Sigma = scenario_covariance (unit diagonal), theta = c*beta
(the generator forms the signal on the standardised X, so theta* = c*beta exactly).
PGD's ratio R0/R+ is invariant to the scale c; the finite-n population-score margin (n = 200) is not.

Candidate column sets (exact reductions, see PROOF.md Prop P2 and §N1):
  S1, S3, S4, S6 (block orthogonal, BO): the 14 truth groups (70 columns) + one null from a pure-null group.
      Every other null is orthogonal to all of these, so its add/swap reductions are 0 and as an extra it
      changes nothing: exact.
  S5 (one factor + groups): 70 truth-group columns + 3 complete pure-null groups (15 columns).  All pure-null
      groups are exchangeable given the truths, so with <= 2 extras any further null is equivalent to a
      member of an included pure-null group: exact.
  S2 (AR(1), rho = .5, truths 35 apart): windows of +-W columns around each truth (W = 10). Columns outside
      have |corr| <= .5^11 ~ 5e-4 with every truth: APPROXIMATE (truncation), flagged.
Regions: R_{14,0} (all subsets of S0), R_{14,1} (one extra among the candidate nulls; S2: nulls within +-3),
         R_{3,2} (<= 3 missing truths, <= 2 extras).
Outputs (results/pop_check.json): eta = 1 - max R0/R+ over states with m >= 1, the binding move type and
state, max GERC, min TRC, and for c in {1, .5} the n = 200 population-score margin quantiles.
Seed: none needed (deterministic).
"""
import json, sys, time
import numpy as np
from pgd_core import Engine, scenario_covariance, truth, region_batches, region_size, TYPE_NAMES


def candidate_set(scen, p, W=10):
    act, beta = truth(p)
    groups = act // 5
    if scen in (1, 3, 4, 6):
        cols = sorted(set(int(5 * g + k) for g in groups for k in range(5)))
        free = next(x for x in range(p) if x // 5 not in set(groups))
        cols = sorted(cols + [free]); exact = True
    elif scen == 5:
        cols = set(int(5 * g + k) for g in groups for k in range(5))
        pure = [g for g in range(p // 5) if g not in set(groups)][:3]
        cols |= set(5 * g + k for g in pure for k in range(5))
        cols = sorted(cols); exact = True
    else:
        cols = sorted(set(int(x) for a in act for x in range(max(0, a - W), min(p, a + W + 1))))
        exact = False
    return np.array(cols), act, beta, exact


def run(scen, p, regions, want_erc=True):
    cols, act, beta, exact = candidate_set(scen, p)
    Sig = scenario_covariance(scen, p)[np.ix_(cols, cols)]
    pos = {c: i for i, c in enumerate(cols)}
    tp = np.array([pos[a] for a in act])
    res = dict(scenario=scen, p=p, n_candidates=len(cols), exact_reduction=exact, regions={})
    for (a, d, extras_rule) in regions:
        if extras_rule == 'all':
            extras = [i for i in range(len(cols)) if i not in set(tp)]
        else:  # near: within +-3 of a truth (S2)
            extras = [i for i, c in enumerate(cols) if i not in set(tp) and min(abs(c - act)) <= 3]
        rec = {}
        for cc in (1.0, 0.5):
            th = np.zeros(len(cols)); th[tp] = cc * beta
            E = Engine(Sig, th, tp, n=200, sigma2=1.0, p_prior=p)
            t0 = time.time()
            worst = (-np.inf, None, None); gerc = -np.inf; trc = np.inf; margins = []; nst = 0
            ms = []
            types = {}
            for idx in region_batches(tp, extras, a, d, batch=3000, amin=1):
                o = E.batch(idx, want_erc=(want_erc and cc == 1.0), want_fbar=True)
                ratio = o['R0'] / o['Rp']
                k = int(np.argmax(ratio))
                if ratio[k] > worst[0]:
                    worst = (float(ratio[k]), [int(cols[x]) for x in idx[k]], TYPE_NAMES[int(o['R0_type'][k])])
                for t in o['R0_type'][ratio > 0.9 * max(worst[0], 0)]:
                    types[TYPE_NAMES[int(t)]] = types.get(TYPE_NAMES[int(t)], 0) + 1
                if 'GERC' in o:
                    gerc = max(gerc, float(o['GERC'].max()))
                trc = min(trc, float(o['TRC'].min()))
                margins.append(o['Fbar_margin']); ms.append(o['m']); nst += len(idx)
            mg = np.concatenate(margins); mm = np.concatenate(ms)
            by_m = {int(k): [float(np.mean(mg[mm == k] > 0)), float(mg[mm == k].min())] for k in np.unique(mm)}
            rec[f'c={cc}'] = dict(states=nst, eta=1 - worst[0], max_ratio=worst[0], worst_state=worst[1],
                                 worst_type=worst[2], near_worst_types=types,
                                 GERC_max=(gerc if cc == 1.0 and want_erc else None), TRC_min=trc,
                                 fbar_margin_q=[float(np.quantile(mg, q)) for q in (0, .01, .05, .25, .5)],
                                 fbar_frac_pos=float(np.mean(mg > 0)), fbar_by_m_fracpos_min=by_m, secs=round(time.time() - t0, 1))
            print(scen, p, (a, d), cc, {k: v for k, v in rec[f'c={cc}'].items() if k not in ('worst_state',)}, flush=True)
        res['regions'][f'R_{a},{d}'] = rec
    return res


if __name__ == '__main__':
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    scens = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1, 2, 3, 4, 5, 6]
    out = []
    for s in scens:
        rule = 'near' if s == 2 else 'all'
        regions = [(14, 0, rule), (14, 1, rule), (3, 2, rule)]
        out.append(run(s, p, regions))
        json.dump(out, open(f'../results/pop_check_p{p}.json', 'w'), indent=1)
