# Ten state-of-the-art benchmarks for variable selection

Independent literature review, 3 October 2026. It was done without using the earlier `Variable_Selection_Benchmarks_20261003` folder. No simulations were run.

## 1. Recommendation

| # | Benchmark (reference) | Paradigm | Primary implementation | Used as comparator in (of 108 papers read) | Citations (OpenAlex) |
|---|---|---|---|---|---|
| 1 | **Lasso** (Tibshirani 1996) | convex penalty | `glmnet` 5.1 | **44** (23 since 2023) | 53,106 |
| 2 | **Elastic net** (Zou & Hastie 2005) | convex penalty, correlation-aware | `glmnet` | 12 | 21,790 |
| 3 | **Adaptive lasso** (Zou 2006) | weighted convex penalty, oracle property | `glmnet` + ridge weights | 13 | 7,719 |
| 4 | **SCAD** (Fan & Li 2001), MCP from the same fit as a sensitivity | nonconvex penalty | `ncvreg` 3.16 | 17 (SCAD 14, MCP 11) | 9,288 (MCP 4,027) |
| 5 | **Best-subset / L0 via L0Learn** (Hazimeh & Mazumder 2020) | L0 subset search | `L0Learn` 2.1 (exact best subset as a check at p = 30) | 11 L0/best-subset, plus 16 stepwise | 148 (best subset via MIO: 683) |
| 6 | **Knockoff filter** (Barber & Candès 2015; Candès et al. 2018) | finite-sample FDR control | `knockoff` 0.3.6 / `knockpy` (MVR) | 12 (10 since 2023) | 575 + 676 |
| 7 | **Horseshoe** (Carvalho, Polson & Scott 2010) | continuous shrinkage prior | `horseshoe` / `bayesreg` 1.3 | 16 (horseshoe 14) | 1,451 |
| 8 | **Spike-and-slab LASSO** (Ročková & George 2018) | Bayesian penalized (posterior mode) | `SSLASSO` 1.2.3 | 9 (SSL 6, EMVS 3) | 359 |
| 9 | **SuSiE** (Wang, Sarkar, Carbonetto & Stephens 2020) | Bayesian sum of single effects (IBSS) | `susieR` 0.14.2 | 7 (**all** since 2023) | 1,249 |
| 10 | **BAS: g-prior BMA** (Clyde, Ghosh & Littman 2011; Liang et al. 2008) | point-mass spike-and-slab / BMA over model space | `BAS` 2.0.2 | 13 g-prior BMA (BAS 12) | 272 + 1,152 |

Six of the ten are frequentist and four Bayesian. Each slot is a distinct statistical procedure, so no two slots answer the same question. Bayesian evidence comes from the closed-form model score, so it is model-specific; it cannot be compared across these procedures.

**Not in the ten, but required for the SMC paper (see §5).** These are same-posterior computational controls, compared on PIP and evidence accuracy against exact enumeration at equal cost:

- a long-run single-site Gibbs / add-delete-swap MCMC;
- weighted tempered Gibbs (wTGS);
- Schäfer–Chopin binary SMC.

They answer "how well is *this* posterior computed?" rather than "how good is this selection procedure?". The ten cannot answer that question, and the samplers do not belong in a selection leaderboard: if they converge, their selections match the SMC's.

## 2. How the list was decided

**Reading.** Eight parallel reading passes each covered one part of the literature:

- A: neutral comparison studies
- B: Bayesian prior/variational methods
- C: model-space MCMC/SMC samplers
- D: correlated predictors and fine-mapping
- E: frequentist L0 and FDR-controlled methods
- F: shrinkage priors and selection rules
- G: BMA, g-priors and nonlocal priors
- H: 2025–2026 papers

Each pass opened the full text (PDF or HTML, saved in `sources/`), read the simulation or experiments section, and recorded the competitors *actually run*, with a location and a verbatim quote. Bibliographies and abstracts were not used as evidence.

