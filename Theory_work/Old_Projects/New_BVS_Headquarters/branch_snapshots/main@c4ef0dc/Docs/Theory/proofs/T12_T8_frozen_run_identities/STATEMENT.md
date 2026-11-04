# STATEMENT — T12 (T8): frozen-run evidence and recorded Rao–Blackwell identities

Methodology: SMC-BVS v3.0 (METHODOLOGY_v3.md, SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c), §§6.3–6.5, 6.8, 6.11, 6.12. Source conjecture: `theorems/T12_T8_frozen_run_identities.md`. This file is the precise statement to be proved; nothing else is assumed.

## 0. Data and target (fixed, deterministic objects)

A **valid input** is (X^r, y^r) with finite entries, n ≥ 3, at least one retained (non-constant) column, and y^r not constant. X and y are the standardised data (columns and y centred and scaled so that every squared norm is n − 1). p ≥ 1 is the number of retained columns, K = min(p, ⌊n/2⌋) ≥ 1, and the state space is Ω = {S ⊆ [p] : |S| ≤ K} (finite, |Ω| ≥ 2).

For S ∈ Ω, with k = |S|, G_S = X_SᵀX_S, z_S = X_Sᵀy, a₀ = b₀ = 0.01 and ν = a₀ + n/2 (the v3 target, METHODOLOGY §5 and 00_COMMON §1):
- H_S = (n + 1)G_S + I_k, D_S = det H_S / det(G_S + I_k), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S (for S = ∅: D_∅ = 1, Q_∅ = yᵀy);
- m(S) = C_n D_S^{−1/2}(2b₀ + Q_S)^{−ν} with C_n = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) > 0, so BF(S) := m(S)/m(∅) = D_S^{−1/2}[(2b₀ + Q_S)/(2b₀ + yᵀy)]^{−ν};
- ϖ(S) = w(k)/W_K with w(k) = B(1 + k, 2p − k)/B(1, p) = ½/C(2p − 1, k) and W_K = Σ_{j≤K} C(p, j)w(j) (the BB(1, p) prior capped at K);
- Z = Σ_{S∈Ω} ϖ(S)m(S), π(S) = ϖ(S)m(S)/Z, PIP_j = π({S : j ∈ S}).

m > 0 (Q_S > 0, as Q_S ≥ yᵀy/(n + 1)) and ϖ > 0. Everything except the explicit instance of (iv.b)/(iv.e) uses only m > 0 and ϖ > 0. The instance uses the formulas above.

The following are deterministic functions of the data (method §§6.3–6.4):
- blocks C₁, …, C_J partitioning [p]; tables r_b(U) = BF(U) > 0 for U ⊆ C_b;
- γ₀(S) = ϖ(S)∏_b r_b(S ∩ C_b), Z̄₀ = Σ_Ω γ₀, π₀ = γ₀/Z̄₀ (so π₀(S) > 0 for every S ∈ Ω);
- the discrepancy d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b) (so d(∅) = 0); for real φ, γ_φ = γ₀e^{φd}, Z̄_φ = Σ_Ω γ_φ, q_φ = γ_φ/Z̄_φ; note q₀ = π₀ and q₁ = π, and m(∅)Z̄₁ = Z;
- the neighbour graph N(·), symmetric: l ∈ N(j) ⇔ j ∈ N(l); B = min(⌊√n⌋, ⌊√p⌋, 16).

## 1. Elementary steps and rounds (method §6.5)

At temperature φ there are m = p + B + 2 labelled elementary steps, each a Markov kernel on Ω:
- **Gibbs coordinate j** (j ∈ [p]): at S, with S⁺ = S ∪ {j} and S⁻ = S \ {j}: if |S⁺| ≤ K, move to S⁺ with probability o_j(S, φ) = γ_φ(S⁺)/(γ_φ(S⁺) + γ_φ(S⁻)) and to S⁻ otherwise; if |S⁺| > K, set o_j(S, φ) = 0 and move to S⁻ (= S). The value o_j(S, φ) is the **pre-draw recording** of the step.
- **Uniform swap:** at S with |S| ∈ {0, p}, stay. Otherwise choose j ∈ S and l ∈ [p] \ S uniformly and independently, propose S′ = S \ {j} ∪ {l}, accept with probability 1 ∧ γ_φ(S′)/γ_φ(S), else stay.
- **Neighbour swap** (B copies, each a separate label): at S = ∅, stay. Otherwise choose j ∈ S uniformly; if N(j) \ S = ∅, stay; else choose l uniformly in N(j) \ S, propose S′ = S \ {j} ∪ {l}, accept with probability 1 ∧ [γ_φ(S′)/γ_φ(S)]·|N(j) \ S|/|N(l) \ S′|, else stay.
- **Independence proposal:** draw S′ ~ π₀, accept with probability 1 ∧ e^{φ[d(S′) − d(S)]}, else stay.

