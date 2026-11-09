"""pk_core.py -- W2-FAC-PK numerics: exact-Gram compound symmetry with p > K = floor(n/2).

Closed forms of W2-FAC-B lemmas/L1 (copied scorer cs_core.py, unchanged):
  z_j = kappa_c + kappa_1 xi_j + lambda_1 theta_j,  F(U) depends on (|U|, A_U = sum z^2, B_U = sum z).
This module adds
  * start_mode_cs: the exact start mode argmax gamma_0 on Omega = {|S| <= K} for a given partition (per-block
    enumeration of all sub-models in closed form, per-size maxima, max-plus DP over blocks with the size prior,
    size ties -> smaller size; within-size ties have probability 0 in floats and are reported if they occur);
  * cs_partition: the method's partition for an exactly equicorrelated Gram (verified against bvs_core's complete
    linkage + cut + next-fit packing in pk_selftest.py);
  * path_from: the uncapped production local search (flip + swap, best strict improvement, exact float ties ->
    lexicographically smallest set) from any start, in gain form (log1p-stable, as cs_gain.py), with per-move
    diagnostics in xi-units, and the first scan index at which S0 is in N(C) u {C}.
"""
import math
import numpy as np
from scipy.special import gammaln
import cs_core as cc


def ell_cap(n, p):
    return math.ceil(math.log2(n + p + 1))


def block_size(n, p):
    return min(math.isqrt(n), math.isqrt(p), 16)


def cs_partition(p, B):
    """consecutive blocks of size B (last one p mod B): the output of the method's complete linkage + cut +
    next-fit packing on an exactly equicorrelated matrix (chain dendrogram under the union-lexicographic tie rule);
    checked against bvs_core.partition_from_corr in pk_selftest.py."""
    return [list(range(s, min(s + B, p))) for s in range(0, p, B)]


def make_cs(rho, theta, n, seed, sigma2=1.0):
    rng = np.random.default_rng(seed)
    return cc.CS(rho, theta, n, sigma2=sigma2, rng=rng)


def _ldet(P, u):
    u = np.asarray(u, float)
    al, be, al2, be2 = P.al, P.be, P.al2, P.be2
    um = np.maximum(u, 1.0)
    v = ((um - 1) * math.log(al) + np.log(al + um * be)) - ((um - 1) * math.log(al2) + np.log(al2 + um * be2))
    return np.where(u > 0, v, 0.0)


def logr_stats(P, u, A, B):
    """log r_b(U) = log m(U) - log m(empty) from (u, A_U, B_U), vectorised."""
    n = P.n
    u = np.asarray(u)
    gam = P.be / (P.al + u * P.be)
    quad = np.where(u > 0, (A - gam * B ** 2) / P.al, 0.0)
    psi = 0.02 + (n - 1.0) - n * quad
    return -0.5 * _ldet(P, u) - P.nu * (np.log(psi) - math.log(0.02 + n - 1.0))


_BITS = {}


def _bits(m):
    if m not in _BITS:
        masks = np.arange(1 << m, dtype=np.int64)
        _BITS[m] = ((masks[:, None] >> np.arange(m)) & 1).astype(np.float64)
    return _BITS[m]


_GROUPS = {}


def _groups(m):
    if m not in _GROUPS:
        u = _bits(m).sum(1).astype(int)
        _GROUPS[m] = [np.flatnonzero(u == s) for s in range(m + 1)]
    return _GROUPS[m]


