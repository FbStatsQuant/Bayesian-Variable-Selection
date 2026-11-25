# Frequentist benchmarks for S1/S2: lasso-CV (glmnet) and SCAD (ncvreg)

Builder: Fable-F, 2026-11-25. Contract: `../../INTERFACE.md`. Nothing here is committed by the builder.

| File | What it is |
|---|---|
| `fit_lasso_cv.R` | `fit_lasso_cv(X, y, method_seed, ctrl)`: `glmnet::cv.glmnet` at its defaults |
| `fit_scad.R` | `fit_scad(X, y, method_seed, ctrl)`: `ncvreg::cv.ncvreg(penalty = "SCAD")` at its defaults |
| `test_frequentist.R` | unit test (defaults pinned, contract, fidelity, determinism, never-error, timing) |

Each script opens with a PROVENANCE block (paper, DOI, section, package version, every setting with its source). This README is the summary.

## Software (authors' own, nothing reimplemented)

| Package | Version | Source | Library |
|---|---|---|---|
| glmnet | 5.2 (CRAN, Date 2026-10-26) | already installed | `/home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib` |
| ncvreg | 3.16.0 (CRAN, published 2025-11-06) | installed 2026-11-25 from cloud.r-project.org | same |

R 4.6.0 on Owls. Neither adapter uses `parallel` or a cluster. Both shared objects link `libgomp` and `flexiblas`, so the harness should export `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` (or any value up to 4) to hold the core limit; the adapters do not set thread counts themselves.

## Protocol

**Lasso.** `set.seed(method_seed); cvfit <- cv.glmnet(X, y)`; selected = nonzero coefficients of `coef(cvfit, s = "lambda.1se")`. All glmnet defaults: gaussian, `alpha = 1`, 100 λ values, `lambda.min.ratio = 0.01` if n < p else `1e-4`, `standardize = TRUE`, `intercept = TRUE`, `thresh = 1e-7`, `fdev = 1e-5`, `devmax = 0.999`, 10 folds, MSE loss. The fit is isolated from the session: the adapter saves the caller's `glmnet.control()`, applies `glmnet.control(factory = TRUE)` for the fit, and restores the caller's values on exit. `grouped` is recorded at its effective value (glmnet turns it off below 3 observations per fold).

**SCAD.** `set.seed(method_seed); cvfit <- cv.ncvreg(X, y, penalty = "SCAD")`; selected = nonzero coefficients of `coef(cvfit)`, which is at `lambda.min` (minimum CV error). All ncvreg defaults: gaussian, `gamma = 3.7`, `alpha = 1`, 100 λ values, `lambda.min = 0.001` if n > p_eff else `0.05`, `dfmax = p_eff + 1`, `eps = 1e-4`, `max.iter = 10000`, 10 folds, deviance loss; ncvreg always standardizes and fits an intercept. p_eff is the number of non-constant columns, which is the p ncvreg uses for both defaults.

Both return `pip = NULL`. Both never raise an R error: a method-level failure (including any NA, NaN, Inf or -Inf in X or y) returns `selected = integer(0)` and `extra$status = "failed: <msg>"`. Warnings are captured in `extra$warnings`.

## Sources read, and what each one fixes

