"""Population (or realised-Gram) scan of PGD, GERC and TRC over a region R_{a,d}(D) (W3-PGD PROOF §1).

scan(Sig, th, truth, extras, a, d): over states S = U u P (U subset of truth missing m in [1, a], P subset of extras,
|P| <= d) and ALL feasible flips/swaps over the columns of Sig (no cap K: the study's K = 100 > s0 + d + 1):
  rho+(S) = max progress reduction of Delta, rho0(S) = max non-progress reduction  (Delta = ||(I-P_S)mu||^2/N),
  eta_hat = 1 - max rho0/rho+, the binding state and move type (N1 add null, N2 delete truth, N3 swap truth->null,
  N4 swap extra->null, N5 swap truth->truth), TRC_min = min a_u(S-u+j)/a_j(S) (u in U, j in M),
  GERC_max = max ERC(S, l) over states with 1 <= m <= a_gerc and all nulls l not in S (optional).
Deterministic (no randomness).
"""
import itertools
import numpy as np
from engine import NbrEngine, region_states

TYPES = ['N1 add null', 'N2 delete truth', 'N3 swap truth->null', 'N4 swap extra->null', 'N5 swap truth->truth']


def scenario_covariance(scenario, p):
    """Verbatim port of Scripts/Data_generators/gen_dev_data.R::scenario_covariance (unit diagonal)."""
    group = np.ceil(np.arange(1, p + 1) / 5).astype(int)
    H = (group[:, None] == group[None, :]).astype(float)
    I = np.eye(p)
    if scenario == 1:
        return I
    if scenario == 2:
        i = np.arange(p)
        return 0.5 ** np.abs(i[:, None] - i[None, :])
    if scenario == 3:
        return 0.7 * H + 0.3 * I
    if scenario == 4:
        return 0.85 * H + 0.15 * I
    if scenario == 5:
        return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    if scenario == 6:
        rho = 0.4 + 0.1 * ((group - 1) % 6)
        S = H * rho[:, None]
        np.fill_diagonal(S, 1.0)
        return S
    raise ValueError(scenario)


def truth(p):
    """Port of gen_dev_data.R::truth; returns 0-based active indices and beta (p in {30, 500, 1000})."""
    s0, step = {30: (5, 1), 500: (14, 7), 1000: (14, 13)}[p]
    pos = [3, 2, 4, 1, 5, 3]
    pattern = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    k = np.arange(s0)
    block = 1 + step * k
    active = 5 * (block - 1) + np.array([pos[i % 6] for i in k])
    return active - 1, np.array([pattern[i % 6] for i in k])


