"""n = 200 check of the W3-PGD conditions on realised designs, and greedy-path margins.

Designs: Python re-implementation of Scripts/Data_generators/gen_prod_data.R (same law, NOT the same bits: R's RNG
is not reproduced). Seed of replicate r of scenario s at p: numpy default_rng(base_p + 10000 s + r) with
base_500 = 1410000, base_1000 = 1510000 (the R seeds, reused as numpy seeds).  y = c X beta + eps, c in {1, .5}.

Per dataset we compute
  design side (realised R = X'X/(n-1), theta = c beta, all p columns):
    eta_hat(R_{14,0}), eta_hat(R_{2,1}) = 1 - max R0/R+ (sample PGD), binding move types; GERC on R_{14,0};
    TRC min; anchored SE: min lambda_min(R_{S0 u J}) over |J| <= 2; LD-flat level rho1 = max |pcorr(l, e | S0)| over
    null pairs that are not neighbours (neighbours: same 5-group; S2: |l - e| <= 3);
    finite-n population-score margins (Fbar) on R_{2,1}.
  noise side (actual y, exact score F of 00_COMMON via td_core.Scorer):
    (L) S0 strict local max?  null-addition margin c_{s0} - max_l [F(S0+l) - F(S0) + c_{s0}] etc.;
    superset states S0+e (all e): D_S holds?  (Theorem W (H1) event);
    greedy paths from centres: all S0-j (14), 40 random S0+e, 40 random R_{2,1}, 40 random R_{14,0} with m in 3..6;
    per step: actual margin F(best progress) - max(F(S), F(best non-progress)), Fbar margin, move class;
    per path: reached S0 with local_certified within ell = 10 moves (production cap) / uncapped (<= 30).
Output: results/n200_p{p}_S{s}.json
"""
import json, sys, time
import numpy as np
from pgd_core import Engine, scenario_covariance, truth, gen_design, region_batches, TYPE_NAMES
from td_core import Scorer, classify

BASE = {500: 1410000, 1000: 1510000}


