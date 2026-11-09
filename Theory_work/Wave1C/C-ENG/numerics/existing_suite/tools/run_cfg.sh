#!/usr/bin/env bash
# usage: run_cfg.sh PRODUCTION_CORE NEW_OUTPUT_DIR INDEX  -- manual port of run_suite.sh (no hostname/nice checks, python for python3)
set -uo pipefail
SP="C:/Users/felip/AppData/Local/Temp/claude/7f4deb75538d3cf7/03611146-335e-4730-9f01-d3ebd88e845b/scratchpad/suite"
WT="C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-68de3711"
tests="$WT/Scripts/SMC_BVS/tests"; proto="$WT/Scripts/SMC_BVS/reference/prototype_core"
prod=$1; out_arg=$2; index=$3
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MAKEFLAGS=-j1
export V3_TEST_COMPILE_CACHE="C:/Users/felip/AppData/Local/Temp/v3c"
python "$SP/prep_wrap.py" "$tests/prepare.py" prepare "$out_arg" --prototype "$proto" --production "$prod" --tests "$tests" --index "$index" || exit 1
out=$(cd -- "$out_arg" && pwd); frozen="$out/sources/tests"
printf '%q ' "$0" "$@" > "$out/launch_command.txt"; printf '\n' >> "$out/launch_command.txt"
date -u +%FT%TZ > "$out/started_utc.txt"; printf '%s\n' "$$" > "$out/runner_pid.txt"
mkdir -p "$out/prototype" "$out/production"
# prototype and production workers are independent (different compile keys); run them as 2 concurrent R processes
Rscript --vanilla "$frozen/worker.R" "$out/sources/prototype" prototype "$out/prototype" "$index" "$frozen" > "$out/prototype/worker.log" 2>&1 &
p1=$!
Rscript --vanilla "$frozen/worker.R" "$out/sources/production" production "$out/production" "$index" "$frozen" > "$out/production/worker.log" 2>&1 &
p2=$!
wait $p1; ref_rc=$?; wait $p2; prod_rc=$?
Rscript --vanilla "$frozen/compare.R" "$out" "$frozen" > "$out/compare.log" 2>&1; compare_rc=$?
printf 'prototype\t%s\nproduction\t%s\ncomparison\t%s\n' "$ref_rc" "$prod_rc" "$compare_rc" > "$out/exit_status.tsv"
date -u +%FT%TZ > "$out/finished_utc.txt"
python "$SP/prep_wrap.py" "$frozen/prepare.py" finish "$out" > "$out/audit.log" 2>&1; audit_rc=$?
echo "rc proto=$ref_rc prod=$prod_rc compare=$compare_rc audit=$audit_rc"
