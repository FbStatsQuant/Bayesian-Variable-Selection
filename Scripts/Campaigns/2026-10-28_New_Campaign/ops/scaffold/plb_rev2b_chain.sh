#!/bin/bash
# plb_rev2b_chain.sh : (laptop; detached via detach_run.sh) PROD_L_BENCH rev 2 resume (HQ D85), STAMP 20261102T2309Z, after the 23:10Z stop at
# the over-strict NOTS ledger check (nothing submitted; tar 7e663e2f… still on scratch upload/, runs/<RID> extracted and STAGED_OK).
# Control lane, detached on NOTS: plb_submit_remote_rev2b.sh (gates; re-verify existing extraction; corrected ledger check; dry run; submit).
# Then PLB_JOBIDS + the bundle waiter. Status: ops9_plb_rev2_chain.txt (appended; CHAIN_END SUBMITTED / STOP).
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; OUT=$E/ops9_plb_rev2_chain.txt
STAMP=20261102T2309Z; LEDGER=da08f38c39d1701bcca69b5d01faeeb3315d2a7d9ca645142f941fef7fee186a; SHA=7e663e2fd80f953e6939b5922987decc8ec0fb5ab13ac600c27c96c701be65e6
stop() { echo "STOP: $1" >> $OUT; echo "CHAIN_END STOP" >> $OUT; exit 1; }
echo "resume (rev2b) start $(date -u +%FT%TZ)" >> $OUT
export NOTS_SSH_LANE=control
bash $S/remote_bg.sh plb_submit2_$STAMP $S/plb_submit_remote_rev2b.sh $E/ops9_plb_rev2b_submit.txt STAMP=$STAMP TAR_SHA=$SHA LEDGER_SHA=$LEDGER
echo "submit_bg_rc=$?" >> $E/ops9_plb_rev2b_submit.txt; cat $E/ops9_plb_rev2b_submit.txt >> $OUT
IDS=$(awk -F'\t' 'NR>1 && $1=="main" {print $3}' <(sed -n '/^== jobids/,$p' $E/ops9_plb_rev2b_submit.txt | tail -n +2) | paste -sd, -)
[ -n "$IDS" ] || stop "no job ids (see ops9_plb_rev2b_submit.txt)"
echo "PLB_JOBIDS=$IDS" >> $OUT; echo "CHAIN_END SUBMITTED" >> $OUT
exec bash $CAMP/jobs/PROD_L_BENCH/waiter.sh $E/ops9_plb_rev2_waiter.log "$IDS" 72