A **round at φ** applied to a particle: draw an order σ (a bijection from positions {1, …, m} to the m labels) uniformly at random, independently of the particle's state, and apply the elementary steps σ(1), …, σ(m) in turn. The states X_{[0]} (round start), X_{[1]}, …, X_{[m]} (round end) form the particle's **within-round path**. K_φ denotes the resulting round kernel.

## 2. The frozen run with fixed parameters

**Frozen parameters** c consist of: a grid 0 = φ₀ < φ₁ < … < φ_T = 1 with integer T ≥ 1 (Δ_t = φ_t − φ_{t−1}, G_t = e^{Δ_t d}); an integer particle number N ≥ 1; an integer number L′ ≥ 0 of rounds at φ = 1 run after the stage-T round; an integer number M ≥ 1 of measured rounds; and a flag saying whether a round at φ₀ = 0 is applied at stage 0. **The method** (METHODOLOGY §6.8: "one move round per stage, then L burn-in rounds and 4 measured rounds") is the case N = N_e, M = 4, L′ = L, flag unset. Other values are generalisations, covered by the same statements.

**One island I(c):**
1. Stage 0: X₀^i iid ~ π₀ (i = 1, …, N); Ẑ₀ = Z₀ := m(∅)Z̄₀; if the flag is set, each particle performs one round at φ₀. Call the population X^{(0)}.
2. Stage t = 1, …, T: weights w^i = G_t(X^{(t−1),i}); Ẑ_t = Ẑ_{t−1}·(1/N)Σ_i w^i; multinomial resampling (ancestors A¹, …, A^N iid with P(A = k) = w^k/Σ_l w^l given the past); each resampled particle X^{(t−1),A^i} performs one round at φ_t; call the population X^{(t)}. q̂_t := (1/N)Σ_i δ_{X^{(t),i}}; q̂₀ := (1/N)Σ_i δ_{X^{(0),i}}.
3. After stage T: L′ rounds at φ = 1, then M measured rounds at φ = 1. In measured round u, Y^i_{u,j} is particle i's state immediately before its Gibbs-j step. Island evidence Ẑ := Ẑ_T; island RB estimate PIP̂_j := (MN)⁻¹Σ_{u=1}^{M}Σ_{i=1}^{N} o_j(Y^i_{u,j}, 1).

Stage notation: q_t = q_{φ_t}, Z_t = m(∅)Z̄_{φ_t}; so Z_T = Z.

**Randomness (from EX-S and the prescribed operations).** (R1) the stage-0 draws are iid π₀; (R2) given everything before a resampling, the ancestors are iid with the stated law; (R3) given the σ-field H of everything before a round (including the states entering it), the particles' (order, within-round path) pairs are conditionally independent across particles, each order is uniform and independent of H, and given H and its order σ, a particle's within-round path is a Markov chain started at its entering state with kernels K_{σ(1)}, …, K_{σ(m)} (each step uses fresh randomness; the independence proposal is a fresh exact π₀ draw).

**Hypotheses.**
- **EX-A:** exact arithmetic: every score, table, Z̄₀, probability and comparison is exact (no numerical-failure status occurs).
- **START** (imported dependency: T09(i) / project P1, not re-proved here): the start sampler returns exact iid π₀ draws, the reported Z̄₀ equals Σ_Ω γ₀, and the independence proposals use the same exact sampler. This is not an extra restriction on inputs: the definition of I(c) above already uses these properties, and START is what makes the method's final island an instance of I(c). EX-A alone does not give it.
- **EX-S:** independent ideal uniform streams with the method's stream separation; in particular (R1)–(R3). The stream model includes measurability: the map (c, u) ↦ Φ(c, u) below, from (calibration value, stream) to the island record, is jointly measurable, and the record takes values in a Polish space. This holds for any algorithmic realisation from uniform streams.
- **CAL:** the calibration output 𝓒 (grid, T, L, N_e, tier, candidate set and every other setting the final run uses) is measurable with respect to the data and streams 0–9 only; the final islands r = 1, …, 4 use streams 10–13, which are independent of each other and of streams 0–9; escalation is decided before any final randomness.
- **Success:** 𝒜 ∈ σ(𝓒) is the event that calibration succeeds (a grid is constructed at the final tier, so the final run executes). On 𝒜 the final islands are O_r = Φ(𝓒, U_r), r = 1, …, 4, where U_r is stream 9 + r and Φ(c, ·) realises I(c) with the method's parameters (N = N_e, M = 4, L′ = L, flag unset). "Given 𝓒" means conditional on σ(𝓒) on the event 𝒜. Island r's outputs are Ẑ_r, PIP̂_{rj}, and its stage quantities Ẑ_{r,t}, q̂_{r,t}.
- **Pooled estimators:** Ẑ = ¼Σ_rẐ_r; primary P̄_j = ¼Σ_r PIP̂_{rj}; secondary P̃_j = Σ_rẐ_rPIP̂_{rj}/Σ_rẐ_r.

