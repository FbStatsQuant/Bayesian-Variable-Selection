# S-a-1
stop_reason: end_turn

# Card S, route S-a — Lemma S (exponential size tail, reference-adaptive)

Route S-a goes through with no gap, and it yields slightly more than the card asks: **n₀ = 3, every t > 0 (no upper limit), constants independent of κ₀.** The card's statement follows by restricting to 1 ≤ t ≤ n^{1−κ₀}.

I use my own two-sided bracket for s_y² (not [P1]'s 𝓑_n), so that its failure probability is exponential at every n ≥ 3. The constant c♯ below is therefore not [T03R]'s; it still depends on (σ*², M) only.

## Statement proved

Fixed design, n ≥ 3, p ≥ 2, y_c = μ_c + e with e ~ N_N(0, σ*²I), μ_c ∈ ℝ^N arbitrary with ‖μ_c‖² = ‖μ‖² ≤ nM (μ ∈ 1^⊥ need not lie in col X). Let T ∈ Ω and ϑ ∈ ℝ^T be non-random (functions of X only) with B_T(ϑ) ≤ B. Put R^T_m := Σ_{m<k≤K} q_k / w(|T|).

Define
- b₋ := 0.01·σ*²/4, b₊ := 0.01·(4σ*² + 3M), κ := (b₊/b₋)^{0.51};
- c_IG := min_{v∈[σ*², 2σ*²]} IG(v; 0.51, b₊) > 0, c♯ := κ²/(c_IG σ*²);
- C₁ := 2 + B/(2σ*²) + √(2B)/σ*, **C := max{5, C₁ + log₊ c♯}**, c := 1/16.

**Claim.** For every n ≥ 3, every real t > 0 and every integer m with

  log R^T_m + ½ log D_T + ½ log n + C[1 + √t + t/√n] ≤ −2t  (log 0 := −∞),

we have P_e[π(|S| > m) > e^{−t}] ≤ 5e^{−t} + 3e^{−n/16} ≤ Ce^{−t} + Ce^{−cn}.

If R^T_m is read with the sum running to p instead of K, it is larger, so that hypothesis implies the one above; the claim covers both readings.

## External results used

- **(LM)** Laurent & Massart (2000), Ann. Statist. 28, Lemma 1: for d ≥ 1 and x > 0, P(χ²_d − d ≥ 2√(dx) + 2x) ≤ e^{−x} and P(χ²_d − d ≤ −2√(dx)) ≤ e^{−x}.
- **(GT)** For Z ~ N(0,1) and x ≥ 0: P(Z ≥ x) ≤ e^{−x²/2}. (Chernoff: E e^{λZ} = e^{λ²/2}, take λ = x.)
- **[P1] `lem:slab`**: ∫ N_N(x; X_{c,S}θ, vI) N_k(θ; 0, nv(G_S+I)⁻¹) dθ = (2πv)^{−N/2} D_S^{−1/2} e^{−Q^c_S(x)/(2v)}, and Q^c_S is the minimum in the Common definitions. I re-checked the algebra: completing the square with H_S/n = G_S + (G_S+I)/n; the determinant factors give D_S^{−1/2}. It holds for singular G_S and S = ∅.
- **[P1] `lem:IGint`**: ∫₀^∞ v^{−a−1}e^{−β/v}dv = Γ(a)β^{−a}.

## Proof

**Step 0 (fixed-rate proper mixtures).** For a data-free b > 0 and S ∈ Ω (k = |S|), let

  m_b(S)(x) := ∫₀^∞ ∫ N_N(x; X_{c,S}θ, vI) N_k(θ; 0, nv(G_S+I)⁻¹) IG(v; 0.51, b) dθ dv, x ∈ ℝ^N.

(i) The integrand is the joint density of (x, θ, v) under a proper prior (G_S + I ≻ 0 always). By Tonelli, m_b(S) is a probability density on ℝ^N, for every S ∈ Ω including sizes near n/2 and rank-deficient X_S.

(ii) By `lem:slab`,

  m_b(S)(x) = D_S^{−1/2} ∫₀^∞ (2πv)^{−N/2} e^{−Q^c_S(x)/(2v)} IG(v; 0.51, b) dv.  (0.1)

By `lem:IGint` with a = N/2 + 0.51 = ν,

  m_b(S)(x) = (2π)^{−N/2} [Γ(ν)/Γ(0.51)] · b^{0.51} D_S^{−1/2} (b + Q^c_S(x)/2)^{−ν}.  (0.2)

(iii) By (0.2), the factor multiplying D_S^{−1/2}(2b + Q^c_S)^{−ν} does not depend on S. With ϖ(S) := w(|S|)/W_K, the posterior of the Common definitions is, for every data point with s_y > 0 (a.s.),

  π(S) = ϖ(S) m_b(S)(y_c) / Σ_{S′∈Ω} ϖ(S′) m_b(S′)(y_c) at b = 0.01·s_y².  (0.3)

(iv) Envelope. For b₋ ≤ b ≤ b₊ and any Q ≥ 0, b ↦ b^{0.51} is increasing and b ↦ (b + Q/2)^{−ν} is decreasing. So b^{0.51}(b+Q/2)^{−ν} ≤ b₊^{0.51}(b₋+Q/2)^{−ν} = κ·b₋^{0.51}(b₋+Q/2)^{−ν}, and ≥ b₋^{0.51}(b₊+Q/2)^{−ν} = κ⁻¹·b₊^{0.51}(b₊+Q/2)^{−ν}. By (0.2), pointwise in x and for all S:

  κ⁻¹ m_{b₊}(S)(x) ≤ m_b(S)(x) ≤ κ m_{b₋}(S)(x).  (0.4)

**Step 1 (bracket event, exponential).** Let 𝓑 := {σ*²/4 ≤ s_y² ≤ 4σ*² + 3M} = {b₋ ≤ 0.01 s_y² ≤ b₊}.

*Lower side.* Let Π be the orthogonal projection of ℝ^N onto μ_c^⊥ (rank ≥ N − 1 ≥ 1). Then ‖y_c‖² ≥ ‖Πy_c‖² = ‖Πe‖², and ‖Πe‖²/σ*² stochastically dominates χ²_{N−1}. By (LM) with d = N − 1, x = d/16: P(χ²_d ≤ d/2) ≤ e^{−d/16}. Off that event s_y² ≥ σ*²(N−1)/(2N) ≥ σ*²/4, since N ≥ 2.

*Upper side.* ‖y_c‖² ≤ 2‖μ_c‖² + 2‖e‖² ≤ 2nM + 2σ*²E′, with E′ := ‖e‖²/σ*² ~ χ²_N. By (LM) with x = N/8: 2√(N·N/8) + N/4 < N, so P(E′ > 2N) ≤ e^{−N/8}. Off that event s_y² ≤ 2nM/N + 4σ*² ≤ 3M + 4σ*², since n/N ≤ 3/2.

Hence P(𝓑ᶜ) ≤ e^{−(n−2)/16} + e^{−(n−1)/8} ≤ (e^{1/8} + 1)e^{−n/16} ≤ 3e^{−n/16}, for every n ≥ 3.

**Step 2 (numerator; Markov at level e^t).** Fix m with R^T_m > 0. (If R^T_m = 0 then {S ∈ Ω : |S| > m} = ∅, π(|S| > m) = 0, nothing to prove.) Let E_m := {S ∈ Ω : |S| > m} and let f₀ := N_N(·; μ_c, σ*²I) > 0 be the density of y_c. Define

  Θ^{(1)} := [Σ_{S∈E_m} ϖ(S) m_{b₋}(S)(y_c)/f₀(y_c)] / ϖ(E_m).

Since b₋ is data-free, Step 0(i) gives E[m_{b₋}(S)(y_c)/f₀(y_c)] = ∫ m_{b₋}(S)(x)dx = 1 for each S. So EΘ^{(1)} = 1 and P(Θ^{(1)} > e^t) ≤ e^{−t}. No property of X or μ is used.

**Step 3 (reference bound on Q^c_T).** Put r := μ − X_Tϑ ∈ 1^⊥ and r_c := Uᵀr, so ‖r_c‖ = ‖r‖ and y_c − X_{c,T}ϑ = e + r_c. Taking φ = ϑ in the variational form of Q^c_T (for T = ∅: Q^c_∅ = ‖y_c‖², r = μ):

  Q^c_T ≤ ‖e + r_c‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n = σ*²E′ + 2eᵀr_c + B_T(ϑ) ≤ σ*²E′ + ρ″, ρ″ := B + 2|eᵀr_c| ≥ 0.

Here eᵀr_c ~ N(0, σ*²‖r_c‖²) and ‖r_c‖² ≤ B.

**Step 4 (denominator).** By (0.1) with S = T, b = b₊, and f₀(y_c) = (2πσ*²)^{−N/2}e^{−E′/2}:

  m_{b₊}(T)(y_c)/f₀(y_c) = D_T^{−1/2} ∫₀^∞ exp{−(N/2) log(v/σ*²) + E′/2 − Q^c_T/(2v)} IG(v; 0.51, b₊) dv.

For v = σ*²u with 1 ≤ u ≤ 1 + n^{−1/2}, use log u ≤ u − 1, Step 3, u ≥ 1 and 1/u ≥ 2 − u. The exponent is

  ≥ −(N/2)(u−1) + (E′/2)(1 − 1/u) − ρ″/(2σ*²)
  = ((u−1)/2)(E′/u − N) − ρ″/(2σ*²)
  ≥ ((u−1)/2)(E′ − N) − (u−1)²E′/2 − ρ″/(2σ*²)
  ≥ −Λ″,

where Λ″ := |E′ − N|/(2√n) + E′/(2n) + ρ″/(2σ*²). The v-interval [σ*², σ*²(1+n^{−1/2})] ⊆ [σ*², 2σ*²] has length σ*²n^{−1/2} and the IG density is ≥ c_IG on it. Hence

  m_{b₊}(T)(y_c)/f₀(y_c) ≥ D_T^{−1/2} c_IG σ*² n^{−1/2} e^{−Λ″}.  (4.1)

D_T is kept exact.

**Step 5 (exponential tail of Λ″).** Let 𝓔_t be the intersection of
- (a) E′ − N ≤ 2√(Nt) + 2t,
- (b) E′ − N ≥ −2√(Nt),
- (c) |eᵀr_c| ≤ σ*‖r_c‖√(2t).

By (LM) with d = N, x = t, and (GT) on both sides, P(𝓔_tᶜ) ≤ e^{−t} + e^{−t} + 2e^{−t} = 4e^{−t}. On 𝓔_t:
- |E′ − N|/(2√n) ≤ √t + t/√n;
- E′/(2n) ≤ (N + 2√(Nt) + 2t)/(2n) ≤ (2N + 3t)/(2n) ≤ 1 + t/√n, using 2√(Nt) ≤ N + t and 3/(2n) ≤ 1/√n for n ≥ 3;
- ρ″/(2σ*²) ≤ B/(2σ*²) + √(2Bt)/σ*.

So Λ″ ≤ [1 + B/(2σ*²)] + [1 + √(2B)/σ*]√t + 2t/√n ≤ C₁(1 + √t + t/√n).

**Step 6 (assembly).** On 𝓑, b := 0.01 s_y² ∈ [b₋, b₊]. By (0.3), (0.4), and keeping only the term S′ = T in the denominator (allowed since T ∈ Ω):

  π(E_m) ≤ κ Σ_{S∈E_m} ϖ(S)m_{b₋}(S)(y_c) / [κ⁻¹ ϖ(T) m_{b₊}(T)(y_c)] = κ² ϖ(E_m)Θ^{(1)} / [ϖ(T)·m_{b₊}(T)(y_c)/f₀(y_c)].

W_K cancels in ϖ(E_m)/ϖ(T) = Σ_{m<k≤K} C(p,k)w(k)/w(|T|) = R^T_m. With (4.1), on 𝓑 ∩ {Θ^{(1)} ≤ e^t} ∩ 𝓔_t:

  log π(E_m) ≤ log R^T_m + ½ log D_T + ½ log n + log c♯ + t + C₁(1 + √t + t/√n)
       ≤ log R^T_m + ½ log D_T + ½ log n + C(1 + √t + t/√n) + t ≤ −2t + t = −t.

The middle step uses log c♯ ≤ log₊c♯·(1 + √t + t/√n); the last is the hypothesis on m. Therefore

  P[π(|S| > m) > e^{−t}] ≤ P(𝓑ᶜ) + P(Θ^{(1)} > e^t) + P(𝓔_tᶜ) ≤ 3e^{−n/16} + e^{−t} + 4e^{−t}. ∎

## Remarks

1. **Uniformity.** The bound holds for every n ≥ 3, t > 0 and integer m, and depends on (X, μ, T, ϑ) only through (σ*², M, B). The range t ≤ n^{1−κ₀} and a large n₀ are not needed in the lemma. They matter only for checking the hypothesis at a concrete cutoff (Remark 3).

2. **Reference must not depend on e.** (T, ϑ) may be any function of X. If the design is random with e ⫫ X, apply the claim conditionally on X. Step 3's N(0, σ*²‖r_c‖²) law for eᵀr_c fails for references chosen after seeing y. Models of size near n/2 are harmless: Step 2 uses only properness of each mixture.

3. **Cutoff m_n(t) (by-product; not part of the card).** Take μ = Xθ*, s₀ ≤ K, (E; M), (C; M′), T = S₀, ϑ = θ*, so B = M + M′. Then m = m_n(t) satisfies the hypothesis whenever n ≥ 9C² and t ≥ 9C²; in particular for all t ≥ log n once n ≥ e^{9C²}, with no upper limit on t.
   - If m_n(t) = K, the tail is 0.
   - Otherwise m ≥ 0 and Σ_{k>m}q_k ≤ 2^{−m}, because q₁ ≤ ½ and q_{k+1}/q_k = (p−k)/(2p−k−1) ≤ ½ for k ≥ 1. Also w(s₀) ≥ ½(2p)^{−s₀} and D_{S₀} ≤ (n+1)^{s₀}.
   - These give log R_m + ½ log D_{S₀} + ½ log n ≤ log 2 − ½ log(n+1) − 3t ≤ −3t.
   - Finally C(1 + √t + t/√n) ≤ t when t ≥ 9C² and n ≥ 9C² (each of the three terms is ≤ t/3, using C ≥ 5).

4. **Difference from Claim B's proof.** The structure (Steps 0, 2, 3, 4, 6) is that of `B_tail_approx.md` Steps 1–4. The changes are:
   - Chebyshev on [P1]'s 𝓑_n is replaced by the (LM) bracket of Step 1, with endpoints σ*²/4 and 4σ*² + 3M, hence different κ and c_IG;
   - Markov on Λ″ is replaced by Step 5;
   - Markov on Θ^{(1)} is taken at level e^t;
   - the envelope is derived from the closed form (0.2).

ATTEMPT S/S-a RESULT=PROVED GAPS=0
