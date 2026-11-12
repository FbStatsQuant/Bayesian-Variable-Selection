MANIFEST b9c2675af243ac0945b09a015de87d0e4cdf42d790965312e49e84d5569dcec8

Hunks: numbered, per file, classified (a)/(b)/(c).

Line references below are old MP1 -> current RC4, inclusive. Content comparison normalises CRLF/LF. To make every change explicit, the inventory separates contiguous changed blocks within the ten unified-diff hunks (three in ASSUMPTION_MAP, two in PLAN, and five across L0–L3).

ASSUMPTION_MAP.md

1. 9 -> 9: (a), MP1-3. Replaces observations at n ≤ 3200 by completed sizes n = 400 and 1600. Faithful to the correction and RESULTS §4.
2. 25 -> 25: (a), MP1-1. Replaces the Gaussian-row “iff b < ½-type” assertion by the sufficient entrywise bound q√(log n/n) → 0, in particular b < ½, with necessity explicitly not asserted. This is the requested correction, with permitted typographic rendering; the assumed floor and its uses are unchanged.
3. 27 -> 27: (a), MP1-3. Updates B4 from 3/5 to 4/6 failures at η = 1, n = 1600, and identifies this as a finite-n LS0-probe failure. The near-frontier η ≤ 0.2 observation remains unchanged.
4. 31 -> 31: (a), MP1-2. Replaces “NECESSARY-FOR-ROUTE” and the unqualified nonnecessity assertion for reporting by sufficient negative divergence, a positive-divergence obstruction to whole-lattice NA, and an unresolved bounded-gap regime. B2 is expressly finite-n LS0 evidence; necessity for asymptotic reporting is neither proved nor refuted. Faithful to MP1 and consistent with STATEMENT §6, lines 279–293.
5. 46–47 -> 46–49: (a), MP1-3. Updates 207/204 to 208 runs and 204 successes; records completed sizes 400 and 1600, no completed 3200 run, p = 2n, nominal population-design classifications, and uncertified realised-design hypotheses. Explicitly limits observations to the validated LS0 re-implementation and excludes tests of sampler, posterior input, or the full reported model.
6. 49 -> 51: (a), MP1-3. Changes the table's “outside it, the conclusion” heading to “nominally outside it, the LS0 probe”, implementing the requested nominal/LS0 qualification.
7. 52–54 -> 54–56: mixed (a)/(b), comprising exactly these three row replacements:
   - B2: (a), MP1-2. Retains the counts and replaces “forced for the route” by finite-n LS0 success despite observed NA violations, explicitly denying an asymptotic nonnecessity inference.
   - B3: (b), the disposition's listed record correction. Renames A:BM-Q to A:BM-W and “no information on BM-Q” to “no information on the signal floor”. Counts and observations are unchanged; no signal hypothesis is altered.
   - B4: (a), MP1-3. Changes failures 3/5 to 4/6, the approximate outside-column count to 505–727, and swaps 19–35 to the four failing-run counts 19, 24, 35, 73. Qualifies failure as LS0-probe failure under the shipped cap. Retains the 32/32 near-frontier and 10/10 n = 400 successes and slack 15.
8. 56 -> 58: (a), MP1-3. Replaces “Inside every assumption” by “Nominal baseline cells (B1 at b ≤ 0.375)”; retains the 32/32 observation. This is the requested correction, not a certification of assumptions.

PLAN.md

9. 12 -> 12: (a), MP1-2. Replaces “survives iff” by the positive proof margin [β(η,A) − b] log n under b < β(η,A), explicitly disclaims necessity, and labels the above-√n discussion heuristic. The formula β = ½ − η/2 − √(2Aη) is unchanged.
10. 15 -> 15: (a), MP1-2. Replaces “exact complexity condition” and “route cannot do with less” by the sufficient negative-gap condition, positive-gap obstruction, and unresolved bounded-gap regime. No threshold, sufficient-form condition, or converse statement is changed.
11. 46 -> 46–47: (a), MP1-2. Replaces “what the route needs” by the precise positive-diverging-gap obstruction to whole-lattice NA and leaves the bounded-gap case unresolved.

lemmas/L0_toolkit_b.md

12. 3 -> 3–6: (b), listed review-status record. Quotes LC1-A's Toolkit-b VERIFIED-WITH-AMENDMENTS and MP1's CONTINUE WITH CHANGES, with the key lemma standing and no FATAL/MAJOR finding. Retains **PROVED (by this seat, unchecked)**. Body unchanged.

lemmas/L1_sandF_b.md

