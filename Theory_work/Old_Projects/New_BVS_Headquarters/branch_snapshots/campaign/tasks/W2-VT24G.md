# W2-VT24G: Adversarial verification of W1-T24G (restated T24, Theorem B)

Run `git fetch origin theory/W1-T24G` and read `theory_campaign/W1-T24G/` on that branch: REPORT.md, PROOF.md, NOTES.md, scripts/ and results/.

You are an **independent referee**. Try to break the claims; don't just restate them.
1. Check **Theorem B**, **Prop. U** (resolution of EXIT_d), **Lemmas F/O/C/P**, **Cor. B-M** and **Cor. P1** line by line against `Docs/Methodology/METHODOLOGY_v3.md` (what one terminal round actually does: label order, swaps, independence moves, what counts as "scored") and against the T09 and T10 statements. For each step, record one of: VERIFIED, GAP (and whether it is fixable), or ERROR (with a counterexample).
2. Re-run or reimplement the numerical evidence for **CE1** (H24 is false: look-alike exit probability 0.62–0.98 in S2–S6 at p = 20, n = 200) and **CE2**. Independently confirm or refute them.
3. Check the claimed drop-in rewrite of **T21 route (e)** (W1-T24G §5) against `Docs/Theory/proofs/T21_T14H_HPM_composition/PROOF_v3.tex`.
4. **Deliverable:** `theory_campaign/W2-VT24G/REPORT.md` with a verdict table (claim | verdict | evidence), the fixes for any GAP you can repair (complete proofs), and the confidence card.
