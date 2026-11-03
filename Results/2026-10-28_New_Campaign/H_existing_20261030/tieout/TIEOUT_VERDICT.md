# Tie-out verdict (manager, 2026-10-30; wording corrected after Sol review finding 8)

- **Worker:** Terra 6.1 (high), independent of the table build. Its brief forbade reading the pipeline, the tables and the scoring code; the manager reports this, and the code alone cannot prove the worker's read history. It recomputed from the raw SMCBVS and benchmark CSVs plus the truth RDS files. Its code does not import any scoring or build code.
- **Design:** 44 targeted, seeded, stratified checks from `scripts/make_tieout_claims.py` (seed 20261030):
  - 34 exact-recovery counts: 14 SMC, 17 benchmark primary (including F4 `ebic1_K37` at c = 0.5, a registered primary) and 3 supplementary (F1 `cv_1se`, SSL-RS, SuSiE-refine);
  - 4 FP/FN/error-type cells;
  - 2 diag_flag cells;
  - 2 paired cells;
  - 2 fixed reconciliation checks.

  Not sampled: any c = 1 post hoc K37 exact cell, and the F5 `ebic1_K37` exact cell at c = 0.5.
- **Canaries:** 5 claimed values were planted wrong (key: `CANARY_KEY.json`). The worker flagged exactly those 5 (cells 1, 10, 12, 30, 35), and its recomputed value equals the true value in every case (370, 93, 93, 0, 0.05).
- **The other 39 cells:** all match.
- **Truth:** all 1,200 truth RDS files agree with `truth_manifest.csv`.

**Verdict: PASS for the checked scoring claims, including canary detection.** It is not an exhaustive check and does not certify the fitting code.
