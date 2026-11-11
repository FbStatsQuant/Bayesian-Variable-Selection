# W3-START — sharpness-gate numerics: RESULTS (2026-11-11)

**Observations, not proofs; every theorem is asymptotic.** Production core (`Scripts/SMC_BVS/core`, compiled locally
with Rcpp; no NOTS): π₀(S₀) is read from the coded start (`cpp_start_logmass`), the block tables from `cpp_setup`, and
the lattice mass in `ar1` from 20000 draws of the coded sampler. Files: `start_common.R` (helpers, designs),
`run_start.R` (driver; `Rscript run_start.R results_raw.csv 7`), `summarise.R`, `results_raw.csv` (1018 runs, none
failed), `summary.csv` (one row per cell, all columns). p = 2n throughout (A_n := log p/log n ≈ 1.09–1.13, so
1 + 2A_n ≈ 3.2); σ = 1; 10 seeds per cell for n ≤ 800, 6 seeds at n = 1600 (a reduced layer of 12 cells); `ar1`: 8 seeds.
All entries below are medians over seeds unless stated.

Quantities (STATEMENT §2): o₀ start odds against S₀; T₁ sum of single-null block Bayes factors (from the tables);
f_n the floor of (T0); U = p⁻¹Σ m_l; e_n the truth-deletion functional of v1.0/T22; Ξ the truth-block functional
(reported: Σ_b Ξ_b); pred := ((s₀ + 1)p/(2p − 1 − s₀))·n^{−1/2}·𝔏^{b,0}_n — the scale the theorem assigns to T₁, computed
from (X, θ*) only; c_null := max over nulls of δ²/(τ² log n) at U*_b (realised leakage level); c_truth := min over truths
of δ²/(τ² log n) at U*_b ∖ {j}; c_vis,all := min over truths and **all** U in the block (the (V-c) quantity; seeds 1–2).

## 1. Deterministic claims (all 1018 runs)
| check | result |
|---|---|
| (T0)/(FLOOR): T₁ ≥ f_n(s₀) | holds in every run; min T₁/f_n = 1.10 |
| (AGG-b): o₀ ≥ T₁ | holds in every run; min o₀/T₁ = 1.03 |
| (AGG-b): T₁ ≤ (s₀ + 1)U | 0 violations |
| (AGG-b) upper bound o₀ ≤ T₁ + R₂ + [∏(1 + Ξ_b) − 1](1 − U)^{−(16s₀+1)} (runs with U < 1: 629) | 0 violations; max o₀/bound = 0.90 |
| (AGG-b) lower bound o₀ ≥ c_sΞ | 0 violations (very slack constant) |

## 2. Inside the assumptions
| design | n | π₀(S₀) | o₀·√n | o₀/T₁ | T₁/pred |
|---|---|---|---|---|---|
| `base_orth` (fixed design, nulls ⊥ truths: zero leakage, strong signals; F2 with η′ = 0), s₀ = 3 | 100 / 200 / 400 / 800 / 1600 | 0.79 / 0.85 / 0.89 / 0.92 / 0.94 | 2.62 / 2.56 / 2.51 / 2.45 / 2.39 | 1.16 / 1.11 / 1.08 / 1.05 / 1.04 | 0.97 / 0.93 / 0.98 / 1.00 / 0.99 |
| `leakall` η = 0 (structured fixed design: each truth has B − 1 correlates at 0.9; zero leakage), s₀ = 2 | 200 / 400 / 800 / 1600 | 0.82 / 0.91 / 0.94 / 0.96 | 3.21 / 2.00 / 1.92 / 1.89 | 1.75 / 1.07 / 1.04 / 1.03 | 1.00 / 1.00 / 0.99 / 1.00 |
| `base_iid` (Gaussian rows, independent columns; (T3)(b) with C_L = 0), s₀ = 3 | 100 / 200 / 400 / 800 / 1600 | 0.40 / 0.65 / 0.73 / 0.81 / 0.87 | 14.8 / 7.8 / 7.3 / 6.6 / 6.1 | 2.34 / 1.31 / 1.21 / 1.14 / 1.09 | 0.99 / 0.84 / 0.80 / 0.72 / 0.85 |

