#!/usr/bin/env python3
"""gc_wave_check.py -- the 1M WAVE CHECK (HQ H-48 / H-49): after the collection of every 1M wave from W1 on, per fit:
  HPM = S0?, MPM = S0?, E1 / E2 / E3, sigma-hat = sd(log Z_r), C2 (M1 <= 0.05, M2 <= 0.005, the evidence bound, HPM certified, PIP agreement; from the REGISTERED gc_readback.py, unedited, run on the wave's records),
  the minimum empirical ESS / N with its island, stage, phi and DELTA-PHI at the dip (the stage's phi step), EVERY island-stage below 0.5 N (each with its Delta-phi), and the engine flag low_empirical_ESS.
The ESS values come from the island sections st_ess / st_phi (the islands stay on NOTS; gc_ess_nots.py reads them there, detached, nice 19) or from records/ when the islands are on Owls (the pilot).
FLAG -> STOP rule (H-48): low_empirical_ESS TOGETHER WITH ANY of an E-flag (E1 / E2 / E3), sigma-hat > 0.5, a C2 failure, or HPM != S0 -> "FLAG: STOP, tell the manager, no next wave".
low_empirical_ESS ALONE is reported (expected on about 1 fit in 7 of the frozen arm, H-49), never a stop. Stdlib only; writes wave_check_<W>.md and .json.
Usage: gc_wave_check.py --wave W1 --records-dir <records/gc1m/GC_W1> --ess-json <ess json from gc_ess_nots.py> [--readback-json <gc_readback.json>] --out-dir DIR [--gc-readback PATH]"""
import argparse, glob, json, math, os, subprocess, sys, tempfile
LOW = 0.5        # low_empirical_ESS: any island stage ESS < 0.5 N (merge.h l.486 of F2)
SIGMA_STOP = 0.5

def ess_dips(isl, N):
    """isl = {island_file: {st_phi, st_ess}} -> (min record, all island-stages < LOW N). Each record: ESS, ESS/N, island, stage (1-based), phi_from, phi_to, dphi."""
    recs = []
    for f, s in isl.items():
        phi, ess = s["st_phi"], s["st_ess"]
        assert len(phi) == len(ess), "st_phi / st_ess lengths differ in " + f
        for t, e in enumerate(ess):
            p0 = phi[t - 1] if t else 0.0
            recs.append({"ess": e, "ess_over_N": e / N, "island": f, "stage": t + 1, "phi_from": p0, "phi_to": phi[t], "dphi": phi[t] - p0})
    mn = min(recs, key=lambda r: r["ess"])
    return mn, [r for r in sorted(recs, key=lambda r: r["ess"]) if r["ess"] < LOW * N], len(recs)

