#!/usr/bin/env bash
# submit_wave.sh <WAVE> -- SUBMITS both batches of the wave through the driver's submit.sh (the manager's step; needs GO=yes).
# Order: T first (its calibration is the long pole), then V, in ONE ssh session. Each submit.sh verifies SHA256SUMS + the binary first.
# Only run after: all three H-18 gates, presubmit_check.sh OK, the pre-announce in REQUESTS.md, and the manager's per-batch OK.
set -euo pipefail; . "$(dirname "$0")/common.sh"
[[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set (the manager submits, or tells Sonnet ops to)" >&2; exit 64; }
WAVE=${1:?WAVE}
ssh $NOTS "set -e; for b in OV_${WAVE}_T OV_${WAVE}_V; do echo \"== submit \$b\"; cd $D/scripts/\$b && CONFIRM=yes bash submit.sh; done; \
           echo '--- queue'; squeue -u fb31 -h -o '%i %j %T %r' | head -40"
