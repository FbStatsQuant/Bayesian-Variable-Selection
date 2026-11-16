# B-a-1
stop_reason: end_turn

# Card B, route B-a (ε-net + Bernstein per support + union): proof of B2-core and of the B2 consequence

**Result.** The statement holds with c₂ = 1/98304; no constant C₂ is needed. The proof gives slightly more than asked: a two-sided bound, λ_min(X_TᵀX_T) ≥ c_ψ/4 instead of c_ψ/8, and the B1 event for free on the constructed event. No gaps.

**Notation.** K denotes the sub-Gaussian constant of the card (not the model-size cap). Σ := Cov(z), with unit diagonal. For u ∈ ℝ^p, σ_u² := Var(uᵀz) = uᵀΣu. q′ := min(q, p), h := q′ log(ep/q′), with h := 0 if q = 0. Constants: c_B := 1/12288, c₂ := c_B/8 = 1/98304.

**Trivial case q = 0.** Then u = 0 and n⁻¹Σ_i a² = a² ≥ ½a² surely. Assume q ≥ 1 from here on.

**Fact 0 (K ≥ 1; h ≥ q′ ≥ 1).** Taking u = e₁ gives σ_u² = 1 and E e^{λz₁} ≤ e^{K²λ²/2} for all λ. All moments are finite, so E e^{λz₁} = 1 + λ²/2 + o(λ²) as λ → 0, which forces K² ≥ 1. Since p/q′ ≥ 1, log(ep/q′) ≥ 1, so h ≥ q′ ≥ 1.

## 1. Scalar Bernstein bound (proved here)

**Lemma 1.** Let W, W₁, …, W_n be i.i.d. real with E W = 0, E W² = σ² ≤ 1 and E e^{λW} ≤ exp(K²λ²σ²/2) for all λ, K ≥ 1. Let a ∈ ℝ with a² + σ² = 1 and Y_i := (a + W_i)², so E Y_i = 1. Then

  P( |n⁻¹Σ_i (Y_i − 1)| ≥ ¼ ) ≤ 4 exp(−c_B n/K⁴).

*Proof.* If σ = 0 then W = 0 a.s. and Y_i = 1 a.s. Let σ > 0, τ := K²σ² ∈ [σ², K²], and write Y_i − 1 = Z_i + 2aW_i with Z_i := W_i² − σ².

*(a) Square-MGF.* Let g ~ N(0,1) be independent of W and 0 ≤ θ < 1/(2τ). Since E_g e^{sg} = e^{s²/2}, Tonelli gives
E e^{θW²} = E_W E_g e^{√(2θ) g W} = E_g E_W e^{√(2θ) g W} ≤ E_g e^{τθg²} = (1 − 2τθ)^{−1/2}.
At θ = 1/(4τ): E exp(W²/(4τ)) ≤ √2. Since x^k/k! ≤ e^x, E W^{2k} ≤ √2·k!(4τ)^k for k ≥ 1.

*(b) Moments of Z.* |Z| ≤ max(W², σ²), so E|Z|^k ≤ E W^{2k} + σ^{2k}. For k ≥ 2, σ^{2k} ≤ τ^k = 4^{−k}(4τ)^k ≤ k!(4τ)^k/32. Hence E|Z|^k ≤ (√2 + 1/32) k!(4τ)^k ≤ 1.5·k!(4τ)^k.

*(c) MGF of Z.* Let |θ| ≤ 1/(8τ) and x := 4τ|θ| ≤ ½. Using E Z = 0 and termwise integration (justified by E e^{|θ||Z|} < ∞):
E e^{θZ} ≤ 1 + Σ_{k≥2} |θ|^k E|Z|^k/k! ≤ 1 + 1.5x²/(1 − x) ≤ 1 + 3x² ≤ exp(48τ²θ²).

*(d) Chernoff.* For s > 0 and 0 < θ ≤ 1/(8τ): P(n⁻¹ΣZ_i ≥ s) ≤ exp(−nθs + 48nτ²θ²).
- If s ≤ 12τ, take θ = s/(96τ²) ≤ 1/(8τ); the exponent is −ns²/(192τ²).
- If s > 12τ, take θ = 1/(8τ); the exponent is −ns/(8τ) + 3n/4 ≤ −ns/(16τ).

