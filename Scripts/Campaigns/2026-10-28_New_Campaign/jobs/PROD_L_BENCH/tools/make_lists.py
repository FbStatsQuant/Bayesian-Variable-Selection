#!/usr/bin/env python3
"""Generate the benchmark inventory; cell order and blocks match PROD-L SMC."""
import argparse
import csv
import io
from pathlib import Path

HEADER = ("piece", "task", "unit", "dataset", "scale", "repeat")
DEST = Path(__file__).resolve().parent.parent / "lists" / "units.tsv"


def rows():
    for pidx, p in enumerate((20, 30)):
        for s in range(1, 7):
            for cidx, scale in enumerate(("c100", "c050")):
                cell = pidx * 12 + (s - 1) * 2 + cidx
                for r in range(1, 101):
                    dataset = f"p{p:04d}_S{s}_r{r:03d}"
                    yield ("bench", 4 * cell + (r - 1) // 25,
                           f"{dataset}_{scale}", dataset, scale, 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = list(rows())
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, delimiter="\t", lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(data)
    expected = buf.getvalue().encode()
    if args.check:
        if not DEST.is_file() or DEST.read_bytes() != expected:
            raise SystemExit("FAIL: units.tsv differs from deterministic output")
        groups = {i: [] for i in range(96)}
        for row in data:
            groups[row[1]].append(row[2])
        if len(data) != 2400 or len({x[2] for x in data}) != 2400 or any(len(v) != 25 for v in groups.values()):
            raise SystemExit("FAIL: benchmark coverage")
        print("PASS bench: 2400 unique units, 96 tasks of 25")
    else:
        DEST.parent.mkdir(parents=True, exist_ok=True)
        DEST.write_bytes(expected)
        print(f"wrote {DEST} ({len(data)} units)")


if __name__ == "__main__":
    main()
