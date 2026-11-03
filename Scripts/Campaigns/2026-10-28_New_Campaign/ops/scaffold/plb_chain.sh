#!/bin/bash
# plb_chain.sh : (laptop; detached via detach_run.sh) after the PROD-L logs pull (verified + deleted; JOB.md order): (1) PROD-L cleanup_prodl.sh
# dry run + --yes, (2) PROD_L_BENCH upload + guard 75 + stage + dry run + submit (alone), (3) exec its waiter.
# HQ D76 (2026-11-02) lanes: clean-up and submit run DETACHED on NOTS via remote_bg.sh (control lane: start + short polls, each ssh <= 5 min);
# the 64.5 MB tar upload uses the bulk lane (with_lock.sh, NOTS_SSH_LANE=bulk); the waiter's squeue/sacct checks use the control lane.
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; OUT=$E/ops9_plb_chain.txt
STAMP=20261102T1311Z; RID=${STAMP}_lowp_bench
TAR="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/runs/$RID/bundle/prodLB_bundle_$STAMP.tar"
export NOTS_SSH_LANE=control
until grep -q '^PULL_LIST_DONE' $E/ops_pulls3_20261102.txt 2>/dev/null; do sleep 60; done
{ echo "start $(date -u +%FT%TZ)"; grep '^PULL_LIST_DONE' $E/ops_pulls3_20261102.txt; } >> $OUT
if ! grep -q 'PULL /scratch/fb31/New_Campaign/logs/20261030T1811Z_lowp_prodL' $E/ops_pulls3_20261102.txt || ! grep -q '^PULL_LIST_DONE OK' $E/ops_pulls3_20261102.txt; then
  echo "STOP: PROD-L logs not pulled or pull chain failed: no cleanup, no BENCH submission" >> $OUT; echo "CHAIN_END STOP" >> $OUT; exit 1; fi
# (1) PROD-L clean-up, detached on NOTS (receipt outside the removed tree, on scratch)
bash $S/remote_bg.sh prodl_cleanup_20261030T1811Z $S/prodl_cleanup_remote.sh $E/ops9_prodl_cleanup.txt; crc=$?
cat $E/ops9_prodl_cleanup.txt >> $OUT; echo "cleanup_bg_rc=$crc" >> $OUT
grep -q '^cleanup_rc=0' $E/ops9_prodl_cleanup.txt && grep -q 'CLEANUP VERIFIED' $E/ops9_prodl_cleanup.txt || { echo "STOP: PROD-L cleanup not verified" >> $OUT; echo "CHAIN_END STOP" >> $OUT; exit 1; }
# (2) PROD_L_BENCH upload (bulk lane) + submit (detached, control lane)
SHA=$(cut -c1-64 "$TAR.sha256")
NOTS_SSH_LANE=bulk bash $S/sshlock/with_lock.sh bash -c "MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'mkdir -p /scratch/fb31/New_Campaign/upload && test ! -e /scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar && cat > /scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar && sha256sum /scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar' < '$TAR'" >> $OUT 2>&1 || { echo "STOP: upload failed" >> $OUT; echo "CHAIN_END STOP" >> $OUT; exit 1; }
grep -q "^$SHA " $OUT || { echo "STOP: uploaded tar sha256 differs from $SHA" >> $OUT; echo "CHAIN_END STOP" >> $OUT; exit 1; }
bash $S/remote_bg.sh plb_submit_$STAMP $S/plb_submit_remote.sh $E/ops9_plb_submit.txt STAMP=$STAMP TAR_SHA=$SHA
echo "submit_bg_rc=$?" >> $E/ops9_plb_submit.txt; cat $E/ops9_plb_submit.txt >> $OUT
IDS=$(awk -F'\t' 'NR>1 && $1=="main" {print $3}' <(sed -n '/^== jobids/,$p' $E/ops9_plb_submit.txt | tail -n +2) | paste -sd, -)
echo "PLB_JOBIDS=$IDS" >> $OUT; echo "CHAIN_END SUBMITTED" >> $OUT
[ -n "$IDS" ] && exec bash $CAMP/jobs/PROD_L_BENCH/waiter.sh $E/ops9_plb_waiter.log "$IDS" 72
