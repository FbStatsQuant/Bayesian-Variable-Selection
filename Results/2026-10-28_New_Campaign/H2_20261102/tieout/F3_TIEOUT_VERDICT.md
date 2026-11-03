# F3 (adaptive lasso, BENCH_F3_PROD) tie-out verdict: PASS

**Worker:** Terra 6.1 (codex, high), working from the raw F3.rds rule rows and the truth with its own code (`terra_f3_code/`), not the campaign scoring code. Run locally on 2026-11-02.

**Claims:** `F3_CLAIMS.csv`, 44 cells = 41 genuine + 3 planted canaries. The key (`F3_CANARY_KEY.json`) was held outside Terra's paths until it reported. The genuine cells cover:
- all 24 per-scenario `ebic1_K37` cells;
- pooled /600 for `ebic1_K37`, `cv_min`, `cv_1se` and `ebic1` in each of the 4 p × c pools;
- the 4 D55 `lambda_last` counts.

**Result:** 41/41 genuine cells match. All 3 canaries were detected, each recomputed to its true value:

| Cell | Planted | Recomputed = true |
|---|---|---|
| 2 | 86 | 89 |
| 21 | 29 | 32 |
| 36 | 2 | 0 |

No data problems. Details: `F3_TIEOUT_REPORT.md` and `F3_TIEOUT_RESULT.csv`.
