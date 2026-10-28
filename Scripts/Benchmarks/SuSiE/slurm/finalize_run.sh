#!/bin/bash
# Complete the record of one submission attempt after its array has ended (master §IV.3.1).
# Runs once per attempt manifest: refuses a manifest not in state "submitted", refuses while tasks
# are active or when accounting cannot be read. Status "completed" requires BOTH every allocation of
# the attempt COMPLETED (scheduler) AND every expected bundle of the RUN valid (integrity: the
# expected (case, method) set is enumerated from the run's attempt-1 manifest, array and chunk size,
# and each bundle must satisfy the bundles.sh contract; method failures are valid bundles).
# A missing results directory counts as an empty inventory (status incomplete), so retry_prod.sh can
# proceed. Semantic validation (check_dev.R, including the canaries) is a separate, mandatory step.
# Usage (login node):
#   bash slurm/finalize_run.sh <run_dir>/manifest.json            # attempt 1
#   bash slurm/finalize_run.sh <run_dir>/manifest_attempt2.json   # the retry attempt
set -eo pipefail
MAN=$1
[ -f "${MAN}" ] || { echo "usage: finalize_run.sh <manifest.json>"; exit 1; }
RUN=$(dirname "${MAN}"); TAG=$(basename "${MAN}" .json)
source "$(dirname "$0")/bundles.sh"
M1=${RUN}/manifest.json
grep -q '^  "status": "submitted"$' "${MAN}" || { echo "refusing: ${MAN} is not in state submitted"; exit 1; }
JOB=$(sed -n 's/^  "job_id": "\(.*\)",$/\1/p' "${MAN}")
[ -n "${JOB}" ] && [ "${JOB}" != PENDING ] || { echo "no job_id in manifest"; exit 1; }
OUT=$(sed -n 's/^  "outputs": "\(.*\)",$/\1/p' "${M1}")
CHUNK=$(sed -n 's/^  "a1_chunk": "\(.*\)",$/\1/p' "${M1}")
MAP=$(sed -n 's/^  "map": "\(.*\)",$/\1/p' "${M1}"); SCALE=$(sed -n 's/^  "scale_key": "\(.*\)",$/\1/p' "${M1}")
ARR1=$(sed -n 's/^  "array": "\([^;]*\);.*$/\1/p' "${M1}")
ARRM=$(sed -n 's/^  "array": "\([^;"]*\)[;"].*$/\1/p' "${MAN}")
[ -n "${OUT}" ] && [ -n "${CHUNK}" ] && [ -n "${MAP}" ] && [ -n "${SCALE}" ] && [ -n "${ARR1}" ] && [ -n "${ARRM}" ] || { echo "incomplete run record"; exit 1; }
EXPECTED=$(array_tasks "${ARRM}" | wc -l)
if ! ACC=$(sacct -j "${JOB}" -X -n -P --format=JobID,State,ExitCode,Start,End 2>&1); then echo "sacct failed: ${ACC}"; exit 1; fi
[ -n "${ACC}" ] || { echo "no accounting records for job ${JOB}"; exit 1; }
if echo "${ACC}" | awk -F'|' '$2 ~ /PENDING|RUNNING|REQUEUED|SUSPENDED|CONFIGURING|COMPLETING|RESIZING/' | grep -q .; then
  echo "tasks still active; not finalizing"; exit 1
fi
N=$(echo "${ACC}" | wc -l)
NC=$(echo "${ACC}" | awk -F'|' '$2 == "COMPLETED"' | wc -l)
# Integrity over the run's expected bundle set.
if [ -e "${OUT}" ] && [ ! -d "${OUT}" ]; then echo "results path is not a directory: ${OUT}"; exit 1; fi
[ ! -d "${OUT}" ] || [ -r "${OUT}" ] || { echo "results directory unreadable: ${OUT}"; exit 1; }
NEXP=0; VALID=0; : > "${RUN}/${TAG}_missing_bundles.txt"
for t in $(array_tasks "${ARR1}"); do
  for id in $(task_datasets "$t" "${MAP}"); do
    for m in ${A1_METHODS}; do
      NEXP=$((NEXP + 1)); stem=$(bundle_stem "${OUT}" "$id" "$m" "${SCALE}")
      if valid_bundle "${stem}"; then VALID=$((VALID + 1)); else echo "task ${t} $(basename "$(dirname "${stem}")") ${m}" >> "${RUN}/${TAG}_missing_bundles.txt"; fi
    done
  done
done
EXTRA=0
if [ -d "${OUT}" ]; then
  EXTRA=$(find "${OUT}" -name '*.done' -not -path '*quarantine*' | wc -l); EXTRA=$((EXTRA - VALID))
fi
if [ "${N}" -eq "${EXPECTED}" ] && [ "${NC}" -eq "${EXPECTED}" ] && [ "${VALID}" -eq "${NEXP}" ] && [ "${EXTRA}" -eq 0 ]; then
  STATE=completed
else
  STATE="incomplete: scheduler ${NC} of ${EXPECTED} tasks COMPLETED (${N} records); integrity ${VALID} of ${NEXP} expected bundles valid; ${EXTRA} unexpected or invalid .done"
fi
START=$(echo "${ACC}" | cut -d'|' -f4 | sort | head -1)
END=$(echo "${ACC}" | cut -d'|' -f5 | sort | tail -1)
echo "${ACC}" > "${RUN}/${TAG}_sacct_allocations.txt"
sacct -j "${JOB}" --format=JobID,State,ExitCode,Start,End,Elapsed,MaxRSS,ReqMem,Timelimit,NodeList -P > "${RUN}/${TAG}_sacct.txt" || true
if [ -d "${OUT}" ]; then
  (cd "${OUT}" && find . -type f \( -name '*.rds' -o -name '*.csv' \) -not -path '*quarantine*' | sort | xargs -r sha256sum) > "${RUN}/${TAG}_outputs_sha256.txt"
else
  : > "${RUN}/${TAG}_outputs_sha256.txt"
fi
NFILES=$(wc -l < "${RUN}/${TAG}_outputs_sha256.txt")
OSHA=$(sha256sum "${RUN}/${TAG}_outputs_sha256.txt" | cut -d' ' -f1)
TMP=$(mktemp "${RUN}/${TAG}.json.XXXX")
sed "s|^  \"status\": \"submitted\"$|  \"status\": \"${STATE}\",\n  \"start\": \"${START}\",\n  \"end\": \"${END}\",\n  \"expected_bundles\": \"${NEXP}\",\n  \"valid_bundles\": \"${VALID}\",\n  \"missing_bundles_file\": \"${TAG}_missing_bundles.txt\",\n  \"accounting_files\": \"${TAG}_sacct_allocations.txt, ${TAG}_sacct.txt\",\n  \"outputs_sha256_file\": \"${TAG}_outputs_sha256.txt (${NFILES} files)\",\n  \"outputs_sha256_tree\": \"${OSHA}\"|" "${MAN}" > "${TMP}"
grep -q '"status": "submitted"' "${TMP}" && { rm -f "${TMP}"; echo "manifest update failed"; exit 1; }
mv "${TMP}" "${MAN}"
echo "finalized ${MAN}: ${STATE}; ${NFILES} output files"
