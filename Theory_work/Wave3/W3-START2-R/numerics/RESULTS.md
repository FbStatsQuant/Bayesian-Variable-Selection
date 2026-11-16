# W3-START2-R boundary numerics (Helper B) — OBSERVATIONS ONLY, not proofs

## Setup
* Ticket W3-START2-R, `TARGET.md` §3; statement `STATEMENT.md` v1.5. Production core `Scripts/SMC_BVS/core` (unchanged), compiled with Rcpp.
  **Deviation from the brief:** `v3.R` writes its compile cache to `<core>/.cpp_cache`, which is outside the write scope; I therefore pointed
  `W3START_CORE` at a byte-identical copy of the core in the temp folder (removed afterwards). Compilation succeeded.
* `r_common.R` = verbatim copy of `W3-START/numerics/start_common.R`. π₀(S₀) and o₀ = (1−π₀)/π₀ come from the coded start (`cpp_start_logmass`);
  T₁ from the block tables (`start_stats`). New code: `gens.R` (designs), `run_numerics.R` (driver), `summarise.R`, `make_tables.R`.
  Raw rows (not in git, not in the frozen content) are kept in /home/fb31/SMC_Theory_Department/helpers/W3-START2-R-numerics-out/ until ticket close; the scripts write to a git-ignored `out/`; `summary.csv` is the small tracked summary.
* Designs. Run 1: orthonormal frame of 1^⊥ (BASE L11.0), one truth e₁, null columns e_j, σ = 1, θ² = T/(N − T) so that δ²_{∅,1}/τ²_∅ = T = c log n + 2 log p;
  p = max(⌈n^A⌉, 17), nominal A ∈ {0.3, 0.9} (so p = 17 for A = 0.3 at all three n; the effective log p/log n there is 0.53, 0.42, 0.35).
  Run 2: BASE L11.3 (ρ² = 0.4, θ*₁² = 2(1+2A)σ² log n/(n−1), p = min(⌊n^A⌋, n−1), A = 0.9). Runs 3–4: Gaussian rows Σ = I, s₀ = 2, θ* = (1,1), σ = 1, p = 2n;
  run 4 adds one null (column 3) with population correlation ρ_n to truth 1: `lg0a` ρ_n = 2/√(n log n), `lg0b` ρ_n = 2/√n; run 3 is the ρ = 0 baseline.
* 10 seeds per cell everywhere, all n up to 3200 (no cell cut). 4 workers for runs 1–2, 8 for runs 3–4, all under `nice -n 10`. All 420 jobs status ok.
  Medians with [Q25, Q75] over the 10 seeds. Seeds are different across cells, so cells are independent samples.

## Run 1 — (V-cp), small p

| nominal A | n | p | c | target delta^2/tau^2 | ratio to v1.4 level (1+2A)log n | median pi0 [IQR] | median o0 | #seeds pi0>0.5 |
|---|---|---|---|---|---|---|---|---|
| 0.3 | 200 | 17 | 0.6 | 8.85 | 1.04 | 0.265 [0.114, 0.483] | 2.78 | 3/10 |
| 0.3 | 200 | 17 | 0.9 | 10.43 | 1.23 | 0.803 [0.113, 0.854] | 0.246 | 6/10 |
| 0.3 | 200 | 17 | 1.1 | 11.49 | 1.36 | 0.465 [0.193, 0.833] | 1.34 | 5/10 |
| 0.3 | 200 | 17 | 1.5 | 13.61 | 1.61 | 0.692 [0.343, 0.841] | 0.45 | 7/10 |
| 0.3 | 800 | 17 | 0.6 | 9.68 | 0.90 | 0.0285 [0.0131, 0.165] |   41 | 2/10 |
| 0.3 | 800 | 17 | 0.9 | 11.68 | 1.09 | 0.821 [0.517, 0.925] | 0.224 | 7/10 |
| 0.3 | 800 | 17 | 1.1 | 13.02 | 1.22 | 0.165 [0.0252, 0.308] | 5.08 | 1/10 |
| 0.3 | 800 | 17 | 1.5 | 15.69 | 1.47 | 0.679 [0.236, 0.867] | 0.483 | 7/10 |
| 0.3 | 3200 | 17 | 0.6 | 10.51 | 0.81 | 0.0494 [0.00169, 0.655] |  132 | 3/10 |
| 0.3 | 3200 | 17 | 0.9 | 12.93 | 1.00 | 0.361 [0.0866, 0.906] | 1.83 | 4/10 |
| 0.3 | 3200 | 17 | 1.1 | 14.54 | 1.13 | 0.853 [0.0839, 0.945] | 0.176 | 6/10 |
| 0.3 | 3200 | 17 | 1.5 | 17.77 | 1.38 | 0.945 [0.486, 0.962] | 0.0586 | 7/10 |
| 0.9 | 200 | 118 | 0.6 | 12.72 | 0.86 | 0.0401 [0.0182, 0.0967] | 25.4 | 0/10 |
| 0.9 | 200 | 118 | 0.9 | 14.31 | 0.96 | 0.443 [0.193, 0.788] | 1.69 | 5/10 |
| 0.9 | 200 | 118 | 1.1 | 15.37 | 1.04 | 0.454 [0.0525, 0.809] | 2.85 | 5/10 |
| 0.9 | 200 | 118 | 1.5 | 17.49 | 1.18 | 0.668 [0.248, 0.773] | 0.513 | 7/10 |
| 0.9 | 800 | 410 | 0.6 | 16.04 | 0.86 | 0.12 [0.0453, 0.716] | 7.34 | 4/10 |
| 0.9 | 800 | 410 | 0.9 | 18.05 | 0.96 | 0.0914 [0.0382, 0.556] | 11.5 | 3/10 |
| 0.9 | 800 | 410 | 1.1 | 19.39 | 1.04 | 0.336 [0.0367, 0.87] | 4.39 | 5/10 |
| 0.9 | 800 | 410 | 1.5 | 22.06 | 1.18 | 0.663 [0.273, 0.868] | 0.575 | 6/10 |
| 0.9 | 3200 | 1428 | 0.6 | 19.37 | 0.86 | 0.115 [0.0742, 0.481] | 7.78 | 3/10 |
| 0.9 | 3200 | 1428 | 0.9 | 21.79 | 0.96 | 0.355 [0.0119, 0.904] | 5.61 | 5/10 |
| 0.9 | 3200 | 1428 | 1.1 | 23.41 | 1.04 | 0.0278 [0.0111, 0.677] | 37.8 | 3/10 |
| 0.9 | 3200 | 1428 | 1.5 | 26.63 | 1.18 | 0.86 [0.344, 0.933] | 0.166 | 7/10 |

