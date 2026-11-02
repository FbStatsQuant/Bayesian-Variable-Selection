#!/bin/bash
# status2_remote.sh (ON NOTS via: ssh nots 'bash -s' < this): HQ D62 step 2 — one batched, read-only status: squeue; sacct since 2026-11-02T03:00Z;
# PROD-L enum20/enum30 close state after the 04:08Z connection reset; P5 scan state (PROD-H and PROD-L); BENCH_F3_DEV folders; scratch/home usage.
set -u
HR=/home/fb31/projects/BVS/New_Campaign; S=/scratch/fb31/New_Campaign
RH=$HR/runs/20261030T0934Z_prodH; RL=$HR/runs/20261030T1811Z_lowp_prodL; LL=$S/logs/20261030T1811Z_lowp_prodL
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== squeue"; squeue -h -u fb31 -o '%i %j %T %M' 2>&1
echo "== sacct since 2026-11-02T03:00"; sacct -u fb31 -S 2026-11-02T03:00:00 -X -n -o JobID%22,JobName%40,State%12,ExitCode,Elapsed 2>&1 | awk '{split($1,a,"_"); k=a[1]" "$2" "$3; c[k]++} END{for(k in c) print k, c[k]}' | sort
echo "== live make_manifests/reconcile/submit processes"; ps -u fb31 -o pid,etime,args | grep -E "[m]ake_manifests|[r]econcile_prodl|[s]ubmit_prodl|[p]5_s" | cut -c1-160
echo "== PROD-L manifests dir"; ls -la $RL/manifests 2>&1
for p in enum20 enum30; do d=$S/results/20261030T1811Z_lowp_$p; echo "== $p: $(ls -la $d/MANIFEST.sha256 2>&1 | cut -c1-120)"; echo "   lines: $(wc -l < $d/MANIFEST.sha256 2>/dev/null)  files: $(find $d -type f ! -name MANIFEST.sha256 | wc -l)  tmp/lock: $(find $d -maxdepth 3 \( -name '*.tmp*' -o -name '*.lock' \) | wc -l)"; done
echo "== PROD-L p5 + scan logs"; ls -la $RL/p5 2>&1 | head; ls $LL 2>&1 | tr '\n' ' '; echo
echo "== PROD-H P5 artefacts"; ls $RH | grep -iE 'p5|scan' 2>&1; ls $RH/p5 2>&1 | head
echo "== BENCH_F3_DEV"; ls $S/logs/20261030T1855Z_bench_f3v2_dev 2>&1 | tr '\n' ' '; echo; find $S/results/20261030T1855Z_bench_f3v2_dev -name 'F3.done' 2>/dev/null | wc -l | sed 's/^/F3.done files: /'
echo "== disk"; du -sk $S/results/* $S/logs/* $S/upload/* 2>/dev/null | sort -k2; quota -s 2>&1 | sed -n 3p
