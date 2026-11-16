#!/usr/bin/env bash
# run_tests.sh -- one-command test runner for engine_v4 (INTERFACES §1).
#   tests/run_tests.sh [--quick|--full] [--threads k] [--build-dir DIR] [--fixtures] [--allow-missing-fixtures]
# TMPDIR must be set (never /tmp; the build goes to $TMPDIR/v4_build by default). Configures and builds (nice -n 19,
# make -j3), runs v4_tests, prints machine / compiler / binary block. Exit 0 iff every test passes. --fixtures first
# regenerates tests/fixtures from core/ (needs R with Rcpp, digest, jsonlite). A missing fixture is a FAIL.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -z "${TMPDIR:-}" ]]; then echo "run_tests.sh: set TMPDIR (department tmp folder; never /tmp)" >&2; exit 2; fi
mode=quick; threads=3; build="$TMPDIR/v4_build"; fixtures=0; allow=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --quick) mode=quick ;; --full) mode=full ;;
    --threads) threads="$2"; shift ;; --build-dir) build="$2"; shift ;; --fixtures) fixtures=1 ;;
    --allow-missing-fixtures) allow=(--allow-missing-fixtures) ;;
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
"$build/smcbvs4" version --record "$build/version.json" | grep -E '"(git_commit|flags|glibc|path|sha256|fma_variant)"' || true
if [[ "$fixtures" == 1 ]]; then
  nice -n 19 Rscript "$here/tools/make_fixtures.R" "$here" "$build/smcbvs4" "$TMPDIR/v4_fixwork"
fi
args=("${allow[@]}"); [[ "$mode" == full ]] && args+=(--full)
nice -n 19 "$build/v4_tests" "${args[@]}"
