import Mathlib

/-!
# T37(i) / Theorem A: deterministic greedy repair — abstract combinatorial core

Source: branch `theory/W1-T37R`, `theory_campaign/W1-T37R/PROOF.md`, "Lemma 0", "Definitions for
the refined statement" and "Theorem A (refined T37(i))", with the repairs of branch
`theory/W3-VT37R`, `theory_campaign/W3-VT37R/REPAIRS.md` R1 (POS, only for A5, not used here) and
R3 ("ℓ ≥ τ(S_c) suffices"; TD′_P is sufficient, not claimed necessary, for reaching within Φ).

Abstract setting (EX-A: exact scores and comparisons; data fixed):
* `α` the states (models), `N : α → Finset α` the feasible neighbourhood (flips and swaps),
  `F : α → ℝ` the log-score;
* `M : α → Option α` a **best-improvement map**: `M S = none` iff no neighbour strictly improves
  `F`; otherwise `M S = some T` with `T` a neighbour of maximal score and `F T > F S`. Any tie rule
  is allowed (`IsBestImprovement`); one exists for every injective rank (`exists_bestImprovement`),
  e.g. the method's lexicographic rule;
* the greedy path `path M S k = (step M)^[k] S`, where `step M S = (M S).getD S` (a state with no
  improving neighbour is a fixed point, so the path "stops" there);
* the production search with move cap `ℓ` returns `path M S_c ℓ` and is *certified* when the
  returned centre has no improving neighbour (`M (path M S_c ℓ) = none`).

Results
* `path_F_strictMono`   (Lemma 0(a)): `F` strictly increases along the moves actually made.
* `theoremA1`           (A1, ⇒): under TD′_∞(R), from `S ∈ R` the path stays in `R` and reaches
  `S₀` within `r_R(S) = #{S' ∈ R : F S' > F S}` moves.
* `theoremA1_converse`  (A1, ⇐).
* `theoremA2`           (A2): under TD′_P(R) (with `Φ : α → ℕ`), from `S ∈ R` the path stays in
  `R`, `Φ` strictly decreases at each move, and `S₀` is reached after `τ ≤ Φ(S)` moves.
* `theoremA3`           (A3): if moreover `ℓ ≥ τ` (in particular `ℓ ≥ Φ(S_c)`), the capped search
  from `S_c` returns `S₀` certified, and every model scored by the search has `F ≤ F(S₀)`
  (Lemma 0(c)).
* `pd_of_reach`         (A4, PD part): reaching `S₀` from `S ≠ S₀` forces `F S < F S₀`.
-/

namespace SmcBvs.Greedy

variable {α : Type*}

/-- `M` is a best strict-improvement map for neighbourhood `N` and score `F` (any tie rule). -/
structure IsBestImprovement (N : α → Finset α) (F : α → ℝ) (M : α → Option α) : Prop where
  none_iff : ∀ S, M S = none ↔ ∀ T ∈ N S, F T ≤ F S
  some_mem : ∀ S T, M S = some T → T ∈ N S
  some_lt : ∀ S T, M S = some T → F S < F T
  some_max : ∀ S T, M S = some T → ∀ T' ∈ N S, F T' ≤ F T

/-- One greedy move (identity at a state with no improving neighbour). -/
def step (M : α → Option α) (S : α) : α := (M S).getD S

/-- The greedy path from `S`. -/
def path (M : α → Option α) (S : α) (k : ℕ) : α := (step M)^[k] S

theorem path_zero (M : α → Option α) (S : α) : path M S 0 = S := rfl

