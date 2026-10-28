#!/usr/bin/env bash
# One Slurm array task = one dataset chunk: its units run in order (c100, then c050).
# Usage (by submit.sh / rerun.sh only): sbatch ... task.sh RUN_DIR [UNITS_FILE]
# RUN_DIR holds config.env and chunks.tsv (frozen at submission). Seeds are never passed:
# the adapter derives them from the dataset ID (method seed = data seed + 4,000,000).
# UNITS_FILE (reruns only): one case_id per line; units of this chunk not listed are not touched,
# so a rerun never repeats a finished, timed-out or still-pending unit (GO_2400 C4).
set -euo pipefail
RUN_DIR=$(realpath "$1")
UNITS_FILE=${2:-}
[[ -z $UNITS_FILE || -s $UNITS_FILE ]] || { echo "FATAL: empty or missing units file" >&2; exit 65; }
[[ -n ${SLURM_JOB_ID:-} && -n ${SLURM_ARRAY_TASK_ID:-} && ${SLURM_CPUS_PER_TASK:-} == 1 ]] || { echo "FATAL: not a 1-CPU array task" >&2; exit 65; }
source "$RUN_DIR/config.env"   # RUN_ID CODE STUDY OUTROOT DEV MEM_GB L500 L1000 KILL_MARGIN RUNNER
source "$RUNNER/env.sh"

row=$(awk -F'\t' -v t="$SLURM_ARRAY_TASK_ID" 'NR > 1 && $1 == t' "$RUN_DIR/chunks.tsv")
[[ -n $row ]] || { echo "FATAL: no chunk row for task $SLURM_ARRAY_TASK_ID" >&2; exit 65; }
IFS=$'\t' read -r task dataset p scales <<< "$row"
[[ $task == "$SLURM_ARRAY_TASK_ID" && $dataset =~ ^(dev_)?p(0500|1000)_S[1-6]_r[0-9]{3}$ ]] || { echo "FATAL: bad chunk row" >&2; exit 65; }
case $p in 500) L=$L500 ;; 1000) L=$L1000 ;; *) echo "FATAL: bad p" >&2; exit 65 ;; esac
HOURS=$(awk -v s="$L" 'BEGIN { printf "%.10g", s / 3600 }')
HARD=$((L + KILL_MARGIN))
dev_args=(); [[ $DEV == 1 ]] && dev_args=(--development)

export TMPDIR=/tmp/fb31_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}
mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT

utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
IFS=',' read -r -a scale_list <<< "$scales"
for scale in "${scale_list[@]}"; do
  case_id=${dataset}_${scale}
  if [[ -n $UNITS_FILE ]] && ! grep -qxF "$case_id" "$UNITS_FILE"; then continue; fi
  att_dir=$OUTROOT/attempts/$case_id
  mkdir -p "$att_dir"
  # Rerun mode (units file): run a unit only if it has no attempt yet (orphan) or exactly ONE attempt
  # that ended without .done and not by timeout (review R2). Anything else is left untouched.
  if [[ -n $UNITS_FILE ]]; then
    n_prev=$(find "$att_dir" -maxdepth 1 -name 'attempt_*.start.json' | wc -l)
    eligible=false
    if (( n_prev == 0 )); then eligible=true
    elif (( n_prev == 1 )) && [[ -f $att_dir/attempt_1.end.json ]] \
         && grep -q '"done":false' "$att_dir/attempt_1.end.json" && grep -q '"timed_out":false' "$att_dir/attempt_1.end.json"; then eligible=true
    elif (( n_prev == 1 )) && [[ ! -f $att_dir/attempt_1.end.json ]]; then eligible=true   # task died mid-unit
    fi
    if [[ $eligible == false ]]; then
      printf '{"case_id":"%s","utc":"%s","job":"%s","skipped":"not eligible for a rerun","previous_attempts":%d}\n' \
        "$case_id" "$(utc)" "$SLURM_JOB_ID" "$n_prev" >> "$att_dir/rerun_skips.jsonl"
      continue
    fi
  fi
  cmd=(Rscript --vanilla "$CODE/code/study/run_case.R" --case "$dataset" --scale "$scale"
       --study "$STUDY" --outroot "$OUTROOT" --run-id "$RUN_ID" --core-dir "$CODE/code/core"
       --mem-gb "$MEM_GB" --hours "$HOURS" "${dev_args[@]}")
  # Atomic attempt number: noclobber creation fails if another task took this k (review R2).
  k=1
  while ! ( set -C; printf '{"case_id":"%s","attempt":%d,"job":"%s","array_job":"%s","task":"%s","scale":"%s","host":"%s","started_utc":"%s","unit_limit_s":%d,"hard_kill_s":%d,"hours":"%s","command":"%s"}\n' \
      "$case_id" "$k" "$SLURM_JOB_ID" "${SLURM_ARRAY_JOB_ID:-}" "$SLURM_ARRAY_TASK_ID" "$scale" "$(hostname -s)" "$(utc)" \
      "$L" "$HARD" "$HOURS" "${cmd[*]}" > "$att_dir/attempt_$k.start.json" ) 2>/dev/null; do
    k=$((k + 1))
    # Review N3: a create failure other than "exists" (quota, missing dir) must not spin to the wall.
    (( k <= 20 )) || { echo "FATAL: cannot create an attempt record in $att_dir" >&2; exit 70; }
  done
  stem=$att_dir/attempt_$k
  prefix=$OUTROOT/results/$RUN_ID/p$(printf '%04d' "$p")/$case_id/SMCBVS
  lock_before=false; [[ -d $prefix.lock ]] && lock_before=true
  t0=$(date +%s)
  rc=0
  # One job step per unit, so sacct reports its own State, Elapsed and MaxRSS.
  # timeout runs inside the step: a unit-limit kill exits 124 (TERM) or 137 (KILL after 60 s).
  srun --ntasks=1 --cpus-per-task=1 --job-name="$case_id" --kill-on-bad-exit=0 \
    nice -n 19 timeout --signal=TERM --kill-after=60 "$HARD" "${cmd[@]}" > "$stem.log" 2>&1 || rc=$?
  wall=$(( $(date +%s) - t0 ))
  done_flag=false; [[ -f $prefix.done ]] && done_flag=true
  timed_out=false; [[ ($rc == 124 || $rc == 137) && $wall -ge $HARD ]] && timed_out=true
  # A lock that did NOT exist before this attempt was made by this attempt's child, which has
  # now exited (SIGTERM/SIGKILL skip R's on.exit), so it is stale and safe to remove. A lock that
  # pre-existed is never touched here: `reconcile.py --clear-stale-locks` (run by rerun.sh) clears it
  # on the login node only after confirming that no job of this run holds that unit (review F4, C4).
  # Review R7: also require that the lock's owner process (recorded by the adapter) is not alive here.
  lock_removed=false
  if [[ $lock_before == false && -d $prefix.lock ]]; then
    owner_pid=$(awk '$1 == "pid" { print $2 }' "$prefix.lock/owner.txt" 2>/dev/null || true)
    owner_host=$(awk '$1 == "host" { print $2 }' "$prefix.lock/owner.txt" 2>/dev/null || true)
    # No owner.txt (yet): leave it; reconcile.py --clear-stale-locks handles dead units on the login node.
    if [[ -n $owner_pid && ( $owner_host == "$(hostname -s)" || $owner_host == "$(hostname)" ) && ! -e /proc/$owner_pid ]]; then
      rm -rf "$prefix.lock"; lock_removed=true
    fi
  fi
  printf '{"case_id":"%s","attempt":%d,"finished_utc":"%s","exit":%d,"wall_s":%d,"timed_out":%s,"done":%s,"lock_preexisted":%s,"stale_lock_removed":%s}\n' \
    "$case_id" "$k" "$(utc)" "$rc" "$wall" "$timed_out" "$done_flag" "$lock_before" "$lock_removed" > "$stem.end.json"
done
