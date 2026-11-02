#!/usr/bin/env python3
"""Replace a copied resource config with the four measured pilot recommendations."""
import csv
import json
from pathlib import Path
import sys


def fill(rows):
    result = {}
    for r in rows:
        if r["p"] == "total_core_hours":
            continue
        p, scale = int(r["p"]), r["scale"]
        key = f"p{p:04d}_{scale}"
        if key in result or p not in (500, 1000) or scale not in ("c100", "c050"):
            raise ValueError("unexpected or duplicate cell " + key)
        minutes, memory = int(r["time_minutes"]), int(r["mem_gib"])
        if not (1 <= minutes <= 10080 and 1 <= memory <= 1024):
            raise ValueError("invalid resources")
        result[key] = {"minutes": minutes, "mem_gib": memory}
    if set(result) != {f"p{p:04d}_{s}" for p in (500, 1000) for s in ("c100", "c050")}:
        raise ValueError("four cells required")
    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: fill_resources.py sizing.tsv output.json")
    with open(sys.argv[1], newline="", encoding="utf-8") as f:
        result = fill(csv.DictReader(f, delimiter="\t"))
    path = Path(sys.argv[2])
    if path.exists():
        sys.exit("refusing to overwrite resource file")
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
