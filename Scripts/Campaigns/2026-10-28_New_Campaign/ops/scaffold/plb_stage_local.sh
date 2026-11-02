#!/bin/bash
# plb_stage_local.sh STAMP : (laptop) PROD_L_BENCH JOB.md §2 local part: verify the authoritative ledger BUNDLE_SHA256SUMS.txt (HQ D67: 32 files,
# 2a7ceba7…dfc3) and the frozen bench_lowp r2 manifest (85a18248…a6b7), then stage_local.sh with a fresh STAMP into the durable NOTS Data run folder.
set -u
STAMP=${1:?STAMP}; RID="${STAMP}_lowp_bench"
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
B=$CAMP/jobs/PROD_L_BENCH
[ "$(sha256sum "$B/BUNDLE_SHA256SUMS.txt" | cut -c1-64)" = 2a7ceba783215f21d2f0dbd3ca5d3a8b457134d52eb2e49b4db289c3ab08dfc3 ] || { echo "LEDGER HASH DIFFERS FROM HQ D67"; exit 1; }
( cd "$B" && sha256sum --quiet -c BUNDLE_SHA256SUMS.txt ) || { echo "BUNDLE LEDGER MISMATCH"; exit 1; }
echo "BUNDLE_OK $(wc -l < "$B/BUNDLE_SHA256SUMS.txt") files"
r2=$(sha256sum "$CAMP/code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt" | cut -c1-64); echo "r2 manifest $r2"
[ "${r2:0:12}" = 85a182488450 ] && [ "${r2: -4}" = a6b7 ] || { echo "R2 MANIFEST DIFFERS"; exit 1; }
"C:/Program Files/Git/bin/bash.exe" "$B/stage_local.sh" --sealed "C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/inputs/lowp_study" --stamp "$STAMP" --out "C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/runs/$RID/bundle"
echo "stage_rc=$?"
