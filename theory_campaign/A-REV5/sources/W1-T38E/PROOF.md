# W1-T38E — PROOF.md (delivery, eligibility, composition of T38(b))

Notation of `Docs/Theory/theorems/00_COMMON.md`. All results are **candidates pending cross-family review**. Status words: PROVED (checked line by line by this run), PROOF SKETCH, COUNTEREXAMPLE, CONJECTURE, OPEN.

Additional notation used throughout.
- γ₁ := γ₀e^{d} = ϖ·BF (∝ π). Since γ_φ = γ₀e^{φd}, **γ_φ = γ₀^{1−φ}γ₁^{φ}** for every real φ.
- For S ∈ Ω: U(S) = S ∩ S₀ (true content), N(S) = |S ∖ S₀| (number of extras). Then 𝓡_d = {S ∈ Ω : N(S) ≤ d}.
- Flip neighbour S⊕l := S Δ {l}; a flip is feasible if S⊕l ∈ Ω. Endpoint flip odds κ_i(S,l) := γ_i(S⊕l)/γ_i(S), i ∈ {0,1} (0 if infeasible).
- Affinity aff_φ := Σ_Ω π₀(S)^{1−φ}π(S)^{φ} (so Z̄_φ = Z̄₀^{1−φ}Z̄₁^{φ}·aff_φ).
- 𝒮 is the method's scored set; with the LS0 tweak, 𝒮⁺ = 𝒮 ∪ 𝒮_{LS0}. U = "no usable HPM output".

---

## 1. Lemma A (log-linear odds domination) — PROVED

**Statement.** For S, S′ ∈ Ω and φ ∈ [0,1]: γ_φ(S′)/γ_φ(S) = ρ₀^{1−φ}ρ₁^{φ} ≤ max(ρ₀, ρ₁), ρ_i := γ_i(S′)/γ_i(S). In particular the probability that the Gibbs update of coordinate l, executed at state S at temperature φ, changes the state is at most κ_φ(S,l) := γ_φ(S⊕l)/γ_φ(S) ≤ max{κ₀(S,l), κ₁(S,l)}, uniformly in φ ∈ [0,1].

**Proof.** The identity is γ_φ = γ₀^{1−φ}γ₁^{φ}. For a,b > 0 and φ ∈ [0,1], a^{1−φ}b^{φ} ≤ max(a,b) (weighted geometric ≤ max). Gibbs (M §6.5; engine `step_gibbs`): o_l = a/(1+a), a = γ_φ(S∪l)/γ_φ(S∖l), and o_l = 0 when the addition is infeasible. If l ∉ S and the addition is feasible, the change probability is o_l = a/(1+a) ≤ a = κ_φ(S,l). If l ∈ S, it is 1 − o_l = 1/(1+a) ≤ 1/a = γ_φ(S∖l)/γ_φ(S) = κ_φ(S,l). If the addition is infeasible, the change probability is 0. ∎

*Use.* Any bound on a Gibbs departure or leakage sum at the two endpoints transfers to every temperature of the bridge. It does **not** transfer non-Gibbs acceptances, and it is useless whenever one endpoint odds is huge (for example a proxy of a missing true variable at φ = 1). See §4 for how D2 avoids this.

---

## 2. Bridge mass on 𝓡_d (the T22(iv) question)

### 2.1 COUNTEREXAMPLE C0: the endpoint bound does not transfer to sets
T22(iv) gives inf_φ q_φ(S₀) ≥ min{π₀(S₀), π(S₀)} for the **singleton**. The set analogue inf_φ q_φ(A) ≥ min{π₀(A), π(A)} is false. Take three states a₁, a₂, o with A = {a₁, a₂}, log γ₀ = (0, −30, −5), log γ₁ = (−30, 0, −5). Then q₀(A) = q₁(A) = 0.9933 but q_{1/2}(A) = 9.1·10⁻⁵ (`scripts/toys_C0_C1.py`, output `toys_C0_C1.out`). The reason: q_φ(A^c)/q_φ(A) has a Hölder-bounded numerator but a denominator Σ_A γ₀^{1−φ}γ₁^{φ} that is not bounded below by the endpoints when γ₀ and γ₁ put their A-mass on different states. That is exactly the masked situation (γ₀ on S°, γ₁ on S₀).

### 2.2 Lemma B (structured bridge mass on 𝓡_d) — PROVED (deterministic)

