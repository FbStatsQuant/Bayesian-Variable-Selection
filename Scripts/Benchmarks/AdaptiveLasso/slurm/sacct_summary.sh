#!/bin/bash
# Elapsed time and MaxRSS of the dev array tasks as CSV (case_id, state, elapsed_s, maxrss_mb).
# Usage: bash slurm/sacct_summary.sh <array job id> > sacct.csv
set -eo pipefail
JOB=$1
echo "case_id,array_task,state,elapsed_s,maxrss_mb"
sacct -j "$JOB" --format=JobID,State,ElapsedRaw,MaxRSS -P -n | awk -F'|' '
  $1 ~ /\.batch$/ {
    split($1, a, "[_.]"); t = a[2] + 0
    if (t <= 6) { p = "0500"; s = t } else { p = "1000"; s = t - 6 }
    rss = $4; mb = rss
    if (rss ~ /K$/) mb = substr(rss, 1, length(rss) - 1) / 1024
    else if (rss ~ /M$/) mb = substr(rss, 1, length(rss) - 1) + 0
    else if (rss ~ /G$/) mb = substr(rss, 1, length(rss) - 1) * 1024
    else if (rss != "") mb = rss / 1048576
    printf "dev_p%s_S%d_r001_c100,%d,%s,%s,%.1f\n", p, s, t, $2, $3, mb
  }'
