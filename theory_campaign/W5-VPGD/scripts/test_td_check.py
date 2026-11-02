"""Test realised.td_check against full brute force (every neighbour scored by engine.F_direct). Seed 3.
Output: results/test_td_check.txt"""
import numpy as np
from realised import td_check
from engine import F_direct, region_states
rng = np.random.default_rng(3)
n, p = 40, 9
X = rng.standard_normal((n, p)); X[:, 1] += 0.8 * X[:, 0]; X = (X - X.mean(0)) / X.std(0, ddof=1)
act = np.array([0, 4]); th = np.zeros(p); th[act] = [1.0, -0.7]
Y = np.stack([X @ th + rng.standard_normal(n), 0.3 * X @ th + rng.standard_normal(n)], 1)
D = [1, 2, 5]
res = td_check(X, Y, act, D)
Yc = (Y - Y.mean(0)) / Y.std(0, ddof=1)
T = set(act.tolist()); out = []
for k in range(2):
    y = Yc[:, k]; fails = 0; L = True
    for s, lst in region_states([0, 4], D, 2, 2).items():
        for S, m, e in lst:
            S = frozenset(S); FS = F_direct(X, y, sorted(S)); prog = []; non = []
            for x in range(p):
                if x in S: continue
                (prog if x in T else non).append(F_direct(X, y, sorted(S | {x})))
            for i in S:
                (non if i in T else prog).append(F_direct(X, y, sorted(S - {i})))
                for x in range(p):
                    if x in S: continue
                    (prog if (i not in T and x in T) else non).append(F_direct(X, y, sorted((S - {i}) | {x})))
            if S == T: L = max(prog + non) < FS
            elif not (max(prog) > max([FS] + non)): fails += 1
    out.append(f"response {k}: brute force (L)={L}, #failing D_S={fails} | td_check (L)={res[k]['L']}, #failing={res[k]['fail_states']}")
print('\n'.join(out)); open('../results/test_td_check.txt', 'w').write('\n'.join(out) + '\n')