## 3. Conclusions

Let E_c denote expectation for the frozen run with fixed parameters c. For every valid input:

**(i) Evidence identities.**
- (i.a) For every c, t ∈ {0, …, T} and f : Ω → ℝ: E_c[Ẑ_t q̂_t(f)] = Z_t q_t(f). In particular E_c[Ẑ] = Z.
- (i.b) *Terminal invariant rounds with unit potentials.* After stage T, let any fixed finite sequence of operations be applied, each either a round at φ = 1 or a multinomial resampling with unit weights (which leaves Ẑ unchanged). For the population q̂ after any of these operations, E_c[Ẑ q̂(f)] = Z π(f).
- (i.c) *State-independent prefixes.* Consider any round of the run (a stage-t round, with Ẑ_t and target q_t, or a post-terminal round, with Ẑ_T and target π) and, for each particle i, a prefix length κ_i = κ(σ_i) ∈ {0, …, m} that is a fixed function of that particle's order σ_i alone (examples: a fixed k; κ(σ) = σ⁻¹(ℓ) − 1, the position just before a specified label ℓ). Then E_c[Ẑ_t (1/N)Σ_i f(X^i_{[κ_i]})] = Z_t q_t(f).
- (i.d) *Not at state-dependent stopping times.* For every c and every round of the run (with its Ẑ_t, q_t as in (i.c)), there are f and a stopping time τ_i of particle i's within-round path for which E_c[Ẑ_t (1/N)Σ_i f(X^i_{[τ_i]})] > Z_t q_t(f). Namely τ_i = min{k ∈ {0, …, m} : X^i_{[k]} = ∅} ∧ m, with min ∅ = ∞, and f = 1{∅}.

**(ii) Recorded RB identity.** For every c and j ∈ [p]: E_c[Ẑ·PIP̂_j] = Z·PIP_j.

**(iii) Pooled evidence.** Under EX-A, START, EX-S, CAL, given 𝓒 on 𝒜: for every r and every stage t ≤ T of 𝓒's grid, E[Ẑ_{r,t}q̂_{r,t}(f) | 𝓒] = Z_tq_t(f) (Z_t and q_t are those of 𝓒's grid, so this right side is 𝓒-measurable) and E[Ẑ_rPIP̂_{rj} | 𝓒] = Z·PIP_j; E[Ẑ | 𝓒] = Z; E[log Ẑ | 𝓒] ≤ log Z and E[log Ẑ_r | 𝓒] ≤ log Z; and for every 0 < α < 1, P(Z ≥ αẐ | 𝓒) ≥ 1 − α and P(Z ≥ αẐ_r | 𝓒) ≥ 1 − α.

