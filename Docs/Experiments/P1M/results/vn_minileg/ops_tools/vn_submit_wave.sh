#!/usr/bin/env bash
# vn_submit_wave.sh <WAVE> -- V-N mini-leg: submit the wave's batches through each batch's own driver submit.sh (GO=yes), batches >= 5 min apart (GAP_S, default 300), one ssh per batch.
# Only after vn_presubmit.sh passed and the manager's GO. BATCHES="..." submits a subset in that order. Send the monitor START line after the LAST batch.
set -euo pipefail; . "$(dirname "$0")/common.sh"
[[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set" >&2; exit 64; }
WAVE=${1:?WAVE}; BL=${BATCHES:-$(batches_of "$STG/current/scripts" "$WAVE")}; GAP=${GAP_S:-300}; n=0
for B in $BL; do
  [[ $n -eq 0 ]] || { echo "-- waiting ${GAP}s before $B (batches >= 5 min apart)"; sleep "$GAP"; }
  echo "== submit $B"; ssh $NOTS "cd $D/scripts/$B && CONFIRM=yes bash submit.sh"; n=$((n+1))
done
