#!/bin/bash
# inspect_after_backoff.sh OUTFILE : (laptop) wait the charter's 15-min back-off, then ONE read-only ssh (through the shim/lock) inspecting what the
# interrupted PROD-L `make_manifests enum20` left, the P5 scan state, and the BENCH_F3_DEV run folders.
set -u
OUT=${1:?outfile}
sleep 900
bash /c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold/sshlock/ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'date -u +%FT%TZ; squeue -h -u fb31 -o "%i %j %T"
R=/home/fb31/projects/BVS/New_Campaign/runs/20261030T1811Z_lowp_prodL; S=/scratch/fb31/New_Campaign/results/20261030T1811Z_lowp_enum20
echo "== manifests dir"; ls -la $R/manifests 2>&1
echo "== enum20 top"; ls -la $S | head -8; ls -la $S/MANIFEST* 2>&1
echo "== tmp/lock/hidden in enum20 (depth 2) + manifests"; find $S $R/manifests -maxdepth 2 \( -name "*.tmp*" -o -name "*.lock" -o -name ".*" \) 2>&1 | head
echo "== make_manifests processes"; ps -u fb31 -o pid,etime,args | grep -E "[m]ake_manifests|[r]econcile_prodl" | head
echo "== p5"; ls -la $R/p5 2>&1 | head; ls /scratch/fb31/New_Campaign/logs/20261030T1811Z_lowp_prodL/ 2>&1 | tr "\n" " "; echo
echo "== F3 dev"; ls /scratch/fb31/New_Campaign/logs/20261030T1855Z_bench_f3v2_dev 2>&1 | tr "\n" " "; echo; du -sk /scratch/fb31/New_Campaign/results/20261030T1855Z_bench_f3v2_dev 2>&1' > "$OUT" 2>&1
echo "ssh_rc=$?" >> "$OUT"
