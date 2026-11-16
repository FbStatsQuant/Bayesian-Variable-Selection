# B-c-1
stop_reason: end_turn

# Card B, route B-c (adversarial): no counterexample exists; the statement is true with c₂ = 1/87552

The three attack families (degenerate directions, atoms, q at its limit) only constrain the constant c₂ or hit trivial cases. The reason they must fail is a complete proof, given in §2–3. One nearby weakening of the hypothesis is false, with an explicit counterexample (§1, A2).

Throughout, 𝖭 := n/K⁴ and Λ := q′ log(ep/q′). For q ≥ 1 two facts hold:
- **K ≥ 1.** Since cosh x ≥ 1 + x²/2 and Var(z₁) = 1, we get 1 + λ²/2 ≤ E cosh(λz₁) ≤ e^{K²λ²/2}; let λ → 0.
- **Λ ≥ q′ ≥ 1**, because p/q′ ≥ 1.

For q = 0 the claim reads a² ≥ a²/2 and is trivial.

## 1. Attacks and why each fails

**A1. Exactly degenerate directions.** Take z₂ = z₁ and u = e₁ − e₂. The hypothesis holds for u (it reads 1 ≤ 1). The conclusion reads a² ≥ a²/2, which is true. In general Var(uᵀz) = 0 forces uᵀz = 0 a.s., and the kernel of Cov(z_T) is spanned by finitely many such u, so one null set covers all of them. No failure. A Euclidean net in u would break here, but the statement is scale-free in Cov(z_T)^{1/2}u (Step 1 of §2).

**A2. Nearly degenerate direction with an atom.** Let g ~ N(0,1) and let h be independent with P(h = ±δ^{−1/2}) = δ/2, P(h = 0) = 1 − δ. Put z₁ = g, z₂ = √(1−δ)·g + √δ·h, δ = 1/n.
- Each coordinate is sub-Gaussian with K² = 2: E e^{λ√δh} = 1 − δ + δ cosh λ ≤ cosh λ ≤ e^{λ²/2}.
- λ_min(Corr) = 1 − √(1−δ) ≥ 1/(2n), so (A4) holds with c_ψ = ½.
- For u = (−√(1−δ), 1)/√δ we have uᵀz = h, Var = 1. With probability (1 − 1/n)ⁿ ≥ 8/27 all h_i = 0, so n⁻¹Σ(uᵀz_i)² = 0 < ½.
- On that event the two standardised columns coincide, λ_min(G_T) = 0, and D_{12}/D_{1} = (2n² − 1)/(n(2n − 1)) ≈ 1 + 1/(2n): no Occam factor.

This is not a counterexample to the card. The card's hypothesis for 2-sparse u fails here unless K² ≥ 1/(2δ log(2/δ)) = n/(2 log 2n) (computed in A3), and then q′log(ep/q′) ≤ c₂n/K⁴ is violated. It does show that (A3) on q-sparse directions cannot be replaced by coordinatewise sub-Gaussianity, nor by a bounded-K coordinate condition plus (A4) at level c_ψ/n. It also shows that route B-b's fourth-moment variant must be imposed on sparse directions, since E h⁴ = n here.

**A3. Atoms in a coordinate.**
- *Rademacher z₁ (K = 1), u = e₁.* Minimising LHS − a²/2 over a gives 1 − 2m² with m the sample mean. Failure occurs iff |m| > ½, with probability e^{−n(I+o(1))}, I = ½(1.5 ln 1.5 + 0.5 ln 0.5) = 0.1308. This forces c₂ ≤ 0.131 and nothing more.
- *Sparse atom z₁ = h.* Failure probability is at least (1−δ)ⁿ. Taking λ = t√δ with t = 2 log(2/δ): E e^{λh} ≥ 2/δ, so K² ≥ 2 log(2/δ)/(t²δ) = 1/(2δ log(2/δ)). The claimed bound e^{−c₂n/K⁴} is at least e^{−4c₂nδ² log²(2/δ)}. This would be beaten only if 4c₂δ log²(2/δ) ≳ 1, which is impossible for c₂ < 0.23 since sup_δ δ log²(2/δ) = 4·2/e² ≈ 1.08. The K⁻⁴ rate is lossy (the true rate is about 1/(K² log K)), not optimistic.

