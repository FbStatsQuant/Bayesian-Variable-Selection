#!/usr/bin/env bash
# W3-SCALE submit. Usage: submit.sh RUN_ID TASKS_TSV SCRIPTS_DIR CODE_DIR PARTITION TIME MEM THROTTLE [extra sbatch args]
# Freezes tasks + scripts into runs/RUN_ID (read-only, sha256 manifest) and submits one array (job name w3scale_RUN_ID).
# The admission ledger (worst case = tasks x TIME) is kept by the lead in LOG.md BEFORE calling this script.
set -euo pipefail
RUN_ID=$1; TASKS=$(realpath "$2"); SCR=$(realpath "$3"); CODE=$(realpath "$4"); PART=$5; TIME=$6; MEM=$7; THR=$8; shift 8
[[ $PART == commons || $PART == scavenge ]] || { echo "partition must be commons or scavenge" >&2; exit 64; }
(( THR >= 1 && THR <= 24 )) || { echo "throttle 1..24" >&2; exit 64; }
BASE=/scratch/fb31/w3scale
RUN_DIR=$BASE/runs/$RUN_ID; OUT=$BASE/out/$RUN_ID
[[ ! -e $RUN_DIR && ! -e $OUT ]] || { echo "run exists" >&2; exit 66; }
[[ -f $CODE/v3.R ]] || { echo "CODE has no v3.R" >&2; exit 66; }
mkdir -p "$RUN_DIR" "$OUT/slurm"
cp "$TASKS" "$RUN_DIR/tasks.tsv"; cp -a "$SCR" "$RUN_DIR/scripts"; cp "$BASE/nots/run_task.sh" "$BASE/nots/env_scale.sh" "$RUN_DIR/"
printf 'RUN_ID=%s\nOUT=%s\nCODE=%s\n' "$RUN_ID" "$OUT" "$CODE" > "$RUN_DIR/config.env"
( cd "$RUN_DIR" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
chmod -R a-w "$RUN_DIR"
n=$(awk -F'\t' 'NF>=2' "$RUN_DIR/tasks.tsv" | wc -l)
args=(--parsable --job-name="w3scale_$RUN_ID" --account=commons --partition=$PART --qos=nots_$PART --nodes=1 --ntasks=1 --cpus-per-task=1
      --mem=$MEM --time=$TIME --export=NONE --no-requeue --array="1-$n%$THR" --output="$OUT/slurm/%A_%a.out" --error="$OUT/slurm/%A_%a.err" "$@")
job=$(sbatch "${args[@]}" "$RUN_DIR/run_task.sh" "$RUN_DIR")
printf '{"run_id":"%s","job":"%s","tasks":%d,"time":"%s","mem":"%s","partition":"%s","submitted_utc":"%s","sbatch":"%s"}\n' \
  "$RUN_ID" "$job" "$n" "$TIME" "$MEM" "$PART" "$(date -u +%FT%TZ)" "${args[*]}" | tee -a "$BASE/submissions.jsonl"
