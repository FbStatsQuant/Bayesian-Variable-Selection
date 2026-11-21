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

def island_timing(batch_dirs):
    """H-50 / H-51 wave-line extra: per fit the island ELAPSED spread (sacct), the engine's own seconds.total (island_k.bin.json), the pre-engine wait (elapsed - engine total), the Slurm-billed island core-h against the
    engine-time core-h (total x allocated CPUs / 3600), and the elapsed by NODE TYPE (the node-name suffix bb<N>u<M><c|g><K>: c1 vs g1) from the batch's sacct dump (NodeList). Returns (per-fit dict, node-type dict, sentence)."""
    import re
    fits, bytype = {}, {}
    for d in batch_dirs:
        bn = os.path.basename(d.rstrip("/")); bu = os.path.join(d, "_batch_" + bn)
        if not os.path.exists(os.path.join(bu, "sacct_dump.txt")): continue
        jobfit = {}
        for l in open(os.path.join(bu, "submissions.jsonl")):
            j = json.loads(l)
            if j["stage"] == "islands": jobfit[j["job"]] = j["fit"]
        for l in open(os.path.join(bu, "sacct_dump.txt")):
            f = l.rstrip("\n").split("|")
            if len(f) < 8 or not re.match(r"^\d+_\d+$", f[0]) or "islands" not in f[1] or f[2] != "COMPLETED": continue
            base, k = f[0].split("_"); rid = jobfit.get(base)
            if rid is None: continue
            sc = os.path.join(d, rid, "island_%s.bin.json" % k); eng = json.load(open(sc))["seconds"]["total"] if os.path.exists(sc) else None
            node = f[7]; m = re.match(r"^bb\d+u\d+([a-z])\d+$", node); typ = m.group(1) if m else "?"
            rec = {"island": int(k), "elapsed": int(f[3]), "cpus": int(f[4]), "billed_core_h": int(f[5]) / 3600.0, "engine": eng, "node": node, "type": typ}
            fits.setdefault(rid, []).append(rec); bytype.setdefault(typ, []).append(rec)
    out = {}
    stat = lambda v: {"min": min(v), "mean": sum(v) / len(v), "max": max(v)} if v else None
    for rid, rs in fits.items():
        eng = [r for r in rs if r["engine"] is not None]
        out[rid] = {"n": len(rs), "elapsed": stat([r["elapsed"] for r in rs]), "engine_total": stat([r["engine"] for r in eng]), "pre_engine_wait": stat([r["elapsed"] - r["engine"] for r in eng]),
                    "billed_core_h": sum(r["billed_core_h"] for r in rs), "engine_core_h": sum(r["engine"] * r["cpus"] / 3600.0 for r in eng) if eng else None,
                    "max_engine_core_h": max((r["engine"] * r["cpus"] / 3600.0 for r in eng), default=None)}
    nt = {t: {"n": len(rs), "elapsed": stat([r["elapsed"] for r in rs]), "engine_total": stat([r["engine"] for r in rs if r["engine"] is not None]),
              "pre_engine_wait": stat([r["elapsed"] - r["engine"] for r in rs if r["engine"] is not None])} for t, rs in bytype.items()}
    sent = "no node-type contrast in this wave (single node type observed: %s)" % ", ".join(sorted(bytype)) if len(bytype) < 2 else None
    if sent is None:
        allr = [r for rs in bytype.values() for r in rs]; mean_el = {t: nt[t]["elapsed"]["mean"] for t in nt}; fast = min(mean_el, key=mean_el.get)
        save = sum(max(0.0, r["elapsed"] - mean_el[fast]) * r["cpus"] / 3600.0 for r in allr if r["type"] != fast); tot = sum(r["billed_core_h"] for r in allr)
        sent = ("Proposal only (a node constraint to type %s): the %s-type islands average %s s elapsed against %.0f s on type %s; had every island run at the %s mean, the wave would have billed about %.1f core-h less of %.1f island core-h (%.1f %%), "
                "before any extra queue wait that a constraint could add (not measured here), so it pays for itself only if the wait of the constrained type stays small."
                % (fast, "/".join(sorted(t for t in mean_el if t != fast)), "/".join("%.0f" % mean_el[t] for t in sorted(mean_el) if t != fast), mean_el[fast], fast, fast, save, tot, 100.0 * save / tot if tot else 0.0))
    return out, nt, sent

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
        fit = {"run_id": rid, "N": N, "pi_hat_S0": (f.get("science") or {}).get("pi_hat_S0"), "hpm": sel["hpm"], "hpm_eq_S0": bool(sel["hpm_eq_S0"]), "mpm_eq_S0": bool(sel["mpm_eq_S0"]), "E": {k: bool(f["C5"].get(k)) for k in ("E1", "E2", "E3")},
               "sigma_hat": evd.get("sigma_hat"), "sd_logZ_r": sd, "C2_verdict": f["C2"]["verdict"], "C2": {k: f["C2"].get(k) for k in ("M1", "M2", "evidence_gap", "evidence_bound_3se", "local_certified", "max_abs_eq_minus_T", "eq_T_target")},
               "low_empirical_ESS": bool(f["C5"].get("low_empirical_ESS")), "min_ess": mn, "n_islands": len(ess_by_run[rid]), "n_island_stages": n_st, "ess_low_stages": lows}
        low, reasons, stop = decide(fit); fit.update(low_ESS=low, flag_reasons=reasons, flag_stop=stop, ess_flag_consistent=(bool(lows) == fit["low_empirical_ESS"])); fits.append(fit)
    timing, bytype, tsent = island_timing(a.records_dir)
    any_stop = any(x["flag_stop"] for x in fits)
    out = {"wave": a.wave, "rule": "H-48: low_empirical_ESS together with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0 -> FLAG, STOP; low_ESS alone is reported (H-49: expected ~ 1 in 7 fits on the frozen arm)", "fits": fits, "flag_stop": any_stop, "island_timing": {"per_fit": timing, "by_node_type": bytype, "node_constraint_sentence": tsent}}
    L = ["# wave check %s (HQ H-48 / H-49)" % a.wave, "", "**%s**" % ("FLAG: STOP, tell the manager, no next wave: " + "; ".join("%s (%s)" % (x["run_id"], ", ".join(x["flag_reasons"])) for x in fits if x["flag_stop"]) if any_stop else "no FLAG: no fit has low_empirical_ESS together with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0"), ""]
    L += ["| fit | HPM = S0 | MPM = S0 | pi-hat(S0) | E1 / E2 / E3 | sigma-hat (sd log Z_r) | C2 | min ESS / N | island, stage | phi step (dphi) at the dip | low_empirical_ESS (engine / sections) | flag |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in fits:
        m = x["min_ess"]; L.append("| %s | %s | %s | %s | %s | %.4f (%.4f) | %s (M1 %.4f, M2 %.5f, evid gap %.4f <= %.4f) | **%.3f** (ESS %.1f of N %d) | %s, stage %d | %.4f -> %.4f, **dphi %.4f** | %s / %s | %s |" % (
            x["run_id"], "yes" if x["hpm_eq_S0"] else "**NO**", "yes" if x["mpm_eq_S0"] else "**NO**", ("%.3f" % x["pi_hat_S0"]) if x.get("pi_hat_S0") is not None else "n/a", " / ".join("TRUE" if x["E"][k] else "False" for k in ("E1", "E2", "E3")), x["sigma_hat"], x["sd_logZ_r"], x["C2_verdict"], x["C2"]["M1"], x["C2"]["M2"], x["C2"]["evidence_gap"], x["C2"]["evidence_bound_3se"],
            m["ess_over_N"], m["ess"], x["N"], m["island"], m["stage"], m["phi_from"], m["phi_to"], m["dphi"], "TRUE" if x["low_empirical_ESS"] else "False", "TRUE" if x["ess_low_stages"] else "False", "**STOP: " + ", ".join(x["flag_reasons"]) + "**" if x["flag_stop"] else ("low_ESS alone: reported" if x["low_ESS"] else "-")))
    L += ["", "## Every low_ESS fit (island-stages with ESS < 0.5 N)"]
    lows = [x for x in fits if x["low_ESS"]]
    if not lows: L.append("- none in this wave")
    for x in lows:
        L.append("- **%s**: %d island-stage(s) of %d below 0.5 N = %d: %s; min ESS/N %.3f; %s" % (x["run_id"], len(x["ess_low_stages"]), x["n_island_stages"], x["N"] // 2, "; ".join("%s stage %d ESS %.1f (%.3f N), phi %.4f -> %.4f, dphi %.4f" % (r["island"], r["stage"], r["ess"], r["ess_over_N"], r["phi_from"], r["phi_to"], r["dphi"]) for r in x["ess_low_stages"]),
                 x["min_ess"]["ess_over_N"], "engine flag and sections AGREE" if x["ess_flag_consistent"] else "**engine flag and section ESS DISAGREE**"))
    L += ["", "## Island timing (H-50 / H-51): elapsed vs engine time, pre-engine wait, billed vs engine-time cost, node types"]
    for rid, t in timing.items():
        e, g, w = t["elapsed"], t["engine_total"], t["pre_engine_wait"]
        L.append("- **%s** (%d islands): Slurm elapsed min / mean / max **%d / %.0f / %d s**; engine `seconds.total` %s; **pre-engine wait (elapsed - engine) %s**; **Slurm-billed island cost %.1f core-h** beside the **engine-time cost %s** (max single island %s core-h; K2 compute line 33.6)." % (
            rid, t["n"], e["min"], e["mean"], e["max"], ("%d / %.0f / %d s" % (g["min"], g["mean"], g["max"])) if g else "n/a (no sidecars)", ("%d / %.0f / %d s" % (w["min"], w["mean"], w["max"])) if w else "n/a", t["billed_core_h"],
            ("%.1f core-h" % t["engine_core_h"]) if t["engine_core_h"] is not None else "n/a", ("%.1f" % t["max_engine_core_h"]) if t["max_engine_core_h"] is not None else "n/a"))
    for typ, t in sorted(bytype.items()):
        e, g, w = t["elapsed"], t["engine_total"], t["pre_engine_wait"]
        L.append("- node type **%s**: %d islands, elapsed min / mean / max %d / %.0f / %d s; engine mean %s; pre-engine wait mean %s." % (typ, t["n"], e["min"], e["mean"], e["max"], ("%.0f s" % g["mean"]) if g else "n/a", ("%.0f s" % w["mean"]) if w else "n/a"))
    allw = []; allb = 0.0; alle = 0.0
    if timing:
        n_all = sum(t["n"] for t in timing.values()); wsum = sum(t["pre_engine_wait"]["mean"] * t["n"] for t in timing.values() if t["pre_engine_wait"])
        n_w = sum(t["n"] for t in timing.values() if t["pre_engine_wait"]); mean_wait = wsum / n_w if n_w else None
        bill = sum(t["billed_core_h"] for t in timing.values()); eng = sum(t["engine_core_h"] or 0.0 for t in timing.values())
        out["island_timing"]["wave"] = {"islands": n_all, "mean_pre_engine_wait_s": mean_wait, "slurm_billed_island_core_h": bill, "engine_island_core_h": eng, "H52_throttle_rule": (None if mean_wait is None else ("mean wait > 300 s: W3 onward %8 island-array throttle per fit, stagger kept" if mean_wait > 300 else "mean wait <= 300 s: stagger only"))}
        L.append("- **Wave: mean pre-engine wait per island %s s over %d islands (W1: 526 / 373 s per fit; pilot 205 s); Slurm-billed island cost %.1f core-h vs engine-time %.1f core-h. HQ H-52 rule: %s.**" % ("%.0f" % mean_wait if mean_wait is not None else "n/a", n_w, bill, eng, out["island_timing"]["wave"]["H52_throttle_rule"]))
    L.append("- Node constraint, one sentence: " + tsent)
    L += ["", "H-48 rule: STOP only for low_ESS with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0; low_ESS alone is reported (H-49: expected about 1 fit in 7). The ESS values are read from the island sections st_ess / st_phi (the engine's own per-stage ESS; Delta-phi = st_phi[t] - st_phi[t-1], the first stage from 0)."]
    open(os.path.join(a.out_dir, "wave_check_%s.md" % a.wave), "w").write("\n".join(L) + "\n")
    json.dump(out, open(os.path.join(a.out_dir, "wave_check_%s.json" % a.wave), "w"), indent=1); open(os.path.join(a.out_dir, "wave_check_%s.json" % a.wave), "a").write("\n")
    print("wave_check_%s: %d fits; %s; low_ESS fits: %s" % (a.wave, len(fits), "FLAG: STOP" if any_stop else "no FLAG", ", ".join(x["run_id"] for x in lows) or "none"))
    sys.exit(2 if any_stop else 0)

if __name__ == "__main__":
    main()
