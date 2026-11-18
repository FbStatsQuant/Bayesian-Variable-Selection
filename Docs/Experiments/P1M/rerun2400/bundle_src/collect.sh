#!/usr/bin/env bash
# collect.sh RUN_ID [DEST]  -- run ON OWLS after the arrays finished. ONE ssh call to NOTS (the multiplexed master) for the accounting, one rsync over the
# same master for the results (~0.4 GB). Then checks the per-fit sha256 files locally and runs the comparator.
#   bash collect.sh rr2400_<STAMP>            (DEST default: /home/fb31/SMC_Engineering_Department/records/rerun2400/<RUN_ID>)
set -euo pipefail
RUN_ID=${1:?RUN_ID}; DEST=${2:-/home/fb31/SMC_Engineering_Department/records/rerun2400/$RUN_ID}
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
R=/scratch/fb31/SMC_Engineering_Department/runs/rerun2400/$RUN_ID
B=/home/fb31/SMC_Engineering_Department/scripts/rerun2400
mkdir -p "$DEST"
ssh nots "set -e; ids=\$(awk -F'\t' 'NR>1{print \$1}' $B/run/jobs.tsv | paste -sd,); \
  squeue -h -u fb31 -o '%i|%j|%T' > $R/squeue_at_collect.txt 2>&1 || true; \
  sacct -j \$ids -P -n --format=JobID,JobName%40,State,ExitCode,Elapsed,ElapsedRaw,MaxRSS,AllocCPUS,NodeList,Start,End > $R/sacct.psv; \
  cp $B/run/jobs.tsv $B/run/config.env $R/; ls $R/old/results/$RUN_ID/p*/*/SMCBVS.done 2>/dev/null | wc -l; ls $R/new/results/$RUN_ID/p*/*/NEWFIT.done 2>/dev/null | wc -l; ls $R | tr '\n' ' '"
rsync -a --exclude tmp/ -e ssh "nots:$R/" "$DEST/"
n=0; bad=0
for f in "$DEST"/old/results/"$RUN_ID"/p*/*/SMCBVS.sha256 "$DEST"/new/results/"$RUN_ID"/p*/*/NEWFIT.sha256; do
  [ -e "$f" ] || continue; n=$((n+1)); ( cd "$(dirname "$f")" && sha256sum --quiet -c "$(basename "$f")" >/dev/null 2>&1 ) || { bad=$((bad+1)); echo "BAD CHECKSUM: $f"; }
done
echo "checksum files verified: $n, bad: $bad"
nice -n 19 Rscript --vanilla "$HERE/../analysis/comparator.R" --old-root "$DEST/old" --new-root "$DEST/new" --run-id "$RUN_ID" --out "$DEST/compare" --expect-grid || true
ls "$DEST"/ALERT_* 2>/dev/null || true
