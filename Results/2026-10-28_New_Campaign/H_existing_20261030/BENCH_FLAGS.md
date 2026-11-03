# Benchmark flags for the audit team (HQ launches; not launched here)

**Question:** where a benchmark performs poorly, is the fault ours (the implementation or the rule) or the method's?

**Evidence used:** the scored outputs (`tables/`) and the existing G5 verification reports. Nothing was refit. The counts alone do not diagnose a defect. Every stated cause is a hypothesis.

**Priority:** 1 = audit, 2 = audit is worthwhile, 3 = a quick confirmation is enough.

## Flag 1 (priority 1): F3 adaptive lasso, tuning and implementation

**Observed:**
- `cv_min`: 0/2,400 exact at both scales and both p, including scenario 1 (independent design) at c = 1.
- `cv_1se`: 9/600 at p500, c = 1; 0 elsewhere.
- Mean FP under `cv_min`:

  | | p500 | p1000 |
  |---|---|---|
  | c = 1 | 30 | 46 |
  | c = 0.5 | 54 | 78 |

- Its EBIC rules also trail SCAD's:

  | p, c = 1 | adaptive lasso `ebic1` | SCAD `ebic1` |
  |---|---|---|
  | 500 | 247/600 | 454/600 |
  | 1000 | 96/600 | 417/600 |

**Why audit:** the CV-min over-selection, together with the weaker EBIC recovery, motivates a tuning and implementation audit. These counts alone do not diagnose a defect.

**What G5 already covers:** G5 is PARTIAL because the original non-primary coefficient vectors are unavailable. Already checked and passed:
- all-case rule, weight and CV arithmetic (including the ridge choice and the weights);
- sampled primary coefficient checks;
- at c = 0.5, the sampled non-primary supports.

Sources: `BS/verify/G5_freq/REPORT.md` and `BS/verify/G5_freq/c050/REPORT.md`, where BS = `02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019`.

**Further probes of tuning and fold handling:**
- whether CV folds re-estimate the initial estimator and weights;
- glmnet `penalty.factor` scaling and convergence (`maxit`, `thresh`);
- the λ-grid end points;
- the weight power and the handling of zero initial coefficients.

## Flag 2 (priority 2): F5 ABESS (splicing heuristic), search quality

**Observed:**

| | p500 | p1000 |
|---|---|---|
| c = 1 (`ebic1`) | 365/600 | 323/600 |
| c = 0.5 (`ebic1_K37`) | 256/600 | 214/600 |

- Scenario 4 at c = 1: 26/100 and 24/100.
- At c = 1, most errors are "truth + extras".

**Direct evidence (G5 check 4 FAIL):** an independent same-size search finds a lower-RSS subset than ABESS's selected support:
- for 7 of 48 sampled primary `ebic1` selections at c = 1;
- at c = 0.5, for 109 of 168 sampled selected-rule rows, and 9 of 24 for the `ebic1_K37` primary. The largest relative RSS gain over those c = 0.5 rows is 0.49.

A lower-RSS same-size subset does not establish improved truth recovery.

**What to check:** the splicing settings (`support.size` range, `c.max`, `tune.type`), warm starts and screening, and whether the package default or our wrapper limits the search.

## Flag 3 (priority 3): F1 lasso and F2 elastic net, CV rules

**Observed:** 0/2,400 exact under each CV rule.
- Every `cv_min` selection adds false positives. Some also omit true variables:
  - F1 has 1, 47 and 68 mixed-error fits at p500 c = 1, p500 c = 0.5 and p1000 c = 0.5;
  - F2 has 1, 46 and 67.
- Pooled mean FP is about 53–80 under `cv_min` and 24–40 under `cv_1se`.
- Their EBIC-K37 companions recover 50–111/600 at c = 1 and 10–24/600 at c = 0.5.

**Hypothesis:** prediction-tuned (CV) penalties over-select; that is rule behaviour, not a defect. The cause is not established.

**What G5 already covers:** all-case CV arithmetic at the primary point passes.

**Quick confirmation:** on a few datasets, check that the `cv_min` λ equals `lambda.min` from an independent `cv.glmnet` call with the same folds.

## Watch list (no audit proposed; cause not established)

- **SSL-RS (supplementary arm), c = 0.5:** 32/600 at both p, against 593 and 592 at c = 1.
  - Most pooled misses omit variables: 499 and 497 are strict subsets of the truth. 69 and 71 also add false positives.
  - In scenario 1: recovery is 10/100 at each p; all 90 misses are strict subsets of the truth (mean FP 0; mean FN 2.61 and 3.55).
  - Hypothesis: its ladder runs λ0 up to p, where the primary SSL ladder stops at n, so weak signals are shrunk harder.
  - A2 SSL on the primary ladder gets 303/600 and 255/600.
- **Horseshoe `ci95`, c = 0.5, scenario 4:** 0/100 at both p.
  - Misses omit variables (mean FN about 4.6).
  - PREREG R7 states that `ci95` under-selects at weak signals by construction.
  - G5 passes.
- **SuSiE `pip05`, c = 0.5, scenario 5:** 3/100 (p500) and 0/100 (p1000).
  - Misses omit variables (mean FN 5.4 and 8.6).
  - L = 50 exceeds the truth size of 14, but that does not diagnose the cause.
  - SuSiE-refine gets 6 and 3. G5 passes.
- **MCP `ebic1` at c = 1** (235/600 at p1000):
  - The c = 0.5 fidelity audit (`BS/verify/fidelity_c050/`) found an EBIC false minimum near the size cap.
  - The pre-registered K = 37 rule gives 386/600 there; at c = 1 that row is post hoc.
