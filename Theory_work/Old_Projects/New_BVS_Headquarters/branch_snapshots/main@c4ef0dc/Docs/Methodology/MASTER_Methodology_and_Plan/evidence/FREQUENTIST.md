# Frequentist variable-selection benchmarks for the n = 200 study (Regime L: p = 30; Regime H: p = 500, 1000)

Compiled 2026-10-19. This document builds on three earlier pieces of work:

- `Papers/VS_Benchmarks_Independent_Review_20261003/BENCHMARK_RECOMMENDATION.md`, a review of 108 papers for n = 100, p = 30;
- `Papers/VS_2020_Comparators_20261006/SUMMARY.md`;
- the p = 500 panel already run in `Experiment/Experiments_October_14_Benchmarks/` (Lasso CV-min/1se; Lasso/MCP/ABESS with EBIC, gamma 0.5 and 1).

It changes the frequentist part of that list for p > n. Every reference, software version and usage quote below was opened on 2026-10-19. The verbatim quotes, with file and section, are in `notes_frequentist/EVIDENCE_LOG.md`. `notes_frequentist/check_quotes.py` re-matches all 23 quotes against the saved source text (23/23 OK). Sources are saved under `notes_frequentist/sources/`. No simulations were run.

**What changes at p > n.**

- Fixed-X knockoffs and BH on full-model OLS p-values need n > p. The R `knockoff::create.fixed` stops with "Input X must have dimensions n > p". They are therefore Regime L only.
- Exact best subset is infeasible at p = 500 to 1000. COMBSS dropped MIO at p = 1000 "due to time computational constraints". It is replaced by ABESS in Regime H.
- The FDR slot in Regime H becomes model-X knockoffs with an estimated covariance. This is the standard p > n replacement in recent FDR papers (Xing et al. 2023; Dai et al. 2023; Machkour et al.; Huang et al.).
- Stability selection is added as the resampling and error-control paradigm.

> Lead edit 2026-10-19: truth sizes updated from 6 to 5 (L) / 14 (H) after the design change; original saved in notes_frequentist/FREQUENTIST_as_delivered.md.

## 1. Recommended panel (7 slots)

Common conventions apply to every slot.

- **Data handling.**
  - Use the same (X, y) as the SMC.
  - X is centred and scaled; y is uncentred.
  - Fit with no intercept, and turn off package standardisation where possible (`intercept = FALSE, standardize = FALSE` in glmnet).
  - For ncvreg, which always centres and standardises, use the exact algebraic compensation already validated in `Experiments_October_14_Benchmarks/METHODS_REVIEW.md` (lambda/s, shape·s², s = sqrt((n-1)/n)).
- **Cross-validation.** CV-tuned methods use the same saved 10 folds per dataset, and those folds are identical across signal scales c.
- **EBIC.** EBIC means `n·log(RSS/n) + k·log n + 2γ·log C(p,k)` (Chen & Chen 2008, doi:10.1093/biomet/asn034). It is evaluated on zero-intercept OLS refits of each distinct support on the method's path.
  - The null model is eligible.
  - Supports are capped at 100 in Regime H and at 30 (the full model) in Regime L.
  - This is exactly the Oct-14 rule. γ = 0 is BIC.
- **No oracle information.** No method receives the true size (5 in L, 14 in H), the true support, block labels, or the generating Σ.
- **Compute.** One thread; package seeds are recorded.

