# Historical bundle ledgers (do not verify current files against these)

The authoritative ledger is `../BUNDLE_SHA256SUMS_FINAL` (written 2026-11-02 after the HQ D64 resource fill).

| File | State it records |
|---|---|
| `BUNDLE_SHA256SUMS_prefreeze_20261030` | pre-freeze draft (placeholder `freeze.json`) |
| `BUNDLE_SHA256SUMS_FINAL_R2REVIEWED_20261030` | bundle as Sol review 2 saw it (before the R2-1/2/3 fixes); digest b81e3009…66e7 |
| `BUNDLE_SHA256SUMS_FINAL_SOLNARROW_20261030` | bundle as Sol's narrow check verified it (65 entries, 9129e5df…4827); differs from the current bundle only in `runner/resources.json` (D64 values), `tests/test_workflow.py` (the expected wall-time literal), `JOB.md`, and the archived ledgers' locations |
