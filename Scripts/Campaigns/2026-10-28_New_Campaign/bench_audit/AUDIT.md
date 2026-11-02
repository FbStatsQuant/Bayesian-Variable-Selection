# BENCH-AUDIT: is the poor benchmark performance our fault or the method's? (v2.1, 2026-10-30)

**Team.**
- Manager: Opus 5.5 (BENCH-AUDIT thread).
- Workers:
  - W1, Terra 6.1: lasso/EN CV.
  - W2, Sonnet 5.5: adaptive lasso.
  - W3, Terra 6.1: F1–F3 provenance chain.
  - W4, Terra 6.1: adaptive-lasso pilot, 90 datasets.
  - W5, Sonnet 5.5: ABESS.
  - W6, Terra 6.1: F5 provenance chain.
- Checking: every worker result was re-checked by a different worker or by the manager's own code (`mgr_checks/`).
- Review: Sol 6.1, `review/SOL_REVIEW_1.md`. v2 answers it point by point (§7).

**Scope.** Local only. Nothing on NOTS was touched, and no published number is changed here.
**What was audited.** F1 lasso, F2 elastic net, F3 adaptive lasso and F5 ABESS, at p ≫ n (n = 200, p ∈ {500, 1000}, S1–S6, c ∈ {1, 0.5}). F4 MCP/SCAD and A1–A3 were not audited.

## Verdict (read this first)

**Is 0/600 normal for the CV rules, or our bug? Under the registered configuration it is what prediction-tuned CV does here. No implementation fault was found in the inspected code, runs or samples.**
- **Reproduction.** Our code re-fits the stored rows exactly on the sampled datasets: F1/F2 24/24 rule rows, F3 30/30. That is equal supports and λ, not a bit-level check of every coefficient. An independent plain `cv.glmnet` gives the same picture: 0/80 exact. An independent recount reproduces all 288 published F1–F3 cells.
- **The selected sets contain the truth.** At p500, c = 1, the `cv_1se` set contains all 14 true variables in 598/600 datasets for both F1 and F2. It also adds noise variables: 5–103 for F1 (median 23) and 7–109 for F2 (median 31.5). The 2 other datasets add extras and miss one true variable. At c = 0.5 more fits also miss true variables (47–68 mixed-error fits per cell, BENCH_FLAGS).
- **The true model is out of reach of the 1-SE rule.** In the 10 sampled S1/S2 datasets, the exact true model lies on the path in 5/10 (F1) and 3/10 (F2 at α*). There it sits at a λ 1.8–4.8 times λ_1se, where the CV error is 8–68 standard errors above its minimum.
  - Prediction tuning chooses smaller λ than selection needs. This is consistent with Meinshausen & Bühlmann (2006) and Leng, Lin & Wahba (2006), both checked against their abstracts. Master §III.2 already flags CV-min over-selection.
- **Adaptive lasso CV.** F3 `cv_1se` is 9/600 at p500 c = 1 (3/4/0/0/1/1 by scenario), not 0. Its `cv_min` is 0/600.
- **D35 (EBIC as the lasso-family headline).** Finding no implementation fault meets D35's condition. The decision stays HQ's and is outcome-informed.

| Method | `cv_min` | `cv_1se` | `ebic1` (cap 100) | `ebic1_K37` |
|---|---|---|---|---|
| F1 Lasso | ORGANIC* | ORGANIC* | ORGANIC* | ORGANIC* |
| F2 Elastic net | ORGANIC*; α-grid edge unresolved | same | same | same |
| F3 Adaptive lasso | ORGANIC* (either pilot) | ORGANIC* (either pilot) | CONFIGURATION CHOICE: ridge pilot | CONFIGURATION CHOICE: ridge pilot |
| F5 ABESS | — | — | METHOD (splicing returns suboptimal supports) + RULE (cap-100 EBIC false minimum, p1000 S1) | METHOD (splicing returns suboptimal supports) |

\*ORGANIC means method behaviour under the registered configuration, observed in these data. Our code, runs and scoring were found faithful where inspected.
- **F2 α grid.** CV picks α* = 0.9, the top edge of the frozen grid {.1, .25, .5, .75, .9}, in 2,399/2,400 fits (`mgr_checks/f2_alpha_table.csv`). Whether a wider grid would change F2's EBIC rows is untested; it is disclosed, not ruled out.
- **F3.** The ridge pilot is a defensible reading of Zou (2006), but at p ≫ n it weights the variables poorly. The exact recommended replacement, F1's own `cv_min` lasso fit as pilot (Zhou, van de Geer & Bühlmann 2009, §2.1 and Remark 2.4), raises EBIC-K37 recovery. These are production replicates S1–S6 r011–r015 (30 datasets per cell), which were not used in the earlier exploration; they are not the study's sealed `holdout/` set:

  | Cell | ridge pilot (stored) | lasso pilot (F1 `cv_min`) |
  |---|---|---|
  | p500, c = 1 | 13 | **23** |
  | p1000, c = 1 | 8 | **23** |
  | p500, c = 0.5 | 2 | **13** |
  | p1000, c = 0.5 | 0 | **9** |
