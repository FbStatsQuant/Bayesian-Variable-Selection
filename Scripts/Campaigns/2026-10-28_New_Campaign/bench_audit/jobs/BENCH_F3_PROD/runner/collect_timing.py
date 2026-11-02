#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from units import units


def main():
    p = argparse.ArgumentParser()
    p.add_argument("kind", choices=("dev", "prod"))
    p.add_argument("timing_dir", type=Path)
    a = p.parse_args()
    out = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    out.writerow(("index", "p", "scale", "wall_seconds", "max_rss_kib", "attempt"))
    for index, dim, _, _, scale, _, _ in units(a.kind):
        paths = [(attempt, a.timing_dir / f"{index}_attempt{attempt}.tsv") for attempt in (1, 2)]
        existing = [(attempt, path) for attempt, path in paths if path.is_file()]
        if not existing:
            raise ValueError(f"missing timing {index}")
        attempt, path = existing[-1]
        data = path.read_text().strip().splitlines()
        if len(data) != 1:
            raise ValueError(f"invalid timing file {path}")
        fields = data[0].split("\t")
        if len(fields) != 2 or float(fields[0]) <= 0 or int(fields[1]) <= 0:
            raise ValueError(f"invalid timing {path}")
        out.writerow((index, dim, scale, *fields, attempt))


if __name__ == "__main__":
    main()
