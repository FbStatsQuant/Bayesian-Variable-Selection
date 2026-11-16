# W3-RM2-R numerics — RESULTS (boundary numerics for (V♭), (BM-W⁺), BM(c))

**Finite-n observations of the validated LS0 re-implementation, not evidence about asymptotic necessity.** The sufficient
constants of STATEMENT §2 (M_V⁰, c_TL⁰, c₀, κ₀) are proof artefacts and much larger than the levels probed here (κ ≤ 32);
nothing below says that the order σ² log n/n is, or is not, necessary in the limit. Design, tools and compute rules:
`SPEC.md`. Nothing in the production core was edited; the sampler, calibration, final local search and the posterior
input [POST] are **not** run.

## 0. What was run

* **Tools.** `rm2r_common.R` is the parent `rm2_common.R` (production score/context/partition from `Scripts/SMC_BVS/core`,
  compiled from a **copy** of the core in `$TMPDIR`, so the core directory was not written) with the same re-implemented
  start-mode DP `start_mode_dp` and `ls0_fast` (SW1-3 departures from production LS0 kept and documented in the file header:
  improvement > 1e-9; at the cap the current centre is returned; ties to the first maximum). New: designs P and G, the
  truth-removal statistic, visibility and mode-margin statistics. `validate.R` was re-run on this branch (`validate_out.txt`):
  306 scores agree with `v3_score` to 8.5e-13; the DP start mode has larger production start mass than all 600 single
  flips and 1985 random perturbations; `ls0_fast` equals a brute-force LS0 on production scores from 4 centres; the
  truth-removal margin of `ls0_fast` equals the production-score brute force to 2.8e-14; design P has the exact Gram
  (6.7e-16) and `delta2`/`delta2_blockmin` match direct projections/enumeration. **VALIDATION PASSED.**
* **Designs.** **P** (Ex-Proxy, fixed design, exact Gram): p = ⌊n/3⌋, q = ⌊n^b⌋, r² = log n/n (C₀ = 1), S₀ = {1},
  μ = θ_n x₁, σ = 1, b ∈ {0.3, 0.45}, n ∈ {400, 1600}; the n-fixed orthonormal frame comes from the QR of a centred
  Gaussian matrix (seed 1000 + n); seeds change the noise only (the same noise for every κ). **G** (Gaussian rows, two
  truths): parent design B1 at b = 0.375, p = 2n, |Q| = 2 + ⌈n^b⌉ (12 at n = 400, 18 at n = 1600), truth 1 θ₁ = 3,
  proxies of truth 1 at the parent strength (r fixed by the parent τ₀² with θ = (3, 1), so the leak set is the same for
  every κ), truth 2 swept: θ₂ = θ_n; the same seed gives the same X and noise for every κ.
* **Sweep.** θ_n² = κ σ² log n/n, κ ∈ {0.5, 1, 2, 4, 8, 16, 32}; 10 seeds per cell at n = 400, 6 at n = 1600.
  **336 runs (design P 224, design G 112), 0 failed, no cell dropped** (design G at n = 1600 was kept; one sweep takes
  about 5 min on 8 single-thread workers; the sweep was run three times because columns were added — the numbers are
  those of the last, complete run; seeds are deterministic).

## 1. Quantities and how to read the tables

* κ = nθ²/(σ² log n). **λ_n/log n** = (n − 1)φ₀²θ²_min/(σ² log n) with φ₀² := the **realised** λ_min of the correlation
  matrix of the columns of Q (P: 0.64–0.82; G: 0.24 at n = 400, 0.39 at n = 1600), not the φ₀² = ½ of STATEMENT §5.
* **vis (U\*)** = δ²_{U*,j}/log n for the swept truth j (P: j = 1; G: j = 2; μ includes both truths), with
  U\* = S̃₀ ∩ block(j) ∖ {j} the block-mates in the start mode; **vis (block min)** = the minimum of δ²_{U,j}/log n over **all**
  U ⊆ block(j) ∖ {j} (the (V_b♭) quantity; median over seeds and, in brackets for G, the minimum over seeds; for P the
  value is the same for every seed and the minimum is shown). Median over seeds for U\*.
