import SmcBvs.Basic

/-!
# T07: size-only ranking ceiling and Bayes decisions (finite, exact)

Source: `Docs/Theory/proofs/T06_T07_identifiability_size_prior/STATEMENT.md` §2 and `PROOF_v2.tex`
§"T07" (Theorems ceiling / bayes / reported, Lemma psi); the sharpness clause (i′) and the
certificate (iii′) are from branch `theory/W2-BOOK`, `theory_campaign/W2-BOOK/PROOF.md` §3.

Setting. Models are `Finset (Fin p)`; `Ωf p K = {S : |S| ≤ K}`. The tie order `≺` is an injective
rank `rk` (smaller = preferred); the paper notes (PROOF_v2 Remark "the tie order") that any fixed
total order works. `m` is the marginal likelihood (only `m > 0` is used, and only where stated).
A positive size-only prior is `w̃ : ℕ → ℝ` with `w̃ k > 0` for `k ≤ K`, normalised by
`W̃ = Σ_{k ≤ K} C(p,k) w̃(k)`.

For the decision results `F` is any real score on models, `π = post F (Ωf p K)` (so `π = 0` off
`Ω`), `PIP_j = Σ_{S ∈ Ω, j ∈ S} π(S)`, `ρ₀₁(a) = Σ_{S∈Ω} π(S) 1{a ≠ S}`,
`ρ_H(a) = Σ_{S∈Ω} π(S) |a △ S|`, `ψ_q(a) = Σ_{j∈a} (1 - 2 q_j)`, `J₊(q) = {j : q_j > 1/2}`.
-/

open Finset

namespace SmcBvs.T07

variable {p : ℕ}

/-- The feasible model space `Ω = {S ⊆ [p] : |S| ≤ K}`. -/
def Ωf (p K : ℕ) : Finset (Finset (Fin p)) := univ.filter fun S => S.card ≤ K

/-- The size class `{S : |S| = k}`. -/
def sizeClass (p k : ℕ) : Finset (Finset (Fin p)) := univ.filter fun S => S.card = k

/-- Normaliser `W̃ = Σ_{k ≤ K} C(p,k) w̃(k)` of a size-only prior. -/
noncomputable def normW (p K : ℕ) (w : ℕ → ℝ) : ℝ := ∑ k ∈ range (K + 1), (p.choose k : ℝ) * w k

/-- The size-only prior `ϖ_w̃(S) = w̃(|S|)/W̃`. -/
noncomputable def sizePrior (p K : ℕ) (w : ℕ → ℝ) (S : Finset (Fin p)) : ℝ :=
  w S.card / normW p K w

/-- Positivity of a size-only prior on `0..K`. -/
def PosSizePrior (K : ℕ) (w : ℕ → ℝ) : Prop := ∀ k ≤ K, 0 < w k

