#!/bin/bash
# f3prod_prepare.sh RUN_ID : (laptop) BENCH_F3_PROD JOB.md "Prepare and stage" (local part): verify the single authoritative ledger
# BUNDLE_SHA256SUMS_FINAL (HQ D65: 63 entries, 90579ad6…7e07) and the freeze (manifest file hash = freeze.json), then prepare.py prod.
set -u
RUN_ID=${1:?run_id}
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
CAMPW=C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
B=$CAMP/bench_audit/jobs/BENCH_F3_PROD
[ "$(sha256sum "$B/BUNDLE_SHA256SUMS_FINAL" | cut -c1-64)" = 90579ad6a592916f2a87e5be614a468901884610421ab0c4809ae86666875e07 ] || { echo "LEDGER HASH DIFFERS FROM HQ D65"; exit 1; }
( cd "$B" && sha256sum --quiet -c BUNDLE_SHA256SUMS_FINAL ) || { echo "BUNDLE LEDGER MISMATCH"; exit 1; }
echo "BUNDLE_OK $(wc -l < "$B/BUNDLE_SHA256SUMS_FINAL") entries (ledger 90579ad6…7e07)"
m=$(sha256sum "$CAMP/code/bench_v2/MANIFEST_SHA256.txt" | cut -c1-64)
grep -q "\"manifest_sha256\": \"$m\"" "$B/runner/freeze.json" || { echo "FREEZE MISMATCH ($m)"; exit 1; }
echo "FREEZE_OK manifest $m"; cat "$B/runner/resources.json"
py -3 -B "$CAMPW/bench_audit/jobs/BENCH_F3_PROD/prepare.py" prod "$RUN_ID" "$CAMPW/code/bench_v2"
echo "prepare_rc=$?"
