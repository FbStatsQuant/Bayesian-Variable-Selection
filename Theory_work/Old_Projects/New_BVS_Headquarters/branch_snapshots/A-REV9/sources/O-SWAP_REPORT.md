# O-SWAP: finite-n theory of the posterior misses (n = 200, p ∈ {500, 1000}, s₀ = 14)

Run: O-SWAP (Opus 5.5), branch `theory/O-SWAP`, 2026-11-02. Everything here is a **candidate**: not reviewed, not adopted.

## 1. Headline

**Status:** Props 1–3 PROVED under the projection approximation PA (Lemma 0, PROVED; its error is O(10⁻³) nats). Thm 4, Prop. 5 and Prop. 6 PROVED. Cor. 2.1 PROOF SKETCH. Predictor T2 is an approximation. The SuSiE/SSL link is a CONJECTURE.

- **Each posterior-miss mode has an exact finite-n law** given X: Gaussian/χ² events in residual projections, under PA.
  - Swap: Prop. 1, P ≈ Φ(−|δ_j|√((1−ρ_{jl})/2)), with no size-prior term (T07).
  - Superset: Prop. 2, a χ²₁ tail at a p-free threshold t_add ≈ 3.7–4.1σ that **rises with the SNR** through the τ = 1 pseudo-observation (Cor. 2.1).
  - Subset: Prop. 3, Φ(t_drop − |δ_j|).
- **The observed misses match the one-move posterior misses.** On the study's own data (regenerated in Python with R's RNG ported exactly), the exact-score one-move check reproduces the observed SMC-BVS miss count in all 24 cells to within ±1: 39 / 37 / 227 / 257 against 40 / 37 / 230 / 259.
- **The theory predicts the rates.** The design-averaged predictor T2 (Props 1–3 + 6) gives 43 / 40 misses per 600 at c = 1 against 40 / 37 observed, and 251 / 271 at c = 0.5 against 230 / 259. It reproduces the scenario ranking (S4 ≫ S5 > S6 ≈ S3 > S1 ≈ S2) and the type split: supersets at c = 1, swaps and drops at c = 0.5.
- **Why the modes switch with c.** Supersets face a nearly fixed prior threshold (it falls only slightly with ω₀), so their rate only doubles from c = 1 to c = 0.5. Swaps and drops are exponential in δ² ∝ c². A higher-threshold selector (SuSiE/SSL-like) is predicted to win at c = 1 and lose at c = 0.5 (CONJECTURE as applied to those methods).

## 2. Setting and notation

Notation is that of `Docs/Theory/theorems/00_COMMON.md`. We fix the design X (standardised, ‖x_j‖² = n − 1), the truth S₀ (s₀ = |S₀|), and the coefficients θ on the X scale. In the study θ = c·β, where β has the pattern (1.4, −1, 1.8, −1.2, 0.8, −1.6) cycled over the 14 truths, c ∈ {1, 0.5}, and the noise sd is σ = 1. We write ỹ = C y^r = μ + Cε with μ = X_{S₀}θ and ε ~ N(0, σ²I). All probabilities are **conditional on X** and are over ε.

F is invariant under y ↦ a·y except through the constant 2b₀ = 0.02. So we work on the raw contrast scale with b̃ := 2b₀ s_y². In every formula b̃ is replaced by its design-level value 2b₀ s̄_y², where s̄_y² = (‖μ‖² + (n − 1)σ²)/(n − 1). The resulting error in a log-score difference is at most ν·2b₀|s_y² − s̄_y²|/Q, which is below 10⁻³ nats here.

New symbols (all deterministic given X):

- For T ⊂ [p] and k ∉ T: r_{k|T} = (I − P_T)x_k. For a truth j, T_j := S₀ − j and r_j := r_{j|T_j}.
- For a swap pair (j, l): ρ_{jl} := cor(r_{j|T_j}, r_{l|T_j}), the partial correlation of x_j and x_l given the other truths.
- δ_j := θ_j‖r_j‖/σ = θ_j √((n−1)(1 − R²_{j|T_j}))/σ, the signal-to-noise of truth j given the other truths.
- Log determinant ratios use D_S = det H_S / det(G_S + I) exactly:
  - adding l: κ⁺_l := log(w(s₀)/w(s₀+1)) + ½ log(D_{S₀+l}/D_{S₀}) = log((2p−1−s₀)/(s₀+1)) + ½ log(D_{S₀+l}/D_{S₀});
  - dropping j: γ_j := log(w(s₀−1)/w(s₀)) + ½ log(D_{S₀}/D_{S₀−j}) = log((2p−s₀)/s₀) + ½ log(D_{S₀}/D_{S₀−j});
  - swapping j for l: κ_{jl} := ½ log(D_{S₀−j+l}/D_{S₀}). The size prior cancels exactly.
- λ := e^{κ/ν} for each κ, and ν = a₀ + n/2.
- Residual sums: E_A := ‖(I − P_A)ỹ‖², W_A := ‖P_A ỹ‖². The pseudo-observation terms are Ω₀ := E W_{S₀}/(n+1) + b̃ and Ω_j := E W_{T_j}/(n+1) + b̃, with ω = Ω/σ².
- **First-order (one-move) posterior-miss event:** L := {∃ S' ∈ 𝒩(S₀) : F(S') > F(S₀)}, where 𝒩(S₀) holds the p − s₀ adds, the s₀ drops and the s₀(p − s₀) swaps.

At c = 1, Ω₀/σ² ≈ ‖μ‖²/(n+1) ≈ 24; at c = 0.5 it is ≈ 6. The τ = 1 pseudo-observation in H_S = (n+1)G_S + I leaves a fraction 1/(n+1) of the fitted sum of squares in Q_S. This acts as an **SNR-dependent extra size penalty** (Prop. 2).

## 3. Statements and proofs

### Lemma 0 (projection approximation PA). PROVED.

