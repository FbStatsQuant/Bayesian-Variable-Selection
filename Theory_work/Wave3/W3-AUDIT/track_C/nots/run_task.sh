#!/usr/bin/env bash
# W3-AUDIT-C array task: runs line $SLURM_ARRAY_TASK_ID of $PKG/tasks_<CLASS>.tsv (columns: task_id did n p reps).
# Usage (via sbatch, see submit.sh): run_task.sh PKG CLASS
set -euo pipefail
PKG=$1; CLASS=$2
OUT=/scratch/fb31/SMC_Theory_Department/W3-AUDIT-C
source "$PKG/env_c.sh" >/dev/null 2>&1
row=$(awk -v t="$SLURM_ARRAY_TASK_ID" '$1 == t' "$PKG/tasks_${CLASS}.tsv")
[[ -n $row ]] || { echo "no task $SLURM_ARRAY_TASK_ID" >&2; exit 65; }
read -r _ did n p reps <<<"$row"
export TMPDIR=/tmp/fb31_w3auditc_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}; mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
export C_LDIR="$PKG/data"
mkdir -p "$OUT/out" "$OUT/log"
t0=$(date +%s)
rc=0; python3 "$PKG/scripts/c_run_cell.py" "$did" "$n" "$p" "$reps" "$OUT/out" > "$OUT/log/${CLASS}_${SLURM_ARRAY_TASK_ID}.log" 2>&1 || rc=$?
printf '{"class":"%s","task":%s,"did":%s,"n":%s,"p":%s,"job":"%s","host":"%s","rc":%d,"wall_s":%d,"end":"%s"}\n' \
  "$CLASS" "$SLURM_ARRAY_TASK_ID" "$did" "$n" "$p" "${SLURM_ARRAY_JOB_ID:-$SLURM_JOB_ID}" "$(hostname -s)" "$rc" "$(( $(date +%s) - t0 ))" "$(date -u +%FT%TZ)" >> "$OUT/log/ends.jsonl"
exit $rc
