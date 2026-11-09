"""W2-SIM family S5, experiment E-S5CC: instrumented copy of W2-FAC-S5 numerics/s3_cc.py (snapshot
tickets_20261109T0943, sha256 2886c060...8c928b3), scorer bcs_core.py imported UNCHANGED from the ticket snapshot
(sha256 b6c0fb53...ed98c9).

The loop, RNG seeding (default_rng(10007*seed + p)), deletion rule and every original output field are copied verbatim
from s3_cc.py (validated identical: S5/validation/). The only change inside the loop is gains(swaps=_dosw) instead of
gains(swaps=False) at swap checkpoints (deletion/addition gains are computed by identical code either way; the swap value
is only recorded, never acted on). Added, read-only (R01 design review fixes applied):
  H := sqrt(2 log 2p)  (NOT H_q);  r(T) := kappa0 * max(vals) / H with vals = (|e_T|, max_{retained null j}|e_{T minus j}|)
  (the same vals as cc_max);  rT(T) := kappa0 |e_T| / H (centre only);  m := # retained nulls at T.
  phases: bulk m >= 30, mid 30 > m >= 5, end m < 5 (incl. m = 0 = S0); visited_states counts states per phase;
  every phase statistic is null if the phase was not visited (deletion path stopped early).
  r_bulk/r_mid/r_end, rT_*; band maxima over m in [30,100), ..., [1e5, inf); r over m >= p/10 and m >= sqrt p;
  m_checkpoints {m: [r, rT]} (single states) at m in (30, 50, 100, ..., 1e5);
  admissible delta: delta(T) := 1 - (H_q + kappa0 max(vals))^2 / Lambda_k, Lambda_k = log n + 2 log((2p-k)/(k+1))
  (CC_n(delta) holds along the path iff delta <= min_T delta(T)); delta_adm_min (+ bulk/end), delta_baseline_e0 = the
  same with e = 0 (deterministic: H_q and Lambda_k only);
  competing moves (NOT acted on: the path is the deletion-only path Pi of s3_cc.py): max (best_add - best_del)/log n by
  phase, # steps with best_add >= best_del, # with best_add > 0; candidate-swap value (bcs_core Path._swaps) at
  checkpoints (every ceil(p/400)-th step and every step with m <= 100): max (best_swap - best_del)/log n, # steps with
  best_swap >= best_del; terminal state (m = 0): best truth deletion, best addition, best candidate swap, improvable flag;
  deletion_path_complete (= reached_S0, i.e. the deletion-only path reached S0; NOT a certification of the LS0 path),
  fail_reason, del_sequence_sha1 (digest of the deleted-index sequence);
  imbalance I(m) := #(tau > 0) - #(tau < 0) over retained nulls, tau = tau_{j | T minus j} (bcs_core noise_tau()["tau"]),
  at m = 30, 10, 5, max |I| over m <= 5 and over 5 < m <= 30 (null if not visited); I_A same with the group part A;
  end_trace: for m <= 30: [m, I, I_A, kappa0*e_T/H (signed), r(T)] (unrounded).
usage: python s5cc.py p n seed [q rb rw]   -> one JSON line on stdout
"""
import os, sys, math, json, time
TICK = os.environ.get("TICKETS")
sys.path.insert(0, (TICK + "/Theory_work/Wave2/W2-FAC-S5/numerics") if TICK else os.environ["BCS_CORE_DIR"])
import numpy as np
import bcs_core as B

