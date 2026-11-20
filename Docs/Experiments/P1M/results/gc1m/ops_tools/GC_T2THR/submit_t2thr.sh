#!/usr/bin/env bash
# submit_t2thr.sh -- GC_T2THR (HQ H-47): ONE sbatch (the island 1 re-run at 48 threads). Run ON NOTS by ops after the manager's GO; CONFIRM=yes.
set -euo pipefail
DEPT=/home/fb31/SMC_Engineering_Department
SCR=$DEPT/scripts/GC_T2THR
[[ ${CONFIRM:-} == yes ]] || { echo "refusing: set CONFIRM=yes" >&2; exit 64; }
cd "$SCR"
sha256sum --quiet -c SHA256SUMS || { echo "FATAL: scripts differ from SHA256SUMS" >&2; exit 66; }
[[ -x $SCR/bin/smcbvs4 ]] || { echo "FATAL: binary missing" >&2; exit 66; }
[[ -d $DEPT/scratch/slurm_out && -d $DEPT/scratch/tmp ]] || { echo "FATAL: scratch/slurm_out or scratch/tmp missing" >&2; exit 66; }
mkdir -p "$DEPT/scratch/runs/GC_T2THR"
LOG=$DEPT/scratch/runs/GC_T2THR/submissions.jsonl
log() { printf '{"stage":"%s","fit":"%s","job":"%s","submitted_utc":"%s"}\n' "$1" "$2" "$3" "$(date -u +%FT%TZ)" | tee -a "$LOG"; }
jt=$(sbatch --parsable --array=1-1 stage_t2thr.sbatch); log t2thr 6-AR-n200-r01-V-s1 "$jt"
echo "submitted T2THR"
