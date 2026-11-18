#!/usr/bin/env bash
# run_tests.sh -- one-command test runner for engine_v4 (INTERFACES §1; TESTING.md).
#   tests/run_tests.sh [--quick|--full] [--threads k] [--build-dir DIR] [--fixtures] [--allow-missing-fixtures] [--keep]
#                      [--allow-skip] [--only SUITE[,SUITE]] [--list]
# TMPDIR must be set (never /tmp; the build goes to $TMPDIR/v4_build by default). Configures and builds (nice -n 19,
# make -j3), runs the suites (--list names them), prints machine / compiler / binary block and ends with ONE summary line:
# PASS / FAIL / SKIPPED per suite with its time. --fixtures first regenerates tests/fixtures from core/ (needs R with Rcpp,
# digest, jsonlite). A missing fixture is a FAIL.
# Exit status: 0 every suite that was asked for ran and passed; 1 a suite FAILED (or the build failed); 2 bad usage / TMPDIR
# unset; 3 nothing failed but a suite was SKIPPED (R or python3 missing) -- pass --allow-skip to accept that (e.g. a machine
# without R); the SKIPPED suite is still named in the summary.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mode=quick; threads=3; build=""; fixtures=0; allow=(); keep=(); allow_skip=0; list=0; only=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --quick) mode=quick ;; --full) mode=full ;;
    --threads) threads="$2"; shift ;; --build-dir) build="$2"; shift ;; --fixtures) fixtures=1 ;;
    --allow-missing-fixtures) allow=(--allow-missing-fixtures) ;;
    --keep) keep=(--keep) ;;   # keep the WP4 golden work dir ($TMPDIR/wp4_golden) for debugging
    --allow-skip) allow_skip=1 ;;
    --only) only="$2"; shift ;;   # these suites only (the build always runs): cpp,driver,competitors,install,golden
    --list) list=1 ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac; shift
done
if [[ $list == 1 ]]; then
  cat <<'EOF'
suites, in the order they run (details, timings and what PASS means: TESTING.md):
  build        cmake + make: smcbvs4, v4_tests, v4_pmath_check                       needs GCC >= 11, CMake >= 3.20, OpenMP, libquadmath
  cpp          v4_tests: unit, golden-vs-core and end-to-end C++ test cases           (--full adds the tagged "full" cases)
  driver       tools/slurm/test_p1m_driver.py: the SLURM plan driver and its tools     needs python3 (stdlib only)
  competitors  tools/competitors/test_competitors.sh: the competitor harness           needs R
  install      tools/competitors/test_install_script.sh: install-script guards         needs R
  golden       tests/golden/wp4_golden.R: WP4 calibration / merge / paths vs core/     needs R with Rcpp, digest, jsonlite
options: --quick (default) | --full, --threads k (default 3; Owls rule: at most 3), --build-dir DIR, --fixtures,
         --allow-missing-fixtures, --keep, --allow-skip (a SKIPPED suite does not fail the run), --only a,b (these suites
         only; the build always runs), --list
EOF
  exit 0
fi
for o in ${only//,/ }; do
  case "$o" in cpp|driver|competitors|install|golden) ;; *) echo "run_tests.sh: unknown suite '$o' for --only (see --list)" >&2; exit 2 ;; esac
done
want() { [[ -z "$only" || ",$only," == *",$1,"* ]]; }
if [[ -z "${TMPDIR:-}" ]]; then echo "run_tests.sh: set TMPDIR (department tmp folder; never /tmp)" >&2; exit 2; fi
[[ -n "$build" ]] || build="$TMPDIR/v4_build"
if [[ "$threads" -gt 3 ]]; then echo "note: Owls rule is <= 3 threads per builder" >&2; fi
export OMP_NUM_THREADS="$threads"

