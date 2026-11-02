#!/bin/bash
#SBATCH --job-name=lowpL_s8_unlock
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:15:00
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}"
source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init unlock
pilot_modules lowp
mkdir -p -- "$LOG_RUN/truthlock/$WAVE"
[ -r "$LOG_RUN/jobids.tsv" ] || { echo "STOP: missing job ids; trees stay locked" >&2; exit 1; }
FITS=$(awk -F'\t' 'NR>1 && $2 ~ /^s[1234]_/ {if($3 !~ /^[0-9]+$/)exit 1; print $3}' "$LOG_RUN/jobids.tsv" | paste -sd, -) || { echo "STOP: invalid recorded fitting ID" >&2; exit 1; }
if [ -n "$FITS" ]; then
  Q=$("${SQUEUE:-squeue}" -h -u fb31 -o '%i|%j|%T') || { echo "STOP: squeue failed; trees stay locked" >&2; exit 1; }
  printf '%s\n' "$Q" | awk -F'|' -v ids="$FITS" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{if(NF<3 || $1 !~ /^[0-9]+(_[^|]+)?$/)bad=1;split($1,b,"_");if(x[b[1]])bad=1} END{exit bad}' || { echo "STOP: active job or invalid queue" >&2; exit 1; }
  A=$("${SACCT:-sacct}" -X -n -P -j "$FITS" -o JobID,State) || { echo "STOP: sacct failed" >&2; exit 1; }
  printf '%s\n' "$A" | awk -F'|' -v ids="$FITS" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{if(NF<2 || $1 !~ /^[0-9]+(_[^|]+)?$/){bad=1;next} split($1,b,"_");if(!x[b[1]]){bad=1;next} seen[b[1]]=1;if($2 !~ /^(COMPLETED|FAILED|CANCELLED.*|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)$/)bad=1} END{for(i in x)if(!seen[i])bad=1;exit bad}' || { echo "STOP: incomplete terminal accounting" >&2; exit 1; }
fi
timed unlock apply 1 env RSCRIPT=Rscript bash "$PILOT_DIR/truth_wave.sh" unlock "$STUDY" "$LOWPR_DIR" "$LOG_RUN/truthlock/$WAVE/WAVE_UNLOCK.txt" "$LOG_RUN/truthlock/$WAVE/evidence"
pilot_finish
