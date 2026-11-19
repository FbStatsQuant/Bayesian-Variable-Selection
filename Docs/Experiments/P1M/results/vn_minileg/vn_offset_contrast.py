#!/usr/bin/env python3
"""vn_offset_contrast.py -- the V-N mini-leg's N contrast of the offset measurement (MINILEG_PREREG.md section 5). Stdlib only (python3.9), deterministic, read-only.
The registered precision_offset.py (sha256 cbbc23012e6900ff7798267cc7325816ad0b8312ec6e26fd09972adc9780d300, UNEDITED) writes offset_per_fit.csv and offset.json; it builds its N contrasts
only for I_max = 3 cells ((10^4, 1, 3) - (2500, 1, 3) at k = 64). This script reads offset_per_fit.csv and computes the SAME contrast, with the registered formulas (dataset = the
unit; per-dataset mean over replicates; paired by dataset; t interval, df = datasets - 1, the registered t table), for ANY pair of cells, in particular the FROZEN configuration
(10^4, 1, 0) - (2500, 1, 0). It reports the two pre-declared reference values (no pass/fail):  H0: contrast = 0 (no N dependence of V's log Z-hat);  H-N: the V - T offset is a finite-N
effect proportional to 1/N, i.e. contrast = -(1 - N0/N1) * delta_{N0} (delta of the N0 cell, same datasets): +0.75 * |delta_2500| for a negative delta.
  vn_offset_contrast.py --per-fit offset_per_fit.csv --out DIR [--pair 10000,1,0:2500,1,0 ...] [--k 64]
Default pairs: the frozen-configuration pair and the registered I_max = 3 pair."""
import argparse, csv, json, math, os, sys

T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145,
        15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 25: 2.060, 30: 2.042}     # the registered table of precision_offset.py


def tq(df):
    if df < 1:
        return float("nan")
    ks = sorted(T975)
    return T975[max(k for k in ks if k <= df)] if df < 30 else (2.042 if df == 30 else 1.96)


def mean(xs):
    return sum(xs) / len(xs)


def sd(xs):
    return math.sqrt(sum((x - mean(xs)) ** 2 for x in xs) / (len(xs) - 1)) if len(xs) > 1 else float("nan")


def summ(vals):
    n = len(vals); m = mean(vals); s = sd(vals); se = s / math.sqrt(n) if n > 1 else float("nan"); h = tq(n - 1) * se if n > 1 else float("nan")
    return {"n": n, "mean": m, "sd": s, "se": se, "lo": m - h, "hi": m + h, "neg": sum(v < 0 for v in vals)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--per-fit", required=True); ap.add_argument("--out", required=True); ap.add_argument("--k", type=int, default=64)
    ap.add_argument("--pair", action="append", default=None, help="N1,m,I:N0,m,I (the contrast cell1 - cell0); default the frozen and the I_max = 3 pairs")
    a = ap.parse_args(argv)
    pairs = a.pair or ["10000,1,0:2500,1,0", "10000,1,3:2500,1,3"]
    D = {}
    rows = list(csv.reader(open(a.per_fit)))
    # DEFECT of the registered precision_offset.py, named (not edited): its per-fit CSV rows carry a `src` field (ovl | prec) after I_max that its header lacks, so every
    # column after I_max is shifted by one in the file. Both layouts are read by position: [run_id, dataset, N, m, I_max, (src,) rep, Rp, k, L, D, ...]. Only src = prec cells enter.
    for r in rows[1:]:
        shifted = r[5] in ("ovl", "prec")
        if shifted and r[5] != "prec":
            continue
        off = 1 if shifted else 0
        k, Dv = int(r[7 + off]), float(r[9 + off])
        if k != a.k:
            continue
        D.setdefault((int(r[2]), int(r[3]), int(r[4])), {}).setdefault(r[1], []).append(Dv)
    out = {"k": a.k, "contrasts": []}
    lines = ["# V-N mini-leg: N contrast of the offset measurement at k = %d (no pass/fail)" % a.k, "| cell1 - cell0 | datasets | delta(cell0) | delta(cell1) | contrast | se | 95% t-CI | neg | H0 = 0 | H-N prediction |", "|---|---|---|---|---|---|---|---|---|---|"]
    for p in pairs:
        c1, c0 = [tuple(int(x) for x in q.split(",")) for q in p.split(":")]
        if c1 not in D or c0 not in D:
            lines.append("| %s - %s | cells missing | | | | | | | | |" % (c1, c0)); out["contrasts"].append({"pair": p, "status": "NOT_COMPUTABLE"}); continue
        ds = sorted(set(D[c1]) & set(D[c0]))
        d1 = {d: mean(D[c1][d]) for d in ds}; d0 = {d: mean(D[c0][d]) for d in ds}
        vals = [d1[d] - d0[d] for d in ds]; s = summ(vals); delta0 = mean([d0[d] for d in ds]); delta1 = mean([d1[d] for d in ds])
        pred = -(1.0 - c0[0] / float(c1[0])) * delta0
        ex0 = "excluded" if (s["lo"] > 0 or s["hi"] < 0) else "not excluded"
        exN = "excluded" if (s["lo"] > pred or s["hi"] < pred) else "not excluded"
        out["contrasts"].append({"pair": p, "datasets": ds, "delta_cell0": delta0, "delta_cell1": delta1, "contrast": s, "per_dataset": {d: round(v, 6) for d, v in zip(ds, vals)}, "H_N_prediction": pred, "H0_by_CI": ex0, "H_N_by_CI": exN})
        lines.append("| %s - %s | %d | %+.5f | %+.5f | %+.5f | %.5f | %+.5f .. %+.5f | %d/%d | %s | %+.5f (%s) |" % (c1, c0, len(ds), delta0, delta1, s["mean"], s["se"], s["lo"], s["hi"], s["neg"], len(ds), ex0, pred, exN))
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "vn_offset_contrast.json"), "w"), indent=1)
    open(os.path.join(a.out, "vn_offset_contrast.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