**Corpus.** 110 unique papers after merging duplicates across passes; 108 were read in full text.

| Publication years | Papers |
|---|---|
| 2025–26 | 27 |
| 2023–24 | 27 |
| 2020–22 | 25 |
| 2016–19 | 16 |
| ≤ 2015 | 13 |

By type: 83 new-method papers, 16 neutral comparisons, 5 reviews, 4 software papers.

**Quality control.** I checked each verbatim quote against the saved sources (`quote_verification.txt`). 85 of 116 matched exactly after normalisation. The rest share long verbatim runs and differ only by PDF-extraction artifacts; I hand-checked the weakest seven. I also read the two most decision-relevant comparator tables myself (Porwal & Raftery 2022 Table 2; Kim et al. 2024 Table 1), and the two caveats that drive design choices below (Spector & Janson 2022 Thm 2.4; Wang et al. 2020 §6).

**Usage by method family** (`family_frequency.txt`). Here n is the number of papers that ran the method as a competitor. The Bayesian-paper count uses a keyword heuristic.

| Family | All | ≥2020 | ≥2023 | In Bayesian papers | In frequentist papers |
|---|---|---|---|---|---|
| Lasso (+ relaxed) | 44 | 33 | 23 | 22 | 22 |
| Model-space MCMC (Gibbs / SSVS / add-delete-swap / MC3) | 23 | 15 | 8 | 19 | 4 |
| Nonconvex (SCAD or MCP) | 17 | 10 | 5 | 9 | 8 |
| Horseshoe family | 16 | 11 | 7 | 14 | 2 |
| Forward / backward stepwise | 16 | 13 | 9 | 4 | 12 |
| g-prior BMA (BAS, BMS, bicreg) | 13 | 7 | 5 | 12 | 1 |
| Adaptive lasso | 13 | 10 | 7 | 6 | 7 |
| Knockoffs (fixed-X or model-X) | 12 | 11 | 10 | 1 | 11 |
| Elastic net | 12 | 11 | 7 | 7 | 5 |
| L0 / best subset (MIO, L0Learn, ABESS) | 11 | 10 | 6 | 1 | 10 |
| SSL / EMVS | 9 | 8 | 6 | 7 | 2 |
| Bayesian lasso | 8 | 4 | 4 | 7 | 1 |
| BH on OLS p-values | 8 | 6 | 5 | 0 | 8 |
| SuSiE | 7 | 7 | 7 | 6 | 1 |
| Adaptive / informed samplers (TGS, wTGS, ASI, LIT, HBS) | 7 | 6 | 3 | 6 | 1 |
| Variational spike-and-slab (varbvs, sparsevb) | 5 | 4 | 3 | 5 | 0 |
| Nonlocal priors (mombf etc.) | 4 | 3 | 1 | 3 | 1 |
| Stability selection | 3 | 3 | 3 | 0 | 3 |
| SMC (Schäfer–Chopin) | 1 | 1 | 0 | 1 | 0 |

**Judgement layered on the counts.** The counts were not used mechanically. Six rules shaped the final list:

1. **One slot per distinct paradigm.**
   - Stepwise selection is folded into the L0 slot; at p = 30, exact best subset dominates it.
   - MCP shares the SCAD slot, since one `ncvreg` call gives both.
2. **Same-posterior samplers move to the computational panel.** Model-space MCMC is the second most-used family, but statistically it estimates the same kind of posterior as BAS and the SMC. BAS represents it in the ten because its MCMC is itself an MC3 sampler.
3. **Recent-usage trajectory matters.**
   - SuSiE: every use is from 2023 or later.
   - Knockoffs: 10 of 12 uses since 2023.
   - SSL: the "state-of-the-art" label in several papers.
   - All three outrank older entries with similar raw counts (Bayesian lasso, stepwise).
