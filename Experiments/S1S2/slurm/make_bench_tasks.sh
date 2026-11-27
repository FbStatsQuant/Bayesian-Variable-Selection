#!/usr/bin/env bash
# make_bench_tasks.sh -- writes the benchmark task list of one (suite, method) to stdout. OURS (operational).
#   make_bench_tasks.sh --suite 1|2 --method M [--config bench_budget.tsv]   > tasks_S<suite>_bench_<M>.tsv
# One row per array task = one (setting, block of reps). Batch plan (HQ 2026-11-26, both suites): batch 1 = reps 1-25,
# batch 2 = 26-60, batch 3 = 61-100; each batch is cut into blocks of `block` reps (bench_budget.tsv row (suite, M); the
# last block of a batch may be shorter), so no block crosses a batch boundary.
#   task_id = (cell - 1) * 100 + rep_lo    (S1: cell 1..16 = S1_01..S1_16; S2: cell 1..120 = S2_001..S2_120; the
#                                          formula of tasks_S<suite>_smcbvs.tsv, whose rows are the block-1 case; ids
#                                          are unique because rep_lo is unique per cell)
# Columns: task_id  setting_id  rep_lo  rep_hi  batch. submit_bench.sh regenerates the list and refuses a deploy whose
# tasks_S<suite>_bench_<M>.tsv differs (e.g. after a block change in bench_budget.tsv without regenerating).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
suite=""; method=""; conf=$HERE/bench_budget.tsv
while (($#)); do case "$1" in --suite) suite="$2"; shift 2;; --method) method="$2"; shift 2;; --config) conf="$2"; shift 2;;
  *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$suite" == 1 || "$suite" == 2 ]] || { echo "--suite must be 1 or 2" >&2; exit 64; }
block=$(awk -F'\t' -v s="$suite" -v m="$method" 'NR > 1 && $1 == s && $2 == m { print $3 }' "$conf")
[[ "$block" =~ ^[0-9]+$ ]] && (( block >= 1 && block <= 100 )) || { echo "no valid block for suite $suite method '$method' in $conf" >&2; exit 65; }
PLAN="1-25 26-60 61-100"
if [[ $suite == 1 ]]; then ncell=16; fmt='S1_%02d'; else ncell=120; fmt='S2_%03d'; fi
printf 'task_id\tsetting_id\trep_lo\trep_hi\tbatch\n'
for cell in $(seq 1 "$ncell"); do
  b=0
  for r in $PLAN; do
    b=$(( b + 1 )); lo=${r%-*}; hi=${r#*-}
    for (( s = lo; s <= hi; s += block )); do
      e=$(( s + block - 1 )); if (( e > hi )); then e=$hi; fi
      printf "%d\t$fmt\t%d\t%d\t%d\n" $(( (cell - 1) * 100 + s )) "$cell" "$s" "$e" "$b"
    done
  done
done
