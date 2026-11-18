# D18C reply (Claude Opus 5.5 high, fresh, delegate 6af4955e; 2026-11-17) — summary of record (full reply in the delegate thread)

- Step 1 Structure: CONFIRMED (a) finitely many patterns (labelled principal submatrices of Σ₀, zeros across copies);
  (b) λ_min(L Lᵀ + 0.1 I) = 0.1 (rank 70), E-1: the code's unit-diagonal matrix has λ_min = 0.1 − O(1e-13) (0.09999999999976);
  (c) placements: clustered columns 0, 214, 660, 295 for every p > 4088 (correlations with column 0: −0.707, −0.700, −0.687),
  θ = (1.4, 1.0, 1.8, 1.2); spread k·⌊p/4⌋, θ = (1.4, −1, 1.8, −1.2); (d) for p ≥ 16352 the spread truths are in different
  copies and Cov(W_j, Wᵀθ | W_U) = θ_j Var(W_j | W_U) ≥ |θ_j|·λ_min; B = coordinate hyperplanes, δ = 1.0; n ≥ 1636 correct.
- Step 2 Independent reproduction: CONFIRMED; greedy reproduces j=214: Cov −1.908384e-7 (Var 0.2004, δ² 1.8175e-13, |U| 15),
  j=0: 6.615e-7 (|U| 10), j=660: 0.149, j=295: 0.0757. Randomized greedy + swap search: j=0 Cov −6.896e-9 (Var 0.529) at
  U = {3648, 1914, 66, 1565, 1189, 572, 777, 4062, 323, 126, 1342, 3900, 2782, 4048, 1774}; j=214 −1.212e-8. Exact rational
  recomputation two ways (float Σ entries; exact L Lᵀ with diagonal 1) agree to ~9 digits; none zero. Spread p = 16000:
  greedy δ² 1.41643e-3 (j=4000), 0.128 (j=0); swap search Cov 2.382e-6 (Var 0.2727, δ² 2.08e-11) at
  U = {1437, 559, 3641, 2231, 3365, 1713, 4055, 2563, 3729, 3347, 3997, 2832, 3959, 1173, 1506}, exact-rational confirmed.
- Step 3: spread covered with a ≥ 0.1 (− 5e-14) for p ≥ 16352: CONFIRMED. Clustered not certifiable: CONFIRMED, margin
  ≤ 6.9e-9 (E-2). Reconciliation: CONFIRMED numerically; S-1: spread is effectively 0 for every p < 16352 (not "only p ≤ 8000").
- Step 4: `d18.py` computes what the verdict says; E-3: it uses L Lᵀ + 0.1 I (≤ 4.8e-14 from the code's diagonal).
D18C-VERDICT: spread=CONFIRMED; clustered=CONFIRMED; reconcile=CONFIRMED
