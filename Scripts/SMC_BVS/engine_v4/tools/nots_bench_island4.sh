#!/usr/bin/env bash
# nots_bench_island4.sh -- WP3 SPR batch for the 10^6 levers (manager 11-16): per-round counters ([round] lines),
# socket-local islands, G = 256 with the --mem-budget plan, a near-stationary 10^6 island, products blocking A/B.
# Run inside ONE allocation of a full SPR node half (96 CPUs = 2 sockets x 24 cores x 2 threads, as jobs 2748104/5).
# Usage: tools/nots_bench_island4.sh <build-dir> <mode> [p]
#   mode single4    : one island, 96 threads, G = 64,  near-stationary (phi = 1, 2 burn-in + 2 measured), products block 4
#   mode single1    : the same with the original products loop (block 1)                                  [A/B of the lever]
#   mode g256       : one island, 96 threads, G = 256, near-stationary, --mem-budget 60 GB (the plan is printed)
#   mode socket     : two islands at once, one per socket, each bound close to its socket's CPUs (and its NUMA node's
#                     memory when numactl exists); X, the tiled X and the score rows are first-touched by that socket's
#                     threads. Prints each island's wall and the node total.
#   mode all        : single4, single1, g256, socket (in that order)
# ESTIMATE per mode at p = 10^6 (from job 2748105): 10-15 min wall; 'all' ~ 1 h on 96 CPUs ~ 100 core-h -- run a subset
# to stay inside the approved batch (e.g. single4 + socket + g256 ~ 75 core-h).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build="${1:?build dir}"; mode="${2:?mode}"; p="${3:-1000000}"
cmake -S "$here" -B "$build" -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA=sapphirerapids > "$build.cmake.log"
make -C "$build" -j 16 v4_bench_island 2>&1 | grep -E "error|warning" || true
B="$build/v4_bench_island"
GRID="steps:1"; L=2; HM=2          # near-stationary: one stage to phi = 1, 2 burn-in + 2 measured rounds
lscpu | grep -E "Model name|^CPU\(s\)|Socket|NUMA node\(s\)"
export V4_VERBOSE=1
run_single() {   # $1 = label, $2 = G, extra env in the caller
  echo "== $1: p=$p G=$2 threads=96 $(date +%T)"
  OMP_PROC_BIND=spread OMP_PLACES=threads OMP_NUM_THREADS=96 "$B" island "$p" 2500 96 A lm "$2" 128 "$GRID" "$L" "$HM"
}
run_socket() {
  # the CPUs of this allocation, grouped by socket (lscpu -p: CPU,Core,Socket,Node)
  allowed=$(python3 -c "import os; print(' '.join(str(c) for c in sorted(os.sched_getaffinity(0))))")
  declare -A cpus node
  while IFS=, read -r cpu core sock nd; do
    [[ "$cpu" =~ ^# ]] && continue
    for a in $allowed; do if [[ "$a" == "$cpu" ]]; then cpus[$sock]="${cpus[$sock]:-}${cpus[$sock]:+,}$cpu"; node[$sock]="$nd"; fi; done
  done < <(lscpu -p=CPU,CORE,SOCKET,NODE)
  echo "== socket-local: p=$p G=64, one island per socket $(date +%T)"
  t0=$(date +%s.%N); pids=(); id=1
  for s in "${!cpus[@]}"; do
    list="${cpus[$s]}"; nthr=$(echo "$list" | tr ',' '\n' | wc -l)
    places=$(echo "$list" | sed 's/\([0-9]\+\)/{\1}/g')
    pre=""; if command -v numactl > /dev/null; then pre="numactl --cpunodebind=${node[$s]} --membind=${node[$s]}"; fi
    echo "   island $id on socket $s (node ${node[$s]}): $nthr CPUs [$list] ${pre:-no numactl: first touch only}"
    ( export OMP_PLACES="$places" OMP_PROC_BIND=close OMP_NUM_THREADS=$nthr V4_ISLAND_ID=$id
      $pre taskset -c "$list" "$B" island "$p" 2500 "$nthr" A lm 64 128 "$GRID" "$L" "$HM" > "$build.socket$id.log" 2>&1 ) &
    pids+=($!); id=$((id + 1))
  done
  for pid in "${pids[@]}"; do wait "$pid"; done
  t1=$(date +%s.%N)
  for f in "$build".socket*.log; do echo "--- $f"; grep -E "^\s+\[round\]|wall .* s \||peak RSS|memory plan" "$f"; done
  python3 -c "print('== node total (both islands): %.1f s wall' % ($t1 - $t0))"
}
case "$mode" in
  single4) run_single "single, products block 4" 64 ;;
  single1) V4_PRODUCTS_BLOCK=1 run_single "single, products block 1 (original loop)" 64 ;;
  g256)    V4_MEM_BUDGET_GB=60 run_single "single, G = 256, mem budget 60 GB" 256 ;;
  socket)  run_socket ;;
  all)     run_single "single, products block 4" 64; V4_PRODUCTS_BLOCK=1 run_single "single, products block 1" 64
           V4_MEM_BUDGET_GB=60 run_single "single, G = 256" 256; run_socket ;;
  *) echo "unknown mode $mode" >&2; exit 2 ;;
esac
