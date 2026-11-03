# Tie-out verdict: PASS

- **Worker:** Terra 6.1 (codex, medium effort), working locally. Attempt 1 computed nothing: its standing config pointed it at the Owls remote host. Attempt 2 was briefed local-only.
- **Recomputed from:** the raw SMC records (primary + repeats), the EXACT records and the truth, with its own R code (`code/tieout.R`; SMC core sourced for the API only). It did not read `code/scoring` or any ANALYSIS-L output.
- **Cells:** 43, drawn at random (seed 20261102) by `scripts/make_tieout_claims.py` from the Q1–Q4, stability and theory tables. They cover Q1 bias, RMSE, p90 and coverage; Q2 percentages; Q3 RB and plain errors and MPM; Q4 recovery counts; stability; posterior-miss counts; and π₀ median.
- **Canaries:** 5 planted, at cells 5, 28, 35, 37 and 41. The key was held in the session scratchpad until Terra reported, and is now copied to `CANARY_KEY.json`.

**Result: 38/38 genuine cells MATCH. 5/5 canaries were flagged as MISMATCH, each with the true value recovered:**

| cell | planted | true | Terra's value |
|---|---|---|---|
| 5 | 0.023817 | 0.011054 | 0.0110542 |
| 28 | 125 | 100 | 100 |
| 35 | 90 | 93 | 93 |
| 37 | 0.024263 | 0.0114107 | 0.0114107 |
| 41 | 2 | 4 | 4 |

0 UNVERIFIED.