Write G_S = VΛVᵀ and X_S = U Λ^{1/2} Vᵀ, where UᵀU = I and P_S = UUᵀ. Then

  Q_S = Q̃_S + η_S,  with Q̃_S := E_S + W_S/(n+1) and η_S = Σ_i n (u_iᵀỹ)² / ((n+1)((n+1)λ_i + 1)) ∈ [0, n W_S/((n+1)((n+1)λ_min(G_S)+1))].

*Proof.* n X_S H_S⁻¹ X_Sᵀ = U diag(nλ_i/((n+1)λ_i+1)) Uᵀ. Also n/(n+1) − nλ/((n+1)λ+1) = n/((n+1)((n+1)λ+1)), and ỹᵀỹ − (n/(n+1))W_S = E_S + W_S/(n+1). ∎

To first order, η_S ≈ ‖θ̂_S‖²·n/(n+1)², where θ̂_S is the OLS coefficient vector. The error it induces in a one-move log-score difference is ν(η_{S'} − η_{S₀})/Q ≈ (θ̂²_{in} − θ̂²_{out})/(2σ²(n−s₀)), which is O(10⁻³) nats in this study. Every analytic statement below is exact for the score with Q replaced by Q̃ (call it F̃). The conditional Monte Carlo of §4 uses the **exact** F, so the PA is checked empirically.

### Proposition 1 (within-size swap). PROVED under PA.

Fix a truth j and a null l. Set A := r_jᵀỹ/‖r_j‖ and B := r_{l|T_j}ᵀỹ/‖r_{l|T_j}‖. Then (A, B) ~ N(σ(δ_j, ρδ_j), σ²[[1, ρ],[ρ, 1]]) with ρ = ρ_{jl}. Let U = S₀ ∪ {l}, E_U ~ σ²χ²_{n−2−s₀}, and W_{T_j}. These three are mutually independent and independent of (A, B). Then

  {F̃(S₀ − j + l) > F̃(S₀)} = { (n/(n+1))(λ B² − A²) > (λ − 1)(E_U + ‖v‖² + W_{T_j}/(n+1) + b̃) },  where λ = e^{κ_{jl}/ν} and ‖v‖² = (A² − 2ρAB + B²)/(1 − ρ²).

In particular, when κ_{jl} = 0 (to first order κ_{jl} = O(1/n); see the remark),

  **P_swap(j, l) = Φ(−d₋)Φ(d₊) + Φ(d₋)Φ(−d₊),  d∓ := |δ_j| √((1 ∓ ρ)/2)**,

and Φ(−d₋)Φ(d₊) ≤ P_swap ≤ Φ(−d₋) + Φ(−d₊). For ρ > 0 and δ_j → ∞, P_swap ~ Φ(−d₋).

*Proof.*
1. ỹ − P_{T_j}ỹ lies in span(r_j) ⊕ span(r_l)^⊥-part ⊕ (I − P_U)ỹ. Because the components are orthogonal projections of an isotropic Gaussian, A, B, E_U and W_{T_j} have the stated joint law. The means are r_jᵀμ/‖r_j‖ = θ_j‖r_j‖ and r_{l|T}ᵀμ/‖r_{l|T}‖ = θ_j r_{l|T}ᵀr_j/‖r_{l|T}‖ = ρθ_j‖r_j‖, because (I − P_T)μ = θ_j r_j. μ ∈ span X_{S₀} ⊆ span X_U, so E_U is central.
2. Write P_U − P_T = projection onto span(r_j, r_l) =: v. Then Q̃_{T+k} = E_U + ‖v‖² − (n/(n+1))·(coordinate of k)² + W_T/(n+1), where the coordinate is A for k = j and B for k = l. Substituting into F̃(S') − F̃(S₀) = −κ_{jl} − ν log((Q̃_{S'} + b̃)/(Q̃_{S₀} + b̃)) gives the displayed event.
3. When λ = 1 the event is B² > A² ⇔ (B − A)(B + A) > 0. (B − A, B + A) is Gaussian with Cov = Var B − Var A = 0, so its two coordinates are independent. Their standardised means are −δ√((1−ρ)/2) and δ√((1+ρ)/2), which gives the closed form.
4. The bounds follow by dropping a non-negative term, and by the union bound on {B − A > 0} ∪ {B + A < 0}. ∎

The general-λ probability is computed exactly by a Gauss–Hermite integral over the s-coordinate and a closed-form interval in the d-coordinate (`scripts/analytic.py::p_swap`; it agrees with direct MC to 3 decimals in `scripts/test_analytic.py`). There E_U is replaced by its mean. The error this causes is at most |λ − 1|·σ²√(2(n−2−s₀)) ≈ 0.03σ².

*Remark (κ_{jl} is small but not negligible).* In this study |κ_{jl}| ≲ 0.3 nats. That moves P_swap by up to about 15 % relative (e.g. δ = 4, ρ = 0.85: 0.137 at λ = 1 versus 0.116 at λ = 1.002), so the predictions use the exact κ_{jl}.

*Margin link to W1-T37R.* The mean log-score gap is M_{jl} := E[A² − B²]/(2σ²) = δ_j²(1 − ρ²)/2 = (n−1)θ_j²(1 − R²_{j|T_j})(1 − ρ²)/(2σ²). This is T37R's margin, with the partial R² factor added. The miss probability is governed by d₋² = M_{jl}/(1 + ρ), not by M_{jl}: **P_swap ≈ Φ̄(√(M_{jl}/(1+ρ)))**.

### Proposition 2 (superset by one null). PROVED under PA.

For a null l, let u_l = r_{l|S₀}/‖r_{l|S₀}‖ and B_l := u_lᵀỹ. B_l ~ N(0, σ²) exactly, for every design and every θ. Let E := E_{S₀} ~ σ²χ²_{n−1−s₀}. Then

  {F̃(S₀ + l) > F̃(S₀)} = { B_l² / (E + Ω₀) > τ_l },  τ_l := (n+1)(1 − e^{−κ⁺_l/ν})/n.

