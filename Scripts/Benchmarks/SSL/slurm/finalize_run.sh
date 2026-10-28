#!/bin/bash
# Completion step of an A2 dev run (policy §8; master §IV.3.1): validate the outputs, score them,
# summarise the ladder diagnostics, save sacct, and write status, runtime and output checksums
# into manifest.json and a RUNS.md row (output folder). Scoring runs only if validation passed.
# Every stage's outcome is recorded; the script exits 1 if any stage failed or was skipped.
# Usage (NOTS login node, after the array has ended): bash slurm/finalize_run.sh <RUN_ID> <JOB>
set -uo pipefail
RUN_ID=$1; JOB=$2
B=/projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL
DEV=/projects/ml75/fb31/BVS/bench20261019/dev
C=$B/runs/$RUN_ID/code
module load GCC/14.3.0 >/dev/null 2>&1; module load R/4.5.2 >/dev/null 2>&1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p "$B/checks/$RUN_ID" "$B/scores/$RUN_ID"
Rscript "$C/check_dev.R" --code "$C" --results "$B/results/$RUN_ID" --manifest "$DEV/manifests/dev_inputs_manifest.csv" --out "$B/checks/$RUN_ID"
CHECK=$?
if [ "$CHECK" -eq 0 ]; then
  Rscript "$C/score_dev.R" --results "$B/results/$RUN_ID" --truth "$DEV/truth" --out "$B/scores/$RUN_ID" > "$B/scores/$RUN_ID/score_stdout.txt"
  SCORE=$?
else
  SCORE=skipped
fi
Rscript "$C/tests/summarise_dev_paths.R" --results "$B/results/$RUN_ID" --out "$B/checks/$RUN_ID/dev_path_summary.csv" > /dev/null
SUMMARY=$?
sacct -j "$JOB" --format=JobID,JobName,State,Elapsed,MaxRSS,NodeList,ExitCode -P > "$B/checks/$RUN_ID/sacct.txt"
SACCT=$?
python3 - "$B" "$RUN_ID" "$JOB" "$CHECK" "$SCORE" "$SUMMARY" "$SACCT" <<'PY'
import hashlib, json, os, sys, datetime
B, run_id, job, check, score, summary, sacct_rc = sys.argv[1:]
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
res = os.path.join(B, 'results', run_id)
outs = {os.path.relpath(os.path.join(r, f), res): sha(os.path.join(r, f)) for r, _, fs in os.walk(res) for f in sorted(fs)}
sacct = [l.split('|') for l in open(os.path.join(B, 'checks', run_id, 'sacct.txt')).read().split('\n')[1:] if l]
tasks = [x for x in sacct if x[1] != 'batch' and x[1] != 'extern' and '.' not in x[0]]
states = sorted(set(x[2] for x in tasks))
man_p = os.path.join(B, 'runs', run_id, 'manifest.json')
m = json.load(open(man_p))
m.update({"status": "completed" if states == ['COMPLETED'] else "states: " + ",".join(states),
          "completed_recorded_utc": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
          "task_elapsed": {x[0]: x[3] for x in tasks},
          "validation": "check_dev all pass" if check == '0' else "check_dev FAILED (exit %s)" % check,
          "stages": {"check_dev": check, "score_dev": score, "summarise_dev_paths": summary, "sacct": sacct_rc},
          "output_sha256": outs,
          "derived": {"check": os.path.join(B, 'checks', run_id), "scores": os.path.join(B, 'scores', run_id)}})
json.dump(m, open(man_p, 'w'), indent=2)
runs = os.path.join(B, 'RUNS.md')
if not os.path.exists(runs):
    open(runs, 'w').write("# RUNS (A2 SSL thread)\n\n| run id | piece | job | status | validation | outputs |\n|---|---|---|---|---|---|\n")
open(runs, 'a').write("| %s | %s | %s | %s | %s | %s (%d files) |\n" % (run_id, m["piece"], job, m["status"], m["validation"], res, len(outs)))
print(m["status"], m["validation"], len(outs), "output files", m["stages"])
ok = m["status"] == "completed" and all(v == '0' for v in m["stages"].values())
sys.exit(0 if ok else 1)
PY
