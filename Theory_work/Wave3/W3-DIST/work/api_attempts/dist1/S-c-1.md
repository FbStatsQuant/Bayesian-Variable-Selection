# S-c-1
stop_reason: end_turn

# Card S, route S-c (adversarial): no counterexample exists

**Verdict.** I could not break Lemma S as written, and the reason is structural: every attack runs into the same two-factor bound, which I prove in §1 with explicit constants. That obstruction is in fact a complete proof of the statement (by the S-a mechanism), so no counterexample exists inside the card's hypotheses. The only counterexample I found (§3) needs a design that depends on the noise, which the card excludes.

Two side findings:
- The range 1 ≤ t ≤ n^{1−κ₀} and κ₀ play no role; the statement holds for every real t > 0.
- For t ≤ n the term t/√n in the hypothesis is redundant, since t/√n ≤ √t.

## 1. Obstruction (rigorous)

**Notation.** E_m := {S ∈ Ω : |S| > m}; ϖ(S) = w(|S|)/W_K; f₀ := N_N(·; μ_c, σ*²I), the density of y_c; E′ := ‖e‖²/σ*² ~ χ²_N. From [P1]: b₋ = b₀σ*²/2, b₊ = b₀(2(σ*²+M)+1), κ = (b₊/b₋)^{0.51}, 𝓑_n = {σ*²/2 ≤ s_y² ≤ 2(σ*²+M)+1}, c_IG = min_{v∈[σ*²,2σ*²]} IG(v; 0.51, b₊), c♯ = κ²/(c_IG σ*²). These depend on (σ*², M) only. Put r_c := μ_c − X_{c,T}ϑ, so ‖r_c‖² = ‖μ − X_Tϑ‖² ≤ B.

**External result (LM).** Laurent & Massart (2000), Ann. Statist. 28, Lemma 1: for Z ~ χ²_D and x > 0, P(Z − D ≥ 2√(Dx) + 2x) ≤ e^{−x} and P(D − Z ≥ 2√(Dx)) ≤ e^{−x}. Also the Chernoff bound P(|g| ≥ s√(2x)) ≤ 2e^{−x} for g ~ N(0, s²).

**(O1) Numerator.** For the data-free rate b₋, each m^c_{b₋}(S) is a probability density in y_c, because the slab N(0, nv(G_S+I)⁻¹) and IG(0.51, b₋) are proper for every S, any rank, any size up to K. So N_m := Σ_{S∈E_m} ϖ(S) m^c_{b₋}(S)(y_c)/f₀(y_c) has E N_m = ϖ(E_m) ([P1] `lem:num`; it needs only that f₀ > 0 is the density of y_c, with μ arbitrary). Markov gives P(N_m > e^t ϖ(E_m)) ≤ e^{−t}.

**(O2) Denominator.** By [P1] `lem:slab` with φ = ϑ:

Q^c_T ≤ ‖e + r_c‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n = ‖e‖² + 2eᵀr_c + B_T(ϑ) ≤ σ*²E′ + ρ″, with ρ″ := B + 2|eᵀr_c|.

The exponent computation of [P1] `lem:den` uses only this inequality. Restricting v = σ*²u to u ∈ [1, 1 + n^{−1/2}], with log u ≤ u − 1 and 1/u ≥ 2 − u, gives

m^c_{b₊}(T)/f₀(y_c) ≥ D_T^{−1/2} c_IG σ*² n^{−1/2} e^{−Λ″}, where Λ″ := |E′ − N|/(2√n) + E′/(2n) + ρ″/(2σ*²).

Let 𝓔₁ := {|E′ − N| ≤ 2√(Nt) + 2t} and 𝓔₂ := {|eᵀr_c| ≤ σ*√(2Bt)}. Each fails with probability ≤ 2e^{−t} (LM; eᵀr_c ~ N(0, σ*²‖r_c‖²)). On 𝓔₁ ∩ 𝓔₂:

Λ″ ≤ ½ + B/(2σ*²) + (2 + √(2B)/σ*)√t + 2t/√n ≤ C₀[1 + √t + t/√n], with C₀ := max{2 + √(2B)/σ*, ½ + B/(2σ*²)}.

**(O3) Rate bracket.** Since π = Π_b with b = b₀s_y², [P1] `thm:Ta` (deterministic, on 𝓑_n; it needs only T ∈ Ω) gives

π(E_m) ≤ κ² I_{b₋}(E_m)/(ϖ(T) m^c_{b₊}(T)) = κ² N_m / (ϖ(T) m^c_{b₊}(T)/f₀).

