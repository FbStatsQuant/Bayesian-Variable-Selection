# Sourced by the F2 job scripts: modules, threads, paths (master §III.3.0 threads; brief).
module load GCC/14.3.0 || { echo "module load GCC/14.3.0 failed"; exit 4; }
module load R/4.5.2 || { echo "module load R/4.5.2 failed"; exit 4; }
module is-loaded R/4.5.2 || { echo "R/4.5.2 not loaded"; exit 4; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export R_LIBS_USER=
STUDY=/projects/ml75/fb31/BVS/bench20261019
DEV=$STUDY/dev
OUTROOT=$STUDY/dev_test/F2_ElasticNet
