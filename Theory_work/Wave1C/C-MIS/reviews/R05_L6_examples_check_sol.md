# R05 — Lemma Z, examples, and Corollary N

Overall verdict: **VERIFIED-WITH-AMENDMENTS**. The posterior-concentration arguments and all three examples' intended conclusions survive scrutiny. E1 contains an incorrect coefficient formula caused by mixing raw and standardised coordinates. Corollary N needs qualifications on its density and random-target wording. The null-projection parenthesis in STATEMENT.md is false. None of these defects invalidates Lemma Z's rate or the examples' target-separation conclusions.

Scope: inspected the requested passages against STATEMENT.md, L1's reduction/MIS, L2's Proposition P/GD(a), L4's Theorem F/Corollary F(a), [P3], T03♯, 00_COMMON.md, and the N6/N7 summary. This is a proof review; numerical summaries are corroboration, not proof. No git commands were used. Only this review file was written.

## 1. L6_null.md — Lemma Z

Verdict: **VERIFIED-WITH-AMENDMENTS** (two minor definitions below; substantive proof verified).

- **Setting and reduction, lines 6–11:** Correct. Under GR with zero projected coefficient, Lemma R gives the centred isotropic Gaussian experiment with r = 0 and fixed variance σ_𝒞². Under EP with θ^𝒞 = 0, the deterministic full mean is orthogonal to the whole candidate span. The full-Gram lower bound supplies full column rank and all subset eigenvalue bounds. No upper bound on ‖r‖ is needed for this lemma.
- **Score identity, lines 15–16:** Correct. [P3] eq:score is an identity for every valid input, independently of the mean model. Q^c_∅ = ‖y_c‖² = Q^c_S + t_S, D_∅ = 1, and the common response-dependent rate is b = b₀‖y_c‖²/N. Thus the displayed ratio has exactly the stated sign, denominator, and exponent ν = n/2 + 0.01. There is no substitution of a raw-likelihood posterior or fixed IG rate.
- **Determinant, lines 17–18:** Correct. [P3] lem:det's proof gives D_S = ∏f(λ_i(G_S)), f increasing, and f(g) ≥ (n+1)g/(g+1). Interlacing gives λ_min(G_S) ≥ g₀. Using that proof with an unnormalised floor g₀ is legitimate; the stronger normalised floor in the lemma's stated comparison bound is unnecessary here.
- **Uniform numerator and denominator, lines 19–21:** Correct. M_S ≼ nP_S/(n+1), P_Sr = 0, and nested candidate spans imply ‖P_Se‖² ≤ ‖P_𝒞e‖². Also Q^c_S ≥ ‖(I−P_S)y_c‖². Orthogonality makes the cross term exactly 2rᵀe, and nested orthogonal complements give the claimed lower bound using I−P_𝒞. These inequalities hold simultaneously for every feasible S.
- **Completion of square, line 22:** Correct for r ≠ 0: ‖r‖² + 2σ_*‖r‖Z = (‖r‖ + σ_*Z)² − σ_*²Z² ≥ −σ_*²Z². Z is standard normal for deterministic nonzero r. Its dependence on V_n is harmless; independence is never used.
- **Exponent tightness, lines 23–26:** Correct. U_n is tight because p_𝒞 is bounded, V_n/N → 1, Z² is tight, and N/n → 1. Therefore P(V_n−Z² > 0) → 1 and ν/(V_n−Z²) → 1/2 in probability. Consequently Λ_n = O_P(1) on that event, and exp(Λ_n) is tight there. This does not assert a bounded exponential moment, which would be unjustified and is not needed.
- **Prior, line 27:** Correct even though the main T03♯ theorem excludes s₀ = 0. The algebraic proof of [P3] lem:prior(b) explicitly handles s₀ = i = 0: the first product factor is p/(2p−1) ≤ 1, and subsequent factors are ≤ 1/2. Hence C(p,k)w(k)/w(0) ≤ 2·2^(−k), including p = k = 1. No empty-truth version of T03♯ is being assumed.
- **Sum and rate, lines 28–30:** Correct. The actual sum stops at K; extending the positive numerical bound to infinity gives Σ_{k≥1}2(a_n/2)^k = a_n/(1−a_n/2) ≤ 2a_n. The exceptional event has probability tending to zero, which suffices for O_P(n^(−1/2)); it need not have that rate itself.
- **Consequences, lines 12–13 and 30–31:** Correct as probability statements. With δ_n = 1−π_𝒞(∅|y), every PIP is ≤ δ_n, and δ_n < 1/2 forces both an empty MPM and an empty strict global HPM. Boundedness implies Eδ_n → 0, without an expectation-rate claim. Corollary H gives P(𝒪 ∩ {Ŝ⁺ ≠ ∅}) ≤ 2Eδ_n + D_n(∅); this does not eliminate the never-scored term.

