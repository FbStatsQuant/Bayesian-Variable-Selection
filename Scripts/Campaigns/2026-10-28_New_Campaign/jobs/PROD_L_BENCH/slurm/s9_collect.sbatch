#!/bin/bash
#SBATCH --job-name=lowpB_s9_collect
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
source "$HOME_ROOT/runs/${STAMP}_lowp_bench/code/prod_l_bench/bench.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init collect
mkdir -p -- "$LOG_RUN/accounting/$WAVE"
IDS=$(awk -F'\t' -v wave="$WAVE" 'NR>1 && $1==wave && $3 ~ /^[0-9]+$/ {print $3}' "$LOG_RUN/jobids.tsv" | paste -sd, -)
[ -n "$IDS" ] || { echo "no predecessor job ids" >&2; exit 1; }
"${SACCT:-sacct}" -j "$IDS" -P --units=M --format=JobID,JobName%28,Partition,State,ExitCode,AllocCPUS,ReqMem,Timelimit,Elapsed,TotalCPU,CPUTime,MaxRSS,AveRSS,MaxVMSize,NodeList,Start,End > "$LOG_RUN/accounting/$WAVE/sacct_collector.tsv"
if awk -F'|' -v self="${SLURM_JOB_ID:-}" 'NR>1 && $1 != self && $1 !~ /\./ && $4 !~ /^(COMPLETED|FAILED|CANCELLED.*|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)$/ {bad=1} END{exit !bad}' "$LOG_RUN/accounting/$WAVE/sacct_collector.tsv"; then echo "predecessor not terminal" >&2; exit 1; fi
# every predecessor id of the wave must have at least one accounting row (complete accounting, as the waiter's F10 rule); missing = not proven
if ! awk -F'|' -v ids="$IDS" -v self="${SLURM_JOB_ID:-}" 'BEGIN{n=split(ids,a,","); for(i=1;i<=n;i++) if(a[i]!=self) want[a[i]]=1} NR>1 {split($1,b,"[_.]"); seen[b[1]]=1} END{for(i in want) if(!(i in seen)) bad=1; exit bad}' "$LOG_RUN/accounting/$WAVE/sacct_collector.tsv"; then
  echo "accounting is missing for a predecessor job of the wave: not proven terminal; guard not run" >&2; exit 1
fi
rc=0; "$GUARD" 0 > "$LOG_RUN/accounting/$WAVE/guard_after.txt" 2>&1 || rc=$?
printf 'guard_rc=%s\n' "$rc" >> "$LOG_RUN/accounting/$WAVE/guard_after.txt"
[ "$rc" = 0 ] || exit 1
pilot_finish

