#!/usr/bin/env bash
# Root launches this on Owls; no SSH or scheduler operation is performed here.
set -euo pipefail
if [[ $# -lt 3 || $# -gt 4 ]]; then
  echo 'usage: run_suite.sh PROTOTYPE_CORE PRODUCTION_CORE NEW_OUTPUT_DIR [fixed-seed-index]' >&2
  exit 64
fi
tests=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
index=${4:-1}
# Root is the sole execution funnel. Owls only, nice19, one R process at a time.
case $(hostname -f) in owls|owls.*) ;; *) echo 'Execution destination must be Owls (AMENDMENT 1).' >&2; exit 65;; esac
if [[ $(ps -o ni= -p $$ | tr -d ' ') != 19 ]]; then exec nice -n 19 bash "$0" "$@"; fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MAKEFLAGS=-j1
export V3_TEST_COMPILE_CACHE=${V3_TEST_COMPILE_CACHE:-"$(dirname -- "$3")/shared_compile_cache"}
python3 "$tests/prepare.py" prepare "$3" --prototype "$1" --production "$2" --tests "$tests" --index "$index"
out=$(cd -- "$3" && pwd)
frozen="$out/sources/tests"
printf '%q ' "$0" "$@" > "$out/launch_command.txt"
printf '\n' >> "$out/launch_command.txt"
date -u +%FT%TZ > "$out/started_utc.txt"
printf '%s\n' "$$" > "$out/runner_pid.txt"
set +e
mkdir -p "$out/prototype" "$out/production"
Rscript --vanilla "$frozen/worker.R" "$out/sources/prototype" prototype "$out/prototype" "$index" "$frozen" > "$out/prototype/worker.log" 2>&1
ref_rc=$?
Rscript --vanilla "$frozen/worker.R" "$out/sources/production" production "$out/production" "$index" "$frozen" > "$out/production/worker.log" 2>&1
prod_rc=$?
Rscript --vanilla "$frozen/compare.R" "$out" "$frozen" > "$out/compare.log" 2>&1
compare_rc=$?
printf 'prototype\t%s\nproduction\t%s\ncomparison\t%s\n' "$ref_rc" "$prod_rc" "$compare_rc" > "$out/exit_status.tsv"
date -u +%FT%TZ > "$out/finished_utc.txt"
python3 "$frozen/prepare.py" finish "$out" > "$out/audit.log" 2>&1
audit_rc=$?
set -e
if (( ref_rc || prod_rc || compare_rc || audit_rc )); then
  echo "FAIL seed-index=$index; inspect $out/REPORT.md, worker logs and source_validation.json" >&2
  exit 1
fi
echo "PASS seed-index=$index evidence=$out"
