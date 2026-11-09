# W3-SAMP numerics index

All scripts: Python 3.13 + numpy, run from this folder (`py -3.13 <script>`); local, small.
- `samp_sim.py` — floating-point simulation of T12 §1–§2's frozen island on a small Ω (arbitrary positive γ₀, d), vectorised
  over islands; exact kernel matrices; RB recording before each Gibbs draw. Verified as such by LC1.
- `run_checks.py` (seed 20261109) → `RESULTS_v1.txt`: MR identities, ST (exact), LT inequalities, C (v1 bounds, T sweep),
  NC probes, D equality. The v1 "kappa0 sharpness" line is withdrawn (filter omitted A_0 = 1; LC1 issue 6).
- `sec4.py` → `RESULTS_v1_sec4b.txt`: re-run of section 4 (NC probes) with a stronger "near" collapse. The file is a
  **combined log of two invocations**: the first two rows with L = 5 (seed 4), the last row with L = 20 (sec4.py edited to
  L = 20, I = 2000, same seed). Finite-n illustrations only (LC1 issue 3).
- `run_checks_v2.py` (seed 7) + `run_checks_v2b.py` (seed 11) → `RESULTS_v2.txt`: regression-realisable targets (T12 §0
  score/prior, block-product start), pointwise stopped-sum and C-i checks, heavy-tailed W, concentrated n = 400 case.
- `run_checks_v3.py` (seed 31) → `RESULTS_v3.txt`: T-free C (telescoping budget, β bound), E E_r ≤ g + β/2, bias ≤ β/2,
  TR minorization (exact kernel products for 200 random orders) and TR bound.
