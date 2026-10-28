#!/usr/bin/env bash
# AMENDMENT 1: root launches one persistent Owls process, no NOTS/Slurm.
set -euo pipefail
if [[ $# -lt 3 || $# -gt 4 ]]; then
  echo 'usage: run_all_seeds.sh FROZEN_PROTOTYPE_CORE FROZEN_PRODUCTION_CORE NEW_EVIDENCE_ROOT [comma-separated-indices]' >&2
  exit 64
fi
case $(hostname -f) in owls|owls.*) ;; *) echo 'Owls only.' >&2; exit 65;; esac
if [[ $(ps -o ni= -p $$ | tr -d ' ') != 19 ]]; then exec nice -n 19 bash "$0" "$@"; fi
tests=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
out=$3
if [[ -e $out ]]; then echo "Refusing to overwrite suite evidence: $out" >&2; exit 66; fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MAKEFLAGS=-j1
# Check shared-machine capacity before the batch, and between seeds. A single
# root-owned sequential job uses <=1 busy R/compiler core (<=4 allowed for A).
wait_for_capacity() {
  while true; do
    load=$(awk '{print $1}' /proc/loadavg)
    available_kb=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
    uptime
    free -g
    if awk -v load1="$load" -v kb="$available_kb" 'BEGIN {exit !(load1<=40 && kb>=30*1024*1024)}'; then return; fi
    echo "$(date -u +%FT%TZ) capacity above amendment threshold; retry in 15 minutes"
    sleep 900
  done
}
wait_for_capacity
mkdir -p "$out"
out=$(cd -- "$out" && pwd)
export V3_TEST_COMPILE_CACHE="$out/shared_compile_cache"
printf '%q ' "$0" "$@" > "$out/suite_launch_command.txt"
printf '\n' >> "$out/suite_launch_command.txt"
date -u +%FT%TZ > "$out/suite_started_utc.txt"
printf '%s\n' "$$" > "$out/suite_pid.txt"
if [[ $# -eq 4 ]]; then IFS=',' read -r -a indices <<< "$4"; else mapfile -t indices < <(awk 'NR>1 {print $1}' "$tests/seeds.tsv"); fi
failed=0
for index in "${indices[@]}"; do
  wait_for_capacity >> "$out/capacity.log" 2>&1
  if ! bash "$tests/run_suite.sh" "$1" "$2" "$out/seed_$index" "$index" > "$out/seed_${index}_launch.log" 2>&1; then
    failed=1
    echo "Seed index $index failed; stop now for root inspection (remaining rows are incomplete)."
    break
  fi
  # Sequential: no background workers or compiler fan-out.
done
joined=$(IFS=,; echo "${indices[*]}")
if ! python3 "$tests/summarize.py" "$out" --indices "$joined" > "$out/summary.log" 2>&1; then failed=1; fi
date -u +%FT%TZ > "$out/suite_finished_utc.txt"
printf '%s\n' "$failed" > "$out/suite_exit_status.txt"
exit "$failed"
