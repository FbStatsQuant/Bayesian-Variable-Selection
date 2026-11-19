#!/usr/bin/env python3
"""precision_offset.py -- the pre-declared MEASUREMENT of the V - T log Z-hat offset against N, m, I_max and R' (PREREG.md section 4).
Stdlib only (python3.9), read-only on the run dirs, deterministic (no randomness). It reports numbers; it has no pass/fail rule.

  precision_offset.py --records ROOT [ROOT ...] --out OUTDIR [--only-full]
      ROOT = directories searched recursively for run dirs (the overlap records W0..W3 and the leg's records). A run dir holds
      eval.bin.json (or eval.json), calib.bin.json (arm identity) and run_manifest.json. When a run id occurs twice the newest
      eval record wins (the rule of compare_overlap_v2.find_runs); the duplicates are listed in offset.json.
      --only-full computes ONLY the full-pool offset (k = R' of each fit), the quantity of OVERLAP_1e4_VERDICT section 3b / F3 (reader check).

ESTIMAND (all log Z-hat on the same dataset d; V = the engineered variant, T = the theory-mode fits of the overlap):
  fit f, k islands pooled (k | R'_f, k <= R'_f): L_f(k) = mean over the R'_f / k DISJOINT consecutive blocks b of  [ logsumexp(logZ_r, r in b) - log k ]
      (a block's Z-hat is the mean of its islands' Z-hat_r; k = R'_f is the fit's own `evidence.logZ`).
  reference  Tbar_d = mean over the T seeds of dataset d of evidence.logZ (R' = 4; tier 0 N = 10^4, tier 1 N = 4 x 10^4; the tier mix is reported)
  D_f(k) = L_f(k) - Tbar_d;   D_{cell,k,d} = mean over the cell's fits on d;   delta_{cell,k} = mean over the datasets of D_{cell,k,d}
  cell = (N, m, I_max, src) read from calib.bin.json settings; src = ovl (the overlap's V fits, R' = 16) or prec (the leg's fits, R' = 64) (run id and settings must agree, else the fit is listed as ARM_MISMATCH and dropped).
CONTRASTS (the reference T cancels): paired by dataset, at the stated k:
  R' slope   D_{cell,k2,d} - D_{cell,k1,d};   m   (2500,4,3) - (2500,1,3);   I_max   (2500,1,0) - (2500,1,3);   N   (10000,m,3) - (2500,m,3)
UNCERTAINTY: dataset-clustered (datasets are the independent units): mean, sd over datasets, t interval (df = datasets - 1, table below),
  every per-dataset value is printed. Second yardstick for the leg's contrasts: s_rep = pooled sd of the two replicates of a cell
  (sqrt(mean of diff^2/2) over the datasets x cells that have 2 replicates), se_rep = s_rep sqrt(2/r)/sqrt(n_datasets). Yardstick for V - T:
  s_T = pooled seed-to-seed sd of T (2 seeds per dataset). Companions (reported, no inference): the Jensen term -v/(2k) (v = relative variance
  of Z-hat_r over the fit's islands) and the full-pool offset of log Z-hat_occ (M = 1000).
"""
import argparse, csv, glob, hashlib, json, math, os, re, sys

RUN = re.compile(r"^4-(?P<design>IND|ARweak|AR|BLK|ADJOPP|NULL)-n200-r(?P<rep>\d+)-(?:(?P<arm>[TV])-s(?P<seed>[12])|P-N(?P<N>\d+)-m(?P<m>\d+)(?:-I(?P<I>\d))?-c(?P<c>[12])-s1)(?:\.[TV]2)?$")
EVAL = ("eval.bin.json", "eval.json")
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145,
        15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 25: 2.060, 30: 2.042}


def tq(df):
    if df < 1:
        return float("nan")
    ks = sorted(T975)
    return T975[max(k for k in ks if k <= df)] if df < 30 else (2.042 if df == 30 else 1.96)


def jload(p):
    with open(p) as fh:
        return json.load(fh)


