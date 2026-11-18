#!/usr/bin/env bash
# presubmit_check.sh <WAVE> -- ONE read-only ssh call to NOTS: what must be true right before submit_wave.sh (plan §4 'before').
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}
ssh $NOTS "set -u; D=$D; fail=0
echo \"UTC \$(date -u +%FT%TZ)  host \$(hostname -s)\"
for b in OV_${WAVE}_T OV_${WAVE}_V; do
  S=\$D/scripts/\$b
  (cd \$S && sha256sum --quiet -c SHA256SUMS) && echo \"\$b SHA256SUMS ok\" || { echo \"\$b SHA256SUMS BAD\"; fail=1; }
  [[ -x \$S/bin/smcbvs4 ]] && echo \"\$b binary \$(cut -c1-16 \$S/bin/smcbvs4.sha256)  isa=\$(\$S/bin/smcbvs4 version | grep -o '\"island_isa\": *\"[^\"]*\"' | head -1)\" || { echo \"\$b NO BINARY\"; fail=1; }
  [[ -z \$(ls -A \$D/scratch/runs/\$b 2>/dev/null) ]] && echo \"\$b run dir empty (fresh)\" || { echo \"\$b run dir NOT empty:\"; ls \$D/scratch/runs/\$b | head; fail=1; }
done
echo \"home MB used: \$(quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{print \$1}')  (guard 8192)\"
echo \"my queue now: \$(squeue -u fb31 -h | wc -l) jobs\"
echo \"SPR nodes with >=24 CPU & >=16G free:\"; sinfo -h -p commons -N -t idle,mixed -o '%N %f %C %e' | awk '\$2 ~ /sapphirerapids/ {split(\$3,c,\"/\"); if (c[2]>=24 && \$4>=16384) n++} END{print n+0}'
exit \$fail"
