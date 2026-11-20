#!/usr/bin/env python3
"""gb_imax_rule.py -- the G-B copy of the REGISTERED I_max rule (precision_freeze.py sha256 7cdd69a1...6279605, PREREG section 3.2, "I_max = 0" block;
precision_freeze_vn.py sha256 114f7e78...4cf73 is its mini-leg copy). NOT the registered file; both are unedited. Neither can score the 10^5 pairs:
their run-id regex is the precision leg's (4-<design>-n200-r01-P-N<N>-m<m>[-I<i>]-c<1|2>-s1) and `val()` requires exactly 2 replicates per cell.
This copy differs in exactly three places (tests/test_gb_imax_rule.py proves the equality on the leg's REAL FZ records: --ids precision --N 2500 --reps 2 gives the
same ratios as fz/freeze.json for the knob I_max=0):
  (1) run ids: --ids gb (default): 5-<AR|ADJOPP>-n200-r01-(V|VI3)-s1 (V = the frozen I_max 0 fit, VI3 = its I_max 3 twin); --ids precision: the leg's ids (golden test);
  (2) --reps R (default 1): a cell's value = the mean of its R fits (both arms of a dataset must have R delivered, identity-verified fits), registered R = 2;
  (3) only the I_max rule is computed (no cost ratio, no N / m knobs), and the final-merge flags are reported beside it.
THE RULE (unchanged): per dataset d and metric k in (M1, M2, M3): r_{k,d} = value(I_max 0 cell) / value(I_max 3 cell); r_k = geometric mean over the datasets.
  I_max = 0 PASSES iff r_k <= 1.15 for k = 1, 2, 3 AND r_{k,d} <= 1.30 for every dataset AND selection.hpm is identical in every fit of both arms of every dataset.
  With ONE dataset the two bars apply to the same number and 1.15 binds; with 2 datasets they are the registered two bars.
M1 = fit.meta.occ[M = 1000].sd_log_Z_occ_r; M2 = pip.island_spread.max_sd; M3 = evidence.sigma_hat (= sd(log Z-hat_r); PREREG section 8 erratum).
ARM IDENTITY (as registered): each fit is scored by its RECORDED arm (N, m, I_max) from calib_meta.json (else calib.bin.json settings); a fit whose recorded arm contradicts its plan arm,
whose rule is not `bounded`, whose I_used > I_max, or without a calibration record is an IDENTITY FAILURE -> INCOMPLETE (never scored). Missing metric, missing fit or a
non-positive denominator -> NOT_EVALUATED. No default action in either case (HQ decides).
  python3 -I gb_imax_rule.py --records ROOT [ROOT ...] --N 10000 --out OUTDIR [--reps 1] [--ids gb|precision]
"""
import argparse, hashlib, json, math, os, re, sys

RUN_GB = re.compile(r"^5-(?P<d>AR|ADJOPP)-n200-r01-(?P<arm>V|VI3)-s1$")
RUN_PREC = re.compile(r"^4-(?P<d>ARweak|AR|ADJOPP)-n200-r01-P-N(?P<N>\d+)-m(?P<m>\d+)(?:-I(?P<I>\d))?-c(?P<c>[12])-s1$")
EVAL = ("eval.bin.json", "eval.json")
SKIP = ("_batch_", "manifests", "scripts", "refused_", "rescue_", "cost", "log")
BAR_GEO, BAR_DS = 1.15, 1.30


def jl(p):
    return json.load(open(p))


def gmean(xs):
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def plan_of(rid, ids):
    """(dataset, (N, m, I_max)) from the run id; N is None for gb ids (taken from --N)."""
    if ids == "gb":
        g = RUN_GB.match(rid)
        return (g["d"], None, 1, 0 if g["arm"] == "V" else 3) if g else None
    g = RUN_PREC.match(rid)
    return (g["d"], int(g["N"]), int(g["m"]), int(g["I"]) if g["I"] is not None else 3) if g else None


