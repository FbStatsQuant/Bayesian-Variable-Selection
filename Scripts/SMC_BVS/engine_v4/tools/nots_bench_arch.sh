#!/usr/bin/env bash
# nots_bench_arch.sh -- WP3 architect SPR measurement (branch exp/P1M-wp3-arch): the levers of WP3_ARCH_REVIEW.md on a
# late 10^6 round, A/B on the SAME rounds of the SAME island.
#
# One island is run once through its transient (pi_0 -> phi = 1 in one stage, 2 burn-in rounds) and stopped with a
# checkpoint; every variant then resumes from that checkpoint and runs the 2 measured rounds. Variants differ only in
# execution parameters (never in the law), so every variant must print the SAME output hash (checked here).
# Run inside ONE allocation of one whole socket: 96 CPUs of one socket + its memory (the H-9 island shape).
#   sbatch --nodes=1 --ntasks=1 --cpus-per-task=96 --mem=72G --time=00:45:00 --constraint=<SPR 8468> ...
# Usage: tools/nots_bench_arch.sh <build-dir> [variants]
#   variants (space separated, default "ref check bounded gram fma"):
#     ref      PR #26 head behaviour: L5, dense scoring, I1 check after every step (this build's Philox multiply included)
#     check    ref without the per-step I1 check                               (lever 1: the check)
#     bounded  check + bounded scoring, bounded scan, one-particle phase B     (lever 2; same output hash)
#     gram     bounded + Gram rows of active columns kept across passes        (lever 3; same output hash; + 5.1 GB)
#     fma      gram + FMA in the class-A tile products                         (other class-A bits: its hash differs)
#     g64      `gram` at G = 64          smt48  `gram` with 48 threads (one per core)
# Cost ESTIMATE at p = 10^6 (from job 2748756: transient 656 s, measured rounds 29-31 s each at G = 256): transient ~10 min,
# each variant ~2.5 min (data + setup 20 s, checkpoint load, 2 rounds) -> 5 variants ~ 23 min x 96 CPUs ~ 37 core-h.
# Requires TMPDIR and a build directory under the department folders (tools/nots_guard.sh); logs in <build-dir>/logs.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$here/tools/nots_guard.sh"
build="${1:?build dir}"; variants="${2:-ref check bounded gram fma}"; p="${V4_BENCH_P:-1000000}"
nots_guard "$build"
cmake -S "$here" -B "$build" -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA="${V4_ISLAND_ISA_BUILD:-sapphirerapids}" > "$LOGDIR/cmake.log"
make -C "$build" -j "${V4_MAKE_J:-16}" v4_bench_island v4_bench_arch > "$LOGDIR/make.log" 2>&1 || { tail -30 "$LOGDIR/make.log" >&2; exit 5; }
B="$build/v4_bench_island"
export V4_K_STORE="${V4_K_STORE:-8}" V4_VERBOSE=1 V4_MEM_BUDGET_GB="${V4_MEM_BUDGET_GB:-60}"
export OMP_PROC_BIND=close OMP_PLACES=threads
N="${V4_BENCH_N:-2500}"; G=256; GRID="steps:1"; L=2; HM=2; NT="${V4_BENCH_THREADS:-96}"
ck="$TMPDIR/arch_ckpt_$$"; trap 'rm -f "$ck".a "$ck".b "$ck".a.tmp.* "$ck".b.tmp.*' EXIT
lscpu | grep -E "Model name|^CPU\(s\)|Socket|NUMA node\(s\)"
pre=""; if command -v numactl > /dev/null; then pre="numactl --localalloc"; fi
echo "== transient (stage 1 + 2 burn-in rounds), stop after step 3 with a checkpoint  $(date +%T)"
V4_CKPT="$ck" V4_STOP_AFTER=3 V4_NO_CHECK_STORE=1 OMP_NUM_THREADS=$NT $pre "$B" island "$p" "$N" "$NT" A lm "$G" 128 "$GRID" "$L" "$HM" > "$LOGDIR/transient.log" 2>&1 \
  || { tail -5 "$LOGDIR/transient.log" >&2; exit 6; }
