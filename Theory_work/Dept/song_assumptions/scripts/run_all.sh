#!/bin/bash
# run_all.sh -- reproduces every table (order matters). Analytic / retabulation only; no fits, no Slurm.
# usage: bash scripts/run_all.sh   (from song_assumptions/)   -> tables/*.tsv, logs/*.txt, logs/cpu_times.tsv
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 GOTO_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
cd "$(dirname "$0")/.."; mkdir -p tables logs; : > logs/cpu_times.tsv; echo -e "script\twall_s\tuser_s\tsys_s" >> logs/cpu_times.tsv
for s in e1_margin e1_fitlevel e0_e3_e4_e5_e6 e7_retab_proxy e7_bt2diag_crosscheck e1_pool_check make_summary_tables; do
  /usr/bin/time -f "$s\t%e\t%U\t%S" -a -o logs/cpu_times.tsv nice -n 19 Rscript scripts/$s.R > logs/$s.txt 2>&1 || echo "FAILED $s"
done
awk -F'\t' 'NR>1{u+=$3+$4} END{printf "total user+sys CPU: %.1f s = %.3f CPU-h\n", u, u/3600}' logs/cpu_times.tsv | tee -a logs/cpu_times.tsv
