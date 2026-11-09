# T2 NOTES — status of this seat (W2-FAC-X Target 2, first case)

**Status: PARTIAL.** Lemma L4r-S is **PROVED (by this seat, unchecked)** on p ≤ n^{A₁}, A₁ < A_S(loadings); the full
range (FACB-type A up to ½) for finitely many loading classes is **not** proved. The exact failing steps are listed below.

## 1. What is proved (STATEMENT_T2.md §3; L4r_path.md §L4r.0–L4r.3)

* **Exact closed form (L4r.0)** for exact-Gram one-factor designs with **arbitrary** loadings λ_j ∈ [λ_lo, λ_hi] ⊂ (0, 1):
  the ridge score is still "diagonal + rank one" (H_U = Δ(I + ℓ'ℓ'ᵀ)Δ with ridge-modified loadings ℓ'_j = ε_jℓ_j,
  ε_j = 1 − O(n⁻²)), so every deletion/addition/swap gain is an explicit function of one scalar centre
  X_T = (Σ_{K_T}ε_i²ℓ_iξ_i − ϱ)/(1 + ‖ℓ'_T‖²) with the exact drift identity. κ₀ = 1 and ϱ = η − Σ_{S₀}ε_i²ℓ_iξ_i + O(n^{−3/2})
  (the truths' ξ enter ϱ because X_T is written over kept nulls only; written as a sum over all of T, with the truths'
  noise coordinates ξ_i included, the offset is exactly the ticket's ϱ = η up to an O(n^{−3/2}) ridge term). The ridge/determinant corrections are j-dependent only
  through λ_j, so **within a loading value the best deletion is exactly the argmin of |ξ_j − ℓ_jX_T|**; across values
  the comparison carries deterministic O(1/n) offsets. Validated: closed form = direct linear algebra (10⁻¹⁴) and
  closed-form paths = general production-path code (32/32 identical).
* **Lemma L4r-S** (all items of the deliverable: pure null deletions, each the within-loading-value argmin of the
  reference statistic; additions ≤ −c log n; swaps below the chosen deletion; truth moves lose; ends at S₀, strict
  local max) for A₁ < A_S := min{1/(2max(1, γ̄)), 1/(2((1 + R)² − 1))}, R = ℓ_hi/ℓ_lo, γ̄ = ℓ_hi²/(1 + s₀ℓ_lo²).
  The argument is uniform over all sets T ⊇ S₀ (no path structure); new ingredients: L4r.2(a) (the identity
  Σ_{K}ℓ'_iτ_i = κ'_SX_T + ϱ forces a kept null with |τ| ≤ H̄ + O(L_n), which removes all R-dependence from the deletion
  side) and L4r.2(b) (centre bound |X_T| ≤ (Z_m² + 2)^{1/2}/ℓ_lo + |ϱ| from top-square sums). For CS this gives
  A_S = 1/6 (vs FACB's regime (S) p ≤ n^{1/200}); for λ ∈ {0.2, 0.95} A_S ≈ 0.002. Needs neither finitely many classes
  nor class sizes ≥ cp nor (FS).
* **L4r.4 per-class gap invariant (deterministic):** own-class deletions never cross; a foreign deletion crosses only if
  d_c < θ_{cc′}(d_c² + C/n)^{1/2}; in the bulk this needs d_c ≤ C/(m√n). Exact (no offsets) for r = 1.
* **L4r.5 static per-class B3** (conditional on per-class two-sidedness): X_T ≤ max{0.34ε_bH̄/ℓ_lo + o(1), max_c Δ_c/(2ℓ_c)}.

## 2. Exact obstruction to the full range (L4r_path.md §L4r.6; numerics/N_T2_summary.md)

1. **Uniform route stops at ≈ A_S.** On sets the path never visits (S₀ ∪ same-sign low-loading nulls), additions
   have **positive** gains beyond A_S (CS at log p/log n = 0.33: +0.083 log n; {0.2, 0.95} at 0.155: +0.115 log n).
   Any proof past A_S must use the path.
2. **First failing step of the FACB route: (B2) per class.** FACB's recursion Δ_{i+1} ≤ max(Δ_i, g + 2d/(k − 1 + κ))
   uses that every step deletes from the one class. With r ≥ 2, a deletion in class c′ moves class c's centre by
   ℓ_cℓ_{c′}τ/(D' − ℓ'²_{c′}) without touching class c's hole, so Δ_c accumulates (backlash: Δ_c ≲ 2ℓ_c·TV(X)), and
   L4r.5 then only returns |X| ≤ TV(X) — the B2/B3 induction does not close. Numerically max Δ_c/(2ℓ_c) = 0.70H̄
   while max |X_T| = 0.074H̄ in the bulk: the per-class B3 route is quantitatively off by ~10×.
3. **(B1) per class fails:** classes become one-sided during the bulk (up to 30 steps with m ≥ 30; 20%/80% shares and
   r = 3), so L4r.5's hypothesis is false on actual paths.
4. **End phase (E-side) fails:** near balance the smallest-loading class is deleted first on either side (deletion
   statistic ≈ h·D'/(D' − ℓ'_c²)); minority-side deletions occur (up to 13/160 end-phase steps; never in CS); no
   centre-ratio invariant (max_c ℓ_c|X_T|/H̄ up to 1.75 on real paths). Additions still lose only thanks to the factor
   D'/(D' + ℓ'_c²) in the addition statistic — a correct end-phase invariant must be on h·(D'/(D' + ℓ'_c²))(1 + ℓ_c|X|/H̄)²
   itself, via the finite dynamics of signed loading counts.
5. **Per-class exact gap:** cross-class O(1/n) offsets make an exact FACB L4.1(i) analogue require excluding
   O(n^{−1/2}/m) near-coincidences on the data-dependent path (not done; X3-type band is the natural route). In the end
   phase (D' = O(1)) θ_{cc′} can exceed 1 and crossings are not excluded at all. Never observed numerically.

## 3. Numerical evidence (numerics/N_T2_summary.md)

366/366 exact-Gram paths from [p] (r ∈ {1, 2, 3}; λ down to 0.1 and up to 0.98, R up to 49; class shares 10–90%;
truths in low/high/mixed classes; n from 10⁴ to 10¹⁴; log p/log n up to 0.87) are pure null deletions ending at S₀,
no ties, per-class interval holes exact at every step, min addition margin 0.062 log n (r = 3, {0.2, 0.6, 0.95},
n = 10⁴, p = 3000). So nothing falsifies the full Target-2 path claim; the gap is in the proof technique.

## 4. Suggested next step (for HQ)

Replace FACB's per-class B1/B2/B3 by a **single weighted potential**: X_T is the ridge-regression slope of the kept ξ's
on their loadings (X_T = argmin_x Σ_K(ζ_i − ℓ'_ix)² + κ'_S(x + ϱ/κ'_S)²) and the path deletes the best-fitting point
(smallest leverage-adjusted residual). A bulk proof should bound the slope of a "residual-trimmed" regression directly
(the deleted set is, per class, the set of residuals below a common level ≈ d, up to O(n^{−1/2}) offsets), rather than
per-class hole asymmetries; the end phase should be a finite-state analysis of (counts per class and sign, W = X·D'/H̄)
with the addition statistic as the invariant.

## Files (all under Theory_work/Wave2/W2-FAC-X/T2/)

STATEMENT_T2.md, L4r_path.md, NOTES.md, numerics/{eg_core.py, eg_selftest.py, eg_selftest_out.txt, run_t2.py,
summarize.py, T2_raw.jsonl, T2_stress_raw.jsonl, run_t2_log.txt, run_t2_stress_log.txt, adversarial_T.py,
adversarial_T_out.txt, end_phase_detail.py, end_phase_detail_out.txt, N_T2_summary.md}.