The same holds for −Z. With s = 1/8 and τ ≤ K², K ≥ 1: s²/(192τ²) ≥ 1/(12288K⁴) and s/(16τ) ≥ 1/(128K²) ≥ 1/(128K⁴). So
P(|n⁻¹ΣZ_i| ≥ 1/8) ≤ 2exp(−n/(12288K⁴)).

*(e) Linear term.* If a = 0 it vanishes. Otherwise E e^{λΣW_i} ≤ exp(nK²σ²λ²/2), so P(|n⁻¹ΣW_i| ≥ r) ≤ 2exp(−nr²/(2K²σ²)). Take r = 1/(16|a|) and use a²σ² ≤ ¼ (as a² + σ² = 1):
P(|2a·n⁻¹ΣW_i| ≥ 1/8) ≤ 2exp(−n/(512a²σ²K²)) ≤ 2exp(−n/(128K²)) ≤ 2exp(−n/(12288K⁴)).

Adding (d) and (e) gives the claim. ∎

## 2. Net lemma (standard; proved)

**Lemma 2.** Let d ≥ 1. (i) The unit sphere of ℝ^d has a ¼-net 𝒩 with |𝒩| ≤ 9^d. (ii) For symmetric A ∈ ℝ^{d×d}, ‖A‖_op ≤ 2·max_{x∈𝒩}|xᵀAx|.

*Proof.* (i) Take a maximal ¼-separated subset of the sphere. The balls of radius 1/8 around its points are disjoint and lie in the ball of radius 9/8, so |𝒩| ≤ (9/8)^d/(1/8)^d = 9^d. Maximality makes it a ¼-net.
(ii) Take a unit x with |xᵀAx| = ‖A‖ and x₀ ∈ 𝒩 with ‖x − x₀‖ ≤ ¼. Then |xᵀAx − x₀ᵀAx₀| = |xᵀA(x − x₀) + (x − x₀)ᵀAx₀| ≤ ½‖A‖, so ‖A‖ ≤ |x₀ᵀAx₀| + ½‖A‖. ∎

(These are Corollary 4.2.13 and Exercise 4.4.3 of Vershynin, *High-Dimensional Probability*, 2018; not needed since proved.)

## 3. Theorem (B2-core, two-sided form)

**Theorem.** Let q ≥ 1 and h = q′log(ep/q′) ≤ c₂n/K⁴. There is an event 𝓔 with P(𝓔) ≥ 1 − exp(−c₂n/K⁴) on which, for all a ∈ ℝ and all u ∈ ℝ^p with at most q nonzero entries,

  ½(a² + σ_u²) ≤ n⁻¹Σ_i (a + uᵀz_i)² ≤ (3/2)(a² + σ_u²).

The lower bound is the card's statement. Degenerate directions σ_u = 0 are included.

*Proof.*

*Step 1 (supports).* Every u with at most q nonzero entries has support inside some T ⊆ [p] with |T| = q′. There are C(p, q′) ≤ (ep/q′)^{q′} such T. Fix one.

*Step 2 (whitening with the intercept; handles degeneracy).* Let w := (1, z_T) ∈ ℝ^{q′+1} and w_i := (1, z_{i,T}). Since E z = 0, Γ_T := E wwᵀ = diag(1, Σ_T). Let d := rank Γ_T = 1 + rank Σ_T ≤ q′ + 1 and Γ_T = VΛVᵀ with V ∈ ℝ^{(q′+1)×d}, VᵀV = I_d, Λ ≻ 0 diagonal. Put B := VΛ^{1/2}, ξ := Λ^{−1/2}Vᵀw, ξ_i := Λ^{−1/2}Vᵀw_i. Then:
- E ξξᵀ = Λ^{−1/2}VᵀΓ_TVΛ^{−1/2} = I_d.
- For v ∈ ker Γ_T, E(vᵀw)² = 0, so vᵀw = 0 a.s. Applying this to a basis of ker Γ_T, the event 𝓡_T := {w_i ∈ range Γ_T for all i ≤ n} has probability 1. On 𝓡_T, Bξ_i = VVᵀw_i = w_i.
- For a unit x ∈ ℝ^d put (a_x, u_x) := VΛ^{−1/2}x ∈ ℝ × ℝ^T, with u_x extended by 0 to ℝ^p (support ⊆ T, so at most q nonzero entries). Then xᵀξ = a_x + u_xᵀz and a_x² + σ_{u_x}² = (a_x, u_x)Γ_T(a_x, u_x)ᵀ = ‖x‖² = 1.

