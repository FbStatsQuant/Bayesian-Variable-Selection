#!/usr/bin/env bash
# build.sh -- build g0_bench. P1M gate G0, Part K.
# Usage: build.sh nots OUTDIR   (on a NOTS Sapphire Rapids compute node, inside the job: GCC 14.3.0 module, -march=sapphirerapids)
#        build.sh owls OUTDIR   (Owls dry run: system gcc, -march=native)
# Flags as in the feasibility benchmark (README of /home/fb31/p1m_feas_bench), only -march differs:
#   -O3 -ffp-contract=off (no FMA contraction: the bit form must equal v3::Scorer) -fno-math-errno -fopenmp -std=c++17,
#   linked with libmvec (_ZGVeN8v_log/_exp, glibc) and libm.
# Writes OUTDIR/g0_bench and OUTDIR/build_info.txt (compiler, flags, source and binary sha256).
set -euo pipefail
WHERE=${1:?nots|owls}; OUT=${2:?OUTDIR}
SRC=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
mkdir -p "$OUT"
if [[ $WHERE == nots ]]; then
  set +u
  if ! type module >/dev/null 2>&1; then source /etc/profile.d/modules.sh 2>/dev/null || source /usr/share/lmod/lmod/init/bash; fi
  type module >/dev/null 2>&1 || { echo "FATAL: no module function after Lmod init" >&2; exit 66; }
  module use /opt/apps/modules/Core
  module purge
  module load GCC/14.3.0
  set -u
  [[ $(g++ -dumpfullversion) == 14.3.0 ]] || { echo "FATAL: g++ is not 14.3.0" >&2; exit 67; }
  MARCH=-march=sapphirerapids
elif [[ $WHERE == owls ]]; then
  MARCH=-march=native
else
  echo "first argument must be nots or owls" >&2; exit 64
fi
grep -q avx512f /proc/cpuinfo || { echo "FATAL: this CPU has no AVX-512 (the kernels need it)" >&2; exit 68; }
FLAGS="-O3 $MARCH -ffp-contract=off -fno-math-errno -fopenmp -std=c++17"
t0=$(date +%s)
g++ $FLAGS -o "$OUT/g0_bench" "$SRC/g0_bench.cpp" -lmvec -lm
{
  echo "built $(date -u +%FT%TZ) on $(hostname -s) in $(( $(date +%s) - t0 )) s"
  echo "compiler: $(command -v g++) $(g++ -dumpfullversion)"
  echo "flags: $FLAGS ... -lmvec -lm"
  echo "glibc: $(ldd --version | head -1)"
  ( cd "$SRC" && sha256sum g0_bench.cpp core_copy/v3_score.h core_copy/v3_util.h )
  sha256sum "$OUT/g0_bench"
} | tee "$OUT/build_info.txt"
