Verdict: ACCEPT WITH FIXES

Independent Sol 6.1 review, round 2 (final full round), 2026-11-02. Paths below are relative to `analysis/L_20261102`. This verdict covers the current benchmark-pending deliverables. All eight R1 findings are RESOLVED; the optional pooled-percent clarification is also resolved. No class (i) finding. One new class (ii) finding concerns the planned benchmark rendering, not today's numerical results.

## Status of R1 findings

1. **RESOLVED ? own-chunk merge and benchmark duplication.** `scripts/merge_chunks.R:27?55` filters accuracy, selection, reference, theory and stability by the owning chunk before concatenation. Selection is then checked for unique `(case_id, method_id, rule_id)` keys and roster ? required-registry coverage. Accuracy has a `(case_id, rep)` uniqueness check; nonempty theory must cover the roster exactly once. Diagnostics are deduplicated. The fix retains the correctly scored owning row rather than arbitrarily deduplicating conflicting rows. I independently SHA-256-compared all 14 CSVs in `score_final/` against `work/score_final_r1fix/`: all are byte-identical. I read the synthetic test source and saved test output and independently recounted its saved case-selection CSVs: unfiltered 152 rows/76 keys, filtered 76 rows/76 keys, zero failed filtered rows. The test exercises the same own-filter logic on two chunks, although it is not an end-to-end invocation of the full merger. Source inspection plus the production re-merge supports closure.

2. **RESOLVED ? T37 sufficiency and mechanism overclaims.** `EVIDENCE_L.md`, T37, now distinguishes observed association from logical necessity and a proved sufficient condition. The 1,511 d=1 successes are described as consistent with the proposed implication; the toward form needs assumptions and proof. Literal premise failure is explicitly not theorem refutation. First-score attribution is correctly limited and leaves a possible later local-search role open.

3. **RESOLVED ? T37 counts.** The report now gives 992,065 d=1 violating centres (991,882 a/b plus 183 at truth) and 930 d=2 hits violating toward TD. These agree with the inspected `evidence/td.csv` and `evidence/td_vs_outcome.csv` overall rows.

4. **RESOLVED ? bias and consistency claims.** `HEADLINE_L.md` and its renderer now describe similar seed spread/RMSE as compatible with seed variability dominating. `EVIDENCE_L.md`, T26/T12, explicitly permits case-specific bias and aggregate cancellation, uses compatibility with zero for pooled bias, attributes ?Var/2 to a second-order approximation, and remains silent on consistency/rates. These changes address the requested inference limits.

5. **RESOLVED ? start-mass association and phase attribution.** T22/T27 includes the p=30/c050 contrast, 76.6% versus 98.0%, and states that SMC matches exact HPM across the classes without claiming start mass is irrelevant. The pilot-first-scoring wording replaces the unsupported bridge claim. The stratified values and pooled counts agree with `evidence/recovery_by_pi0.csv`.

6. **RESOLVED ? coverage and first-score summaries.** T21 now reports median coverage 0.99995, minimum 0.9980, all cases ?0.99 and 99.8% ?0.999. Its pilot mechanism counts (1,304/1,038/31/26/1) agree with `evidence/truth_first.csv` and sum to 2,400. The distinction between scoring and particle visitation/retention is explicit.

7. **RESOLVED ? six-fit stability disclosure.** The headline explicitly identifies primary plus five extras and acknowledges the widened definition relative to the earlier brief. Extra-seed accuracy is separate. This is acceptable as disclosed; it does not purport to provide five-extras-only PIP spread.

8. **RESOLVED ? passing-only scenario disclosure.** `tables/Q4_recovery.csv` now contains `passing_S1`?`passing_S6`; `scripts/build_tables.py` checks each against H4. The headline identifies both SMC rules, S4 94/100 at p=20/c100 and S3 96/100 at p=30/c100, pooled 575/600 and 570/600, with fixed denominators. I reproduced the table calculations in memory and found no difference from the saved CSVs.