declare -A RES SECS DET
ORDER=()
record() { ORDER+=("$1"); RES[$1]=$2; SECS[$1]=$3; DET[$1]=${4:-}; }
summary_and_exit() {   # one table, then one line; exit status as documented at the top
  local rc=0 skipped=0 failed=0 total=0 line="" s
  echo; echo "== suite summary ($mode, $threads threads)"
  for s in "${ORDER[@]}"; do
    printf '  %-12s %-8s %6d s  %s\n' "$s" "${RES[$s]}" "${SECS[$s]}" "${DET[$s]}"
    total=$((total + SECS[$s])); line+="${RES[$s]} $s ${SECS[$s]}s | "
    if [[ ${RES[$s]} == FAIL ]]; then failed=$((failed + 1)); fi
    if [[ ${RES[$s]} == SKIPPED ]]; then skipped=$((skipped + 1)); fi
  done
  if (( failed )); then rc=1; elif (( skipped && ! allow_skip )); then rc=3; fi
  if (( rc == 3 )); then echo "  a suite was SKIPPED (R or python3 missing): the run is not a full pass; install them or pass --allow-skip"; fi
  echo "SUMMARY: ${line}total ${total}s | exit $rc"
  exit $rc
}
# The trap: a build directory left by ANOTHER checkout makes CMake stop with "does not match the source". Say so, once, clearly.
stale_dir() {   # stale_dir DIR -> prints the offending CMakeCache and returns 0 if DIR was configured for another source tree
  local f home
  f=$(find "$1" -maxdepth 4 -name CMakeCache.txt 2>/dev/null | head -1) || true
  [[ -n "$f" ]] || return 1
  home=$(sed -n 's/^CMAKE_HOME_DIRECTORY:INTERNAL=//p' "$f" | head -1)
  [[ -n "$home" ]] || return 1
  [[ "$(realpath -m "$home")" == "$(realpath -m "$here")" ]] && return 1
  echo "$f (configured for $home)"; return 0
}

echo "== machine: $(hostname)  cpu: $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | sed 's/^ //')  date: $(date -Iseconds)"
echo "== compiler: $(g++ --version | head -1)   cmake: $(cmake --version | head -1)"
mkdir -p "$build"

# ---- suite: build
t0=$SECONDS
if bad=$(stale_dir "$build"); then
  echo "build directory $build was configured for another checkout: $bad"
  echo "  remove it or choose another --build-dir / TMPDIR (TESTING.md, 'the stale TMPDIR trap')"
  record build FAIL $((SECONDS - t0)) "stale build directory"; summary_and_exit
fi
nice -n 19 cmake -S "$here" -B "$build" -DCMAKE_BUILD_TYPE=Release > "$build/cmake.log"
nice -n 19 make -C "$build" -j3 smcbvs4 v4_tests v4_pmath_check 2>&1 | grep -E "error|warning" || true
if [[ ! -x "$build/v4_tests" ]]; then
  echo "build failed (see $build)"; record build FAIL $((SECONDS - t0)) "see $build/cmake.log and the make output"; summary_and_exit
fi
record build PASS $((SECONDS - t0)) "$build"
"$build/smcbvs4" version --record "$build/version.json" | grep -E '"(git_commit|flags|glibc|path|sha256|fma_variant)"' || true
if [[ "$fixtures" == 1 ]]; then
  nice -n 19 Rscript "$here/tools/make_fixtures.R" "$here" "$build/smcbvs4" "$TMPDIR/v4_fixwork"
fi
if [[ "$fixtures" == 1 ]]; then   # WP2: core/'s Rcpp dup components, cut group and cpp_setup -> tests/fixtures/setup_wp2
  nice -n 19 Rscript "$here/tools/golden_setup_ref.R" "$here/../core" "$here/tests/fixtures/setup_wp2" "$TMPDIR/v4_fixwork_wp2"
fi

# ---- suite: cpp (v4_tests)
if want cpp; then
  args=("${allow[@]}"); [[ "$mode" == full ]] && args+=(--full)
  t0=$SECONDS
  if nice -n 19 "$build/v4_tests" "${args[@]}" 2>&1 | tee "$build/v4_tests.log"; then r=PASS; else r=FAIL; fi
  record cpp $r $((SECONDS - t0)) "$(grep -E '^[0-9]+ test cases' "$build/v4_tests.log" | tail -1)"
fi

