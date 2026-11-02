# W7-SEC — working notes (chronological)

Run W7-SEC, branch `theory/W7-SEC`, 2026-11-02. Nothing here is reviewed.

## 0. Orientation
- Task: T05 (disclosed negative, explicit constants), T33 (fp error bound for F(S) on the Cholesky path + induced
  HPM / log Ẑ bounds, combined with W2-BOOK's VAL-FP), T32(i) (verify W5-LOCKBOOK, do not duplicate).
- W5-LOCKBOOK (`origin/theory/W5-LOCKBOOK`) PROVED T32(i) as a deterministic count with corollary T32(c). Code
  referenced at commit 9db8748; `git diff 9db8748 HEAD -- Scripts/SMC_BVS/core` is empty, so the code read here is
  the same code.

## 1. T32(i) verification log (code re-read independently)
- Round: `one_round` → m labels, Gibbs evaluates ≤ 1 (the other configuration), uswap ≤ 1, nswap ≤ 1 (0 if no
  candidate), indep exactly 1 → ≤ m = p + B + 2 evaluations. Confirmed (`v3_engine.h:113–214`).
- Island: N initial evals + T stages × N rounds + L + Hm rounds; Hm = 4 (`v3_run.R:87`, `v3_calib.R:12`). Confirmed.
- Calibration tier: pilot (1 island of H_e, then 1 LS), ≤ ℓ diagnostic iterations (`for (it in seq_len(cs$ell))`),
  each 4 islands + 1 LS; V builds: preliminary + ≤ 1 per iteration = ≤ ℓ + 1; |V| ≤ 1 + 20p + 20p
  (`v3_ledger.h:76`: top 40p+1, lead0/lead1 20p). Confirmed.
- Tiers ≤ 2 (`v3_calibrate`: `if (!fired || e == 1) break`). Confirmed.
- Final: inherited rescoring ≤ |top ∪ lead0 ∪ lead1| ≤ 80p + 1, 4 islands (`islands = 4L`), 1 LS. Confirmed.
- LS: 1 centre eval + ≤ ℓ+1 scans, each ≤ p flips + k(p−k) swaps. Confirmed (`v3_engine.h:378–418`).
- Tables: once in `cpp_setup` (`v3_core.cpp:280`); `cpp_tables` (:178) and `cpp_score` (:112) are user interfaces;
  timing scores only on the exact branch (`v3_fit.R:21–25`). Confirmed.
- **Addendum (floating point).** W5's step 2(a) uses EX-A for "pilot ≤ T_e stages". Without EX-A: every pilot step
  advances φ by ≥ 1/T_e − 2u (u = 2⁻⁵³) unless it ends at 1, and any step from φ > 1 − 1/T_e ends at exactly 1
  (pass at 1, or forced min(1, φ + 1/T_e) then snapped). Hence in floating point the pilot has ≤ T_e + 1 stages, and
  ≤ T_e unless a *non-forced* bisection value lands in [1 − 2T_e u, 1). The fp-safe form of T32(i) replaces T_e by
  T_e + 1 in the pilot term only. Details in REPORT §3.3.

## 2. T05 plan
Exact representation under ORTH: Q_S = (n−1)V_S/V_tot with V_S = R′ + Σ_{j∉S}T_j² + n⁻¹Σ_{j∈S}T_j²,
T_j = √(n−1)θ*_j/σ* + ξ_j, ξ iid N(0,1), R′ ~ χ²_{n−1−p} independent. The s_y standardisation cancels exactly.
Then the HPM is a top-k set; prove (ii) both halves and (iii) with explicit finite-n constants.

## 3. T33 plan
Compile `v3_score.h` in a C++ harness, compare log m(S) with an mpmath reference at 60 digits on well- and
ill-conditioned designs; derive a rigorous bound via Cholesky backward error + the structural facts λ_min(H_S) ≥ 1,
λ_min(A_S) ≥ 1, Q_S ≥ y′y/(n+1).
