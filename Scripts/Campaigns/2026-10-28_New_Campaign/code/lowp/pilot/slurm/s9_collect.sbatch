#!/bin/bash
#SBATCH --job-name=lowp_p9_collect
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:15:00
# P9: collection, AFTER the truth trees were restored (afterany of s8_unlock). It captures terminal accounting of every predecessor job
# (it cannot see its own terminal state: OPS runs final_accounting.sh once it has finished), queries the guard (the campaign tree is readable
# again), and FAILS on any accounting or guard error. Output stays on scratch.
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init collect
mkdir -p -- "$LOG_RUN/accounting"
IDS=$(awk -F'\t' 'NR>1 && $1 != "s9_collect" && $2 ~ /^[0-9]+$/ {print $2}' "$LOG_RUN/jobids.tsv" | paste -sd, -)
[ -n "$IDS" ] || { echo "no predecessor job ids" >&2; exit 1; }
sacct -j "$IDS" -P --units=M \
  --format=JobID,JobName%28,Partition,State,ExitCode,AllocCPUS,ReqMem,Timelimit,Elapsed,TotalCPU,CPUTime,MaxRSS,AveRSS,MaxVMSize,NodeList,Start,End \
  > "$LOG_RUN/accounting/sacct_collector.tsv" || { echo "sacct failed: accounting evidence is incomplete" >&2; exit 1; }
if awk -F'|' 'NR>1 && $1 !~ /\./ && $4 ~ /^(PENDING|RUNNING|REQUEUED|RESIZING|SUSPENDED)/ {bad=1} END{exit !bad}' "$LOG_RUN/accounting/sacct_collector.tsv"; then
  echo "a predecessor job is not terminal" >&2; exit 1
fi
set +e
{ echo "# guard after restoration $(date -u +%FT%TZ)"; "$GUARD" 0; echo "guard_rc=$?"; } > "$LOG_RUN/accounting/guard_after.txt" 2>&1
set -e
grep -q '^guard_rc=0$' "$LOG_RUN/accounting/guard_after.txt" || { echo "guard did not report OK after the pilot" >&2; exit 1; }
{ echo "# disk footprint of the pilot at $(date -u +%FT%TZ), KB"
  for d in "$SCR_ROOT/results/${PILOT_ID}"_* "$LOG_RUN" "$CACHE_ROOT" "$TMP_ROOT" "$CORE_DIR/.cpp_cache" "$RUN_HOME" "$DEV_STUDY" "$STUDY"; do
    if [ -e "$d" ]; then du -sk -- "$d"; fi
  done; } > "$LOG_RUN/accounting/disk_after.txt"
pilot_finish
