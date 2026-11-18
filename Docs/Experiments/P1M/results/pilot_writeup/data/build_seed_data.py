#!/usr/bin/env python3
"""One-off PROVENANCE script: builds the seed rows of scaling.csv and stages_1e6.csv.

Not needed to re-run make_figures.py. It documents where every number came from.
Reads (read-only):
  * /home/fb31/SMC_Engineering_Department/records/F1M_pilot/*.json, cost/*.jsonl, starts/ends.jsonl
  * results/F1M_PILOT_FIT.md, T5_1e5.md, ../LEDGER.md (sacct core-h are only in the .md/ledger, not in records)
  * ../rerun2400/verdict/per_fit.csv  (v2.2.1 vs v3.1 at p = 500, 1000)
Never overwrites data/scaling.csv: pass --out DIR (a scratch dir) and diff by hand.
Usage:  python3 build_seed_data.py --out /some/scratch/dir
"""
import argparse, csv, glob, json, os, datetime as dt

REC = "/home/fb31/SMC_Engineering_Department/records/F1M_pilot"
HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.abspath(os.path.join(HERE, "..", "..", ".."))           # .../Docs/Experiments/P1M
PER_FIT = os.path.join(EXP, "rerun2400", "verdict", "per_fit.csv")

SCALING_COLS = [
    "run_id", "p", "n", "design", "signal", "replicate", "in_rep_set", "engine", "mode", "fit_type", "status",
    "machine", "core_h", "wall_s", "wall_basis", "wall_e2e_s", "peak_rss_gib", "rss_basis", "peak_rss_sacct_gib",
    "hpm_eq_S0", "mpm_eq_S0", "logZ", "logZ_T",
    "pred_h2_hpm", "pred_h2_mpm", "pred_h2_T", "pred_h2_oracle", "kl_hpm", "kl_T", "test_mlpd_hpm", "test_mlpd_T",
    "evidence", "source", "notes"]
STAGE_COLS = [
    "run_id", "p", "stage", "n_tasks", "cpus_per_task", "mem_req_gb", "wall_s", "wall_mean_s", "wall_span_s",
    "core_h", "peak_mem_gib", "mem_basis", "evidence", "source", "wall_note"]


def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def jl(path):
    return [json.loads(l) for l in open(path) if l.strip()]