**A4. q at its limit.**
- *Rank.* If q′ ≥ n and some Corr(x_T), |T| = n, is nonsingular, the n equations a + uᵀz_i = 0 have a solution (a, u) ≠ 0 with u ≠ 0, so the conclusion fails surely. The condition excludes this: q′ ≤ Λ ≤ c₂n < n.
- *Gaussian, p = q, K = 1.* Here Λ = q. By Bai–Yin (Ann. Probab. 21 (1993) 1275–1294, Thm 2), λ_min(n⁻¹ΣzzᵀT) → (1 − √γ)² when q/n → γ. This is below ½ for γ > (1 − 2^{−1/2})² ≈ 0.0858, so c₂ ≤ 0.0858 is forced.

Both are constraints on c₂ only.

**A5. Same c₂ in the condition and in the probability; small n.** For q ≥ 1 the condition forces c₂𝖭 ≥ Λ ≥ 1, so prefactors are absorbed (end of §2). No failure.

**A6. The consequence.** I attacked the data-dependent standardisation at floor level c_ψ/n. The transfer is multiplicative and holds with slack factor 2 (§3). No failure.

## 2. Proof of B2-core (q ≥ 1), c₂ := 1/87552

**Fact 1 (scalar tails).** Let g be real with E g = 0, E g² = 1, E e^{λg} ≤ e^{K²λ²/2} for all λ, and g₁, …, g_n i.i.d. copies. Then

- (a) P(ḡ ≥ s) ≤ e^{−ns²/(2K²)} for s > 0;
- (b) P(|n⁻¹Σg_i² − 1| ≥ t) ≤ 2e^{−nt²/(228K⁴)} for 0 < t ≤ 1.

*Proof.* (a) is Chernoff with λ = s/K².

For (b), put ξ = g².
- *Moment generating function of ξ.* With γ ~ N(0,1) independent and Tonelli, for 0 ≤ μ < 1/(2K²): E e^{μξ} = E_γE_g e^{√(2μ)γg} ≤ E_γ e^{K²μγ²} = (1 − 2K²μ)^{−1/2}.
- *Moments.* At μ = 1/(4K²), using x^k/k! ≤ e^x: E ξ² ≤ 2·16·√2·K⁴ ≤ 46K⁴ and E ξ⁴ ≤ 24·256·√2·K⁸ ≤ 8689K⁸.
- *Lower tail.* Since e^{−x} ≤ 1 − x + x²/2 for x ≥ 0, E e^{−λξ} ≤ exp(−λ + 23K⁴λ²). Chernoff with λ = t/(46K⁴) gives P(n⁻¹Σξ_i ≤ 1 − t) ≤ e^{−nt²/(92K⁴)}.
- *Upper tail.* Use e^y ≤ 1 + y + (y²/2)e^{y₊} with y = λ(ξ − 1), 0 ≤ λ ≤ 1/(8K²), y₊ ≤ λξ and (ξ−1)² ≤ ξ² + 1. Then E e^y ≤ 1 + (λ²/2)[(Eξ⁴)^{1/2}(E e^{2λξ})^{1/2} + E e^{λξ}] ≤ 1 + (λ²/2)[93.3·2^{1/4} + 1.16]K⁴ ≤ exp(57K⁴λ²). Chernoff with λ = t/(114K⁴), which is ≤ 1/(8K²) for t ≤ 1, gives e^{−nt²/(228K⁴)}. ∎

**Step 1 (whitening; handles all degenerate directions).** Fix T ⊆ [p] with |T| = q′. Let Σ_T = Cov(z_T) and V = range Σ_T, with r = dim V ∈ [1, q′].
- For u ∈ ker Σ_T, uᵀz_T = 0 a.s. Hence a.s. z_{i,T} ∈ V for all i.
- Put w_i := (Σ_T^†)^{1/2}z_{i,T} ∈ V. Then z_{i,T} = Σ_T^{1/2}w_i, and for all u ∈ ℝ^T simultaneously, uᵀz_i = v_uᵀw_i with v_u := Σ_T^{1/2}u and |v_u|² = Var(uᵀz).
- For v ∈ V, vᵀw = ũᵀz with ũ = (Σ_T^†)^{1/2}v supported in T (at most q nonzeros) and Var(ũᵀz) = |v|². So E e^{λvᵀw} ≤ e^{K²λ²|v|²/2}: for unit v ∈ V, g = vᵀw satisfies Fact 1.