theorem path_succ (M : α → Option α) (S : α) (k : ℕ) :
    path M S (k + 1) = step M (path M S k) := by
  simp only [path, Function.iterate_succ_apply']

theorem step_of_some {M : α → Option α} {S T : α} (h : M S = some T) : step M S = T := by
  simp [step, h]

theorem step_of_none {M : α → Option α} {S : α} (h : M S = none) : step M S = S := by
  simp [step, h]

/-- Once the path is at a fixed point it stays there. -/
theorem path_stays {M : α → Option α} {S : α} {k : ℕ} (h : M (path M S k) = none) :
    ∀ j, k ≤ j → path M S j = path M S k := by
  intro j hj
  induction j, hj using Nat.le_induction with
  | base => rfl
  | succ j hkj ih => rw [path_succ, ih, step_of_none h]

/-- Existence of a best-improvement map for any injective tie rank (e.g. lexicographic). -/
theorem exists_bestImprovement (N : α → Finset α) (F : α → ℝ) :
    ∃ M : α → Option α, IsBestImprovement N F M := by
  classical
  -- for each S choose a neighbour of maximal score among the strict improvements, if any
  let imp : α → Finset α := fun S => (N S).filter fun T => F S < F T
  have hchoice : ∀ S, (imp S).Nonempty → ∃ T ∈ imp S, ∀ T' ∈ imp S, F T' ≤ F T :=
    fun S h => (imp S).exists_max_image F h
  let M : α → Option α := fun S =>
    if h : (imp S).Nonempty then some (Classical.choose (hchoice S h)) else none
  refine ⟨M, ?_, ?_, ?_, ?_⟩
  · intro S
    by_cases h : (imp S).Nonempty
    · simp only [M, h, dite_true, reduceCtorEq, false_iff, not_forall, not_le]
      obtain ⟨T, hT⟩ := h
      simp only [imp, Finset.mem_filter] at hT
      exact ⟨T, hT.1, hT.2⟩
    · simp only [M, h, dite_false, true_iff]
      intro T hT
      by_contra hlt
      exact h ⟨T, by simp only [imp, Finset.mem_filter]; exact ⟨hT, lt_of_not_ge hlt⟩⟩
  · intro S T hST
    by_cases h : (imp S).Nonempty
    · simp only [M, h, dite_true, Option.some.injEq] at hST
      have := (Classical.choose_spec (hchoice S h)).1
      rw [hST] at this
      exact (Finset.mem_filter.mp this).1
    · simp [M, h] at hST
  · intro S T hST
    by_cases h : (imp S).Nonempty
    · simp only [M, h, dite_true, Option.some.injEq] at hST
      have := (Classical.choose_spec (hchoice S h)).1
      rw [hST] at this
      exact (Finset.mem_filter.mp this).2
    · simp [M, h] at hST
  · intro S T hST T' hT'
    by_cases h : (imp S).Nonempty
    · simp only [M, h, dite_true, Option.some.injEq] at hST
      have hspec := Classical.choose_spec (hchoice S h)
      rw [hST] at hspec
      by_cases hlt : F S < F T'
      · exact hspec.2 T' (Finset.mem_filter.mpr ⟨hT', hlt⟩)
      · have := (Finset.mem_filter.mp hspec.1).2
        linarith [not_lt.mp hlt]
    · simp [M, h] at hST

variable {N : α → Finset α} {F : α → ℝ} {M : α → Option α}

/-- **Lemma 0(a)**: every move made strictly increases the score. -/
theorem path_F_le (hM : IsBestImprovement N F M) (S : α) (k : ℕ) :
    F (path M S k) ≤ F (path M S (k + 1)) := by
  rw [path_succ]
  cases h : M (path M S k) with
  | none => rw [step_of_none h]
  | some T => rw [step_of_some h]; exact (hM.some_lt _ _ h).le

theorem path_F_mono (hM : IsBestImprovement N F M) (S : α) : Monotone fun k => F (path M S k) :=
  monotone_nat_of_le_succ (path_F_le hM S)

/-- **Lemma 0(a)**, strict form: if a move is made at step `k`, then `F` strictly increases
from step `k` to every later step. -/
theorem path_F_strictMono (hM : IsBestImprovement N F M) (S : α) {k j : ℕ} (hkj : k < j)
    (hmove : M (path M S k) ≠ none) : F (path M S k) < F (path M S j) := by
  obtain ⟨T, hT⟩ := Option.ne_none_iff_exists'.mp hmove
  have h1 : F (path M S k) < F (path M S (k + 1)) := by
    rw [path_succ, step_of_some hT]; exact hM.some_lt _ _ hT
  exact lt_of_lt_of_le h1 (path_F_mono hM S hkj)

