# nots_env_bench.sh -- NOTS environment for the S1/S2 BENCHMARK methods (lasso_cv, scad, bas_mc3, susie, asi).
# Installed by deploy_to_nots.sh as /home/fb31/SMC-BVS/_local/engineering/envs/S1S2/env_bench.sh. OURS (operational).
# = env.sh (R 4.5.2 / GCC 14.3.0 modules, user profile/library off, single-threaded numerics)
#   + R_LIBS = envs/S1S2/Rlib_bench: glmnet 5.2, ncvreg 3.16.0, BAS 2.1.0, susieR 0.14.2 (+ RhpcBLASctl and every
#     non-base dependency) at the versions of the Owls smoke; pinned in Rlib_bench/VERSIONS.tsv (CRAN url + sha256);
#     compiled on a Cascade Lake node (R's Makeconf is -march=native) so it also runs on Sapphire Rapids
#   + GNU Octave 10.3.0 (conda-forge octave-10.3.0-pl5321hd0fbda6_4, OpenBLAS 0.3.34), the Owls env re-created from its
#     md5-pinned lock (envs/octave_lock/explicit_linux-64.txt, micromamba 2.10.0). Prefix on /scratch because the env
#     (1.8 GB) does not fit the 10 GB home quota; scratch purges files after 14 days without access, so rebuild with
#     envs/octave_lock/build_octave.sbatch if the check below fails.
#   + the authors' ASI Version3.0 folder (ASI_sampler.m sha256-checked by fit_asi.R before every run).
# Fails loudly (exit/return 67) if a package, octave-cli or ASI_sampler.m is missing.
__eb_dir=/home/fb31/SMC-BVS/_local/engineering/envs
source "$__eb_dir/S1S2/env.sh" || { echo "FATAL: env_bench.sh: env.sh failed" >&2; return 66 2>/dev/null || exit 66; }
export R_LIBS="$__eb_dir/S1S2/Rlib_bench"
export S1S2_ASI_OCTAVE_HOME=${S1S2_ASI_OCTAVE_HOME:-/scratch/fb31/SMC-BVS/envs/octave}
# the conda build carries a placeholder prefix: octave-cli finds its own m-files only with OCTAVE_HOME (fit_asi.R also
# passes it to the Octave call)
export OCTAVE_HOME=$S1S2_ASI_OCTAVE_HOME
export S1S2_ASI_SAMPLER_DIR=${S1S2_ASI_SAMPLER_DIR:-/home/fb31/SMC-BVS/_local/engineering/ext/griffin_asi_original/Version3.0}
# temporary root of the ASI Octave exchange files: the job's TMPDIR (node-local) if Slurm set one, else scratch tmp
export S1S2_ASI_TMP=${S1S2_ASI_TMP:-${TMPDIR:-/scratch/fb31/SMC-BVS/tmp}}
# single-threaded numerics, also for Octave's OpenBLAS (pthreads build) and GOTO-style variables
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 \
       GOTO_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MC_CORES=1 R_PARALLEL_CORES=1
__eb_fail=
for __eb_p in glmnet ncvreg BAS susieR; do
  [[ -f "$R_LIBS/$__eb_p/DESCRIPTION" ]] || __eb_fail+=" R:$__eb_p"
done
[[ -x "$S1S2_ASI_OCTAVE_HOME/bin/octave-cli" ]] || __eb_fail+=" octave-cli($S1S2_ASI_OCTAVE_HOME)"
[[ -f "$S1S2_ASI_SAMPLER_DIR/ASI_sampler.m" ]] || __eb_fail+=" ASI_sampler.m($S1S2_ASI_SAMPLER_DIR)"
[[ -d "$S1S2_ASI_TMP" && -w "$S1S2_ASI_TMP" ]] || __eb_fail+=" S1S2_ASI_TMP($S1S2_ASI_TMP)"
if [[ -n $__eb_fail ]]; then
  echo "FATAL: env_bench.sh: missing:$__eb_fail" >&2; unset __eb_dir __eb_p __eb_fail; return 67 2>/dev/null || exit 67
fi
unset __eb_dir __eb_p __eb_fail