def pilot():
    ev = json.load(open(f"{REC}/eval.bin.json"))
    setup = json.load(open(f"{REC}/setup.bin.json"))
    d = ev["dist"]; sel = ev["selection"]
    starts, ends = jl(f"{REC}/starts.jsonl"), jl(f"{REC}/ends.jsonl")
    # island walls from the start/end log (task 2's start line is missing: 15 of 16)
    st = {(r["stage"], r["task"]): ts(r["start"]) for r in starts}
    en = {(r["stage"], r["task"]): ts(r["end"]) for r in ends}
    isl = [(en[k] - st[k]).total_seconds() for k in st if k[0] == "islands" and k in en]
    t_first = min(st[k] for k in st if k[0] == "islands"); t_last = max(en[k] for k in en if k[0] == "islands")
    span = (t_last - t_first).total_seconds()
    e2e = (en[("eval", "")] - st[("setup", "1")]).total_seconds()
    # calibration peak: max VmHWM over the 13 cost records (KiB -> GiB)
    cal_peak = max(max(r["hwm_kb"] for r in jl(f)[1:]) for f in glob.glob(f"{REC}/cost/cost_*.jsonl")) / 1024 ** 2
    setup_peak = setup["peak_rss_mb"] / 1024
    print(f"island walls (15 of 16 from log): min {min(isl):.0f} max {max(isl):.0f}; span {span:.0f}; e2e {e2e:.0f}; "
          f"cal peak {cal_peak:.2f} GiB; setup peak {setup_peak:.2f} GiB")

    # stage elapsed from sacct (F1M_PILOT_FIT.md); billed core-h likewise (CPUTimeRAW / 3600)
    stages = [  # stage, tasks, cpus, mem, wall(max), wall_mean, span, core_h, peak, basis, note
        ("setup", 1, 48, 48, 1144, 1144, 1143, 15.25, setup_peak, "process peak RSS (setup.bin.json peak_rss_mb, read as MiB)",
         f"sacct 19:04; inner seconds: correlation {setup['seconds']['correlation']:.0f}, tables {setup['seconds']['tables']:.0f}, start law {setup['seconds']['start_law']:.0f}"),
        ("calibrate", 1, 96, 128, 5086, 5086, 5085, 135.63, cal_peak, "process VmHWM (max of 13 cost records, KiB->GiB)",
         "sacct 1:24:46; inner 4,808 s; pilot island + 12 diagnostic islands (3 iterations x 4)"),
        ("islands", 16, 96, 64, 792, 16.83 * 3600 / 96, span, 269.25, 27.1, "process peak RSS per island (F1M_PILOT_FIT.md O2 cost records; 27.1 = late-round max)",
         "wall_s = slowest of 16 tasks (13:12); wall_mean_s = billed core-h/96 CPUs; wall_span_s = first start to last end (queue stagger, 1,536-CPU cap)"),
        ("merge", 1, 32, 80, 1902, 1902, 1900, 16.91, 75.1, "sacct MaxRSS incl. page cache (process need est. 26-34 GiB, INFERENCE: MERGE_MEM.md)",
         "sacct 31:42; recorded merge_islands 834 s is NESTED in merge_tail 1,215 s (whole command before write); ~690 s after it (write + exit)"),
        ("eval", 1, 8, 16, 181, 181, 179, 0.40, "", "not recorded", "sacct 3:01; inner eval_wall 38.9 s"),
    ]
    rows_st = [dict(run_id="6-AR-n200-r01-V-s1", p=1000000, stage=s[0], n_tasks=s[1], cpus_per_task=s[2], mem_req_gb=s[3],
                    wall_s=round(s[4]), wall_mean_s=round(s[5]), wall_span_s=round(s[6]), core_h=s[7], peak_mem_gib=(round(s[8], 2) if s[8] != "" else ""),
                    mem_basis=s[9], evidence="MEASURED", source="results/F1M_PILOT_FIT.md; records/F1M_pilot", wall_note=s[10]) for s in stages]
    wall_sum = sum(s[4] for s in stages)
    row = dict(
        run_id="6-AR-n200-r01-V-s1", p=1000000, n=200, design="AR", signal="strong", replicate=1, in_rep_set=1,
        engine="v4 smcbvs4", mode="V", fit_type="full fit", status="completed", machine="NOTS SPR (commons)",
        core_h=437.44, wall_s=wall_sum, wall_basis="stage_sum", wall_e2e_s=round(e2e), peak_rss_gib=round(cal_peak, 2),
        rss_basis="process peak (calibration VmHWM)", peak_rss_sacct_gib=75.1,
        hpm_eq_S0=int(sel["hpm_eq_S0"]), mpm_eq_S0=int(sel["mpm_eq_S0"]), logZ=ev["evidence"]["logZ"], logZ_T=ev["evidence"]["logZ_T"],
        pred_h2_hpm=d["H"]["predictive"]["h2"], pred_h2_mpm=d["M"]["predictive"]["h2"], pred_h2_T=d["T"]["predictive"]["h2"],
        pred_h2_oracle=d["oracle"]["predictive"]["h2"], kl_hpm=d["H"]["predictive"]["kl"], kl_T=d["T"]["predictive"]["kl"],
        test_mlpd_hpm=d["H"]["test"]["mlpd"], test_mlpd_T=d["T"]["test"]["mlpd"],
        evidence="MEASURED", source="results/F1M_PILOT_FIT.md; records/F1M_pilot/{eval,fit,setup,calib}.bin.json",
        notes="code 2cfaa9e5, seed 602020001, N 2500, R' 16; wall_s = sum of stage elapsed on critical path (slowest island, no queue wait); "
              "wall_e2e_s = 3:04 setup start to eval end incl. queueing; counts as replicate 1 conditional on freeze hash check (CAMPAIGN_PLAN_1117 s3)")
    return row, rows_st


