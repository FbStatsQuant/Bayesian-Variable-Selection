#!/usr/bin/env bash
# W3-SCALE array task: runs line $SLURM_ARRAY_TASK_ID of RUN_DIR/tasks.tsv (columns: task_id <TAB> command).
# The command runs from RUN_DIR/scripts (frozen copy) with OUT, CODE and RUN_DIR exported.
set -euo pipefail
RUN_DIR=$1
source "$RUN_DIR/config.env"     # RUN_ID OUT CODE
source "$RUN_DIR/env_scale.sh" >/dev/null 2>&1
row=$(awk -F'\t' -v t="$SLURM_ARRAY_TASK_ID" '$1 == t' "$RUN_DIR/tasks.tsv")
[[ -n $row ]] || { echo "no task $SLURM_ARRAY_TASK_ID" >&2; exit 65; }
cmd=${row#*$'\t'}
export TMPDIR=/tmp/fb31_w3scale_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}; mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
export RUN_DIR OUT CODE
mkdir -p "$OUT/res" "$OUT/log"
cd "$RUN_DIR/scripts"
t0=$(date +%s)
printf '{"task":%s,"job":"%s","host":"%s","cpu":"%s","start":"%s"}\n' "$SLURM_ARRAY_TASK_ID" "${SLURM_ARRAY_JOB_ID:-$SLURM_JOB_ID}" "$(hostname -s)" "$(grep -m1 'model name' /proc/cpuinfo | sed 's/.*: //')" "$(date -u +%FT%TZ)" >> "$OUT/log/starts.jsonl"
rc=0; bash -c "$cmd" > "$OUT/log/task_${SLURM_ARRAY_TASK_ID}.log" 2>&1 || rc=$?
printf '{"task":%s,"job":"%s","rc":%d,"wall_s":%d,"end":"%s"}\n' "$SLURM_ARRAY_TASK_ID" "${SLURM_ARRAY_JOB_ID:-$SLURM_JOB_ID}" "$rc" "$(( $(date +%s) - t0 ))" "$(date -u +%FT%TZ)" >> "$OUT/log/ends.jsonl"
exit $rc
