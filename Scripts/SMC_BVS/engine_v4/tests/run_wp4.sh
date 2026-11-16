#!/usr/bin/env bash
# run_wp4.sh -- WP4 tests: C++ unit tests (no R) and, if R is present, the golden bit tests against core/.
#   tests/run_wp4.sh [--quick|--full] [--threads k]
# Owls discipline: nice -n 19, <= 3 threads; TMPDIR must be set by the caller (department tmp folder).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; eng="$(cd "$here/.." && pwd)"; core="$(cd "$eng/../core" && pwd)"
level=quick; threads=3
while [ $# -gt 0 ]; do case "$1" in --quick) level=quick;; --full) level=full;; --threads) threads="$2"; shift;; esac; shift; done
: "${TMPDIR:?set TMPDIR to the department tmp folder}"
work="$TMPDIR/wp4_tests"; mkdir -p "$work"
export OMP_NUM_THREADS="$threads" OPENBLAS_NUM_THREADS=1
echo "machine: $(hostname)  compiler: $(g++ --version | head -1)  date: $(date -Is)"
FLAGS="-std=c++20 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2 -fopenmp"
echo "flags: $FLAGS"
nice -n 19 g++ $FLAGS -Wall -Wno-misleading-indentation -I "$eng/include" "$here/test_wp4.cpp" -o "$work/test_wp4"
nice -n 19 "$work/test_wp4"
if command -v Rscript >/dev/null 2>&1; then
  nice -n 19 Rscript "$here/golden/wp4_golden.R" "$core" "$eng" "$work/golden" "$level" "$threads"
else
  echo "R not found: golden tests NOT RUN"
fi
