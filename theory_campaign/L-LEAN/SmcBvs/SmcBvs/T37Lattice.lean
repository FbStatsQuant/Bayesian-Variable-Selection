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

end SmcBvs.Lattice