**Optional R1 clarification: RESOLVED.** The headline now says pooled, about 2.1%, and discloses the per-cell p90 reaching 0.029 (about 3%).

## Independent tie-out

**The PASS is sound for the stated 43-cell sample.** I read the brief, claims, result, report, verdict, canary key and full `code/tieout.R`. Regenerating the claim selection and perturbations in memory with seed 20261102 reproduced all claim descriptors/values and the canary key from the current tables. Thus the key agrees with the underlying table cells rather than merely with the result file. All 43 unique result rows have the required 100 or 600 cases; there are 38 MATCH, exactly five MISMATCH at cells 5, 28, 35, 37 and 41, and zero UNVERIFIED. Independently applying the specified rounding to every saved recomputation recovers every genuine claim and every canary's true value.

The worker code reads the raw manifest, SMC primary/repeat RDS records, exact enumeration records and truth. Its scale alignment, strict PIP threshold, set comparisons, max PIP errors, type-7 quantiles and six-seed sample SDs implement the brief. The selected posterior-miss cells can use complete exact enumeration plus HPM agreement; the fallback scores models using the allowed core. The start-mass cell reconstructs from X/Y, preprocessing, recorded blocks and core start functions and checks the normalizer. No scoring-pipeline or analysis-result dependency appears in the worker calculation. The copied core source files also match the allowed campaign core byte-for-byte by SHA-256.

Accordingly, the saved implementation is computationally independent under the brief's explicit allowance for the shared core. The report and verdict are consistent with that implementation. The supplied artifacts cannot prove the negative claim that the worker never opened a forbidden file; I did not inspect a complete worker tool transcript, and do not certify that behavioral claim independently. I found no evidence of an independence breach. PASS is sample validation, not independent validation of every table cell, the full TD audit, or future benchmark outputs. I did not rerun the raw-record tie-out because its script writes protected outputs.

## New findings

9. **Class (ii), should-fix before publishing the benchmark update: the generated short answer will still announce benchmarks as pending after pass C.** Location: `scripts/render_headline.py:44`, versus the conditional benchmark rendering at lines 77?84.

   Evidence: short answer 4 unconditionally appends ?The benchmark rows are **pending**: PROD_L_BENCH has not landed yet.? The later Q4 section switches to measured benchmark rows when any `n_not_run < n_pooled`. Therefore the planned merge/build/re-render alone will produce contradictory status text once benchmark records arrive. Today's pending headline is correct.

   Suggested fix: compute benchmark availability before constructing the short answers and use that same state in both locations, distinguishing pending, partial and complete availability as appropriate. A narrow renderer check with a benchmark-present table is sufficient; no new simulation is needed.

Class (i): none. Class (ii): finding 9. No additional class (iii) finding.

## Benchmark plan and verification scope

Pass C with theory off, followed by the repaired merge taking theory from pass A, table rebuild and headline render is otherwise coherent. Pass C must include all pass-B roots (including repeat fits) plus the verified benchmark root and use a fresh output name: `run_chunks.sh` deliberately skips existing successful chunks and does not invalidate them when ROOTS changes. Preserve the existing snapshots. The merger checks rep-0 equality against pass A; recheck six-fit/repeat availability and expected benchmark keys/statuses after pass C. Acceptance here does not certify benchmark data that have not landed. Address finding 9 as part of that update.

All work was local and read-only except this review file; no SSH or remote host was used. I executed the table builder, renderer and claim generator only as in-memory source prefixes stopping before filesystem writes. The builder returned zero problems/warnings, and all eight recomputed tables matched the saved tables; the generated headline matched `HEADLINE_L.md` exactly. Current saved outputs contain 2,400 roster cases, 14,400 accuracy rows and 2,400 stability rows, with unique expected selection keys. These checks supplement the saved synthetic-test recount and SHA-256 comparisons; they do not claim a fresh raw-data scoring run.