Readings. (i) **Exact order n^{−1/2}** in the fixed zero-leakage designs: o₀√n is flat (slope of log o₀ on log n:
−0.53) and sits just above the floor (T₁/f_n ≈ 1.13–1.2). (ii) **First-order form**: o₀/T₁ → 1 in all three designs.
(iii) The leakage functional predicts T₁ within a few per cent in the fixed designs (T₁/pred ≈ 1), and within its
truncation slack for Gaussian rows. (iv) For independent Gaussian columns the realised sample leakage level is
c_null ≈ 1.3–1.6, far above η_A ≈ 0.09: a uniform bound δ² ≤ ητ² log n with η < η_A fails on every data set, the
averaged condition holds, and π₀(S₀) → 1.

## 3. Boundary violations
**(a) Visibility, `vis`** (independent Gaussian columns, s₀ = 1, the truth's gain set to δ² = c·τ² log n).
| c | π₀(S₀) at n = 200 / 400 / 800 / 1600 | Ξ at n = 200 / 400 / 800 / 1600 |
|---|---|---|
| 1 | 5·10⁻⁴ / 4·10⁻⁴ / 6·10⁻⁴ / — | 2·10³ / 2·10³ / 1·10³ / — |
| 2 | 0.005 / 0.008 / 0.024 / 0.026 | 167 / 118 / 34 / 35 |
| 3 | 0.07 / 0.14 / 0.41 / — | 11 / 5.7 / 0.9 / — |
| 4.5 | 0.69 / 0.79 / 0.82 / 0.88 | 0.15 / 0.05 / 0.004 / 0.002 |
| 6 | 0.81 / 0.83 / 0.88 / — | 2·10⁻³ / 4·10⁻⁴ / 2·10⁻⁵ / — |
| 9 | 0.83 / 0.85 / 0.89 / — | 6·10⁻⁸ / 2·10⁻⁸ / 4·10⁻¹⁰ / — |
Reading: the start mass is lost below c ≈ 3 and present above c ≈ 4.5; the predicted threshold is 1 + 2A_n ≈ 3.2
((N3) and (V-c)/(V-m)). Above the threshold Ξ decays polynomially and o₀ is driven by T₁ (o₀/T₁ → 1.1). **NECESSARY at
the constant 1 + 2A** (consistent with the claim; seed-to-seed spread is large below the threshold).

**(b) (V-c) over all 15-sets versus Ξ, `leakall` η = 0 and `leak1`** (each truth has B − 1 correlates at 0.9).
| n | c_vis,all (min over all U) | e_n | Ξ | π₀(S₀) |
|---|---|---|---|---|
| 200 / 400 / 800 / 1600 | 0.31 / 0.42 / 0.89 / 1.64 | 1·10⁴ / 3·10⁴ / 3·10⁴ / 7·10³ | 0.16 / 2·10⁻³ / 3·10⁻⁷ / 3·10⁻¹³ | 0.82 / 0.91 / 0.94 / 0.96 |
Reading: (V-c) fails (level < 3.2 given the 15 correlates) and v1.0's functional e_n is of order 10⁴, yet Ξ → 0 fast
and the conclusion holds with the exact order. **(V-c) is IMPROVABLE**; the truth-block functional Ξ and the margin
form (V-m) (which this design is expected to satisfy — not computed here: a deletion that keeps 15 correlates is paid
for by 15 prior-plus-dimension prices) are the right objects. This is the finding behind amendment [G1] of v1.1.

**(c) One leaking null, `leak1`** (same structured design; one null gets δ² = c·τ² log n at U = ∅; its block has no truth).
| c | π₀(S₀) at n = 200 / 400 / 800 | o₀ at n = 200 / 400 / 800 | T₁/pred |
|---|---|---|---|
| 1 | 0.80 / 0.91 / 0.94 | 0.26 / 0.10 / 0.07 | 0.92 / 0.93 / 0.93 |
| 2 | 0.68 / 0.87 / 0.90 | 0.48 / 0.15 / 0.11 | 0.17 / 0.13 / 0.10 |
| 3 | 0.34 / 0.45 / 0.39 | 1.9 / 1.2 / 1.6 | 0.014 / 0.012 / 0.009 |
| 4.5 | 0.014 / 0.007 / 0.004 | 70 / 137 / 283 | 0.002 / 0.002 / 0.001 |
| 6 | 2·10⁻⁴ / 5·10⁻⁵ / 2·10⁻⁵ | 5·10³ / 2·10⁴ / 6·10⁴ | 3·10⁻⁴ / 3·10⁻⁴ / 1·10⁻⁴ |
Reading: one null kills the start mass above c ≈ 3.2 = 1 + 2A_n and is harmless below — (N2) is sharp. A uniform
leakage bound with η < η_A ≈ 0.09 is **not necessary** (c = 1, 2 are fine). The averaged functional is **conservative
for an isolated leaking null**: pred, which integrates that null's noise up to the uniform truncation z_n, exceeds
the realised T₁ by a factor 10–10³ at c ≥ 2, so (AL) with Q = S₀ would reject c ∈ (≈1.3, 3.2) although the conclusion
holds there. Flag: `improvable` — isolated strong leakers should be handled through Q (the lattice form) with the
individual threshold 1 + 2A (candidate Corollary F4, see CHECKPOINT_1).

**(d) All nulls leaking, `leakall`** (same design; every free null gets δ² = η·τ² log n; here τ²/Δ = 1.5).
| η | o₀ at n = 200 / 400 / 800 / 1600 | slope of log o₀ on log n | predicted exponent −(1 − 1.5η)/2 | T₁/pred |
|---|---|---|---|---|
| 0 | 0.23 / 0.10 / 0.068 / 0.047 | −0.73 | −0.50 | 1.00 |
| 0.1 | 0.29 / 0.16 / 0.11 / — | −0.68 | −0.43 | 0.99 |
| 0.2 | 0.41 / 0.25 / 0.20 / — | −0.53 | −0.35 | 0.99 |
| 0.4 | 1.03 / 0.77 / 0.67 / 0.54 | −0.30 | −0.20 | 0.97–0.99 |
| 0.6 | 3.8 / 3.8 / 4.2 / — | +0.07 | −0.05 | 0.93–0.99 |
| 0.8 | 66 / 362 / 8·10³ / 4·10⁴ | +3.2 | +0.10 (single additions only) | 0.90–0.98 |
| 1.0 | 2·10⁶ / 3·10¹⁴ / 2·10³⁹ / — | +55 | +0.25 (single additions only) | 0.87–0.98 |
Reading: the transition is near η = 2/3, where the leakage functional predicts it (J1: 𝔏 ≍ n^{ητ²/(2Δ)}, so n^{−1/2}𝔏 → 0
iff η < Δ/τ² = 2/3), **not** at η_A ≈ 0.09: the uniform (L-gain) condition with η < η_A is sufficient but far from
necessary when the unexplained signal is strong; (AL) tracks the truth (T₁/pred ≈ 1 for every η). Past the threshold
U > 1 and the mass moves to very large models (the multi-addition terms of Lemma AGG), which is why the divergence is
much faster than the single-addition exponent. The fitted slopes for η ≤ 0.4 are steeper than the asymptotic exponent
because of the second-order terms at n = 200.

**(e) Eigenvalue floor, `twin`** (independent Gaussian columns; every second null is a near-twin of another null,
correlation ≈ 1 − 1/n, so λ_min of those pairs ≈ 1/n: (FL-16) fails).
o₀√n at n = 200 / 400 / 800 / 1600: 6.9 / 7.0 / 6.8 / 7.4 (`base_iid`: 7.8 / 7.3 / 6.6 / 6.1); π₀(S₀): 0.67 / 0.74 / 0.81 / 0.84.
Reading: the conclusion survives with a slightly larger constant. **(FL-16) is IMPROVABLE among null columns.**

**(f) Energy bound, `energy`** (θ = n^{1/4}(1, −1, 1): ‖μ‖²/n unbounded). o₀√n at n = 200 / 400 / 800: 7.6 / 6.5 / 7.6;
T₁/pred ≈ 1.0. Reading: the conclusion survives. **‖μ‖² ≤ Mn is IMPROVABLE** (a constant of the toolkit).

**(g) Number of truths, `s0grow`** (independent Gaussian columns, θ_j = ±1).
| s₀ | π₀(S₀) at n = 200 / 800 | o₀√n/(s₀ + 1) at n = 200 / 800 | c_truth at n = 200 / 800 |
|---|---|---|---|
| 1 | 0.82 / 0.91 | 1.6 / 1.4 | 18.8 / 59.8 |
| 4 | 0.67 / 0.75 | 1.4 / 1.9 | 6.7 / 22.1 |
| 16 | 2·10⁻¹⁴ / 0.40 | — / 2.5 | 0.65 / 3.98 |
| 32 | 2·10⁻⁴⁶ / 4·10⁻⁶ | — | 0.03 / 1.24 |
Reading: the (s₀ + 1) scaling of the bound is visible for s₀ ≤ 4. For s₀ = 16, 32 the mass is lost at these n, and the
reason is **visibility**, not the bookkeeping in s₀: with many truths the unexplained energy τ² ≈ σ² + ‖θ‖² is large and
the level θ_j²n/(τ² log n) falls below 1 + 2A (c_truth 0.03–1.2); at s₀ = 16, n = 800 it has just crossed (3.98) and
π₀(S₀) = 0.40. The τ²-normalisation of (V-c)/(V-m) is what the data show: the start needs
θ_j²·n ≳ (1 + 2A)(σ² + unexplained signal)·log n.

**(h) Population leakage for Gaussian rows, `gleak`** (every null has population correlation ρ with truth 1; s₀ = 2).
| ρ | π₀(S₀) at n = 200 / 400 / 800 / 1600 | o₀√n | U |
|---|---|---|---|
| 1/√n (inside (L-gain-R), C_L = 1) | 0.42 / 0.58 / 0.71 / — | 19 / 14 / 12 / — | 1.7 / 0.9 / 0.44 / — |
| 2/√n (inside, C_L = 2) | 0.015 / 0.035 / 0.16 / 0.08 | 997 / 604 / 159 / 817 | 5.1 / 6.4 / 2.6 / 3.4 |
| 4/√n (inside, C_L = 4) | 5·10⁻³⁷ / 1·10⁻⁶¹ / 1·10⁻¹¹² / — | — | 988 / 515 / 271 / — |
| √(0.25 log n/n) (outside) | 0.35 / 0.46 / 0.60 / — | 26 / 24 / 19 / — | 1.6 / 1.2 / 0.68 / — |
| √(0.5 log n/n) (outside) | 0.12 / 0.14 / 0.28 / — | 103 / 126 / 76 / — | 3.7 / 2.9 / 1.6 / — |
| √(1.0 log n/n) (outside) | 1·10⁻⁴ / 2·10⁻⁴ / 1·10⁻⁴ / — | — | 16 / 13 / 8.5 / — |
Reading: for C_L = 1 the mass converges. For C_L = 2 and 4 the functional U decreases with n (as the theorem's
n^{−1/2}e^{C_R√log n} says it must) but is still above 1 at these sizes, and while U > 1 the start mass sits on very
large models (one leaking null per block): the constant C_R, which grows with C_L·θ/√Δ, decides where the asymptotic
regime starts. Just outside the assumption (ρ² = η log n/n) the picture is graded in η, not a cliff at C_L n^{−1/2}:
η = 0.25 behaves like C_L = 1. **The scale C_L n^{−1/2} of (L-gain-R) is not a threshold**; the natural statement
has a population leakage level η with an explicit exponent (candidate extension, see CHECKPOINT_1).

**(i) Lattice form, `ar1`** (Gaussian AR(1) rows, ρ = 0.5, s₀ = 2 separated truths; Q = neighbourhoods of radius
d_n = ⌈log n/(2 log 2)⌉). π₀(S₀) at n = 200 / 400 / 800: 0.20 / 0.003 / 5·10⁻¹²; lattice mass π₀(𝓛(Q)): 0.66 / 0.68 / 0.81;
c_null: 3.1 / 4.8 / 9.8. Reading: with leakage (nulls near the truths gain more than (1 + 2A)τ² log n) the mass at S₀
itself vanishes — the theorem at Q = S₀ does not apply and (N2) says it cannot — while the mass of the lattice
increases, as the lattice form (T1)(a)/(T3)(b) claims.

## 4. Summary of the necessity readings
| hypothesis | reading | evidence |
|---|---|---|
| visibility at level 1 + 2A | NECESSARY (constant sharp) | (a); (N3) |
| (V-c) over all 15-sets | IMPROVABLE → Ξ / (V-m) (adopted in v1.1) | (b) |
| averaged leakage (AL) | NECESSARY-FOR-ROUTE; tracks the truth when all nulls leak; conservative for isolated leakers | (c), (d); (AGG-b) o₀ ≥ T₁ |
| uniform leakage η < η_A (Corollary F1) | sufficient, far from necessary | §2 (iv), (c), (d) |
| one null below (1 + 2A)τ² log n | NECESSARY (constant sharp) | (c); (N2) |
| (FL-16) among nulls | IMPROVABLE | (e) |
| ‖μ‖² ≤ Mn | IMPROVABLE | (f) |
| s₀ fixed | not binding by itself; visibility binds through τ² | (g) |
| (L-gain-R) scale C_L n^{−1/2} | not a threshold; constant C_R decisive at finite n; η-version natural | (h) |
| exponent ½ | NECESSARY (deterministic floor) | §1 |
