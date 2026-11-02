#!/bin/bash
# Freeze the A1 code into a read-only snapshot under $STUDY/runs/<run_id>/code/, copy the input and
# environment manifests into the run directory, write manifest.json (attempt 1), verify the snapshot
# against the source and its hash list, then submit the array from the snapshot.
# Usage (login node):
#   bash slurm/submit_prod.sh --dry-run   # everything except sbatch; prints the sbatch command
#   bash slurm/submit_prod.sh --smoke     # tasks 91 (p1000_S4_r001 only, A1_CHUNK=1) and 121 (canaries)
#   bash slurm/submit_prod.sh             # full array: 120 production tasks + canary task 121
# Afterwards: bash slurm/finalize_run.sh --manifest <run>/manifest.json --results <results>/<run_id> --tasks N --bundles M
# One infrastructure retry of missing cases: bash slurm/retry_prod.sh <RUN_ID>
set -eo pipefail
MODE=prod
case "${1:-}" in --dry-run) MODE=dry;; --smoke) MODE=smoke;; "") ;; *) echo "unknown option $1"; exit 1;; esac
CODE=/home/fb31/projects/BVS/Benchmarks/A1_SuSiE
STUDY=/projects/ml75/fb31/BVS/bench20261019
LIB=${STUDY}/lib/R452
TIME=02:00:00     # see README: 3 x dev p95 rule gives 30 min; raised to cover slow (non-converging) fits
MEM=2G            # 2 x dev max MaxRSS (322 MB) = 0.65 GB -> 2 GB minimum
CONC=60
FILES="config.R common.R run_case.R methods/fit_A1_susie.R tests/test_A1_susie.R tests/stress_sweeps_A1.R check_dev.R score_dev.R slurm/prod_A1.sbatch slurm/submit_prod.sh slurm/retry_prod.sh slurm/finalize_run.sh slurm/bundles.sh slurm/dev_A1.sbatch slurm/test_A1.sbatch slurm/submit_dev.sh"
module load GCC/14.3.0 >/dev/null 2>&1 || { echo "module load GCC/14.3.0 failed"; exit 1; }
module load R/4.5.2 >/dev/null 2>&1 || { echo "module load R/4.5.2 failed"; exit 1; }
RVER=$(Rscript --vanilla -e 'cat(R.version.string)' 2>/dev/null)
case "${RVER}" in "R version 4.5.2 "*) ;; *) echo "wrong R: ${RVER}"; exit 1;; esac
BLAS=$(Rscript --vanilla -e 'cat(extSoftVersion()[["BLAS"]], La_library(), sep = " | ")' 2>/dev/null)
TS=$(date -u +%Y%m%dT%H%MZ)
if [ "${MODE}" = smoke ]; then
  RUN_ID=${TS}_bench20261019_prodsmoke_A1_SuSiE; ARRAY="91,121"; A1_CHUNK=1; NTASKS=2; NBUNDLES=8
else
  RUN_ID=${TS}_bench20261019_prod_A1_SuSiE; ARRAY="1-121%${CONC}"; A1_CHUNK=10; NTASKS=121; NBUNDLES=2406
