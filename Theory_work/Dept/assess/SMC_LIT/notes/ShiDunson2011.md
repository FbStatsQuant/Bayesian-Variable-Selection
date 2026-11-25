# Reader notes: Shi & Dunson (2011), "Bayesian variable selection via particle stochastic search" (PSS)

## 0. Bibliographic
- Title: "Bayesian variable selection via particle stochastic search". Authors: Minghui Shi, David B. Dunson. Year 2011. Venue: Statistics & Probability Letters 81(2):283-291 (page range and volume from Crossref). DOI 10.1016/j.spl.2010.10.011 (from Crossref; the PDF itself carries no DOI).
- File read: /home/fb31/SMC_Theory_Department/SMC_LIT/papers/ShiDunson2011_particle_stochastic_search_preprint.pdf, 21 PDF pages. THIS IS THE AUTHOR PREPRINT (manuscript layout, "[Figure n about here]" placeholders, figures and a list of figures at the end), NOT the typeset journal version (9 journal pages). I cannot say whether the published text differs (e.g. in the figures, wording, or added references). Printed page number = PDF page number throughout the notes below.
- No supplement is referenced; the only appendix is the probit implementation appendix (p. 11). All 21 pages read page by page with the Read tool (pages 1-11, 12-21).

## 1. Coverage log
- p. 1: title, abstract, keywords, Sec. 1 start: model (1), model space Gamma = {0,1}^p.
- p. 2: posterior (2), marginal likelihood (3), SSVS (George-McCulloch) and its mixing complaints, marginal inclusion probability MIP q_j (4).
- p. 3: literature on SMC for model selection (Chopin 2000/2007, Del Moral et al 2002, Toni et al 2009, Zhang et al 2007), outline of PSS (sequence of partial posteriors pi(gamma | y_{1:n}); particles rejuvenated and reweighed as subjects are added); Sec. 2 start, MIP estimator (5) = particle frequency.
- p. 4: Sec. 2.1 SMC for variable selection: particle approximation (6), weight update (7), initialisation from the prior, degeneracy, resampling, kernel K with invariant law pi(gamma | y_{1:n}) (8).
- p. 5: kernels: (1) Metropolis-Hastings (9) with generic proposal q; (2) Gibbs systematic scan with Bernoulli(p_hat_j) (10); ESS (11) = N / (1 + var(w)); Algorithm 1 steps (i), (ii)a (reweighting (12)).
- p. 6: Algorithm 1 steps b1 (resample if ESS < M/2), b2 (rejuvenate); remark that Del Moral et al (2006) alternatives to sequential data-adding are NOT considered; Sec. 2.2 latent-variable (probit, Albert-Chib) extension; Theorem 1 (Liu 2001, quoted).
- p. 7-8: justification for marginalising parameters; kernels (16)-(17); Algorithm 2 (probit PSS with latent z in the particles).
- p. 8-10: Sec. 3 Examples: Ex. 1 normal linear (George-McCulloch 1997 design, p=15, then padded to p=100), Ex. 2 probit (p=16, then 100); Sec. 4 Conclusion (p. 10-11).
- p. 11: Sec. 5 Appendix: probit PSS details (weights, truncated normal propagation, Gibbs rejuvenation).
- p. 12-13: references. p. 14: list of figures. p. 15-21: Figures 1-7 (boxplots of log marginal likelihoods of visited models; MIP scatter plots with MC standard errors).

## 2. Model and prior
- Likelihood: normal linear regression (Ex. 1) and probit regression via Albert-Chib latent z (Ex. 2); general f(y_i | x_{gamma,i}, gamma, theta_gamma) in (1) (p. 1).
- Model space: all 2^p subsets, no size cap (p. 1).
- Model prior pi(gamma): not specified for the experiments (the particles are initialised from "the prior distribution pi(gamma)", p. 5). I did not find the model prior or the coefficient/variance prior hyperparameters stated for Example 1; the text only says "normal-gamma prior" gives a closed-form marginal likelihood (p. 2). For probit: beta ~ N(b, v) (p. 11). So the g-prior / spike-and-slab details are NOT given.
- Marginal likelihood: closed form for normal-gamma (p. 2); for probit it is closed form only conditionally on latent z (p. 6, 11); the "log complete-data marginal likelihood" is used as the performance metric (p. 9).

