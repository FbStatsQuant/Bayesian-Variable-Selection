#!/usr/bin/env bash
# sha256 -c every SMCBVS bundle in both laptop results roots; writes a per-bundle log.
R=/c/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/claude
OUT="$1"; : > "$OUT/bundle_check.tsv"
for run in prod_p0500_20261023T1227Z prod_p1000_20261023T1227Z; do
  for d in "$R/$run"/p*/*/; do
    if ( cd "$d" && sha256sum -c --quiet SMCBVS.sha256 >/dev/null 2>&1 ); then s=PASS; else s=FAIL; fi
    [ -f "$d/SMCBVS.done" ] && dn=1 || dn=0
    printf '%s\t%s\t%s\t%s\n' "$run" "$(basename "$d")" "$s" "$dn" >> "$OUT/bundle_check.tsv"
  done
done
echo "PASS $(grep -c $'\tPASS\t' "$OUT/bundle_check.tsv") FAIL $(grep -c $'\tFAIL\t' "$OUT/bundle_check.tsv") TOTAL $(wc -l < "$OUT/bundle_check.tsv")" > "$OUT/bundle_check_summary.txt"
