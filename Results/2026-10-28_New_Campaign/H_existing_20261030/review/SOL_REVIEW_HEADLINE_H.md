ACCEPT WITH FIXES

Independent Sol review of the existing-fit deliverable. The numerical headline is sound and suitable for the PI meeting after the presentation and evidence qualifications below are corrected. No deliverable was edited. Checks used read-only `py -3 -I` against the permitted saved files; no fits, simulations, network access, or SSH were used.

1. **Severity: should-fix — The headline omits preregistered companion-rule presentation.**

   **Location:** `HEADLINE_H.md` §§1–2 and Files; `BENCH_OPEN_ITEMS.md` §3; `PREREG_c050.md` R2 and R4.

   **Evidence:** R2 explicitly requires every headline table to show F1–F3 `cv_min`, `cv_1se`, and `ebic1_K37` side by side with equal prominence. The headline shows only `cv_min`, relegating companions to a CSV reference. These are materially different results: F3 at p500, c=1 has 0/600, 9/600, and 247/600 respectively; F1's EBIC-K37 totals are 111/89 at c=1 and 24/15 at c=0.5. R4 also requires SuSiE-refine beside default SuSiE, with the c=1 arm's retrospective addition disclosed. No such companion appears in the main tables. The chosen primary rules themselves are correct.

   **Exact fix:** Add adjacent companion rows/panels from `all_rules_recovery_long.csv` for those three F-family rules, and SuSiE-refine `pip05` beside A1, without changing which rules determine the primary comparison/rank. Preserve the supplied pre-registered/post-hoc labels, including the c=1 refine label “arm added after the c=1 results were seen; fit selection by ELBO.” Explicitly qualify the frequentist comparison as a comparison of registered primary rules. A reference to an ancillary CSV alone does not meet R2's equal-prominence requirement.

2. **Severity: should-fix — The lasso/elastic-net error description is false and conflates two CV rules.**

   **Location:** `BENCH_FLAGS.md` Flag 3, line 65; related wording in `HEADLINE_H.md` §4, line 89.

   **Evidence:** Zero exact recoveries under both F1/F2 CV rules is correct. “They always include the truth” is not: for `cv_min`, F1 has 1/47/68 mixed-error fits in p500 c=1 / p500 c=0.5 / p1000 c=0.5; F2 has 1/46/67. Pooled weak-signal mean FN reaches 0.125 for `cv_min` and 0.255 for `cv_1se`. The approximately 53–80 mean FP range describes `cv_min`; `cv_1se` means are approximately 24–40. All are visible in `all_rules_recovery_long.csv` and the primary error table. The main headline's “always add variables” does hold for its `cv_min` rows; it should not be read as “always retains every truth variable.”

   **Exact fix:** Replace the Flag 3 observation with: “F1 and F2 have 0/2,400 exact recoveries under each CV rule. Every cv_min selection adds false positives, and some also omit true variables. Pooled mean FP is about 53–80 under cv_min and 24–40 under cv_1se.” Label the headline sentence explicitly `CV-min`.

3. **Severity: should-fix — SSL-RS pooled errors are described using a scenario-specific zero-FP fact.**

   **Location:** `BENCH_FLAGS.md` watch list, lines 77–80.

   **Evidence:** The 32/600 weak-signal totals and 593/592 strong-signal totals are correct. However, pooled c=0.5 SSL-RS has 499/497 missed-only errors and 69/71 mixed errors at p500/p1000, with mean FP 0.1383/0.1600. Thus the pooled misses are not all FP=0. Scenario 1 alone has 10/100 recoveries at each p, 90 missed-only errors, FP=0, and mean FN 2.61/3.55. “S1” is also used as a supplementary-role code, making this passage unnecessarily ambiguous.

   **Exact fix:** Keep the pooled totals, followed by: “Most pooled misses omit variables; 69/71 also add false positives. In scenario 1 specifically, recovery is 10/100 at each p, all 90 misses are strict subsets of truth, mean FP=0, and mean FN=2.61/3.55.” Spell out “scenario 1” when discussing that scenario, and identify the supplementary role separately if needed.

