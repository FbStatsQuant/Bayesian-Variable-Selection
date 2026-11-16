# B-b-1
stop_reason: end_turn

# Card B, route B-b — truncated-quadratic (integrated small-ball) lower bound

**Result.** The card's statement is proved, with c₂ = 1/409600, and the mgf hypothesis is used only through a fourth-moment (L⁴–L²) bound. The consequence holds with the better floor c_ψ/4, hence also with g₀ = c_ψ/8 as stated. One external theorem is used (Bousquet's inequality); everything else is proved here. The card's constant C₂ is not needed.

**Why not single-level small-ball.** A one-level Paley–Zygmund bound gives n⁻¹Σf² ≥ τ²·#{i: |f(z_i)| ≥ τ}/n, whose constant is at most τ²P(|f| ≥ τ)/2 < ½ by Markov. To reach ½ I use all levels at once: min(f², τ²) = ∫₀^{τ²} 1{f² > s} ds. The only distributional input is E min(f², τ²) ≥ E f² − E f⁴/τ².

## 1. Theorem (fourth-moment form)

Let z₁, …, z_n be i.i.d. in ℝ^p with E z = 0 and finite fourth moments, Σ := Cov(z), q ≥ 1, q′ := min(q, p). Assume

**(M4; κ₄)** E(a + uᵀz)⁴ ≤ κ₄ (a² + uᵀΣu)² for all a ∈ ℝ and all u with at most q′ nonzero entries.

If q′ log(ep/q′) ≤ n/(16384 κ₄), then with probability ≥ 1 − exp(−n/(256 κ₄)), for all a ∈ ℝ and all u with at most q nonzero entries:

  n⁻¹ Σ_i (a + uᵀz_i)² ≥ ½ (a² + uᵀΣu).

No sub-Gaussianity, no eigenvalue floor on Σ, no continuity of the law, and Var(z_j) = 1 is not used.

*Sufficient for (M4).* If E(uᵀz)⁴ ≤ κ⁴(uᵀΣu)² for q′-sparse u, then by Minkowski and Cauchy–Schwarz ‖a + uᵀz‖₄ ≤ |a| + κ(uᵀΣu)^{1/2} ≤ (1 + κ²)^{1/2}(a² + uᵀΣu)^{1/2}, so (M4) holds with κ₄ = (1 + κ²)².

## 2. Proof

**Step 0 (reduction to one support).** A u ∈ ℝ^p with at most q nonzero entries is supported in some T₀ ⊆ [p] with |T₀| = q′. There are C(p, q′) ≤ (ep/q′)^{q′} such sets (k! ≥ (k/e)^k). Fix T₀ and put d := q′ + 1, w := (1, z_{T₀}) ∈ ℝ^d, w_i likewise, and Γ := E wwᵀ = diag(1, Σ_{T₀}) (uses E z = 0). For v = (a, u_{T₀}): f_v(z) := vᵀw = a + uᵀz and E f_v² = vᵀΓv = a² + uᵀΣu.

*Degenerate directions.* If x ∈ ker Γ then E(xᵀw)² = 0, so xᵀw = 0 a.s. Taking a basis of ker Γ gives the event N_{T₀} := {w_i ∈ range Γ for all i ≤ n}, of probability 1. Write v = v₁ + v₀ with v₁ ∈ range Γ, v₀ ∈ ker Γ. On N_{T₀}, vᵀw_i = v₁ᵀw_i for all i, and vᵀΓv = v₁ᵀΓv₁ =: s². If s = 0 the claim is trivial (right side 0). If s > 0, divide by s. So it suffices to prove, on N_{T₀} and outside an event of probability ≤ exp(−n/(128κ₄)):

  (★) n⁻¹ Σ_i f_v(z_i)² ≥ ½ for all v ∈ V := {v ∈ range Γ : vᵀΓv = 1}.

V is compact, and E f_v² = 1, E f_v⁴ ≤ κ₄ on V.

**Step 1 (truncation).** Let τ² := 8κ₄ and ψ(x) := min(x², τ²). Then 0 ≤ ψ ≤ τ², ψ(x) ≤ x², and ψ is 2τ-Lipschitz. For v ∈ V, since f²1{|f| > τ} ≤ f⁴/τ²:

  E ψ(f_v) ≥ E f_v² − E f_v²1{|f_v| > τ} ≥ 1 − κ₄/τ² = 7/8.  (1)

**Step 2 (the process).** Let h_v(z) := E ψ(f_v) − ψ(f_v(z)). Then E h_v = 0, |h_v| ≤ τ² =: b (indeed h_v ≤ 1), and Var h_v ≤ E ψ(f_v)² ≤ E f_v⁴ ≤ κ₄ =: σ². The map v ↦ h_v(z) is continuous (dominated convergence for the mean), so with V₀ a countable dense subset of V,

  Z := sup_{v∈V₀} Σ_i h_v(z_i) = sup_{v∈V} Σ_i h_v(z_i).

**Step 3 (E Z ≤ 4τ√(nd)).**