| # | Method | Paradigm | Regime | Reference (verified id) | Software, version, date (verified) | Tuning / selection rule (non-oracle) | Evidence of use with p > n (paper, location) | Caveats |
|---|---|---|---|---|---|---|---|---|
| 1 | **Lasso** | convex ℓ1 | L + H | Tibshirani 1996, JRSS-B 58(1) 267-288, doi:10.1111/j.2517-6161.1996.tb02080.x; algorithm Friedman, Hastie & Tibshirani 2010, JSS 33(1), doi:10.18637/jss.v033.i01 | `glmnet` 5.1, CRAN 2026-09-24 | `cv.glmnet(alpha=1, intercept=FALSE, standardize=FALSE, foldid=common)`. **Primary arm: λ_min.** Pre-declared arms from the same fit: λ_1se, and EBIC(γ=1) on the path (as Oct-14). | Hastie, Tibshirani & Tibshirani 2020, Stat. Sci. 35(4), doi:10.1214/19-STS733, §3.1: "high-5: n = 50, p = 1000, s = 5" and "we run the lasso, relaxed lasso, forward stepwise selection, and best subset selection". Zhu et al. 2020 PNAS (ABESS), Simulation, "High-Dimensional Case": LASSO via glmnet with SIC and CV, n = 500, p up to 2,500. | CV-min is prediction-tuned and over-selects. Hazimeh & Mazumder 2020 §5.3.1: "tuning parameter selection based on prediction error makes the Lasso select models with many nonzero coefficients". Expect near-zero exact recovery for λ_min, so always report all three arms. Irrepresentability is likely violated in S3/S4. |
| 2 | **Elastic net** | convex ℓ1+ℓ2, correlation-aware | L + H | Zou & Hastie 2005, JRSS-B 67(2) 301-320, doi:10.1111/j.1467-9868.2005.00503.x | `glmnet` 5.1 (2026-09-24) | `cv.glmnet` for each α ∈ {0.1, 0.25, 0.5, 0.75, 0.9} on the common folds. Choose (α, λ) jointly by minimum CV error; support = nonzeros. EBIC(γ=1) on the chosen α's path is a sensitivity. | Hazimeh & Mazumder 2020, Oper. Res. 68(5), doi:10.1287/opre.2019.1919, §5.1/§5.3: "Elastic Net ... We use the implementation of glmnet", with p = 1000 and n swept from 100 to 1000. Kim, Wang, Carbonetto & Stephens 2024, JMLR 25(185), §5.1 Table 1 and §5.2: "n = 500 and p = 1,000". | The grouping effect pulls in same-block proxies (S3-S6). That is informative, not a bug. It is the slowest of the convex slots (Kim et al. §5.4.4: EN "was considerably slower ... because we tuned both of the Elastic Net parameters by CV"). |
| 3 | **Adaptive lasso** | weighted convex (oracle-property penalty) | L + H | Zou 2006, JASA 101(476) 1418-1429, doi:10.1198/016214506000000735 | `glmnet` 5.1 (`penalty.factor`) | Initial estimate: ridge, `cv.glmnet(alpha=0)` at λ_min on the common folds. Weights w_j = 1/\|β̂_ridge,j\| (γ = 1). Then `cv.glmnet(alpha=1, penalty.factor=w)`, primary λ_min, with EBIC(γ=1) on the path as a sensitivity. Ridge, not OLS, so the same rule works when p > n. | Freijeiro-González, Febrero-Bande & González-Manteiga 2022, Int. Stat. Rev. 90(1), doi:10.1111/insr.12469, §4.1. This is a neutral comparison with p = 100 and n = 25, 50 (p > n): "Adaptive LASSO (AdapL): glmnet". It found AdapL the only method that "selects the complete set S without including any noise ... for a large enough value of n". Nouraie, Zhu & Muller 2025 (arXiv:2511.02306, preprint), §3, n = 100, p = 1000: "Adaptive Lasso with Lasso initial values ... Adaptive Lasso with univariate regression initial values". | Weights computed on the full data and then CV'd ignore weight uncertainty. Nested weights inside folds are an optional sensitivity. Ridge weights at p = 1000 are dense and small; check in the pilot that the selection is not driven by weight ties. |
| 4 | **Nonconvex penalty: MCP** (SCAD from the same package) | folded-concave | L + H | MCP: Zhang 2010, Ann. Statist. 38(2) 894-942, doi:10.1214/09-AOS729. SCAD: Fan & Li 2001, JASA 96(456) 1348-1360, doi:10.1198/016214501753382273. Algorithm: Breheny & Huang 2011, Ann. Appl. Stat. 5(1), doi:10.1214/10-AOAS388 | `ncvreg` 3.16.0, CRAN 2025-11-06 | `ncvreg(penalty="MCP", gamma=3)` with the Oct-14 scale compensation. **Primary:** EBIC(γ=1) in Regime H (continuity with the Oct-14 p = 500 panel) and BIC (γ=0) in Regime L. EBIC(0.5) and `cv.ncvreg` λ_min are sensitivities. SCAD (γ=3.7) under the same rules is a sensitivity. | Zhu et al. 2020 PNAS, "High-Dimensional Case": "LASSO ( 4 ), SCAD ( 6 ), and MCP ( 7 ) ... implemented in R packages glmnet and ncvreg . For all of these methods, we use SIC ... We also consider cross-validation", n = 500, p ∈ {500, 1500, 2500}. Huang, Muller & Tarr (arXiv:2505.22012v2, 2026), §4: SCAD via ncvreg at 10-fold-CV λ, with (n, p) = (20, 1000) and (100, 500). Kim et al. 2024 JMLR, Table 1. | Pathwise local solution with no global-optimum certificate. Keep convergence flags. Zhu et al. report that "the MCP and SCAD underestimate the model size" under SIC. |
| 5 | **Best subset / L0**: exact best subset (L), ABESS (H) | ℓ0 / subset search | L: leaps exact; H: ABESS | Best subset by branch and bound: Furnival & Wilson 1974, Technometrics 16(4) 499-511, doi:10.1080/00401706.1974.10489231. ABESS: Zhu, Wen, Zhu, Zhang & Wang 2020, PNAS 117(52) 33117-33123, doi:10.1073/pnas.2014241117 | L: `leaps` 3.2, CRAN 2024-06-10 (`regsubsets(method="exhaustive", nvmax=30, intercept=FALSE, really.big=TRUE)`). H: `abess` 0.4.11, CRAN 2025-12-08 | **L:** exact RSS-best subset of each size 0..30, chosen by **BIC** (as in `SMC_Composite_Likelihood_Methodology.tex` §Benchmarks), with EBIC(0.5, 1) as sensitivities. **H:** ABESS over sizes 0..100 with no screening (`screening.num=NULL`; see the Oct-14 0.4.11 bug note), no normalisation, centred y; external **EBIC(γ=1)** primary, 0.5 as a sensitivity. The package's internal GIC (`tune.type` default `"gic"`) is a sensitivity. | L: Zhu et al. 2020 PNAS, "Low-Dimensional Case", Table 1: "all-subsets regression (ASR), which exhaustively searches ... via an efficient branch-and-bound algorithm ... We use SIC (ASR-SIC)". H: Hazimeh, Mazumder & Nonet 2023, JMLR 24 (L0Learn), §4 Table 1: "we compare with glmnet, ncvreg, picasso, and abess", n = 1000, p ∈ {10^3, 10^4, 10^5}. | Exact search is infeasible at p ≥ 500; COMBSS (Stat. Comput. 2024, §7.1) dropped MIO at n = 100, p = 1000. ABESS has no global certificate in finite samples. At p = 30, time the exhaustive `leaps` search in the pilot. Branch and bound is exact, but its cost is design-dependent and was not measured here. |
| 6 | **Knockoff filter**: fixed-X (L), model-X with estimated Σ (H) | finite-sample FDR control | L: fixed-X; H: model-X (second-order) | Fixed-X: Barber & Candès 2015, Ann. Statist. 43(5) 2055-2085, doi:10.1214/15-AOS1337. Model-X: Candès, Fan, Janson & Lv 2018, JRSS-B 80(3) 551-577, doi:10.1111/rssb.12265. Robustness to estimated Σ: Barber, Candès & Samworth 2020, Ann. Statist. 48(3), doi:10.1214/19-AOS1852. Construction: Spector & Janson 2022, Ann. Statist. 50(1), doi:10.1214/21-AOS2104 | R `knockoff` 0.3.6 (CRAN 2022-08-15); Python `knockpy` 1.3.5 (PyPI 2025-07-12) | **L (n = 200 ≥ 2p = 60):** `knockoff.filter(X, y, knockoffs=create.fixed, statistic=stat.glmnet_lambdasmax, fdr=q, offset=1)`. This is the signed-max lasso statistic, which respects fixed-X sufficiency; no CV statistic is used. **H:** Gaussian model-X knockoffs with Σ estimated from X only (Ledoit-Wolf; `knockpy` `ksampler="gaussian"`, `knockoff_kwargs={"method":"mvr"}`, `fstat="lasso"` CV coefficient difference). **Levels:** q ∈ {0.1, 0.2}, both offset 1 (knockoff+, FDR) and offset 0. The **primary** level is q = 0.2, offset 1, for the reason given in the next column. | L: Xing, Zhao & Liu 2023, JASA 118(541), doi:10.1080/01621459.2021.1923510, §6.1: "the knockoff filter when p < n/2", n = 1000, p = 300. H: same paper, §6.2, p = 1000, n = 300: "the second-order knockoffs with estimated covariance matrix as implemented in the R package knockoff. Note that the original knockoff method can not be applied when p [≥] n". Dai, Lin, Xing & Liu 2023, JASA 118(544), doi:10.1080/01621459.2022.2060113, §4.1: "the covariance matrix of features is estimated using the R package knockoff", n = 800, p ∈ {1000, 2000}. Machkour, Muma & Palomar (arXiv:2110.06048v7), §IV: "model-X knockoff methods [20] are the benchmarks in high-dimensional settings (i.e., p > n)". | (a) Derived from the knockoff+ threshold definition: knockoff+ can only reject if at least ⌈1/q⌉ variables pass (10 at q = 0.1, 5 at q = 0.2). With 5 signals (L), q = 0.1 is nearly powerless by construction; with 14 (H) the floor matters less. Report this as the price of the guarantee. (b) In H the FDR guarantee is only approximate. Barber et al. 2020: FDR inflation is "proportional to our errors in estimating the distribution of each feature". Machkour et al. Fig. 5: "The model-X knockoff method fails to control the FDR" (offset 0). (c) Spector & Janson: MAC/SDP knockoffs "can be powerless ... including Gaussian linear models with correlated exchangeable features", which is S3/S4. Hence MVR is primary and R's default ASDP/SDP is a sensitivity. Dai et al. also find knockoffs "significantly less powerful ... when [ρ ≥] 0.4" under constant correlation. (d) Knockoffs are random, so fix and record the seed. |
| 6b | *Companion:* **BH on full-model OLS p-values** | marginal FDR on OLS t-tests | **L only** | Benjamini & Hochberg 1995, JRSS-B 57(1) 289-300, doi:10.1111/j.2517-6161.1995.tb02031.x | base R (`lm`, `p.adjust(method="BH")`) | Zero-intercept OLS on all 30 predictors; two-sided t-test p-values; BH at q ∈ {0.1, 0.2}. | Xing et al. 2023 JASA §6.1 (n = 1000, p = 300): "For the BH method, we calculate the z-statistics z1, . . . , zp for the OLS estimates". Machkour et al. §IV, low-dimensional benchmarks: BH, BY, fixed-X knockoffs. | Free to run, and valid because n > p. BH's guarantee under arbitrary dependence of OLS t-statistics is not claimed here. It is reported as a reference arm, not as a separate slot. |
| 7 | **Stability selection** (complementary pairs) | subsampling with PFER error control | L + H | Meinshausen & Bühlmann 2010, JRSS-B 72(4) 417-473, doi:10.1111/j.1467-9868.2010.00740.x. CPSS: Shah & Samworth 2013, JRSS-B 75(1) 55-80, doi:10.1111/j.1467-9868.2011.01034.x | `stabs` 0.7-1, CRAN 2026-01-31 | `stabsel(X, y, fitfun=glmnet.lasso, cutoff=0.75, PFER=1, sampling.type="SS", B=50, papply=lapply)`. That is complementary pairs, 2B = 100 half-samples (checked in the `stabs` source: `folds <- cbind(folds, rep(1, n) - folds)`), the package's default "unimodal" bound, and one core. Selected set = `$selected`. `cutoff=0.9` is a sensitivity. | Huang, Muller & Tarr (arXiv:2505.22012v2, 2026), §4: a static threshold of 0.75 "through the stabsel package", benchmarked against "the LASSO ..., knockoff, and ... SCAD", with (n, p) = (20, 1000) and (100, 500). Nouraie, Zhu & Muller (arXiv:2511.02306, 2025), §3: methods embedded "in the Stability Selection framework", n = 100, p = 1000. | Both usage papers are preprints from stability-selection authors. Freijeiro-González et al. 2022 excluded it because "a proper choice of the threshold value seems to depend on the sample size ... as well as the sparsity". The PFER target fixes the per-subsample model size q. In the pilot, check the q reported by `stabsel` in both regimes. If q is near or below the true size (5 in L, 14 in H), the bound itself caps selections and makes exact recovery impossible, so state it. |

