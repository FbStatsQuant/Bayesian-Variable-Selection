# Competitor acceptance runs (Sol F8) — protocol draft (WP5, 2026-11-16)

Purpose: before any competitor result is quoted, prove for each retained method that the actual package/version, data
conversion, tuning and prediction code run at the target p, with measured cost and memory, and that the harness reads
the real API correctly (the mocks of `mock_packages.R` check only our extraction logic).

## 1. Install (manager, NOTS, once)
`install_competitor_packages.sh` (dry run by default; `--apply` needs `CONFIRM=yes`; every path it is given must resolve
inside the department folder; R's temp files go to `$DEPT/tmp/r-install-*`, removed after). Library:
`$DEPT/R/4.5.2/library`; the user library `~/R/...` is not used. Versions: one dated CRAN
snapshot (`--snapshot 2026-11-02`); at that snapshot (MEASURED from the snapshot index, 2026-11-16): glmnet 5.2,
ncvreg 3.16.0, biglasso 1.7.2, bigmemory 4.6.6, L0Learn 2.1.0, susieR 0.14.2, varbvs 2.6-10, BAS 2.0.2 (+ 19 dependencies,
fewer if the R/4.5.2 module library already has them). glmnet 5 and BAS 2 are major versions above the API the harness
was written against: the acceptance run is where that is checked. The lock file records every package of the installed
closure with its version and library path (target library or the R module's own). A package installed below its API
floor is reinstalled; the run fails if any floor is unmet afterwards.
If NOTS cannot reach the repository: `--download-only DIR` on Owls, copy DIR, `CONFIRM=yes … --apply --from-dir DIR` on
NOTS (DIR is indexed as a local repository, so dependencies install before the packages that need them; tested in
`test_install_script.sh`).

## 2. Acceptance cells (one dataset per cell; the same regenerated datasets as the engine)
| rung | data | methods (records) |
|---|---|---|
| 10⁴ | AR(0.6) strong, n = 200 (= the A2 pilot dataset) | all, **12 records**: lasso_cv_min, lasso_cv_1se, mcp_cv, scad_cv, l0learn_cv, susie, varbvs, bas, lasso_cv_big, sis_screen, marg_ols, ols_oracle |
| 10⁵ | AR strong, n = 200 | **8 records**: lasso_cv_min, lasso_cv_1se, mcp_cv, lasso_cv_big, l0learn_cv, susie, varbvs, sis_screen |
| 10⁶ | AR strong, n = 200 | **5 records**: lasso_cv_big, susie, varbvs, sis_screen, and lasso_cv_min via glmnet on the dense 1.6 GB X (attempted, outcome recorded) |

lasso_cv_min and lasso_cv_1se are two records, each from its own `cv.glmnet` call (`p1m_competitors.R`), so they count
as two runs. Per (cell, method): status (completed / failed / timeout / package_missing), wall, CPU (sacct CPUTimeRAW,
all threads and all CV folds), peak RSS, package version (from the record), and the evaluator record (`smcbvs4 eval --competitor`).
Pass = completed within the declared limit with a non-empty predictive the evaluator scores; a failure or timeout is an
outcome with its allocated cost, never a dropped dataset. Large-p check: no p² array (peak RSS ≤ 3 × X).

## 3. Cost (ESTIMATE, planning; replaced by the acceptance measurements)
Plan §4: under 10 core-h per dataset for the penalised and variational methods at 1M. Acceptance worst case, as limits
(billed CPUs × time): 10⁴ cell 12 records × 4 CPUs × 1 h = 48; 10⁵ cell 8 × 8 × 2 h = 128; 10⁶ cell 5 × 16 × 2 h = 160
→ **≤ 336 billed core-h worst case**, as limits; expected far less (MANIFEST_CELLS's 400 core-h competitor line plans
the expected use at all rungs, acceptance included). One job array per rung (the Slurm driver's conventions: sapphirerapids, department paths, ≤ 2 h per task, `--kill-on-invalid-dep`); submitted by the manager.

## 4. Open
- **Equal-CPU model-space MCMC at 10⁴ (Sol F8)**, with the same prior and scorer as the engine: not in this package
  list, and engine_v4 has no MCMC mode (as of this PR). OPEN for the manager: an engine MCMC mode (WP-level work), or
  BAS `method = "MCMC"` as a labelled stand-in (its g-prior and model prior are not the engine's), or drop it with a
  stated reason.

## 5. What it does not establish
Agreement with each package's documentation beyond the fields used; convergence diagnostics beyond each package's own
(recorded when exposed); superiority claims (H-4: "not found in the literature", never "first").
