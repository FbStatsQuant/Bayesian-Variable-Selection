# Source (do not execute) at the top of every Claude NOTS job script.
# Explicit Lmod initialisation: with --export=NONE, compute nodes start without the module
# function and without /opt/apps/modules/Core on MODULEPATH (C_ops N0 jobs 2357592, 2357666).
set +u
if ! type module >/dev/null 2>&1; then
  source /etc/profile.d/modules.sh 2>/dev/null || source /usr/share/lmod/lmod/init/bash
fi
type module >/dev/null 2>&1 || { echo "FATAL: no module function after Lmod init" >&2; exit 66; }
module use /opt/apps/modules/Core
module purge
module load GCC/14.3.0 R/4.5.2
set -u
[[ $(gcc -dumpfullversion) == 14.3.0 && $(g++ -dumpfullversion) == 14.3.0 ]] || { echo "FATAL: GCC is not 14.3.0" >&2; exit 67; }
[[ $(Rscript --vanilla -e 'cat(as.character(getRversion()))') == 4.5.2 ]] || { echo "FATAL: R is not 4.5.2" >&2; exit 67; }
# One numerical thread everywhere; the module's own R library only (Rcpp 1.1.0, digest, jsonlite).
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1
export FLEXIBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MAKEFLAGS=-j1
export R_LIBS_USER=/opt/apps/software/R/4.5.2-gfbf-2025b/lib64/R/library R_LIBS_SITE=/nonexistent
unset R_LIBS R_MAKEVARS_USER R_MAKEVARS_SITE PKG_CPPFLAGS PKG_CXXFLAGS
# Fixed collation for every R process (the v2.1 source hash no longer depends on it; this is belt and braces).
export LC_ALL=C.UTF-8 LANG=C.UTF-8
# srun job steps must see this environment (sbatch --export=NONE sets SLURM_EXPORT_ENV=NONE).
export SLURM_EXPORT_ENV=ALL
