#!/usr/bin/env python3
"""Generate the deterministic production inventory.

Within each cell replicates ascend. Enum30 task = 4*(scenario-1)+block.
SMC cells are ordered p20, p30; scenario 1..6; c100, c050. The task
is 4*cell+block. For repeats it is 20*cell+4*(repeat-1)+block.
Blocks are zero-based and contain 25 consecutive replicates.
"""
import argparse
import csv
import io
from pathlib import Path

HEADER = ("piece", "task", "unit", "dataset", "scale", "repeat")
DEST = Path(__file__).resolve().parent.parent / "lists" / "units.tsv"


def rows():
    for p in (20, 30):
        for s in range(1, 7):
            for r in range(1, 101):
                dataset = f"p{p:04d}_S{s}_r{r:03d}"
                yield (f"enum{p}", 0 if p == 20 else 4 * (s - 1) + (r - 1) // 25, dataset, dataset, "-", 0)
    for pidx, p in enumerate ( (20, 30) ):
        for s in range(1, 7):
            for cidx, scale in enumerate(("c100", "c050")):
                cell = pidx * 12 + (s - 1) * 2 + cidx
                for r in range(1, 101):
                    dataset = f"p{p:04d}_S{s}_r{r:03d}"
                    unit = f"{dataset}_{scale}"
                    yield ("smc", 4 * cell + (r - 1) // 25, unit, dataset, scale, 0)
    for pidx, p in enumerate((20, 30)):
        for s in range(1, 7):
            for cidx, scale in enumerate(("c100", "c050")):
                cell = pidx * 12 + (s - 1) * 2 + cidx
                for repeat in range(1, 6):
                    for r in range(1, 101):
                        dataset = f"p{p:04d}_S{s}_r{r:03d}"
                        yield ("smcrep", 20 * cell + 4 * (repeat - 1) + (r - 1) // 25, f"{dataset}_{scale}_rep{repeat}", dataset, scale, repeat)


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
        for piece, count, tasks, size in (("enum20", 600, 1, 600), ("enum30", 600, 24, 25), ("smc", 2400, 96, 25), ("smcrep", 12000, 480, 25)):
            subset = [row for row in data if row[0] == piece]
            groups = {i: [] for i in range(tasks)}
            for row in subset:
                groups[row[1]].append(row[2])
            if len(subset) != count or len({x[2] for x in subset}) != count or any(len(v) != size for v in groups.values()):
                raise SystemExit(f"FAIL: {piece}")
            print(f"PASS {piece}: {count} unique units, {tasks} tasks of {size}")
    else:
        DEST.parent.mkdir(parents=True, exist_ok=True)
        DEST.write_bytes(expected)
        print(f"wrote {DEST} ({len(data)} units)")


if __name__ == "__main__":
    main()