- **F5.** In S4 the true model has a lower RSS than ABESS's size-14 support in 71/100 (p500) and 70/100 (p1000) datasets at c = 1. Tested settings did not remove these failures, though some improved recovery a little. A single-swap polish of sizes 10–20 removes most of them in S4, and does not help S1. That is the method, not us.

### Actions and costs (HQ decides; costs are provisional planning estimates in core-hours)

| # | Method | Action | NOTS rerun | Cost |
|---|---|---|---|---|
| 1 | F1, F2 CV rules | Keep + disclose (cell-specific numbers above) | none | 0 |
| 2 | F2 | Add the per-cell α* distribution and `alpha_edge` rate (PREREG R3) to the headline tables, at both scales and both regimes | none | analysis only |
| 3 | F3 | Fix: lasso pilot = F1's `cv_min` fit, with full contract and tests (§3); ridge rows kept as a labelled sensitivity; validate on dev data, then Sol review, then pilot, then rerun | F3 × p ∈ {500, 1000} × c ∈ {1, 0.5} = 2,400 fits | ≈ 75–90 core-h (first stage ≈ F1's 73 core-h; second stage measured locally ≈ 2 s/case); replace by the pilot's measured cost |
| 4 | F5 | Keep + disclose the search failures; optional companion "ABESS + swap polish" registered separately | none (local) | to be costed once specified (§4) |
| 5 | F4, F5 | Pre-register `ebic1_K37` as primary at both scales for any redeployment | none | 0 |
| 6 | F1–F5 | Redeployment evidence package (§5): every rule's coefficient vector, pilot/screen map, hashes, logs, independent tie-out | with any rerun | negligible storage |
| 7 | Low p | The PROD-L benchmark arm waits as a whole, under D36.2 and D36.4 (§6). The F3 fix goes into `code/bench_lowp/` too; the F5 low-p exact check needs new code (§4) | — | sizing pilot rerun if the F3 cost changes (D36.3) |

## 1. Lasso (F1) and elastic net (F2): the whole chain

| Link | What was done, by whom, when | Faithful? | Evidence |
|---|---|---|---|
| Spec | Master §III.3.1–3.2, written 2026-10-19 by two Opus agents + Astra and reviewed by Fable. PREREG_c050 (2026-10-21) fixed `cv_min` as primary, with `cv_1se` and EBIC as companions and the K37 bound | FAITHFUL WITH DISCLOSED DEPARTURE | `cv_min` was pre-declared, and Fable kept it (FABLE_JUDGE Q2). Master §III.3.1 a (l.~1075) and §III.2 (l.899, citing Hazimeh & Mazumder 2020 §5.3.1) say that CV-min over-selects. F2's α grid is narrower than Zou–Hastie's λ₂ grid; it is frozen and disclosed under PREREG R3, but the headline tables omit that disclosure (§2) |
| Code | Opus 5.5 threads F1 and F2, 2026-10-19. Each had two Sol reviews and an Astra production consult (`methods_dev/F*/LEDGER_ENTRY.md`) | FAITHFUL | The deployed NOTS copy, the laptop copy and the c050 copy are identical (5 files each). Runner tree hashes F1 `ad995a78…` and F2 `669bd70e…` equal the stored `source_sha256` (W3 `work_chain/tree_hashes.csv`) |
| Run | c = 1: F1 job 2282261 (2026-10-19 23:08Z), F2 2280939 (22:32Z). c = 0.5: F1 2332157, F2 2329049 (2026-10-21) | FAITHFUL | R 4.5.2 and glmnet 5.1 from the sealed library. 1,200/1,200 cases per run; all rule rows ok, 0 failed. Seed = data seed + 4,000,000. Folds and inputs match the manifests, 1,200/1,200 (W3) |
| Outputs | Stored rule rows and full-data path tables | FAITHFUL where sampled; evidence gap | Rule supports equal the path keys at the stored CV indices and the EBIC argmin (W3: 108/108 sampled checks, sidecars 72/72). Local re-fit with our code under glmnet 4.1.10: 24/24 rule rows identical, λ within 1.4e-15 (`mgr_checks/repro_f1f2.R`). Gap: non-primary coefficient vectors were not saved, so G5 is PARTIAL |
| Scoring | Thread S (Opus 5.5), 2026-10-19/21; ANALYSIS-H 2026-10-30 | FAITHFUL | Independent recount from the RDS files and the truth manifest: 288/288 published cells agree (W3). W1's pooled recount and the manager's F3 recount agree. Sol re-ran the F3 recount |

