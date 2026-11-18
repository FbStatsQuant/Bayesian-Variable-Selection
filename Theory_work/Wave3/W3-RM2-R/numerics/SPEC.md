# W3-RM2-R numerics — SPEC (boundary numerics for the weakened hypotheses (V♭), (BM-W⁺), BM(c); observations only)

Purpose (TARGET.md §3): sweep the signal level across the constant-level regime and record where the route's events
and the LS0 probe fail. **Observations only**; the sufficient constants of STATEMENT §2 (M_V⁰, c_TL⁰, c₀, κ₀) are
proof artefacts and much larger than the levels probed; nothing here bears on asymptotic necessity.

## Tools (read-only parent, copied)
Copy `../../W3-RM2/numerics/rm2_common.R` and `validate.R` into this folder as `rm2r_common.R` (adapt; keep the
SW1-3 departures note) — it gives the production-score context, the start-mode DP `start_mode_dp`, and `ls0_fast`.
Production core: `Scripts/SMC_BVS/core` (compile locally, do not edit). Re-run `validate.R` once on this branch and
save `validate_out.txt`.

## Designs and sweep
* **P (Ex-Proxy, fixed design, exact Gram)**: STATEMENT §5 / PARENT `lemmas/L6_examples.md:334-347`: p = ⌊n/3⌋,
  q = ⌊n^b⌋, r² = C₀ log n/n with C₀ = 1, S₀ = {1}, μ = θ_n x₁, σ = 1. b ∈ {0.3, 0.45}; n ∈ {400, 1600}.
  (Build e_1..e_p as centred orthonormal vectors, e.g. QR of a centred Gaussian matrix, fixed per n, then x_j = √(n−1) z_j.)
* **G (Gaussian rows, two truths)**: PARENT SPEC design B1 at b = 0.375, but truth 2 has θ₂ swept (truth 1 fixed at 3).
* Sweep θ_n² = κ σ² log n / n (design P: θ = θ_n; design G: θ₂ = θ_n), κ ∈ {0.5, 1, 2, 4, 8, 16, 32}.
* Seeds: 10 per cell at n = 400, 6 at n = 1600.

## Record per run (`arrays/results_raw.csv`, summary `summary.csv`, prose `RESULTS.md`)
start-mode size, S₀ ⊆ S̃₀ (truth inclusion), S̃₀ ⊆ Q (sandwich); λ_n/log n and the realised visibility min_U δ²_{U,1}/log n
over U = S̃₀ ∩ block ∖ {1}; the truth-removal statistic at visited sets (min over visited T of F(T) − max over
truth-removing neighbours A of F(A)); path-level NA as in PARENT SPEC; LS0 endpoint = S₀ and certification;
for design P at n = 400 also: F(S₀) − max_{S ≠ S₀, |S| ≤ 3} F(S) over a candidate list (a mode-margin proxy).
For design P also compute d_n by Monte Carlo (2000 draws of g, max over truth-removal directions for proxy subsets of
the start mode's lattice — or use the closed form of STATEMENT §5(a) and report both) to illustrate d_n = O(1).

## Compute discipline (binding)
`export TMPDIR=/home/fb31/SMC_Theory_Department/tmp/20261116-W3-RM2-R-numerics; mkdir -p "$TMPDIR"`; run R with
`nice -n 10`, at most 8 worker processes (ramp up: start with 2), never NOTS; arrays and any large output only in
`numerics/arrays/` (git-ignored); write nothing outside `Theory_work/Wave3/W3-RM2-R/numerics/` and `$TMPDIR`;
delete `$TMPDIR` when done. Budget ~1–1.5 h wall time; if a cell is too slow, drop n = 1600 for design G first and
say so.