Exact minor amendments:

1. At line 22, write the displayed division by ‖r‖² only for r ≠ 0. For r = 0, state separately that the lower bound is 0 ≥ −σ_*²Z² = 0. Defining Z = 0 does not itself define the intermediate expression 0/0.
2. Define Λ_n = 0 on {V_n−Z² ≤ 0}, retaining its ratio definition on the positive event. All bounds are asserted only on the positive event. This makes the global O_P notation formally unambiguous.

**Related contextual error — STATEMENT.md:92–93:** The parenthesis identifying β^𝒞 = 0 with “every omitted signal is independent of the candidates” is **FALSE**. For independent standard Gaussian x₁,z, take x_k = −x₁+z and β₁ = β_k = 1. Then γ₁ = −1 and β^𝒞 = 0, although cov(x₁,x_k) = −1. Exact amendment: replace that parenthesis with “β^𝒞 = β_𝒞 + γ = 0: the candidate coefficient and the projected omitted contribution cancel coordinatewise.” Under EP, state instead P_𝒞μ_c = 0. This corrects the interpretation, not the lemma.

N6 is consistent with the null rate but does not establish it. The growing-p exclusion is appropriate for this proof.

## 2. L2_gaussian.md — R04 edits and Example E1

### Setting and Proposition P(a), lines 5–18

Verdict: **VERIFIED**.

Taking 𝒪 = S₀ ∖ 𝒞 and inverting the covariance of the marginal vector (x_𝒞,x_𝒪) repairs the inactive-omitted-variable problem. In R04's matrix example, the marginal covariance on {1,2} is [[3/2,1/2],[1/2,3/2]], whose precision is [[3/4,−1/4],[−1/4,3/4]]. The repaired singleton formula gives −(−1/4)/(3/4) = 1/3, as required. The block identities also remain valid for larger omitted sets with zero coefficients included, provided all covariance/precision blocks refer to that same vector.

Gaussian conditioning gives the displayed γ, a, Schur-complement variance, and iid residual entries independent of the candidate matrix. Independence of the predictors and ε also supplies conditional independence from ε. At each n, ε′ has the stated isotropic law independent of X^r_𝒞. The new distinction between this finite-n identity and GR's requirement τ_n² ≡ τ² is correct. With Σ_𝒞𝒞 ≻ 0, the conditional mean coefficient and residual variance are uniquely determined, so the “iff” concerning fixed τ² is justified. GD(a)'s fixed parameters meet that requirement.

### Example E1, lines 113–124

Verdict: **VERIFIED-WITH-AMENDMENTS** (one erroneous formula; support conclusion verified).

The cancellation, proxy, residual variance, precision entries, and GD(a)/MIS application are correct. Writing a = (−1,1,0)ᵀ, the precision matrix of (x_𝒞,x_k) is [[I+aaᵀ,−a],[−aᵀ,1]], verifying every precision entry quoted. Thus π_𝒞({2}|y) → 1, while π_𝒞({1}|y) → 0.

**Required correction at line 122:** The displayed expression mixes the raw coefficient mean (0,1,0) with a noise coefficient computed using standardised X_𝒞. Set A = X^r_𝒞 and v = (0,1,0)ᵀ. The candidate slopes in the projection on [1,A] are

β̂_proj = v + (AᵀCA)^(−1)AᵀCz.

Equivalently, the coefficients of the centred projection in standardised columns X_𝒞 = CAD_x^(−1) are

θ̂_proj = D_xv + (X_𝒞ᵀX_𝒞)^(−1)X_𝒞ᵀCz.

Use either formula and call these the three candidate slopes, excluding the intercept. Conditional on A, the raw noise coefficient has covariance (AᵀCA)^(−1) ≻ 0. Each coordinate therefore has a continuous nondegenerate Gaussian law and is nonzero almost surely, even when its mean is zero. Full centred rank holds almost surely for n ≥ 4; the dense model is feasible eventually (n ≥ 6). Diagonal rescaling preserves support. Hence the dense sample-projection support is {1,2,3} almost surely and its posterior mass tends to zero as claimed. N7 corroborates these conclusions.