def start_mode_cs(P, blocks):
    """returns dict(mode=sorted tuple, size, n_size_ties, within_ties) -- the unique maximiser w.p. 1."""
    K = P.K
    z = P.z
    J = len(blocks)
    best_val = []   # per block: array over sizes 0..m of max log r
    best_set = []   # per block: list over sizes of the argmax subset (global indices)
    within_ties = 0
    for C in blocks:
        m = len(C)
        bits = _bits(m)
        zb = z[C]
        A = bits @ (zb ** 2)
        Bs = bits @ zb
        u = bits.sum(1).astype(int)
        lr = logr_stats(P, u, A, Bs)
        vals = np.full(m + 1, -np.inf)
        sets = [None] * (m + 1)
        groups = _groups(m)
        for s in range(m + 1):
            sel = groups[s]
            if s > K:
                continue
            v = lr[sel]
            i = int(np.argmax(v))
            if np.sum(v == v[i]) > 1:
                within_ties += 1
            vals[s] = v[i]
            msk = int(sel[i])
            sets[s] = [C[t] for t in range(m) if (msk >> t) & 1]
        best_val.append(vals)
        best_set.append(sets)
    # max-plus DP over blocks, sizes 0..K, with argmax pointers
    Fm = np.full(K + 1, -np.inf)
    Fm[0] = 0.0
    ptr = np.zeros((J, K + 1), dtype=np.int8)
    for b in range(J):
        vals = best_val[b]
        new = np.full(K + 1, -np.inf)
        arg = np.zeros(K + 1, dtype=np.int8)
        for j in range(len(vals)):
            if not np.isfinite(vals[j]):
                continue
            cand = np.full(K + 1, -np.inf)
            cand[j:] = vals[j] + Fm[:K + 1 - j]
            better = cand > new
            new = np.where(better, cand, new)
            arg = np.where(better, j, arg)
        Fm = new
        ptr[b] = arg
    tot = P.lw + Fm
    kbest = int(np.argmax(tot))   # first maximiser = smaller size on exact ties
    n_size_ties = int(np.sum(tot == tot[kbest]))
    # backtrack
    r = kbest
    mode = []
    sizes = [0] * J
    for b in range(J - 1, -1, -1):
        j = int(ptr[b, r])
        sizes[b] = j
        mode += best_set[b][j]
        r -= j
    assert r == 0
    return dict(mode=tuple(sorted(mode)), size=kbest, n_size_ties=n_size_ties, within_ties=within_ties,
                block_sizes=sizes, logg0=float(tot[kbest]))


def xi_units(P):
    """kappa_1 (t = kappa_1 (xi - x_T) for nulls)."""
    return math.sqrt(P.n - 1.0) * math.sqrt(1 - P.rho) / P.s


