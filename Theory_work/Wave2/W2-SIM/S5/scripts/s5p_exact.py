"""W2-SIM family S5, experiment E-S5P(i): exact-Gram block compound symmetry at finite n with p up to n/2.
Scorer bcs_core.py imported UNCHANGED from the ticket snapshot (W2-FAC-S5, tickets_20261109T0943).
Path rule = W2-FAC-S5 numerics/s1_path.py (uncapped production search from T0 = [p], best of best deletion / best
addition / best candidate swap (bcs_core.Path._swaps: top-J deletions x all outside, all retained x top-J additions, all
same-group pairs), stop when no strictly positive move), with ONE change for cost: the candidate-swap scan is evaluated
at every step when p <= SWAP_ALL_P (default 5000) and otherwise only at "swap checkpoints" (every step with
m <= 100 retained nulls, plus every ceil(p/400)-th step). Steps without a swap scan choose between deletion and
addition only; this is recorded (swap_checked_steps / steps). With swaps at every step the move sequence is identical
to s1_path.py (validated: S5/validation/).

Recorded (noise-space statistics from bcs_core.Path.noise_tau(); tau = tau_{l | T minus l}):
* moves by type, final_is_S0, pure_deletion, MR1 cap a_n = ceil(log2(n+p+1)) + |S~0| with S~0 = T0 = [p]; moves - cap;
* margins (units log n): best_add - best_del (every step), best_swap - best_del (checked steps), by phase m >= 30 / m < 30;
* deletion level d_T = min |tau| over retained nulls; nonargmin = # deletions whose chosen null is not argmin |tau|;
* Dout = max |tau| over outside nulls; ratio Dout/d_T: max by phase and the m where attained (raw: ratio_*; restricted to
  states with d_T >= H/4: ratioR_*, since the ratio is meaningless while d_T ~ 0);
* add-threshold proximity: Dout / sqrt(2 Delta_k), Delta_k = log((2p-k)/k) + 0.5 log(n+1) (deletion gain ~ Delta_k - tau^2/2,
  addition profitable roughly when tau^2 > 2 Delta); max over path;
* within-group jumps: when null j (group g) is deleted at step t, for every other member l of g (null, retained or
  outside) jump_l := |tau_l(t+1)| - |tau_l(t)|. Reported (a) in units of H = sqrt(2 log 2p) for all events
  (histogram over BINS_H, max, q99), and (b) in units of the deletion level d_j := |tau_j(t)| only for events with
  d_j >= H/4 (early deletions have d_j ~ 0, where the ratio is meaningless): histogram over BINS, max, q99, counts;
  separately for outside (previously deleted) and retained mates; the global (e_T) contribution is included (it is
  the actual change of the statistic); dA = same for the group part A alone (units d_j, events d_j >= H/4);
* crossings: distinct deleted nulls l that at some later step have |tau_l| > current d_T (c = 1, 1.5, 2);
* global error: kappa0 |e_T| / H, H = sqrt(2 log 2p), max over m >= 30 and m < 30 (as E-S5CC, centre only).
usage: python s5p_exact.py p n seed [q rb rw] [SWAP_ALL_P]
"""
import os, sys, math, json, time
TICK = os.environ.get("TICKETS")
sys.path.insert(0, (TICK + "/Theory_work/Wave2/W2-FAC-S5/numerics") if TICK else os.environ["BCS_CORE_DIR"])
import numpy as np
import bcs_core as B

