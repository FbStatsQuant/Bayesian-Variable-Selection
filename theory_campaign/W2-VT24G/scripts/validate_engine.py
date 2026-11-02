"""Validate ref_engine / exact_laws (W2-VT24G). Seed 11.
(1) every elementary law is pi-reversible (detailed balance) on a p = 10 design (exact, all 2^10 states);
(2) the vectorised round (ref_engine.Model.round) matches a slow sequential round that samples each label from
    the exact law dict (exact_laws), compared on the end-state distribution from 3 fixed states (TV distance).
"""
import sys, math, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import make_data, Model, mask_to_list
from exact_laws import label_laws, indep_accept

rng = np.random.default_rng(11)
X, y, S0 = make_data(5, 1.0, p=10, n=200, seed=3)
M = Model(X, y, S0)
N = 1 << M.p
logpi = M.F - M.lse
worst = 0.0; underflow = 0; real_zero = 0
for x in range(N):
    for name, law in label_laws(M, x):
        for yy, pr in law.items():
            if yy == x or pr == 0:
                continue
            back = dict(label_laws(M, yy))[name].get(x, 0.0)
            if back < 1e-280 or pr < 1e-280:
                # float64 underflow of a Gibbs conditional (|log odds| > ~37) is not a reversibility failure
                if abs(logpi[x] - logpi[yy]) > 30: underflow += 1
                else: real_zero += 1
                continue
            lhs = logpi[x] + math.log(pr); rhs = logpi[yy] + math.log(back)
            if abs(logpi[x] - logpi[yy]) < 30:
                worst = max(worst, abs(lhs - rhs))
# independence: pi(x) pi0(y) min(1, e^{d(y)-d(x)}) symmetric
for x in range(0, N, 7):
    a = indep_accept(M, x)
    for yy in range(0, N, 13):
        if yy == x:
            continue
        b = indep_accept(M, yy)[x]
        if a[yy] > 0:
            worst = max(worst, abs((logpi[x] + math.log(a[yy])) - (logpi[yy] + math.log(b))))
print('max |log detailed-balance residual| =', worst, ' underflow pairs', underflow, ' unexplained zero pairs', real_zero)


def slow_round(x):
    labs = list(range(M.m)); rng.shuffle(labs)
    for lab in labs:
        if lab < M.p:
            law = label_laws(M, x)[lab][1]
        elif lab == M.p:
            law = label_laws(M, x)[M.p][1]
        elif lab <= M.p + M.B:
            law = label_laws(M, x)[M.p + 1][1]
        else:
            a = indep_accept(M, x)
            stay = 1 - a.sum() + a[x]
            u = rng.random()
            if u < stay:
                continue
            a2 = a.copy(); a2[x] = 0
            x = int(rng.choice(N, p=a2 / a2.sum()))
            continue
        ks = list(law.keys()); ps = np.array([law[k] for k in ks]); ps /= ps.sum()
        x = int(ks[rng.choice(len(ks), p=ps)])
    return x


res = {'detailed_balance_max_resid': worst, 'underflow_pairs': underflow, 'unexplained_zero_pairs': real_zero, 'tv': []}
for x0 in [S0, S0 & ~(1 << int(mask_to_list(S0)[0])), 0b1010101]:
    R = 4000
    fast = M.round(np.full(R, x0, dtype=np.int64), rng)[0]
    slow = np.array([slow_round(x0) for _ in range(R)])
    cf = np.bincount(fast, minlength=N) / R; cs = np.bincount(slow, minlength=N) / R
    tv = 0.5 * np.abs(cf - cs).sum()
    # null reference: TV between two fast samples
    fast2 = M.round(np.full(R, x0, dtype=np.int64), rng)[0]
    tv0 = 0.5 * np.abs(cf - np.bincount(fast2, minlength=N) / R).sum()
    print('start', mask_to_list(x0), 'TV(fast,slow) =', round(tv, 4), ' TV(fast,fast) =', round(tv0, 4))
    res['tv'].append(dict(start=mask_to_list(x0), tv_fast_slow=tv, tv_fast_fast=tv0))
json.dump(res, open(sys.argv[1], 'w'), indent=1) if len(sys.argv) > 1 else None
