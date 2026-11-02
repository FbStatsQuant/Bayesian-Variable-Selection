import Mathlib

/-!
# Shared finite objects for the SMC-BVS formalisation

* `post F A S`   : the posterior `π(S) = exp(F S) / Σ_{T ∈ A} exp(F T)` on a finite model set `A`
                   (and `0` off `A`).
* `IsLeastArgmax rk g A S` : `S` is the `≺`-least element of `argmax_A g`, where the fixed total
  tie order `≺` is encoded by an injective rank `rk` (smaller rank = preferred). Every total order
  on a finite set is of this form, so this is the method's tie rule "smaller size, then
  lexicographically smaller index list" as one instance.

Sources: `Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md` §1 and
`Docs/Theory/proofs/T06_T07_identifiability_size_prior/STATEMENT.md` §0.
-/

open Finset

namespace SmcBvs

variable {M : Type*} [DecidableEq M]

/-- Posterior `π(S) = e^{F(S)} / Σ_{T∈A} e^{F(T)}` on the finite model set `A`, and `0` off `A`. -/
noncomputable def post (F : M → ℝ) (A : Finset M) (S : M) : ℝ :=
  if S ∈ A then Real.exp (F S) / ∑ T ∈ A, Real.exp (F T) else 0

/-- `S` maximises `g` over `A`. -/
def IsArgmax (g : M → ℝ) (A : Finset M) (S : M) : Prop :=
  S ∈ A ∧ ∀ T ∈ A, g T ≤ g S

/-- `S` is the `≺`-least element of `argmax_A g`, with `≺` given by the injective rank `rk`. -/
def IsLeastArgmax (rk : M → ℕ) (g : M → ℝ) (A : Finset M) (S : M) : Prop :=
  IsArgmax g A S ∧ ∀ T, IsArgmax g A T → rk S ≤ rk T


/-! ### Least argmax: uniqueness and existence -/

theorem IsLeastArgmax.unique {rk : M → ℕ} (hrk : Function.Injective rk) {g : M → ℝ}
    {A : Finset M} {S T : M} (hS : IsLeastArgmax rk g A S) (hT : IsLeastArgmax rk g A T) :
    S = T :=
  hrk (le_antisymm (hS.2 T hT.1) (hT.2 S hS.1))

theorem exists_isLeastArgmax (rk : M → ℕ) (g : M → ℝ) {A : Finset M} (hA : A.Nonempty) :
    ∃ S, IsLeastArgmax rk g A S := by
  classical
  obtain ⟨S₁, hS₁A, hS₁⟩ := A.exists_max_image g hA
  set B := A.filter (fun S => ∀ T ∈ A, g T ≤ g S) with hB
  have hBne : B.Nonempty := ⟨S₁, by simp [hB, hS₁A, hS₁]⟩
  obtain ⟨S, hSB, hS⟩ := B.exists_min_image rk hBne
  rw [hB, mem_filter] at hSB
  refine ⟨S, ⟨hSB.1, hSB.2⟩, fun T hT => hS T ?_⟩
  rw [hB, mem_filter]
  exact ⟨hT.1, hT.2⟩

/-- An argmax of `g` over `A` that is a strict maximiser over a superset is the strict one. -/
theorem IsArgmax.eq_of_strict {g : M → ℝ} {A : Finset M} {S₀ S : M} (hS₀ : S₀ ∈ A)
    (hstrict : ∀ T ∈ A, T ≠ S₀ → g T < g S₀) (hS : IsArgmax g A S) : S = S₀ := by
  by_contra hne
  have h1 := hstrict S hS.1 hne
  have h2 := hS.2 S₀ hS₀
  linarith

/-! ### The posterior -/

theorem post_of_mem {F : M → ℝ} {A : Finset M} {S : M} (hS : S ∈ A) :
    post F A S = Real.exp (F S) / ∑ T ∈ A, Real.exp (F T) := by
  simp [post, hS]

theorem post_of_not_mem {F : M → ℝ} {A : Finset M} {S : M} (hS : S ∉ A) :
    post F A S = 0 := by
  simp [post, hS]

theorem sum_exp_pos {F : M → ℝ} {A : Finset M} (hA : A.Nonempty) :
    0 < ∑ T ∈ A, Real.exp (F T) :=
  Finset.sum_pos (fun T _ => Real.exp_pos (F T)) hA

theorem post_nonneg (F : M → ℝ) (A : Finset M) (S : M) : 0 ≤ post F A S := by
  unfold post
  split_ifs
  · exact div_nonneg (Real.exp_pos _).le (Finset.sum_nonneg fun T _ => (Real.exp_pos _).le)
  · exact le_rfl

theorem post_sum {F : M → ℝ} {A : Finset M} (hA : A.Nonempty) :
    ∑ S ∈ A, post F A S = 1 := by
  rw [Finset.sum_congr rfl (fun S hS => post_of_mem (F := F) hS), ← Finset.sum_div]
  exact div_self (sum_exp_pos hA).ne'

theorem post_le_one {F : M → ℝ} {A : Finset M} (S : M) : post F A S ≤ 1 := by
  by_cases hS : S ∈ A
  · have hA : A.Nonempty := ⟨S, hS⟩
    rw [← post_sum (F := F) hA]
    exact Finset.single_le_sum (fun T _ => post_nonneg F A T) hS
  · rw [post_of_not_mem hS]; norm_num

/-- If `π(S₀) > 1/2` then `S₀ ∈ A` and `S₀` is the strict maximiser of `F` on `A`
(T21 PROOF_v3 lines 64–68; T06(ii)(a)). -/
theorem strict_max_of_post_gt_half {F : M → ℝ} {A : Finset M} {S₀ : M}
    (h : 1 / 2 < post F A S₀) : S₀ ∈ A ∧ ∀ S ∈ A, S ≠ S₀ → F S < F S₀ := by
  have hS₀ : S₀ ∈ A := by
    by_contra hn
    rw [post_of_not_mem hn] at h
    norm_num at h
  refine ⟨hS₀, fun S hS hne => ?_⟩
  have hA : A.Nonempty := ⟨S₀, hS₀⟩
  -- π(S) + π(S₀) ≤ 1
  have hpair : post F A S + post F A S₀ ≤ 1 := by
    rw [← post_sum (F := F) hA, ← Finset.sum_pair hne]
    exact Finset.sum_le_sum_of_subset_of_nonneg
      (by intro x hx; simp only [Finset.mem_insert, Finset.mem_singleton] at hx
          rcases hx with rfl | rfl <;> assumption)
      (fun T _ _ => post_nonneg F A T)
  have hlt : post F A S < post F A S₀ := by linarith
  rw [post_of_mem hS, post_of_mem hS₀] at hlt
  have := (div_lt_div_iff_of_pos_right (sum_exp_pos (F := F) hA)).mp hlt
  exact Real.exp_lt_exp.mp this

end SmcBvs
