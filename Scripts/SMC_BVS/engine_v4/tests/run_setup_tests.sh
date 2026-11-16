#!/usr/bin/env bash
# run_setup_tests.sh -- WP2 one-command test runner (folded into tests/run_tests.sh at integration with WP1).
#   tests/run_setup_tests.sh [--quick|--full] [--threads k]
# configure + build (make -j3, nice -n 19) + run the unit, T11, invariance and golden (vs core/) tests. Exit 0 iff all pass.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ENGINE="$(dirname "$HERE")"
LEVEL=--quick; THREADS=3
while [ $# -gt 0 ]; do case "$1" in --quick|--full) LEVEL=$1;; --threads) THREADS=$2; shift;; esac; shift; done
: "${TMPDIR:=$ENGINE/build-setup/tmp}"; export TMPDIR; mkdir -p "$TMPDIR"
BUILD="${V4_SETUP_BUILD:-$TMPDIR/build-setup}"
echo "machine: $(hostname) | $(uname -r) | $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2)"
echo "compiler: $(g++ --version | head -1)"
echo "flags: -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2 (bit library and golden reference)"
LIBM=$(ldd "$(command -v true)" | awk '/libm\.so/{print $3}'); [ -z "$LIBM" ] && LIBM=$(ls /lib64/libm.so.6 2>/dev/null || true)
[ -n "$LIBM" ] && echo "libm: $LIBM sha256 $(sha256sum "$(readlink -f "$LIBM")" | cut -c1-16)"
nice -n 19 cmake -S "$ENGINE/src/setup" -B "$BUILD" -DCMAKE_BUILD_TYPE=Release > "$BUILD.cmake.log" 2>&1 || { cat "$BUILD.cmake.log"; exit 1; }
nice -n 19 make -C "$BUILD" -j3 v4_setup_tests v4_setup_bench 2>&1 | grep -E "error|warning" || true
OMP_NUM_THREADS=$THREADS nice -n 19 "$BUILD/v4_setup_tests" $LEVEL --threads "$THREADS"