**Slot count.** Seven slots: Lasso, EN, adaptive lasso, nonconvex, L0, knockoffs, stability selection. Six run in both regimes. Slots 5 and 6 change implementation between regimes, and BH-OLS (6b) is a Regime-L companion only.

## 2. Sensitivities (variants of the slots above, not separate benchmarks)

| Sensitivity | Applies to | Regime | Rule | Verified basis |
|---|---|---|---|---|
| Relaxed lasso | slot 1 | L + H | `cv.glmnet(..., relax=TRUE)`; (λ, γ_relax) by CV min | Meinshausen 2007, CSDA 52(1) 374-393, doi:10.1016/j.csda.2006.12.019. `relax` argument present in glmnet 5.1 source. Used by Hastie et al. 2020 §3.1 and Hazimeh & Mazumder 2020 §5.1 at p = 1000. |
| λ_1se; EBIC(γ = 0.5) on the path | slots 1-4 | L + H | as named | Oct-14 panel convention. Chen & Chen 2008 verified. |
| SCAD (γ = 3.7) | slot 4 | L + H | same tuning rules as MCP | Fan & Li 2001. Zhu et al. 2020 (above). |
| `cv.ncvreg` λ_min | slot 4 | L + H | common folds | Zhu et al. 2020 ("We also consider cross-validation"). |
| L0Learn (L0L2, CDPSI) | slot 5 | L + H | `L0Learn.cvfit(X, y, penalty="L0L2", algorithm="CDPSI", nFolds=10, intercept=FALSE, maxSuppSize=100, seed=<recorded>)`; minimum CV error over (λ, γ). Arguments checked in the CRAN-mirror source. L0Learn draws its own folds from `seed`, so its folds differ from the common folds; record this. | Hazimeh & Mazumder 2020 doi:10.1287/opre.2019.1919. `L0Learn` 2.1.0 (CRAN 2023-03-07; no release since). Used by Moka et al. 2024 Stat. Comput. §7 (n = 100, p = 1000) and Kim et al. 2024 JMLR. |
| ABESS in Regime L | slot 5 | L | as in H, with sizes 0..30 | Links the two regimes and checks ABESS against the exact optimum (the Zhu et al. 2020 Table 1 design). |
| ABESS internal GIC | slot 5 | H | `tune.type="gic"` (package default) | `abess` 0.4.11 source. |
| Knockoffs: offset 0; q = 0.1; R default ASDP/equi second-order construction | slot 6 | L/H | `knockoff::create.second_order(X, method="asdp" or "equi")`, which shrinks automatically when the sample covariance is not PD; `stat.glmnet_coefdiff` | Package source verified. Used by Xing et al. 2023 §6.2, Dai et al. 2023 §4.1 (equi) and Huang et al. 2026 §4 (ASDP when p > 500). |
| Fixed-X knockoffs with MVR (`knockpy`, `ksampler="fx"`, `fstat="lsm"`) | slot 6 | L | q, offset as primary | `knockpy` 1.3.5 docstring: 'fx' = "Fixed-X knockoffs"; 'lsm' = "signed maximum of the lasso path statistic as in Barber and Candes 2015". |
| SIS / ISIS + SCAD | screening before a nonconvex fit | **H only** | `SIS(X, y, family="gaussian", penalty="SCAD", tune="ebic", gamma.ebic=1, iter=TRUE, parallel=FALSE)` | Fan & Lv 2008, JRSS-B 70(5) 849-911, doi:10.1111/j.1467-9868.2008.00674.x. `SIS` 1.5 (CRAN 2026-03-14); defaults verified in source (`tune` default "bic", `gamma.ebic=1`, `iter=TRUE`, `parallel=TRUE`, so set it to FALSE). Usage: Sanyal & Prempeh (arXiv:2609.24945, 2026) §4.1.2, "one-pass SIS followed by the same selector", n ∈ {200, 500, 800}, p ≥ 10,000. Not a primary slot: at p ≤ 1000, slots 1-5 run on all p directly, so screening is not needed. |
| Stability selection, cutoff 0.9 / `sampling.type="MB"` | slot 7 | L + H | as named | `stabs` source. |

