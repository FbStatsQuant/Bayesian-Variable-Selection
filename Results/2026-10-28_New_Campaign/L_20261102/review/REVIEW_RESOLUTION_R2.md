# Resolution of Sol review R2 (final full round, HQ D53)

**Verdict: ACCEPT WITH FIXES.** All 8 R1 findings and the optional item are RESOLVED, the tie-out PASS is supported, there are no class (i) findings, and there is one new class (ii) finding.

| # | Class | Finding | Resolution | Evidence |
|---|---|---|---|---|
| 9 | ii | Short answer 4 always said the benchmarks were pending, even after benchmark rows arrive. | **Fixed.** `render_headline.py` computes one benchmark-availability state (pending / partial / complete) from `Q4_recovery.csv`. Both the short answer and the Q4 section use it. | `review/TEST_R2_FINDING9.txt` (narrow check, `scripts/test_render_bench/check_render.py`): the pending, complete and partial synthetic tables each render consistent text, and re-rendering from the real tables is byte-identical to the current `HEADLINE_L.md`. **TEST_PASS.** |

Under D53 there is no further full Sol round. Finding 9 is closed by this narrow check.

## Pass C procedure (benchmarks), incorporating Sol R2's plan notes
1. **Wait for HQ's signal** that PROD_L_BENCH has landed, then check its OPS_LOG line: PULL … VERIFIED for the benchmark results folder.
2. **Run pass C detached** under a fresh output name (`run_chunks.sh` skips finished chunks and does not invalidate them when the roots change): `run_bg.sh passC bash scripts/run_chunks.sh 6 "<enum20>,<enum30>,<smc>,<smcrep>,<bench>" passC 0`. Use Windows-form paths (`C:/…`) for every root.
3. **Merge:** `merge_chunks.R STUDY work/chunks work/passC score_final_bench work/passA`. This checks rep-0 equality with pass A. Keep `score_final/` as the benchmark-free snapshot.
4. **Rebuild and render:** `build_tables.py score_final_bench tables` (the bench rows are then cross-checked against H4), then `build_theory.py`, then `render_headline.py`.
5. **Re-check:** 14,400 accuracy rows and 2,400 stability rows; the expected benchmark keys and statuses (n_not_run, failed) per method; the F1–F3 `ebic1_K37` headline with `cv_min` as sensitivity.
6. **Benchmark tie-out:** a narrow one (Terra, about 10 benchmark cells plus canaries).
