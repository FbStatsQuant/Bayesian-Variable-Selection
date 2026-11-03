#!/bin/bash
# plb_stage_local_rev2.sh STAMP : (laptop) PROD_L_BENCH rev 2 (HQ D85): verify the authoritative ledger BUNDLE_SHA256SUMS.txt (32 files,
# da08f38c…186a) and the frozen bench_lowp r2 manifest (85a18248…a6b7), then stage_local.sh with a FRESH STAMP (never 20261102T1311Z) into the
# durable NOTS Data run folder.
set -u
STAMP=${1:?STAMP}; RID="${STAMP}_lowp_bench"
[ "$STAMP" != 20261102T1311Z ] || { echo "STAMP 20261102T1311Z must not be reused (HQ D82)"; exit 1; }
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
B=$CAMP/jobs/PROD_L_BENCH
[ "$(sha256sum "$B/BUNDLE_SHA256SUMS.txt" | cut -c1-64)" = da08f38c39d1701bcca69b5d01faeeb3315d2a7d9ca645142f941fef7fee186a ] || { echo "LEDGER HASH DIFFERS FROM HQ D85"; exit 1; }
( cd "$B" && sha256sum --quiet -c BUNDLE_SHA256SUMS.txt ) || { echo "BUNDLE LEDGER MISMATCH"; exit 1; }
echo "BUNDLE_OK $(wc -l < "$B/BUNDLE_SHA256SUMS.txt") files ledger da08f38c…"
r2=$(sha256sum "$CAMP/code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt" | cut -c1-64); echo "r2 manifest $r2"
[ "${r2:0:12}" = 85a182488450 ] && [ "${r2: -4}" = a6b7 ] || { echo "R2 MANIFEST DIFFERS"; exit 1; }
"C:/Program Files/Git/bin/bash.exe" "$B/stage_local.sh" --sealed "C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/inputs/lowp_study" --stamp "$STAMP" --out "C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/runs/$RID/bundle"
echo "stage_rc=$?"
