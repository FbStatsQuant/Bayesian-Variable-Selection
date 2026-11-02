# BENCH-FIX independent checker report (Sonnet 5.5, 2026-10-30)

Scope: verify W1/W2 claims with my own scripts (all under this folder). I did not run or trust W1/W2 verifier scripts. Only R process at a time, every script < 10 min. Nothing outside `review/checker/` was written.

Evidence files: `check1_hashes.txt` (+`.ps1`), `check3_out.txt`/`check3_results.csv`, `check3b_all24.csv`, `check2_edges_out.txt`/`check2_edges_results.csv`, `check4_out.txt`/`check4_results.csv`, `check5_inject_out.txt`/`check5_inject_results.csv`. Scripts: `check1_hashes.ps1`, `check3_recompute.R`, `check3b_all24.R`, `check2_edges.R`, `check4_lowp.R`, `check5_inject.R` (`peek*.R` only print structure).

## Verdicts

| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Hashes | **PASS** | 15/15 v2 code files equal `repro/snapshot_2a8362b2f348` (sha256). Exactly the 3 `glmnet_helpers.R` files equal deployed (plus 2 F2 `tests/diag_*.R`); the other 12 differ as BASELINE states. Deployed files on disk equal the BASELINE deployed column (22/22 rows) and the audit `file_hashes.csv` (8 prefixes spot-checked). 9/9 bench_lowp copies (`fit_F1/F2/F3`, `glmnet_helpers_F1/F2/F3`, `common_F1/F2/F3`) equal the bench_v2 files; 17/17 `CHANGED_SHA256.txt` "current" hashes equal disk. |
| 2 | Code reading vs AUDIT §3 | **PASS** (no deviation; 5 notes) | Clause table below; the m = 0, m = 1, failure, weight-extreme and permutation branches were also run (check2_edges: 36/36). |
| 3 | Independent recomputation, 4 cases | **PASS** | check3: 168/168 assertions (42 per case). Cross-case structure over all 24 cases (check3b): see below. |
| 4 | Low-p outputs | **PASS** | check4: 204/204 (2 designated cases + 4 more smoke cases; F1–F5). |
| 5 | Diff | **PASS** | No F1/F2 hunk touches fitting arithmetic, CV choice or the original-4 rule logic (table below). Two hunks rewrite lines of original-rule code as behaviour-preserving refactors; both proven bit-identical empirically. |
| + | KKT injection on F1/F2 (extra) | **PASS** | check5: 32/32, deployed vs v2 on a synthetic fixture under four injections. |

## Check 3 detail (dev_p0500_S1_r001_c100, dev_p1000_S4_r001_c050, dev_p0500_S5_r001_c050, dev_p1000_S6_r001_c100)

All via my own code on the saved RDS and the dev input (input sha256 matches the RDS record).

