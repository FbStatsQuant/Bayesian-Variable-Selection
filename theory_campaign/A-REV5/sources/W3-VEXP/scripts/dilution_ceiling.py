"""Prop D (deterministic start-mass ceiling) vs exact pi0(S0), n = 200, p = 500, same designs/seeds as study_exp.py.
pi0(S0) <= min_U [w(s0)/w(s0-|U|)] prod_{j in U} BF({j}),  U = truths that are the only truth in their block;
the minimum is attained by taking U = {j alone : BF({j}) * marginal prior factor < 1} greedily in order of BF.
BF({j}) closed form in r_jy:  D_j = ((n+1)(n-1)+1)/n,  Q_j = (n-1)(1 - n(n-1) r^2/((n+1)(n-1)+1)).
Also the population 'dilution' prediction r^2 ~ theta_j^2 c^2 / (1 + c^2 sum theta_k^2) (S1/S3/S4/S6, independent truths)."""
import math, sys, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import vcore as V
from scen import scenario_cov, truth
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
p = 500
act, beta = truth(p); th = np.zeros(p); th[act] = beta; S0 = set(int(a) for a in act); s0 = len(S0)
def logBF(r2, n):
    nu = 0.01 + n / 2; H = (n + 1) * (n - 1) + 1
    Q = (n - 1) * (1 - n * (n - 1) * r2 / H)
    return -0.5 * math.log(H / n) - nu * (math.log(0.02 + Q) - math.log(0.02 + n - 1))
for sc in (1, 3, 4, 6):
    Lc = np.linalg.cholesky(scenario_cov(sc, p))
    for cs in (1.0, 0.5, 4.0):
        for r in range(3 if N == 200 else 2):
            rng = np.random.default_rng(20261102 + 10 * sc + r)
            Z = rng.standard_normal((N, p)) @ Lc.T
            X = Z - Z.mean(0); X /= X.std(0, ddof=1)
            eps = rng.standard_normal(N); Y = cs * (X @ th) + eps
            Yc = Y - Y.mean(); y = Yc / Yc.std(ddof=1)
            blocks = V.make_blocks((X.T @ X) / (N - 1), V.B_rule(N, p))
            blk = {j: b for b, C in enumerate(blocks) for j in C}
            alone = [j for j in S0 if sum(1 for k in S0 if blk[k] == blk[j]) == 1]
            r2 = {j: float((X[:, j] @ y / (N - 1)) ** 2) for j in alone}
            lb = sorted((logBF(r2[j], N), j) for j in alone)
            best = 0.0; cur = 0.0
            for a, (l, j) in enumerate(lb, 1):
                # w(s0)/w(s0-a) = prod_{i=1..a} (s0-a+i)/(2p-s0+a-i); recompute exactly for prefix of size a
                lw = sum(math.log((s0 - a + i) / (2 * p - s0 + a - i)) for i in range(1, a + 1))
                cur = lw + sum(x for x, _ in lb[:a])
                best = min(best, cur)
            v = 1 + cs ** 2 * float(np.sum(beta ** 2))
            npred = sum(1 for b in beta if (N / 2) * -math.log(1 - (cs * b) ** 2 / v) > math.log((2 * p - s0) / s0) + 0.5 * math.log(N))
            print(json.dumps(dict(S=sc, c=cs, rep=r, n=N, log10_ceiling=round(best / math.log(10), 2), n_alone=len(alone),
                                  n_truths_pop_visible=npred)), flush=True)
