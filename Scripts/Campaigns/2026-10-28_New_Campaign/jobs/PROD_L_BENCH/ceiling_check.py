#!/usr/bin/env python3
"""Fail-closed Slurm potential-CPU admission check (Python 3.9)."""
import argparse
import csv
import math
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


def billed(n):
    if n <= 0:
        raise ValueError("CPU count must be positive")
    return 2 * math.ceil(n / 2)


def count_range(spec):
    total = 0
    seen = set()
    for part in spec.split(","):
        match = re.fullmatch(r"(\d+)(?:-(\d+)(?::(\d+))?)?", part)
        if not match:
            raise ValueError("unparsable array range: " + spec)
        lo = int(match.group(1))
        hi = int(match.group(2) or lo)
        stride = int(match.group(3) or 1)
        if hi < lo or stride < 1 or hi - lo > 1000000:
            raise ValueError("invalid array range: " + spec)
        for index in range(lo, hi + 1, stride):
            if index in seen:
                raise ValueError("overlapping array range: " + spec)
            seen.add(index)
            total += 1
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, choices=("alone", "withH"))
    parser.add_argument("--plan", required=True)
    parser.add_argument("--squeue", required=True)
    parser.add_argument("--own-ids", default="")
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = []
    try:
        phases = defaultdict(list)
        with open(args.plan, newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream, delimiter="\t")
            if reader.fieldnames != ["step", "cpus", "max_concurrent_tasks", "phase"]:
                raise ValueError("invalid plan header")
            for row in reader:
                cpus, concurrency = int(row["cpus"]), int(row["max_concurrent_tasks"])
                if None in row or concurrency < 0 or not row["step"] or not row["phase"]:
                    raise ValueError("invalid plan row")
                value = billed(cpus) * concurrency
                phases[row["phase"]].append((row["step"], value))
                receipt.append(f"plan {row['phase']} {row['step']} cpus={cpus} billed={billed(cpus)} tasks={concurrency} peak={value}")
        if not phases:
            raise ValueError("empty plan")
        peaks = []
        for phase, steps in phases.items():
            # These two lanes are explicitly serialized by the driver.
            serial = [value for name, value in steps if phase == "fit" and name in ("s2_smc", "s3_smcrep")]
            peak = sum(value for name, value in steps if not (phase == "fit" and name in ("s2_smc", "s3_smcrep"))) + max(serial, default=0)
            peaks.append(peak)
            receipt.append(f"phase {phase} peak={peak}")
        own = set(args.own_ids.split(",")) if args.own_ids else set()
        if any(not x.isdigit() for x in own):
            raise ValueError("invalid own job id")
        raw = sys.stdin.read() if args.squeue == "-" else Path(args.squeue).read_text(encoding="utf-8")
        rows = []
        for line in raw.splitlines():
            if not line.strip():
                continue
            parts = line.split("|")
            if len(parts) != 4 or not all(parts):
                raise ValueError("unparsable squeue row: " + line)
            jid, name, state, cpus = parts
            match = re.fullmatch(r"(\d+)(?:_(\d+|\[([^\]]+)\]))?", jid)
            if not match or not cpus.isdigit() or state not in ("RUNNING", "PENDING", "CONFIGURING", "COMPLETING", "SUSPENDED"):
                raise ValueError("unparsable squeue row: " + line)
            if match.group(1) not in own:
                rows.append((jid, match.group(1), match.group(3), name, state, int(cpus)))
        running = defaultdict(int)
        for jid, root, array, name, state, cpus in rows:
            if state != "PENDING" and "_" in jid and array is None:
                running[root] += 1
        other = 0
        prod_h = False
        for jid, root, array, name, state, cpus in rows:
            prod_h |= "_prodH" in name
            count = 1
            if state == "PENDING" and array is not None:
                pieces = array.split("%")
                if len(pieces) > 2 or (len(pieces) == 2 and (not pieces[1].isdigit() or int(pieces[1]) < 1)):
                    raise ValueError("invalid array throttle: " + jid)
                pending = count_range(pieces[0])
                count = pending if len(pieces) == 1 else max(0, min(pending, int(pieces[1]) - running[root]))
                receipt.append(f"array {jid} pending={pending} throttle={pieces[1] if len(pieces) == 2 else 'none'} running={running[root]} admitted_tasks={count}")
            contribution = billed(cpus) * count
            other += contribution
            receipt.append(f"other {jid} state={state} cpus={cpus} billed={billed(cpus)} tasks={count} peak={contribution}")
        peak = max(peaks)
        limit = int(os.environ.get("CEIL_ALONE" if args.profile == "alone" else "CEIL_WITHH", "132" if args.profile == "alone" else "68"))
        global_limit = int(os.environ.get("CEIL_COMBINED", "192"))
        if limit <= 0 or global_limit <= 0:
            raise ValueError("invalid CPU ceiling")
        receipt.append(f"profile={args.profile} prod_h_present={prod_h} prod_l_peak={peak} profile_limit={limit} others_peak={other} combined={other + peak} global_limit={global_limit}")
        reasons = []
        if args.profile == "alone" and prod_h:
            reasons.append("PROD-H present with alone profile")
        if peak > limit:
            reasons.append("PROD-L profile ceiling exceeded")
        if other + peak > global_limit:
            reasons.append("global ceiling exceeded")
        if reasons:
            raise ValueError("; ".join(reasons))
        receipt.append("ADMITTED")
        rc = 0
    except (OSError, ValueError, TypeError, KeyError, csv.Error, UnicodeError) as exc:
        receipt.append("REFUSED: " + str(exc))
        rc = 2
    result = "\n".join(receipt) + "\n"
    try:
        Path(args.receipt).write_text(result, encoding="utf-8")
    except OSError as exc:
        print("REFUSED: cannot write receipt: " + str(exc), file=sys.stderr)
        return 2
    print(result, end="")
    return rc


if __name__ == "__main__":
    sys.exit(main())

