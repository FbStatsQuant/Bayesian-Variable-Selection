"""N2 (W2-FAC-PK): per-move diagnostics of the LS0 path from the saturated start (exact-Gram CS, p > K).
Records, at every visited T: k, move type, centre x_T (xi-units), M_T (nu*n*k1^2/(al*psi)), Delta_k (deletion size
term dw), d = min_{retained null}|xi - x_T|, the max over outside nulls of (1-g_{k+1}) M_T tau^2 split into
LEFTOVERS (outside at the end of the swap phase and never retained since) and HOLE (removed by a move), and the
margins Delta_k - those maxima.  Also start-mode structure: rank of excluded nulls inside their block, how many of the
L lowest nulls are excluded, x at T_0, and at the end of the swap phase the band check (every null with
M(1-g)tau^2 > Delta_K retained).
usage: python n2_diag.py rho n p seed OUT.json"""
import sys, json, math
import numpy as np
import pk_core as pk

rho, n, p, seed, outf = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
th = np.zeros(p); S0 = [2, 26, 53, 75]; th[S0] = [1.4, 1.0, 1.8, 1.2]
P = pk.make_cs(rho, th, n, seed)
B = pk.block_size(n, p); blocks = pk.cs_partition(p, B)
sm = pk.start_mode_cs(P, blocks)
k1 = pk.xi_units(P)
isS0 = np.zeros(p, bool); isS0[S0] = True
null = ~isS0
st0 = np.zeros(p, bool); st0[list(sm["mode"])] = True
# start structure
xi = P.xi
excl = np.flatnonzero(~st0 & null)
low_rank_ok = 0
for C in blocks:
    C = np.array(C); Cn = C[null[C]]
    kept = Cn[st0[Cn]]; ex = Cn[~st0[Cn]]
    if len(ex) and len(kept):
        low_rank_ok += int(xi[ex].max() < xi[kept].min())
nb_mixed = sum(1 for C in blocks if (st0[np.array(C)] & null[np.array(C)]).any() and (~st0[np.array(C)] & null[np.array(C)]).any())
order = np.argsort(xi[null]); nulls = np.flatnonzero(null)
lowest = nulls[order[:50]]
start_info = dict(n=n, p=p, K=P.K, rho=rho, seed=seed, start=sm["size"], blocks_with_kept_and_excl=nb_mixed,
                  blocks_where_excluded_below_kept=low_rank_ok, lowest50_excluded=int((~st0[lowest]).sum()),
                  lowest10_excluded=int((~st0[lowest[:10]]).sum()))
rows = []
state = dict(in_swap=True, hole=np.zeros(p, bool), leftover=None, W=0)
def cb(d):
    inT, k, c, psi = d["inT"], d["k"], d["c"], d["psi"]
    MT = P.nu * n * k1 ** 2 / (P.al * psi)
    tau = (P.z - c) / k1            # = xi - x_T for nulls
    nn = np.flatnonzero(null)
    xT = float(np.median(xi[nn] - tau[nn]))
    ret = nn[inT[nn]]; out = nn[~inT[nn]]
    gk1 = P.be / (P.al + (k + 1) * P.be)
    q = (1 - gk1) * MT * tau ** 2
    dmin = float(np.min(np.abs(tau[ret]))) if len(ret) else None
    if state["leftover"] is None:
        lo = out; ho = np.array([], int)
    else:
        lo = out[state["leftover"][out]]; ho = out[state["hole"][out]]
    row = dict(i=d["nmoves"], k=k, xT=xT, MT=MT, Dk=d["dw"], d=dmin,
               qmax_left=float(q[lo].max()) if len(lo) else None, qmax_hole=float(q[ho].max()) if len(ho) else None,
               n_left=int(len(lo)), n_hole=int(len(ho)), best=d["best"],
               move=("-" if d["li"] is None else ("+" if d["jo"] is None else "s")))
    if d["jo"] is not None and d["li"] is not None:
        row.update(tau_in=float(tau[d["li"]]), tau_out=float(tau[d["jo"]]),
                   in_is_lowest_out=bool(abs(tau[d["li"]]) >= np.abs(tau[out]).max() - 1e-12),
                   out_is_nearest=bool(abs(tau[d["jo"]]) <= dmin + 1e-12))
        if state["leftover"] is not None: row["late_swap"] = True
    if row["move"] != "s" and state["leftover"] is None:
        # end of swap phase: freeze leftovers, band check
        lf = np.zeros(p, bool); lf[out] = True; state["leftover"] = lf
        gK1 = gk1
        start_info.update(W=d["nmoves"], x_W=xT, M_W=MT, Delta_K=d["dw"],
                          band_viol=int(np.sum(q[out] > d["dw"])), max_q_out=float(q[out].max()),
                          min_q_ret_null_far=float(q[ret].max()))
    if d["jo"] is not None and d["li"] is None and state["leftover"] is not None:
        state["hole"][d["jo"]] = True
    if d["jo"] is not None and d["li"] is not None:
        state["hole"][d["jo"]] = True
    rows.append(row)
r = pk.path_from(P, sm["mode"], callback=cb)
start_info.update(moves=r["n_moves"], final_is_S0=r["final_is_S0"], k_hit=r["k_hit"], summ=pk.summarize_moves(r["moves"]))
# margins in the deletion phase
dl = [x for x in rows if start_info.get("W") is not None and x["i"] >= start_info["W"]]
def mg(x):
    m = [v for v in (x["qmax_left"], x["qmax_hole"]) if v is not None]
    return x["Dk"] - max(m) if m else None
mgs = [(mg(x), x["k"]) for x in dl if mg(x) is not None]
start_info["min_margin_del_phase"] = min(mgs) if mgs else None
start_info["xT_range_del_phase"] = [min(x["xT"] for x in dl), max(x["xT"] for x in dl)] if dl else None
json.dump(dict(info=start_info, rows=rows[::max(1, len(rows) // 400)] + rows[-30:]), open(outf, "w"))
print(json.dumps(start_info))
