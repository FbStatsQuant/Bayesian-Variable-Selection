"""R06 scratch: independent L4 checks with an independent D0 scorer (numpy only; no PKA/FAC-B imports).
(1) table-model inclusion <-> block containment over all partitions of p=6;
(2) transfer: S0 contained in a block and pi(S0)>1/2 => all-scored HPM (tables U arbitrary extra scored set) = S0;
(3) non-vacuity controls: contained but pi<=1/2 can give HPM != S0; uncontained S0 is never a table model.
Writes only l4_check_out.json."""
import sys, json, math, itertools
sys.dont_write_bytecode = True
from pathlib import Path
import numpy as np
from math import lgamma
HERE = Path(__file__).resolve().parent

def partitions(seq):
    if not seq: yield []; return
    f = seq[0]
    for rest in partitions(seq[1:]):
        yield [[f]] + [b[:] for b in rest]
        for i in range(len(rest)):
            yield [([f] + b if j == i else b[:]) for j, b in enumerate(rest)]

def make(n, p, theta, rho, rng):
    L = np.linalg.cholesky((1 - rho) * np.eye(p) + rho * np.ones((p, p)))
    Xr = rng.standard_normal((n, p)) @ L.T
    X = Xr - Xr.mean(0); X = X / np.sqrt((X ** 2).sum(0) / (n - 1))
    Y = X @ theta + rng.standard_normal(n); Y = Y - Y.mean(); y = Y / math.sqrt(Y @ Y / (n - 1))
    return X, y

def scorer(X, y):
    n, p = X.shape; K = min(p, n // 2); nu = .01 + n / 2; yy = float(y @ y)
    G = X.T @ X; zf = X.T @ y
    def lw(k): return -math.log(2) - (lgamma(2 * p) - lgamma(k + 1) - lgamma(2 * p - k))
    def F(S):
        S = list(S); k = len(S)
        if k > K: return None
        if k == 0: return lw(0) - nu * math.log(.02 + yy)
        Gs = G[np.ix_(S, S)]; z = zf[S]; H = (n + 1) * Gs + np.eye(k)
        Q = yy - n * z @ np.linalg.solve(H, z)
        return lw(k) - .5 * (np.linalg.slogdet(H)[1] - np.linalg.slogdet(Gs + np.eye(k))[1]) - nu * math.log(.02 + Q)
    return F, K

out = {}
p = 6; parts = list(partitions(list(range(p))))
cnt = cont = fail = 0
for blocks in parts:
    tab = {tuple(sorted(S)) for b in blocks for k in range(len(b) + 1) for S in itertools.combinations(sorted(b), k)}
    for s in (1, 2, 3):
        for T in itertools.combinations(range(p), s):
            hit = any(set(T) <= set(b) for b in blocks); cnt += 1; cont += hit; fail += ((T in tab) != hit)
out['inclusion'] = dict(partitions=len(parts), cases=cnt, contained=cont, failures=fail)

rng = np.random.default_rng(2026)
p = 8; parts8 = [b for b in partitions(list(range(p))) if max(map(len, b)) <= 4]
stats = dict(designs=0, transfer_cases=0, transfer_failures=0, contained_low_pi=0, contained_low_pi_hpm_wrong=0,
             uncontained=0, uncontained_truth_in_table=0)
for rep in range(60):
    s0 = int(rng.integers(1, 4)); n = int(rng.choice([20, 40, 80])); amp = float(rng.choice([.3, .6, 1.5]))
    rho = float(rng.choice([.2, .5, .8]))
    S0 = tuple(sorted(rng.choice(p, s0, replace=False).tolist())); theta = np.zeros(p); theta[list(S0)] = amp
    X, y = make(n, p, theta, rho, rng); F, K = scorer(X, y)
    allS = [S for k in range(K + 1) for S in itertools.combinations(range(p), k)]
    Fv = np.array([F(S) for S in allS]); w = np.exp(Fv - Fv.max()); pi = w / w.sum()
    pi0 = float(pi[allS.index(S0)]) if len(S0) <= K else 0.0
    stats['designs'] += 1
    for blocks in [parts8[i] for i in rng.choice(len(parts8), 40, replace=False)]:
        tab = {tuple(sorted(S)) for b in blocks for k in range(min(len(b), K) + 1) for S in itertools.combinations(sorted(b), k)}
        extra = {allS[i] for i in rng.choice(len(allS), 15, replace=False)}
        scored = tab | extra
        hpm = max(scored, key=lambda S: (F(S), -len(S), tuple(-v for v in S)))
        contained = any(set(S0) <= set(b) for b in blocks) and len(S0) <= K
        if contained and pi0 > .5:
            stats['transfer_cases'] += 1; stats['transfer_failures'] += (hpm != S0)
        elif contained:
            stats['contained_low_pi'] += 1; stats['contained_low_pi_hpm_wrong'] += (hpm != S0)
        else:
            stats['uncontained'] += 1; stats['uncontained_truth_in_table'] += (S0 in tab)
out['transfer'] = stats
(HERE / 'l4_check_out.json').write_text(json.dumps(out, indent=2), encoding='utf8')
print(json.dumps(out, indent=2))
