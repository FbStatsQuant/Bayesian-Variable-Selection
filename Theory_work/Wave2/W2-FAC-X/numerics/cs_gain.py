"""cs_gain.py -- numerically stable version of cs_core.ls0_path_cs: every neighbour is scored by its exact gain
F(nb) - F(T), written with log1p and the exact identities (lemmas/L1):
  quad_{T-j} = quad_T - (1+g_{k-1}) t_j^2/alpha,  quad_{T+l} = quad_T + (1-g_{k+1}) t_l^2/alpha,
  quad_{T-j+l} = quad_T + [t_l^2 - t_j^2 - g_k (t_l-t_j)^2]/alpha,   t = z - g_k B_T,
so F differences need no cancellation of O(n) quantities.  Same move rule as the production search."""
import math, numpy as np
import cs_core as cc

def ldet_terms(P, u):
    al, be, al2, be2 = P.al, P.be, P.al2, P.be2
    if u == 0: return 0.0
    return ((u - 1) * math.log(al) + math.log(al + u * be)) - ((u - 1) * math.log(al2) + math.log(al2 + u * be2))

def ls0_path_gain(P, start=None, max_moves=10 ** 7):
    n, p, K = P.n, P.p, P.K
    z = P.z; S0 = set(P.S0); nu = P.nu; al, be = P.al, P.be
    inT = np.zeros(p, bool)
    if start is None: inT[:] = True
    else: inT[list(start)] = True
    k = int(inT.sum()); A = float((z[inT] ** 2).sum()); B = float(z[inT].sum())
    g = lambda u: be / (al + u * be)
    moves = []; info = dict(max_add_gain=-np.inf, max_add_gain_over_logn=-np.inf, max_swap_minus_del=-np.inf,
                            min_del_gain=np.inf, ties=0, max_truth_move=-np.inf)
    while True:
        quad = (A - g(k) * B * B) / al
        psi = 0.02 + (n - 1.0) - n * quad
        idx_in = np.flatnonzero(inT); idx_out = np.flatnonzero(~inT)
        c = g(k) * B
        tin, tout = z[idx_in] - c, z[idx_out] - c
        LD = ldet_terms(P, k)
        # deletions
        if k >= 1:
            dw = P.lw[k - 1] - P.lw[k] - 0.5 * (ldet_terms(P, k - 1) - LD)
            Gd = dw - nu * np.log1p(n * (1 + g(k - 1)) * tin ** 2 / (al * psi))
        else:
            Gd = np.array([])
        if k < K and len(idx_out):
            aw = P.lw[k + 1] - P.lw[k] - 0.5 * (ldet_terms(P, k + 1) - LD)
            Ga = aw - nu * np.log1p(-n * (1 - g(k + 1)) * tout ** 2 / (al * psi))
        else:
            Ga = np.array([])
        if len(idx_out) and k >= 1:
            ext = np.unique([int(np.argmin(tout)), int(np.argmax(tout))])
            tl = tout[ext]
            Dq = tl[None, :] ** 2 - tin[:, None] ** 2 - g(k) * (tl[None, :] - tin[:, None]) ** 2
            Gs = -nu * np.log1p(-n * Dq / (al * psi))
        else:
            Gs = np.zeros((len(idx_in), 0)); ext = np.array([], int)
        best = max([0.0] + ([float(Gd.max())] if len(Gd) else []) + ([float(Ga.max())] if len(Ga) else []) + ([float(Gs.max())] if Gs.size else []))
        isN = np.array([j not in S0 for j in idx_in])
        if len(Ga):
            info["max_add_gain"] = max(info["max_add_gain"], float(Ga.max()))
            info["max_add_gain_over_logn"] = max(info["max_add_gain_over_logn"], float(Ga.max()) / math.log(n))
        if (~isN).any():
            tm = float(Gd[~isN].max())
            if Gs.size: tm = max(tm, float(Gs[~isN].max()))
            info["max_truth_move"] = max(info["max_truth_move"], tm)
        if isN.any() and Gs.size:
            info["max_swap_minus_del"] = max(info["max_swap_minus_del"], float(Gs[isN].max()) - float(Gd[isN].max()))
        if Gs.size:
            info["max_swap_gain"] = max(info.get("max_swap_gain", -np.inf), float(Gs.max()))
        if not best > 0.0:
            break
        # production rule: among all neighbours attaining the best gain, take the lexicographically smallest
        # resulting set (SoP 02_method.tex:483); ties are also counted (info["ties"])
        cand_sets = []
        cur = idx_in.tolist()
        for i in np.flatnonzero(Gd == best):
            jj = int(idx_in[i]); cand_sets.append((tuple(v for v in cur if v != jj), jj, None))
        if len(Ga):
            for i in np.flatnonzero(Ga == best):
                ll = int(idx_out[i]); cand_sets.append((tuple(sorted(cur + [ll])), None, ll))
        if Gs.size:
            for i, e in zip(*np.nonzero(Gs == best)):
                jj, ll = int(idx_in[i]), int(idx_out[ext[e]])
                cand_sets.append((tuple(sorted([v for v in cur if v != jj] + [ll])), jj, ll))
        if len(cand_sets) > 1: info["ties"] += 1
        cand_sets.sort()
        _, jo, li = cand_sets[0]
        if jo is not None and li is None:
            info["min_del_gain"] = min(info["min_del_gain"], best)
        if jo is not None: inT[jo] = False; k -= 1; A -= z[jo] ** 2; B -= z[jo]
        if li is not None: inT[li] = True; k += 1; A += z[li] ** 2; B += z[li]
        typ = "-" if li is None else ("+" if jo is None else "s")
        moves.append((typ + ("T" if (jo in S0 or li in S0) else "N"), jo, li))
        if len(moves) >= max_moves: break
    final = tuple(int(j) for j in np.flatnonzero(inT))
    return dict(moves=moves, final=final, final_is_S0=(set(final) == S0), info=info)
