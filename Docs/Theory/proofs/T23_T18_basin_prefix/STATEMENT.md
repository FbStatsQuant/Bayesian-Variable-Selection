# STATEMENT — T23(ii): pathwise Rao–Blackwell PIP bound and its basin consequence

Source: `theorems/T23_T18_basin_prefix.md`, part (ii) only (SMC-BVS v3.0, METHODOLOGY_v3.md SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c), read with `theorems/00_COMMON.md`. Parts (i), (iii), (iv), (v) are not claimed here.

Statement analysis outcome: **(a) correct as stated.** No assumption is changed or added. EXP / EXP′ is not needed. No other v3 conjecture is used as a hypothesis: the expectation bound is proved from the BASIN conditions directly (it does not cite part (i)). Section 5 lists the readings fixed here.

## 1. Setting (compact; the method file is authoritative)

- **Models and target.** Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋). Each S ∈ Ω has weight γ₁(S) = ϖ(S)m(S) > 0; Z = Σ_Ω γ₁ and π = γ₁/Z on Ω. The data (X, y) are fixed throughout.
- **Gibbs conditional.** For S ∈ Ω and j ∈ [p], o_j(S, 1) is the inclusion probability that the Gibbs step for coordinate j uses at state S (at φ = 1):
  - if j ∈ S, or j ∉ S and |S| < K: o_j(S,1) = γ₁(S ∪ {j}) / [γ₁(S ∪ {j}) + γ₁(S ∖ {j})];
  - if j ∉ S and |S| = K (addition excluded): o_j(S,1) = 0.
- **Truth and stability constant.** S₀ ⊆ [p] is a fixed set (the true support). δ₁ = 1 − π(S₀), u_π = δ₁/π(S₀) (u_π = +∞ if π(S₀) = 0).
- **Round at φ = 1.** One round of a particle is m = p + B + 2 labelled elementary steps (p Gibbs coordinate steps, one uniform swap, B neighbour swaps, one independence proposal from π₀), applied in a uniformly random order drawn independently of the particle's state, afresh for every particle and every round. Each Gibbs step for coordinate j records o_j(S,1) at the state S held immediately before its draw. A round started at x produces a path x = X⁽⁰⁾, X⁽¹⁾, …, X⁽ᵐ⁾ (X⁽ᵏ⁾ = state after k steps). K₁ is the one-round transition kernel (law of X⁽ᵐ⁾ given X⁽⁰⁾ = x); K₁^r its r-fold power.
- **Calibration.** 𝓒 is the frozen calibration output (grid, T, L, N_e, all settings), measurable with respect to streams 0–9 and the data; we fix a 𝓒 for which the final run is executed (successful grid construction). P_𝓒, E_𝓒 are probability and expectation over the final-run randomness (streams 10–13) given 𝓒.
- **Final run, island r ∈ {1,2,3,4}.** N = N_e particles; T bridge stages (reweight, multinomial resampling, one round per stage); then the **terminal rounds**: L burn-in rounds and 4 measured rounds, all with the kernel K₁ and with no reweighting or resampling. For particle i, X_{i,s} denotes its state after s terminal rounds (s = 0: after the stage-T resampling and the stage-T round). Measured round h ∈ {1,2,3,4} is terminal round L + h; it starts at X_{i,L+h−1}.
- **Estimators.** For island r, PIP̂_{rj} = (4N)⁻¹ Σ_{h=1}^{4} Σ_{i=1}^{N} o_j(S_{i,h,j}, 1), where S_{i,h,j} is particle i's state immediately before its Gibbs step for j in measured round h. Primary PIP̂_j = ¼ Σ_r PIP̂_{rj}. MPM̂ = {j : PIP̂_j > ½}.
- **Bad-round indicators.** B_{i,h} = 1 if particle i's path in measured round h, X⁽⁰⁾, …, X⁽ᵐ⁾ (including its start X⁽⁰⁾ = X_{i,L+h−1}), contains a state ≠ S₀; else 0. B̄_r = (4N)⁻¹ Σ_{h=1}^{4} Σ_{i=1}^{N} B_{i,h}.

