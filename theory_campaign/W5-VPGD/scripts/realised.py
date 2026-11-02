"""Realised-design transfer (W3-PGD Cor P6) on the study's designs, p = 500, n in {200, 800, 3200}.

Per design (Python re-implementation of gen_dev_data.R: raw rows ~ N(0, Sigma), X = scale(raw) with sd ddof=1,
signal = X beta, Y = c*signal + eps, eps ~ N(0,1); same law, NOT the same bits as R):
  eta_hat : 1 - max rho0/rho+ over R_{2,2}(D) (states missing 1-2 truths, <= 2 extras in D), D = the 56 nulls in
            the truth blocks, moves over ALL 500 columns, computed on the realised Gram R = X'X/(n-1) with theta = beta
            (PGD is invariant to c).  "PGD(eta/2)" = eta_hat >= eta_pop/2, eta_pop from results/study_pop_*.
  TD'_P   : for c in {1, 0.5}: (L) at S0 and D_S at every S in R_{2,2}(D) \\ {S0} (includes the 1,596 superset
            states S0 u P), with the exact score F of 00_COMMON (ridge, BB(1,p) prior, K = min(p, n/2)).
            Records #failing states by (m, e) and the binding comparator.
Usage: python3 realised.py <scenarios comma> <n comma> <reps> <seed0>   (seed = seed0 + 1000*scen + n + rep)
Appends one JSON line per design to results/realised.jsonl.
"""
import json, sys, time
import numpy as np
from engine import Scorer, region_states
from popcheck import scenario_covariance, truth, mates, scan


def gen(scen, p, n, rng, L):
    Xr = rng.standard_normal((n, p)) @ L.T
    X = (Xr - Xr.mean(0)) / Xr.std(0, ddof=1)
    eps = rng.standard_normal(n)
    return X, eps


def td_check(X, Y, act, D, batch=192):
    n, p = X.shape
    Yc = (Y - Y.mean(0)) / Y.std(0, ddof=1)
    Sc = Scorer(X, Yc)
    is_t = np.zeros(p, bool); is_t[act] = True
    r = Y.shape[1]
    res = [dict(L=True, fail_states=0, fail_by_me={}, binding={}, states=0) for _ in range(r)]
    by = region_states(list(map(int, act)), D, 2, 2, amin=0)
    names = ['add null', 'delete truth', 'swap truth->null', 'swap extra->null', 'swap truth->truth', 'stay']
    for s, lst in sorted(by.items()):
        for b0 in range(0, len(lst), batch):
            chunk = lst[b0:b0 + batch]
            idx = np.array([S for S, _, _ in chunk], dtype=int).reshape(len(chunk), s)
            mm = np.array([m for _, m, _ in chunk]); ee = np.array([e for _, _, e in chunk])
            o = Sc.eval(idx)
            inS = o['inS']
            tS = is_t[idx]
            for k in range(r):
                F = o['F'][:, k]
                add = np.where(inS, -np.inf, o['add'][:, :, k])
                pa = np.where(is_t[None], add, -np.inf).max(1)
                na = np.where(~is_t[None], add, -np.inf).max(1)
                cand = [na]
                prog = pa
                if s > 0:
                    de = o['del'][:, :, k]
                    prog = np.maximum(prog, np.where(~tS, de, -np.inf).max(1))
                    cand.append(np.where(tS, de, -np.inf).max(1))
                    sw = np.where(inS[:, None, :], -np.inf, o['swap'][:, :, :, k])
                    it = tS[:, :, None]; xt = is_t[None, None, :]
                    prog = np.maximum(prog, np.where(~it & xt, sw, -np.inf).max((1, 2)))
                    cand += [np.where(it & ~xt, sw, -np.inf).max((1, 2)), np.where(~it & ~xt, sw, -np.inf).max((1, 2)),
                             np.where(it & xt, sw, -np.inf).max((1, 2))]
                else:
                    cand += [np.full(len(F), -np.inf)] * 4
                cand.append(F)
                C = np.stack(cand, 1)
                non = C.max(1); arg = C.argmax(1)
                isS0 = (mm == 0) & (ee == 0)
                if isS0.any():
                    j = np.nonzero(isS0)[0][0]
                    best_nb = max(prog[j], C[j, :5].max())
                    res[k]['L'] = bool(best_nb < F[j])
                    res[k]['L_margin'] = float(F[j] - best_nb)
                fail = (prog <= non) & ~isS0
                res[k]['states'] += int((~isS0).sum())
                res[k]['fail_states'] += int(fail.sum())
                for j in np.nonzero(fail)[0]:
                    key = f"m{mm[j]}e{ee[j]}"
                    res[k]['fail_by_me'][key] = res[k]['fail_by_me'].get(key, 0) + 1
                    res[k]['binding'][names[arg[j]]] = res[k]['binding'].get(names[arg[j]], 0) + 1
    for k in range(r):
        res[k]['TD'] = bool(res[k]['L'] and res[k]['fail_states'] == 0)
    return res


if __name__ == '__main__':
    scens = [int(x) for x in sys.argv[1].split(',')]
    ns = [int(x) for x in sys.argv[2].split(',')]
    reps = int(sys.argv[3]); seed0 = int(sys.argv[4]) if len(sys.argv) > 4 else 20261102
    p = 500
    act, beta = truth(p)
    D = mates(act, p)
    Ls = {scen: np.linalg.cholesky(scenario_covariance(scen, p)) for scen in scens}
    for rep in range(reps):
        for n in ns:
            for scen in scens:
                L = Ls[scen]
                seed = seed0 + 1000 * scen + n + rep
                rng = np.random.default_rng(seed)
                X, eps = gen(scen, p, n, rng, L)
                t0 = time.time()
                R = X.T @ X / (n - 1)
                th = np.zeros(p); th[act] = beta
                sc = scan(R, th, list(map(int, act)), D, 2, 2)
                t1 = time.time()
                sig = X @ th
                Y = np.stack([1.0 * sig + eps, 0.5 * sig + eps], 1)
                td = td_check(X, Y, act, D)
                rec = dict(scen=scen, n=n, rep=rep, seed=seed, eta_hat=sc['eta'], binding=sc['worst_type'],
                           trc_min=sc['trc_min'], c1=td[0], c05=td[1], secs_pgd=round(t1 - t0, 1), secs_td=round(time.time() - t1, 1))
                with open('../results/realised.jsonl', 'a') as f:
                    f.write(json.dumps(rec) + '\n')
                print(scen, n, rep, f"eta_hat={sc['eta']:.4f}", 'TD c=1', td[0]['TD'], td[0]['fail_states'], 'c=.5', td[1]['TD'], td[1]['fail_states'], rec['secs_pgd'], rec['secs_td'], flush=True)