t0 = time.time()
p, n, seed = int(sys.argv[1]), int(float(sys.argv[2])), int(sys.argv[3])
q = int(sys.argv[4]) if len(sys.argv) > 4 else 5
rb = float(sys.argv[5]) if len(sys.argv) > 5 else .3
rw = float(sys.argv[6]) if len(sys.argv) > 6 else .7
rng = np.random.default_rng(10007 * seed + p)
P = B.BCS(n, np.arange(p) // q, rb, rw, B.layout(p, q, s0=4), rng)
isnull = np.ones(p, bool); isnull[P.S0] = False
path = B.Path(P, np.ones(p, bool))
k0 = 1 / math.sqrt(1 - rb); Hq = math.sqrt(2 * math.log(2 ** q * p) + 2 * math.log(math.log(n)))
logn = math.log(n)
# --- added (R01 fixes: explicit phase chain, visitation flags, admissible delta, add/swap/endpoint checks, digest)
import hashlib
H = math.sqrt(2 * math.log(2 * p))
NEG = -float("inf")
r_b = r_m = r_e = rT_b = rT_m = rT_e = None; r_b_at = None
vis = dict(bulk=0, mid=0, end=0)
BANDS = [30, 100, 300, 1000, 3000, 10000, 30000, 100000]
band = [None] * len(BANDS)
MCHK = (30, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000)
mtrace = {}; r_p10 = None; r_sq = None; m_p10 = p / 10.0; m_sq = math.sqrt(p)
Iat = {}; IAat = {}; maxI_end = None; maxI_mid = None; trace = []
dmax = dict(all=float("inf"), bulk=float("inf"), end=float("inf")); dbase = float("inf"); dmax_at = None
add_md = dict(bulk=NEG, mid=NEG, end=NEG); add_viol = 0; add_pos = 0
sw_md = dict(bulk=NEG, mid=NEG, end=NEG); sw_viol = 0; sw_checked = 0; every = max(1, math.ceil(p / 400))
term = None; fail_reason = None; dig = hashlib.sha1(); stepno = 0
mx = lambda a, b: b if a is None else max(a, b)
# ---
marg = 1e9; marg_at = None; cc_max = 0.0; cc_bulk = 0.0; gain_err = 0.0; pure = True; steps = 0; at = None
while True:
    _m0 = int(np.sum(isnull & path.inT)); _dosw = (stepno % every == 0) or (_m0 <= 100)  # added (swap checkpoint)
    G = path.gains(swaps=_dosw)  # added: swaps=_dosw instead of False; gdel/gadd are computed identically either way
    sw_checked += int(_dosw); stepno += 1
    nt = path.noise_tau()
    Tidx = G["Tidx"]; retN = Tidx[isnull[Tidx]]
    vals = [abs(nt["e_T"])] + ([float(np.max(np.abs(nt["eR"][retN])))] if len(retN) else [])
    cc = k0 * max(vals) / Hq
    if cc > cc_max: cc_max, at = cc, len(retN)
    kk = path.k
    mg = (math.log(n) + 2 * math.log((2 * p - kk) / (kk + 1)) - (Hq + k0 * max(vals)) ** 2) / logn
    if mg < marg: marg, marg_at = mg, len(retN)
    if len(retN) >= 30: cc_bulk = max(cc_bulk, cc)
    # --- added (read-only use of vals / nt / G)
    m = len(retN)
    rr = k0 * max(vals) / H; rT = k0 * abs(nt["e_T"]) / H
    ph = "bulk" if m >= 30 else ("mid" if m >= 5 else "end")
    vis[ph] += 1
    if ph == "bulk":
        if r_b is None or rr > r_b: r_b, r_b_at = rr, m
        rT_b = mx(rT_b, rT)
        bi = max(i for i, lo in enumerate(BANDS) if m >= lo); band[bi] = mx(band[bi], rr)
    elif ph == "mid":
        r_m = mx(r_m, rr); rT_m = mx(rT_m, rT)
    else:
        r_e = mx(r_e, rr); rT_e = mx(rT_e, rT)
    if m >= m_p10: r_p10 = mx(r_p10, rr)
    if m >= m_sq: r_sq = mx(r_sq, rr)
    if m in MCHK: mtrace[str(m)] = [rr, rT]
    Lam_k = math.log(n) + 2 * math.log((2 * p - kk) / (kk + 1))
    dl = 1 - (Hq + k0 * max(vals)) ** 2 / Lam_k
    if dl < dmax["all"]: dmax["all"], dmax_at = dl, m
    dmax["bulk" if m >= 30 else "end"] = min(dmax["bulk" if m >= 30 else "end"], dl)
    dbase = min(dbase, 1 - Hq ** 2 / Lam_k)
    if m <= 30:
        I = int(np.sum(nt["tau"][retN] > 0) - np.sum(nt["tau"][retN] < 0))
        IA = int(np.sum(nt["A"][retN] > 0) - np.sum(nt["A"][retN] < 0))
        if m in (30, 10, 5): Iat[m] = I; IAat[m] = IA
        if m <= 5: maxI_end = mx(maxI_end, abs(I))
        else: maxI_mid = mx(maxI_mid, abs(I))
        trace.append([m, I, IA, k0 * float(nt["e_T"]) / H, rr])
    bd = float(G["gdel"].max()) if len(G["gdel"]) else NEG
    ba = float(G["gadd"].max()) if len(G["gadd"]) else NEG
    bs = G["swap"][0] if _dosw else None
    if m > 0:
        add_md[ph] = max(add_md[ph], (ba - bd) / logn); add_viol += int(ba >= bd); add_pos += int(ba > 0)
        if bs is not None and bs > NEG:
            sw_md[ph] = max(sw_md[ph], (bs - bd) / logn); sw_viol += int(bs >= bd)
    else:
        term = dict(best_truth_del=bd, best_add=ba, best_swap=bs, improvable=bool(max(bd, ba, bs if bs is not None else NEG) > 0))
    # ---
    if len(retN):
        k = path.k
        Dk = math.log((2 * p - k) / k) + 0.5 * math.log(n + 1)
        approx = Dk - 0.5 * nt["tau"][retN] ** 2
        exact = G["gdel"][isnull[Tidx]]
        gain_err = max(gain_err, float(np.max(np.abs(exact - approx))) / logn)
        j = int(Tidx[int(np.argmax(G["gdel"]))])
        if not isnull[j] or G["gdel"].max() <= 0:
            fail_reason = "truth_deletion_is_best" if not isnull[j] else "best_null_deletion_nonpositive"  # added
            pure = False; break
        dig.update(str(j).encode() + b",")  # added
        path.apply("del", j=j); steps += 1
    else:
        break
out = dict(p=p, n=n, seed=seed, alpha=math.log(p) / logn, steps=steps, reached_S0=pure,
           cc_max=cc_max, cc_max_at_m=at, cc_bulk_m30=cc_bulk, gain_approx_err_over_logn=gain_err,
           CCdelta_margin_over_logn=marg, margin_at_m=marg_at, c_needed_for_alpha=1 / math.sqrt(2 * math.log(p) / logn) - 1)
fin = lambda x: x if (x is None or math.isfinite(x)) else None
out.update(q=q, rb=rb, rw=rw, rng_seed=10007 * seed + p, H=H, kappa0=k0, Hq=Hq,
           deletion_path_complete=pure, fail_reason=fail_reason, m_final=int(np.sum(isnull & path.inT)),
           visited_states=vis, del_sequence_sha1=dig.hexdigest(),
           r_bulk=r_b, r_bulk_at_m=r_b_at, r_mid=r_m, r_end=r_e, rT_bulk=rT_b, rT_mid=rT_m, rT_end=rT_e,
           band_lo=BANDS, band_max=band, r_m_ge_p10=r_p10, r_m_ge_sqrtp=r_sq, m_checkpoints=mtrace,
           delta_adm_min=fin(dmax["all"]), delta_adm_min_at_m=dmax_at, delta_adm_min_bulk=fin(dmax["bulk"]),
           delta_adm_min_end=fin(dmax["end"]), delta_baseline_e0=fin(dbase),
           add_minus_del_max=dict((k_, fin(v)) for k_, v in add_md.items()), add_ge_del_steps=add_viol, add_positive_steps=add_pos,
           swap_minus_del_max=dict((k_, fin(v)) for k_, v in sw_md.items()), swap_ge_del_steps=sw_viol,
           swap_checked_steps=sw_checked, swap_checkpoint_every=every, terminal=term,
           I30=Iat.get(30), I10=Iat.get(10), I5=Iat.get(5), IA30=IAat.get(30), IA10=IAat.get(10), IA5=IAat.get(5),
           maxabsI_m_le5=maxI_end, maxabsI_5_lt_m_le30=maxI_mid, end_trace=trace,
           wall_s=round(time.time() - t0, 2))
print(json.dumps(out, default=lambda x: None))
