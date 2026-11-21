#!/usr/bin/env bash
# gc_submit_wave.sh <WAVE P|D|D2|W1|W2|W3> -- 1M pilot GC_P ALONE (GC_PLAN §2, HQ H-45): submit the one batch GC_P through its driver script (submit.sh) with GO=yes. No second batch, no gate. Only after gc_presubmit.sh passed and the manager's GO.
# Waves with several batches (W1.., X1, D, S*) get their own gating when they are released; this script refuses anything but wave P.
set -euo pipefail; . "$(dirname "$0")/common.sh"
[[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set" >&2; exit 64; }
WAVE=${1:?WAVE}; [[ $WAVE == P || $WAVE == D || $WAVE == D2 || $WAVE == W1 || $WAVE == W2 || $WAVE == W3 ]] || { echo "refusing: only the released waves P (pilot, done), D / D2 (option D, done) and W1 (AR r02 + ADJ-OPP r01) may be submitted" >&2; exit 64; }
BL=$(batches_of "$SCRIPTS" "$WAVE"); [[ $BL == GC_P || $BL == GC_D || $BL == GC_D2 || $BL == GC_W1 || $BL == GC_W2 || $BL == GC_W3 ]] || { echo "refusing: unexpected batch list '$BL'" >&2; exit 64; }
SUBMIT=submit.sh; [[ ${STAGGER:-} == 1 ]] && SUBMIT=submit_stagger.sh   # H-51: staggered island arrays for the pair waves from W2 on (gc_stagger_submit.py)
echo "== submit $BL via $SUBMIT"; ssh $NOTS "cd $D/scripts/$BL && CONFIRM=yes bash $SUBMIT"
echo "all batches submitted: $BL"
