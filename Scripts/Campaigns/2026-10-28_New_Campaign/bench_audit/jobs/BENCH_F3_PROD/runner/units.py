#!/usr/bin/env python3
"""Deterministic F3 task mapping; indices are one-based and one task is one fit."""
import argparse
import csv
import sys


def units(kind):
    if kind not in ("dev", "prod"):
        raise ValueError(kind)
    rows = []
    for p in (500, 1000):
        for scenario in range(1, 7):
            for replicate in range(1, 2 if kind == "dev" else 101):
                for scale in ("c100", "c050"):
                    prefix = "dev_" if kind == "dev" else ""
                    dataset = f"{prefix}p{p:04d}_S{scenario}_r{replicate:03d}"
                    rows.append((len(rows) + 1, p, scenario, replicate, scale, dataset,
                                 "dev" if kind == "dev" else "prod"))
    if kind == "dev":
        for scenario in (4, 6):
            dataset = f"p1000_S{scenario}_r001"
            rows.append((len(rows) + 1, 1000, scenario, 1, "c050", dataset, "prod"))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("dev", "prod"))
    parser.add_argument("--index", type=int)
    args = parser.parse_args()
    rows = units(args.kind)
    if args.index is not None:
        if not 1 <= args.index <= len(rows):
            parser.error("index out of range")
        rows = [rows[args.index - 1]]
    out = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    out.writerow(("index", "p", "scenario", "replicate", "scale", "dataset_id", "input_kind"))
    out.writerows(rows)


if __name__ == "__main__":
    main()