def mates(active, p):
    """Nulls in the truth blocks (the generator's groups of 5 that contain a truth)."""
    act = set(int(a) for a in active)
    out = sorted(set(int(5 * (a // 5) + k) for a in active for k in range(5)) - act)
    return [x for x in out if x < p]


def scan(Sig, th, truth_idx, extras, a, d, gerc_a=None, batch=512, amin=1, verbose=False):
    Sig = np.asarray(Sig, float)
    c = Sig.shape[0]
    truth_idx = [int(t) for t in truth_idx]
    is_t = np.zeros(c, bool); is_t[truth_idx] = True
    E = NbrEngine(Sig, Sig @ th, th @ Sig @ th)
    res = dict(states=0, max_ratio=-np.inf, worst=None, worst_type=None, trc_min=np.inf, trc_state=None,
               gerc_max=-np.inf, gerc_state=None, rho_plus_min=np.inf)
    a_hi = max(a, gerc_a or 0)
    by = region_states(truth_idx, list(extras), a_hi, d, amin=amin)
    for s, lst in sorted(by.items()):
        for b0 in range(0, len(lst), batch):
            chunk = lst[b0:b0 + batch]
            idx = np.array([S for S, _, _ in chunk], dtype=int).reshape(len(chunk), s)
            mm = np.array([m for _, m, _ in chunk])
            o = E.eval(idx, ld=False)
            inS = o['inS']
            if gerc_a:
                g = erc_batch(Sig, idx, inS, is_t)
                k = int(np.argmax(g))
                if g[k] > res['gerc_max']:
                    res['gerc_max'] = float(g[k]); res['gerc_state'] = list(map(int, idx[k]))
            sel = mm <= a
            if not sel.any():
                continue
            idx, inS = idx[sel], inS[sel]
            DS = o['v'][sel, 0]
            add = DS[:, None] - o['add_v'][sel, :, 0]                 # (B, c) reductions, nan in S
            prog_add = np.where(is_t[None, :] & ~inS, add, -np.inf)
            non_add = np.where(~is_t[None, :] & ~inS, add, -np.inf)
            rho_p = prog_add.max(1)
            r0 = non_add.max(1); t0 = np.zeros(len(DS), int)
            if s > 0:
                tS = is_t[idx]                                          # (B, s) truth in S?
                dele = DS[:, None] - o['del_v'][sel, :, 0]
                rho_p = np.maximum(rho_p, np.where(~tS, dele, -np.inf).max(1))
                dn = np.where(tS, dele, -np.inf).max(1)
                upd = dn > r0; r0 = np.where(upd, dn, r0); t0 = np.where(upd, 1, t0)
                sw = DS[:, None, None] - o['swap_v'][sel, :, :, 0]        # (B, s, c)
                ok = ~inS[:, None, :]
                xt = is_t[None, None, :]
                it = tS[:, :, None]
                prog_sw = np.where(ok & ~it & xt, sw, -np.inf).max((1, 2))
                rho_p = np.maximum(rho_p, prog_sw)
                for typ, mask in ((2, it & ~xt), (3, ~it & ~xt), (4, it & xt)):
                    v = np.where(ok & mask, sw, -np.inf).max((1, 2))
                    upd = v > r0; r0 = np.where(upd, v, r0); t0 = np.where(upd, typ, t0)
                # TRC: a_u(S-u+j)/a_j(S) = (Delta_{S-u+j} - Delta_{S+j}) / (Delta_S - Delta_{S+j})
                addv = o['add_v'][sel, :, 0]
                num = o['swap_v'][sel, :, :, 0] - addv[:, None, :]
                den = np.broadcast_to((DS[:, None] - addv)[:, None, :], num.shape)
                with np.errstate(divide='ignore', invalid='ignore'):
                    trc = np.where(ok & it & xt & (den > 0), num / np.where(den > 0, den, 1.0), np.inf).min((1, 2))
                k = int(np.argmin(trc))
                if trc[k] < res['trc_min']:
                    res['trc_min'] = float(trc[k]); res['trc_state'] = list(map(int, idx[k]))
            ratio = r0 / rho_p
            k = int(np.argmax(ratio))
            res['states'] += len(DS)
            res['rho_plus_min'] = min(res['rho_plus_min'], float(rho_p.min()))
            if ratio[k] > res['max_ratio']:
                res['max_ratio'] = float(ratio[k]); res['worst'] = list(map(int, idx[k])); res['worst_type'] = TYPES[t0[k]]
        if verbose:
            print('  size', s, 'done; states so far', res['states'], 'max ratio', res['max_ratio'], flush=True)
    res['eta'] = 1 - res['max_ratio']
    return res


def erc_batch(Sig, idx, inS, is_t):
    """max_l ERC(S, l) per state; ERC = || Ghat^{-1} b ||_1 with residualised, normalised atoms (W3-PGD §1)."""
    Bt, s = idx.shape
    c = Sig.shape[0]
    out = np.full(Bt, -np.inf)
    # group states by their missing set size
    Mlist = [np.nonzero(is_t & ~inS[b])[0] for b in range(Bt)]
    msz = np.array([len(M) for M in Mlist])
    for m in np.unique(msz):
        if m == 0:
            continue
        bs = np.nonzero(msz == m)[0]
        Mi = np.array([Mlist[b] for b in bs])                      # (B, m)
        ii = idx[bs]
        if s > 0:
            Gsc = Sig[ii]                                          # (B, s, c)
            Gs = np.take_along_axis(Gsc, ii[:, None, :].repeat(s, 1), axis=2)
            Wt = np.linalg.solve(Gs, Gsc)                          # (B, s, c)
            CM = Sig[Mi] - np.einsum('bsm,bsc->bmc', np.take_along_axis(Wt, Mi[:, None, :].repeat(s, 1), axis=2), Gsc)
            dg = 1 - np.einsum('bsc,bsc->bc', Wt, Gsc)
        else:
            CM = Sig[Mi]
            dg = np.ones((len(bs), c))
        CMM = np.take_along_axis(CM, Mi[:, None, :].repeat(m, 1), axis=2)   # (B, m, m)
        dM = np.sqrt(np.einsum('bmm->bm', CMM))
        Gh = CMM / dM[:, :, None] / dM[:, None, :]
        bl = CM / dM[:, :, None] / np.sqrt(np.maximum(dg, 1e-300))[:, None, :]  # (B, m, c)
        coef = np.linalg.solve(Gh, bl)
        erc = np.abs(coef).sum(1)                                   # (B, c)
        nullmask = (~is_t[None, :]) & (~inS[bs]) & (dg > 1e-12)
        out[bs] = np.where(nullmask, erc, -np.inf).max(1)
    return out
