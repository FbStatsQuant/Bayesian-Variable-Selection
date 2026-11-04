# STATEMENT — T15 (L-OCC): occupancy from an evidence lower tail

Source: `theorems/T15_LOCC_occupancy.md` (SMC-BVS v3.0, METHODOLOGY_v3.md SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c), read with `theorems/00_COMMON.md`. Parts to prove: all.

## 1. Setting (compact; the method file is authoritative)

- **Target.** Ω = {S ⊆ [p] : |S| ≤ K} is a finite set of models. Each S ∈ Ω has a strictly positive unnormalised posterior weight γ₁(S) = ϖ(S)m(S) (prior × marginal likelihood). Z := Σ_{S∈Ω} γ₁(S) ∈ (0, ∞) is the evidence and π := γ₁/Z the posterior on Ω. For A ⊆ Ω, π(A) = Σ_{S∈A} π(S).
- **Calibration.** 𝓒 is the frozen output of the calibration phase (temperature grid 0 = φ₀ < φ₁ < … < φ_T = 1, budgets, N = N_e, and all other settings). It is measurable with respect to calibration random streams 0–9 and the data. "Successful 𝓒" means the calibration ended with a constructed grid and the final run is launched. P_𝓒 and E_𝓒 denote probability and expectation over the final-run randomness (streams 10–13) given 𝓒 and the data.
- **Final run, island r ∈ {1, 2, 3, 4}.** N particles drawn i.i.d. from the start law π₀; for t = 1, …, T: reweight by G_t(S) = exp{(φ_t − φ_{t−1})d(S)}, multinomial resampling, one move round at temperature φ_t; then L burn-in rounds and 4 measured rounds at φ = 1 (no reweighting in these terminal rounds). A move round is a list of elementary steps applied, for each particle, in a uniformly random order drawn independently of the particle's state.
- **Island evidence.** Ẑ_r := m(∅)Z̄₀ ∏_{t=1}^{T} (1/N) Σ_{i=1}^{N} G_t(S_i^{(t−1)}), the product over all stages (the terminal rounds contribute no factor). Here m(∅) > 0 is the marginal likelihood of the empty model, π₀ = γ₀/Z̄₀ is the composite start law with normaliser Z̄₀ = Σ_Ω γ₀ > 0 (γ₀ > 0), and d(S) is the real-valued discrepancy (all defined in `theorems/00_COMMON.md` §§1–2). Since every factor is a finite positive number (each G_t(S) = e^{(φ_t−φ_{t−1})d(S)} ∈ (0, ∞)), Ẑ_r is a finite, strictly positive random variable under EX-A. The proof uses only W_r ≥ 0. Write **W_r := Ẑ_r / Z**. Pooled evidence: Ẑ := ¼ Σ_r Ẑ_r, and W̄ := Ẑ/Z = ¼ Σ_r W_r.
- **Recording positions.** 𝒯 denotes the set of positions τ in island r's terminal part at which T12(i) is stated: (a) τ = "end of stage T" (after the stage-T resampling and move round); (b) any fixed elementary prefix within the L + 4 terminal rounds; (c) "immediately before a specified Gibbs label" in a terminal round, under the state-independent random order. q̂_{r,τ} is the empirical measure (1/N)Σ_i δ_{S_i(τ)} of island r's particle states at position τ.
- **Outside set and outside fraction.** 𝔄 ⊆ Ω is a set that is fixed given 𝓒 (𝓒- and data-measurable, independent of streams 10–13). f_r := q̂_{r,τ}(1_{𝔄ᶜ}) ∈ [0, 1], the fraction of island r's particles outside 𝔄 at a fixed τ ∈ 𝒯.

## 2. Hypotheses

