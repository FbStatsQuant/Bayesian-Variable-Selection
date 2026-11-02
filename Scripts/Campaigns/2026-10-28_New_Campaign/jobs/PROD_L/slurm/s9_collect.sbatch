#!/bin/bash
#SBATCH --job-name=lowpL_s9_collect
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:15:00
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}"
source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init collect
mkdir -p -- "$LOG_RUN/accounting/$WAVE"
IDS=$(awk -F'\t' -v wave="$WAVE" 'NR>1 && $1==wave && $3 ~ /^[0-9]+$/ {print $3}' "$LOG_RUN/jobids.tsv" | paste -sd, -)
[ -n "$IDS" ] || { echo "no predecessor job ids" >&2; exit 1; }
"${SACCT:-sacct}" -j "$IDS" -P --units=M --format=JobID,JobName%28,Partition,State,ExitCode,AllocCPUS,ReqMem,Timelimit,Elapsed,TotalCPU,CPUTime,MaxRSS,AveRSS,MaxVMSize,NodeList,Start,End > "$LOG_RUN/accounting/$WAVE/sacct_collector.tsv"
if ! grep -q WAVE_UNLOCK_VERIFIED "$LOG_RUN/truthlock/$WAVE/WAVE_UNLOCK.txt" 2>/dev/null || [[ $(stat -c %a "$STUDY/truth" 2>/dev/null) != 755 || $(stat -c %a "$STUDY/dev/truth" 2>/dev/null) != 755 ]]; then
  echo "Guard skipped: run recover_truth.sh, then verify truth hashes." > "$LOG_RUN/accounting/$WAVE/GUARD_SKIPPED.txt"; exit 1
fi
if awk -F'|' -v self="${SLURM_JOB_ID:-}" 'NR>1 && $1 != self && $1 !~ /\./ && $4 !~ /^(COMPLETED|FAILED|CANCELLED.*|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)$/ {bad=1} END{exit !bad}' "$LOG_RUN/accounting/$WAVE/sacct_collector.tsv"; then echo "predecessor not terminal" >&2; exit 1; fi
rc=0; "$GUARD" 0 > "$LOG_RUN/accounting/$WAVE/guard_after.txt" 2>&1 || rc=$?
printf 'guard_rc=%s\n' "$rc" >> "$LOG_RUN/accounting/$WAVE/guard_after.txt"
[ "$rc" = 0 ] || exit 1
pilot_finish
