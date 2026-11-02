#!/usr/bin/env bash
# final_accounting.sh -- OPS, on NOTS, AFTER every job of the run is terminal (primary arrays, reruns, P5): the terminal sacct snapshot of EVERY
# job id in jobs.tsv, and the core-hour totals by array (primary p500, primary p1000, P5, precompile, reruns).
#   bash RUN_DIR/runner/final_accounting.sh
# Writes (home, small) RUN_DIR/accounting/sacct_final.tsv and RUN_DIR/accounting/core_hours.{tsv,json}; copies them to LOGROOT/accounting/ so
# they travel with the logs folder. Columns: JobID,JobName,State,ExitCode,Elapsed,NodeList,MaxRSS,AllocCPUS,CPUTimeRAW.
# Exit 0 = snapshot written and every job-level row terminal | 1 = some job not terminal | 2 = sacct failed or no job ids (never silent).
set -uo pipefail
RUNNER_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$RUNNER_DIR/common.sh"
nc_refuse_hooks
RUN_DIR="$HOME_ROOT/runs/$(basename "$(cd "$RUNNER_DIR/.." && pwd)")"
nc_load_run "$RUN_DIR"
PY=$(nc_python)
IDS=$(nc_job_ids "$RUN_DIR" | paste -sd, -)
[[ -n $IDS ]] || { echo "no job ids in $RUN_DIR/jobs.tsv" >&2; exit 2; }
live=$(nc_live_jobs "$RUN_DIR") || { echo "squeue failed" >&2; exit 2; }
[[ -z $live ]] || { echo "NOT TERMINAL (still in the queue): $(echo $live)" >&2; exit 1; }
first=$(awk -F'\t' 'NR == 2 { print substr($3, 1, 10) }' "$RUN_DIR/jobs.tsv")
since=$(date -u -d "$first - 1 day" +%F) || { echo "bad submission date in jobs.tsv" >&2; exit 2; }
mkdir -p "$RUN_DIR/accounting"
sacct -S "$since" -j "$IDS" -P -o JobID,JobName%40,State,ExitCode,Elapsed,NodeList,MaxRSS,AllocCPUS,CPUTimeRAW > "$RUN_DIR/accounting/sacct_final.tsv" \
  || { echo "sacct failed" >&2; exit 2; }
[[ $(wc -l < "$RUN_DIR/accounting/sacct_final.tsv") -gt 1 ]] || { echo "sacct returned no rows" >&2; exit 2; }
bad=$(awk -F'|' 'NR > 1 && $1 !~ /\./ && $3 !~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)/ { print $1 " " $3 }' "$RUN_DIR/accounting/sacct_final.tsv")
if [[ -n $bad ]]; then echo "NOT TERMINAL:" >&2; echo "$bad" >&2; exit 1; fi
# every recorded job must appear in the snapshot
for j in $(nc_job_ids "$RUN_DIR"); do
  awk -F'|' -v j="$j" 'NR > 1 { split($1, a, /[_.]/); if (a[1] == j) f = 1 } END { exit !f }' "$RUN_DIR/accounting/sacct_final.tsv" \
    || { echo "job $j is missing from the sacct snapshot" >&2; exit 2; }
done
"$PY" "$RUNNER/accounting_summary.py" "$RUN_DIR" "$RUN_DIR/accounting/sacct_final.tsv" "$RUN_DIR/accounting/core_hours" > /dev/null || { echo "accounting summary failed" >&2; exit 2; }
mkdir -p "$LOGROOT/accounting"; cp "$RUN_DIR"/accounting/* "$LOGROOT/accounting/"
echo "final accounting written: $RUN_DIR/accounting/sacct_final.tsv ($(( $(wc -l < "$RUN_DIR/accounting/sacct_final.tsv") - 1 )) rows); totals:"
cat "$RUN_DIR/accounting/core_hours.tsv"
exit 0