**CV step, item by item** (W1 `work_cv/REPORT_W1.md` §3; file:line under `methods_dev/`):
- **Folds.** The common 10 folds, 20 rows each, are all used (`F1_Lasso/methods/glmnet_helpers.R:61,66`). Stored folds equal the inputs in 20/20.
- **λ grid.** 200 points, ratio 1e-4, entry 1.01·max|X'y|/n (÷α for EN) (`F1_Lasso/config.R:32`, `fit_F1_lasso.R:36`, `F2_ElasticNet/methods/fit_F2_enet.R:70`).
  - No `dfmax`/`pmax` truncation; a short path fails the fit (`glmnet_helpers.R:28`).
  - The stored paths are complete for the 10 sampled datasets.
- **Standardisation.** None inside glmnet; X arrives centred with sd 1, which is checked (`common.R:9`). Independent refits with glmnet's default standardisation behave the same.
- **EN α.** Cross-validated over the 5-point grid jointly with λ; ties go to the larger α, then the larger λ (`fit_F2_enet.R:17-21,69`). α* = 0.9 in 2,399/2,400 fits.
- **`lambda.1se`.** glmnet's getOptcv rule on a decreasing grid (`glmnet_helpers.R:78-82`). `cv.glmnet` on the same grid reproduces our λ_min and λ_1se to 1e-14 (W2 a2; Sol, S1_r001 and S2_r001).
- **Zero threshold.** Exactly nonzero (`config.R:21`).
- **Edge cases.**
  - Size-0 selections are encoded as the empty key.
  - Flat or monotone CV curves pick the first minimum and get informational codes.
  - Non-finite summaries fail the fit.
  - All 28,800 rule rows of the 6 runs are `ok` (W3).

**Is `cv_1se` = 0/100 in the easy S1 cell plausible?** Yes, for these data. Where the truth is on the path, it lies 2–5× above λ_1se and at least 8 SE above the CV minimum (W1 §4). The 1-SE rule lowers F1's median FP from 51 to 23, never to 0. EBIC on the same path recovers 67/100 in S1.

**Recommendation F1/F2: keep as is and disclose** (cost 0). Add the α disclosure (§2).

**Low-p impact.** The low-p method files are byte-identical (`code/bench_lowp/R/methods/fit_F1_lasso.R`, `fit_F2_enet.R` and helpers; `diff -q` by the manager, hashes by Sol). No code fault carries over. CV over-selection may also occur at p ≤ 30; this audit did not evaluate it. The same α disclosure applies to low-p reporting.

## 2. F2 reporting gap (not a fit fault)

PREREG R3 requires the α* distribution and the `alpha_edge` rate per cell beside every F2 table. `HEADLINE_H.md` omits them (W3 link 1).

| Cell | α* = 0.9 / `alpha_edge` | Other α* |
|---|---|---|
| All 24 (p × c × scenario) cells except one | 100/100 | — |
| p500, c = 0.5, S4 | 99/100 | one α* = 0.5 |

- **Source:** `mgr_checks/f2_alpha_table.csv`.
- **Fix:** add this per-cell table to the headline tables, and to the low-p reporting when it exists. No rerun.
- **Test that would have caught it:** a render check that every PREREG R-item with a "report beside" clause has a matching table column.

## 3. Adaptive lasso (F3)

### Chain
- **Spec** (master §III.3.3 a, l.~1308): "data-driven weights from a ridge pilot (Zou 2006, γ = 1). Ridge, not OLS, supplies the pilot because OLS does not exist at p > n."
  - FA-F3 (2026-10-21) judged it FAITHFUL WITH DEPARTURES.
  - Zou suggests a ridge pilot under collinearity.
  - Zou tuned γ ∈ {.5, 1, 2}; that attribution fix is pending.
  - Pilot weights are not re-estimated inside the λ-CV folds (documented, O7).
- **Code:** tree hash `320936a7…` equals the stored rows (W3).
- **Run:** jobs 2279914 (c = 1, submitted 2026-10-19 22:19Z; 21:57Z is the snapshot/run-ID time) and 2329050 (c = 0.5). 1,200/1,200 ok per run.
- **Outputs:** our code re-fits the stored rows exactly, 30/30 (W2 Task 1). Penalty-factor scaling is a no-op, as intended.
- **Scoring:** p500 c = 1 gives 9/600 `cv_1se` and 247/600 `ebic1`, confirmed by W3, the manager and Sol.

### CV rules: organic under either pilot
- **Independent minimal aLasso** (ridge `cv.glmnet` + `penalty.factor`): 0/10 exact at both λ_min and λ_1se (W2 Task 2).
- **Pilot variants** (lasso, marginal, γ = 0.5 or 2, nested weights): 0/14 at `cv_min` and at most 1/14 at `cv_1se` (W2 Task 3).
- **Exact recommended pilot:** 0/30 at `cv_min` and 0–1/30 at `cv_1se` in all four cells (table below).