def lse(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def mean(xs):
    return sum(xs) / len(xs)


def sd(xs):
    return math.sqrt(sum((x - mean(xs)) ** 2 for x in xs) / (len(xs) - 1)) if len(xs) > 1 else float("nan")


def eval_file(dp):
    """the engine eval record of a run dir: eval.bin.json / eval.json that holds an `evidence` block (a driver MANIFEST named eval.json does not)."""
    for n in EVAL:
        p = os.path.join(dp, n)
        if os.path.isfile(p):
            try:
                if "evidence" in jload(p):
                    return p
            except Exception:
                pass
    return None


SKIP_DIRS = ("_batch_", "manifests", "scripts", "refused_", "rescue_", "cost", "log")


def find_runs(roots):
    runs, dups = {}, []
    for root in roots:
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if not d.startswith(SKIP_DIRS)]
            ef = eval_file(dp)
            if ef is None:
                continue
            rid = None
            if "run_manifest.json" in fns:
                try:
                    rid = jload(os.path.join(dp, "run_manifest.json")).get("run_id")
                except Exception:
                    rid = None
            rid = rid or os.path.basename(dp)
            if not RUN.match(rid):
                continue
            if rid in runs:
                dups.append([rid, runs[rid], dp])
                if os.path.getmtime(ef) > os.path.getmtime(eval_file(runs[rid])):   # the newest eval record wins (compare_overlap_v2.find_runs)
                    runs[rid] = dp
            else:
                runs[rid] = dp
            dns[:] = []
    return runs, dups


def parse(rid, dp):
    m = RUN.match(rid)
    g = m.groupdict()
    ev = jload(eval_file(dp))
    o = {"run_id": rid, "dir": dp, "ds": "%s-r%s" % (g["design"], g["rep"]), "problems": []}
    fm = ev.get("fit", {}).get("meta", {})
    evd = ev.get("evidence", {})
    o["Rp"] = int(fm.get("Rp", 0)); o["tier"] = fm.get("tier"); o["N_fit"] = fm.get("N")
    lr = evd.get("logZ_r")
    if ev.get("status") != "completed" or ev.get("fit_status", "completed") != "completed" or not isinstance(lr, list) or len(lr) != o["Rp"] or not all(isinstance(x, (int, float)) and math.isfinite(x) for x in lr):
        o["problems"].append("NOT_DELIVERED")
        o["logZ_r"] = []; o["logZ"] = float("nan")
    else:
        o["logZ_r"] = [float(x) for x in lr]; o["logZ"] = float(evd["logZ"])
    o["occ1000"] = None
    for e in fm.get("occ", []) or []:
        if e.get("M") == 1000 and isinstance(e.get("log_Z_occ"), (int, float)):
            o["occ1000"] = float(e["log_Z_occ"])
    if g["arm"] == "T":
        o["arm"] = "T"; o["seed"] = int(g["seed"]); o["cell"] = None
        return o
    o["arm"] = "V"
    want = (2500, 1, 3) if g["arm"] == "V" else (int(g["N"]), int(g["m"]), int(g["I"]) if g["I"] is not None else 3)
    o["seed"] = int(g["seed"]) if g["arm"] == "V" else int(g["c"])
    cb = os.path.join(dp, "calib.bin.json")
    try:
        cs = jload(cb)["settings"]; tf = jload(cb).get("tier_final", 0)
        got = (int(cs["tiers"][tf]["N_final"]), int(cs["refine_m"]), int(cs["I_max"]))
        if cs.get("rule") != "bounded":
            o["problems"].append("RULE_%s" % cs.get("rule"))
    except Exception as e:
        got = None; o["problems"].append("NO_CALIB_SETTINGS")
    if got is not None and got != want:
        o["problems"].append("ARM_MISMATCH want %s got %s" % (want, got))
    o["cell"] = want + (("ovl",) if g["arm"] == "V" else ("prec",))     # the overlap fits (R' = 16) and the leg's fits (R' = 64) stay separate cells
    return o


def blocks_mean(lr, k):
    return mean([lse(lr[i:i + k]) - math.log(k) for i in range(0, len(lr), k)])


def jensen(lr, k):
    mx = max(lr); w = [math.exp(x - mx) for x in lr]; mu = mean(w)
    v = sd(w) ** 2 / mu ** 2
    return -v / (2.0 * k), v


