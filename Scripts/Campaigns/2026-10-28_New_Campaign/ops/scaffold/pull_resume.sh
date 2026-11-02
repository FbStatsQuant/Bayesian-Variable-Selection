#!/bin/bash
# pull_resume.sh : (laptop; detached) the pulls that remained after the 13:48Z stop (PROD-H home summary refused: local runs/<RID> already held bundle/).
# Home summaries go to fresh siblings runs/<RID>/home_summary/... (never merged). Log: ops/evidence/ops_pulls2_20261102.txt.
set -u
S=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold
E=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/evidence
W='C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign\runs'
H=/scratch/fb31/New_Campaign; HH=/home/fb31/projects/BVS/New_Campaign/runs
bash $S/pull_list.sh $E/ops_pulls2_20261102.txt \
 "$HH/20261030T0934Z_prodH|keep|$W\\20261030T0934Z_prodH\\home_summary" \
 "$H/results/20261030T1811Z_lowp_enum20|delete" "$H/results/20261030T1811Z_lowp_enum30|delete" \
 "$H/results/20261030T1811Z_lowp_smc|delete" "$H/results/20261030T1811Z_lowp_smcrep|delete" \
 "$H/logs/20261030T1811Z_lowp_prodL|delete" \
 "$HH/20261030T1811Z_lowp_prodL/manifests|keep|$W\\20261030T1811Z_lowp_prodL\\home_summary\\manifests" \
 "$HH/20261030T1811Z_lowp_prodL/inventory_final|keep|$W\\20261030T1811Z_lowp_prodL\\home_summary\\inventory_final" \
 "$H/results/20261030T1855Z_bench_f3v2_dev/p0500|keep" "$H/results/20261030T1855Z_bench_f3v2_dev/p1000|keep" \
 "$H/logs/20261030T1855Z_bench_f3v2_dev|keep" "$H/upload/20261030T1855Z_bench_f3v2_dev|keep"