* **S₀ ⊆ S̃₀** truth inclusion in the coded start mode; **S̃₀ ⊆ Q** (here always true in all 336 runs; no outside column
  entered the start mode); the sandwich is the conjunction.
* **Truth removal.** *At T = S₀:* F(S₀) − max over truth-removing neighbours A of S₀ (deleting a truth, or swapping a
  truth for another column) of F(A); "> 0" means TL holds at the base set of the lattice (path independent, every run).
  *At visited sets:* the same margin at every centre T ⊇ S₀ visited by LS0; this is **conditional on LS0 visiting such a
  centre**, so it is undefined when S̃₀ lacks a truth and LS0 never adds it (stated as "no visited T ⊇ S₀"); "k of d" =
  k of the d runs that visited one have a positive minimum margin.
* **NA at lattice centres** = no addition improving F (and the two swap/deletion path margins of the parent SPEC) at every
  visited centre inside the lattice [S₀, Q]; "visited / ok" = runs that visited at least one lattice centre / runs with
  all those margins < 0. Where no lattice centre is visited, the check is vacuous and is shown by the first count.
  Separately, F(S₀ ∪ {l}) − F(S₀) < 0 for every l ∉ S₀ in all 336 runs (largest value −1.73).
* **LS0 ends at S₀ (cert.)** = LS0 from the start mode ends at S₀ **and** the last scan found no strict improvement.
  Every run was certified (cap ℓ_n + |S̃₀| never reached in 336 runs), so "fails" below always means "certified at a set
  ≠ S₀".
* **Mode margin ≥ 3** (design P, n = 400 only): F(S₀) − max over **all** S ≠ S₀ with |S| ≤ 3 (empty set, all singletons,
  pairs and triples of [p], exhaustive, exact scores): ">0 / median / min". A proxy of the mode event 𝓜_n only (models of
  size ≥ 4 are not scanned).
* **non-deletion moves** (design G) = total number of LS0 moves that are not deletions of an extra, over the seeds.

## 2. Design P (one truth, ⌊n^b⌋ − 1 weak proxies, exact Gram)

**Design P, n = 400, b = 0.3 (p = 133, q = 6, r² = log n/n = 0.0150)**

| κ | λ_n/log n | vis (U*) | vis (block min) | start size | S0⊆S̃0 | S̃0⊆Q | F(S0)−best truth-removal nbr > 0 (at T=S0) | visited T⊇S0: runs with TL>0 of runs with such a T; min margin | NA at lattice centres (visited / ok) | LS0 ends at S0 (cert.) | mode margin ≥3: >0 / median / min |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 0.38 | 0.50 | 0.46 | 0 | 0/10 | 10/10 | 0/10 | no visited T⊇S0 | 0/10 / 10/10 | 0/10 | 0/10 / -7.39 / -8.48 |
| 1 | 0.75 | 1.00 | 0.93 | 0 | 0/10 | 10/10 | 0/10 | no visited T⊇S0 | 0/10 / 10/10 | 0/10 | 0/10 / -6.10 / -7.93 |
| 2 | 1.51 | 1.99 | 1.85 | 0 | 1/10 | 10/10 | 1/10 | 1 of 1 defined; min 2.15 | 1/10 / 10/10 | 1/10 | 1/10 / -3.45 / -6.34 |
| 4 | 3.01 | 3.99 | 3.71 | 1 | 9/10 | 10/10 | 9/10 | 9 of 9 defined; min 0.37 | 9/10 / 10/10 | 9/10 | 9/10 / 1.93 / -2.51 |
| 8 | 6.02 | 7.98 | 7.42 | 1 | 10/10 | 10/10 | 10/10 | 10 of 10 defined; min 5.87 | 10/10 / 10/10 | 10/10 | 10/10 / 3.75 / 1.76 |
| 16 | 12.04 | 15.96 | 14.83 | 1 | 10/10 | 10/10 | 10/10 | 10 of 10 defined; min 22.85 | 10/10 / 10/10 | 10/10 | 10/10 / 3.75 / 1.76 |
| 32 | 24.09 | 31.92 | 29.66 | 1 | 10/10 | 10/10 | 10/10 | 10 of 10 defined; min 54.46 | 10/10 / 10/10 | 10/10 | 10/10 / 3.76 / 1.76 |

