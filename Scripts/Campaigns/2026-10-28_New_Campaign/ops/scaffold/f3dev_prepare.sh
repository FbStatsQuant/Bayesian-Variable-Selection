#!/bin/bash
# f3dev_prepare.sh RUN_ID : (laptop) BENCH_F3_DEV JOB.md "Freeze, prepare and stage" steps 1-2: verify the reviewed bundle ledger
# (BUNDLE_SHA256SUMS_FINAL = the state named in Sol narrow check R2 evidence sol_scripts_r3, paths relative to BENCH_F3_DEV) and the freeze (manifest file hash = freeze.json), then run prepare.py dev.
set -u
RUN_ID=${1:?run_id}
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
CAMPW=C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
( cd "$CAMP/bench_audit/jobs/BENCH_F3_DEV" && sha256sum --quiet -c BUNDLE_SHA256SUMS_FINAL ) || { echo "BUNDLE LEDGER MISMATCH"; exit 1; }
echo "BUNDLE_OK $(wc -l < "$CAMP/bench_audit/jobs/BENCH_F3_DEV/BUNDLE_SHA256SUMS_FINAL") files"
m=$(sha256sum "$CAMP/code/bench_v2/MANIFEST_SHA256.txt" | cut -c1-64)
grep -q "\"manifest_sha256\": \"$m\"" "$CAMP/bench_audit/jobs/BENCH_F3_PROD/runner/freeze.json" || { echo "FREEZE MISMATCH ($m)"; exit 1; }
echo "FREEZE_OK manifest $m"
py -3 -B "$CAMPW/bench_audit/jobs/BENCH_F3_PROD/prepare.py" dev "$RUN_ID" "$CAMPW/code/bench_v2"
echo "prepare_rc=$?"