## 3. Considered and rejected

| Candidate | Reason (evidence) |
|---|---|
| Fixed-X knockoffs in Regime H | Infeasible: `create.fixed` stops with "Input X must have dimensions n > p". Xing et al. 2023 §6.2: "the original knockoff method can not be applied when p [≥] n". |
| BH on OLS p-values in Regime H | The OLS fit does not exist for p > n. Kept in Regime L only (6b). |
| Exact best subset (leaps/MIO) in Regime H | Computationally infeasible at p ≥ 500. Moka et al. 2024 §7.1 dropped MIO at p = 1000. The `bestsubset` (Gurobi MIO) package used by Hastie et al. is not on CRAN (the CRAN lookup returned no package page) and needs a Gurobi licence. ABESS fills the slot. |
| Forward stepwise | Dominated by exact best subset at p = 30 (prior review §4). In H it is the same ℓ0 paradigm as ABESS. Hazimeh & Mazumder 2020 §5.3.1 report FStepwise recovery "around 0.3 even when n = p = 1000" at ρ = 0.9. Optional, not recommended. |
| Debiased/desparsified lasso + BH | Main software is gone: `hdi` was archived on CRAN 2026-07-10 ("requires archived package 'scalreg'"). Dai et al. 2023 §3.1: debiased-lasso "null p-values may appear highly non-uniform in finite-sample cases". References verified: van de Geer, Bühlmann, Ritov & Dezeure 2014, AoS 42(3), doi:10.1214/14-AOS1221; Zhang & Zhang 2014, JRSS-B 76(1), doi:10.1111/rssb.12026. |
| Multi-split p-values (Meinshausen et al. 2009) + BH | Uses `hdi::multi.split`, which is archived (see above). Dai et al. 2023 ran it ("MBHq"), but with no maintained package it is not included. |
| Post-selection inference (`selectiveInference`) | `selectiveInference` 1.2.5 has had no release since 2019-09-07. Dai et al. 2023 §3.1: the theory "is mostly developed case by case". |
| Data splitting / multiple data splitting (DS/MDS), Gaussian mirror | Recent and powerful under correlation (Dai et al. 2023 §4.1; Xing et al. 2023). But no CRAN package was verified, and they were run as comparators mainly within their authors' group. Better as a later FDR extension than as a panel slot. |
| T-Rex selector | `TRexSelector` 1.0.0 (CRAN 2024-02-23) exists. It was run mainly in its authors' own papers in what was read here, and it targets FDR like slot 6. Its journal venue is UNVERIFIED. |
| Scaled / square-root lasso, Dantzig selector | Run in Freijeiro-González et al. 2022 §4.1. `scalreg` was archived on 2026-07-10; `flare` 1.8 (CRAN 2026-02-19) is maintained. Same convex ℓ1 paradigm as slot 1, with no distinct selection behaviour for known-σ-free tuning here. |
| SLOPE | `SLOPE` 2.1.1 (CRAN 2026-08-29) is maintained. It did not appear as a comparator in any of the 13 p > n papers opened here. Not adopted. |
| Group lasso / group knockoffs / sparse group lasso | Need group labels. The true blocks are generating-Σ information (oracle). |
| Random forest / boosting importance | Nonlinear learners in a correctly specified linear model. Prior review §4: run in 1 of 108 papers. |
| uniLasso (2025) | The prior review §4 reports that it fails on opposite-sign correlated pairs. Not re-verified here (UNVERIFIED). Too new to be a standard comparator. |

