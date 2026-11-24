#!/usr/bin/env bash
# submit.sh [--dry-run] -- run ON NOTS (login node, one ssh), from the staged bundle: runner/submit.sh
# Verifies the bundle and both frozen trees, then submits: precompile job -> p1000 array (%20) and p500 array (%20), both afterok on the
# precompile. Same resources as PROD_H: commons, sapphirerapids, nots_commons, 1 CPU, 2G, --no-requeue, --export=NONE.
# At most 40 tasks run at once in total (20 + 20). Task wall: p1000 14:00:00, p500 06:00:00 (each task = 4 fits, 2 per side).
set -euo pipefail
RUNNER=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); BUNDLE=$(dirname "$RUNNER"); RUN_DIR=$BUNDLE/run
DRY=0; [[ ${1:-} == --dry-run ]] && DRY=1
STAMP=${STAMP:-$(date -u +%Y%m%dT%H%MZ)}; RUN_ID=rr2400_$STAMP
SCR=/scratch/fb31/SMC_Engineering_Department/runs/rerun2400; OUTROOT=$SCR/$RUN_ID
T1=20; T2=20; W1000=14:00:00; W500=06:00:00
source "$RUNNER/frozen_check.sh"
refuse() { echo "REFUSED: $*" >&2; exit 2; }
( cd "$BUNDLE" && sha256sum --quiet -c SHA256SUMS ) || refuse "bundle does not match SHA256SUMS"
nc_check_frozen "$BUNDLE/old" "$BUNDLE/old.SHA256SUMS" || refuse "old tree"
nc_check_frozen "$BUNDLE/new" "$BUNDLE/new.SHA256SUMS" || refuse "new tree"
[ "$(grep -c . "$BUNDLE/tables/chunks_p1000.tsv")" = 31 ] && [ "$(grep -c . "$BUNDLE/tables/chunks_p0500.tsv")" = 32 ] || refuse "chunk tables: expected 30 + 31 tasks"
[ ! -e "$RUN_DIR" ] || refuse "$RUN_DIR exists (a run was already prepared; use a clean bundle)"
echo "squeue (own jobs) before:"; squeue -h -u "$USER" -o "%i|%j|%T|%P" || true
COMMON=(--parsable --account=commons --partition=commons --qos=nots_commons --nodes=1 --ntasks=1 --constraint=sapphirerapids --export=NONE --no-requeue --chdir="$OUTROOT")
if [[ $DRY == 1 ]]; then echo "DRY-RUN ok: would use RUN_ID=$RUN_ID OUTROOT=$OUTROOT, T1=$T1 T2=$T2, W1000=$W1000 W500=$W500"; exit 0; fi
mkdir -p "$RUN_DIR" "$OUTROOT/slurm" "$OUTROOT/old" "$OUTROOT/new" "$OUTROOT/meta"
cp "$BUNDLE/tables/chunks_p1000.tsv" "$BUNDLE/tables/chunks_p0500.tsv" "$RUN_DIR/"
cat > "$RUN_DIR/config.env" <<CFG
RUN_ID=$RUN_ID
BUNDLE=$BUNDLE
RUNNER=$RUNNER
CODE_OLD=$BUNDLE/old
SUMS_OLD=$BUNDLE/old.SHA256SUMS
CODE_NEW=$BUNDLE/new
SUMS_NEW=$BUNDLE/new.SHA256SUMS
GEN=$BUNDLE/gen
OUTROOT=$OUTROOT
MEM_GB=2
L500=6300
L1000=24000
KILL_MARGIN=300
CFG
SUBMITTED=()
abort() { echo "ABORT: $*" >&2; for j in "${SUBMITTED[@]}"; do scancel "$j" || echo "cancel of $j FAILED" >&2; done; echo "$*" > "$RUN_DIR/SUBMISSION_ABORTED.txt"; exit 5; }
sub() { local out; out=$(sbatch "$@") || abort "sbatch failed: $*"; out=${out%%;*}; [[ $out =~ ^[0-9]+$ ]] || abort "bad job id $out"; SUBMITTED+=("$out"); echo "$out"; }
JP=$(sub "${COMMON[@]}" --job-name="rr2400_${STAMP}_precompile" --cpus-per-task=1 --mem=4G --time=01:00:00 \
  --output="$OUTROOT/slurm/%j.out" --error="$OUTROOT/slurm/%j.err" "$RUNNER/precompile.sbatch" "$RUN_DIR")
arr() { # NAME ARRAY WALL CHUNKS
  sub "${COMMON[@]}" --job-name="rr2400_${STAMP}_$1" --cpus-per-task=1 --mem=2G --time="$3" --array="$2" \
    --dependency="afterok:$JP" --kill-on-invalid-dep=yes \
    --output="$OUTROOT/slurm/%A_%a.out" --error="$OUTROOT/slurm/%A_%a.err" "$RUNNER/task.sh" "$RUN_DIR" "$4"; }
J1=$(arr p1000 "1-30%$T1" "$W1000" chunks_p1000.tsv)
J5=$(arr p500 "1-31%$T2" "$W500" chunks_p0500.tsv)
printf 'job\tkind\tarray\tsubmitted_utc\n%s\tprecompile\t-\t%s\n%s\tp1000\t1-30%%%s\t%s\n%s\tp500\t1-31%%%s\t%s\n' \
  "$JP" "$(date -u +%FT%TZ)" "$J1" "$T1" "$(date -u +%FT%TZ)" "$J5" "$T2" "$(date -u +%FT%TZ)" > "$RUN_DIR/jobs.tsv"
echo "RUN_ID=$RUN_ID OUTROOT=$OUTROOT precompile=$JP p1000=$J1 p500=$J5"
squeue -h -u "$USER" -o "%i|%j|%T|%P" || true
