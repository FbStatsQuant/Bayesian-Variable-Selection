# Independent review (d): scoring and metrics

**Verdict: REJECT.** The ordinary-case formulas are largely sound, but missing main fits disappear from headline denominators, numeric empty exact supports become missing, and the dropped-truth theory branch is incorrect. Resolve the blocking findings and rerun independent checks before accepting production tables.

Reviewer: Sol 6.1, acting independently; no subagents. Review completed 2026-10-28 America/Chicago (2026-10-29 UTC). No reviewed file was edited.

## Scope and reproducible evidence

Read the scoring tree and the named contracts, master excerpts, T37 definition, enumerator R API/README, schema and native assembly files. `conformance/OUTPUT_FIELDS.md` does not exist. Findings below use paths relative to `CAMP/code/scoring/` unless stated otherwise; line numbers refer to the preserved snapshot.

Scratch/evidence root: `<PC_TEMP_PATH>`.

- `review_checks.R`, `extra_checks.R`: independent adversarial checks, seed **20261028**; R **4.4.1**, Windows, one thread for OMP/BLAS/MKL. Both final executions exited **0**, taking approximately **7.7 s** and **5.3 s**. The second script also reruns the first script.
- `review_checks.log`, `extra_checks.log`, `run_status.json`, `extra_status.json`: inspected output, UTC timestamps, process IDs, session/package details, commands and exit statuses. Earlier exploratory attempts are preserved separately, including a corrected final-print syntax error in the reviewer script.
- `synthetic/`, `output/`, `observations.rds`, `observations_extra.rds`: generated inputs, injected records, actual pipeline CSV/Markdown output, and saved measurements. Synthetic study: four datasets, two paired scales; valid, absent-main, failed-main and NA-evidence cases, plus a failed repeat. Separate in-memory grid: six scenarios × 100 datasets × two scales.
- `snapshot/scoring/`, `source_hashes_before.csv`, `source_integrity.csv`: source snapshots and SHA-256 comparison; **22/22 scoring files unchanged**. `evidence_sha256.csv` inventories the saved review evidence.

Commands executed, with scratch TEMP/TMP/TMPDIR and thread counts set by the launcher:

```text
"C:/Program Files/R/R-4.4.1/bin/Rscript.exe" --vanilla "<PC_TEMP_PATH>"
"C:/Program Files/R/R-4.4.1/bin/Rscript.exe" --vanilla "<PC_TEMP_PATH>"
```

These are synthetic scoring checks. I sourced the unchanged scoring functions and injected explicit mathematical scorer/setup APIs to avoid reading unlisted core compilation dependencies. I did **not** run a real fit, compile C++, use SSH, or rerun the author's full suite: that suite writes reviewed reports and loads dependencies outside the allowed paths. Its reported 92/92 result and real-p20 integration report were read, not independently reproduced. The C++ result normalization was checked using its documented return shape; actual C++ TD execution remains outside this review's dynamic coverage.

## Findings

1. **Blocking — missing main fits are excluded from H1–H3 instead of retained.**

   **Location:** `R/tables.R:9–13`; `run_scoring.R:45–55,76–83`.

   `has_exact` is carried only on an existing accuracy row. After the left join, an absent main fit gets `has_exact=FALSE` and is filtered out, even when its dataset has an exact reference. A case with repeat fits but no main fit has the same problem. If no SMC accuracy rows exist, the runner does not create H1–H3 or HEADLINE at all.

   **Evidence:** `missing_main_H2` / `missing_main_and_NA_Z_H1`: each scale has four expected cases and four exact references, but H1/H2 report **n_cases=3**. Two known SMC HPM hits become **66.6667%**, instead of **2/4=50%**. H4 correctly reports **2/4**, exposing disagreement between headline tables.

   **Fix:** join reference availability and exact-vs-truth quantities from a separate expected-case/reference table; synthesize a failed/missing main-fit row independently of `acc`. Generate all headline tables even when every SMC output is missing. Add a regression with an absent main, an available exact reference, and a repeat-only case.