def decide(fit):
    """the H-48 rule on one fit dict: returns (low_ESS: bool, reasons: list, flag_stop: bool)"""
    low = bool(fit["low_empirical_ESS"]) or bool(fit["ess_low_stages"])
    reasons = []
    if any(fit["E"].get(k) for k in ("E1", "E2", "E3")): reasons.append("E-flag " + ",".join(k for k in ("E1", "E2", "E3") if fit["E"].get(k)))
    if fit["sigma_hat"] is not None and fit["sigma_hat"] > SIGMA_STOP: reasons.append("sigma-hat %.4f > %.1f" % (fit["sigma_hat"], SIGMA_STOP))
    if fit["C2_verdict"] != "PASS": reasons.append("C2 %s" % fit["C2_verdict"])
    if not fit["hpm_eq_S0"]: reasons.append("HPM != S0")
    return low, reasons, bool(low and reasons)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--wave", required=True); ap.add_argument("--records-dir", required=True, nargs="+", help="records/gc1m/<batch> dir(s) holding the fit units")
    ap.add_argument("--ess-json", required=True); ap.add_argument("--readback-json"); ap.add_argument("--out-dir", required=True)
    ap.add_argument("--gc-readback", default="/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/results/gc1m/gc_readback.py")
    a = ap.parse_args(); os.makedirs(a.out_dir, exist_ok=True)
    units = sorted(u for d in a.records_dir for u in glob.glob(os.path.join(d, "6-*")) if os.path.isdir(u))
    if not units: sys.exit("no fit units under %s" % a.records_dir)
    rb = json.load(open(a.readback_json)) if a.readback_json else None
    if rb is None:   # the registered read-back, UNEDITED, scoped to this wave's records
        odir = os.path.join(a.out_dir, "gc_readback_%s" % a.wave); os.makedirs(odir, exist_ok=True); out = os.path.join(odir, "gc_readback.json")
        r = subprocess.run([sys.executable, a.gc_readback, "--records"] + list(a.records_dir) + ["--out", odir], capture_output=True, text=True)
        if r.returncode not in (0, 1) or not os.path.exists(out): sys.exit("gc_readback.py failed (rc %d): %s" % (r.returncode, r.stderr[-400:]))
        rb = json.load(open(out))
    ess = json.load(open(a.ess_json)); ess_by_run = {}
    for k, v in ess.items(): ess_by_run[os.path.basename(k.rstrip("/"))] = v
    fits = []
    for u in units:
        rid = os.path.basename(u); ev = json.load(open(os.path.join(u, "eval.bin.json"))); cm = json.load(open(os.path.join(u, "calib_meta.json")))["meta"]; N = cm["N"]
        f = rb["fits"][rid]; sel = ev["selection"]; evd = ev["evidence"]; lz = evd["logZ_r"]; mean = sum(lz) / len(lz); sd = math.sqrt(sum((x - mean) ** 2 for x in lz) / (len(lz) - 1))
        if rid not in ess_by_run: sys.exit("no ESS data for %s (--ess-json has %s)" % (rid, sorted(ess_by_run)))
        mn, lows, n_st = ess_dips(ess_by_run[rid], N)
        fit = {"run_id": rid, "N": N, "hpm": sel["hpm"], "hpm_eq_S0": bool(sel["hpm_eq_S0"]), "mpm_eq_S0": bool(sel["mpm_eq_S0"]), "E": {k: bool(f["C5"].get(k)) for k in ("E1", "E2", "E3")},
               "sigma_hat": evd.get("sigma_hat"), "sd_logZ_r": sd, "C2_verdict": f["C2"]["verdict"], "C2": {k: f["C2"].get(k) for k in ("M1", "M2", "evidence_gap", "evidence_bound_3se", "local_certified", "max_abs_eq_minus_T", "eq_T_target")},
               "low_empirical_ESS": bool(f["C5"].get("low_empirical_ESS")), "min_ess": mn, "n_islands": len(ess_by_run[rid]), "n_island_stages": n_st, "ess_low_stages": lows}
        low, reasons, stop = decide(fit); fit.update(low_ESS=low, flag_reasons=reasons, flag_stop=stop, ess_flag_consistent=(bool(lows) == fit["low_empirical_ESS"])); fits.append(fit)
    any_stop = any(x["flag_stop"] for x in fits)
    out = {"wave": a.wave, "rule": "H-48: low_empirical_ESS together with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0 -> FLAG, STOP; low_ESS alone is reported (H-49: expected ~ 1 in 7 fits on the frozen arm)", "fits": fits, "flag_stop": any_stop}
    json.dump(out, open(os.path.join(a.out_dir, "wave_check_%s.json" % a.wave), "w"), indent=1); open(os.path.join(a.out_dir, "wave_check_%s.json" % a.wave), "a").write("\n")
    L = ["# wave check %s (HQ H-48 / H-49)" % a.wave, "", "**%s**" % ("FLAG: STOP, tell the manager, no next wave: " + "; ".join("%s (%s)" % (x["run_id"], ", ".join(x["flag_reasons"])) for x in fits if x["flag_stop"]) if any_stop else "no FLAG: no fit has low_empirical_ESS together with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0"), ""]
    L += ["| fit | HPM = S0 | MPM = S0 | E1 / E2 / E3 | sigma-hat (sd log Z_r) | C2 | min ESS / N | island, stage | phi step (dphi) at the dip | low_empirical_ESS (engine / sections) | flag |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in fits:
        m = x["min_ess"]; L.append("| %s | %s | %s | %s | %.4f (%.4f) | %s (M1 %.4f, M2 %.5f, evid gap %.4f <= %.4f) | **%.3f** (ESS %.1f of N %d) | %s, stage %d | %.4f -> %.4f, **dphi %.4f** | %s / %s | %s |" % (
            x["run_id"], "yes" if x["hpm_eq_S0"] else "**NO**", "yes" if x["mpm_eq_S0"] else "**NO**", " / ".join("TRUE" if x["E"][k] else "False" for k in ("E1", "E2", "E3")), x["sigma_hat"], x["sd_logZ_r"], x["C2_verdict"], x["C2"]["M1"], x["C2"]["M2"], x["C2"]["evidence_gap"], x["C2"]["evidence_bound_3se"],
            m["ess_over_N"], m["ess"], x["N"], m["island"], m["stage"], m["phi_from"], m["phi_to"], m["dphi"], "TRUE" if x["low_empirical_ESS"] else "False", "TRUE" if x["ess_low_stages"] else "False", "**STOP: " + ", ".join(x["flag_reasons"]) + "**" if x["flag_stop"] else ("low_ESS alone: reported" if x["low_ESS"] else "-")))
    L += ["", "## Every low_ESS fit (island-stages with ESS < 0.5 N)"]
    lows = [x for x in fits if x["low_ESS"]]
    if not lows: L.append("- none in this wave")
    for x in lows:
        L.append("- **%s**: %d island-stage(s) of %d below 0.5 N = %d: %s; min ESS/N %.3f; %s" % (x["run_id"], len(x["ess_low_stages"]), x["n_island_stages"], x["N"] // 2, "; ".join("%s stage %d ESS %.1f (%.3f N), phi %.4f -> %.4f, dphi %.4f" % (r["island"], r["stage"], r["ess"], r["ess_over_N"], r["phi_from"], r["phi_to"], r["dphi"]) for r in x["ess_low_stages"]),
                 x["min_ess"]["ess_over_N"], "engine flag and sections AGREE" if x["ess_flag_consistent"] else "**engine flag and section ESS DISAGREE**"))
    L += ["", "H-48 rule: STOP only for low_ESS with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0; low_ESS alone is reported (H-49: expected about 1 fit in 7). The ESS values are read from the island sections st_ess / st_phi (the engine's own per-stage ESS; Delta-phi = st_phi[t] - st_phi[t-1], the first stage from 0)."]
    open(os.path.join(a.out_dir, "wave_check_%s.md" % a.wave), "w").write("\n".join(L) + "\n")
    print("wave_check_%s: %d fits; %s; low_ESS fits: %s" % (a.wave, len(fits), "FLAG: STOP" if any_stop else "no FLAG", ", ".join(x["run_id"] for x in lows) or "none"))
    sys.exit(2 if any_stop else 0)

if __name__ == "__main__":
    main()
