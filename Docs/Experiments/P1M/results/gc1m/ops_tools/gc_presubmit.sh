#!/usr/bin/env bash
# gc_presubmit.sh <WAVE> -- 1M pilot GC_P: ONE read-only ssh. REFUSES (exit 1) unless, for EVERY batch of the wave: bin/smcbvs4 sha256 (computed now) == the BUILD_F2 line of deploy_gc.log
# (any other sha refused), `version` (env.sh sourced) git_commit == e993ece2.. EXACTLY, island_isa sapphirerapids, libm self-test pass, bin copied from VN_ID_1 (COPIED_FROM),
# SHA256SUMS ok, run dir fresh; home <= 7,900. BATCHES="..." restricts. The batch list is read from $SCRIPTS.
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; BL=${BATCHES:-$(batches_of "$SCRIPTS" "$WAVE")}; SHA=$(f2_sha)
[[ -n $SHA && -n $BL ]] || { echo "REFUSED: no BUILD_F2 line or no batches" >&2; exit 1; }
for B in $BL; do awk -F'\t' -v b="$B" '$2==b && $3=="COPYBIN"{f=1} END{exit !f}' "$LOG" || { echo "REFUSED: $B has no COPYBIN line in $LOG (not deployed through gc_deploy_wave.sh)" >&2; exit 1; }; done
echo "BUILD_F2 sha256 (deploy_gc.log): $SHA"
ssh $NOTS "set -u; D=$D; F2=$F2; SHA=$SHA; fail=0
echo \"UTC \$(date -u +%FT%TZ)  host \$(hostname -s)\"
for b in $BL; do
  S=\$D/scripts/\$b
  (cd \$S && sha256sum --quiet -c SHA256SUMS) && echo \"\$b SHA256SUMS ok\" || { echo \"\$b SHA256SUMS BAD\"; fail=1; }
  if [[ -x \$S/bin/smcbvs4 ]]; then
    sh=\$(sha256sum \$S/bin/smcbvs4 | cut -d' ' -f1)
    [[ \$sh == \$SHA ]] && echo \"\$b bin sha256 \${sh:0:16}.. == BUILD_F2\" || { echo \"\$b REFUSED: bin sha256 \$sh != BUILD_F2 \$SHA\"; fail=1; }
    v=\$( ( set +u; source \$S/env.sh >/dev/null 2>&1; \$S/bin/smcbvs4 version 2>&1 ) )
    gc=\$(echo \"\$v\" | grep -o '\"git_commit\": *\"[^\"]*\"' | head -1 | grep -o '\"[^\"]*\"\$' | tr -d '\"')
    echo \"\$b version: git_commit=\$gc  \$(echo \"\$v\" | grep -o '\"island_isa\": *\"[^\"]*\"' | head -1)  libm_selftest_pass=\$(echo \"\$v\" | grep -c '\"pass\": *true')\"
    [[ \$gc == \$F2 ]] || { echo \"\$b REFUSED: git_commit '\$gc' != F2 \$F2\"; fail=1; }
    echo \"\$v\" | grep -q '\"island_isa\": *\"sapphirerapids\"' || { echo \"\$b REFUSED: island_isa is not sapphirerapids\"; fail=1; }
    echo \"\$v\" | grep -q '\"pass\": *true' || { echo \"\$b binary self-test FAILED\"; fail=1; }
  else echo \"\$b NO BINARY\"; fail=1; fi
  [[ -f \$S/bin/COPIED_FROM ]] && echo \"\$b bin copied from \$(cat \$S/bin/COPIED_FROM)\" || { echo \"\$b bin/COPIED_FROM missing (not a COPYBIN deploy)\"; fail=1; }
  [[ -z \$(ls -A \$D/scratch/runs/\$b 2>/dev/null) ]] && echo \"\$b run dir empty (fresh)\" || { echo \"\$b run dir NOT empty:\"; ls \$D/scratch/runs/\$b | head; fail=1; }
done
hm=\$(quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}')
echo \"home MB used: \$hm  (refuse above $HOME_LIMIT_MB)\"; [[ \$hm -le $HOME_LIMIT_MB ]] || { echo \"HOME TOO FULL\"; fail=1; }
echo \"my queue now: \$(squeue -u fb31 -h | wc -l) jobs\"
exit \$fail"
