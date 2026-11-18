# Audit audit1b-core3-s1: Theory_work/Wave3/API_AUDIT/audit1b/REQ_core3.md
claims: core3:B7.SL, core3:B1.SL, core3:B2.SL, core3:B7.IO, core3:A2.SL, core3:A2.IO, core3:B8.SL, core3:B8.LEMMA, core3:B8.IO, core3:B9.SL, core3:B9.IO, core3:B5.SL, core3:B10-FL.SL, core3:A5.IO, core3:A6.SL, core3:A6.IO, core3:SCOPE.IO
stop_reason: end_turn

## core3:B7.SL — REFUTED

**Problem.** The implication "Gaussian rows ⇒ Condition 1" (TRACK_B.md:140 "stronger still"; :250 "(implies it)"; AUDIT.md:76) fails for the hypothesis as we state it.

- Our hypothesis is rows i.i.d. N_p(m_n, Σ_n) with an unrestricted mean sequence m_n (READER_VERSIONS.md:666; RM STATEMENT.md:41–42).
- Song–Liang p. 953 verifies Condition 1 only for "a Gaussian process with zero mean and var(x_i) = 1". That is a sufficient case, and its zero-mean premise is not ours.
- Condition 1 is stated on the raw x with fixed constants M and δ, and their model (1) has no intercept to absorb a mean.

**Counterexample.** Take r = 1, a_1 = δ (δ < 1/√2 is forced, otherwise the expectation is infinite even at mean 0), and x_1 ~ N(m, 1) with m = m_{n,1}. Then

E exp{(δ x_1)²} = (1 − 2δ²)^{−1/2} · exp{δ² m² / (1 − 2δ²)}.

For m_{n,1} → ∞ (say m_{n,1} = n) this exceeds exp(M) for every fixed M. So Theorem 6's row law does not imply Condition 1; it does so only for centred rows or bounded means.

The first half of the verdict ("Thm 9 (A3) … implies it") cannot be checked: Thm 9 (A3) is not among the excerpts.

## core3:B2.SL — UNCLEAR

- **Lower range:** confirmed. Song–Liang p. 950 assume P_n ≻ n^θ; (S2) asks only 2 ≤ p ≤ n^A.
- **Upper range:** cannot be settled. The claim rests on "Corollary 1, p. 954, allows P_n < exp(Cn^α), α ∈ (0, 1)", and no p. 954 passage is supplied.

Needed: the statement of Corollary 1 (p. 954) and the growth condition on P_n in the theorem it specialises.

## core3:A2.SL — REFUTED

**Problem.** AUDIT.md:77 maps "(A2) s₀ fixed, fixed nonzero signals" to "same: (4), p. 950". That is a direction error.

- Display (4) says only lim Σ_j 1{β*_j ≠ 0} < ∞. It places no constraint on the size of the nonzero coefficients.
- (A2) also requires θ_lo ≤ |θ*_j| ≤ θ_hi with fixed constants in (0, ∞) (READER_VERSIONS.md:670–671; RM STATEMENT.md:43).
- So (A2) ⇒ (4) but not conversely. A sequence with s₀ = 1 and β*_1 = 1/n (or β*_1 = n) satisfies (4) and violates (A2).

The correct relation is "strictly stronger than (4)", not "same". The audit's own dossier text agrees: TRACK_B.md:89–92 reports no beta-min in Theorem 3 and no bound under (4) alone. Only the s₀-fixed half is "same".

Not checkable from the excerpts: "(4) used by Theorems 2–3; Theorem 1 alone allows (3)" and "|x_i| ≤ 1 (Theorem 1, p. 952)". The statements of Theorems 1 and 2 are not supplied; p. 953 says only "bounded by some constant m, as assumed in theorem 1".

## core3:B8.IO — REFUTED

**Problem.** The P6 cell "cs in; fac2, s5 unclear" (TRACK_B.md:251) is contradicted by direct computation. With the P6 truth (all coefficients positive: β = (1.4, 1.0, 1.8, 1.2), "aligned signs", DESIGN.md:16), fac2 and s5 satisfy (A3) with an explicit constant. They are inside for the same reason cs is.