### EBIC rules: configuration choice (the ridge pilot)
- **Ridge weights rank the true variables poorly.** On average only 11.2 of the 14 true variables are among the 14 smallest weights. Between 5 and 134 noise variables have a smaller weight than the weakest true variable (W2 Task 4).
- **Exact recommended pilot, on production replicates S1–S6 r011–r015** (not used in the earlier exploration; not the sealed holdout). The pilot is the stored F1 `cv_min` coefficient vector (study grid, thresh 1e-16, glmnet 5.1). The second stage runs through the study's own glmnet engine (thresh 1e-16, maxit 1e7; locally glmnet 4.1.10 with the documented argument override). Evidence: `mgr_checks/exact_pilot/` (script, per-case CSV, summary).

  | Cell (30 each) | EBIC-K37 exact: ridge → lasso pilot | paired: only lasso / only ridge | truth inside the pilot set | truth on the 2nd-stage path | KKT failures |
  |---|---|---|---|---|---|
  | p500, c = 1 | 13 → **23** | 13 / 3 | 30 | 29 | 0 |
  | p1000, c = 1 | 8 → **23** | 16 / 1 | 30 | 30 | 0 |
  | p500, c = 0.5 | 2 → **13** | 11 / 0 | 27 | 14 | 0 |
  | p1000, c = 0.5 | 0 → **9** | 9 / 0 | 27 | 11 | 0 |

  - **Pilot set size:** 35–163 variables.
  - **Second-stage cost:** about 2 s per case locally.
  - **Sample vs published ridge rates:** the stored ridge rates in this sample are 43%, 27%, 7% and 0%. The published rates are 41%, 16%, 6% and 2% (247, 96, 36 and 12 of 600).
  - **Comparison with SCAD (descriptive only):** with the lasso pilot, c = 1 recovery is 77% on 30-dataset samples, against SCAD's published 76% on 600. The samples are unequal, so this is not evidence of equivalence.
  - **Literature claim, kept narrow:** ZvB support a lasso first stage. They do not establish F1's prediction-CV choice of the pilot λ as their theoretical tuning.
- **Exploratory runs agree.** W4, with default-grid `cv.glmnet` pilots (labelled exploratory per Sol finding 1), got 22, 23 and 13 of 30. The manager's corrected 14-dataset run got 12/14 vs 8/14.
- **A W2 error was caught here.** W2's first lasso-pilot run used the screened set size instead of p in log C(p, k) (`work_f3/scripts/lib.R:15-26`), which gave 0/14. It was withdrawn.
- **Why this is a configuration choice and not a bug.** The spec's reason for ridge rules out OLS but does not choose ridge over a lasso pilot. The code does what the spec says. The high-dimensional two-stage adaptive lasso uses the lasso as its first stage. Zhou, van de Geer & Bühlmann 2009 was checked in full text (`mgr_checks/zvb2009_p1-8.txt`): §2.1 eq. 2.1 sets w_j = max{1/|β_init,j|, 1}, notes Zou's 1/|β_init,j|^γ with "γ = 1 the most common choice", and Remark 2.4 and §§3–6 "consider the Lasso as initial estimator".

### Recommendation F3: fix the pilot, validate, then rerun F3 only

**Exact change** (one change, applied to `methods_dev/F3_AdaptiveLasso/methods/fit_F3_alasso.R` and `code/bench_lowp/R/methods/fit_F3_alasso.R`; D36.1):
1. **Pilot.**
   - Replace `ridge_cv` (l.36–56) and its use (l.89–95) with F1's engine at F1's registered settings: `glmnet_cv_engine(X, y, foldid, alpha = 1, lam = F1 grid, pf = rep(1, p), G = GLMNET)`, then `cv_choose()["min"]`. b = the full-data coefficients at that index.
   - This is the same computation F1 stores as `beta`. A test must show they are bit-identical in the same environment.
   - If the pilot fails (jerr, KKT at the pilot point, non-finite values), the whole fit fails. It never becomes a successful null fit.
2. **Screen and weights.**
   - keep = {j : b_j ≠ 0}, m = |keep|.
   - Weights w_j = 1/|b_j| (Zou, γ = 1) on keep; this is the form that was tested.
   - ZvB's max{1/|b_j|, 1} floor is not adopted; this is declared in the master. The old ε floor is removed; it is unnecessary because b_j ≠ 0 on keep.
   - Normalise stably: r = w/max(w), then v = m·r/Σr. glmnet rescales the factors to sum to the number of columns, so this changes nothing in the fit.
  - Assert that every v is finite and strictly positive, and that Σv = m within tolerance.
  - An unrepresentable reciprocal, or an underflowed factor, fails the fit. Such values are never silently floored or dropped (Sol R2-1; e.g. b = (1e-308, 1e-308) makes the naive m·w/Σw NaN).