**(iv) Limits.**
- (iv.a) *log Ẑ.* For every c: if d ≡ 0 on Ω then Ẑ = Z almost surely; otherwise E_c[log Ẑ] < log Z, and, for the four islands of the method given 𝓒, E[log Ẑ | 𝓒] < log Z and E[log Ẑ_r | 𝓒] < log Z.
- (iv.b) *Normalised PIPs.* Given 𝓒, E[P̄_j | 𝓒] − PIP_j = −Cov(PIP̂_{1j}, Ẑ₁ | 𝓒)/Z. *Component example.* There is a valid input and frozen parameters c for which both normalised estimators are biased: n = 20, p = 2 with the data of the appendix, T = 1, N = 1, M = 4, L′ = L = max(4, ⌈log₂(n + 1)⌉) = 5, flag unset, four independent islands I(c), and j = 1. Then E[P̄₁] − PIP₁ < −0.17 and E[P̃₁] − PIP₁ < −0.15. The same bounds hold with the flag set and/or L′ = L − 1 (generalisations). Scope: at p = 2 the full method would take the exact branch, and N = 1 is not the production budget. So this shows bias of the frozen SMC component, not bias of the full method's output on this input.
- (iv.c) *Island independence.* Given 𝓒, the islands O₁, …, O₄ are independent, each with the law of I(𝓒). Assume P(𝒜) > 0. Under P(· | 𝒜), for every bounded measurable h of an island's outputs, Cov(h(O₁), h(O₂)) = Var(E[h(O₁) | 𝓒]). Hence the islands are independent under P(· | 𝒜) if and only if the conditional law of an island given 𝓒 is a.s. constant, which none of the hypotheses ensure. In particular the island law does depend on c: if d has a unique maximiser on Ω, the law of Ẑ under (grid, N) differs from that under (grid, 4N). (Not claimed: that the actual calibration procedure produces, on some specific input, two values of 𝓒 with different island laws, each with positive probability.)
- (iv.d) *Launch events.* Let A ∈ σ(𝓒) with A ⊆ 𝒜 and P(A) > 0. The conclusions of (iii) whose right side does not depend on 𝓒 hold under P(· | A): E[Ẑ | A] = E[Ẑ_r | A] = Z, E[Ẑ_rPIP̂_{rj} | A] = Z·PIP_j, E[log Ẑ | A] ≤ log Z, E[log Ẑ_r | A] ≤ log Z, P(Z ≥ αẐ | A) ≥ 1 − α and P(Z ≥ αẐ_r | A) ≥ 1 − α. For an intermediate stage t and A ⊆ {T ≥ t}, the averaged form holds: E[Ẑ_{r,t}q̂_{r,t}(f) | A] = E[Z_tq_t(f) | A], where Z_tq_t(f) is computed on 𝓒's grid. The left side is a number, whereas Z_tq_t(f) is a random variable, and it is non-constant when, for example, φ_t takes two values with positive probability under P(· | A) and f = 1{S} with d(S) ≠ 0.
- (iv.e) *Favourable final diagnostics.* Let F be the event that the final E2 check passes: the standard deviation of {log Ẑ_r}_{r=1}^{4} is ≤ 1 nat (either the 1/4 or the 1/3 normalisation). In the component example of (iv.b) (same scope), P(F) > 0, E[Ẑ_r | F] < Z, E[Ẑ | F] < Z and E[Ẑ_r PIP̂_{r1} | F] ≠ Z·PIP₁. So conditioning on a favourable final diagnostic breaks an identity in each of (i) (E Ẑ_r = Z), (ii) and (iii) (E Ẑ = Z). This is not a claim that the Jensen or Markov inequalities of (iii) fail under F; in this example they still hold, because E[Ẑ | F] < Z.
- (iv.f) *NUM alone.* A NUM-compatible perturbed-score model with bound η > 0 is the same algorithm in exact arithmetic with every evaluated log m(S) replaced by a value within η of it. (This does not assert that any particular floating-point implementation makes this error; it shows that NUM alone does not exclude it.) For every η > 0 there is such an implementation (log m(S) + η for every S) with E_c[Ẑ^impl] = e^ηZ ≠ Z for every c and valid input; and on every valid input with d ≡ 0 (for example p = 1), P(Z ≥ αẐ^impl) = 0 for every α ∈ (e^{−η}, 1).

## Appendix: data for (iv.b) and (iv.e)

n = 20, p = 2, i = 0, …, 19: x1_i = (7i mod 20) − 9.5; x2_i = x1_i + ((5i² mod 7) − 3); y_i = x1_i − x2_i + ((3i mod 5) − 2). (Raw data; standardised as in §0.) Then B = 1, the blocks are {1}, {2}, N(1) = {2}, N(2) = {1}, K = 2, m = 5, L = 5.

## Statement history

- v1 (2026-10-22): written by the lead from the conjecture. The formalisation choices are listed in review/packets/STATEMENT_REPORT_A1_call1.md.
- v2 (2026-10-22): statement check by Astra #1 (review/A1_call1_statement_check_REPLY.md), ruling APPROVED WITH CHANGES. All four required changes adopted:
  1. (iv.d) repaired. v1 claimed every conclusion of (iii) under P(· | A). That is false for intermediate stages, whose targets depend on the random grid; only the 𝓒-free conclusions survive, and intermediate stages hold in averaged form.
  2. The method is identified as L′ = L, flag unset (METHODOLOGY §6.8); other values are labelled generalisations; count parameters are declared integers.
  3. START is labelled an imported dependency (T09(i)), not a new restriction.
  4. Component scope stated beside (iv.b)/(iv.e). (iv.e) is stated as breaking the identities, not the Jensen/Markov inequalities.
  Also, following Astra's item 5: min ∅ = ∞ and time 0 are made explicit in (i.d).
- v2.1 (2026-10-22): after Astra #1's proof review (verdict verified; three exposition findings), the assumption P(𝒜) > 0 was made explicit in (iv.c). This is exposition only.
- v2.2 (2026-10-22): after the Stage B reviews (Astra #2 and Opus xhigh; both raised the same gap). §0 now writes out the target formulas (m(S), BF, ϖ, w, W_K, a₀ = b₀ = 0.01, ν = a₀ + n/2), copied from METHODOLOGY §5 / 00_COMMON §1, Felipe's fixed target. EX-S now states that joint measurability of Φ is part of the stream model. In (iv.d), 'only … in general random' is replaced by an exact remark. No conclusion changed.
