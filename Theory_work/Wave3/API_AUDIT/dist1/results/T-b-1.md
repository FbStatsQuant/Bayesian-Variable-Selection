# T-b-1
stop_reason: end_turn

# Card T, route T-b — Lemma T via Bousquet's (Talagrand-type) inequality

**Outcome.** Route T-b proves Lemma T with the same form and the same domain, but with larger numerical constants. The card's constant 4 is not reached by this route. Nothing below needs a moment, tail or eigenvalue condition.

## 0. What is proved

**Lemma T♭.** Let x₁,…,x_n be i.i.d. from any Borel law on ℝ^P, 1 ≤ d ≤ min(P, n−1), δ ∈ (0,1). There is a measurable event of probability ≥ 1−δ on which, simultaneously for all a ∈ ℝ, c > 0 and u ∈ ℝ^P with |supp u| ≤ d,

  E_x min{1,(a+uᵀx)²/c} ≤ 2 n⁻¹Σ_i min{1,(a+uᵀx_i)²/c} + η_b²,

  η_b² := (1/n)[192 Λ_n + (124/3) log(1/δ)],
  Λ_n := d log(eP/d) + 2(d+1) log(en/(d+1)) + log(2 + log₂ n).

For n ≥ 3, η_b² ≤ (240/n)[d log(eP/d) + 2(d+1) log(2en/(d+1)) + log(4/δ)]. That is the card's statement with 4/n replaced by 240/n.