def find(roots, ids):
    out = {}
    for root in roots:
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if not d.startswith(SKIP)]
            ef = next((os.path.join(dp, n) for n in EVAL if n in fns), None)
            if ef is None:
                continue
            try:
                ev = jl(ef)
            except Exception:
                continue
            rid = jl(os.path.join(dp, "run_manifest.json")).get("run_id") if "run_manifest.json" in fns else os.path.basename(dp)
            if "evidence" in ev and plan_of(rid or "", ids) and (rid not in out or os.path.getmtime(ef) > os.path.getmtime(out[rid][0])):
                out[rid] = (ef, dp, ev)
            dns[:] = []
    return out


def recorded_arm(dp):
    p = os.path.join(dp, "calib_meta.json")
    try:
        if os.path.isfile(p):
            j = jl(p); m = j.get("meta", j)
            return {"N": int(m["N"]), "m": int(m["refine_m"]), "I": int(m["I_max"]), "I_used": m.get("I_used"),
                    "grid_unconverged": (m.get("flags") or {}).get("grid_unconverged"), "rule": m.get("rule"), "src": "calib_meta.json"}, None
        j = jl(os.path.join(dp, "calib.bin.json")); s = j["settings"]; tf = j.get("tier_final", 0)
        return {"N": int(s["tiers"][tf]["N_final"]), "m": int(s["refine_m"]), "I": int(s["I_max"]), "I_used": None, "grid_unconverged": None,
                "rule": s.get("rule"), "src": "calib.bin.json"}, None
    except Exception as e:
        return None, "NO_CALIB_RECORD (%s)" % type(e).__name__