**Design P, n = 400, b = 0.45 (p = 133, q = 14, r² = log n/n = 0.0150)**

| κ | λ_n/log n | vis (U*) | vis (block min) | start size | S0⊆S̃0 | S̃0⊆Q | F(S0)−best truth-removal nbr > 0 (at T=S0) | visited T⊇S0: runs with TL>0 of runs with such a T; min margin | NA at lattice centres (visited / ok) | LS0 ends at S0 (cert.) | mode margin ≥3: >0 / median / min |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 0.32 | 0.50 | 0.43 | 0 | 0/10 | 10/10 | 0/10 | no visited T⊇S0 | 0/10 / 10/10 | 0/10 | 0/10 / -7.39 / -8.48 |
| 1 | 0.64 | 1.00 | 0.87 | 0 | 0/10 | 10/10 | 0/10 | no visited T⊇S0 | 0/10 / 10/10 | 0/10 | 0/10 / -6.10 / -7.93 |
| 2 | 1.28 | 1.99 | 1.73 | 0 | 1/10 | 10/10 | 1/10 | 1 of 1 defined; min 2.15 | 1/10 / 10/10 | 1/10 | 1/10 / -3.45 / -6.34 |
| 4 | 2.55 | 3.99 | 3.46 | 1 | 9/10 | 10/10 | 9/10 | 9 of 9 defined; min 0.37 | 9/10 / 10/10 | 9/10 | 9/10 / 1.93 / -2.51 |
| 8 | 5.10 | 7.98 | 6.93 | 1 | 10/10 | 10/10 | 10/10 | 10 of 10 defined; min 5.87 | 10/10 / 10/10 | 10/10 | 10/10 / 3.75 / 1.76 |
| 16 | 10.21 | 15.96 | 13.85 | 1 | 10/10 | 10/10 | 10/10 | 10 of 10 defined; min 22.85 | 10/10 / 10/10 | 10/10 | 10/10 / 3.75 / 1.76 |
| 32 | 20.41 | 31.92 | 27.71 | 1 | 10/10 | 10/10 | 10/10 | 10 of 10 defined; min 54.46 | 10/10 / 10/10 | 10/10 | 10/10 / 3.76 / 1.76 |

**Design P, n = 1600, b = 0.3 (p = 533, q = 9, r² = log n/n = 0.0046)**

| κ | λ_n/log n | vis (U*) | vis (block min) | start size | S0⊆S̃0 | S̃0⊆Q | F(S0)−best truth-removal nbr > 0 (at T=S0) | visited T⊇S0: runs with TL>0 of runs with such a T; min margin | NA at lattice centres (visited / ok) | LS0 ends at S0 (cert.) | mode margin ≥3: >0 / median / min |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 0.41 | 0.50 | 0.48 | 0 | 0/6 | 6/6 | 0/6 | no visited T⊇S0 | 0/6 / 6/6 | 0/6 | – |
| 1 | 0.82 | 1.00 | 0.96 | 0 | 0/6 | 6/6 | 0/6 | no visited T⊇S0 | 0/6 / 6/6 | 0/6 | – |
| 2 | 1.65 | 2.00 | 1.93 | 0 | 0/6 | 6/6 | 0/6 | no visited T⊇S0 | 0/6 / 6/6 | 0/6 | – |
| 4 | 3.29 | 4.00 | 3.85 | 1 | 6/6 | 6/6 | 6/6 | 6 of 6 defined; min 4.96 | 6/6 / 6/6 | 6/6 | – |
| 8 | 6.58 | 8.00 | 7.71 | 1 | 6/6 | 6/6 | 6/6 | 6 of 6 defined; min 20.25 | 6/6 / 6/6 | 6/6 | – |
| 16 | 13.17 | 15.99 | 15.42 | 1 | 6/6 | 6/6 | 6/6 | 6 of 6 defined; min 48.94 | 6/6 / 6/6 | 6/6 | – |
| 32 | 26.33 | 31.98 | 30.84 | 1 | 6/6 | 6/6 | 6/6 | 6 of 6 defined; min 102.92 | 6/6 / 6/6 | 6/6 | – |

