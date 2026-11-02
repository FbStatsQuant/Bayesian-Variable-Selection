#!/bin/bash
# chain_finalacct_pulls.sh : (laptop; detached via detach_run.sh) 1) PROD-L final accounting + logs close (one ssh); 2) all pulls via pull_list.sh.
# The PROD-L logs folder is pulled with --delete only if the logs close succeeded (rc 0); otherwise it is skipped (D58 workaround first).
set -u
S=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold
E=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/evidence
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'bash -s' < $S/prodl_finalacct_logs_remote.sh > $E/ops6_prodl_finalacct_logs_20261102.txt 2>&1
echo "ssh_rc=$?" >> $E/ops6_prodl_finalacct_logs_20261102.txt
H=/scratch/fb31/New_Campaign; HH=/home/fb31/projects/BVS/New_Campaign/runs
SPECS=(
 "$H/results/20261030T0934Z_prodH/p0500|delete" "$H/results/20261030T0934Z_prodH/p1000|delete" "$H/logs/20261030T0934Z_prodH|delete"
 "$HH/20261030T0934Z_prodH|keep"
 "$H/results/20261030T1811Z_lowp_enum20|delete" "$H/results/20261030T1811Z_lowp_enum30|delete"
 "$H/results/20261030T1811Z_lowp_smc|delete" "$H/results/20261030T1811Z_lowp_smcrep|delete"
 "$HH/20261030T1811Z_lowp_prodL/manifests|keep" "$HH/20261030T1811Z_lowp_prodL/inventory_final|keep"
 "$H/results/20261030T1855Z_bench_f3v2_dev/p0500|keep" "$H/results/20261030T1855Z_bench_f3v2_dev/p1000|keep" "$H/logs/20261030T1855Z_bench_f3v2_dev|keep" "$H/upload/20261030T1855Z_bench_f3v2_dev|keep"
)
grep -q '^close_logs_rc=0' $E/ops6_prodl_finalacct_logs_20261102.txt && SPECS+=("$H/logs/20261030T1811Z_lowp_prodL|delete")
bash $S/pull_list.sh $E/ops_pulls_20261102.txt "${SPECS[@]}"
