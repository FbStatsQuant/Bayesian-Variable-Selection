# W2-FAC-X Target 2 (first case) — STATEMENT of what this seat proves

Seat: T2 parallel prover (subagent). Status: **PROVED (by this seat, unchecked)** for Lemma L4r-S below — key-lemma check R11 (Codex Sol xhigh): L4r.0–L4r.3 **VERIFIED**;
everything beyond it is PARTIAL (see NOTES.md). FACB = `Theory_work/Wave2/W2-FAC-B/` (Theorem FAC-CS, PROVED-CHECKED);
X1 = `Theory_work/Wave2/W2-FAC-X/lemmas/X1_representation.md`. All results are asymptotic.

## 1. Setting (exact Gram, one factor, general loadings)

* Score, prior, cap K = min(p, ⌊n/2⌋), production move rule of the §6.10 local search, uncapped search: exactly as
  FACB STATEMENT §1 (D0, Method). Model G of FACB §1 (fixed raw design, X := CX^rD_x⁻¹, θ* := D_xβ, Y := Cy^r = Xθ* + Cε,
  y := Y/s, s² := ‖Y‖²/(n − 1), ε ~ N_n(0, σ²I)), S₀ := supp θ*, s₀ := |S₀|.
* **(EG-1F)** XᵀX = (n − 1)Σ_n exactly, Σ_n = Υ_n(λλᵀ + Ψ)Υ_n, Ψ := diag(1 − λ_j²), Υ_n diagonal ±1, with
  λ = λ^{(n)} ∈ [λ_lo, λ_hi]^p, 0 < λ_lo ≤ λ_hi < 1 **fixed constants**. The loadings are otherwise arbitrary
  (they may depend on n; no finiteness of the set of loading values and no class-size condition is needed for L4r-S).
* **(θ)** s₀ ≥ 1 fixed; the sign-corrected truth coefficients ((Υ_nθ*)_{i_r(n)})_{r ≤ s₀} = ϑ ∈ (ℝ ∖ {0})^{s₀} fixed;
  σ² > 0 fixed. (No (FS) no-cancellation condition is needed for the path lemma; it enters only the start lemma FACB L2.)
* Notation: ℓ_j := λ_j/√(1 − λ_j²), ℓ_lo, ℓ_hi the images of λ_lo, λ_hi, **R := ℓ_hi/ℓ_lo ≥ 1**,
  **γ̄ := ℓ_hi²/(1 + s₀ℓ_lo²)**, ψ_lo := 1 − λ_hi², L_n := log log n.
