# Stage B, Opus 5.5 (xhigh) reviewer, round 1 — reply saved verbatim (PROOF_v1)

# Review report: T31 (T22), part (i), PROOF_v1

Packet read: STATEMENT.md, PROOF_v1.tex, PROOF_v1.pdf, REPORT_FORMAT.md. I read nothing else and ran nothing. The PDF matches the .tex: same numbering (Lemma 1 to Remark 12) and the same content.

## A. Step-by-step verification log (what was checked and found correct)

**Lemma 1 (lines 26–73).**
- (i) Q_S bound. With X_S = UΣVᵀ, the matrix I_n − nX_S H_S⁻¹ X_Sᵀ has eigenvalues (σ_j² + 1)/((n+1)σ_j² + 1) ≥ 1/(n+1), plus 1's for the zero entries. So Q_S ≥ yᵀy/(n+1) > 0, using yᵀy = n−1 ≥ 2. Checked.
- (i) The factors D_S > 0, Γ(ν), Γ(0.01) and 0.02^{0.01} are all finite and positive. Checked.
- (i) Weights. C(2p−1, k) ≥ 1 for k ≤ K ≤ p ≤ 2p−1, and W_K ≥ ½ from the k = 0 term. Ω is finite and nonempty, so Z ∈ (0, ∞). Checked.
- (ii) Z̄₀ ∈ (0, ∞) and d is finite. Checked (see finding 8 for a wording issue).
- (iii) Ẑ_r = g(A_r), where g maps the finite set Ω^{N_e T} into (0, ∞). So Ẑ_r and Ẑ take finitely many positive values, and log Ẑ is bounded. Checked (see findings 6 and 7).

**Lemma 2 (lines 79–93).**
- Markov's inequality gives P(αW > Z) ≤ α, so P(Z ≥ αW) ≥ 1 − α.
- Finite Jensen for the concave log gives E log W ≤ log Z.
- Both checked.

**Theorem 3 (lines 95–107).** Lemma 1 plus (H-T12), E_c Ẑ = Z, meets every hypothesis of Lemma 2. That yields (a), the special case α = 0.05, and both parts of (b): log Ẑ is well defined and integrable, and E_c log Ẑ ≤ log Z. Checked. CAL is listed as a hypothesis but never used; this is harmless.

**Remark 4 (lines 109–114).** For any law in 𝓛(Z), Ẑ is finitely valued in (0, ∞) with mean Z by linearity, so Lemma 2 applies. Checked.

**Lemma 5 (lines 118–129).**
- c′ ∈ (0, ½], ε ∈ (0, ¼), B > 0, and B − c′ = (1 − c′)/ε > 0.
- E Ẑ_r = Z((1−ε)c′ + 1 − (1−ε)c′) = Z.
- On A, Ẑ = c′Z ≤ (c₀/2)Z < c₀Z.
- P(A) = (1−ε)⁴ ≥ 1 − 4ε = 1 − η.
- All checked.

**Corollary 6 (lines 131–141).** "Follows from the properties defining 𝓛(Z)" is read correctly as "holds for every law in 𝓛(Z)".
- If γ > 1, the bound fails for every law, and 𝓛(Z) is nonempty.
- If γ ≤ 1, take c₀ = c₁ and η = γ/2 < 1. Then P(c₁Z ≤ Ẑ ≤ c₂Z) ≤ P(Ẑ ≥ c₁Z) ≤ η < γ.
- The "in particular not from those used in (a)–(b)" part holds because those properties are a subset of the defining ones (Remark 4).
- Checked.

**Lemma 8 (lines 152–163).**
- (u−m)² + (v−m)² = ½(u−v)² + 2((u+v)/2 − m)², so SS ≥ R²/2.
- SS/4 ≥ R²/8 and SS/3 ≥ R²/6 ≥ R²/8.
- If R ≥ 3, both SDs are at least √(9/8) > 1, strictly.
- Checked.

**Corollary 9 (lines 165–175).**
- All four values equal: SD = 0 ≤ 1, so the flag is not raised. The flag rule is "exceeds 1", strict.
- Otherwise the log-range is at least 3, so SD > 1 for both divisors.
- Checked.

**Theorem 10 (lines 177–191).**
- ε = 3α/(32−α) ∈ (0, 1) because α < 8.
- a + ε(b−a) = ¼ + [3α/(32−α)]·[(32−α)/(4α)] = 1.
- log(b/a) = log(32/α) > log 32 > 3.
- P(raised) ≥ ε(1−ε)³ > 0.
- On the raised event at least one coordinate equals bZ, so Ẑ > bZ/4 = 2Z/α. Coverage then fails surely, and the conditional coverage is 0.
- Checked.