**Statement.** Fix integers 0 ≤ d < m, states x, y ∈ Ω, and a partition 2^{S₀} = 𝒰_good ⊔ 𝒰_bad. For U ∈ 𝒰_good and k ≥ 0 put
Λ_k^U := max{ Σ_{l ∉ S₀ ∪ T, T+l ∈ Ω} max(κ₀(T,l), κ₁(T,l)) : U(T) = U, N(T) = k },
θ := max_{U ∈ 𝒰_good} max_{d ≤ k < m} Λ_k^U/(k+1), and 𝔅 := {S : N(S) > m} ∪ {S : U(S) ∈ 𝒰_bad, N(S) > d}.
If θ < 1, then for every φ ∈ [0,1]:
  q_φ(𝓡_d^c) ≤ θ/(1−θ) + max{π₀(𝔅), π(𝔅)} / [min{π₀(x), π(y)} · max{π(x), π₀(y)}].

**Proof.** *Peeling inside a good class.* Fix U ∈ 𝒰_good and let M_k := Σ_{S: U(S)=U, N(S)=k} γ_φ(S). Each S with U(S) = U, N(S) = k+1 equals T + l with U(T) = U, N(T) = k, l ∈ S∖S₀, in exactly k+1 ways, and T + l ∈ Ω. Hence M_{k+1} = (k+1)⁻¹ Σ_T Σ_l γ_φ(T+l) ≤ (k+1)⁻¹ Σ_T γ_φ(T) Σ_l max(κ₀,κ₁)(T,l) ≤ (Λ_k^U/(k+1)) M_k ≤ θ M_k for d ≤ k < m, by Lemma A. So Σ_{k=d+1}^{m} M_k ≤ M_d(θ + θ² + …) ≤ θ M_d/(1−θ). Summing over good U and dividing by Z̄_φ: q_φ(good, d < N ≤ m) ≤ θ/(1−θ) · q_φ(N = d) ≤ θ/(1−θ).
*Remaining part.* 𝓡_d^c ∖ (good, d < N ≤ m) ⊆ 𝔅. By Hölder, Σ_𝔅 π₀^{1−φ}π^{φ} ≤ π₀(𝔅)^{1−φ}π(𝔅)^{φ} ≤ max{π₀(𝔅), π(𝔅)}, so q_φ(𝔅) = Σ_𝔅 π₀^{1−φ}π^{φ}/aff_φ ≤ max{π₀(𝔅),π(𝔅)}/aff_φ.
*Affinity.* aff_φ ≥ π₀(x)^{1−φ}π(x)^{φ} and aff_φ ≥ π₀(y)^{1−φ}π(y)^{φ}. With α = π₀(x), u = π(x), v = π₀(y), β = π(y), all in [0,1]: α^{1−φ} ≥ α ≥ min(α,β), u^{φ} ≥ u, v^{1−φ} ≥ v, β^{φ} ≥ β ≥ min(α,β). Hence aff_φ ≥ min(α,β)·max(u,v). ∎

**Asymptotic reading (PROOF SKETCH, not used by the composition theorem).** Take x = S° (start reference), y = S₀, 𝒰_bad = the true contents U that admit proxies at φ = 1. Under T27(i), π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}, so the denominator is ≥ c₀·n^{−c(A+½)}e^{−O_P(1)}. T02(i) gives π(N > m) ≤ 2^{−m}·poly(n), and T03 makes π(bad U) tiny. A start-side extras tail π₀(N > d, bad U) ≤ n^{−κ(d+1)} (a T22(i)-type generating-function consequence; **not proved here**) then requires **d + 1 > c(A+½)/κ**: d must grow with the masking depth c. θ → 0 needs NL_avg/TL_avg-type leakage averages uniformly over good classes with ≤ m_n extras.

**What Lemma B does not do.** It is a statement about the target laws q_φ, not about particles. §5 shows that start mass plus uniform bridge mass on A plus zero exits still allow every particle of A to die.

---

## 3. Lemma S (ESS share lemma) — PROVED

**Statement.** Let w₁,…,w_H > 0 have population ESS (Σw)²/Σw² ≥ eH, with e ∈ (0,1]. For any index set A with |A| = fH:
  ω(A) := Σ_A w/Σ w ≥ f − √(f(1−f)(1/e − 1)).
The bound is attained by two-level weights.

