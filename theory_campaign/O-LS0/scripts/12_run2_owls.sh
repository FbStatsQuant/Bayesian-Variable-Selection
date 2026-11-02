#!/usr/bin/env bash
# two shards inside ONE owls_run -j 2 job: $1 = spec, $2 = out dir
S=/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-de01d90c/theory_campaign/O-LS0/scripts/11_run.R
export LS0_LAT_MAX=${LS0_LAT_MAX:-1024}
Rscript $S /home/fb31/ls0_work/study "$2" "$1" 1 2 &
Rscript $S /home/fb31/ls0_work/study "$2" "$1" 2 2 &
wait
