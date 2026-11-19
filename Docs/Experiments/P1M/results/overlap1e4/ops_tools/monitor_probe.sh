#!/usr/bin/env bash
# monitor_probe.sh <WAVE> -- ONE ssh call to NOTS = ONE squeue + ONE sacct (POLICIES §12: <= 1 per 5 min; normally every 20-30 min).
# Writes the raw probe to $STG/monitor/<WAVE>/probe_<UTC>.txt (Owls) and prints the stop-rule verdict (stop_rules.py). Read-only.
# Everything else in the call is plain file reads on 2 run dirs (submissions.jsonl, truth.json X/y hashes, OUTCOME / resource_limit hits).
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}
# batches of the wave: W0 = the original T, V (evidence: T had its merge refused, GUARD-W) + the rebuilds T2, V2; other waves T, V. ARMS= overrides.
if [[ -z ${ARMS_SET:-} && $WAVE == W0 && $ARMS == "T V" ]]; then ARMS="T V T2 V2"; fi
BL=$(for a in $ARMS; do printf "OV_%s_%s " "$WAVE" "$a"; done)
if [[ $WAVE == W0 ]]; then   # known failures (INFO, not STOP): the evidence batch OV_W0_T; the AR-T2 islands refused on N (2777597) and the cancelled merge / eval (2777598/99), rescued by 2783938-40
  export IGNORE_FAILED=${IGNORE_FAILED-OV_W0_T} IGNORE_JOBS=${IGNORE_JOBS-2777597,2777598,2777599} IGNORE_ENGINE=${IGNORE_ENGINE-OV_W0_T2/4-AR-n200-r01-T-s1/log/island_}
fi
OUT=$STG/monitor/$WAVE; mkdir -p "$OUT"; P=$OUT/probe_$(date -u +%Y%m%dT%H%M%SZ).txt
ssh $NOTS "set -u; D=$D
echo \"### META utc=\$(date -u +%FT%TZ)\"
ids=''
for b in $BL; do
  echo \"### SUBMISSIONS \$b\"; cat \$D/scratch/runs/\$b/submissions.jsonl 2>/dev/null || true
  ids=\"\$ids,\$(grep -o '\"job\": *\"[0-9]*\"' \$D/scratch/runs/\$b/submissions.jsonl 2>/dev/null | grep -o '[0-9][0-9]*' | paste -sd, || true)\"
done
ids=\$(echo \"\$ids\" | sed 's/^,*//; s/,,*/,/g; s/,*\$//')
echo '### SQUEUE'; squeue -u fb31 -h -o '%i|%j|%T|%r|%M|%C'
echo '### SACCT'; [[ -n \$ids ]] && sacct -X -P -n -j \"\$ids\" --format=JobID,JobName,State,ElapsedRaw,AllocCPUS,CPUTimeRAW,Timelimit || true
echo '### DATA_HASH'
for b in $BL; do for f in \$D/scratch/runs/\$b/*/truth.json; do [[ -f \$f ]] && printf '%s|%s|%s\n' \$b \$(basename \$(dirname \$f)) \$(grep -o '\"[Xy]_sha256\": *\"[0-9a-f]*\"' \$f | grep -o '[0-9a-f]\{64\}' | tr -d '\n'); done; done
echo '### ENGINE_FLAGS'
for b in $BL; do ls \$D/scratch/runs/\$b/*/OUTCOME 2>/dev/null; grep -l -s -i 'resource_limit\|admission' \$D/scratch/runs/\$b/*/log/*.log 2>/dev/null; done; true" > "$P"
python3 "$(dirname "$0")/stop_rules.py" "$P" --wave "$WAVE" --plans "$STG/current/scripts" ${QUOTE:+--quote $QUOTE}   # QUOTE=<expected core-h of the wave> for W1+ (W0 default 100)
