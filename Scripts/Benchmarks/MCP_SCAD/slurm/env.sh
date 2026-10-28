# Common job environment for F4 (master §III.3.0 "Threads", "Library"; runtime stack GCC/14.3.0 + R/4.5.2).
# Sourced by the job scripts; returns non-zero (and the caller stops) if any module step fails.
module purge                || { echo "FATAL: module purge failed"; return 1; }
module load GCC/14.3.0      || { echo "FATAL: module load GCC/14.3.0 failed"; return 1; }
module load R/4.5.2         || { echo "FATAL: module load R/4.5.2 failed"; return 1; }
command -v Rscript >/dev/null || { echo "FATAL: Rscript not on PATH"; return 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export R_LIBS_USER= R_LIBS=
export STUDY=/projects/ml75/fb31/BVS/bench20261019
export F4_OUT=$STUDY/dev_test/F4_MCP_SCAD
export STUDY_DEV=$STUDY/dev
