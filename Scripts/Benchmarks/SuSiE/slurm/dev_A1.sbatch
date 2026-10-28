#!/bin/bash
# Dev test of A1 SuSiE and SuSiE-L100 on the 12 dev datasets (dev replicate 1), scale c100 only.
# Task t = 1..12: p = 500 for t <= 6 else 1000; scenario s = (t - 1) %% 6 + 1.
# Submitted by slurm/submit_dev.sh, which sets CODE_DIR (frozen snapshot) and RUN_ID.
#SBATCH --job-name=A1_dev
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=01:00:00
#SBATCH --array=1-12
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A1_SuSiE/logs/dev_%A_%a.out
module load GCC/14.3.0 || { echo "module load GCC/14.3.0 failed"; exit 1; }
module load R/4.5.2 || { echo "module load R/4.5.2 failed"; exit 1; }
case "$(Rscript -e 'cat(R.version.string)')" in "R version 4.5.2 "*) ;; *) echo "wrong R version"; exit 1;; esac
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
: "${CODE_DIR:?CODE_DIR not set}" "${RUN_ID:?RUN_ID not set}"
t=${SLURM_ARRAY_TASK_ID}
if [ "$t" -le 6 ]; then p=500; else p=1000; fi
s=$(( (t - 1) % 6 + 1 ))
pp=$(printf "p%04d" "$p")
IN=/projects/ml75/fb31/BVS/bench20261019/dev/inputs/${pp}/dev_${pp}_S${s}_r001.rds
OUTROOT=/projects/ml75/fb31/BVS/bench20261019/dev_test/A1_SuSiE/results
echo "host $(hostname) task ${t} input ${IN} start $(date -u +%FT%TZ)"
Rscript "${CODE_DIR}/run_case.R" --code_dir="${CODE_DIR}" --input="${IN}" \
  --out_root="${OUTROOT}" --run_id="${RUN_ID}" --methods=A1,SuSiE-L100 --scales=c100
rc=$?
echo "exit ${rc} end $(date -u +%FT%TZ)"
exit ${rc}
