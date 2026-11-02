# Historical bundle ledgers (do not verify current files against these)

The authoritative ledger is `../BUNDLE_SHA256SUMS_FINAL` (written 2026-11-02 after the HQ D64 production resource fill changed the shared `../BENCH_F3_PROD/runner/resources.json`).

| File | State it records |
|---|---|
| `BUNDLE_SHA256SUMS_prefreeze_20261030` | pre-freeze draft |
| `BUNDLE_SHA256SUMS_FINAL_R2REVIEWED_20261030` | bundle as Sol review 2 saw it (before the R2-1/2/3 fixes) — OPS found it does not match the current files; that is expected, it is historical |
| `BUNDLE_SHA256SUMS_FINAL_SOLNARROW_20261030` | bundle as Sol's narrow check verified it and as the dev run `20261030T1855Z_bench_f3v2_dev` was prepared from (28 entries, d5da3b0d…c4d4) |