grep -E "\[round\]|\[arch\]|stopped after" "$LOGDIR/transient.log" || true
hashes=()
for v in $variants; do
  envs=(); g=$G; nt=$NT
  case "$v" in
    ref)     envs=(V4_NO_BOUNDED=1) ;;
    check)   envs=(V4_NO_BOUNDED=1 V4_NO_CHECK_STORE=1) ;;
    bounded) envs=(V4_NO_CHECK_STORE=1) ;;
    gram)    envs=(V4_NO_CHECK_STORE=1 V4_GRAM_SLOTS=640) ;;
    fma)     envs=(V4_NO_CHECK_STORE=1 V4_GRAM_SLOTS=640 V4_PRODUCTS_FMA=1) ;;
    g64)     envs=(V4_NO_CHECK_STORE=1 V4_GRAM_SLOTS=640); g=64 ;;
    smt48)   envs=(V4_NO_CHECK_STORE=1 V4_GRAM_SLOTS=640 OMP_PLACES=cores); nt=48 ;;
    *) echo "unknown variant $v" >&2; exit 2 ;;
  esac
  echo "== variant $v: G=$g threads=$nt ${envs[*]}  $(date +%T)"
  env "${envs[@]}" V4_CKPT="$ck" OMP_NUM_THREADS=$nt $pre "$B" island "$p" "$N" "$nt" A lm "$g" 128 "$GRID" "$L" "$HM" > "$LOGDIR/variant_$v.log" 2>&1 \
    || { tail -5 "$LOGDIR/variant_$v.log" >&2; exit 7; }
  grep -E "\[round\]|\[arch\]|resumed after|output hash|peak RSS" "$LOGDIR/variant_$v.log" || true
  h="$(grep -o "output hash [0-9a-f]*" "$LOGDIR/variant_$v.log" | head -1)"
  if [[ "$v" == fma ]]; then echo "   (fma: class-A bits differ by design: $h)"; else hashes+=("$h"); fi
done
# Early bridge stages (optional, V4_BENCH_EARLY=1): the first three stages of a bridge from pi_0 (phi = 0.01, 0.02, 0.03),
# where the supports are pi_0-sized and a particle takes many sweeps per round. N = G = 64 so that the Gram rows of every
# active column fit (4,000 rows = 32 GB). Reference and `gram`; the two must stop in the same state (same hash).
# ESTIMATE (Owls: 13-16 us thread-time per step for ref, 3.1-3.6 for gram): ref ~ 3 x 10 s, gram ~ 3 x 3 s of wall on
# 96 threads, plus 2 x 25 s of data and setup: ~ 2 min x 96 CPUs ~ 3 core-h.
if [[ -n "${V4_BENCH_EARLY:-}" ]]; then
  eh=()
  for v in ref gram; do
    envs=(V4_NO_CHECK_STORE=1); [[ "$v" == ref ]] && envs+=(V4_NO_BOUNDED=1); [[ "$v" == gram ]] && envs+=(V4_GRAM_SLOTS=4000)
    cke="$TMPDIR/arch_ckpt_early_$$"; rm -f "$cke".a "$cke".b
    echo "== early stages, variant $v: N=G=64 threads=$NT ${envs[*]}  $(date +%T)"
    env "${envs[@]}" V4_MEM_BUDGET_GB=0 V4_CKPT="$cke" V4_STOP_AFTER=3 OMP_NUM_THREADS=$NT $pre "$B" island "$p" 64 "$NT" A lm 64 128 steps:0.01,0.02,0.03,1 0 1 > "$LOGDIR/early_$v.log" 2>&1 \
      || { tail -5 "$LOGDIR/early_$v.log" >&2; exit 9; }
    grep -E "\[round\]|\[arch\]|output hash|peak RSS" "$LOGDIR/early_$v.log" || true
    eh+=("$(grep -o "output hash [0-9a-f]*" "$LOGDIR/early_$v.log" | head -1)"); rm -f "$cke".a "$cke".b
  done
  if [[ "${eh[0]}" != "${eh[1]}" || -z "${eh[0]}" ]]; then echo "ERROR: early-stage hashes differ or are missing: ${eh[*]}" >&2; exit 10; fi
  echo "== early stages: ${eh[0]} (identical)"
fi
uniq_h=$(printf '%s\n' "${hashes[@]}" | sort -u | wc -l)
if [[ "$uniq_h" -ne 1 || -z "${hashes[0]}" ]]; then echo "ERROR: the variants' output hashes differ or are missing: ${hashes[*]}" >&2; exit 8; fi
echo "== all variants: ${hashes[0]} (identical)"
