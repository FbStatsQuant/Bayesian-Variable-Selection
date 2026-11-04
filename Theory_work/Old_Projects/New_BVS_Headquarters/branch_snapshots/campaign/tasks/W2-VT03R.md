# W2-VT03R: Adversarial verification of W1-T03R (exact BB(1,p) tail, T02(i♯), T03♯)

Run `git fetch origin theory/W1-T03R` and read `theory_campaign/W1-T03R/` on that branch: REPORT.md, PROOF.md and scripts/.

You are an **independent referee**. Try to break the claims.
1. Check **Lemma E1** (a)–(d), **Lemma E2 / Prop. E3**, **T02(i♯)** with its explicit constants, **T02(ii♯)** under SE_w, and **T03♯** under SE_λ(j₀) + SE_w(m♯; g₀) + BM. Check them against the locked proofs: `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex` and `T03_A2_selection_consistency/PROOF_v2.tex`. For each changed step, record one of: VERIFIED, GAP, or ERROR.
2. Reproduce **Prop. D**, the duplicated-columns counterexample, numerically and analytically.
3. Is the "anchored" SE (unions S₀ ∪ J only) really enough at *every* place the proof uses SE? Hunt for a hidden use on unions that do not contain S₀.
4. **Deliverable:** `theory_campaign/W2-VT03R/REPORT.md` with a verdict table, repairs of any GAP (complete proofs), and the confidence card.