## 4. Sources

V = opened on 2026-10-19 from the primary source: Crossref record, arXiv/journal/PMC full text, CRAN/PyPI page or package source. U = not opened or not confirmed. Local copies are under `notes_frequentist/sources/`.

### Method references (metadata from the Crossref API: `https://api.crossref.org/works/<doi>`)
| # | Reference | Flag |
|---|---|---|
| R1 | Tibshirani (1996) JRSS-B 58(1) 267-288, doi:10.1111/j.2517-6161.1996.tb02080.x | V |
| R2 | Friedman, Hastie & Tibshirani (2010) JSS 33(1), doi:10.18637/jss.v033.i01 | V |
| R3 | Zou & Hastie (2005) JRSS-B 67(2) 301-320, doi:10.1111/j.1467-9868.2005.00503.x | V |
| R4 | Zou (2006) JASA 101(476) 1418-1429, doi:10.1198/016214506000000735 | V |
| R5 | Fan & Li (2001) JASA 96(456) 1348-1360, doi:10.1198/016214501753382273 | V |
| R6 | Zhang (2010) Ann. Statist. 38(2) 894-942, doi:10.1214/09-AOS729 | V |
| R7 | Breheny & Huang (2011) Ann. Appl. Stat. 5(1) 232-253, doi:10.1214/10-AOAS388 | V |
| R8 | Furnival & Wilson (1974) Technometrics 16(4) 499-511, doi:10.1080/00401706.1974.10489231 | V |
| R9 | Zhu, Wen, Zhu, Zhang & Wang (2020) PNAS 117(52) 33117-33123, doi:10.1073/pnas.2014241117; full text https://pmc.ncbi.nlm.nih.gov/articles/PMC7777147/ | V |
| R10 | Hazimeh & Mazumder (2020) Oper. Res. 68(5) 1517-1537, doi:10.1287/opre.2019.1919; text read from arXiv:1803.01454v3 | V (journal text not compared) |
| R11 | Chen & Chen (2008) Biometrika 95(3) 759-771, doi:10.1093/biomet/asn034 | V (metadata only) |
| R12 | Barber & Candès (2015) Ann. Statist. 43(5) 2055-2085, doi:10.1214/15-AOS1337 | V (metadata) |
| R13 | Candès, Fan, Janson & Lv (2018) JRSS-B 80(3) 551-577, doi:10.1111/rssb.12265 | V (metadata) |
| R14 | Barber, Candès & Samworth (2020) Ann. Statist. 48(3) 1409-1431, doi:10.1214/19-AOS1852; abstract https://arxiv.org/abs/1801.03896 | V |
| R15 | Spector & Janson (2022) Ann. Statist. 50(1) 252-276, doi:10.1214/21-AOS2104; abstract https://arxiv.org/abs/2011.14625 | V |
| R16 | Benjamini & Hochberg (1995) JRSS-B 57(1) 289-300, doi:10.1111/j.2517-6161.1995.tb02031.x | V (metadata) |
| R17 | Meinshausen & Bühlmann (2010) JRSS-B 72(4) 417-473, doi:10.1111/j.1467-9868.2010.00740.x | V (metadata) |
| R18 | Shah & Samworth (2013) JRSS-B 75(1) 55-80, doi:10.1111/j.1467-9868.2011.01034.x | V (metadata) |
| R19 | Meinshausen (2007) CSDA 52(1) 374-393, doi:10.1016/j.csda.2006.12.019 | V (metadata) |
| R20 | Fan & Lv (2008) JRSS-B 70(5) 849-911, doi:10.1111/j.1467-9868.2008.00674.x | V (metadata) |
| R21 | van de Geer, Bühlmann, Ritov & Dezeure (2014) Ann. Statist. 42(3) 1166-1202, doi:10.1214/14-AOS1221 | V (metadata) |
| R22 | Zhang & Zhang (2014) JRSS-B 76(1) 217-242, doi:10.1111/rssb.12026 | V (metadata) |

