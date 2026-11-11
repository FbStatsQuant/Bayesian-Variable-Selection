#!/usr/bin/env bash
# W3-P6 array task: runs line $SLURM_ARRAY_TASK_ID of RUN_DIR/tasks.tsv (columns: task_id <TAB> command).
# The command runs from RUN_DIR/scripts (frozen copy) with OUT=/scratch/fb31/theory_w3/<RUN_ID>.
set -euo pipefail
RUN_DIR=$1
source "$RUN_DIR/config.env"     # RUN_ID OUT CODE TICKETS
source /home/fb31/projects/BVS/theory_w3/sim/env_sim.sh >/dev/null 2>&1
row=$(awk -F'\t' -v t="$SLURM_ARRAY_TASK_ID" '$1 == t' "$RUN_DIR/tasks.tsv")
[[ -n $row ]] || { echo "no task $SLURM_ARRAY_TASK_ID" >&2; exit 65; }
cmd=${row#*$'\t'}
export TMPDIR=/tmp/fb31_w3p6_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}; mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
export RUN_DIR OUT CODE TICKETS
mkdir -p "$OUT/raw" "$OUT/rds" "$OUT/log"
cd "$RUN_DIR/scripts"
t0=$(date +%s)
printf '{"task":%s,"job":"%s","host":"%s","start":"%s"}\n' "$SLURM_ARRAY_TASK_ID" "${SLURM_ARRAY_JOB_ID:-$SLURM_JOB_ID}" "$(hostname -s)" "$(date -u +%FT%TZ)" >> "$OUT/log/starts.jsonl"
rc=0; bash -c "$cmd" > "$OUT/log/task_${SLURM_ARRAY_TASK_ID}.log" 2>&1 || rc=$?
printf '{"task":%s,"job":"%s","rc":%d,"wall_s":%d,"end":"%s"}\n' "$SLURM_ARRAY_TASK_ID" "${SLURM_ARRAY_JOB_ID:-$SLURM_JOB_ID}" "$rc" "$(( $(date +%s) - t0 ))" "$(date -u +%FT%TZ)" >> "$OUT/log/ends.jsonl"
exit $rc