- (a) `identical(F3 pilot$beta, F1 v2 beta)`: TRUE in all 4 (nonzeros 78/70/56/81); `pilot_beta`, `pilot_index`, `pilot_lambda`, `pilot_k`, pilot `cvm`/`cvsd` also equal F1's.
- (b) support == nonzeros(beta_pen) for all 6 F1, 6 F2 and 6 F3 rules in each case (12 method-case sets, 4 cases x 3 methods). All rules `ok`, so the `support_audit` branch is only exercised in check2/5 (injected failures).
- (c) Own zero-intercept `lm.fit` on the FULL design for all F3 path supports (53–57 candidates): candidate set, RSS, EBIC1 and EBIC0.5 equal the saved table (relative difference 0). Re-picks with order (crit, k, key) reproduce `ebic1`, `ebic05`, `ebic1_K37`, `ebic05_K37`: support, k, crit_value, rss, ebic1_value, k_valid_max, index (first KKT-passing occurrence), lambda and the `ebic_at_largest` code all match, 16/16. Negative control: using the screened m instead of p changes the ebic1_K37 pick in 3 of 4 cases (k 15 to 20, 14 to 23, 14 to 19).
- (d) `beta_ols` equals own OLS slopes: relative difference 0 (limit 1e-8) for all EBIC rules of F1, F2, F3; zero off support; CV rules all-NA vectors; `alpha` NA for F1/F3, finite for F2.
- (e) F1 and F2: the 4 original rule rows (every old column), `beta`, `converged` and `diagnostics` are `identical()` between the deployed and v2 runs inside the same RDS. New columns: none (columns unchanged, 2 added rows). K37 rows have role S0 and k <= 37.
- (f) keep == which(b != 0), m == pilot_k; sum(v) − m <= 1.4e-14; v > 0; v·|b| constant (spread <= 5.2e-16); w == 1/|b| exactly; v equals my own m·r/Σr to 5e-17.
- Extra (x): own `glmnet` second stage on `X[,keep]` with penalty factors v: lambda grid equal (rel 0); own 10-fold CV equals saved `cvm`/`cvsd` (rel 0); own cv_min/cv_1se indices equal the saved ones (200/169, 154/128, 162/128, 200/165); own coefficients at the 6 rule indices equal saved `beta_pen` (rel 0) with equal supports; own weighted-KKT at the selected indices <= 1.5e-8 (limit 1e-5); own path supports equal saved `path$key` at all 200 lambdas (0 mismatches).

Cross-case (check3b, all 24 controlled cases, no refit): pilot identity 24/24; coefficient provenance F1/F2/F3 24/24 each; F1/F2 original-4 + beta + diagnostics + converged identity 24/24 each; all rules `ok` for F1, F2, F3 24/24; re-pick from saved candidate tables 24/24; sum(v)=m 24/24. Pilot m range 56–103; ebic1 (cap) k 13–18; the cap-100 and K37 supports are identical in 24/24 cases (K37 never binds on dev data).

## Check 4 detail (`lowp_port/smoke_output/results/smoke`)

Designated: `p0020_S1_r001_c100`, `p0030_S4_r050_c050`; extras: `p0020_S1_r001_c050`, `p0030_S4_r050_c100`, `p0030_S6_r100_c050`, `p0030_S6_r100_c100`. For each of F1–F5:

- no duplicate rule ids; coefficient ids equal row ids; every rule `ok`;
- support == nonzeros(beta_pen) for every rule (F1 6, F2 6, F3 6, F4 7, F5 7);
- K37 rows equal cap rows in support, k, crit_value, rss, lambda, index, beta_pen and beta_ols (F1/F2/F3: ebic1 and ebic05; F4/F5: ebic1, ebic05, bic);
- roles in the stored `rows` follow LA-4: F1–F3 cv_min primary, cv_1se S0, cap rows secondary, K37 S0; F4/F5 ebic1_K37 primary, other K37 S0, cap rows secondary, extras (ebic1_lam005, sic_smax) S0; exactly one primary per method;
- own OLS (input file accessible) equals `beta_ols` for every EBIC-type rule, relative difference 0;
- F3: pilot identical to F1 `fit$beta`; sum(v) = m, v > 0; retired ridge fields absent, `pilot_k/index/lambda` present; schema_version 2 on all five methods.
- Note: the wrapper's own `fit$rules$role` still says S0 for the cap rows (config roles); the stored `rows` carry `secondary`. The low-p runner remaps; scoring or analysis must read the stored `rows`.
- Limits: no saved low-p output has m = 0 or m = 1. Those branches were exercised in check2 (p = 30 fixtures). F4/F5 code was not reviewed; only their saved outputs.
- My first run of this script reported 30 failures ("unique rule ids / coef ids match rows") that were a bug in my own comparison (named vector from `vapply`). Fixed; the rerun is the 204/204 above.

## Check 5: diff classification (`DIFF_vs_deployed.patch`, F1/F2 non-test files)

