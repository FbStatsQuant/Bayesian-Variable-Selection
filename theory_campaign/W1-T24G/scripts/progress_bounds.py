"""
Exact constants of Theorem B (PROOF.md s4): per-round progress-or-bad bounds on start-adapted families.

Phase 2 family  S_a = {S0 u P : |P| <= a}.  At W != S0:
  bad  : Gibbs truth deletion; Gibbs null addition; swap removing a truth; independence to S' notin S_a or
         |P(S')| > |P(W)|.
  progress: Gibbs deletion of an extra; independence to S' in S_a with |P(S')| < |P(W)|.
  neutral : everything else (extra-for-null swaps, failed deletions, ...).
  eta2   = sum_labels max_{W in S_a \\ S0} P_W(bad)
  epsdel = max_{W in S_a\\S0, l in P(W)} o_l(W)
  h(l)   = 1/2 sum_{e in NG} max_{W in S_a, l in W} P_W(e accepted, removes l, not bad, not progress)
  Hmax   = max_{W0 in S_a\\S0} min_{l in P(W0)} h(l)
  c2     = 1 - epsdel - min(Hmax, (B'+2)/(B'+3)),   B'+2 = number of non-Gibbs labels.
Phase 1 family Z(x) = {U u P u Q : x cap S0 subset U subset S0, P subset A, Q subset (S0 u A)^c, |Q| <= c},
  A = union_{j in M(x)} N(j) \\ S0 (neighbour-graph look-alikes of the missing truths), c = |x \\ (S0 u A)|.
  At W in Z with M(W) != empty:
  bad  : truth deletion (any label); move leaving Z; independence to S' with |M(S')| > |M(W)|.
  progress: |M| decreases (Gibbs addition of a missing truth, proxy->truth swap, independence).
  eta1 = sum_labels max_{W in Z, M(W) != 0} P_W(bad);  epsadd = min_{j in M(x)} max_{W in Z, j notin W} (1 - o_j(W));
  c1 = 1 - epsadd.
"""
import math
import numpy as np
from bvs_engine import *
from sweep_bounds import gibbs_o, popcnt, SortedAcc, bits_of


def swap_pairs(M, W, kind):
    p = M.p
    k = M.size[W].astype(float)
    Nb = np.array(M.Nb, dtype=np.int64)
    for j in range(p):
        hasj = ((W >> j) & 1) == 1
        if not hasj.any():
            continue
        if kind == 'N':
            nc = popcnt(Nb[j] & ~W)
        for l in range(p):
            if l == j:
                continue
            ok = hasj & (((W >> l) & 1) == 0)
            if kind == 'N':
                ok = ok & (((Nb[j] >> l) & 1) == 1)
            if not ok.any():
                continue
            dest = (W & ~np.int64(1 << j)) | np.int64(1 << l)
            ratio = np.exp(M.F[dest] - M.F[W])
            if kind == 'U':
                pr = np.where(ok, np.minimum(1, ratio) / (k * (p - k)), 0.0)
            else:
                rev = popcnt(Nb[l] & ~dest)
                pr = np.where(ok, (1.0 / k) / np.maximum(nc, 1) * np.minimum(1, ratio * nc / np.maximum(rev, 1)), 0.0)
            yield j, l, dest, pr


