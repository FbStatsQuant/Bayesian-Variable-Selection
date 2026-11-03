#!/bin/bash
# f3prod_chain_cell1_now.sh : (laptop; detached via detach_run.sh) HQ D72: do not hold BENCH_F3_PROD cell 1 behind the pull chain. Takes the global
# NOTS ssh lock at the next gap between pulls (lock waiters retry every 2 s; pull_list runs its local sha256sum -c between pulls without the lock)
# and holds it across upload (scp -r) + stage + ceiling check + dry run + launch of cell 1 (one ssh), so no pull interleaves inside the sequence.
# Then starts the array monitor. Replaces f3prod_chain_cell1.sh (which waited for PULL_LIST_DONE).
set -u
RUN_ID=20261102T1252Z_bench_f3v2_prod; UPSHA=b7d0e36bec8ada2fd991e706da8b895a2bd2a579d9f64aaa4916355284b15424
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; SRC=$CAMP/bench_audit/jobs/staging/$RUN_ID
export NOTS_SSH_LOCK_WAIT_S=14400
# shellcheck disable=SC1091
source $S/sshlock/lock_lib.sh
echo "waiting for NOTS lock from $(date -u +%FT%TZ)" > $E/ops8_f3prod_lockwait.txt
nots_lock_acquire || { echo "LOCK FAILED (no gap within 4 h)" > $E/ops8_f3prod_cell1.txt; echo "ssh_rc=7" >> $E/ops8_f3prod_cell1.txt; exit 1; }
echo "lock acquired $(date -u +%FT%TZ)" >> $E/ops8_f3prod_lockwait.txt
{ MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "mkdir -p /scratch/fb31/New_Campaign/upload && test ! -e /scratch/fb31/New_Campaign/upload/$RUN_ID" && scp -r -o BatchMode=yes "$SRC" nots:/scratch/fb31/New_Campaign/upload/; } > $E/ops8_f3prod_scp.txt 2>&1 \
  || { echo "UPLOAD FAILED (see ops8_f3prod_scp.txt)" > $E/ops8_f3prod_cell1.txt; echo "ssh_rc=8" >> $E/ops8_f3prod_cell1.txt; nots_lock_release; exit 1; }
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "RUN_ID=$RUN_ID UPSHA=$UPSHA STAGE=1 bash -s" < $S/f3prod_stage_launch_remote.sh > $E/ops8_f3prod_cell1.txt 2>&1
echo "ssh_rc=$?" >> $E/ops8_f3prod_cell1.txt
nots_lock_release
echo "lock released $(date -u +%FT%TZ)" >> $E/ops8_f3prod_lockwait.txt
JID=$(grep -oE '^prod[^0-9]*([0-9]+) submitted' $E/ops8_f3prod_cell1.txt | grep -oE '[0-9]+' | head -1)
[ -z "$JID" ] && JID=$(grep -oE '[0-9]{7} submitted' $E/ops8_f3prod_cell1.txt | grep -oE '[0-9]{7}' | head -1)
if [ -n "$JID" ]; then echo "CELL1_JOB=$JID" >> $E/ops8_f3prod_cell1.txt
  exec bash $S/array_monitor.sh $E/ops8_f3prod_cell1_monitor.log $JID 'f3v2_' 60
fi
