#!/bin/bash
# G3 unit tests for A1 SuSiE (master §III.3.6 i). Submit: sbatch slurm/test_A1.sbatch
#SBATCH --job-name=A1_tests
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A1_SuSiE/logs/tests_%j.out
module load GCC/14.3.0 || { echo "module load GCC/14.3.0 failed"; exit 1; }
module load R/4.5.2 || { echo "module load R/4.5.2 failed"; exit 1; }
case "$(Rscript -e 'cat(R.version.string)')" in "R version 4.5.2 "*) ;; *) echo "wrong R version"; exit 1;; esac
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
CODE=${CODE_DIR:-/home/fb31/projects/BVS/Benchmarks/A1_SuSiE}
OUT=/projects/ml75/fb31/BVS/bench20261019/dev_test/A1_SuSiE/tests/job_${SLURM_JOB_ID}
echo "host $(hostname) start $(date -u +%FT%TZ) code ${CODE}"
Rscript "${CODE}/tests/test_A1_susie.R" "${CODE}" "${OUT}"
rc=$?
echo "exit ${rc} end $(date -u +%FT%TZ)"
exit ${rc}
