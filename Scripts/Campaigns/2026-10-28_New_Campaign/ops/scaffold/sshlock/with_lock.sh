#!/bin/bash
# with_lock.sh CMD [ARGS...] : run CMD while holding a NOTS lane lock (for tools that call ssh outside the bash shim, e.g. Windows Python
# nots_pull.py). Lane = NOTS_SSH_LANE, default **bulk** here (HQ D76: pulls/uploads). The shim directory is put first in PATH and the lane's
# NOTS_SSH_LOCK_HELD_<LANE>=1 is exported, so nested shim calls IN THE SAME LANE do not wait (a nested shim call defaults to control, so pass
# NOTS_SSH_LANE=bulk through when a bulk holder runs ssh itself, e.g. an upload).
# shellcheck disable=SC1091
export NOTS_SSH_LANE=${NOTS_SSH_LANE:-bulk}
D="$(cd "$(dirname "$0")" && pwd)"
source "$D/lock_lib.sh"
nots_lock_acquire || { echo "with_lock: could not get the NOTS $NOTS_SSH_LANE lock within ${NOTS_SSH_LOCK_WAIT_S}s" >&2; exit 255; }
PATH="$D:$PATH" "$@"; rc=$?
nots_lock_release
exit $rc
