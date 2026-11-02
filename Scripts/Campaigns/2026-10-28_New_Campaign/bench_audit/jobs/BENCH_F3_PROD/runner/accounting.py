#!/usr/bin/env python3
"""Capture sacct for each recorded primary/retry job and sum per-cell elapsed core-hours."""
import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
import re
import shlex
import subprocess
import sys
sys.dont_write_bytecode = True
from units import units
from terminal import assert_absent


def main():
    p = argparse.ArgumentParser()
    p.add_argument("logroot", type=Path)
    a = p.parse_args()
    kind = "dev" if a.logroot.name.endswith("_bench_f3v2_dev") else "prod"
    mapping = {r[0]: f"p{r[1]:04d}_{r[4]}" for r in units(kind)}
    with (a.logroot / "jobs.tsv").open(newline="") as f:
        jobs = [(r["cell"], r["job_id"], {i for i, cell in mapping.items() if r["cell"] == "dev" or r["cell"] == cell})
                for r in csv.DictReader(f, delimiter="\t")]
    for marker in sorted(a.logroot.glob("retry_*.intent")):
        match = re.search(r"^job_id=(\d+)$", marker.read_text(), re.MULTILINE)
        if not match:
            raise ValueError(f"retry marker lacks accepted job id: {marker}")
        command = shlex.split(marker.read_text().splitlines()[0])
        array = next(x for x in command if x.startswith("--array="))
        selected = {int(x) for x in array.split("=", 1)[1].split("%", 1)[0].split(",")}
        jobs.append((marker.name[len("retry_"):-len(".intent")], match[1], selected))
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("cell", "job", "tasks", "states", "elapsed_core_hours", "allocated_cpu_hours"))
    total_elapsed = total_cpu = 0
    cells = defaultdict(lambda: [0, 0, 0, Counter()])
    for cell, job, expected in jobs:
        assert_absent(job)
        raw = subprocess.run(["sacct", "-n", "-P", "-j", job,
                              "--format=JobID%40,State%30,ElapsedRaw,AllocCPUS,CPUTimeRAW,ExitCode"],
                             text=True, capture_output=True, check=True).stdout
        (a.logroot / f"sacct_{job}.txt").write_text(raw, encoding="utf-8")
        records = []
        for row in csv.reader(raw.splitlines(), delimiter="|"):
            if row and re.fullmatch(re.escape(job) + r"_\d+", row[0]):
                if len(row) < 6 or not row[2].isdigit() or not row[4].isdigit():
                    raise ValueError("invalid accounting row")
                if row[1].split()[0].rstrip("+") not in {"COMPLETED","FAILED","TIMEOUT","OUT_OF_MEMORY","CANCELLED","NODE_FAIL","PREEMPTED","BOOT_FAIL","DEADLINE"}:
                    raise ValueError("accounting not terminal")
                records.append(row)
        observed = {int(r[0].split("_")[1]) for r in records}
        if not expected or observed != expected or len(observed) != len(records):
            raise ValueError(f"accounting incomplete or duplicate: {job} {len(records)}/{len(expected)}")
        elapsed = sum(int(r[2]) for r in records)
        cpu = sum(int(r[4]) for r in records)
        states = Counter(r[1] for r in records)
        writer.writerow((cell, job, len(records), ";".join(f"{k}={v}" for k, v in sorted(states.items())), elapsed/3600, cpu/3600))
        for r in records:
            group = mapping[int(r[0].split("_")[1])]
            cells[group][0] += 1; cells[group][1] += int(r[2]); cells[group][2] += int(r[4])
            cells[group][3].update([r[1]])
        total_elapsed += elapsed; total_cpu += cpu
    for cell, (count, elapsed, cpu, states) in sorted(cells.items()):
        writer.writerow((cell, "CELL_TOTAL", count, ";".join(f"{k}={v}" for k, v in sorted(states.items())), elapsed/3600, cpu/3600))
    writer.writerow(("TOTAL", "", "", "", total_elapsed/3600, total_cpu/3600))


if __name__ == "__main__":
    main()
