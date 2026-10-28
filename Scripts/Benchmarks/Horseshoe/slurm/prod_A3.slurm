#!/bin/bash
# Longer-chain sensitivity array for A3 (longchain copy; PREREG_c050 R6): list mode, ONE fit per task.
# Run kinds (from RUN_ID): longc050 (A3_SCALE=c050) and longc100 (A3_SCALE=c100). Task t fits dataset
# line t of the frozen case list A3_CASES (the ess_tau-flagged production fits of that scale), with the
# 8 x budget of config.R, then writes a comparison with the production fit of the same case
# (A3_PROD_RUN) to results/<RUN_ID>/longchain_compare/<case_id>.csv (tools/longchain_compare.R).
# One R process per dataset (no state across fits); the runner skips cases with a valid
# .done + .sha256 for this case, code and inputs, so a resubmission redoes only missing cases.
# Exported by submit_prod.sh: RUN_ID, A3_CODE (frozen snapshot), A3_SCALE, A3_CASES, A3_CASES_SHA256,
# A3_PROD_RUN, A3_DATASETS (empty in
# production; one dataset id for the smoke test), A3_MANIFEST and A3_MANIFEST_SHA256 (the inputs
# manifest frozen with the run), A3_LIBMAN_SHA256 (hash of the sealed library's manifest).
#SBATCH --job-name=A3_prod
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/logs/prod/A3_Horseshoe/%x_%A_%a.out
set -uo pipefail
: "${RUN_ID:?}" "${A3_CODE:?}" "${A3_MANIFEST:?}" "${A3_MANIFEST_SHA256:?}" "${A3_LIBMAN_SHA256:?}"
A3_DATASETS=${A3_DATASETS:-}
A3_SCALE=${A3_SCALE:-c100}
STUDY=/projects/ml75/fb31/BVS/bench20261019
RUN_DIR=$STUDY/runs/$RUN_ID
fatal() { echo "FATAL: $*"; exit 3; }
case "$RUN_ID" in
  *_bench20261019_longc050_A3_Horseshoe) MAP=list; WANT=c050 ;;
  *_bench20261019_longc100_A3_Horseshoe) MAP=list; WANT=c100 ;;
  *) fatal "unexpected RUN_ID $RUN_ID" ;;
esac
: "${A3_CASES:?}" "${A3_CASES_SHA256:?}" "${A3_PROD_RUN:?}"
[ "$(sha256sum "$A3_CASES" | cut -d' ' -f1)" = "$A3_CASES_SHA256" ] || fatal "frozen case list changed"
[ -d "$STUDY/results/$A3_PROD_RUN" ] || fatal "production run $A3_PROD_RUN not found"
[ "$A3_SCALE" = "$WANT" ] || fatal "run $RUN_ID requires A3_SCALE=$WANT (got $A3_SCALE)"
# Preflight: the snapshot, the frozen inputs manifest and the library manifest are as recorded.
( cd "$A3_CODE" && sha256sum --quiet -c "$RUN_DIR/code_sha256.txt" ) || fatal "snapshot hashes do not match $RUN_DIR/code_sha256.txt"
[ "$(sha256sum "$A3_MANIFEST" | cut -d' ' -f1)" = "$A3_MANIFEST_SHA256" ] || fatal "frozen inputs manifest changed"
[ "$(sha256sum "$STUDY/lib/environment_manifest.txt" | cut -d' ' -f1)" = "$A3_LIBMAN_SHA256" ] || fatal "library manifest changed"
source "$A3_CODE/slurm/env.sh" || fatal "environment setup failed"
RV=$(Rscript --vanilla -e 'cat(R.version$major, R.version$minor, sep = ".")') || fatal "Rscript does not start"
[ "$RV" = "4.5.2" ] || fatal "R version $RV, expected 4.5.2"
t=$SLURM_ARRAY_TASK_ID
if [ -n "$A3_DATASETS" ]; then
  IFS=, read -ra DS <<< "$A3_DATASETS"
else
  N=$(grep -c . "$A3_CASES")
  [ "$t" -ge 1 ] && [ "$t" -le "$N" ] || fatal "array task id $t outside 1-$N (case list)"
  ID=$(sed -n "${t}p" "$A3_CASES")
  [[ "$ID" =~ ^p(0500|1000)_S[1-6]_r[0-9]{3}$ ]] || fatal "bad case id '$ID' on line $t"
  DS=( "$ID" )
fi
echo "host $(hostname)  task $t  run $RUN_ID  R $RV  scale $A3_SCALE  map $MAP  datasets ${DS[*]}  start $(date -u +%FT%TZ)"
Rscript --vanilla -e 'cat("detectCores:", parallel::detectCores(), "\n")'
fail=0
for ds in "${DS[@]}"; do
  P=${ds:1:4}
  t0=$(date +%s)
  Rscript --vanilla "$A3_CODE/run_case.R" --input "$STUDY/inputs/p$P/$ds.rds" --manifest "$A3_MANIFEST" \
    --outroot "$STUDY" --run-id "$RUN_ID" --methods A3 --scales "$A3_SCALE"
  # run_case.R exits 0 (all rules ok or warning), 2 (a method failure, recorded in its rows: not
  # retried) or 1 (fatal or infrastructure: no outputs written, e.g. a hash mismatch or memory
  # exhaustion; the case stays missing for the one infrastructure resubmission).
  rc=$?; echo "dataset $ds exit $rc wall_s $(( $(date +%s) - t0 ))"; [ $rc -eq 0 ] || [ $rc -eq 2 ] || fail=1
  if [ $rc -eq 0 ] || [ $rc -eq 2 ]; then
    CID=${ds}_$A3_SCALE
    Rscript --vanilla "$A3_CODE/tools/longchain_compare.R" "$STUDY/results/$RUN_ID/p$P/$CID/A3.rds" \
      "$STUDY/results/$A3_PROD_RUN/p$P/$CID/A3.rds" "$STUDY/results/$RUN_ID/longchain_compare/$CID.csv" || fail=1
  fi
done
echo "end $(date -u +%FT%TZ)  any_failure $fail"
exit $fail