fi
export A1_CHUNK            # authoritative values in the submitting environment (validated in the task)
RUN=${STUDY}/runs/${RUN_ID}
LOGS=${STUDY}/logs/prod/A1_SuSiE
mkdir -p "${STUDY}/runs" "${STUDY}/results" "${LOGS}"
mkdir "${RUN}"                                   # exclusive: fails if this run id exists
SNAP=${RUN}/code
mkdir -p "${SNAP}/methods" "${SNAP}/slurm" "${SNAP}/tests" "${RUN}/manifests"
for f in ${FILES}; do cp "${CODE}/${f}" "${SNAP}/${f}"; done
(cd "${SNAP}" && sha256sum ${FILES}) > "${RUN}/code_sha256.txt"
chmod -R a-w "${SNAP}"
cp ${STUDY}/manifests/cells/*_inputs.csv ${STUDY}/dev/manifests/dev_inputs_manifest.csv \
   ${STUDY}/lib/environment_manifest.txt "${RUN}/manifests/"
(cd "${RUN}/manifests" && sha256sum *) > "${RUN}/manifests_sha256.txt"
chmod -R a-w "${RUN}/manifests"
# Environment baseline: every fit of this run must see exactly this fingerprint (run_case.R --env_baseline).
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1 LC_ALL=C Rscript --vanilla -e "
  e <- new.env(); sys.source('${SNAP}/run_case.R', envir = e)
  .libPaths(c('${LIB}', .Library)); loadNamespace('susieR'); loadNamespace('digest')
  saveRDS(e\$env_fingerprint('${LIB}'), '${RUN}/env_fingerprint.rds'); print(readRDS('${RUN}/env_fingerprint.rds'))"
chmod a-w "${RUN}/env_fingerprint.rds"
CMD="sbatch --parsable --array=${ARRAY} --time=${TIME} --mem=${MEM} --output=${LOGS}/%x_%A_%a.out --export=ALL,CODE_DIR=${SNAP},RUN_ID=${RUN_ID},A1_CHUNK=${A1_CHUNK} ${SNAP}/slurm/prod_A1.sbatch"
cat > "${RUN}/manifest.json" <<JSON
{
  "run_id": "${RUN_ID}",
  "attempt": "1",
  "piece": "A1 SuSiE + SuSiE-L100 production, scale c100 (D3); mode ${MODE}",
  "code_sha256_file": "code_sha256.txt (per-file sha256sum of the frozen snapshot)",
  "tree_sha256": "$(sha256sum "${RUN}/code_sha256.txt" | cut -d' ' -f1)",
  "sbatch_command": "${CMD}",
  "array": "${ARRAY}; tasks 1-120: p = 500 if t <= 60 else 1000, u = (t-1) mod 60, scenario = floor(u/10)+1, replicates 10*(u mod 10)+1 to +A1_CHUNK; task 121: dev canaries dev_p0500_S4_r001, dev_p1000_S2_r001, dev_p1000_S6_r001",
  "a1_chunk": "${A1_CHUNK}",
  "time": "${TIME}",
  "mem": "${MEM}",
  "expected_tasks": "${NTASKS}",
  "expected_bundles": "${NBUNDLES}",
  "host_submit": "$(hostname)",
  "job_id": "PENDING",
  "seeds": "method_seed = data_seed + 4000000 (data_seed = 1410000/1510000 + 10000 s + r); asserted per dataset by run_case.R",
  "modules": "GCC/14.3.0 R/4.5.2; Rscript --vanilla; LC_ALL=C; thread variables 1",
  "r_version": "${RVER}",
  "blas": "${BLAS}",
  "library": "${LIB}",
  "manifests_copy": "manifests/ (cell input manifests, dev input manifest, environment_manifest.txt); hashes in manifests_sha256.txt",
  "environment_manifest_sha256": "$(sha256sum ${STUDY}/lib/environment_manifest.txt | cut -d' ' -f1)",
  "environment_baseline": "env_fingerprint.rds (R, environment_manifest.txt hash, susieR, BLAS); required by every fit",
  "inputs": "${STUDY}/inputs/{p0500,p1000} (canaries: ${STUDY}/dev/inputs)",
  "outputs": "${STUDY}/results/${RUN_ID}",
  "logs": "${LOGS}",
  "status": "submitted"
}
JSON
export CODE_DIR=${SNAP} RUN_ID=${RUN_ID}
# Refuse to submit unless the frozen snapshot, the source and the manifest copies match their hash lists.
(cd "${RUN}/manifests" && sha256sum -c --quiet "${RUN}/manifests_sha256.txt") || { echo "manifest copy mismatch; not submitting"; exit 1; }
(cd "${SNAP}" && sha256sum -c --quiet "${RUN}/code_sha256.txt") || { echo "snapshot hash mismatch; not submitting"; exit 1; }
(cd "${CODE}" && sha256sum -c --quiet "${RUN}/code_sha256.txt") || { echo "source differs from snapshot; not submitting"; exit 1; }
if [ "${MODE}" = dry ]; then
  sed -i 's/^  "status": "submitted"$/  "status": "dry-run (not submitted)"/' "${RUN}/manifest.json"
  echo "DRY RUN: RUN_ID=${RUN_ID}"; echo "would run: ${CMD}"; exit 0
fi
JOB=$(${CMD})
sed -i "s/^  \"job_id\": \"PENDING\",$/  \"job_id\": \"${JOB}\",/" "${RUN}/manifest.json"
echo "RUN_ID=${RUN_ID} JOB=${JOB}"
