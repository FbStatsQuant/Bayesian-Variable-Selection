#!/usr/bin/env bash
# Native NOTS harness. Does not call/bypass the Owls-only run_all_seeds.sh or
# run_suite.sh. Executes their unchanged prepare/worker/compare/audit components.
set -euo pipefail
[[ $# == 2 ]] || exit 64
SNAPSHOT=$(realpath "$1"); ROOT=$(realpath "$2")
[[ $(basename "$SNAPSHOT") != v1 ]] || exit 65
[[ ${SLURM_JOB_ID:-} =~ ^[0-9]+$ && ${SLURM_CPUS_PER_TASK:-} == 1 && -z ${SLURM_ARRAY_TASK_ID:-} ]] || exit 65
[[ "$SNAPSHOT" == /projects/ml75/fb31/BVS/smcbvs_v3_deploy_20261022/code/snapshots/v* ]] || exit 65
[[ "$ROOT" == /scratch/fb31/smcbvs_v3_deploy_20261022/A_build/* && -s "$ROOT/TOOLCHAIN_PASS.json" ]] || exit 65
[[ $(gcc -dumpfullversion) == 14.3.0 && $(g++ -dumpfullversion) == 14.3.0 ]] || exit 67
Rscript --vanilla -e 'stopifnot(getRversion() == "4.5.2")'
OUT="$ROOT/tests"
[[ ! -e "$OUT" ]] || { echo 'Refusing to overwrite regression evidence'; exit 66; }
mkdir "$OUT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MAKEFLAGS=-j1
export V3_TEST_COMPILE_CACHE="$OUT/shared_compile_cache"
TESTS="$SNAPSHOT/tests"
# Preserve fixed-seed mapping, including edge seeds. No arbitrary overrides.
cp "$TESTS/seeds.tsv" "$OUT/seeds.tsv"
mapfile -t indices < <(awk 'NR>1 {print $1}' "$TESTS/seeds.tsv")
[[ ${#indices[@]} == 32 ]] || exit 68
printf '%q ' "$0" "$@" > "$OUT/suite_launch_command.txt"
printf '\n' >> "$OUT/suite_launch_command.txt"
printf '%s\n' "$$" > "$OUT/suite_pid.txt"
date -u +%FT%TZ > "$OUT/suite_started_utc.txt"
failed=0
for index in "${indices[@]}"; do
  [[ "$index" =~ ^[0-9]+$ ]] || exit 68
  out="$OUT/seed_$index"
  python3 -B "$TESTS/prepare.py" prepare "$out" --prototype "$SNAPSHOT/reference/prototype_core" \
    --production "$SNAPSHOT/code/core" --tests "$TESTS" --index "$index"
  frozen="$out/sources/tests"
  # Generated manifest is mutable evidence, never frozen source. Correct the
  # inherited prepare.py execution label and attach actual Slurm provenance.
  python3 -B - "$out" "$SLURM_JOB_ID" <<'PY'
import json, pathlib, sys
r=pathlib.Path(sys.argv[1]); p=r/'manifest.json'; m=json.loads(p.read_text())
m.update(execution='NOTS Slurm sequential prototype regression; unchanged R workers',
         slurm_job_id=sys.argv[2], legacy_worker_metadata_execution_label='Owls (historical literal, not actual host)')
p.write_text(json.dumps(m, indent=2)+'\n')
PY
  mkdir "$out/prototype" "$out/production"
  date -u +%FT%TZ > "$out/started_utc.txt"
  printf '%q ' Rscript --vanilla "$frozen/worker.R" "$out/sources/prototype" prototype "$out/prototype" "$index" "$frozen" > "$out/launch_command.txt"
  printf '\n' >> "$out/launch_command.txt"
  printf '%q ' Rscript --vanilla "$frozen/worker.R" "$out/sources/production" production "$out/production" "$index" "$frozen" >> "$out/launch_command.txt"
  printf '\n' >> "$out/launch_command.txt"
  printf '%q ' Rscript --vanilla "$frozen/compare.R" "$out" "$frozen" >> "$out/launch_command.txt"
  printf '\n' >> "$out/launch_command.txt"
  set +e
  Rscript --vanilla "$frozen/worker.R" "$out/sources/prototype" prototype "$out/prototype" "$index" "$frozen" > "$out/prototype/worker.log" 2>&1
  ref_rc=$?
  Rscript --vanilla "$frozen/worker.R" "$out/sources/production" production "$out/production" "$index" "$frozen" > "$out/production/worker.log" 2>&1
  prod_rc=$?
  Rscript --vanilla "$frozen/compare.R" "$out" "$frozen" > "$out/compare.log" 2>&1
  compare_rc=$?
  printf 'prototype\t%s\nproduction\t%s\ncomparison\t%s\n' "$ref_rc" "$prod_rc" "$compare_rc" > "$out/exit_status.tsv"
  date -u +%FT%TZ > "$out/finished_utc.txt"
  python3 -B "$frozen/prepare.py" finish "$out" > "$out/audit.log" 2>&1
  audit_rc=$?
  set -e
  if (( ref_rc || prod_rc || compare_rc || audit_rc )); then
    failed=1
    echo "FAIL seed-index=$index; stopping for inspection"
    break
  fi
done
joined=$(IFS=,; echo "${indices[*]}")
if ! python3 -B "$TESTS/summarize.py" "$OUT" --indices "$joined" > "$OUT/summary.log" 2>&1; then failed=1; fi
date -u +%FT%TZ > "$OUT/suite_finished_utc.txt"
printf '%s\n' "$failed" > "$OUT/suite_exit_status.txt"
exit "$failed"
