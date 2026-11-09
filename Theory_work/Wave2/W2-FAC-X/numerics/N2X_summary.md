# N2X — Target 2 diagnosis: one factor, heterogeneous loadings (numerics/n2x_loadings.py → N2X_raw.jsonl, n2x_log.txt)

Designs: loadings two03_09 (λ alternating 0.3/0.9), two05_095 (0.5/0.95), unif02_09 (λ_j ~ U[0.2, 0.9], fixed), cs07
(CS control, λ² = 0.7). Modes: 'ref' = exact reference design (iid_core mode="ref": W = N·I, a = 0, factor row of norm
√N — Gram equal to the population compound/factor structure up to the rank-one noise term, the exact-Gram analogue)
at n ∈ {1e5, 1e8}; 'iid' = iid Gaussian rows at n ∈ {1e5, 1e6}. p ∈ {100, 400}, s0 = 4, 2 seeds: 64 data sets. Uncapped
LS0 path from [p].

* 64/64 paths are pure null deletions ending at S0; no ties; max addition gain/log n ≤ −0.047 (smallest margins at
  p = 400, n = 1e5, i.e. log p/log n = 0.52).
* rank_var = max (over steps) rank of the deleted null in the variable-centre reference statistic
  |ξ_j − ℓ_jX_T|/√(1 − ℓ_j²/(κ₀ + ‖ℓ_T‖²)), X_T = (ℓ_Tᵀξ_T − η)/(‖ℓ_T‖² + κ₀) (κ₀ ≈ 1 approximated): **0–2 in all 'ref'
  runs** (0 at n = 1e8; the 1–2 at n = 1e5 come from the κ₀ ≈ 1 approximation) — the exact path is the argmin of the
  variable-centre statistic, as the whitened reduction predicts. rank_common (common centre ℓ̄X_T) up to 19 in 'ref'
  runs of the two-class designs: a single common centre does **not** describe the path when loadings differ.
* 'iid' runs: rank_var 2–65 (the Wishart band of Target 1, of the same size as in the CS control).
Interpretation: general loadings keep the one-scalar centre X_T but with loading-specific centres ℓ_jX_T; the deleted
set is no longer an interval of the sorted ξ's. For finitely many loading values the reference path keeps an exact
interval hole **within each loading class** (see T2 notes).
