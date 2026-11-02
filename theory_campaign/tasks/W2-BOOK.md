# W2-BOOK: Bookkeeping restatements (phase P5): T12, T31(i), T21, T07, and the run/output split

**Paper role:** Prop 2 (T12 + T31(i)), Prop 1 (T07), Thm 4 (T21) wording. See `Docs/THEORY_PRIORITIES.md` §2 ("Open obligation (bookkeeping)") and §4 item 6.

**Steps:**
1. **T12 + T31(i).**
   - Freeze everything before the final randomness.
   - Use the **islandwise** wording, E[Ẑ_r·PIP̂_rj] = Z·PIP_j. It is NOT a pooled × pooled identity, and the normalised PIP is not claimed unbiased.
   - Drop the secondary-PIP clause.
   - State the potential-uninterrupted-run vs output-available split (the `resource_limit` caveat: 6 of 2,400 fits stopped).
   - Validate floating point separately.

   Write the restated statements, and the exact proof edits against the locked proofs in `COLLECTED_PROOFS_v2.tex`.
2. **The same run/output split for** T11(iii), T14, T15, T23, T25(iv), T31 and T34. For each: the one-line statement change, and whether the proof changes. Never condition on observed completion.
3. **T07, with one sentence of T06(i):** a paper-ready statement (HPM = Bayes rule for exact recovery, MPM for Hamming loss, PIP error bounds the excess risk, no size-only prior fixes a within-size swap). Tie it to the empirical finding that c = 0.5 misses are mostly same-size swaps.
4. **T21:** a paper-ready statement of (C1) with routes (a), (d) and (e′). Route (e′) uses the restated T24, "Theorem B", from branch `theory/W1-T24G` (`theory_campaign/W1-T24G/REPORT.md` §5). Mark how T37 would enter if it closes.
5. **Deliverable:** `theory_campaign/W2-BOOK/REPORT.md` with paper-ready statements, proof edits and the confidence card. Optionally add a LaTeX fragment `STATEMENTS.tex`.