**Design P, n = 1600, b = 0.45 (p = 533, q = 27, r² = log n/n = 0.0046)**

| κ | λ_n/log n | vis (U*) | vis (block min) | start size | S0⊆S̃0 | S̃0⊆Q | F(S0)−best truth-removal nbr > 0 (at T=S0) | visited T⊇S0: runs with TL>0 of runs with such a T; min margin | NA at lattice centres (visited / ok) | LS0 ends at S0 (cert.) | mode margin ≥3: >0 / median / min |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 0.35 | 0.50 | 0.47 | 0 | 0/6 | 6/6 | 0/6 | no visited T⊇S0 | 0/6 / 6/6 | 0/6 | – |
| 1 | 0.71 | 1.00 | 0.93 | 0 | 0/6 | 6/6 | 0/6 | no visited T⊇S0 | 0/6 / 6/6 | 0/6 | – |
| 2 | 1.41 | 2.00 | 1.87 | 0 | 0/6 | 6/6 | 0/6 | no visited T⊇S0 | 0/6 / 6/6 | 0/6 | – |
| 4 | 2.82 | 4.00 | 3.74 | 1 | 6/6 | 6/6 | 6/6 | 6 of 6 defined; min 4.96 | 6/6 / 6/6 | 6/6 | – |
| 8 | 5.65 | 8.00 | 7.48 | 1 | 6/6 | 6/6 | 6/6 | 6 of 6 defined; min 20.25 | 6/6 / 6/6 | 6/6 | – |
| 16 | 11.30 | 15.99 | 14.95 | 1 | 6/6 | 6/6 | 6/6 | 6 of 6 defined; min 48.94 | 6/6 / 6/6 | 6/6 | – |
| 32 | 22.60 | 31.98 | 29.90 | 1 | 6/6 | 6/6 | 6/6 | 6 of 6 defined; min 102.92 | 6/6 / 6/6 | 6/6 | – |

For κ ≥ 8 the mode margin no longer grows with κ (median 3.75): it equals −(F(S₀ ∪ {l}) − F(S₀)) maximised over l, exactly
the best addition margin (checked: sum = 0 to rounding in all κ ≥ 8 runs), i.e. the binding competitor is "S₀ plus one
noise column"; below κ = 4 the binding competitor is the empty set.

### d_n for design P (illustration of d_n = O(1), STATEMENT §5(a))

