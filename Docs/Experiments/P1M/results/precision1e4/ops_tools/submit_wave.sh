#!/usr/bin/env bash
# submit_wave.sh <WAVE> -- PRECISION LEG. SUBMITS the wave's batches through each batch's own driver submit.sh (needs GO=yes).
# Pacing (LEG_PLAN §4): one submit.sh per batch, the batches of a wave >= 5 min apart (GAP_S, default 300), never a burst. One ssh call per batch.
# Only after presubmit_check.sh passed and the manager's GO. BATCHES="..." (env) submits a subset, in that order.
set -euo pipefail; . "$(dirname "$0")/common.sh"
[[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set" >&2; exit 64; }
WAVE=${1:?WAVE}; BL=${BATCHES:-$(batches_of "$STG/current/scripts" "$WAVE")}; GAP=${GAP_S:-300}; n=0
for B in $BL; do
  [[ $n -eq 0 ]] || { echo "-- waiting ${GAP}s before $B (batches >= 5 min apart)"; sleep "$GAP"; }
  echo "== submit $B"; ssh $NOTS "cd $D/scripts/$B && CONFIRM=yes bash submit.sh"; n=$((n+1))
done
ssh $NOTS "echo '--- queue'; squeue -u fb31 -h -o '%i %j %T %r' | head -40"
