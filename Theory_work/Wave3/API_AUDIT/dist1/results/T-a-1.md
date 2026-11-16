# T-a-1
stop_reason: end_turn

# Card T, route T-a — Lemma T (distribution-free transfer)

**Result.** The card's statement is proved with its exact constants. The relative-deviation inequality is proved here (Theorem RD), using one cited external fact (a binomial lower bound) and the Sauer–Shelah lemma. Both citations are from memory and need a cite-check. Remark 2 gives a variant with no external probability input, with constant 6 in place of 4.

Throughout, P is the (Borel) law of x, P_n the empirical measure of x₁, …, x_n, and Pg := E_x g(x).

## 0. External results

**(BIN)** Greenberg & Mohri (2014), "Tight lower bound on the probability of a binomial exceeding its expectation", *Statist. Probab. Lett.* 86, 91–98, Theorem 1. For every integer m ≥ 1 and p ∈ (1/m, 1], if B ~ Bin(m, p) then P(B ≥ mp) > 1/4.

**(SS)** Sauer–Shelah lemma: Sauer (1972), *J. Combin. Theory Ser. A* 13, 145–147; also van der Vaart & Wellner (1996), Cor. 2.6.3. If no set of V + 1 points is shattered by a class 𝒞, then 𝒞 has at most Σ_{i=0}^{V} C(N, i) distinct traces on any N points.

Everything else is proved below. For orientation only (not used): Theorem RD is the inequality usually attributed to Vapnik, as in Anthony & Shawe-Taylor (1993), *Discrete Appl. Math.* 47, 207–217, Thm 2.1, and Boucheron–Bousquet–Lugosi (2005), *ESAIM: P&S* 9, 323–375, Thm 5.1.

## 1. Theorem RD (relative deviation, countable class)

For a class 𝒜 of Borel sets and N ≥ 1, let S_𝒜(N) := sup over tuples (z₁, …, z_N) ∈ (ℝ^P)^N, repetitions allowed, of the number of distinct vectors (1_A(z_i))_{i≤N}, A ∈ 𝒜.

**Theorem RD.** Let 𝒜₀ be a countable class of Borel sets, n ≥ 1, η > 0, and x₁, …, x_n i.i.d. P. Then

  P( ∃A ∈ 𝒜₀ : P(A) − P_n(A) > η√P(A) ) ≤ 4 S_{𝒜₀}(2n) exp(−nη²/4).

*Proof.* If nη² ≤ 4 log 4 the right side is ≥ 1. Assume nη² > 4 log 4 > 1.

Let x′₁, …, x′_n be an independent ghost sample with empirical measure P′_n. Define

- E := {∃A ∈ 𝒜₀ : P(A) − P_n(A) > η√P(A)},
- E₂ := {∃A ∈ 𝒜₀ : P′_n(A) − P_n(A) > η√((P_n(A) + P′_n(A))/2)}.

Both are countable unions of measurable events.

*Step 1: P(E) ≤ 4P(E₂).*

1. Enumerate 𝒜₀ = {A₁, A₂, …}. On E let A* := A_k with k minimal such that the inequality in E holds. A* is a function of (x_i) with countably many values, each taken on a measurable event. Put p* := P(A*).
2. On E, p* − η√p* > P_n(A*) ≥ 0, so √p* > η and p* > η² > 1/n.
3. Conditionally on (x_i), by independence, nP′_n(A*) ~ Bin(n, p*). By (BIN), P(P′_n(A*) ≥ p* | (x_i)) > 1/4 on E.
4. For 0 ≤ x < y let F(x, y) := (y − x)/√((x + y)/2). Then ∂_yF has the sign of (x + y) − (y − x)/2 = (3x + y)/2 > 0, and ∂_xF has the sign of −(x + y) − (y − x)/2 < 0.
5. On E ∩ {P′_n(A*) ≥ p*} write x := P_n(A*) and y := P′_n(A*), with x₀ := p* − η√p* > 0. Then x < x₀ < p* ≤ y, so
  F(x, y) ≥ F(x, p*) ≥ F(x₀, p*) = η√p*/√(p* − η√p*/2) > η.
 Hence E₂ holds.
6. Therefore P(E₂) ≥ E[1_E · P(P′_n(A*) ≥ p* | (x_i))] ≥ P(E)/4.

*Step 2: P(E₂) ≤ S_{𝒜₀}(2n) e^{−nη²/4}.*