### Usage-evidence papers (full text read; quotes in `notes_frequentist/EVIDENCE_LOG.md`)
| # | Paper | URL read | Flag |
|---|---|---|---|
| U1 | Hastie, Tibshirani & Tibshirani (2020) Stat. Sci. 35(4) 579-592, doi:10.1214/19-STS733 | https://arxiv.org/pdf/1707.08692 (v2) | V (preprint text; journal version not compared) |
| U2 | Hazimeh & Mazumder (2020) Oper. Res., doi:10.1287/opre.2019.1919 | https://arxiv.org/pdf/1803.01454 (v3) | V (preprint text) |
| U3 | Kim, Wang, Carbonetto & Stephens (2024) JMLR 25(185):1-59 | https://arxiv.org/pdf/2208.10910 (v3); venue at https://www.jmlr.org/papers/v25/ | V |
| U4 | Zhu et al. (2020) PNAS (ABESS) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7777147/ | V |
| U5 | Hazimeh, Mazumder & Nonet (2023) JMLR 24, L0Learn | https://www.jmlr.org/papers/volume24/22-0189/22-0189.pdf | V |
| U6 | Moka, Liquet, Zhu & Muller (2024) Stat. Comput. 34(2), doi:10.1007/s11222-024-10387-8 | https://arxiv.org/pdf/2205.02617 (v3) | V (preprint text) |
| U7 | Freijeiro-González, Febrero-Bande & González-Manteiga (2022) Int. Stat. Rev. 90(1) 118-145, doi:10.1111/insr.12469 | https://arxiv.org/pdf/2012.11470 (v1) | V (preprint text) |
| U8 | Nouraie, Zhu & Muller (2025) "A Stable Lasso" | https://arxiv.org/pdf/2511.02306 (v1) | V (preprint; not peer reviewed) |
| U9 | Huang, Muller & Tarr (2026) "Data-Adaptive Automatic Threshold Calibration for Stability Selection" | https://arxiv.org/pdf/2505.22012 (v2) | V (preprint) |
| U10 | Xing, Zhao & Liu (2023) JASA 118(541) 222-241, doi:10.1080/01621459.2021.1923510 | https://arxiv.org/pdf/1911.09761 (v3) | V (preprint text) |
| U11 | Dai, Lin, Xing & Liu (2023) JASA 118(544) 2503-2520, doi:10.1080/01621459.2022.2060113 | https://arxiv.org/pdf/2002.08542 (v2) | V (preprint text) |
| U12 | Machkour, Muma & Palomar, "The Terminating-Random Experiments Selector" | https://arxiv.org/pdf/2110.06048 (v7) | V for text; **U for journal venue** |
| U13 | Sanyal & Prempeh (2026) "Structured Screen-and-Select for Ultra-High-Dimensional Variable Selection" | https://arxiv.org/pdf/2609.24945 (v1) | V (preprint) |

### Software pages (fetched 2026-10-19)
| Package | Version / date | URL | Flag |
|---|---|---|---|
| glmnet | 5.1 / 2026-09-24 | https://cran.r-project.org/package=glmnet | V |
| ncvreg | 3.16.0 / 2025-11-06 | https://cran.r-project.org/package=ncvreg | V |
| abess | 0.4.11 / 2025-12-08 | https://cran.r-project.org/package=abess | V |
| L0Learn | 2.1.0 / 2023-03-07 | https://cran.r-project.org/package=L0Learn | V |
| leaps | 3.2 / 2024-06-10 | https://cran.r-project.org/package=leaps | V |
| knockoff | 0.3.6 / 2022-08-15 | https://cran.r-project.org/package=knockoff ; source https://github.com/msesia/knockoff-filter | V |
| knockpy | 1.3.5 / 2025-07-12 | https://pypi.org/project/knockpy/ ; source https://github.com/amspector100/knockpy | V |
| stabs | 0.7-1 / 2026-01-31 | https://cran.r-project.org/package=stabs | V |
| SIS | 1.5 / 2026-03-14 | https://cran.r-project.org/package=SIS | V |
| hdi | archived 2026-07-10 | https://cran.r-project.org/package=hdi | V |
| scalreg | archived 2026-07-10 | https://cran.r-project.org/package=scalreg | V |
| selectiveInference | 1.2.5 / 2019-09-07 | https://cran.r-project.org/package=selectiveInference | V |
| TRexSelector | 1.0.0 / 2024-02-23 | https://cran.r-project.org/package=TRexSelector | V |
| SLOPE | 2.1.1 / 2026-08-29 | https://cran.r-project.org/package=SLOPE | V |
| flare | 1.8 / 2026-02-19 | https://cran.r-project.org/package=flare | V |
| bestsubset (MIO) | not on CRAN | https://cran.r-project.org/package=bestsubset (no package page returned) | V (absence) |

### Unverified items
- Journal venue of U12 (T-Rex): not confirmed.
- uniLasso failure claim: carried over from the prior review, not re-opened.
- Run times: none measured or claimed. These include exhaustive `leaps` at p = 30, knockpy MVR at p = 1000, and EN tuning; each needs pilot timing.

**Counts.**

- Verified: 22 method references, 13 usage papers and 16 software checks, 51 in total.
- Unverified: 2 items (U12 venue; uniLasso claim).
- Every recommended slot (1-7 and 6b) has a verified reference id, a verified software page, at least one verified p > n (or, for Regime-L-only arms, n > p) usage quote with its location, and a rule that uses no oracle information.


## Deployment study 2026-10-19

Added 2026-10-19 by the F1–F5 deployment study (`deployment_20261019/FREQ/DEPLOY_F.md`). Nothing above this section was changed. Every fact below was read from the extracted CRAN source tarball named, or printed read-only on NOTS (login node, `module load GCC/14.3.0 R/4.5.2`, `R_LIBS_USER=$HOME/R/library`). No code was run. These facts back the tag [V-src] used in `DEPLOY_F.md`.

