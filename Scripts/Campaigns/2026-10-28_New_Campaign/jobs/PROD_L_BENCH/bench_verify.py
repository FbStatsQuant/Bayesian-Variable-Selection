#!/usr/bin/env python3
"""Strict, dependency-free verification of a benchmark case's method units."""
import csv
import hashlib
import re
from pathlib import Path

METHODS = ("F1", "F2", "F3", "F4", "F5", "A1", "A2", "A3")
STATUSES = frozenset(("ok", "warning", "failed"))


def verify_method(directory, method, case):
    """Return (valid, detail, rows); malformed or incomplete units are invalid."""
    directory = Path(directory)
    paths = {ext: directory / (method + "." + ext) for ext in ("rds", "csv", "sha256", "done")}
    try:
        if any(not p.is_file() or p.stat().st_size == 0 for p in paths.values()):
            return False, "missing or empty file", []
        lines = paths["sha256"].read_text(encoding="utf-8").splitlines()
        if len(lines) != 2:
            return False, "invalid checksum line count", []
        for line, ext in zip(lines, ("rds", "csv")):
            match = re.fullmatch(r"([0-9a-fA-F]{64})  (.+)", line)
            if not match or match.group(2) != method + "." + ext:
                return False, "invalid checksum entry", []
            digest = hashlib.sha256(paths[ext].read_bytes()).hexdigest()
            if digest != match.group(1).lower():
                return False, "checksum mismatch", []
        marker = paths["done"].read_text(encoding="utf-8").splitlines()
        if not marker or not marker[0].startswith("status "):
            return False, "invalid done marker", []
        with paths["csv"].open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            required = {"rule_id", "role", "status", "method_id", "case_id"}
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                return False, "missing CSV columns", []
            rows = list(reader)
        if not rows or any(row.get("status") not in STATUSES or row.get("method_id") != method or row.get("case_id") != case for row in rows):
            return False, "invalid CSV rows", []
        return True, "ok", rows
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        return False, str(exc), []


def verify_case(directory, case):
    results = {method: verify_method(directory, method, case) for method in METHODS}
    return all(result[0] for result in results.values()), results