2. **Blocking — empty integer supports from the real exact API become missing.**

   **Location:** `R/common.R:15–20`; `R/extract_exact.R:19`; `R/metrics_selection.R:13,41–44`. Producer: `CAMP/code/lowp/enum/lowp_enum.R:151–154`.

   `parse_support(integer(0))` returns NULL before distinguishing an empty numeric support from missing. The enumerator returns integer supports, including `integer(0)` for an empty MPM. Exact empty HPM/MPM comparisons therefore become NA or FALSE; reference selections are classified as failed. This affects legitimate nonempty-truth cases whenever the exact MPM is empty, not just null-truth fixtures.

   **Evidence:** `empty_exact_support` confirms numeric-empty → NULL, text-empty → integer(0), NA → NULL. `empty_exact_reference_rows`, with known empty truth and exact supports, produces **two `status=ok`, `k=NA`, `exact=FALSE`, `error_type=failed` rows**; both should be successful empty selections with exact recovery.

   **Fix:** preserve zero-length numeric/integer supports; reserve NULL/NA for unavailable support. Test actual integer exact outputs, empty HPM, empty MPM, empty truth, and CSV text-empty versus NA separately.

3. **Blocking — a dropped true variable invalidates the theory wrapper and incorrectly zeros all near-truth region masses.**

   **Location:** `R/theory_measures.R:107,114–122,126–132`; `THEORY_MEASURES.md` dropped-variable rule; `run_scoring.R:62–63`.

   An unavailable full truth has π₀(S₀)=0, but R_d contains **subsets** of S₀, including the empty model and retained true-only subsets. Its intersection with the feasible model space need not have zero mass. The code zeros π₀(R₀), π₀(R₁), π₀(R₂). With a completed fit, `F_truth=NA` additionally reaches `if (F_truth > F_hpm)` and throws, so the runner logs an error and omits the whole theory row.

   **Evidence:** independent six-variable block tables, S₀={2,7}, retained variables 1:6: wrapper returns **(0,0,0)**; explicit summation gives **(0.5262586669022963, 0.7885557028535969, 0.9173298220617911)**. `dropped_truth_with_completed_fit` returns **“missing value where TRUE/FALSE needed”**.

   **Fix:** compute region mass over feasible retained supports, using retained truths to classify block members; keep full-truth mass zero and mark TD undefined when appropriate. Guard unavailable truth scores and preserve a theory row with explicit availability/status fields. Correct the documentation and test with a genuinely dropped column, such as a constant column.

4. **Should-fix — unavailable evidence remains `ok`; summary validity and coverage denominators are inconsistent.**

   **Location:** `R/extract_smc.R:88–95,118–122`; `R/metrics_smc.R:41–46`; `R/tables.R:19–22,36–43`; `METRICS.md` and `R/tables.R:63` denominator promises.

   `ok` trusts status/availability without validating each estimate. H1 mixes NA-dropping helpers with `mean`/`median` calls that retain NA. H3's `n_ok` need not equal the number contributing RB or plain errors. Lower-bound coverage is conditional on `ok`, whereas the documentation says failed/missing fits stay in every rate denominator.

   **Evidence:** an injected completed record with `log_Z=NA` remains **ok=TRUE**. H1 reports **n_ok=2**, bias **0.1**, p90 **0.1**, but **RMSE, median absolute error and lb_coverage are NA**. Only one fit has usable evidence. A two-island record is also accepted and receives `sd/2`, despite the documented four-island statistic (`two_islands_divided_by_two`).

   **Fix:** validate fields and report per-metric contributing counts (`n_evidence`, `n_rb`, `n_plain`, etc.). Require four valid islands for the prescribed island statistic. Define coverage explicitly as either a fixed-case rate with unavailable cases separately counted, or conditional coverage with its own denominator; make code and prose agree. Do not infer that an unavailable evidence field invalidates an otherwise valid HPM.

