#!/bin/bash
# lock_lib.sh (sourced): one global lock so that at most ONE ssh connection to NOTS is open at a time (charter §3), across the PROD-H poller,
# the PROD-L waiter, the dev-pilot monitor and OPS's own commands. mkdir is atomic; the holder's PID is recorded; a lock whose holder is dead is
# taken over. Re-entrant: a holder exports NOTS_SSH_LOCK_HELD=1 so nested ssh calls (shim) do not wait for themselves.
NOTS_SSH_LOCK=${NOTS_SSH_LOCK:-/tmp/nots_ssh.lock}
NOTS_SSH_LOCK_WAIT_S=${NOTS_SSH_LOCK_WAIT_S:-1800}
nots_lock_acquire() {      # returns 0 when acquired (or already held by an ancestor), 1 after NOTS_SSH_LOCK_WAIT_S
  [ "${NOTS_SSH_LOCK_HELD:-0}" = 1 ] && { NOTS_LOCK_MINE=0; return 0; }
  local t0 owner; t0=$(date +%s)
  while :; do
    if mkdir "$NOTS_SSH_LOCK" 2>/dev/null; then echo $$ > "$NOTS_SSH_LOCK/pid"; NOTS_LOCK_MINE=1; export NOTS_SSH_LOCK_HELD=1; return 0; fi
    owner=$(cat "$NOTS_SSH_LOCK/pid" 2>/dev/null)
    if [ -n "$owner" ] && ! kill -0 "$owner" 2>/dev/null; then rm -f -- "$NOTS_SSH_LOCK/pid"; rmdir -- "$NOTS_SSH_LOCK" 2>/dev/null; continue; fi
    if [ -z "$owner" ] && [ $(( $(date +%s) - t0 )) -gt 30 ]; then rmdir -- "$NOTS_SSH_LOCK" 2>/dev/null; continue; fi   # half-made lock (no pid after 30 s)
    [ $(( $(date +%s) - t0 )) -ge "$NOTS_SSH_LOCK_WAIT_S" ] && return 1
    sleep 2
  done
}
nots_lock_release() {
  [ "${NOTS_LOCK_MINE:-0}" = 1 ] || return 0
  [ "$(cat "$NOTS_SSH_LOCK/pid" 2>/dev/null)" = "$$" ] && { rm -f -- "$NOTS_SSH_LOCK/pid"; rmdir -- "$NOTS_SSH_LOCK" 2>/dev/null; }
  NOTS_LOCK_MINE=0; unset NOTS_SSH_LOCK_HELD
}