### Tarballs

Downloaded from `https://cran.r-project.org/src/contrib/` on 2026-10-19 into `C:/Users/felip/Documents/bench_scratch_20261019/freq/tarballs/` and extracted into `.../freq/src/` (outside the project; untrusted data, read only).

| Tarball | SHA-256 | Same as Oct-7 `vendor/` copy |
|---|---|---|
| glmnet_5.1.tar.gz | a6c23c906806f89a451de30b202e5bf088577f4da260d0b7f8887a7df3f22778 | yes |
| ncvreg_3.16.0.tar.gz | 354ec5c7166ae0b166878b4609fafe4542e2be4f8df936671243d5a8be092145 | (no Oct-7 copy) |
| abess_0.4.11.tar.gz | 44bf69f7504bbd48630af714e8f400f1138753e307fee1dc14db8fab7fe7a31c | yes |

DESCRIPTION: glmnet Version 5.1, Date 2026-09-23; ncvreg Version 3.16.0, Date/Publication 2025-11-06; abess Version 0.4.11, Date/Publication 2025-12-08.

### glmnet 5.1 (paths relative to `glmnet/`)

| Fact | Location |
|---|---|
| Signature defaults: `thresh=1e-7`, `maxit=100000`, `type.gaussian=ifelse(nvars<500,"covariance","naive")`, `lambda.min.ratio=ifelse(nobs<nvars,1e-2,1e-4)`, `control=list()` | `R/glmnet.R` l.389 |
| `thresh`, `dfmax`, `pmax`, `maxit` documented as deprecated; use `control = list(...)` | `R/glmnet.R` l.164–170, l.201–203 |
| Deprecated top-level args are folded into `control` and emit `.Deprecated()` once per session per argument | `R/glmnet.R` l.407–417; `R/glmnet.control.R` l.238–250 |
| `control` overrides are pushed per call and restored by a thunk | `R/glmnet.control.R` l.256–259; registered with `on.exit` at `R/glmnet.R` l.419 |
| Valid control keys include `fdev`, `devmax`, `thresh`, `maxit`, `dfmax`, `pmax` | `R/glmnet.control.R` l.214–218 |
| Defaults `dfmax = nvars + 1`, `pmax = min(2·dfmax + 20, nvars)` | `R/glmnet.control.R` l.270–273 |
| User λ: `flmin = 1`, `ulam = rev(sort(lambda))` | `R/glmnet.R` l.538–540 |
| With `flmin >= 1` the path never stops early (no fdev/devmax/dfmax stop) | `src/glmnetpp/include/glmnetpp_bits/elnet_path/base.hpp` l.307 |
| No intercept: weights normalised to sum 1; y multiplied by sqrt(w); `ys = norm(y)` (= sqrt(mean(y²)) for unit weights); `y /= ys` | `.../elnet_driver/standardize.hpp` l.35–47 |
| `standardize = FALSE`: `xs(j) = 1`; `xv(j)` = squared norm of `x_j·sqrt(w)` | `.../elnet_driver/standardize.hpp` l.53–62 |
| Bounds and user λ divided by ys; λ and coefficients multiplied back by ys (and divided by xs) | `.../elnet_driver/gaussian.hpp` l.430, l.437, l.447–451 |
| Intercept set to 0 unless `intr` | `.../elnet_driver/gaussian.hpp` l.453–459 |
| Penalty factors: clipped at 0 and rescaled to sum to nvars | `.../elnet_driver/base.hpp` l.10–14; doc `R/glmnet.R` l.188 |
| Coordinate update: soft-threshold of u by `penalty·l1_regul`, divided by `x_var + penalty·l2_regul` | `.../elnet_point/internal/base.hpp` l.50–68 |
| Convergence: `dlx = max(x_var·Δβ²) < thr` | `.../elnet_point/internal/base.hpp` l.44–45, l.275 |
| `type.gaussian`: `ka == 2` selects naive | `src/elnet_exp.cpp` l.52 |
| jerr codes: `-m-1` maxit reached at λ m; `-10001-m` pmax exceeded | `.../util/exceptions.hpp` l.14–21 |
| Non-fatal jerr gives an R warning; fatal gives an error | `R/elnet.R` l.50–52 |
| cv.glmnet: full fit, then fold fits on the same user λ (`lambda=glmnet.object$lambda` commented out) | `R/cv.glmnet.raw.R` l.13, l.20, l.48–58 |
| Grouped CV: fold means; infinite losses set to NA | `R/cvcompute.R` l.10 |
| `cvm` weighted mean of fold MSEs; `cvsd` = square root of the weighted mean of squared deviations divided by (N − 1) | `R/cvstats.R` l.6–7 |
| `lambda.min` = largest λ among exact minima; `lambda.1se` = largest λ with `cvm ≤ cvm_min + cvsd_min` | `R/getOptcv.glmnet.R` l.5–12 |
| Generic-family path (`family = gaussian()`) computes λ_max from the gradient with no response rescaling | `R/glmnetFlex.R` l.1040, l.1093 |
| `cv.glmnet` predicts each fold fit at the master grid with `predict(..., s = lambda)` | `R/buildPredmat.default.R` l.18–19 |
| `lambda.interp` clamps requested λ outside a fit's returned path to its end point, so a truncated fold path still gives finite predictions (point found by Astra, verified) | `R/lambda.interp.R` l.21–22 |

### ncvreg 3.16.0 (paths relative to `ncvreg/`)

