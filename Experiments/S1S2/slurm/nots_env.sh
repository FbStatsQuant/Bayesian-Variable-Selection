# nots_env.sh -- NOTS environment for the S1/S2 SMC-BVS run. Installed by deploy_to_nots.sh as
#   /home/fb31/SMC-BVS/_local/engineering/envs/S1S2/env.sh
# and sourced by s1_smcbvs_array.sbatch, check_batch.sh and the toy fit. OURS (operational).
# R 4.5.2 / GCC 14.3.0 = the NOTS toolchain named in the engine README ("NOTS GCC14.3.0/R4.5.2 build").
# No private R library: Rcpp 1.1.0, digest 0.6.37 and jsonlite 2.0.0 ship with the R/4.5.2 module (extensions).
# ~/.Rprofile on NOTS prepends ~/R/library (another project's Rcpp etc.), so the user profile, user Renviron and user
# library are switched off here: the run sees ONLY the module's library.
# Lmod returns non-zero internally; run it with errexit/nounset/pipefail off and restore the caller's options.
__s1_flags=$-; __s1_pf=$(shopt -po pipefail || true); set +e +u +o pipefail
type module >/dev/null 2>&1 || source /etc/profile.d/modules.sh
module purge
module load GCC/14.3.0
module load R/4.5.2
[[ $__s1_flags == *e* ]] && set -e; [[ $__s1_flags == *u* ]] && set -u; eval "$__s1_pf"; unset __s1_flags __s1_pf
command -v Rscript >/dev/null && [[ $(g++ -dumpfullversion) == 14.3.0 ]] || { echo "FATAL: env.sh: GCC 14.3.0 / R 4.5.2 not loaded" >&2; return 66 2>/dev/null || exit 66; }
export R_PROFILE_USER=/dev/null R_ENVIRON_USER=/dev/null R_LIBS_USER=/dev/null R_LIBS=
# single-threaded numerics (the engine is serial; R's BLAS here is FlexiBLAS -> OpenBLAS)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 \
       VECLIB_MAXIMUM_THREADS=1 MC_CORES=1 R_PARALLEL_CORES=1
