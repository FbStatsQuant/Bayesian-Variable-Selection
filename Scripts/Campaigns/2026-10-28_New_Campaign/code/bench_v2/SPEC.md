# bench_v2: implementation contract (BENCH-FIX, D42; manager Opus 5.5, 2026-10-30)

Binding sources: `../../DECISIONS.md` D36, D38, D42; `../../bench_audit/AUDIT.md` v2.1 §3 and §5 (the contract); `../../bench_audit/review/SOL_REVIEW_{1,2}.md`. Where this file and AUDIT §3 disagree, AUDIT §3 wins; report the conflict.

## 0. Paths
- CAMP = `<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign`
- DEPLOYED = `<PC_NB_ARCHIVE>/NOTS_home/projects/BVS/Benchmarks` (local mirror of NOTS `/home/fb31/projects/BVS/Benchmarks`; READ ONLY)
- STUDY = `<PC_NB_ARCHIVE>/NOTS_projects_ml75/BVS/bench20261019` (local mirror of the frozen study; READ ONLY). Dev inputs: `STUDY/dev/inputs/p0500/dev_p0500_S{1..6}_r001.rds`, `.../p1000/...`; dev manifest `STUDY/dev/manifests/dev_inputs_manifest.csv`.
- Scoring (frozen, READ ONLY): `ROOT/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/scoring/` (`code/registry.R`, `derived_rules/derive_rules.R`).
- Local R: `C:/Program Files/R/R-4.4.1/bin/Rscript.exe` (glmnet 4.1-10 locally; production pins 5.1 — use the deployed tests' documented version override for local runs only, and record it).

## 1. Layout
```
code/bench_v2/
  SPEC.md  PROGRESS.md  CHANGES_v2.md  CONSUMERS.md
  BASELINE_SHA256.txt        deployed hashes of every copied file, checked against bench_audit/work_chain/file_hashes.csv
  F1_Lasso/        config.R common.R run_case.R methods/{glmnet_helpers.R,fit_F1_lasso.R}  tests/
  F2_ElasticNet/   config.R common.R run_case.R methods/{glmnet_helpers.R,fit_F2_enet.R}   tests/
  F3_AdaptiveLasso/config.R common.R run_case.R methods/{glmnet_helpers.R,fit_F3_alasso.R} tests/
  tests/           cross-method tests, fixtures, run_all_tests.R, TEST_REPORT.md
  repro/           F1/F2 old-vs-new reproduction + F3 dev runs (scripts, logs, exit codes, CSV summaries, REPRO_REPORT.md)
  DIFF_vs_deployed.patch     unified diff of every changed file vs DEPLOYED
  MANIFEST_SHA256.txt        sha256 of every file under F1_/F2_/F3_ code (written last, at freeze)
  review/
```
Copy the deployed files byte-for-byte first (F1, F2, F3: the 5 tree-hashed files each, plus their `tests/`), verify hashes, then edit.

## 2. F3 change (AUDIT §3, "Exact change", items 1–5)
1. **Pilot = F1's `cv_min` fit, computed in F3.** `zmax <- max(abs(crossprod(X, y))) / n` (F1's exact expression); `lam1 <- GRID$max_mult * zmax * lambda_fraction(GRID)`; `cv1 <- glmnet_cv_engine(X, y, foldid, alpha = 1, lam = lam1, pf = rep(1, p), G = GLMNET)`; `i_p <- cv_choose(cv1$cvm, cv1$cvsd)[["min"]]`; `b <- unname(cv1$full$B[, i_p])`.
   - Pilot failure fails the WHOLE fit (never a null fit): any engine error, non-finite b, or KKT failure at `i_p` in the full fit or any fold fit (exactly F1's `ok_min` condition).
   - Remove `ridge_path_svd`, `ridge_normal_residual`, `ridge_cv`, the ε floor and `alasso_weights`' floor logic.
2. **Screen and weights.** `keep <- which(b != 0)`, `m <- length(keep)`; `w <- abs(b[keep])^(-gamma)`, gamma = 1 (config; assert gamma == 1). Fail the fit if any w is non-finite. `r <- w / max(w)`; `v <- m * (r / sum(r))`. Assert all v finite and > 0 and `abs(sum(v) - m) <= 1e-10 * m`; otherwise fail the fit (never floor or drop).
3. **Second stage.**
   - m ≥ 2: `Xk <- X[, keep, drop = FALSE]`; `zk <- abs(drop(crossprod(Xk, y))) / n`; `lam <- GRID$max_mult * max(zk / v) * lambda_fraction(GRID)`; `glmnet_cv_engine(Xk, y, foldid, 1, lam, v, GLMNET)`; map coefficient rows back to the original p columns.
   - m = 1: closed-form path on the same objective and grid: `beta(λ) = S(x'y/n_d, λ v)/(x'x/n_d)` with S the soft threshold; full data uses n and x'x, fold k uses n_train and x_train'x_train. Same OOF/cvm/cvsd formulas, same `cv_choose`, KKT by `kkt_glmnet`. Code `pilot_single`. Engine-only fields (jerr, npasses) = 0 / NA, declared.
   - m = 0 (genuine empty pilot): every registered rule row is status ok with code `pilot_null`; support "" and k 0; coefficient vectors = zero p-vectors; RSS = Σy²; λ/index/cv fields NA; path table = one row for the null model; candidate table = null model only (`ebic_candidates(X, y, list(), ...)`).
   - KKT checked on the screened problem; CV-rule and EBIC-rule failure conditions exactly as deployed.
4. **EBIC.** Candidates = null + distinct MAPPED supports, computed with the FULL X so p = ncol(X) in log C(p, k). Rules: `ebic1`, `ebic05` (k ≤ 100) and `ebic1_K37`, `ebic05_K37` (k ≤ K, K = floor(n/log n) = 37; assert). K37 picks minimise over valid candidates with k ≤ K using `ebic_pick`'s order (crit, k, key); same occurrence/KKT failure rule as the cap rows; `ebic_at_largest` relative to the rule's own eligible set; `k_valid_max` likewise. These must equal what `derive_rules.R` would derive from the same candidate table (test it).
5. **Schema.** F3 registry: rule_ids `cv_min, cv_1se, ebic1, ebic05, ebic1_K37, ebic05_K37`; roles `primary, S0, S0, S0, S0, S0` (the D42 headline promotion is an analysis-level label, not a code role). Extra cols: drop `kappa`; add `pilot_k`, `pilot_index`, `pilot_lambda`. Retire fields `kappa, ridge, ridge_resid_max, ridge_fold_mse, kappa_min, kappa_index, kappa_boundary, eps_floor, n_floored` and codes `kappa_edge, floored_selected` from F3; add codes `pilot_null, pilot_single` to F3's closed vocabulary. Config: remove the ridge block; `F3 <- list(pilot = "lasso_cv_min", gamma = 1, K_size_bound = 37L)`. Diagnostics add: `pilot = list(lambda = lam1, index = i_p, beta = b, cvm, cvsd, kkt_full, kkt_fold_at_index, fits)`, `keep`, `w`, `v`, and the path table on original indices.

## 3. Evidence saving (all three methods; D42.5, AUDIT §5)
- Every wrapper returns `coefficients`: a named list, one element per registered rule id, each `list(rule_id, status, support, k, index, lambda, alpha (F2 only; NA otherwise), beta_pen, beta_ols)`:
  - `beta_pen`: length-p penalised coefficient vector on original columns, at the rule's index (CV rules: the CV index; EBIC rules: the first, largest-λ, KKT-passing occurrence of the support, else the first occurrence, as the rows already use; null support with no index: zeros).
  - `beta_ols`: EBIC rules only — zero-intercept OLS slopes on the support (zeros elsewhere); NA vector for CV rules. Labelled separately; never mixed.
  - Failed fit: `coefficients` holds NA vectors with the row's status.
- Internal assertion: for every non-failed rule, `support_key(which(beta_pen != 0)) == support`, else the fit fails with a clear error.
- F1 and F2 also gain `ebic1_K37`, `ebic05_K37` rows (roles S0), computed as in §2.4 from their existing candidate tables.
- **F1/F2 invariance:** for the 4 original rules the rule-row values (every column), `beta`, the path/candidate/fold diagnostics and `converged` must be identical to the deployed code's on the same inputs in the same environment. Only additions are allowed.
- Runners: bump `schema_version` to 2 in the RDS; CSV schema = SCHEMA_HEAD + extra cols (new F3 extras). Nothing else changes in the runner unless required; document every runner change.

## 4. Tests (AUDIT §3 "Tests" — all required, with negative controls)
Each test that guards a fault class needs a negative control (a deliberately broken variant, e.g. a mutated function, that the test must FAIL on). Report the pass/fail of each control.
1. **Ridge-weakness test (would have caught it).** A hard assertion that FAILS on the deployed F3 and PASSES on v2. Required: (a) pilot identity — F3's pilot b is `identical()` to the F1 v2 wrapper's `beta` on all 12 dev datasets (c100; plus c050 if time allows), same environment; (b) a synthetic p ≫ n fixture with known truth (block correlation, strong signals) where the assertion "every true variable has a smaller adaptive weight than every noise variable, and the truth lies on the second-stage path" holds for v2 and fails for the deployed ridge pilot. Show both outcomes.
2. Pilot failure propagates to a failed fit (inject a KKT failure / non-finite pilot).
3. Edge sizes m = 0 and m = 1 (fixtures at p ≫ n and at p = 20, 30); m = 1 CV choices and path checked against an independent scalar solution (both cv_min and cv_1se).
4. Weight extremes: |b| ≈ 1e-12; overflow of Σw (e.g. b = (1e-308, 1e-308)) handled by the stable normalisation; underflowed factor fails the fit cleanly.
5. Index mapping: permuted-column fixture; supports map back to original indices.
6. Full-p EBIC vs a hand computation; negative control with screened m instead of p must change a pick.
7. OLS rank deficiency rejected (candidate invalid, scores Inf).
8. Deterministic EBIC ties (crit, k, key).
9. Selected-point KKT on the screened problem; a KKT failure at a selected point fails that rule.
10. Rule consistency: every non-failed rule's support = nonzeros of its saved `beta_pen` (all methods, all dev runs).
11. RSS validity: non-positive / non-finite RSS candidates score Inf.
12. K37 rows equal `derive_rules.R`'s derivation on the same candidate tables (F1, F2, F3).
13. Low-p fixtures p = 20 and 30 for items 2–5 (the same wrapper must work; bench_lowp port is a separate step).
14. Existing deployed tests rerun and adapted (retired ridge tests replaced, not silently deleted — list each).

## 5. Local reproduction and dev runs (`repro/`)
- F1, F2: deployed code vs v2 code, same local environment, on the 12 dev datasets × {c100, c050} (24 cases per method). Compare per §3 invariance. Report every difference (expected: none outside added fields).
- F3 v2 on the same 24 cases: status, pilot k, m, rule supports, runtime; pilot identity vs F1 v2 (test 1a).
- Long runs DETACHED (`Start-Process`/background) with per-job log and exit-code files; parallelise across local cores; record wall times.

## 6. Rules for every worker (D38, charter)
- Edit files only with the Edit/Write tools (or apply_patch). No Python/heredoc edits in a shell.
- Absolute paths always. No `cd … &&`. No `rm` with globs. One simple command per shell call. Scripts run by absolute path.
- Never modify DEPLOYED, STUDY, the frozen scoring folder, or anything on NOTS. No SSH.
- Do not read truth/holdout folders from fitting code; tests may read `STUDY/dev/truth` only for post-fit diagnostics.
- Keep `code/bench_v2/PROGRESS.md` updated after each step (done / running / next).