1. Let σ₁, …, σ_n be i.i.d. Rademacher signs independent of (x, x′). Swap x_i ↔ x′_i when σ_i = −1. The swapped pair of samples has the law of (x, x′), so P(E₂) = P(E₂^σ), where E₂^σ is E₂ evaluated on the swapped samples.
2. For A ∈ 𝒜₀ put a_i := 1_A(x′_i) − 1_A(x_i) ∈ {−1, 0, 1} and Σ_A := Σ_i (1_A(x_i) + 1_A(x′_i)). On the swapped samples, P′_n(A) − P_n(A) = n⁻¹Σ_iσ_ia_i and P_n(A) + P′_n(A) = Σ_A/n (unchanged).
3. So E₂^σ = ∪_A {Σ_iσ_ia_i > η√(nΣ_A/2)}. Given (x, x′), the event for A depends on A only through its trace on the 2n points, so the union has at most S_{𝒜₀}(2n) distinct members.
4. For one of them: if Σ_ia_i² = 0 the event is {0 > η√(nΣ_A/2)}, which is empty. Otherwise use Hoeffding for Rademacher sums: E e^{λΣσ_ia_i} = Π cosh(λa_i) ≤ e^{λ²Σa_i²/2}, so P_σ(Σσ_ia_i > t) ≤ exp(−t²/(2Σa_i²)).
5. Since Σ_ia_i² ≤ Σ_A, with t² = η²nΣ_A/2 the bound is ≤ exp(−nη²/4).
6. Union bound, then expectation over (x, x′). ∎

## 2. Growth function of the level-set class

Let 1 ≤ d ≤ P and 𝒜 := { A_{a,u,s} := {x : |a + uᵀx| > s} : a ∈ ℝ, u ∈ ℝ^P, |supp u| ≤ d, s ≥ 0 }.

**Lemma G.** For N ≥ d + 1: S_𝒜(N) ≤ C(P, d)·(eN/(d+1))^{2(d+1)} ≤ (eP/d)^d (eN/(d+1))^{2(d+1)}.

*Proof.*

1. *Reduction to half-spaces.* Since d ≤ P, every u with |supp u| ≤ d has supp u ⊆ T for some T ⊆ [P] with |T| = d. Then A_{a,u,s} = {a − s + uᵀx > 0} ∪ {−a − s − uᵀx > 0} is a union of two members of ℋ_T := {{f > 0} : f ∈ 𝒱_T}, where 𝒱_T := span{1, x_j (j ∈ T)} has dimension d + 1.
2. *ℋ_T shatters no d + 2 points.* Let z₁, …, z_{d+2} be given. The map f ↦ (f(z_i))_i sends 𝒱_T to a subspace of ℝ^{d+2} of dimension ≤ d + 1. So there is w ≠ 0 with Σ_iw_if(z_i) = 0 for all f ∈ 𝒱_T, and after a sign change I₊ := {i : w_i > 0} ≠ ∅. If some f had {i : f(z_i) > 0} = I₊, then Σ_{i∈I₊}w_if(z_i) > 0 and every other term w_if(z_i) is ≥ 0 (w_i ≤ 0, f(z_i) ≤ 0), a contradiction.
3. *Trace count for ℋ_T.* A trace on a tuple is determined by the trace on its N′ ≤ N distinct points. By (SS) with V = d + 1 the number of traces is ≤ Σ_{i≤V}C(N, i). For N ≥ V: (V/N)^VΣ_{i≤V}C(N, i) ≤ Σ_iC(N, i)(V/N)^i = (1 + V/N)^N ≤ e^V. So the count is ≤ (eN/(d+1))^{d+1}.
4. *Unions and supports.* The trace of H₁ ∪ H₂ is the coordinatewise maximum of the two traces, so unions of two members of ℋ_T have ≤ (eN/(d+1))^{2(d+1)} traces. Sum over the C(P, d) ≤ P^d/d! ≤ (eP/d)^d choices of T (using d! ≥ (d/e)^d). ∎

## 3. Proof of Lemma T

Fix 1 ≤ d ≤ min(P, n − 1) and δ ∈ (0, 1). Set

  η² := (4/n)[ d log(eP/d) + 2(d+1) log(2en/(d+1)) + log(4/δ) ] > 0.