def lambda_min_anchored(R, tp, others, maxJ=2):
    S0 = list(tp); out = np.linalg.eigvalsh(R[np.ix_(S0, S0)])[0]
    o = np.array(others)
    # |J| = 1
    for l in o:
        I = S0 + [int(l)]
        out = min(out, np.linalg.eigvalsh(R[np.ix_(I, I)])[0])
    if maxJ >= 2:
        pairs = np.array([(a, b) for i, a in enumerate(o) for b in o[i + 1:]])
        for ch in np.array_split(pairs, max(1, len(pairs) // 4000)):
            idx = np.column_stack([np.tile(S0, (len(ch), 1)), ch])
            M = R[idx[:, :, None], idx[:, None, :]]
            out = min(out, np.linalg.eigvalsh(M)[:, 0].min())
    return float(out)


def ld_level(R, tp, nulls, nbr):
    """max |pcorr(l, e | S0)| over null pairs with e not a neighbour of l."""
    S0 = list(tp)
    A = R[np.ix_(nulls, S0)]
    Rc = R[np.ix_(nulls, nulls)] - A @ np.linalg.solve(R[np.ix_(S0, S0)], A.T)
    d = np.sqrt(np.diag(Rc)); P = Rc / np.outer(d, d)
    np.fill_diagonal(P, 0)
    mask = np.array([[nbr(a, b) for b in nulls] for a in nulls])
    P[mask] = 0
    return float(np.abs(P).max())


def margins_at(sc, S, S0set):
    """actual-score margin at state S and the greedy move class."""
    moves, gains = sc.scan(S)
    F0 = 0.0
    prog = [g for mv, g in zip(moves, gains) if classify(mv, S0set)[0] + classify(mv, S0set)[1] < 0]
    non = [g for mv, g in zip(moves, gains) if classify(mv, S0set)[0] + classify(mv, S0set)[1] >= 0]
    bp = max(prog) if prog else -np.inf
    bn = max([F0] + non)
    t = int(np.argmax(gains)) if len(gains) else None
    cls = None if t is None or gains[t] <= 0 else (sum(classify(moves[t], S0set)) < 0)
    return bp - bn, cls


def run(p, s, rep, c):
    t0 = time.time()
    act, beta = truth(p); tp = np.sort(act); order = np.argsort(act)
    X, eps = gen_design(p, s, n=200, seed=BASE[p] + 10000 * s + rep)
    n = 200
    R = X.T @ X / (n - 1)
    th = np.zeros(p); th[act] = c * beta
    E = Engine(R, th, act, n=n, sigma2=1.0, p_prior=p)
    nulls = [x for x in range(p) if x not in set(act)]
    out = dict(p=p, scenario=s, rep=rep, c=c)
    # ---- design side
    for (a, d, erc) in ((14, 0, True), (2, 1, False)):
        worst = (-np.inf, None); gerc = -np.inf; trc = np.inf; fb = []; fbm = []
        for idx in region_batches(act, nulls, a, d, batch=600 if d else 1500, amin=1):
            o = E.batch(idx, want_erc=erc, want_fbar=True)
            ratio = o['R0'] / o['Rp']; k = int(np.argmax(ratio))
            if ratio[k] > worst[0]:
                worst = (float(ratio[k]), TYPE_NAMES[int(o['R0_type'][k])])
            if erc:
                gerc = max(gerc, float(o['GERC'].max()))
            trc = min(trc, float(o['TRC'].min())); fb.append(o['Fbar_margin']); fbm.append(o['m'])
        fb = np.concatenate(fb); fbm = np.concatenate(fbm)
        out[f'R_{a},{d}'] = dict(eta_hat=1 - worst[0], binding=worst[1], GERC=gerc if erc else None, TRC=trc,
                                 fbar_frac_pos=float(np.mean(fb > 0)),
                                 fbar_frac_pos_m1=float(np.mean(fb[fbm == 1] > 0)),
                                 fbar_q05=float(np.quantile(fb, .05)))
    if c == 1.0:
        near = [x for x in nulls if (x // 5) in set(act // 5)] if s != 2 else [x for x in nulls if min(abs(x - act)) <= 3]
        far = [x for x in nulls if x not in set(near)]
        rng = np.random.default_rng(7 + rep)
        others = near + list(rng.choice(far, 60, replace=False))
        out['SE_lambda_min_J2_subsample'] = lambda_min_anchored(R, list(act), others, maxJ=2)
        out['SE_lambda_min_J1_all'] = lambda_min_anchored(R, list(act), nulls, maxJ=1)
        if s == 2:
            nbr = lambda a, b: abs(a - b) <= 3
        else:
            nbr = lambda a, b: a // 5 == b // 5
        out['LD_rho1'] = ld_level(R, list(act), nulls, nbr)
    # ---- noise side
    yr = X @ th + eps
    y = (yr - yr.mean()); y = y / y.std(ddof=1)
    sc = Scorer(X, y)
    S0 = tuple(sorted(act.tolist())); S0set = set(S0)
    mg0, _ = margins_at(sc, S0, S0set)
    moves, gains = sc.scan(S0)
    out['L_S0_strict_local_max'] = bool(gains.max() < 0)
    out['L_best_gain_at_S0'] = float(gains.max())
    lab = [('add_null' if mv[0] == 'add' else mv[0] + ('_truth' if mv[1] in S0set else '')) for mv in moves]
    out['L_best_add_null_gain'] = float(max(g for g, l in zip(gains, lab) if l == 'add_null'))
    sup_ok = 0
    for e in nulls:
        S = tuple(sorted(S0 + (e,)))
        mg, _ = margins_at(sc, S, S0set)
        sup_ok += mg > 0
    out['H1_superset_DS_frac'] = sup_ok / len(nulls)
    # greedy paths
    rng = np.random.default_rng(1000 + 10 * rep + int(10 * c))
    centres = [tuple(x for x in S0 if x != j) for j in S0]
    centres += [tuple(sorted(S0 + (int(e),))) for e in rng.choice(nulls, 40, replace=False)]
    for _ in range(40):
        mm = rng.integers(1, 3); drop = rng.choice(S0, mm, replace=False)
        U = [x for x in S0 if x not in drop]; P = list(rng.choice(nulls, rng.integers(0, 2), replace=False))
        centres.append(tuple(sorted(U + [int(x) for x in P])))
    for _ in range(40):
        mm = rng.integers(3, 7); drop = rng.choice(S0, mm, replace=False)
        centres.append(tuple(sorted(x for x in S0 if x not in drop)))
    kinds = ['S0-j'] * 14 + ['S0+e'] * 40 + ['R21'] * 40 + ['m3to6'] * 40
    paths = []
    for cen, kd in zip(centres, kinds):
        S = cen; steps = []
        reached10 = None
        for it in range(30):
            mg, cls = margins_at(sc, S, S0set)
            idx = np.array([S], int).reshape(1, len(S))
            fbm = float(E.batch(idx, want_fbar=True)['Fbar_margin'][0]) if S != S0 else None
            steps.append((float(mg), fbm, cls, len(set(S) ^ S0set)))
            t, mv, gn = sc.best_move(S)
            if t is None:
                break
            S = mv[t][3]
            if it + 1 == 10:
                reached10 = (S == S0)
        final = S
        cert = sc.best_move(final)[0] is None
        paths.append(dict(kind=kd, phi0=len(set(cen) ^ S0set), reached=bool(final == S0 and cert),
                          moves=len(steps) - 1, all_progress=bool(all(st[2] for st in steps[:-1])),
                          steps=steps))
    out['paths'] = paths
    out['secs'] = round(time.time() - t0, 1)
    return out


if __name__ == '__main__':
    p = int(sys.argv[1]); s = int(sys.argv[2]); reps = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    res = []
    for rep in range(1, reps + 1):
        for c in (1.0, 0.5):
            r = run(p, s, rep, c)
            print(p, s, rep, c, {k: v for k, v in r.items() if k != 'paths'},
                  'reached', np.mean([q['reached'] for q in r['paths']]), flush=True)
            res.append(r)
            json.dump(res, open(f'../results/n200_p{p}_S{s}.json', 'w'))
