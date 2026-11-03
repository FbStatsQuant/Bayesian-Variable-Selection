#!/bin/bash
# lock_lib.sh (sourced): per-lane global locks for ssh connections to NOTS from this laptop (HQ D76, 2026-11-02; before D76 a single lock).
# Two lanes, at most one connection each, so at most TWO concurrent connections:
#   bulk    : long transfers (nots_pull pulls, uploads)          lock /tmp/nots_ssh.lock          (the pre-D76 path: a holder from before D76
#                                                                                                    is therefore automatically a bulk holder)
#   control : short commands (squeue/sacct, monitor checks, starting and polling detached NOTS steps, small deletes), each <= 5 min wall
#             (enforced by the shim)                              lock /tmp/nots_ssh_control.lock
# Lane = NOTS_SSH_LANE (bulk|control); default control. mkdir is atomic; the holder's PID is recorded; a lock whose holder is dead is taken
# over. Re-entrant PER LANE: a holder exports NOTS_SSH_LOCK_HELD_<LANE>=1 so nested calls in the same lane do not wait for themselves.
NOTS_SSH_LANE=${NOTS_SSH_LANE:-control}
case "$NOTS_SSH_LANE" in
  bulk)    NOTS_SSH_LOCK=${NOTS_SSH_LOCK_BULK:-/tmp/nots_ssh.lock}; _HELD_VAR=NOTS_SSH_LOCK_HELD_BULK ;;
  control) NOTS_SSH_LOCK=${NOTS_SSH_LOCK_CONTROL:-/tmp/nots_ssh_control.lock}; _HELD_VAR=NOTS_SSH_LOCK_HELD_CONTROL ;;
  *) echo "lock_lib: unknown NOTS_SSH_LANE=$NOTS_SSH_LANE" >&2; return 2 2>/dev/null || exit 2 ;;
esac
NOTS_SSH_LOCK_WAIT_S=${NOTS_SSH_LOCK_WAIT_S:-1800}
nots_lock_acquire() {      # returns 0 when acquired (or already held in this lane by an ancestor), 1 after NOTS_SSH_LOCK_WAIT_S
  [ "${!_HELD_VAR:-0}" = 1 ] && { NOTS_LOCK_MINE=0; return 0; }
  local t0 owner; t0=$(date +%s)
  while :; do
    if mkdir "$NOTS_SSH_LOCK" 2>/dev/null; then echo $$ > "$NOTS_SSH_LOCK/pid"; NOTS_LOCK_MINE=1; export "$_HELD_VAR"=1; return 0; fi
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
  NOTS_LOCK_MINE=0; unset "$_HELD_VAR"
}