def phase2_B(M, a):
    p, S0 = M.p, M.S0
    s0b = set(bits_of(S0, p))
    nulls = [l for l in range(p) if l not in s0b]
    allidx = np.arange(1 << p, dtype=np.int64)
    ex_all = popcnt(allidx & ~np.int64(S0))
    fam = ((allidx & S0) == S0) & (ex_all <= a)
    W = allidx[fam & (allidx != S0)]
    exW = ex_all[W]
    nng = M.n_nb + 2
    eta_lab = {}
    # Gibbs
    for i in s0b:
        eta_lab['G%d' % i] = float(np.max(1 - gibbs_o(M, W, i)))
    epsdel = 0.0
    for l in nulls:
        o = gibbs_o(M, W, l)
        inW = ((W >> l) & 1) == 1
        eta_lab['G%d' % l] = float(o[~inW].max()) if (~inW).any() else 0.0
        if inW.any():
            epsdel = max(epsdel, float(o[inW].max()))
    # swaps
    rem = {kind: np.zeros((p, len(W))) for kind in 'UN'}
    for kind in 'UN':
        bad = np.zeros(len(W))
        for j, l, dest, pr in swap_pairs(M, W, kind):
            if j in s0b:
                bad += pr
            else:
                rem[kind][j] += pr          # extra j removed, replaced by null l (neutral, may hide slot j)
        eta_lab[kind] = float(bad.max())
    # independence
    dW = M.d[W]
    outside = SortedAcc(M, ~fam)(dW)
    byc = [SortedAcc(M, fam & (ex_all == c)) for c in range(a + 1)]
    accc = np.stack([f(dW) for f in byc])               # (a+1, |W|)
    badI = outside + np.array([accc[exW[i] + 1:, i].sum() for i in range(len(W))])
    eta_lab['I'] = float(badI.max())
    remI = np.zeros((p, len(W)))
    for l in nulls:
        for c in range(1, a + 1):
            selW = (exW == c) & (((W >> l) & 1) == 1)
            if not selW.any():
                continue
            setc = fam & (ex_all == c) & (((allidx >> l) & 1) == 0)
            remI[l, selW] = SortedAcc(M, setc)(dW[selW])
    eta2 = sum(v for k, v in eta_lab.items() if k.startswith('G')) + eta_lab['U'] + M.n_nb * eta_lab['N'] + eta_lab['I']
    # slot-hiding h(l)
    h = np.zeros(p)
    for l in nulls:
        has = ((W >> l) & 1) == 1
        if not has.any():
            continue
        h[l] = 0.5 * (rem['U'][l][has].max() + M.n_nb * rem['N'][l][has].max() + remI[l][has].max())
    hmin_slot = np.array([min(h[l] for l in nulls if (w >> l) & 1) for w in W])
    Hmax = float(hmin_slot.max())
    c2 = 1 - epsdel - min(Hmax, (nng) / (nng + 1))
    return dict(a=a, eta2=float(eta2), epsdel=epsdel, Hmax=Hmax, c2=float(c2), famsize=int(fam.sum()),
                eta_parts=eta_lab, order_floor=1 / (nng + 1))


def lookalike_set(M, x):
    S0 = M.S0
    A = 0
    for j in bits_of(S0 & ~x, M.p):
        A |= M.Nb[j] & ~S0
    return A


def phase1_B(M, x):
    p, S0 = M.p, M.S0
    s0b = set(bits_of(S0, p))
    A = lookalike_set(M, x)
    U0 = x & S0
    junk_mask = ((1 << p) - 1) & ~S0 & ~A
    c = bin(x & junk_mask).count('1')
    allidx = np.arange(1 << p, dtype=np.int64)
    qcnt = popcnt(allidx & junk_mask)
    famZ = ((allidx & U0) == U0) & (qcnt <= c)
    missc = popcnt(np.int64(S0) & ~allidx)
    W = allidx[famZ & (missc > 0)]
    mW = missc[W]
    eta = 0.0; parts = {}
    for j in range(p):
        o = gibbs_o(M, W, j)
        inW = ((W >> j) & 1) == 1
        if j in s0b:
            v = float((1 - o)[inW].max()) if inW.any() else 0.0          # truth deletion
        elif (junk_mask >> j) & 1:
            sel = (~inW) & (qcnt[W] == c)                                 # junk addition beyond count
            v = float(o[sel].max()) if sel.any() else 0.0
        else:
            v = 0.0                                                       # look-alikes: neutral
        parts['G%d' % j] = v; eta += v
    for kind in 'UN':
        bad = np.zeros(len(W))
        for j, l, dest, pr in swap_pairs(M, W, kind):
            if j in s0b and l not in s0b:
                bad += pr
            elif j in s0b and l in s0b:
                bad += np.where((dest & U0) == U0, 0.0, pr)              # truth-for-truth: bad only if leaves Z
            elif not famZ[dest].all():
                bad += np.where(famZ[dest], 0.0, pr)
        parts[kind] = float(bad.max())
    eta += parts['U'] + M.n_nb * parts['N']
    dW = M.d[W]
    tot = SortedAcc(M, np.ones(1 << p, bool))(dW)
    good = np.zeros(len(W))
    for mm in np.unique(mW):
        sel = mW == mm
        good[sel] = SortedAcc(M, famZ & (missc <= mm))(dW[sel])
    parts['I'] = float((tot - good).max()); eta += parts['I']
    # epsadd
    best = 1.0
    for j in bits_of(S0 & ~x, p):
        sel = ((W >> j) & 1) == 0
        best = min(best, float((1 - gibbs_o(M, W[sel], j)).max()))
    a = bin(A).count('1') + c
    return dict(eta1=float(eta), epsadd=best, c1=1 - best, a=a, A=A, c=c, famsize=int(famZ.sum()), parts=parts)


def binom_lt(H, c, k):
    c = min(max(c, 0.0), 1.0)
    return sum(math.comb(H, i) * c ** i * (1 - c) ** (H - i) for i in range(min(k, H + 1)))
