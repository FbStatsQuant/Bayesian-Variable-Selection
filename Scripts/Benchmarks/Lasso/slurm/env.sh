# env.sh -- common environment for F1 jobs (sourced by the job scripts). Paths per BRIEF_F1_Lasso.md.
# Module or R-version problems abort the job (exit 4) instead of running in an unintended environment.
export STUDY=/projects/ml75/fb31/BVS/bench20261019
export BENCH_LIB=$STUDY/lib/R452
export F1_CODE=/home/fb31/projects/BVS/Benchmarks/F1_Lasso
export F1_OUT=$STUDY/dev_test/F1_Lasso
export DEV_INPUTS=$STUDY/dev/inputs
export DEV_MANIFEST=$STUDY/dev/manifests/dev_inputs_manifest.csv
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export R_LIBS_USER=/dev/null/none   # keep $HOME/R/library off the path; the study library is set in R
module purge >/dev/null 2>&1 || true
module load GCC/14.3.0 >/dev/null 2>&1 || { echo "module load GCC/14.3.0 failed" >&2; exit 4; }
module load R/4.5.2 >/dev/null 2>&1 || { echo "module load R/4.5.2 failed" >&2; exit 4; }
Rscript --version 2>&1 | grep -q "version 4.5.2" || { echo "Rscript is not R 4.5.2: $(command -v Rscript)" >&2; exit 4; }
