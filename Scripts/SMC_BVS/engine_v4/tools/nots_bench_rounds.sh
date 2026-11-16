#!/usr/bin/env bash
# nots_bench_rounds.sh -- WP3 SPR measurement of a FIXED NUMBER OF ROUNDS at p = 1e5 and 1e6 (manager, after job 2747881).
# Two islands per p: (a) transient: 3 bridge stages (phi = 0.3, 0.7, 1) + 1 measured round; (b) near-stationary: one
# stage to phi = 1 + 3 burn-in + 1 measured round. [island] lines on stderr give each step's wall time (+dt).
# Each island:
# class A, label-major, tile 128; G = 256 at 1e5, G = 64 at 1e6 (memory, manager Q3). One process per p builds the data
# once and runs the island once per thread count (same output hash required: T3 on SPR).
# Usage: tools/nots_bench_rounds.sh <build-dir> [threads, default 24,48,96] [p list, default 100000,1000000]
# ESTIMATE (Owls p = 1e5, N = 500: 107 s at 3 threads for (a)): 1e5 ~ 2-4 min in total; 1e6 ~ 20-40 min in total
# (store compactions in the first rounds are serial: see WP3 report), peak RSS ~ 12-15 GB.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build="${1:?build dir}"; thr="${2:-24,48,96}"; plist="${3:-100000,1000000}"
cmake -S "$here" -B "$build" -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA=sapphirerapids > "$build.cmake.log"
make -C "$build" -j 16 v4_bench_island 2>&1 | grep -E "error|warning" || true
B="$build/v4_bench_island"
export OMP_PROC_BIND=spread OMP_PLACES=threads
lscpu | grep -E "Model name|^CPU\(s\)|Socket|NUMA node\(s\)"
for p in ${plist//,/ }; do
  G=256; [[ "$p" -ge 1000000 ]] && G=64
  echo "== p=$p G=$G transient: 3 bridge stages (phi 0.3, 0.7, 1) + 1 measured round $(date +%T)"
  V4_VERBOSE=1 $B island "$p" 2500 "$thr" A lm "$G" 128 steps:0.3,0.7,1 0 1
  echo "== p=$p G=$G near-stationary: 1 bridge stage (phi 1) + 3 burn-in + 1 measured round; read the last rounds from the [island] lines $(date +%T)"
  V4_VERBOSE=1 $B island "$p" 2500 "$thr" A lm "$G" 128 steps:1 3 1
done
# optional NUMA check (one socket): OMP_PROC_BIND=close OMP_PLACES=cores $B island 1000000 2500 24 A lm 64 128 steps:0.3,0.7,1 0 1
