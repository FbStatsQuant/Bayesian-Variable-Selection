#!/bin/bash
# Freeze the A1 code into a read-only snapshot under $STUDY/runs/<run_id>/code/, copy the input and
# environment manifests into the run directory, write manifest.json (attempt 1), verify the snapshot
# against the source and its hash list, then submit the array from the snapshot.
# Refine tree (SuSiE-refine only, PREREG_c050 R4): one run kind per submission
# (run id <UTC>_bench20261019_<kind>_SuSiErefine):
#   prodc050 / prodc100   production map, SCALE c050 / c100, array 1-400%133 (400 tasks x 3 datasets)
#   pilotc050 / pilotc100 pilot map, SCALE c050 / c100, array 1-4 (replicate 1 of S1-S6 x p 500/1000)
# Usage (login node):
#   bash slurm/submit_prod.sh --kind KIND [--time HH:MM:SS] [--mem NG] [--dry-run]
#     --dry-run: everything except sbatch; prints the sbatch command
# Afterwards: bash slurm/finalize_run.sh --manifest <run>/manifest.json --results <results>/<run_id> --tasks N --bundles M
# One infrastructure retry of missing cases: bash slurm/retry_prod.sh <RUN_ID>
set -eo pipefail
MODE=prod; KIND=""
TIME=02:00:00     # c = 1 value (10 datasets per task); production c050 value from the pilot via --time
MEM=2G            # c = 1 value; production c050 value from the pilot via --mem
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) MODE=dry ;;
    --kind) KIND=$2; shift ;;
    --time) TIME=$2; shift ;;
    --mem) MEM=$2; shift ;;
    --array) ARRAY_OVERRIDE=$2; shift ;;
    *) echo "unknown option $1"; exit 1 ;;
  esac
  shift
done
CODE=/home/fb31/projects/BVS/Benchmarks/A1_SuSiE/c050/refine
STUDY=/projects/ml75/fb31/BVS/bench20261019
LIB=${STUDY}/lib/R452
CONC=133
case "${MEM}" in [0-9]*G) ;; *) echo "--mem must be whole GB, e.g. 2G (retry_prod.sh doubles it)"; exit 1;; esac
FILES="config.R common.R run_case.R methods/fit_A1_susie.R tests/test_A1_susie.R tests/stress_sweeps_A1.R check_dev.R score_dev.R slurm/prod_A1.sbatch slurm/submit_prod.sh slurm/retry_prod.sh slurm/finalize_run.sh slurm/bundles.sh slurm/dev_A1.sbatch slurm/test_A1.sbatch slurm/submit_dev.sh tools/compare_c050check.R tests/test_refine.R slurm/test_refine.sbatch"
module load GCC/14.3.0 >/dev/null 2>&1 || { echo "module load GCC/14.3.0 failed"; exit 1; }
module load R/4.5.2 >/dev/null 2>&1 || { echo "module load R/4.5.2 failed"; exit 1; }
RVER=$(Rscript --vanilla -e 'cat(R.version.string)' 2>/dev/null)
case "${RVER}" in "R version 4.5.2 "*) ;; *) echo "wrong R: ${RVER}"; exit 1;; esac
BLAS=$(Rscript --vanilla -e 'cat(extSoftVersion()[["BLAS"]], La_library(), sep = " | ")' 2>/dev/null)
TS=$(date -u +%Y%m%dT%H%MZ)
A1_CHUNK=3
case "${KIND}" in
  prodc050)  SCALE=c050; MAP=prod;  ARRAY="1-400%${CONC}"; NTASKS=400; NBUNDLES=1200 ;;
  prodc100)  SCALE=c100; MAP=prod;  ARRAY="1-400%${CONC}"; NTASKS=400; NBUNDLES=1200 ;;
  pilotc050) SCALE=c050; MAP=pilot; ARRAY="1-4"; NTASKS=4; NBUNDLES=12 ;;
  pilotc100) SCALE=c100; MAP=pilot; ARRAY="1-4"; NTASKS=4; NBUNDLES=12 ;;
  *) echo "--kind must be prodc050, prodc100, pilotc050 or pilotc100"; exit 1 ;;
esac
[ -z "${ARRAY_OVERRIDE:-}" ] || { ARRAY=${ARRAY_OVERRIDE}; NTASKS=$(echo "${ARRAY%%\%*}" | tr ',' '\n' | while IFS=- read -r a b; do seq "$a" "${b:-$a}"; done | wc -l); NBUNDLES=$((3 * NTASKS)); }
RUN_ID=${TS}_bench20261019_${KIND}_SuSiErefine
export A1_CHUNK SCALE      # authoritative values in the submitting environment (validated in the task)
RUN=${STUDY}/runs/${RUN_ID}
LOGS=${STUDY}/logs/prod/A1_SuSiE
mkdir -p "${STUDY}/runs" "${STUDY}/results" "${LOGS}"
mkdir "${RUN}"                                   # exclusive: fails if this run id exists
SNAP=${RUN}/code
mkdir -p "${SNAP}/methods" "${SNAP}/slurm" "${SNAP}/tests" "${SNAP}/tools" "${RUN}/manifests"   # refine tree
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
CMD="sbatch --parsable --array=${ARRAY} --time=${TIME} --mem=${MEM} --output=${LOGS}/%x_%A_%a.out --export=ALL,CODE_DIR=${SNAP},RUN_ID=${RUN_ID},A1_CHUNK=${A1_CHUNK},SCALE=${SCALE} ${SNAP}/slurm/prod_A1.sbatch"
cat > "${RUN}/manifest.json" <<JSON
{
  "run_id": "${RUN_ID}",
  "attempt": "1",
  "piece": "SuSiE-refine (A1 refine tree, PREREG_c050 R4), kind ${KIND}, scale ${SCALE}; mode ${MODE}",
  "code_sha256_file": "code_sha256.txt (per-file sha256sum of the frozen snapshot)",
  "tree_sha256": "$(sha256sum "${RUN}/code_sha256.txt" | cut -d' ' -f1)",
  "sbatch_command": "${CMD}",
  "array": "${ARRAY}; map ${MAP} (slurm/bundles.sh::task_datasets): prod = tasks 1-400 of 3 datasets, p = 500 if t <= 200 else 1000, u = (t-1) mod 200, positions 3u..3u+2 of the scenario-major order (scenario i div 100 + 1, replicate i mod 100 + 1), task 401 dev canaries at c100; pilot = tasks 1-4: p0500 S1-S3, p0500 S4-S6, p1000 S1-S3, p1000 S4-S6, replicate 1",
  "a1_chunk": "${A1_CHUNK}",
  "map": "${MAP}",
  "scale_key": "${SCALE}",
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
