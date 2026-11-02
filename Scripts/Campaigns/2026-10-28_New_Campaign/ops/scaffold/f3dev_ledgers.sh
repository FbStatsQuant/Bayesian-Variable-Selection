#!/bin/bash
# f3dev_ledgers.sh : (laptop, read-only) check the current BENCH_F3_DEV files against each of its three ledgers; show ledger dates and the
# differing files' current hashes, and whether the Sol narrow check R2 names the current hashes.
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
cd "$CAMP/bench_audit/jobs/BENCH_F3_DEV" || exit 3
for L in BUNDLE_SHA256SUMS BUNDLE_SHA256SUMS_FINAL BUNDLE_SHA256SUMS_FINAL_R2REVIEWED; do
  echo "== $L ($(date -r "$L" -u +%FT%TZ), $(wc -l < "$L") lines)"; sha256sum --quiet -c "$L" 2>&1 | tail -4; echo "rc=${PIPESTATUS[0]}"
done
echo "== current hashes of the two files"; sha256sum ../BENCH_F3_PROD/runner/validate.R JOB.md; date -r ../BENCH_F3_PROD/runner/validate.R -u +%FT%TZ; date -r JOB.md -u +%FT%TZ
for h in $(sha256sum ../BENCH_F3_PROD/runner/validate.R JOB.md | cut -c1-64); do echo "$h in reviews: $(grep -rl "$h" "$CAMP/code/bench_v2/review" "$CAMP/bench_audit" 2>/dev/null | head -5 | tr '\n' ' ')"; done