## 2. Hypotheses

- **EX-A** (exact scores and probabilities, so o_j and π₀ draws are exact), **EX-S** (independent ideal uniform streams with the method's stream separation), **CAL** (𝓒 uses streams 0–9 only; streams 10–13 are fresh).
- **BASIN(𝓡, r₀, a, η, ρ, δ)**, given 𝓒: 𝓡 ⊆ Ω with S₀ ∈ 𝓡; an integer r₀ ≥ 1; numbers a, η, ρ ∈ [0,1], δ ≥ 0, such that
  - (entrance) K₁^{r₀}(x, {S₀}) ≥ a for every x ∈ 𝓡;
  - (basin exit) for every x ∈ 𝓡, the probability that a round started at x has some state outside 𝓡 on its path X⁽¹⁾, …, X⁽ᵐ⁾ is ≤ η;
  - (truth departure) the probability that a round started at S₀ has some state ≠ S₀ on its path X⁽¹⁾, …, X⁽ᵐ⁾ is ≤ ρ;
  - (initial occupancy) for every island r, E_𝓒[ N⁻¹ Σ_i 1{X_{i,0} ∉ 𝓡} ] ≤ δ.

Part (ii)'s first inequality (pathwise) uses only the setting and EX-A; the second uses S₀ ∈ Ω; the expectation and MPM bounds use EX-S, CAL and BASIN.

## 3. Conclusions

(ii-a) **Pathwise RB bound.** On every realisation of the final run, for each island r,
  max_j |PIP̂_{rj} − 1{j ∈ S₀}| ≤ B̄_r + max_j |o_j(S₀,1) − 1{j ∈ S₀}|.
  If S₀ ∉ Ω, the method does not define o_j(S₀, 1); it may then be given any real value, and the inequality holds for every such choice, because every path state lies in Ω and so B̄_r = 1.

(ii-b) **Truth term.** If S₀ ∈ Ω, then max_j |o_j(S₀,1) − 1{j ∈ S₀}| ≤ u_π. (If S₀ ∉ Ω, u_π = +∞ and the bound is trivial.)

(ii-c) **Expectation bound for the primary PIP.** Under BASIN,
  E_𝓒 max_j |PIP̂_j − 1{j ∈ S₀}| ≤ δ + (1−a)^{⌊L/r₀⌋} + (L+4)(η+ρ) + u_π =: 𝓑_n.

(ii-d) **MPM.** P_𝓒(MPM̂ ≠ S₀) ≤ 2𝓑_n.

The bounds use no independence between particles and no union bound over the p coordinates.

## 4. Scope

- All conclusions are given the data and a fixed successful 𝓒 (calibration-conditional). They say nothing about whether BASIN holds; statistical instances are parts (iii)–(v), not claimed here.

## 5. Readings fixed here (precisions, not changes)

1. **ρ is the whole-round departure probability from S₀.** The theorem file says "truth prefix-departure ≤ ρ" and, in (iii), bounds ρ by summing first-departure probabilities over all p + B + 2 labels of a round. B_{i,h} counts a departure anywhere in the round. The whole-round reading is the one consistent with both.
2. **η is the one-round first-exit probability from 𝓡,** maximised over starts in 𝓡 (path version). The proof uses only its consequence K₁(x, 𝓡ᶜ) ≤ η for x ∈ 𝓡, so the end-of-round version would also suffice.
3. **Terminal rounds have no resampling** (the method resamples after every reweighting; there is no reweighting at φ = 1 after stage T). Particle identities persist through the L + 4 terminal rounds.
4. **δ is per island** (islands are i.i.d. given 𝓒 under EX-S and CAL, so a bound for one island holds for all).
5. "MPM error" means the event MPM̂ ≠ S₀.
