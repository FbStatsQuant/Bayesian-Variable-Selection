# W7-SEP: Separation theorem — what the tempering bridge buys

**Paper role:** the conceptual spine of the story ("the sampler is needed in the masked regime"). Not on the frozen list; recommended by HQ after the campaign's results.

**Claim to prove.** On an explicit masked family (LH / LH-iid: branches `theory/W1-EXP`, `theory/W3-VEXP`, `theory/W3-PXN`; masking per CL(L), W1-EXP Thm 3/4), with cancellation depth c ≥ 2:
- (a) **Start-only methods fail.** Q iid draws from π₀ followed by the production local search from each draw (and from the start mode S̃₀, i.e. LS0 alone without the bridge) score S₀ with probability → 0 for every polynomial budget Q = n^A — unless the greedy basin of S₀ contains S̃₀ (quantify exactly when LS0 alone suffices, using Theorem A/TD′ from `theory/W1-T37R` + `theory/W3-VT37R`). Use R-T20(i) in `Docs/Theory/DROPPED.md` (iid discovery fails for c ≥ 3 under the n^{−c/2} law) and W1-T38E's iid-miss numbers.
- (b) **One-shot importance correction fails.** Importance weights π/π₀ from the start have χ² → ∞ (F-DRAFT Theorem W, branch `theory/F-DRAFT`; O-WSTAB in progress on `theory/O-WSTAB`), so the one-shot corrected estimator of 1{S = S₀} has relative variance → ∞ for p ≫ n.
- (c) **v3 succeeds.** Cite T38(b) with LS0 (`theory/W4-T38FULL`, `theory/W3-PXN`) and, if available, the no-tweak routes (`theory/W4-SHARE`, `theory/O-BGIBBS`, `theory/W5-B2ENV`).

Write (a)–(c) as one **Separation Theorem** with all hypotheses named, prove (a) and (b) in full (they are the new content), and state (c) as a citation with its premises. Give the budget exponents explicitly: the polynomial budget that v3 needs versus the super-polynomial budget that start-only discovery needs. Verify (a) numerically at small p on the LH family.

**Deliverable:** `theory_campaign/W7-SEP/REPORT.md` with the theorem, proofs, numerics and the confidence card.
