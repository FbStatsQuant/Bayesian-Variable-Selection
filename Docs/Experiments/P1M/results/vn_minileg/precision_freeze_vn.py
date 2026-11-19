#!/usr/bin/env python3
"""precision_freeze_vn.py -- the V-N mini-leg's copy of the REGISTERED rule (MINILEG_PREREG.md section 3). NOT the registered file.
precision_freeze.py (sha256 7cdd69a11f3aaffa7a6615df639aefbe101042e9d37a8d520999ccbdc6279605) is unedited. This copy differs in exactly three places (a diff is in
MINILEG_PREREG section 3.2, and tests/test_vn_golden.py proves the equality on the leg's real FZ records):
  (1) --baseline N,m,I (default 2500,1,3 = the registered B) and (2) --knob NAME:N,m,I:up|down (repeatable; default: the registered four knobs), so that an N arm at
  the FROZEN configuration (10^4, m 1, I_max 0) can be scored against the N = 2,500 baseline of the SAME I_max; (3) cost files without a `stages` key (the per-batch
  cost_batch.json that the glob also matches: the defect named in CAMPAIGN_FREEZE_ADDENDUM section 4) are skipped instead of raising KeyError. No threshold, metric,
  ratio, identity rule or HPM rule is changed. Everything below is the registered docstring.

precision_freeze.py -- applies the pre-registered FREEZE RULE of the precision study (PREREG.md section 3) to the leg's records.
Stdlib only (python3.9), read-only, deterministic. It computes the rule's inputs and prints ADOPT / KEEP / INCOMPLETE / NOT_RUN / NOT_EVALUATED per knob; the
Engineering manager records the outcome, an independent review confirms it (PREREG section 6).

  precision_freeze.py --records ROOT [ROOT ...] --cost-dir DIR [DIR ...] --out OUTDIR

Precision fits only: run ids 4-<design>-n200-r01-P-N<N>-m<m>[-I<i>]-c<1|2>-s1 on the three datasets AR, ARweak, ADJOPP (R' = 64).
ARM IDENTITY (plan review R2): every fit is scored by its RECORDED arm = (N, m, I_max) read from the fit's own records: `calib_meta.json` (the dump of
`smcbvs4 info calib.bin --meta 1`: N, refine_m, I_max, I_used, flags.grid_unconverged, rule), else `calib.bin.json settings` (N_final, refine_m, I_max, rule). A fit whose
recorded arm contradicts its plan arm (the run id), whose rule is not `bounded`, whose I_used > I_max, or which has no calibration record, is an IDENTITY FAILURE: it is
never scored and every knob that uses it (the knob's arm or the baseline) is INCOMPLETE. Behaviour is reported beside the identity (not decisive): island T (m = 4: T % 4 == 0
and T >= 36), diagnostic-island files in cost/ (I_max = 0: none; I_max = 3: k = I_used).
Per fit (engine eval record): M1 = fit.meta.occ[M = 1000].sd_log_Z_occ_r (sd over islands of log Z-hat_occ,r; spec target <= 0.05);
  M2 = pip.island_spread.max_sd (max over variables of the sd over islands of the PIP; target <= 0.005); M3 = evidence.sigma_hat (island sd of Z-hat_r / Z-hat; goal <= 0.5;
  evidence.sigma_hat_robust is reported beside it).
Per (dataset, cell) value = mean over the 2 replicates; ratio r_X = geometric mean over the datasets of value(X) / value(B), B = (N 2500, m 1, I_max 3).
Cost ratio c_X = mean over the fits of billed ISLANDS core-h(X) / the same for B (cost files cost_<run_id>.json, stage `islands`; calibration is excluded, plan review R16).
RULE (cost-raising knob X = m 4 or N 10^4): ADOPT iff for EACH of M1, M2, M3: r_X <= 1/sqrt(c_X) (the gain beats spending the same extra cost on more islands,
  whose pooled sd falls as 1/sqrt(R')) AND r_X < 1 in EVERY dataset AND the HPM set is the same in every fit of X and B (PER KNOB: X u B only; plan review R1). Otherwise KEEP.
RULE (I_max = 0): a NON-INFERIORITY margin, not a cost rule (plan review R4): ADOPT iff for EACH of M1, M2, M3: r <= 1.15 AND r <= 1.30 in every dataset AND the HPM set is
  the same in every fit of the arm and B; otherwise KEEP I_max = 3.
Systematic resampling: not testable with the frozen binary (PREREG blocker B3): frozen OFF, reported "not tested" (HQ Q5). N = 10^4 arms: NOT_RUN unless the fits exist (B2, HQ Q1).
"""
import argparse, glob, hashlib, json, math, os, re, sys

