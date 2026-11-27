#!/usr/bin/env bash
# install_md5_ref.sh -- run on OWLS. Builds the SMC-BVS data_md5 reference index (harness/md5_index.R) from the Owls
# copies of the SMC-BVS records and installs it on NOTS, where check_bench.sh reads it:
#   nots:/home/fb31/SMC-BVS/_local/engineering/S1S2/ref/smcbvs_data_md5.tsv  (+ .sha256, verified on NOTS after copy)
#   install_md5_ref.sh [--roots DIR[,DIR...]] [--dry-run]
# Default roots: Owls runs/S1S2 (all 12,000 S2 records, S1 batch 1) and the S1 staging copy
# _local/engineering/staging/S1_interim_20261127T014708Z (S1 to date). Only R 4.5.2 (NOTS) records carrying a data_md5
# enter the index; reps not in it (e.g. the S1 p=5000 fits still running) are checked against the live NOTS json by
# check_bench.sh. Re-run (it replaces the file atomically) after the last S1 SMC-BVS fits are pulled, and BEFORE
# free_nots_scratch.sh deletes any SMC-BVS records from NOTS scratch. The Owls copy is kept in
# _local/engineering/runs/S1S2/_ref/ (not in git).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ENGO=/home/fb31/Bayesian-Variable-Selection/_local/engineering
REFN=/home/fb31/SMC-BVS/_local/engineering/S1S2/ref
roots="$ENGO/runs/S1S2,$ENGO/staging/S1_interim_20261127T014708Z"; dry=0
while (($#)); do case "$1" in --roots) roots="$2"; shift 2;; --dry-run) dry=1; shift;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
out=$ENGO/runs/S1S2/_ref; mkdir -p "$out"; f=$out/smcbvs_data_md5.tsv
nice -n 19 Rscript "$HERE/../harness/md5_index.R" --roots "$roots" --dest "$f"
( cd "$out" && sha256sum smcbvs_data_md5.tsv > smcbvs_data_md5.tsv.sha256 )
echo "index: $f ($(( $(wc -l < "$f") - 1 )) rows) sha256 $(cut -c1-16 "$f.sha256")"
if ((dry)); then echo "[dry-run] not copied to nots:$REFN/"; exit 0; fi
ssh nots "mkdir -p '$REFN'"
rsync -a "$f" "$f.sha256" "nots:$REFN/.incoming/"
ssh nots "set -e; cd '$REFN/.incoming' && sha256sum --quiet -c smcbvs_data_md5.tsv.sha256 && mv smcbvs_data_md5.tsv smcbvs_data_md5.tsv.sha256 '$REFN/' && rmdir '$REFN/.incoming' && cd '$REFN' && sha256sum -c smcbvs_data_md5.tsv.sha256" && echo "INSTALLED nots:$REFN/smcbvs_data_md5.tsv (sha256 verified)"
