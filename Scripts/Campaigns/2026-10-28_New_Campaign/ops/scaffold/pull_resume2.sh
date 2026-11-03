#!/bin/bash
# pull_resume2.sh : (laptop; detached) after the 16:17Z PROD-L logs pull failed (remote manifest > nots_pull's 3600 s limit; nothing copied or
# deleted): (1) orphan check on NOTS (kill only our remote_pack processes hashing that folder, by explicit PID); (2) the remaining pulls with a
# 4 h per-call limit (NOTS_PULL_TIMEOUT_S). Log: ops/evidence/ops_pulls3_20261102.txt.
set -u
S=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold
E=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/evidence
W='C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign\runs'
H=/scratch/fb31/New_Campaign; HH=/home/fb31/projects/BVS/New_Campaign/runs
export NOTS_PULL_TIMEOUT_S=14400
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'bash -s' < $S/orphan_pack_remote.sh > $E/ops_orphan_pack_20261102.txt 2>&1
echo "ssh_rc=$?" >> $E/ops_orphan_pack_20261102.txt
# quick pulls first; the long PROD-L logs pull (50,533 files) last
bash $S/pull_list.sh $E/ops_pulls3_20261102.txt \
 "$HH/20261030T1811Z_lowp_prodL/manifests|keep|$W\\20261030T1811Z_lowp_prodL\\home_summary\\manifests" \
 "$HH/20261030T1811Z_lowp_prodL/inventory_final|keep|$W\\20261030T1811Z_lowp_prodL\\home_summary\\inventory_final" \
 "$H/results/20261030T1855Z_bench_f3v2_dev/p0500|keep" "$H/results/20261030T1855Z_bench_f3v2_dev/p1000|keep" \
 "$H/logs/20261030T1855Z_bench_f3v2_dev|keep" "$H/upload/20261030T1855Z_bench_f3v2_dev|keep" \
 "$H/logs/20261030T1811Z_lowp_prodL|delete"