4. **Severity: should-fix — G5 coverage is understated for F3 and ambiguously described for the weak-signal MCP primary.**

   **Location:** `BENCH_FLAGS.md` Flag 1, line 34; `BENCH_OPEN_ITEMS.md` §2, line 33; `HEADLINE_H.md` §6.

   **Evidence:** “Only the primary point was checked” is not the G5 finding. The cited c050 G5 report states that F1–F3 had 144 independently solved rule comparisons per method across six raw/derived targets, all with matching supports. Twenty-four original cv_min coefficient comparisons also pass; 120 nonprimary comparisons are support-only. All-case F3 checks include ridge choice, weights and CV arithmetic. For MCP/SCAD, the report explicitly says coefficient certification is at raw `ebic1` only, excluding K37 and lam005. Consequently c=0.5 MCP's registered headline primary, `ebic1_K37`, is itself outside the saved-vector certification. “Non-primary rules were not saved” can conceal that distinction.

   **Exact fix:** Replace the F3 statement with: “G5 is PARTIAL because nonprimary original coefficient vectors are unavailable; all-case rule/weight/CV checks and sampled primary coefficient checks pass, and the c050 sampled nonprimary supports also reproduce.” In both caveat summaries add: “For MCP/SCAD, saved-vector checks cover raw ebic1, not K37; therefore the c=0.5 MCP headline primary lacks that coefficient-level certification.” Describe the proposed F3 checks as additional probes of tuning/fold handling, acknowledging the arithmetic already audited.

5. **Severity: should-fix — Literature and causal claims exceed the evidence supplied for the audit priorities.**

   **Location:** `BENCH_FLAGS.md` lines 28–33, 56, 67–71, and 75–85.

   **Evidence:** The file declares its evidence to be scored outputs and verification reports, but adds unlinked theoretical claims, unspecified project-memory quotations/October 7 results, and an unidentified “Kollipara et al.” assertion. No supplied source establishes that oracle-property conditions apply to these finite-sample CV-tuned fits, or that reweighting “should remove most” false positives here. Likewise G5 reproducibility does not establish why a method performs poorly. L=50 exceeding truth size 14 does not by itself exclude capacity/optimization effects. The ABESS search witnesses are strong direct evidence, but they do not establish a change in exact recovery under better search; the G5 reports explicitly preserve that limitation. The cited papers were not independently verified, consistent with this review's no-network scope.

   **Exact fix:** Base priorities on the observed counts and explicit G5 evidence. Replace the adaptive-lasso rationale with: “The observed CV-min over-selection and its weaker EBIC recovery motivate a tuning/implementation audit; these counts alone do not diagnose a defect.” Replace “probably/likely the method” with “rule/algorithm-behaviour hypothesis; cause not established.” Remove the unsupported memory/October 7/Kollipara sentences and theoretical performance expectations, or supply exact source locations and applicable conditions before using them. State the SSL ladder and horseshoe explanations as hypotheses, and replace the SuSiE capacity assertion with “L exceeds the truth size, but this does not diagnose the cause.” Retain the ABESS witnesses and add: “A lower-RSS same-size subset does not establish improved truth recovery.”

6. **Severity: should-fix — The rerun is presented as an observed reproduction.**

   **Location:** `HEADLINE_H.md` Sources, line 5.

   **Evidence:** This deliverable and all inspected numerical evidence concern the 2026-10-28 existing-fit scoring passes. D23 approves a rerun; the inspected decision log also records readiness problems. D10 expressly excludes wall-clock guard stops from the conditional identity guarantee. No completed full-rerun comparison is supplied here. The wording echoes D23, but approval/expected identity is not saved evidence of an executed reproduction, especially for stopped fits and retries.

   **Exact fix:** Replace the last Sources sentence with: “These tables use the existing fits. D23 approves a rerun to collect additional outputs; agreement of its completed results with these tables remains to be checked. Original outcomes remain primary, with doubled-allocation retries reported separately under D11.” Do not alter any existing-fit recovery count.

