"""Test engine.py against brute force (direct projections / direct score formula). Seed 20261102.
Run: python3 test_engine.py  -> prints max abs errors; must be < 1e-8."""
import numpy as np
from engine import NbrEngine, Scorer, F_direct

rng = np.random.default_rng(20261102)


def Delta_direct(Sig, th, T):
    T = sorted(T)
    tot = th @ Sig @ th
    if not T:
        return tot
    c = Sig[T] @ th
    return tot - c @ np.linalg.solve(Sig[np.ix_(T, T)], c)


# population side
c = 12
A = rng.standard_normal((c, 40))
Sig = A @ A.T / 40
dd = np.sqrt(np.diag(Sig)); Sig = Sig / dd[:, None] / dd[None, :]
th = np.zeros(c); th[[1, 4, 7]] = [1.3, -0.8, 2.0]
E = NbrEngine(Sig, Sig @ th, th @ Sig @ th)
err = 0.0
for s in range(0, 5):
    states = [tuple(sorted(rng.choice(c, s, replace=False))) for _ in range(6)]
    o = E.eval(np.array(states).reshape(len(states), s))
    for b, S in enumerate(states):
        err = max(err, abs(o['v'][b, 0] - Delta_direct(Sig, th, S)))
        for x in range(c):
            if x in S:
                continue
            err = max(err, abs(o['add_v'][b, x, 0] - Delta_direct(Sig, th, S + (x,))))
        for k, i in enumerate(S):
            Si = tuple(t for t in S if t != i)
            err = max(err, abs(o['del_v'][b, k, 0] - Delta_direct(Sig, th, Si)))
            for x in range(c):
                if x in S:
                    continue
                err = max(err, abs(o['swap_v'][b, k, x, 0] - Delta_direct(Sig, th, Si + (x,))))
print('population Delta: max abs error', err)

# score side
n, p = 40, 15
X = rng.standard_normal((n, p)); X = X - X.mean(0); X = X / X.std(0, ddof=1)
y = X[:, [2, 5]] @ np.array([0.7, -0.5]) + rng.standard_normal(n); y = y - y.mean(); y = y / y.std(ddof=1)
Sc = Scorer(X, y)
err = 0.0
for s in range(0, 5):
    states = [tuple(sorted(rng.choice(p, s, replace=False))) for _ in range(5)]
    o = Sc.eval(np.array(states).reshape(len(states), s))
    for b, S in enumerate(states):
        err = max(err, abs(o['F'][b, 0] - F_direct(X, y, S)))
        for x in range(p):
            if x in S:
                continue
            err = max(err, abs(o['add'][b, x, 0] - F_direct(X, y, S + (x,))))
        for k, i in enumerate(S):
            Si = tuple(t for t in S if t != i)
            err = max(err, abs(o['del'][b, k, 0] - F_direct(X, y, Si)))
            for x in range(p):
                if x in S:
                    continue
                err = max(err, abs(o['swap'][b, k, x, 0] - F_direct(X, y, Si + (x,))))
print('score F: max abs error', err)
