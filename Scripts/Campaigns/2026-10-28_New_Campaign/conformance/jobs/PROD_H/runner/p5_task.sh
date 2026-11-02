#!/usr/bin/env bash
# One P5 array task = ONE unit (DECISIONS D11): the primary CLI plus --p5-retry, with the PRIMARY --mem-gb 2 --hours L/3600
# (the adapter doubles both itself; Slurm gives 4G). Submitted by p5_submit.sh only:  sbatch ... p5_task.sh RUN_DIR
# At most ONE P5 attempt per unit, ever: the task first creates LOGROOT/p5_attempts/<case_id>.start.json with noclobber. If the file exists
# the task refuses (writes <case_id>.refused.jsonl, runs nothing, exits 0). The attempt record is never removed.
# Retry files: <results>/pPPPP/<case_id>/P5_retry/SMCBVS_p5retry.{rds,csv,sha256,done}. Logs and attempt files: LOGROOT (scratch).
# Hard limit per unit: timeout 2L + 300 s (then KILL after 60 s).
set -euo pipefail
RUN_DIR=$(realpath "$1")
[[ -n ${SLURM_JOB_ID:-} && -n ${SLURM_ARRAY_TASK_ID:-} && ${SLURM_CPUS_PER_TASK:-} == 1 ]] || { echo "FATAL: not a 1-CPU array task" >&2; exit 65; }
source "$RUN_DIR/config.env"
source "$RUNNER/env.sh"
source "$RUNNER/frozen_check.sh"
source "$RUNNER/common.sh"
[[ $MEM_GB == 2 && $L500 == 6300 && $L1000 == 24000 && $KILL_MARGIN == 300 ]] || { echo "FATAL: config.env is not the GO_2400 C1 allocation" >&2; exit 65; }
row=$(awk -F'\t' -v t="$SLURM_ARRAY_TASK_ID" 'NR > 1 && $1 == t' "$RUN_DIR/p5/units.tsv")
[[ -n $row ]] || { echo "FATAL: no P5 unit for task $SLURM_ARRAY_TASK_ID" >&2; exit 65; }
IFS=$'\t' read -r idx case_id dataset scale p L <<< "$row"
[[ $case_id == "${dataset}_${scale}" && $dataset =~ ^p(0500|1000)_S[1-6]_r[0-9]{3}$ && $scale =~ ^c(100|050)$ ]] || { echo "FATAL: bad P5 row" >&2; exit 65; }
case $p in 500) [[ $L == "$L500" ]] || exit 65 ;; 1000) [[ $L == "$L1000" ]] || exit 65 ;; *) exit 65 ;; esac
HOURS=$(awk -v s="$L" 'BEGIN { printf "%.10g", s / 3600 }')
HARD=$((2 * L + KILL_MARGIN))
nc_check_frozen "$CODE" "$SUMS" || { echo "FATAL: the v2.2.1 tree is not the frozen one" >&2; exit 67; }
nc_cache_ready "$CODE" "$RUN_DIR" || { echo "FATAL: compile cache not READY; tasks never compile" >&2; exit 66; }
export TMPDIR=$LOGROOT/tmp/p5_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}
mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"; rmdir "$LOGROOT/tmp" 2>/dev/null || true' EXIT
utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
att=$LOGROOT/p5_attempts
mkdir -p "$att"
cmd=(Rscript --vanilla "$CODE/study/run_case.R" --case "$dataset" --scale "$scale"
     --study "$STUDY" --outroot "$OUTROOT" --run-id "$RUN_ID" --core-dir "$CODE/core"
     --mem-gb "$MEM_GB" --hours "$HOURS" --p5-retry)
# the durable attempt record (noclobber): a second attempt of this unit is refused
if ! ( set -C; printf '{"case_id":"%s","job":"%s","array_job":"%s","task":"%s","host":"%s","started_utc":"%s","unit_limit_s":%d,"hard_kill_s":%d,"hours":"%s","command":"%s"}\n' \
      "$case_id" "$SLURM_JOB_ID" "${SLURM_ARRAY_JOB_ID:-}" "$SLURM_ARRAY_TASK_ID" "$(hostname -s)" "$(utc)" "$L" "$HARD" "$HOURS" "${cmd[*]}" > "$att/$case_id.start.json" ) 2>/dev/null; then
  printf '{"case_id":"%s","utc":"%s","job":"%s","refused":"second P5 attempt"}\n' "$case_id" "$(utc)" "$SLURM_JOB_ID" >> "$att/$case_id.refused.jsonl"
  echo "REFUSED: $case_id already has a P5 attempt record; at most one P5 attempt per unit, ever" >&2
  exit 0
fi
prefix=$OUTROOT/results/$RUN_ID/p$(printf '%04d' "$p")/$case_id/P5_retry/SMCBVS_p5retry
t0=$(date +%s); rc=0
srun --ntasks=1 --cpus-per-task=1 --job-name="${case_id}_p5" --kill-on-bad-exit=0 \
  nice -n 19 timeout --signal=TERM --kill-after=60 "$HARD" "${cmd[@]}" > "$att/$case_id.log" 2>&1 || rc=$?
wall=$(( $(date +%s) - t0 ))
done_flag=false; [[ -f $prefix.done ]] && done_flag=true
# A hard-killed child (SIGKILL, OOM-kill, node loss) leaves its lock and temporary files. They are NOT removed here (the owner may be on another
# host and no job of the run is known to be dead yet): cleanup_terminal.sh archives and removes only PROVEN-stale ones once every job is terminal.
lock_left=false; [[ -d $prefix.lock ]] && lock_left=true
timed_out=false; [[ ($rc == 124 || $rc == 137) && $wall -ge $HARD ]] && timed_out=true
v3s=$(tail -n 1 "$att/$case_id.log" 2>/dev/null | tr '\t' '\n' | sed -n 's/^v3_status=//p' | tr -c 'A-Za-z0-9_,\n' '?' | head -n 1 || true)
stp=$(tail -n 1 "$att/$case_id.log" 2>/dev/null | tr '\t' '\n' | sed -n 's/^stop=//p' | tr -c 'A-Za-z0-9_./\n' '?' | head -n 1 || true)
printf '{"case_id":"%s","finished_utc":"%s","exit":%d,"wall_s":%d,"timed_out":%s,"done":%s,"lock_left":%s,"v3_status":"%s","stop":"%s"}\n' \
  "$case_id" "$(utc)" "$rc" "$wall" "$timed_out" "$done_flag" "$lock_left" "${v3s:-}" "${stp:-}" > "$att/$case_id.end.json"
exit 0
