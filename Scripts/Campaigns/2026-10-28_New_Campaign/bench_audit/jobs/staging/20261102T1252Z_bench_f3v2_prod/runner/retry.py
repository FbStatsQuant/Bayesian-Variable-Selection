#!/usr/bin/env python3
"""Submit at most one retry for each primary TIMEOUT task, after accounting is terminal."""
import argparse
import csv
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
from reconcile import check_case
from units import units
import throttle as throttle_gate
from terminal import assert_absent
from validate_args import args_for

TERMINAL = {"COMPLETED", "FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "NODE_FAIL", "PREEMPTED", "BOOT_FAIL", "DEADLINE"}


def select(text, job, expected):
    found = {}
    for row in csv.DictReader(text.splitlines(), delimiter="|"):
        jid = row["JobID"]
        m = re.fullmatch(re.escape(job) + r"_(\d+)", jid)
        if not m:
            continue
        index = int(m[1]); state = row["State"].split()[0].rstrip("+")
        if index in found or index not in expected or state not in TERMINAL:
            raise ValueError(f"duplicate, unexpected or nonterminal task {jid} {state}")
        found[index] = state
    if set(found) != set(expected):
        raise ValueError(f"incomplete accounting for {job}: {len(found)}/{len(expected)}")
    return found


def retry_command(job, selected, kind, run_id, runner, source, logs, limit=30):
    return ["sbatch", "--parsable", "--account=commons", "--partition=commons",
            "--qos=nots_commons", "--constraint=sapphirerapids", "--ntasks=1",
            "--cpus-per-task=1", "--export=NONE", "--no-requeue",
            "--array=" + ",".join(str(i) for i, _ in selected) + ("%" + str(min(26, limit) if kind == "dev" else limit)),
            "--time=" + str(2 * int(job["minutes"])), "--mem=" + job["mem_gib"] + "G",
            "--output=" + str(logs / "slurm" / "%A_%a_retry.out"),
            "--chdir=/scratch/fb31/New_Campaign", "--comment=" + run_id,
               "--job-name=f3v2_" + run_id + "_retry_" + job["cell"],
            str(runner / "task.sh"), str(runner), kind, run_id, source, "2"]


def claim(marker, cmd):
    with marker.open("x", encoding="utf-8") as f:
        f.write(shlex.join(cmd) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=("dev", "prod"))
    ap.add_argument("run_id")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--throttle", type=int)
    a = ap.parse_args()
    if not re.fullmatch(r"[0-9]{8}T[0-9]{4,6}Z_bench_f3v2_" + a.kind, a.run_id):
        ap.error("invalid run id")
    a.throttle = a.throttle if a.throttle is not None else (13 if a.kind == "dev" else 30)
    if not 1 <= a.throttle <= 96:
        ap.error("throttle must be 1..96")
    runner = Path(__file__).resolve().parent
    freeze = json.loads((runner / "freeze.json").read_text())
    source = freeze["source_sha256"]
    if not re.fullmatch(r"[0-9a-f]{64}", source):
        raise ValueError("unfrozen source")
    root = Path("/scratch/fb31/New_Campaign")
    logs = root / "logs" / a.run_id
    rows = units(a.kind)
    with (logs / "jobs.tsv").open(newline="") as f:
        jobs = list(csv.DictReader(f, delimiter="\t"))
    if len(jobs) != (1 if a.kind == "dev" else 4):
        raise ValueError("incomplete primary job record")
    for marker in sorted(logs.glob("retry_*.intent")):
        text = marker.read_text(encoding="utf-8")
        accepted = re.search(r"^job_id=(\d+)$", text, re.MULTILINE)
        if not accepted:
            raise ValueError("retry acceptance unresolved: " + str(marker))
        cmd = shlex.split(text.splitlines()[0])
        arg = next(x for x in cmd if x.startswith("--array="))
        expected = {int(x) for x in arg.split("=", 1)[1].split("%", 1)[0].split(",")}
        jobid = accepted[1]
        assert_absent(jobid)
        ac = subprocess.run(["sacct", "-n", "-P", "-j", jobid, "--format=JobID%40,State%30"], capture_output=True, text=True, check=True)
        select("JobID|State\n" + ac.stdout, jobid, expected)
    plans = []
    for job in jobs:
        cell = job["cell"]
        subset = rows if a.kind == "dev" else [r for r in rows if f"p{r[1]:04d}_{r[4]}" == cell]
        if len(subset) != (26 if a.kind == "dev" else 600):
            raise ValueError("wrong primary cell")
        assert_absent(job["job_id"])
        out = subprocess.run(["sacct", "-n", "-P", "-j", job["job_id"], "--format=JobID%40,State%30"],
                             text=True, capture_output=True, check=True).stdout
        states = select("JobID|State\n" + out, job["job_id"], {r[0] for r in subset})
        selected = []
        for unit in subset:
            index, p, _, _, scale, dataset, _ = unit
            if states[index] != "TIMEOUT":
                continue
            folder = root / "results" / a.run_id / f"p{p:04d}" / f"{dataset}_{scale}"
            state, _ = check_case(folder, a.run_id, dataset, scale, source)
            if state == "valid":
                verdict = subprocess.run(["Rscript", "--vanilla", str(runner / "validate.R")] +
                                          args_for(root / "results" / a.run_id,a.run_id,source,unit), capture_output=True)
                if verdict.returncode:
                    state = "invalid_rds"
            if state != "valid":
                selected.append((index, folder))
        print(cell, "states", {s: list(states.values()).count(s) for s in sorted(set(states.values()))},
              "timeouts_without_valid_result", len(selected))
        if selected:
            plans.append((job, selected))
    plans = [(job, selected) for job, selected in plans if not (logs / ("retry_" + job["cell"] + ".intent")).exists()]
    if not a.dry_run:
        plans = plans[:1]
    for job, selected in plans:
        cell = job["cell"]
        marker = logs / ("retry_" + cell + ".intent")
        if marker.exists():
            raise ValueError("retry already attempted for " + cell)
        cmd = retry_command(job, selected, a.kind, a.run_id, runner, source, logs, a.throttle)
        print(shlex.join(cmd))
        if a.dry_run:
            continue
        gate = subprocess.run(["bash", str(runner / "gate.sh"), str(runner), a.run_id],
                              text=True, capture_output=True, check=True)
        (logs / f"gate_retry_{cell}.txt").write_text(gate.stdout + gate.stderr, encoding="utf-8")
        snapshot = throttle_gate.check(min(26, a.throttle) if a.kind == "dev" else a.throttle)
        (logs / f"squeue_before_retry_{cell}.txt").write_text(snapshot, encoding="utf-8")
        claim(marker, cmd)
        archive = logs / "retry_originals" / cell
        archive.mkdir(parents=True, exist_ok=False)
        for index, folder in selected:
            if folder.exists():
                shutil.copytree(folder, archive / str(index))
        try:
            result = subprocess.run(cmd, text=True, capture_output=True, check=True)
        except subprocess.CalledProcessError as error:
            try:
                (logs / f"retry_{cell}.sbatch_error.txt").write_text(
                    f"client_status={error.returncode}\nstdout={error.stdout or ''}\nstderr={error.stderr or ''}\n", encoding="utf-8")
            except OSError:
                print("warning: could not record sbatch diagnostics; intent retained", file=sys.stderr)
            raise
        jobid = result.stdout.strip().split(";")[0]
        if not re.fullmatch(r"[0-9]+", jobid):
            raise ValueError("invalid retry job id")
        with marker.open("a") as f:
            f.write("job_id=" + jobid + "\n")
            f.flush()
            os.fsync(f.fileno())
        print("retry submitted", cell, jobid, "; rerun after terminal for any remaining cells")


if __name__ == "__main__":
    main()
