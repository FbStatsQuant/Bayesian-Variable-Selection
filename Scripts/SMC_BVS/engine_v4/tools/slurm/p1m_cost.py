#!/usr/bin/env python3
"""p1m_cost.py -- cost fields of the evaluator (EXPERIMENT_PLAN §3.5) from ONE sacct dump per batch. Stdlib only.

The manager runs one sacct call per batch (POLICIES §12: at most one per 5 minutes), e.g.
  sacct -P -n -j <ids> --format=JobID,JobName,State,ElapsedRaw,AllocCPUS,CPUTimeRAW,MaxRSS,NodeList,Timelimit > sacct.txt
then:  p1m_cost.py --sacct sacct.txt --submissions submissions.jsonl --out-dir <dir>
writes <dir>/cost_<run_id>.json (per stage: wall s, billed core-h = CPUTimeRAW/3600, peak MaxRSS) and cost_batch.json.
`smcbvs4 eval --cost cost_<run_id>.json` (or a re-run of eval) folds it into the per-fit record.
"""
import argparse
import json
import os
import sys

FIELDS = ["JobID", "JobName", "State", "ElapsedRaw", "AllocCPUS", "CPUTimeRAW", "MaxRSS", "NodeList", "Timelimit"]


def rss_bytes(s):
    if not s:
        return 0
    mult = {"K": 1 << 10, "M": 1 << 20, "G": 1 << 30, "T": 1 << 40}
    return int(float(s[:-1]) * mult[s[-1]]) if s[-1] in mult else int(s)


def parse_sacct(text):
    """Allocation lines (JobID without '.') carry CPUTimeRAW (billed CPUs x elapsed); step lines carry MaxRSS."""
    alloc, rss = {}, {}
    for line in text.splitlines():
        if not line.strip():
            continue
        f = line.split("|")
        if len(f) < len(FIELDS):
            raise ValueError("sacct line has %d fields, expected %d: %r" % (len(f), len(FIELDS), line))
        r = dict(zip(FIELDS, f))
        jid = r["JobID"]
        if "." in jid:
            base = jid.split(".")[0]
            rss[base] = max(rss.get(base, 0), rss_bytes(r["MaxRSS"]))
        else:
            alloc[jid] = {"job": jid, "name": r["JobName"], "state": r["State"], "elapsed_s": int(r["ElapsedRaw"] or 0),
                          "cpus": int(r["AllocCPUS"] or 0), "cpu_time_raw": int(r["CPUTimeRAW"] or 0), "node": r["NodeList"]}
    for jid, a in alloc.items():
        a["max_rss_bytes"] = rss.get(jid, 0)
    return alloc


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sacct", required=True)
    ap.add_argument("--submissions", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args(argv)
    with open(a.sacct) as fh:
        alloc = parse_sacct(fh.read())
    subs = []
    with open(a.submissions) as fh:
        for line in fh:
            if line.strip():
                subs.append(json.loads(line))
    order = runs_all_order(subs)
    per_run = {r: {"run_id": r, "stages": {}} for r in order}
    batch_tot = {"billed_core_h": 0.0, "jobs": 0, "states": {}}
    for s in subs:
        jid = s["job"].split(";")[0]
        tasks = [v for k, v in alloc.items() if k == jid or k.startswith(jid + "_")]
        for t in tasks:
            batch_tot["billed_core_h"] += t["cpu_time_raw"] / 3600.0
            batch_tot["jobs"] += 1
            batch_tot["states"][t["state"]] = batch_tot["states"].get(t["state"], 0) + 1
        if s["fit"] == "all":   # setup / calibrate arrays: task i belongs to the i-th run (fit index order)
            for i, r in enumerate(order):
                per_run[r]["stages"][s["stage"]] = summarise([t for t in tasks if t["job"] == "%s_%d" % (jid, i + 1)])
        else:
            per_run[s["fit"]]["stages"][s["stage"]] = summarise(tasks)
    os.makedirs(a.out_dir, exist_ok=True)
    for r, d in per_run.items():
        d["billed_core_h"] = round(sum(st["billed_core_h"] for st in d["stages"].values()), 4)
        d["source"] = os.path.basename(a.sacct)
        with open(os.path.join(a.out_dir, "cost_%s.json" % r), "w") as fh:
            json.dump(d, fh, indent=1)
    batch_tot["billed_core_h"] = round(batch_tot["billed_core_h"], 4)
    with open(os.path.join(a.out_dir, "cost_batch.json"), "w") as fh:
        json.dump(batch_tot, fh, indent=1)
    print("cost: %d runs, %.2f billed core-h (MEASURED, sacct CPUTimeRAW)" % (len(per_run), batch_tot["billed_core_h"]))
    return 0


def runs_all_order(subs):
    """Run ids in fit-index order, from the per-fit submissions (islands lines appear in index order)."""
    order = []
    for s in subs:
        if s["fit"] != "all" and s["fit"] not in order:
            order.append(s["fit"])
    return order


def summarise(tasks):
    return {"tasks": len(tasks), "wall_s_max": max([t["elapsed_s"] for t in tasks] or [0]),
            "billed_core_h": round(sum(t["cpu_time_raw"] for t in tasks) / 3600.0, 4),
            "max_rss_bytes": max([t["max_rss_bytes"] for t in tasks] or [0]),
            "states": sorted({t["state"] for t in tasks}), "nodes": sorted({t["node"] for t in tasks})}


if __name__ == "__main__":
    sys.exit(main())