**Theorem 11 (lines 193–225).**
- ℓ̄ < (h/M)/(e³−1) ≤ 1/(e³−1) < 1/19, using M ≥ h.
- q ∈ (0, 1), and q > (18/19)/h = 9α/19 > α/3.
- Mean qh + (1−q)ℓ̄ = 1.
- Consecutive log-gaps are exactly 3, so Corollary 9 applies.
- P(H) = q⁴ and P(L) = (1−q)⁴M⁻³.
- Coverage fails on H (αẐ = 2Z) and holds on L (αẐ = 2e^{−3k}Z < Z).
- x/(q⁴ + x) < x/q⁴ ≤ M⁻³/q⁴ < 81/(α⁴M³) ≤ γ.
- A suitable integer M exists. Checked.
- The γ = 1 − α case gives conditional coverage below 1 − α. Checked.

**Remark 12 (lines 227–234).** Consistent with the disclaimer in STATEMENT §3.

**Statement against the source clause.**
- Source "P_𝓒(Z ≥ αẐ) ≥ 1−α": formalised as (a) for every successful c and every α ∈ (0, 1).
- Source "E_𝓒 log Ẑ ≤ log Z": formalised as (b), with well-definedness added.
- Source "0.05Ẑ has coverage at least 95%": the α = 0.05 case of (a).
- Source "Not a relative-error interval": formalised as non-implication (c).
- Source "Does not preserve this coverage automatically": formalised as non-implication (d1)/(d2).
- The word "automatically" supports the non-implication reading. Finding 1 shows this reading is also forced, because the stronger literal reading is false for the actual estimator.

## B. Findings

**Finding 1**
- Location: STATEMENT.md §3, preamble to (c)–(d), and (c).
- Severity: exposition.
- Claim: The non-implication reading of "it is not a relative-error interval" (and of (d)) is the only reading under which the clause is true. The statement does not say this. Without it, a reader may take (c) as saying the actual estimator has no relative-error guarantee, which is false.
- Evidence:
  - From the §1 formulas, each stage factor of Ẑ_r lies in [exp(Δφ_t·d_min), exp(Δφ_t·d_max)], since Δφ_t > 0. Because Σ_t Δφ_t = 1, Ẑ_r ∈ m(∅)Z̄₀·[e^{d_min}, e^{d_max}].
  - The definitions give ϖ(S)BF(S) = γ₀(S)e^{d(S)}. So Z = m(∅)Σ_S γ₀(S)e^{d(S)} lies in the same interval.
  - Hence, surely, e^{−Δ}Z ≤ Ẑ ≤ e^{Δ}Z, where Δ = d_max − d_min depends on the data. That is a two-sided relative-error bound with probability 1.
  - Likewise for (d), the log-range of (Ẑ_r) is at most Δ. The largest SD for four points in an interval of length R is R/2 (divisor 4) or R/√3 (divisor 3). So if Δ ≤ 2 (divisor 4) or Δ ≤ √3 (divisor 3), E2_final can never be raised. If Δ < log(1/α), coverage holds surely. On such data, conditioning on "not raised" does preserve coverage.
  - This does not contradict (c) or (d), which quantify over the abstract class 𝓛(Z) with constants that cannot depend on the law. The statement's disclaimer ("do not assert that any particular data set realises the laws exhibited") covers it. The point is that the disclaimer is essential, and the statement would be more precise if it said so.

**Finding 2**
- Location: STATEMENT.md §1 ("Final E2 flag") and §3 (d), compared with the source's "final flags" (plural).
- Severity: exposition.
- Claim: The source speaks of final flags in general. The statement treats only E2_final and does not say whether other final flags exist or why one suffices.
- Evidence:
  - Read existentially ("conditioning on final flags is not automatically coverage-preserving"), one witness flag is enough, and (d1)/(d2) provide it.
  - Read as "for every final flag", the claim would need each flag, and it can fail: conditioning on a flag independent of Ẑ preserves coverage.
  - Whether the method has other final flags cannot be checked from this packet.

**Finding 3**
- Location: STATEMENT.md §1 (P_c, E_c); PROOF line 21; Theorem 3.
- Severity: exposition.
- Claim: The statement asserts, without proof, that P_c and E_c are the conditional law and expectation given 𝓒 = c, which is what links (a)–(b) to the source's P_𝓒 and E_𝓒. The proof works only with P_c as defined and never addresses the link.
- Evidence:
  - The link is the standard substitution lemma. It requires the final run to be a jointly measurable function F(c, U₁₀..₁₃) of the calibration and the independent final streams. CAL plus "all other frozen settings" in c, together with EX-S, make this plausible, but it is not written out.
  - The identification holds only almost surely, as a version.
  - The source's statement concerns only the successful-calibration event, which the statement handles implicitly by restricting to successful c.
  - This is why CAL appears in Theorem 3's hypotheses without being used.

