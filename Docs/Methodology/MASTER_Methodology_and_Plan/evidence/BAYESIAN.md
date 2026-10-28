# Bayesian benchmarks for the composite-start SMC study (n = 200; Regime L p = 30, Regime H p = 500/1000)

Prepared 2026-10-19 and revised the same day after a design change from the lead. The true support now depends on the regime:
- **Regime L** (p = 30): 5 signals, (1.4, −1.0, 1.8, −1.2, 0.8).
- **Regime H** (p = 500 or 1000): 14 signals, one per block, with coefficients cycling through (1.4, −1.0, 1.8, −1.2, 0.8, −1.6).

Both regimes use n = 200, the six designs S1–S6 and the scales c ∈ {1, .75, .5, .35, .25}. Every setting below is chosen without using the true size 5 or 14.

The report builds on `Papers/VS_Benchmarks_Independent_Review_20261003/BENCHMARK_RECOMMENDATION.md` (108-paper review, n = 100, p = 30) and on Methodology §7. No simulations were run.

**How the evidence was checked.**
- Usage quotes were read in the local full-text copies kept by that review (`.../sources/*.txt`) or in pages fetched today.
- DOIs were checked against the Crossref API.
- Package versions were taken from the CRAN index pages and manuals fetched today.
- GitHub repositories were checked with the GitHub API.

Raw evidence, quotes and line numbers are in `benchmarks/notes_bayesian/evidence_log.md`; fetched pages and manuals are in the same folder. Source IDs such as [S3] or [E1] refer to §5.

**What changed since the p = 30 list.**
- `horseshoe` was removed from CRAN on 2025-10-10, and `mombf` on 2026-09-30. Their maintained replacements are `bayesreg` and `modelSelection`.
- The SMC now selects by HPM (highest-posterior model) under a BB(1,p) model prior, not by MPM (median-probability model) under Bernoulli(0.2). Rules and priors below are aligned to that.
- The p > n literature (2020–2026) adds the nonlocal-prior model-space slot and changes how BAS is run. SuSiE, SSL and the horseshoe remain the most-run Bayesian comparators at n = 200, p = 1000 [E1, E4].

