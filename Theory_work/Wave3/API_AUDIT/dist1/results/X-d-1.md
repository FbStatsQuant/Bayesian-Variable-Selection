# X-d-1
stop_reason: end_turn

# Card X, route X-d (adversarial): no counterexample found

**Verdict.** I found no design satisfying (E), (C) and (ND) that violates Lemma X as written, and the reason is structural rather than a lack of candidates. What I can give is (1) the reason every attack class is dominated, (2) the attacks I ran with their computations, and (3) two boundary facts: (C) cannot be dropped, and the constants must satisfy two relations. Nothing below is a proof of Lemma X.

## 1. Why the design has no freedom left

Write ρ′ := (‖μ‖² + ‖θ*‖²)/n ≤ M + M′, ℓ(S) := w(|S|)D_S^{−1/2}(2b + Q^c_S)^{−ν}, and for J ∩ S₀ = ∅ put S_J := S₀ ∪ J, χ²_J := σ*⁻²‖(P_{S_J} − P_{S₀})e‖² ~ χ²_{d_J} with d_J ≤ |J|.

- **(R1) Non-supersets, any design.** For S ⊉ S₀: π(S) ≤ ℓ(S)/ℓ(S₀) ≤ (2p)^{s₀}(n+1)^{s₀/2}·ℓ(S ∪ S₀)/ℓ(S₀). This is [T03R] (C6)(a); it uses only D_{S′}/D_S ≤ (n+1)^{|S′∖S|}, the prior ratio, and Q monotone.
- **(R2) Supersets, no floor on S₀.** Taking φ = θ* in the min-formula gives Q^c_{S₀} ≤ ‖e‖² + ρ′. Since μ_c ∈ col X_{c,S_J}, Q^c_{S_J} ≥ ‖(I − P_{S_J})e‖². Hence
  ℓ(S_J)/ℓ(S₀) ≤ [w(s₀+j)/w(s₀)]·(D_{S₀}/D_{S_J})^{1/2}·exp{ν(σ*²χ²_J + ‖P_{S₀}e‖² + ρ′)/(‖e‖² − ‖P_{S_J}e‖²)}.
- **(R3) The prior is exchangeable.** Σ_{|J|=j}[w(s₀+j)/w(s₀)](D_{S₀}/D_{S_J})^{1/2} = C(p−s₀, j)·[w(s₀+j)/w(s₀)]·(the (ND) average) ≤ 2(j+1)^{s₀}2^{−j}[c_D(n+1)]^{−j/2}, by [P1] `lem:prior`(e). So (ND) is exactly the prior-weighted Occam sum. The only J-dependent random factor left is e^{χ²_J/2}1{χ²_J ≤ τ_j}, whose mean is ≤ (eτ_j/j)^{j/2} uniformly in J. Markov uses linearity only, so dependence between different J cannot be exploited.
- **(R4) Small models, deterministic on the noise event.** For |S| ≤ d_t either L_S ≤ C″σ*²t, and D1(b),(d) of `D_hellinger.md` give a good fit and variance; or L_S > C″σ*²t, and Q^c_S − Q^c_{S₀} ≥ L_S/2 − Cσ*²t kills the model against S₀ with prior loss at most 2(2p)^{s₀}(n+1)^{s₀/2}.

So the design enters only through D-ratios (averaged exactly as the prior counts them), ranks d_J (monotone in the favourable direction) and L_S (a dichotomy). A counterexample must therefore sit in one of three places: the complement of the noise event (probability ≤ e^{−t}), the Markov failure for (R3) (probability ≤ e^{−ct} once C′ is large), or sizes above m_n(t) (Card S). I found no way to make any of these large.

**GAP 1.** (R1)–(R4) with constants and one n₀ is route X-a's job, and sizes above m_n(t) rest on Card S. I checked the inequalities in (R1)–(R3) but not the full bookkeeping.

## 2. Attacks tried

**A1. Clone cluster saturating the average in (ND).** Take s₀ = 0, μ = 0, with k copies of z = √N·Uu₀ and p − k further columns √N·Uu_i, the u's orthonormal. A set J with i ≥ 1 clones has D_J = f(iN)n^{j−i} ≥ n^{j−i+1}, and the chance of i clones among j draws is ≤ C(j,i)(k/p)^i. So the (ND) average is ≤ n^{−j/2}(1+ρ)^j with ρ := k√n/p, and (ND) holds for every m with c_D = 3/(4(1+ρ)²). Thus k ≈ ρp/√n clones are allowed, each a free extension of any other clone (D-ratio ≈ 1).

It fails because the posterior odds of i clones against one clone, for the same other columns T with |T| = r, are ≤ (1+o(1))·C(k,i)w(r+i)/(k·w(r+1)) ≤ (ρ(r+i)/(2√n))^{i−1}/i!. Each extra clone still costs about ρ/√n, since few clones means few such models; this is (R3). All clone models fit the single direction u₀, so the fitted noise is unchanged. The same holds with the clones aligned to a weak direction of S₀.

**A2. Cheap directions that fit fresh noise.** A direction with Gram eigenvalue λ has Occam factor f(λ)^{−1/2} and smoother weight h(λ), and 1 − h(λ) = 1/f(λ) exactly. A direction that is cheap (f ≈ 1) has h ≈ 0: it gains no likelihood and fits no noise. Equivalently, with known variance and ρ′ = 0, E[(D_{S₀}/D_S)^{1/2}e^{eᵀ(M_S−M_{S₀})e/2σ*²}] = 1 for every S ⊇ S₀. No family is both under-penalised and noise-fitting.

