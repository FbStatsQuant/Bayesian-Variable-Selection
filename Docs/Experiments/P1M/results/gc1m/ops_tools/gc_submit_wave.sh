#!/usr/bin/env bash
# gc_submit_wave.sh <WAVE P|D> -- 1M pilot GC_P ALONE (GC_PLAN §2, HQ H-45): submit the one batch GC_P through its driver script (submit.sh) with GO=yes. No second batch, no gate. Only after gc_presubmit.sh passed and the manager's GO.
# Waves with several batches (W1.., X1, D, S*) get their own gating when they are released; this script refuses anything but wave P.
set -euo pipefail; . "$(dirname "$0")/common.sh"
[[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set" >&2; exit 64; }
WAVE=${1:?WAVE}; [[ $WAVE == P || $WAVE == D ]] || { echo "refusing: only wave P (the pilot, done) and D (option D, alone) are released" >&2; exit 64; }
BL=$(batches_of "$SCRIPTS" "$WAVE"); [[ $BL == GC_P || $BL == GC_D ]] || { echo "refusing: unexpected batch list '$BL'" >&2; exit 64; }
echo "== submit $BL"; ssh $NOTS "cd $D/scripts/$BL && CONFIRM=yes bash submit.sh"
echo "all batches submitted: $BL"