Observed: with 10 seeds per cell the median π₀(S₀) is not monotone in c within a (A, n) group and the seed-to-seed spread is as wide as the differences between c = 0.6, 0.9, 1.1 (e.g. A = 0.9, n = 3200: medians 0.115, 0.355, 0.028, 0.86); the only separation seen at every (A, n) is between c = 1.5 (π₀ > 0.5 in 6–7 of 10 seeds, median o₀ between 0.06 and 0.58) and c = 0.6 (median π₀ ≤ 0.27, o₀ from 2.8 up to 132), at both p regimes; the switch at c = 1 is not resolved at these n (the shift in the standardised gain is of order (c−1)√log n ≈ 0.2–0.3 for c = 0.9, 1.1 against Gaussian noise of order 1), and the "ratio to v1.4 level" column shows the p = 17 cells at c = 0.9 and 1.1 lie at 1.0–1.4 times the v1.4 level (1+2A)log n with A = 0.3, which here is not distinguishable from the c-based reading.

## Run 2 — F-2 at A = 0.9 (o₀/T₁)

| n | p | median o0/T1 [IQR] | median o0 [IQR] | median pi0 |
|---|---|---|---|---|
| 200 | 117 | 1.77 [1.51, 2.01] |  354 [6.46, 1857] | 0.00985 |
| 800 | 409 | 1.16 [ 1.1, 1.35] | 0.134 [0.112, 0.169] | 0.882 |
| 3200 | 1427 | 1.88 [1.05, 3.43] | 0.134 [0.0653, 0.202] | 0.882 |

Observed: o₀/T₁ has medians 1.77 (n = 200, where π₀ ≈ 0.01 and θ*² is still small), 1.16 (n = 800) and 1.88 (n = 3200; IQR [1.05, 3.43], one seed with π₀ = 0.41 and o₀/T₁ ≈ 19), i.e. it is of order 1 at n ≥ 800 but not visibly converging to 1 on this grid, and the n = 3200 spread is larger than at n = 800.

## Runs 3–4 — G-1 rate and (L-gain-0) boundary: o₀·√(n/log n)

| n | p | G-1 (rho=0) | lg0a rho=2/sqrt(n log n) | lg0b rho=2/sqrt(n) | G-1 o0/T1 | max over seeds (G-1 / lg0a / lg0b) |
|---|---|---|---|---|---|---|
| 200 | 400 |  1.9 [1.76,  2.6] | 2.63 [ 1.7, 3.38] | 2.21 [1.97, 3.39] |  1.2 | 5.07 / 21.1 / 69.8 |
| 400 | 800 |  1.9 [1.84, 2.18] | 1.91 [1.79, 3.12] | 1.87 [1.71, 2.08] | 1.15 | 2.84 / 4.38 / 3.03 |
| 800 | 1600 | 1.86 [1.69, 2.08] | 2.31 [ 1.9, 2.69] | 2.01 [1.82, 2.65] | 1.11 | 2.94 / 4.03 / 4.83 |
| 1600 | 3200 | 2.19 [1.88, 2.67] | 1.76 [1.69, 2.12] | 1.77 [1.69, 2.35] | 1.09 | 3.68 / 2.32 / 3.69 |
| 3200 | 6400 | 1.98 [1.82,  2.3] | 1.73 [1.69, 1.79] | 2.31 [1.92,  2.9] | 1.06 | 3.34 / 2.22 /   21 |

Observed (run 3): o₀√(n/log n) has median 1.9, 1.9, 1.86, 2.19, 1.98 for n = 200, …, 3200 (IQR within [1.7, 2.7]; max over seeds 5.1 at n = 200 and ≤ 3.7 afterwards), i.e. flat on this grid; median o₀/T₁ falls 1.2 → 1.06.
Observed (run 4): with ρ_n = 2/√(n log n) the median is 2.63, 1.91, 2.31, 1.76, 1.73 and with ρ_n = 2/√n it is 2.21, 1.87, 2.01, 1.77, 2.31, both between 1.7 and 2.7 at every n, comparable to the run-3 medians (1.86–2.19); the largest seed values (21.1 and 69.8 at n = 200, 21.0 at n = 3200 for ρ_n = 2/√n, where that seed has π₀ = 0.49) are isolated, and no systematic growth in n of the median or the IQR is visible for either ρ_n over this range (a √(log n)-type factor between the two cases would not be resolvable here).

## Caveats
Single-point observations at finite n with 10 seeds; no statement may cite them as support beyond "observed". Core copy used instead of the in-tree path (cache write scope), see Setup.
