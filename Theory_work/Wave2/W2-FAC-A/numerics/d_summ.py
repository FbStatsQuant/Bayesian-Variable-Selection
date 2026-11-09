"""d_summ.py -- summarise D1_*_raw.jsonl files into a markdown table. usage: py -3.13 d_summ.py out.md file1 file2 ..."""
import sys, json
import numpy as np


def med(v):
    v = [x for x in v if x is not None]
    return float(np.median(v)) if v else float("nan")


def main():
    out = sys.argv[1]
    rows = []
    for fn in sys.argv[2:]:
        with open(fn) as f:
            rows += [json.loads(l) for l in f]
    keys = sorted({(r["design"], r["mode"], r["p"], r["n"], r["c"]) for r in rows})
    L = ["| design | mode | p | n | N | K | |S~0| med (min-max) | extras med | frac nulls in med | S0⊆S~0 | S~0=[p] | at K | moves med (max) | pure -N path | swaps tot | adds tot | -T tot | reach S0 | MR1 ok | ell_n ok | path NA fail (runs) | path TL fail | min del margin | lattice NA fail (sets) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        rr = [r for r in rows if (r["design"], r["mode"], r["p"], r["n"], r["c"]) == k]
        N = len(rr)
        ss = [r["start_size"] for r in rr]
        sw = sum(r["nswN>N"] + r["nswN>T"] + r["nswT>N"] + r["nswT>T"] for r in rr)
        ad = sum(r["n+N"] + r["n+T"] for r in rr)
        dT = sum(r["n-T"] for r in rr)
        latf = sum(r.get("lat_NA_fail", 0) for r in rr)
        lats = sum(r.get("lat_nsamp", 0) for r in rr)
        mm = [r.get("path_min_del_margin") for r in rr]
        L.append("| %s | %s | %d | %d | %d | %d | %g (%d-%d) | %g | %.2f | %d/%d | %d/%d | %d/%d | %g (%d) | %d/%d | %d | %d | %d | %d/%d | %d/%d | %d/%d | %d/%d | %d/%d | %.2f | %d/%d |" % (
            k[0], k[1], k[2], k[3], N, rr[0]["K"], med(ss), min(ss), max(ss), med([r["n_extra"] for r in rr]),
            med([r["frac_nulls_in"] for r in rr]), sum(r["n_missing"] == 0 for r in rr), N,
            sum(r["start_is_all"] for r in rr), N, sum(r["start_at_K"] for r in rr), N,
            med([r["unc_moves"] for r in rr]), max(r["unc_moves"] for r in rr),
            sum(r["path_pure_delN"] for r in rr), N, sw, ad, dT,
            sum(r["unc_final_eq_S0"] for r in rr), N, sum(r["MR1_ok"] for r in rr), N, sum(r["ell_ok"] for r in rr), N,
            sum((r.get("path_NA_fail") or 0) > 0 for r in rr), N, sum((r.get("path_TL_fail") or 0) > 0 for r in rr), N,
            min([m for m in mm if m is not None] or [float("nan")]), latf, lats))
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
