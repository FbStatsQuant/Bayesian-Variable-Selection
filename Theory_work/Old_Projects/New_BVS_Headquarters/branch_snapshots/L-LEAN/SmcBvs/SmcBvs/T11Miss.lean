import Mathlib.Probability.Independence.Basic
import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.Analysis.Complex.Exponential

/-!
# T11(iii): miss probability of `Q` iid `π₀` draws

Source: `Docs/Theory/proofs/T11_LLED_scoring_ledger/STATEMENT.md`, "Claim (iii)":
`P(S* is not among the Q_f final iid draws | 𝓒) = (1 − π₀(S*))^{Q_f} ≤ exp(−Q_f π₀(S*))`.

Abstract version. Given the frozen calibration `𝓒`, `Q = Q_f` is a fixed natural number, `S*` a
fixed model and the designated draws are iid with law `π₀` (this is what EX-S, CAL and START give;
STATEMENT.md "Setting"). We state the claim in two forms:
* `t11_miss_pi`  : on the canonical product space `(Fin Q → M, ⊗ π₀)`;
* `t11_miss_iid` : for any family `X : Fin Q → Ω → M` of independent random variables, each with
  law `π₀`, on a probability space `(Ω, P)`;
and the exponential bound `t11_pow_le_exp`.
The conditional-on-`𝓒` statement is the pointwise application of these with `π₀`, `Q`, `S*`
fixed by `𝓒` (see ASSUMPTIONS.md, A-T11-1).
-/

open MeasureTheory ProbabilityTheory

namespace SmcBvs

variable {M : Type*} [MeasurableSpace M] [MeasurableSingletonClass M]

/-- Elementary bound `(1 - a)^Q ≤ exp(-Q a)` for `a ≤ 1`. -/
theorem t11_pow_le_exp (a : ℝ) (ha : a ≤ 1) (Q : ℕ) :
    (1 - a) ^ Q ≤ Real.exp (-(Q * a)) := by
  have h0 : 0 ≤ 1 - a := by linarith
  have h1 : 1 - a ≤ Real.exp (-a) := by linarith [Real.add_one_le_exp (-a)]
  calc (1 - a) ^ Q ≤ (Real.exp (-a)) ^ Q := pow_le_pow_left₀ h0 h1 Q
    _ = Real.exp (-(Q * a)) := by rw [← Real.exp_nat_mul]; ring_nf

/-- **T11(iii), product-space form.** Under `Q` iid draws from `π₀`, the probability that the
fixed model `s` is never drawn is `(1 - π₀{s})^Q`. -/
theorem t11_miss_pi (π₀ : Measure M) [IsProbabilityMeasure π₀] (Q : ℕ) (s : M) :
    (Measure.pi fun _ : Fin Q => π₀) {x | ∀ i, x i ≠ s} = (1 - π₀ {s}) ^ Q := by
  have hset : {x : Fin Q → M | ∀ i, x i ≠ s} = Set.univ.pi fun _ => ({s}ᶜ : Set M) := by
    ext x; simp
  rw [hset, Measure.pi_pi, prob_compl_eq_one_sub (measurableSet_singleton s)]
  simp

/-- **T11(iii), product-space form, real-valued with the exponential bound.** -/
theorem t11_miss_pi_real (π₀ : Measure M) [IsProbabilityMeasure π₀] (Q : ℕ) (s : M) :
    (Measure.pi fun _ : Fin Q => π₀).real {x | ∀ i, x i ≠ s} = (1 - π₀.real {s}) ^ Q ∧
      (1 - π₀.real {s}) ^ Q ≤ Real.exp (-(Q * π₀.real {s})) := by
  refine ⟨?_, t11_pow_le_exp _ measureReal_le_one Q⟩
  rw [measureReal_def, t11_miss_pi, ENNReal.toReal_pow, ENNReal.toReal_sub_of_le prob_le_one
    ENNReal.one_ne_top]
  simp [measureReal_def]

variable {Ω : Type*} [MeasurableSpace Ω]

/-- **T11(iii), random-variable form.** If `X 0, …, X (Q-1)` are independent, each with law `π₀`,
then `P(s ∉ {X i}) = (1 - π₀{s})^Q`. -/
theorem t11_miss_iid (P : Measure Ω) [IsProbabilityMeasure P] (π₀ : Measure M) (Q : ℕ)
    (X : Fin Q → Ω → M) (hXm : ∀ i, Measurable (X i)) (hind : iIndepFun X P)
    (hlaw : ∀ i, P.map (X i) = π₀) (s : M) :
    P {ω | ∀ i, X i ω ≠ s} = (1 - π₀ {s}) ^ Q := by
  have hset : {ω | ∀ i, X i ω ≠ s} = ⋂ i, X i ⁻¹' ({s}ᶜ : Set M) := by
    ext ω; simp
  have hmeas : MeasurableSet ({s}ᶜ : Set M) := (measurableSet_singleton s).compl
  rw [hset, hind.meas_iInter (fun i => ⟨{s}ᶜ, hmeas, rfl⟩)]
  have hi : ∀ i, P (X i ⁻¹' ({s}ᶜ : Set M)) = 1 - π₀ {s} := by
    intro i
    have hπ₀ : IsProbabilityMeasure π₀ := by
      rw [← hlaw i]; infer_instance
    rw [← Measure.map_apply (hXm i) hmeas, hlaw i,
      prob_compl_eq_one_sub (measurableSet_singleton s)]
  simp only [hi, Finset.prod_const, Finset.card_univ, Fintype.card_fin]

/-- **T11(iii), random-variable form, real-valued with the exponential bound.** -/
theorem t11_miss_iid_real (P : Measure Ω) [IsProbabilityMeasure P] (π₀ : Measure M)
    [IsProbabilityMeasure π₀] (Q : ℕ)
    (X : Fin Q → Ω → M) (hXm : ∀ i, Measurable (X i)) (hind : iIndepFun X P)
    (hlaw : ∀ i, P.map (X i) = π₀) (s : M) :
    P.real {ω | ∀ i, X i ω ≠ s} = (1 - π₀.real {s}) ^ Q ∧
      (1 - π₀.real {s}) ^ Q ≤ Real.exp (-(Q * π₀.real {s})) := by
  refine ⟨?_, t11_pow_le_exp _ measureReal_le_one Q⟩
  rw [measureReal_def, t11_miss_iid P π₀ Q X hXm hind hlaw s, ENNReal.toReal_pow,
    ENNReal.toReal_sub_of_le prob_le_one ENNReal.one_ne_top]
  simp [measureReal_def]

end SmcBvs