a = sys.argv[1:]
p, n, seed = int(a[0]), int(float(a[1])), int(a[2])
q = int(a[3]) if len(a) > 3 else 5
rb = float(a[4]) if len(a) > 4 else .3
rw = float(a[5]) if len(a) > 5 else .7
SWAP_ALL_P = int(a[6]) if len(a) > 6 else 5000
J = 12
t0 = time.time()
rng = np.random.default_rng(10007 * seed + p)
grp = np.arange(p) // q
P = B.BCS(n, grp, rb, rw, B.layout(p, q, s0=4), rng)
S0 = set(P.S0.tolist())
isnull = np.ones(p, bool); isnull[P.S0] = False
path = B.Path(P, np.ones(p, bool))
logn = math.log(n)
k0 = 1 / math.sqrt(1 - rb); H = math.sqrt(2 * math.log(2 * p))
ell = int(math.ceil(math.log2(n + p + 1))); cap = ell + p
every = max(1, math.ceil(p / 400))
# group membership lists
order = np.argsort(grp, kind="stable"); gstart = np.searchsorted(grp[order], np.arange(grp.max() + 2))
members = lambda g: order[gstart[g]:gstart[g + 1]]
BINS = np.array([-np.inf, -1.0, -0.5, -0.25, -0.1, 0.0, 0.1, 0.25, 0.5, 1.0, 1.5, 2.0, np.inf])
BINS_H = np.array([-np.inf, -0.5, -0.25, -0.1, -0.05, 0.0, 0.05, 0.1, 0.25, 0.5, 1.0, np.inf])
hist_out = np.zeros(len(BINS) - 1, np.int64); hist_ret = np.zeros(len(BINS) - 1, np.int64)
hH_out = np.zeros(len(BINS_H) - 1, np.int64); hH_ret = np.zeros(len(BINS_H) - 1, np.int64)
jo_all, jr_all, dA_all, joH, jrH = [], [], [], [], []
deleted_once = np.zeros(p, bool); cross = {1.0: np.zeros(p, bool), 1.5: np.zeros(p, bool), 2.0: np.zeros(p, bool)}
W = dict(add_minus_del_bulk=-np.inf, add_minus_del_end=-np.inf, swap_minus_del_bulk=-np.inf, swap_minus_del_end=-np.inf,
         best_add_max=-np.inf, ratio_bulk=0.0, ratio_end=0.0, ratio_max_at_m=None, addprox_max=0.0, addprox_at_m=None,
         eT_bulk=0.0, eT_end=0.0, nonargmin=0, dellevel_over_sqrt2D_max=0.0, ratioR_bulk=0.0, ratioR_end=0.0, ratioR_max_at_m=None)
mv = []; swap_checked = 0; step = 0; pend = None; trace = []
while True:
    m = int(np.sum(isnull & path.inT))
    do_sw = (p <= SWAP_ALL_P) or (m <= 100) or (step % every == 0)
    G = path.gains(swaps=do_sw, J=J)
    swap_checked += int(do_sw)
    Tidx, gdel, Oidx, gadd = G["Tidx"], G["gdel"], G["Oidx"], G["gadd"]
    sw, sj, sl = G["swap"]
    best_del = float(gdel.max()) if len(gdel) else -np.inf
    best_add = float(gadd.max()) if len(gadd) else -np.inf
    bestv = max(best_del, best_add, sw)
    nt = path.noise_tau(); tau = nt["tau"]; A = nt["A"]
    atau = np.abs(tau)
    # jumps caused by the previous deletion
    if pend is not None:
        j, dj, mates, prev_abs, prev_A, was_out = pend
        dabs = atau[mates] - prev_abs
        jH = dabs / H
        hH_out += np.histogram(jH[was_out], BINS_H)[0]; hH_ret += np.histogram(jH[~was_out], BINS_H)[0]
        joH.extend(jH[was_out].tolist()); jrH.extend(jH[~was_out].tolist())
        if dj >= H / 4:
            jump = dabs / dj
            dA = (np.abs(A[mates]) - np.abs(prev_A)) / dj
            jo, jr = jump[was_out], jump[~was_out]
            hist_out += np.histogram(jo, BINS)[0]; hist_ret += np.histogram(jr, BINS)[0]
            jo_all.extend(jo.tolist()); jr_all.extend(jr.tolist()); dA_all.extend(dA.tolist())
        pend = None
    retN = Tidx[isnull[Tidx]]; outN = Oidx[isnull[Oidx]]
    k = path.k
    dT = float(atau[retN].min()) if len(retN) else np.nan
    Dk = math.log((2 * p - k) / k) + 0.5 * math.log(n + 1) if k >= 1 else np.nan
    if len(retN):
        W["dellevel_over_sqrt2D_max"] = max(W["dellevel_over_sqrt2D_max"], dT / math.sqrt(2 * Dk))
    if len(outN):
        Dout = float(atau[outN].max())
        prox = Dout / math.sqrt(2 * Dk)
        if prox > W["addprox_max"]: W["addprox_max"], W["addprox_at_m"] = prox, m
        if len(retN):
            ratio = Dout / dT
            key = "ratio_bulk" if m >= 30 else "ratio_end"
            if ratio > max(W["ratio_bulk"], W["ratio_end"]): W["ratio_max_at_m"] = m
            W[key] = max(W[key], ratio)
            if dT >= H / 4:
                if ratio > max(W["ratioR_bulk"], W["ratioR_end"]): W["ratioR_max_at_m"] = m
                W["ratioR_" + key[6:]] = max(W["ratioR_" + key[6:]], ratio)
            for c, arr in cross.items():
                arr[outN[atau[outN] > c * dT]] = True
    else:
        Dout = 0.0
    eT = k0 * abs(nt["e_T"]) / H
    if m >= 30: W["eT_bulk"] = max(W["eT_bulk"], eT)
    else: W["eT_end"] = max(W["eT_end"], eT)
    W["best_add_max"] = max(W["best_add_max"], best_add)
    if m > 0:
        ph = "bulk" if m >= 30 else "end"
        W["add_minus_del_" + ph] = max(W["add_minus_del_" + ph], (best_add - best_del) / logn)
        if do_sw and sw > -np.inf:
            W["swap_minus_del_" + ph] = max(W["swap_minus_del_" + ph], (sw - best_del) / logn)
    if step % every == 0 or m <= 30:
        trace.append([step, k, m, round(best_del / logn, 5), round(best_add / logn, 5),
                      (round(sw / logn, 5) if (do_sw and sw > -np.inf) else None), round(dT, 5) if len(retN) else None,
                      round(Dout, 5), round(eT, 5)])
    if not bestv > 0:
        break
    if bestv == best_del:
        j = int(Tidx[int(np.argmax(gdel))])
        if isnull[j] and len(retN):
            if int(retN[np.argmin(atau[retN])]) != j: W["nonargmin"] += 1
            mates = members(grp[j]); mates = mates[(mates != j) & isnull[mates]]
            if len(mates) and atau[j] > 0:
                pend = (j, float(atau[j]), mates, atau[mates].copy(), A[mates].copy(), ~path.inT[mates])
        mv.append("-N" if isnull[j] else "-T")
        path.apply("del", j=j)
    elif bestv == best_add:
        l = int(Oidx[int(np.argmax(gadd))])
        mv.append("+N" if isnull[l] else "+T")
        path.apply("add", l=l)
    else:
        mv.append("sw" + ("T" if (sj in S0 or sl in S0) else "N"))
        path.apply("swap", j=sj, l=sl)
    step += 1
    if step > 3 * p:
        break