* **(P-S)** p = p_n ≤ n^{A₁} for n ≥ n₀ with a fixed A₁ satisfying

  A₁ < A_S := min{ 1/(2 max(1, γ̄)),  1/(2((1 + R)² − 1)) }.

  (Compound symmetry: R = 1, γ̄ = ℓ²/(1 + s₀ℓ²) < 1, so A_S = 1/6. Two classes λ ∈ {0.2, 0.95}: R = 14.9,
  A_S ≈ 0.002. The proof gives the slightly better γ̄ = ℓ_hi²/(1 + Σ_{i∈S₀}ℓ_i²) if the truths' loadings are known.)

## 2. Reference statistic (exact; L4r.0)

Υ_n = I w.l.o.g. (FACB L1.0). There are η ~ N(0, 1), ξ ~ N(0, I_p), r ~ χ²_{n−1−p}, independent, with
g := Xᵀε/(σ√(n − 1)) = λη + Ψ^{1/2}ξ, such that every score is a function of (η, ξ, r) (FACB L1.1, verbatim). With
a := n² − 1, ε_j := (aψ_j/(aψ_j + 1))^{1/2} ∈ (1 − 1/(aψ_lo), 1), ℓ'_j := ε_jℓ_j, and for S₀ ⊆ T ⊆ [p], K_T := T ∖ S₀:

  X_T := (Σ_{i∈K_T} ε_i²ℓ_iξ_i − ϱ) / (1 + Σ_{i∈T} ℓ'_i²),   ϱ := η − Σ_{i∈S₀}ε_i²ℓ_iξ_i + (√(n − 1)/σ)Σ_{i∈S₀}(1 − ε_i²)λ_iθ*_i

(ϱ is T-independent). The **reference statistic** of a null j is |ξ_j − ℓ_jX_T|, with exact drift identity
X_{T∖j} = X_T − ℓ'_jε_j(ξ_j − ℓ_jX_T)/(1 + ‖ℓ'_T‖² − ℓ'_j²). The exact deletion gain is
G_del(j; T) = Δ_k + ½e_j(T) − ν log(1 + M_T(1 + γ'_j(T))ε_j²(ξ_j − ℓ_jX_T)²/ν), where e_j(T) (|e_j| ≤ 3/((n − 1)ψ_lo)),
γ'_j(T) := ℓ'_j²/(1 + ‖ℓ'_T‖² − ℓ'_j²) and ε_j depend on j **only through λ_j**, and M_T > 0 does not depend on j.
Hence among nulls with a common loading value the best deletion is **exactly** the argmin of |ξ_j − ℓ_jX_T|.
(For λ_j ≡ λ this is FACB L1.3–L1.4 up to the ridge reparametrisation; ϱ = η − Σ_{S₀}ℓ_iξ_i + o_P(1) and X_T = (Σ_{i∈T}ℓ_iξ_i − η)/(1 + ‖ℓ_T‖²) + o_P(1); corrected by the lead after R11 item 3 — unused by the proof.)

## 3. Lemma L4r-S (the path lemma; proved in L4r_path.md §L4r.3)

Under §1 including (P-S), there are an event E_n with P(E_n) → 1 and n₀ (depending on λ_lo, λ_hi, ϑ, σ, s₀, A₁) such
that for n ≥ n₀, on E_n, simultaneously for **every** set T with S₀ ⊆ T ⊆ [p]:

1. if T ≠ S₀, the best feasible move at T is a null deletion; every maximiser of F over the neighbourhood of T is a
   null deletion j° ∈ argmax_{j∈K_T} G_del(j; T) (so j° is the argmin of the reference statistic within its loading
   value), and G_del(j°; T) ≥ c_del log n, c_del := ½ − A₁max(1, γ̄) − o(1) > 0;
2. every addition (l ∉ T) has gain ≤ −c_add log n, c_add := ½ − A₁((1 + R)² − 1) − o(1) > 0;
3. every null-out swap (j ∈ K_T, l ∉ T) has gain ≤ G_del(j; T) − c_add log n < G_del(j°; T);
4. every truth deletion and every truth-out swap has negative gain (≤ −c n);
5. at T = S₀ no feasible neighbour has F ≥ F(S₀) (strict local maximum).

Consequently, for every start T₀ with S₀ ⊆ T₀ ⊆ [p] (in particular S* = [p] ∖ N for every N ⊆ [p] ∖ S₀, so the
data-dependence of the block structure N₀ is irrelevant), the uncapped search makes exactly |T₀ ∖ S₀| moves, each the
deletion of a null that is the within-loading-value argmin of |ξ_j − ℓ_jX_T|, and ends at S₀ as a strict local maximum.
For every integer cap a ≥ |T₀ ∖ S₀| the capped search ends at S₀ certified (single-search prefix property, FACB L4.5(1)).

This is the analogue of FACB L4 (deliverable items: only null deletions, each the argmin of the reference statistic;
additions lose ≥ c log n; swaps below the chosen deletion; truth moves lose; ends at S₀, strict local max) on the range
p ≤ n^{A₁}, A₁ < A_S. It does **not** need the per-class interval structure, the order-statistics events E5–E7, or
finitely many loading classes.

## 4. Proved partial results toward the full range (L4r_path.md §L4r.4–L4r.5)

* **L4r.4 (deterministic per-class gap invariant).** Along any path of best null deletions, a class's own deletions never
  make its centre ℓ_cX_T cross a kept point of the class; a deletion in another class c′ can make class c's centre cross
  a kept class-c point only if d_c(T) ≤ θ_{cc′}(T)(d_c(T)² + C/n)^{1/2} with θ_{cc′}(T) = ℓ_cℓ_{c′}((1 + γ'_c)/(1 + γ'_{c′}))^{1/2}/
  (1 + ‖ℓ'_T‖² − ℓ'_{c′}²); if no crossing occurs, each class's deleted set is the interval of its sorted ξ's between the
  two kept points adjacent to its centre. In the bulk (θ ≤ C/m) a crossing needs d_c ≤ C/(m√n).
* **L4r.5 (static per-class B3).** Under per-class two-sidedness and class sizes ≥ c_*p, X_T ≤ max{ε H̄/ℓ_lo,
  max_c Δ_c/(2ℓ_c)} (and symmetrically), with Δ_c the per-class hole asymmetry.

## 5. Not proved (exact obstruction in NOTES.md)

The full range of the ticket (p ≤ n^A for A up to FACB's ½-type range) for finitely many classes. The failing steps are
FACB L4.3 (B1)/(B2) per class (classes become one-sided in the bulk; Δ_c is not controlled by the FACB recursion under
cross-class drift) and FACB L4.4 (E-side) (minority-side deletions; no centre-ratio invariant: max_c ℓ_c|X_T|/H̄ reaches
1.75 on actual paths), with numerical evidence in numerics/N_T2_summary.md.