For the bracket probability:
- *Lower side.* ‖μ_c + e‖² ≥ ‖(I − P_{μ_c})e‖² ~ σ*²χ²_{N−1}. By LM with x = (N−1)/25, P(s_y² < σ*²/2) ≤ e^{−(N−1)/25} for N ≥ 6.
- *Upper side.* ‖μ_c + e‖² ≤ 2nM + 2‖e‖², so s_y² > 2(σ*²+M)+1 forces E′ > N + (N − 2M)/(2σ*²) ≥ N(1 + δ) for N ≥ 4M, with δ := 1/(4σ*²). By LM with x = γN, γ := min(δ²/16, δ/4), this has probability ≤ e^{−γN}.

Hence P(𝓑_nᶜ) ≤ 2e^{−cn} with c := min(1/25, γ)/2, for n ≥ n₀ := max(7, 4M + 1).

**(O4) Assembly.** Since ϖ(E_m)/ϖ(T) = R^T_m, on 𝓑_n ∩ 𝓔₁ ∩ 𝓔₂ ∩ {N_m ≤ e^tϖ(E_m)}:

log π(E_m) ≤ log c♯ + [log R^T_m + ½ log D_T + ½ log n] + t + C₀[1 + √t + t/√n].

Under the card's hypothesis with C ≥ C₀ + log⁺c♯ the right side is ≤ −t. (If R^T_m = 0 then E_m = ∅.) Therefore, for n ≥ n₀ and every t > 0,

P_e[π(|S| > m) > e^{−t}] ≤ 5e^{−t} + 2e^{−cn}.

So the lemma holds with C := max{5, C₀ + log⁺c♯}, and c, n₀ as above, all depending on (σ*², M, B) only. Nothing depends on p, |T|, D_T or the spectrum of any model.

**What a counterexample would have to do.** It must (i) make N_m exceed e^t times its mean with probability ≫ e^{−t}, (ii) make Λ″ ≫ √t + t/√n with probability ≫ e^{−t}, or (iii) make 𝓑_nᶜ likely. (O1)–(O3) show each is impossible under the card's hypotheses.

## 2. The attacks and where each dies

**A. Models of size near n/2 with small Q^c_S.** Write X_{c,S} with squared singular values λ_i and left singular vectors u_i. Then M_S = Σ h(λ_i)u_iu_iᵀ, D_S = Π f(λ_i), and 1 − h(λ) = 1/f(λ) exactly. At a fixed variance v and y_c ~ N(0, vI):

E[D_S^{−1/2} exp{y_cᵀM_Sy_c/(2v)}] = Π_i f(λ_i)^{−1/2}(1 − h(λ_i))^{−1/2} = 1.

So the fit bought by any direction, at any λ ∈ [0, ∞) (near-duplicates included), is paid for exactly by D_S, at every model size. (O1) is the same identity after mixing over v and for arbitrary μ.

*Illustration (order of magnitude, not used).* Take a fixed orthogonal design with p = K = n/2, x_{c,j} = √N u_j, μ = 0, F = [p]. Then π(F)/π(∅) = C(2K−1, K)⁻¹ n^{−n/4}((2b + ‖e‖²)/(2b + Q^c_F))^ν with Q^c_F = ‖e‖²(1 − (N/n)ρ) and ρ = ‖P_Fe‖²/‖e‖² ≈ ½. Typically this is ≈ 2^{−n} n^{−n/4} 2^{n/2}. Odds ≥ 1 need 1 − ρ ≲ n^{−1/2}, a Beta small-ball event of probability e^{−(n/8) log n (1+o(1))}. A large model can have small Q^c_S only when the noise aligns with its column space, and the probability of that is what Markov on N_m charges.

**B. The data-dependent IG rate.** The plug-in map y_c ↦ m^c_{b₀s_y²(y_c)}(S)(y_c) is homogeneous of degree 2(0.51) − 2ν = −N, so it is not integrable on ℝ^N. A Markov argument at the plug-in rate would therefore be invalid, and this is the natural place to look for a failure. But the divergence sits at s_y → 0 and s_y → ∞, inside 𝓑_nᶜ, which has probability ≤ 2e^{−cn} uniformly over ‖μ‖² ≤ nM. The statement pays for exactly that with its Ce^{−cn} term, and on 𝓑_n the IG density ratio is pointwise within κ.