7. **Severity: minor — An EBIC-K37 equality explanation is too broad.**

   **Location:** `BENCH_OPEN_ITEMS.md` §3, line 52.

   **Evidence:** Exact-recovery counts do agree for F1–F3's capped/uncapped EBIC pairs. The assertion that no EBIC choice exceeds 37 is false across both scales/all EBIC rules: F3 `ebic05`, p1000_S6_r079_c100, selects k=40 in the permitted joined-scored input. At p1000 c=1 its uncapped/capped pooled mean FP changes 3.385→3.345 and mean FN 0.1733→0.1767; extra-only/mixed counts also change, while exact recovery stays 91/600.

   **Exact fix:** Replace the sentence with: “F1–F3 capped and uncapped EBIC rules have the same exact-recovery counts in these tables. This does not imply identical selections or error breakdowns; F3 ebic05 at p1000, c=1 contains a k=40 choice and changes under K37.” If the intended statement concerns only c=0.5 or only ebic1, state that scope explicitly.

8. **Severity: minor — Tie-out PASS is justified for the sample, but its coverage classification is inaccurate.**

   **Location:** `tieout/TIEOUT_VERDICT.md` lines 4–5; `scripts/make_tieout_claims.py` sensitivity comment; `PROGRESS.md` item 8.

   **Evidence:** All 44 result rows align with the claim file. Exactly cells 1, 10, 12, 30 and 35 mismatch; every correction equals the canary key (370, 93, 93, 0, 0.05). The other 39 agree. The worker's code independently compares saved supports with R-extracted truth and does not import the scoring/build code. This supports a sampled scoring tie-out PASS, not certification of benchmark fitting or exhaustive checking. However cell 32, F4 `ebic1_K37` c050, is a registered primary, not a sensitivity/post-hoc rule. Actual exact-count coverage is 14 SMC, 17 benchmark-primary, 3 supplementary; no c=1 post-hoc K37 exact cell or weak-signal F5 K37 exact cell was sampled. Reconciliation cells are fixed, while other groups are seeded/stratified; “44 drawn at random” is imprecise. Blinding is reported by the manager; the code alone cannot prove the worker's read history.

   **Exact fix:** Describe the design as “44 targeted/seeded stratified checks, including two fixed reconciliation checks,” and correct the 14/17/3 classification. State: “PASS for the checked scoring claims, including canary detection; not an exhaustive result or fitting-code certificate.” Keep the canary mismatch evidence intact. Do not claim a c=1 K37 or weak-F5-primary independent raw tie-out unless a separately identified additional check is performed.

9. **Severity: minor — The main benchmark table lacks its own stated disclosure and ABESS label.**

   **Location:** `HEADLINE_H.md` introductory Columns and §6; `BENCH_OPEN_ITEMS.md` lines 39–41; `PREREG_c050.md` R7.

   **Evidence:** The main report does disclose G5 PARTIAL/ABESS search failure, but omits the AI-written/provisional disclosure that its own open-items file says accompanies any benchmark table. R7 specifies the label “ABESS (splicing heuristic).” Neither “PASS” for Bayesian reproduction nor correct scoring removes the separate code-review qualification in the cited scoring summary.

   **Exact fix:** Add near the tables: “Benchmark code is AI-written; frequentist G5 reproduction is partial, and ABESS fails the independent same-size search check. These caveats qualify the comparisons.” Label the ABESS rows “ABESS (splicing heuristic)” with the applicable primary rule/size cap. Retain the more detailed §6 caveats.