final = set(np.flatnonzero(path.inT).tolist())
qs = lambda x, qq: float(np.quantile(x, qq)) if len(x) else None
out = dict(p=p, n=n, seed=seed, q=q, rb=rb, rw=rw, rng_seed=10007 * seed + p, alpha=math.log(p) / logn,
           p_over_n=p / n, swap_all_p=SWAP_ALL_P, J=J, steps=step, swap_checked_steps=swap_checked,
           moves=len(mv), n_delN=mv.count("-N"), n_delT=mv.count("-T"), n_addN=mv.count("+N"), n_addT=mv.count("+T"),
           n_swapN=mv.count("swN"), n_swapT=mv.count("swT"), final_is_S0=(final == S0),
           pure_deletion=(mv.count("-N") == len(mv)), final_size=len(final), ell_n=ell, cap_MR1=cap, moves_minus_cap=len(mv) - cap,
           first_nondel=(next((i for i, x in enumerate(mv) if x != "-N"), None)), **W,
           jumpH_bins=BINS_H[1:-1].tolist(), jumpH_hist_out=hH_out.tolist(), jumpH_hist_ret=hH_ret.tolist(),
           jumpH_out_n=len(joH), jumpH_out_max=(max(joH) if joH else None), jumpH_out_q99=qs(joH, .99),
           jumpH_ret_max=(max(jrH) if jrH else None), jumpH_ret_q99=qs(jrH, .99),
           jump_bins=BINS[1:-1].tolist(), jump_hist_out=hist_out.tolist(), jump_hist_ret=hist_ret.tolist(),
           jump_out_n=len(jo_all), jump_out_max=(max(jo_all) if jo_all else None), jump_out_q99=qs(jo_all, .99),
           jump_out_q50=qs(jo_all, .5), jump_ret_max=(max(jr_all) if jr_all else None), jump_ret_q99=qs(jr_all, .99),
           dA_max=(max(dA_all) if dA_all else None), dA_q99=qs(dA_all, .99),
           cross_c1=int(cross[1.0].sum()), cross_c1p5=int(cross[1.5].sum()), cross_c2=int(cross[2.0].sum()),
           trace=trace, wall_s=round(time.time() - t0, 1))
print(json.dumps(out, default=lambda x: None if (isinstance(x, float) and not math.isfinite(x)) else x))
