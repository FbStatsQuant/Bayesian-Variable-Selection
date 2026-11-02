#!/usr/bin/env python3
"""Pilot sizing from validated per-fit measurements, one TSV row per task."""
import argparse
import csv
import math
from collections import defaultdict


def sizing(rows):
    cells = defaultdict(list)
    ids = set()
    for row in rows:
        index = int(row["index"])
        if index in ids:
            raise ValueError(f"duplicate task index {index}")
        ids.add(index)
        p, scale = int(row["p"]), row["scale"]
        expected = ((500 if index <= 12 else 1000), ("c100" if index % 2 else "c050")) if 1 <= index <= 24 else (1000, "c050")
        if (p, scale) != expected:
            raise ValueError(f"task {index} does not match its p/scale mapping")
        seconds, rss = float(row["wall_seconds"]), int(row["max_rss_kib"])
        if p not in (500, 1000) or scale not in ("c100", "c050") or not math.isfinite(seconds) or seconds <= 0 or rss <= 0:
            raise ValueError(f"invalid measurement for {index}")
        cells[(p, scale)].append((seconds, rss))
    if ids != set(range(1, 27)):
        raise ValueError("need exactly pilot task indices 1..26")
    result = []
    for p in (500, 1000):
        for scale in ("c100", "c050"):
            cell = cells[(p, scale)]
            expected_n = 8 if (p, scale) == (1000, "c050") else 6
            if len(cell) != expected_n:
                raise ValueError(f"wrong cell size for {(p, scale)}")
            seconds = sorted(x[0] for x in cell)
            p95 = seconds[math.ceil(0.95 * len(seconds)) - 1]
            memory_gib = max(2, math.ceil(1.5 * max(x[1] for x in cell) / (1024 * 1024)))
            wall_minutes = max(10, math.ceil(3 * p95 / 60))
            mean = sum(seconds) / len(seconds)
            result.append((p, scale, len(cell), mean, p95, max(x[1] for x in cell), wall_minutes, memory_gib, mean * 600 / 3600))
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("measurements", help="TSV: index,p,scale,wall_seconds,max_rss_kib")
    a = p.parse_args()
    with open(a.measurements, encoding="utf-8", newline="") as f:
        result = sizing(csv.DictReader(f, delimiter="\t"))
    w = csv.writer(__import__("sys").stdout, delimiter="\t", lineterminator="\n")
    w.writerow(("p", "scale", "n", "mean_s", "p95_nearest_rank_s", "max_rss_kib", "time_minutes", "mem_gib", "estimated_core_hours"))
    w.writerows(result)
    w.writerow(("total_core_hours", "", "", "", "", "", "", "", sum(r[-1] for r in result)))


if __name__ == "__main__":
    main()