RUN = re.compile(r"^4-(?P<d>ARweak|AR|ADJOPP)-n200-r01-P-N(?P<N>\d+)-m(?P<m>\d+)(?:-I(?P<I>\d))?-c(?P<c>[12])-s1$")
EVAL = ("eval.bin.json", "eval.json")
SKIP = ("_batch_", "manifests", "scripts", "refused_", "rescue_", "cost", "log")


def jl(p):
    return json.load(open(p))


def gmean(xs):
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def find(roots):
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
            if "evidence" in ev and RUN.match(rid or "") and (rid not in out or os.path.getmtime(ef) > os.path.getmtime(out[rid][0])):
                out[rid] = (ef, dp, ev)
            dns[:] = []
    return out


def recorded_arm(dp):
    """(N, m, I_max, I_used, grid_unconverged, rule, source) from the fit's own calibration records, or (None, reason)."""
    p = os.path.join(dp, "calib_meta.json")
    try:
        if os.path.isfile(p):
            j = jl(p); m = j.get("meta", j)
            return {"N": int(m["N"]), "m": int(m["refine_m"]), "I": int(m["I_max"]), "I_used": m.get("I_used"), "grid_unconverged": (m.get("flags") or {}).get("grid_unconverged"),
                    "rule": m.get("rule"), "src": "calib_meta.json"}, None
        j = jl(os.path.join(dp, "calib.bin.json")); s = j["settings"]; tf = j.get("tier_final", 0)
        return {"N": int(s["tiers"][tf]["N_final"]), "m": int(s["refine_m"]), "I": int(s["I_max"]), "I_used": None, "grid_unconverged": None, "rule": s.get("rule"), "src": "calib.bin.json"}, None
    except Exception as e:
        return None, "NO_CALIB_RECORD (%s)" % type(e).__name__


def behaviour(dp, rec):
    T = None
    try:
        T = int(jl(os.path.join(dp, "island_1.bin.json"))["T"])
    except Exception:
        pass
    ks = [int(m.group(1)) for f in glob.glob(os.path.join(dp, "cost", "cost_diag_t*_k*_r*.jsonl")) for m in [re.search(r"_k(\d+)_r", f)] if m]
    return {"T": T, "diag_k_max": max(ks) if ks else 0, "m4_T_ok": (T % 4 == 0 and T >= 36) if T is not None else None}


