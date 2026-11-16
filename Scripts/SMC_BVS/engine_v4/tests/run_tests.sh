#!/usr/bin/env bash
# run_tests.sh -- one-command test runner for engine_v4 (INTERFACES §1).
#   tests/run_tests.sh [--quick|--full] [--threads k] [--build-dir DIR] [--fixtures]
# Configures and builds (nice -n 19, make -j3), runs v4_tests, prints machine / compiler / flags / libm. Exit 0 iff
# every test passes. --fixtures first regenerates tests/fixtures from core/ (needs R with Rcpp, digest, jsonlite).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mode=quick; threads=3; build="${TMPDIR:-$here}/v4_build"; fixtures=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --quick) mode=quick ;; --full) mode=full ;;
    --threads) threads="$2"; shift ;; --build-dir) build="$2"; shift ;; --fixtures) fixtures=1 ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac; shift
done
if [[ "$threads" -gt 3 ]]; then echo "note: Owls rule is <= 3 threads per builder" >&2; fi
export OMP_NUM_THREADS="$threads"
echo "== machine: $(hostname)  cpu: $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | sed 's/^ //')  date: $(date -Iseconds)"
echo "== compiler: $(g++ --version | head -1)   cmake: $(cmake --version | head -1)"
mkdir -p "$build"
nice -n 19 cmake -S "$here" -B "$build" -DCMAKE_BUILD_TYPE=Release > "$build/cmake.log"
nice -n 19 make -C "$build" -j3 smcbvs4 v4_tests v4_pmath_check 2>&1 | grep -E "error|warning" || true
test -x "$build/v4_tests" || { echo "build failed (see $build)"; exit 1; }
"$build/smcbvs4" version | grep -E '"(flags|glibc|libm|libm_sha256|libm_fma_variant|pmath_binding)"'
if [[ "$fixtures" == 1 ]]; then
  nice -n 19 Rscript "$here/tools/make_fixtures.R" "$here" "$build/smcbvs4" "${TMPDIR:-/tmp}/v4_fixwork"
fi
args=(); [[ "$mode" == full ]] && args+=(--full)
nice -n 19 "$build/v4_tests" "${args[@]}"
