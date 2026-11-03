#!/bin/bash
# run_chunks.sh NPAR RESULTS_ROOTS(comma-separated) OUTNAME THEORY(1|0) : runs run_scoring.R on every work/chunks/chunk_XX.txt
# into work/OUTNAME/out_XX, skipping chunks whose out_XX.rc is 0. Resumable: rerun the same command after a crash/sleep.
# THEORY=1 adds theory + TD d=1,2; THEORY=0 skips it. Each chunk: log work/OUTNAME/out_XX.log, rc work/OUTNAME/out_XX.rc (written last).
# Launch detached via run_bg.sh.
set -u
NPAR=${1:?npar}; ROOTS=${2:?roots}; OUTNAME=${3:?outname}; THEORY=${4:?theory}
A=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
C=$A/analysis/L_20261102/work/chunks
W=$A/analysis/L_20261102/work/$OUTNAME
STUDY="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/inputs/lowp_study"
R="/c/Program Files/R/R-4.4.1/bin/Rscript.exe"
mkdir -p "$W"
export A C W STUDY R ROOTS THEORY
one() {
  k=$1
  if [ -e "$W/out_$k.rc" ] && [ "$(cat "$W/out_$k.rc")" = "0" ]; then echo "skip $k (done)"; return 0; fi
  rm -f "$W/out_$k.rc"; rm -rf "$W/out_$k"
  if [ "$THEORY" = "1" ]; then TH=(--theory 1 --td-d 1,2); else TH=(--theory 0); fi
  "$R" "$A/code/scoring/run_scoring.R" --study "$STUDY" --results "$ROOTS" --out "$W/out_$k" --cases "$C/chunk_$k.txt" \
       --scales c100,c050 "${TH[@]}" --core "$A/code/core/v2_2_1/core" > "$W/out_$k.log" 2>&1
  rc=$?; echo $rc > "$W/out_$k.rc"; echo "chunk $k rc=$rc $(date -u +%H:%M:%SZ)"
}
export -f one
ls "$C"/chunk_*.txt | sed 's/.*chunk_\([0-9]*\)\.txt/\1/' | xargs -P "$NPAR" -I{} bash -c 'one {}'
bad=0; for f in "$C"/chunk_*.txt; do k=$(basename "$f" .txt); k=${k#chunk_}; [ "$(cat "$W/out_$k.rc" 2>/dev/null)" = "0" ] || bad=$((bad+1)); done
echo "chunks not ok: $bad"; [ $bad -eq 0 ]