**A3. Degenerate or junk S₀.** I tried duplicate truths, negligible coefficients on columns chosen adversarially, and a null proxy z ∝ μ that beats S₀ by a factor of order p. The dominant model T ≠ S₀ is then a good model (L_T small). Large extensions of T are covered by (R1) through T ∪ J ∪ S₀, at the polynomial cost (2p)^{s₀}(n+1)^{s₀/2} ≤ e^{Ct/M₀}. By interlacing, an extension that is cheap relative to T is cheap relative to S₀ up to (n+1)^{s₀}, so (ND) sees it.

**A4. Compensating coefficients inside (C).** Take θ* = τa with a the eigenvector of G_{S₀} for a small eigenvalue γ, τ² ≤ nM′. Then L_{S₀} = τ²γ(γ+1)/((n+1)γ+1) ≤ max(2M, 2M′), and a null column along that direction gains at most e^{(‖P_{S₀}e‖² + ρ′)/2σ*²}. That is the j-independent factor in (R2), paid once.

**A5. Top of the range, t = n^{1−κ₀}.** The plug-in surcharge per extra variable is exp{ε·C_A log n/2} with ε = O(√(t/n) + t log n/n), and ε log n ≤ n^{−κ₀/2}log n + n^{−κ₀}log²n → 0 uniformly in the range. The same computation at t ≍ n gives a factor n^{c} per variable; that is outside the statement.

**A6. Cap and unions outside Ω.** For |S| ≤ m_n(t), |S∖S₀| ≤ min(m_n(t), p − s₀), which is inside the (ND) range even when S ∪ S₀ ∉ Ω. With K = p nothing happens.

**A7. Spike columns (high-leverage rows).** Columns ∝ e_i − 1/n are nearly orthonormal in contrast coordinates, so this is the orthogonal design of §3(b). It gives relations among constants, not a violation.

## 3. Boundary facts

**(a) (C) cannot be dropped; rigorous counterexample to that variant.** Take n ≥ 4, p = s₀ = K = 2, X_c = √N[u₁, cos φ·u₁ + sin φ·u₂], and γ := N(1 − cos φ) = n^{−4}. Let a = (1, −1)/√2, u_w := X_ca/√γ, θ* := √(nM/γ)·a. Then:

- μ_c = √(nM)u_w, so (E; M) holds with equality; (ND) is vacuous since p − s₀ = 0; ‖θ*‖² = n⁵M, so (C) fails.
- For every S ⊆ {1,2}, M_S ⪯ M_{12} and M_{12}u_w = h(γ)u_w with h(γ) ≤ nγ. Hence |u_wᵀM_Sy_c| ≤ √(nγ)‖y_c‖ and Var(u_wᵀX_{c,S}θ | v, S, y) ≤ vnγ.
- On {‖y_c‖² ≤ 4n(M+σ*²)}, which has probability → 1, E[v | S, y] ≤ 2s_y² ≤ 12(M+σ*²).
- By Markov, Π(‖μ̂ − μ‖² ≥ nM/4 | y) ≥ 1 − O(n^{−4}) for large n.

Since nM/4 > Cσ*²n^{1−κ₀} eventually, the mean clause fails with posterior mass → 1 on an event of probability → 1, for every choice of constants. Here L_{S₀} ≥ (1 − nγ)nM. So a bound on L_{S₀} is essential.

**(b) Relations the constants must satisfy (orthogonal design).** Take p = min(⌊n^A⌋, ⌊n/2⌋) with A ≤ 1, x_j = √N·Uu_j with u_j orthonormal, s₀ = 0, μ = 0. Then D_S = n^{|S|}, M_S = (N/n)P_S, and (ND; n/(n+1), every m) holds. Let Z_j := u_jᵀe/σ*, iid N(0,1).

- For j ∉ S: π(S)/π(S ∪ {j}) ≤ 2p√n·exp{−Z_j²/(2(1+δ′))} on {‖e‖² ≤ Nσ*²(1+δ)}, with δ′ → 0.
- Let x_k := 2(1+δ′)log(8kp√n). If Z_j² ≥ x_k for all j in a k-set S*, then π(S ⊇ S*) ≥ 3/4.
- Then Π(‖μ̂ − μ‖² ≥ (N/n)²σ*²k·x_k | y) ≥ 3/8, because a Gaussian vector exceeds its mean in norm with probability ≥ ½.
- By a binomial count, this event has probability ≥ (7/18)(p·e^{−x_k/2}/(6k√x_k))^k = n^{−k/2−o(1)} for fixed k.

Applying Lemma X at t = M₀ log n forces, to leading order,

  ⌈C′M₀⌉ + 1 ≥ 2cM₀  and  C ≥ (4A+2)c − (2A+1)/M₀.

Both are compatible with the statement. They show that d_t ≍ t/log n and the linear-in-t radius, with A-dependence, are the right shape, and that c cannot be taken near 1 with a small C.

**GAP 2.** The o(1) terms in (b) (δ′, √x_k, k-dependence) are tracked to leading order only. This affects only the necessary relations, not the verdict.

**Not attempted.** Whether the mean clause survives without (ND) (the S-FIT question). The size clause is known to fail there by [T03R] Proposition D.

ATTEMPT X/X-d RESULT=NO-PROGRESS GAPS=2