| Source | Read as | What it fixes |
|---|---|---|
| Tibshirani 1996, JRSS-B 58(1):267-288, DOI 10.1111/j.2517-6161.1996.tb02080.x | PDF on Owls (scanned) | §2.1 lasso, standardized x, intercept = ȳ. §4 tuning by fivefold CV / GCV / risk estimate, lowest estimated prediction error |
| Friedman, Hastie & Tibshirani 2010, JSS 33(1), DOI 10.18637/jss.v033.i01 | PDF on Owls | §2 objective; §2.5 path of K = 100 λ; §2.6 centring, unpenalized intercept; §6 K-fold CV, "we often use the one-standard-error rule" |
| glmnet 5.2 manual + vignette "An Introduction to glmnet" + NEWS | installed package | `nfolds = 10`; `coef`/`predict` on `cv.glmnet` default to `s = "lambda.1se"`; `standardize`, `intercept` defaults |
| Fan & Li 2001, JASA 96(456):1348-1360, DOI 10.1198/016214501753382273 | PDF on Owls (`Benchmark_methods/Fan_Li_2001_SCAD.pdf`, open copy from J. Fan's Princeton page) | §2.1 SCAD penalty, a ≈ 3.7 by a Bayes-risk argument; §4.2 tuning by fivefold CV or GCV; §4.3 Table 1 tests a fixed a = 3.7 ("SCAD2") against a chosen by GCV ("SCAD1") |
| Breheny & Huang 2011, AOAS 5(1):232-253, DOI 10.1214/10-AOAS388 | PDF on Owls | §2 standardization and intercept; §2.2 SCAD coordinate descent; §2.4 100 λ on the log scale; §4.2 convexity diagnostic; §4.3 hybrid γ choice (from the AIC/BIC-selected λ against the convexity boundary), then CV for λ; §5.2 tenfold CV for λ |
| ncvreg 3.16.0 manual + vignette "Getting started with ncvreg" + R source | installed package | `gamma = 3.7` for SCAD, `nfolds = 10`, `coef(cvfit)` at `lambda.min`, no 1se rule |
| Hastie, Tibshirani & Tibshirani 2020, Stat. Sci. 35(4):579-592, DOI 10.1214/19-STS733 (S2 source) | arXiv:1707.08692v2 on Owls, §3.1, and their code `github.com/ryantibs/best-subset` @ `796e8171` (`sims/sim.hi5.R`, `bestsubset/R/lasso.R`, `R/sim.R`) | how S2 ran the lasso (below) |
| Griffin, Łatuszyński & Steel 2021, Biometrika 108(1):53-69, DOI 10.1093/biomet/asaa055 (S1 source) | arXiv:1708.05678v3 on Owls, §4.1 | no frequentist comparator was run |

**How the S2 paper ran the lasso**: `glmnet.control(fdev = 0)`, then `lasso(x, y, intercept = FALSE, nlam = 100)` (50 in their "low" setting), `standardize = TRUE`; λ chosen as the **minimum prediction error on an independent validation set of size n**. They did not run SCAD. The S1 paper ran neither method.

We depart from that in four ways, each recorded as OURS in every run's `settings`: CV instead of the validation set (OURS-2), the one-standard-error rule instead of minimum error (OURS-1), `intercept = TRUE` (OURS-3), and glmnet's factory path stopping instead of `fdev = 0` (OURS-6). The same in both: `standardize = TRUE` and 100 λ values (their "low" setting used 50; we keep 100 throughout).

## OURS flags

Lasso (labels match the PROVENANCE block of `fit_lasso_cv.R`):

| Flag | Choice | Reason |
|---|---|---|
| OURS-1 | λ rule = `lambda.1se`, not `lambda.min` | Documented rationale: `lambda.1se` is the default of `coef`/`predict` on a `cv.glmnet` object and favours parsimony when CV errors are close (Friedman et al. 2010 §6, doi 10.18637/jss.v033.i01: it "errs on the side of parsimony"). Using it as the rule for exact support recovery is OURS. Tibshirani 1996 §4 and the S2 paper used the minimum-error rule, so the `lambda.min` set is also returned from the same fit (`extra$selected_lambda_min`); `ctrl$lambda_rule = "lambda.min"` makes it primary. |
| OURS-2 | 10-fold CV instead of the S2 paper's validation set | The adapter receives only (X, y). A fresh validation set of size n would give the lasso data the other methods never see. 10-fold CV is the software authors' default. |
| OURS-3 | `intercept = TRUE` (S2 scripts: `FALSE`) | glmnet default, as INTERFACE.md directs ("each adapter does whatever its author does"). |
| OURS-4 | folds seeded by `set.seed(method_seed)` | INTERFACE.md seed rule. |
| OURS-5 | selected = nonzero coefficients | INTERFACE.md selection rule. |
| OURS-6 | factory path stopping (`fdev = 1e-5`, `devmax = 0.999`), with the fit isolated from ambient `glmnet.control()` | The S2 scripts set `fdev = 0`. We keep the glmnet factory values, and force them for the fit so that no session-level control setting can change a result; the caller's controls are restored on exit. |

SCAD (labels match the PROVENANCE block of `fit_scad.R`):

| Flag | Choice | Reason |
|---|---|---|
| OURS-1 | γ fixed at 3.7, not tuned | 3.7 is the ncvreg default for SCAD and the value Fan & Li recommend (§2.1) and test as a fixed choice (§4.3 Table 1, "SCAD2", doi 10.1198/016214501753382273). Not done: Fan & Li §4.2's two-dimensional (λ, a) search, and Breheny & Huang §4.3's hybrid choice, which selects λ by AIC/BIC, compares it with the convexity boundary, adjusts γ by hand over a few iterations, and only then cross-validates λ. ncvreg automates neither, and writing a γ search would be a reimplementation. The §4.2 convexity diagnostic is reported for the CV-chosen λ (`extra$convex.min`, `extra$cv_min_in_nonconvex_region`) as information only. |
| OURS-2 | folds seeded by `set.seed(method_seed)` | INTERFACE.md seed rule (`cv.ncvreg` 3.16.0 has no seed argument). |
| OURS-3 | selected = nonzero coefficients at `lambda.min` | INTERFACE.md selection rule. |

Two things that follow from using the authors' current software rather than the original papers' procedures: 10-fold CV where Tibshirani 1996 and Fan & Li 2001 used fivefold CV or GCV, and coordinate descent where Fan & Li used local quadratic approximation.

**Asymmetry to know about.** The lasso primary rule is `lambda.1se` and SCAD is at `lambda.min`, each being its own software's default (ncvreg has no 1se rule). For a like-for-like comparison at minimum CV error, use `extra$selected_lambda_min` of the lasso.

## Unit test

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 19 Rscript test_frequentist.R [--full]
```

Exit status 0 means every check passed. The test data generators are local to the test (S1 design of Griffin et al. §4.1, S2 design of Hastie et al. §3.1); the harness generator is not involved. What it checks:

1. the package defaults cited above are the installed ones (a package upgrade that changes a default fails the test);
2. the return value matches the INTERFACE.md contract;
3. fidelity: the adapter's selected set and λ are identical to a direct `set.seed(s); cv.glmnet(X, y)` / `cv.ncvreg(X, y, penalty = "SCAD")` call read with the package's own `predict(type = "nonzero")` / `predict(type = "vars")`;
4. determinism: the result depends on `method_seed` only, not on the RNG state before the call;
5. never-error: 17 bad or awkward inputs per method (NA, Inf and -Inf in X and in y, wrong length, constant y, data.frame, bad seeds, one column, zero-variance column, n = 12) return a well-formed result, and every non-finite input gives `integer(0)` with a `failed: ` status;
5b. recorded settings are the effective ones: `grouped`, the n-fold protocol string, the four S2 departures tagged OURS, factory `fdev`/`devmax`/`thresh`/`maxit`; the lasso fit is unchanged under an ambient `glmnet.control(fdev = 0, thresh = 1e-4, devmax = 0.5)` and the caller's controls are restored (also after a failed call); SCAD's recorded `lambda.min` and `dfmax` follow p_eff and match the fitted path;
6. sanity: in the high-SNR cases at least half of the true signals are selected and fewer than n/2 variables are selected. This gate only catches bugs; exact TP / FP / FN are reported, not gated, because check 3 already shows the output is the authors' own.

### Results (2026-11-25, Owls, one thread, `nice -n 19`, machine load 80 to 115, `--full`)

**130 of 130 checks passed, exit status 0** (rerun after the review fixes; selected sets and λ identical to the pre-review run of 108 checks). No package warnings in the 10 fits below. Log: `/home/fb31/BVS-wt/P1M/.rc_tmp/fableF/test_run6_full.log` (scratch, untracked).

| Case | Method | selected | TP | FP | FN | exact | fit time (s) | Note |
|---|---|---|---|---|---|---|---|---|
| S1-like n=200 p=500 ρ=0.6 SNR=3 | lasso (1se) | 47 | 10 | 37 | 0 | no | 0.47 | at `lambda.min`: 71 selected, 61 FP |
| | SCAD | 11 | 10 | 1 | 0 | no | 0.46 | CV minimum in the non-convex region |
| S1-like n=200 p=500 ρ=0.6 SNR=0.5 | lasso (1se) | 0 | 0 | 0 | 10 | no | 0.62 | null model at both rules |
| | SCAD | 1 | 1 | 0 | 9 | no | 4.43 | |
| S2 high-5 n=50 p=1000 ρ=0.35 SNR=6 | lasso (1se) | 5 | 5 | 0 | 0 | **yes** | 0.21 | at `lambda.min`: 47 selected, 42 FP |
| | SCAD | 5 | 5 | 0 | 0 | **yes** | 0.39 | |
| S2 high-5 n=50 p=1000 ρ=0.35 SNR=0.42 | lasso (1se) | 0 | 0 | 0 | 5 | no | 0.21 | at `lambda.min`: 15 selected, 4 TP |
| | SCAD | 15 | 4 | 11 | 1 | no | 0.45 | CV minimum in the non-convex region |
| S1 full size n=1000 p=5000 ρ=0.6 SNR=2 | lasso (1se) | 32 | 8 | 24 | 2 | no | 11.9 | at `lambda.min`: 109 selected, 10 TP, 99 FP |
| | SCAD | 30 | 10 | 20 | 0 | no | 51.0 | CV minimum in the non-convex region |

One dataset per case, so these are illustrations, not rates.

What the manager should expect from this, before the grid is run:

- **On the S1 design the CV-tuned lasso did not recover the exact support in any test case, under either λ rule.** With ρ = 0.6 it keeps tens of false positives, and at full size `lambda.1se` also dropped 2 of the 10 signals. The output is identical to the authors' direct call, so this is the method.
- SCAD's CV minimum fell in the locally non-convex region in 3 of 5 cases. That is the Breheny & Huang §4.2 diagnostic, reported for information. It is not their §4.3 criterion for raising γ, which looks at the AIC/BIC-selected λ; we compute no AIC/BIC λ and keep γ = 3.7 (SCAD OURS-1). The flag is in every record.
- Timing at the largest S1 size was 7 to 12 s (lasso) and 43 to 51 s (SCAD) per fit over two runs on a busy machine.

History of the test itself: the first sanity gate required all true signals found and at most 10 false positives. It failed on the lasso (37 false positives at n=200; 8 of 10 signals at full size). Because the fidelity check shows those sets are exactly glmnet's, the gate was changed to the bug-detecting bound above rather than the adapter being changed. One early foreground run was stopped by an outside signal (shell exit 147, not an R error) while machine load was above 100; reruns with stdin detached completed.

## Missing papers

None. Fan & Li 2001 was not on Owls at the start; an open copy was fetched from the first author's Princeton page and the manager filed it at `/home/fb31/Bayesian-Variable-Selection/_local/papers/Benchmark_methods/Fan_Li_2001_SCAD.pdf`. No copy remains in the worktree scratch.

Two caveats on versions read: Hastie et al. 2020 and Griffin et al. 2021 were read in their arXiv versions (the PDFs on Owls), not the journal versions.

## Review

Astra-F, 2026-11-25: PASS-WITH-FIXES. All 7 fixes applied the same day: (1) documented rationale for `lambda.1se`; (2) every S2 departure recorded as OURS in `settings`; (3) fit isolated from ambient `glmnet.control()`, `fdev` and `devmax` recorded; (4) `is.finite` input checks with Inf and -Inf tests; (5) effective `grouped` and n-fold protocol string; (6) SCAD `lambda.min` and `dfmax` from p_eff; (7) Fan & Li §4.3 Table 1 cited for γ = 3.7, and the Breheny & Huang §4.3 wording corrected.
