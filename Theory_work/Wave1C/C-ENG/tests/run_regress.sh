#!/usr/bin/env bash
# run_regress.sh CORE_DIR WORK_DIR MODE(old|off|on) OUT_DIR [JOBS]
# Fits S1-S6 x replicates 1..4 x scales {1, 0.5} at n = 100, p = 30 with one core; MODE old = 4-argument v3_fit.
set -u
core=$1; work=$2; mode=$3; out=$4; jobs=${5:-4}
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
case $mode in old) ls0=NA;; off) ls0=FALSE;; on) ls0=TRUE;; esac
# build the testing copy once
Rscript -e "source('$here/ceng_load.R'); ceng_load('$core', '$work', exports = FALSE)" > "$out/build_$mode.log" 2>&1
for s in 1 2 3 4 5 6; do for r in 1 2 3 4; do for c in 1 0.5; do
  echo "$s $r $c"
done; done; done | xargs -P "$jobs" -n 3 sh -c 'Rscript "'"$here"'/run_fit.R" "'"$core"'" "'"$work"'" '"$ls0"' "$0" "$1" 100 "$2" "'"$out"'/S$0_r$1_c$2_'"$mode"'.rds" 2>/dev/null | tail -1'
