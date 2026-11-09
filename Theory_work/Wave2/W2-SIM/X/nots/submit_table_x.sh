#!/usr/bin/env bash
# W2-SIM family X copy of sim/submit_table.sh: identical except RUN_DIR lives under /scratch/fb31/theory_w2/fam_X/runs (home quota full 2026-11-09 10:13).
# Usage: submit_table.sh RUN_ID TASKS_TSV SCRIPTS_DIR PARTITION TIME MEM THROTTLE [extra sbatch args]
# Freezes tasks + scripts into runs/RUN_ID, writes manifest.json (code commit, sha256 of every frozen file), submits.
set -euo pipefail
RUN_ID=$1; TASKS=$(realpath "$2"); SCR=$(realpath "$3"); PART=$4; TIME=$5; MEM=$6; THR=$7; shift 7
[[ $PART == commons || $PART == scavenge ]] || { echo "partition must be commons or scavenge" >&2; exit 64; }
(( THR >= 1 && THR <= 60 )) || { echo "throttle 1..60" >&2; exit 64; }
BASE=/home/fb31/projects/BVS/theory_w2
RUN_DIR=/scratch/fb31/theory_w2/fam_X/runs/$RUN_ID; OUT=/scratch/fb31/theory_w2/$RUN_ID
[[ ! -e $RUN_DIR && ! -e $OUT ]] || { echo "run exists" >&2; exit 66; }
# global concurrency guard: sum of throttles of my queued arrays + THR <= 150
active=$(squeue -h -u fb31 -t RUNNING -o "%i" | wc -l); pending_arrays=$(squeue -h -u fb31 -o "%i" | sed 's/_.*//' | sort -u | wc -l)
echo "currently running tasks: $active ; queued array jobs: $pending_arrays"
mkdir -p "$RUN_DIR" "$OUT/slurm"
cp "$TASKS" "$RUN_DIR/tasks.tsv"; cp -a "$SCR" "$RUN_DIR/scripts"; cp "$BASE/sim/run_table.sh" "$BASE/sim/env_sim.sh" "$RUN_DIR/"
cat > "$RUN_DIR/config.env" <<CFG
RUN_ID=$RUN_ID
OUT=$OUT
CODE=$BASE/code/main_11dc9b7/repo
TICKETS=$BASE/code/$(cat $BASE/code/TICKETS_CURRENT)
CFG
chmod -R a-w "$RUN_DIR"
n=$(awk -F'\t' 'NF>=2' "$RUN_DIR/tasks.tsv" | wc -l)
args=(--parsable --job-name="w2sim_$RUN_ID" --account=commons --partition=$PART --qos=nots_$PART --nodes=1 --ntasks=1 --cpus-per-task=1
      --mem=$MEM --time=$TIME --export=NONE --no-requeue --array="1-$n%$THR" --output="$OUT/slurm/%A_%a.out" --error="$OUT/slurm/%A_%a.err" "$@")
job=$(sbatch "${args[@]}" "$RUN_DIR/run_table.sh" "$RUN_DIR")
python3 - "$RUN_DIR" "$job" "${args[*]}" <<'PY'
import hashlib, json, os, sys
from datetime import datetime, timezone
rd, job, args = sys.argv[1:4]
cfg = dict(l.strip().split("=", 1) for l in open(os.path.join(rd, "config.env")) if "=" in l)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
files = {}
for root, _, fs in os.walk(rd):
    for f in fs:
        p = os.path.join(root, f)
        if not p.endswith("manifest.json"): files[os.path.relpath(p, rd)] = sha(p)
m = dict(run_id=cfg["RUN_ID"], slurm_job_id=job, submitted_utc=datetime.now(timezone.utc).isoformat(), sbatch_args=args,
         code_commit=open("/home/fb31/projects/BVS/theory_w2/code/main_11dc9b7/COMMIT").read().strip(), config=cfg, files_sha256=files,
         modules="GCC/14.3.0 R/4.5.2 SciPy-bundle/2025.07 (Python 3.13.5, numpy 2.3.2, scipy 1.16.1)")
os.chmod(rd, 0o755); json.dump(m, open(os.path.join(rd, "manifest.json"), "w"), indent=1); os.chmod(rd, 0o555)
print(json.dumps(dict(run_id=m["run_id"], job=job, tasks=sum(1 for _ in open(os.path.join(rd, "tasks.tsv"))))))
PY
