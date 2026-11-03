#!/bin/bash
# pull_logs_prodl.sh : (laptop; detached) only the PROD-L logs pull (50,533 files) with a 4 h per-call limit, appended to ops_pulls3_20261102.txt
# (plb_chain.sh waits there for PULL_LIST_DONE). The 17:29Z attempt was stopped by OPS in its manifest phase (nothing copied or deleted) to free
# the NOTS lane for the home diagnosis after the F3 cell-1 guard refusal.
set -u
S=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold
E=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/evidence
export NOTS_PULL_TIMEOUT_S=14400
echo "NOTE $(date -u +%FT%TZ): the 17:29:01Z logs pull above was stopped by OPS in its manifest phase (pull_list pid 12806, py 12932); restarting it" >> $E/ops_pulls3_20261102.txt
bash $S/pull_list.sh $E/ops_pulls3_20261102.txt "/scratch/fb31/New_Campaign/logs/20261030T1811Z_lowp_prodL|delete"
