import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.BigOperators.Field
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-!
# T12(i.a): unbiasedness of the frozen-run evidence — deterministic core and reduction

Source: `Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md` §3 (i.a):
"For every c, t ∈ {0, …, T} and f : Ω → ℝ: E_c[Ẑ_t q̂_t(f)] = Z_t q_t(f). In particular
E_c[Ẑ] = Z."

**Status: partial.** This file formalises, sorry-free,
1. the invariance algebra `γ_{t-1}(G_t · K_t f) = γ_t(f)` (`invariance_step`);
2. the one-step resample–move identity for a fixed population (`resample_move_step`):
   with `Ẑ' = Ẑ · (1/N) Σ_k G(x_k)` and each new particle having marginal
   `Σ_k (G(x_k)/Σ_l G(x_l)) K(x_k, ·)`,
   `Ẑ' · (1/N) Σ_i E f(Y_i) = Ẑ · (1/N) Σ_k G(x_k) (K f)(x_k)`;
3. the induction (`unbiased_of_step`): if the expectation functionals `E_t f := E_c[Ẑ_t q̂_t(f)]`
   satisfy the stage-0 identity and the one-step recursion `E_t f = E_{t-1}(G_t · K_t f)`, then
   `E_t f = Σ_x γ_t(x) f(x) = Z_t q_t(f)` for all `t ≤ T`.

**Not formalised (TODO, see `T12_PLAN.md`)**: the derivation of the recursion hypothesis
`hstep` from a probabilistic model of the island (multinomial resampling, conditionally
independent rounds (R2)–(R3), tower property). The recursion is the conditional-expectation form
of (2); it enters `unbiased_of_step` as an explicit hypothesis, never as an axiom.
-/

open Finset

namespace SmcBvs.T12

variable {α : Type*} [Fintype α]

/-- Apply a (row-stochastic) kernel matrix to a test function: `(K f)(x) = Σ_y K(x,y) f(y)`. -/
def kapply (K : α → α → ℝ) (f : α → ℝ) (x : α) : ℝ := ∑ y, K x y * f y

/-- `γ`-invariance of a kernel: `Σ_x γ(x) K(x,y) = γ(y)`. -/
def Invariant (γ : α → ℝ) (K : α → α → ℝ) : Prop := ∀ y, ∑ x, γ x * K x y = γ y

/-- **Invariance step**: if `γ_t = γ_{t-1} · G_t` and `K_t` is `γ_t`-invariant then
`Σ_x γ_{t-1}(x) G_t(x) (K_t f)(x) = Σ_y γ_t(y) f(y)`. -/
theorem invariance_step (γprev γ G : α → ℝ) (K : α → α → ℝ) (hγ : ∀ x, γ x = γprev x * G x)
    (hK : Invariant γ K) (f : α → ℝ) :
    ∑ x, γprev x * G x * kapply K f x = ∑ y, γ y * f y := by
  simp only [kapply, Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun y _ => ?_
  rw [← hK y, Finset.sum_mul]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [hγ x]; ring

/-- **One-step resample–move identity** for a fixed population `x : Fin N → α` with positive
total weight: the new evidence `Ẑ' = Ẑ (1/N) Σ_k G(x_k)` times the mean over `N` particles of the
mixture-marginal expectation equals `Ẑ (1/N) Σ_k G(x_k) (K f)(x_k)`. -/
theorem resample_move_step {N : ℕ} (x : Fin N → α) (G : α → ℝ) (K : α → α → ℝ) (Zhat : ℝ)
    (hG : 0 < ∑ k, G (x k)) (f : α → ℝ) :
    (Zhat * ((1 / N) * ∑ k, G (x k))) *
        ((1 / N) * ∑ _i : Fin N, ∑ k, (G (x k) / ∑ l, G (x l)) * kapply K f (x k)) =
      Zhat * ((1 / N) * ∑ k, G (x k) * kapply K f (x k)) := by
  have hNpos : (0 : ℝ) < N := by
    rcases Nat.eq_zero_or_pos N with h | h
    · subst h; simp at hG
    · exact_mod_cast h
  set SG := ∑ k, G (x k) with hSG
  have hmix : ∑ k, (G (x k) / SG) * kapply K f (x k) = (∑ k, G (x k) * kapply K f (x k)) / SG := by
    rw [Finset.sum_div]
    exact Finset.sum_congr rfl fun k _ => by ring
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, hmix]
  field_simp

/-- **T12(i.a), reduction**: if the functionals `E t f` (standing for `E_c[Ẑ_t q̂_t(f)]`) are
given at stage 0 by `E 0 f = Σ γ₀ f` (stage 0: `Ẑ₀ = Z₀ = Σ γ₀` and the particles are iid
`π₀ = γ₀/Z₀`, so `E[Ẑ₀ q̂₀(f)] = Z₀ π₀(f) = Σ γ₀ f`; here `γ₀` includes the factor `m(∅)`) and satisfy the resample–move recursion
`E t f = E (t-1) (G_t · K_t f)`, with `γ_t = γ_{t-1} G_t` and `K_t` `γ_t`-invariant, then
`E t f = Σ_x γ_t(x) f(x)` (`= Z_t q_t(f)`) for every `t`. -/
theorem unbiased_of_step (γ : ℕ → α → ℝ) (G : ℕ → α → ℝ) (K : ℕ → α → α → ℝ)
    (hγ : ∀ t x, γ (t + 1) x = γ t x * G (t + 1) x) (hK : ∀ t, Invariant (γ (t + 1)) (K (t + 1)))
    (E : ℕ → (α → ℝ) → ℝ) (h0 : ∀ f, E 0 f = ∑ x, γ 0 x * f x)
    (hstep : ∀ t f, E (t + 1) f = E t (fun x => G (t + 1) x * kapply (K (t + 1)) f x)) :
    ∀ t f, E t f = ∑ x, γ t x * f x := by
  intro t
  induction t with
  | zero => exact h0
  | succ t ih =>
    intro f
    rw [hstep, ih]
    rw [← invariance_step (γ t) (γ (t + 1)) (G (t + 1)) (K (t + 1)) (hγ t) (hK t) f]
    refine Finset.sum_congr rfl fun x _ => ?_
    ring

end SmcBvs.T12