/-! ### TD′_∞ and (A1) -/

/-- **TD′_∞(R)** (W1-T37R PROOF.md, Definitions): (L) `S₀` has no strictly improving neighbour;
(N) every other state of `R` has a greedy move, and it lands in `R`. -/
def TDinf (M : α → Option α) (R : Finset α) (S₀ : α) : Prop :=
  M S₀ = none ∧ ∀ S ∈ R, S ≠ S₀ → ∃ T, M S = some T ∧ T ∈ R

/-- `r_R(S) = #{S' ∈ R : F S' > F S}`. -/
noncomputable def rankAbove (F : α → ℝ) (R : Finset α) (S : α) : ℕ :=
  ((R.filter fun S' => F S < F S').card)

/-- Under TD′_∞(R) the path from a state of `R` stays in `R` (before and after reaching `S₀`). -/
theorem path_mem_of_TDinf (hTD : TDinf M R S₀) {S : α} (hS : S ∈ R) (hS₀ : S₀ ∈ R) :
    ∀ k, path M S k ∈ R := by
  intro k
  induction k with
  | zero => exact hS
  | succ k ih =>
    rw [path_succ]
    by_cases h0 : path M S k = S₀
    · rw [h0, step_of_none hTD.1]; exact hS₀
    · obtain ⟨T, hT, hTR⟩ := hTD.2 _ ih h0
      rw [step_of_some hT]; exact hTR

/-- **Theorem A (A1, ⇒)**. Under TD′_∞(R), from `S ∈ R` the greedy path stays in `R` and reaches
`S₀` after at most `r_R(S)` moves, and then stays at `S₀` (terminates there). -/
theorem theoremA1 [DecidableEq α] (hM : IsBestImprovement N F M) {R : Finset α} {S₀ : α}
    (hTD : TDinf M R S₀) (hS₀ : S₀ ∈ R) {S : α} (hS : S ∈ R) :
    (∀ k, path M S k ∈ R) ∧ ∃ τ ≤ rankAbove F R S, path M S τ = S₀ ∧
      ∀ j, τ ≤ j → path M S j = S₀ := by
  classical
  have hmem := path_mem_of_TDinf hTD hS hS₀
  refine ⟨hmem, ?_⟩
  -- first show `S₀` is hit within `r` steps
  suffices h : ∃ τ ≤ rankAbove F R S, path M S τ = S₀ by
    obtain ⟨τ, hτ, hp⟩ := h
    refine ⟨τ, hτ, hp, fun j hj => ?_⟩
    rw [path_stays (by rw [hp]; exact hTD.1) j hj, hp]
  by_contra hcon
  push_neg at hcon
  set r := rankAbove F R S
  -- all steps `0..r` are moves
  have hmove : ∀ k ≤ r, M (path M S k) ≠ none := by
    intro k hk
    obtain ⟨T, hT, -⟩ := hTD.2 _ (hmem k) (hcon k hk)
    rw [hT]; exact Option.some_ne_none T
  -- the states `path 1, …, path (r+1)` are distinct elements of `{S' ∈ R : F S < F S'}`
  have hinj : Set.InjOn (fun k => path M S (k + 1)) (Finset.range (r + 1) : Set ℕ) := by
    intro a ha b hb hab
    simp only [Finset.coe_range, Set.mem_Iio] at ha hb
    by_contra hne
    rcases lt_or_gt_of_ne hne with h | h
    · have := path_F_strictMono hM S (Nat.succ_lt_succ h) (hmove (a + 1) (by omega))
      simp only at hab; rw [hab] at this; exact lt_irrefl _ this
    · have := path_F_strictMono hM S (Nat.succ_lt_succ h) (hmove (b + 1) (by omega))
      simp only at hab; rw [hab] at this; exact lt_irrefl _ this
  have hmaps : Set.MapsTo (fun k => path M S (k + 1)) (Finset.range (r + 1) : Set ℕ)
      (R.filter fun S' => F S < F S' : Finset α) := by
    intro k hk
    simp only [Finset.coe_filter, Set.mem_setOf_eq]
    refine ⟨hmem _, ?_⟩
    have := path_F_strictMono hM S (Nat.succ_pos k) (hmove 0 (Nat.zero_le _))
    rwa [path_zero] at this
  have hcard := Finset.card_le_card_of_injOn _ hmaps hinj
  simp only [Finset.card_range] at hcard
  have : (R.filter fun S' => F S < F S').card = r := rfl
  omega