def fit_metrics(ev):   # verbatim from precision_freeze.py, plus the final-merge flags and log Z-hat (reported, never scored)
    fm = ev.get("fit", {}).get("meta", {})
    m1 = next((e.get("sd_log_Z_occ_r") for e in fm.get("occ", []) or [] if e.get("M") == 1000), None)
    fl = fm.get("flags", {})
    return {"M1": m1, "M2": ev.get("pip", {}).get("island_spread", {}).get("max_sd"), "M3": ev.get("evidence", {}).get("sigma_hat"), "M3r": ev.get("evidence", {}).get("sigma_hat_robust"),
            "hpm": tuple(ev.get("selection", {}).get("hpm", [])), "ok": ev.get("status") == "completed" and ev.get("fit_status", "completed") == "completed",
            "target_pip": ev.get("pip", {}).get("island_spread", {}).get("target_met"), "inhom": fl.get("occ_inhomogeneous"),
            "flags": {k: fl.get(k) for k in ("E1", "E2", "E3", "low_empirical_ESS", "checks_passed_final")}, "logZ": ev.get("evidence", {}).get("logZ")}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", nargs="+", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--N", type=int, required=True, help="N of the pair (N*, 10000 or 2500)")
    ap.add_argument("--reps", type=int, default=1); ap.add_argument("--ids", choices=("gb", "precision"), default="gb")
    a = ap.parse_args(argv)
    runs = find(a.records, a.ids)
    fits, ident = {}, {}
    for rid, (ef, dp, ev) in sorted(runs.items()):
        d, nplan, mplan, iplan = plan_of(rid, a.ids)
        nplan = a.N if nplan is None else nplan
        if (nplan, mplan) != (a.N, 1):
            continue                                     # other N / m cells of the precision leg are not part of this rule
        x = fit_metrics(ev); x["rid"] = rid
        rec, why = recorded_arm(dp)
        reasons = [] if rec else [why]
        if rec:
            if (rec["N"], rec["m"], rec["I"]) != (nplan, mplan, iplan):
                reasons.append("ARM_MISMATCH plan %s recorded %s" % ((nplan, mplan, iplan), (rec["N"], rec["m"], rec["I"])))
            if rec["rule"] != "bounded":
                reasons.append("RULE_%s" % rec["rule"])
            if rec["I_used"] is not None and rec["I_used"] > rec["I"]:
                reasons.append("I_USED_GT_IMAX")
        x["ident_ok"] = not reasons; x["rec"] = rec
        ident[rid] = {"plan_arm": [nplan, mplan, iplan], "recorded": rec, "reasons": reasons}
        fits.setdefault((d, iplan), []).append(x)
    dss = sorted({d for d, _ in fits})
    report = {"script_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest(), "N": a.N, "reps": a.reps, "datasets": dss, "identity": ident,
              "bars": {"geo": BAR_GEO, "per_dataset": BAR_DS}, "outcome": None, "detail": {}}
    bad = {r: v["reasons"] for r, v in ident.items() if v["reasons"]}
    cells_ok = dss and all(len(fits.get((d, i), [])) >= a.reps for d in dss for i in (0, 3))
    if bad:
        report["outcome"], report["detail"] = "INCOMPLETE", {"reason": "identity failure", "fits": bad}
    elif not cells_ok:
        report["outcome"], report["detail"] = "NOT_EVALUATED", {"reason": "arm fits missing (need %d per arm per dataset)" % a.reps}
    else:
        def val(d, i, k):
            xs = [f[k] for f in fits[(d, i)] if f["ok"] and f[k] is not None]
            return sum(xs) / len(xs) if len(xs) == a.reps else None
        rs, ok, nev = {}, True, None
        hpm_same = all(len({f["hpm"] for i in (0, 3) for f in fits[(d, i)] if f["ok"]}) == 1 for d in dss)
        for k in ("M1", "M2", "M3"):
            per = {}
            for d in dss:
                x, b = val(d, 0, k), val(d, 3, k)
                if x is None or b is None or not b > 0 or not math.isfinite(x / b):
                    nev = "metric %s missing / non-positive denominator for %s" % (k, d); break
                per[d] = x / b
            if nev:
                break
            rs[k] = {"per_dataset": per, "geo_mean": gmean(list(per.values()))}
            ok = ok and rs[k]["geo_mean"] <= BAR_GEO and all(v <= BAR_DS for v in per.values())
        if nev:
            report["outcome"], report["detail"] = "NOT_EVALUATED", {"reason": nev}
        else:
            report["outcome"] = "PASS" if (ok and hpm_same) else "FAIL"
            report["detail"] = {"n_datasets": len(dss), "form": "n=1: the two bars coincide, 1.15 binds" if len(dss) == 1 else "n=%d datasets x %d replicate(s): registered two bars" % (len(dss), a.reps),
                                "hpm_identical": hpm_same, "ratios": rs,
                                "reported_not_scored": {"%s I%d" % (d, i): [{"rid": f["rid"], "M1": f["M1"], "M2": f["M2"], "M3": f["M3"], "M3_robust": f["M3r"], "target_pip": f["target_pip"],
                                                                           "occ_inhomogeneous": f["inhom"], "final_flags": f["flags"], "logZ": f["logZ"],
                                                                           "I_used": (f["rec"] or {}).get("I_used"), "grid_unconverged": (f["rec"] or {}).get("grid_unconverged")} for f in fits[(d, i)]]
                                                       for d in dss for i in (0, 3)}}
    os.makedirs(a.out, exist_ok=True)
    json.dump(report, open(os.path.join(a.out, "gb_imax.json"), "w"), indent=1, default=str)
    print(json.dumps({"outcome": report["outcome"], "N": a.N, "datasets": dss, "ratios": {k: v["geo_mean"] for k, v in report["detail"].get("ratios", {}).items()},
                      "per_dataset": {k: v["per_dataset"] for k, v in report["detail"].get("ratios", {}).items()}, "hpm_identical": report["detail"].get("hpm_identical"),
                      "form": report["detail"].get("form"), "reason": report["detail"].get("reason"), "script_sha256": report["script_sha256"]}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
