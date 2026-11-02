#!/bin/bash
# Production array for A3 (scale c100 only; decision D3). 120 tasks of 10 datasets of one p:
# task t = 1..60 -> p = 500, t = 61..120 -> p = 1000; within a p, u = t (or t - 60):
# scenario s = ceil(u / 10), replicates r = 10 (u - 1 - 10 (s - 1)) + 1 .. + 10.
# One R process per dataset (no state across fits); the runner skips cases with a valid
# .done + .sha256 for this case, code and inputs, so a resubmission redoes only missing cases.
# Exported by submit_prod.sh: RUN_ID, A3_CODE (frozen snapshot), A3_DATASETS (empty in
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
STUDY=/projects/ml75/fb31/BVS/bench20261019
RUN_DIR=$STUDY/runs/$RUN_ID
fatal() { echo "FATAL: $*"; exit 3; }
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
  [ "$t" -ge 1 ] && [ "$t" -le 120 ] || fatal "array task id $t outside 1-120"
  if [ "$t" -le 60 ]; then p=500; u=$t; else p=1000; u=$(( t - 60 )); fi
  s=$(( (u - 1) / 10 + 1 )); r0=$(( 10 * (u - 1 - 10 * (s - 1)) + 1 ))
  DS=(); for r in $(seq $r0 $(( r0 + 9 ))); do DS+=( "$(printf "p%04d_S%d_r%03d" $p $s $r)" ); done
fi
echo "host $(hostname)  task $t  run $RUN_ID  R $RV  datasets ${DS[*]}  start $(date -u +%FT%TZ)"
Rscript --vanilla -e 'cat("detectCores:", parallel::detectCores(), "\n")'
fail=0
for ds in "${DS[@]}"; do
  P=${ds:1:4}
  t0=$(date +%s)
  Rscript --vanilla "$A3_CODE/run_case.R" --input "$STUDY/inputs/p$P/$ds.rds" --manifest "$A3_MANIFEST" \
    --outroot "$STUDY" --run-id "$RUN_ID" --methods A3 --scales c100
  # run_case.R exits 0 (all rules ok or warning), 2 (a method failure, recorded in its rows: not
  # retried) or 1 (fatal or infrastructure: no outputs written, e.g. a hash mismatch or memory
  # exhaustion; the case stays missing for the one infrastructure resubmission).
  rc=$?; echo "dataset $ds exit $rc wall_s $(( $(date +%s) - t0 ))"; [ $rc -eq 0 ] || [ $rc -eq 2 ] || fail=1
done
echo "end $(date -u +%FT%TZ)  any_failure $fail"
exit $fail