- **EX-A** (exact arithmetic), **EX-S** (independent ideal uniform streams, with the method's stream separation), **CAL** (𝓒 uses streams 0–9 only; streams 10–13 are fresh; escalation is decided before any final randomness). These are standing assumptions of the setting.
- **(H-T12) Frozen-run identity** (the conclusion of the sibling conjecture T12(i), used here only as an explicit hypothesis): conditional on a successful 𝓒, for island r, each τ ∈ 𝒯, and every bounded function f on Ω that is fixed given 𝓒,

  E_𝓒[ Ẑ_r · q̂_{r,τ}(f) ] = Z · π(f).

  (At these positions the target is q_T = q₁ = π and Z_T = Z.) Parts (i)–(ii) use only the instance f = 1_{𝔄ᶜ}, and only the inequality E_𝓒[W_r f_r] ≤ π(𝔄ᶜ). The first claim of (iii), P_𝓒(W_r < c) ≤ B/(1 − c), uses only its own L¹ hypothesis; its "consequently" clause rests on (i)–(ii) and hence on the same instance of (H-T12). Part (iv) is a statement about abstract laws and uses no hypothesis; it shows that even the identity of (H-T12) for every test function does not yield the pooled form.

## 3. Conclusions

Fix a successful 𝓒, an island r, a position τ ∈ 𝒯, and a set 𝔄 fixed given 𝓒. Let f_r = q̂_{r,τ}(1_{𝔄ᶜ}) and W_r = Ẑ_r/Z.

**(i) Mean bound.** For every c ∈ (0, 1):
  E_𝓒 f_r ≤ min{ 1, π(𝔄ᶜ)/c + P_𝓒(W_r < c) }.

**(ii) Tail bound.** For every c, u ∈ (0, 1):
  P_𝓒(f_r > u) ≤ π(𝔄ᶜ)/(cu) + P_𝓒(W_r < c).

**(iii) Lower tail from an L¹ bound.** If E_𝓒|W_r − 1| ≤ B for a constant B ≥ 0, then for every c ∈ (0, 1), P_𝓒(W_r < c) ≤ B/(1 − c). Consequently (i) and (ii) hold with P_𝓒(W_r < c) replaced by B/(1 − c).

**(iv) The lower tail must be islandwise.** The bounds (i)–(ii) with the pooled lower tail P_𝓒(W̄ < c) in place of the islandwise P_𝓒(W_r < c) do not follow from the structure used, even with the identity of (H-T12) for every test function. (This is a non-implication about direct substitution; it does not assert that every conceivable occupancy bound must use islandwise evidence.) Precisely, fix c, u ∈ (0, 1) and a ∈ (0, cu/4].

(iv-a) There are four i.i.d. random pairs (W_r, f_r), r = 1, …, 4, with W_r > 0 (strictly), f_r ∈ {0, 1}, E W_r = 1 and E[W_r f_r] = a, such that, with W̄ = ¼ Σ_r W_r,
  E f_1 > a/c + P(W̄ < c)  and  P(f_1 > u) > a/(cu) + P(W̄ < c);
in particular, since min{1, x} ≤ x, also E f_1 > min{1, a/c + P(W̄ < c)}.

(iv-b) Moreover, let Ω′ be any finite set, π′ any probability on Ω′, 𝔄′ ⊆ Ω′ with π′(𝔄′ᶜ) = a, and N ≥ 1. (For example, the method's Ω and π whenever some 𝔄 ⊆ Ω has π(𝔄ᶜ) = a; such an 𝔄 exists for a := the smallest posterior mass of a single model whenever |Ω| ≥ 4/(cu), since that mass lies in (0, 1/|Ω|] ⊆ (0, cu/4].) Then the pairs of (iv-a) can be realised jointly with random populations (S_{r,1}, …, S_{r,N}) ∈ Ω′^N, r = 1, …, 4, such that the four pairs (W_r, (S_{r,i})_{i≤N}) are i.i.d., f_r = q̂_r(1_{𝔄′ᶜ}) for the empirical measure q̂_r = (1/N) Σ_i δ_{S_{r,i}}, and

  E[ W_r · q̂_r(g) ] = π′(g)  for every function g : Ω′ → ℝ,

which is the identity of (H-T12) with Ẑ_r := Z′ W_r for any constant Z′ > 0, for every test function g and not only for g ∈ {1, 1_{𝔄′ᶜ}}. Each island has one population; using it at every recording position (q̂_{r,τ} := q̂_r for all τ ∈ 𝒯) gives the identity at every position as well. The four islands of this example are i.i.d.; that property only strengthens the example and is not asserted here as a property of the method.

## 4. Scope remarks (from the theorem file; interpretations, not separate claims)

- (i)–(iii) are statements about the law of the final run given 𝓒 (calibration-conditional). They give no bound on the outside fraction of an already realised population; for a realised population its actual f_r must be used.
- Part (iv) formalises the theorem file's sentence "a pooled-evidence lower tail does not substitute" as a non-implication from the properties listed (W_r > 0, f_r a fraction in [0,1], i.i.d. islands, and the identity of (H-T12) for every test function and every recording position). It does not claim that the SMC final run, for a particular data set and calibration, realises the counterexample law.

## 5. Changes relative to the theorem file

- None to the inequalities, their constants or their quantifiers.
- The theorem file's dependency on T12 ("Builds on: T12"; "prefixes as specified in T12") is stated as the explicit hypothesis (H-T12), as the run rules require for sibling conjectures. The positions 𝒯 are exactly those named in T12(i).
- The sentence on pooled lower tails is made precise as part (iv) (a non-implication), and the sentence on realised populations is kept as a scope remark (§4).
- Assumption EXP (and its replacement EXP′) is not used.
- v2 (after Astra round 1, exposition finding 1): in (iv) the example pairs are required to have W_r > 0 strictly (v1 allowed W_r ≥ 0), matching the strict positivity of actual island evidence, and a sentence fixes the scope of the heading. The inequalities of (i)–(iii) are unchanged.
- v3 (after Stage B, Opus exposition findings 1–5; no fatal or gap findings in any review): (iv) now holds for every a ∈ (0, cu/4] (v2: a = cu/4 only) and adds (iv-b), realising the example with particle populations that satisfy the full identity (H-T12) for every test function; the min{1,·} form is refuted explicitly; the sentence presenting island i.i.d. as a method property is removed; Ẑ_r's symbols and positivity are spelled out; the hypothesis-use note in §2 is made exact. (i)–(iii) unchanged.
- v4 (after Stage B round 2; both reviewers verified v3 with exposition findings only): wording only — the hypothesis-use note for (iii) separates its two claims; "full identity" replaced by "identity for every test function", with the single-population/every-position remark; the method's-Ω example states when a set of mass a exists. No mathematical content changed.
- Post-review alignment (after Stage B round 3, Opus finding 1, marked optional): the last "full identity" in the §4 scope remark replaced by the v4 wording. Wording only, in a scope remark; not re-sent for review.
