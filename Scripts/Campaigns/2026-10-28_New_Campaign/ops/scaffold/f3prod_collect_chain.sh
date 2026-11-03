#!/bin/bash
# f3prod_collect_chain.sh : (laptop; detached via detach_run.sh) BENCH_F3_PROD collection after cell 4 (2509541) is terminal:
# (1) wait for ops8_f3prod_cell4_monitor.log ALL_TERMINAL (EARLY_FAILURE / MAX -> stop for OPS), + 5 min for accounting to settle;
# (2) f3prod_collect_remote.sh detached on NOTS (control lane): retry dry run (stop if any TIMEOUT unit or non-COMPLETED state), reconcile,
#     accounting, timing, manifests;
# (3) on COLLECT_OK: copy-pulls (bulk lane; may queue behind the PROD-L logs pull) of results p0500, p1000, logs, upload; local
#     manifests.py --verify on each. Stops before any deletion (Sol reviews the exact deletion list first). Status: ops8_f3prod_collect_chain.txt.
set -u
R=20261102T1252Z_bench_f3v2_prod
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; C=$E/ops8_f3prod_collect_chain.txt
DM='C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign'
stop() { echo "CHAIN STOP $(date -u +%FT%TZ): $1" >> $C; exit 1; }
echo "start $(date -u +%FT%TZ)" >> $C
M=$E/ops8_f3prod_cell4_monitor.log
until grep -qE '^(ALL_TERMINAL|EARLY_FAILURE|MAX_CHECKS_REACHED)' $M 2>/dev/null; do sleep 60; done
grep -q '^ALL_TERMINAL' $M || stop "cell 4 monitor ended with $(grep -E '^(EARLY_FAILURE|MAX_CHECKS_REACHED)' $M | tail -1)"
echo "cell 4 ALL_TERMINAL; settling 5 min $(date -u +%FT%TZ)" >> $C; sleep 300
NOTS_SSH_LANE=control bash $S/remote_bg.sh f3prod_collect_$(date -u +%Y%m%dT%H%M%SZ) $S/f3prod_collect_remote.sh $E/ops8_f3prod_collect.txt; crc=$?
echo "collect_bg_rc=$crc" >> $C; grep -E '^(COLLECT_OK|COLLECT_STOP|MANIFEST )' $E/ops8_f3prod_collect.txt >> $C
grep -q '^COLLECT_OK' $E/ops8_f3prod_collect.txt || stop "collection did not complete (see ops8_f3prod_collect.txt)"
# (3) pulls, copy only, bulk lane (wait up to 6 h for the lane)
export NOTS_SSH_LOCK_WAIT_S=21600
bash $S/pull_list.sh $E/ops8_f3prod_pulls.txt \
  "/scratch/fb31/New_Campaign/results/$R/p0500|keep" "/scratch/fb31/New_Campaign/results/$R/p1000|keep" \
  "/scratch/fb31/New_Campaign/logs/$R|keep" "/scratch/fb31/New_Campaign/upload/$R|keep"
grep -q '^PULL_LIST_DONE OK' $E/ops8_f3prod_pulls.txt || stop "pulls failed (see ops8_f3prod_pulls.txt)"
for rel in "results\\$R\\p0500" "results\\$R\\p1000" "logs\\$R"; do
  out=$(py -3 -B "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/manifests.py" "$DM\\$rel" --verify 2>&1); vrc=$?
  echo "VERIFY $rel rc=$vrc :: $out" >> $C
  [ $vrc -eq 0 ] || stop "local manifests --verify failed for $rel"
done
echo "CHAIN DONE $(date -u +%FT%TZ): collected + pulled + verified; next = Sol deletion-list review, then remote_pack.sh delete" >> $C