*Step 3 (net points).* Let 𝒩_T be the net of Lemma 2 in ℝ^d, |𝒩_T| ≤ 9^{q′+1}. For x ∈ 𝒩_T, W := u_xᵀz satisfies the hypotheses of Lemma 1 (E W = 0, variance σ_{u_x}² ≤ 1, the card's MGF bound, K ≥ 1 by Fact 0), with a = a_x and Y_i = (xᵀξ_i)². Hence
P( |n⁻¹Σ_i(xᵀξ_i)² − 1| ≥ ¼ ) ≤ 4exp(−c_Bn/K⁴).

*Step 4 (union).* Let 𝓝 be the event that |xᵀ(Γ̂^ξ_T − I_d)x| < ¼ for every T and every x ∈ 𝒩_T, where Γ̂^ξ_T := n⁻¹Σ_iξ_iξ_iᵀ. By Fact 0, (q′+1)log 9 ≤ 2 log 9·h and log 4 ≤ log 4·h, and 1 + 2 log 9 + log 4 < 7. So
P(𝓝ᶜ) ≤ (ep/q′)^{q′}·9^{q′+1}·4·exp(−c_Bn/K⁴) ≤ exp(7h − c_Bn/K⁴) ≤ exp((7c₂ − 8c₂)n/K⁴) = exp(−c₂n/K⁴).
Put 𝓔 := 𝓝 ∩ ⋂_T 𝓡_T; then P(𝓔) ≥ 1 − exp(−c₂n/K⁴).

*Step 5 (net to sphere, back to (a, u)).* On 𝓝, Lemma 2(ii) gives ‖Γ̂^ξ_T − I_d‖ ≤ ½ for every T. So ½‖x‖² ≤ xᵀΓ̂^ξ_Tx ≤ (3/2)‖x‖² for all x ∈ ℝ^d. Let a ∈ ℝ and u be supported in T, v := (a, u_T). On 𝓡_T, vᵀw_i = (Bᵀv)ᵀξ_i, hence
n⁻¹Σ_i(a + uᵀz_i)² = (Bᵀv)ᵀΓ̂^ξ_T(Bᵀv) ∈ [½, 3/2]·‖Bᵀv‖², and ‖Bᵀv‖² = vᵀΓ_Tv = a² + σ_u². ∎

Remarks on quantifiers. c₂ is absolute and there is no n₀. For q ≥ 1 the hypothesis forces n ≥ K⁴/c₂ ≥ 98304. The sub-Gaussian hypothesis is used only at the finitely many net directions (a_x, u_x), all supported in sets of size q′ ≤ q. The intercept costs one net dimension and the linear term of Lemma 1(e).

## 4. Consequence (B1 + B2)

Setting: raw rows x₁, …, x_n i.i.d. in ℝ^p with 0 < Var(x_j) < ∞; z_{ij} := (x_{ij} − E x_j)/sd(x_j), so Cov(z) = Corr(x). ŝ_j² := (n − 1)⁻¹Σ_i(x_{ij} − x̄_j)²; standardised columns X_{ij} := (x_{ij} − x̄_j)/ŝ_j, so ‖X_j‖² = n − 1. Let 𝓗 := {½ ≤ ŝ_j²/Var(x_j) ≤ 2 for all j}.

**Proposition B2.** On (the card's B2-core event) ∩ 𝓗, if λ_min(Corr(x_T)) ≥ c_ψ/n for all |T| ≤ q, then:

(i) λ_min(X_TᵀX_T) ≥ c_ψ/4 ≥ c_ψ/8 =: g₀ for every T with |T| ≤ q. This is (F_w; g₀) on all sets of size ≤ q.

(ii) For every S with |S| < q and j ∉ S: D_{S∪{j}}/D_S ≥ ((n+1)g₀ + 1)/(g₀ + 1) ≥ (n+1)g₀/(1 + g₀).

(iii) Hence (DG; c_D) and (ND; c_D, m) hold with c_D = g₀/(1 + g₀) for every m ≤ q − s₀.

*Proof.* (i) On 𝓗 all ŝ_j > 0, so no column is dropped. Since x_{ij} − x̄_j = sd(x_j)(z_{ij} − z̄_j), X_{ij} = ρ_j(z_{ij} − z̄_j) with ρ_j := sd(x_j)/ŝ_j and ρ_j² ≥ ½ on 𝓗. Let u ∈ ℝ^T, |T| ≤ q, and ũ_j := ρ_ju_j (supported in T). Then
‖X_Tu‖² = Σ_i(ũᵀz_i − ũᵀz̄)² = min_{a∈ℝ} Σ_i(a + ũᵀz_i)²
 ≥ (n/2)·min_a(a² + Var(ũᵀz)) = (n/2)·ũᵀCorr(x_T)ũ ≥ (c_ψ/2)‖ũ‖² ≥ (c_ψ/4)‖u‖².
The first inequality is B2-core applied for every a.

(ii) Let S′ := S ∪ {j}, |S′| ≤ q, k := |S|. By [P1] `lem:spec`(e), D_S = Π_i f(λ_i(G_S)) with f(λ) = ((n+1)λ + 1)/(λ + 1) increasing and f ≥ 1 (D_∅ = 1). G_S is a principal submatrix of G_{S′}, so Cauchy interlacing gives λ_i(G_S) ≤ λ_{i+1}(G_{S′}) for 1 ≤ i ≤ k (increasing order). Thus D_S ≤ Π_{i=2}^{k+1} f(λ_i(G_{S′})) and D_{S′}/D_S ≥ f(λ_min(G_{S′})) ≥ f(g₀) ≥ (n+1)g₀/(1 + g₀) by (i).

(iii) Iterate (ii) along J ⊆ [p]∖S₀ with s₀ + |J| ≤ q: D_{S₀∪J}/D_{S₀} ≥ [c_D(n+1)]^{|J|}. Averaging (D_{S₀}/D_{S₀∪J})^{1/2} ≤ [c_D(n+1)]^{−|J|/2} over |J| = j ≤ min(m, p − s₀) gives (ND). ∎

**Addendum (B1 is automatic on 𝓔).** On the event 𝓔 of §3 with q ≥ 1, 𝓗 holds. For u = e_j: Σ_i(z_{ij} − z̄_j)² = min_a Σ_i(a + z_{ij})², which is ≥ n/2 by the lower bound and ≤ Σ_iz_{ij}² ≤ 3n/2 by the upper bound at a = 0. So ŝ_j²/Var(x_j) = (n − 1)⁻¹Σ_i(z_{ij} − z̄_j)² ∈ [n/(2(n−1)), 3n/(2(n−1))] ⊆ [½, 2], since n ≥ 4 is forced. Consequently, under (A3) with q ≥ 1 and h ≤ c₂n/K⁴, Proposition B2 holds on the single event 𝓔 of probability ≥ 1 − exp(−c₂n/K⁴). The separate B1 event and its 4p·exp(−c₁n/K⁴) term are not needed for B2. They are still needed for the "without (A4)" variant, where (A3) is only assumed for single coordinates; there Lemma 1 with q = 1 gives the same conclusion per column by a union over p.

## 5. Differences from the card and from STATEMENT §3

- **C₂ is not needed.** c₂ = 1/98304 works, as does any smaller value.
- **K ≥ 1 is forced** by the hypothesis when q ≥ 1 (Fact 0); it is used to replace K² by K⁴ in the exponents.
- **The bound is two-sided** (constants ½ and 3/2); the card asks only for the lower half.
- **The floor is c_ψ/4, not c_ψ/8.** The chain in STATEMENT §3 B2, "(n − 1)·λ_min(Σ̂^z_T)/max_j(·) ≥ (n − 1)c_ψ/(4n)", loses a harmless factor (n − 1)/n against the direct computation above.
- **(A4) at level c_ψ/n is enough** because the transfer is multiplicative (Σ̂ ⪰ ½Σ on sparse directions), unlike the additive Weyl transfer of [POST] step (3), which needs ψ_n√n/(log n)^{3/2} → ∞.

ATTEMPT B/B-a RESULT=PROVED GAPS=0