**Proof.** Normalise w̄_i = w_i/mean(w). Then mean(w̄) = 1 and mean(w̄²) ≤ 1/e, so Σ_i(w̄_i − 1)² ≤ H(1/e − 1) =: Hc. Let a = Σ_A(w̄−1)² and b = Σ_{A^c}(w̄−1)², so a + b ≤ Hc. Since Σ_A(w̄−1) = −Σ_{A^c}(w̄−1), Cauchy–Schwarz gives |Σ_A(w̄−1)| ≤ min{√(fH·a), √((1−f)H·b)}. The minimum of the two is largest under a + b = Hc when f·a = (1−f)·b, giving the value H√(f(1−f)c). Hence ω(A) = H⁻¹Σ_A w̄ = f + H⁻¹Σ_A(w̄−1) ≥ f − √(f(1−f)c). For tightness, take w̄ = 1 − √c√((1−f)/f) on A and 1 + √c√(f/(1−f)) off A. ∎
With e = 0.9 (the pilot threshold), g(f) := f − √(f(1−f))/3 is > 0 iff f > 1/10, and is increasing on [1/10, 1) (g′ is increasing and g′(0.1) = 5/9). Checked on 200,000 random cases (worst slack −1.1·10⁻¹³) and on the tight two-level cases (`scripts/share_lemma_check.py`).

**Companion facts used in D2.**
(i) Population ESS is non-increasing in φ ≥ 0: d/dφ log[(Σe^{φd})²/Σe^{2φd}] = 2E_φ[d] − 2E_{2φ}[d] ≤ 0, since the tilted mean is non-decreasing in the tilt.
(ii) Kantorovich: if w_i ∈ [m, M] then ESS/H ≥ 4mM/(m+M)². This is ≥ 0.9 when M/m ≤ 1.925.

---

## 4. Theorem D2 (pilot one-flip Gibbs discovery: delivery without terminal rounds) — PROVED

**Setting.** SMC branch, tier-0 pilot (stream 0) with H = H₀ particles; each pilot stage reweights by e^{(φ′−φ)d}, resamples multinomially and runs one round at φ′. The first temperature φ₁ follows `pilot_next_phi` (φ₁ = 1 if that passes ESS ≥ 0.9H; otherwise bisection; forced floor step to 1/T_e). Verified in `Scripts/SMC_BVS/core/cpp/v3_engine.h` (`run_island_s`) and `v3_calib.h`. Assumptions: EX-A, EX-S, **SR** (both Gibbs configurations scored; engine `step_gibbs` evaluates and records the flipped configuration).

**Hypotheses.**
- (D2-a) *one-flip reference:* x° ∈ Ω with x° Δ S₀ = {j}. If x° = S₀ − j, then s₀ ≤ K.
- (D2-b) *start mass:* π₀(x°) ≥ b with b > 1/10.
- (D2-c) *stability off a bounded set:* a data-measurable 𝒟 ⊆ [p]∖{j} with |𝒟| ≤ k_D, and Dep := Σ_{l ∉ 𝒟 ∪ {j}} max{κ₀(x°,l), κ₁(x°,l)}.
- (D2-d) *no first-stage blow-up:* on the initial pilot population, either S₀ is among the draws, or max_i d(X_i) − min_i d(X_i) ≤ T_e·log 1.925; call the failure event NB^c.

**Conclusion.** For every t ∈ (0, b − 1/10), with β := (1 − Dep)₊/(k_D + B + 3):
  P(S₀ ∉ 𝒮_cal | data) ≤ e^{−2Ht²} + P(NB^c | data) + exp{−H β g(b − t)}.

**Proof.**
1. *Initial fraction.* Let X₁,…,X_H be the iid π₀ initial draws (T09(i)) and f̂ the fraction equal to x°. Hoeffding: P(f̂ < b − t) ≤ e^{−2Ht²}. If S₀ is among the initial draws it is scored (initial draws are scored), so assume not.
2. *First-step ESS.* On NB, the weights e^{φd(X_i)} at φ = 1/T_e have ratio max/min ≤ 1.925, so ESS(1/T_e) ≥ 0.9H by Lemma S(ii). By monotonicity (Lemma S(i)), ESS(φ) ≥ 0.9H for every φ ≤ 1/T_e. The rule then yields φ₁ with ESS(φ₁) ≥ 0.9H in every branch. If φ₁ = 1 this is by the first test. If the bisection is not forced, lo passes by construction. If it is forced, φ₁ = 1/T_e, which passes on NB.
3. *Share.* On NB ∩ {f̂ ≥ b − t}, Lemma S with e = 0.9 gives a weighted share ω of x° of at least g(f̂) ≥ g(b − t) > 0, because g is increasing on [1/10,1) and b − t > 1/10.
4. *Resampling.* Given the weighted population, the number M of resampled particles at x° is Binomial(H, ω).
5. *One round from x°.* Fix a resampled particle at x°. Its round order is uniform and independent of its state and of all other randomness (EX-S, fresh per particle). Let O be the event that label j (Gibbs coordinate j) precedes every label in 𝒟 and every one of the B+2 non-Gibbs labels; P(O) = 1/(|𝒟| + B + 3) ≥ 1/(k_D + B + 3). On O, every label executed before j is a Gibbs label l ∉ 𝒟 ∪ {j}. Until the first change the state is x°, so the probability that the i-th such label is the first change is at most κ_φ₁(x°, l_i) ≤ max(κ₀,κ₁)(x°, l_i) by Lemma A (each label executes once, with a fresh uniform). A union bound gives P(change before j | order ∈ O) ≤ Dep. On O ∩ {no change}, the update of j executes at X = x°, and under SR the engine evaluates x° ⊕ j = S₀ (feasible by D2-a). So P(S₀ scored in this round) ≥ P(O)(1 − Dep)₊ ≥ β, uniformly in φ₁ ∈ [0,1].
6. *Independence across particles.* Given the resampled population, the particles' rounds use independent uniforms. So P(no particle scores S₀ | ω) ≤ E[(1−β)^M | ω] = (1 − βω)^H ≤ e^{−Hβω} ≤ exp{−Hβ g(b−t)}.
Adding the excluded events gives the bound. ∎

