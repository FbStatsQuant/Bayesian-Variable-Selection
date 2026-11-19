#!/usr/bin/env bash
# vn_submit.sh -- submit the ONE identity-check batch through the driver's submit.sh (GO=yes). Refuses unless the binary sha256 == the BUILD_F2 line and git_commit == F2.
set -euo pipefail; . "$(dirname "$0")/common.sh"
[[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set" >&2; exit 64; }
EXP=$(awk -F'\t' '$3=="BUILD_F2"{print $4; exit}' "$LOG"); [[ -n $EXP ]] || { echo "REFUSED: no BUILD_F2 line in $LOG" >&2; exit 1; }
ssh $NOTS "set -e; S=$D/scripts/$BATCH; sh=\$(sha256sum \$S/bin/smcbvs4 | cut -d' ' -f1); [[ \$sh == $EXP ]] || { echo \"REFUSED: bin sha256 \$sh != BUILD_F2 $EXP\" >&2; exit 1; }
  v=\$( ( set +u; source \$S/env.sh >/dev/null 2>&1; \$S/bin/smcbvs4 version 2>&1 ) ); echo \"\$v\" | grep -q \"\\\"git_commit\\\": *\\\"$F2\\\"\" || { echo 'REFUSED: git_commit != F2' >&2; exit 1; }
  echo 'binary == BUILD_F2, git_commit == F2'; cd \$S && CONFIRM=yes bash submit.sh"