5. **Should-fix — expected datasets and method/rule roster are inferred from observed files.**

   **Location:** `run_scoring.R:25–31`; `R/truth.R:16–19`; `R/metrics_selection.R:25–28`; `R/tables.R:49–50`.

   Missing rows are synthesized only for methods/rules observed somewhere, and only for datasets with a present truth file. An entirely absent benchmark method vanishes instead of reporting 0/100 and 0/600. A missing truth file silently removes the dataset; `--cases` only filters that already-reduced roster. No production completeness check enforces the campaign's 100/600 cells.

   **Evidence:** the independent 1,200-case grid correctly gives **1/100 and 1/600** for a method with one saved success, with scales separated. However, its method roster contains only **LASSO**; every wholly absent method has **no row** (`absent_methods_not_created`). The four-dataset pipeline willingly labels arbitrary observed cell sizes in HEADLINE.

   **Fix:** supply the planned case grid and expected primary method/rule roster explicitly, with a clearly labelled partial-study/test mode. Missing truth should trigger an explicit scoring-completeness error/status, not reduce the denominator. Instantiate all planned missing fit pairs as not_run.

6. **Should-fix — duplicate result roots overweight main fits and repeat-seed stability; selection silently chooses a winner.**

   **Location:** `R/extract_bench.R:20–38`; `run_scoring.R:34,50–57`; `R/tables.R:10`; `R/metrics_selection.R:22–24`.

   The documented multi-root input can contain the same (case, rep) more than once. Main-fit joins retain duplicates; seed stability treats duplicates as additional fits. Selection, inconsistently, keeps the last conflicting (case, method, rule) row without recording the conflict. Exact references likewise use the last dataset path.

   **Evidence:** adding one duplicate of a successful main row changes H2 from **n=3, 66.6667%** to **n=4, 75%**, with no new case or seed (`duplicate_main_H2`).

   **Fix:** resolve units before scoring using case/rep/method_seed and immutable output identity. Deduplicate identical copies, reject conflicting copies or require an explicit recorded precedence rule. Assert unique main-case keys and distinct repeat seeds.

7. **Should-fix — exact PIP extraction discards the original-index map on dropped columns.**

   **Location:** `R/extract_exact.R:16–18`; producer `CAMP/code/lowp/enum/lowp_enum.R:150–154`; enumerator README preprocessing contract.

   The real API names retained PIPs by original index. `exact_scale()` removes those names and relabels 1:length, without expanding to input p. Against a correctly expanded SMC vector, errors become unavailable; the extracted reference itself also misstates variable identities.

   **Evidence:** exact PIPs **c(`1`=.8, `4`=.2)** become **c(`1`=.8, `2`=.2)**. A matching SMC vector **(.8,0,0,.2)** produces **all NA RB error summaries**, instead of zero (`exact_dropped_columns`).

   **Fix:** preserve and validate original names, expand the exact PIPs to original input p with zeros for confirmed dropped columns, and check the retained map. Test nonconsecutive retained indices through the actual API-shaped output.

8. **Should-fix — extraction can manufacture valid-looking values from incomplete fields.**

   **Location:** `R/extract_smc.R:65–76,91–98,107–110,133`; `R/metrics_smc.R:71,77`.

   The native path lookup is isolated and uses exact names, which is good. Subsequent expansion/reduction is less safe: a named partial PIP is assumed to describe every retained variable; no-final-stage tables fall back to calibration; all-NA costs become numbers. Missing reference supports are reported as FALSE for exact-vs-truth equality rather than NA.

   **Evidence:** with `kept=1:4`, a retained vector containing only names {1,4} becomes **(.2,0,0,.8)**, inventing zero PIPs for retained variables 2 and 3. A diag-only stage table reports **min_ess=1** as final cost. All-NA ESS/fresh counts yield **Inf / 0**. An unavailable exact HPM/MPM yields **exact_hpm_eq_truth=FALSE / exact_mpm_eq_truth=FALSE**, although SMC-vs-exact equalities are NA.

   **Fix:** require the vector/matrix names to cover exactly `kept`, validate dimensions/ranges, and expand zeros only for confirmed dropped predictors. Select final stages strictly; keep absent/all-NA costs as NA. Use availability-aware equality for reference-vs-truth too. Add malformed/absent-field tests rather than accepting plausible defaults.