4. **Neutral comparisons carry extra weight.** Porwal & Raftery (PNAS 2022) ran 21 methods and found three adaptive g-prior BMA methods performed best across all tasks (`BAS`, with the `MCMC` method). Sekulovski et al. (2025, logistic, preregistered) reached the same conclusion for BAS.
5. **Fit to the five scenarios and to the SMC's outputs.**
   - Correlation-aware methods (EN, SuSiE) and an FDR-controlling method (knockoffs) are kept because S3–S5 are correlation designs.
   - The SMC reports Bayesian-FDR selections, which need a frequentist error-control counterpart.
6. **Maintained software.** All ten have a CRAN package; nine were updated in 2023–2026, the exceptions being `knockoff` (2022) and `horseshoe` (2019), which has `bayesreg` (2024) as a maintained alternative. Details in `software_snapshot.json`.

## 3. Why each method, and how to run it without oracle information

Common rules for every method:

- Never give a method the true model size (k = 5), the true support, or the generating Σ.
- Use the same 10 CV folds per dataset for every CV-tuned method.
- Use one intercept/centring convention for all. The SMC uses centred and scaled X, uncentred y and no intercept; since X is centred and the truth has no intercept, this is easy to match.
- Report every tuning choice.

1. **Lasso.**
   - *Why:* The universal anchor. It was run in 44 of 108 papers: 13 of 16 neutral studies and 22 Bayesian papers.
   - *How:* `cv.glmnet`, alpha = 1. λ_min is the main arm; λ_1se and the relaxed lasso (`relax = TRUE`) are sensitivities. Hastie, Tibshirani & Tibshirani (2020) call the relaxed lasso the "overall winner".
   - *Watch for:* S4 likely violates the irrepresentable condition, so lasso selection is expected to degrade there.
2. **Elastic net.**
   - *Why:* The correlation-specific convex method. Hanke et al. (2024) found it beat lasso, forward stepwise and best subset under block and Toeplitz correlation. Bertsimas et al. (2020) found EN and SCAD dominate under high noise plus high correlation.
   - *How:* `cv.glmnet` with α ∈ {0.1, 0.25, 0.5, 0.75, 0.9}, tuned jointly with λ on the common folds.
   - *Watch for:* Its grouping effect will pull in block proxies. That is informative in S3–S5, not a bug.
3. **Adaptive lasso.**
   - *Why:* Run in 13 papers, including 6 neutral studies. Freijeiro-González et al. (2022) found it the only lasso derivative robust under both block and Toeplitz dependence.
   - *How:* `glmnet` with `penalty.factor` = 1/|β̂_ridge|. Ridge rather than OLS weights, because OLS is unstable at ρ = 0.85. Choose λ by CV; ideally re-estimate the weights inside folds.
4. **SCAD (MCP from the same call).**
   - *Why:* Nonconvex penalties are the third most-used family (17). SCAD is used more in Bayesian papers (9 vs 5) and is more cited.
   - *How:* `cv.ncvreg(penalty = "SCAD", gamma = 3.7)`, with `penalty = "MCP", gamma = 3` as a sensitivity. Keep convergence flags.
5. **Best-subset / L0 (L0Learn).**
   - *Why:* L0Learn is the L0 implementation other authors most often benchmark against: Hastie et al. 2020 (supplement), Moka et al. 2024 (COMBSS), Kim et al. 2024 (Mr.ASH) and Zhang, Bien & Taeb 2025. ABESS appears once.
   - *How:* `cv.L0Learn(penalty = "L0L2", algorithm = "CDPSI")`, tuned by CV over (λ, γ). The L0L2 penalty guards against the low-SNR overfitting reported for pure L0.
   - *Check at p = 30:* exact best subset is feasible (`leaps` branch-and-bound or L0BnB), so it gives a certified optimum, with size chosen by BIC.
