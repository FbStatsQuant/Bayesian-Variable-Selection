import SmcBvs.T37Greedy
import Mathlib.Data.Fintype.Powerset
import Mathlib.Order.SymmDiff

/-!
# T37(i) / Theorem A on the model lattice: Lemma 2(a) and the concrete (A2), (A3)

Source: branch `theory/W1-T37R`, `theory_campaign/W1-T37R/PROOF.md`: the move-class table,
"Lattice of a centre", "Lemma 2 (lattice closure)" (a), and "Theorem A" (A2), (A3); repairs in
`theory/W3-VT37R` `REPAIRS.md` R3 (`ℓ ≥ τ(S_c)` suffices).

Concrete setting: models `Finset (Fin p)`, truth `S₀`, cap `K`;
* feasible neighbourhood `nbhd K S`: all flips (one addition, one deletion) and swaps (one out,
  one in) of `S` with size `≤ K`;
* `mis S = |S₀ ∖ S|`, `ext S = |S ∖ S₀|`, `Φ S = |S △ S₀|`;
* `Rad a d = {S : mis S ≤ a, ext S ≤ d}` (the region `R_{a,d}`; when `s₀ + d ≤ K` it is feasible);
* `Lat S = {T : S ∩ S₀ ⊆ T ⊆ S ∪ S₀}` (= `{U′ ∪ P′ : U ⊆ U′ ⊆ S₀, P′ ⊆ P}` for `S = U ∪ P`).

TD′_P(R_{a,d}) (W1 Definitions) asks: `M S₀ = none`, and at every `S ∈ R_{a,d} ∖ {S₀}` the greedy
move exists and is a progress move (`Φ` drops). Lemma 2(a) supplies the closure that the abstract
`Greedy.TDP` takes as a hypothesis.
-/

open Finset

namespace SmcBvs.Lattice

variable {p : ℕ}

/-- `T` is a flip (addition or deletion) or a swap of `S`. -/
def IsFlipSwap (S T : Finset (Fin p)) : Prop :=
  (∃ j ∉ S, T = insert j S) ∨ (∃ i ∈ S, T = S.erase i) ∨
    (∃ i ∈ S, ∃ j ∉ S, T = insert j (S.erase i))

/-- Feasible flip-or-swap neighbourhood (size `≤ K`). -/
noncomputable def nbhd (K : ℕ) (S : Finset (Fin p)) : Finset (Finset (Fin p)) := by
  classical exact univ.filter fun T => T.card ≤ K ∧ IsFlipSwap S T

variable (S₀ : Finset (Fin p))

/-- Number of missing truths `m(S) = |S₀ ∖ S|`. -/
def mis (S : Finset (Fin p)) : ℕ := (S₀ \ S).card

/-- Number of extras `e(S) = |S ∖ S₀|`. -/
def ext (S : Finset (Fin p)) : ℕ := (S \ S₀).card

/-- Potential `Φ(S) = |S △ S₀|`. -/
def Φ (S : Finset (Fin p)) : ℕ := (symmDiff S S₀).card

/-- The region `R_{a,d}`. -/
noncomputable def Rad (a d : ℕ) : Finset (Finset (Fin p)) := by
  classical exact univ.filter fun S => mis S₀ S ≤ a ∧ ext S₀ S ≤ d

/-- The lattice of a centre, `Lat(S) = {T : S ∩ S₀ ⊆ T ⊆ S ∪ S₀}`. -/
noncomputable def Lat (S : Finset (Fin p)) : Finset (Finset (Fin p)) := by
  classical exact univ.filter fun T => S ∩ S₀ ⊆ T ∧ T ⊆ S ∪ S₀

/-- `Φ = m + e`. -/
theorem Φ_eq (S : Finset (Fin p)) : Φ S₀ S = mis S₀ S + ext S₀ S := by
  unfold Φ mis ext
  rw [Finset.symmDiff_def, Finset.card_union_of_disjoint disjoint_sdiff_sdiff, Nat.add_comm]

theorem mem_Lat {S T : Finset (Fin p)} : T ∈ Lat S₀ S ↔ S ∩ S₀ ⊆ T ∧ T ⊆ S ∪ S₀ := by
  unfold Lat
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]