| File | Hunks | Class |
|---|---|---|
| F1 `common.R` | +`coefficient_evidence` | addition. Adds new failure modes: support mismatch and rank-deficient OLS evidence stop the fit. No fitting arithmetic. |
| F1/F2 `config.R` | rule ids and roles (6 rules) | registry only |
| F1 `run_case.R` | schema 2; outer-failure coefficients; `coefficients` stored | evidence only |
| F2 `run_case.R` | `SCHEMA_VERSION` 2; outer-failure coefficients; `coefficients` stored | evidence only |
| F1 `fit_F1_lasso.R` | failure return adds coefficients; status propagation; `ebic_rule(column, candidates = cand)`; K37 rows; coefficients returned | evidence/K37. The `ebic_rule` signature change keeps the default `cand`, so the original 4 rules take the same path. |
| F2 `common.R` | +`coefficient_evidence` | as F1 |
| F2 `fit_F2_enet.R` | failure return; status propagation; loop `for g` over `names(gammas)` becomes `for rid` over 4 ids (`eligible` = `cand` for non-K37); coefficients returned | evidence/K37. The loop refactor rewrites original-rule lines but is behaviour-preserving. |

Hunks touching fitting behaviour (CV choice, glmnet calls, grids, KKT thresholds, EBIC scoring): **none**. Empirical confirmation: original-4 rule rows, beta, diagnostics and converged identical deployed vs v2 in 24/24 controlled cases (F1 and F2), and in 8/8 paired runs on a synthetic fixture (check5: no injection plus three KKT injections, F1 and F2). The F1/F2/F3 test-file hunks (not fitting code) relax or rewrite deployed assertions, all disclosed in `TEST_REPORT.md`: CV-min exact recovery on orthogonal canaries becomes a diagnostic with paired deployed/v2 identity; the shifted-response 1e-8 path tolerance becomes paired identity plus KKT plus zero intercept.

## Check 2: clause table (`F3_AdaptiveLasso/methods/fit_F3_alasso.R` unless noted)

