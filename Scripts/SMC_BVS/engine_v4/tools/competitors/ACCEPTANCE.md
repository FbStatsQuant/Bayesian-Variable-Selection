# Competitor acceptance runs (Sol F8) — protocol draft (WP5, 2026-11-16)

Purpose: before any competitor result is quoted, prove for each retained method that the actual package/version, data
conversion, tuning and prediction code run at the target p, with measured cost and memory, and that the harness reads
the real API correctly (the mocks of `mock_packages.R` check only our extraction logic).

## 1. Install (manager, NOTS, once)
`install_competitor_packages.sh` (dry run by default). Library: `$DEPT/R/4.5.2/library`. Versions: one dated CRAN
snapshot (`--snapshot 2026-11-02`); at that snapshot (MEASURED from the snapshot index, 2026-11-16): glmnet 5.2,
ncvreg 3.16.0, biglasso 1.7.2, bigmemory 4.6.6, L0Learn 2.1.0, susieR 0.14.2, varbvs 2.6-10, BAS 2.0.2 (+ 19 dependencies,
fewer if the R/4.5.2 module library already has them). glmnet 5 and BAS 2 are major versions above the API the harness
was written against: the acceptance run is where that is checked. The lock file records the installed versions.
If NOTS cannot reach the repository: `--download-only DIR` on Owls, copy DIR, `--apply --from-dir DIR` on NOTS.

## 2. Acceptance cells (one dataset per cell; the same regenerated datasets as the engine)
| rung | data | methods |
|---|---|---|
| 10⁴ | AR(0.6) strong, n = 200 (= the A2 pilot dataset) | all: lasso_cv_min/1se, mcp_cv, scad_cv, l0learn_cv, susie, varbvs, bas, lasso_cv_big, sis_screen, marg_ols |
| 10⁵ | AR strong, n = 200 | lasso_cv_min/1se, mcp_cv, lasso_cv_big, l0learn_cv, susie, varbvs, sis_screen |
| 10⁶ | AR strong, n = 200 | lasso_cv_big, susie, varbvs, sis_screen (lasso via glmnet on the dense 1.6 GB X: attempted, outcome recorded) |

Per (cell, method): status (completed / failed / timeout / package_missing), wall, CPU (sacct CPUTimeRAW, all threads and
all CV folds), peak RSS, package version (from the record), and the evaluator record (`smcbvs4 eval --competitor`).
Pass = completed within the declared limit with a non-empty predictive the evaluator scores; a failure or timeout is an
outcome with its allocated cost, never a dropped dataset. Large-p check: no p² array (peak RSS ≤ 3 × X).

## 3. Cost (ESTIMATE, planning; replaced by the acceptance measurements)
Plan §4: under 10 core-h per dataset for the penalised and variational methods at 1M. Acceptance worst case, as limits
(billed CPUs × time): 10⁴ cell 11 methods × 4 CPUs × 1 h = 44; 10⁵ cell 7 × 8 × 2 h = 112; 10⁶ cell 4 × 16 × 2 h = 128
→ **≤ 284 billed core-h worst case**, expected far less. One job array per rung (the Slurm driver's conventions:
sapphirerapids, department paths, ≤ 2 h per task, `--kill-on-invalid-dep`); submitted by the manager.

## 4. What it does not establish
Agreement with each package's documentation beyond the fields used; convergence diagnostics beyond each package's own
(recorded when exposed); superiority claims (H-4: "not found in the literature", never "first").
