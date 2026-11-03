# Resolution of Sol review 1 (SOL_REVIEW_HEADLINE_H.md: ACCEPT WITH FIXES, 0 blocking / 6 should-fix / 5 minor)

All 11 findings were applied. No recovery count changed.

1. **Companion rules (R2/R4).**
   - **What changed:** HEADLINE_H §1–2 now show, in the same tables, F1–F3 `cv_min` / `cv_1se` / `ebic1_K37` side by side, SuSiE-refine beside SuSiE, and the other MCP/ABESS EBIC variant, each with its registry label.
   - **Source:** the tables are rendered from `all_rules_recovery_long.csv` by `scripts/render_tables.py`.
   - **Ranks** use the primary rules, as stated.
2. **Lasso/ENet wording.** Fixed in BENCH_FLAGS Flag 3, with the mixed-error counts and the separate cv_min and cv_1se FP ranges. HEADLINE §4 now says "CV-min".
3. **SSL-RS.** Pooled misses (499/497 strict subsets, 69/71 mixed) are now separated from the scenario 1 facts, and "scenario 1" is spelled out.
4. **G5 coverage.** The F3 statement is corrected. The fact that MCP/SCAD saved-vector checks cover raw `ebic1`, not K37, is added to HEADLINE §6 and BENCH_OPEN_ITEMS §2. The F3 probes are framed as additional to the arithmetic already audited.
5. **Literature and causal claims.** Removed: the oracle-property and memory/Oct-7/Kollipara claims. Every cause is now a hypothesis. The ABESS caveat is added ("lower RSS ≠ better recovery"). R7 is cited for the horseshoe.
6. **Rerun wording.** The Sources paragraph is replaced with Sol's wording (agreement is still to be checked; D11 retries are reported separately).
7. **K37 equality sentence.** Corrected: equal exact counts, not identical selections (F3 `ebic05` k = 40 example).
8. **Tie-out verdict.** It now describes 44 targeted, seeded, stratified checks with 2 fixed reconciliation checks. Classification: 14 SMC / 17 primary / 3 supplementary, with the unsampled cells named. Scope: PASS for the checked claims, not exhaustive. The script comment is fixed.
9. **Disclosure.** The AI-written/G5 caveat now sits above the tables, and the label reads "ABESS (splicing heuristic)".
10. **build_headline.py hardening:**
    - full benchmark equality, now including the FP/FN/MCSE columns, is asserted;
    - other-p all-missing, key uniqueness and the 100/600 denominators are asserted;
    - paired joins use `validate="one_to_one"`.

    Rerun: exit 0. All 12 output CSVs are byte-identical to before (`logs/build2.*`).
11. **Gain range.** It now reads "Relative to the best benchmark in each cell…".

## Re-check (SOL_RECHECK_HEADLINE_H.md: FIXES INCOMPLETE, 9/11) — remaining items applied

- **Fix 1.** The SuSiE-refine labels now carry the full registry qualification: "…; fit selection by ELBO" at both scales. `headline_tables.md` was regenerated, and both rows in HEADLINE_H were synced. Every rendered row now appears verbatim in HEADLINE_H.
- **Fix 10 (first attempt).** Superseded: re-check 2 found that the headline-row and paired-merge checks still ran after the first CSV write. The checks added in this attempt were:
  - identical schemas across passes, and unique keys per pass;
  - an explicit expected key set: 52 method/rule pairs × 2 scales × 2 p × 7 scenario cells = 1,456;
  - the exact wrong-pass SMC key set, all missing;
  - full-frame equality of the benchmark rows across passes, in all saved columns;
  - the combined key set and the 100/600 denominators.

  Rerun `logs/build3.*`: exit 0. All 12 CSVs are byte-identical to the previous build (`logs/build3_bytecompare.txt`).
- **N1.** The Files entry is split: `headline_tables.md` holds the expanded tables, and the long/wide CSVs hold the primary/secondary tables.

## Re-check 2 (SOL_RECHECK2_HEADLINE_H.md: items 1 and N1 accepted; item 10 ordering open) — applied

- **Fix 10 (ordering).** `build_headline.py` now stages all 11 output tables in memory (`STAGED`). The aggregate checks, the headline 14-row assertion, every one-to-one paired merge and the paired 1,200-row coverage assertion all run during staging. Every `to_csv` and the checks-JSON write happen in one final publication block, which is reached only if all assertions pass.
- **Rerun** `logs/build4.*`: exit 0. All 12 CSVs are byte-identical to the previous build (`logs/build4_bytecompare.txt`). `win_loss.py` is a separate, assertion-free summary step run after the build.
- **Not re-reviewed by Sol:** this ordering-only change. The manager closes it on the build4 evidence; the checks themselves are unchanged from re-check 2, where all 14 negative tests passed.
