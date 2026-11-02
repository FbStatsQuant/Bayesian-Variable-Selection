"""Checkers for the conditions of T37 / W1-T37R on an explicit family R (referee code).

literal_TD(M, S0, R, m, strict): the TD(d, m) of the T37 file, verbatim:
  (1) S in R, S not superset of S0: some missing truth j with g(S,j) >= m + gain of every OTHER feasible move;
  (2) S in R, S proper superset of S0: some extra l with h(S,l) >= m + gain of every other move;
  (3) at S0 every move has gain <= -m.          (strict: '>' / '<' in place of '>=' / '<=')
TDP(M, S0, R):   (L) M(S0) = None and for S in R minus S0: M(S) is not None and Phi(M(S)) < Phi(S).
TDinf(M, S0, R): (L) and for S in R minus S0: M(S) is not None and M(S) in R.
"""
from vt_core import phi


def _gains(M, S):
    nb, f = M.scan(S)
    return nb, f - M.F(S)


def literal_TD(M, S0, R, m=0.0, strict=True):
    S0 = tuple(sorted(S0)); S0s = set(S0)
    ge = (lambda a, b: a > b) if strict else (lambda a, b: a >= b)
    fails = []
    for S in R:
        Ss = set(S)
        nb, g = _gains(M, S)
        if S == S0:
            if not all(ge(-m, x) for x in g):
                fails.append((S, '3'))
            continue
        if not S0s <= Ss:
            cand = [t for t, T in enumerate(nb) if len(T) == len(S) + 1 and (set(T) - Ss) <= S0s]
            clause = '1'
        else:
            cand = [t for t, T in enumerate(nb) if len(T) == len(S) - 1 and not ((Ss - set(T)) <= S0s)]
            clause = '2'
        ok = False
        for t in cand:
            others = [g[u] for u in range(len(nb)) if u != t]
            if all(ge(g[t], m + x) for x in others):
                ok = True; break
        if not ok:
            fails.append((S, clause))
    return fails


def TDP(M, S0, R):
    S0 = tuple(sorted(S0)); fails = []
    if M.M(S0) is not None:
        fails.append((S0, 'L'))
    for S in R:
        if S == S0:
            continue
        T = M.M(S)
        if T is None or not phi(T, S0) < phi(S, S0):
            fails.append((S, 'P'))
    return fails


def TDinf(M, S0, R):
    S0 = tuple(sorted(S0)); Rs = set(R); fails = []
    if M.M(S0) is not None:
        fails.append((S0, 'L'))
    for S in R:
        if S == S0:
            continue
        T = M.M(S)
        if T is None or T not in Rs:
            fails.append((S, 'N'))
    return fails