3. **Second stage.**
   - Fit on `X[, keep, drop = FALSE]` and map the indices back.
   - The λ entry and grid are built over keep (`1.01·max_j |X_j'y|/(n v_j)·frac`). CV runs on the common folds. Full-data weights are used in the folds (O7, disclosed); nesting the new pilot is not validated.
   - **m = 0 (a genuine empty pilot, not a failed one).** Every registered rule row returns status ok with code `pilot_null`:
     - support "" and k = 0;
     - β = the zero p-vector, predictions 0, and RSS = Σy²;
     - λ, index and path fields set to the declared sentinels: NA, plus a one-row path table for the null model;
     - candidate table = the null model only.
   - **m = 1.** glmnet needs at least 2 columns, so use a closed-form one-variable path on the same objective and grid.
     - The estimate is β(λ) = S(x'y/n, λ·v)/(x'x/n), with S the soft-threshold, where n and x'x come from the data being fitted: n and x'x on the full data, n_train and x_train'x_train in each training fold.
     - CV and the rule code are the same as for m ≥ 2. Code `pilot_single`.
     - Test both CV choices against an independent scalar solution.
4. **EBIC.** Candidates are the null model plus the distinct mapped supports with k ≤ 37 (primary, K37) and k ≤ 100 (secondary). The penalty uses **p = ncol(X)** in log C(p, k). OLS rank and RSS validity and the deterministic tie order (`order(crit, k, key)`) are unchanged.
5. **Schema.**
   - **Rule IDs and roles:**
     - `cv_min`, primary;
     - `cv_1se`, `ebic1` and `ebic05`, S0 (cap 100);
     - `ebic1_K37` and `ebic05_K37`, companions (K37 primary among the EBIC rules).
   - **Retire the ridge-only items:** the fields `kappa`, `ridge`, `ridge_resid_max`, `ridge_fold_mse`, `kappa_min`, `kappa_index`, `kappa_boundary`, `eps_floor` and `n_floored`, and the codes `kappa_edge` and `floored_selected`.
   - **Add:** `pilot_k`, `pilot_index`, `pilot_lambda`, `pilot_beta` and the screen map `keep`, plus the codes `pilot_null` and `pilot_single` in the closed vocabulary.
   - **Update every consumer:** validators, scoring, `derive_rules.R`, and the low-p runner.
   - **Coefficient provenance:**
     - each CV rule saves the penalised coefficient vector at its λ index;
     - each EBIC rule saves the penalised vector at the first (largest-λ) KKT-passing path occurrence of its support, plus its OLS-refit slopes, labelled separately.
   - Update `config.R`, the registry metadata and the master §III.3.3 (lasso pilot, citations, Zou's tuned γ). The ridge rows stay published as "F3-ridge (first deployment), sensitivity".

**Tests** (negative controls included; the truth-based items are diagnostics, not proofs):
- **Pilot identity.** Pilot = F1 `cv_min` β bit for bit on the 12 dev datasets.
- **Pilot failure.** A failed pilot propagates to a failed fit.
- **Edge sizes.** m = 0 and m = 1 fixtures.
- **Weight extremes.** Extreme weights, e.g. |b| near 1e-12.
- **Index mapping.** Screened-to-original mapping on a permuted-column fixture.
- **Full-p EBIC.** Full-p EBIC against a hand computation; this is the class of W2's slip.
- **OLS rank deficiency.** Rank-deficient OLS candidates are rejected.
- **Tie order.** Deterministic EBIC ties.
- **KKT.** Selected-point KKT on the screened problem.
- **Rule consistency.** Every rule's support equals the nonzeros of its saved coefficient vector.
- **Weight-normalisation stability.** Overflow of Σw, and underflowed factors, must fail the fit cleanly.
- **RSS validity.** Non-positive or non-finite RSS candidates score Inf.
- **Second-stage KKT failure.** A KKT failure at a selected point fails that rule.
- **Pre-implementation status.** These are specifications. None of these failures occurred in the 120 ordinary cases, where m = 35–163, so the m < 2 branches remain untested.
- **Low-p fixtures.** The same fixtures at p = 20 and 30.
- **Diagnostics.**
  - Truth on the second-stage path in the p500, c = 1 cell (pooled S1–S6): ridge 13/30 (W4), lasso pilot 29/30.
  - The rank of the true variables among the weights.

**Validation before any rerun** (Sol finding 1):
- Run the frozen wrapper on separate dev data at both p, both c and both low-p values.
- Record measured time per fit.
- Get a Sol review to ACCEPT.

**Cells to rerun:** F3 × p ∈ {500, 1000} × c ∈ {1, 0.5} = 2,400 fits, on the same datasets. Nothing else.

**Cost (provisional):**
- The first stage equals F1's cost at thresh 1e-16: 27.9 + 45.3 = 73.2 core-h, from the 2,400 stored F1 runtimes (Sol: 73.2).
- The second stage measured about 2 s per case locally, so roughly 2–4 core-h on NOTS.
- Total ≈ 75–90 core-h, plus a dev pilot under 2 core-h. These are core-hours; elapsed time depends on the array width.
- The alternative that reads F1's stored β (≈ 5 core-h) would need hash, fold, config and status binding to F1's files, and is not recommended.
- Replace these numbers with the pilot's measured cost.

**Caveat for HQ.** The change is informed by outcomes. It is defensible because it follows the high-dimensional adaptive-lasso literature, the ridge rows remain published as a labelled sensitivity, and the CV-rule verdict does not depend on it. HQ decides.

**Low-p impact.**
- The low-p F3 is byte-identical and keeps the ridge pilot (`code/bench_lowp/ADAPTATIONS.md`: "F3 ridge pilot … unchanged").
- At p ≤ 30 < n the master's reason for ridge disappears, and Zou's own default would be OLS.
- The p ≫ n gain is not evidence that the lasso pilot helps at low p. One code tree (D19) means the same fix goes in, with an OLS pilot as a registered low-p sensitivity.
- The low-p fixtures above are required. The low-p cost must be measured in the sizing pilot (D36.3).
- **Possible future work (HQ D54.2, 2026-10-30):** the OLS-pilot low-p sensitivity is out of D42's scope and is not implemented.

## 4. ABESS (F5)

### Chain
| Link | What was done, by whom, when | Faithful? | Evidence (W6 `work_chain_f5/REPORT_W6.md` unless noted) |
|---|---|---|---|
| Spec | Master §III.3.5 (2026-10-19). PREREG_c050 made K37 the primary at c = 0.5 and added `sic_smax` as an S0 row; K37 at c = 1 is labelled post hoc | FAITHFUL WITH DISCLOSED DEPARTURE | `M:1482-1486,1548-1557`. The fidelity audit notes that the authors' own SIC tuning, with its size limit of 19/17, differs from our external EBIC over 0:100 (`fidelity_c050/F5_ABESS/REPORT.md:5-30`); this is disclosed |
| Code | Opus 5.5 F5 thread, 2026-10-19; Sol and Astra reviews (`methods_dev/F5_ABESS/LEDGER_ENTRY.md:9-29`) | FAITHFUL | The 4 tree files are identical across the laptop, deployed and c050 copies. The tree hash `efb11718…` equals the stored rows in 18/18 sampled cases. `run_task.R` differs at c050 only in the array mapping and the scale argument |
| Run | c = 1 array 2278613 (2026-10-19 21:57Z); c = 0.5 2331188 (2026-10-21 16:04Z), 400/400 | FAITHFUL | abess 0.4.11 (pinned DESCRIPTION, built 2026-10-19), R 4.5.2. 1,200 cases per scale; 3,600/3,600 rule rows ok per scale. Seed, fold and input hashes match the manifest 1,200/1,200. No production retry was found |
| Outputs | Stored paths and candidate tables | FAITHFUL for the EBIC argmin and sidecars. The search limitation is known | Rule support = candidate argmin 36/36; sidecars 24/24. G5 had already found same-size lower-RSS subsets: 2,560/4,848 sampled c = 1 path supports and 1,477/2,424 at c = 0.5. W6 labels this "DEFECT (independent search)". This audit classes it as method behaviour (below) |
| Scoring | Thread S and ANALYSIS-H | FAITHFUL | Independent recount: 96/96 cells agree (`ebic1`, `ebic05`, `bic`, `ebic1_K37`; both p, both c). Consistent with the manager's S1/S4 recount and Sol's |

- **Spec** (master §III.3.5 a–c, l.1482 ff.). It states that splicing "is not certified even against all two-variable swaps" and has "no global certificate". Our departures from the package defaults all widen the search:

  | Setting | Ours | Package default |
  |---|---|---|
  | `support.size` | 0:100 | 0:19 |
  | `important.search` | p | 128 |
  | `max.splicing.iter` | 100 | 20 |

  `c.max` = 2 and `splicing.type` = 2 are the defaults the authors ask users to keep (abess 0.4.11 help, `work_abess/abess_help.txt`).
- **Reproduction.** Our call and our wrapper reproduce the stored path exactly: 0 mismatches over 101 sizes on each of 5 datasets (W5 Task 1).
- **Recount.** At c = 1, stored `ebic1` exact is 66 / 40 / 26 / 24 (p500 S1, p1000 S1, p500 S4, p1000 S4), recomputed by W5, by the manager (`mgr_checks/spot_abess.R`) and by Sol.

### Diagnosis: the method returns suboptimal supports (c = 1; mainly S1 and S4 were tested)
- **S4 search failures.** In S4 (within-block correlation 0.85), ABESS's size-14 support equals the truth in 28/100 (p500) and 29/100 (p1000) datasets. In 71/100 and 70/100, the true model has a lower OLS RSS than the support ABESS returns at size 14. The search returned a suboptimal support, and a lower RSS proves that. Whether those supports are local optima is not claimed: single swaps improve many of them.
- **Search and criterion effects coexist.** In 8 (p500) and 7 (p1000) of the S4 misses, the pick also has a lower EBIC than the truth (W5 class A2).
- **Settings.** The tested settings did not eliminate the sampled failures; some improved recovery a little.
  - p500 S4, 20 datasets: `warm.start = FALSE` gave 5 → 7/20; `c.max` 5/10/20 and `splicing.type` 1 stayed at 5/20.
  - p1000 S4, 10 datasets: package defaults gave 2 → 4/10.
  - Source: `work_abess/task3_summary_by_group.csv`.
- **Polish.** W5's `05_polish_all.R` refits ABESS with sizes 0:37, polishes sizes 10–20 only (best single swap, repeated while RSS decreases), then applies external EBIC over 0:37.
  - **S4:** 26 → 77/100 (p500) and 24 → 75/100 (p1000).
  - **S1:** 68 → 67/100 (p500) and 63 → 63/100 (p1000). The polish does not improve every cell.
  - **Independent check:** the manager's own polish at size 14 (`mgr_checks/spot_polish.R`) gives the truth in 19/20 S4 datasets at each p, against 5 and 6 for ABESS. In 1/20 at each p, the polished support beats the truth in RSS.
- **S1 misses are criterion misses.** In S1 the size-14 support is the truth 100/100, so every miss comes from the EBIC choice. Under the cap-100 rule (the c = 1 primary), p1000 S1 recovers 40/100, against 63/100 under K37. This is the cap-100 false minimum seen earlier for MCP. K37 is a disclosed prospective rule choice, not a search repair.
- **Untested.** c = 0.5 was not tested here; the earlier G5 check 4 found lower-RSS same-size subsets in 109/168 sampled c = 0.5 rows.

### Recommendation F5
- **Keep the frozen ABESS arm as is and disclose:** "splicing returns suboptimal supports: in S4 at c = 1 the true model has a lower RSS than ABESS's size-14 support in 71/100 (p500) and 70/100 (p1000)". Fable's ruling stands: polishing is not ABESS.
- **Optional companion "ABESS + swap polish"**, registered separately and never substituted:
  - **Algorithm, as W5 actually ran it** (`work_abess/scripts/lib.R:52–69`):
    1. Start from ABESS's size-k support for k = 10..20, with ABESS refit on sizes 0:37.
    2. Repeat the best single swap: accept the candidate if RSS_cand < RSS_best − 1e-9·max(1, RSS_best).
    3. Stop after at most 200 iterations.
    4. On ties, the first winner encountered in the numeric scan is kept; there is no support-key tie-break.
    5. Then apply EBIC-K37 over 0:37.
  - **Changes need their own validation.** Any change, such as a key tie-break or polishing every size, makes it a new prospective companion that must be validated separately.
  - **Transfer:** verify on the stored paths that polishing the stored supports gives the same result as W5's refit version.
  - **Cost:** run locally, timed on a sample before quoting a cost.
  - **Literature alternative:** L0Learn (coordinate descent with local swaps, Hazimeh & Mazumder 2020). Not tested here.
- **Rule:** pre-register `ebic1_K37` as the F4/F5 primary at both scales for any redeployment.
- **Low-p impact.**
  - `fit_F5_abess.R` is byte-identical in `code/bench_lowp/`.
  - **Exact reference does not exist yet.** The low-p enumeration does not save per-size OLS minima. It stores posterior Z/PIPs, size masses and a top-1000 by Bayesian score (`code/lowp/enum/lowp_enum.cpp:413–420`, `exact_contract.R`; Sol finding 4). An exact size-k check therefore needs new code. Either instrument the enumeration to accumulate the minimum RSS and its support per size, which is cheap inside the existing 2^p loop but changes frozen v2.2.1 code, or run a separate exact best-subset search per size: at p ≤ 30, a branch-and-bound or complete enumeration of OLS RSS.
  - **Comparison rules:** no intercept, the same preprocessing, rank checks, and comparison by RSS within a tolerance, allowing tied optimal supports.
  - **Cost:** to be measured. It is not "≈ 0".
  - **HQ D54.3 (2026-10-30): DEFERRED,** not a PROD-L gate; disclosed as a limitation in `code/bench_lowp/ADAPTATIONS.md`.

## 5. Redeployment evidence package (all benchmark bundles; D36.4)
- **Frozen code and manifest.** Frozen code with a sha256 manifest; the runner's `source_sha256` must be checked against it.
- **Saved per fit:**
  - every rule's full coefficient vector, with λ, index, support and status (this closes G5 PARTIAL);
  - the pilot, screen map and weights (F3), and the path/candidate tables;
  - seeds, folds and input hashes;
  - command, job ID, timestamps, exit status and logs.
- **Before release:**
  - local tests, including the negative controls in §3;
  - a Sol review to ACCEPT;
  - a pilot before scale;
  - an independent table tie-out (a recount from the RDS files and the truth manifest, as W3 did);
  - full reconciliation: expected = observed cases, with no silent drops.
- Do not rerun existing fits only to strengthen this audit's claims.

## 6. PROD-L gate (corrected per Sol finding 2)
- **No partial release.** Under D36.2, PROD-L's **benchmark arm waits as a whole** for BENCH-AUDIT's verdict and fixes. Its enumeration and SMC arms do not wait. This audit authorises no benchmark release.
- **Gate conditions:**
  - the F3 fix implemented in both trees, tested and Sol-ACCEPTed;
  - the F2 α disclosure added to the low-p reporting;
  - the F5 low-p exact check implemented, or explicitly deferred by HQ;
  - the D36.4 items for the low-p bundle;
  - the benchmark sizing step rerun if F3's cost changes materially (D36.3).
- **Not covered:** F4 and A1–A3 were not part of this audit and are not certified by it.

## 7. Response to Sol review 1

| # | Sol finding | Resolution in v2 |
|---|---|---|
| 1 | BLOCKING: the tested pilot was not the recommended pilot | Re-tested with the exact pilot (stored F1 `cv_min` β, study engine), all four cells including p1000 c = 0.5 (§3 table). Exploratory results relabelled. ZvB full text checked. Validation of the frozen wrapper on dev data (both regimes) is required before any rerun |
| 2 | BLOCKING: partial PROD-L release | Replaced by the D36.2/D36.4 whole-arm gate (§6). F4 and A1–A3 are stated as not certified |
| 3 | SHOULD-FIX: F3 contract and tests | m = 0 / m = 1, failure propagation, floor policy, schema and vocabulary, and the full test list (§3) |
| 4 | SHOULD-FIX: low-p enumeration lacks per-size minima | §4 low-p: new code required, two options, tolerance rules, cost to be measured |
| 5 | SHOULD-FIX: ABESS overstatement | "Tested settings did not eliminate failures; some improved"; "suboptimal returned supports", not "local optimum"; exact polish algorithm; the S1 counter-case; c = 1, S1/S4 scope stated |
| 6 | SHOULD-FIX: scopes and verdict language | F1 FP 5–103 and F2 7–109; on path in 5/10 and 3/10; F3 `cv_1se` 9/600; ORGANIC qualified; α grid unresolved; per-cell α table (§2); low-p "may occur; not evaluated" |
| 7 | SHOULD-FIX: F5 chain and evidence checklist | W6 F5 chain (§4); §5 evidence package |
| 8 | MINOR: cost provisional | All costs labelled provisional; F3 re-estimated from the measured second stage; core-h distinguished from elapsed time |

### Sol review 2 (`review/SOL_REVIEW_2.md`): ACCEPT WITH FIXES, applied in v2.1

| # | Finding | Applied |
|---|---|---|
| R2-1 | SHOULD-FIX: unstable weight normalisation | Stable r = w/max(w) normalisation, assertions and fail-on-unrepresentable rule (§3, step 2); overflow and underflow fixtures added to the tests |
| R2-2 | SHOULD-FIX: edge and schema contract | Full m = 0 output; singleton full-data and fold denominators with an independent scalar check; rule IDs and roles; retired and added fields and codes; consumers; coefficient provenance; RSS and KKT negative controls (§3) |
| R2-3 | SHOULD-FIX: polish algorithm | The exact W5 algorithm is stated (relative 1e-9, cap 200, scan order, no key tie-break); any change is a new companion to be validated (§4) |
| R2-4 | MINOR: scope wording | Replicates relabelled as production replicates not used in the earlier exploration (not the sealed holdout); the SCAD comparison marked descriptive; the diagnostic cell named |
| R2-5 | MINOR: F3 job time | 22:19Z submission vs 21:57Z snapshot time |

Sol's own re-runs: 4 cases (one per cell), 12/12 case-rule records match. Pilot binding to `F1.rds$beta` was confirmed (local F1 re-fit β within 1.4e-14). An independent second stage gave identical paths. A screened-p negative control showed that the wrong p changes the EBIC picks. The aggregate tie-out reconciles. The v2.1 text edits were not re-reviewed.

## 8. Not checked
- glmnet 5.1 was not run locally (Windows has 4.1.10). The sampled local reproductions match the stored supports and λ; that is evidence, not proof, that the version does not matter.
- F4 MCP/SCAD and A1–A3 were not audited.
- ABESS at c = 0.5, and scenarios other than S1 and S4, were not re-diagnosed.
- The abess PNAS paper was not read.
- Literature checked: Meinshausen & Bühlmann 2006 and Leng, Lin & Wahba 2006 (abstracts and secondary summaries); Zhou, van de Geer & Bühlmann 2009 (full text, §§1–2).
