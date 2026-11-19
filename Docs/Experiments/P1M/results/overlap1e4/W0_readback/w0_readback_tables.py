#!/usr/bin/env python3
"""w0_readback_tables.py -- W0 read-back cost / escalation tables (stdlib only, read-only on records/overlap1e4/W0).
Writes W0_sacct_jobs.csv, W0_cost_stages.csv, W0_escalation.csv into --out."""
import argparse, csv, glob, json, os, re, sys

FIELDS = ["JobID", "JobName", "State", "ElapsedRaw", "AllocCPUS", "CPUTimeRAW", "MaxRSS", "NodeList", "Timelimit"]
BATCHES = ["OV_W0_T", "OV_W0_V", "OV_W0_T2", "OV_W0_V2"]
ROLE = {"OV_W0_T": "evidence (merge refused, git unknown)", "OV_W0_V": "evidence (V cross-check)", "OV_W0_T2": "COUNTS (T)", "OV_W0_V2": "COUNTS (V)"}


def rss_mb(s):
    if not s:
        return 0.0
    m = {"K": 1 / 1024, "M": 1, "G": 1024, "T": 1024 * 1024}
    return float(s[:-1]) * m[s[-1]] if s[-1] in m else float(s) / 1048576


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rec", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    sacct = {}
    for line in open(os.path.join(a.rec, "_batch_OV_W0_T2", "sacct_dump.txt")):
        if line.strip():
            f = line.rstrip("\n").split("|"); r = dict(zip(FIELDS, f)); sacct[r["JobID"]] = r
    # ---- A: job-level rows
    rows = []
    for b in BATCHES:
        subs = [json.loads(l) for l in open(os.path.join(a.rec, "_batch_" + b, "submissions.jsonl")) if l.strip()]
        order = []
        for s in subs:
            if s["fit"] != "all" and s["fit"] not in order:
                order.append(s["fit"])
        for s in subs:
            jid = s["job"]
            for k, r in sacct.items():
                if "." in k:
                    continue
                if not (k == jid or k.startswith(jid + "_")):
                    continue
                fit = s["fit"]
                if fit == "all":
                    m = re.match(r"\d+_(\d+)$", k); fit = order[int(m.group(1)) - 1] if m else "all"
                rss = max([rss_mb(v["MaxRSS"]) for kk, v in sacct.items() if kk.startswith(k + ".")] or [0])
                cpu = int(r["CPUTimeRAW"] or 0)
                rows.append({"batch": b, "role": ROLE[b], "stage": s["stage"], "fit": fit, "jobid": k, "state": r["State"],
                             "elapsed_s": int(r["ElapsedRaw"] or 0), "alloc_cpus": int(r["AllocCPUS"] or 0), "cputimeraw_s": cpu,
                             "core_h": round(cpu / 3600, 4), "maxrss_mb": round(rss, 1), "node": r["NodeList"], "timelimit": r["Timelimit"]})
    with open(os.path.join(a.out, "W0_sacct_jobs.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    # ---- B: stage-level from the p1m_cost.py records (billed = CPUTimeRAW/3600)
    srows = []
    for b in BATCHES:
        for f in sorted(glob.glob(os.path.join(a.rec, "_batch_" + b, "cost", "cost_4-*.json"))):
            j = json.load(open(f))
            for st, d in j["stages"].items():
                srows.append({"batch": b, "role": ROLE[b], "fit": j["run_id"], "stage": st, "tasks": d["tasks"], "wall_s_max": d["wall_s_max"],
                              "billed_core_h": d["billed_core_h"], "max_rss_mb": round(d["max_rss_bytes"] / 1048576, 1), "states": "/".join(d["states"])})
            srows.append({"batch": b, "role": ROLE[b], "fit": j["run_id"], "stage": "TOTAL", "tasks": "", "wall_s_max": "",
                          "billed_core_h": j["billed_core_h"], "max_rss_mb": "", "states": ""})
    with open(os.path.join(a.out, "W0_cost_stages.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(srows[0].keys())); w.writeheader(); w.writerows(srows)
    # ---- C: escalation data (counted batches)
    def stage(b, fit, st):
        for r in srows:
            if r["batch"] == b and r["fit"] == fit and r["stage"] == st:
                return r
        return None
    erows = []
    for b in ("OV_W0_T2", "OV_W0_V2"):
        arm = "T" if b.endswith("T2") else "V"
        for ds in ("4-AR-n200-r01", "4-ADJOPP-n200-r01"):
            fit = "%s-%s-s1" % (ds, arm); unit = os.path.join(a.rec, "%s.%s2" % (fit, arm))
            cb = json.load(open(os.path.join(unit, "calib.bin.json"))); tiers = cb["settings"]["tiers"]; tf = cb["tier_final"]
            Nfin = [t["N_final"] for t in tiers if t["tier"] == tf][0]
            cal = stage(b, fit, "calibrate")["billed_core_h"]
            # tier split of the calibration from cost-file mtimes (rsync -a keeps NOTS mtimes): +-2 min, ESTIMATE
            t0 = [os.path.getmtime(p) for p in glob.glob(os.path.join(unit, "cost", "cost_*_t0_*.jsonl"))]
            t1 = [os.path.getmtime(p) for p in glob.glob(os.path.join(unit, "cost", "cost_*_t1_*.jsonl"))]
            cal_wall = stage(b, fit, "calibrate")["wall_s_max"]
            split = ""
            if t1 and t0:
                end = max(t1); start = end - cal_wall; tier0_s = max(t0) - start
                split = "tier0 ~%.0f s (%.1f core-h), tier1 ~%.0f s (%.1f core-h) [mtimes, +-2 min]" % (tier0_s, cal * tier0_s / cal_wall, cal_wall - tier0_s, cal * (cal_wall - tier0_s) / cal_wall)
            isl = stage(b, fit, "islands"); mrg = stage(b, fit, "merge"); ev = stage(b, fit, "eval"); setup = stage(b, fit, "setup")
            isl_r = stage(b, fit, "islands_rescue"); mrg_r = stage(b, fit, "merge_rescue"); ev_r = stage(b, fit, "eval_rescue")
            if isl_r:   # AR-T2: first islands refused at N 10^4 (wasted), final-N islands = the rescue
                final_isl, waste = isl_r, isl
                final_mrg, final_ev = mrg_r, ev_r
                waste_ch = round(isl["billed_core_h"] + mrg["billed_core_h"] + ev["billed_core_h"], 4)
            else:
                final_isl, waste, final_mrg, final_ev, waste_ch = isl, None, mrg, ev, 0.0
            tot = stage(b, fit, "TOTAL")["billed_core_h"]
            erows.append({"fit": fit, "batch": b, "arm": arm, "rule": cb["settings"]["rule"], "tier_final": tf, "N_final": Nfin, "N_tiers_run": len(tiers) if tf else 1,
                          "setup_core_h": setup["billed_core_h"], "calibrate_core_h": cal, "calibrate_wall_s": cal_wall, "calib_tier_split": split,
                          "islands_core_h_final_N": final_isl["billed_core_h"], "islands_wall_s_max": final_isl["wall_s_max"], "islands_tasks": final_isl["tasks"],
                          "merge_core_h": final_mrg["billed_core_h"], "eval_core_h": final_ev["billed_core_h"], "merge_eval_core_h": round(final_mrg["billed_core_h"] + final_ev["billed_core_h"], 4),
                          "refused_attempt_core_h": waste_ch, "fit_total_core_h": tot})
    with open(os.path.join(a.out, "W0_escalation.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(erows[0].keys())); w.writeheader(); w.writerows(erows)
    for r in erows:
        print(r)
    print(len(rows), "job rows;", len(srows), "stage rows")


if __name__ == "__main__":
    main()
