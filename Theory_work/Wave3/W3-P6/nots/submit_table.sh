#!/usr/bin/env bash
# W3-P6 (adapted from W2-SIM sim/submit_table.sh). Usage: submit_table.sh RUN_ID TASKS_TSV SCRIPTS_DIR PARTITION TIME MEM THROTTLE [extra sbatch args]
# Freezes tasks + scripts into runs/RUN_ID, writes manifest.json (code commit, sha256 of every frozen file), submits.
set -euo pipefail
RUN_ID=$1; TASKS=$(realpath "$2"); SCR=$(realpath "$3"); PART=$4; TIME=$5; MEM=$6; THR=$7; shift 7
[[ $PART == commons || $PART == scavenge ]] || { echo "partition must be commons or scavenge" >&2; exit 64; }
(( THR >= 1 && THR <= 150 )) || { echo "throttle 1..150" >&2; exit 64; }
BASE=/home/fb31/projects/BVS/theory_w3
RUN_DIR=$BASE/runs/$RUN_ID; OUT=/scratch/fb31/theory_w3/$RUN_ID
[[ ! -e $RUN_DIR && ! -e $OUT ]] || { echo "run exists" >&2; exit 66; }
mine=$(squeue -h -u fb31 -t RUNNING -o %j | grep -c "^w3p6_" || true)
echo "currently running w3p6 tasks: $mine"
mkdir -p "$RUN_DIR" "$OUT/slurm"
cp "$TASKS" "$RUN_DIR/tasks.tsv"; cp -a "$SCR" "$RUN_DIR/scripts"; cp "$BASE/sim/run_table.sh" "$BASE/sim/env_sim.sh" "$RUN_DIR/"
cat > "$RUN_DIR/config.env" <<CFG
RUN_ID=$RUN_ID
OUT=$OUT
CODE=$BASE/code/main_2252d57/repo
TICKETS=/nonexistent
CFG
chmod -R a-w "$RUN_DIR"
n=$(awk -F'\t' 'NF>=2' "$RUN_DIR/tasks.tsv" | wc -l)
args=(--parsable --job-name="w3p6_$RUN_ID" --account=commons --partition=$PART --qos=nots_$PART --nodes=1 --ntasks=1 --cpus-per-task=1
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
         code_commit=open("/home/fb31/projects/BVS/theory_w3/code/main_2252d57/COMMIT").read().strip(), config=cfg, files_sha256=files,
         modules="GCC/14.3.0 R/4.5.2 SciPy-bundle/2025.07")
os.chmod(rd, 0o755); json.dump(m, open(os.path.join(rd, "manifest.json"), "w"), indent=1); os.chmod(rd, 0o555)
print(json.dumps(dict(run_id=m["run_id"], job=job, tasks=sum(1 for _ in open(os.path.join(rd, "tasks.tsv"))))))
PY