theorem mem_Rad {a d : ℕ} {S : Finset (Fin p)} : S ∈ Rad S₀ a d ↔ mis S₀ S ≤ a ∧ ext S₀ S ≤ d := by
  unfold Rad
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]

omit S₀ in
theorem mem_nbhd {K : ℕ} {S T : Finset (Fin p)} : T ∈ nbhd K S ↔ T.card ≤ K ∧ IsFlipSwap S T := by
  unfold nbhd
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]

theorem S₀_mem_Rad (a d : ℕ) : S₀ ∈ Rad S₀ a d := by
  rw [mem_Rad]
  simp [mis, ext]

theorem self_mem_Lat (S : Finset (Fin p)) : S ∈ Lat S₀ S :=
  (mem_Lat S₀).mpr ⟨Finset.inter_subset_left, Finset.subset_union_left⟩

theorem S₀_mem_Lat (S : Finset (Fin p)) : S₀ ∈ Lat S₀ S :=
  (mem_Lat S₀).mpr ⟨Finset.inter_subset_right, Finset.subset_union_right⟩

/-- Adding a truth lowers `Φ` by one. -/
theorem Φ_insert_of_mem {A : Finset (Fin p)} {x : Fin p} (hx : x ∉ A) (h0 : x ∈ S₀) :
    Φ S₀ (insert x A) + 1 = Φ S₀ A := by
  unfold Φ
  have hmem : x ∈ symmDiff A S₀ := Finset.mem_symmDiff.mpr (Or.inr ⟨h0, hx⟩)
  have heq : symmDiff (insert x A) S₀ = (symmDiff A S₀).erase x := by
    ext y
    simp only [Finset.mem_symmDiff, Finset.mem_insert, Finset.mem_erase]
    by_cases hy : y = x
    · subst hy
      simp [h0]
    · simp [hy]
  rw [heq, Finset.card_erase_of_mem hmem]
  have := Finset.card_pos.mpr ⟨x, hmem⟩
  omega

/-- Adding a null raises `Φ` by one. -/
theorem Φ_insert_of_notMem {A : Finset (Fin p)} {x : Fin p} (hx : x ∉ A) (h0 : x ∉ S₀) :
    Φ S₀ (insert x A) = Φ S₀ A + 1 := by
  unfold Φ
  have hmem : x ∉ symmDiff A S₀ := by
    rw [Finset.mem_symmDiff]
    tauto
  have heq : symmDiff (insert x A) S₀ = insert x (symmDiff A S₀) := by
    ext y
    simp only [Finset.mem_symmDiff, Finset.mem_insert]
    by_cases hy : y = x
    · subst hy
      simp [h0]
    · simp [hy]
  rw [heq, Finset.card_insert_of_notMem hmem]

/-- Deleting a truth raises `Φ` by one. -/
theorem Φ_erase_of_mem {A : Finset (Fin p)} {x : Fin p} (hx : x ∈ A) (h0 : x ∈ S₀) :
    Φ S₀ (A.erase x) = Φ S₀ A + 1 := by
  have := Φ_insert_of_mem S₀ (Finset.notMem_erase x A) h0
  rw [Finset.insert_erase hx] at this
  omega

/-- Deleting an extra lowers `Φ` by one. -/
theorem Φ_erase_of_notMem {A : Finset (Fin p)} {x : Fin p} (hx : x ∈ A) (h0 : x ∉ S₀) :
    Φ S₀ (A.erase x) + 1 = Φ S₀ A := by
  have := Φ_insert_of_notMem S₀ (Finset.notMem_erase x A) h0
  rw [Finset.insert_erase hx] at this
  omega

