"""Local falsification of L8; 8 seed values, p=6 exhaustive enumeration.
No imports of other tickets; no artifacts outside N9*. Run with Python+NumPy.
Numerical evidence does not establish asymptotic assertions.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import json
import math
from pathlib import Path
import numpy as np


def standardize(a):
    a = a - a.mean(axis=0)
    return a / np.sqrt(np.sum(a*a, axis=0)/(a.shape[0]-1))


def check(seed, n, rho, masked=False):
    rng = np.random.default_rng(seed)
    p = 6
    raw = np.sqrt(rho)*rng.normal(size=(n, 1)) + np.sqrt(1-rho)*rng.normal(size=(n,p))
    X = standardize(raw)
    theta = np.array([1., -2. if masked else .7, 0, 0, 0, 0])
    eps = rng.normal(size=n)
    Y = X@theta + eps-eps.mean()
    y = standardize(Y)
    G, z = X.T@X, X.T@y
    R = G/(n-1)
    scores, lms, omegas, identity_errors = {}, {}, [], []
    lw = lambda k: -math.log(2)-math.log(math.comb(2*p-1, k))
    for mask in range(1 << p):
        ids = [j for j in range(p) if mask >> j & 1]
        k = len(ids)
        if not ids:
            q, determinant, rss = n-1., 0., n-1.
        else:
            g = G[np.ix_(ids, ids)]
            zz = z[ids]
            h = (n+1)*g+np.eye(k)
            q = n-1 - n*zz@np.linalg.solve(h, zz)
            determinant = .5*(np.linalg.slogdet(h)[1]-np.linalg.slogdet(g+np.eye(k))[1])
            coef = np.linalg.solve(g, zz)
            rss = np.sum((y-X[:,ids]@coef)**2)
            beta = n*np.linalg.solve(h, zz)
            fit = X[:,ids]@beta
            q_nonnegative = np.sum((y-fit)**2)+(fit@fit+beta@beta)/n
            identity_errors.append(abs(q-q_nonnegative))
        omegas.append(q-rss)
        lm = -determinant-(n/2+.01)*np.log(.02+q)
        lms[mask], scores[mask] = float(lm), float(lm+lw(k))
    truth = 3
    deltas = []
    for T in range(1 << p):
        if T & truth != truth:
            continue
        for i in (0,1):
            A = T ^ (1 << i)
            deltas.append(scores[A]-scores[T])
            for j in range(p):
                if not T >> j & 1:
                    deltas.append(scores[A | (1 << j)]-scores[T])

    # Partition selection uses X only; noise is never used in its selection.
    null_rank = sorted(range(2,p), key=lambda j: (-abs(R[0,j]), j))
    layouts = {
        'singletons': [[j] for j in range(p)],
        'truths_spread': [[0,2,3], [1,4,5]],
        'X_selected_truth_block': [[0,1]+null_rank[:2]]+[[j] for j in null_rank[2:]],
    }
    starts = []
    for name, blocks in layouts.items():
        bm = [sum(1 << j for j in b) for b in blocks]
        N0 = 0
        for b in bm:
            if b & truth == truth:
                N0 |= b & ~truth
        expected = ((1 << p)-1) ^ N0
        js = [lw(S.bit_count())+sum(lms[S & b]-lms[0] for b in bm) for S in range(1 << p)]
        order = sorted(range(1 << p), key=lambda S: (-js[S],S))
        starts.append(dict(layout=name, blocks=blocks, N0_mask=N0,
                           expected_mask=expected, observed_mask=order[0],
                           matches=order[0]==expected,
                           best_minus_second=float(js[order[0]]-js[order[1]]),
                           expected_minus_best_other=float(js[expected]-max(v for S,v in enumerate(js) if S!=expected))))
    pe = X@np.linalg.solve(G, X.T@(eps-eps.mean()))
    return dict(seed=seed,n=n,p=p,rho=rho,masked=masked,
                within_locked_dimension=p<=n**.24,
                gram_floor=float(np.linalg.eigvalsh(R)[0]),
                projected_noise_energy=float(pe@pe),
                max_truth_move=float(max(deltas)),
                max_truth_move_over_n=float(max(deltas)/n),
                truth_move_violation=max(deltas)>=0,
                ridge_omega_min=float(min(omegas)),ridge_omega_max=float(max(omegas)),
                nonnegative_Q_identity_max_error=float(max(identity_errors)), starts=starts)


def main():
    rows = [check(seed,n,rho) for seed in range(8) for n in (256,4096) for rho in (.4,.98)]
    # Deliberately outside FS: rho=.5, theta=(1,-2), c(empty,truth 0)=0.
    # Singleton partition exposes the cancellation, testing necessity of visibility.
    bad = [check(seed,4096,.5,True) for seed in range(8)]
    result = dict(status='Local falsification only; not an independent proof review',
                  seeds=list(range(8)),seed_count=8,
                  score='Exact D0 formulas, independently implemented in NumPy; not a production binary test',
                  exhaustive_p=6, rows=rows, FS_violating_masked_cases=bad,
                  summary=dict(target_truth_move_violations=sum(r['truth_move_violation'] for r in rows),
                    target_start_misses=sum(not s['matches'] for r in rows for s in r['starts']),
                    target_start_checks=sum(len(r['starts']) for r in rows),
                    masked_singleton_excludes_truth0=sum(not (r['starts'][0]['observed_mask'] & 1) for r in bad),
                    max_Q_identity_error=max(r['nonnegative_Q_identity_max_error'] for r in rows+bad)))
    Path(__file__).with_name('N9_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['summary'],indent=2))


if __name__ == '__main__':
    main()