**Corollary D2-∞ (PROVED given the hypotheses).** Along R1/R4: if b > 1/10 is fixed, k_D and B are bounded (B ≤ 16), Dep ≤ 1 − c₁ < 1 w.p. → 1, and P(NB^c) → 0, then P(S₀ ∉ 𝒮_cal) → 0. The reason is H = H₀ = ⌈512N₀/2500⌉ ≥ 0.2·max(n,p) → ∞ (take t = (b − 1/10)/2). No final-run, delivery, launch or repair hypothesis is used, and S₀ ∈ 𝒮_cal ⊆ 𝒮.

*Remarks.* (1) 𝒟 absorbs the proxies of the missing variable (in CF1, the B−1 copies of x₂), whose φ = 1 odds are e^{Θ(n)}. Lemma A is applied only off 𝒟. (2) D2 needs Gibbs distance 1. For distance ≥ 2 the intermediate addition has odds ≈ n^{−1/2}/p at small φ, so a crossing temperature must first be reached. That is the genuine delivery problem of §5. (3) Numerically (`cf_family.out`), CF1 has Dep = 0.091 at n = 400 (|𝒟| = 8, β ≥ 0.045, share ≥ 0.84, bound 3·10⁻⁹) and Dep = 0.049 at n = 1600 (bound 1·10⁻⁶).

---

## 5. General delivery to the terminal rounds

### 5.1 Theorem D1 (T15 route) — PROVED (from locked T15)
Conditional on a successful 𝓒, for island r, a recording position τ covered by T12(i) (end of stage T or a fixed terminal prefix), and every c ∈ (0,1):
  P_𝓒(no particle of island r in 𝓡_d at τ) ≤ π(𝓡_d^c)/c + P_𝓒(Ẑ_r/Z < c).
*Proof.* On the event, f_r(𝓡_d^c) = 1 > u for every u < 1. T15 gives P(f_r > u) ≤ π(𝓡_d^c)/(cu) + P(Ẑ_r/Z < c); let u ↑ 1. ∎
T03 gives π(𝓡_d^c) ≤ 1 − π(S₀) → 0, so delivery follows from an **islandwise evidence lower tail** LT: P_𝓒(Ẑ_r/Z < c) → 0 for one c and one island.

**Why this route is not viable in the masked regime (COUNTEREXAMPLE C1 below).** LT fails whenever the particles cross from the S°-region to S₀ late in the bridge. The evidence increments are then computed on S°-particles, and Ẑ_r/Z ≈ e^{−(large)} **even when delivery and the HPM succeed**. In C1 every one of 400 islands had log(Ẑ/Z) ≤ −1800, including the islands in which A survived. LT is sufficient but far from necessary, and it fails exactly in the regime (b) is meant for.

### 5.2 Proposition D3 (forward chain) — PROVED (conditional on SHARE)
Island r of the final run, N = N_e particles, stages t = 1..T, the stage-t round at φ_t (φ_T = 1). A_t := {some particle in 𝓡_d after the stage-t round}; A₀ := {some initial draw in 𝓡_d}.
- (SHARE) P(A_{t−1} ∩ {no stage-t resampled particle in 𝓡_d}) ≤ ζ_t.
- (EXIT-end) sup_{x∈𝓡_d} P_x(one round at φ_t ends outside 𝓡_d) ≤ η_t.
Then P(A_T^c | 𝓒) ≤ (1 − π₀(𝓡_d))^N + Σ_{t=1}^T(ζ_t + η_t).
*Proof.* A_T^c ⊆ A₀^c ∪ ⋃_t (A_{t−1} ∩ A_t^c). On A_{t−1} ∩ A_t^c, either no resampled particle lies in 𝓡_d (probability ≤ ζ_t), or the smallest-index resampled particle in 𝓡_d (measurable w.r.t. the resampled population) ends its round outside. That has conditional probability ≤ η_t because its round uses fresh randomness. P(A₀^c) = (1−π₀(𝓡_d))^N by iid start draws (T09(i), T11(iii)-type). ∎
EXIT-end is weaker than T24's first-exit η_n (only end-of-round membership matters). Lemma A reduces its Gibbs part to endpoint odds, except for proxy labels, where the actual-φ odds must be used.