| AUDIT §3 clause | Code | Verdict |
|---|---|---|
| 1 Pilot = F1 engine at F1 settings: zmax expression, `lam1 = 1.01·zmax·frac`, `alpha = 1`, `pf = 1`, `G` | l.70–73 (same text as `fit_F1_lasso.R` l.35–42) | OK. `identical()` to F1 v2 beta 24/24 dev + 6/6 low-p. |
| 1 `cv_choose()["min"]`, b = full-data coefficients at that index | l.74–75 | OK |
| 1 Pilot failure fails the whole fit (engine error, non-finite, KKT at i_p in full or any fold fit); never a null fit | l.76–79; outer capture l.180–185 | OK, stricter than F1 `ok_min` only by also rejecting non-finite KKT. Tested: kkt tolerance 0 gives 6 failed rows, support NA, NA coefficient vectors; injected engine error gives the same. |
| 1 Ridge, floor, `alasso_weights` floor removed | l.1–13; grep of non-test sources for kappa/ridge/eps_floor/n_floored/floored_selected/kappa_edge | OK (only the retired-field list in `validate_outputs.R` and legacy test text mention them) |
| 2 keep = {b != 0}, m = |keep| | l.80 | OK |
| 2 w = |b|^(−gamma), gamma = 1 asserted, non-finite w fails | l.3–6, l.65–66 | OK. Tested: gamma 2, b = 0, b = NA all rejected. |
| 2 r = w/max w; v = m·r/Σr; assert v finite, > 0, \|Σv − m\| <= 1e-10·m; fail, never floor or drop | l.7–11 | OK. Tested: b = (1e-308, 1e-308) gives v = (1, 1); b = (1e-12, 1, 3) gives v > 0 and Σv = 3; b = 1e-320 (1/b = Inf) fails; b = (1e-300, 1e300) (v underflows to 0) fails. |
| 2 ZvB floor not adopted | l.5 | OK |
| 3 Second stage on `X[, keep]`, map back | l.110, 115–116, 118 | OK. Permuted-column fixture: all 6 supports and keep map back. |
| 3 Grid `1.01·max(z/v)·frac`, common folds, full-data weights in folds (O7) | l.111–116 | OK (grid equal to my own, rel 0) |
| 3 m >= 2: glmnet engine with pf = v | l.116 | OK (own glmnet reproduces coefficients, CV, indices) |
| 3 m = 1: closed form `S(x'y/n_d, λv)/(x'x/n_d)`, training-fold n and Gram, same OOF/cvm/cvsd formulas, `cv_choose`, KKT by `kkt_glmnet`, code `pilot_single` | l.22–52, 115, 126 | OK. Independent scalar solution (p = 30 fixture, m = 1): cvm rel 2.2e-16, cvsd rel 4e-16, cv_min/cv_1se indices 133/1 equal, coefficients equal, EBIC picks equal, path supports equal. |
| 3 m = 0: all rows ok, `pilot_null`, support "", k 0, zero vectors, RSS = Σy², lambda/index/cv fields NA, one-row path, null-only candidate table | l.87–107 | OK. Tested on a pure-noise p = 30 fixture; also null EBIC1 = n·log(RSS/n). |
| 3 KKT on the screened problem; CV and EBIC failure conditions as deployed | l.121–123, 146–147, 155 (vs `fit_F1_lasso.R` l.83–84, 89) | OK. Second-stage KKT injection: CV rules fail, EBIC rules fail iff the chosen support is non-null, and `beta_pen` equals the `support_audit` vector. |
| 4 EBIC on the null plus distinct mapped supports, full-X p = ncol(X) | l.124; `common.R` l.60–77 (`p <- ncol(X)`) | OK. Own recomputation matches; screened-m negative control changes the pick in 3 of 4 cases. |
| 4 K37 rules k <= 37; ties (crit, k, key); rank and RSS validity; `ebic_at_largest` / `k_valid_max` relative to the rule's own eligible set | l.148–161 (eligible l.150, valid_max l.154, code l.160); `common.R` l.51–85 | OK |
| 4 Bound K = 37 asserted | l.67–68 | OK, with note 3 |
| 5 Rule ids/roles: `cv_min` primary, other five S0 | `config.R` l.60–61 | OK, with note 1 |
| 5 Extra cols: drop kappa; add `pilot_k`, `pilot_index`, `pilot_lambda` | `config.R` l.62–63; extras l.85 | OK |
| 5 Retire fields and codes; add `pilot_null`, `pilot_single` | `config.R` l.65–70 | OK |
| 5 `pilot_beta` and `keep` saved | l.100, 163 (diagnostics) | OK (not row columns, as SPEC) |
| 5 Coefficient provenance incl. failed rules: CV at CV index; EBIC at first KKT-passing occurrence else first; beta_ols labelled separately; failed fit gives NA vectors | l.105, 170, 190; `common.R` l.137–163 | OK. Tested with injected failures (check2, check5). |
| 5 `config.R` F3 block `pilot/gamma/K_size_bound` | `config.R` l.45 | OK |

Notes (none is a deviation from AUDIT §3):
1. AUDIT calls `ebic1_K37`/`ebic05_K37` "companions" while also calling K37 "primary among the EBIC rules"; the code gives them role S0 (SPEC: the headline promotion is analysis-level). Consistent with SPEC and with the low-p LA-4 mapping.
2. m = 0 stores `heldout = matrix(0, n, 2)` (predictions 0, per AUDIT) and has no `cv_*`/`index` diagnostics; consumers must not read them for `pilot_null` fits.
3. K37 uses `floor(n/log(n))` from the data; it is asserted equal to 37 only when n = 200, and `F3$K_size_bound` is otherwise unused.
4. F1 and F3 pilots agree because their GRID/GLMNET/COMMON blocks are equal today. Identity is verified numerically (24/24), not enforced structurally, so a later config edit in one folder would silently break it.
5. m = 0 and m = 1 branches were never reached by the 24 dev fits (m = 56–103). They are supported by the check2 fixtures and W1/W2 tests, not by dev data.

