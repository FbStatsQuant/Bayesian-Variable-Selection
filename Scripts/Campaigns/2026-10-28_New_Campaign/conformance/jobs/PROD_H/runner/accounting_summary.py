"""Core-hour totals by array from a terminal sacct snapshot (Python 3.9 standard library only).

Usage: python3 accounting_summary.py RUN_DIR SACCT_TSV OUT_PREFIX
SACCT_TSV is the pipe-separated sacct output (header first) with JobID,JobName,State,ExitCode,Elapsed,NodeList,MaxRSS,AllocCPUS,CPUTimeRAW.
Groups (from RUN_DIR/jobs.tsv kinds): primary_p500, primary_p1000, p5, p5scan (the compute jobs of p5_scan_run.sh), precompile, reruns (every rerun_N).
Per group, job-level rows only (array tasks ID_n; no steps): tasks, states, alloc_cpu_hours = sum(CPUTimeRAW)/3600 (CPUs as allocated and
billed by Slurm), elapsed_core_hours = sum(Elapsed)/3600 (1 CPU per task as requested), and the largest MaxRSS of the step rows (MB).
Two different ceilings are shown (Sol review 2): the NATIVE-FIT-BUDGET ceiling is the sum of the native fit budgets (600 tasks x 2 fits x L:
p500 2,100 h, p1000 8,000 h = 10,100 core-hours; it excludes the 300 s hard-limit margins, the 60 s KILL grace and the 600 s per-task overhead) and
the REQUESTED-WALL ceiling is the Slurm wall requested by the primary arrays (600 tasks x 03:52:00 = 2,320 h, 600 x 13:42:00 = 8,220 h =
10,540 core-hours; 10,541 with the one-hour precompile request). Neither includes reruns or P5. Expected usage and billed logical-CPU time are
other quantities again (allocated vs elapsed, below).
Writes OUT_PREFIX.tsv and OUT_PREFIX.json.
"""
import csv
import json
import re
import sys
from pathlib import Path

NATIVE_FIT_BUDGET_H = {"primary_p500": 2100.0, "primary_p1000": 8000.0}    # 600 tasks x 2 fits x L / 3600 (native fit budgets only)
REQUESTED_WALL_H = {"primary_p500": 2320.0, "primary_p1000": 8220.0, "precompile": 1.0}   # 600 x 03:52:00; 600 x 13:42:00; 1 x 01:00:00


def secs(e):
    m = re.match(r"^(?:(\d+)-)?(\d+):(\d+):(\d+)(?:\.\d+)?$", e or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return ((d * 24 + h) * 60 + mi) * 60 + s


def mb(r):
    m = re.match(r"^([0-9.]+)([KMGT]?)$", r or "")
    if not m:
        return 0.0
    return float(m.group(1)) * {"": 1 / 1048576, "K": 1 / 1024, "M": 1, "G": 1024, "T": 1048576}[m.group(2)]


def main(argv):
    run_dir, tsv, prefix = Path(argv[0]), Path(argv[1]), argv[2]
    kinds = {r["job"]: r["kind"] for r in csv.DictReader(open(run_dir / "jobs.tsv", newline=""), delimiter="\t")}
    group_of = lambda job: ("reruns" if kinds.get(job, "").startswith("rerun_") else
                            "p5scan" if kinds.get(job, "").startswith("p5scan_") else kinds.get(job, "unknown"))
    g = {}
    with open(tsv, newline="") as f:
        for r in csv.DictReader(f, delimiter="|"):
            jid = r["JobID"]
            job = re.split(r"[_.]", jid)[0]
            grp = g.setdefault(group_of(job), dict(tasks=0, states={}, cpu_s=0, elapsed_s=0, max_rss_mb=0.0))
            if "." in jid:
                grp["max_rss_mb"] = max(grp["max_rss_mb"], mb(r["MaxRSS"]))
                continue
            grp["tasks"] += 1
            st = r["State"].split()[0].rstrip("+")
            grp["states"][st] = grp["states"].get(st, 0) + 1
            grp["cpu_s"] += int(r["CPUTimeRAW"] or 0)
            grp["elapsed_s"] += secs(r["Elapsed"])
    out = {}
    for name in ("primary_p500", "primary_p1000", "p5", "p5scan", "precompile", "reruns"):
        x = g.get(name, dict(tasks=0, states={}, cpu_s=0, elapsed_s=0, max_rss_mb=0.0))
        out[name] = dict(tasks=x["tasks"], states=x["states"], alloc_cpu_hours=round(x["cpu_s"] / 3600, 2),
                         elapsed_core_hours=round(x["elapsed_s"] / 3600, 2), native_fit_budget_ceiling_core_hours=NATIVE_FIT_BUDGET_H.get(name),
                         requested_wall_ceiling_core_hours=REQUESTED_WALL_H.get(name),
                         max_step_maxrss_mb=round(x["max_rss_mb"], 1))
    out["total"] = dict(alloc_cpu_hours=round(sum(v["alloc_cpu_hours"] for k, v in out.items() if k != "total"), 2),
                        elapsed_core_hours=round(sum(v["elapsed_core_hours"] for k, v in out.items() if k != "total"), 2),
                        native_fit_budget_ceiling_core_hours=sum(NATIVE_FIT_BUDGET_H.values()),
                        requested_wall_ceiling_primary_core_hours=REQUESTED_WALL_H["primary_p500"] + REQUESTED_WALL_H["primary_p1000"],
                        requested_wall_ceiling_with_precompile_core_hours=sum(REQUESTED_WALL_H.values()))
    if "unknown" in g:
        out["unknown_job_rows"] = g["unknown"]["tasks"]
    cols = ["group", "tasks", "states", "alloc_cpu_hours", "elapsed_core_hours", "native_fit_budget_ceiling_core_hours",
            "requested_wall_ceiling_core_hours", "max_step_maxrss_mb"]
    with open(prefix + ".tsv", "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(cols)
        for k, v in out.items():
            if k in ("total", "unknown_job_rows"):
                continue
            w.writerow([k, v["tasks"], ";".join("%s=%d" % kv for kv in sorted(v["states"].items())), v["alloc_cpu_hours"],
                        v["elapsed_core_hours"], v["native_fit_budget_ceiling_core_hours"] or "", v["requested_wall_ceiling_core_hours"] or "",
                        v["max_step_maxrss_mb"]])
        w.writerow(["total", "", "", out["total"]["alloc_cpu_hours"], out["total"]["elapsed_core_hours"],
                    out["total"]["native_fit_budget_ceiling_core_hours"], out["total"]["requested_wall_ceiling_with_precompile_core_hours"], ""])
    Path(prefix + ".json").write_text(json.dumps(out, indent=1) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1:])))
