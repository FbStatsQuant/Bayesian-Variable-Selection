import SmcBvs.Basic

/-!
# T21 (C1): composition inequality for the reported HPM — abstract finite version

Source: `Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md` §3 (C1) and `PROOF_v3.tex`
lines 52–86 (theorem C1 and its proof); restated as (C1′) in branch `theory/W2-BOOK`,
`theory_campaign/W2-BOOK/PROOF.md` §4.1.

Abstract setting (no regression structure is used by C1):
* `M` a type of models, `A : Finset M` the finite model space `Ω` (`S₀ ∈ A` is *not* needed);
* a probability space `(Ω, P)` (`Ω` here is the sample space, written `ω`), carrying
  - `F ω : M → ℝ`, the log-score (larger preferred), with posterior `π_ω = post (F ω) A`;
  - `U : Set Ω`, the event "no usable HPM output";
  - `𝒮 ω : Finset M`, the cumulative scored set, `𝒮 ω ⊆ A` on `Uᶜ`;
  - `Ŝ ω : M`, the reported HPM; on `Uᶜ` it is *some* maximiser of `F ω` over `𝒮 ω`. The
    method's fixed tie rule gives one such maximiser (`IsLeastArgmax`), so the results below hold
    for every tie rule, in particular for the method's.
* "`U` or `Ŝ ≠ S₀`" is the event `U ∪ {ω ∉ U, Ŝ ω ≠ S₀}` (no output is needed on `U`).