## 3. Sampler design
- Is it SMC over models: YES. A particle is a model indicator vector gamma_m (plus the latent variables z_{1:n,m} in the probit case, Algorithm 2) with weight w_m (p. 4, 7).
- Initial distribution: the prior pi(gamma), equal weights 1/M (p. 4, Algorithm 1(i), p. 5). Not data-driven.
- Path / "tempering": DATA-SEQUENTIAL. Targets are the partial posteriors pi(gamma | y_{1:n}, X_{1:n}), n = 1..N, obtained by adding one observation at a time (p. 3-4). This is the Chopin (2002) data-annealing construction, an implicit temperature sequence (p. 10), not likelihood tempering with a geometric bridge. They explicitly decline the alternatives of Del Moral et al (2006): "For simplicity ... we do not consider such alternatives" (p. 6). The path depends on the order of observations; nothing is said about order dependence.
- Schedule: the schedule is the data order (one observation per step); no adaptive temperatures. Resampling is adaptive: resample when ESS(M) < M/2 with ESS = M / (1 + var(w)) (p. 5-6). The resampling scheme is only called "an efficient sampling strategy" (p. 6), not specified.
- Reweighting: general form (7), w_m^n = pi(gamma^n | y_{1:n}) / pi(gamma^{n-1} | y_{1:n-1}) * w^{n-1} (p. 4). In Algorithm 1 it is written as w_m^n proportional to L(y_n; gamma_m^n, x_n) w^{n-1} (12) (p. 5). Because the parameters are integrated out, (12) must be read as the conditional marginal (predictive) likelihood of y_n given y_{1:n-1} and gamma; the notation L(y_n; gamma, x_n) is loose (my reading; the paper does not spell this out). In the probit algorithm the weight is the predictive probability of y_n given the current latent z_{1:n-1} (p. 7, 11).
- MCMC move kernels (rejuvenation after resampling, kernel invariant for the current partial posterior): (a) Metropolis-Hastings with generic proposal q(gamma*; gamma), acceptance (9) (the proposal q is NOT specified, p. 5); (b) Gibbs: systematic scan over a permutation of coordinates, gamma_j | gamma_(j) ~ Bernoulli(p_hat_j) (10) (p. 5). No swap moves, no neighbour/informed proposals, no independence proposals from a data-driven law. Blocking/marginalisation are mentioned as possible improvements (p. 5).
- Parallel / islands: they use "parallel implementation" on a single machine (C++, 3.0 GHz Dell, p. 8) and say PSS "can take advantage of distributed computing on a cluster" and "automatically communicates across the particles" (p. 3, 10). It is one particle population, not independent non-communicating islands.
- Outputs: MIP estimator (5): q_hat_j = (1/S) sum_s 1(gamma_j^(s) = 1) over Monte Carlo samples from the posterior (p. 3), i.e. a RAW PARTICLE FREQUENCY. (6) shows the weighted particle approximation; the paper does not say whether the final MIPs use weights or equal weights after the last resampling (the final step N is, per Algorithm 1, resampled only if ESS < M/2). They do NOT renormalise over distinct particle models; no Rao-Blackwellisation of the Gibbs probabilities in the output; no list of top models; no evidence (marginal-likelihood) estimate is discussed or used; no reported "best model" or local search (they only show that particles sit in high-posterior regions via boxplots of log marginal likelihoods of visited models, p. 8-9, Figs 1, 3, 5, 7). MC standard errors in Figs 2, 4, 6 (bottom panels): the paper does not say how they are computed (across repeated runs is my guess; not stated).
- Largest p and n: Example 1 has N = 100 subjects, p = 15 (George-McCulloch 1997 design with correlations up to 0.998, sigma^2 = 2.5) then p = 100 by adding 85 null predictors (p. 8-9). Example 2 (probit): p = 16 (intercept + 15) then 100 (p. 9-10). So the largest p = 100 and p ~ n (not p >> n). Particles: M = 1000 for p = 15 and 10,000 for p = 100 (p. 8-9); competitor SSVS (Gibbs and MH versions) run 5000 iterations (p = 15) and 20,000 (p = 100), "matching implementation time approximately" (p. 8). No run-time table, no replicate runs described beyond the MC standard-error panels.
- Findings: p = 15: "comparable performances", PSS "slightly better" in finding high-probability regions; MIPs "comparable" to SSVS (p. 8-9). p = 100: PSS (10,000 particles) finds higher-posterior regions than 20,000 Gibbs-SSVS iterations; MIPs again comparable (p. 9). Probit: PSS particles in somewhat higher regions than SSVS; MIPs "perform similarly" (Fig. 6, p. 20, compares both against "true" MIPs computed given the true latent z; the estimates visibly differ from those "true" MIPs at several predictors, e.g. 4 and 6; I read this from the plot and the paper does not comment on it).
- Self-assessment (p. 10-11): "PSS is by no means a perfect alternative to SSVS in that accurate approximation of the posterior of gamma when p is large would seem to necessitate using an enormous number of particles"; "these algorithms are designed to search for good models and not to accurately approximate the posterior for large p"; "more extensive simulations and theoretical studies are needed".