10. **Severity: minor — Merge sanity checks are logged but do not enforce their requirements.**

    **Location:** `scripts/build_headline.py` lines 38–52 and paired merge.

    **Evidence:** Current inputs pass: all 1,400 benchmark aggregate rows agree across passes in every column, not just the tested numeric subset; all 120,000 benchmark joined rows agree in the inspected relevant fields; other-p SMC aggregate rows are all missing. However `same=False` or a failed other-p check would still write output. The current code also omits FP/FN summaries from its cross-pass equality check and does not request one-to-one validation on paired joins. Actual saved keys/joins are unique, so this is hardening rather than a discovered numerical defect.

    **Exact fix:** Before writing tables, assert full intended benchmark equality (including error summaries), expected key coverage/uniqueness, wrong-pass all-missing status, and denominators 100/600. Use `validate='one_to_one'` in paired merges. Preserve the existing checks JSON. These changes need not alter the current output values.

11. **Severity: minor — The scenario-gain range lacks its comparator.**

    **Location:** `HEADLINE_H.md` §4, line 68, immediately after the paired SuSiE comparison.

    **Evidence:** +11 to +23 in S3/S4/S6 is correct against the best benchmark separately in each cell (`smc_vs_best_benchmark.csv`). It is not that range against SSL (p500 S6 is +24), and is not the largest-gain description against SuSiE (p500 S5 is +56). The immediately preceding sentence invites the latter reading.

    **Exact fix:** Replace with: “Relative to the best benchmark separately in each cell, HPM gains in S3, S4 and S6 range from 11 to 23 datasets.”

Verification supporting the verdict:

- All 280 printed numeric entries in §§1–2 match `headline_recovery_long.csv`; all 280 long-table rows also reproduce from the appropriate joined-scored rows. Per-scenario/pooled denominators are 100/600 and pooled counts equal the six scenario sums. The merged 1,456 all-rule aggregate rows exactly match the intended source-pass combination.
- Every recovery percentage/count pair in §3, the paired counts/error table/ranks in §4, and the fit accounting/flag-rate/flag-conditioned counts in §5 agree with the tables. All 448 paired contingency rows were independently recomputed using unique case joins. HPM is first/tied in 11/12 weak-signal cells, fourth of nine primary methods pooled at strong signal, and strictly beats MCP/ABESS primaries in all 24 scenario cells. The strongest-gap claim, 84 versus 98, is correct.
- SMC accounting is 2,394 completed + 6 resource limits + 0 missing. Stops are failed/non-exact and all occur in S5, split 1/3/2 as stated. Three of four strong-signal stopped audit supports match the common saved exact-recovery support for that p/S5; they remain excluded. Conditional HPM recovery is 34/34, 48/56, 4/6 and 6/14, with rounded unflagged rates 93%, 94%, 62%, 57%. Pooled-share MCSE “about 1–2 percentage points” is reasonable.
- The G9 120,000-outcome/700-paired-row agreement, outstanding strict publication FAIL, and scorer-reported v7 correction are accurately distinguished in `BENCH_OPEN_ITEMS.md`. G5 verdicts and ABESS 7/48 and 109/168 search counts match the cited reports. The maximum approximately 0.49 RSS gain is across the c050 selected-rule search, not specifically the headline K37 primary (9/24 beaten). No evidence here requires discarding the existing recovery tables.
- D22 is satisfied: no high-p Z-accuracy, exact-posterior HPM-accuracy, or PIP-error claim is made. MPM is correctly presented as selection against truth using the existing RB-PIP rule. Informational diagnostics are labelled as such.
- The tie-out PASS is accepted at its stated sampled-scoring scope, with the coverage correction in finding 8. This reviewer did not reopen raw fit/truth folders, rerun the worker's file-writing script, freshly verify bundle SHA sidecars, or independently reproduce literature claims. The 2,400-bundle hash assertion is supported in the deliverable by its cited logs; those logs are outside the requested read list and were not newly audited here.

Verdict: ACCEPT WITH FIXES.
Findings: 0 blocking; 6 should-fix; 5 minor.
Meeting readiness: numerical results stand; correct the presentation and evidence qualifications above.
Most important finding: restore preregistered companion-rule visibility before presenting method-level comparisons.
Review path: <OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\analysis\H_existing_20261030\review\SOL_REVIEW_HEADLINE_H.md
