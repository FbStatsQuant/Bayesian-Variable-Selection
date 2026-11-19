#!/usr/bin/env bash
# presubmit_check.sh <WAVE> <F40> -- PRECISION LEG. ONE read-only ssh call to NOTS. REFUSES (exit 1) unless, for EVERY batch of the wave:
#   * sha256 of bin/smcbvs4 (computed now, not read from a file) == the leg's single build (first BUILD line of deploy_leg.log) -- H-25 (2): any other sha is refused;
#   * `version` (batch env.sh sourced) git_commit == F EXACTLY (no -dirty, not unknown), island_isa sapphirerapids, libm self-test pass;
#   * SHA256SUMS ok; the master batch's code is a symlink into scratch (clean tree); the run dir is fresh; home <= 7,900 MB.
# BATCHES="..." (env) restricts to a subset (default: all of the wave in $STG/current/scripts).
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; F=${2:?F}; need_full_sha "$F"
BL=${BATCHES:-$(batches_of "$STG/current/scripts" "$WAVE")}; LEGSHA=$(leg_sha)
[[ -n $LEGSHA ]] || { echo "REFUSED: $LEG_LOG has no BUILD line: nothing to compare the binaries with" >&2; exit 1; }
for B in $BL; do awk -F'\t' -v b="$B" '$2==b && ($3=="BUILD"||$3=="COPYBIN"){f=1} END{exit !f}' "$LEG_LOG" || { echo "REFUSED: $B has no BUILD/COPYBIN line in $LEG_LOG (not deployed through deploy_wave.sh)" >&2; exit 1; }; done
echo "leg build sha256 (deploy_leg.log): $LEGSHA"
ssh $NOTS "set -u; D=$D; F=$F; LEGSHA=$LEGSHA; fail=0
echo \"UTC \$(date -u +%FT%TZ)  host \$(hostname -s)\"
for b in $BL; do
  S=\$D/scripts/\$b
  (cd \$S && sha256sum --quiet -c SHA256SUMS) && echo \"\$b SHA256SUMS ok\" || { echo \"\$b SHA256SUMS BAD\"; fail=1; }
  if [[ -x \$S/bin/smcbvs4 ]]; then
    sh=\$(sha256sum \$S/bin/smcbvs4 | cut -d' ' -f1)
    [[ \$sh == \$LEGSHA ]] && echo \"\$b bin sha256 \${sh:0:16}.. == the leg build\" || { echo \"\$b REFUSED: bin sha256 \$sh != the leg's \$LEGSHA\"; fail=1; }
    v=\$( ( set +u; source \$S/env.sh >/dev/null 2>&1; \$S/bin/smcbvs4 version 2>&1 ) )
    gc=\$(echo \"\$v\" | grep -o '\"git_commit\": *\"[^\"]*\"' | head -1 | grep -o '\"[^\"]*\"\$' | tr -d '\"')
    echo \"\$b version: git_commit=\$gc  \$(echo \"\$v\" | grep -o '\"island_isa\": *\"[^\"]*\"' | head -1)  libm_selftest_pass=\$(echo \"\$v\" | grep -c '\"pass\": *true')\"
    [[ \$gc == \$F ]] || { echo \"\$b REFUSED: git_commit '\$gc' != F \$F (unknown/-dirty/other)\"; fail=1; }
    echo \"\$v\" | grep -q '\"island_isa\": *\"sapphirerapids\"' || { echo \"\$b REFUSED: island_isa is not sapphirerapids\"; fail=1; }
    echo \"\$v\" | grep -q '\"pass\": *true' || { echo \"\$b binary self-test FAILED\"; fail=1; }
  else echo \"\$b NO BINARY\"; fail=1; fi
  if [[ \$b == $MASTER_BATCH ]]; then
    [[ -L \$S/code ]] && echo \"\$b code -> \$(readlink \$S/code)  HEAD=\$(git -C \$S/code rev-parse HEAD 2>/dev/null | cut -c1-12) dirty-lines=\$(git -C \$S/code status --porcelain --untracked-files=no 2>/dev/null | wc -l)\" || { echo \"\$b code is not a symlink into scratch\"; fail=1; }
  else [[ -f \$S/bin/COPIED_FROM ]] && echo \"\$b bin copied from \$(cat \$S/bin/COPIED_FROM)\" || { echo \"\$b bin/COPIED_FROM missing (not a COPYBIN deploy)\"; fail=1; }; fi
  [[ -z \$(ls -A \$D/scratch/runs/\$b 2>/dev/null) ]] && echo \"\$b run dir empty (fresh)\" || { echo \"\$b run dir NOT empty:\"; ls \$D/scratch/runs/\$b | head; fail=1; }
done
hm=\$(quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}')
echo \"home MB used: \$hm  (refuse above $HOME_LIMIT_MB; hard guard 8192)\"; [[ \$hm -le $HOME_LIMIT_MB ]] || { echo \"HOME TOO FULL\"; fail=1; }
echo \"my queue now: \$(squeue -u fb31 -h | wc -l) jobs\"
echo \"SPR nodes with >=24 CPU & >=16G free:\"; sinfo -h -p commons -N -t idle,mixed -o '%N %f %C %e' | awk '\$2 ~ /sapphirerapids/ {split(\$3,c,\"/\"); if (c[2]>=24 && \$4>=16384) n++} END{print n+0}'
exit \$fail"
