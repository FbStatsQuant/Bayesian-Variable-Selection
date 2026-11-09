"""W2-SIM family S5, experiment E-S5P(ii): iid-Gaussian-row block compound symmetry (random Gram), p <= n/2.
Data + path: W2-FAC-X numerics/iid_core.py imported UNCHANGED from the ticket snapshot (tickets_20261109T0943,
sha256 d410eaa9...6b210): IidData (exact Bartlett sufficient statistics of iid factor rows) with the S5 loading matrix
Lam = [sqrt(rb) 1 | sqrt(b) * group indicators] (k = 1 + G factors, psi = d = 1 - rw), and ls0_path (uncapped
production local search, best strict improvement over ALL deletions, additions and swaps (complete scans), exact ties ->
lexicographically smallest set) from T0 = [p]. Truths: bcs_core.layout(p, q, s0=4) as raw coefficients (population
column variance 1), sigma = 1.
Score-scale statistics (from iid_core.PathState; psi_T := 0.02 + y'y - n quad_T):
  deletion  tau_j^2 := 2 nu log1p(n dq_del_j / psi_T)     (gain = prior/logdet terms - tau_j^2 / 2)
  addition  tau_l^2 := -2 nu log1p(-n dq_add_l / psi_T)   (gain = prior/logdet terms + tau_l^2 / 2)
Recorded: as s5p_exact.py (moves by type, final_is_S0, pure_deletion, MR1 cap, margins best_add - best_del and best_swap -
best_del in units log n by phase, d_T = min deletion |tau| over retained nulls, Dout = max addition |tau| over outside
nulls, Dout/d_T (raw ratio_*; restricted to d_T >= H/4: ratioR_*), add-threshold proximity Dout/sqrt(2 Delta_k), within-group jumps of |tau| of null group-mates after each
null deletion (units H for all events; units d_j for events with d_j >= H/4), crossings c*d_T, c = 1, 1.5, 2) and
iid_core's info (max_add_gain, max_truth_move, max_swap_minus_del, min_del_gain, ties).
usage: python s5p_iid.py p n seed [q rb rw]
"""
import os, sys, math, json, time
TICK = os.environ.get("TICKETS")
if TICK:
    sys.path.insert(0, TICK + "/Theory_work/Wave2/W2-FAC-X/numerics")
    sys.path.insert(1, TICK + "/Theory_work/Wave2/W2-FAC-S5/numerics")
else:
    sys.path.insert(0, os.environ["IID_CORE_DIR"]); sys.path.insert(1, os.environ["BCS_CORE_DIR"])
import numpy as np
import iid_core as IC
import bcs_core as BC


def s5_loadings(p, q, rb, rw):
    grp = np.arange(p) // q
    G = int(grp.max()) + 1
    Lam = np.zeros((p, 1 + G))
    Lam[:, 0] = math.sqrt(rb)
    Lam[np.arange(p), 1 + grp] = math.sqrt(rw - rb)
    return Lam, grp


def build(p, n, seed, q=5, rb=.3, rw=.7):
    Lam, grp = s5_loadings(p, q, rb, rw)
    beta = BC.layout(p, q, s0=4)
    rng = np.random.default_rng(30011 * seed + p + 7 * n)
    return IC.IidData(Lam, beta, n, rng, sigma=1.0), grp, beta