Main results
* `hpm_eq_truth`         : deterministic core: `π(S₀) > 1/2`, `S₀ ∈ 𝒮` ⇒ `Ŝ = S₀`.
* `t21_event_subset`     : the event inclusion of PROOF_v3 line 71, sharpened.
* `t21_decomposition`    : `P(U ∨ Ŝ≠S₀) ≤ P(U) + P(Uᶜ, S₀∉𝒮) + P(Uᶜ, S₀∈𝒮, π(S₀) ≤ 1/2)`.
* `t21_decomposition'`   : the form in the L-LEAN brief, with `P(S₀ ∉ 𝒮)`.
* `markov_half`          : `P(δ ≥ 1/2) ≤ 2 E δ` for `0 ≤ δ`.
* `t21_C1`               : `P(U ∨ Ŝ≠S₀) ≤ P(U) + 2 E δ₁ + P(Uᶜ, S₀∉𝒮)`, `δ₁ = 1 - π(S₀)`.
* `integral_le_eps_add_prob` : `E δ ≤ ε + P(δ > ε)` for `0 ≤ δ ≤ 1` (the step used for "H03 ⇒
  E₀δ₁ → 0", PROOF_v3 lines 78–84).
-/

open MeasureTheory Finset

namespace SmcBvs

variable {M : Type*} [DecidableEq M]

/-- Deterministic core of C1: if `π(S₀) > 1/2` and `S₀` has been scored, every maximiser of the
score over the scored set `𝒮 ⊆ A` is `S₀` (whatever the tie rule). -/
theorem hpm_eq_truth {F : M → ℝ} {A 𝒮 : Finset M} {S₀ Ŝ : M} (h𝒮 : 𝒮 ⊆ A)
    (hS₀ : S₀ ∈ 𝒮) (hπ : 1 / 2 < post F A S₀) (hŜ : IsArgmax F 𝒮 Ŝ) : Ŝ = S₀ := by
  obtain ⟨-, hstrict⟩ := strict_max_of_post_gt_half hπ
  exact hŜ.eq_of_strict hS₀ (fun T hT hne => hstrict T (h𝒮 hT) hne)

variable {Ω : Type*} [MeasurableSpace Ω]

/-- The event inclusion behind C1:
`{U or Ŝ ≠ S₀} ⊆ U ∪ {Uᶜ, S₀ ∉ 𝒮} ∪ {Uᶜ, S₀ ∈ 𝒮, π(S₀) ≤ 1/2}`. -/
theorem t21_event_subset (U : Set Ω) (A : Finset M) (𝒮 : Ω → Finset M) (F : Ω → M → ℝ)
    (Ŝ : Ω → M) (S₀ : M) (h𝒮 : ∀ ω ∉ U, 𝒮 ω ⊆ A)
    (hŜ : ∀ ω ∉ U, IsArgmax (F ω) (𝒮 ω) (Ŝ ω)) :
    U ∪ {ω | ω ∉ U ∧ Ŝ ω ≠ S₀} ⊆
      U ∪ {ω | ω ∉ U ∧ S₀ ∉ 𝒮 ω} ∪ {ω | ω ∉ U ∧ S₀ ∈ 𝒮 ω ∧ post (F ω) A S₀ ≤ 1 / 2} := by
  intro ω hω
  rcases hω with hU | ⟨hU, hne⟩
  · exact Or.inl (Or.inl hU)
  · by_cases hmem : S₀ ∈ 𝒮 ω
    · by_cases hπ : post (F ω) A S₀ ≤ 1 / 2
      · exact Or.inr ⟨hU, hmem, hπ⟩
      · exact absurd (hpm_eq_truth (h𝒮 ω hU) hmem (lt_of_not_ge hπ) (hŜ ω hU)) hne
    · exact Or.inl (Or.inr ⟨hU, hmem⟩)

/-- **T21 decomposition** (sharp form). No measurability is needed (outer measure). -/
theorem t21_decomposition (P : Measure Ω) (U : Set Ω) (A : Finset M) (𝒮 : Ω → Finset M)
    (F : Ω → M → ℝ) (Ŝ : Ω → M) (S₀ : M) (h𝒮 : ∀ ω ∉ U, 𝒮 ω ⊆ A)
    (hŜ : ∀ ω ∉ U, IsArgmax (F ω) (𝒮 ω) (Ŝ ω)) :
    P (U ∪ {ω | ω ∉ U ∧ Ŝ ω ≠ S₀}) ≤
      P U + P {ω | ω ∉ U ∧ S₀ ∉ 𝒮 ω} +
        P {ω | ω ∉ U ∧ S₀ ∈ 𝒮 ω ∧ post (F ω) A S₀ ≤ 1 / 2} := by
  calc P (U ∪ {ω | ω ∉ U ∧ Ŝ ω ≠ S₀})
      ≤ P (U ∪ {ω | ω ∉ U ∧ S₀ ∉ 𝒮 ω} ∪
          {ω | ω ∉ U ∧ S₀ ∈ 𝒮 ω ∧ post (F ω) A S₀ ≤ 1 / 2}) :=
        measure_mono (t21_event_subset U A 𝒮 F Ŝ S₀ h𝒮 hŜ)
    _ ≤ P (U ∪ {ω | ω ∉ U ∧ S₀ ∉ 𝒮 ω}) +
          P {ω | ω ∉ U ∧ S₀ ∈ 𝒮 ω ∧ post (F ω) A S₀ ≤ 1 / 2} := measure_union_le _ _
    _ ≤ _ := by gcongr; exact measure_union_le _ _

/-- **T21 decomposition**, the form of the L-LEAN brief:
`P(U ∨ Ŝ ≠ S₀) ≤ P(U) + P(S₀ ∉ 𝒮) + P(Uᶜ ∧ S₀ ∈ 𝒮 ∧ π(S₀) ≤ 1/2)`. -/
theorem t21_decomposition' (P : Measure Ω) (U : Set Ω) (A : Finset M) (𝒮 : Ω → Finset M)
    (F : Ω → M → ℝ) (Ŝ : Ω → M) (S₀ : M) (h𝒮 : ∀ ω ∉ U, 𝒮 ω ⊆ A)
    (hŜ : ∀ ω ∉ U, IsArgmax (F ω) (𝒮 ω) (Ŝ ω)) :
    P (U ∪ {ω | ω ∉ U ∧ Ŝ ω ≠ S₀}) ≤
      P U + P {ω | S₀ ∉ 𝒮 ω} +
        P {ω | ω ∉ U ∧ S₀ ∈ 𝒮 ω ∧ post (F ω) A S₀ ≤ 1 / 2} := by
  refine (t21_decomposition P U A 𝒮 F Ŝ S₀ h𝒮 hŜ).trans ?_
  gcongr
  exact fun ω hω => hω.2

/-- Markov's inequality at level `1/2`: `P(δ ≥ 1/2) ≤ 2 E δ` for an integrable `δ ≥ 0`. -/
theorem markov_half (P : Measure Ω) (δ : Ω → ℝ) (hδ0 : ∀ ω, 0 ≤ δ ω)
    (hint : Integrable δ P) :
    P.real {ω | 1 / 2 ≤ δ ω} ≤ 2 * ∫ ω, δ ω ∂P := by
  have h := mul_meas_ge_le_integral_of_nonneg (μ := P) (Filter.Eventually.of_forall hδ0) hint
    (1 / 2)
  linarith

/-- `δ₁ = 1 - π(S₀)` is measurable when each score `ω ↦ F ω S` is. -/
theorem measurable_post (A : Finset M) (F : Ω → M → ℝ) (S₀ : M)
    (hF : ∀ S, Measurable fun ω => F ω S) : Measurable fun ω => post (F ω) A S₀ := by
  unfold post
  by_cases h : S₀ ∈ A
  · simp only [h, if_true]
    exact (Real.measurable_exp.comp (hF S₀)).div
      (Finset.measurable_sum A fun T _ => Real.measurable_exp.comp (hF T))
  · simp only [h, if_false]
    exact measurable_const

/-- **T21 (C1)**: `P(U or Ŝ ≠ S₀) ≤ P(U) + 2 E δ₁ + P(Uᶜ, S₀ ∉ 𝒮)`, with `δ₁ = 1 - π(S₀)`.
(STATEMENT.md §3 (C1); PROOF_v3 eq. (C1).) -/
theorem t21_C1 (P : Measure Ω) [IsProbabilityMeasure P] (U : Set Ω) (A : Finset M)
    (𝒮 : Ω → Finset M) (F : Ω → M → ℝ) (Ŝ : Ω → M) (S₀ : M)
    (hF : ∀ S, Measurable fun ω => F ω S) (h𝒮 : ∀ ω ∉ U, 𝒮 ω ⊆ A)
    (hŜ : ∀ ω ∉ U, IsArgmax (F ω) (𝒮 ω) (Ŝ ω)) :
    P.real (U ∪ {ω | ω ∉ U ∧ Ŝ ω ≠ S₀}) ≤
      P.real U + 2 * ∫ ω, (1 - post (F ω) A S₀) ∂P + P.real {ω | ω ∉ U ∧ S₀ ∉ 𝒮 ω} := by
  set δ : Ω → ℝ := fun ω => 1 - post (F ω) A S₀ with hδ
  have hδm : Measurable δ := measurable_const.sub (measurable_post A F S₀ hF)
  have hδ0 : ∀ ω, 0 ≤ δ ω := fun ω => by simp only [hδ]; linarith [post_le_one (F := F ω) (A := A) S₀]
  have hδ1 : ∀ ω, ‖δ ω‖ ≤ 1 := fun ω => by
    rw [Real.norm_eq_abs, abs_of_nonneg (hδ0 ω)]
    simp only [hδ]; linarith [post_nonneg (F ω) A S₀]
  have hint : Integrable δ P :=
    Integrable.of_bound hδm.aestronglyMeasurable 1 (Filter.Eventually.of_forall hδ1)
  have hsub : {ω | ω ∉ U ∧ S₀ ∈ 𝒮 ω ∧ post (F ω) A S₀ ≤ 1 / 2} ⊆ {ω | 1 / 2 ≤ δ ω} := by
    intro ω hω
    simp only [Set.mem_setOf_eq, hδ] at hω ⊢
    linarith [hω.2.2]
  have hmain := t21_decomposition P U A 𝒮 F Ŝ S₀ h𝒮 hŜ
  have hreal : P.real (U ∪ {ω | ω ∉ U ∧ Ŝ ω ≠ S₀}) ≤
      P.real U + P.real {ω | ω ∉ U ∧ S₀ ∉ 𝒮 ω} +
        P.real {ω | ω ∉ U ∧ S₀ ∈ 𝒮 ω ∧ post (F ω) A S₀ ≤ 1 / 2} := by
    simp only [measureReal_def]
    rw [← ENNReal.toReal_add (measure_ne_top _ _) (measure_ne_top _ _),
      ← ENNReal.toReal_add (by finiteness) (measure_ne_top _ _)]
    exact ENNReal.toReal_mono (by finiteness) hmain
  have hmk := markov_half P δ hδ0 hint
  have hle : P.real {ω | ω ∉ U ∧ S₀ ∈ 𝒮 ω ∧ post (F ω) A S₀ ≤ 1 / 2} ≤
      P.real {ω | 1 / 2 ≤ δ ω} := measureReal_mono hsub
  linarith

/-- For `0 ≤ δ ≤ 1` and `ε ≥ 0`: `E δ ≤ ε + P(δ > ε)` (PROOF_v3 line 82). -/
theorem integral_le_eps_add_prob (P : Measure Ω) [IsProbabilityMeasure P] (δ : Ω → ℝ)
    (hδm : Measurable δ) (hδ0 : ∀ ω, 0 ≤ δ ω) (hδ1 : ∀ ω, δ ω ≤ 1) (ε : ℝ) (hε : 0 ≤ ε) :
    ∫ ω, δ ω ∂P ≤ ε + P.real {ω | ε < δ ω} := by
  set E := {ω | ε < δ ω} with hE
  have hEm : MeasurableSet E := measurableSet_lt measurable_const hδm
  have hbound : ∀ ω, δ ω ≤ ε + E.indicator (fun _ => (1 : ℝ)) ω := by
    intro ω
    by_cases h : ω ∈ E
    · rw [Set.indicator_of_mem h]; linarith [hδ1 ω]
    · rw [Set.indicator_of_notMem h]; simp only [hE, Set.mem_setOf_eq, not_lt] at h; linarith
  have hint : Integrable δ P := Integrable.of_bound hδm.aestronglyMeasurable 1
    (Filter.Eventually.of_forall fun ω => by
      rw [Real.norm_eq_abs, abs_of_nonneg (hδ0 ω)]; exact hδ1 ω)
  have hint2 : Integrable (fun ω => ε + E.indicator (fun _ => (1 : ℝ)) ω) P :=
    (integrable_const ε).add ((integrable_const (1 : ℝ)).indicator hEm)
  calc ∫ ω, δ ω ∂P ≤ ∫ ω, (ε + E.indicator (fun _ => (1 : ℝ)) ω) ∂P :=
        integral_mono hint hint2 hbound
    _ = ε + P.real E := by
        rw [integral_add (integrable_const ε) ((integrable_const (1 : ℝ)).indicator hEm),
          integral_const, integral_indicator_one hEm]
        simp

end SmcBvs