## 3. L5_frontier.md §6 — boundary examples

### Example E2, lines 78–87

Verdict: **VERIFIED**.

The balanced ±1 column makes each omitted coordinate N(0,1), but cov(ω) = x₂x₂ᵀ has rank one and off-diagonal dependence. A deterministic candidate design cannot absorb the random slope into GR's deterministic γ; nor is its residual covariance τ²I. Thus GR fails even though the entire omitted vector is Gaussian.

For each fixed z ≠ 0, the conditional experiment has truth {1,2}, variance 1, standardised coefficients √(n/N)(1,z), orthogonal Gram NI, bounded signal energy per observation, and BM-∞. T03♯ applies along even n. Its energy bound and starting index may depend on z; no uniformity in z is required. For each η > 0, the bounded conditional failure probabilities P(1−π_𝒞({1,2}|y)>η | Z=z) tend to zero for almost every z. Dominated convergence integrates them to zero. This proves the joint-law claim and then π_𝒞({1}|y) → 0. The iid-row disclaimer and the restricted interpretation of the example are correct.

### Example E3, lines 89–96

Verdict: **VERIFIED** (using the section's contrast-coordinate convention).

Read x₁,x₂ in μ_c as the contrast columns X_{c,𝒞}; their Gram is NI. The remainder r′ for target {1} has x₂ᵀr′ = cN ≠ 0, so EP fails for that target. For target {1,2}, EP holds, s = p = 2, K = 2 eventually, all eigenvalue requirements hold, and the prior-size tail is identically zero. The total energy satisfies ‖μ_c‖² = N(b²+c²)+‖r‖² ≤ (b²+c²+M)N. Choose the theorem's energy constant accordingly; it need not equal the symbol bounding the residual alone. Since σ²+‖r‖²/N ≤ σ²+M, fixed nonzero b,c imply BM-∞. Corollary F(a) therefore gives the claimed concentration on {1,2} and rejection of {1}. There is no missing substantive hypothesis.

## 4. L1_reduction.md — Corollary N, lines 62–68

Verdict: **VERIFIED-WITH-AMENDMENTS** (core inequality verified; qualify the explanatory extensions).

The inequality is pathwise and simultaneous over all T ≠ S₀^𝒞 in Ω_𝒞. It immediately gives the stated rate and rejection of any feasible wrong retained-truth model. The equivalence between differing supports and the existence of a proxy or exact cancellation is correct.

Exact amendments:

1. Explicitly extend π_𝒞(T|y) = 0 for T outside Ω_𝒞 when discussing the retained-truth and sample-projection supports. Full column rank does not imply capped feasibility. With this convention the same upper bound holds for every wrong subset, feasible or otherwise.
2. Replace “generically all of 𝒞” with: “If τ² > 0 and the centred candidate matrix has full column rank, this sample-projection support is all of 𝒞 almost surely.” Indeed, under fixed-design GR the sample coefficient is β^𝒞 + (AᵀCA)^(−1)AᵀCξ, with covariance τ²(AᵀCA)^(−1) ≻ 0. GR permits τ² = 0; then the sample projection is exactly β^𝒞 and can be sparse. For example, β^𝒞 = (1,0) with full-rank candidates and an omitted contribution exactly in their span satisfies GR with τ² = 0. Density is therefore not an unconditional consequence of the corollary's hypotheses.
3. Make the random-target qualification precise. For a measurable sample-projection support T_n, the unconditional assertion justified without further assumptions is

   1{T_n ≠ S₀^𝒞}π_𝒞(T_n|y) ≤ 1−π_𝒞(S₀^𝒞|y) = O_P(r_n).

   In particular, π_𝒞(T_n|y) → 0 if P(T_n ≠ S₀^𝒞) → 1. Do not infer a conditional convergence statement given a potentially vanishing-probability mismatch event. E1 has almost-sure mismatch, so its conclusion is unaffected.

No GAP or FALSE verdict applies to the central posterior claims reviewed here. The explicitly identified false contextual independence statement and erroneous E1 formula require the corrections above before an unqualified VERIFIED status.
