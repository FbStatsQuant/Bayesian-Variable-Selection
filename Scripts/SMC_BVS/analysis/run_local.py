"""One-command local mock suite, with immutable execution evidence. Relocatable: every path is an argument.

F_analysis_claude copy of D's run_local.py. Changes: --evidence-root and --reproduction-root are explicit
(audit D-F3); the D-era freeze step (which rewrote D's HANDOFF/STATUS/ledger files) runs only with --freeze.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

from run_pipeline import ROOT, sha, utc
from execution_environment import memory_limits

DEPLOY = ROOT.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rscript", default="C:/Program Files/R/R-4.4.1/bin/Rscript.exe")
    parser.add_argument("--benchmark-scoring", type=Path, default=DEPLOY.parent/"F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/scoring")
    parser.add_argument("--reproduction-root", type=Path, default=DEPLOY/"D_analysis"/"reproduction",
                        help="read-only D reproduction folder holding runs.tsv and local_outputs/")
    parser.add_argument("--evidence-root", type=Path, default=ROOT/"validation",
                        help="where the new local_<stamp>/ evidence directory is created")
    parser.add_argument("--freeze", action="store_true", help="also run the D-era freeze_evidence.py (rewrites pipeline docs)")
    a = parser.parse_args()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    launch = a.evidence_root.resolve()/("local_"+stamp)
    launch.mkdir(parents=True)
    argv = [sys.executable, str(ROOT/"verify_fixture.py"), "--local-mock", "--work", str(launch/"suite"),
            "--benchmark-scoring", str(a.benchmark_scoring.resolve()), "--rscript", a.rscript,
            "--reproduction-root", str(a.reproduction_root.resolve())]
    env = dict(os.environ, LC_ALL="C", LANG="C")
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[key] = "1"
    record = dict(argv=argv, launcher_argv=sys.argv, started_utc=utc(), pid=os.getpid(),
                  host=platform.node(), platform=platform.platform(), python=sys.version,
                  cwd=str(Path.cwd()), rscript_sha256=sha(a.rscript),
                  memory_and_job_at_start=memory_limits(),
                  thread_environment={k:v for k,v in env.items() if k.endswith("NUM_THREADS") or k in {"LANG", "LC_ALL"}})
    with (launch/"launcher.log").open("w", encoding="utf-8") as log:
        proc = subprocess.Popen(argv, stdout=log, stderr=subprocess.STDOUT, env=env)
        record["child_pid"] = proc.pid
        (launch/"launch.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        rc = proc.wait()
    record.update(exit_status=rc, finished_utc=utc(), log_sha256=sha(launch/"launcher.log"),memory_and_job_at_end=memory_limits())
    (launch/"launch.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    if rc==0 and a.freeze:
        freeze_record=dict(argv=[sys.executable,str(ROOT/"freeze_evidence.py"),"--evidence",str(launch)],started_utc=utc())
        with (launch/"freeze.log").open("w",encoding="utf-8") as f:
            proc=subprocess.Popen(freeze_record["argv"],stdout=f,stderr=subprocess.STDOUT)
            freeze_record["pid"]=proc.pid
            rc=proc.wait()
        freeze_record.update(exit_status=rc,finished_utc=utc(),log_sha256=sha(launch/"freeze.log"))
        (launch/"freeze.command.json").write_text(json.dumps(freeze_record,indent=2),encoding="utf-8")
    print(json.dumps(dict(evidence=str(launch), exit_status=rc)), flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
