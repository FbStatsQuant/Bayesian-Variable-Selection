#!/bin/bash
# test_lanes.sh : offline test of the HQ D76 two-lane locks (no NOTS contact: REAL_SSH is a local fake; private lock paths).
D=$(cd "$(dirname "$0")" && pwd); T=$(mktemp -d)
export NOTS_SSH_LOCK_BULK=$T/bulk.lock NOTS_SSH_LOCK_CONTROL=$T/control.lock
printf '#!/bin/bash\nsleep "${FAKE_SLEEP:-0}"; echo fake-ssh-done\n' > $T/fakessh; chmod +x $T/fakessh
export REAL_SSH=$T/fakessh
pass=0; fail=0; ok() { echo "PASS $1"; pass=$((pass+1)); }; ko() { echo "FAIL $1"; fail=$((fail+1)); }
# 1: a bulk holder does not block a control call
NOTS_SSH_LANE=bulk bash $D/with_lock.sh sleep 6 & B=$!; sleep 1
t0=$(date +%s); FAKE_SLEEP=0 bash $D/ssh nots true >/dev/null; t1=$(date +%s)
[ $((t1-t0)) -le 3 ] && ok "control not blocked by bulk ($((t1-t0)) s)" || ko "control blocked by bulk ($((t1-t0)) s)"
# 2: a second bulk caller waits for the first
t0=$(date +%s); NOTS_SSH_LANE=bulk bash $D/with_lock.sh true; t1=$(date +%s)
[ $((t1-t0)) -ge 3 ] && ok "bulk serialised ($((t1-t0)) s)" || ko "bulk not serialised ($((t1-t0)) s)"
wait $B
# 3: control calls serialise
FAKE_SLEEP=4 bash $D/ssh nots true >/dev/null & C=$!; sleep 1
t0=$(date +%s); FAKE_SLEEP=0 bash $D/ssh nots true >/dev/null; t1=$(date +%s)
[ $((t1-t0)) -ge 2 ] && ok "control serialised ($((t1-t0)) s)" || ko "control not serialised ($((t1-t0)) s)"
wait $C
# 4: control wall bound -> 124, lock released afterwards
FAKE_SLEEP=6 NOTS_CONTROL_WALL_S=2 bash $D/ssh nots true >/dev/null 2>$T/err; rc=$?
[ $rc = 124 ] && grep -q 'exceeded 2s wall' $T/err && ok "control wall bound rc=124" || ko "control wall bound rc=$rc"
[ ! -e $NOTS_SSH_LOCK_CONTROL ] && ok "control lock released after timeout" || ko "control lock left behind"
# 5: bulk lane has no wall bound
FAKE_SLEEP=3 NOTS_CONTROL_WALL_S=1 NOTS_SSH_LANE=bulk bash $D/ssh nots true >/dev/null; rc=$?
[ $rc = 0 ] && ok "bulk not wall-bounded" || ko "bulk wall-bounded rc=$rc"
# 6: re-entrancy within a lane (bulk holder running a bulk ssh) and NOT across lanes (bulk holder's nested control call takes control lock)
NOTS_SSH_LANE=bulk bash $D/with_lock.sh bash -c 'NOTS_SSH_LANE=bulk ssh nots true' >/dev/null && ok "bulk re-entrant" || ko "bulk re-entrancy"
mkdir $NOTS_SSH_LOCK_CONTROL; echo $$ > $NOTS_SSH_LOCK_CONTROL/pid      # control held by this live shell
NOTS_SSH_LOCK_WAIT_S=3 NOTS_SSH_LANE=bulk bash $D/with_lock.sh bash -c 'NOTS_SSH_LANE=control ssh nots true' >/dev/null 2>&1; rc=$?
[ $rc = 255 ] && ok "no cross-lane re-entrancy (nested control waited, rc 255)" || ko "cross-lane re-entrancy rc=$rc"
rm -rf $NOTS_SSH_LOCK_CONTROL
# 7: dead-owner takeover still works
mkdir $NOTS_SSH_LOCK_CONTROL; echo 999999 > $NOTS_SSH_LOCK_CONTROL/pid
bash $D/ssh nots true >/dev/null && ok "dead-owner takeover" || ko "dead-owner takeover"
rm -rf $T; echo "RESULT pass=$pass fail=$fail"