**Step 2 (deterministic).** Let Â = n⁻¹Σw_iw_iᵀ on V. If ‖Â − I_V‖ ≤ ¼ and |w̄| ≤ ¼, then for all a ∈ ℝ, v ∈ V:

n⁻¹Σ(a + vᵀw_i)² = a² + 2a·vᵀw̄ + vᵀÂv ≥ a² − ½|a||v| + ¾|v|² ≥ ¾a² + ½|v|² ≥ ½(a² + |v|²).

By Step 1 this is the claim for every u supported in T.

**Step 3 (net).** Let 𝒩 be a ¼-net of the unit sphere of V with |𝒩| ≤ 9^r ≤ 9^{q′} (volumetric bound (1 + 2/ε)^r; Vershynin, *High-Dimensional Probability*, Cor. 4.2.13).
- For symmetric B on V: ‖B‖ ≤ 2 max_𝒩|v₀ᵀBv₀|, because |vᵀBv − v₀ᵀBv₀| ≤ 2|v − v₀|‖B‖.
- For h ∈ V: |h| ≤ (4/3) max_𝒩 v₀ᵀh.
- So the event of Step 2 holds if for all v₀ ∈ 𝒩, |n⁻¹Σ(v₀ᵀw_i)² − 1| ≤ 1/8 and v₀ᵀw̄ ≤ 3/16.
- By Fact 1 with t = 1/8, s = 3/16 and K ≥ 1, this fails with probability at most 9^{q′}[2e^{−𝖭/14592} + e^{−9n/(512K²)}] ≤ 4·9^{q′}e^{−c₀𝖭}, c₀ := 1/14592.

**Step 4 (union).** Every u with at most q nonzeros is supported in some T with |T| = q′, and there are C(p, q′) ≤ (ep/q′)^{q′} such T. Using log 4 ≤ 1.39Λ and q′ log 9 ≤ 2.2Λ:

P(fail) ≤ exp(log 4 + Λ + q′ log 9 − c₀𝖭) ≤ exp(4.6Λ − c₀𝖭) ≤ exp((4.6c₂ − c₀)𝖭) ≤ e^{−c₂𝖭},

since Λ ≤ c₂𝖭 and c₂ = c₀/6. ∎

## 3. Proof of the consequence (B1 + B2)

Let ℓ_j := ŝ_j/sd(x_j), where ŝ_j² has divisor n − 1. The standardised entries are X_ij = (z_ij − z̄_j)/ℓ_j.

For |T| ≤ q and u ∈ ℝ^T put v_j = u_j/ℓ_j, which has the same support. On the B2-core event and {ℓ_j² ≤ 2 ∀j}:

‖X_Tu‖² = Σ_i(vᵀ(z_i − z̄))² = min_a Σ_i(a + vᵀz_i)² ≥ (n/2)·Var(vᵀz) = (n/2)·vᵀCorr(x_T)v ≥ (c_ψ/2)|v|² ≥ (c_ψ/4)|u|².

So λ_min(G_T) ≥ c_ψ/4 ≥ c_ψ/8 = g₀ for all |T| ≤ q. Only the upper half ŝ_j² ≤ 2Var(x_j) of the variance event is used.

For |S| < q and j ∉ S, [P1] `lem:spec`(e) with one adjoined column (Cauchy interlacing) gives D_{S∪{j}}/D_S ≥ f(λ_min(G_{S∪{j}})) ≥ f(g₀) ≥ (n+1)g₀/(1+g₀), with f(λ) = ((n+1)λ + 1)/(λ + 1) increasing. ∎

## 4. Wording defects found (none affects truth)

1. C₂ is declared in the card but never used.
2. K denotes both the sub-Gaussian constant and the model-size cap min(p, ⌊n/2⌋).
3. For q = 0 the hypothesis is vacuous and K is unconstrained; the claim is trivial. For q ≥ 1, K ≥ 1 is forced.
4. In the consequence, "j ∉ S" must be read in (for j ∈ S the ratio is 1).
5. The constant is c_ψ/4, not just c_ψ/8. STATEMENT B2's chain through (n−1)c_ψ/(4n) is correct but loses the factor n/(n−1) and a factor 2.
6. Outside the card: STATEMENT B2's sentence "q_n ≥ m_n(M log n) + s" is literally false when q_n = p (e.g. p = 2, s = 1). It is harmless, since then (F_w) holds on all subsets of [p] and (ND) ranges only over j ≤ p − s₀.

ATTEMPT B/B-c RESULT=PROVED GAPS=0