**P6 s5** (x_j = √.3 f + √.4 g_group + √.3 e_j, truths in distinct groups, DESIGN.md:15–17).

- Let j, k ∉ U lie in different groups, with a_j and a_k columns of U in their groups, and write γ_a = 3/(4a + 3) > 0.
- Conditioning on f first gives Cov(W_j, W_k | W_U) = 0.3 · γ_{a_j} · γ_{a_k} · Var(f | W_U) ≥ 0.
- Hence Cov(W_j, Wᵀθ* | W_U) = θ_j Var(W_j | W_U) + Σ_{k ∈ S₀∖(U∪{j})} θ_k Cov(W_j, W_k | W_U) ≥ θ_j · λ_min(Σ) ≥ 1.0 × 0.3.
- This holds for every U ∌ j of any size, so (A3) holds with a = 0.3.

**P6 fac2** (loadings (√.35, ±√.25), idiosyncratic variance .40, DESIGN.md:14).

- Suppose U has m_e even and m_o odd columns, N = m_e + m_o. The posterior precision of (f₁, f₂) is P = I + (1/.4) Σ_{u∈U} l_u l_uᵀ.
- For j, k ∉ U: opposite parity gives Cov(W_j, W_k | W_U) = 0.10 / det P > 0.
- Both even gives (0.6 + 0.875 m_o) / det P > 0; both odd gives (0.6 + 0.875 m_e) / det P > 0.
- All θ_k > 0, so Cov(W_j, Wᵀθ* | W_U) ≥ θ_j Var(W_j | W_U) ≥ 1.0 × 0.4. (A3) holds with a = 0.4.

This agrees with track C's own finding that aligned truths in factor designs are inside (RESULTS.md:63–64).

The remaining cells survive:
- S1–S4, S6, IND, AR and BLK are in.
- Study S5 (mixed signs) stays unclear. For θ_j = 0.8, U = ∅ gives +0.80, while U = the six other positive truths plus one pure-factor column gives 0.56 − 2.34·0.25 = −0.025. So no sign argument applies, and I found no exact zero.
- 1M FAC stays unclear because the coefficient signs are not given.

## core3:B5.SL — UNCLEAR

- **"Stronger in level":** confirmed. A fixed c against δ_n ≻ ε_n² (p. 955), where ε_n → 0 is forced because δ_n ≤ 1.
- **"Stronger conclusion":** confirmed against Theorem 3 (p. 956), which gives sure screening only.
- **"On smaller sets":** cannot be settled. Condition 3 ranges over r̄_n + 1 predictors, and no excerpt gives the definition or growth rate of r̄_n. Without it, sets of size 5(A+1)(s₀+1) log n cannot be ranked against r̄_n + 1.

Needed: Song–Liang's definition of, and rate conditions on, r̄_n (and ε_n) from the prior specification and the conditions of Theorem 2.

AUDIT1 core3:B7.SL VERDICT=REFUTED
AUDIT1 core3:B1.SL VERDICT=NO-FINDING
AUDIT1 core3:B2.SL VERDICT=UNCLEAR
AUDIT1 core3:B7.IO VERDICT=NO-FINDING
AUDIT1 core3:A2.SL VERDICT=REFUTED
AUDIT1 core3:A2.IO VERDICT=NO-FINDING
AUDIT1 core3:B8.SL VERDICT=NO-FINDING
AUDIT1 core3:B8.LEMMA VERDICT=NO-FINDING
AUDIT1 core3:B8.IO VERDICT=REFUTED
AUDIT1 core3:B9.SL VERDICT=NO-FINDING
AUDIT1 core3:B9.IO VERDICT=NO-FINDING
AUDIT1 core3:B5.SL VERDICT=UNCLEAR
AUDIT1 core3:B10-FL.SL VERDICT=NO-FINDING
AUDIT1 core3:A5.IO VERDICT=NO-FINDING
AUDIT1 core3:A6.SL VERDICT=NO-FINDING
AUDIT1 core3:A6.IO VERDICT=NO-FINDING
AUDIT1 core3:SCOPE.IO VERDICT=NO-FINDING