/-- **Theorem A (A1, ⇐)**. If from every `S ∈ R` the greedy path stays in `R` and terminates at
`S₀` (reaches `S₀`, where no improving move exists), then TD′_∞(R) holds. -/
theorem theoremA1_converse {R : Finset α} {S₀ : α}
    (h : ∀ S ∈ R, (∀ k, path M S k ∈ R) ∧ ∃ τ, path M S τ = S₀ ∧ M S₀ = none)
    (hS₀ : S₀ ∈ R) : TDinf M R S₀ := by
  refine ⟨((h S₀ hS₀).2.choose_spec).2, fun S hS hne => ?_⟩
  obtain ⟨hmem, τ, hτ, -⟩ := h S hS
  cases hMS : M S with
  | none =>
    exfalso
    have := path_stays (M := M) (S := S) (k := 0) (by rw [path_zero]; exact hMS) τ (Nat.zero_le _)
    rw [hτ, path_zero] at this
    exact hne this.symm
  | some T =>
    refine ⟨T, rfl, ?_⟩
    have := hmem 1
    rwa [path_succ, path_zero, step_of_some hMS] at this

/-! ### TD′_P, (A2) and (A3) -/

/-- **TD′_P(R)** with potential `Φ` (W1-T37R PROOF.md, Definitions; closure of `R` under the
progress moves is part of the hypothesis here; for `R = R_{a,d}` it is Lemma 2(a), proved in
`SmcBvs.T37Lattice`). -/
def TDP (M : α → Option α) (Φ : α → ℕ) (R : Finset α) (S₀ : α) : Prop :=
  M S₀ = none ∧ ∀ S ∈ R, S ≠ S₀ → ∃ T, M S = some T ∧ T ∈ R ∧ Φ T < Φ S

/-- **Theorem A (A2)**. Under TD′_P(R), from `S ∈ R` the greedy path reaches `S₀` after
`τ ≤ Φ(S)` moves; before that it stays in `R`, every step is a move, and `Φ` strictly decreases;
afterwards it stays at `S₀`. -/
theorem theoremA2 {Φ : α → ℕ} {R : Finset α} {S₀ : α} (hTD : TDP M Φ R S₀) (hS₀ : S₀ ∈ R)
    {S : α} (hS : S ∈ R) :
    ∃ τ ≤ Φ S, path M S τ = S₀ ∧
      (∀ k, path M S k ∈ R) ∧
      (∀ k < τ, M (path M S k) = some (path M S (k + 1)) ∧
        Φ (path M S (k + 1)) < Φ (path M S k)) ∧
      (∀ j, τ ≤ j → path M S j = S₀) := by
  classical
  -- membership in R for all k
  have hmem : ∀ k, path M S k ∈ R := by
    intro k
    induction k with
    | zero => exact hS
    | succ k ih =>
      rw [path_succ]
      by_cases h0 : path M S k = S₀
      · rw [h0, step_of_none hTD.1]; exact hS₀
      · obtain ⟨T, hT, hTR, -⟩ := hTD.2 _ ih h0
        rw [step_of_some hT]; exact hTR
  -- while not at S₀, Φ drops
  have hdrop : ∀ k, path M S k ≠ S₀ →
      M (path M S k) = some (path M S (k + 1)) ∧ Φ (path M S (k + 1)) < Φ (path M S k) := by
    intro k hk
    obtain ⟨T, hT, -, hΦ⟩ := hTD.2 _ (hmem k) hk
    rw [path_succ, step_of_some hT]
    exact ⟨hT, hΦ⟩
  -- S₀ is hit within Φ S steps
  have hhit : ∃ k ≤ Φ S, path M S k = S₀ := by
    by_contra hcon
    push_neg at hcon
    have hbound : ∀ k ≤ Φ S, Φ (path M S k) + k ≤ Φ S := by
      intro k hk
      induction k with
      | zero => simp [path_zero]
      | succ k ih =>
        have := (hdrop k (hcon k (by omega))).2
        have := ih (by omega)
        omega
    have h1 := hbound (Φ S) le_rfl
    have h2 := (hdrop (Φ S) (hcon (Φ S) le_rfl)).2
    omega
  -- take the first hitting time
  let τ := Nat.find hhit
  have hτspec : τ ≤ Φ S ∧ path M S τ = S₀ := Nat.find_spec hhit
  have hτmin : ∀ k < τ, path M S k ≠ S₀ := fun k hk h =>
    Nat.find_min hhit hk ⟨by have := hτspec.1; omega, h⟩
  refine ⟨τ, hτspec.1, hτspec.2, hmem, fun k hk => hdrop k (hτmin k hk), fun j hj => ?_⟩
  rw [path_stays (by rw [hτspec.2]; exact hTD.1) j hj, hτspec.2]

