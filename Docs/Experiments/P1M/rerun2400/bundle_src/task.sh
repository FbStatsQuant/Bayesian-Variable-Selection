#!/usr/bin/env bash
# task.sh -- ONE Slurm array task = ONE dataset (rerun2400): its fits run SEQUENTIALLY on this node, alternating OLD and NEW:
#     c100: first side, second side;  c050: first side, second side      (first side = OLD for odd task index, NEW for even)
#   OLD = frozen SMC-BVS v2.2.1 with its own, unchanged study layer (study/run_case.R, adapter reads X/y from a study dir built here by
#         gen_inputs.R with the frozen generator, hash-checked against a manifest row like the original run);
#   NEW = frozen method v3.1 core (Scripts/SMC_BVS/core @ git tree 8ff2d876), list_pip_ab/ab_run.R route (new_fit.R, no adapter).
# Usage (by sbatch only):   task.sh RUN_DIR CHUNKS_FILE_NAME
# The allocation is the original PROD-H one (1 CPU, --mem-gb 2, hours 1.75 for p500 / 24000 s = 6.666666667 for p1000), so stops are
# like for like; both sides get the identical allocation numbers. A task NEVER compiles (precompile job first).
# SMOKE (Owls): LOCAL=1 skips modules/srun/Slurm checks; everything else is this very script.
set -euo pipefail
RUN_DIR=$(realpath "$1"); CHUNKS=$RUN_DIR/${2:?chunks file name}
source "$RUN_DIR/config.env"   # RUN_ID BUNDLE CODE_OLD SUMS_OLD CODE_NEW SUMS_NEW GEN OUTROOT MEM_GB L500 L1000 KILL_MARGIN RUNNER LOCAL(opt)
LOCAL=${LOCAL:-0}
if [[ $LOCAL == 1 ]]; then
  : "${SLURM_ARRAY_TASK_ID:?}"; : "${TMPDIR:?}"
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  export LC_ALL=C.UTF-8 LANG=C.UTF-8
  SLURM_JOB_ID=${SLURM_JOB_ID:-local$$}
else
  [[ -n ${SLURM_JOB_ID:-} && -n ${SLURM_ARRAY_TASK_ID:-} && ${SLURM_CPUS_PER_TASK:-} == 1 ]] || { echo "FATAL: not a 1-CPU array task" >&2; exit 65; }
  source "$RUNNER/env.sh"
fi
source "$RUNNER/frozen_check.sh"
[[ $MEM_GB == 2 && $L500 == 6300 && $L1000 == 24000 && $KILL_MARGIN == 300 ]] || { echo "FATAL: config.env is not the PROD-H allocation" >&2; exit 65; }

row=$(awk -F'\t' -v t="$SLURM_ARRAY_TASK_ID" 'NR > 1 && $1 == t' "$CHUNKS")
[[ -n $row ]] || { echo "FATAL: no chunk row for task $SLURM_ARRAY_TASK_ID" >&2; exit 65; }
IFS=$'\t' read -r task dataset p scales <<< "$row"
[[ $task == "$SLURM_ARRAY_TASK_ID" && $dataset =~ ^p(0500|1000)_S[1-6]_r[0-9]{3}$ ]] || { echo "FATAL: bad chunk row" >&2; exit 65; }
case $p in 500) L=$L500 ;; 1000) L=$L1000 ;; *) echo "FATAL: bad p" >&2; exit 65 ;; esac
HOURS=$(awk -v s="$L" 'BEGIN { printf "%.10g", s / 3600 }'); HARD=$((L + KILL_MARGIN))

( cd "$BUNDLE" && sha256sum --quiet -c SHA256SUMS ) || { echo "FATAL: bundle does not match SHA256SUMS" >&2; exit 67; }
nc_check_frozen "$CODE_OLD" "$SUMS_OLD" || { echo "FATAL: the OLD (v2.2.1) tree is not the frozen one" >&2; exit 67; }
nc_check_frozen "$CODE_NEW" "$SUMS_NEW" || { echo "FATAL: the NEW (v3.1) tree is not the frozen one" >&2; exit 67; }
if [[ $LOCAL != 1 ]]; then
  for pair in "$CODE_OLD" "$CODE_NEW"; do
    key=$(awk '$1 == "compiled_key" { print $2; exit }' "$RUN_DIR/precompile.ok.$(basename "$pair")" 2>/dev/null || true)
    [[ $key =~ ^[0-9a-f]{64}$ && -f $pair/core/.cpp_cache/${key:0:16}/READY ]] || { echo "FATAL: compile cache of $pair not READY; tasks never compile" >&2; exit 66; }
  done