6. **Knockoff filter.**
   - *Why:* The modern standard for selection with finite-sample FDR control. Every FDR-method paper in the corpus ran it, and it is the natural frequentist counterpart to the SMC's Bayesian-FDR rule.
   - *Which version:* Use fixed-X, which is valid because n = 100 ≥ 2p = 60. Model-X would need Σ, and that is oracle information here.
   - *Construction:* Use **MVR or ME** (Spector & Janson 2022, `knockpy`) as the main construction and the default SDP as a sensitivity. Their Thm 2.4: with SDP knockoffs on an equicorrelated design with ρ ≥ 0.5, the power of *every* permutation-invariant statistic → 0. This covers S3 and S4.
   - *Statistic:* Use one that respects fixed-X sufficiency, e.g. the lasso λ at entry (signed max). Do not use a CV-tuned statistic.
   - *Levels:* q ∈ {0.1, 0.2}, reporting both knockoff (offset 0, modified FDR) and knockoff+ (offset 1, FDR).
   - *Structural limit:* knockoff+ selects nothing unless at least ⌈1/q⌉ variables pass, i.e. 10 at q = 0.1 and 5 at q = 0.2. With 5 true signals it is close to powerless at q = 0.1. Report this as the price of the guarantee, not as a win for the SMC.
   - *Companion:* BH on the full-model OLS p-values is valid here because n > p, costs nothing, and is the standard low-dimensional FDR comparator.
7. **Horseshoe.**
   - *Why:* The most-used Bayesian comparator (16 papers; 14 of them Bayesian), including in Porwal & Raftery, Kollipara et al. 2026, the R2D2, Dirichlet–Laplace and l1-ball papers, and Das 2026.
   - *How:* `horseshoe::horseshoe` (Jeffreys σ², half-Cauchy τ), with `bayesreg(prior = "hs")` as the maintained alternative.
   - *Selection rule:* Two published rules. **Primary:** the 95% credible interval excludes 0; this is the rule in Porwal & Raftery and most of the corpus. **Secondary:** shrinkage factor 1 − κ̂ > 0.5 (`HS.var.select(method = "threshold")`), the analogue of PIP > 0.5.
   - *Watch for:* The interval rule is consistently reported as conservative under correlation (Piironen et al. 2020; Kowal 2022). Expect low power in S3–S5.
8. **Spike-and-slab LASSO.**
   - *Why:* The leading fast Bayesian selector. Ray & Szabó (2022) call it state of the art, and it was run by Porwal & Raftery, Kim et al., Kollipara et al., Liu & Ročková and Das.
   - *How:* `SSLASSO(penalty = "adaptive", variance = "unknown")` with the package's λ0 ladder (dynamic posterior exploration) and beta-binomial θ (a = 1, b = p). Selection = support at the end of the ladder.
   - *Mixed evidence:* SSL won its own ρ = 0.9 block design, but "sometimes very poorly" with correlated predictors in Kim et al. (that study measured prediction).
9. **SuSiE.**
   - *Why:* The fastest-rising Bayesian comparator (7 of 7 uses since 2023; 1,249 citations), built specifically for correlated predictors (S3–S5). It yields PIPs and credible sets, so it maps directly onto the SMC outputs.
   - *How:* `susie(L = 10, estimate_prior_variance = TRUE, estimate_residual_variance = TRUE, refine = TRUE)`. Use L = 10, not the oracle 5. Selection: PIP > 0.5 as the main arm, plus 95% credible sets (min purity 0.5) for block-level localisation.
   - *Key design interaction:* IBSS adds one effect at a time. Wang et al. (2020, §6) show it can stick in a poor local optimum when two effects cancel. Your opposing-sign pair (x2 = +1, x3 = −1, correlation 0.7/0.85) is that case. This is probably the most interesting head-to-head with a full model-space posterior.
