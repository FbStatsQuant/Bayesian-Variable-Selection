#!/usr/bin/env python3
"""Prepare paths/selector only, without numerical work or touching source artifacts."""
import argparse
import csv
import json
from pathlib import Path
from run_pipeline import TABLES, ROOT, OWNER
from verify_fixture import KEYS


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("out", "analysis-out", "runs-tsv", "scored-root", "canonical-root", "benchmark-scoring",
                 "inputs-manifest", "truth-manifest", "truth-dir",
                 "ops-outputs", "smc-c100", "smc-c050"):
        p.add_argument("--"+name, required=True)
    p.add_argument("--source-map", help="Optional JSON mapping of run_id to scored_dir; reproduction agent owns these paths")
    p.add_argument("--mapping-ruling", default=str(ROOT/"vendor"/"RULINGS_LEAD.md"))
    p.add_argument("--mapping-csv", help="Optional mock audit table; R-1 is the mapping authority")
    p.add_argument("--rscript", default="C:/Program Files/R/R-4.4.1/bin/Rscript.exe")
    p.add_argument("--design", choices=("full", "amendment1"), default="full",
                   help="full = Campaign 2 r1..100 (1,200 datasets / 2,400 cases); amendment1 = r1..10")
    a = vars(p.parse_args())
    absolute = lambda name: str(Path(a[name]).expanduser().resolve())
    destination = Path(absolute("out"))
    if destination.exists():
        raise ValueError("refuse to overwrite an existing config")
    source_map = json.loads(Path(a["source_map"]).read_text()) if a["source_map"] else {}
    with Path(a["runs_tsv"]).open(newline="", encoding="utf-8-sig") as f:
        runs = list(csv.DictReader(f, delimiter="\t"))
    if len(runs) != 18 or len({r["run_id"] for r in runs}) != 18 or {r["scale_key"] for r in runs} != {"c100", "c050"}:
        raise ValueError("expected explicit inventory of all 18 benchmark production runs")
    sources = [{"scored_dir": source_map.get(r["run_id"], str(Path(absolute("scored_root"))/
                 ("combined_v3_v7" if r["scale_key"]=="c100" else "combined_c050_v7")/"runs"/r["run_id"])),
                "version": "Phase1 unchanged-v7 raw rescoring; full benchmark design", "scale_key": r["scale_key"]}
               for r in runs]
    combined = {}
    for sk, version in (("c100", "combined_v3_v7"), ("c050", "combined_c050_v7")):
        tables = {}
        for tb in TABLES:
            path = Path(absolute("canonical_root"))/version/(tb+".csv")
            if path.is_file():
                tables[tb] = {"path": str(path), "keys": ["run_id"]+KEYS[tb]}
            else:
                tables[tb] = {"unavailable": "Original canonical v7 CSV not supplied; regenerated output cannot establish exact reproduction of an absent original."}
        combined[sk] = {"version": version, "tables": tables}
    cfg = {"mode": "assessment", "out": absolute("analysis_out"), "output_root": str(Path(absolute("analysis_out")).parent), "rscript": a["rscript"],
           "assessment_selector": {"p": [500,1000], "scenario": list(range(1,7)),
                                   "replicate": list(range(1, 101 if a["design"]=="full" else 11)), "scale_key": ["c100","c050"]},
           "benchmark_sources": sources, "combined_references": combined,
           "smc_sources": [{"scale_key": "c100", "results_dir": absolute("smc_c100")},
                           {"scale_key": "c050", "results_dir": absolute("smc_c050")}],
           "source_inventory": absolute("runs_tsv")}
    for name in ("benchmark_scoring", "inputs_manifest", "truth_manifest", "truth_dir", "mapping_ruling", "ops_outputs"):
        cfg[name] = absolute(name)
    if a["mapping_csv"]: cfg["mapping_csv"] = absolute("mapping_csv")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(cfg, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
