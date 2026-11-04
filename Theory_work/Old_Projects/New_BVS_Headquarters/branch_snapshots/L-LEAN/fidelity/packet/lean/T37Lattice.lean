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
  sorry

/-- **Move-class table** (W1 PROOF.md): a flip or swap that strictly decreases `Φ` is a progress
move, i.e. it stays in the lattice of its start. -/
theorem progress_mem_Lat {S T : Finset (Fin p)} (hT : IsFlipSwap S T) (hΦ : Φ S₀ T < Φ S₀ S) :
    T ∈ Lat S₀ S := by
  sorry

/-- Within a lattice, missing truths and extras do not increase. -/
theorem mis_ext_le_of_mem_Lat {S T : Finset (Fin p)} (hT : T ∈ Lat S₀ S) :
    mis S₀ T ≤ mis S₀ S ∧ ext S₀ T ≤ ext S₀ S := by
  sorry

/-- Lattices are nested: `T ∈ Lat S → Lat T ⊆ Lat S`. -/
theorem Lat_subset {S T : Finset (Fin p)} (hT : T ∈ Lat S₀ S) : Lat S₀ T ⊆ Lat S₀ S := by
  sorry

/-- **Lemma 2(a)**: progress moves map `Lat(S)` into `Lat(S)` and `R_{a,d}` into `R_{a,d}`. -/
theorem lemma2a {a d : ℕ} {S T : Finset (Fin p)} (hT : IsFlipSwap S T) (hΦ : Φ S₀ T < Φ S₀ S) :
    T ∈ Lat S₀ S ∧ (S ∈ Rad S₀ a d → T ∈ Rad S₀ a d) := by
  sorry

/-- **TD′_P(R_{a,d})** on the lattice (W1 Definitions): (L) and, at every other state of
`R_{a,d}`, the greedy move exists and strictly decreases `Φ`. -/
def TDP' (M : Finset (Fin p) → Option (Finset (Fin p))) (a d : ℕ) : Prop :=
  M S₀ = none ∧ ∀ S ∈ Rad S₀ a d, S ≠ S₀ → ∃ T, M S = some T ∧ Φ S₀ T < Φ S₀ S

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
  sorry

/-- **Theorem A (A3), concrete form.** Under the hypotheses of `theoremA2_lattice`, from a
centre `S_c ∈ R_{a,d}` and any cap `ℓ ≥ Φ(S_c)` (in particular `ℓ ≥ a + d`), the capped search
returns `S₀` with no improving neighbour (certified). -/
theorem theoremA3_lattice {K : ℕ} {F : Finset (Fin p) → ℝ} {M : Finset (Fin p) → Option (Finset (Fin p))}
    (hM : Greedy.IsBestImprovement (nbhd K) F M) {a d : ℕ} (hTD : TDP' S₀ M a d)
    {Sc : Finset (Fin p)} (hSc : Sc ∈ Rad S₀ a d) {ℓ : ℕ} (hℓ : Φ S₀ Sc ≤ ℓ) :
    Greedy.path M Sc ℓ = S₀ ∧ M (Greedy.path M Sc ℓ) = none := by
  sorry

/-- `Φ(S) ≤ a + d` on `R_{a,d}`, so the cap `ℓ ≥ a + d` suffices (W3-VT37R R3). -/
theorem Φ_le_of_mem_Rad {a d : ℕ} {S : Finset (Fin p)} (hS : S ∈ Rad S₀ a d) :
    Φ S₀ S ≤ a + d := by
  sorry

end SmcBvs.Lattice