## 4. What they prove
- No theory of their own. The only numbered result is "Theorem 1 (Liu [2001])" (p. 6): for pi_0, pi_1 densities with supp(pi_0) in supp(pi_1), var_{pi_1}{pi_0(x,y)/pi_1(x,y)} >= var_{pi_0}{pi_0(x)/pi_1(x)} (15) (Rao-Blackwell / marginalisation reduces importance-weight variance). It is quoted (not proved) to motivate integrating out regression parameters from the particles (p. 7). Type: a general Monte Carlo variance inequality, not a statement about PSS output, consistency or convergence.
- No convergence/CLT of PSS, no complexity bounds, no posterior consistency, no guarantee on the reported model. Informal claims only (quoted above in Sec. 3 "Self-assessment"; also "PSS has an automatic annealing feature", "avoids the need to choose tuning parameters", p. 10, which are not supported by any analysis).

## 5. Comparison with ours (METHOD_SUMMARY.md)
| Feature | Shi-Dunson PSS | Verdict vs ours |
|---|---|---|
| (a) SMC over models | yes, particles are models (and z for probit) | SAME (concept) |
| (b) path/bridge | data-sequential partial posteriors from the prior; no geometric likelihood bridge (explicitly not considered, p. 6) | DIFFERENT (ours: geometric bridge in the discrepancy from a block-exact start law) |
| (c) adaptive vs frozen schedule | schedule = data order, fixed; adaptive only in ESS-triggered resampling | DIFFERENT (ours: ESS-adaptive pilot then frozen temperatures) |
| (d) move set | MH with unspecified q, or Gibbs scan; no swaps, no informed neighbour moves, no independence move | SIMILAR for Gibbs, DIFFERENT otherwise |
| (e) independent islands | single population (distributed computation possible); no independent islands | DIFFERENT |
| (f) PIP estimator | raw particle frequency (5); no RB, no list renormalisation | DIFFERENT (ours: RB + list-renormalised) |
| (g) evidence estimate | none | DIFFERENT |
| (h) block-structured start law | prior start | DIFFERENT |
| (i) reported model + local search certification | none; only log marginal likelihood boxplots of visited models | DIFFERENT |
- Theory overlap with Thm 1-6, P1-P5: NONE. They prove nothing; Liu's variance inequality is unrelated to our statements. Their largest p (100, p ~ n) is far from p up to 10^6 and the paper itself says PSS is not designed to approximate the posterior at large p.
- Unbiased evidence (our Prop 5): the generic SMC unbiasedness of the normalising-constant estimate (Del Moral 2004) is not mentioned or used by them.

## 6. Verdict
- Novelty risk to us: PARTIAL OVERLAP at the level of the generic idea "SMC with MCMC rejuvenation on the model space {0,1}^p for Bayesian variable selection". It is an early (2010/2011) instance of that idea. It does not overlap on the path (data-sequential vs our geometric discrepancy bridge from a block-exact law), on any proved result, on evidence estimation, on large p, or on the algorithm-output guarantee.
- Must cite: Shi & Dunson (2011) as the earliest SMC-for-variable-selection paper (together with Chopin 2002, Del Moral-Doucet-Jasra 2006, Schafer-Chopin 2013).
- One-sentence differentiation: "Shi and Dunson (2011) introduced data-sequential SMC over models with MCMC rejuvenation and report simulations up to p = 100 without theory, whereas we use a tempered bridge from a block-exact start law, an unbiased evidence estimate and prove posterior and output-level consistency at p >> n."