def fit_metrics(ev):
    fm = ev.get("fit", {}).get("meta", {})
    m1 = next((e.get("sd_log_Z_occ_r") for e in fm.get("occ", []) or [] if e.get("M") == 1000), None)
    return {"M1": m1, "M2": ev.get("pip", {}).get("island_spread", {}).get("max_sd"), "M3": ev.get("evidence", {}).get("sigma_hat"), "M3r": ev.get("evidence", {}).get("sigma_hat_robust"),
            "hpm": tuple(ev.get("selection", {}).get("hpm", [])), "ok": ev.get("status") == "completed" and ev.get("fit_status", "completed") == "completed",
            "target_pip": ev.get("pip", {}).get("island_spread", {}).get("target_met"), "inhom": fm.get("flags", {}).get("occ_inhomogeneous")}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", nargs="+", required=True); ap.add_argument("--cost-dir", nargs="*", default=[]); ap.add_argument("--out", required=True)
    ap.add_argument("--baseline", default="2500,1,3", help="baseline cell N,m,I_max (registered: 2500,1,3)")
    ap.add_argument("--knob", action="append", default=None, help="NAME:N,m,I:up|down, repeatable (default: the registered four knobs)")
    a = ap.parse_args(argv)
    runs = find(a.records)
    cost = {}
    for d in a.cost_dir:
        for p in glob.glob(os.path.join(d, "cost_*.json")):
            j = jl(p)
            if "stages" not in j:       # (3) cost_batch.json etc.
                continue
            cost[j["run_id"]] = j["stages"].get("islands", {}).get("billed_core_h")
    fits, ident = {}, {}
    for rid, (ef, dp, ev) in sorted(runs.items()):
        g = RUN.match(rid).groupdict()
        plan = (int(g["N"]), int(g["m"]), int(g["I"]) if g["I"] is not None else 3)
        x = fit_metrics(ev); x["cost"] = cost.get(rid); x["rid"] = rid
        rec, why = recorded_arm(dp)
        reasons = [] if rec else [why]
        if rec:
            got = (rec["N"], rec["m"], rec["I"])
            if got != plan:
                reasons.append("ARM_MISMATCH plan %s recorded %s" % (plan, got))
            if rec["rule"] != "bounded":
                reasons.append("RULE_%s" % rec["rule"])
            if rec["I_used"] is not None and rec["I_used"] > rec["I"]:
                reasons.append("I_USED_GT_IMAX")
        x["ident_ok"] = not reasons; x["ident_reasons"] = reasons; x["rec"] = rec; x["beh"] = behaviour(dp, rec)
        ident[rid] = {"plan_arm": plan, "recorded": rec, "reasons": reasons, "behaviour": x["beh"]}
        fits.setdefault((g["d"], plan), []).append(x)      # filed under the PLAN arm; a contradicting fit is flagged, never scored
    B = tuple(int(x) for x in a.baseline.split(","))
    cells = sorted({c for _, c in fits})
    dss = sorted({d for d, _ in fits})
    report = {"script_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest(), "datasets": dss, "cells": [list(c) for c in cells],
              "identity": ident, "decisions": {}, "detail": {}}

    def val(d, c, k):
        xs = [f[k] for f in fits.get((d, c), []) if f["ok"] and f["ident_ok"] and f[k] is not None]
        return sum(xs) / len(xs) if len(xs) == 2 else None            # both replicates delivered and identity-verified, else the dataset is not evaluable

    def evaluate(c, kind):
        if c not in cells or B not in cells:
            return "NOT_RUN", {"reason": "arm or baseline fits missing"}
        bad = [(f["rid"], f["ident_reasons"]) for cc in (c, B) for d in dss for f in fits.get((d, cc), []) if not f["ident_ok"]]
        if bad:
            return "INCOMPLETE", {"reason": "identity failure in the arm or the baseline", "fits": bad}
        # HPM check PER KNOB: the fits of X and B only (plan review R1)
        hpm_sets = {d: {f["hpm"] for cc in (c, B) for f in fits.get((d, cc), []) if f["ok"]} for d in dss}
        hpm_same = all(len(v) == 1 for v in hpm_sets.values())
        det = {"hpm_identical_X_and_B": hpm_same}
        ok = hpm_same; rs = {}
        for k in ("M1", "M2", "M3"):
            per = {}
            for d in dss:
                x, b = val(d, c, k), val(d, B, k)
                if x is None or b is None or b <= 0:
                    return "NOT_EVALUATED", {"reason": "metric %s missing for %s" % (k, d)}
                per[d] = x / b
            rs[k] = {"per_dataset": per, "geo_mean": gmean(list(per.values()))}
        cx = None
        if kind == "up":
            num = [f["cost"] for d in dss for f in fits.get((d, c), []) if f["cost"] is not None]
            den = [f["cost"] for d in dss for f in fits.get((d, B), []) if f["cost"] is not None]
            if not num or not den:
                return "NOT_EVALUATED", {"reason": "island cost records missing"}
            cx = (sum(num) / len(num)) / (sum(den) / len(den)); lim = 1.0 / math.sqrt(cx)
            for k in rs:
                ok = ok and rs[k]["geo_mean"] <= lim and all(v < 1.0 for v in rs[k]["per_dataset"].values())
        else:
            for k in rs:
                ok = ok and rs[k]["geo_mean"] <= 1.15 and all(v <= 1.30 for v in rs[k]["per_dataset"].values())
        det.update({"ratios": rs, "cost_ratio": cx, "limit_geo": (1.0 / math.sqrt(cx) if cx else 1.15)})
        return ("ADOPT" if ok else "KEEP"), det
    if a.knob:
        knobs = [(k.split(":")[0], tuple(int(x) for x in k.split(":")[1].split(",")), k.split(":")[2]) for k in a.knob]
    else:
        knobs = [("m=4", (2500, 4, 3), "up"), ("N=10000 (m=1)", (10000, 1, 3), "up"), ("N=10000 (m=4)", (10000, 4, 3), "up"), ("I_max=0", (2500, 1, 0), "down")]
    report["baseline"] = list(B)
    for name, c, kind in knobs:
        r, det = evaluate(c, kind); report["decisions"][name] = r; report["detail"][name] = det
    report["decisions"]["resampling"] = "OFF, not tested (systematic not available in the frozen binary; D-14 default; HQ Q5)"
    # targets and calibration flags per fit, reported (spec 0-v2.3; never used to switch estimators)
    tg = {}
    for (d, c), fl in sorted(fits.items()):
        for f in fl:
            tg.setdefault(str(c), []).append({"dataset": d, "run_id": f["rid"], "M1<=0.05": (f["M1"] <= 0.05) if f["M1"] is not None else None, "M2<=0.005": f["target_pip"],
                                              "M3<=0.5": (f["M3"] <= 0.5) if f["M3"] is not None else None, "M3_robust": f["M3r"], "occ_inhomogeneous": f["inhom"],
                                              "I_used": (f["rec"] or {}).get("I_used"), "grid_unconverged": (f["rec"] or {}).get("grid_unconverged")})
    report["targets_per_fit"] = tg
    os.makedirs(a.out, exist_ok=True)
    json.dump(report, open(os.path.join(a.out, "freeze.json"), "w"), indent=1, default=str)
    print(json.dumps({"decisions": report["decisions"], "identity_failures": {r: v["reasons"] for r, v in ident.items() if v["reasons"]}, "script_sha256": report["script_sha256"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