10. **BAS g-prior BMA.**
    - *Why:* The best-performing family in the largest neutral Bayesian-vs-frequentist comparison (Porwal & Raftery 2022), confirmed by Sekulovski et al. (2025). It is the standard model-space package (Forte, García-Donato & Steel 2018) and was run in 12 papers.
    - *How (selection slot):* `bas.lm(prior = "hyper-g", modelprior = beta.binomial(1,1), method = "MCMC")`. Porwal & Raftery's top three were hyper-g, EB-local and g = √n. Use `method = "MCMC"`, **not** `"MCMC+BAS"`: García-Donato & Martínez-Beneito (2013) and Forte et al. (2018) report biased PIPs from the latter. Selection = MPM, the same rule as the SMC.
    - *What it tests:* This slot asks whether your fixed prior (g = n plus a unit ridge, Bernoulli(0.2)) is competitive with adaptive-g BMA. Porwal & Raftery (2023) found fixed-θ Bernoulli model priors worse than beta-binomial.

## 4. Strong candidates that were not selected

| Candidate | Evidence | Why not in the ten |
|---|---|---|
| MCP as its own slot | 11 papers | Comes free from the SCAD slot's `ncvreg` call; report as sensitivity. |
| Relaxed lasso | 7 | A `glmnet` option; run inside slot 1. |
| Forward/backward stepwise | 16 (mostly biostatistics neutral studies) | Classical; at p = 30 the exact best-subset check dominates it. |
| ABESS | 1 | Good alternative L0 implementation; L0Learn is the one others benchmark against. |
| Model-space MCMC (SSVS/Gibbs, add-delete-swap, BoomSpikeSlab) | 23 | Same model class as BAS and your SMC, so it has no distinct selection behaviour. **Used in the computational panel** (§5). |
| Bayesian lasso | 8 | Mostly a weak foil; not a selector without an extra rule; superseded by the horseshoe. |
| Regularized horseshoe / horseshoe+ / R2D2 / Dirichlet–Laplace | 5 / 3 / 1 / 4 | Variants of slot 7. Use the regularized horseshoe instead if you run Stan. R2D2 is rising but rarely run by others yet. |
| projpred / DSS | 1 / 1 | Decision rules applied to a shrinkage posterior, not separate models. projpred keeps one or two variables per correlated block by design. |
| EMVS | 5 | Superseded by SSL from the same authors. |
| varbvs / sparsevb | 5 | Mean-field VI concentrates on one variable per correlated group (Carbonetto & Stephens 2012). SuSiE is the variational representative actually adopted. |
| Skinny Gibbs / BASAD | 4 | Designed for p ≫ n (Skinny Gibbs mainly logistic); no current CRAN package for Skinny Gibbs. |
| Nonlocal priors (mombf) | 4 | Rarely run outside the originators' group. Changes the prior; better as a prior-sensitivity extension. |
| Stability selection, Gaussian mirror, data-splitting/MDS, T-Rex, Nullstrap | 3 / 2 / 2 / – / – | FDR/stability alternatives with little adoption as comparators outside their own sub-literature. Data splitting halves n = 100. |
| BH on OLS p-values | 8 | Not a modern method, but a free companion to slot 6 (valid since n > p). |
| Fine-mapping tools (FINEMAP, DAP-G, CAVIAR, SuSiE-inf, CARMA) | 2–3 | Genetics or summary-statistics specific; SuSiE is the general-purpose member. |
| uniLasso (2025), subspace stability selection (2025) | 1 / 0 | Too new to be adopted as comparators. The 2025–26 reading pass reports uniLasso fails on opposite-sign correlated pairs. |
| Random forest / boosting | 1 | Nonlinear learners; uninformative in a correctly specified linear design. |

## 5. Companion computational panel (same posterior, not counted in the ten)

For the claim that composite-start SMC computes the BVS posterior better, compare samplers on **your exact score**, against the exact enumeration you already have, at equal CPU time and equal score evaluations. Measure:

- PIP MAE and MaxAE;
- MPM agreement;
- posterior mass found;
- evidence error, for the methods that give one.

The corpus supports these comparators:

