# Common environment for A3 jobs (master §III.3.0 Threads; brief: R module lines).
# A failed module load returns non-zero to the sourcing job script, which stops.
module load GCC/14.3.0 || return 1
module load R/4.5.2 || return 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export R_LIBS_USER="" R_LIBS=""
export STUDY=/projects/ml75/fb31/BVS/bench20261019
export A3_OUT=$STUDY/dev_test/A3_Horseshoe