theorem normW_pos {K : ℕ} {w : ℕ → ℝ} (hw : PosSizePrior K w) : 0 < normW p K w := by
  unfold normW
  rw [sum_range_succ']
  have h0 : (0 : ℝ) < (p.choose 0 : ℝ) * w 0 := by simpa using hw 0 (Nat.zero_le _)
  have hrest : 0 ≤ ∑ k ∈ range K, (p.choose (k + 1) : ℝ) * w (k + 1) :=
    sum_nonneg fun k hk => mul_nonneg (Nat.cast_nonneg _)
      (hw (k + 1) (by simp at hk; omega)).le
  linarith

theorem empty_mem_Ωf (K : ℕ) : (∅ : Finset (Fin p)) ∈ Ωf p K := by simp [Ωf]

theorem Ωf_nonempty (K : ℕ) : (Ωf p K).Nonempty := ⟨∅, empty_mem_Ωf K⟩

/-! ## T07(i): the size-only ceiling -/

/-- **T07(i), ceiling.** If `S₀` is the global HPM `S†_w̃` under a positive size-only prior, then
`s₀ ≤ K` and `S₀ = S*_{s₀}`, the `≺`-least maximiser of `m` within its size class. -/
theorem ceiling {K : ℕ} (rk : Finset (Fin p) → ℕ) (m : Finset (Fin p) → ℝ) {w : ℕ → ℝ}
    (hw : PosSizePrior K w) {S₀ : Finset (Fin p)}
    (h : IsLeastArgmax rk (fun S => sizePrior p K w S * m S) (Ωf p K) S₀) :
    S₀.card ≤ K ∧ IsLeastArgmax rk m (sizeClass p S₀.card) S₀ := by
  have hS₀K : S₀.card ≤ K := (mem_filter.mp h.1.1).2
  have hγ : 0 < w S₀.card / normW p K w := div_pos (hw _ hS₀K) (normW_pos hw)
  have hclassΩ : ∀ T ∈ sizeClass p S₀.card, T ∈ Ωf p K := fun T hT => by
    simp only [sizeClass, mem_filter, mem_univ, true_and] at hT
    simp [Ωf, hT, hS₀K]
  have hg : ∀ T ∈ sizeClass p S₀.card, sizePrior p K w T * m T = (w S₀.card / normW p K w) * m T :=
    fun T hT => by
      simp only [sizeClass, mem_filter, mem_univ, true_and] at hT
      simp [sizePrior, hT]
  have hS₀class : S₀ ∈ sizeClass p S₀.card := by simp [sizeClass]
  have hargmax : IsArgmax m (sizeClass p S₀.card) S₀ := by
    refine ⟨hS₀class, fun T hT => ?_⟩
    have := h.1.2 T (hclassΩ T hT)
    simp only at this
    rw [hg T hT, hg S₀ hS₀class] at this
    exact le_of_mul_le_mul_left this hγ
  refine ⟨hS₀K, hargmax, fun T hT => h.2 T ⟨hclassΩ T hT.1, fun U hU => ?_⟩⟩
  have hmT : m T = m S₀ := le_antisymm (hargmax.2 T hT.1) (hT.2 S₀ hS₀class)
  have := h.1.2 U hU
  simp only at this ⊢
  rwa [hg S₀ hS₀class, ← hmT, ← hg T hT.1] at this

/-- **T07(i), "no size-only prior can repair a within-size ranking error"** (contrapositive of
the ceiling). If some model `S'` of the same size as `S₀` beats `S₀` in `m`, or ties it and
precedes it in `≺`, then for *every* positive size-only prior `S₀` is not the global HPM.
(This is also W2-BOOK (iii′), stated in terms of `m`.) -/
theorem no_size_prior_repairs {K : ℕ} (rk : Finset (Fin p) → ℕ) (m : Finset (Fin p) → ℝ)
    {S₀ S' : Finset (Fin p)} (hcard : S'.card = S₀.card)
    (hbeat : m S₀ < m S' ∨ (m S' = m S₀ ∧ rk S' < rk S₀)) :
    ∀ w : ℕ → ℝ, PosSizePrior K w →
      ¬ IsLeastArgmax rk (fun S => sizePrior p K w S * m S) (Ωf p K) S₀ := by
  intro w hw h
  obtain ⟨-, hstar⟩ := ceiling rk m hw h
  have hS' : S' ∈ sizeClass p S₀.card := by simp [sizeClass, hcard]
  rcases hbeat with hlt | ⟨heq, hrk⟩
  · linarith [hstar.1.2 S' hS']
  · have : IsArgmax m (sizeClass p S₀.card) S' :=
      ⟨hS', fun T hT => by rw [heq]; exact hstar.1.2 T hT⟩
    have := hstar.2 S' this
    omega

/-- **T07(i′), sharpness of the ceiling** (W2-BOOK PROOF.md §3 (i′)). If `s₀ ≤ K`, `m > 0` and
`S₀ = S*_{s₀}`, then some positive size-only prior makes `S₀` the global HPM. -/
theorem ceiling_sharp {K : ℕ} (rk : Finset (Fin p) → ℕ) (m : Finset (Fin p) → ℝ)
    (hm : ∀ S, 0 < m S) {S₀ : Finset (Fin p)} (hS₀K : S₀.card ≤ K)
    (hstar : IsLeastArgmax rk m (sizeClass p S₀.card) S₀) :
    ∃ w : ℕ → ℝ, PosSizePrior K w ∧
      IsLeastArgmax rk (fun S => sizePrior p K w S * m S) (Ωf p K) S₀ := by
  classical
  set sumM := ∑ S ∈ Ωf p K, m S with hsumM
  have hS₀Ω : S₀ ∈ Ωf p K := by simp [Ωf, hS₀K]
  have hle : ∀ S ∈ Ωf p K, m S ≤ sumM := fun S hS =>
    single_le_sum (fun T _ => (hm T).le) hS
  have hsumpos : 0 < sumM := lt_of_lt_of_le (hm S₀) (hle S₀ hS₀Ω)
  set ε := m S₀ / (2 * sumM) with hε
  have hεpos : 0 < ε := div_pos (hm S₀) (by linarith)
  -- ε * m S < m S₀ on Ω
  have hεm : ∀ S ∈ Ωf p K, ε * m S < m S₀ := by
    intro S hS
    have h1 : ε * m S ≤ ε * sumM := mul_le_mul_of_nonneg_left (hle S hS) hεpos.le
    have h2 : ε * sumM = m S₀ / 2 := by rw [hε]; field_simp
    linarith [hm S₀]
  let w : ℕ → ℝ := fun k => if k = S₀.card then 1 else ε
  have hw : PosSizePrior K w := fun k _ => by
    simp only [w]; split_ifs <;> [exact one_pos; exact hεpos]
  have hW := normW_pos (p := p) hw
  refine ⟨w, hw, ?_⟩
  set g : Finset (Fin p) → ℝ := fun S => sizePrior p K w S * m S with hgdef
  have hgS₀ : g S₀ = m S₀ / normW p K w := by simp [hgdef, sizePrior, w]; ring
  -- models of another size score strictly less than S₀
  have hother : ∀ S ∈ Ωf p K, S.card ≠ S₀.card → g S < g S₀ := by
    intro S hS hc
    have : g S = ε * m S / normW p K w := by simp [hgdef, sizePrior, w, hc]; ring
    rw [this, hgS₀]
    exact div_lt_div_of_pos_right (hεm S hS) hW
  have hsame : ∀ S, S.card = S₀.card → g S = m S / normW p K w := by
    intro S hc; simp [hgdef, sizePrior, w, hc]; ring
  have hargmax : IsArgmax g (Ωf p K) S₀ := by
    refine ⟨hS₀Ω, fun S hS => ?_⟩
    by_cases hc : S.card = S₀.card
    · rw [hsame S hc, hgS₀]
      exact div_le_div_of_nonneg_right (hstar.1.2 S (by simp [sizeClass, hc])) hW.le
    · exact (hother S hS hc).le
  refine ⟨hargmax, fun T hT => ?_⟩
  have hTeq : g T = g S₀ := le_antisymm (hargmax.2 T hT.1) (hT.2 S₀ hS₀Ω)
  have hc : T.card = S₀.card := by
    by_contra hc; exact absurd hTeq (hother T hT.1 hc).ne
  have hmT : m T = m S₀ := by
    rw [hsame T hc, hgS₀] at hTeq
    exact (div_left_inj' hW.ne').mp hTeq
  refine hstar.2 T ⟨by simp [sizeClass, hc], fun U hU => ?_⟩
  rw [hmT]; exact hstar.1.2 U hU

/-! ## T07(ii): Bayes decisions -/

variable (K : ℕ) (F : Finset (Fin p) → ℝ)

/-- Posterior `π` on `Ω = Ωf p K` from the log-score `F` (and `0` off `Ω`). -/
noncomputable abbrev π := post F (Ωf p K)

/-- Posterior inclusion probability `PIP_j = π({S : j ∈ S})`. -/
noncomputable def PIP (j : Fin p) : ℝ := ∑ S ∈ Ωf p K, if j ∈ S then π K F S else 0

/-- Posterior 0–1 risk `ρ(a) = Σ_{S∈Ω} π(S) 1{a ≠ S}`. -/
noncomputable def risk01 (a : Finset (Fin p)) : ℝ := ∑ S ∈ Ωf p K, π K F S * if a = S then 0 else 1

/-- Posterior Hamming risk `ρ_H(a) = Σ_{S∈Ω} π(S) |a △ S|`. -/
noncomputable def riskH (a : Finset (Fin p)) : ℝ :=
  ∑ S ∈ Ωf p K, π K F S * ((symmDiff a S).card : ℝ)

/-- `ψ_q(a) = Σ_{j∈a} (1 - 2 q_j)`. -/
def psi (q : Fin p → ℝ) (a : Finset (Fin p)) : ℝ := ∑ j ∈ a, (1 - 2 * q j)

/-- `J₊(q) = {j : q_j > 1/2}`; `MPM = J₊(PIP)`. -/
noncomputable def Jplus (q : Fin p → ℝ) : Finset (Fin p) := univ.filter fun j => 1 / 2 < q j

theorem risk01_eq (a : Finset (Fin p)) : risk01 K F a = 1 - π K F a := by
  have h1 : ∀ S, post F (Ωf p K) S * (if a = S then (0 : ℝ) else 1) =
      post F (Ωf p K) S - (if a = S then post F (Ωf p K) S else 0) := by
    intro S; split_ifs <;> ring
  unfold risk01
  unfold π
  rw [Finset.sum_congr rfl (fun S _ => h1 S), Finset.sum_sub_distrib,
    post_sum (Ωf_nonempty K), Finset.sum_ite_eq]
  split_ifs with ha
  · rfl
  · rw [post_of_not_mem ha]

/-- **T07(ii)(a)**: `a` minimises the posterior 0–1 risk over all subsets of `[p]` iff
`a ∈ argmax_Ω F`. -/
theorem risk01_min_iff (a : Finset (Fin p)) :
    (∀ b, risk01 K F a ≤ risk01 K F b) ↔ IsArgmax F (Ωf p K) a := by
  have hZ : 0 < ∑ T ∈ Ωf p K, Real.exp (F T) := sum_exp_pos (Ωf_nonempty K)
  simp only [risk01_eq, sub_le_sub_iff_left]
  unfold π
  constructor
  · intro h
    have ha : a ∈ Ωf p K := by
      by_contra ha
      have h0 := h ∅
      rw [post_of_not_mem ha, post_of_mem (empty_mem_Ωf K)] at h0
      have : 0 < Real.exp (F ∅) / ∑ T ∈ Ωf p K, Real.exp (F T) := div_pos (Real.exp_pos _) hZ
      linarith
    refine ⟨ha, fun T hT => ?_⟩
    have hT' := h T
    rw [post_of_mem hT, post_of_mem ha] at hT'
    exact Real.exp_le_exp.mp ((div_le_div_iff_of_pos_right hZ).mp hT')
  · intro ha b
    by_cases hb : b ∈ Ωf p K
    · rw [post_of_mem hb, post_of_mem ha.1]
      exact div_le_div_of_nonneg_right (Real.exp_le_exp.mpr (ha.2 b hb)) hZ.le
    · rw [post_of_not_mem hb]; exact post_nonneg _ _ _

/-- **T07(ii)(a)**: the HPM `S†` minimises the posterior 0–1 risk. -/
theorem hpm_min_risk01 (rk : Finset (Fin p) → ℕ) {Sd : Finset (Fin p)}
    (hd : IsLeastArgmax rk F (Ωf p K) Sd) : ∀ b, risk01 K F Sd ≤ risk01 K F b :=
  (risk01_min_iff K F Sd).mpr hd.1

/-- `ρ_H(a) = Σ_j PIP_j + ψ_PIP(a)` (PROOF_v2, proof of Theorem bayes (b)). -/
theorem riskH_eq (a : Finset (Fin p)) :
    riskH K F a = ∑ j, PIP K F j + psi (PIP K F) a := by
  have hA := Ωf_nonempty (p := p) K
  have hsum := post_sum (F := F) hA
  have hcard : ∀ s : Finset (Fin p), ((s.card : ℕ) : ℝ) = ∑ j, if j ∈ s then (1 : ℝ) else 0 := by
    intro s; rw [Finset.sum_boole]; congr 2; ext j; simp
  have hj : ∀ j, ∑ S ∈ Ωf p K, post F (Ωf p K) S * (if j ∈ symmDiff a S then (1 : ℝ) else 0) =
      PIP K F j + if j ∈ a then 1 - 2 * PIP K F j else 0 := by
    intro j
    by_cases hja : j ∈ a
    · have : ∀ S, post F (Ωf p K) S * (if j ∈ symmDiff a S then (1 : ℝ) else 0) =
          post F (Ωf p K) S - (if j ∈ S then post F (Ωf p K) S else 0) := by
        intro S; by_cases hjS : j ∈ S <;> simp [Finset.mem_symmDiff, hja, hjS]
      rw [Finset.sum_congr rfl (fun S _ => this S), Finset.sum_sub_distrib, hsum]
      simp only [hja, ↓reduceIte]
      unfold PIP; ring
    · have : ∀ S, post F (Ωf p K) S * (if j ∈ symmDiff a S then (1 : ℝ) else 0) =
          (if j ∈ S then post F (Ωf p K) S else 0) := by
        intro S; by_cases hjS : j ∈ S <;> simp [Finset.mem_symmDiff, hja, hjS]
      rw [Finset.sum_congr rfl (fun S _ => this S)]
      simp only [hja, ↓reduceIte]
      unfold PIP; ring
  have hpsi : psi (PIP K F) a = ∑ j, if j ∈ a then 1 - 2 * PIP K F j else 0 := by
    unfold psi; rw [Finset.sum_ite_mem, Finset.univ_inter]
  unfold riskH
  rw [hpsi, ← Finset.sum_add_distrib]
  simp_rw [hcard, Finset.mul_sum]
  rw [Finset.sum_comm]
  exact Finset.sum_congr rfl fun j _ => hj j

theorem mem_Jplus {q : Fin p → ℝ} {j : Fin p} : j ∈ Jplus q ↔ 1 / 2 < q j := by
  simp [Jplus]

theorem coef_nonneg_of_notMem_Jplus {q : Fin p → ℝ} {j : Fin p} (hj : j ∉ Jplus q) :
    0 ≤ 1 - 2 * q j := by
  have : q j ≤ 1 / 2 := not_lt.mp fun h => hj (mem_Jplus.mpr h)
  linarith

theorem coef_neg_of_mem_Jplus {q : Fin p → ℝ} {j : Fin p} (hj : j ∈ Jplus q) :
    1 - 2 * q j < 0 := by
  have := mem_Jplus.mp hj
  linarith

/-- `ψ_q(a) = ψ_q(a ∩ J₊) + ψ_q(a ∖ J₊)`. -/
theorem psi_split (q : Fin p → ℝ) (a : Finset (Fin p)) :
    psi q a = psi q (a ∩ Jplus q) + psi q (a \ Jplus q) :=
  (sum_inter_add_sum_sdiff a (Jplus q) (fun j => 1 - 2 * q j)).symm

theorem psi_sdiff_Jplus_nonneg (q : Fin p → ℝ) (a : Finset (Fin p)) :
    0 ≤ psi q (a \ Jplus q) :=
  sum_nonneg fun _ hj => coef_nonneg_of_notMem_Jplus (mem_sdiff.mp hj).2

/-- On subsets of `J₊`, `ψ_q` is antitone. -/
theorem psi_anti_Jplus (q : Fin p → ℝ) {b c : Finset (Fin p)} (hbc : b ⊆ c)
    (hc : c ⊆ Jplus q) : psi q c ≤ psi q b := by
  have h := sum_sdiff (f := fun j => 1 - 2 * q j) hbc
  have hn : ∑ j ∈ c \ b, (1 - 2 * q j) ≤ 0 :=
    sum_nonpos fun _ hj => (coef_neg_of_mem_Jplus (hc (mem_sdiff.mp hj).1)).le
  unfold psi
  linarith

/-- **Lemma psi (a)**: `J₊(q)` minimises `ψ_q` over all subsets. -/
theorem psi_Jplus_le (q : Fin p → ℝ) (a : Finset (Fin p)) : psi q (Jplus q) ≤ psi q a := by
  have h1 := psi_anti_Jplus q (inter_subset_right : a ∩ Jplus q ⊆ Jplus q) subset_rfl
  have h2 := psi_split q a
  have h3 := psi_sdiff_Jplus_nonneg q a
  linarith

/-- **Lemma psi (a)**, uniqueness: `J₊(q)` is the unique minimiser iff no `q_j = 1/2`. -/
theorem psi_Jplus_unique_iff (q : Fin p → ℝ) :
    (∀ a, (∀ b, psi q a ≤ psi q b) → a = Jplus q) ↔ ∀ j, q j ≠ 1 / 2 := by
  constructor
  · intro h j hj
    have hjn : j ∉ Jplus q := fun hm => by have := mem_Jplus.mp hm; linarith
    have heq : psi q (insert j (Jplus q)) = psi q (Jplus q) := by
      unfold psi
      rw [sum_insert hjn, hj]
      ring
    have hmin := h (insert j (Jplus q)) fun b => heq ▸ psi_Jplus_le q b
    exact hjn (hmin ▸ mem_insert_self j (Jplus q))
  · intro h a ha
    have hle := ha (Jplus q)
    have hsplit := psi_split q a
    have hdiff := psi_sdiff_Jplus_nonneg q a
    have hinter := psi_anti_Jplus q (inter_subset_right : a ∩ Jplus q ⊆ Jplus q) subset_rfl
    refine Subset.antisymm (fun j hj => ?_) (fun j hj => ?_)
    · by_contra hjJ
      have hqj : q j < 1 / 2 := lt_of_le_of_ne (not_lt.mp fun h' => hjJ (mem_Jplus.mpr h')) (h j)
      have hsingle : 1 - 2 * q j ≤ psi q (a \ Jplus q) :=
        single_le_sum (f := fun i => 1 - 2 * q i)
          (fun _ hi => coef_nonneg_of_notMem_Jplus (mem_sdiff.mp hi).2)
          (mem_sdiff.mpr ⟨hj, hjJ⟩)
      linarith
    · by_contra hja
      have hjd : j ∈ Jplus q \ (a ∩ Jplus q) :=
        mem_sdiff.mpr ⟨hj, fun hm => hja (mem_inter.mp hm).1⟩
      have hsd := sum_sdiff (f := fun i => 1 - 2 * q i)
        (inter_subset_right : a ∩ Jplus q ⊆ Jplus q)
      have hera := add_sum_erase (Jplus q \ (a ∩ Jplus q)) (fun i => 1 - 2 * q i) hjd
      have hrest : ∑ i ∈ (Jplus q \ (a ∩ Jplus q)).erase j, (1 - 2 * q i) ≤ 0 :=
        sum_nonpos fun _ hi =>
          (coef_neg_of_mem_Jplus (mem_sdiff.mp (mem_of_mem_erase hi)).1).le
      have hcj := coef_neg_of_mem_Jplus hj
      unfold psi at hle hsplit hdiff
      linarith

/-- **T07(ii)(b)**: the MPM minimises the posterior Hamming risk over all subsets. -/
theorem mpm_min_riskH (a : Finset (Fin p)) :
    riskH K F (Jplus (PIP K F)) ≤ riskH K F a := by
  rw [riskH_eq, riskH_eq]
  linarith [psi_Jplus_le (PIP K F) a]

/-- **T07(ii)(b)**, uniqueness: the MPM is the unique Hamming-risk minimiser iff no
`PIP_j = 1/2`. -/
theorem mpm_unique_iff :
    (∀ a, (∀ b, riskH K F a ≤ riskH K F b) → a = Jplus (PIP K F)) ↔
      ∀ j, PIP K F j ≠ 1 / 2 := by
  rw [← psi_Jplus_unique_iff]
  simp only [riskH_eq, add_le_add_iff_left]

/-- **Lemma psi (b)**, capped. If `a* ⊆ J₊(q)`, `|a*| = min(K', |J₊(q)|)` and every `q_j` on `a*`
is at least every `q_k` on `J₊(q) ∖ a*`, then `a*` minimises `ψ_q` over `{a : |a| ≤ K'}`. -/
theorem psi_capped_le (q : Fin p → ℝ) (K' : ℕ) (astar : Finset (Fin p))
    (hsub : astar ⊆ Jplus q) (hcard : astar.card = min K' (Jplus q).card)
    (htop : ∀ j ∈ astar, ∀ k ∈ Jplus q \ astar, q k ≤ q j) :
    ∀ a : Finset (Fin p), a.card ≤ K' → psi q astar ≤ psi q a := by
  intro a ha
  have hpa : psi q (a ∩ Jplus q) ≤ psi q a := by
    have := psi_split q a
    have := psi_sdiff_Jplus_nonneg q a
    linarith
  have ha'J : a ∩ Jplus q ⊆ Jplus q := inter_subset_right
  have hca' : (a ∩ Jplus q).card ≤ astar.card := by
    rw [hcard]
    exact le_min ((card_le_card inter_subset_left).trans ha) (card_le_card ha'J)
  have e1 : psi q astar = psi q (astar ∩ (a ∩ Jplus q)) + psi q (astar \ (a ∩ Jplus q)) :=
    (sum_inter_add_sum_sdiff astar (a ∩ Jplus q) (fun j => 1 - 2 * q j)).symm
  have e2 : psi q (a ∩ Jplus q) =
      psi q ((a ∩ Jplus q) ∩ astar) + psi q ((a ∩ Jplus q) \ astar) :=
    (sum_inter_add_sum_sdiff (a ∩ Jplus q) astar (fun j => 1 - 2 * q j)).symm
  rw [inter_comm (a ∩ Jplus q) astar] at e2
  have hc1 := card_sdiff_add_card_inter astar (a ∩ Jplus q)
  have hc2 := card_sdiff_add_card_inter (a ∩ Jplus q) astar
  rw [inter_comm (a ∩ Jplus q) astar] at hc2
  have hD : ((a ∩ Jplus q) \ astar).card ≤ (astar \ (a ∩ Jplus q)).card := by omega
  have key : psi q (astar \ (a ∩ Jplus q)) ≤ psi q ((a ∩ Jplus q) \ astar) := by
    obtain ⟨t, ht, h1, h2⟩ : ∃ t : ℝ, 1 / 2 ≤ t ∧ (∀ j ∈ astar \ (a ∩ Jplus q), t ≤ q j) ∧
        ∀ k ∈ (a ∩ Jplus q) \ astar, q k ≤ t := by
      rcases ((a ∩ Jplus q) \ astar).eq_empty_or_nonempty with he | hne
      · refine ⟨1 / 2, le_rfl, fun j hj => (mem_Jplus.mp (hsub (mem_sdiff.mp hj).1)).le, ?_⟩
        intro k hk
        rw [he] at hk
        exact absurd hk (notMem_empty k)
      · obtain ⟨k0, hk0, hmax⟩ := exists_max_image _ q hne
        have hk0J : k0 ∈ Jplus q \ astar :=
          mem_sdiff.mpr ⟨ha'J (mem_sdiff.mp hk0).1, (mem_sdiff.mp hk0).2⟩
        exact ⟨q k0, (mem_Jplus.mp (mem_sdiff.mp hk0J).1).le,
          fun j hj => htop j (mem_sdiff.mp hj).1 k0 hk0J, hmax⟩
    have s1 : psi q (astar \ (a ∩ Jplus q)) ≤ (astar \ (a ∩ Jplus q)).card • (1 - 2 * t) :=
      sum_le_card_nsmul (astar \ (a ∩ Jplus q)) (fun j => 1 - 2 * q j) (1 - 2 * t)
        fun j hj => by have := h1 j hj; linarith
    have s2 : ((a ∩ Jplus q) \ astar).card • (1 - 2 * t) ≤ psi q ((a ∩ Jplus q) \ astar) :=
      card_nsmul_le_sum ((a ∩ Jplus q) \ astar) (fun j => 1 - 2 * q j) (1 - 2 * t)
        fun k hk => by have := h2 k hk; linarith
    rw [nsmul_eq_mul] at s1 s2
    have hDr : (((a ∩ Jplus q) \ astar).card : ℝ) ≤ (astar \ (a ∩ Jplus q)).card := by
      exact_mod_cast hD
    have hmul : ((astar \ (a ∩ Jplus q)).card : ℝ) * (1 - 2 * t) ≤
        (((a ∩ Jplus q) \ astar).card : ℝ) * (1 - 2 * t) :=
      mul_le_mul_of_nonpos_right hDr (by linarith)
    linarith
  linarith

/-- Existence of the capped action `a*` (any deterministic tie rule selects one). -/
theorem exists_capped (q : Fin p → ℝ) (K' : ℕ) :
    ∃ astar : Finset (Fin p), astar ⊆ Jplus q ∧ astar.card = min K' (Jplus q).card ∧
      ∀ j ∈ astar, ∀ k ∈ Jplus q \ astar, q k ≤ q j := by
  obtain ⟨astar, hmem, hmax⟩ :=
    exists_max_image ((Jplus q).powersetCard (min K' (Jplus q).card)) (fun b => ∑ j ∈ b, q j)
      (powersetCard_nonempty.mpr (min_le_right _ _))
  rw [mem_powersetCard] at hmem
  refine ⟨astar, hmem.1, hmem.2, fun j hj k hk => ?_⟩
  by_contra hlt
  have hlt' : q j < q k := not_le.mp hlt
  have hk' := mem_sdiff.mp hk
  have hkn : k ∉ astar.erase j := fun h => hk'.2 (mem_of_mem_erase h)
  have hb : insert k (astar.erase j) ∈ (Jplus q).powersetCard (min K' (Jplus q).card) := by
    rw [mem_powersetCard]
    refine ⟨insert_subset hk'.1 ((erase_subset j astar).trans hmem.1), ?_⟩
    rw [card_insert_of_notMem hkn, card_erase_of_mem hj, ← hmem.2]
    have := card_pos.mpr ⟨j, hj⟩
    omega
  have h' : ∑ x ∈ insert k (astar.erase j), q x ≤ ∑ x ∈ astar, q x := hmax _ hb
  rw [sum_insert hkn, ← add_sum_erase astar q hj] at h'
  linarith

/-- **T07(ii)(c)**: the capped MPM `a*` (with `K' = K`, `q = PIP`) minimises `ρ_H` over `Ω`. -/
theorem capped_mpm_min_riskH (astar : Finset (Fin p))
    (hsub : astar ⊆ Jplus (PIP K F)) (hcard : astar.card = min K (Jplus (PIP K F)).card)
    (htop : ∀ j ∈ astar, ∀ k ∈ Jplus (PIP K F) \ astar, PIP K F k ≤ PIP K F j) :
    astar ∈ Ωf p K ∧ ∀ a ∈ Ωf p K, riskH K F astar ≤ riskH K F a := by
  refine ⟨by simp [Ωf, hcard], fun a ha => ?_⟩
  rw [riskH_eq, riskH_eq]
  have := psi_capped_le (PIP K F) K astar hsub hcard htop a (mem_filter.mp ha).2
  linarith

/-! ## T07(iii): target versus reported decisions -/

/-- **T07(iii)(a)**: for a nonempty scored set `𝒮 ⊆ Ω`, `Ŝ = S†` iff `S† ∈ 𝒮`. -/
theorem reported_eq_hpm_iff (rk : Finset (Fin p) → ℕ) (hrk : Function.Injective rk)
    {𝒮 : Finset (Finset (Fin p))} (h𝒮 : 𝒮 ⊆ Ωf p K) {Sd Sh : Finset (Fin p)}
    (hd : IsLeastArgmax rk F (Ωf p K) Sd) (hh : IsLeastArgmax rk F 𝒮 Sh) :
    Sh = Sd ↔ Sd ∈ 𝒮 := by
  constructor
  · intro h; rw [← h]; exact hh.1.1
  · intro hd𝒮
    have h1 : rk Sh ≤ rk Sd := hh.2 Sd ⟨hd𝒮, fun T hT => hd.1.2 T (h𝒮 hT)⟩
    have hFle : F Sd ≤ F Sh := hh.1.2 Sd hd𝒮
    have h2 : rk Sd ≤ rk Sh :=
      hd.2 Sh ⟨h𝒮 hh.1.1, fun T hT => (hd.1.2 T hT).trans hFle⟩
    exact hrk (le_antisymm h1 h2)

/-- **T07(iii)(a)**: `Ŝ` minimises the posterior 0–1 risk iff `𝒮 ∩ argmax_Ω F ≠ ∅`. -/
theorem reported_min_risk01_iff (rk : Finset (Fin p) → ℕ)
    {𝒮 : Finset (Finset (Fin p))} (h𝒮 : 𝒮 ⊆ Ωf p K) {Sh : Finset (Fin p)}
    (hh : IsLeastArgmax rk F 𝒮 Sh) :
    (∀ b, risk01 K F Sh ≤ risk01 K F b) ↔ ∃ T ∈ 𝒮, IsArgmax F (Ωf p K) T := by
  rw [risk01_min_iff]
  constructor
  · intro h; exact ⟨Sh, hh.1.1, h⟩
  · rintro ⟨T, hT𝒮, hT⟩
    have hFT : F T ≤ F Sh := hh.1.2 T hT𝒮
    exact ⟨h𝒮 hh.1.1, fun U hU => (hT.2 U hU).trans hFT⟩

/-- **T07(iii)(b)**: with `F = log(ϖ m)` for a positive size-only weight and `m > 0`:
`{Ŝ = S₀} ∩ {S*_{s₀} ≠ S₀} ⊆ {S*_{s₀} ∉ 𝒮}`. -/
theorem reported_truth_needs_unscored (rk : Finset (Fin p) → ℕ) (hrk : Function.Injective rk)
    (m : Finset (Fin p) → ℝ) (hm : ∀ S, 0 < m S) (pw : ℕ → ℝ) (hpw : PosSizePrior K pw)
    {𝒮 : Finset (Finset (Fin p))} (h𝒮 : 𝒮 ⊆ Ωf p K) {S₀ Sstar : Finset (Fin p)}
    (hh : IsLeastArgmax rk (fun S => Real.log (pw S.card * m S)) 𝒮 S₀)
    (hstar : IsLeastArgmax rk m (sizeClass p S₀.card) Sstar) (hne : Sstar ≠ S₀) :
    Sstar ∉ 𝒮 := by
  intro hin
  have hS₀𝒮 : S₀ ∈ 𝒮 := hh.1.1
  have hS₀K : S₀.card ≤ K := (mem_filter.mp (h𝒮 hS₀𝒮)).2
  have hc : Sstar.card = S₀.card := by
    have := hstar.1.1; simp only [sizeClass, mem_filter, mem_univ, true_and] at this; exact this
  have hpwpos : 0 < pw S₀.card := hpw _ hS₀K
  have hS₀class : S₀ ∈ sizeClass p S₀.card := by simp [sizeClass]
  have hFle : Real.log (pw Sstar.card * m Sstar) ≤ Real.log (pw S₀.card * m S₀) := hh.1.2 Sstar hin
  rw [hc, Real.log_le_log_iff (mul_pos hpwpos (hm _)) (mul_pos hpwpos (hm _))] at hFle
  have hm1 : m Sstar ≤ m S₀ := le_of_mul_le_mul_left hFle hpwpos
  have hm2 : m S₀ ≤ m Sstar := hstar.1.2 S₀ hS₀class
  have hmeq : m Sstar = m S₀ := le_antisymm hm1 hm2
  have r1 : rk Sstar ≤ rk S₀ :=
    hstar.2 S₀ ⟨hS₀class, fun T hT => by rw [← hmeq]; exact hstar.1.2 T hT⟩
  have r2 : rk S₀ ≤ rk Sstar := by
    refine hh.2 Sstar ⟨hin, fun T hT => ?_⟩
    have := hh.1.2 T hT
    simp only at this ⊢
    rw [hc, hmeq]; exact this
  exact hne (hrk (le_antisymm r1 r2))

/-- **T07(iii)(c)**: PIP error bounds the excess Hamming risk. For any PIP estimate `q̂`, action
class `𝒜`, `â ∈ 𝒜` minimising `ψ_q̂` over `𝒜`, and `a_opt ∈ 𝒜` minimising `ρ_H` over `𝒜`:
`0 ≤ ρ_H(â) - ρ_H(a_opt) ≤ 2 Σ_{j ∈ â △ a_opt} |q̂_j - PIP_j| ≤ 2 Σ_j |q̂_j - PIP_j|`. -/
theorem excess_riskH_le (qhat : Fin p → ℝ) (𝒜 : Finset (Finset (Fin p)))
    {ahat aopt : Finset (Fin p)} (hahat : ahat ∈ 𝒜) (hahat_min : ∀ a ∈ 𝒜, psi qhat ahat ≤ psi qhat a)
    (haopt : aopt ∈ 𝒜) (haopt_min : ∀ a ∈ 𝒜, riskH K F aopt ≤ riskH K F a) :
    0 ≤ riskH K F ahat - riskH K F aopt ∧
      riskH K F ahat - riskH K F aopt ≤ 2 * ∑ j ∈ symmDiff ahat aopt, |qhat j - PIP K F j| ∧
      2 * ∑ j ∈ symmDiff ahat aopt, |qhat j - PIP K F j| ≤ 2 * ∑ j, |qhat j - PIP K F j| := by
  have hconst : ∀ x, riskH K F x = ∑ j, PIP K F j + psi (PIP K F) x := riskH_eq K F
  set D : Fin p → ℝ := fun j => 2 * (qhat j - PIP K F j) with hD
  have key : ∀ x, psi (PIP K F) x = psi qhat x + ∑ j ∈ x, D j := by
    intro x; unfold psi; rw [← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun j _ => by simp only [hD]; ring
  have split : ∀ x y : Finset (Fin p), ∑ j ∈ x, D j = ∑ j ∈ x \ y, D j + ∑ j ∈ x ∩ y, D j := by
    intro x y
    rw [← Finset.sum_union (Finset.disjoint_sdiff_inter x y), Finset.sdiff_union_inter]
  have hsd : ∑ j ∈ symmDiff ahat aopt, |qhat j - PIP K F j| =
      ∑ j ∈ ahat \ aopt, |qhat j - PIP K F j| + ∑ j ∈ aopt \ ahat, |qhat j - PIP K F j| := by
    rw [symmDiff_def, Finset.sup_eq_union, Finset.sum_union disjoint_sdiff_sdiff]
  have hmin := hahat_min aopt haopt
  have b1 : ∑ j ∈ ahat \ aopt, D j ≤ 2 * ∑ j ∈ ahat \ aopt, |qhat j - PIP K F j| := by
    rw [Finset.mul_sum]
    exact Finset.sum_le_sum fun j _ => by simp only [hD]; nlinarith [le_abs_self (qhat j - PIP K F j)]
  have b2 : -∑ j ∈ aopt \ ahat, D j ≤ 2 * ∑ j ∈ aopt \ ahat, |qhat j - PIP K F j| := by
    rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
    exact Finset.sum_le_sum fun j _ => by simp only [hD]; nlinarith [neg_abs_le (qhat j - PIP K F j)]
  have hinter : ahat ∩ aopt = aopt ∩ ahat := Finset.inter_comm _ _
  refine ⟨by linarith [haopt_min ahat hahat], ?_, ?_⟩
  · rw [hconst, hconst, key, key, split ahat aopt, split aopt ahat, hinter, hsd]
    linarith
  · have hnn : ∀ j ∈ (univ : Finset (Fin p)), j ∉ symmDiff ahat aopt → 0 ≤ |qhat j - PIP K F j| :=
      fun j _ _ => abs_nonneg _
    have := Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ (symmDiff ahat aopt)) hnn
    linarith

/-- **T07(iii)(c)**, last clause: `MPM̂ = MPM` iff `q̂_j > 1/2 ⇔ PIP_j > 1/2` for every `j`. -/
theorem mpm_hat_eq_iff (qhat : Fin p → ℝ) :
    Jplus qhat = Jplus (PIP K F) ↔ ∀ j, (1 / 2 < qhat j ↔ 1 / 2 < PIP K F j) := by
  constructor
  · intro h j
    have := congrArg (fun s => j ∈ s) h
    simpa [Jplus] using this
  · intro h
    ext j
    simpa [Jplus] using h j

end SmcBvs.T07
