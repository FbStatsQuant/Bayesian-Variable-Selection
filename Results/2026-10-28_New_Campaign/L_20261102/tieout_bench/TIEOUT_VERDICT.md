# Benchmark tie-out verdict (pass C): PASS

- **Worker:** Terra 6.1, working locally.
- **Method:** numbers only, recomputed from the raw benchmark records (`$rows` status and support), the SMC plain PIPs and the truth. The ABESS cells were recomputed with its own exhaustive best-subset search. It did not read `code/scoring` or any ANALYSIS-L output.
- **Cells:** 25 claims, drawn by `scripts/make_bench_claims.py` (seed 20261103):
  - 21 benchmark recovery cells (all 8 headline rules plus the 3 CV sensitivities; scenario cells, pooled cells, and S1/S2 cells);
  - 2 SMC plain-MPM cells;
  - 2 ABESS exact-size cells.
- **Canaries:** 4 planted. The key was held in the session scratchpad until Terra reported, and is now copied to `CANARY_KEY.json`.

**Result: 21/21 genuine cells MATCH, including both ABESS size counts. 4/4 canaries were flagged as MISMATCH, each with the true value recovered:**

| cell | planted | true | Terra's value |
|---|---|---|---|
| 6 | 94 | 91 | 91 |
| 16 | 547 | 550 | 550 |
| 19 | 81 | 83 | 83 |
| 21 | 88 | 91 | 91 |
