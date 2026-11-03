#!/bin/bash
# d74_erase_then_cell1.sh : (laptop; detached via detach_run.sh) HQ D74 sequence, one NOTS lock hold:
#   (1) erase ~/.vscode-server/data/CachedExtensionVSIXs (vsix_erase_remote.sh R3, Sol rounds 1-3), require ERASE VERIFIED;
#   (2) BENCH_F3_PROD cell 1: stage.sh (its guard_check 30 = the guard rerun) + ceiling + dry run + launch (upload already on scratch: no scp);
# release the lock; (3) restart the PROD-L logs pull (4 h limit) detached; (4) exec the cell-1 array monitor.
set -u
RUN_ID=20261102T1252Z_bench_f3v2_prod; UPSHA=b7d0e36bec8ada2fd991e706da8b895a2bd2a579d9f64aaa4916355284b15424
LSHA=c708bf0627cc2fe99c9a0b5e693e85491e4dcdc7f8386996df17db4d7873b2e5
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence
export NOTS_SSH_LOCK_WAIT_S=3600
# shellcheck disable=SC1091
source $S/sshlock/lock_lib.sh
nots_lock_acquire || { echo "LOCK FAILED" > $E/ops8_f3prod_cell1.txt; echo "ssh_rc=7" >> $E/ops8_f3prod_cell1.txt; exit 1; }
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "EXPECT_SHA=$LSHA bash -s" < $S/vsix_erase_remote.sh > $E/ops_d74_vsix_erase_20261102.txt 2>&1
echo "ssh_rc=$?" >> $E/ops_d74_vsix_erase_20261102.txt
if ! grep -q '^ERASE VERIFIED' $E/ops_d74_vsix_erase_20261102.txt; then
  nots_lock_release
  { echo "D74 erase not verified (see ops_d74_vsix_erase_20261102.txt): cell 1 NOT attempted"; echo "ssh_rc=6"; } > $E/ops8_f3prod_cell1.txt
  exit 1
fi
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "RUN_ID=$RUN_ID UPSHA=$UPSHA STAGE=1 bash -s" < $S/f3prod_stage_launch_remote.sh > $E/ops8_f3prod_cell1.tmp 2>&1
echo "ssh_rc=$?" >> $E/ops8_f3prod_cell1.tmp
nots_lock_release
JID=$(grep -oE '[0-9]{7} submitted' $E/ops8_f3prod_cell1.tmp | grep -oE '[0-9]{7}' | head -1)
[ -n "$JID" ] && echo "CELL1_JOB=$JID" >> $E/ops8_f3prod_cell1.tmp
mv $E/ops8_f3prod_cell1.tmp $E/ops8_f3prod_cell1.txt
# (3) restart the PROD-L logs pull (independent of the cell-1 outcome)
bash $S/detach_run.sh $E/ops_pull_resume.pid $S/pull_logs_prodl.sh > /dev/null 2>&1 &
# (4) monitor cell 1
[ -n "$JID" ] && exec bash $S/array_monitor.sh $E/ops8_f3prod_cell1_monitor.log $JID 'f3v2_' 60