/-- **Theorem A (A3)** with **Lemma 0(c)**. Under TD′_P(R), from a centre `S_c ∈ R`, let `τ` be
the number of moves to `S₀` (from A2). If the cap satisfies `ℓ ≥ τ` (in particular if
`ℓ ≥ Φ(S_c)`), the capped search returns `S₀` and is certified (`M S₀ = none`). Moreover every
model scored by the search up to that point (each centre `path k`, `k ≤ τ`, and each neighbour it
scans) has score `≤ F(S₀)`. -/
theorem theoremA3 (hM : IsBestImprovement N F M) {Φ : α → ℕ} {R : Finset α} {S₀ : α}
    (hTD : TDP M Φ R S₀) (hS₀ : S₀ ∈ R) {Sc : α} (hSc : Sc ∈ R) :
    ∃ τ ≤ Φ Sc, (∀ ℓ, τ ≤ ℓ → path M Sc ℓ = S₀ ∧ M (path M Sc ℓ) = none) ∧
      (∀ k ≤ τ, F (path M Sc k) ≤ F S₀ ∧ ∀ T ∈ N (path M Sc k), F T ≤ F S₀) := by
  obtain ⟨τ, hτΦ, hτ, -, hmoves, hstay⟩ := theoremA2 hTD hS₀ hSc
  refine ⟨τ, hτΦ, fun ℓ hℓ => ⟨hstay ℓ hℓ, by rw [hstay ℓ hℓ]; exact hTD.1⟩, ?_⟩
  intro k hk
  have hFk : F (path M Sc k) ≤ F S₀ := by rw [← hτ]; exact path_F_mono hM Sc hk
  refine ⟨hFk, fun T hT => ?_⟩
  rcases lt_or_eq_of_le hk with hlt | heq
  · -- a move is made at step k: neighbours score ≤ the chosen move ≤ F S₀
    have hmv := (hmoves k hlt).1
    have h1 := hM.some_max _ _ hmv T hT
    have h2 : F (path M Sc (k + 1)) ≤ F S₀ := by rw [← hτ]; exact path_F_mono hM Sc hlt
    linarith
  · -- at S₀ itself: no improving neighbour
    rw [heq, hτ] at hT
    exact (hM.none_iff S₀).mp hTD.1 T hT

/-- **Theorem A (A4), PD part**: if the greedy path from `S ≠ S₀` reaches `S₀`, then
`F S < F S₀`. -/
theorem pd_of_reach (hM : IsBestImprovement N F M) {S S₀ : α} (hne : S ≠ S₀) {τ : ℕ}
    (hτ : path M S τ = S₀) : F S < F S₀ := by
  have hpos : 0 < τ := by
    rcases Nat.eq_zero_or_pos τ with h | h
    · rw [h, path_zero] at hτ; exact absurd hτ hne
    · exact h
  have hmove : M (path M S 0) ≠ none := by
    intro h0
    have := path_stays h0 τ (Nat.zero_le _)
    rw [hτ, path_zero] at this; exact hne this.symm
  have := path_F_strictMono hM S hpos hmove
  rwa [path_zero, hτ] at this

end SmcBvs.Greedy
