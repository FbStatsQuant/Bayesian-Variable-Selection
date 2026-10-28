#!/bin/bash
# Freeze the code into a read-only snapshot (created exclusively), verify it, write manifest.json,
# then submit the dev array from the snapshot (policy §8, master §IV.3.1).
# Usage (login node): bash slurm/submit_dev.sh
# The dev runs of 2026-10-19 were finalized with the dev version of finalize_run.sh (see their run
# records); the current slurm/finalize_run.sh reads production manifests (submit_prod.sh) only.
set -eo pipefail
CODE=/home/fb31/projects/BVS/Benchmarks/A1_SuSiE
BASE=/projects/ml75/fb31/BVS/bench20261019/dev_test/A1_SuSiE
FILES="config.R common.R run_case.R methods/fit_A1_susie.R tests/test_A1_susie.R check_dev.R score_dev.R slurm/dev_A1.sbatch slurm/test_A1.sbatch slurm/submit_dev.sh slurm/finalize_run.sh"
module load GCC/14.3.0 >/dev/null 2>&1 || { echo "module load GCC/14.3.0 failed"; exit 1; }
module load R/4.5.2 >/dev/null 2>&1 || { echo "module load R/4.5.2 failed"; exit 1; }
RVER=$(Rscript -e 'cat(R.version.string)' 2>/dev/null)
case "${RVER}" in "R version 4.5.2 "*) ;; *) echo "wrong R: ${RVER}"; exit 1;; esac
RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)_bench20261019_devA1
RUN=${BASE}/runs/${RUN_ID}
mkdir -p "${BASE}/runs" "${BASE}/logs" "${BASE}/results"
mkdir "${RUN}"                                   # fails if the run directory already exists
SNAP=${RUN}/code
mkdir -p "${SNAP}/methods" "${SNAP}/slurm" "${SNAP}/tests"
for f in ${FILES}; do cp "${CODE}/${f}" "${SNAP}/${f}"; done
(cd "${SNAP}" && sha256sum ${FILES}) > "${RUN}/code_sha256.txt"
chmod -R a-w "${SNAP}"
(cd "${SNAP}" && sha256sum -c --quiet "${RUN}/code_sha256.txt")   # verify the frozen copy
(cd "${CODE}" && sha256sum -c --quiet "${RUN}/code_sha256.txt")   # and that it equals the source
BLAS=$(Rscript -e 'cat(extSoftVersion()[["BLAS"]], La_library(), sep = " | ")' 2>/dev/null)
INMAN=/projects/ml75/fb31/BVS/bench20261019/dev/manifests/dev_inputs_manifest.csv
CMD="sbatch --parsable --export=ALL,CODE_DIR=${SNAP},RUN_ID=${RUN_ID} ${SNAP}/slurm/dev_A1.sbatch"
JOB=$(${CMD})
cat > "${RUN}/manifest.json" <<JSON
{
  "run_id": "${RUN_ID}",
  "piece": "A1 SuSiE dev test (12 dev datasets x {A1, SuSiE-L100} x c100)",
  "code_sha256_file": "code_sha256.txt (per-file sha256sum of the frozen snapshot)",
  "tree_sha256": "$(sha256sum "${RUN}/code_sha256.txt" | cut -d' ' -f1)",
  "sbatch_command": "${CMD}",
  "host_submit": "$(hostname)",
  "job_id": "${JOB}",
  "seeds": "method_seed = data_seed + 4000000 (6420001..6470001 p500, 6520001..6570001 p1000)",
  "modules": "GCC/14.3.0 R/4.5.2",
  "r_version": "${RVER}",
  "blas": "${BLAS}",
  "package_manifest_sha256": "$(sha256sum /projects/ml75/fb31/BVS/bench20261019/lib/environment_manifest.txt | cut -d' ' -f1)",
  "inputs": "/projects/ml75/fb31/BVS/bench20261019/dev/inputs/{p0500,p1000}",
  "inputs_manifest_sha256": "$(sha256sum ${INMAN} | cut -d' ' -f1)",
  "outputs": "${BASE}/results/${RUN_ID}",
  "status": "submitted"
}
JSON
echo "RUN_ID=${RUN_ID} JOB=${JOB}"
