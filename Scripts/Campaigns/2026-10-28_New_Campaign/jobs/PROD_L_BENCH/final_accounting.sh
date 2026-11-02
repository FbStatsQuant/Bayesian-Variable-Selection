#!/bin/bash
# final_accounting.sh -- OPS, on NOTS, AFTER the collect job has finished: the terminal accounting snapshot of EVERY pilot job including the
# collector (the collector cannot see its own terminal state). Writes LOG_RUN/accounting/sacct_final.tsv and the exit status says whether all
# recorded jobs (and array tasks) are terminal.
#   bash final_accounting.sh STAMP
# Exit 0 = snapshot written and every row terminal; 1 = some job not terminal; 2 = sacct failed or no job ids (never silent).
set -uo pipefail
STAMP="${1:?usage: final_accounting.sh STAMP}"
export STAMP
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$HERE/bench.env"
[[ "$STAMP" =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || { echo "bad STAMP" >&2; exit 2; }
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"; SCR_ROOT="${NC_SCR_ROOT:-/scratch/fb31/New_Campaign}"
PID="${STAMP}_lowp_bench"; LOG_RUN="$SCR_ROOT/logs/$PID"; SACCT="${SACCT:-sacct}"
[ -r "$LOG_RUN/jobids.tsv" ] || { echo "no $LOG_RUN/jobids.tsv" >&2; exit 2; }
IDS=$(awk -F'\t' 'NR>1 && $3 ~ /^[0-9]+$/ {print $3}' "$LOG_RUN/jobids.tsv" | paste -sd, -)
[ -n "$IDS" ] || { echo "no job ids recorded" >&2; exit 2; }
mkdir -p "$LOG_RUN/accounting"
"$SACCT" -j "$IDS" -P --units=M --format=JobID,JobName%28,Partition,State,ExitCode,AllocCPUS,ReqMem,Timelimit,Elapsed,ElapsedRaw,TotalCPU,CPUTime,MaxRSS,AveRSS,MaxVMSize,NodeList,Start,End \
  > "$LOG_RUN/accounting/sacct_final.tsv" || { echo "sacct failed" >&2; exit 2; }
awk -F'|' 'NR==FNR {if(FNR>1) {split($0,j,"\t"); step[j[3]]=j[2]} next} FNR>1 && $1 !~ /\./ {split($1,a,"_"); if(!(a[1] in step) || $6 !~ /^[0-9]+$/ || $10 !~ /^[0-9]+$/) {bad=1; next} seen[a[1]]=1; h[step[a[1]]]+=$6*$10/3600; total+=$6*$10/3600} END {print "step\tcore_hours"; for (s in h) printf "%s\t%.6f\n",s,h[s]; printf "TOTAL\t%.6f\n",total; for(i in step)if(!seen[i])bad=1; if(bad)exit 1}' "$LOG_RUN/jobids.tsv" "$LOG_RUN/accounting/sacct_final.tsv" > "$LOG_RUN/accounting/core_hours.tsv" || { echo "invalid or missing accounting rows" >&2; exit 2; }
cat "$LOG_RUN/accounting/core_hours.tsv"
echo "Estimate: $HERE/CORE_HOURS.md"
bad=$(awk -F'|' 'NR>1 && $1 !~ /\./ && $4 !~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)/ {print $1" "$4}' "$LOG_RUN/accounting/sacct_final.tsv")
if [ -n "$bad" ]; then echo "NOT TERMINAL:" >&2; echo "$bad" >&2; exit 1; fi
echo "final accounting written: $LOG_RUN/accounting/sacct_final.tsv ($(($(wc -l < "$LOG_RUN/accounting/sacct_final.tsv") - 1)) rows)"
cp "$LOG_RUN/jobids.tsv" "$HOME_ROOT/runs/$PID/JOBIDS.tsv" 2>/dev/null || true
mkdir -p "$HOME_ROOT/runs/$PID/manifests"
cp "$LOG_RUN/jobids.tsv" "$HOME_ROOT/runs/$PID/manifests/JOBIDS.tsv"
exit 0