def path_from(P, start, max_moves=10 ** 7, keep_rows=False, callback=None):
    """uncapped production local search from `start` (gain form).  Returns moves, final set, first hit index
    (smallest scan index k such that S0 in N(C_k) u {C_k}; LS0 with cap a scores S0 iff a >= k_hit), and
    per-move rows (type, k, x_T, M_T, tau_in, tau_out, gains)."""
    n, p, K = P.n, P.p, P.K
    z = P.z
    S0 = set(P.S0)
    s0 = len(S0)
    nu, al, be = P.nu, P.al, P.be
    k1 = xi_units(P)
    inT = np.zeros(p, bool)
    inT[list(start)] = True
    isS0 = np.zeros(p, bool)
    isS0[list(S0)] = True
    k = int(inT.sum())
    A = float((z[inT] ** 2).sum())
    B = float(z[inT].sum())
    g = lambda u: be / (al + u * be)
    moves = []
    rows = []
    k_hit = None
    nmoves = 0
    while True:
        ex = int((inT & ~isS0).sum())
        mi = int((~inT & isS0).sum())
        if k_hit is None and ((ex + mi <= 1) or (ex == 1 and mi == 1)):
            k_hit = nmoves
        quad = (A - g(k) * B * B) / al
        psi = 0.02 + (n - 1.0) - n * quad
        idx_in = np.flatnonzero(inT)
        idx_out = np.flatnonzero(~inT)
        c = g(k) * B
        tin, tout = z[idx_in] - c, z[idx_out] - c
        LD = float(_ldet(P, k))
        if k >= 1:
            dw = P.lw[k - 1] - P.lw[k] - 0.5 * (float(_ldet(P, k - 1)) - LD)
            Gd = dw - nu * np.log1p(n * (1 + g(k - 1)) * tin ** 2 / (al * psi))
        else:
            dw = None
            Gd = np.array([])
        if k < K and len(idx_out):
            aw = P.lw[k + 1] - P.lw[k] - 0.5 * (float(_ldet(P, k + 1)) - LD)
            Ga = aw - nu * np.log1p(-n * (1 - g(k + 1)) * tout ** 2 / (al * psi))
        else:
            Ga = np.array([])
        if len(idx_out) and k >= 1:
            ext = np.unique([int(np.argmin(tout)), int(np.argmax(tout))])
            tl = tout[ext]
            Dq = tl[None, :] ** 2 - tin[:, None] ** 2 - g(k) * (tl[None, :] - tin[:, None]) ** 2
            Gs = -nu * np.log1p(-n * Dq / (al * psi))
        else:
            Gs = np.zeros((len(idx_in), 0))
            ext = np.array([], int)
        bd = float(Gd.max()) if len(Gd) else -np.inf
        ba = float(Ga.max()) if len(Ga) else -np.inf
        bs = float(Gs.max()) if Gs.size else -np.inf
        best = max(0.0, bd, ba, bs)
        if not best > 0.0:
            break
        cand = []
        cur = idx_in.tolist()
        for i in np.flatnonzero(Gd == best):
            jj = int(idx_in[i])
            cand.append((tuple(v for v in cur if v != jj), jj, None))
        if len(Ga):
            for i in np.flatnonzero(Ga == best):
                ll = int(idx_out[i])
                cand.append((tuple(sorted(cur + [ll])), None, ll))
        if Gs.size:
            for i, e in zip(*np.nonzero(Gs == best)):
                jj, ll = int(idx_in[i]), int(idx_out[ext[e]])
                cand.append((tuple(sorted([v for v in cur if v != jj] + [ll])), jj, ll))
        if len(cand) > 1:
            cand.sort()
        _, jo, li = cand[0]
        if callback is not None:
            callback(dict(P=P, inT=inT, k=k, c=c, psi=psi, Gd=Gd, Ga=Ga, Gs=Gs, idx_in=idx_in, idx_out=idx_out,
                          jo=jo, li=li, best=best, nmoves=nmoves, dw=dw))
        typ = "-" if li is None else ("+" if jo is None else "s")
        tag = typ + ("T" if ((jo is not None and isS0[jo]) or (li is not None and isS0[li])) else "N")
        if keep_rows:
            # M_T: nu * n/(al*psi) * k1^2 (multiplier of tau^2 in the linearised gains)
            MT = nu * n * k1 ** 2 / (al * psi)
            xT = None
            rows.append(dict(i=nmoves, k=k, tag=tag, MT=MT, dw=dw, bd=bd, ba=ba, bs=bs,
                             tau_out=(float((z[jo] - c) / k1) if jo is not None else None),
                             tau_in=(float((z[li] - c) / k1) if li is not None else None),
                             xi_out=(float(P.xi[jo]) if jo is not None else None),
                             xi_in=(float(P.xi[li]) if li is not None else None),
                             cen=float((c - P.z.mean() + P.z.mean()) / k1)))
        if jo is not None:
            inT[jo] = False
            k -= 1
            A -= z[jo] ** 2
            B -= z[jo]
        if li is not None:
            inT[li] = True
            k += 1
            A += z[li] ** 2
            B += z[li]
        moves.append(tag)
        nmoves += 1
        if nmoves >= max_moves:
            break
    ex = int((inT & ~isS0).sum())
    mi = int((~inT & isS0).sum())
    if k_hit is None and ((ex + mi <= 1) or (ex == 1 and mi == 1)):
        k_hit = nmoves
    final = tuple(int(j) for j in np.flatnonzero(inT))
    return dict(moves=moves, final=final, final_is_S0=(set(final) == S0), k_hit=k_hit, rows=rows,
                n_moves=nmoves)


def summarize_moves(moves):
    from collections import Counter
    c = Counter(moves)
    # phases: index of first deletion, number of swaps after the first deletion, additions
    first_del = next((i for i, m in enumerate(moves) if m.startswith("-")), None)
    sw_after = sum(1 for m in moves[first_del:] if m.startswith("s")) if first_del is not None else 0
    lead_sw = 0
    for m in moves:
        if m.startswith("s"):
            lead_sw += 1
        else:
            break
    return dict(counts=dict(c), first_del=first_del, lead_swaps=lead_sw, swaps_after_first_del=sw_after)
