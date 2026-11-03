#!/bin/bash
# plb_post_chain_fromB.sh : RESUME after the 01:24Z VPN outage; phase A was COMPLETED on NOTS (CLOSE_BENCH_OK 02:13:51Z, see ops_nots_recheck2_20261103.txt) and is NOT rerun.
# Original header: (laptop; detached via detach_run.sh) PROD_L_BENCH rev 2 (STAMP 20261102T2309Z) after ALL_TERMINAL (98 COMPLETED), JOB.md §5:
#  A control: plb_close_remote.sh PHASE=bench (reconcile, clear_stale list, make_resubmit r1 = NOTHING_TO_RESUBMIT, manifests bench)
#  B bulk   : pull results/<STAMP>_lowp_benchres --delete (+ local MANIFEST check by pull_list)
#  C control: plb_close_remote.sh PHASE=logs (final_accounting, manifests logs)
#  D bulk   : pull logs/<STAMP>_lowp_bench --delete; home summaries manifests, inventory_final (+ resubmit if present) copy into
#             runs\<RID>\home_summary\<name> (fresh siblings; runs\<RID>\ already holds bundle\)
#  E laptop : accept_bench.R -> ACCEPT_BENCH.md must say ACCEPTED (exit 0)
#  F control: cleanup_bench.sh dry run + --yes + receipt (CLEANUP VERIFIED)
# Any failure -> CHAIN STOP for OPS (never retried here). Status: ops9_plb_post_chain.txt.
set -u
STAMP=20261102T2309Z; RID=${STAMP}_lowp_bench
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; C=$E/ops9_plb_post_chain.txt
DMW='C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign'; DMU="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign"
stop() { echo "CHAIN STOP $(date -u +%FT%TZ): $1" >> $C; exit 1; }
echo "resume from B $(date -u +%FT%TZ) (A done on NOTS: CLOSE_BENCH_OK 02:13:51Z)" >> $C
export NOTS_SSH_LOCK_WAIT_S=7200
export NOTS_PULL_TIMEOUT_S=14400   # results folder = 76,800 files: remote manifest can exceed nots_pull's 3600 s default (cf. PROD-L logs)
# B
bash $S/pull_list.sh $E/ops9_plb_pulls.txt "/scratch/fb31/New_Campaign/results/${STAMP}_lowp_benchres|delete"
grep -q '^PULL_LIST_DONE OK' $E/ops9_plb_pulls.txt || stop "phase B (bench results pull) failed"
echo "B results pulled+verified+deleted" >> $C
# C
NOTS_SSH_LANE=control bash $S/remote_bg.sh plb_close_logs_$STAMP $S/plb_close_remote.sh $E/ops9_plb_close_logs.txt STAMP=$STAMP PHASE=logs
grep -E '^(final_accounting_rc|make_manifests_logs_rc|MANIFEST|CLOSE_LOGS_OK|STOP)' $E/ops9_plb_close_logs.txt >> $C
grep -q '^CLOSE_LOGS_OK' $E/ops9_plb_close_logs.txt || stop "phase C (close logs) did not complete"
# D
specs=("/scratch/fb31/New_Campaign/logs/$RID|delete"
       "/home/fb31/projects/BVS/New_Campaign/runs/$RID/manifests|keep|$DMW\\runs\\$RID\\home_summary\\manifests"
       "/home/fb31/projects/BVS/New_Campaign/runs/$RID/inventory_final|keep|$DMW\\runs\\$RID\\home_summary\\inventory_final")
grep -qx 'resubmit' <(sed -n '/CLOSE_LOGS_OK/q;p' $E/ops9_plb_close_logs.txt) && specs+=("/home/fb31/projects/BVS/New_Campaign/runs/$RID/resubmit|keep|$DMW\\runs\\$RID\\home_summary\\resubmit")
bash $S/pull_list.sh $E/ops9_plb_pulls.txt "${specs[@]}"
[ "$(grep -c '^PULL_LIST_DONE OK' $E/ops9_plb_pulls.txt)" = 2 ] || stop "phase D (logs + home summaries pull) failed"
echo "D logs pulled+deleted; home summaries copied" >> $C
# E
mkdir -p "$DMU/runs/$RID/accept"
"/c/Program Files/R/R-4.4.1/bin/Rscript.exe" "$CAMP/jobs/PROD_L_BENCH/accept_bench.R" --results "$DMW\\results\\${STAMP}_lowp_benchres" --lists "$CAMP/jobs/PROD_L_BENCH/lists/units.tsv" --code "$CAMP/code/bench_lowp" --r2-manifest "$CAMP/code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt" --inputs-manifest "$DMW\\inputs\\lowp_study\\manifests\\inputs_manifest_lowp.csv" --out "$DMW\\runs\\$RID\\accept" > $E/ops9_plb_accept.txt 2>&1
arc=$?; echo "accept_rc=$arc" >> $C; tail -5 $E/ops9_plb_accept.txt >> $C
[ $arc -eq 0 ] && grep -q 'ACCEPTED' "$DMU/runs/$RID/accept/ACCEPT_BENCH.md" || stop "phase E: accept_bench not ACCEPTED (rc=$arc) -> HQ"
# F
cat > $S/_plb_cleanup_rev2_remote.sh <<EOF
#!/bin/bash
export STAMP=$STAMP
B=/home/fb31/projects/BVS/New_Campaign/runs/$RID/code/prod_l_bench
REC=/scratch/fb31/New_Campaign/upload/cleanup_receipt_$RID.txt
cd /scratch/fb31/New_Campaign || exit 2
echo "== dry run"; bash \$B/cleanup_bench.sh $STAMP < /dev/null 2>&1 | tail -12; echo "dry_rc=\${PIPESTATUS[0]}"
echo "== --yes"; bash \$B/cleanup_bench.sh $STAMP --yes --receipt \$REC < /dev/null 2>&1 | tail -15; rc=\${PIPESTATUS[0]}; echo "cleanup_rc=\$rc"; exit \$rc
EOF
NOTS_SSH_LANE=control bash $S/remote_bg.sh plb_cleanup_$STAMP $S/_plb_cleanup_rev2_remote.sh $E/ops9_plb_cleanup.txt
grep -E '^(dry_rc|cleanup_rc)|CLEANUP' $E/ops9_plb_cleanup.txt >> $C
grep -q '^cleanup_rc=0' $E/ops9_plb_cleanup.txt && grep -q 'CLEANUP VERIFIED' $E/ops9_plb_cleanup.txt || stop "phase F: cleanup not verified"
echo "CHAIN DONE $(date -u +%FT%TZ)" >> $C
