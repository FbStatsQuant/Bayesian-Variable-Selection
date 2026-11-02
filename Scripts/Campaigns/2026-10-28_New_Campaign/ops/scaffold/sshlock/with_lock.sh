#!/bin/bash
# with_lock.sh CMD [ARGS...] : run CMD while holding the global NOTS ssh lock (for tools that call ssh outside the bash shim, e.g. Windows
# Python nots_pull.py). The shim directory is put first in PATH and NOTS_SSH_LOCK_HELD=1 is exported, so nested shim calls do not wait.
# shellcheck disable=SC1091
D="$(cd "$(dirname "$0")" && pwd)"
source "$D/lock_lib.sh"
nots_lock_acquire || { echo "with_lock: could not get the NOTS ssh lock within ${NOTS_SSH_LOCK_WAIT_S}s" >&2; exit 255; }
PATH="$D:$PATH" "$@"; rc=$?
nots_lock_release
exit $rc
