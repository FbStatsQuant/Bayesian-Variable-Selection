#!/usr/bin/env bash
# nots_bench_island.sh -- WP3 SPR measurement (manager Q9). Self-contained: configure + build v4_bench_island, then run
# the class-A label-major island at p = 1e4 and 1e5 at 1/24/48/96 threads. Exploratory; run inside a Slurm allocation
# of one SPR node (>= 96 CPUs, >= 16 GB). Usage: tools/nots_bench_island.sh <build-dir> [threads-list]
# Each run prints: ns per elementary step (thread-time and wall), M, products, offers, phase times, peak RSS, and an
# output hash that must be the same for every thread count (T3 on SPR).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build="${1:?build dir}"; thr="${2:-1,24,48,96}"
cmake -S "$here" -B "$build" -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA=sapphirerapids > "$build.cmake.log"
make -C "$build" -j 16 v4_bench_island 2>&1 | grep -E "error|warning" || true
B="$build/v4_bench_island"
export OMP_PROC_BIND=spread OMP_PLACES=threads
lscpu | grep -E "Model name|^CPU\(s\)|Socket|NUMA node\(s\)"
# p = 1e4: N = 2500, calibrated-like adaptive grid (ESS >= 0.9 N per stage), L = 8, Hm = 4
$B island 10000 2500 "$thr" A lm 256 128 adaptive:200 8 4
# p = 1e4: the planning grid size (geometric, T = 30) for comparison with Owls
$B island 10000 2500 "$thr" A lm 256 128 geo:30 8 4
# p = 1e5: N = 2500, adaptive grid, L = 2, Hm = 2 (shorter terminal phase to bound the run)
$B island 100000 2500 "$thr" A lm 256 128 adaptive:200 2 2