(a) *Symmetrisation, one-sided.* Let (z_i′) be an independent copy and (ε_i) independent Rademacher signs. By Jensen and coordinatewise exchangeability of (z_i, z_i′):
E Z ≤ E sup_v Σ_i [ψ(f_v(z_i′)) − ψ(f_v(z_i))] = E sup_v Σ_i ε_i[ψ(f_v(z_i′)) − ψ(f_v(z_i))] ≤ 2 E sup_v Σ_i ε_i ψ(f_v(z_i)).
All suprema are finite because ψ is bounded.

(b) *Contraction, proved here.* Let 𝒯 ⊂ ℝⁿ be bounded and φ 1-Lipschitz. Claim: E_ε sup_{t∈𝒯} Σ ε_iφ(t_i) ≤ E_ε sup_{t∈𝒯} Σ ε_i t_i. Replace one coordinate at a time. Fix k and the other signs, and let A(t) := Σ_{i<k} ε_i t_i + Σ_{i>k} ε_iφ(t_i). Then
E_{ε_k} sup_t [A(t) + ε_kφ(t_k)] = ½ sup_{t,s}[A(t) + A(s) + φ(t_k) − φ(s_k)] ≤ ½ sup_{t,s}[A(t) + A(s) + |t_k − s_k|] = ½ sup_{t,s}[A(t) + A(s) + t_k − s_k] = E_{ε_k} sup_t [A(t) + ε_k t_k],
where the third equality uses symmetry in (t, s). Induct on k.
Apply this conditionally on the data with φ = ψ/(2τ) and 𝒯 = {(f_v(z_i))_i : v ∈ V₀} (bounded since V is compact): E_ε sup_v Σ ε_iψ(f_v(z_i)) ≤ 2τ E_ε sup_v Σ ε_i vᵀw_i.

(c) *Linear part.* On N_{T₀}, ξ := Σ ε_i w_i ∈ range Γ. For v ∈ V, vᵀξ = (Γ^{1/2}v)ᵀ(Γ^{1/2})⁺ξ ≤ ‖(Γ^{1/2})⁺ξ‖. Since cross terms vanish, E‖(Γ^{1/2})⁺ξ‖² = n·E wᵀΓ⁺w = n·rank Γ ≤ nd.

Combining: E Z ≤ 2·2τ·√(nd) = 4τ√(nd).

**Step 4 (concentration; the one external result).**

*Bousquet's inequality* (Bousquet 2002, C. R. Acad. Sci. Paris Sér. I 334, 495–500, Thm 2.3; Boucheron–Lugosi–Massart 2013, *Concentration Inequalities*, Thm 12.5). Let X₁, …, X_n be i.i.d., ℱ countable, E f(X₁) = 0 and f ≤ 1 for all f ∈ ℱ, σ² ≥ sup_f Var f(X₁), Z = sup_f Σ_i f(X_i), v = nσ² + 2EZ. Then P(Z ≥ EZ + t) ≤ exp(−v·h(t/v)) for t ≥ 0, with h(x) = (1 + x)log(1 + x) − x.

Using h(x) ≥ x²/(2(1 + x/3)) and rescaling by b (functions bounded by b):

  P(Z ≥ EZ + t) ≤ exp(−t² / (2(nσ² + 2b·EZ) + 2bt/3)).  (2)

I apply (2) with b = τ² = 8κ₄, for which |h_v| ≤ b, so the hypothesis holds whether the source is read with one-sided or two-sided boundedness.

Assume dκ₄ ≤ n/8192. Then 4τ√(d/n) = 4√(8κ₄d/n) ≤ 1/8, so EZ ≤ n/8 and nσ² + 2b·EZ ≤ nκ₄ + 2nκ₄ = 3nκ₄. Take t = n/4 in (2). The exponent is

  (n²/16) / (6nκ₄ + (4/3)nκ₄) = 3n/(352κ₄) ≥ n/(128κ₄).

So with probability ≥ 1 − exp(−n/(128κ₄)), Z < n/8 + n/4. On that event and N_{T₀}, for every v ∈ V, by (1):

  n⁻¹Σ_i f_v(z_i)² ≥ n⁻¹Σ_i ψ(f_v(z_i)) ≥ E ψ(f_v) − Z/n ≥ 7/8 − 3/8 = ½.

This is (★).

**Step 5 (union over supports).** Since log(ep/q′) ≥ 1, the hypothesis q′ log(ep/q′) ≤ n/(16384κ₄) gives dκ₄ ≤ 2q′κ₄ ≤ n/8192, as Step 4 requires. The total failure probability is at most

  (ep/q′)^{q′}·exp(−n/(128κ₄)) ≤ exp(n/(16384κ₄) − n/(128κ₄)) ≤ exp(−n/(256κ₄)),

and the null sets N_{T₀}ᶜ are finitely many. ∎

## 3. The card's statement (sub-Gaussian K)

Assume E exp(λuᵀz) ≤ exp(K²λ²σ_u²/2) for q-sparse u, with σ_u² := Var(uᵀz), and Var(z_j) = 1.

