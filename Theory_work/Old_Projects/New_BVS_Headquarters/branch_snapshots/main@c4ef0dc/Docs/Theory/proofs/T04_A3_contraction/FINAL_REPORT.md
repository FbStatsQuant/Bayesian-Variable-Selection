# FINAL REPORT — T04 (A3 = T4): contraction without beta-min

**Result:** proved (Opus 5.5 lead; reviewed by 2 independent Opus 5.5 xhigh, CP + CW); not adopted. Adoption is Felipe's decision.

**Scope of the result.** All four parts, (i)–(iv), are proved, including the secondary double-logarithm fallback (i). The proof is conditional on one explicit hypothesis, H-T02, which is T02(i) (being proved in a sibling thread). It is used once, as Π(|S| > m_n | y) → 0 with ω_n = ½ log n. T01 is not needed as a hypothesis: the proof shows directly that the S-marginal of the contrast posterior Π† equals the v3 target π (Lemma 1.2). T01(i) only says that Π† is the transformed v3 joint posterior, which is how Π† is defined.

## Final files
- STATEMENT.md
- proof/PROOF_v2.tex and proof/PROOF_v2.pdf (14 pages). This is the final proof. PROOF_v1 is kept for the record.
- CLAIMS_OF_FATAL_FLAWS.md
- review/ROUND1_CP.md, review/ROUND1_CW.md, review/ROUND2_CP.md, review/ROUND2_CW.md
- helpers/make_v2.py (the lead's revision script)

## Statement changes
None. STATEMENT.md writes out the following, without changing the statement:
- the readings: the meaning of Π†, the "applicable ε_n", and what C depends on;
- H-T02 as an explicit hypothesis;
- after round 1, the v3 definition of m(S) and π, copied verbatim from 00_COMMON §1.

No statement checker was needed.

## How the proof works (plain words)
1. **Reduction to an ordinary regression.**
   - In centred ("contrast") coordinates the problem is an ordinary Gaussian regression with n−1 noise dimensions.
   - The data-dependent prior rate b₀s_y² only matters through the bound 0 < 2b ≤ const, which holds on a high-probability event.
   - So no change of the inverse-gamma rate is needed.
2. **Master theorem.**
   - A model whose best ridge fit to the true mean is poor loses to the true model. This is deterministic on a high-probability noise event.
   - If the posterior puts little mass on models of size greater than d, prediction contracts at rate (d+s₀+1)log(p∨n)/n, and v at that rate plus u_n/√n.
   - No beta-min condition is needed, because a weak true variable that is missed costs little fit.
3. **Part (i) (fallback).** Take d = m_n = O(log n), using H-T02. The rate is (s₀+1)log²(p∨n)/n.
4. **Part (ii) (sharp rate, under SE).**
   - Compare each model with its union with S₀. This union is always inside the cap K for large n.
   - Sum over the supersets of S₀ in expectation, after truncating on the noise event.
   - This gives posterior dimension ≤ d_* = s₀ + ⌈s₀(2A+1)⌉, and then the rate (s₀+1)log(p∨n)/n.
   - Coefficient error follows by SE. Part (iv) is the raw-scale back-transform: divide by the column standard deviations, each at least d₋.
5. **Provenance.** The argument re-proves, for v3, the old draft proof Proposed_project/proofs/T9_C9 (§§1–5, §9 and its addendum). The changes for v3 are:
   - noise dimension n−1 and column norms n−1;
   - the IG(0.51, b₀s_y²) prior;
   - the cap K = min(p, ⌊n/2⌋);
   - T02(i) in place of the old Fact D.

   Note that the old folder Proposed_project/proofs/T4 is a different theorem (a two-state switch) and was not used.

## Review history
- **Round 1 (PROOF_v1).**
  - CP: verified.
  - CW: not verified, because of one gap. CW-F1 found that the formula for π was quoted from 00_COMMON, which is outside the review packet. It was accepted and fixed by writing the formula into STATEMENT.md and §0. CP had raised the same point as an exposition issue.
  - All exposition notes were applied in v2: notation renames, a corrected remark on hypotheses, the n ≥ 8 condition in Theorem 5.1(ii), G listed in §7, and clearer Ξ̄_n notation.
- **Round 2 (PROOF_v2).**
  - CP: verified. CW: verified.
  - Both confirm that CW-F1 is closed. Both also checked the π identity numerically, with errors ≤ 3·10⁻¹⁶; CW also checked it by direct quadrature, without the closed forms.
- **Open dispute:** none.
- **Judge:** not used.

## Exposition notes left open (deliberately not applied)
These are not applied, so that the final file is exactly the text both reviewers verified. They should be applied when the proof is integrated.
- STATEMENT's Q_S and Z correspond to the proof's Q^{v3}_S and the normaliser. The proof's Q_S = s_y²Q^{v3}_S, and its Z = UᵀX.
- "| y" in Π† means conditioning on y_c.
- Local letter clashes: ζ_j vs ζ (Lemma 3.1), t_k vs the vector t, and e (noise) vs Euler's e.
- The notation paragraph's remark on C should say "§0–§1 and the claim paragraph".

## Agent counts
- Lead: 1 (Opus 5.5 high).
- Helpers: 0.
- Statement checker: 0.
- Reviewers: 2 (Opus 5.5 xhigh: CP on Claude Personal, CW on Claude Work). Each did 2 rounds, for 4 review calls.
- Judge: 0.
- Fable: 0.
