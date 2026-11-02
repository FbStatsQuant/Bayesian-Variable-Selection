#!/bin/bash
# f3prod_chain_cell1.sh : (laptop; detached via detach_run.sh) wait for the pull chain (PULL_LIST_DONE in ops_pulls2_20261102.txt), then upload the
# prepared BENCH_F3_PROD staging folder (scp -r, holding the NOTS lock), stage + ceiling check + dry run + launch cell 1 (one ssh), then start the
# detached array monitor for the submitted job.
set -u
RUN_ID=20261102T1252Z_bench_f3v2_prod; UPSHA=b7d0e36bec8ada2fd991e706da8b895a2bd2a579d9f64aaa4916355284b15424
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; SRC=$CAMP/bench_audit/jobs/staging/$RUN_ID
until grep -q '^PULL_LIST_DONE' $E/ops_pulls2_20261102.txt 2>/dev/null; do sleep 60; done
grep -q '^PULL_LIST_DONE OK' $E/ops_pulls2_20261102.txt || { echo "pull chain did not finish OK: not launching" > $E/ops8_f3prod_cell1.txt; echo "ssh_rc=9" >> $E/ops8_f3prod_cell1.txt; exit 1; }
bash $S/sshlock/with_lock.sh bash -c "MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'mkdir -p /scratch/fb31/New_Campaign/upload && test ! -e /scratch/fb31/New_Campaign/upload/$RUN_ID' && scp -r -o BatchMode=yes '$SRC' nots:/scratch/fb31/New_Campaign/upload/" > $E/ops8_f3prod_scp.txt 2>&1 || { echo "UPLOAD FAILED (see ops8_f3prod_scp.txt)" > $E/ops8_f3prod_cell1.txt; echo "ssh_rc=8" >> $E/ops8_f3prod_cell1.txt; exit 1; }
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "RUN_ID=$RUN_ID UPSHA=$UPSHA STAGE=1 bash -s" < $S/f3prod_stage_launch_remote.sh > $E/ops8_f3prod_cell1.txt 2>&1
echo "ssh_rc=$?" >> $E/ops8_f3prod_cell1.txt
JID=$(grep -oE '^prod[^0-9]*([0-9]+) submitted' $E/ops8_f3prod_cell1.txt | grep -oE '[0-9]+' | head -1)
[ -z "$JID" ] && JID=$(grep -oE '[0-9]{7} submitted' $E/ops8_f3prod_cell1.txt | grep -oE '[0-9]{7}' | head -1)
if [ -n "$JID" ]; then echo "CELL1_JOB=$JID" >> $E/ops8_f3prod_cell1.txt
  exec bash $S/array_monitor.sh $E/ops8_f3prod_cell1_monitor.log $JID 'f3v2_' 60
fi