/-- **Move-class table** (W1 PROOF.md): a flip or swap that strictly decreases `Φ` is a progress
move, i.e. it stays in the lattice of its start. -/
theorem progress_mem_Lat {S T : Finset (Fin p)} (hT : IsFlipSwap S T) (hΦ : Φ S₀ T < Φ S₀ S) :
    T ∈ Lat S₀ S := by
  rw [mem_Lat]
  rcases hT with ⟨j, hj, rfl⟩ | ⟨i, hi, rfl⟩ | ⟨i, hi, j, hj, rfl⟩
  · -- addition
    by_cases h0 : j ∈ S₀
    · refine ⟨fun x hx => Finset.mem_insert_of_mem (Finset.mem_inter.mp hx).1, fun x hx => ?_⟩
      rcases Finset.mem_insert.mp hx with hxj | hx
      · rw [hxj]; exact Finset.mem_union_right _ h0
      · exact Finset.mem_union_left _ hx
    · have := Φ_insert_of_notMem S₀ hj h0
      omega
  · -- deletion
    by_cases h0 : i ∈ S₀
    · have := Φ_erase_of_mem S₀ hi h0
      omega
    · refine ⟨fun x hx => ?_, fun x hx => Finset.mem_union_left _ (Finset.mem_of_mem_erase hx)⟩
      obtain ⟨hxS, hx0⟩ := Finset.mem_inter.mp hx
      exact Finset.mem_erase.mpr ⟨fun h => h0 (h ▸ hx0), hxS⟩
  · -- swap
    have hjU : j ∉ S.erase i := fun h => hj (Finset.mem_of_mem_erase h)
    by_cases hi0 : i ∈ S₀
    · have h1 := Φ_erase_of_mem S₀ hi hi0
      by_cases hj0 : j ∈ S₀
      · have h2 := Φ_insert_of_mem S₀ hjU hj0
        omega
      · have h2 := Φ_insert_of_notMem S₀ hjU hj0
        omega
    · by_cases hj0 : j ∈ S₀
      · refine ⟨fun x hx => ?_, fun x hx => ?_⟩
        · obtain ⟨hxS, hx0⟩ := Finset.mem_inter.mp hx
          exact Finset.mem_insert_of_mem (Finset.mem_erase.mpr ⟨fun h => hi0 (h ▸ hx0), hxS⟩)
        · rcases Finset.mem_insert.mp hx with hxj | hx
          · rw [hxj]; exact Finset.mem_union_right _ hj0
          · exact Finset.mem_union_left _ (Finset.mem_of_mem_erase hx)
      · have h1 := Φ_erase_of_notMem S₀ hi hi0
        have h2 := Φ_insert_of_notMem S₀ hjU hj0
        omega

/-- Within a lattice, missing truths and extras do not increase. -/
theorem mis_ext_le_of_mem_Lat {S T : Finset (Fin p)} (hT : T ∈ Lat S₀ S) :
    mis S₀ T ≤ mis S₀ S ∧ ext S₀ T ≤ ext S₀ S := by
  obtain ⟨h1, h2⟩ := (mem_Lat S₀).mp hT
  unfold mis ext
  refine ⟨Finset.card_le_card fun x hx => ?_, Finset.card_le_card fun x hx => ?_⟩
  · obtain ⟨hx0, hxT⟩ := Finset.mem_sdiff.mp hx
    exact Finset.mem_sdiff.mpr ⟨hx0, fun hxS => hxT (h1 (Finset.mem_inter.mpr ⟨hxS, hx0⟩))⟩
  · obtain ⟨hxT, hx0⟩ := Finset.mem_sdiff.mp hx
    rcases Finset.mem_union.mp (h2 hxT) with h | h
    · exact Finset.mem_sdiff.mpr ⟨h, hx0⟩
    · exact absurd h hx0

/-- Lattices are nested: `T ∈ Lat S → Lat T ⊆ Lat S`. -/
theorem Lat_subset {S T : Finset (Fin p)} (hT : T ∈ Lat S₀ S) : Lat S₀ T ⊆ Lat S₀ S := by
  intro U hU
  obtain ⟨h1, h2⟩ := (mem_Lat S₀).mp hT
  obtain ⟨h3, h4⟩ := (mem_Lat S₀).mp hU
  refine (mem_Lat S₀).mpr ⟨fun x hx => h3 ?_, fun x hx => ?_⟩
  · exact Finset.mem_inter.mpr ⟨h1 hx, (Finset.mem_inter.mp hx).2⟩
  · rcases Finset.mem_union.mp (h4 hx) with h | h
    · exact h2 h
    · exact Finset.mem_union_right _ h