**Differences from the card.**
- Constant 192 (or 240 in the card's bracket) instead of 4.
- Growth function at n points instead of 2n points (a small gain).
- An extra log(2 + log₂ n) term, which is at most ¼ of the term 2(d+1) log(en/(d+1)) for n ≥ 3.
- 41.4·log(1/δ) instead of 4·log(4/δ).
- The order C(d log(P∨n) + log(1/δ))/n is unchanged, so ROUTES §2 Step 2 goes through with different constants.

## 1. External results used

**(B) Bousquet's inequality.** Bousquet (2002), "A Bennett concentration inequality and its application to suprema of empirical processes", C. R. Math. Acad. Sci. Paris 334, 495–500, Theorem 2.3; also Boucheron–Lugosi–Massart, *Concentration Inequalities* (2013), Theorem 12.5. Statement: let X₁,…,X_n be i.i.d. and 𝓗 a countable class of measurable functions with E h(X₁) = 0 and h ≤ 1 for all h. Put Z = sup_h Σ_i h(X_i), take σ² ≥ sup_h Var h(X₁), and v = nσ² + 2EZ. Then for all x ≥ 0, P(Z ≥ EZ + √(2vx) + x/3) ≤ e^{−x}. The bound is monotone in v, so v may be replaced by any upper bound.

**(S) Sauer's lemma.** Sauer (1972), J. Combin. Theory A 13, 145–147; van der Vaart–Wellner (1996), Cor. 2.6.3. A class of VC dimension ≤ V has at most Σ_{i≤V} C(n,i) ≤ (en/V)^V traces on n points, for n ≥ V ≥ 1.

The following three facts are proved here.

**(V) Positivity sets.** If 𝒢 is a vector space of real functions with dim 𝒢 ≤ m, then {{g > 0} : g ∈ 𝒢} has VC dimension ≤ m.
*Proof.* Suppose x₁..x_{m+1} are shattered. The image of g ↦ (g(x_i))_i has dimension ≤ m, so there is γ ≠ 0 with Σγ_i g(x_i) = 0 for all g. Flip the sign of γ if needed so that I₊ = {i : γ_i > 0} ≠ ∅. Pick g with {i : g(x_i) > 0} = I₊. Then Σ_{I₊} γ_i g(x_i) > 0 and Σ_{γ_i<0} γ_i g(x_i) ≥ 0, a contradiction. ∎

**(M) Massart's finite-class lemma.** For finite W ⊂ ℝⁿ with max_{w∈W}‖w‖₂ ≤ ρ and Rademacher signs σ: E max_w ⟨σ,w⟩ ≤ ρ√(2 log|W|).
*Proof.* For s > 0, exp(s·E max) ≤ Σ_w E e^{s⟨σ,w⟩} ≤ |W| e^{s²ρ²/2}. So E max ≤ log|W|/s + sρ²/2; optimise over s (let s ↓ 0 if |W| = 1). ∎

**(Sym) One-sided symmetrisation.** For a countable class 𝓕 of [0,1]-valued functions, E sup_f (P−P_n)f and E sup_f (P_n−P)f are both ≤ 2 E sup_f n⁻¹Σσ_i f(x_i).
*Proof.* With a ghost sample x′, sup_f (P−P_n)f = sup_f E′[(P′_n−P_n)f] ≤ E′ sup_f n⁻¹Σ(f(x′_i) − f(x_i)). The law of this is invariant under swapping x_i ↔ x′_i, so its expectation equals E sup_f n⁻¹Σσ_i(f(x′_i) − f(x_i)) ≤ 2E sup_f n⁻¹Σσ_i f(x_i). The other sign is identical. ∎

## 2. Reduction to a countable class of sets

For a ∈ ℝ, s ≥ 0, u ∈ ℝ^P put A_{a,u,s} := {x : |a + uᵀx| > s}. Let 𝒜 := {A_{a,u,s} : |supp u| ≤ d} and let 𝒜₀ ⊆ 𝒜 be the subclass with rational (a,u,s). Then ∅ = A_{0,0,0} ∈ 𝒜₀.

**(2a) Level sets.** For g = min{1,(a+uᵀx)²/c} and z ∈ [0,1): {g > z} = A_{a,u,√(cz)} ∈ 𝒜. By Tonelli, Pg = ∫₀¹P(g>z)dz and P_n g = ∫₀¹P_n(g>z)dz. Hence, for any η² ≥ 0,

  [P(A) ≤ 2P_n(A) + η² for all A ∈ 𝒜] ⇒ [Pg ≤ 2P_n g + η² for all (a,u,c)]. (2.1)

The target inequality is linear in A, so no Cauchy–Schwarz step is needed.

**(2b) Growth function.** Any u with |supp u| ≤ d has supp u ⊆ T for some |T| = d (possible since d ≤ P). Then A_{a,u,s} = {a − s + uᵀx > 0} ∪ {−a − s − uᵀx > 0} is a union of two positivity sets of span{1, x_j (j ∈ T)}, which has dimension ≤ d+1. By (V) and (S), since n ≥ d+1, each T contributes at most (en/(d+1))^{2(d+1)} traces on any n points (repetitions allowed). There are C(P,d) ≤ (eP/d)^d sets T. So

  log S_𝒜(n) ≤ d log(eP/d) + 2(d+1) log(en/(d+1)). (2.2)

**(2c) From 𝒜₀ to 𝒜, pathwise.** Fix a sample and A = A_{a,u,s} ∈ 𝒜. Choose rational (a_k,u_k) → (a,u) with supp u_k ⊆ supp u. Put ε_k := max_i |a_k − a + (u_k − u)ᵀx_i| → 0 and take rational s_k ∈ [s+ε_k, s+2ε_k+1/k]. Write A_k := A_{a_k,u_k,s_k} ∈ 𝒜₀.
- If x_i ∉ A then |a_k + u_kᵀx_i| ≤ s + ε_k ≤ s_k, so x_i ∉ A_k. Hence P_n(A_k) ≤ P_n(A).
- If x ∈ A then x ∈ A_k eventually, since s_k → s. By Fatou, P(A) ≤ liminf P(A_k).

So if P(A′) ≤ 2P_n(A′) + η² for all A′ ∈ 𝒜₀, the same holds for all A ∈ 𝒜. The event for 𝒜₀ is measurable (countable class). This settles measurability of the supremum.

## 3. Ratio inequality for sets from Bousquet's inequality

**Proposition R.** Let 𝒜₀ be a countable class of measurable sets with ∅ ∈ 𝒜₀, n ≥ 2, x > 0, and L ≥ log S_{𝒜₀}(n) + log(2 + log₂ n). With probability ≥ 1 − e^{−x},

  P(A) ≤ 2P_n(A) + (192 L + (124/3)x)/n for all A ∈ 𝒜₀.

*Proof.* Put ℓ := L/n, ξ := x/n, r := 768ℓ + (496/3)ξ. Since L ≥ log 2, r > 1/n.

*Weights.* For A ∈ 𝒜₀ let k(A) := min{k ∈ ℕ₀ : r2^k ≥ P(A)} and f_A := 2^{−k(A)}1_A ∈ [0,1]. Then:
- k(A) ≤ k_max := max(0, ⌈log₂(1/r)⌉) ≤ ⌈log₂ n⌉, so k(A) takes at most 2 + log₂ n values.
- P f_A² = 2^{−2k}P(A) ≤ r2^{−k} ≤ r, so Var f_A ≤ r.
- f_∅ = 0.

Put V := sup_A (P−P_n)f_A ≥ 0 and V⁻ := sup_A (P_n−P)f_A ≥ 0.

*Step 1 (deterministic).* On {V ≤ r/4}, every A ∈ 𝒜₀ satisfies P(A) ≤ 2P_n(A) + r/4.
Indeed (P−P_n)(A) = 2^k(P−P_n)f_A ≤ 2^{k−1}·r/2. If k = 0 this is r/4. If k ≥ 1, minimality of k gives r2^{k−1} < P(A), so (P−P_n)(A) < P(A)/2 and P(A) < 2P_n(A).

*Step 2 (expectation).* EV ≤ 2√(2ℓr) + 8ℓ.
Let ρ := E sup_A n⁻¹Σσ_i f_A(x_i). By (Sym), EV ≤ 2ρ and EV⁻ ≤ 2ρ. Given the sample, the vectors (f_A(x_i))_{i≤n} have the form 2^{−k}·(trace of A) with 0 ≤ k ≤ k_max. There are at most S(n)(2 + log₂ n) ≤ e^L of them, each with squared norm nP_n f_A². Also

  P_n f_A² = P f_A² + 2^{−k}(P_n−P)f_A ≤ r + V⁻.

By (M) and Jensen, ρ ≤ E√(2L(r+V⁻)/n) ≤ √(2ℓ(r+2ρ)). So ρ² ≤ 2ℓr + 4ℓρ, which gives ρ ≤ 2ℓ + √(4ℓ² + 2ℓr) ≤ √(2ℓr) + 4ℓ.

*Step 3 (concentration).* Apply (B) to h_A := Pf_A − f_A. These have mean 0, h_A ≤ 1, Var ≤ r, and Z = nV. With probability ≥ 1 − e^{−x},

  V < EV + √(2ξ(r + 2EV)) + ξ/3 ≤ (3/2)EV + √(2ξr) + (7/3)ξ,

using 2√(ξ·EV) ≤ EV/2 + 2ξ. By Step 2 and AM–GM:
- (3/2)EV ≤ 3√(2ℓr) + 12ℓ ≤ r/8 + 36ℓ + 12ℓ;
- √(2ξr) ≤ r/16 + 8ξ.

Hence V < 3r/16 + 48ℓ + (31/3)ξ = 3r/16 + r/16 = r/4 by the choice of r. Step 1 gives the claim with r/4 = 192ℓ + (124/3)ξ. ∎

*Check for r ≥ 1.* Then k(A) ≡ 0 and all steps hold verbatim; the claim is trivial anyway.

*General parameters.* Use peeling ratio λ > 1 instead of 2, α > 0 in the split 2√(ξ·EV) ≤ α·EV + ξ/α, and AM–GM weights g₁/(2λ), g₂/(2λ) with g₁ + g₂ < 1. The same proof gives

  η² = {[4λ(1+α)²/g₁ + 8(1+α)]ℓ_λ + [λ/g₂ + 1/3 + 1/α]ξ}/(1 − g₁ − g₂),

with ℓ_λ = [log S(n) + log(2 + log_λ n)]/n. The choice above is λ = 2, α = ½, g₁ = ½, g₂ = ¼.

## 4. Proof of Lemma T♭

By (2.2), L := Λ_n satisfies the hypothesis of Proposition R for 𝒜₀, since S_{𝒜₀} ≤ S_𝒜. Take x = log(1/δ). On the resulting event, P(A) ≤ 2P_n(A) + η_b² for all A ∈ 𝒜₀, hence for all A ∈ 𝒜 by (2c), hence the claim by (2.1).

For the 240-form, take n ≥ 3. The map m ↦ m log(en/m) is increasing on (0,n], so 2(d+1) log(en/(d+1)) ≥ 4 log(en/2). Also log(2 + log₂ n) ≤ log(en/2) for n ≥ 3: it holds at n = 3 (1.277 ≤ 1.405) and the difference is increasing. Therefore Λ_n ≤ (5/4)[d log(eP/d) + 2(d+1) log(en/(d+1))], and 192·(5/4) = 240, 124/3 < 240. ∎

## 5. Comparison of constants with route T-a, and limits of this route

| | leading constant | growth function | δ term |
|---|---|---|---|
| Card / T-a | 4 | log S(2n) | 4 log(4/δ) |
| T-b, clean choice | 192 | log S(n) + log(2 + log₂ n) | (124/3) log(1/δ) |
| T-b, best possible by this argument | > 16 | log S(n) + log(2 + log_λ n) | blows up as the limit is approached |

- The T-a figures rest on the relative-deviation inequality P(sup_A (P−P_n)(A)/√P(A) > η) ≤ 4S(2n)e^{−nη²/4}, attributed to Anthony–Shawe-Taylor (1993). I did not verify that source; it is not used here.
- The infimum of the T-b leading coefficient is 16, approached as λ → 1, α → 0, g₁ → ½, g₂ → 0. The factor 16 comes from two symmetrisations (factor 2 each on the √ term, squared) and the AM–GM step. So this route cannot give the card's constant 4.
- Replacing the weight-counting in Step 2 by peeling in expectation (Bartlett–Bousquet–Mendelson style) removes the log log term but costs a factor λ/(1−λ^{−1/2})² ≥ 16, giving a leading constant ≥ 256. Counting is the better variant.
- The published Giné–Koltchinskii and Bartlett–Bousquet–Mendelson ratio theorems are not used; everything rests on Bousquet's inequality plus the elementary facts proved in §1.
- **Recommendation.** If the exact constant 4 matters, it must come from T-a. For DIST-1 and DIST-2 only η² ≤ C(d log(P∨n) + log(1/δ))/n is used, and T♭ supplies that with no unverified citation beyond Bousquet's theorem and Sauer's lemma.

**Robustness points (the T-c concerns, as they bear on this proof).**
- Heavy tails and atoms: only indicators of sets enter. Repeated sample points only reduce the number of traces.
- d close to n: (2.2) needs exactly n ≥ d+1, the card's domain. Λ_n ≥ 0 throughout, so S1-01's negative-remainder problem cannot occur.
- Measurability: handled in (2c).

ATTEMPT T/T-b RESULT=PROVED-VARIANT GAPS=0
