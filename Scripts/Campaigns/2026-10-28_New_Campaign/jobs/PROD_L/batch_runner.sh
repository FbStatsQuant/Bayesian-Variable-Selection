#!/bin/bash
# Sourced after pilot initialization. The inventory EXIT trap also preserves pilot cleanup.
: "${PIECE:?}" "${UNITS_FILE:?}" "${PRODL_T0:?}" "${PRODL_WALL_S:?}" "${UNIT_BUDGET_S:?}"
if [[ ${SLURM_RESTART_COUNT:-0} != 0 ]]; then echo "Refusing restarted job ${SLURM_JOB_ID:-unknown}" >&2; exit 71; fi
TASK_ID=${TASK_ID:-${SLURM_ARRAY_TASK_ID:-0}}
JOB_TAG="${SLURM_ARRAY_JOB_ID:-${SLURM_JOB_ID:-local}}_${TASK_ID}"
wall=${PRODL_WALL_S}; budget=${UNIT_BUDGET_S}; offset=0
if [ "${PILOT_LOCAL_TEST:-0}" = 1 ]; then
  wall=${PRODL_TEST_WALL_S:-$wall}; budget=${PRODL_TEST_BUDGET_S:-$budget}; offset=${PRODL_TEST_NOW_OFFSET_S:-0}
fi
deadline=$((PRODL_T0 + wall - START_SLACK_S))
end_source=missing; end_epoch=0
if [[ ${SLURM_JOB_END_TIME:-} =~ ^[0-9]+$ ]]; then end_source=SLURM_JOB_END_TIME; end_epoch=$SLURM_JOB_END_TIME
elif [[ -n ${SLURM_JOB_ID:-} ]]; then
  end_text=$("${SQUEUE:-squeue}" -h -j "$SLURM_JOB_ID" -o %e 2>/dev/null) || end_text=
  candidate=
  if [[ -n $end_text && $end_text != N/A && $end_text != Unknown && $end_text != *$'\n'* ]]; then candidate=$(date -d "$end_text" +%s 2>/dev/null) || candidate=; fi
  if [[ $candidate =~ ^[0-9]+$ ]]; then end_source=squeue; end_epoch=$candidate; fi
fi
if [[ $end_source == missing && ${PILOT_LOCAL_TEST:-0} == 1 ]]; then end_source=local_script_time; end_epoch=$((PRODL_T0 + wall)); fi
if [[ $end_source != missing ]] && (( end_epoch - 60 < deadline )); then deadline=$((end_epoch - 60)); fi
need=$((budget + KILL_GRACE_S + COMMIT_MARGIN_S))
[ -r "$UNITS_FILE" ] || { echo "missing units file: $UNITS_FILE" >&2; exit 66; }
mapfile -t rows < <(awk -F'\t' -v p="$PIECE" -v t="$TASK_ID" 'NR>1 && $1==p && $2==t {print}' "$UNITS_FILE")
(("${#rows[@]}" > 0)) || { echo "no units for $PIECE task $TASK_ID" >&2; exit 66; }
declare -a units outcomes
for row in "${rows[@]}"; do
  IFS=$'\t' read -r pc task unit dataset scale repeat base_piece <<< "$row"
  units+=("$unit"); outcomes+=(not_reached)