/-- **Lemma 2(a)**: progress moves map `Lat(S)` into `Lat(S)` and `R_{a,d}` into `R_{a,d}`. -/
theorem lemma2a {a d : ℕ} {S T : Finset (Fin p)} (hT : IsFlipSwap S T) (hΦ : Φ S₀ T < Φ S₀ S) :
    T ∈ Lat S₀ S ∧ (S ∈ Rad S₀ a d → T ∈ Rad S₀ a d) := by
  have hL := progress_mem_Lat S₀ hT hΦ
  refine ⟨hL, fun hS => ?_⟩
  obtain ⟨ha, hd⟩ := (mem_Rad S₀).mp hS
  obtain ⟨hm, he⟩ := mis_ext_le_of_mem_Lat S₀ hL
  exact (mem_Rad S₀).mpr ⟨hm.trans ha, he.trans hd⟩

/-- **TD′_P(R_{a,d})** on the lattice (W1 Definitions): (L) and, at every other state of
`R_{a,d}`, the greedy move exists and strictly decreases `Φ`. -/
def TDP' (M : Finset (Fin p) → Option (Finset (Fin p))) (a d : ℕ) : Prop :=
  M S₀ = none ∧ ∀ S ∈ Rad S₀ a d, S ≠ S₀ → ∃ T, M S = some T ∧ Φ S₀ T < Φ S₀ S

