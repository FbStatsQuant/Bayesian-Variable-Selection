# STATEMENT — T15 (L-OCC): occupancy from an evidence lower tail

Source: `theorems/T15_LOCC_occupancy.md` (SMC-BVS v3.0, METHODOLOGY_v3.md SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c), read with `theorems/00_COMMON.md`. Parts to prove: all.

## 1. Setting (compact; the method file is authoritative)

- **Target.** Ω = {S ⊆ [p] : |S| ≤ K} is a finite set of models. Each S ∈ Ω has a strictly positive unnormalised posterior weight γ₁(S) = ϖ(S)m(S) (prior × marginal likelihood). Z := Σ_{S∈Ω} γ₁(S) ∈ (0, ∞) is the evidence and π := γ₁/Z the posterior on Ω. For A ⊆ Ω, π(A) = Σ_{S∈A} π(S).
- **Calibration.** 𝓒 is the frozen output of the calibration phase (temperature grid 0 = φ₀ < φ₁ < … < φ_T = 1, budgets, N = N_e, and all other settings). It is measurable with respect to calibration random streams 0–9 and the data. "Successful 𝓒" means the calibration ended with a constructed grid and the final run is launched. P_𝓒 and E_𝓒 denote probability and expectation over the final-run randomness (streams 10–13) given 𝓒 and the data.
- **Final run, island r ∈ {1, 2, 3, 4}.** N particles drawn i.i.d. from the start law π₀; for t = 1, …, T: reweight by G_t(S) = exp{(φ_t − φ_{t−1})d(S)}, multinomial resampling, one move round at temperature φ_t; then L burn-in rounds and 4 measured rounds at φ = 1 (no reweighting in these terminal rounds). A move round is a list of elementary steps applied, for each particle, in a uniformly random order drawn independently of the particle's state.
- **Island evidence.** Ẑ_r := m(∅)Z̄₀ ∏_{t=1}^{T} (1/N) Σ_{i=1}^{N} G_t(S_i^{(t−1)}), the product over all stages (the terminal rounds contribute no factor). Under EX-A, Ẑ_r is a finite, strictly positive random variable. Write **W_r := Ẑ_r / Z**. Pooled evidence: Ẑ := ¼ Σ_r Ẑ_r, and W̄ := Ẑ/Z = ¼ Σ_r W_r.
- **Recording positions.** 𝒯 denotes the set of positions τ in island r's terminal part at which T12(i) is stated: (a) τ = "end of stage T" (after the stage-T resampling and move round); (b) any fixed elementary prefix within the L + 4 terminal rounds; (c) "immediately before a specified Gibbs label" in a terminal round, under the state-independent random order. q̂_{r,τ} is the empirical measure (1/N)Σ_i δ_{S_i(τ)} of island r's particle states at position τ.
- **Outside set and outside fraction.** 𝔄 ⊆ Ω is a set that is fixed given 𝓒 (𝓒- and data-measurable, independent of streams 10–13). f_r := q̂_{r,τ}(1_{𝔄ᶜ}) ∈ [0, 1], the fraction of island r's particles outside 𝔄 at a fixed τ ∈ 𝒯.

## 2. Hypotheses

- **EX-A** (exact arithmetic), **EX-S** (independent ideal uniform streams, with the method's stream separation), **CAL** (𝓒 uses streams 0–9 only; streams 10–13 are fresh; escalation is decided before any final randomness). These are standing assumptions of the setting.
- **(H-T12) Frozen-run identity** (the conclusion of the sibling conjecture T12(i), used here only as an explicit hypothesis): conditional on a successful 𝓒, for island r, each τ ∈ 𝒯, and every bounded function f on Ω that is fixed given 𝓒,

  E_𝓒[ Ẑ_r · q̂_{r,τ}(f) ] = Z · π(f).

  (At these positions the target is q_T = q₁ = π and Z_T = Z.) Only the instance f = 1_{𝔄ᶜ}, giving E_𝓒[W_r f_r] = π(𝔄ᶜ), and, in part (iv), the instance f ≡ 1, giving E_𝓒 W_r = 1, are used. For parts (i)–(iii), only the inequality E_𝓒[W_r f_r] ≤ π(𝔄ᶜ) is needed.

## 3. Conclusions

Fix a successful 𝓒, an island r, a position τ ∈ 𝒯, and a set 𝔄 fixed given 𝓒. Let f_r = q̂_{r,τ}(1_{𝔄ᶜ}) and W_r = Ẑ_r/Z.

**(i) Mean bound.** For every c ∈ (0, 1):
  E_𝓒 f_r ≤ min{ 1, π(𝔄ᶜ)/c + P_𝓒(W_r < c) }.

**(ii) Tail bound.** For every c, u ∈ (0, 1):
  P_𝓒(f_r > u) ≤ π(𝔄ᶜ)/(cu) + P_𝓒(W_r < c).

**(iii) Lower tail from an L¹ bound.** If E_𝓒|W_r − 1| ≤ B for a constant B ≥ 0, then for every c ∈ (0, 1), P_𝓒(W_r < c) ≤ B/(1 − c). Consequently (i) and (ii) hold with P_𝓒(W_r < c) replaced by B/(1 − c).

**(iv) The lower tail must be islandwise.** The bounds (i)–(ii) with the pooled lower tail P_𝓒(W̄ < c) in place of the islandwise P_𝓒(W_r < c) do not follow from the structure used. Precisely: for every c, u ∈ (0, 1) there are a number a ∈ (0, 1) and four i.i.d. random pairs (W_r, f_r), r = 1, …, 4, with W_r ≥ 0, f_r ∈ {0, 1} (so f_r ∈ {0, 1/N, …, 1} for every N), E W_r = 1 and E[W_r f_r] = a (the properties that (H-T12) gives with a = π(𝔄ᶜ), together with conditional independence and identical distribution of the islands given 𝓒), such that, with W̄ = ¼ Σ_r W_r,
  E f_1 > a/c + P(W̄ < c)  and  P(f_1 > u) > a/(cu) + P(W̄ < c).

## 4. Scope remarks (from the theorem file; interpretations, not separate claims)

- (i)–(iii) are statements about the law of the final run given 𝓒 (calibration-conditional). They give no bound on the outside fraction of an already realised population; for a realised population its actual f_r must be used.
- Part (iv) formalises the theorem file's sentence "a pooled-evidence lower tail does not substitute" as a non-implication from the properties listed. It does not claim that a particular data set and calibration realise the counterexample law.

## 5. Changes relative to the theorem file

- None to the inequalities, their constants or their quantifiers.
- The theorem file's dependency on T12 ("Builds on: T12"; "prefixes as specified in T12") is stated as the explicit hypothesis (H-T12), as the run rules require for sibling conjectures. The positions 𝒯 are exactly those named in T12(i).
- The sentence on pooled lower tails is made precise as part (iv) (a non-implication), and the sentence on realised populations is kept as a scope remark (§4).
- Assumption EXP (and its replacement EXP′) is not used.
