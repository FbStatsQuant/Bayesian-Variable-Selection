#!/usr/bin/env bash
# presubmit_check.sh <WAVE> <F40> -- ONE read-only ssh call to NOTS: what must be true right before submit_wave.sh (plan §4 'before').
# ARMS="T2 V2" (env) selects the batches. REFUSES (exit 1) unless every binary's `version` (env.sh sourced) shows git_commit == F EXACTLY
# (not 'unknown', not -dirty), the libm self-test passed, SHA256SUMS ok, code is a symlink into scratch, run dir fresh, home <= 7,500 MB.
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; F=${2:?F}; need_full_sha "$F"; BL=$(for a in $ARMS; do printf 'OV_%s_%s ' "$WAVE" "$a"; done)
ssh $NOTS "set -u; D=$D; F=$F; fail=0
echo \"UTC \$(date -u +%FT%TZ)  host \$(hostname -s)\"
for b in $BL; do
  S=\$D/scripts/\$b
  (cd \$S && sha256sum --quiet -c SHA256SUMS) && echo \"\$b SHA256SUMS ok\" || { echo \"\$b SHA256SUMS BAD\"; fail=1; }
  # the binary must run in the batch's module environment (GCC 14.3.0 -> CXXABI_1.3.15); bare it gives a false 'CXXABI_1.3.15 not found'
  if [[ -x \$S/bin/smcbvs4 ]]; then
    v=\$( ( set +u; source \$S/env.sh >/dev/null 2>&1; \$S/bin/smcbvs4 version 2>&1 ) )
    gc=\$(echo \"\$v\" | grep -o '\"git_commit\": *\"[^\"]*\"' | head -1 | grep -o '\"[^\"]*\"\$' | tr -d '\"')
    echo \"\$b version: git_commit=\$gc  \$(echo \"\$v\" | grep -o '\"island_isa\": *\"[^\"]*\"' | head -1)  libm_selftest_pass=\$(echo \"\$v\" | grep -c '\"pass\": *true')  bin sha256 \$(cut -c1-16 \$S/bin/smcbvs4.sha256)\"
    [[ \$gc == \$F ]] || { echo \"\$b REFUSED: git_commit '\$gc' != F \$F (unknown/-dirty/other)\"; fail=1; }
    echo \"\$v\" | grep -q '\"pass\": *true' || { echo \"\$b binary version/self-test FAILED:\"; echo \"\$v\" | head -3; fail=1; }
  else echo \"\$b NO BINARY\"; fail=1; fi
  [[ -L \$S/code ]] && echo \"\$b code -> \$(readlink \$S/code)  HEAD=\$(git -C \$S/code rev-parse HEAD 2>/dev/null | cut -c1-12) dirty-lines=\$(git -C \$S/code status --porcelain --untracked-files=no 2>/dev/null | wc -l)\" || { echo \"\$b code is not a symlink into scratch (home use!)\"; fail=1; }
  [[ -z \$(ls -A \$D/scratch/runs/\$b 2>/dev/null) ]] && echo \"\$b run dir empty (fresh)\" || { echo \"\$b run dir NOT empty:\"; ls \$D/scratch/runs/\$b | head; fail=1; }
done
hm=\$(quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}')
echo \"home MB used: \$hm  (refuse above 7900; hard guard 8192)\"; [[ \$hm -le 7900 ]] || { echo \"HOME TOO FULL\"; fail=1; }
echo \"my queue now: \$(squeue -u fb31 -h | wc -l) jobs\"
echo \"SPR nodes with >=24 CPU & >=16G free:\"; sinfo -h -p commons -N -t idle,mixed -o '%N %f %C %e' | awk '\$2 ~ /sapphirerapids/ {split(\$3,c,\"/\"); if (c[2]>=24 && \$4>=16384) n++} END{print n+0}'
exit \$fail"
