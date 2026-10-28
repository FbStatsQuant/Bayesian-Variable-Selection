#!/bin/bash
# One infrastructure retry (master §IV.2.4) of an A1 production (or smoke) run: resubmits only the
# array tasks that still have an expected (case, method) without a valid bundle (bundles.sh
# contract), from the SAME frozen snapshot and run id, with doubled --time and --mem and %133.
# Valid bundles (including saved method failures) are skipped by the runner; partial bundles are
# quarantined by the runner before refitting.
# Exclusive: the retry slot is reserved by an atomic mkdir of <run>/attempt2.reserved before any
# check; the submission intent is written before sbatch and the job id atomically after it, so an
# interrupted submission leaves an explicit "ambiguous" record instead of allowing a second retry.
# Refuses if: the slot is taken, attempt 1 is not finalized, the scheduler cannot be queried, any job
# of the run is active, or the snapshot does not match its hash list.
# Pairs still missing after this retry are final; the G8 reconciliation writes timeout/not_run rows.
# Usage (login node): bash slurm/retry_prod.sh <RUN_ID> [--dry-run]
set -eo pipefail
RUN_ID=$1; DRY=${2:-}
STUDY=/projects/ml75/fb31/BVS/bench20261019
RUN=${STUDY}/runs/${RUN_ID}; SNAP=${RUN}/code
LOGS=${STUDY}/logs/prod/A1_SuSiE
M1=${RUN}/manifest.json; M2=${RUN}/manifest_attempt2.json
source "${SNAP}/slurm/bundles.sh"
[ -f "${M1}" ] || { echo "no manifest for ${RUN_ID}"; exit 1; }
if [ "${DRY}" != --dry-run ]; then
  mkdir "${RUN}/attempt2.reserved" 2>/dev/null || { echo "refusing: the retry slot of ${RUN_ID} is already taken"; exit 1; }
  trap 'rmdir "${RUN}/attempt2.reserved" 2>/dev/null' EXIT   # released on any exit before the intent record
fi
grep -q '^  "status": "submitted"$' "${M1}" && { echo "refusing: finalize attempt 1 first"; exit 1; }
J1=$(sed -n 's/^  "job_id": "\(.*\)",$/\1/p' "${M1}")
if ! Q=$(squeue -h -j "${J1}" -o "%i %T" 2>&1); then
  # squeue errors on job ids no longer known to the controller; confirm with sacct before accepting.
  if ! sacct -j "${J1}" -X -n -P --format=State >/dev/null 2>&1; then echo "refusing: scheduler query failed: ${Q}"; exit 1; fi
  Q=""
fi
[ -z "${Q}" ] || { echo "refusing: job ${J1} still active"; exit 1; }
(cd "${SNAP}" && sha256sum -c --quiet "${RUN}/code_sha256.txt") || { echo "snapshot hash mismatch"; exit 1; }
OUT=$(sed -n 's/^  "outputs": "\(.*\)",$/\1/p' "${M1}")
CHUNK=$(sed -n 's/^  "a1_chunk": "\(.*\)",$/\1/p' "${M1}")
MAP=$(sed -n 's/^  "map": "\(.*\)",$/\1/p' "${M1}"); SCALE=$(sed -n 's/^  "scale_key": "\(.*\)",$/\1/p' "${M1}")
T1=$(sed -n 's/^  "time": "\(.*\)",$/\1/p' "${M1}"); MEM1=$(sed -n 's/^  "mem": "\([0-9]*\)G",$/\1/p' "${M1}")
ARRAY1=$(sed -n 's/^  "array": "\([^;]*\);.*$/\1/p' "${M1}")
NEXP_RUN=$(sed -n 's/^  "expected_bundles": "\(.*\)",$/\1/p' "${M1}")
[ -n "${OUT}" ] && [ -n "${CHUNK}" ] && [ -n "${MAP}" ] && [ -n "${SCALE}" ] && [ -n "${T1}" ] && [ -n "${MEM1}" ] && [ -n "${ARRAY1}" ] || { echo "incomplete run record"; exit 1; }
MISS=${RUN}/missing_before_attempt2.txt; [ "${DRY}" = --dry-run ] && MISS=$(mktemp)
RETRY=""; : > "${MISS}"
for t in $(array_tasks "${ARRAY1}"); do
  miss=0
  for id in $(task_datasets "$t" "${MAP}"); do
    for m in ${A1_METHODS}; do
      stem=$(bundle_stem "${OUT}" "$id" "$m" "${SCALE}")
      if ! valid_bundle "${stem}"; then echo "task ${t} $(basename "$(dirname "${stem}")") ${m}" >> "${MISS}"; miss=1; fi
    done
  done
  if [ "$miss" -eq 1 ]; then RETRY="${RETRY:+${RETRY},}${t}"; fi
done
NPAIRS=$(wc -l < "${MISS}")
echo "missing (case, method) pairs: ${NPAIRS}; tasks to retry: ${RETRY:-none}"
if [ -z "${RETRY}" ]; then echo "nothing to retry"; exit 0; fi
IFS=: read -r TH TM TSEC <<< "${T1}"                                   # doubled time (HH:MM:SS)
SEC2=$(( 2 * (10#$TH * 3600 + 10#$TM * 60 + 10#$TSEC) ))
T2=$(printf "%02d:%02d:%02d" $(( SEC2 / 3600 )) $(( SEC2 % 3600 / 60 )) $(( SEC2 % 60 )))
MEM2=$(( MEM1 * 2 ))G
NT=$(echo "${RETRY}" | tr ',' '\n' | wc -l)
# Authoritative values in the submitting environment (inherited values cannot override them).
export CODE_DIR=${SNAP} RUN_ID=${RUN_ID} A1_CHUNK=${CHUNK} SCALE=${SCALE}
CMD="sbatch --parsable --array=${RETRY}%133 --time=${T2} --mem=${MEM2} --output=${LOGS}/%x_%A_%a.out --export=ALL,CODE_DIR=${SNAP},RUN_ID=${RUN_ID},A1_CHUNK=${CHUNK},SCALE=${SCALE} ${SNAP}/slurm/prod_A1.sbatch"
if [ "${DRY}" = --dry-run ]; then echo "DRY RUN: would run: ${CMD}"; rm -f "${MISS}"; exit 0; fi
write_m2() {  # $1 = job id, $2 = status
  local tmp; tmp=$(mktemp "${RUN}/manifest_attempt2.json.XXXX")
  cat > "${tmp}" <<JSON
{
  "run_id": "${RUN_ID}",
  "attempt": "2",
  "reason": "infrastructure retry of ${NPAIRS} missing (case, method) pairs (list: missing_before_attempt2.txt)",
  "sbatch_command": "${CMD}",
  "array": "${RETRY}%133",
  "time": "${T2}",
  "mem": "${MEM2}",
  "expected_tasks": "${NT}",
  "expected_bundles_run": "${NEXP_RUN}",
  "host_submit": "$(hostname)",
  "job_id": "$1",
  "status": "$2"
}
JSON
  mv "${tmp}" "${M2}"
}
write_m2 "PENDING" "intent: sbatch about to run; if this status persists the submission is ambiguous (check sacct for job name A1_prod) and no further retry is allowed"
trap - EXIT                                                   # from here on the slot stays taken
JOB=$(${CMD})
write_m2 "${JOB}" "submitted"
echo "RUN_ID=${RUN_ID} retry JOB=${JOB} tasks=${RETRY} time=${T2} mem=${MEM2}"