9. **Should-fix — the master-required passing-only recovery counts are absent.**

   **Location:** `R/tables.R:47–51`; master **§IV.1.3, line 2371**.

   `diag_flag` survives in case_selection, but H4 only reports all-saved recovery. The master requires all-saved and passing-only counts, both with the full 100/600 denominator. Charter's fourth question can accommodate these as recovery columns; diagnostic theory/cost tables need not be added to HEADLINE.

   **Evidence:** a flagged exact success yields the sole recovery **1/100**. Required passing-only recovery is **0/100**, but no corresponding column/table exists (`flagged_recovery_only_one_version`).

   **Fix:** add explicitly named all-saved and passing-only recovery counts at the same fixed denominator, and preserve separate failure counts. No supplied decision explicitly removes this denominator rule.

10. **Should-fix — EXACT readiness is not enforced.**

    **Location:** `R/extract_bench.R:18,29–30`; `R/extract_exact.R:7–10`.

    The scanner promises a unit counts only with `.done`, but the EXACT branch bypasses that check. The enumerator API README specifies `.done` last. A readable uncommitted or abandoned exact RDS is accepted as the definitive reference.

    **Evidence:** `exact_without_done_is_used` returns the injected EXACT path with **no EXACT.done present**.

    **Fix:** require the completion marker for exact units too and validate the envelope's schema/dataset/scale identity. Treat a present but uncommitted reference as unavailable with an explicit diagnostic.

11. **Minor — repeat-seed summaries do not meet their documented eligibility/count contract.**

    **Location:** `R/metrics_smc.R:92–105`; `run_scoring.R:57`; `METRICS.md` “cases with >=2 completed fits”.

    The caller checks the count before completed-fit filtering; the function permits one remaining fit. For ragged fields, NULL PIP vectors are dropped by cbind but a single common `n_fits` is reported.

    **Evidence:** one completed main plus one failed repeat writes a stability row with **n_fits=1**. Three completed records, one lacking both PIP vectors, report **n_fits=3**, while both PIP SDs use **two** vectors; the measured RB SD is **0.0707106781**. A genuinely missing repeat file creates no synthetic repeat or availability count.

    **Fix:** require two eligible distinct seeds after filtering, and report attempted/completed and per-metric seed counts. Define the expected repeat roster if missing-repeat reporting is required. The two-complete-seed baseline itself passes: log-Z SD **0.7071067812**, agreement **1**, RB SD **0.0707106781**, plain SD **0.1414213562**.

12. **Minor — slow TD does not skip infeasible centres above K.**

    **Location:** `R/td_slow.R:30,48–51`; contrast `CAMP/code/lowp/enum/lowp_enum.R:183–185`.

    The documented capped-centre API promises |S|≤K, and the enumerator counts only those centres. The R engine constructs all U/P combinations and calls F before checking feasibility. This is outside T37's assumption s₀+d≤K, but within the broader capped API description.

    **Evidence:** p=4, K=2, S₀={1,2}, d=1 reaches a three-variable centre and throws **“infeasible centre”** with the independent scorer. The supplied K-cap tests only reach equality, s₀+d=K.

    **Fix:** filter centres to |S|≤K before scoring and update total/done counts, or reject the unsupported request explicitly and consistently across engines.

## What passed and what the existing tests miss

For complete, correctly mapped inputs, the implementations match their stated formulas and the master scale convention:

