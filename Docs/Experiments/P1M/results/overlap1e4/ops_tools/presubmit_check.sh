#!/usr/bin/env bash
# presubmit_check.sh <WAVE> -- ONE read-only ssh call to NOTS: what must be true right before submit_wave.sh (plan §4 'before').
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}
ssh $NOTS "set -u; D=$D; fail=0
echo \"UTC \$(date -u +%FT%TZ)  host \$(hostname -s)\"
for b in OV_${WAVE}_T OV_${WAVE}_V; do
  S=\$D/scripts/\$b
  (cd \$S && sha256sum --quiet -c SHA256SUMS) && echo \"\$b SHA256SUMS ok\" || { echo \"\$b SHA256SUMS BAD\"; fail=1; }
  # the binary must run in the batch's module environment (GCC 14.3.0 -> CXXABI_1.3.15); running it bare gives a false 'CXXABI_1.3.15 not found'
  if [[ -x \$S/bin/smcbvs4 ]]; then
    v=\$( ( set +u; source \$S/env.sh >/dev/null 2>&1; \$S/bin/smcbvs4 version 2>&1 ) )
    echo \"\$b binary \$(cut -c1-16 \$S/bin/smcbvs4.sha256)  isa=\$(echo \"\$v\" | grep -o '\"island_isa\": *\"[^\"]*\"' | head -1)  libm_selftest_pass=\$(echo \"\$v\" | grep -c '\"pass\": *true')\"
    echo \"\$v\" | grep -q '\"pass\": *true' || { echo \"\$b binary version/self-test FAILED:\"; echo \"\$v\" | head -3; fail=1; }
  else echo \"\$b NO BINARY\"; fail=1; fi
  [[ -L \$S/code ]] && echo \"\$b code -> \$(readlink \$S/code) (scratch)\" || { echo \"\$b code is not a symlink into scratch (home use!)\"; fail=1; }
  [[ -z \$(ls -A \$D/scratch/runs/\$b 2>/dev/null) ]] && echo \"\$b run dir empty (fresh)\" || { echo \"\$b run dir NOT empty:\"; ls \$D/scratch/runs/\$b | head; fail=1; }
done
hm=\$(quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}')
echo \"home MB used: \$hm  (refuse above 7500; hard guard 8192)\"; [[ \$hm -le 7500 ]] || { echo \"HOME TOO FULL\"; fail=1; }
echo \"my queue now: \$(squeue -u fb31 -h | wc -l) jobs\"
echo \"SPR nodes with >=24 CPU & >=16G free:\"; sinfo -h -p commons -N -t idle,mixed -o '%N %f %C %e' | awk '\$2 ~ /sapphirerapids/ {split(\$3,c,\"/\"); if (c[2]>=24 && \$4>=16384) n++} END{print n+0}'
exit \$fail"
