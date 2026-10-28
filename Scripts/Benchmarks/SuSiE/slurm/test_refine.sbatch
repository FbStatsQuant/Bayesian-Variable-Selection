#!/bin/bash
# Unit tests of SuSiE-refine (tests/test_refine.R, PREREG_c050 R4) run from the frozen snapshot of a
# refine-tree run, on synthetic fixtures and the 12 dev datasets (inputs only) at c100 and c050.
# Submit (login node), after a refine pilot has been frozen:
#   sbatch --parsable --export=ALL,CODE_DIR=$STUDY/runs/<RUN_ID>/code,RUN_ID=<RUN_ID> <CODE_DIR>/slurm/test_refine.sbatch
# Writes $STUDY/results/<RUN_ID>/tests_refine/{test_results.csv,refine_cases.csv}.
#SBATCH --job-name=A1_refine_tests
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=03:00:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/logs/prod/A1_SuSiE/%x_%j.out
module load GCC/14.3.0 || { echo "module load GCC/14.3.0 failed"; exit 1; }
module load R/4.5.2 || { echo "module load R/4.5.2 failed"; exit 1; }
case "$(Rscript --vanilla -e 'cat(R.version.string)')" in "R version 4.5.2 "*) ;; *) echo "wrong R version"; exit 1;; esac
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1 LC_ALL=C
: "${CODE_DIR:?CODE_DIR not set}" "${RUN_ID:?RUN_ID not set}"
STUDY=/projects/ml75/fb31/BVS/bench20261019
case "${RUN_ID}" in *_SuSiErefine) ;; *) echo "not a refine-tree run: ${RUN_ID}"; exit 1 ;; esac
[ "${CODE_DIR}" = "${STUDY}/runs/${RUN_ID}/code" ] || { echo "CODE_DIR is not the snapshot of ${RUN_ID}"; exit 1; }
(cd "${CODE_DIR}" && sha256sum --quiet -c "${STUDY}/runs/${RUN_ID}/code_sha256.txt") || { echo "snapshot hash mismatch"; exit 1; }
OUT=${STUDY}/results/${RUN_ID}/tests_refine
echo "host $(hostname) start $(date -u +%FT%TZ) code ${CODE_DIR} out ${OUT}"
Rscript --vanilla "${CODE_DIR}/tests/test_refine.R" "${CODE_DIR}" "${OUT}" "${STUDY}/dev/inputs"
rc=$?
echo "exit ${rc} end $(date -u +%FT%TZ)"
exit ${rc}