Hence, with E' := E − B_l² ~ σ²χ²_{n−2−s₀} independent of B_l,

  **P_add(l) = P( χ²₁ (1 − λ_l/(n+1)) > (λ_l − 1)(χ²_{n−2−s₀} + ω₀) )**,  λ_l = e^{κ⁺_l/ν}.

Under the same PA, the union over nulls is exactly {max_l B_l²/τ_l > E + Ω₀}, where (B_l/σ)_l ~ N(0, Γ) with Γ_{ll'} = u_lᵀu_{l'}.

*Proof.* P_{S₀+l} = P_{S₀} + u_lu_lᵀ, so Q̃_{S₀+l} = E − B_l² + (W_{S₀} + B_l²)/(n+1) and Q̃_{S₀} = E + W_{S₀}/(n+1). The event Q̃_{S₀} + b̃ > λ(Q̃_{S₀+l} + b̃) rearranges to λ(n/(n+1))B_l² > (λ − 1)(E + Ω₀), which is the displayed event. Because u_l ⟂ span X_{S₀} ∋ μ, B_l is central. ∎

*Consequences.*
- (i) P_add(l) depends on the design only through κ⁺_l. For every l, κ⁺_l ≈ ½ log(n+1) + log((2p−1−s₀)/(s₀+1)), which is 6.83 at p = 500 and 7.54 at p = 1000. It depends on the signal only through ω₀ ≈ ‖μ‖²/((n+1)σ²).
- (ii) **The superset rate is essentially scenario-free.** For nearly orthogonal u_l, P(superset) ≈ 1 − (1 − q)^{p−s₀}, where q = P_add: 1.5–3.0 × 10⁻⁴ at p = 500 and 0.7–1.5 × 10⁻⁴ at p = 1000 (Cor. 2.1). Correlated nulls (S2–S6) lower the effective count.
- (iii) Lowering the SNR from c = 1 to c = 0.5 lowers ω₀ from ≈ 24 to ≈ 6. That lowers the effective χ²₁ threshold by about 9 % and raises q by about 2× (Cor. 2.1).

### Corollary 2.1 (the superset rate is p-free and rises as the signal falls). PROOF SKETCH (expansion); the numbers are exact evaluations of Prop. 2.

Let t_add be the root of P_add: the event of Prop. 2 is |B_l|/σ > t_add·√((E + Ω₀)/(σ²(n − 2 − s₀ + ω₀))) ≈ t_add, with

  t_add² = (λ − 1)(n − 2 − s₀ + ω₀)/(1 − λ/(n+1)) = 2κ⁺(1 + η)(1 + O(κ⁺/n)),  η := (ω₀ − s₀ − 2)/n.

With κ⁺ = ½ log(n+1) + log((2p − 1 − s₀)/(s₀ + 1)) + O(1/n),

  log[(p − s₀)q] ≈ log[(p − s₀)·2φ(t_add)/t_add] = −η log(2p) − ½(1+η) log(n+1) + (1+η) log(s₀+1) − log t_add − ½ log(2π) + o(1).

The step uses log(p − s₀) − log(2p − 1 − s₀) = −log 2 + o(1), which cancels the factor 2 of the two-sided tail.

So the family-wise superset rate 1 − (1 − q)^{p−s₀} depends on p only through p^{−η}/t_add, with |η| < 0.05 here. **The BB(1, p) term log((2p−k−1)/(k+1)) cancels the multiplicity of the nulls almost exactly.** The SNR enters through ω₀ ≈ ‖μ‖²/((n+1)σ²): the pseudo-observation's share of the fitted sum of squares raises the threshold when the signal is strong.

| | κ⁺ | γ (drop) | t_add (σ units) | q per null | 1 − (1 − q)^{p−s₀} | t_drop |
|---|---|---|---|---|---|---|
| p = 500, c = 1 (ω₀ ≈ 24.6) | 6.84 | 6.91 | 3.85 | 1.51 × 10⁻⁴ | 0.071 | 3.88 |
| p = 500, c = 0.5 (ω₀ ≈ 6.2) | 6.84 | 6.91 | 3.68 | 3.03 × 10⁻⁴ | 0.137 | 3.71 |
| p = 1000, c = 1 | 7.54 | 7.61 | 4.05 | 6.88 × 10⁻⁵ | 0.066 | 4.08 |
| p = 1000, c = 0.5 | 7.54 | 7.61 | 3.87 | 1.48 × 10⁻⁴ | 0.136 | 3.90 |

