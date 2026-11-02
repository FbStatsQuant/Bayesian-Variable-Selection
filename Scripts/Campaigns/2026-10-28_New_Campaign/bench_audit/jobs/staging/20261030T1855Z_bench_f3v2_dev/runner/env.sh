#!/usr/bin/env bash
set -euo pipefail
set +u
if ! type module >/dev/null 2>&1; then
  source /etc/profile.d/modules.sh 2>/dev/null || source /usr/share/lmod/lmod/init/bash
fi
module use /opt/apps/modules/Core
module purge
module load GCC/14.3.0 R/4.5.2
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export R_LIBS_USER=/dev/null/none R_LIBS_SITE=/nonexistent
export LC_ALL=C.UTF-8 LANG=C.UTF-8 SLURM_EXPORT_ENV=ALL
TIME_BIN=/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time
mkdir -p /scratch/fb31/New_Campaign/tmp
time_probe=$(mktemp /scratch/fb31/New_Campaign/tmp/f3_time.XXXXXX)
if ! bash "$(dirname "${BASH_SOURCE[0]}")/time_check.sh" "$TIME_BIN" "$time_probe"; then
  rm -f -- "$time_probe"
  echo "verified GNU time unavailable; refusing" >&2
  exit 68
fi
rm -f -- "$time_probe"
echo "GNU_TIME path=$TIME_BIN sha256=$(sha256sum "$TIME_BIN" | cut -d' ' -f1)"
export TIME_BIN
Rscript --vanilla -e 'p <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452"; stopifnot(dir.exists(p)); .libPaths(c(p,.Library)); stopifnot(as.character(packageVersion("glmnet")) == "5.1", startsWith(normalizePath(find.package("glmnet")),paste0(normalizePath(p),"/")), as.character(getRversion()) == "4.5.2")'