### 5.3 COUNTEREXAMPLE C1 (SHARE cannot be dropped) — reproducible
Abstract four-state SMC (not a BVS instance): A = {a₁, m, a₂} plays 𝓡_d and o lies outside, with log γ₀ = (0, −120, −55.2, −10) and log γ₁ = (−2000, −2000, 0, −1930). Metropolis on the path a₁–m–a₂ under γ_φ; o isolated, so **zero exits from A**. Then:
- π₀(A) = 0.99995;
- π(A) = 1 − 10⁻⁸³⁸;
- sup_φ q_φ(A^c) = 3.3·10⁻⁴ (uniform bridge mass on A ≥ 0.9997);
- d(o) − d(a₁) = 80.
With multinomial resampling, T = 1000 uniform stages and 9 terminal rounds, the fraction of islands with **no particle in A** at the end was 0.480 (N = 10⁵) and 0.995 (N = 10⁶), out of R = 200 each (seed 20261102). Mechanism: the few initial o-copies (π₀(o) = 4.5·10⁻⁵) gain e^{80φ} over a₁ by selection before the A-internal kernel can carry a₁ to a₂ (possible only near φ = 1). The larger N makes extinction of A *more* likely, because it makes survival of an o-lineage more likely.
**Consequence.** Start mass on 𝓡_d, uniform bridge mass on 𝓡_d (Lemma B) and exit control (T24's η) do **not** imply delivery. A particle-level hypothesis (SHARE, or LT) or a structural no-fitter-outsider condition is necessary. Whether a BVS design realises C1's structure (an outside-𝓡_d state with start mass ≳ 1/N whose discrepancy exceeds that of the start reference by ≫ log N, yet negligible bridge mass) is OPEN.

---

## 6. Local-search eligibility (Task 2)

### 6.1 Proposition E1 (the sufficient condition F(S°) > sup_{𝓡_d^c} F fails under omission masking) — PROVED (deterministic part)
For every S ∈ Ω and P ⊆ S^c with |S ∪ P| ≤ K: F(S∪P) − F(S) ≥ −|P|·[log(2p) + ½ log(n+1)].
*Proof.* (a) Q_S = min_β{‖y − X_Sβ‖² + (‖X_Sβ‖² + ‖β‖²)/n}: the stationarity equation gives ((n+1)G_S + I)β = nz_S, so β̂ = nH_S⁻¹z_S, and the minimum is yᵀy − nz_SᵀH_S⁻¹z_S. Restricting β_P = 0 shows Q_{S∪P} ≤ Q_S, so −ν log(2b₀+Q) does not decrease. (b) Adding one column l: by Woodbury, det H ratio = 1 + (n+1)a and det(G+I) ratio = 1 + b, with a = x_lᵀ(I + (n+1)X_SX_Sᵀ)⁻¹x_l ≤ b = x_lᵀ(I + X_SX_Sᵀ)⁻¹x_l. So D_{S+l}/D_S = (1+(n+1)a)/(1+b) ≤ (1+(n+1)b)/(1+b) ≤ n+1. Iterating gives D_{S∪P}/D_S ≤ (n+1)^{|P|}. (c) w(k+1)/w(k) = (k+1)/(2p−1−k) ≥ 1/(2p). ∎
Apply this with S = S₀ and any P of d+1 extras. Every S₀ ∪ P ∉ 𝓡_d has F(S₀∪P) ≥ F(S₀) − κ_n(d), with κ_n(d) := (d+1)[log 2p + ½ log(n+1)] = O(log n). Hence **F(S₀) − F(S°) > κ_n(d) ⇒ ∃ S ∉ 𝓡_d with F(S) > F(S°)**.
When S° ⊉ S₀ omits a true variable, T03-type margins (BM-∞, SE) give F(S₀) − F(S°) ≫ log n w.p. → 1 (PROOF SKETCH; numerically 44.5 vs κ = 16.4 at n = 400 and 180 vs 30 at n = 1600 in CF2, `cf_extra.out`). So the sufficient condition proposed in the brief **fails w.p. → 1 in omission-type (T27) masking**. Without LS0, eligibility of the best-scored model then depends on which outside states the sampler happens to score, a dynamic property (OPEN). To keep the whole upper level set {F ≥ F(S°)} inside a greedy basin, one would need greedy repair from supersets with Θ(n/log n) extras in strong-signal designs, which exceeds the move budget ℓ_n = O(log n).

### 6.2 Remark E2 (proxy-only masking, S° ⊇ S₀) — PROOF SKETCH
If S° = S₀ ∪ P°, |P°| ≤ d, the per-extra loss from S₀ is between (½ − o(1)) log n (best null, max-selection over p) and (½ + A + o(1)) log n. So {F ≥ F(S°)} ⊆ 𝓡_{d′} with d′ ≈ d(1 + 2A), and greedy deletion repair on 𝓡_{d′} would give eligibility without LS0. Not pursued.

### 6.3 Theorem E3 (LS0 eligibility) — PROVED
LS0 is the production local search (M §6.10) started from the start mode S̃₀ = argmax π₀; its scores join the HPM. Let 𝔅 ⊆ Ω be any set such that **TD′(𝔅, ℓ)** holds: from every centre c ∈ 𝔅, the production local search (≤ ℓ moves, then one further scan) scores S₀. Then S̃₀ ∈ 𝔅 ⇒ S₀ ∈ 𝒮⁺. Moreover:
(i) if some x° ∈ 𝓡_d has π₀(x°) > ½, then S̃₀ = x° ∈ 𝓡_d (no other state can have mass ≥ ½, so there are no ties);
(ii) T22(i) for the reference x° gives π₀(x°) ≥ (1−q_n)^{s+1}/(1+e_n)^s, so (i) holds whenever this exceeds ½;
(iii) under T27's H3 with c₀ > ½ and S^{(0)} ⊆ S₀, (i) holds with x° = S^{(0)} ∈ 𝓡₀.
*Proof.* The search is deterministic given the data, and every scanned model is scored. (i) follows from Σπ₀ = 1. (ii) and (iii) are substitutions. ∎
**Computability.** S̃₀ is computed exactly by max-plus convolution: for each block and size, take the best log r_b; then do a DP over blocks for the total size k, add log w(k), and maximise over k. This costs O(J·K·B) after the tables (implemented in `cf_family.py`). **Cost of LS0:** at most (ℓ+1)·max_{k≤K}[p + k(p−k)] scores. That is not "≈ ℓp": each scan includes k(p−k) swaps.
**Move budget.** TD′ needs a greedy path of length ≤ ℓ+1 (the final scan scores a flip neighbour). T37's own claim requires ℓ ≥ |S Δ S₀| for *certification*, but only ℓ + 1 for *scoring*. In the masked T27 case the relevant length is |S̃₀ Δ S₀| = c (fixed), not s₀ + d. The risk "ℓ_n < s₀ + d at n = 200" therefore applies only to worst-case centres.

### 6.4 Finding on T37's TD(d,0) — COUNTEREXAMPLE (reproducible)
In CF1 (n = 400 and 1600), TD(1,0) **as worded in T37** fails at 248/352 and 728/1004 states of 𝓡₁ (margin −7.5 and −9.2 nats); in CF2 TD(2,0) fails at 26,019/29,936 states. At S = U ∪ {proxy of a missing truth j}, the swap proxy→j beats the plain addition of j by the deletion gain of the useless proxy, ≈ ½ log n + log p. That gap grows with n, so TD(d,0) fails with probability → 1, not merely at finite n. Greedy still progresses. GP(d) (the best move improves F, stays in 𝓡_d and reduces |S Δ S₀|) holds in all states for d ≤ 1. For d = 2 it fails at 4 states, where two proxies jointly replace x₃ and the greedy *deletes the true* x₃. All 4 still reach S₀ in 3 moves (`gp_fail_probe.out`). The correct black-box input is TD′ (reachability within the move budget); GP(d) with ℓ + 1 ≥ s₀ + d is a sufficient condition. TD(d,0) should be replaced. **Escalate to W1-T37R.**

---

## 7. Theorem T38(b)-R (composition) — PROVED given the named inputs

**Setting.** R1/R4 triangular array (s₀ fixed, p_n ≤ n^A, B ≤ 16, K_n = ⌊n/2⌋, v3 budgets indexed by n), EX-A, EX-S, CAL, SR. 𝒮⁺ = 𝒮 ∪ 𝒮_{LS0} when LS0 is used, else 𝒮⁺ = 𝒮. Ŝ⁺ = best model in 𝒮⁺ (method tie rule); Ŝ⁺ = Ŝ without LS0.

**Hypotheses.**
- (H-T03) G, R, SE, BM-C (or BM-∞): δ₁ = 1 − π(S₀) → 0 in P₀-probability (T03(i), locked).
- Discovery route, at least one of:
  - **(b1) LS0 route.** (ELIG) P₀(S̃₀ ∉ 𝔅_n) → 0; (TD′) P₀(TD′(𝔅_n, ℓ_n) fails) → 0. Sufficient: ∃ x° ∈ 𝓡_d with π₀(x°) > ½ w.p. → 1 (T22(i) / T27-H3 with c₀ > ½), and TD′(𝓡_d, ℓ_n) w.p. → 1 (black box from W1-T37R; sufficient GP(d) with ℓ_n + 1 ≥ s₀ + d).
  - **(b1′) pilot one-flip route (original method).** D2's hypotheses w.p. → 1, with P(NB^c) → 0.
  - **(b2) Gibbs-path route.** (DELIV) P(Uᶜ ∩ {no particle of the final run in 𝓡_d after stage T}) → 0, for example by D3 (SHARE, EXIT-end, and E[(1−π₀(𝓡_d))^{N_e}] → 0). (REPAIR(a_n, H)) for every x ∈ 𝓡_d, P_x(no truth score in H = L+4 terminal rounds) ≤ ε_rep(n) → 0 (black box from W1-T24G; T24(ii) form (1−a_n)^H + Hη_n).
- (OP) Operational: LS0, when used, runs whenever output is usable.

**Conclusion.**
  P(U ∪ {Ŝ⁺ ≠ S₀}) ≤ P(U) + 2E₀δ₁ + P(Uᶜ, S₀ ∉ 𝒮⁺),
and the discovery term is bounded:
- in route (b1) by P₀(S̃₀ ∉ 𝔅_n) + P₀(TD′ fails);
- in route (b1′) by D2's bound;
- in route (b2) by P(DELIV fails) + ε_rep.
All three tend to 0, so limsup_n P(U ∪ {Ŝ⁺ ≠ S₀}) ≤ limsup_n P(U), i.e. **liminf_n P(Uᶜ ∩ {Ŝ⁺ = S₀}) ≥ 1 − limsup_n P(U)**. If P(U) → u, then P(Uᶜ, Ŝ⁺ = S₀) → 1 − u. (The brief's "P(Ŝ = S₀) → 1 − limsup P(U)" is not a well-formed limit; this is the correct form.)

**Proof.**
(1) *C1 for any scored set containing S₀.* If π(S₀) > ½ then F(S₀) > F(S) for every S ≠ S₀, so S₀ = S† is the strict global maximiser. On Uᶜ ∩ {S₀ ∈ 𝒮⁺} ∩ {π(S₀) > ½}, the running-best rule over 𝒮⁺ returns S₀ (T11(vii); no tie is possible since the maximum is strict). Therefore U ∪ {Ŝ⁺ ≠ S₀} ⊆ U ∪ {δ₁ ≥ ½} ∪ (Uᶜ ∩ {S₀ ∉ 𝒮⁺}), and Markov gives P(δ₁ ≥ ½) ≤ 2E₀δ₁. Adding LS0 scores cannot hurt: they only enlarge 𝒮⁺.
(2) *Middle term.* δ₁ ∈ [0,1] and δ₁ → 0 in probability, so E₀δ₁ → 0 by bounded convergence.
(3) *(b1).* On {S̃₀ ∈ 𝔅_n} ∩ {TD′(𝔅_n, ℓ_n)}, LS0 scores S₀ deterministically (E3), so {S₀ ∉ 𝒮⁺} ⊆ {S̃₀ ∉ 𝔅_n} ∪ {TD′ fails}.
(4) *(b1′).* S₀ ∈ 𝒮_cal ⊆ 𝒮 ⊆ 𝒮⁺ outside D2's exceptional events.
(5) *(b2).* Condition on the population at the end of stage T. Let ι be the smallest index with X_ι ∈ 𝓡_d, which is measurable. The terminal rounds involve no reweighting and no resampling (engine: L burn-in + 4 measured rounds of `population_round`), so particle ι evolves as the φ = 1 Markov chain from X_ι with fresh randomness. REPAIR gives P(no truth score | ι exists) ≤ ε_rep. Hence P(Uᶜ, S₀ ∉ 𝒮) ≤ P(DELIV fails) + ε_rep. If DELIV is supplied by D3, P(DELIV fails) ≤ E[(1−π₀(𝓡_d))^N] + Σ_t(ζ_t + η_t) on launched runs; non-launch is part of U or must be added as P(Uᶜ, not launched, S₀ ∉ 𝒮_cal).
(6) Combine (1)–(5) and take limsups. ∎

**Corollary (c), cost (PROVED given T32(i), which is itself an unlocked conjecture).** The total number of score evaluations is deterministically bounded by T32(i)'s ceiling, Σ_b 2^{|C_b|} + Σ_{e=0}^{1}(1+4ℓ)H_e[1 + 2m(T_e+L+4)] + 4N₁[1 + 2m(T₁+L+4)] + (8ℓ+3)(ℓ+1)[p + k_*(p−k_*)], plus (ℓ+1)[p + k_*(p−k_*)] for LS0. With N_e ≤ 4(2500 + n + p), T_e ≤ 4·max(1000, ℓ²), m = p + B + 2, ℓ = O(log n) and 2^B ≤ 2^16, this is O((n+p)(p+B)log²n + p²log²n) = poly(n). The brief's form O(N T(p+B+2) + ℓp) omits the scan's k(p−k) swaps and the number of local searches.

---

## 8. Compatibility (Task 4) — explicit family CF(c)

**Construction** (`scripts/cf_family.py`; contrast coordinates; all columns have norm √(n−1)). Let f₁,…,f_{c+1}, e₁,… be orthonormal and orthogonal to 1.
- x₁ = f₁, and x_j = ρf₁ + √(1−ρ²)f_j for j = 2..c+1 (ρ = ½).
- μ = θ₁x₁ + tΣ_{j≥2}x_j with t = −θ₁ρ/(1+(c−1)ρ²), so **x_jᵀμ = 0 exactly** for the c cancelled variables.
- Each true x_j has B−1 copies 0.9x_j + √0.19·e. All other columns are orthonormal nulls.
- p = ⌊n^{3/4}⌋, ε ~ N(0, I), θ₁ = 1.

Complete linkage puts each truth-plus-copies cluster in its own block (verified: "truth-cluster blocks pure: True"). So the cancellation is **cross-block**: the block of x_j sees no marginal signal (T27 H2), while the full posterior needs x_j.

| premise | CF2 (c = 2) status |
|---|---|
| G, R (s₀ = 3 fixed, p = n^{0.75}, λ_min(R_{S₀}) > 0) | by construction |
| SE | λ_min of the **full** correlation matrix = 0.024 (n = 400, B = 9), 0.015 (n = 1600, B = 15). This bounds every subset by interlacing. The correlation matrix depends on n only through B (orthonormal construction), so for n ≥ 1,626 (B = 16) it is a fixed matrix and SE holds exactly with φ₀² = λ_min(B = 16) > 0. |
| BM-∞ | fixed coefficients |
| T03 ⇒ π(S₀) → 1 | locked theorem under the above |
| T27 H1–H3 (masking; iid fails) | chain {1} ⊂ {1,2} ⊂ S₀. π₀(S₀) = 5.9·10⁻⁷ (n = 400) and 1.5·10⁻⁸ (n = 1600). π₀({1}) = 0.926 and 0.964. iid miss ≥ 0.0026 and **0.86**. Exponent β = −2a < 0. |
| start mass on 𝓡_d (T22(i)) | π₀(𝓡₀) = 0.927 and 0.964 (≥ π₀({1}); H3 implies it, since S^{(0)} ∈ 𝓡₀) |
| ELIG for LS0 | S̃₀ = {1} ∈ 𝓡₀ at both n |
| TD′(𝓡_d, ℓ) | GP(0), GP(1) hold at all states; 𝓡₂ (n = 400): GP fails at 4 states but all reach S₀ in 3 moves; LS0 path {1}→{1,2}→S₀ (or via {1,3}) |
| T37's TD(d,0), d ≥ 1 | **fails** (§6.4) — not needed |
| route (b2) SHARE, EXIT-end | not checkable from the design; OPEN |

**Answer to Astra's question.** T27 masking (H2, H3) and T22(i)'s near-truth start mass are **compatible**, and in fact aligned. H3 *is* a reference start-mass bound for S^{(0)} ∈ 𝓡₀. T22(i) for that reference needs visibility of S^{(0)}'s own variables and no leakage relative to S^{(0)}, while H2 needs invisibility of S₀ ∖ S^{(0)}. These involve disjoint coordinates, and CF2 satisfies both. The real obstructions lie elsewhere:
- (i) route (b2) needs a particle-level SHARE/LT hypothesis that C1 shows cannot be derived from start mass, bridge mass and exit control;
- (ii) T37's TD(d,0) is false for d ≥ 1 in proxy-rich designs;
- (iii) eligibility of the best-scored model (no LS0) fails the brief's sufficient condition by E1;
- (iv) CF has p < n. A p ≫ n family with cross-block cancellation (random design plus planted cancellation) is CONJECTURE, not constructed.