(ω₀ is the design average, and the κ's here are the leading-order values; the cell predictions in §4 use the exact per-design values.) The independence value 1 − (1 − q)^{p−s₀} is an upper-type approximation: correlated nulls (S2–S6) lower the effective number of independent competitors.

### Proposition 3 (subset: a truth dropped). PROVED under PA.

With A := r_jᵀỹ/‖r_j‖ ~ N(σδ_j, σ²), independent of E ~ σ²χ²_{n−1−s₀}, and Λ_j = e^{γ_j/ν},

  **P_drop(j) = E[ Φ(t − |δ_j|) − Φ(−t − |δ_j|) ]**, where t = √((Λ_j − 1)(χ²_{n−1−s₀} + ω_j)/(1 − Λ_j/(n+1))).

*Proof.* Q̃_{S₀−j} = E + A² + W_T/(n+1) and Q̃_{S₀} = E + W_T/(n+1) + A²/(n+1). The event Q̃_{S₀−j} + b̃ < Λ(Q̃_{S₀} + b̃) rearranges to A²(1 − Λ/(n+1)) < (Λ − 1)(E + Ω_j). ∎

The drop gain is γ_j ≈ ½ log(n+1) + log((2p−s₀)/s₀), which is 6.90 at p = 500 and 7.60 at p = 1000. So a truth is at risk when |δ_j| ≲ 3.6 + 2 = 5.6. At c = 0.5 the weakest truths have |θ| = 0.4 and |δ| ≈ 5.4–5.6: they sit right at the edge.

### Theorem 4 (first-order bracket). PROVED (exact F, no PA needed for the inequalities).

For every X and θ:

  max_e p_e ≤ P(L | X) ≤ P(S₀ ≠ S† | X), and P(L | X) ≤ Σ_e p_e,

where e runs over the one-move events and p_e = P(F(S') > F(S₀) | X).

*Proof.* On L, some S' ∈ Ω beats S₀ strictly, so S₀ is not the argmax (ties have probability 0). The other two inequalities are monotonicity and the union bound. ∎

The **predictor T1** is P̂_T1(X) = 1 − Π_e(1 − p_e): independence across events, with p_e from Props. 1–3 and the exact κ's. It is an approximation, not a theorem; its accuracy is reported in §4. The **lower bracket T1-lo** treats each cluster as perfectly dependent and the clusters as independent. The clusters are: the adds of the nulls in one generator group of 5; and, for each truth j, {drop_j} ∪ {swap_{jl} : all l}. The per-cell prediction is the average of P̂(X) over the 100 actual study designs of that cell.

### Proposition 5 (the swap ceiling is information-theoretic). PROVED (standard two-point bound).

Fix (j, l) and let μ' := P_{S₀−j+l} μ be the closest mean supported on S' = S₀ − j + l. Then ‖μ − μ'‖ = σ|δ_j|√(1 − ρ²), and for **any** selector Ŝ (any prior, any method),

  ½[P_μ(Ŝ ≠ S₀) + P_{μ'}(Ŝ ≠ S')] ≥ Φ(−|δ_j|√(1 − ρ²)/2).

The HPM's own swap error is P_swap ≈ Φ(−|δ_j|√((1−ρ)/2)). The squared exponents differ by a factor (1 + ρ)/2, which tends to 1 as ρ → 1.

*Proof.* (I − P_{S'})μ = θ_j(I − P_{S'})x_j and ‖(I − P_{S'})r_j‖² = ‖r_j‖²(1 − ρ²). The rest is Le Cam's two-point bound for N(μ, σ²I) against N(μ', σ²I), whose minimal sum of errors is 2Φ(−‖μ − μ'‖/(2σ)). ∎

*Connection to T07.* Prop. 1 contains no size-prior term: the size prior cancels exactly in a within-size swap. This is T07's Prop. 1 in quantitative form. The swap probability also changes with g only through κ_{jl} = O(1/n). Prop. 5 says more: for look-alikes (ρ ≈ 0.85, as in S4), no method can push the averaged swap error much below the HPM's. The numbers are δ = 5.4, ρ = 0.85: the HPM gives Φ(−1.49) = 0.068 and the two-point bound gives Φ(−1.43) = 0.076.

### Proposition 6 (conditional representation of a truth's competitor cluster). PROVED (exact, no PA). Predictor T2: approximation.

Fix a truth j and write A_j := r_jᵀỹ/‖r_j‖ and B_{jl} := r_{l|T_j}ᵀỹ/‖r_{l|T_j}‖ (Prop. 1). Then, for every null l,

  B_{jl} = ρ_{jl} A_j + √(1 − ρ²_{jl}) Z_{jl},  with Z_{jl} ~ N(0, σ²) independent of A_j,

and the Z_{jl} are **central**: their mean is 0 whatever θ is.

*Proof.* (A_j, B_{jl}) is bivariate normal with unit correlation ρ_{jl} and equal variances σ² (Prop. 1, step 1). So Z_{jl} := (B_{jl} − ρ_{jl}A_j)/√(1 − ρ²_{jl}) is uncorrelated with A_j, hence independent of it. Its mean is (ρ_{jl}θ_j‖r_j‖ − ρ_{jl}θ_j‖r_j‖)/√(1−ρ²_{jl}) = 0. ∎

*Consequence (the cluster event).* Under PA and with λ ≡ 1, the event that truth j is lost to a one-move competitor (a drop or any swap (j, l)) is

  {A_j² < t_j²(E)} ∪ {max_l |ρ_{jl}A_j + √(1−ρ²_{jl})Z_{jl}| > |A_j|}.

Conditional on A_j, its probability is driven by the signs and sizes of the ρ_{jl}, and the large-|ρ| competitors (the group-mates in S3–S6) dominate. For a single competitor this reduces to Prop. 1.

**Predictor T2** evaluates P(L) as E_E[ Π_l (1 − q_l(E)) · Π_j (1 − P_j(E)) ]. Here E is the common residual χ²_{n−1−s₀}, q_l(E) is the add probability of Prop. 2 given E, and

  P_j(E) = 1 − E_{A_j}[ 1{A_j ∉ drop region(E)} · Π_l P(B_{jl}² ≤ thr_{jl}(A_j) | A_j) ],

with the exact κ's (`scripts/t2.py`). T2 makes three approximations:
- (a) the Z_{jl} are taken as independent across l given A_j (they are correlated through the partial correlations of the nulls);
- (b) the clusters (the add block and each truth) are taken as independent given E;
- (c) inside the O(λ − 1) terms, ‖v‖² ≈ A² + σ², the swap thresholds use E at its mean, and E_U, E', E_{S₀} are identified (each error is O(10⁻³) in probability).

It is an approximation, not a bound. A Šidák/Royen-type inequality does not apply directly: the slabs in (a) are not centred, and E is not independent of the B_l. Its accuracy is measured against the exact-score MC in §4.

## 4. Evidence: prediction vs observed

### 4.1 Procedure (all on the laptop, Python only)

- **Data.** `scripts/rgen.py` ports `Scripts/Data_generators/gen_prod_data.R` and R's `set.seed` / Mersenne-Twister / Inversion `rnorm` exactly. It matches R's `set.seed(1); rnorm(5)` and `set.seed(42); rnorm(3)` to all printed digits. So every one of the 1,200 study designs X, every ε, every S₀ and every β is the study's own, up to floating-point rounding in `chol` and the matrix product.
- **Per dataset and scale** (`scripts/run_local.py`, 4 cores, ≈ 35 min in total):
  - **Analytic.** The one-move probabilities of Props 1–3 with the exact κ⁺_l, γ_j and κ_{jl} of that design, combined as T1 (independence) and T1-lo (cluster maximum).
  - **T2** (Prop. 6, `scripts/t2.py`), and the Le Cam pairwise floor max_{(j,l)} Φ(−|δ_j|√(1−ρ²_{jl})/2).
  - **Realised check on the study's own y.** Is S₀ beaten, under the **exact** score F, by any one-move neighbour (adds, drops, swaps: ≈ 14p models) or by any of the 91 double drops? If it is, a best-improvement add/drop/swap hill-climb runs from the best such neighbour, and the end point is classified against S₀ with the study's categories (extra-only / missed-only / mixed).
  - **Conditional MC.** The same check on R = 40 fresh noise vectors given the actual X (8,000 draws per cell and scale, exact F).
- **Observed** = SMC-BVS v3 HPM from `Results/SMC_BVS_v3_production/p*/exact_recovery_long.csv`: miss = n_success − exact, split into err_extra_only / err_missed_only / err_mixed. The 4 no-output fits are excluded, and their cells are rescaled to 100.
- **z** = (observed − Σ_i p̂_i)/√(Σ_i p̂_i(1 − p̂_i)) over the 100 designs of the cell, with p̂_i from T2 or from the MC.

### 4.2 Tables


#### c = 1  (counts per 100 datasets; observed = SMC-BVS v3 HPM)

| p | S | **observed** miss (extra/missed/mixed) | realised on study y (extra/missed/mixed) | MC P(miss) (extra/missed/mixed) | MC P(L) one-move | **T2** (add / drop+swap) | T1 indep. | T1-lo | z(obs vs T2) | z(obs vs MC) | Le Cam floor |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 500 | S1 | **5** (5/0/0) | 5 (5/0/0) | 7.4 (7.4/0.0/0.0) | 7.4 | **6.5** (6.5 / 0.0) | 7.0 | 1.5 | -0.6 | -0.9 | 0.0 |
| 500 | S2 | **4** (4/0/0) | 4 (4/0/0) | 6.9 (6.9/0.0/0.0) | 6.9 | **6.6** (6.6 / 0.0) | 7.1 | 1.5 | -1.1 | -1.1 | 0.0 |
| 500 | S3 | **6** (6/0/0) | 6 (6/0/0) | 6.3 (6.2/0.0/0.0) | 6.3 | **6.7** (6.7 / 0.0) | 7.1 | 1.5 | -0.3 | -0.1 | 0.0 |
| 500 | S4 | **9** (5/0/4) | 9 (5/0/4) | 5.9 (4.5/0.0/1.4) | 5.9 | **8.0** (6.6 / 1.5) | 8.4 | 2.0 | +0.4 | +1.3 | 0.4 |
| 500 | S5 | **10** (10/0/0) | 9 (9/0/0) | 8.3 (8.3/0.0/0.0) | 8.3 | **8.6** (8.5 / 0.0) | 9.2 | 2.0 | +0.6 | +0.7 | 0.0 |
| 500 | S6 | **6** (6/0/0) | 6 (6/0/0) | 5.9 (5.5/0.0/0.3) | 5.9 | **6.8** (6.5 / 0.3) | 7.2 | 1.6 | -0.3 | +0.1 | 0.1 |
| 1000 | S1 | **5** (5/0/0) | 5 (5/0/0) | 6.2 (6.2/0.0/0.0) | 6.2 | **6.1** (6.1 / 0.0) | 6.5 | 1.4 | -0.4 | -0.5 | 0.0 |
| 1000 | S2 | **5** (5/0/0) | 5 (5/0/0) | 5.5 (5.5/0.0/0.0) | 5.5 | **6.1** (6.1 / 0.0) | 6.5 | 1.4 | -0.4 | -0.2 | 0.0 |
| 1000 | S3 | **3** (3/0/0) | 2 (2/0/0) | 5.5 (5.5/0.0/0.0) | 5.5 | **6.0** (6.0 / 0.0) | 6.4 | 1.3 | -1.3 | -1.1 | 0.0 |
| 1000 | S4 | **7** (4/0/3) | 7 (4/0/3) | 5.7 (4.0/0.0/1.6) | 5.7 | **7.6** (6.1 / 1.6) | 8.0 | 2.0 | -0.2 | +0.6 | 0.4 |
| 1000 | S5 | **13** (13/0/0) | 14 (14/0/0) | 8.4 (8.4/0.0/0.0) | 8.4 | **8.1** (8.1 / 0.0) | 8.8 | 1.9 | +1.9 | +1.8 | 0.0 |
| 1000 | S6 | **4** (4/0/0) | 4 (4/0/0) | 6.3 (5.9/0.0/0.4) | 6.3 | **6.3** (6.0 / 0.3) | 6.8 | 1.5 | -1.0 | -1.0 | 0.1 |
| 500 | sum (6 cells) | **40** | 39 | 41 | 41 | **43** | 46 | 10 | | | |
| 1000 | sum (6 cells) | **37** | 37 | 38 | 38 | **40** | 43 | 9 | | | |

RMS z (obs vs T2) = 0.86; RMS z (obs vs MC) = 0.93 over 12 cells.

#### c = 0.5  (counts per 100 datasets; observed = SMC-BVS v3 HPM)

| p | S | **observed** miss (extra/missed/mixed) | realised on study y (extra/missed/mixed) | MC P(miss) (extra/missed/mixed) | MC P(L) one-move | **T2** (add / drop+swap) | T1 indep. | T1-lo | z(obs vs T2) | z(obs vs MC) | Le Cam floor |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 500 | S1 | **21** (13/6/2) | 20 (12/6/2) | 21.9 (12.6/7.6/1.7) | 21.6 | **21.5** (12.6 / 9.9) | 31.3 | 11.4 | -0.1 | -0.2 | 0.4 |
| 500 | S2 | **16** (9/7/0) | 16 (9/7/0) | 22.4 (12.6/7.0/2.8) | 22.2 | **22.6** (12.7 / 11.2) | 33.1 | 11.6 | -1.6 | -1.5 | 1.2 |
| 500 | S3 | **36** (11/7/18) | 36 (11/7/18) | 31.5 (9.6/6.4/15.5) | 31.4 | **34.7** (12.7 / 25.0) | 44.6 | 13.1 | +0.3 | +1.0 | 3.4 |
| 500 | S4 | **75** (5/5/65) | 75 (5/5/65) | 65.3 (3.2/3.5/58.6) | 65.3 | **73.2** (12.7 / 69.3) | 78.1 | 31.0 | +0.4 | +2.1 | 9.1 |
| 500 | S5 | **41** (6/18/17) | 40 (5/18/17) | 49.0 (7.7/24.2/17.1) | 48.0 | **52.4** (13.5 / 44.5) | 84.2 | 35.7 | -2.3 | -1.6 | 3.8 |
| 500 | S6 | **41** (6/6/29) | 40 (7/6/27) | 40.0 (7.4/4.7/27.8) | 39.9 | **46.3** (12.6 / 38.4) | 55.0 | 15.2 | -1.1 | +0.2 | 6.4 |
| 1000 | S1 | **29** (10/16/3) | 28 (9/17/2) | 24.4 (11.9/10.5/2.0) | 24.1 | **25.0** (12.4 / 14.1) | 43.3 | 15.3 | +0.9 | +1.1 | 0.4 |
| 1000 | S2 | **25** (12/11/2) | 25 (12/11/2) | 25.8 (11.5/11.2/3.0) | 25.6 | **26.0** (12.4 / 15.2) | 44.6 | 15.5 | -0.2 | -0.2 | 1.2 |
| 1000 | S3 | **33** (7/14/12) | 33 (6/15/12) | 33.4 (9.2/8.5/15.7) | 33.2 | **37.1** (12.4 / 28.0) | 54.1 | 16.8 | -0.9 | -0.1 | 3.5 |
| 1000 | S4 | **65** (3/3/59) | 64 (3/4/57) | 65.1 (3.8/4.4/56.9) | 65.0 | **74.5** (12.4 / 70.8) | 82.3 | 31.4 | -2.2 | -0.0 | 9.2 |
| 1000 | S5 | **68** (10/31/26) | 68 (11/32/25) | 56.9 (7.0/31.4/18.6) | 55.8 | **59.4** (13.3 / 52.6) | 95.0 | 44.4 | +1.8 | +2.4 | 3.9 |
| 1000 | S6 | **39** (5/9/25) | 39 (5/9/25) | 43.5 (7.5/7.7/28.4) | 43.5 | **49.1** (12.4 / 41.8) | 63.3 | 17.6 | -2.0 | -0.9 | 6.6 |
| 500 | sum (6 cells) | **230** | 227 | 230 | 228 | **251** | 326 | 118 | | | |
| 1000 | sum (6 cells) | **259** | 257 | 249 | 247 | **271** | 383 | 141 | | | |

RMS z (obs vs T2) = 1.38; RMS z (obs vs MC) = 1.22 over 12 cells.

### 4.3 What the tables show

1. **The observed miss counts match the one-move posterior misses.** The realised check on the study's own y reproduces the observed SMC-BVS count in every one of the 24 (p, S, c) cells to within ±1 (the type split to within ±2). The totals are 39 / 37 at c = 1 (observed 40 / 37) and 227 / 257 at c = 0.5 (observed 230 / 259). Per-dataset SMC outputs are not on the laptop, so this is a match of counts per cell, not of datasets one by one. Still, ±1 in all 24 cells leaves little room: the observed miss rate is, to within the noise, the posterior quantity P(L | X), and the targets of the theory are the right ones.
2. **Multi-move events add almost nothing.** MC P(L) and MC P(miss) (one move or a double drop) differ by at most 1.1 points (p = 1000, S5, c = 0.5).
3. **c = 1: the theory predicts the rate and the type.**
   - T2 gives 43 / 40 misses per 600 against 40 / 37 observed (MC 41 / 38), and every cell agrees within |z| ≤ 1.9.
   - The prediction is ≈ 6–7 % supersets in every scenario, plus ≈ 1.5 % swaps in S4 only. The observed counts are extra-only everywhere, with mixed only in S4 (4 and 3).
   - S5's higher superset rate (8.5 % predicted, 10 and 13 observed) is the ω₀ effect of Cor. 2.1. In S5, Var(xᵀβ) = Σβ² + 0.3((Σβ)² − Σβ²) = 17.4 instead of 24.6, so ω₀ ≈ 17.6 instead of ≈ 25, and the add threshold is lower.
4. **c = 0.5: T2 tracks the scenario ranking and the level; T1 does not.**
   - The ranking is S4 ≫ S5 > S6 ≈ S3 > S1 ≈ S2.
   - T2 gives 251 / 271 against 230 / 259 observed (MC 230 / 249): T2 is within −0.4 to +9.4 points of the exact MC per cell, most in S4 and S6. The RMS z of the observed counts is 1.38 against T2 and 1.22 against the exact MC. The MC's own excess over 1 is ordinary design-level dispersion; the largest deviation is +2.4 at p = 1000, S5.
   - T1 overshoots by 40–50 % (326 / 383), and T1-lo undershoots by half (118 / 141). T2's residual overshoot most plausibly comes from approximation (a) of Prop. 6 (not isolated numerically): the Z_{jl} of a truth's group-mates are positively correlated, so the union over l is smaller than under independence.
5. **The type split at c = 0.5 follows from the analysis.**
   - The probability of some add event stays at 12.4–13.5 % in every scenario (T2_add, Cor. 2.1). They appear as extra-only only when nothing else goes wrong, hence 3–13 observed.
   - The drop and swap block carries the scenario dependence: in S4 almost everything is a swap (mixed 65 / 59), and in S5 drops of the weak truths add a large missed-only share (18 / 31). Both match the MC split.

### 4.4 Validation of the analytic pieces

- `scripts/test_analytic.py` (rerun on the laptop): P_swap (general λ) against direct MC (400,000 draws), to within 0.001 in all 5 test points. For example, δ = 4, ρ = 0.85, λ = 1.002 gives 0.1160 by quadrature and 0.1163 by MC. P_drop: 0.1995 against 0.1990. P_add: 3.10 × 10⁻⁴ against 2.65 × 10⁻⁴ ± 0.26 × 10⁻⁴ (MC SE), which is 1.7 SE.
- `scripts/check_score_local.py` (laptop): the fast one-move scores against brute-force F_exact on regenerated study data: max |difference| = 8.5 × 10⁻¹³ over 60 comparisons. The previous run's `check_score.py` also matched the engine's logged F(S₀) on the server. The agreement of the realised misses with the observed SMC misses (§4.3(1)) is an end-to-end check of the score, the data port and the standardisation.

## 5. Why c = 1 gives supersets and c = 0.5 gives swaps and subsets

Each one-move probability is a Gaussian tail evaluated at a threshold set by the prior. The threshold is either fixed (adds, drops) or zero (swaps). The SNR enters only through δ_j (drops and swaps) and ω₀ (adds).

| Event | Governing quantity | c = 1 | c = 0.5 |
|---|---|---|---|
| add a null (Prop. 2, Cor. 2.1) | t_add ≈ √(2κ⁺(1+η)) ≈ 3.7–4.1, p-free family-wise rate | ≈ 7 % per dataset, every scenario | ≈ 14 % (threshold falls because ω₀ falls) |
| drop truth j (Prop. 3) | Φ(t_drop − \|δ_j\|), t_drop ≈ 3.7–4.1 | \|δ_j\| ≥ 11·√(1 − R²_{j\|T_j}) ⇒ ≈ 0 | weakest truths (\|θ\| = 0.4) have \|δ\| ≈ 5.6√(1 − R²) ⇒ a few % each, more where R² is large (S5) |
| swap j → l (Prop. 1) | Φ(−\|δ_j\|√((1−ρ)/2)), **no prior term** | needs ρ ≳ 0.85 and the weakest truth (S4, S5) | d₋ halves, so d₋² falls by 4: a look-alike pair with ρ = 0.85 and \|θ\| = 0.4 gives d₋ ≈ 1.5, about 6–7 % per pair, with 4 group-mates per truth |

So at c = 1, the only event with non-negligible probability in every scenario is the superset. Its rate is set by the BB(1, p) + g = n threshold and is scenario-free, which is what the observed extra-only counts show (3–6 per 100 everywhere except S5). At c = 0.5 the superset rate only doubles, but the swap and drop probabilities, which are exponential in δ², grow by orders of magnitude and dominate. This is the observed pattern.

### Connection to T07

Prop. 1 is T07 in quantitative form. In F(S₀ − j + l) − F(S₀) the size prior cancels identically, and the swap probability depends on the prior only through κ_{jl} = ½ log(D_{S₀−j+l}/D_{S₀}) = O(1/n) (|κ_{jl}| ≤ 0.3 nats here). So no size-only prior and no g can move the dominant c = 0.5 failure mode. Prop. 5 adds that **no selector at all** can push the two-point averaged swap error much below the HPM's own: the exponents are δ²(1−ρ²)/8 against δ²(1−ρ)/4, whose ratio (1+ρ)/2 is 0.93 at ρ = 0.85. The per-design Le Cam floor max_{(j,l)} Φ(−|δ_j|√(1−ρ²_{jl})/2) is reported in §4: ≤ 0.4 % at c = 1 and up to ≈ 9 % (S4) at c = 0.5. It is a **pairwise** floor and lies far below the whole-model miss rate. A whole-model floor (Assouad/Fano over the 14 truths and their look-alikes) is OPEN.

### SuSiE and SSL: only what the theory supports

The theory **does** support the following:
1. **At c = 1 the HPM's misses are prior-driven supersets, and a selector with a higher effective inclusion threshold avoids them for free.** Every truth has |δ_j| ≥ 11·√(1 − R²) ≳ 8 at c = 1. A selector that admits a null only when its standardised partial score exceeds t′ has superset rate ≈ (p − s₀)·2Φ̄(t′) and drop rate ≈ Φ(t′ − |δ|_min). For t′ between ≈ 4.5 and ≈ 6, both are below 1 %. The HPM's t_add ≈ 3.9 sits at a 7 % superset rate.
2. **At c = 0.5 the same higher threshold costs subset misses.** The weakest truths have |δ| ≈ 5.6 (less in S5). The drop rate Φ(t′ − 5.6) is 16 % at t′ = 4.6 and 50 % at t′ = 5.6 per weak truth, against ≈ 4–8 % at t_drop ≈ 3.9.
3. **Pairwise swaps have a floor for everyone** (Prop. 5). No method can be uniformly much better than the HPM on S4-type look-alikes.

So "more conservative than BB(1, p) + g = n" is predicted to win at c = 1 and lose at c = 0.5. That is the observed SuSiE and SSL pattern: SuSiE goes from 585/600 to 220/600, SSL from 569 to 303, and SMC-BVS from 559 to 370.

The theory does **not** support the following: that SuSiE's or SSL's effective threshold actually is t′ ≈ 4.5–6. Their thresholds come from SuSiE's estimated prior variance and purity filter, and from SSL's λ₀/θ adaptation, and are not derived here (CONJECTURE). It also does not support any explanation of SuSiE's collapse on S5 at c = 0.5 (3/100 and 0/100). That is plausibly a single-effect/credible-set failure under the global 0.3 equicorrelation, which is outside this score-based theory.

## 6. What fails and why

- **Independence across all one-move events (T1) overshoots at c = 0.5** (§4). For a fixed truth j, the s₀(p − s₀) swap events all share A_j: when A_j comes out low, every swap (j, ·) and the drop of j become likely together. Treating them as independent double-counts. T1 is fine at c = 1, where all events are rare. Prop. 6 / T2 repairs this by conditioning on A_j and E.
- **The cluster-max lower bracket (T1-lo) is far too low** (§4). Inside a truth's cluster the events are not perfectly dependent: different group-mates l compete through independent Z_{jl}.
- **A rigorous upper bound via Šidák or Royen's Gaussian correlation inequality was not obtained.** The swap slabs {|ρA + sZ| ≤ |A|} are not centred in Z, and in the add block E is a function of the same residual vector as the B_l. The natural route (spherical decomposition ε̃ = RΘ) leaves slabs on a sphere, where neither inequality applies directly. OPEN.
- **The one-move event L is only a lower bound for P(S₀ ≠ argmax F)** (Thm 4). The runner also checks the 91 double drops. In the MC, the event "L or double drop" exceeds P(L) by at most about 1 point per cell (S5, c = 0.5). The realised check on the study's own y (one move + double drop + hill-climb) reproduces the observed SMC miss counts (§4). Together these show that the missing multi-move terms are negligible here. That is empirical, not a theorem.
- **The previous O-SWAP run's cell runner (`run_cells.py`) needs the server's `.rds` files.** It is superseded on the laptop by `rgen.py` + `run_local.py`. These regenerate every dataset from the R generator with R's own RNG, ported exactly (validated against R's `set.seed(1); rnorm(5)` and `set.seed(42); rnorm(3)`, and indirectly by the exact match of the realised miss counts).

## 7. Needs escalation

1. **Prop. 1, step 2** (the decomposition of Q̃_{T+k} through the 2-dimensional projection v), and the general-λ quadratic in `analytic.py::p_swap`: an independent line-by-line check. The quadrature was validated against direct MC to 3 decimals, but the algebra deserves a second reader.
2. **A rigorous version of T2.** Either an inequality (upper and lower brackets) that controls the cross-l dependence of the Z_{jl}, which are correlated through the partial correlations of the nulls given S₀ − j, or a Bonferroni–Hunter second-order bracket computed per design. The reward is a proved two-sided bracket on P(L | X) at c = 0.5.
3. **The PA error.** Lemma 0 gives a deterministic bound, but turning it into a bound on the change of the miss *probability* needs a margin (anti-concentration) argument for the score gap at 0. That is routine but unwritten.
4. **The SuSiE/SSL thresholds.** Deriving the effective inclusion thresholds of SuSiE (with estimated prior variance and purity filter) and of SSL (adaptive λ₀, θ) at n = 200 would turn the CONJECTURE of §5 into a statement.

## 8. Outside scope

- **SuSiE's S5 collapse at c = 0.5** (3/100 at p = 500 and 0/100 at p = 1000 exact). The score theory here says nothing about it, and it is probably a credible-set purity issue under global equicorrelation.
- **The HPM delivers what the posterior says.** Because the realised one-move check reproduces the observed SMC miss counts in all 24 cells (to within ±1), the observed miss rates are, to within noise, a property of the **posterior** (the g = n, τ = 1, BB(1, p) score) alone, not of the search. This is consistent with §5 of `THEORY_PRIORITIES.md` ("0 search misses"), and it means T38/T21's discovery term contributes nothing at n = 200 for these cells. A natural target for T03/T02: report "P(posterior miss)" as a named quantity predicted by Props 1–3.
- **The τ = 1 pseudo-observation acts as an SNR-dependent size penalty** (Prop. 2 / Cor. 2.1): stronger signals make the posterior more reluctant to add a null. This is a property of the method's prior, worth a remark in the methodology paper.

## 9. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change needed? |
|---|---|---|---|---|---|
| Swap probability (goal 1) | Prop. 1: exact Gaussian event in (A, B), with closed form Φ(−d₋)Φ(d₊) + Φ(d₋)Φ(−d₊) at λ = 1 and an exact general-λ quadrature. PROVED under PA. | high | done; second reader wanted (§7.1) | the 2-dimensional projection decomposition of Q̃ | no |
| Superset and subset (goal 2) | Props 2, 3 + Cor. 2.1: exact χ²₁/χ² events; the add threshold is ≈ √(2κ⁺(1+η)) and p-free, and falls as the SNR falls. PROVED under PA; Cor. 2.1 is a PROOF SKETCH | high | high | the role of ω₀ (the τ = 1 pseudo-observation) | no |
| Cluster dependence | Prop. 6: B_{jl} = ρA_j + √(1−ρ²)Z_{jl}, Z central and independent of A_j. PROVED | high | done | — | no |
| Combined prediction (goal 3) | T2 predicts P(posterior miss) per cell: within 2 points at c = 1, and +0 to +9 points vs the exact MC at c = 0.5. Approximation; a rigorous two-sided bracket is OPEN | medium-high (as an approximation) | medium (bracket) | dependence of the Z_{jl} across l; E shared with the B_l | no |
| Prediction vs observed (goal 4) | The observed SMC miss count equals the realised one-move posterior-miss count in all 24 cells (±1); the exact-score MC matches observed with RMS z = 0.93 (c = 1) and 1.22 (c = 0.5). Empirical | high | n/a (empirical) | per-dataset SMC outputs would confirm one by one | no |
| T07 link (goal 5) | The size prior cancels in every within-size swap, and g enters only through κ_{jl} = O(1/n). The Le Cam two-point floor is within a factor (1+ρ)/2 in the exponent of the HPM's own pairwise swap error. PROVED (pairwise) | high | a whole-model floor (Assouad over the 14 truths) is OPEN, medium | multi-hypothesis lower bound | no |
| SuSiE / SSL (goal 5) | A higher effective inclusion threshold wins at c = 1 (supersets are free to remove) and loses at c = 0.5 (weak-truth drops). CONJECTURE: their actual thresholds are not derived | medium | low-medium | the effective thresholds of SuSiE and SSL at n = 200 | — |

