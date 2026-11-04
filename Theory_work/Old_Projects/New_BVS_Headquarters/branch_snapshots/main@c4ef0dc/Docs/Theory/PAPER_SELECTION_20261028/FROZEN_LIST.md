# FROZEN: theorem targets for the JRSS-B / Biometrika paper (2026-10-28)

Frozen by HQ after independent reviews by Fable 5.1 (`FABLE_REVIEW.md`) and Astra (`ASTRA_REVIEW.md`) of `PROPOSAL.md`. Both verdicts: ENDORSE WITH CHANGES. Changes are made only where both reviewers agreed, or where one raised a sound point the other did not contest.

**Premise (Felipe).** Every target is assumed provable after restating assumptions, minor methodology tweaks or budget sequences indexed by n. The campaign's job is to prove, restate, or establish that a target is false.

## Main text, JRSS-B version (8 results)

| Paper # | Targets | What it establishes | Change from the proposal |
|---|---|---|---|
| Thm 1 | **T03** (lemmas T01, T02) | The posterior concentrates on the truth | Restatement only (notes below) |
| Prop 1 | **T07** (+ one sentence of T06(i)) | The HPM is the Bayes rule for exact recovery; a size-only prior cannot fix a same-size swap | Kept (Fable); Astra's demotion applied only in the Biometrika cut |
| Thm 2 | **T22 + T27** | The start: provable mass on the truth or near it (favourable regime), and a masking lower bound (masked regime) | T27 merged into one theorem with T22 (Fable). It is a route-specific bound for iid start draws, not a bound for the hybrid sampler (Astra) |
| Thm 3 | **T37** (NEW); T24 as alternative | Repair: from any near-truth centre, the production local search reaches and scores the truth. Finite-n bound | NEW primary route (Fable). T24 kept as the Gibbs-path alternative; whichever closes first becomes Thm 3 |
| Thm 4 | **T21** | P(wrong report) ≤ P(no output) + 2E[posterior mass off the truth] + P(truth never scored) | None. Route (e) is now supplied by Thm 3 |
| Thm 5 | **T38** (NEW, main) | Consistency of the reported HPM in both regimes, *including delivery* of a near-truth centre, plus a polynomial-cost corollary | NEW. Replaces T26(iii) as the headline (both reviewers: T26 needs no sampler; the repair needs a delivered particle) |
| Thm 6 | **T26 (i)–(ii)** | Consistency of the evidence and the PIPs, favourable regime only | Demoted to a favourable-start result (both) |
| Prop 2 | **T12** (+ T31(i)) | Unbiased evidence; islandwise E[Ẑ_r·PIP̂_rj] = Z·PIP_j | Islandwise wording corrected (Astra); Markov 95% bound folded in (Fable) |

**Biometrika version (5):** Thm 1 (T03), Thm 2 (T22, with T27 as a remark), Thm 3 (T37 or T24), Thm 4 (T21), Thm 5 (T38). T07, T26 and T12 become remarks.

**Contingency target: T39** (Astra's C37), independent scoring-only repair tracks with an explicit budget. Use it only if T38(b) cannot be proved for the original method. It is a method extension and would need new validation runs.

## Supplement

- **Lemmas (needed by the proofs):** T01, T02, T09, T10, T11, T13, T14, T15, T20, T23, T32.
- **Remarks:**
  - T04;
  - **T05**, restored by both reviewers: the g-prior + BB(1,p) HPM loses a √log n factor to the oracle under orthogonal design, and should be disclosed before a referee finds it;
  - T06, T33, T34.
- **Dropped:** T08, T16, T17, T18, T19, T25, T28, T29, T30, T35, T36.

## The hole, and how it is filled

Both reviewers found the same hole: a guarantee that a near-truth particle is *delivered* and *repaired* with an explicit, finite budget. T24 and T26 alone do not provide it. The fill:
- **T37**, a finite-n repair through the existing local search (Fable);
- **T38**, a main theorem that contains the delivery step (HQ's synthesis of both reviews);
- **T39** as the fallback (Astra).

New statements are in `new_conjectures/`.

**Rejected as targets** (both reviewers):
- a comparative superiority theorem over SuSiE or SSL (the competitors' fixed points are intractable, and a toy comparison invites attack). The correlated-design mechanism is instead made explicit by T37's look-alike margin (n−1)θ²(1−r²)/(2σ²);
- PIP calibration;
- robustness to misspecification;
- minimax optimality.

## Restatement notes for the campaign

**Common setting:**
- a triangular array with s₀ fixed (14 in our study), p_n ≤ n^A and B ≤ 16, so s₀ = ⌊√n⌋ is not covered;
- separate the potential uninterrupted run from the output-available event, and never condition on observed completion;
- **prove compatible premises jointly**: one statistical family must satisfy every premise used in T38, not each conditional statement separately (Astra).

**Per target:**
- **T03 / T02.**
  - Replace T02(i)'s geometric tail 2^−m with the exact BB(1,p) tail. This cuts m_n from about 200 to s₀ + O(s₀ log n / log p), so SE on sets of size ≤ m_n + s₀ ≤ K becomes meaningful at n = 200 (Fable).
  - Restrict SE to the comparison unions actually used.
  - Use BM-∞ or an unnamed constant C in place of M*.
  - Neither change yields a useful finite-n frequentist error rate.
- **T22.**
  - Prove EXP, visibility and leakage for the actual partition dependent on X.
  - For T38(b), use the deterministic reference bound (the reference may differ from S₀) instead of concentration on the truth.
  - Failure points: normalised mass and uniform score remainders.
- **T27.**
  - Replace the assumed ratio law with a bounded-leakage condition along the chain (Fable), as a two-sided law with a controlled multiplier (Astra).
  - The exponent depends on the budget; recompute it when budgets change.
- **T37.**
  - The 2^{s₀} union is loose at s₀ = 14; a bound along the greedy path is the research part.
  - ℓ = 10 < s₀ + d = 15 at n = 200, so use the extra-scan rule or a closer centre.
- **T24 (alternative).**
  - Evaluate LK only at states that contain S₀, and charge look-alike additions to d.
  - Replace the 1/(s₀+d+B+2)! full-ordering constant with a progress argument of one correct step per round.
  - Failure point: EXIT under internal non-Gibbs moves.
- **T38.**
  - Eligibility in the masked regime: show the best-scored model lands in 𝓡_d, or use tweak LS0 (local search also from the start mode; can be added to existing fits after the fact).
  - Check compatibility of T22(i) with T27.
  - The cost corollary comes from T32.
- **T26 (i)–(ii).**
  - Require (T_n+1)Δ_n → 0 and (L_n+4)ρ*_n → 0.
  - Remove the secondary PIP.
  - Make no claims about the masked regime.
- **T12.**
  - Freeze everything before the final randomness.
  - Use the islandwise product identity; it is NOT an identity for pooled Ẑ × primary pooled PIP.
  - Drop the secondary PIP; validate floating point separately.
- **T21.** Keep P(U) and the non-launch terms. "Scored" includes rejected proposals.

## Suggested campaign order (both reviewers)

1. **T37.** Cheap and finite-n; feeds Thm 3 and T38.
2. **T02(i) tail sharpening and the T03 restatement.**
3. **T22(i)/(iii) and T27** on one compatible family, starting with EXP in the block-orthogonal benchmark.
4. **T38** (composition, plus eligibility).
5. **T24**, only if T37 fails; **T39** only if T38(b) fails.
6. **Bookkeeping restatements:** T12, T21, T26(i)–(ii), T07, the T05 remark.
