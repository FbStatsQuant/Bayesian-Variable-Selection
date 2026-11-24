#!/usr/bin/env bash
# smoke.sh BUNDLE_DIR OUTDIR -- OWLS smoke of the EXACT task script (runner/task.sh, LOCAL=1): p0500_S1_r001 c100 through both cores (one task, 2 fits).
# nice -n 19, one core, TMPDIR inside the department tmp. Works on a COPY of the bundle so the staged one stays pristine (no .cpp_cache).
set -euo pipefail
SRC=$(realpath "$1"); OUT=$(realpath -m "$2"); mkdir -p "$OUT"
export TMPDIR=$OUT/tmp; mkdir -p "$TMPDIR"
B=$OUT/bundle; [ -e "$B" ] || cp -a "$SRC" "$B"
( cd "$B" && sha256sum --quiet -c SHA256SUMS )
RUN_DIR=$B/run; mkdir -p "$RUN_DIR"
printf 'task\tdataset\tp\tscales\n1\tp0500_S1_r001\t500\tc100\n' > "$RUN_DIR/chunks_smoke.tsv"
cat > "$RUN_DIR/config.env" <<CFG
RUN_ID=smoke
BUNDLE=$B
RUNNER=$B/runner
CODE_OLD=$B/old
SUMS_OLD=$B/old.SHA256SUMS
CODE_NEW=$B/new
SUMS_NEW=$B/new.SHA256SUMS
GEN=$B/gen
OUTROOT=$OUT/run
MEM_GB=2
L500=6300
L1000=24000
KILL_MARGIN=300
LOCAL=1
CFG
mkdir -p "$OUT/run/meta"
# prime both compile caches (the cluster does this in the precompile job); outside any fit timing
for side in old new; do nice -n 19 Rscript --vanilla "$B/runner/precompile.R" "$B/$side/core" > "$OUT/precompile_$side.log" 2>&1; grep compiled_key "$OUT/precompile_$side.log"; done
export LOCAL=1 SLURM_ARRAY_TASK_ID=1 SLURM_JOB_ID=smoke1 OMP_NUM_THREADS=1
nice -n 19 bash "$B/runner/task.sh" "$RUN_DIR" chunks_smoke.tsv 2>&1 | tee "$OUT/task.out"
echo "smoke task finished; outputs in $OUT/run"