- Full-scale log-Z subtraction, `expm1(e)`, log(.05) lower-bound direction and inclusive boundary, four-island sample SD and SD/2; no extra m(empty) multiplier is introduced. Hand example: e **0.1**, SE **0.1290994449**.
- RB/plain pooled absolute PIP errors and true/null splits; island maximum errors and mean summaries. Independent nonzero RB example: max **.3**, overall mean **.1625**, true mean **.075**, null mean **.25**. Plain means are **.15/.2/.1** (overall/true/null). PIP=.5 is excluded from the MPM.
- HPM/MPM set equalities on known nonempty supports, score gap, and posterior truth mass `exp(F(S₀)-log Z)`: hand mass **0.2835788993**. A wrong support tied in F gives **gap=0**, **HPM equality=FALSE**, and the declared **posterior_miss** classification. Strictly lower-scoring HPMs use search_miss; no tolerance replaces support equality.
- Distinct-scored-set mass uses the full F scale: injected coverage **.75** is recovered. One inconsistency remains: a failed partial fit's same saved mass gives **.75** in case_smc_accuracy but **NA** in case_theory (`R/metrics_smc.R:58` versus `R/theory_measures.R:135–137`). Clarify whether partial-fit coverage/trace is retained or unavailable and apply the policy consistently.
- Explicit brute-force summation over all 64 models agrees with the block DP, including a K=3 cap, to **1.11e-16**. For K=6, π₀(R₀,R₁,R₂) is **(.5676320453,.8364039235,.9525672545)**; for K=3, **(.5952093015,.8770389184,.9839566946)**. π₀(S₀)'s table formula also agrees.
- Independent TD neighbour enumeration agrees with the R engine for both literal and toward variants on a random p=5 score table and an all-tied capped p=4 table. Random literal clause-a violations **19/21**, toward **17/21**; tied clause counts **(9,2,1)** with **zero violations**, every centre tight, and both carried `holds_strict=FALSE`. Documented enum normalization preserves violation/tight counts. `run_theory_H.R` function and CLI default to **d=0**, restricted d=1 opt-in; full-null moves remain available at d=0.
- TP/FP/FN and none/extra_only/missed_only/mixed/failed classification pass on independently constructed supports. Failed/timeout/not_run saved rows stay as non-recoveries; valid text-empty support is not NA. With an explicit complete grid and a seen method, H4 produces /100 and /600 correctly.
- Independent flag×event fixture has one case in each quadrant, one omitted NA flag: **n=4**, sensitivity=specificity=PPV=**.5**. Existing pooling is descriptive per fit as documented. H1–H4 group by scale; scenario pooling does **not** combine the paired scales or repeat seeds. HEADLINE has exactly the four charter sections and excludes theory/cost/stability diagnostics, subject to the denominator and completeness findings above.
- In the permitted fitting/assembly/API files, no production code reads truth or writes it into fit outputs. Scoring reads sealed truth after fit loading; reconstructed contexts do not modify/save fits. The optional truth_trace field is only consumed; ordinary trace lookup is post-fit over scored_set. This is a scoped truth-separation check, not an audit of unlisted fitting files.

The author's suite is useful for ordinary arithmetic, but several assertions are weaker than their labels:

- `tests/make_fixtures.R:41–42` uses **text** exact supports, masking the real API's numeric-empty defect. `test_scoring.R:386–387` checks only failed-row k is NA; it never round-trips a known successful empty selection.
- All main SMC files exist in the supplied fixture; its one failed file does not exercise an absent file. Methods are all observed somewhere, truth is complete, repeats are uniformly available, and there are no duplicate roots. Thus the headline denominator test at `test_scoring.R:224` does not cover the missing-main bug.
- `test_scoring.R:263–265` duplicates a predictor and explicitly allows `S0_retained=TRUE`. It need not drop anything and does not assert near-truth masses. Use a constant true column and independently sum feasible region mass.
- `tests/make_fixtures.R:36` orders tied equal-size supports by numeric mask, which is **not** master's original-index lexicographic order: {1,4} (mask 9) precedes {2,3} (mask 6) lexicographically. Add deliberate exact ties with a separately computed correct order. Existing random data almost never exercise ties.
- `test_scoring.R:120` claims “both miss classes” but tests only `hit` and `search_miss`; it never requires posterior_miss. `test_scoring.R:145–148` checks sensitivity/specificity but omits PPV. The independent checks above cover those gaps.
- `tests/integration_real_p20.R` prints its final coverage/block/F/lower-bound checks rather than asserting them, and uses a hand-built envelope rather than the adapter itself. Its real-p20 report is valuable evidence for ordinary field names, not coverage of malformed or partial envelopes.

## Compact summary

**REJECT: three blocking findings, seven should-fix findings, two minor findings.** Ordinary formulas, independent DP, literal/toward TD, selection arithmetic, paired-scale grouping and scoped truth separation pass. Headline denominator integrity, real empty exact supports and dropped-truth theory handling must be corrected first; missing-data/roster/duplicate/readiness safeguards then need regression coverage. All reviewed scoring files remain unchanged; runnable synthetic evidence is saved in the designated scratch folder.
