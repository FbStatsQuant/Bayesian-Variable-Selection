# Source (do not execute) at the top of the W3-AUDIT-C array task. Lmod init as in W3-P6 nots/env_sim.sh.
set +u
if ! type module >/dev/null 2>&1; then
  source /etc/profile.d/modules.sh 2>/dev/null || source /usr/share/lmod/lmod/init/bash
fi
type module >/dev/null 2>&1 || { echo "FATAL: no module function after Lmod init" >&2; exit 66; }
module use /opt/apps/modules/Core
module purge
module load GCC/14.3.0 SciPy-bundle/2025.07
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export LC_ALL=C.UTF-8 LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1
