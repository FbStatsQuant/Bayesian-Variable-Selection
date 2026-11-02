#!/usr/bin/env python3
"""Slurm arrays: one task per global mapping index; no submission from dry-run."""
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
sys.dont_write_bytecode = True
import throttle as throttle_gate
from units import units
from retry import select
from terminal import assert_absent

CELLS = [("p0500_c100", "1-1199:2"), ("p0500_c050", "2-1200:2"),
         ("p1000_c100", "1201-2399:2"), ("p1000_c050", "1202-2400:2")]


def commands(kind, run, runner, source, resources, limit=None):
    limit = (13 if kind == "dev" else 30) if limit is None else limit
    cells = [("dev", "1-26")] if kind == "dev" else CELLS
    result = []
    for cell, indices in cells:
        resource = {"minutes": 75, "mem_gib": 4} if kind == "dev" else resources[cell]
        mins, mem = int(resource["minutes"]), int(resource["mem_gib"])
        if not (1 <= mins <= 10080 and 1 <= mem <= 1024):
            raise ValueError("bad resources")
        log = f"/scratch/fb31/New_Campaign/logs/{run}/slurm/%A_%a.out"
        result.append(["sbatch", "--parsable", "--account=commons", "--partition=commons",
                       "--qos=nots_commons", "--constraint=sapphirerapids", "--ntasks=1",
                       "--cpus-per-task=1", "--export=NONE", "--no-requeue",
                       f"--array={indices}%{min(26, limit) if kind == 'dev' else limit}",
                       f"--time={mins}", f"--mem={mem}G", f"--output={log}",
                       "--chdir=/scratch/fb31/New_Campaign", f"--comment={run}", f"--job-name=f3v2_{run}_{cell}",
                       f"{runner}/task.sh", str(runner), kind, run, source, "1"])
    return result


def main():
    a = argparse.ArgumentParser()
    a.add_argument("kind", choices=("dev", "prod"))
    a.add_argument("run_id")
    a.add_argument("--resources", type=Path, required=True)
    a.add_argument("--dry-run", action="store_true")
    a.add_argument("--throttle", type=int)
    opt = a.parse_args()
    if not re.fullmatch(r"[0-9]{8}T[0-9]{4,6}Z_bench_f3v2_" + opt.kind, opt.run_id):
        a.error("invalid run id")
    opt.throttle = opt.throttle if opt.throttle is not None else (13 if opt.kind == "dev" else 30)
    if not 1 <= opt.throttle <= 96:
        a.error("throttle must be 1..96")
    runner = Path(__file__).resolve().parent
    freeze = json.loads((runner / "freeze.json").read_text())
    source = freeze["source_sha256"]
    resources = json.loads(opt.resources.read_text())
    cmds = commands(opt.kind, opt.run_id, runner, source, resources, opt.throttle)
    if opt.dry_run:
        for command in cmds:
            print(shlex.join(command), "[submit only after preceding cell terminal]" if opt.kind == "prod" else "")
        return
    if not re.fullmatch("[0-9a-f]{64}", source):
        raise ValueError("source hash placeholder not filled")
    logroot = Path("/scratch/fb31/New_Campaign/logs") / opt.run_id
    first = subprocess.run(["bash", str(runner / "gate.sh"), str(runner), opt.run_id],
                           text=True, capture_output=True, check=True)
    record = logroot / "jobs.tsv"
    resource_file = logroot / "resources_used.json"
    if not record.exists():
        with record.open("x", encoding="utf-8") as out:
            out.write("cell\tjob_id\tminutes\tmem_gib\tcommand\n")
        with resource_file.open("x", encoding="utf-8") as out:
            json.dump(resources, out, sort_keys=True)
    elif not resource_file.exists() or json.loads(resource_file.read_text()) != resources:
        raise ValueError("resource snapshot missing or changed")
    import csv
    with record.open(newline="") as f:
        prior = list(csv.DictReader(f, delimiter="\t"))
    names = ["dev"] if opt.kind == "dev" else [x[0] for x in CELLS]
    if [r["cell"] for r in prior] != names[:len(prior)]:
        raise ValueError("invalid job journal")
    if len(prior) == len(names):
        print("all cells submitted; inspect scheduler and reconcile")
        return
    i = len(prior)
    if prior:
        prev = prior[-1]
        expected = {r[0] for r in units(opt.kind) if prev["cell"] == "dev" or f"p{r[1]:04d}_{r[4]}" == prev["cell"]}
        assert_absent(prev["job_id"])
        ac = subprocess.run(["sacct", "-n", "-P", "-j", prev["job_id"], "--format=JobID%40,State%30"], capture_output=True, text=True, check=True)
        select("JobID|State\n" + ac.stdout, prev["job_id"], expected)
    cell = names[i]; cmd = cmds[i]
    marker = logroot / f"primary_{cell}.intent"
    if marker.exists():
        raise ValueError("submission acceptance unresolved; inspect intent and scheduler")
    snapshot = throttle_gate.check(min(26, opt.throttle) if opt.kind == "dev" else opt.throttle)
    (logroot / f"squeue_before_cell_{i+1}.txt").write_text(snapshot, encoding="utf-8")
    (logroot / f"gate_cell_{i+1}.txt").write_text(first.stdout + first.stderr, encoding="utf-8")
    with marker.open("x", encoding="utf-8") as f:
        f.write(shlex.join(cmd) + "\n")
        f.flush(); os.fsync(f.fileno())
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as error:
        try:
            (logroot / f"primary_{cell}.sbatch_error.txt").write_text(
                f"client_status={error.returncode}\nstdout={error.stdout or ''}\nstderr={error.stderr or ''}\n", encoding="utf-8")
        except OSError:
            print("warning: could not record sbatch diagnostics; intent retained", file=sys.stderr)
        raise
    job = result.stdout.strip().split(";")[0]
    if not re.fullmatch(r"[0-9]+", job):
        raise ValueError("unparseable sbatch job id; acceptance unknown")
    resource = {"minutes": 75, "mem_gib": 4} if opt.kind == "dev" else resources[cell]
    with record.open("a", encoding="utf-8") as out:
        out.write(f"{cell}\t{job}\t{resource['minutes']}\t{resource['mem_gib']}\t{shlex.join(cmd)}\n")
        out.flush(); os.fsync(out.fileno())
    print(cell, job, "submitted; repeat launch only when this cell is terminal", flush=True)


if __name__ == "__main__":
    main()