d_n = E max over the truth-removal directions u_{A,1} (A any subset of the q − 1 proxies, any l): for design P the
directions are u_A′g = (ρ g₁ − r Σ_{j∈A} g_j)/√(ρ² + |A| r²), ρ = √(1 − r²) (derivation in `dn_P.R`); the maximum over
**all** subsets A of each size is attained by the largest/smallest g_j, so the Monte Carlo maximum is exact over the whole
family 𝒟ᵀ_n (not just the start mode's lattice). Both the Monte Carlo value and the closed-form bound are reported.

| n | b | q | r | d_n (Monte Carlo, 2000 draws) ± s.e. | √(2/π) (t = 0 direction) | closed-form bound of §5(a) | d_n²/log n |
|---|---|---|---|---|---|---|---|
| 400 | 0.3 | 6 | 0.1224 | 1.0412 ± 0.0141 | 0.7979 | 1.2959 | 0.1809 |
| 400 | 0.45 | 14 | 0.1224 | 1.4059 ± 0.0139 | 0.7979 | 2.083 | 0.3299 |
| 1600 | 0.3 | 9 | 0.0679 | 0.9704 ± 0.013 | 0.7979 | 1.2342 | 0.1276 |
| 1600 | 0.45 | 27 | 0.0679 | 1.4792 ± 0.0132 | 0.7979 | 2.2117 | 0.2966 |

The Monte Carlo d_n is below the closed-form bound in the four cells, increases with q (≈ 1.0 at q = 6–9, ≈ 1.4–1.5 at
q = 14–27) and is of order 1 here; d_n²/log n lies in 0.13–0.33.

## 3. Design G (two truths, weak truth 2 swept, ⌈n^0.375⌉ proxies of truth 1)

**Design G, n = 400, b = 0.375 (p = 800, |Q| = 12)**

| κ | λ_n/log n | vis wk (U*) | vis wk (block min: median [min]) | start size | S0⊆S̃0 (truth 2 in start) | S̃0⊆Q | F(S0)−best truth-removal nbr > 0 (at T=S0) | visited T⊇S0: runs with TL>0 of runs with such a T; min margin | NA at lattice centres (visited / ok) | LS0 ends at S0 (cert.) | non-deletion moves |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 0.12 | 1.16 | 0.41 [0.00] | 2.0 | 0/10 | 10/10 | 0/10 | no visited T⊇S0 | 0/10 / 10/10 | 0/10 | 0 |
| 1 | 0.24 | 1.49 | 0.80 [0.00] | 2.0 | 0/10 | 10/10 | 0/10 | no visited T⊇S0 | 0/10 / 10/10 | 0/10 | 0 |
| 2 | 0.48 | 2.65 | 1.68 [0.00] | 2.0 | 0/10 | 10/10 | 2/10 | 2 of 2 defined; min 1.26 | 2/10 / 10/10 | 2/10 | 2 |
| 4 | 0.96 | 4.87 | 3.48 [0.00] | 2.0 | 0/10 | 10/10 | 5/10 | 5 of 5 defined; min 0.95 | 5/10 / 10/10 | 5/10 | 5 |
| 8 | 1.91 | 9.18 | 7.16 [0.63] | 2.0 | 0/10 | 10/10 | 10/10 | 10 of 10 defined; min 0.66 | 10/10 / 10/10 | 10/10 | 10 |
| 16 | 3.82 | 17.61 | 14.62 [3.70] | 2.0 | 0/10 | 10/10 | 10/10 | 10 of 10 defined; min 15.73 | 10/10 / 10/10 | 10/10 | 10 |
| 32 | 7.64 | 34.22 | 29.69 [12.38] | 2.5 | 5/10 | 10/10 | 10/10 | 10 of 10 defined; min 44.64 | 10/10 / 10/10 | 10/10 | 5 |

**Design G, n = 1600, b = 0.375 (p = 3200, |Q| = 18)**

| κ | λ_n/log n | vis wk (U*) | vis wk (block min: median [min]) | start size | S0⊆S̃0 (truth 2 in start) | S̃0⊆Q | F(S0)−best truth-removal nbr > 0 (at T=S0) | visited T⊇S0: runs with TL>0 of runs with such a T; min margin | NA at lattice centres (visited / ok) | LS0 ends at S0 (cert.) | non-deletion moves |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 0.19 | 0.25 | 0.09 [0.03] | 13 | 0/6 | 6/6 | 0/6 | no visited T⊇S0 | 0/6 / 6/6 | 0/6 | 0 |
| 1 | 0.39 | 0.63 | 0.35 [0.00] | 13 | 0/6 | 6/6 | 0/6 | 0 of 1 defined; min -0.33 | 1/6 / 6/6 | 0/6 | 2 |
| 2 | 0.78 | 1.19 | 0.84 [0.04] | 13 | 0/6 | 6/6 | 2/6 | 2 of 3 defined; min -0.18 | 3/6 / 6/6 | 2/6 | 4 |
| 4 | 1.56 | 2.74 | 2.25 [0.07] | 13 | 0/6 | 6/6 | 6/6 | 6 of 6 defined; min 3.08 | 6/6 / 6/6 | 6/6 | 6 |
| 8 | 3.11 | 6.16 | 5.40 [0.00] | 13 | 0/6 | 6/6 | 6/6 | 6 of 6 defined; min 17.75 | 6/6 / 6/6 | 6/6 | 6 |
| 16 | 6.22 | 13.35 | 12.18 [1.22] | 13 | 0/6 | 6/6 | 6/6 | 6 of 6 defined; min 46.33 | 6/6 / 6/6 | 6/6 | 6 |
| 32 | 12.45 | 28.19 | 26.40 [7.57] | 14 | 5/6 | 6/6 | 6/6 | 6 of 6 defined; min 100.33 | 6/6 / 6/6 | 6/6 | 1 |


## 4. Reading (plain language; finite-n observations only)

**Design P.** The three events — truth inclusion S₀ ⊆ S̃₀, truth removal not beating the truth (the empty set is the binding
truth-removing competitor in these runs [R1-sol-3], so the margin at T = S₀ equals F(S₀) − F(∅)), and LS0 ending at S₀ — coincide run by run in all 224
P runs. At n = 400 they hold in all 10 seeds from κ = 8, in 9/10 at κ = 4 (the failing seed has F(∅) > F(S₀) by 2.5 and
the start mode is empty), in 1/10 at κ = 2 and in 0/10 at κ ≤ 1. At n = 1600 they hold in all 6 seeds from κ = 4 and in
0/6 at κ ≤ 2 (κ = 3 was not run). The mode-margin proxy over |S| ≤ 3 follows the same pattern (positive in 9/10 at κ = 4,
10/10 at κ ≥ 8, median −3.5 at κ = 2). The numbers for b = 0.3 and b = 0.45 are identical: the proxies never entered the
start mode or the path (start mode = {1} or ∅), so q played no role at these signal levels, and the failure is the plain
"signal below the detection level" failure (the empty set beats the truth), not a lattice effect. The realised visibility
δ²/log n is within about 15 % of κ (U\*: 0.99 κ; block minimum 0.86–0.97 κ), so on this design κ is also the visibility
level; the cells that fail have visibility ≲ 2 (n = 1600) or ≲ 4 (n = 400, 9/10 at 4), and the failing level is lower at
the larger n (κ between 2 and 4 at n = 1600, between 4 and 8 at n = 400). NA at visited lattice centres never failed
(all margins < 0 whenever a lattice centre was visited).

**Design G.** The coded start mode contains truth 1 in every run and some of its proxies (median start size 2 at n = 400, 13 at n = 1600), but **not truth 2
for κ ≤ 16 in any run** (S₀ ⊆ S̃₀: 0/10 and 0/6), and in only 5/10 (n = 400) and 5/6 (n = 1600) runs at κ = 32 (the largest
level run; the start-mode entry level of order log n + 2 log p is not reached by nθ₂² before κ ≈ 32; κ > 32 was not run).
Nevertheless LS0 recovers S₀ from a start mode that lacks truth 2: it ends at S₀ in 10/10 seeds from κ = 8 at n = 400
(5/10 at κ = 4, 2/10 at κ = 2, 0/10 at κ ≤ 1) and in 6/6 seeds from κ = 4 at n = 1600 (2/6 at κ = 2, 0/6 at κ ≤ 1). Over
all 336 runs, "LS0 ends at S₀" ⇔ "F(S₀) beats every truth-removing neighbour of S₀" holds run by run (no exception:
112 G and 224 P runs), so in these cells the endpoint fails exactly when truth removal fails at the base set. In the 49 failing G runs
the path ends at a single column with one truth missing (final size 1, `final_miss` = 1, no extras): truth 2 was never entered or was
removed again; no failing run ended with extras (`end_extra` = 0 in all 336 runs). Visited-set TL
was positive in every run that visited a centre ⊇ S₀ except two runs at n = 1600 (κ = 1: −0.33; κ = 2: −0.18), where LS0
reached a set ⊇ S₀ (swap of an extra for the missing truth) and then deleted a truth. The block-wise visibility of truth 2 over all subsets U of its block can be ≈ 0 for
single seeds (minimum over seeds 0.00 at κ ≤ 4 at n = 400, and also 0.00 at κ = 8 at n = 1600), while LS0 still ends at S₀ in
all seeds at κ = 8 (n = 1600) and 10/10 at κ = 8 (n = 400): in these cells a vanishing block-minimum visibility (a cancellation
between the two truths inside U) is not accompanied by an endpoint failure, i.e. the (V_b♭) minimum over all U is not
necessary for the endpoint here; the median block visibility, which is of order κ, tracks it better. NA at visited lattice centres never failed.

**Where each event starts to fail (κ grid {0.5, 1, 2, 4, 8, 16, 32}; "all seeds OK from" = smallest grid κ with every seed OK and
all larger grid values also OK; "fails at" = largest grid κ at which some seed fails):**

| design, n | truth inclusion S₀ ⊆ S̃₀ | truth removal at T = S₀ (F(S₀) > every truth-removing neighbour) | LS0 endpoint = S₀ (certified) |
|---|---|---|---|
| P, n = 400 (b = 0.3 and 0.45 identical) | all seeds OK from κ = 8; fails at κ ≤ 4 (9/10 at 4) | all OK from κ = 8; fails at κ ≤ 4 | all OK from κ = 8; fails at κ ≤ 4 |
| P, n = 1600 (b = 0.3 and 0.45) | all OK from κ = 4; fails at κ ≤ 2 | all OK from κ = 4; fails at κ ≤ 2 | all OK from κ = 4; fails at κ ≤ 2 |
| G, n = 400 (b = 0.375) | not reached in range: 0/10 up to κ = 16, 5/10 at κ = 32 | all OK from κ = 8; fails at κ ≤ 4 (5/10 at 4) | all OK from κ = 8; fails at κ ≤ 4 (5/10 at 4) |
| G, n = 1600 (b = 0.375) | not reached in range: 0/6 up to κ = 16, 5/6 at κ = 32 | all OK from κ = 4; fails at κ ≤ 2 (2/6 at 2) | all OK from κ = 4; fails at κ ≤ 2 (2/6 at 2) |

Visited-set truth removal (conditional on LS0 reaching a set ⊇ S₀) was violated only in design G at n = 1600, κ ≤ 2 (two runs).
The grid is coarse (factor 2): "from κ = 8" means between the grid points 4 and 8 for the first column of P at n = 400, etc.

No design or n is reliable at κ = 0.5 or 1; the endpoint and TL at S₀ are reliable in every design from κ = 8 at n = 400
and from κ = 4 at n = 1600.

## 5. Limits of these observations

* Only 6–10 seeds per cell and a coarse κ grid (factor 2); "fails below κ" is a statement about these cells, not a threshold.
* One fixed design per n for P, one construction for G; |S| ≤ 3 only for the mode margin; the sampler is not run, so the
  posterior conclusion [POST] is not probed. The truth-removal statistic at visited sets depends on the path and is undefined
  when LS0 never reaches a set containing S₀ (it is not "satisfied" there); the path-independent statistic at T = S₀ is
  the one to compare across cells.
* These are finite-n observations of the validated LS0 re-implementation, **not evidence about asymptotic necessity**; the
  levels run (κ ≤ 32) are well below the sufficient constants of STATEMENT §2, which are proof artefacts, and the sweep neither
  confirms nor refutes that any threshold of order log n/n is needed in the limit.

## Files

`SPEC.md`, `rm2r_common.R`, `validate.R` / `validate_out.txt`, `run_all.R` (worker driver), `dn_P.R` / `dn_P.csv`,
`summarise.R` → `summary.csv` (cell summaries; wide), `make_tables.R` (the tables above), `arrays/` (git-ignored: per-run
rows, `results_raw.csv`, worker logs).