def run(p, n, seed, q=5, rb=.3, rw=.7):
    t0 = time.time()
    P, grp, beta = build(p, n, seed, q, rb, rw)
    t_build = time.time() - t0
    S0 = set(P.S0)
    isnull = np.ones(p, bool); isnull[list(S0)] = False
    logn = math.log(n); H = math.sqrt(2 * math.log(2 * p)); nu = P.nu
    every = max(1, math.ceil(p / 400))
    order = np.argsort(grp, kind="stable"); gstart = np.searchsorted(grp[order], np.arange(grp.max() + 2))
    BINS = np.array([-np.inf, -1.0, -0.5, -0.25, -0.1, 0.0, 0.1, 0.25, 0.5, 1.0, 1.5, 2.0, np.inf])
    BINS_H = np.array([-np.inf, -0.5, -0.25, -0.1, -0.05, 0.0, 0.05, 0.1, 0.25, 0.5, 1.0, np.inf])
    S = dict(hist_out=np.zeros(len(BINS) - 1, np.int64), hist_ret=np.zeros(len(BINS) - 1, np.int64),
             hH_out=np.zeros(len(BINS_H) - 1, np.int64), hH_ret=np.zeros(len(BINS_H) - 1, np.int64),
             jo=[], jr=[], joH=[], jrH=[], prev=None, trace=[])
    cross = {1.0: np.zeros(p, bool), 1.5: np.zeros(p, bool), 2.0: np.zeros(p, bool)}
    W = dict(add_minus_del_bulk=-np.inf, add_minus_del_end=-np.inf, swap_minus_del_bulk=-np.inf, swap_minus_del_end=-np.inf,
             ratio_bulk=0.0, ratio_end=0.0, ratio_max_at_m=None, addprox_max=0.0, addprox_at_m=None, nonargmin=0,
             dellevel_over_sqrt2D_max=0.0, ratioR_bulk=0.0, ratioR_end=0.0, ratioR_max_at_m=None)

    def diag(P_, st, Gd, Ga, Gs, step):
        T, O = st.T, st.O
        k = len(T)
        psi = 0.02 + P_.yty - P_.n * st.quad
        atau = np.full(p, np.nan)
        if k:
            w1 = np.diag(st.W1)
            atau[T] = np.sqrt(2 * nu * np.log1p(P_.n * (st.u ** 2 / w1) / psi))
        if len(O):
            x = P_.n * (st.bil ** 2 / st.s1) / psi
            with np.errstate(invalid="ignore", divide="ignore"):
                atau[O] = np.sqrt(np.where(x < 1, -2 * nu * np.log1p(-np.minimum(x, 1 - 1e-300)), np.inf))
        Tn = T[isnull[T]]; On = O[isnull[O]]
        m = len(Tn)
        # jumps caused by the previous move (if it was a single null deletion)
        if S["prev"] is not None:
            pT, patau = S["prev"]
            gone = np.setdiff1d(pT, T)
            if len(gone) == 1 and len(T) == len(pT) - 1 and isnull[gone[0]]:
                j = int(gone[0]); dj = float(patau[j])
                mates = order[gstart[grp[j]]:gstart[grp[j] + 1]]
                mates = mates[(mates != j) & isnull[mates]]
                if len(mates):
                    was_out = ~np.isin(mates, pT)
                    dabs = atau[mates] - patau[mates]
                    ok = np.isfinite(dabs)
                    jH = dabs[ok] / H; wo = was_out[ok]
                    S["hH_out"] += np.histogram(jH[wo], BINS_H)[0]; S["hH_ret"] += np.histogram(jH[~wo], BINS_H)[0]
                    S["joH"].extend(jH[wo].tolist()); S["jrH"].extend(jH[~wo].tolist())
                    if dj >= H / 4:
                        jd = dabs[ok] / dj
                        S["hist_out"] += np.histogram(jd[wo], BINS)[0]; S["hist_ret"] += np.histogram(jd[~wo], BINS)[0]
                        S["jo"].extend(jd[wo].tolist()); S["jr"].extend(jd[~wo].tolist())
        S["prev"] = (T.copy(), atau.copy())
        isNT = isnull[T]
        best_del = float(Gd[isNT].max()) if isNT.any() else -np.inf
        best_add = float(Ga.max()) if len(Ga) else -np.inf
        best_sw = float(Gs[isNT].max()) if (Gs.size and isNT.any()) else -np.inf
        S["prev_choice"] = int(T[isNT][np.argmax(Gd[isNT])]) if isNT.any() else None
        dT = float(np.min(atau[Tn])) if m else np.nan
        if m and S["prev_choice"] != int(Tn[np.argmin(atau[Tn])]): W["nonargmin"] += 1
        Dk = math.log((2 * p - k) / k) + 0.5 * math.log(P_.n + 1) if k else np.nan
        if m: W["dellevel_over_sqrt2D_max"] = max(W["dellevel_over_sqrt2D_max"], dT / math.sqrt(2 * Dk))
        Dout = float(np.max(atau[On])) if len(On) else 0.0
        if len(On):
            prox = Dout / math.sqrt(2 * Dk)
            if prox > W["addprox_max"]: W["addprox_max"], W["addprox_at_m"] = prox, m
            if m:
                r = Dout / dT
                if r > max(W["ratio_bulk"], W["ratio_end"]): W["ratio_max_at_m"] = m
                kk = "ratio_bulk" if m >= 30 else "ratio_end"; W[kk] = max(W[kk], r)
                if dT >= H / 4:
                    if r > max(W["ratioR_bulk"], W["ratioR_end"]): W["ratioR_max_at_m"] = m
                    W["ratioR_" + kk[6:]] = max(W["ratioR_" + kk[6:]], r)
                for c, arr in cross.items(): arr[On[atau[On] > c * dT]] = True
        if m:
            ph = "bulk" if m >= 30 else "end"
            W["add_minus_del_" + ph] = max(W["add_minus_del_" + ph], (best_add - best_del) / logn)
            W["swap_minus_del_" + ph] = max(W["swap_minus_del_" + ph], (best_sw - best_del) / logn)
        if step % every == 0 or m <= 30:
            S["trace"].append([step, k, m, round(best_del / logn, 5), round(best_add / logn, 5), round(best_sw / logn, 5),
                               round(dT, 5) if m else None, round(Dout, 5)])

    res = IC.ls0_path(P, list(range(p)), P.S0, diag_every=1, diag_fn=diag)
    mv = [t for (t, _, _, _) in res["moves"]]
    ell = IC.ell_cap(n, p); cap = ell + p
    qs = lambda x, qq: float(np.quantile(x, qq)) if len(x) else None
    mx = lambda x: float(max(x)) if len(x) else None
    out = dict(p=p, n=n, seed=seed, q=q, rb=rb, rw=rw, rng_seed=30011 * seed + p + 7 * n, design="iid-rows S5 (Bartlett)",
               alpha=math.log(p) / logn, p_over_n=p / n, steps=len(mv), moves=len(mv),
               n_delN=mv.count("delN"), n_delT=mv.count("delT"), n_addN=mv.count("addN"), n_addT=mv.count("addT"),
               n_swapN=mv.count("swapN"), n_swapT=mv.count("swapT"), final_is_S0=res["final_is_S0"],
               pure_deletion=(mv.count("delN") == len(mv)), final_size=len(res["final"]),
               final_extra=sorted(set(res["final"]) - S0), final_missing=sorted(S0 - set(res["final"])),
               ell_n=ell, cap_MR1=cap, moves_minus_cap=len(mv) - cap,
               first_nondel=(next((i for i, x in enumerate(mv) if x != "delN"), None)),
               nondel_moves=[[i, x] for i, x in enumerate(mv) if x != "delN"][:50],
               info={k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in res["info"].items()}, **W,
               jumpH_bins=BINS_H[1:-1].tolist(), jumpH_hist_out=S["hH_out"].tolist(), jumpH_hist_ret=S["hH_ret"].tolist(),
               jumpH_out_n=len(S["joH"]), jumpH_out_max=mx(S["joH"]), jumpH_out_q99=qs(S["joH"], .99),
               jumpH_ret_max=mx(S["jrH"]), jumpH_ret_q99=qs(S["jrH"], .99),
               jump_bins=BINS[1:-1].tolist(), jump_hist_out=S["hist_out"].tolist(), jump_hist_ret=S["hist_ret"].tolist(),
               jump_out_n=len(S["jo"]), jump_out_max=mx(S["jo"]), jump_out_q99=qs(S["jo"], .99), jump_out_q50=qs(S["jo"], .5),
               jump_ret_max=mx(S["jr"]), jump_ret_q99=qs(S["jr"], .99),
               cross_c1=int(cross[1.0].sum()), cross_c1p5=int(cross[1.5].sum()), cross_c2=int(cross[2.0].sum()),
               trace=S["trace"], build_s=round(t_build, 1), wall_s=round(time.time() - t0, 1))
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    p, n, seed = int(a[0]), int(float(a[1])), int(a[2])
    kw = {}
    if len(a) > 3: kw["q"] = int(a[3])
    if len(a) > 4: kw["rb"] = float(a[4])
    if len(a) > 5: kw["rw"] = float(a[5])
    print(json.dumps(run(p, n, seed, **kw), default=lambda x: None))