| Fact | Location |
|---|---|
| Signature: `gamma=switch(penalty,SCAD=3.7,3)`, `alpha=1`, `eps=1e-4`, `max.iter=10000`, `convex=TRUE`, `dfmax=p+1` | `R/ncvreg.R` l.164–167 |
| X always standardised by `std()`; gaussian y always centred | `R/ncvreg.R` l.204, l.209 |
| `std`: column mean and RMS scale sqrt(Σ(x − mean)²/n) | `src/standardize.c` l.27, l.35 |
| User λ sorted decreasing; all points fitted from the first | `R/ncvreg.R` l.223, l.238; `src/gaussian.c` l.81–86 |
| Stop when active count > dfmax or total iterations reach max.iter; remaining λ get NA and are dropped | `src/gaussian.c` l.101–104; `R/ncvreg.R` l.254–259 |
| Warning "Maximum number of iterations reached" when `sum(iter) == max.iter` | `R/ncvreg.R` l.261 |
| Convergence per λ: max coefficient change < `eps·sdy`, sdy = sqrt(mean(yc²)) | `src/gaussian.c` l.87, l.150 |
| Coordinate update with `l1 = λ·m_j·α`, unit-RMS columns (`v = 1`) | `src/gaussian.c` l.133–137 |
| MCP and SCAD threshold functions | `src/ncvreg_init.c` l.86–93, l.95–103 |
| `loss` = residual sum of squares on the internal (centred) response | `src/ncvreg_init.c` l.63–66; `src/gaussian.c` l.207 |
| Coefficients unstandardised by `b/scale`; intercept row 1 | `R/ncvreg.R` l.268–270 |
| `convex.min` from eigenvalues of `X_U'X_U/n − k·I` along the path | `R/convexMin.R` |
| `cv.ncvreg`: fold fits call `ncvreg()` on the training X (re-standardised); `cvse = sd/sqrt(n)` | `R/cv-ncvreg.R` l.139, l.170–171 |

### abess 0.4.11 (paths relative to `abess/`)

| Fact | Location |
|---|---|
| Defaults: `normalize=NULL`, `fit.intercept=TRUE`, `c.max=2`, `support.size=NULL`, `max.splicing.iter=20`, `screening.num=NULL`, `important.search=NULL`, `num.threads=0`, `seed=1` | `R/abess.R` l.302–337 |
| `set.seed(seed)` on entry and `set.seed(NULL)` on exit | `R/abess.R` l.338, l.585 |
| `screening.num = NULL` → `screening = FALSE`; numeric → `screening = TRUE` | `R/initialization.R` l.505–534 |
| C++ gets `screening_size = -1` when `screening_num >= nvars` | `R/abess.R` l.452 |
| R post-processing maps coefficients through `screening_A` when `screening` is TRUE (all-zero path if C++ did not screen) | `R/abess.R` l.565–570 |
| Default support sizes 0..min(p, round(n/log(log n)/log p)) = 0..19 at n = 200, p = 500 and 0..17 at p = 1000 (arithmetic for this study) | `R/initialization.R` l.593–594 |
| Largest support size must be < n | `R/initialization.R` l.607 |
| Default `important.search = min(p, 128)` | `R/initialization.R` l.786–802 |
| Gaussian default `normalize = 1` | `R/initialization.R` l.1089–1093 |
| `important.search ≥ N − size` → full splicing set (`U_size = N`) | `src/Algorithm.h` l.231–234 |
| Outer splicing loop bounded by `max_iter`; it exits after the first pass when `U_size == N`; the exchange loop inside is `while (true)` with no cap (point found by Astra, verified) | `src/Algorithm.h` l.357, l.407–435, l.463–467 |
| An exchange is accepted only if the training loss falls by more than τ = 0.01·k·log(N)·log(log n)/n | `src/Algorithm.h` l.174–181, l.537 |
| No iteration count is returned | `src/workflow.h` l.258–262 |
| Early stop is commented out | `src/path.h` l.112–126 |

### NOTS read-only checks (2026-10-19, loginx3)

- `packageVersion`: glmnet 5.1, ncvreg 3.16.0, abess 0.4.11.
- `formals(glmnet::glmnet)` matches `R/glmnet.R` l.389; `formals(glmnet::glmnet.control)` lists `fdev, devmax, …, factory`; `glmnet:::.resolve_control` exists; `glmnet:::getOptcv.glmnet` prints the code of `R/getOptcv.glmnet.R`.
- `formals(abess:::abess.default)` matches `R/abess.R` l.302–337; `abess:::screening_num.glm` prints the code of `R/initialization.R` l.505–534; `deparse(abess:::abess.default)` contains `set.seed(seed)` and `set.seed(NULL)`.
- `ncvreg:::std` prints the code of `R/std.R`.

### Oct-14 measurements recomputed for this study

From `02_Experiments/E_2026-10-14_p500_studies/Experiments_October_14_Benchmarks/summary/validated_rows.csv` (n = 200, p = 500, old 6-signal truth, 3,000 cases, single-thread NOTS):

| Quantity | Lasso (cv.glmnet + EBIC) | MCP | ABESS |
|---|---|---|---|
| Runtime per case, median / p95 / max (s) | 0.776 / 1.386 / 2.052 | 1.50 / 2.37 / 3.35 | 0.114 / 0.179 / 0.695 |
| Selected size, EBIC(1): median / p95 / max | 6 / 8 / 13 | 6 / 7 / 100 | 6 / 7 / 11 |
| Selected size, EBIC(0.5): median / p95 / max | 6 / 9 / 15 | 97 / 100 / 100 | 7 / 100 / 100 |
| Selected size, CV-min and CV-1se: median / p95 / max | 31 / 66 / 118 and 11 / 24 / 60 | — | — |
| Method failures | 0 | 0 | 0 |

Peak MaxRSS of the Oct-14 pilot array (30 tasks, three methods, one case each): 256.7 MiB (`reviews/pilot_resources_2200771.json`).
