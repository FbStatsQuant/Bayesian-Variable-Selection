#!/bin/bash
# plb_failed_cleanup_chain2.sh : (laptop; detached via detach_run.sh) HQ D82 failed-run clean-up, part 2: wait for F3 cell 4 (2509541) to be
# terminal (remote_pack refuses deletes while fb31 jobs run), then plb_failed_cleanup_remote2.sh detached on the control lane (verified delete of
# the scratch logs copy, then cleanup_bench.sh --yes with receipt). Status: ops9_plb_failed_cleanup_chain.txt (CHAIN DONE / CHAIN STOP).
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; C=$E/ops9_plb_failed_cleanup_chain.txt
stop() { echo "CHAIN STOP $(date -u +%FT%TZ): $1" >> $C; exit 1; }
echo "part 2 start $(date -u +%FT%TZ): waiting for F3 cell 4 terminal" >> $C
M=$E/ops8_f3prod_cell4_monitor.log
until grep -qE '^(ALL_TERMINAL|EARLY_FAILURE|MAX_CHECKS_REACHED)' $M 2>/dev/null; do sleep 60; done
grep -q '^ALL_TERMINAL' $M || stop "cell 4 monitor ended without ALL_TERMINAL; OPS decides"
sleep 120
NOTS_SSH_LANE=control bash $S/remote_bg.sh plb_failed_cleanup2_$(date -u +%Y%m%dT%H%M%SZ) $S/plb_failed_cleanup_remote2.sh $E/ops9_plb_failed_cleanup.txt; crc=$?
echo "cleanup_bg_rc=$crc" >> $C; grep -E 'logs_delete_rc|dry_rc|cleanup_rc|CLEANUP|REFUSED|still queued' $E/ops9_plb_failed_cleanup.txt >> $C
grep -q '^cleanup_rc=0' $E/ops9_plb_failed_cleanup.txt && grep -q 'CLEANUP VERIFIED' $E/ops9_plb_failed_cleanup.txt || stop "cleanup not verified (see ops9_plb_failed_cleanup.txt)"
echo "CHAIN DONE $(date -u +%FT%TZ)" >> $C
