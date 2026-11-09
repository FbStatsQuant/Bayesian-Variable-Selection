"""r1_cs.py -- W2-SIM family PK, experiment R1: exact-Gram compound symmetry, closed-form start mode and uncapped LS0 path
at large n (pk_core, unchanged; same pipeline as W2-FAC-PK n1_scale.py).
  python r1_cs.py OUT.jsonl rho n frac LAYOUT REP [EXP (default R1; seeds depend on it)]
p = min(round(frac*n), n-2) as n1_scale.py; partition pk_core.cs_partition(p, B), B = min(isqrt n, isqrt p, 16)
(checked equal to the method's partition in W2-FAC-PK pk_selftest); start mode pk_core.start_mode_cs; path
pk_core.path_from (production local search, gain form, ties -> lexicographically smallest set); the callback adds
NaN guards, tie counts (exact equality of the best gain among the scanned candidates), the minimum winner margin among the
candidates pk_core evaluates (deletions, additions, swaps to the extreme outside z's), arrival at S0 and a move-limit flag.
"""
import sys
import time
import numpy as np
import pk_common as pc
import pk_core as pk


def run(rho, n, frac, layout, rep, exp="R1"):
    p = min(int(round(frac * n)), n - 2)
    seed = pc.cell_seed(exp, rho, n, frac, layout, rep)
    th = pc.theta_vec(p, layout)
    S0 = tuple(int(j) for j in np.flatnonzero(th))
    t0 = time.time()
    P = pk.make_cs(rho, th, n, seed)
    B = pk.block_size(n, p)
    blocks = pk.cs_partition(p, B)
    sm = pk.start_mode_cs(P, blocks)
    t1 = time.time()
    rec = dict(ties=0, arrival=None, min_margin=None, min_margin_scan=None)
    S0arr = np.array(S0)

    def cb(d):
        # called once per executed move, before the move (scan index d["nmoves"])
        G = [a for a in (d["Gd"], d["Ga"], np.ravel(d["Gs"])) if np.size(a)]
        allg = np.concatenate(G)
        if np.isnan(allg).any() or np.isposinf(allg).any() or not np.isfinite(d["psi"]) or d["psi"] <= 0:
            raise FloatingPointError(f"invalid gains at scan {d['nmoves']}")
        if int(np.sum(allg == d["best"])) > 1:
            rec["ties"] += 1
        fin = allg[np.isfinite(allg)]
        if fin.size >= 2:
            t2 = np.partition(fin, fin.size - 2)[-2:]
            mg = float(t2[1] - t2[0])
            if rec["min_margin"] is None or mg < rec["min_margin"]:
                rec["min_margin"], rec["min_margin_scan"] = mg, d["nmoves"]
        if rec["arrival"] is None and d["k"] == len(S0) and d["inT"][S0arr].all():
            rec["arrival"] = d["nmoves"]
    MAXM = 10 ** 7
    r = pk.path_from(P, sm["mode"], max_moves=MAXM, callback=cb)
    limited = r["n_moves"] >= MAXM
    if rec["arrival"] is None and r["final_is_S0"]:
        rec["arrival"] = r["n_moves"]
    t2 = time.time()
    K = P.K
    ell = pk.ell_cap(n, p)
    s = sm["size"]
    st = pc.move_stats(r["moves"])
    kh = r["k_hit"]
    return dict(exp=exp, rho=rho, n=n, frac=frac, p=p, K=K, B=B, layout=layout, rep=rep, seed=seed, S0=list(S0),
                start_size=s, saturated=(s == K), start_has_S0=set(S0) <= set(sm["mode"]),
                start_truths=len(set(S0) & set(sm["mode"])), size_ties=sm["n_size_ties"], within_ties=sm["within_ties"],
                m_star=r["n_moves"], m_star_over_K=r["n_moves"] / K, m_star_over_start=r["n_moves"] / s,
                final_is_S0=r["final_is_S0"], final_size=len(r["final"]), limited=limited, certified=not limited,
                arrival=rec["arrival"], scan_ties=rec["ties"], min_margin_reduced=rec["min_margin"],
                min_margin_scan=rec["min_margin_scan"],
                k_hit=kh, ell=ell, cap_MR1=ell + s, cap_2=ell + 2 * s,
                MR1_scores=(kh is not None and kh <= ell + s), cap2_scores=(kh is not None and kh <= ell + 2 * s),
                excess_over_MR1=(kh - ell - s) if kh is not None else None,
                W_minus_ell_s0=st["lead_swaps"] - ell - len(S0),
                moves_rle=pc.rle(r["moves"]), t_start=round(t1 - t0, 2), t_path=round(t2 - t1, 2),
                module_sha=pc.module_sha(), **st)


if __name__ == "__main__":
    outf, rho, n, frac, layout, rep = sys.argv[1:7]
    res = run(float(rho), int(n), float(frac), layout, int(rep), *(sys.argv[7:8]))
    pc.write_jsonl(outf, res)
    print({k: res[k] for k in ("rho", "n", "p", "rep", "layout", "start_size", "K", "lead_swaps", "m_star", "k_hit",
                               "cap_MR1", "final_is_S0", "t_start", "t_path")}, flush=True)
