# env.sh: common environment for F5 jobs (sourced by the job scripts).
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
module purge >/dev/null 2>&1
module load GCC/14.3.0 >/dev/null 2>&1
module load R/4.5.2 >/dev/null 2>&1
export R_LIBS_USER=
export F5_CODE=/home/fb31/projects/BVS/Benchmarks/F5_ABESS
export F5_OUT=/projects/ml75/fb31/BVS/bench20261019/dev_test/F5_ABESS
export DEV_ROOT=/projects/ml75/fb31/BVS/bench20261019/dev
