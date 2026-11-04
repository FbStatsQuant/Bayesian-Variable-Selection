# Notes 01: Castillo–Schmidt-Hieber–van der Vaart (2015); Yang–Wainwright–Jordan (2016) via Zhou et al. (2022)

## CSvdV 2015, Ann. Statist. 43(5) 1986–2018 (arXiv:1403.0735v3). READ: Papers/Priors_and_decision_rules/Castillo_SchmidtHieber_vanderVaart2015_Sparse_priors_regression.pdf
- Prior: dimension prior pi_p then uniform support then iid Laplace(lambda) slab on nonzeros; sigma known (=1).
- Dimension-prior condition (2.2), quoted: "A1 p^{−A3} πp(s − 1) ≤ πp(s) ≤ A2 p^{−A4} πp(s − 1), s = 1,...,p."
  Example: complexity priors pi_p(s) ∝ c^{−s}p^{−as}; and (line 277) "a Beta(1, p^u) hyper prior with u > 1 satisfies (2.3); cf. Example 2.2 in [16]".
- Thm 1 (Dimension): sup_{β0} E Π(β: |S_β| > s0 + (M/A4)(1 + 16λ/(φ(S0)²λ̄)) s0 | Y) → 0 (any M > 2).
- Thm 4 (Selection: no supersets), quoted: "If λ satisfies (2.1), and πp satisfies (2.2) with A4 > 1, then for every c0 > 0 and any
  sn ≤ p^a with sn λ √log p/‖X‖ → 0 and a < A4 − 1, sup E Π(β : Sβ ⊃ Sβ0, Sβ ≠ Sβ0 | Y) → 0" (sup over φ(S0) ≥ c0, ψ̃(S0) ≥ c0, |S0| ≤ sn).
- Thm 5 (Selection): beta-min thresholds M|S0|√log p /(ψ(S0)²‖X‖φ(S0)²) etc.; Π(S ⊃ {i: |β0_i| ≥ threshold}) → 1.
- Cor 1 (Consistent model selection): with (2.2), A4 > 1, compatibility/ sparse singular values ≥ c0 and beta-min in B̃:
  inf E Π(S_β = S_β0 | Y) → 1.
- Conditions are compatibility numbers φ(S) and "uniform compatibility in sparse vectors" ψ̃(s) over all vectors of dimension ≤ s
  (not anchored at S0); uniform over β0; sigma known.

### Comparison with BB(1,p) (our size prior)
Under BB(1,p) the DIMENSION prior is π_p(s) = C(p,s)B(s+1,2p−s)/B(1,p), so π_p(s)/π_p(s−1) = (p−s+1)/(2p−s) ≈ 1/2.
Hence BB(1,p) satisfies (2.2) only with A4 = log(2)/log p → 0: it is NOT a complexity prior. (Per MODEL, w(k+1)/w(k) =
(k+1)/(2p−1−k) ≈ k/(2p), i.e. a p^{−1} per-variable penalty; the binomial count C(p,k) cancels it.) CSvdV's Example (u > 1) and
Cor 1 (A4 > 1, i.e. u > 2) exclude u = 1. In our setting the missing dimension penalty is supplied by the g = n slab's Occam
factor (n+1)^{−1/2} per variable and p ≤ n^A; that is exactly why T02(i♯)'s cutoff m♯_n involves (n+1)^{s0/2}√n and
SE_w must be imposed up to size m♯_n (≈ s0 + O(log n)), not up to (1+M/A4)s0. → T03♯ is OUTSIDE CSvdV's hypotheses (Laplace slab,
known σ, complexity prior), and CSvdV is OUTSIDE ours. Same architecture (dimension → no supersets → beta-min selection).

## Yang, Wainwright & Jordan (2016), Ann. Statist. 44(6) 2497–2532 — SECOND-HAND via Zhou et al. (2022)
READ (only): Papers/Core_bibliography/10_2022_Zhou_et_al_Dimension_Free_Mixing...pdf (arXiv:2105.05719v3), §2 and Supplement S3
"Theorem S2 (Yang et al. [2016])". Primary YWJ paper NOT read → statements below are UNVERIFIED against YWJ itself.
- Prior (Zhou eq. (3)): π0(γ) ∝ p^{−κ0|γ|} 1_{M(s0)}(γ) (hard cap at max size s0), Zellner g-prior with 1 + g = p^{2κ1}.
- Theorem S2 conditions (quoted, compressed): (A) ‖Xβ*‖² ≤ g log p; (B) X_j'X_j = n and min_{γ∈M(s0)} Λmin(X_γ'X_γ) ≥ nζ
  [all models up to the cap: NOT anchored]; (C) E max_γ max_{k∉γ} |X_k'P⊥_γ z| ≤ ½√(C1ζ n log p); (D) κ0 ≥ 2, κ1 ≥ 1/2,
  κ ≥ 4(C0+C1)+2; (E) irrepresentability-type Ψ(X) bound with s0 ≤ n/(32 log p) − C0/4; (F) β²_min ≥ 128(κ+C0+C1) log p/(ζ²n).
  Conclusion: w.p. 1 − O(p^{−a}) "Condition 1" (local Bayes-factor monotonicity: overfitted ⇒ every addition has BF ≤ p^{−c0};
  underfitted ⇒ some true addition/swap with BF ≥ p^{c1}), which yields π(γ*|y) → 1 AND rapid mixing of RW-MH (YWJ) / LIT-MH (Zhou).
- Contrast with T03♯: YWJ need κ0 ≥ 2 (prior penalty ≥ p^{−2} per variable; our BB(1,p) is ≈ (2p)^{−1}/variable, κ0 ≈ 1),
  g = p^{2κ1} ≥ p (ours g = n with p up to n^{1.3}, so g < p), a hard cap s0 known to bound s*, unanchored RE over all of M(s0),
  and a Ψ condition. They get p ≫ n (s0 log p = O(n)); T03♯ is restricted to p ≤ n^A. They get a RAPID-MIXING theorem as well;
  under Condition 1 the posterior is unimodal in the local-move sense — this is the regime our "favourable" side lives in, and
  their Condition 1 FAILS by construction in our masked LH regime (that is the content of Thm 2 masking). [Interpretation, ours.]