# ---- suite: driver (WP5 extras: dry-run Slurm driver, Python stdlib)
if want driver; then
  t0=$SECONDS
  if command -v python3 > /dev/null; then
    if TMPDIR="${TMPDIR:-$build}" nice -n 19 python3 "$here/tools/slurm/test_p1m_driver.py" > "$build/wp5_driver_tests.log" 2>&1; then
      echo "WP5 Slurm-driver tests: OK ($(grep -E '^Ran' "$build/wp5_driver_tests.log"))"; r=PASS
    else echo "WP5 Slurm-driver tests: FAILED ($build/wp5_driver_tests.log)"; r=FAIL; fi
    record driver $r $((SECONDS - t0)) "$(grep -E '^Ran' "$build/wp5_driver_tests.log" | tail -1)"
  else
    echo "python3 not found: WP5 driver tests NOT RUN"; record driver SKIPPED 0 "python3 not found"
  fi
fi

# ---- suites: competitors, install (R)
if want competitors || want install; then
  if command -v Rscript > /dev/null; then
    if want competitors; then
      t0=$SECONDS
      if TMPDIR="${TMPDIR:-$build}" "$here/tools/competitors/test_competitors.sh" "$build" > "$build/wp5_competitors.log" 2>&1; then
        echo "WP5 competitor harness: OK ($(grep 'packages missing' "$build/wp5_competitors.log" | sed 's/^ *//'))"; r=PASS
      else echo "WP5 competitor harness: FAILED ($build/wp5_competitors.log)"; r=FAIL; fi
      record competitors $r $((SECONDS - t0)) "$(grep 'packages missing' "$build/wp5_competitors.log" | sed 's/^ *//' | head -1)"
    fi
    if want install; then   # install script guards + offline route on dummy packages (PR #19 MINOR-1..3; no network, nothing outside TMPDIR)
      t0=$SECONDS
      if TMPDIR="${TMPDIR:-$build}" nice -n 19 "$here/tools/competitors/test_install_script.sh" > "$build/wp5_install.log" 2>&1; then
        echo "WP5 install script: OK ($(grep -c '^  ok ' "$build/wp5_install.log") checks; $(tail -1 "$build/wp5_install.log"))"; r=PASS
      else echo "WP5 install script: FAILED ($build/wp5_install.log)"; r=FAIL; fi
      note=""; if grep -q "skip install tests" "$build/wp5_install.log"; then note=" (PARTIAL: TMPDIR is not inside the department folder, the install part was skipped)"; fi
      record install $r $((SECONDS - t0)) "$(grep -c '^  ok ' "$build/wp5_install.log") checks$note"
    fi
  else
    echo "R not found: WP5 competitor harness and install-script tests NOT RUN"
    if want competitors; then record competitors SKIPPED 0 "R not found"; fi
    if want install; then record install SKIPPED 0 "R not found"; fi
  fi
fi

# ---- suite: golden (WP4 bit tests against core/: calibration coded rule, T9 merge, T10 paths; needs R with Rcpp)
if want golden; then
  t0=$SECONDS
  if command -v Rscript > /dev/null; then
    if bad=$(stale_dir "${TMPDIR}/wp4_golden"); then
      echo "golden work directory ${TMPDIR}/wp4_golden was configured for another checkout: $bad"
      echo "  remove it or use a fresh TMPDIR (TESTING.md, 'the stale TMPDIR trap')"
      record golden FAIL $((SECONDS - t0)) "stale ${TMPDIR}/wp4_golden"
    else
      if nice -n 19 Rscript "$here/tests/golden/wp4_golden.R" "$here/../core" "$here" "${TMPDIR:-$build}/wp4_golden" "$mode" "$threads" "${keep[@]}" 2>&1 | tee "$build/wp4_golden.log"; then r=PASS; else r=FAIL; fi
      if [[ ${#keep[@]} -eq 0 ]]; then rm -rf "${TMPDIR:-$build}/wp4_golden"; fi   # clean-tmp rule (also after a failure)
      record golden $r $((SECONDS - t0)) "$(grep -E '^WP4 golden:' "$build/wp4_golden.log" | tail -1)"
    fi
  else
    echo "R not found: WP4 golden tests NOT RUN"; record golden SKIPPED 0 "R not found"
  fi
fi
summary_and_exit
