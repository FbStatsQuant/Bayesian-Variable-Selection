#!/usr/bin/env python3
"""gb_readback.py -- the G-B read-back tables (GB_PLAN section 4, GB_PREREG section 5): per fit the C1 cost / C2 precision / C3 memory / C4 completion / C5 E2 recording
values and verdicts, the option-D quantity, and (for VN25 fits) the continuity-twin report of GB_PREREG section 6. READ-ONLY, stdlib, deterministic, no randomness. It has no
decision content beyond the thresholds of GB_PREREG section 5 (written below as constants); the I_max rule itself is gb_imax_rule.py (its JSON is read for C6 only).

  python3 -I gb_readback.py --records ROOT [ROOT ...] --cost-dir DIR [DIR ...] --out OUTDIR [--rule gb_imax.json] [--id-regex RE] [--branch pass|fail]

Inputs per fit (a record dir with eval.bin.json, calib_meta.json (else calib.bin.json), and the leg's cost_<run_id>.json from p1m_cost.py: stages -> billed_core_h, wall_s_max,
max_rss_bytes). Fields used (all present in the 10^4 eval records; names verified on a real mini-leg record):
  M1 fit.meta.occ[M=1000].sd_log_Z_occ_r     M2 pip.island_spread.max_sd (+ target_met)     M3 evidence.sigma_hat (= sd(log Z-hat_r))
  evidence consistency |evidence.logZ - evidence.logZ_occ.M1000| <= 3 sqrt(se_Z^2 + se_occ^2), se = island sd / sqrt(R')     HPM certified fit.meta.local_certified
  PIP agreement pip.eq_T_target_met (= max_abs_eq_minus_T <= 0.01 + (1 - pi_T_hat))     flags fit.meta.flags.{E1,E2,E3,low_empirical_ESS,checks_passed_final,occ_inhomogeneous}
  option D pi_hat(S0) = exp(selection.F_S0 - evidence.logZ) (the estimated posterior probability of S0); beside it the terminal occupancy fit.meta.occ[M=1].occ (= S0's when HPM = S0)
CLASS MODELS (GB_PLAN 2.3, committed; soft = 1.5 E, hard = 2.5 E): keys (design, N, I_max). REQUESTS (GB_PLAN 2.2, GiB): setup 16, calibrate 16, islands 12, merge 24, eval 16.
Verdicts: C1 OK (<= 1.5 E) / SOFT (1.5-2.5 E: G-B cost FAIL, not a stop) / HARD (> 2.5 E: STOP) / NO_MODEL; C3 PASS (< request) / ADVISORY (> 80 %) / FAIL (>= request or a stage not COMPLETED).
"""
import argparse, glob, json, math, os, re, sys

F2_SHA = "da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a"
MODELS = {("AR", 10000, 0): 108, ("AR", 10000, 3): 118, ("ADJOPP", 10000, 0): 133, ("ADJOPP", 10000, 3): 142,
          ("AR", 2500, 0): 30, ("ADJOPP", 2500, 0): 37, ("AR", 2500, 3): 40}
REQ_GIB = {"setup": 16, "calibrate": 16, "islands": 12, "merge": 24, "eval": 16}
STAGES = ("setup", "calibrate", "islands", "merge", "eval")
RUN = re.compile(r"^5-(?P<d>AR|ADJOPP|IND)-n(?P<n>\d+)-r(?P<r>\d+)-(?P<arm>V|VI3|VN25)-s(?P<s>\d+)$")
EVAL = ("eval.bin.json", "eval.json")
SKIP = ("_batch_", "manifests", "scripts", "refused_", "rescue_", "cost", "log")
GIB = 2 ** 30


def jl(p):
    return json.load(open(p))


def find(roots, rx):
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
            if "evidence" in ev and rx.match(rid or ""):
                out[rid] = (dp, ev)
            dns[:] = []
    return out


def recorded_arm(dp):
    try:
        p = os.path.join(dp, "calib_meta.json")
        if os.path.isfile(p):
            j = jl(p); m = j.get("meta", j)
            return {"N": int(m["N"]), "m": int(m["refine_m"]), "I": int(m["I_max"]), "I_used": m.get("I_used"), "rule": m.get("rule"), "grid_unconverged": (m.get("flags") or {}).get("grid_unconverged"),
                    "grid_fallback": (m.get("flags") or {}).get("grid_fallback")}
        j = jl(os.path.join(dp, "calib.bin.json")); s = j["settings"]; tf = j.get("tier_final", 0)
        return {"N": int(s["tiers"][tf]["N_final"]), "m": int(s["refine_m"]), "I": int(s["I_max"]), "I_used": None, "rule": s.get("rule"), "grid_unconverged": None, "grid_fallback": None}
    except Exception:
        return None


