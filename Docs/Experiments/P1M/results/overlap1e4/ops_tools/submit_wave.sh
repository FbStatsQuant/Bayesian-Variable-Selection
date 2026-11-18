#!/usr/bin/env bash
# submit_wave.sh <WAVE> -- SUBMITS the wave's batches through the driver's submit.sh (needs GO=yes). ARMS env: default "T V"; the rebuilds
# use ARMS="T2 V2" (T2 first = the long pole, then V2), ONE ssh session. Each submit.sh verifies SHA256SUMS + the binary first.
# Only after presubmit_check.sh passed (git_commit == F for each binary) and the manager's / HQ's GO.
set -euo pipefail; . "$(dirname "$0")/common.sh"
[[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set" >&2; exit 64; }
WAVE=${1:?WAVE}; BL=$(for a in $ARMS; do printf 'OV_%s_%s ' "$WAVE" "$a"; done)
ssh $NOTS "set -e; for b in $BL; do echo \"== submit \$b\"; cd $D/scripts/\$b && CONFIRM=yes bash submit.sh; done; \
           echo '--- queue'; squeue -u fb31 -h -o '%i %j %T %r' | head -60"