**Step A (countable class).** Let 𝒜₀ := {A_{a,u,s} ∈ 𝒜 : a ∈ ℚ, u ∈ ℚ^P, s ∈ ℚ ∩ [0, ∞)}. It is countable and 𝒜₀ ⊆ 𝒜. Since 2n ≥ d + 1, Lemma G with N = 2n and Theorem RD give

  P(E₀) ≤ 4 (eP/d)^d (2en/(d+1))^{2(d+1)} e^{−nη²/4} = δ,

where E₀ := {∃A ∈ 𝒜₀ : P(A) − P_n(A) > η√P(A)}. The rest is deterministic on E₀ᶜ.

**Step B (real levels).** Fix rational (a, u) with |supp u| ≤ d and real s ≥ 0. Take rational s_k ↓ s. Then A_{a,u,s_k} ↑ A_{a,u,s}, so P and P_n of these sets converge from below. Passing to the limit in P(A_{a,u,s_k}) − P_n(A_{a,u,s_k}) ≤ η√P(A_{a,u,s_k}) gives the same inequality for A_{a,u,s}.

**Step C (layer cake and Cauchy–Schwarz; rational (a, u), c = 1).** Let g(x) := min{1, (a + uᵀx)²} ∈ [0, 1].

1. For z ∈ (0, 1), {g > z} = A_{a,u,√z}. Since g = ∫₀¹1{g > z}dz, Tonelli gives Pg = ∫₀¹P(A_{a,u,√z})dz and P_ng = ∫₀¹P_n(A_{a,u,√z})dz.
2. By Step B and Cauchy–Schwarz on [0, 1]:
  Pg − P_ng ≤ η∫₀¹√P(A_{a,u,√z}) dz ≤ η(∫₀¹P(A_{a,u,√z})dz)^{1/2} = η√(Pg).
3. Since η√(Pg) ≤ (Pg + η²)/2, we get Pg ≤ 2P_ng + η².

**Step D (all real a, u, c).** Let a ∈ ℝ, c > 0, u ∈ ℝ^P with |supp u| ≤ d.

1. min{1, (a + uᵀx)²/c} = min{1, (ã + ũᵀx)²} with (ã, ũ) := (a, u)/√c.
2. Choose rational (a_k, u_k) → (ã, ũ) with supp u_k ⊆ supp u. The functions g_k := min{1, (a_k + u_kᵀx)²} converge pointwise to the target and are bounded by 1.
3. So Pg_k → Pg (dominated convergence) and P_ng_k → P_ng (finite sum). The inequality of Step C passes to the limit.

Hence on E₀ᶜ, which has probability ≥ 1 − δ, simultaneously for all (a, c, u) in the card's range:

  E_x min{1, (a + uᵀx)²/c} ≤ 2n⁻¹Σ_i min{1, (a + uᵀx_i)²/c} + (4/n)[d log(eP/d) + 2(d+1) log(2en/(d+1)) + log(4/δ)]. ∎

## Remarks

1. **What is used.** No moment, tail, atom-freeness or continuity assumption on the law of x is used; repeated sample points are covered by the definition of S(N). Measurability is handled by the countable class plus the pathwise extensions B and D. The range d ≤ n − 1 is more than needed: the proof uses only d ≤ min(P, 2n − 1). On the card's range all three bracket terms are positive.

2. **Variant with no external probability input.** If (BIN) is not accepted, replace item 3 of Step 1 by Cantelli's inequality. Since Var(P′_n(A*) | x) ≤ p*/n, we get P(P′_n(A*) > p* − √(p*/n) | x) ≥ 1/2. For η > n^{−1/2}, on that event F(x, y) ≥ F(x₀, p* − √(p*/n)) > η − n^{−1/2}. Step 2 is unchanged, so
  P(E_η) ≤ 2S(2n) exp(−n(η − n^{−1/2})²/4).
 With L′ := d log(eP/d) + 2(d+1) log(2en/(d+1)) + log(2/δ), the radius becomes η′ = n^{−1/2}(1 + 2√L′). On the card's range L′ ≥ 1 + 4 log(2e) + log 2 > 7, so (1 + 2√L′)² ≤ (1/7 + 4/√7 + 4)L′ ≤ 6L′. Lemma T then holds with remainder (6/n)[d log(eP/d) + 2(d+1) log(2en/(d+1)) + log(2/δ)], using only (SS).

3. **Answer to S1-01's query.** The constant 4, the factor 4·S(2n) and the exponent nη²/4 are correct as stated. The classical side condition (nη² > 1 or > 2) is harmless because the bound is trivial when nη² ≤ 4 log 4.

ATTEMPT T/T-a RESULT=PROVED GAPS=0
