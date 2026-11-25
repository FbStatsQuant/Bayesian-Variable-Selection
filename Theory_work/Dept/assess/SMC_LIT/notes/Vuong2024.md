# Reader notes: Vuong (2024), annealed SMC for joint variable selection and parameter estimation (MSc project, SFU)

## 0. Bibliographic
- Title: "The performance of annealed sequential Monte Carlo sampling as a joint variable selection and parameter estimation method in the linear (mixed) model setting".
- Author: Quang Vuong (B.Sc. UBC 2022). Supervisor Rachel Altman; committee Wei Lin (chair), Haolun Shi, Liangliang Wang (examiner) (p. ii in PDF numbering, roman). Project submitted for the MSc, Dept. of Statistics and Actuarial Science, Simon Fraser University, Spring 2024. No journal, no DOI, no arXiv.
- Source: https://summit.sfu.ca/item/38207. I tried to fetch the landing page (WebFetch) and was blocked by an Anubis bot-protection page ("Access Denied"), so I could not check the SFU record for attachments or other versions. The only file read is the local PDF.
- File read: /home/fb31/SMC_Theory_Department/SMC_LIT/papers/Vuong_2024_SFU_thesis_annealedSMC_VS.pdf, 51 PDF pages (8 front-matter pages i-viii, then thesis pages 1-43; thesis page n = PDF page n+8). All 51 PDF pages read page by page with the Read tool (pages 1-17, 18-34, 35-51). Page numbers below are the PRINTED thesis page numbers (roman for front matter).
- No supplement, no code link in the thesis (I found no code repository cited).

## 1. Coverage log
- i-ii: title page, committee. iii: abstract. iv-v: dedication, acknowledgements. vi-viii: TOC, list of tables (9 tables), list of figures (8 figures).
- p. 1-4 Ch. 1 Introduction: BMA setup and formulas (p. 1-2); why annealed SMC: authors tried RJMCMC in the Barker-Link (2013) Gibbs-equivalent form and found "poor convergence ... computationally inefficient", and direct Monte Carlo evidence calculation "very sensitive to prior hyperparameter selection" (p. 3); survey of EMVS, Bayesian adaptive sampling, split-and-merge, population MCMC/evolutionary MC (p. 3); annealed SMC definition and aim "minimally tuned" scheme (p. 3-4).
- p. 5 Ch. 2 Motivating example: CAYACS data (BC Cancer); data not released in time, so no real-data application.
- p. 6-8 Ch. 3.1 Linear mixed model (random-intercept; model indicator zeta; auxiliary parameter psi of constant dimension), priors.
- p. 8-10 Ch. 3.2.1 Construction: tempered targets, forward/backward kernels, SMC algorithm steps 1-3, ESS-triggered resampling, importance-sampling interpretation.
- p. 10-11 Ch. 3.2.2 Choice of L_{t-1} and K_t: pi^t-invariant backward kernel, incremental weights, symmetric random-walk MH forward kernel (4 blocks), resample-before-propagate ordering.
- p. 12 Ch. 4 intro: performance measures; selection threshold 0.5.
- p. 13-14 Sec. 4.1 fixed-effects benchmark (n=1000, p=3, 500 datasets), Tables 4.1-4.3.
- p. 14-24 Sec. 4.2 full factorial experiment (p=6; factors SS, SNR, Prop, Cor; 200 datasets per cell); models for responses (logistic GLM, ANOVA, quasi-binomial); Figs 4.1-4.8.
- p. 24-25 Sec. 4.3 mixed-effects case (random intercept; n=1000 subjects x 4 times; 100 reps), Tables 4.4-4.6.
- p. 26-27 Sec. 4.4 effect of the number of particles (6000 vs 1000), Tables 4.7-4.9.
- p. 28-32 Ch. 5 Discussion.
- p. 33-34 Bibliography (18 references). p. 35-43 Appendix A: analysis-of-deviance/variance Tables A.1-A.19. Nothing else (no proofs appendix, no code).