**Rules common to every method.**
- **No oracle input.** No method is given the true size (5 in L, 14 in H), the true support, the true blocks, or Σ. Caps on the number of effects (SuSiE's L, the model-size truncations) are set from n, p or package defaults, never from the truth. This applies even where a published comparison did otherwise: Kollipara et al. gave SuSiE the true L, and gave SSVS and the regularized horseshoe the true expected model size [E1].
- **Same data.** Every method gets the same (X, y): X centred and scaled with the sample SD, y uncentred.
- **Intercept.** No intercept where the software allows it. Where it forces one (BAS, bayesreg; SSLASSO centres y), record this; it costs one degree of freedom and is harmless here because X is centred and the truth has no intercept.
- **Fixed settings.** Every setting below is fixed before any run, and every deviation is logged.

## 1. Selection panel (A): Bayesian procedures with their own prior or approximation

Five primary methods. All five run in both regimes.

| # | Method | Prior / approximation | Regime(s) | Reference (verified id) | Software, version, date | Settings and selection rule (no oracle input) | Evidence of use at p > n (paper, location) | Caveats |
|---|---|---|---|---|---|---|---|---|
| A1 | **SuSiE** | Sum of L single-effect regressions; variational IBSS fit | L and H | Wang, Sarkar, Carbonetto & Stephens 2020, JRSSB 82(5):1273–1300, doi:10.1111/rssb.12388 [S1] | `susieR` 0.14.2, CRAN 2025-06-05 [W1] | `susie(X, y, L = L*, intercept = FALSE, standardize = FALSE, estimate_residual_variance = TRUE, estimate_prior_variance = TRUE, coverage = 0.95, min_abs_corr = 0.5, max_iter = 1000)`. These are the package defaults except intercept/standardize (project decision of 2026-10-07) and max_iter (raised for the larger L). **L\* rule (non-oracle):** L\* = 10 in L (the package default, as decided on 2026-10-07), and **L\* = 50 in H** (n/4). The manual says L "should be chosen to provide a reasonable upper bound on the number of non-zero effects to be detected"; unused effects are switched off because `estimate_prior_variance = TRUE` estimates their prior variance at 0. Wang et al. report robustness to overstating L (§3.3) [S1]. **The default L = 10 must not be used in H**, because it makes 14-signal recovery impossible. **Rule:** PIP > 0.5, the same threshold as the SMC. | Kollipara et al. 2026, Stat Med, n = 200, p = 1000: "SuSiE was implemented using susie from susieR" (§4.2) [E1]. Kim et al. 2024 JMLR, n = 500, p = 1000, Table 1: "SuSiE susieR variational inference" (§5.1) [E2]. | Kollipara set L to the true size (oracle), so do not copy that. Kollipara also reports that SuSiE "failed completely" in some correlated and heavy-tail cells (§4.4) [E1]. IBSS can stick in local optima with opposite-sign correlated pairs (Wang et al. §6, per the 2026-10-03 review). Feasibility: 0.4–5 s per fit at n = 200, p = 1000 with small L [E1]. With L = 50 the cost per IBSS sweep grows linearly in L; this is UNVERIFIED but expected to stay in seconds to minutes. |
| A2 | **Spike-and-slab LASSO (SSL)** | Laplace spike and slab mixture; adaptive θ ~ Beta(1, p); posterior mode by coordinate ascent along a λ0 ladder | L and H | Ročková & George 2018, JASA 113(521):431–444, doi:10.1080/01621459.2016.1260469 [S2] | `SSLASSO` 1.2.3, CRAN 2025-11-04 [W2] | `SSLASSO(X, y, penalty = "adaptive", variance = "unknown")` with the package defaults: λ0 = `seq(1, n, length = 100)`, λ1 = λ0[1] = 1, a = 1, b = p (checked in the package source). **Rule:** `$model`, the support at the end of the λ0 ladder ("A single model chosen after the stabilization of the regularization path"). | Kollipara 2026, n = 200, p = 1000: "Spike-and-slab LASSO (SL) ... implemented using SSLASSO" (§4.2) [E1]. Ray & Szabó 2022 JASA, (n, p) = (100, 400), (100, 1000), (200, 800): SSLASSO with "a = 1, b = p, and penalty="adaptive"" (§5.2, Table 2) [E3]. Das 2026, (p, n) = (1000, 200) (§5, Table 1) [E4]. | Its Beta(1, p) prior on θ mirrors the SMC's BB(1,p) prior, but the slab differs (Laplace, not g-type) and the output is a point estimate, so it has no PIPs and no evidence. SSLASSO centres y internally and standardizes X. Ray & Szabó used λ1 = 0.01 and a λ0 ladder up to p (§5.2), which is the sensitivity below. Feasibility: 1–10 s per fit [E1]. |
| A3 | **Horseshoe** | Global-local continuous shrinkage (half-Cauchy local and global scales); Gibbs MCMC | L and H | Carvalho, Polson & Scott 2010, Biometrika 97(2):465–480, doi:10.1093/biomet/asq017 [S3]. Implementation: Makalic & Schmidt 2016, arXiv:1611.06649 (id as cited on the CRAN page) [S4] | `bayesreg` 1.3, CRAN 2024-09-30 [W3]. The `horseshoe` package (last 0.2.0, 2019-07-18) was archived 2025-10-10 [W4]. | `bayesreg(y ~ ., data, model = "normal", prior = "hs", n.samples = 5000, burnin = 1000, thin = 1, n.cores = 1)`. The 5000 + 1000 iteration budget follows Das 2026 and Kollipara 2026 [E1, E4]. **Rule:** 95% credible interval excludes 0 (the rule of Porwal & Raftery 2022: "we calculated a 95% credible interval and checked whether 0 was included") [E5]. | Porwal & Rodríguez 2024 (arXiv:2411.00471v3), n = 500, p = 750: "Computation under the Horseshoe prior relies on version 1.2 of the R package bayesreg" (§6.2) [E6]. Kollipara 2026, n = 200, p = 1000 (horseshoe pkg, §4.2) [E1]. Das 2026 (bayesreg MATLAB, §5) [E4]. | The interval rule is conservative under correlation. No PIPs or evidence. The bayesreg formula interface fits an intercept. Runtime risk at p = 1000: Kollipara reports HS 20–300 s with the `horseshoe` package but HS+ 250–17,000 s with Bayesreg [E1]. Which sampler bayesreg uses when p > n is not stated in the manual (UNVERIFIED); pilot-time one dataset first. |
| A4 | **g-prior BMA (BAS, hyper-g)** | Point-mass spike; hyper-g mixture of g-priors; beta-binomial model prior; MC3 + swap MCMC over models | L and H | Clyde, Ghosh & Littman 2011, JCGS 20(1):80–101, doi:10.1198/jcgs.2010.09049 [S5]. Liang et al. 2008, JASA 103(481):410–423, doi:10.1198/016214507000001337 [S6] | `BAS` 2.0.2, CRAN 2025-12-23 [W5] | `bas.lm(y ~ ., data, prior = "hyper-g", alpha = 3, method = "MCMC")` with the default MCMC.iterations (p·1000) and burnin.iterations (p·25). Use `"MCMC"`, not `"MCMC+BAS"` (2026-10-03 review). Model prior: L uses `beta.binomial(1,1)`; H uses `tr.beta.binomial(1, 1, trunc = n − 2)`, Porwal & Raftery's p > n convention [E5] (the BAS manual: "Truncated versions are useful for p > n"). **Rule:** HPM, `estimator = "HPM"`, the same rule as the SMC; MPM is a sensitivity. | Porwal & Raftery 2022 PNAS ran BAS on 4 p > n datasets (NIR 166×225, Multidrug 60×853, Liver toxicity 64×3116, Nutrimouse 40×120): "For high-dimensional datasets with p > n, a truncated beta-binomial (1, 1) prior is used" (Materials and Methods; Table 2) [E5]. Porwal & Rodríguez 2024, p = 750 > n = 500: "BAS" v1.7.1 (§6.2) [E6]. | This is the closest prior family to the SMC's, but it uses an adaptive g, BB(1,1), a Jeffreys σ² prior and a forced intercept ("By default ... the intercept is always included"). Its evidence is therefore not comparable with the SMC's Z. The MCMC run time at p = 1000 with 10⁶ iterations is UNVERIFIED; pilot first. Porwal & Raftery note hyper-g is "substantially slower" than the fixed-g options [E5]. |
| A5 | **Nonlocal prior (pMOM) model selection** | Product moment (nonlocal) prior on coefficients; beta-binomial model prior; Gibbs over models with exact or Laplace marginal likelihoods | L and H | Johnson & Rossell 2012, JASA 107(498):649–660, doi:10.1080/01621459.2012.682536 [S7]. Rossell & Telesca 2017, JASA 112(517):254–265, doi:10.1080/01621459.2015.1130634 [S8]. Package book: Rossell 2025, doi:10.5281/zenodo.17119597 [S9] | `modelSelection` 1.0.7, CRAN 2026-05-16 [W6], the successor of `mombf` (archived 2026-09-30) [W7] | `modelSelection(y = y, x = X, center = FALSE, scale = FALSE, priorCoef = momprior(taustd = 1), priorModel = modelbbprior(1, 1), priorVar = igprior(.01, .01), enumerate = FALSE, niter = 5000)`. These are the package defaults (`taustd = 1` is "the unit information prior"); burnin defaults to niter/10. **Rule:** HPM = `postMode`, "Model with highest posterior probability amongst all those visited", matching the SMC; PIP (`margpp`) > 0.5 is a sensitivity. | Porwal & Raftery 2022: "NLP ... mombf-V2.2.9 modelSelection()" run on the same 4 p > n datasets with truncated BB(1,1) (Table 2; Materials and Methods) [E5]. Li, Dutta & Roy 2023 JCGS, n = 400, p = 20,000: "S5 (R package: BayesS5)" with piMOM/peMOM nonlocal priors (§4) [E7]. | This is the only primary with a different *type* of prior (nonlocal) but the same HPM decision, so it tests whether prior choice moves support recovery, notably in S4. The manual says "for models with >15 variables ... Laplace approximations are used". The H truth has 14 variables, so the true model and its one-up neighbours sit at the switch between closed-form and Laplace marginals, and the Laplace version "tends to be conservative". No size truncation is available in Gibbs mode. Runtime at p = 1000 is UNVERIFIED; pilot first. The package is new (2025), so check the version on install. |

**Why these five.**
- They span the four Bayesian paradigms that recent p > n papers actually run:
  - model-space BMA: A4, A5;
  - spike-and-slab penalized mode: A2;
  - continuous shrinkage: A3;
  - variational sum-of-effects: A1.
- A1–A3 are the three Bayesian methods run at exactly n = 200, p = 1000 by both Kollipara 2026 and Das 2026 [E1, E4].
- A4 and A5 are the model-space procedures from the largest neutral comparison (Porwal & Raftery 2022). Their HPM rule matches the SMC's.

**Outputs.** Only A4 and A5 give model-level HPMs. A1 and A4 give PIPs as well (A5 gives `margpp`). None gives an evidence value comparable to the SMC's Z, because each has a different model.

## 2. Computational panel (B): samplers that target the SMC's own posterior

**Target.** Every entry must use the project's score l(S) exactly, with:
- the slab N(0, σ² n (X_S'X_S + I)⁻¹);
- the IG(0.01, 0.01) variance prior;
- the BB(1,p) model prior truncated at |S| ≤ 100;
- uncentred y and no intercept.

**What to compare.**
- In Regime L: PIP MAE and max error, HPM agreement and mass found, against exact 2³⁰ enumeration.
- Evidence Z: only for B3, and the exact value only in L.
- In Regime H there is no exact reference (see §3).

| # | Sampler | Reference (verified id) | Code (verified page, last activity) | Accepts a custom score/prior? | What must be re-implemented | Regime(s) |
|---|---|---|---|---|---|---|
| B1 | **PARNI** (point-wise adaptive random neighbourhood informed MH), already in Methodology §7 | Liang, Livingstone & Griffin 2022, Stat Comput 32:84, doi:10.1007/s11222-022-10137-8 [S10] | github.com/XitongLiang/The-PARNI-scheme (R and Python; ADS and ASI included); last commit 2026-03-14 [W8] | **No.** `log_llh.R` hard-codes `log_llh_g_L` (Zellner g) and `log_llh_ind_L` (independent prior), and `make_hyper_par.R` centres y ("y <- scale(y, scale = FALSE)") [W8]. This confirms the project note of 2026-10-07. | Port the sampler mechanics: random neighbourhood from RB-PIPs, informed thinned proposal, min(1, t) balancing, KW adaptation, κ floor. Call the project's l(S), and add the BB(1,p) log prior ratio inside the flip Bayes factors. Keep the tuning fixed on 2026-10-07. | L and H |
| B2 | **Weighted tempered Gibbs (wTGS)** | Zanella & Roberts 2019, JRSSB 81(3):489–517, doi:10.1111/rssb.12316 [S11] | Authors' R code github.com/gzanella/TGS (last push 2018-05-07) [W9]; `scaleBVS` github.com/albcab/scaleBVS (Zanella & Cabezas, last push 2021-07-10) [W10] | **No.** `single_full_cond` hard-codes the g-prior with Bernoulli(h): `post_ratio<-h/(1-h)*(S_old/S_new)^(n/2)/(sqrt(1+c))` [W9]. scaleBVS's README states the same model: Zellner prior, p(σ²) ∝ 1/σ², Bernoulli(h) [W10]. | Replace the full conditionals by exp{l(S∪j) − l(S∖j)} × the BB(1,p) prior ratio. Keep the wTGS index weights and the importance weights, and use the Rao-Blackwellised PIPs. Each iteration needs all p flip scores, so cache scores. | L and H |
| B3 | **Schäfer–Chopin binary SMC** (tempering from the prior, nested-logistic independent MH; waste-free variant as option) | Schäfer & Chopin 2013, Stat Comput 23(2):163–184, doi:10.1007/s11222-011-9299-z [S12]. Waste-free: Dau & Chopin 2022, JRSSB 84(1):114–148, doi:10.1111/rssb.12475 [S13] | Python `particles`, module `binary_smc` (github.com/nchopin/particles, pushed 2026-09-24; PyPI 0.4, 2023-11-06) [W11] | **Yes.** Subclass `VariableSelection`/`StaticModel` and override `loglik(self, gamma, t=None)`; the built-ins are `BayesianVS` and `BayesianVS_gprior` [W11]. The prior is a separate object. | Two things are needed. (1) A vectorised numpy l(S), checked against the R engine to about 1e-10 on random models. (2) A BB(1,p) prior object with `rvs`/`logpdf`, truncated at 100, so that tempering starts from the true prior. Do not fold the prior into `loglik`, which would change the tempering path. This is the only panel member that returns Z. It isolates the value of the composite start, because it is the same SMC family started from the prior. | **L primary.** H as a labelled stress run only (see caveat). |
| B4 | **Add-delete-swap MC3 (ADS)**, long-run baseline | MC3: Madigan, York & Allard 1995, Int Stat Rev 63(2):215, doi:10.2307/1403615 [S14]. ADS as defined in Liang et al. 2022, Example 2 [S10] | `R/sampler/ADS.R` in the PARNI repo [W8]. BAS `method = "MCMC"` implements MC3 + swap but cannot take a custom score [W5]. | **No** (both hard-code their priors). | A trivial re-implementation on l(S). Run one long chain plus independent restarts. | L and H |

**Evidence that each sampler is run at p > n.**
- **B1 PARNI.** Its own paper ran it on PCR data, "60 observations ... 22, 575 genes" (§5.2), and on simulated n = 500, p = 5000 (§5.1) [E9]. Two web searches found **no independent paper (2023–2026) that ran PARNI as a comparator**; the only later uses are by the same authors (GLM extension, PARNI-DAG). Its evidence base is therefore self-reported.
- **B2 wTGS.** Liang et al. 2022, PCR data: "both the tempered Gibbs sampler (TGS) and weighted tempered Gibbs sampler (WTGS) of Zanella and Roberts (2019)" (§5.2) [E9]. Staerk et al. 2024 ran wTGS in its enumerable low-dimensional setting [E11].
- **B3 Schäfer–Chopin.** Griffin, Łatuszyński & Steel 2021, PCR data (n = 60, p = 22,576) and SNP data: "the Hamming Ball sampler with radius 1 and the Schäfer-Chopin algorithm. Three independent runs of all algorithms were executed" (§4.4) [E10]. Staerk et al. 2024 summarise the outcome: SMC and tempered Gibbs "do not provide reliable estimates of posterior inclusion probabilities for the PCR data" [E11].
- **B4 ADS.** Liang et al. 2022, n = 500, p = 50,000: "The ADS scheme fails to converge ... becomes trapped at areas around the null model" (§5.1) [E9]. Griffin et al. 2021 used it on PCR and SNP data (§4.4) [E10].

**Compute budget.** Match on equal wall-clock time and on equal numbers of score evaluations (both reported), single core. Warm-up and adaptation count toward the budget. Run five independent repeats per dataset (as fixed for PARNI on 2026-10-07).

## 3. Key p > n caveats (Regime H)

1. **No exact reference.** With 2¹⁰⁰⁰ models, PIP and Z accuracy in H can only be measured as agreement across independent long runs and samplers, as in Griffin et al. 2021 [E10]. Report this agreement, not "error", and never call a pooled run "exact". Support recovery against the truth remains exact.
2. **Known p > n failures.** ADS gets trapped at p ≫ n [E9]. Schäfer–Chopin and TGS were unreliable on the p > n PCR data [E11]. Expect B3 and B4 to be weak in H. That is a legitimate finding, but it means B1 and B2 are the meaningful competitors in H.
3. **Model-size limits.** The g-type slab needs |S| < n. The SMC's cap of 100 and BAS's truncation at n − 2 are both far above 14 signals, but they differ. modelSelection has no truncation in Gibbs mode.
4. **Oracle settings in the literature.** The closest published design (Kollipara 2026, n = 200, p = 1000) gave SuSiE the true L, and gave SSVS and the regularized horseshoe the true expected size [E1]. Our settings deliberately do not, so do not compare our numbers with theirs cell by cell.
5. **Runtime spread at p = 1000** on one core, from the literature:
   - SuSiE: seconds;
   - SSL: about 10 s;
   - horseshoe: up to minutes, and bayesreg HS+ up to hours [E1];
   - BAS and modelSelection: unmeasured.

   Run one pilot dataset per method in H before fixing iteration budgets, and record the budgets.
6. **Effective prior differences, and what BB(1,p) implies for 14 signals.** Computed exactly with the beta-binomial pmf:
   - Under BB(1,p) the prior on model size is close to geometric with ratio P(k+1)/P(k) = (p−k)/(2p−k−1) ≈ 1/2, and the prior mean size is ≈ 1 (0.968 at p = 30; 0.998 at p = 500; 0.999 at p = 1000).
   - P(|S| ≥ 5) = 2.6e-2 at p = 30. P(|S| ≥ 14) = 5.6e-5 at p = 500 and 5.8e-5 at p = 1000. P(|S| > 100) ≤ 1.4e-32, so the cap at 100 is immaterial.
   - Each added variable therefore costs about log 2 in prior odds on size, on top of the multiplicity correction. In H, at small c, the SMC's HPM and PIP > 0.5 rule will tend to omit the weakest of the 14 signals. This is a property of the prior, not of computation, and it applies equally to B1–B4.
   - BAS and modelSelection use BB(1,1) (a uniform size prior, truncated at n − 2 for BAS). SSL's adaptive θ ~ Beta(1, p) imposes the same strong sparsity as the SMC.
   - So differences in false negatives in H partly measure the model-size prior. The BB(1,p) sensitivity for BAS (§4) isolates this. Report recovery as a function of c, and report it separately for the strongest and weakest coefficient groups.
7. **Effect caps versus 14 signals.**
   - SuSiE's default L = 10 is below 14, so L\* = 50 in H (A1).
   - BAS truncation n − 2 = 198, the SMC cap of 100, and SSL, horseshoe and modelSelection (no cap) are all far above 14.
   - The H sparsity is 14/1000 = 1.4% and 14/500 = 2.8%. This is close to Kollipara's 1% and 3% cells at n = 200, p = 1000 [E1], which are the nearest published reference points.
8. **Rules.** Only A4 and A5 select an HPM. A1 thresholds PIPs, A2 takes a mode, and A3 uses intervals. Report each method's rule beside its exact-recovery rate.

## 4. Sensitivities (labelled; not extra benchmarks)

| Parent | Sensitivity | Why |
|---|---|---|
| A1 SuSiE | (a) **`susie_auto(X, y, L_init = 1, L_max = 512, intercept = FALSE, standardize = FALSE)`**. This is the package's documented L-growing procedure: "If the last step estimates some prior variances to be zero, stop. Otherwise, double L, and repeat." (susieR 0.14.2 manual) [W1]. (b) L = 100 in H, and L = 30 (= p) in L. (c) `refine = TRUE`. (d) CS-lead rule: the top-PIP variable in each 95% credible set with purity ≥ 0.5. | (a) and (b) test whether L\* constrains recovery without using the truth. (c) targets IBSS local optima. (d) gives set-level selection. |
| A2 SSL | λ1 = 0.01 and λ0 = 200-point ladder from 1 to p (Ray & Szabó 2022, §5.2) [E3]. | In H the default ladder stops at n = 200 < p. |
| A3 Horseshoe | (a) Horseshoe+ (`prior = "hs+"`; Bhadra et al. 2017, BA 12(4):1105–1131, doi:10.1214/16-BA1028 [S15]). (b) 2-cluster k-means on \|posterior mean\| (Kollipara rule) [E1]. (c) `horseshoe` 0.2.0 from the CRAN archive, to cross-check the implementation. | Variant prior; an alternative rule; the archived package used by Kollipara and Porwal. |
| A4 BAS | (a) `prior = "g-prior", alpha = sqrt(n)` (BAS manual: "Porwal & Raftery (2022) recommend alpha = sqrt(n)"). (b) `"EB-local"`. (c) Model prior `tr.beta.binomial(1, p, trunc = 100)`, which matches the SMC's model prior so that only the slab differs. (d) MPM rule. | Porwal & Raftery's top three, plus isolating the slab from the model prior. |
| A5 Nonlocal | (a) MPM (`margpp > 0.5`). (b) `momprior(tau = 0.348)` (the default of `modelsearchBlockDiag`). (c) `BayesS5` 1.41 (CRAN 2020-03-24) S5 search, as run by Li et al. 2023 [E7], for H. | Rule, prior scale, and the alternative nonlocal search algorithm. |
| A (extra) | Variational spike-and-slab: `varbvs` 2.6-10 (CRAN 2023-05-31; Carbonetto & Stephens 2012, BA 7(1):73–108, doi:10.1214/12-BA703 [S16]) or `sparsevb` 0.1.1 (CRAN 2025-01-24; Ray & Szabó 2022 [E3]). Rule: PIP > 0.5. | Run in Kim 2024 and Ray & Szabó 2022 [E2, E3]. Mean-field approximations pick one variable per correlated block, which is informative in S3–S6. |
| B (extra) | **Near-match external check:** `modelSelection(..., priorCoef = zellnerprior(taustd = 1), priorModel = modelbbprior(1, p), priorVar = igprior(0.02, 0.02), center = FALSE, scale = FALSE)`. The manual gives "igprior ... inverse gamma prior with parameters alpha/2, lambda/2", so igprior(0.02, 0.02) is IG(0.01, 0.01). | It is an off-the-shelf Gibbs sampler on a posterior differing from the SMC's only by the "+I" ridge in the slab and the 100 cap. The exact Zellner parametrisation is UNVERIFIED: check it numerically with `marginalLikelihood()` against l(S) on toy models before use. |
| B (extra) | LIT-MH (Zhou, Yang, Vats, Roberts & Rosenthal 2022, JRSSB 84(5):1751–1784, doi:10.1111/rssb.12546 [S17]); re-implement on l(S). | An informed proposal with dimension-free mixing theory. The authors' code URL (paper L2993) timed out: UNVERIFIED. |

## 5. Considered and rejected

| Candidate | Reason |
|---|---|
| EMVS | Archived from CRAN 2022-12-05 [W4]. It is superseded by SSL from the same authors. In SVEN it was run with three v0 values because results depend strongly on v0 [E7]. |
| Skinny Gibbs / BASAD (Narisetty, Shen & He 2019, JASA 114(527):1205–1217, doi:10.1080/01621459.2018.1482754 [S18]) | Its simulations are logistic [prior review]. No CRAN package was found (`skinnybasad` returns 404) [W4]. SVEN excluded BASAD "for its high computational burden" [E7]. |
| SSVS via `BoomSpikeSlab` 1.2.7 (`lm.spike`) | Run by Kollipara and Porwal & Raftery, but its default prior needs an expected model size, which Kollipara set to the truth [E1]. It is a model-space spike-and-slab like A4 and A5, so it adds little beyond them. It is not a same-posterior sampler. Optional only. |
| Regularized horseshoe (Piironen & Vehtari 2017, EJS 11(2):5018–5051, doi:10.1214/17-EJS1337SI [S19]) via rstanarm | HMC took 1400–3400 s per fit at n = 200, p = 1000, and Kollipara supplied the true expected size [E1]. Its slab scale needs a guess at p0. Horseshoe+ is the cheaper variant (§4). |
| Dirichlet–Laplace, R2D2 | "become infeasible and are excluded" at (p, n) = (1000, 200) in Das 2026 [E4]. |
| Bayesian lasso | It does not select variables without an added rule, is slow under HMC/MCMC (1150–2000 s [E1]), and the 2026-10-03 review judged it a weak foil. |
| Mr.ASH | An empirical-Bayes prediction method [E2] whose posterior mean is not sparse. `mr.ash.alpha` is not on CRAN (404) [W4]. |
| BLiP (Spector & Janson 2025, JASA 120(549):460–471, doi:10.1080/01621459.2024.2347667 [S20]) | Post-processing of posterior samples rather than a selector. It could later be applied to the SMC particles. Its paper let SuSiE use the true sparsity. |
| Projection predictive (projpred), DSS | Decision rules on a reference posterior, not separate models (2026-10-03 review). |
| ASI (Griffin et al. 2021, Biometrika 108(1):53–69, doi:10.1093/biomet/asaa055 [E10]) | Superseded by PARNI from the same group: "ASI mixes worse and converges slower in high-dimensional data-sets" (Liang 2022 §5.1) [E9]. Code exists in the PARNI repo if needed. |
| TGS (unweighted) | Dominated by wTGS. Reported unreliable on PCR [E11]. |
| Hamming ball sampler (Titsias & Yau 2017, JASA 112(520):1598–1611, doi:10.1080/01621459.2016.1222288 [S21]) | Griffin et al. 2021 report it "required 34 times the run time" of ADS in their comparison [E10]. |
| MAdaSub (Staerk, Kateri & Ntzoufras 2024 [E11]) | Its R code (github.com/chstaerk/MAdaSub, last push 2022-07-05) is paper source files, not a package (CRAN 404) [W12], and is tied to its g-prior/EBIC scores. It is a plausible fifth sampler if the panel grows. |
| Fine-mapping tools (FINEMAP, DAP-G, CARMA, SuSiE-inf) | Genetics or summary-statistic specific; SuSiE is the general-purpose member (2026-10-03 review). |
| `millipede` (Jankowiak 2023, arXiv:2208.01180; subset wTGS) | Built for P ≫ 10⁴. It hard-codes its own prior (README). B2 covers wTGS. |

## 6. Sources

Status: **VERIFIED** means opened today, or read in the local full-text copy, and the id was checked against Crossref, Zenodo or the PDF header. **UNVERIFIED** is stated explicitly.

**Method references**
- [S1] Wang, Sarkar, Carbonetto, Stephens (2020). JRSSB 82(5):1273–1300. https://doi.org/10.1111/rssb.12388. VERIFIED (Crossref; local text).
- [S2] Ročková, George (2018). JASA 113(521):431–444. https://doi.org/10.1080/01621459.2016.1260469. VERIFIED (Crossref).
- [S3] Carvalho, Polson, Scott (2010). Biometrika 97(2):465–480. https://doi.org/10.1093/biomet/asq017. VERIFIED (Crossref).
- [S4] Makalic, Schmidt (2016). arXiv:1611.06649. Id VERIFIED as cited on the CRAN bayesreg page; the arXiv page itself was not opened (arXiv API rate-limited).
- [S5] Clyde, Ghosh, Littman (2011). JCGS 20(1):80–101. https://doi.org/10.1198/jcgs.2010.09049. VERIFIED (Crossref).
- [S6] Liang, Paulo, Molina, Clyde, Berger (2008). JASA 103(481):410–423. https://doi.org/10.1198/016214507000001337. VERIFIED (Crossref).
- [S7] Johnson, Rossell (2012). JASA 107(498):649–660. https://doi.org/10.1080/01621459.2012.682536. VERIFIED (Crossref).
- [S8] Rossell, Telesca (2017). JASA 112(517):254–265. https://doi.org/10.1080/01621459.2015.1130634. VERIFIED (Crossref).
- [S9] Rossell (2025). modelSelection book. https://doi.org/10.5281/zenodo.17119597. VERIFIED (Zenodo API: published 2025-09-15).
- [S10] Liang, Livingstone, Griffin (2022). Stat Comput 32:84. https://doi.org/10.1007/s11222-022-10137-8. VERIFIED (Crossref; local PDF).
- [S11] Zanella, Roberts (2019). JRSSB 81(3):489–517. https://doi.org/10.1111/rssb.12316. VERIFIED (Crossref).
- [S12] Schäfer, Chopin (2013). Stat Comput 23(2):163–184. https://doi.org/10.1007/s11222-011-9299-z. VERIFIED (Crossref).
- [S13] Dau, Chopin (2022). JRSSB 84(1):114–148. https://doi.org/10.1111/rssb.12475. VERIFIED (Crossref).
- [S14] Madigan, York, Allard (1995). Int Stat Rev 63(2):215. https://doi.org/10.2307/1403615. VERIFIED (Crossref). The attribution of MC3 to this paper is from general knowledge, not from a source read today.
- [S15] Bhadra, Datta, Polson, Willard (2017). BA 12(4):1105–1131. https://doi.org/10.1214/16-BA1028. VERIFIED (Crossref).
- [S16] Carbonetto, Stephens (2012). BA 7(1):73–108. https://doi.org/10.1214/12-BA703. VERIFIED (Crossref).
- [S17] Zhou, Yang, Vats, Roberts, Rosenthal (2022). JRSSB 84(5):1751–1784. https://doi.org/10.1111/rssb.12546. VERIFIED (Crossref).
- [S18] Narisetty, Shen, He (2019). JASA 114(527):1205–1217. https://doi.org/10.1080/01621459.2018.1482754. VERIFIED (Crossref).
- [S19] Piironen, Vehtari (2017). EJS 11(2):5018–5051. https://doi.org/10.1214/17-EJS1337SI. VERIFIED (Crossref).
- [S20] Spector, Janson (2025). JASA 120(549):460–471. https://doi.org/10.1080/01621459.2024.2347667. VERIFIED (Crossref).
- [S21] Titsias, Yau (2017). JASA 112(520):1598–1611. https://doi.org/10.1080/01621459.2016.1222288. VERIFIED (Crossref).

**Usage evidence**
- [E1] Kollipara, Maiti, Chakraborty, Sinha (2026). Stat Med 45(3-5):e70428. https://doi.org/10.1002/sim.70428. VERIFIED (Crossref; local PMC full text).
- [E2] Kim, Wang, Carbonetto, Stephens (2024). JMLR 25, paper 22-0953. http://jmlr.org/papers/v25/22-0953.html. VERIFIED (local PDF header).
- [E3] Ray, Szabó (2022). JASA 117(539):1270–1281. https://doi.org/10.1080/01621459.2020.1847121. VERIFIED (Crossref; local arXiv v3 text).
- [E4] Das (2026). arXiv:2604.04964v2. https://arxiv.org/abs/2604.04964. VERIFIED (local PDF header and text).
- [E5] Porwal, Raftery (2022). PNAS 119(16). https://doi.org/10.1073/pnas.2120737119. VERIFIED (Crossref; local full text).
- [E6] Porwal, Rodríguez (2024/2026). arXiv:2411.00471v3. https://arxiv.org/abs/2411.00471. VERIFIED (local PDF header and text).
- [E7] Li, Dutta, Roy (2023). JCGS 32(1):61–73. https://doi.org/10.1080/10618600.2022.2074428. VERIFIED (Crossref; local text).
- [E8] Wang et al. (2020), same as [S1]: §3.3 and §4.2 quotes VERIFIED in local text.
- [E9] Liang, Livingstone, Griffin (2022), same as [S10]: §5.1–5.2 quotes VERIFIED in local text.
- [E10] Griffin, Łatuszyński, Steel (2021). Biometrika 108(1):53–69. https://doi.org/10.1093/biomet/asaa055. VERIFIED (Crossref; local arXiv v3 text).
- [E11] Staerk, Kateri, Ntzoufras (2024). BA 19(1):261–291. https://doi.org/10.1214/22-BA1351. VERIFIED (Crossref; local text).
- Jankowiak (2023). arXiv:2208.01180. Id VERIFIED from the local PDF header. The AISTATS/PMLR 206 venue is UNVERIFIED (not found in the text).
- Papaspiliopoulos & Rossell (2017), Biometrika, doi:10.1093/biomet/asx019. UNVERIFIED: Crossref returns only "OUP accepted manuscript". Not used as evidence.
- Shin, Bhattacharya, Johnson (2018). Stat Sinica, doi:10.5705/ss.202016.0167. DOI resolves on Crossref (author metadata garbled there); arXiv:1507.07106v4 VERIFIED from the local PDF. Cited only via the BayesS5 sensitivity.

**Software pages (fetched 2026-10-19)**
- [W1] https://cran.r-project.org/package=susieR: 0.14.2, 2025-06-05. VERIFIED.
- [W2] https://cran.r-project.org/package=SSLASSO: 1.2.3, 2025-11-04; source defaults read at github.com/cran/SSLASSO. VERIFIED.
- [W3] https://cran.r-project.org/package=bayesreg: 1.3, 2024-09-30. VERIFIED.
- [W4] CRAN archive notices, all VERIFIED:
  - `horseshoe` archived 2025-10-10 (last 0.2.0, 2019-07-18);
  - `mombf` archived 2026-09-30;
  - `EMVS` archived 2022-12-05;
  - `BVSNLP` archived 2025-12-25;
  - 404 pages for `skinnybasad`, `mr.ash.alpha` and `MAdaSub`.
- [W5] https://cran.r-project.org/package=BAS: 2.0.2, 2025-12-23; manual read. VERIFIED.
- [W6] https://cran.r-project.org/package=modelSelection: 1.0.7, 2026-05-16; manual read. VERIFIED.
- [W7] https://cran.r-project.org/package=mombf: archived. VERIFIED.
- [W8] https://github.com/XitongLiang/The-PARNI-scheme: last commit 2026-03-14; `log_llh.R` and `make_hyper_par.R` read. VERIFIED.
- [W9] https://github.com/gzanella/TGS: last push 2018-05-07; `functions_for_BVS.R` read. VERIFIED.
- [W10] https://github.com/albcab/scaleBVS: last push 2021-07-10; README read. VERIFIED.
- [W11] https://github.com/nchopin/particles: last push 2026-09-24; `particles/binary_smc.py` read. PyPI `particles` 0.4, 2023-11-06. VERIFIED.
- [W12] https://github.com/chstaerk/MAdaSub: last push 2022-07-05. VERIFIED.
- Also on CRAN today, all VERIFIED:
  - `BayesS5` 1.41 (2020-03-24);
  - `varbvs` 2.6-10 (2023-05-31);
  - `sparsevb` 0.1.1 (2025-01-24);
  - `BoomSpikeSlab` 1.2.7 (2025-09-04).
- LIT-MH code, https://web.stat.tamu.edu/~quan/code/lit_mh.tgz: UNVERIFIED (request timed out).

**Tally.**
- References and evidence papers: 31 items listed. 28 are VERIFIED, 2 are UNVERIFIED (the Jankowiak venue; the Papaspiliopoulos & Rossell 2017 DOI) and 1 is only partially verified (S4: id taken from CRAN, arXiv page not opened). The MC3 attribution in S14 is also flagged above.
- Software pages: 17 items. 16 are VERIFIED and 1 is UNVERIFIED (LIT-MH code).
- Every *recommended* method (A1–A5, B1–B4) has a verified reference id, a verified software page and at least one verified usage quote with location.

## Deployment study 2026-10-19 (appended; the sections above are unchanged)

Added by the Bayesian deployment agent (`MASTER_Methodology_and_Plan/deployment_20261019/BAYES/`). Facts read in package source; "l." is a line of the named file. Nothing was installed or run on NOTS; NOTS checks were read-only.

**Source files read (untrusted data, not executed), SHA-256.**
- `susieR_0.14.2.tar.gz` `ba02322eb1f7a7cc024c9278aa7903a34d8ad5d6f3b12c168374bc6214ed2c6e` (same as the Oct-7 pin). Files: `R/susie.R` `54dd07f4…cfc9`, `R/susie_utils.R` `19bd168a…40a2`, `R/single_effect_regression.R` `90332cd1…8e64`.
- `bayesreg_1.3.tar.gz` `21e19a4b7314d1741d2565963ab5ca86392caba24dda4fe87a9ef55c314da477`. File `R/bayesreg.R` `069618ae…7c8b`.
- `pgdraw_1.1.tar.gz` `05b951b2ecc829d1e99f8dcf216fd4a4803342de7ec036a5c6d9e7777f0c2be8`; `doParallel_1.0.17.tar.gz` `b96a25ad105a654d70c7b4ca27290dc9967bc47f4668b2763927a886b178abd7`.
- `SSLASSO_1.2.3.tar.gz` re-downloaded: `67fb4a881d0b274b2cf00ce7f40d9e6f964aa7f051094078e0bc1b058cd540c1`, identical to the Oct-7 vendor manifest. Oct-7 vendor files read: `SSLASSO/R/SSLASSO.R` `902eadf6…648e`, `SSLASSO/src/SSL_gaussian.c` `34f52385…53dc`, `SSLASSO/src/SSL_functions.c` `7b14e009…4027`, `patched/SSLASSO/src/SSL_gaussian.c` `dfa13ff4…d56f`.
- R trunk `src/nmath/{rgamma,sexp,snorm,rnorm,rexp}.c` (github.com/wch/r-source, fetched 2026-10-19; identity with R 4.5.2 not checked).
- Local copies: `C:/Users/felip/Documents/bench_scratch_20261019/bayes/{dl,src,rsrc}/`.

**susieR 0.14.2.**
- `intercept = FALSE, standardize = FALSE`: `compute_colstats(X, center = intercept, scale = standardize)`; y centred only if `intercept` (`susie.R` l. 369–383).
- Initial V = `scaled_prior_variance`·var(y), σ² = var(y) (`initialize.R` l. 52–90); lower bound default `var(drop(y))/1e4` (`susie.R` l. 323).
- Stopping: `if ((elbo[i+1] - elbo[i]) < tol) converged = TRUE` (a decrease also stops); warning and `converged = FALSE` at `max_iter` (`susie.R` l. 431–455).
- PIP = 1 − ∏ over effects with V > `prior_tol` of (1 − α) (`susie_utils.R` l. 410–441); credible sets use a hard-coded `V > 1e-9` (l. 279) and subsample 100 members with `sample()` for purity when a set is larger (l. 495).
- EB prior variance: Brent on log V in [−30, 15]; keep the old V if worse; V = 0 if loglik(0) + `check_null_threshold` ≥ loglik(V) (`single_effect_regression.R` l. 135–175).
- `warning_message()` uses `message()` (`susie_utils.R` l. 986–995).
- `susie_auto`: defaults `max_iter = 100`, `tol = 1e-2`; tests `L <= L_max` before doubling (`susie_zzz_auto.R` l. 75–105).
- NOTS (read-only, 2026-10-19): installed body matches the source on the stopping test, `susie_get_pip`, and the 1e-9 threshold in `susie_get_cs`.

**SSLASSO 1.2.3 / 1.2.3.9001.**
- Wrapper: centres X (`scale(X, center = TRUE, scale = FALSE)`, l. 123) and y (l. 127); it does **not** scale X (rescaling commented out, l. 186–191). This corrects the A2 caveat in §1 above ("standardizes X"), which the master already corrected.
- Default ladder `lambda0 <- seq(1, n, length = nlambda)`, `lambda1 <- lambda0[1]` (l. 130–138); σ initial `sqrt(df*ncp/(df+2))`, ncp = sd(y)²·qchisq(0.1, 3)/3, floor sd(y)²/n (l. 154–166); `.Call("SSL_gaussian", XX, yy, beta.init, penalty, variance, lambda1, lambda0, theta, sigma, min_sigma2, a, b, eps, max.iter, counter)` (l. 169–171); `$model` = support at the last λ0 (l. 205).
- C: Gram branch iff p < min(n, max_iter), with the `i = 1` bug (upstream `SSL_gaussian.c` l. 159–184); the patch sets `thres = 0` (patched l. 163). At n = 200, p ≥ 500 both builds use the residual branch.
- θ ← (q + a)/(a + b + p) (`SSL_functions.c` l. 73–87); σ² ← RSS/(n + 2) (l. 102–113); convergence = relative change ≤ eps for all coordinates (l. 36–53).
- σ² re-estimated at a point only if the previous point took < 100 sweeps; capped previous point resets σ² (`SSL_gaussian.c` l. 204–226).
- At a capped point θ, σ may stay NaN and the loss element is not written (l. 104–114, 467–474). A p × p buffer is allocated at every p (l. 144).
- NOTS: patched 1.2.3.9001 in `/home/fb31/projects/BVS/library_portable`, built R 4.5.2 2026-10-05; `SSL_gaussian` registered with 15 parameters.

**bayesreg 1.3.**
- Sampler: `if (p/n >= 2) mvnrue = F` (l. 416–423): Rue when p/n < 2, Bhattacharya et al. otherwise; at n = 200 both p = 500 and 1000 use Bhattacharya.
- Standardisation: columns centred and divided by sd·√(n − 1) (unit length) (l. 389–390, 2145–2174); draws back-transformed (l. 742–747).
- `fit$beta` is p × n.samples (l. 527, 634, 742, 854, 1134).
- Formula interface: `model.matrix(formula, data)` then `X[, -1]` unconditionally (l. 342, 362); intercept always sampled with a flat prior (l. 21, 883–900).
- Priors/conditionals: σ² ~ IG((n + p)/2, …) (l. 908–912), i.e. π(σ²) ∝ 1/σ²; τ², ξ and λ², ν inverse-gamma auxiliaries for half-Cauchy scales (l. 998–1030).
- Cores: `n.cores = min(detectCores() - 1, n.cores)` (l. 543–561); with 1 core a single chain runs on R's global RNG (l. 575–596).
- `summary.bayesreg`: `PerSD = F` (l. 1814) and `stats::quantile(s, c(CI.low, CI.high))` (l. 2054).
- In the Bhattacharya branch `mu.beta` is the mean of the draws (`r$m = r$x`, l. 2334–2335). bayesreg's ESS uses an un-padded FFT autocorrelation (l. 1211–1276).
- `prior = "rr"` also samples τ² with a half-Cauchy prior (l. 998–1007).
- Dependencies (DESCRIPTION): Depends pgdraw (≥ 1.0), doParallel (≥ 1.0.16), foreach (≥ 1.5.1); NAMESPACE imports all three. NOTS 2026-10-19: bayesreg, pgdraw, doParallel not installed; Rcpp 1.1.2, foreach 1.5.2, iterators 1.0.14, coda 0.19.4.1 installed.

**R RNG (trunk source).** `rgamma(a, scale)`: the rejection loop depends on a only; the result is scaled (`rgamma.c` l. 55–214); returns early without drawing for NaN, non-positive or infinite parameters (l. 89–95). `exp_rand` has no parameter (`sexp.c`). Inversion normals use two uniforms per draw (`snorm.c` l. 265–270).

**Timing (local, single thread).** numpy emulation of the matrix work of one Bhattacharya draw: 2.4 ms (p = 500), 3.4 ms (p = 1000) at n = 200 (`bench_scratch_20261019/bayes/scripts/time_bhat.py`, MKL BLAS, 2026-10-19). An EST basis only; bayesreg's R overhead is not included.