**C. A reference chosen after seeing X, or even after seeing y.** The cost B_T(ϑ) involves (μ, X, T, ϑ) only, never y. So 𝒯_B := {T ∈ Ω : min_ϑ B_T(ϑ) ≤ B} = {T ∈ Ω : L_T ≤ B} is a deterministic set. The hypothesis' left side is nonincreasing in m, so for each T the admissible m form an up-set {m ≥ m_T}. Any data-dependent admissible choice (T(y), ϑ(y), m(y)) has m(y) ≥ m_* := min_{T∈𝒯_B} m_T, attained at a deterministic T_*. Hence {π(|S| > m(y)) > e^{−t}} ⊆ {π(|S| > m_*) > e^{−t}}, to which §1 applies. For a random design with ε independent of X, condition on X. This attack fails for the conclusion, although the proof step (O2) would not survive a y-dependent ϑ.

**D. Weakening the denominator.** One needs Q^c_T − ‖e‖² large.
- An ill-conditioned T with huge compensating coefficients (the situation of L1a′ Remark 2) violates B_T(ϑ) ≤ B.
- A mean outside col X_T enters only through 2eᵀr_c, which is Gaussian with variance ≤ 4σ*²B and is absorbed by the √t term.
- The variance profile costs |E′ − N|/(2√n) ≤ √t + t/√n off a set of probability 2e^{−t}.

**E. Edge cases and quantifiers.**
- If m < |T|, then R^T_m ≥ q_{|T|}/w(|T|) = C(p, |T|) ≥ 1 and D_T ≥ 1, so the hypothesis fails; it therefore forces m ≥ |T|.
- If m ≥ K, then R^T_m = 0 and π(E_m) = 0.
- Summing R^T_m to p instead of K only strengthens the hypothesis.
- Huge p changes nothing, since no constant depends on p.
- The same C in hypothesis and conclusion is harmless: both are monotone in C in the right direction.
- |T| = 0 is covered, with r_c = μ_c.

## 3. Boundary counterexample (outside the card): design depending on the noise

This shows the fixed-design assumption (ε independent of X) is load-bearing, and it is exactly attack A with the alignment forced.

**Construction.** Let n be even, p = K = k := n/2, μ = 0, T = ∅ (so B = M = 0, D_∅ = 1). Given e, choose orthonormal u_1, …, u_k ∈ ℝ^N with u_jᵀe = ‖e‖/√k for all j, and set x_j = √N·Uu_j.

**Model quantities.** For |S| = s: G_S = N·I, H_S = n²I, D_S = n^s, M_S = (N/n)P_S, Q^c_S = ‖e‖²(1 − (N/n)s/k), and 2b = 0.02‖e‖²/N.

**Posterior.** With F = [p], 2b + Q^c_F ≤ 1.02‖e‖²/N. For s ≤ k/2, 2b + Q^c_S ≥ ‖e‖²/2. Using Σ_s C(p, s)w(s) ≤ 1 and ν ≥ n/2:

π(|S| ≤ k/2) ≤ Σ_{|S|≤k/2} π(S)/π(F) ≤ w(k)⁻¹ n^{k/2}(2.04/N)^ν ≤ 2^n n^{n/4}(2.04/N)^{n/2} = exp{−(n/4) log n + O(n)} → 0,

for every e ≠ 0.

**Failure of the conclusion.** R^∅_m ≤ 2^{1−m}, so the hypothesis holds at m₁ := ⌈(½ log n + 2t + C[1 + √t + t/√n])/log 2⌉ + 1. For fixed t this is < n/4 for large n. Taking t := max(1, log 4C), we get π(|S| > m₁) → 1 surely, while the claimed bound is Ce^{−t} + Ce^{−cn} < 1.

**Consequence.** Lemma S is false if the design may depend on e (adaptive or sequential designs, columns built from the response). Any random-design use must keep ε independent of X, as W3-DIST's (RD) does.

## 4. Summary

- The statement as written survives, with explicit constants C = max{5, C₀ + log⁺c♯}, c = min(1/25, γ)/2, n₀ = max(7, 4M + 1).
- κ₀ and the upper limit on t are not needed.
- It is uniform over p, T, D_T and all designs independent of the noise, and it is stable under post-hoc (even y-dependent) choice of an admissible reference.
- Inputs relied on from [P1]: `thm:T01i`, `thm:Ta`, `lem:slab`, `lem:num` and the exponent computation of `lem:den`. I re-derived the IG-ratio and exponent steps; the rest is cited from the file.

ATTEMPT S/S-c RESULT=NO-PROGRESS GAPS=0
