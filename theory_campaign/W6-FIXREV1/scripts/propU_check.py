"""Proposition U: the two A-REV1 Sec. 3.1 counterexamples, evaluated with the actual phi = 1 kernels.  Seed 20261106.

For each configuration we enumerate the phase-1 family Z+(x) and compute, per label, the probability of a *bad* step
under (full) the W1-T24G Sec. 0 definition: leaves F(x), raises V, or removes a present truth; and under
(short) Prop. U's shorthand: independence bad iff it leaves F(x) or raises V; extra-for-extra swap always neutral.
The quantity reported is the label's contribution sup_{W in Z+} P_W(label's step is bad) to eta_1.
Blocks are singletons (any partition is allowed in the component claim; pi0 > 0 everywhere either way).
Indices are 0-based in the code; the report uses 1-based labels.
"""
import itertools
import json
import math
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from bvs_core import Target, standardise, all_models  # noqa: E402


def setup(n, p, Sigma_extra, theta, seed):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    for (i, j, r) in Sigma_extra:
        X[:, j] = r * X[:, i] + math.sqrt(1 - r * r) * X[:, j]
    y = X @ theta + rng.standard_normal(n)
    return Target(*standardise(X, y))


def family(T, S0, x, A):
    """Z(x) and S_a of W1-T24G Sec. 0 (with an explicitly chosen look-alike set A)."""
    p = T.p
    J = set(range(p)) - S0 - A
    c = len(set(x) & J)
    a = len(A) + c
    Z = set()
    for S in all_models(p, T.K):
        S = frozenset(S)
        if not (set(x) & S0) <= S:
            continue
        if not (S - S0) <= (A | J):
            continue
        if len(S & J) > c:
            continue
        Z.add(S)
    Sa = {frozenset(S0 | set(P)) for k in range(a + 1) for P in itertools.combinations(sorted(set(range(p)) - S0), k)
          if len(S0) + k <= T.K}
    return Z, Sa, a


def V(W, S0, a):
    M = S0 - W
    return len(M) + a if M else len(W - S0)


def classify(Wf, Wn, S0, F, a):
    out = Wn not in F
    raise_ = (not out) and V(Wn, S0, a) > V(Wf, S0, a)
    removes = not ((Wf & S0) <= Wn)
    return out, raise_, removes


def pi0_table(T):
    models = [frozenset(S) for S in all_models(T.p, T.K)]
    lg = np.array([T.logg0(tuple(sorted(S))) for S in models])
    w = np.exp(lg - lg.max())
    w /= w.sum()
    return dict(zip(models, w))


def eta_terms(T, S0, x, A):
    Z, Sa, a = family(T, S0, x, A)
    F = Z | Sa
    Zplus = [W for W in Z if S0 - W]
    pi0 = pi0_table(T)
    p = T.p
    res = {'I_full': 0.0, 'I_short': 0.0, 'U_full': 0.0, 'U_short': 0.0, 'argmax_I': None, 'argmax_U': None}
    for W in Zplus:
        Wt = tuple(sorted(W))
        # independence
        full = short = 0.0
        for Sp, m in pi0.items():
            acc = min(1.0, math.exp(T.d(tuple(sorted(Sp))) - T.d(Wt)))
            out, r, rem = classify(W, Sp, S0, F, a)
            if out or r or rem:
                full += m * acc
            if out or r:
                short += m * acc
        if full > res['I_full']:
            res['I_full'], res['argmax_I'] = full, sorted(j + 1 for j in W)
        res['I_short'] = max(res['I_short'], short)
        # uniform swap
        if 0 < len(W) < p:
            full = short = 0.0
            for j in W:
                for l in set(range(p)) - W:
                    Wn = (W - {j}) | {l}
                    pr = (1 / len(W)) * (1 / (p - len(W))) * min(1.0, math.exp(T.logg1(tuple(sorted(Wn))) - T.logg1(Wt)))
                    out, r, rem = classify(W, Wn, S0, F, a)
                    if out or r or rem:
                        full += pr
                    extra_for_extra = (j not in S0) and (l not in S0)
                    if (out or r or rem) and not extra_for_extra:
                        short += pr
            if full > res['U_full']:
                res['U_full'], res['argmax_U'] = full, sorted(j + 1 for j in W)
            res['U_short'] = max(res['U_short'], short)
    res['family_Z'] = sorted(sorted(j + 1 for j in W) for W in Z)
    res['a'] = a
    return res


OUT = {}
# Configuration 1 (A-REV1): S0 = {1,2}, x = empty, A = empty, c = a = 0.
T1 = setup(40, 4, [], np.array([1.0, 1.0, 0, 0]), 20261106)
r1 = eta_terms(T1, frozenset({0, 1}), (), frozenset())
W, Wn = frozenset({0}), frozenset({1})
pi0 = pi0_table(T1)
acc = min(1.0, math.exp(T1.d((1,)) - T1.d((0,))))
r1['transition_{1}->{2}_by_I'] = dict(prob=float(pi0[Wn] * acc), V_before=V(W, {0, 1}, 0), V_after=V(Wn, {0, 1}, 0),
                                      in_family=Wn in {frozenset(s) for s in map(frozenset, [(), (0,), (1,), (0, 1)])})
OUT['config1'] = r1
# Configuration 1b: same geometry, truth 1 weak and truth 2 strong, so the missed mass pi0({2}) is large.
T1b = setup(40, 4, [], np.array([0.05, 1.5, 0, 0]), 20261108)
r1b = eta_terms(T1b, frozenset({0, 1}), (), frozenset())
pi0b = pi0_table(T1b)
r1b['transition_{1}->{2}_by_I'] = dict(prob=float(pi0b[frozenset({1})] * min(1.0, math.exp(T1b.d((1,)) - T1b.d((0,))))))
OUT['config1b'] = r1b
# Configuration 2 (A-REV1): S0 = {1}, x = empty, A = {2} (a look-alike of 1), variable 3 junk, c = 0, a = 1.
T2 = setup(40, 4, [(0, 1, 0.8)], np.array([1.0, 0, 0, 0]), 20261107)
r2 = eta_terms(T2, frozenset({0}), (), frozenset({1}))
W, Wn = frozenset({1}), frozenset({2})
Z, Sa, a = family(T2, frozenset({0}), (), frozenset({1}))
r2['transition_{2}->{3}_by_U'] = dict(prob=float((1 / 3) * min(1.0, math.exp(T2.logg1((2,)) - T2.logg1((1,))))),
                                      in_F=bool(Wn in (Z | Sa)))
OUT['config2'] = r2
print(json.dumps(OUT, indent=1))
with open(__file__.rsplit('/', 2)[0] + '/results/propU_check.json', 'w') as fh:
    json.dump(OUT, fh, indent=1)
