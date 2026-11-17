#!/usr/bin/env bash
# nots_bench_k1.sh -- WP6 K1 (bounded scoring) on SPR: late 10^6 rounds before / after, resumed from ONE checkpoint.
# One island (p = 1e6, N = 2500, G = 256, class A, label-major, tile 128, stand-in data of bench_island) runs
# pi_0 -> phi = 1 in one stage + 2 burn-in rounds and checkpoints after step 3; then rounds 4-5 (2 measured rounds)
# are resumed twice per variant, alternating: dense (V4_NO_BOUNDED=1, the merged behaviour) and bounded (K1).
# The I1 store check is off in every variant (V4_NO_CHECK_STORE; since O1 it runs only before checkpoints and the
# final write, the same in both variants). Exit 3 unless all variants print one output hash.
# Read the [round] / [arch] lines of steps 4 and 5 in $LOGDIR/<variant>.err.
# Usage: tools/nots_bench_k1.sh <build-dir> [threads, default 96]
# Dry run elsewhere (Owls): V4_BENCH_P=20000 V4_BENCH_N=300 V4_BENCH_ISA=x86-64-v4 V4_MAKE_J=3 nice -n 19 ... <build> 3
# ESTIMATE: build 3 min, transient ~11 min, 4 resumes x ~2.5 min: ~25 min wall on one socket (96 CPUs) = ~40 core-h.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$here/tools/nots_guard.sh"
build="${1:?build dir}"; thr="${2:-96}"
p="${V4_BENCH_P:-1000000}"; N="${V4_BENCH_N:-2500}"; isa="${V4_BENCH_ISA:-sapphirerapids}"
nots_guard "$build"
cmake -S "$here" -B "$build" -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA="$isa" > "$LOGDIR/cmake.log"
# build: fail hard (review PR48 MINOR-3: a masked failure would benchmark a stale executable); log kept, binary identity recorded
B="$build/v4_bench_island"; rm -f "$B"; t0=$(date +%s)
if ! make -C "$build" -j "${V4_MAKE_J:-16}" v4_bench_island > "$LOGDIR/build.log" 2>&1; then
  grep -E "error" "$LOGDIR/build.log" | head -20 >&2; echo "build FAILED ($LOGDIR/build.log)" >&2; exit 4
fi
if [[ ! -x "$B" || $(stat -c %Y "$B") -lt $t0 ]]; then echo "no fresh $B after the build" >&2; exit 4; fi
echo "== binary $(sha256sum "$B" | cut -c1-16) built from $(git -C "$here" rev-parse --short HEAD 2>/dev/null || echo '?')$(git -C "$here" diff --quiet 2>/dev/null || echo ' (+ local changes)')"
export OMP_PROC_BIND=close OMP_PLACES=threads OMP_NUM_THREADS="$thr"
export V4_K_STORE="${V4_K_STORE:-8}" V4_VERBOSE=1 V4_NO_CHECK_STORE=1 V4_CKPT="$TMPDIR/k1_ckpt"
ARGS=(island "$p" "$N" "$thr" A lm 256 128 steps:1 2 2)
lscpu | grep -E "Model name|^CPU\(s\)|Socket|NUMA node\(s\)"
rm -f "$V4_CKPT".a "$V4_CKPT".b
echo "== transient: phi = 1 in one stage + 2 burn-in rounds, checkpoint after step 3 $(date +%T)"
V4_STOP_AFTER=3 "$B" "${ARGS[@]}" > "$LOGDIR/transient.out" 2> "$LOGDIR/transient.err" || [[ $? -eq 21 ]]   # 21 = interrupted after checkpoint
for v in dense bounded dense2 bounded2; do
  echo "== $v: rounds 4-5 from the checkpoint $(date +%T)"
  if [[ $v == dense* ]]; then V4_NO_BOUNDED=1 "$B" "${ARGS[@]}" > "$LOGDIR/$v.out" 2> "$LOGDIR/$v.err"; else "$B" "${ARGS[@]}" > "$LOGDIR/$v.out" 2> "$LOGDIR/$v.err"; fi
  grep -E "\[round\] step [45]|\[arch\] step [45]" "$LOGDIR/$v.err" || true
  grep -E "output hash" "$LOGDIR/$v.out"
done
rm -f "$V4_CKPT".a "$V4_CKPT".b
n=$(grep -ho "output hash [0-9a-f]*" "$LOGDIR"/{dense,bounded,dense2,bounded2}.out | sort -u | wc -l)
if [[ "$n" -ne 1 ]]; then echo "OUTPUT HASHES DIFFER across variants" >&2; exit 3; fi
echo "== same output hash in all variants $(date +%T)"