## 2. Model and prior
- Likelihood (p. 6-7): Gaussian linear MIXED model, random intercept: Y_i = X_i beta + b_i 1 + eps_i, b_i ~ N(0, sigma_b^2), eps_i ~ N(0, sigma^2 I). Fixed-effects case is the special case without b_i. Predictors standardised (p. 7-8).
- Model space (p. 7): Omega = {0,1}^p, all 2^p subsets, NO size cap. Selection of fixed effects only (p. 2-3).
- Model prior (p. 7): uniform, P(zeta)=2^{-p}. They say other priors "can be used" (no multiplicity correction; stated as having "minimal impact on the details"). NOT beta-binomial.
- Coefficients (p. 7): a constant-dimension auxiliary vector psi = (psi_0, ..., psi_p); beta = psi on the active coordinates, beta = 0 elsewhere. psi_zeta ~ MVN(0, tau diag(v, I)), psi_{-zeta} ~ MVN(0, sigma_u^2 I) (inactive coordinates are drawn from a pseudo-prior). NOT a g-prior; the coefficient prior variance tau (=1, standardised predictors) does not scale with sigma^2 and not with n. v=100 (intercept), sigma_u^2=5 (p. 13). The author notes Bartlett-paradox issues and that tau "remains at the discretion of the analyst" (p. 29-30).
- Variance priors (p. 7): sigma^2 ~ InvGamma(alpha, nu), sigma_b^2 ~ InvGamma(alpha_b, nu_b); benchmark alpha=2.1, nu=100 (p. 13); mixed case alpha_b=200, nu_b=2.1 (p. 25; the text of p. 13 sets alpha_b=0, nu_b=0 for the fixed case where they are unused).
- Marginal likelihood: NOT used. The sampler targets the joint posterior of (Theta, zeta) with Theta=(psi, b_1..b_n, sigma^2, sigma_b^2), the random effects b_i are sampled too "to avoid integrating the likelihood over the random effects" (p. 8). No closed form is exploited even in the fixed-effects case (conjugacy not used).