def get(o, *path):
    for k in path:
        if isinstance(o, dict) and k in o:
            o = o[k]
        else:
            return None
    return o


def occ(ev, M):
    return next((e for e in (get(ev, "fit", "meta", "occ") or []) if e.get("M") == M), None)


def fit_row(rid, dp, ev, costs):
    g = RUN.match(rid); gd = g.groupdict() if g else {}
    rec = recorded_arm(dp)
    lz = get(ev, "evidence", "logZ_r") or []
    Rp = len(lz); sig = get(ev, "evidence", "sigma_hat"); o1000, o1 = occ(ev, 1000), occ(ev, 1)
    sd_occ = (o1000 or {}).get("sd_log_Z_occ_r"); logZ = get(ev, "evidence", "logZ"); lzo = get(ev, "evidence", "logZ_occ", "M1000")
    row = {"run_id": rid, "design": gd.get("d"), "arm": gd.get("arm"), "R'": Rp, "recorded_arm": rec, "binary_sha256": get(ev, "binary", "sha256")}
    row["status_ok"] = ev.get("status") == "completed" and ev.get("fit_status", "completed") == "completed"
    row["logZ_r_finite"] = Rp > 0 and all(isinstance(x, (int, float)) and math.isfinite(x) for x in lz)
    row["build_is_F2"] = row["binary_sha256"] == F2_SHA
    # C2
    c2 = {"M1": sd_occ, "M1<=0.05": (sd_occ <= 0.05) if sd_occ is not None else None, "M2": get(ev, "pip", "island_spread", "max_sd"), "M2<=0.005(target_met)": get(ev, "pip", "island_spread", "target_met"),
          "M3": sig, "M3<=0.5(goal, not gating)": (sig <= 0.5) if sig is not None else None, "local_certified": get(ev, "fit", "meta", "local_certified"),
          "pip_eq_T_target_met": get(ev, "pip", "eq_T_target_met"), "max_abs_eq_minus_T": get(ev, "pip", "max_abs_eq_minus_T"), "eq_T_target": get(ev, "pip", "eq_T_target")}
    if None not in (logZ, lzo, sig, sd_occ) and Rp:
        se = math.sqrt((sig / math.sqrt(Rp)) ** 2 + (sd_occ / math.sqrt(Rp)) ** 2)
        c2["evidence_gap"] = abs(logZ - lzo); c2["evidence_bound_3se"] = 3 * se; c2["evidence_consistent"] = abs(logZ - lzo) <= 3 * se
    else:
        c2["evidence_consistent"] = None
    need = (c2["M1<=0.05"], c2["M2<=0.005(target_met)"], c2["evidence_consistent"], c2["local_certified"])
    c2["pip_agreement_checked"] = c2["pip_eq_T_target_met"] is not None
    c2["verdict"] = ("NOT_EVALUATED" if any(x is None for x in need) else ("PASS" if all(need) and c2["pip_eq_T_target_met"] is not False else "FAIL"))
    row["C2"] = c2
    # flags (C5) and option D
    fl = get(ev, "fit", "meta", "flags") or {}
    row["C5"] = {k: fl.get(k) for k in ("E1", "E2", "E3", "low_empirical_ESS", "checks_passed_final", "occ_inhomogeneous")}
    row["C5"]["sd_logZ_r_gt_1"] = (sig > 1) if sig is not None else None
    row["C5"]["calibration_E1_E2"] = "NOT EVALUATED at I_max 0" if (rec and rec["I"] == 0) else "see calibration record"
    fs0 = get(ev, "selection", "F_S0")
    row["science"] = {"hpm": get(ev, "selection", "hpm"), "hpm_eq_S0": get(ev, "selection", "hpm_eq_S0"), "logZ": logZ, "logZ_minus_logZ_T": get(ev, "evidence", "logZ_minus_logZ_T"),
                      "pi_hat_S0": (math.exp(fs0 - logZ) if None not in (fs0, logZ) else None), "occ_top1": (o1 or {}).get("occ"), "sup_null_eq": get(ev, "pip", "eq", "sup_null"),
                      "min_true_eq": get(ev, "pip", "eq", "min_true"), "T_island": None}
    # cost / memory (C1, C3)
    cj = costs.get(rid)
    st = {}
    if cj:
        for s in STAGES:
            x = (cj.get("stages") or {}).get(s)
            if x:
                rss = x.get("max_rss_bytes")
                st[s] = {"billed": x.get("billed_core_h"), "wall_s_max": x.get("wall_s_max"), "max_rss_gib": (rss / GIB if rss is not None else None), "request_gib": REQ_GIB[s],
                         "rss_pct_of_request": (100.0 * rss / GIB / REQ_GIB[s] if rss is not None else None), "states": x.get("states")}
    row["stages"] = st
    total = sum((v["billed"] or 0) for v in st.values()) if st else None
    key = (row["design"], rec["N"] if rec else None, rec["I"] if rec else None)
    E = MODELS.get(key)
    row["C1"] = {"billed": total, "model_E": E, "soft_1.5E": (1.5 * E if E else None), "hard_2.5E": (2.5 * E if E else None), "ratio": (total / E if (E and total is not None) else None),
                 "verdict": ("NO_MODEL" if not E or total is None else ("OK" if total <= 1.5 * E else ("SOFT" if total <= 2.5 * E else "HARD")))}
    bad_state = [s for s, v in st.items() if v["states"] and any(x != "COMPLETED" for x in v["states"])]
    pcts = [v["rss_pct_of_request"] for v in st.values() if v["rss_pct_of_request"] is not None]
    miss = [s for s in STAGES if s not in st]
    row["C3"] = {"max_pct": max(pcts) if pcts else None, "stages_missing": miss, "not_completed": bad_state,
                 "verdict": ("NOT_EVALUATED" if (not pcts or miss) else ("FAIL" if (bad_state or max(pcts) >= 100) else ("ADVISORY" if max(pcts) > 80 else "PASS")))}
    me = get(ev, "fit", "meta", "mem_estimate", "sacct_upper")
    row["C3"]["merge_engine_estimate_gib"] = me / GIB if me else None
    row["C3"]["merge_measured_over_estimate"] = ((st["merge"]["max_rss_gib"] * GIB) / me) if (me and "merge" in st and st["merge"]["max_rss_gib"] is not None) else None
    row["C4"] = {"delivered": bool(row["status_ok"] and row["logZ_r_finite"] and Rp == 16), "one_build_F2": row["build_is_F2"],
                 "arm_identity": bool(rec and rec["rule"] == "bounded" and not (rec["I_used"] is not None and rec["I_used"] > rec["I"]))}
    return row


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", nargs="+", required=True); ap.add_argument("--cost-dir", nargs="*", default=[]); ap.add_argument("--out", required=True)
    ap.add_argument("--rule", default=None, help="gb_imax.json of gb_imax_rule.py (C6)"); ap.add_argument("--id-regex", default=None, help="override the run-id pattern (tests)")
    ap.add_argument("--branch", choices=("pass", "fail"), default="pass", help="winning configuration: pass = the I_max 0 fits; fail = the confirmation fit (N 2,500, I_max 3)")
    a = ap.parse_args(argv)
    runs = find(a.records, re.compile(a.id_regex) if a.id_regex else RUN)
    costs = {}
    for d in a.cost_dir:
        for p in glob.glob(os.path.join(d, "cost_*.json")):
            j = jl(p)
            if "stages" in j:
                costs[j["run_id"]] = j
    rows = {rid: fit_row(rid, dp, ev, costs) for rid, (dp, ev) in sorted(runs.items())}
    rule = jl(a.rule) if a.rule else None
    win = [r for r in rows.values() if r["arm"] == ("V" if a.branch == "pass" else "VI3") and (a.branch == "pass" or (r["recorded_arm"] or {}).get("N") == 2500)]
    verdict = {"rule_outcome(C6)": (rule or {}).get("outcome", "NOT_RUN"), "branch": a.branch, "winning_fits": [r["run_id"] for r in win]}
    if win:
        v1 = [r["C1"]["verdict"] for r in win]; v2 = [r["C2"]["verdict"] for r in win]; v3 = [r["C3"]["verdict"] for r in win]; v4 = [all(r["C4"].values()) for r in win]
        verdict.update({"C1": v1, "C2": v2, "C3": v3, "C4": v4,
                        "G-B": ("STOP (C1 hard)" if "HARD" in v1 else
                                ("PASS" if (all(x == "OK" for x in v1) and all(x == "PASS" for x in v2) and all(x in ("PASS", "ADVISORY") for x in v3) and all(v4) and verdict["rule_outcome(C6)"] in ("PASS", "FAIL")) else "NOT_PASSED: see the criterion"))})
    else:
        verdict["G-B"] = "AWAITING_FITS"
    # continuity twins (VN25 vs V of the same dataset)
    cont = []
    for rid, r in rows.items():
        if r["arm"] != "VN25":
            continue
        base = rows.get(re.sub(r"-VN25-", "-V-", rid))
        if not base:
            cont.append({"twin": rid, "note": "no N 10^4 partner record"}); continue
        sa, sb = base["science"], r["science"]
        sea = (get(runs[base["run_id"]][1], "evidence", "sigma_hat") or 0) / math.sqrt(base["R'"] or 1); seb = (get(runs[rid][1], "evidence", "sigma_hat") or 0) / math.sqrt(r["R'"] or 1)
        comb = math.sqrt(sea ** 2 + seb ** 2)
        cont.append({"pair": [base["run_id"], rid], "hpm_equal": sa["hpm"] == sb["hpm"], "hpm_eq_S0": [sa["hpm_eq_S0"], sb["hpm_eq_S0"]],
                     "dlogZ(N1e4 - N2500)": (sa["logZ"] - sb["logZ"]) if None not in (sa["logZ"], sb["logZ"]) else None, "dlogZ_in_island_se": ((sa["logZ"] - sb["logZ"]) / comb) if (comb and None not in (sa["logZ"], sb["logZ"])) else None,
                     "logZ-logZ_T": [sa["logZ_minus_logZ_T"], sb["logZ_minus_logZ_T"]], "pi_hat_S0": [sa["pi_hat_S0"], sb["pi_hat_S0"]],
                     "r_N(M1,M2,M3)": [(base["C2"][k] / r["C2"][k]) if None not in (base["C2"][k], r["C2"][k]) and r["C2"][k] else None for k in ("M1", "M2", "M3")],
                     "f_billed_islands": ((base["stages"]["islands"]["billed"] / r["stages"]["islands"]["billed"]) if ("islands" in base["stages"] and "islands" in r["stages"] and r["stages"]["islands"]["billed"]) else None),
                     "dsup_null": (sa["sup_null_eq"] - sb["sup_null_eq"]) if None not in (sa["sup_null_eq"], sb["sup_null_eq"]) else None,
                     "not_computed_here": "max_j |dPIP_eq| (needs the fit.bin reader); d_H between the two laws (needs law.bin, data.bin and the cross-evaluator build at 10^5; not verified)"})
    rep = {"script": "gb_readback.py", "F2_sha256": F2_SHA, "models": {"%s N%d I%d" % k: v for k, v in MODELS.items()}, "requests_gib": REQ_GIB, "fits": rows, "G-B": verdict, "continuity_twins": cont}
    os.makedirs(a.out, exist_ok=True)
    json.dump(rep, open(os.path.join(a.out, "gb_readback.json"), "w"), indent=1, default=str)
    L = ["# G-B read-back (gb_readback.py)", "", "G-B: **%s**; C6 rule: **%s**; branch %s; winning fits %s" % (verdict["G-B"], verdict["rule_outcome(C6)"], a.branch, verdict["winning_fits"]), "",
         "| fit | N / I_max | billed (E, ratio) | C1 | C2 | C3 (max % of request) | C4 | M1 | M2 | M3 | pi_hat(S0) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    f3 = lambda x: "NA" if x is None else ("%.4g" % x)
    for r in rows.values():
        ra = r["recorded_arm"] or {}
        L.append("| %s | %s / %s | %s (%s, %s) | %s | %s | %s (%s) | %s | %s | %s | %s | %s |" % (r["run_id"], ra.get("N"), ra.get("I"), f3(r["C1"]["billed"]), r["C1"]["model_E"], f3(r["C1"]["ratio"]), r["C1"]["verdict"], r["C2"]["verdict"],
                 r["C3"]["verdict"], f3(r["C3"]["max_pct"]), all(r["C4"].values()), f3(r["C2"]["M1"]), f3(r["C2"]["M2"]), f3(r["C2"]["M3"]), f3(r["science"]["pi_hat_S0"])))
    L += ["", "Stages (billed core-h, wall s, MaxRSS GiB of request):"]
    for r in rows.values():
        L.append("- %s: " % r["run_id"] + "; ".join("%s %s / %s s / %s of %d G (%s%%)" % (s, f3(v["billed"]), v["wall_s_max"], f3(v["max_rss_gib"]), v["request_gib"], f3(v["rss_pct_of_request"])) for s, v in r["stages"].items()))
    if cont:
        L += ["", "Continuity twins (report-only): see gb_readback.json `continuity_twins`."]
    open(os.path.join(a.out, "gb_readback.md"), "w").write("\n".join(L) + "\n")
    print(json.dumps({"G-B": verdict["G-B"], "C6": verdict["rule_outcome(C6)"], "fits": len(rows)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
