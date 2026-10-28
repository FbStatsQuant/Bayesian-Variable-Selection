#!/usr/bin/env python3
"""ONE command for Campaign 2 scoring: config -> run_pipeline.py (unchanged benchmark scoring) -> make_results.py.

    python score_campaign2.py --smc-results <.../results/<run_id>> --ops-outputs <E_ops_claude/OUTPUTS.md> \
        --work <new output dir> [--smc-results-c050 <dir>] [--design full|amendment1] [benchmark path overrides]

--smc-results is the A-runner results root whose basename is the run_id (layout <run_id>/pXXXX/<case_id>/SMCBVS.*).
Both scales are read from it unless --smc-results-c050 is given. Every path is an argument; defaults point
at the laptop copies of the benchmark study and D's read-only reproduction outputs.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
EXP = HERE.parents[2]
BENCH = EXP/"F_2026-10-19_benchmark_study_n200"/"Benchmark_Study_20261019"
REPRO = HERE.parents[1]/"D_analysis"/"reproduction"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--smc-results", type=Path, required=True)
    ap.add_argument("--smc-results-c050", type=Path)
    ap.add_argument("--ops-outputs", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True, help="new directory; receives config.json, analysis/, results/")
    ap.add_argument("--design", choices=("full", "amendment1"), default="full")
    ap.add_argument("--benchmark-scoring", type=Path, default=BENCH/"scoring")
    ap.add_argument("--inputs-manifest", type=Path, default=BENCH/"verify/recount/c050/inputs/manifests/inputs_manifest.csv")
    ap.add_argument("--truth-dir", type=Path, default=BENCH/"verify/recount/c050/inputs/truth_scoring")
    ap.add_argument("--truth-manifest", type=Path)
    ap.add_argument("--runs-tsv", type=Path, default=REPRO/"runs.tsv")
    ap.add_argument("--scored-root", type=Path, default=REPRO/"executions/20261022T193656366878Z/local_outputs")
    ap.add_argument("--rscript", default="C:/Program Files/R/R-4.4.1/bin/Rscript.exe")
    a = ap.parse_args()
    work = a.work.resolve(); work.mkdir(parents=True, exist_ok=False)
    truth_manifest = a.truth_manifest or a.truth_dir/"truth_manifest.csv"
    cfg = work/"config.json"
    steps = [
        [sys.executable, HERE/"prepare_assessment_config.py", "--design", a.design, "--out", cfg, "--analysis-out", work/"analysis",
         "--runs-tsv", a.runs_tsv, "--scored-root", a.scored_root, "--canonical-root", a.benchmark_scoring/"out",
         "--benchmark-scoring", a.benchmark_scoring, "--inputs-manifest", a.inputs_manifest, "--truth-manifest", truth_manifest,
         "--truth-dir", a.truth_dir, "--ops-outputs", a.ops_outputs, "--smc-c100", a.smc_results,
         "--smc-c050", a.smc_results_c050 or a.smc_results, "--rscript", a.rscript],
        [sys.executable, HERE/"run_pipeline.py", "--config", cfg],
        [sys.executable, HERE/"make_results.py", "--analysis", work/"analysis", "--out", work/"results"],
    ]
    for i, argv in enumerate(steps):
        argv = list(map(str, argv))
        with (work/f"step{i}.log").open("w", encoding="utf-8") as log:
            rc = subprocess.call(argv, stdout=log, stderr=subprocess.STDOUT)
        (work/f"step{i}.json").write_text(json.dumps(dict(argv=argv, exit_status=rc), indent=2), encoding="utf-8")
        if rc:
            print(f"step {i} failed (exit {rc}); see {work/f'step{i}.log'}"); return rc
    print(json.dumps(dict(work=str(work), exit_status=0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
