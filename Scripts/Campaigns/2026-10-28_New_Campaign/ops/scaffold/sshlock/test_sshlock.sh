#!/bin/bash
# test_sshlock.sh : offline test of the ssh lock (fake real ssh; private lock path). Checks: two concurrent shim calls never overlap; with_lock
# holds the lock across a nested shim call without deadlock; a dead holder's lock is taken over; exit status passes through.
set -u
D=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold/sshlock
W=$(mktemp -d); export NOTS_SSH_LOCK=$W/lock NOTS_SSH_LOCK_WAIT_S=60; NF=0
cat > "$W/fakessh" <<EOS
#!/bin/bash
echo "start \$(date +%s%N)" >> "$W/trace"; sleep 2; echo "end \$(date +%s%N)" >> "$W/trace"; exit \${FAKE_RC:-0}
EOS
chmod 755 "$W/fakessh"; export REAL_SSH=$W/fakessh
ok() { echo "PASS $*"; }; bad() { echo "FAIL $*"; NF=$((NF+1)); }
# 1. two concurrent calls are serialized
bash "$D/ssh" nots x & bash "$D/ssh" nots y & wait
awk '{print $1}' "$W/trace" | tr '\n' ' ' | grep -q '^start end start end $' && ok "serialized" || bad "overlap: $(cat "$W/trace" | tr '\n' ' ')"
# 2. with_lock + nested shim: no deadlock (finishes within 20 s)
: > "$W/trace"; timeout 20 bash "$D/with_lock.sh" bash -c "ssh nots z" && ok "re-entrant" || bad "nested deadlock or failure"
# 3. exit status passes through
FAKE_RC=7 bash "$D/ssh" nots q; [ $? -eq 7 ] && ok "rc passthrough" || bad "rc"
# 4. stale lock of a dead pid is taken over
mkdir "$NOTS_SSH_LOCK"; echo 999999 > "$NOTS_SSH_LOCK/pid"; timeout 20 bash "$D/ssh" nots s && ok "stale takeover" || bad "stale lock"
# 5. lock released at the end
[ ! -e "$NOTS_SSH_LOCK" ] && ok "released" || bad "lock left behind"
rm -rf -- "$W"; echo "sshlock test failures: $NF"; [ $NF -eq 0 ]