- **K ≥ 1.** With u = e₁: 1 + λ²/2 ≤ E cosh(λz₁) ≤ exp(K²λ²/2) for all λ. Subtract 1, divide by λ², let λ → 0.
- **Fourth moment.** By Chernoff, P(|uᵀz| > t) ≤ 2exp(−t²/(2K²σ_u²)). Hence E(uᵀz)⁴ = ∫₀^∞ 4t³P(|uᵀz| > t)dt ≤ 8·2(K²σ_u²)² = 16K⁴σ_u⁴ (trivial if σ_u = 0).
- **(M4).** By §1 with κ = 2K: κ₄ = (1 + 4K²)² ≤ 25K⁴.

The theorem then gives the card's statement with **c₂ = 1/(16384·25) = 1/409600**. If q′log(ep/q′) ≤ c₂n/K⁴ then q′log(ep/q′) ≤ n/(16384κ₄), and the failure probability is ≤ exp(−n/(6400K⁴)) ≤ exp(−c₂n/K⁴). The factor ½, the intercept a, all q-sparse u and degenerate directions are covered. ∎

## 4. Consequence (B2)

**Setting.** Raw rows x_i i.i.d. with positive variances, z_{ij} = (x_{ij} − E x_j)/sd(x_j), so Cov(z) = Corr(x). X_{ij} = (x_{ij} − x̄_j)/ŝ_j with ŝ_j² = (n − 1)⁻¹Σ_i(x_{ij} − x̄_j)², so ‖X_j‖² = n − 1. Work on the event 𝓔 of §3 intersected with {ŝ_j² ≤ 2Var(x_j) ∀j} (only this half of B1 is used; ŝ_j > 0 is needed for X to be defined). Assume λ_min(Corr(x_T)) ≥ c_ψ/n for all |T| ≤ q.

**Claim.** λ_min(X_TᵀX_T) ≥ c_ψ/4 ≥ c_ψ/8 for all |T| ≤ q.

*Proof.* Fix T and u ∈ ℝ^T. Put ũ_j := u_j·sd(x_j)/ŝ_j, zero off T (so ũ is q-sparse), and a := −ũᵀz̄. Since (x_{ij} − x̄_j)/ŝ_j = (sd(x_j)/ŝ_j)(z_{ij} − z̄_j), we have (X_Tu)_i = a + ũᵀz_i. The intercept a is data-dependent, which is allowed because 𝓔 is uniform in a. Then

  ‖X_Tu‖² = Σ_i(a + ũᵀz_i)² ≥ (n/2)(a² + Var(ũᵀz)) ≥ (n/2)·ũᵀCorr(x)_Tũ ≥ (c_ψ/2)‖ũ‖² ≥ (c_ψ/4)‖u‖²,

using Var(x_j)/ŝ_j² ≥ ½ in the last step. ∎

**Determinant ratio.** Let |S| < q, j ∉ S, S′ = S ∪ {j} (so |S′| ≤ min(q, p)), g₀ = c_ψ/8, f(λ) = ((n+1)λ + 1)/(λ + 1) (increasing). By [P1] `lem:spec`(e): D_S = Π_i f(λ_i(G_S)), and G_S is a principal submatrix of G_{S′}, so Cauchy interlacing gives λ_i(G_S) ≤ λ_{i+1}(G_{S′}). Hence

  D_{S′}/D_S ≥ f(λ_min(G_{S′})) ≥ f(g₀) ≥ (n+1)g₀/(1 + g₀).

Iterating over the columns of J gives (DG; g₀/(1+g₀)), hence (ND), on all S₀ ∪ J with |S₀ ∪ J| ≤ q. ∎

## 5. Remarks on scope

1. **What B-b buys.** B2-core needs only L⁴–L² equivalence on q-sparse directions, with exponent n/κ₄. The same proof with τ² = κ₄/ε-type choices gives 1 − ε in place of ½ at cost n ≳ κ₄d/ε² (not written out).
2. **B1 under fourth moments.** The lower half of B1 is free on 𝓔: taking u = e_j, a = −z̄_j gives ŝ_j²/Var(x_j) ≥ n/(2(n−1)) ≥ ½. The upper half ŝ_j² ≤ 2Var(x_j), which §4 uses, is an upper-tail statement over p columns. For p ≫ n it genuinely needs coordinatewise tails (as in (A3) for single coordinates). Route B-b does not remove that.
3. **Self-contained fallback.** Replacing Bousquet by McDiarmid's bounded-differences inequality (range τ²/n per coordinate) makes the proof fully elementary but gives exponent n/κ₄², i.e. n/K⁸ instead of n/K⁴. The card's K⁴ scaling needs the variance-sensitive inequality.
4. **Adversarial points (B-c).** Var(uᵀz) = 0 is handled in Step 0; atoms are harmless since no density or continuity is used; and q′ near its limit is exactly the stated condition, with no hidden n₀.

ATTEMPT B/B-b RESULT=PROVED GAPS=0
