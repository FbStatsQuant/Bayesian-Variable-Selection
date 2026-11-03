#!/bin/bash
# plb_failed_cleanup_chain.sh : (laptop; detached via detach_run.sh) HQ D82: clean up the failed PROD_L_BENCH run 20261102T1311Z_lowp_bench.
# (1) bulk lane: nots_pull --delete of scratch logs/20261102T1311Z_lowp_bench (evidence; copy, verify, delete) -> ops9_plb_failed_pull.txt;
# (2) control lane: plb_failed_cleanup_remote.sh detached (cleanup_bench.sh dry run + --yes + receipt) -> ops9_plb_failed_cleanup.txt;
# (3) pull the receipt (copy). Status: ops9_plb_failed_cleanup_chain.txt (CHAIN DONE / CHAIN STOP).
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; C=$E/ops9_plb_failed_cleanup_chain.txt
stop() { echo "CHAIN STOP $(date -u +%FT%TZ): $1" >> $C; exit 1; }
echo "start $(date -u +%FT%TZ)" >> $C
export NOTS_SSH_LOCK_WAIT_S=7200
bash $S/pull_list.sh $E/ops9_plb_failed_pull.txt "/scratch/fb31/New_Campaign/logs/20261102T1311Z_lowp_bench|delete"
grep -q '^PULL_LIST_DONE OK' $E/ops9_plb_failed_pull.txt && grep -q 'DELETED /scratch/fb31/New_Campaign/logs/20261102T1311Z_lowp_bench' $E/ops9_plb_failed_pull.txt || stop "logs pull/delete failed (see ops9_plb_failed_pull.txt)"
echo "logs pulled, verified, deleted" >> $C
NOTS_SSH_LANE=control bash $S/remote_bg.sh plb_failed_cleanup_$(date -u +%Y%m%dT%H%M%SZ) $S/plb_failed_cleanup_remote.sh $E/ops9_plb_failed_cleanup.txt; crc=$?
echo "cleanup_bg_rc=$crc" >> $C; grep -E 'dry_rc|cleanup_rc|CLEANUP|REFUSED' $E/ops9_plb_failed_cleanup.txt >> $C
grep -q '^cleanup_rc=0' $E/ops9_plb_failed_cleanup.txt && grep -q 'CLEANUP VERIFIED' $E/ops9_plb_failed_cleanup.txt || stop "cleanup_bench not verified"
echo "CHAIN DONE $(date -u +%FT%TZ)" >> $C