**Finding 4**
- Location: STATEMENT.md §1 and §2 ((H-T12), the formula for Ẑ_r, the E2 definition).
- Severity: exposition (scope limitation).
- Claim: Whether these definitions match METHODOLOGY_v3.md (§6.9, §6.12) and the sibling result T12(iii) cannot be checked from the packet.
- Evidence: Only STATEMENT.md is available. The theorem is correctly conditional on (H-T12) as stated: pooled unbiasedness for every successful c. If T12 gives only an almost-sure-in-𝓒 version, the per-c hypothesis is a slight strengthening.

**Finding 5**
- Location: STATEMENT.md §3 preamble ("has all properties of the final-run evidence … together with island independence, identical distribution and islandwise unbiasedness").
- Severity: exposition.
- Claim: The sentence can be read as asserting that the actual final run has i.i.d. islands with islandwise mean Z. Islandwise unbiasedness is not a hypothesis: (H-T12) is pooled only, and T12(i) is mentioned but not assumed. I.i.d. islands are not proved anywhere.
- Evidence: This does not affect validity. Adding properties to the class only strengthens a non-implication: if P′ ⊇ P does not imply Q, neither does P. But as a description of the actual estimator the sentence goes beyond the hypotheses.

**Finding 6**
- Location: PROOF Lemma 1(iii), lines 61–62.
- Severity: exposition.
- Claim: The proof cites π₀, which STATEMENT.md does not define, and says "every move keeps the state in Ω", which is a claim about the algorithm not given in the packet.
- Evidence: Both are redundant, because STATEMENT.md §1 already stipulates S_{r,i}^{(t−1)} ∈ Ω.

**Finding 7**
- Location: PROOF Lemma 1(iii), lines 63–65.
- Severity: exposition.
- Claim: The proof attributes measurability of the particle-state array A_r to EX-S, but EX-S asserts measurability only of the algorithm's "outputs". The proof also uses N_e ≥ 1 (needed for 1/N_e) without saying so.
- Evidence: Not needed. Ẑ_r is an output, so it is a random variable directly by EX-S. Finite-valuedness holds pointwise, since Ẑ_r(ω) ∈ g(Ω^{N_e T}). T ≥ 1 follows from φ₀ = 0 < φ_T = 1.

**Finding 8**
- Location: PROOF Lemma 1(ii), lines 56–57.
- Severity: exposition.
- Claim: "Each table entry r_b(A) = BF(A) is in (0, ∞)" cites (i), which was stated only for S ∈ Ω. Entries with A ⊆ C_b and |A| > K are not covered as written.
- Evidence: Harmless. Only entries A = S ∩ C_b with S ∈ Ω enter γ₀ and d, and |S ∩ C_b| ≤ |S| ≤ K. The argument in (i) also never uses |S| ≤ K.

**Finding 9**
- Location: PROOF Theorem 10 proof, line 189.
- Severity: exposition.
- Claim: "On this event" comes right after a sentence about the single outcome (bZ, aZ, aZ, aZ). The intended event is {E2_final raised}.
- Evidence: Line 190 makes the intended meaning clear. The argument itself is correct.

**Finding 10**
- Location: PROOF Theorem 11 proof, lines 205–206.
- Severity: exposition.
- Claim: The bound e³ − 1 > 19 (that is, e³ > 20) is used without justification. Theorem 10 justifies only the upper bound e³ < 20.1.
- Evidence: I checked it: e > 2.718 gives e³ > 2.718³ ≈ 20.079 > 20.

**Finding 11**
- Location: STATEMENT.md §3 (c), last clause; PROOF Remark 7, lines 143–148.
- Severity: exposition.
- Claim: "The event {Z ≥ αẐ} places no upper limit on Z/Ẑ" is informal. Remark 7 also treats it informally.
- Evidence: As mathematics it is the identity {Z ≥ αẐ} = {Z/Ẑ ≥ α}. It is true, but it is not a separate claim that needs proof.

No fatal findings. No gaps. Under exactly the hypotheses in STATEMENT.md §2, PROOF_v1.tex proves (a), (b), (c), (d1) and (d2), with (d) for both SD divisors. STATEMENT.md is a faithful formalisation of source clause (i); findings 1, 2 and 5 note that it should say more explicitly why the non-implication reading is the one intended.

**verified**