## 3. Sampler design
- Particle (p. 8-9): omega=(Theta, zeta), a full model-parameter pair of fixed dimension p+1+n+2 (psi, b's, sigma^2, sigma_b^2). P particles (P=1000 default; 6000 in Sec. 4.4).
- Initial distribution (p. 9, step 1): pi^0 = pi(Theta|zeta) pi(zeta) = the PRIOR. Not data-driven, no block structure.
- Targets (p. 8): geometric tempering of the likelihood: pi^t proportional to f(y|Theta,zeta)^{alpha_t} pi(Theta|zeta) pi(zeta), alpha_1<...<alpha_T=1 strictly increasing.
- Schedule (p. 8, 10, 13): FIXED, manual, not adaptive: alpha_t = t/10, T=10 evenly spaced. Adaptive choice is mentioned and explicitly "not pursued in this project due to time constraints" (p. 10), and again recommended for future work "hundreds or thousands" of nonlinearly spaced alpha_t (p. 28).
- Weights/resampling (p. 9-10): incremental weight w_t = f(y|Theta_{t-1},zeta_{t-1})^{alpha_t - alpha_{t-1}} (with the pi^t-invariant backward kernel), ESS = (sum W w)^2 / sum (W w)^2 and resampling (type not stated, "according to probabilities W") when ESS < P/2. Resampling is done BEFORE propagation (p. 11) so weights at step t are computed from step t-1 particles, standard DMDJ ordering.
- MCMC move (p. 11): a single symmetric random-walk Metropolis-Hastings kernel invariant for pi^t that "adds or removes a predictor from M_{t-1} with uniform probability" (i.e. a single flip of one inclusion indicator, the paper does not say more) and jointly proposes psi_t ~ MVN(psi_{t-1}, sigma_1^2 I), b_{t,i} ~ N(b_{t-1,i}, sigma_2^2), log sigma^2 and log sigma_b^2 random walks (variances sigma_1^2..sigma_4^2 = 0.25, 0.25, 0.25, 0 in the fixed case, sigma_u^2=5; sigma_4^2=0.25 in the mixed case, p. 13, 25). Number of MH repetitions per temperature is not stated (I read it as one). No Gibbs, no swaps, no neighbour moves, no independence proposal.
- Islands/parallel: only "the algorithm is parallelized to speed up computation" (p. 12) (across simulated datasets/particles, unspecified). No independent non-communicating islands.
- Outputs (p. 12): from the final weighted particle set pi_hat^T: marginal posterior inclusion probabilities as raw weighted particle frequencies (not Rao-Blackwellised); a predictor is "selected" if PIP >= 0.5 (median probability model, citing Barbieri-Berger 2004); 95% credible intervals for beta_j from the weighted particles (point mass at 0 when excluded); posterior mean bias. No evidence estimate / marginal likelihood estimate is computed or discussed. No reported single best model, no local search, no list.
- Experiments: largest p = 6 (Sec. 4.2; p=3 in benchmark and mixed case), largest n = 1000 (subjects). Datasets: Gaussian predictors with sigma_X^2=0.01 (independent or equicorrelated rho=0.5), beta_0=2, effects +-10, sigma^2=15 (benchmark, p. 13); mixed case sigma^2=sigma_b^2=5, 4 measurements per subject (p. 24). Replicates: 500 (benchmark), 200 per cell x 16 cells (factorial), 100 (mixed), 200 (6000-particle study). Competitors: NONE. There is no comparison with any other selection method or sampler in the thesis; "RJMCMC and direct evidence calculation" are only mentioned as preliminary failures (p. 3) with no numbers.

## 4. What they prove
- NO THEORY. No theorem, proposition, lemma or proof anywhere (checked all 51 pages).
- Informal / quoted claims only:
  - p. 3-4: annealed SMC "does not rely on convergence arguments in the same sense as MCMC", but "its theoretical justification still depends on a convergence argument as the number of particles increases [DMDJ 2006]".
  - p. 28-29 (Discussion): "one can show that" sqrt(N)(psi_hat - psi) -> N(0, (sigma*)^2) as the number of particles grows, citing [14] (Del Moral, Doucet, Jasra 2006) - stated, not proved, no conditions given, and with a fixed grid and fixed kernel only implicitly.
  - p. 12: the 0.5 threshold is "inspired by" the Barbieri-Berger median-probability-model result (cited, not used as a theorem).
- Types: (i) Monte Carlo CLT in N: quoted from the literature only; (ii) complexity: only remark "time complexity ... scales linearly with the number of particles" (p. 26, 29); (iii) posterior/selection consistency: none; (iv) output guarantees: none.
- Empirical findings (not theorems): selection and estimation improve with SNR, degrade with predictor correlation (Sec. 4.2, p. 23); 95% credible intervals have LOW coverage when SNR high (about 0.86 at SNR=2 vs 0.97-0.99 at SNR=0.02, Fig. 4.1, p. 18-19) and in the mixed case (0.84, 0.80 for beta_1, beta_2, Table 4.6, p. 25); with 6000 particles coverage about 0.91-0.96 but unimportant-predictor selection worsens (Tables 4.7-4.9, p. 27; false selection rate 0.215 vs 0.186 at 1000 particles). Credible intervals "more than 30 times" wider than a fit of the true submodel (p. 30-31).

## 5. Comparison with ours (METHOD_SUMMARY.md)
| Feature | Vuong 2024 | Ours | Match |
|---|---|---|---|
| (a) SMC over models | Yes: SMC over joint (model zeta, parameters) space with fixed dimension via auxiliary psi | SMC over model space only (marginal likelihood closed form) | SIMILAR (same family; different state space) |
| (b) path/bridge | Likelihood tempering from the prior, alpha_t=t/10 | Geometric bridge from block-product law pi_0 to posterior via discrepancy Delta | SIMILAR for the bridge type (geometric), DIFFERENT start |
| (c) schedule | Fixed, 10 evenly spaced rungs, no adaptivity (p. 10, 13) | Adaptive ESS pilot then FROZEN grid | DIFFERENT |
| (d) move set | One symmetric RW-MH kernel with single-flip of inclusion, p. 11 | Gibbs on every j, uniform swap, correlation-neighbour swap, independence move from pi_0 | DIFFERENT (single flip only) |
| (e) independent islands | No | 4 (16) non-communicating islands | DIFFERENT |
| (f) PIP estimator | Raw weighted particle frequency, threshold 0.5 | Rao-Blackwellised Gibbs probabilities + list-renormalised PIPs | DIFFERENT |
| (g) evidence estimate | Not computed | Unbiased (conditional on frozen calibration) | DIFFERENT |
| (h) block-structured start | No; prior start | Block-product start law pi_0 with exact block tables | DIFFERENT |
| (i) reported model + local search certification | No; selects by PIP >= 0.5; no local search | Best-scoring model after hill climbs, certified flag, list T | DIFFERENT |
- Scale: Vuong p <= 6, n <= 1000; ours p up to 10^6. Vuong is a simulation performance study, not a methodological contribution.
- Theory vs our Theorems 1-6 / P1-P5: NONE overlap, imply or contradict. The only "theory" is a quoted Monte Carlo CLT (to be compared with nothing of ours beyond Prop. 5, which is stronger and specific). Empirical observation of poor credible-interval coverage and degradation with correlation is consistent with, but says nothing about, our P1 trap theorem.

## 6. Verdict
- Novelty risk to us: NONE. It is an unrefereed MSc project: plain annealed SMC from the prior with a fixed 10-step linear grid and one single-flip RW kernel, p <= 6, no competitors, no theory, no evidence estimate. It shares only the generic "annealed SMC over models plus parameters for BMA/selection" idea.
- Cite? Optional low-key citation as an instance of generic tempered SMC applied to Gaussian variable selection (with the caveat that it is a master's project, so it is "grey literature"); if cited, one-sentence differentiation: "Vuong (2024) runs prior-started, fixed-grid annealed SMC with single-flip moves on at most six predictors and reports empirical performance only, whereas we start from an exactly samplable block-product law, use a frozen adaptive calibration with Gibbs/swap/independence moves, and prove consistency and output-level guarantees for p up to 10^6."
- Caveat on unverified items: the SFU record page was not readable (bot protection), so I cannot rule out a revised or supplementary file on Summit.