done
mkdir -p -- "$LOG_RUN/inventory/$PIECE"
inventory() {
  local tmp="$LOG_RUN/inventory/$PIECE/.$JOB_TAG.$$.tmp" i
  { printf 'unit\toutcome\n'; for ((i=0;i<${#units[@]};i++)); do printf '%s\t%s\n' "${units[i]}" "${outcomes[i]}"; done; } > "$tmp"
  if ! (set -o noclobber; cat "$tmp" > "$LOG_RUN/inventory/$PIECE/$JOB_TAG.tsv") 2>/dev/null; then echo "inventory already exists: $JOB_TAG" >&2; fi
  rm -f -- "$tmp"
}
trap 'inventory || true; rm -rf -- "$JOB_TMP"' EXIT
failed=0; deferring=0
if [[ $end_source == missing ]]; then failed=1; deferring=1; fi
for ((i=0;i<${#rows[@]};i++)); do
  IFS=$'\t' read -r pc task unit dataset scale repeat base_piece <<< "${rows[i]}"
  dir="$LOG_RUN/ledger/$PIECE/$unit"; mkdir -p -- "$dir"
  if [[ -e $dir/$JOB_TAG.start ]]; then
    outcomes[i]=unit_failed; failed=1
    # refusal evidence goes to LOG_RUN/refusals/, never into the unit's ledger folder (the earlier attempt's ledger stays byte-identical)
    mkdir -p -- "$LOG_RUN/refusals"; printf 'unit=%s job_tag=%s outcome=unit_failed reason=start_record_exists utc=%s\n' "$unit" "$JOB_TAG" "$(date -u +%FT%TZ)" >> "$LOG_RUN/refusals/$JOB_TAG.txt"
    echo "unit=$unit reason=start_record_exists" >&2; continue
  fi
  now=$(( $(date +%s) + offset ))
  if (( deferring || now + need > deadline )); then
    deferring=1; outcomes[i]=deferred
    reason=deadline; [[ $end_source != missing ]] || reason=no_scheduler_end_time
    printf 'unit=%s reason=%s now_epoch=%s deadline_epoch=%s need_s=%s end_source=%s end_epoch=%s\n' "$unit" "$reason" "$now" "$deadline" "$need" "$end_source" "$end_epoch" > "$dir/.$JOB_TAG.$$.tmp"
    mv -f -- "$dir/.$JOB_TAG.$$.tmp" "$dir/$JOB_TAG.deferred"
    continue
  fi
  if ! (set -o noclobber; printf 'unit=%s piece=%s task=%s job_tag=%s host=%s start_utc=%s deadline_epoch=%s need_s=%s end_source=%s end_epoch=%s\n' "$unit" "$PIECE" "$TASK_ID" "$JOB_TAG" "$(hostname)" "$(date -u +%FT%TZ)" "$deadline" "$need" "$end_source" "$end_epoch" > "$dir/$JOB_TAG.start") 2>/dev/null; then
    outcomes[i]=unit_failed; failed=1
    # refusal evidence goes to LOG_RUN/refusals/, never into the unit's ledger folder (the earlier attempt's ledger stays byte-identical)
    mkdir -p -- "$LOG_RUN/refusals"; printf 'unit=%s job_tag=%s outcome=unit_failed reason=start_record_exists utc=%s\n' "$unit" "$JOB_TAG" "$(date -u +%FT%TZ)" >> "$LOG_RUN/refusals/$JOB_TAG.txt"
    echo "unit=$unit reason=start_record_exists" >&2; continue
  fi
  if [ "${P5:-0}" = 1 ]; then
    mkdir -p -- "$LOG_RUN/p5_attempts"
    if ! (set -o noclobber; printf 'unit=%s job_tag=%s utc=%s\n' "$unit" "$JOB_TAG" "$(date -u +%FT%TZ)" > "$LOG_RUN/p5_attempts/$unit") 2>/dev/null; then
      outcomes[i]=unit_failed; failed=1
      printf 'unit=%s rc=1 outcome=unit_failed wall_s=0 cli_status=NA cli_skipped=NA end_utc=%s reason=p5_attempt_exists\n' "$unit" "$(date -u +%FT%TZ)" > "$dir/.$JOB_TAG.$$.tmp"
      mv -f -- "$dir/.$JOB_TAG.$$.tmp" "$dir/$JOB_TAG.end"
      continue
    fi
  fi
  actual_piece=$PIECE; [ "${P5:-0}" = 1 ] && actual_piece=$base_piece
  runvar="RUNID_$actual_piece"; runid=${!runvar}
  threadsvar="THREADS_$PIECE"; threads=${!threadsvar}
  if [ -n "${PRODL_UNIT_CMD:-}" ] && [ "${PILOT_LOCAL_TEST:-0}" = 1 ]; then cmd=("$PRODL_UNIT_CMD" "$unit")
  elif [[ $actual_piece = enum20 || $actual_piece = enum30 ]]; then
    export OMP_NUM_THREADS="$threads" LOWP_ENUM_CACHE="$CACHE_ROOT/enum" LOWP_CORE_DIR="$CORE_DIR"
    cmd=(Rscript "$ENUM_DIR/run_enum_dataset.R" --dataset "$dataset" --study "$STUDY" --outroot "$SCR_ROOT" --run-id "$runid" --threads "$threads" --core-dir "$CORE_DIR")
  else
    cmd=(Rscript "$V221_DIR/study/run_case.R" --case "$dataset" --scale "$scale" --study "$STUDY" --outroot "$SCR_ROOT" --run-id "$runid" --core-dir "$CORE_DIR" --mem-gb "$SMC_MEM_GB" --hours "$SMC_HOURS")
    [ "$repeat" = 0 ] || cmd+=(--repeat "$repeat")
    [ "${P5:-0}" = 1 ] && cmd+=(--p5-retry)
  fi
  timed "$PIECE" "$unit" "$threads" timeout --signal=TERM --kill-after="$KILL_GRACE_S" "$budget" "${cmd[@]}"
  timing="$LOG_RUN/timing/$PIECE.$JOB_ID_TAG.tsv"
  if [ "${PILOT_DRYRUN:-0}" = 1 ]; then
    rc=0; elapsed=0
  else
    IFS=$'\t' read -r _ _ _ rc elapsed _ < <(tail -n 1 "$timing")
  fi
  rc=${rc:-1}; elapsed=${elapsed:-NA}
  log="$LOG_RUN/units/$PIECE.$unit.$JOB_ID_TAG.log"; status=NA; v3=NA; skipped=NA
  if [ -f "$log" ]; then
    if [[ $actual_piece = enum* ]]; then
      if grep -qi 'nothing to do' "$log"; then skipped=TRUE; fi
    else
      # run_case.R prints "<prefix> status= <s> skipped= <b>" and then one tab-separated key=value line starting "prefix=": find them by content,
      # not by position (R warnings may follow on stderr, which shares the log)
      kv=$(grep -E '^prefix=' "$log" | tail -n 1 || true)
      status=$(grep -E ' status= ' "$log" | tail -n 1 | sed -n 's/.* status= *\([^[:space:]]*\).*/\1/p' || true); status=${status:-NA}
      v3=$(printf '%s\n' "$kv" | tr '\t' '\n' | sed -n 's/^v3_status=//p'); v3=${v3:-NA}
      skipped=$(printf '%s\n' "$kv" | tr '\t' '\n' | sed -n 's/^skipped=//p'); skipped=${skipped:-NA}
    fi
  fi
  outcome=ok
  if [ "$rc" = 124 ] || [ "$rc" = 137 ]; then outcome=killed_timeout; failed=1
  elif [ "$rc" != 0 ]; then outcome=unit_failed; failed=1
  elif [ "$skipped" = TRUE ]; then outcome=skipped; fi
  outcomes[i]=$outcome
  printf 'unit=%s rc=%s outcome=%s wall_s=%s cli_status=%s cli_skipped=%s end_utc=%s v3_status=%s\n' "$unit" "$rc" "$outcome" "$elapsed" "$status" "$skipped" "$(date -u +%FT%TZ)" "$v3" > "$dir/.$JOB_TAG.$$.tmp"
  mv -f -- "$dir/.$JOB_TAG.$$.tmp" "$dir/$JOB_TAG.end"
done
exit "$failed"