## Things that should be settled before the freeze

1. **F1 adapted legacy suite has no completed six-rule pass (blocks "all tests pass" for SPEC §4 item 14).** `repro/controlled_2a8362b2f348/F1_legacy_capped.log` ends "25 of 26 passed"; the failing item is 9f ("isolated KKT violations", `identical(r$status, c("failed","failed","ok","ok"))`, a stale four-rule expectation) and `.capped_exit` = 1. The six-rule rerun (`F1_six_rule.log`) stops after test 3c, has no exit file and no later results (cancelled externally, per PROGRESS). `TEST_REPORT.md` itself says F1 is "incomplete, not acceptance evidence". My check5 shows the underlying behaviour (injected KKT failures) is right for F1 and F2, but the repaired suite must still be run to completion, or the manager must explicitly waive it.
2. All local tests (W1, W2 and mine) ran with glmnet 4.1-10 and the test-only `glmnet_target_path`/`assert_pkg_version` overrides; production pins glmnet 5.1 and F3 shares the helpers byte-for-byte with deployed. The DEV bundle on NOTS is the first evidence under 5.1. Do not treat local results as a PROD release gate.
3. `MANIFEST_SHA256.txt` and the bundle placeholders (`<<BENCH_V2_MANIFEST_SHA256>>`, `<<BENCH_V2_F3_SOURCE_SHA256>>`) are written at freeze and were not checkable; `BASELINE_SHA256.txt` reflects the pre-freeze tree (F2 `run_case.R` was LF-normalised, so the runner tree hash will differ from deployed by design). I verified the 15 code files against the snapshot hash set, not the tree hash `2a8362b2…aa67` itself.
4. The original `repro/*.rds` batch (24 files read from the live tree, F3 edited after launch) is exploratory per REPRO_REPORT; all my checks used only the controlled snapshot RDS. Its evidence is as stated, but the original batch should not be cited as final-source evidence.

## Observations for HQ and the analysis (non-blocking)

- F3 `cv_min` sits at the last grid point (index 200, info code `lambda_last`) in 9 of 24 dev cases, all 9 at c = 1 (9 of 12 c100 cases; none of 12 c050), and in the p = 20, c100 low-p case I printed (the other low-p cases were not tabulated). The weighted second-stage path does not reach a CV minimum inside the 1e-4 grid for these fits. This is the contract (F1 grid rule), but `cv_min` k is then near the screen size and the flag should be reported beside the CV rule.
- K37 never binds on the dev data (cap and K37 supports identical 24/24); the difference between ebic1 and ebic1_K37 will only show where the cap-100 minimum has k > 37.
- Local F3 wall times under heavy laptop contention were 185–757 s per fit (about the F1 time, as the pilot is F1); I cannot validate the NOTS cost estimate.
- Out of scope and not checked: scoring/`derive_rules` consumers (apart from my own K37 re-derivation), F4/F5 and A1–A3 code, the job bundles, `CONSUMERS.md`, and the optional OLS-pilot low-p sensitivity that W2 reports as not implemented.

## Disclosures (D38)

- Two of my scripts first contained bugs of my own (PowerShell alias `H` = `Get-History`; named-vector `identical` in check4). Both were fixed and rerun; reported numbers are from the corrected runs.
- Two read-only shell calls were not "one simple command": `cat … ; echo; cat …` (logs) and `ls -la … | grep` (listing). No writes. R's automatic tempdir is under the Windows user temp folder, outside the tree.
- I ran the v2 F3/F1/F2 wrapper code (sourced read-only, with the same documented local overrides W1 uses) in check2 and check5; no source, mirror or NOTS file was modified, and no SSH was used.