fi

if [[ $LOCAL == 1 ]]; then export TMPDIR=$TMPDIR/${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}   # caller's TMPDIR plus the job suffix
else export TMPDIR=$OUTROOT/tmp/${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}; fi
mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
META=$OUTROOT/meta; mkdir -p "$META"
utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
STUDY=$TMPDIR/study
nice -n 19 Rscript --vanilla "$RUNNER/gen_inputs.R" "$GEN" "$dataset" "$STUDY" > "$META/${dataset}__gen.log" 2>&1 || { echo "FATAL: gen_inputs failed" >&2; exit 68; }

if (( SLURM_ARRAY_TASK_ID % 2 == 1 )); then SIDES=(old new); else SIDES=(new old); fi
IFS=',' read -r -a scale_list <<< "$scales"
k=0
for scale in "${scale_list[@]}"; do
  case_id=${dataset}_${scale}
  for side in "${SIDES[@]}"; do
    k=$((k + 1))
    stem=$META/${case_id}__${side}
    if [[ $side == old ]]; then
      cmd=(Rscript --vanilla "$CODE_OLD/study/run_case.R" --case "$dataset" --scale "$scale" --study "$STUDY" --outroot "$OUTROOT/old"
           --run-id "$RUN_ID" --core-dir "$CODE_OLD/core" --mem-gb "$MEM_GB" --hours "$HOURS")
    else
      cmd=(Rscript --vanilla "$RUNNER/new_fit.R" --case "$dataset" --scale "$scale" --gen-dir "$GEN" --core-dir "$CODE_NEW/core"
           --outroot "$OUTROOT/new" --run-id "$RUN_ID" --mem-gb "$MEM_GB" --hours "$HOURS")
    fi
    pre=(); [[ $LOCAL == 1 ]] || pre=(srun --ntasks=1 --cpus-per-task=1 --job-name="${side}_${case_id}" --kill-on-bad-exit=0)
    t0=$(date +%s); started=$(utc); rc=0
    "${pre[@]}" nice -n 19 timeout --signal=TERM --kill-after=60 "$HARD" "${cmd[@]}" > "$stem.log" 2>&1 || rc=$?
    wall=$(( $(date +%s) - t0 ))
    timed_out=false; [[ ($rc == 124 || $rc == 137) && $wall -ge $HARD ]] && timed_out=true
    v3s=$(tail -n 1 "$stem.log" 2>/dev/null | tr '\t' '\n' | sed -n 's/^v3_status=//p' | tr -c 'A-Za-z0-9_,\n' '?' | head -n 1 || true)
    printf '{"case_id":"%s","side":"%s","order":%d,"task":%s,"array_job":"%s","job":"%s","host":"%s","started_utc":"%s","finished_utc":"%s","wall_s":%d,"exit":%d,"timed_out":%s,"v3_status":"%s","unit_limit_s":%d,"hours":"%s"}\n' \
      "$case_id" "$side" "$k" "$SLURM_ARRAY_TASK_ID" "${SLURM_ARRAY_JOB_ID:-}" "$SLURM_JOB_ID" "$(hostname -s)" "$started" "$(utc)" "$wall" "$rc" "$timed_out" "${v3s:-}" "$L" "$HOURS" > "$stem.json"
    # admission refusal (preflight projects more than the allocation): stop this task and leave an alert for the poller
    if [[ ${v3s:-} == resource_limit && $wall -lt 5 ]]; then
      echo "ALERT admission refusal: $case_id $side resource_limit in ${wall}s" | tee "$OUTROOT/ALERT_admission_${case_id}_${side}" >&2
      exit 3
    fi
  done
done
exit 0
