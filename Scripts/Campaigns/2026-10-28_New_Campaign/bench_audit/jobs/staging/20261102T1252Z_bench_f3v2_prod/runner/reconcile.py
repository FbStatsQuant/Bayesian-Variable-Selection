#!/usr/bin/env python3
"""Reconcile expected F3 cases against files and CSV provenance; never repair results."""
import argparse
from collections import Counter
import csv
import hashlib
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
from units import units
from validate_args import args_for


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_case(folder, run_id, dataset, scale, source):
    required = [folder / ("F3." + x) for x in ("done", "sha256", "rds", "csv")]
    if not all(p.is_file() for p in required):
        return "missing", []
    try:
        lines = (folder / "F3.sha256").read_text(encoding="utf-8").splitlines()
        entries = [re.fullmatch(r"([0-9a-f]{64})  (F3\.(?:rds|csv))", line) for line in lines]
        if len(entries) != 2 or any(x is None for x in entries):
            return "corrupt", []
        hashes = {x.group(2): x.group(1) for x in entries}
        if len(hashes) != 2 or any(digest(folder / k) != v for k, v in hashes.items()):
            return "corrupt", []
        with (folder / "F3.csv").open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        expect = {"run_id": run_id, "dataset_id": dataset, "case_id": dataset + "_" + scale,
                  "scale_key": scale, "method_id": "F3", "source_sha256": source}
        if not rows or any(any(row.get(k) != v for k, v in expect.items()) for row in rows):
            return "provenance_error", []
        rules = [r.get("rule_id", "") for r in rows]
        if any(not r for r in rules) or len(rules) != len(set(rules)):
            return "duplicate_rule", []
        statuses = [row.get("status", "") for row in rows]
        if any(not s for s in statuses):
            return "invalid_status", []
        return "valid", statuses
    except (OSError, UnicodeError, csv.Error, ValueError):
        return "corrupt", []


def reconcile(root, kind, run_id, source):
    expected = units(kind)
    cases = {f"p{p:04d}/{dataset}_{scale}": (index, dataset, scale)
             for index, p, _, _, scale, dataset, _ in expected}
    if len(cases) != len(expected):
        raise ValueError("duplicate expected case")
    found = {str(p.parent.relative_to(root)).replace("\\", "/")
             for p in root.rglob("F3.*") if p.is_file()} if root.exists() else set()
    extras = sorted(found - set(cases))
    output = []
    tally = Counter()
    for rel, (index, dataset, scale) in cases.items():
        state, statuses = check_case(root / rel, run_id, dataset, scale, source)
        tally.update(statuses)
        output.append((index, rel, state, ",".join(statuses)))
    return output, extras, tally


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True, help="results/<run_id>")
    ap.add_argument("--kind", choices=("dev", "prod"), required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--source-sha256", required=True)
    a = ap.parse_args()
    if not re.fullmatch(r"[0-9a-f]{64}", a.source_sha256):
        ap.error("source hash must be 64 lowercase hexadecimal characters")
    result, extras, statuses = reconcile(a.root, a.kind, a.run_id, a.source_sha256)
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("index", "case", "integrity", "rule_statuses"))
    writer.writerows(result)
    for extra in extras:
        writer.writerow(("", extra, "unexpected", ""))
    print("integrity_counts=" + str(dict(Counter(r[2] for r in result))) +
          " rule_status_counts=" + str(dict(statuses)) + f" unexpected={len(extras)}", file=sys.stderr)
    mapping = {r[0]: r for r in units(a.kind)}
    requests = [args_for(a.root,a.run_id,a.source_sha256,mapping[r[0]]) for r in result if r[2] == "valid"]
    proc = subprocess.run(["Rscript", "--vanilla", str(Path(__file__).with_name("validate.R")),
                           "--stdin"], input="".join("\t".join(r)+"\n" for r in requests),
                          text=True, capture_output=True)
    print(proc.stdout, file=sys.stderr, end="")
    print(proc.stderr, file=sys.stderr, end="")
    return int(bool(extras) or any(r[2] != "valid" for r in result) or proc.returncode != 0)


if __name__ == "__main__":
    sys.exit(main())
