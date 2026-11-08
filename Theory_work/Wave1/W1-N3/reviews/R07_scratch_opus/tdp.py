"""tdp.py -- reference tie-aware DP (TDP) of lemmas/L7_tie_aware_dp.md, exact arithmetic (ints / Fractions).

TDP(I):
  1. V* = max_{|S|<=K} f(S) and k* = smallest maximising size, by the max-plus DP over blocks.
  2. For i = 0, 1, ..., p-1 (increasing index): IN := IN u {i} if some S in A* (size k*, f(S) = V*) has
     S n {0..i} = IN u {i}; otherwise OUT := OUT u {i}.  Feasibility = constrained max-plus DP value.
  3. Return IN.
"""
from n3lib import exact

NEG = None  # -infinity


def _mx(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return a if a >= b else b


def block_max(I, b, IN, OUT):
    """mb[j] = max rho_b(U) over U subset C_b, |U| = j <= min(|C_b|, K), IN n C_b subset U, U n OUT = empty."""
    C = I.blocks[b]
    m = len(C)
    top = min(m, I.K)
    must = sum(1 << i for i, x in enumerate(C) if x in IN)
    ban = sum(1 << i for i, x in enumerate(C) if x in OUT)
    mb = [None] * (top + 1)
    for c in range(1 << m):
        j = bin(c).count("1")
        if j > top or (c & must) != must or (c & ban):
            continue
        v = 0 if c == 0 else exact(I.rho[b][c])
        mb[j] = _mx(mb[j], v)
    return mb


def conv_max(I, IN, OUT):
    """M[k] = max over consistent choices of total size k of sum_b rho_b; None if infeasible."""
    M = [None] * (I.K + 1)
    M[0] = 0
    for b in range(len(I.blocks)):
        mb = block_max(I, b, IN, OUT)
        N = [None] * (I.K + 1)
        for k in range(I.K + 1):
            for j in range(min(k, len(mb) - 1) + 1):
                if M[k - j] is None or mb[j] is None:
                    continue
                N[k] = _mx(N[k], M[k - j] + mb[j])
        M = N
    return M


def tdp(I):
    M = conv_max(I, set(), set())
    vals = [None if M[k] is None else exact(I.lam[k]) + M[k] for k in range(I.K + 1)]
    Vstar = None
    for v in vals:
        Vstar = _mx(Vstar, v)
    kstar = min(k for k in range(I.K + 1) if vals[k] is not None and vals[k] == Vstar)
    IN, OUT = set(), set()
    for i in range(I.p):
        Mi = conv_max(I, IN | {i}, OUT)
        if Mi[kstar] is not None and exact(I.lam[kstar]) + Mi[kstar] == Vstar:
            IN.add(i)
        else:
            OUT.add(i)
    return Vstar, kstar, sorted(IN)