/-- TD′_P(R_{a,d}) on the lattice gives the abstract `Greedy.TDP` (closure from Lemma 2(a)). -/
theorem TDP_of_TDP' {K : ℕ} {F : Finset (Fin p) → ℝ} {M : Finset (Fin p) → Option (Finset (Fin p))}
    (hM : Greedy.IsBestImprovement (nbhd K) F M) {a d : ℕ} (hTD : TDP' S₀ M a d) :
    Greedy.TDP M (Φ S₀) (Rad S₀ a d) S₀ := by
  refine ⟨hTD.1, fun S hS hne => ?_⟩
  obtain ⟨T, hT, hΦ⟩ := hTD.2 S hS hne
  have hFS := (mem_nbhd.mp (hM.some_mem S T hT)).2
  exact ⟨T, hT, (lemma2a S₀ (a := a) (d := d) hFS hΦ).2 hS, hΦ⟩

/-- **Theorem A (A2), concrete form.** Let `M` be a best-improvement map for the feasible
flip/swap neighbourhood and `F`, and assume TD′_P(R_{a,d}). From every `S ∈ R_{a,d}` the greedy
path reaches `S₀` after `τ ≤ Φ(S)` moves, stays in `Lat(S) ∩ R_{a,d}`, and `Φ` strictly decreases
at each move. -/
theorem theoremA2_lattice {K : ℕ} {F : Finset (Fin p) → ℝ} {M : Finset (Fin p) → Option (Finset (Fin p))}
    (hM : Greedy.IsBestImprovement (nbhd K) F M) {a d : ℕ} (hTD : TDP' S₀ M a d)
    {S : Finset (Fin p)} (hS : S ∈ Rad S₀ a d) :
    ∃ τ ≤ Φ S₀ S, Greedy.path M S τ = S₀ ∧
      (∀ k, Greedy.path M S k ∈ Rad S₀ a d ∧ Greedy.path M S k ∈ Lat S₀ S) ∧
      (∀ k < τ, Φ S₀ (Greedy.path M S (k + 1)) < Φ S₀ (Greedy.path M S k)) := by
  obtain ⟨τ, hτ, hp, hmem, hmoves, -⟩ :=
    Greedy.theoremA2 (TDP_of_TDP' S₀ hM hTD) (S₀_mem_Rad S₀ a d) hS
  refine ⟨τ, hτ, hp, fun k => ⟨hmem k, ?_⟩, fun k hk => (hmoves k hk).2⟩
  induction k with
  | zero => rw [Greedy.path_zero]; exact self_mem_Lat S₀ S
  | succ k ih =>
    rw [Greedy.path_succ]
    by_cases h0 : Greedy.path M S k = S₀
    · rw [h0, Greedy.step_of_none hTD.1]; exact S₀_mem_Lat S₀ S
    · obtain ⟨T, hT, hΦ⟩ := hTD.2 _ (hmem k) h0
      rw [Greedy.step_of_some hT]
      exact Lat_subset S₀ ih (progress_mem_Lat S₀ (mem_nbhd.mp (hM.some_mem _ _ hT)).2 hΦ)

/-- **Theorem A (A3), concrete form.** Under the hypotheses of `theoremA2_lattice`, from a
centre `S_c ∈ R_{a,d}` and any cap `ℓ ≥ Φ(S_c)` (in particular `ℓ ≥ a + d`), the capped search
returns `S₀` with no improving neighbour (certified). -/
theorem theoremA3_lattice {K : ℕ} {F : Finset (Fin p) → ℝ} {M : Finset (Fin p) → Option (Finset (Fin p))}
    (hM : Greedy.IsBestImprovement (nbhd K) F M) {a d : ℕ} (hTD : TDP' S₀ M a d)
    {Sc : Finset (Fin p)} (hSc : Sc ∈ Rad S₀ a d) {ℓ : ℕ} (hℓ : Φ S₀ Sc ≤ ℓ) :
    Greedy.path M Sc ℓ = S₀ ∧ M (Greedy.path M Sc ℓ) = none := by
  obtain ⟨τ, hτ, -, -, -, hstay⟩ :=
    Greedy.theoremA2 (TDP_of_TDP' S₀ hM hTD) (S₀_mem_Rad S₀ a d) hSc
  have h := hstay ℓ (hτ.trans hℓ)
  exact ⟨h, by rw [h]; exact hTD.1⟩

/-- `Φ(S) ≤ a + d` on `R_{a,d}`, so the cap `ℓ ≥ a + d` suffices (W3-VT37R R3). -/
theorem Φ_le_of_mem_Rad {a d : ℕ} {S : Finset (Fin p)} (hS : S ∈ Rad S₀ a d) :
    Φ S₀ S ≤ a + d := by
  obtain ⟨ha, hd⟩ := (mem_Rad S₀).mp hS
  rw [Φ_eq]
  omega

/-- Feasibility of `R_{a,d}`: if `s₀ + d ≤ K`, every model of `Rad S₀ a d` has size `≤ K`, so
`Rad` is the source's (feasible) region `R_{a,d}`. -/
theorem card_le_of_mem_Rad {K a d : ℕ} (hKd : S₀.card + d ≤ K) {S : Finset (Fin p)}
    (hS : S ∈ Rad S₀ a d) : S.card ≤ K := by
  have he : (S \ S₀).card ≤ d := ((mem_Rad S₀).mp hS).2
  have h1 := Finset.card_sdiff_add_card_inter S S₀
  have h2 : (S ∩ S₀).card ≤ S₀.card := Finset.card_le_card Finset.inter_subset_right
  omega

/-- A flip or swap adds at most one index and removes at most one index. -/
theorem flipSwap_sdiff_card {S T : Finset (Fin p)} (hT : IsFlipSwap S T) :
    (T \ S).card ≤ 1 ∧ (S \ T).card ≤ 1 := by
  have key : ∀ (A : Finset (Fin p)) (z : Fin p), A ⊆ {z} → A.card ≤ 1 :=
    fun A z h => (Finset.card_le_card h).trans (Finset.card_singleton z).le
  rcases hT with ⟨j, hj, rfl⟩ | ⟨i, hi, rfl⟩ | ⟨i, hi, j, hj, rfl⟩
  · refine ⟨key _ j ?_, key _ j ?_⟩ <;> intro x hx <;>
      simp only [Finset.mem_sdiff, Finset.mem_insert, Finset.mem_singleton] at hx ⊢ <;> tauto
  · refine ⟨key _ i ?_, key _ i ?_⟩ <;> intro x hx <;>
      simp only [Finset.mem_sdiff, Finset.mem_erase, Finset.mem_singleton] at hx ⊢ <;> tauto
  · refine ⟨key _ j ?_, key _ i ?_⟩ <;> intro x hx <;>
      simp only [Finset.mem_sdiff, Finset.mem_insert, Finset.mem_erase, Finset.mem_singleton]
        at hx ⊢ <;> tauto

/-- One flip or swap lowers `m` and `e` by at most one each. -/
theorem mis_ext_step {S T : Finset (Fin p)} (hT : IsFlipSwap S T) :
    mis S₀ S ≤ mis S₀ T + 1 ∧ ext S₀ S ≤ ext S₀ T + 1 := by
  obtain ⟨h1, h2⟩ := flipSwap_sdiff_card hT
  constructor
  · have hsub : S₀ \ S ⊆ (S₀ \ T) ∪ (T \ S) := by
      intro x hx; simp only [Finset.mem_sdiff, Finset.mem_union] at hx ⊢; tauto
    have := (Finset.card_le_card hsub).trans (Finset.card_union_le _ _)
    unfold mis; omega
  · have hsub : S \ S₀ ⊆ (T \ S₀) ∪ (S \ T) := by
      intro x hx; simp only [Finset.mem_sdiff, Finset.mem_union] at hx ⊢; tauto
    have := (Finset.card_le_card hsub).trans (Finset.card_union_le _ _)
    unfold ext; omega

theorem Φ_self : Φ S₀ S₀ = 0 := by simp [Φ]

/-- **Theorem A (A2), move count.** Under the hypotheses of `theoremA2_lattice`, the number `τ` of
moves from `S ∈ R_{a,d}` to `S₀` satisfies `max(m(S), e(S)) ≤ τ ≤ Φ(S)`. Each move lowers `Φ`
by 1 or 2, and `τ + σ = m(S) + e(S)`, where `σ` is the number of moves that lower `Φ` by 2
(by the move-class table these are the extra→truth swaps). That is, `τ = m + e − σ`. -/
theorem theoremA2_lattice_count {K : ℕ} {F : Finset (Fin p) → ℝ}
    {M : Finset (Fin p) → Option (Finset (Fin p))}
    (hM : Greedy.IsBestImprovement (nbhd K) F M) {a d : ℕ} (hTD : TDP' S₀ M a d)
    {S : Finset (Fin p)} (hS : S ∈ Rad S₀ a d) :
    ∃ τ ≤ Φ S₀ S, Greedy.path M S τ = S₀ ∧ max (mis S₀ S) (ext S₀ S) ≤ τ ∧
      (∀ k < τ, Φ S₀ (Greedy.path M S (k + 1)) + 1 ≤ Φ S₀ (Greedy.path M S k) ∧
        Φ S₀ (Greedy.path M S k) ≤ Φ S₀ (Greedy.path M S (k + 1)) + 2) ∧
      τ + ((Finset.range τ).filter fun k =>
          Φ S₀ (Greedy.path M S k) = Φ S₀ (Greedy.path M S (k + 1)) + 2).card =
        mis S₀ S + ext S₀ S := by
  obtain ⟨τ, hτ, hp, -, hmoves, -⟩ :=
    Greedy.theoremA2 (TDP_of_TDP' S₀ hM hTD) (S₀_mem_Rad S₀ a d) hS
  set P := Greedy.path M S with hP
  have hfs : ∀ k < τ, IsFlipSwap (P k) (P (k + 1)) := fun k hk =>
    (mem_nbhd.mp (hM.some_mem _ _ (hmoves k hk).1)).2
  have hstep : ∀ k < τ, mis S₀ (P k) ≤ mis S₀ (P (k + 1)) + 1 ∧
      ext S₀ (P k) ≤ ext S₀ (P (k + 1)) + 1 := fun k hk => mis_ext_step S₀ (hfs k hk)
  have hdrop : ∀ k < τ, Φ S₀ (P (k + 1)) + 1 ≤ Φ S₀ (P k) ∧
      Φ S₀ (P k) ≤ Φ S₀ (P (k + 1)) + 2 := by
    intro k hk
    have h1 := (hmoves k hk).2
    have h2 := hstep k hk
    rw [Φ_eq, Φ_eq] at h1 ⊢
    omega
  -- telescoping and the m, e bounds, by induction up to τ
  have hind : ∀ k ≤ τ, mis S₀ S ≤ mis S₀ (P k) + k ∧ ext S₀ S ≤ ext S₀ (P k) + k ∧
      Φ S₀ S = Φ S₀ (P k) + k + ((Finset.range k).filter fun i =>
        Φ S₀ (P i) = Φ S₀ (P (i + 1)) + 2).card := by
    intro k hk
    induction k with
    | zero => simp [hP, Greedy.path_zero]
    | succ k ih =>
      obtain ⟨i1, i2, i3⟩ := ih (by omega)
      have hs := hstep k (by omega)
      have hd := hdrop k (by omega)
      refine ⟨by omega, by omega, ?_⟩
      rw [Finset.range_add_one, Finset.filter_insert]
      by_cases h2 : Φ S₀ (P k) = Φ S₀ (P (k + 1)) + 2
      · rw [ite_eq_left_of_eq_true _ _ (eq_true h2), Finset.card_insert_of_notMem (by simp)]; omega
      · rw [ite_eq_right_of_eq_false _ _ (eq_false h2)]; omega
  obtain ⟨hm, he, hΦ⟩ := hind τ le_rfl
  rw [hp, Φ_self] at hΦ
  have hm0 : mis S₀ S₀ = 0 := by simp [mis]
  have he0 : ext S₀ S₀ = 0 := by simp [ext]
  rw [hp, hm0] at hm
  rw [hp, he0] at he
  refine ⟨τ, hτ, hp, max_le (by omega) (by omega), hdrop, ?_⟩
  rw [← Φ_eq]; omega

/-- **Move-class table, a Φ drop of 2.** A flip or swap that lowers `Φ` by exactly 2 is an
extra→truth swap: an extra `i ∈ S ∖ S₀` goes out and a missing truth `j ∈ S₀ ∖ S` comes in. -/
theorem drop_two_swap {S T : Finset (Fin p)} (hT : IsFlipSwap S T)
    (h2 : Φ S₀ S = Φ S₀ T + 2) :
    ∃ i ∈ S, i ∉ S₀ ∧ ∃ j ∉ S, j ∈ S₀ ∧ T = insert j (S.erase i) := by
  rcases hT with ⟨j, hj, rfl⟩ | ⟨i, hi, rfl⟩ | ⟨i, hi, j, hj, rfl⟩
  · by_cases h0 : j ∈ S₀
    · have := Φ_insert_of_mem S₀ hj h0; omega
    · have := Φ_insert_of_notMem S₀ hj h0; omega
  · by_cases h0 : i ∈ S₀
    · have := Φ_erase_of_mem S₀ hi h0; omega
    · have := Φ_erase_of_notMem S₀ hi h0; omega
  · have hj' : j ∉ S.erase i := fun h => hj (Finset.mem_of_mem_erase h)
    by_cases hi0 : i ∈ S₀ <;> by_cases hj0 : j ∈ S₀
    · have := Φ_erase_of_mem S₀ hi hi0; have := Φ_insert_of_mem S₀ hj' hj0; omega
    · have := Φ_erase_of_mem S₀ hi hi0; have := Φ_insert_of_notMem S₀ hj' hj0; omega
    · exact ⟨i, hi, hi0, j, hj, hj0, rfl⟩
    · have := Φ_erase_of_notMem S₀ hi hi0; have := Φ_insert_of_notMem S₀ hj' hj0; omega

/-- Converse: an extra→truth swap lowers `Φ` by exactly 2. With `drop_two_swap`, the count `σ`
in `theoremA2_lattice_count` is the number of extra→truth swaps on the path. -/
theorem swap_extra_truth_drop_two {S : Finset (Fin p)} {i j : Fin p} (hi : i ∈ S) (hi0 : i ∉ S₀)
    (hj : j ∉ S) (hj0 : j ∈ S₀) : Φ S₀ S = Φ S₀ (insert j (S.erase i)) + 2 := by
  have hj' : j ∉ S.erase i := fun h => hj (Finset.mem_of_mem_erase h)
  have := Φ_erase_of_notMem S₀ hi hi0
  have := Φ_insert_of_mem S₀ hj' hj0
  omega

/-- The one-state progress event `D_S` (W1 PROOF.md, Definitions): the best feasible progress
neighbour (`Φ` decreases) strictly improves on `S` and strictly beats every non-progress
neighbour. It is stated with a witness `T` for the best progress move. -/
def DS (K : ℕ) (F : Finset (Fin p) → ℝ) (S : Finset (Fin p)) : Prop :=
  ∃ T ∈ nbhd K S, Φ S₀ T < Φ S₀ S ∧ F S < F T ∧
    ∀ T' ∈ nbhd K S, ¬ Φ S₀ T' < Φ S₀ S → F T' < F T

/-- Under `D_S`, every best-improvement map makes a progress move at `S`, whatever its tie
rule. -/
theorem DS_move {K : ℕ} {F : Finset (Fin p) → ℝ} {M : Finset (Fin p) → Option (Finset (Fin p))}
    (hM : Greedy.IsBestImprovement (nbhd K) F M) {S : Finset (Fin p)} (hD : DS S₀ K F S) :
    ∃ T, M S = some T ∧ Φ S₀ T < Φ S₀ S := by
  obtain ⟨T, hTN, -, hFT, hbeat⟩ := hD
  cases hMS : M S with
  | none =>
    have := (hM.none_iff S).mp hMS T hTN
    linarith
  | some T₁ =>
    refine ⟨T₁, rfl, ?_⟩
    by_contra hnp
    have h1 := hbeat T₁ (hM.some_mem _ _ hMS) hnp
    have h2 := hM.some_max _ _ hMS T hTN
    linarith

/-- **Theorem A (A3), lattice-condition version** (W1 PROOF.md A3, last sentence; the cap as in
W3-VT37R R3). Assume (L) `M S₀ = none` and `D_{S'}` at every `S' ∈ Lat(S_c) ∖ {S₀}`: only
`2^{Φ(S_c)}` states, with no condition elsewhere in `R_{a,d}`. Then the greedy path from `S_c`
stays in `Lat(S_c)` and reaches `S₀` after `τ ≤ Φ(S_c)` moves. For every cap `ℓ ≥ τ`, the capped
search returns `S₀` certified. -/
theorem theoremA3_lattice_only {K : ℕ} {F : Finset (Fin p) → ℝ}
    {M : Finset (Fin p) → Option (Finset (Fin p))}
    (hM : Greedy.IsBestImprovement (nbhd K) F M) {Sc : Finset (Fin p)} (hL0 : M S₀ = none)
    (hD : ∀ S ∈ Lat S₀ Sc, S ≠ S₀ → DS S₀ K F S) :
    ∃ τ ≤ Φ S₀ Sc, Greedy.path M Sc τ = S₀ ∧ (∀ k, Greedy.path M Sc k ∈ Lat S₀ Sc) ∧
      ∀ ℓ, τ ≤ ℓ → Greedy.path M Sc ℓ = S₀ ∧ M (Greedy.path M Sc ℓ) = none := by
  have hTDP : Greedy.TDP M (Φ S₀) (Lat S₀ Sc) S₀ := by
    refine ⟨hL0, fun S hS hne => ?_⟩
    obtain ⟨T, hT, hΦ⟩ := DS_move S₀ hM (hD S hS hne)
    have hfs := (mem_nbhd.mp (hM.some_mem _ _ hT)).2
    exact ⟨T, hT, Lat_subset S₀ hS (progress_mem_Lat S₀ hfs hΦ), hΦ⟩
  obtain ⟨τ, hτ, hp, hmem, -, hstay⟩ :=
    Greedy.theoremA2 hTDP (S₀_mem_Lat S₀ Sc) (self_mem_Lat S₀ Sc)
  exact ⟨τ, hτ, hp, hmem, fun ℓ hℓ => ⟨hstay ℓ hℓ, by rw [hstay ℓ hℓ]; exact hL0⟩⟩

/-- **Theorem A (A3), concrete form with the sharp cap** (W3-VT37R R3: `ℓ ≥ τ(S_c)` suffices).
Under TD′_P(R_{a,d}), from `S_c ∈ R_{a,d}` there is `τ ≤ Φ(S_c)` such that for every cap `ℓ ≥ τ`
the capped search returns `S₀` certified, and every model scored by the search up to `τ` has
score `≤ F(S₀)`. -/
theorem theoremA3_lattice_tau {K : ℕ} {F : Finset (Fin p) → ℝ}
    {M : Finset (Fin p) → Option (Finset (Fin p))}
    (hM : Greedy.IsBestImprovement (nbhd K) F M) {a d : ℕ} (hTD : TDP' S₀ M a d)
    {Sc : Finset (Fin p)} (hSc : Sc ∈ Rad S₀ a d) :
    ∃ τ ≤ Φ S₀ Sc, (∀ ℓ, τ ≤ ℓ → Greedy.path M Sc ℓ = S₀ ∧ M (Greedy.path M Sc ℓ) = none) ∧
      (∀ k ≤ τ, F (Greedy.path M Sc k) ≤ F S₀ ∧
        ∀ T ∈ nbhd K (Greedy.path M Sc k), F T ≤ F S₀) :=
  Greedy.theoremA3 hM (TDP_of_TDP' S₀ hM hTD) (S₀_mem_Rad S₀ a d) hSc

end SmcBvs.Lattice
