# CONF-2b review 3: disposition (CONF-2b manager, 2026-10-29/30)

Review: `CONF2B_REVIEW3_sol.md`.

**Part A, v2.2.1: YES, ready to FREEZE.** Done.
- FROZEN section added to `code/core/v2_2_1/CHANGES_v2_2_1.md`.
- Final manifest `code/core/v2_2_1.SHA256SUMS`, sha256 d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1 (27 files). Only `CHANGES_v2_2_1.md` differs from the manifest Sol verified (df4e7cf0…).
- Diff: 527 lines.
- CODE_LEDGER entry "v2.2.1 FROZEN".
- The core is byte-identical to v2.2 (21/21 files).

**Part B, PROD-H: NOT READY, 0 blocking.** Accepted, and delegated to a Sonnet worker (`jobs/PROD_H_DRAFT/REVIEW3_FIXES.md`):

| # | Severity | Fix |
|---|---|---|
| R3-1 | should-fix | A failed scheduler query keeps the recorded scan job and resumes the same id. Retire or relaunch only once squeue and sacct prove it terminal. |
| R3-2 | should-fix | The charter disk guard sits inside `p5_scan_run.sh`'s new-job branch, before sbatch, for direct primary and final calls. |
| R3-3 | minor | `make_manifests.sh` supports and validates zero-file folders. |

Next: a narrow Sol confirmation (review 4).
