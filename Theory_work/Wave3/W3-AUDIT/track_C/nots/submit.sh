#!/usr/bin/env bash
# W3-AUDIT-C: submit the six NOTS array classes (one per (n, p) cell; 19 designs each; 1 CPU per task).
# Usage (on NOTS, by Engineering):  bash submit.sh PKG_DIR [THROTTLE]
#   PKG_DIR = the frozen package copy, e.g. /home/fb31/SMC_Theory_Department/W3-AUDIT-C/pkg
# Time limit and memory per class come from classes.tsv (time = 2 x the measured Owls cost, see README.md).
set -euo pipefail
PKG=$(realpath "$1"); THR=${2:-60}
OUT=/scratch/fb31/SMC_Theory_Department/W3-AUDIT-C
mkdir -p "$OUT/slurm" "$OUT/log" "$OUT/out"
( cd "$PKG" && sha256sum scripts/*.py data/*.csv env_c.sh run_task.sh tasks_*.tsv classes.tsv > "$OUT/log/pkg_sha256.txt" )
while read -r CLASS TIME MEM NTASK; do
  [[ $CLASS == class ]] && continue
  job=$(sbatch --parsable --job-name="w3auditc_${CLASS}" --account=commons --partition=commons --qos=nots_commons \
        --nodes=1 --ntasks=1 --cpus-per-task=1 --mem="$MEM" --time="$TIME" --export=NONE --no-requeue \
        --array="1-${NTASK}%${THR}" --output="$OUT/slurm/%x_%A_%a.out" --error="$OUT/slurm/%x_%A_%a.err" \
        "$PKG/run_task.sh" "$PKG" "$CLASS")
  echo "$(date -u +%FT%TZ) class=$CLASS job=$job time=$TIME mem=$MEM tasks=$NTASK" | tee -a "$OUT/log/submitted.txt"
done < "$PKG/classes.tsv"