def summ(vals):
    n = len(vals); m = mean(vals); s = sd(vals) if n > 1 else float("nan")
    se = s / math.sqrt(n) if n > 1 else float("nan"); h = tq(n - 1) * se if n > 1 else float("nan")
    return {"n": n, "mean": m, "sd": s, "se": se, "lo": m - h, "hi": m + h, "neg": sum(v < 0 for v in vals)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", nargs="+", required=True); ap.add_argument("--out", required=True); ap.add_argument("--only-full", action="store_true")
    a = ap.parse_args(argv)
    runs, dups = find_runs(a.records)
    recs = [parse(r, d) for r, d in sorted(runs.items())]
    bad = [r for r in recs if r["problems"]]
    good = [r for r in recs if not r["problems"]]
    T = {}
    for r in good:
        if r["arm"] == "T":
            T.setdefault(r["ds"], []).append(r)
    Tbar = {d: mean([r["logZ"] for r in rs]) for d, rs in T.items()}
    Tbar0 = {d: mean([r["logZ"] for r in rs if r["tier"] == 0]) for d, rs in T.items() if any(r["tier"] == 0 for r in rs)}   # sensitivity: tier-0 T fits only (N = 10^4)
    tiers = {d: sorted((r["seed"], r["tier"], r["N_fit"]) for r in rs) for d, rs in T.items()}
    sT = None
    pairs = [(rs[0]["logZ"], rs[1]["logZ"]) for rs in (sorted(v, key=lambda r: r["seed"]) for v in T.values()) if len(rs) == 2]
    if pairs:
        sT = math.sqrt(mean([(x - y) ** 2 / 2.0 for x, y in pairs]))
    V = [r for r in good if r["arm"] == "V" and r["ds"] in Tbar]
    # per fit rows
    rows = []
    for f in V:
        ks = [f["Rp"]] if a.only_full else [k for k in (4, 8, 16, 32, 64) if k <= f["Rp"] and f["Rp"] % k == 0]
        for k in ks:
            L = f["logZ"] if k == f["Rp"] else blocks_mean(f["logZ_r"], k)
            jn, v = jensen(f["logZ_r"], k)
            rows.append({"run_id": f["run_id"], "ds": f["ds"], "cell": f["cell"], "rep": f["seed"], "Rp": f["Rp"], "k": k, "L": L, "D": L - Tbar[f["ds"]], "D0": (L - Tbar0[f["ds"]]) if f["ds"] in Tbar0 else None, "jensen": jn, "v_rel": v,
                         "occ_full_offset": (f["occ1000"] - mean([r["occ1000"] for r in T[f["ds"]] if r["occ1000"] is not None]) if (k == f["Rp"] and f["occ1000"] is not None and any(r["occ1000"] is not None for r in T[f["ds"]])) else None)})
    # cell x k x dataset
    cells = {}
    for r in rows:
        cells.setdefault((r["cell"], r["k"]), {}).setdefault(r["ds"], []).append(r)
    table, Dd = [], {}
    for (cell, k), byds in sorted(cells.items()):
        Dds = {d: mean([x["D"] for x in rs]) for d, rs in byds.items()}
        Dd[(cell, k)] = Dds
        s = summ(list(Dds.values()))
        D0s = [mean([x["D0"] for x in rs]) for rs in byds.values() if all(x["D0"] is not None for x in rs)]
        occ = [mean([x["occ_full_offset"] for x in rs if x["occ_full_offset"] is not None]) for rs in byds.values() if any(x["occ_full_offset"] is not None for x in rs)]
        table.append({"N": cell[0], "m": cell[1], "I_max": cell[2], "src": cell[3], "k": k, "datasets": s["n"], "fits": sum(len(v) for v in byds.values()), "delta": s["mean"], "sd_ds": s["sd"], "se": s["se"],
                      "lo95": s["lo"], "hi95": s["hi"], "n_negative": s["neg"], "delta_over_sT": (s["mean"] / sT if sT else None), "delta_tier0ref": (mean(D0s) if D0s else None), "datasets_tier0ref": len(D0s),
                      "jensen_mean": mean([x["jensen"] for rs in byds.values() for x in rs]), "occ_offset_mean": (mean(occ) if occ else None),
                      "per_dataset": {d: round(v, 6) for d, v in sorted(Dds.items())}})
    # contrasts (T cancels), paired by dataset
    contrasts = []
    def contrast(name, A, B):
        if A in Dd and B in Dd:
            ds = sorted(set(Dd[A]) & set(Dd[B]))
            if ds:
                vals = [Dd[A][d] - Dd[B][d] for d in ds]
                s = summ(vals)
                contrasts.append({"contrast": name, "datasets": len(ds), "mean": s["mean"], "sd_ds": s["sd"], "se": s["se"], "lo95": s["lo"], "hi95": s["hi"], "n_negative": s["neg"],
                                  "per_dataset": {d: round(v, 6) for d, v in zip(ds, vals)}})
    if not a.only_full:
        for cell in sorted({c for c, _ in Dd}):
            ks = sorted(k for c, k in Dd if c == cell)
            for k1, k2 in zip(ks, ks[1:]):
                contrast("R' slope %s k %d -> %d" % (cell, k1, k2), (cell, k2), (cell, k1))
        kmax = 64
        P = lambda N, m, I: ((N, m, I, "prec"), kmax)
        contrast("m: (2500,4,3) - (2500,1,3) at k=64", P(2500, 4, 3), P(2500, 1, 3))
        contrast("I_max: (2500,1,0) - (2500,1,3) at k=64", P(2500, 1, 0), P(2500, 1, 3))
        contrast("N: (10000,1,3) - (2500,1,3) at k=64", P(10000, 1, 3), P(2500, 1, 3))
        contrast("N: (10000,4,3) - (2500,4,3) at k=64", P(10000, 4, 3), P(2500, 4, 3))
    # replicate yardstick: pooled sd of the two replicates of a precision cell at k = 64
    reps = []
    for (cell, k), byds in cells.items():
        if k == 64:
            for d, rs in byds.items():
                if len(rs) == 2:
                    reps.append((rs[0]["L"] - rs[1]["L"]) ** 2 / 2.0)
    s_rep = math.sqrt(mean(reps)) if reps else None
    os.makedirs(a.out, exist_ok=True)
    me = hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()
    out = {"script_sha256": me, "only_full": a.only_full, "records": a.records, "fits_found": len(recs), "fits_used_V": len(V), "T_datasets": sorted(Tbar), "T_tiers_by_dataset": tiers,
           "dropped": [{"run_id": r["run_id"], "problems": r["problems"]} for r in bad], "duplicates_resolved": dups, "s_T_seed_to_seed": sT, "s_rep_k64": s_rep, "s_rep_pairs": len(reps),
           "table": table, "contrasts": contrasts}
    json.dump(out, open(os.path.join(a.out, "offset.json"), "w"), indent=1, default=str)
    with open(os.path.join(a.out, "offset_per_fit.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["run_id", "dataset", "N", "m", "I_max", "rep", "Rp", "k", "logZ_block_mean", "D_vs_Tbar", "jensen_pred", "v_rel", "occ1000_full_offset"])
        for r in rows:
            w.writerow([r["run_id"], r["ds"], *r["cell"], r["rep"], r["Rp"], r["k"], "%.9f" % r["L"], "%.9f" % r["D"], "%.3e" % r["jensen"], "%.3e" % r["v_rel"], "" if r["occ_full_offset"] is None else "%.9f" % r["occ_full_offset"]])
    L = ["# precision_offset report (script sha256 %s%s)" % (me, ", --only-full" if a.only_full else ""),
         "fits found %d, V fits used %d (datasets with a T reference: %d), dropped %d, duplicates resolved %d; s_T (seed-to-seed, pooled) = %s; s_rep(k=64) = %s over %d dataset-cells"
         % (len(recs), len(V), len(Tbar), len(bad), len(dups), "%.5f" % sT if sT else "n/a", "%.5f" % s_rep if s_rep else "n/a", len(reps)),
         "", "## offset delta(N, m, I_max, k) = mean over datasets of [V block-mean log Z-hat - T reference]   (no pass/fail)",
         "| src | N | m | I_max | k | datasets | fits | delta | se (clustered) | 95% t-CI | neg | delta / s_T | delta (T tier-0 ref only; datasets) | Jensen mean | occ offset |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in table:
        L.append("| %s | %d | %d | %d | %d | %d | %d | %+.5f | %.5f | %+.5f .. %+.5f | %d/%d | %s | %s | %+.1e | %s |" % (t["src"], t["N"], t["m"], t["I_max"], t["k"], t["datasets"], t["fits"], t["delta"], t["se"], t["lo95"], t["hi95"],
                 t["n_negative"], t["datasets"], "%+.2f" % t["delta_over_sT"] if t["delta_over_sT"] is not None else "n/a", ("%+.5f (%d)" % (t["delta_tier0ref"], t["datasets_tier0ref"])) if t["delta_tier0ref"] is not None else "-", t["jensen_mean"], "%+.5f" % t["occ_offset_mean"] if t["occ_offset_mean"] is not None else "-"))
    if contrasts:
        L += ["", "## contrasts (the T reference cancels; paired by dataset)", "| contrast | datasets | mean | se (clustered) | 95% t-CI | neg |", "|---|---|---|---|---|---|"]
        for c in contrasts:
            L.append("| %s | %d | %+.5f | %.5f | %+.5f .. %+.5f | %d/%d |" % (c["contrast"], c["datasets"], c["mean"], c["se"], c["lo95"], c["hi95"], c["n_negative"], c["datasets"]))
    if bad:
        L += ["", "## dropped fits"] + ["- %s: %s" % (r["run_id"], "; ".join(r["problems"])) for r in bad]
    open(os.path.join(a.out, "offset_report.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