| Comparator | Why | Practicalities |
|---|---|---|
| Single-site Gibbs on γ (SSVS-type) and add-delete-swap (MC3) | Most common computational baseline: 23 papers. | Run your own Gibbs kernel at φ = 1 as one long chain (exact same target). BAS `method = "MCMC"` with `prior = "g-prior", alpha = n`, `modelprior = Bernoulli(0.2)` is a near-match external check; it differs by the unit ridge, the σ² prior and the intercept. |
| wTGS (Zanella & Roberts 2019) | The usual strong and gold-standard sampler; best of the samplers on strongly correlated pairs in the head-to-heads read. | Needs only neighbour scores, so it is easy to re-implement on your score at p = 30. |
| Schäfer–Chopin binary SMC (2013) | The SMC ancestor and the only binary-space SMC other papers benchmark against; isolates the value of the composite start. | Python `particles` (module `binary_smc`, including waste-free SMC) accepts a custom `loglik(gamma)`. |
| PARNI / ASI (optional) | Current state of the art for large p. | Authors' code hard-codes its own prior. PARNI did worst on multimodal moderate-p data in its own paper; more relevant once p ≫ 30. |

## 6. Design-specific expectations and metrics

**What is at stake.** In your Experiment 2, the *exact* posterior's median model recovered the true support in 88, 79, 72, **29** and 65 of 100 datasets (S1–S5). S4 is therefore where competing priors and procedures can most plausibly win or lose. Exact SMC computation cannot fix a prior or decision rule that is misaligned with support recovery.

**Selection metrics** (all ten methods plus the SMC, on the same 500 datasets):

- exact support recovery (Ŝ = S†), which matches `true_identified` in your existing reports;
- TPR (power) and empirical FDP (mean = FDR);
- MCC, F1 and Hamming distance;
- selected size;
- threshold-free AUPRC/AUROC from each method's ranking. Porwal & Raftery's convention: PIPs for Bayesian methods, entry order on the λ path for penalized methods, credible level for the horseshoe.

**Design-specific breakdowns:**

- recovery of the cancelling pair (both x2 and x3 selected);
- false positives among same-block proxies versus null-block variables (the three variable groups of Experiment 1);
- block-level localisation (SuSiE credible sets; BLiP-style group discoveries from the SMC's joint draws).

**Secondary metrics:**

- test-set prediction RMSE (independent test draws from the same Σ);
- wall time including tuning;
- for PIP-producing methods (SMC, BAS, SuSiE), PIP calibration plots.

## 7. Files in this folder

| File | Content |
|---|---|
| `notes/{A..H}_*.json`, `notes/*.md` | Per-paper extraction: comparators as named and canonicalised, location, verbatim quote, version read, findings. |
| `sources/` | Downloaded PDFs/HTML and `pdftotext` text for every paper read. |
| `aggregate.py` | Merges duplicates across passes and writes `comparator_frequency.csv`, `paper_comparator_matrix.csv`, `papers_read.csv`. |
| `family_frequency.txt`, `evidence_by_method.txt` | Family-level counts and the list of papers behind each recommended method. |
| `quote_verification.txt` | Automated check of the evidence quotes against the saved sources. |
| `citation_lookup.py`, `citation_snapshot.{json,csv}` | OpenAlex citation counts for 63 candidates (single-record counts; preprint and journal versions not merged; accessed 2026-10-03). |
| `software_snapshot.json` | CRAN version and publication date for 37 candidate packages. |

**Limitations.**

- **Corpus scope:** This is a targeted review of 110 papers chosen by reading passes, not a census. Counts reflect the corpus composition (e.g., the samplers pass inflates model-space MCMC counts).
- **Paper classification:** The Bayesian vs frequentist paper split is a keyword heuristic.
- **Unread material:** Two papers and some online supplements could not be accessed; they are recorded as unread, not guessed.
- **Citation counts:** OpenAlex counts undercount some records relative to Google Scholar.
