#!/bin/bash
# nots_recheck_once.sh : (laptop) after the 15-min back-off: ONE control-lane connection: PLB close step output, its processes, inventory_final.
S=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold
sleep 900
NOTS_SSH_LANE=control PATH="$S/sshlock:$PATH" MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'date -u +%FT%TZ; cat /scratch/fb31/New_Campaign/upload/ops_bg/plb_close_bench_20261102T2309Z.out; echo ==; ps -u fb31 -o pid,etime,pcpu,rss,args | grep -E "reconcile_bench|clear_stale|make_resubmit|make_manifests|plb_close|Rscript|python3" | grep -v grep | cut -c1-220; echo ==; ls -la --time-style=+%FT%T /home/fb31/projects/BVS/New_Campaign/runs/20261102T2309Z_lowp_bench/inventory_final 2>&1 | head' 2>&1
echo "ssh_rc=$?"