13. 3 -> 3–6: (b), listed review-status record. Quotes LC1-A's SAND-F^b VERIFIED and B1 VERIFIED, and the same accurate MP1 verdict. Retains **PROVED (by this seat, unchecked)**. Body unchanged.

lemmas/L2_width.md

14. 3 -> 3–7: (b), listed review-status record. Accurately records LC1-B's VERIFIED verdicts for Lemma 0, NA-conv, NA-W, sufficient forms (i)–(v), Lemma d and TL-W; preserves W-conv (+ corollary) VERIFIED-WITH-AMENDMENTS. MP1's CONTINUE WITH CHANGES and no FATAL/MAJOR finding are accurately recorded. Retains **PROVED (by this seat, unchecked)**. Body unchanged.

lemmas/L3_assemblyF.md

15. 3 -> 3–6: (b), listed review-status record. Accurately quotes LC1-B's Theorem RM2-F (assembly) VERIFIED and containment of RM-F VERIFIED, and MP1's verdict. Retains **PROVED (by this seat, unchecked)** and the qualification “given the cited inputs with their recorded statuses”.
16. 19–20 -> 22–24: (a), MP1-4. Replaces the imprecise “bounded convergence” label by exactly the requested expectation bound and order of limits. Set X_n = 1 − π(S₀). The unchanged O_P(√(log n/n)) input implies X_n → 0 in probability. Since 0 ≤ X_n ≤ 1, splitting over X_n ≤ ε and X_n > ε gives E X_n ≤ ε + P(X_n > ε). Thus limsup E X_n ≤ ε for every ε > 0, and E X_n → 0. This proves the same step from the same input; it needs no almost-sure convergence, stronger posterior theorem, or new rate.

There are no other content changes in the six pairs and no category (c) change. In particular, no hypothesis, lemma statement, constant, code pin, or substantive proof step changes beyond the permitted equivalent clarification in item 16.

Verdicts: MP1-1 RESOLVED; MP1-2 RESOLVED; MP1-3 RESOLVED; MP1-4 RESOLVED.

ATTESTATION: editorial/record only — L0–L3 stand as reviewed by MP1

Checks performed / not checked.

- All six saved MP1 files were checked by raw-byte SHA256 against their corresponding MANIFEST_MP1.txt rows: six matches. The saved lemma files are directly under as_reviewed_by_MP1/, rather than a lemmas/ subdirectory.
- All six current files were checked by raw-byte SHA256 against MANIFEST_RC4.txt: six matches. RESULTS.md and STATEMENT.md also match their RC4 hashes, which are identical to their MP1 hashes. The digest line above is copied verbatim from MANIFEST_RC4.txt. The optional full-manifest verifier was not run; no assertion is made about hashes of files outside this review's allowed source set.
- All six content diffs were inspected after newline normalisation, including the complete status-header and POST replacements. LC1-A/LC1-B were consulted only to check the status-header verdict record; MP1's exact findings and the disposition were compared with every change.
- Numerical cross-check: RESULTS §4 supersedes its frozen §§1–3 totals. Its added 78th n = 1600 run combines with 130 n = 400 runs to give 208; 204 successes leave four failures. In B4/η = 1/n = 1600, 2/6 successes means 4/6 failures, with swaps 19, 24, 35, 73. The old minimum 505 outside columns and the new run's 727 give 505–727. Only sizes 400 and 1600 completed; p = 2n. The B4 near-frontier cells give 2(10 + 6) = 32/32 successes at η = 0.05 and 0.2; η = 1/n = 400 gives 10/10. RESULTS §2 supplies slack 15 at n = 1600.
- Counts in the other touched table rows also agree: B2 has 3(10 + 6) = 48/48 successes, NA-probe violations 6/6 at b = 0.5/n = 1600 and 3/6 at b = 0.375, with no path-level violation; B3 has 2(10 + 6) = 32/32 successes and 32/32 missing weak truths at the start. The B1 baseline has 2(10 + 6) = 32/32 sandwich/path-NA/deletion-only runs at b ≤ 0.375. The unchanged B1 row in the same unified hunk agrees as well: 48/48 successes for b ≥ 0.5, maximum start size 241, √1600 = 40, sandwich failures 3/6 and 2/6, path-NA failures 1/6, 1/6, 4/6, and at most four non-deletion moves with slack 15. These remain observations, not asymptotic or fixed-design certifications.
- No remaining required change. This is a post-review diff check, not a fresh proof audit or numerical re-execution. No LOG, CHECKPOINT, other review report, external source, or production code was read; no git command was used. The only file written is this report.
