# C-DLV numerics brief (falsification run of the production core; which no-output paths fire)

Owner: C-DLV lead. Write ONLY inside `Theory_work/Wave1C/C-DLV/numerics/`. No git commands. Local compute only.

## 0. Setup (do not write outside this folder)
- Copy `Scripts/SMC_BVS/core/` (R files + `cpp/`) byte-for-byte to `numerics/core_copy/`; record sha256 of every copied
  file and of the originals in `numerics/core_copy_hashes.txt` (must match). `v3_compile()` writes `.cpp_cache/` next
  to the sources, so ALWAYS `source("<abs path>/numerics/core_copy/v3.R")` (never the original folder).
- Windows, R 4.6.1, Rcpp + digest present. If compilation fails (e.g. `-march=x86-64-v2` in `Makevars.v3`), report the
  exact error in `numerics/COMPILE.md`; you may then patch ONLY compiler flags in the copy's Makevars (log the diff).

## 1. Designs (R port of `Theory_work/Wave1/W1-GEN/numerics/bvs_core.py` `lh_sigma`, `lh_theta`, `exact_gram_design`,
`iid_design_raw`)
- LH-type correlation: G groups of g = 9, within-group equicorrelation rho = 0.4, c linked pairs (groups 2i, 2i+1,
  0-based), cross block Sigma[C_a, C_b] = psi * Sigma[C_a, j_a] Sigma[j_b, C_b] (hubs = first member of each group).
- (M) MASKED: c = 1, psi = 0.2, theta[a_hub] = 1, theta[b_hub] = -0.2 (S0 = {a_hub, b_hub}; b_hub is marginally masked).
- (F) FAVOURABLE: same Sigma, theta[a_hub] = 1, theta[hub of group 3] = 0.7 (unlinked visible group; no masking).
- Design: exact Gram (sqrt(n-1) Q L^T, Q from QR of centred Gaussian) when p <= n-1, else iid rows N(0, Sigma).
  y = X theta + sigma * eps, sigma = 1. Pass raw X, y to `v3_fit` (it standardises).
- (n, p) ladder, all must take the SMC branch (check `fit$branch_run == "smc"`): (100, 27), (200, 54), (400, 81),
  (800, 108); add (1600, 135) only if a single fit at (800,108) takes < 4 minutes. Seeds 1..8 per (design, n, p)
  (data seed and method seed both = seed; method seed = 1000 + seed). First time ONE fit at (200, 54) and report the
  timing before launching the full ladder; keep the total wall time under ~90 minutes (reduce seeds to 5 if needed).
- Allocation: `allocation = list(mem_gb = 16, hours = 24)`.

## 2. Record per fit (one CSV row, `numerics/dlv_runs.csv`; also save a compact RDS per fit with the fields below)
design, n, p, seed, status, branch_run, estimates_available, escalated, tier_final, hpm == S0 (as set), total seconds,
peak_memory_kb, preflight est_bytes, any runtime_guard checkpoint exceeded;
per tier e in {0,1} that ran: pilot stage count N_p (= length(pilot$schedule) - 1), forced_pilot_steps, and for each
grid construction (preliminary, rebuild_1, ...): ok, reason, intervals, N_b = intervals - N_p (bisection-inserted
points), whether S0 is in that construction's V snapshot (`calibration$tiers[[e]]$snapshots`), |V|, and
Lambda_V := max over t in a grid of 2001 points on [0, 2] of Var_{q_t}(d), where q_t(S) ∝ exp(log_gamma0(S) + t d(S))
over the snapshot models (only when the snapshot is not truncated); also the indicator Lambda_V < log(10/9).
Triggers fired per tier. Rebuild count, converged.

## 3. Output
`numerics/run_dlv.R` (+ any helper), `numerics/dlv_runs.csv`, `numerics/rds/`, and `numerics/SUMMARY_dlv.md` with: a
table per (design, n, p) of status counts, escalation rate, mean/max N_p, max N_b, max intervals vs T_e
(T_0 = max(1000, ceil(log2(n+p+1))^2), T_1 = 4 T_0), fraction of constructions with S0 in V, fraction with
Lambda_V < log(10/9), max time and memory. Report every non-`completed` status with its message. Do not interpret
beyond the numbers; no theory claims.
