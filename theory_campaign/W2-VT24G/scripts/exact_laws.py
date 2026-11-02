"""Exact one-label transition laws at a state x for the phi = 1 round (W2-VT24G, independent of W1 code).
Each law is a dict dest -> probability (self-loop included)."""
import math
import numpy as np


def gibbs_law(M, x, j):
    w, wo = x | (1 << j), x & ~(1 << j)
    if M.sizes[w] > M.K:
        return {wo: 1.0}
    o = 1.0 / (1.0 + math.exp(M.F[wo] - M.F[w]))
    out = {}
    out[w] = out.get(w, 0) + o
    out[wo] = out.get(wo, 0) + 1 - o
    return out


def uswap_law(M, x):
    p = M.p
    S = [j for j in range(p) if x >> j & 1]
    k = len(S)
    if k in (0, p):
        return {x: 1.0}
    out = {x: 0.0}
    nonm = [l for l in range(p) if not x >> l & 1]
    pr = 1.0 / (k * (p - k))
    for j in S:
        for l in nonm:
            y = (x & ~(1 << j)) | (1 << l)
            a = min(1.0, math.exp(min(0.0, M.F[y] - M.F[x])))
            out[y] = out.get(y, 0) + pr * a
            out[x] += pr * (1 - a)
    return out


def nswap_law(M, x):
    p = M.p
    S = [j for j in range(p) if x >> j & 1]
    k = len(S)
    if k == 0:
        return {x: 1.0}
    out = {x: 0.0}
    for j in S:
        cand = [l for l in M.Nb[j] if not x >> l & 1]
        if not cand:
            out[x] += 1.0 / k
            continue
        for l in cand:
            y = (x & ~(1 << j)) | (1 << l)
            back = sum(1 for t in M.Nb[l] if not y >> t & 1)
            la = M.F[y] - M.F[x] + math.log(len(cand)) - math.log(back)
            a = math.exp(min(0.0, la))
            pr = 1.0 / (k * len(cand))
            out[y] = out.get(y, 0) + pr * a
            out[x] += pr * (1 - a)
    return out


def indep_accept(M, x):
    """vector over all masks: pi0(S') * min(1, exp(d(S') - d(x)))  (probability of moving to S')."""
    return M.pi0 * np.exp(np.minimum(0.0, M.d - M.d[x]))


def label_laws(M, x):
    """list of (label name, law) for the p Gibbs labels, U, B copies of N; independence handled separately."""
    laws = [('G%d' % j, gibbs_law(M, x, j)) for j in range(M.p)]
    laws.append(('U', uswap_law(M, x)))
    nl = nswap_law(M, x)
    for b in range(M.B):
        laws.append(('N%d' % (b + 1), nl))
    return laws


# Gauss-Legendre on [0,1] for integrals int_0^1 prod_j (1 - t q_j) dt (polynomial degree <= m: exact)
_GX, _GW = np.polynomial.legendre.leggauss(40)
GT = (_GX + 1) / 2
GW = _GW / 2


def first_change_prob(s, q):
    """Lemma O(iii)/Lemma P: P(first state-changing-or-Good label is Good) = sum_e s_e int prod_{j!=e}(1-t q_j) dt."""
    s = np.asarray(s, float); q = np.clip(np.asarray(q, float), 0, 1)
    tot = 0.0
    for e in np.nonzero(s > 0)[0]:
        qq = np.delete(q, e)
        tot += s[e] * float(GW @ np.prod(1 - GT[:, None] * qq[None, :], axis=1))
    return tot