def t5():
    cal = 594; wall = 46 + cal + 153 + 167 + 30
    row = dict(
        run_id="5-AR-n200-r01-V-s1", p=100000, n=200, design="AR", signal="strong", replicate=1, in_rep_set=0,
        engine="v4 smcbvs4", mode="V", fit_type="full fit", status="completed", machine="NOTS SPR (commons)",
        core_h=42.18, wall_s=wall, wall_basis="stage_sum", wall_e2e_s="", peak_rss_gib=11.0,
        rss_basis="process peak (calibration islands 8-11 GB; islands 4.5 GB; setup/merge not recorded)", peak_rss_sacct_gib="",
        hpm_eq_S0=1, mpm_eq_S0=1, logZ=-233.27, logZ_T="", pred_h2_hpm=0.00538, pred_h2_mpm=0.00538, pred_h2_T="", pred_h2_oracle=0.00538,
        kl_hpm="", kl_T="", test_mlpd_hpm="", test_mlpd_T="", evidence="MEASURED (core-h) / DERIVED (wall)",
        source="results/T5_1e5.md", notes="code 04d8d2b5 (no offer floor); core_h 42.18 includes the 2.21 core-h D-32 isa_check; wall_s = 46+594+153(slowest island)+167+30 s, "
        "isa_check excluded; HPM = MPM = S0 via plug-in h2 = oracle h2 (0.0047015); log Z, pred h2 as printed (3-5 sig. figs)")
    return row


def g0():
    base = dict(n=200, design="S3-type (s3gen)", signal="14 signals", replicate=1, in_rep_set=0, engine="v3 rev. D (stage run)", mode="stage run",
                fit_type="stage-level run (tier 0, LS0 off; NOT a full fit)", status="completed", machine="NOTS SPR (Xeon 8468)",
                wall_basis="job_elapsed", wall_e2e_s="", peak_rss_gib="", rss_basis="not recorded", peak_rss_sacct_gib="",
                hpm_eq_S0=1, mpm_eq_S0="", evidence="MEASURED", source="LEDGER.md; records/G0/stage_*/log")
    r5 = dict(base, run_id="G0-stage-p5000", p=5000, core_h=9.67, wall_s=17398,
              notes="job 2747799_1; 16 islands N 2,500; seed 20261111; HPM = truth; calibration + 16 islands, no escalation tiers")
    r10 = dict(base, run_id="G0-stage-p10000", p=10000, core_h=16.87, wall_s=30369,
               notes="job 2747372_2; 8 islands N 2,500; seed 20261111; HPM = truth; calibration + 8 islands, no escalation tiers")
    return [r5, r10]


def rerun():
    import pandas as pd
    d = pd.read_csv(PER_FIT)
    out = []
    for _, r in d.iterrows():
        for side, eng, key in (("old", "v2.2.1", "old"), ("new", "v3.1", "new")):
            ok = r[f"{key}_status"] == "completed"
            out.append(dict(
                run_id=f"{key.upper()}-{r.case_id}", p=int(r.p), n=200, design=f"PROD-H S{int(r.S)}", signal=f"c={0.5 if r.c == 'c050' else 1}",
                replicate=int(r.r), in_rep_set=0, engine=eng, mode="default fit", fit_type="full fit",
                status=r[f"{key}_status"], machine="NOTS SPR (1 CPU task)", core_h=round(2 * r[f"runtime_{key}"] / 3600, 5),
                wall_s=r[f"runtime_{key}"], wall_basis="record runtime_s", wall_e2e_s="",
                peak_rss_gib=round(r[f"rss_{key}_mb"] / 1024, 4), rss_basis="VmHWM end of fit", peak_rss_sacct_gib="",
                hpm_eq_S0="", mpm_eq_S0="", logZ="", logZ_T="", pred_h2_hpm="", pred_h2_mpm="", pred_h2_T="", pred_h2_oracle="",
                kl_hpm="", kl_T="", test_mlpd_hpm="", test_mlpd_T="", evidence="MEASURED",
                source="rerun2400/verdict/per_fit.csv; RERUN_2400_VERDICT.md",
                notes="paired same-node rerun rr2400_20261118T0636Z; core_h = 2 billed CPUs x runtime (1-CPU task); recovery vs S0 not in per_fit (hpm_F only: "
                      f"{r[f'hpm_F_{key}']:.6f})" + ("; known stop (resource_limit), excluded from medians" if not ok else "")))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    prow, pst = pilot()
    rows = rerun() + g0() + [t5(), prow]
    with open(os.path.join(a.out, "scaling.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCALING_COLS); w.writeheader(); [w.writerow(r) for r in rows]
    with open(os.path.join(a.out, "stages_1e6.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=STAGE_COLS); w.writeheader(); [w.writerow(r) for r in pst]
    print("wrote", len(rows), "scaling rows,", len(pst), "stage rows to", a.out)


if __name__ == "__main__":
    main()
