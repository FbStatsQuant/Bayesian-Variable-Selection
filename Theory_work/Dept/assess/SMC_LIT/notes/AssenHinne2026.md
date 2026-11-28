# Reader notes: van Assen and Hinne (2026), Anchored Reversible Jump Sequential Monte Carlo

## 0. Bibliographic
- Title: "Anchored Reversible Jump Sequential Monte Carlo". Authors: Janna van Assen (Eindhoven Univ. of Technology), Max Hinne (Donders Institute, Radboud Univ.). Dated 8 Oct 2026 on the PDF; arXiv:2610.09930 [stat.ME], v1 submitted 7 Oct 2026.
- Venue: preprint only (arXiv page: no journal ref). DOI (arXiv-issued) 10.48550/arXiv.2610.09930. Comments field: "20 pages, 4 figures".
- Version check: I fetched the arXiv abstract page; it lists ONLY v1 (no later version). It mentions no supplement. The appendices are inside the PDF.
- File read: /home/fb31/SMC_Theory_Department/SMC_LIT/papers/AssenHinne2026_anchored_RJSMC.pdf, 20 pages, all 20 read with the Read tool (pp. 1-10 and 11-20). Page numbers below are PDF = printed pages.
- Code: https://github.com/jannavanassen/RJSMC (README fetched: algorithms/rjsmc.py, birth_death.py, mcmc.py; experiments 01_count_data_models, 02_bayesian_linear_regression, 03_bayesian_factor_analysis; derived from the first author's master thesis). Code not read beyond the README.

## 1. Coverage log
- p. 1: abstract, Sec. 1 Introduction (Bayesian model comparison, eq. 1).
- p. 2: RJMCMC motivation, limitations; contributions list (4 items); Sec. 2.1 RJMCMC target (eq. 2-3).
- p. 3: RJMCMC move, dimension matching, acceptance (eq. 4-5); related automatic proposals (AutoMix, normalising-flow transport RJ, Gagnon informed RJ); Sec. 2.2 SMC begins.
- p. 4: tempered SMC (eq. 6-7), adaptive ESS temperature; Sec. 3 Proposed methods; 3.1 RJSMC: super-particle representation; weights (eq. 8).
- p. 5: representation weights (eq. 9), representation ESS (eq. 10; eta_repr=0.9), algorithm outline; 3.2 Anchored RJ proposals: independent parameter-space construction (eq. 11-13), weighted Gaussian KDE (eq. 14), anchor weight omega.
- p. 6: grace parameter gamma and jump probabilities (eq. 15), acceptance (eq. 16), Metropolised-independence remark; start of Sec. 4 experiments (hardware, software, code URL).
- p. 7: Algorithm 1 (A-RJSMC); Sec. 4.1 Poisson vs negative binomial (Hastie-Green).
- p. 8: setup of six methods, Fig. 1, Table 1 text.
- p. 9: Table 1 (results); Sec. 4.2 Variable selection (setup), baseline BD-RJMCMC.
- p. 10: Table 2; Sec. 4.3 Bayesian factor analysis setup.
- p. 11: Table 3 (T-RJMCMC vs A-RJSMC); Sec. 5 Conclusion.
- p. 12-14: Acknowledgements, 41 references.
- p. 15: App. A (Algorithm 2: RJSMC). p. 16: App. B complexity; App. C variable-selection setup (g-prior, Bayes factor formula). p. 17: Table 4 (exact vs estimated posterior model probabilities for 16 models), App. D birth-death RJMCMC (whitened g-prior). p. 18: App. E efficiency per density evaluation; App. F evolution of model probabilities. p. 19-20: Fig. 2, App. G posterior densities for factor models (Figs 3-4).
- No supplement exists.

## 2. Model and prior
- Setting: general Bayesian model comparison (trans-dimensional), not primarily variable selection. Variable selection is ONE of three experiments (Sec. 4.2, App. C).
- Variable-selection likelihood (App. C, p. 16): Gaussian linear regression y_i = mu + X_{i,M} beta_M + eps_i, with Jeffreys priors on mu and sigma^2, Zellner g-prior beta_M | sigma^2, M ~ N(0, g sigma^2 (X_M'X_M)^{-1}) with g = n (unit-information, Kass-Wasserman), UNIFORM prior over the 2^p models (no multiplicity correction). Closed-form Bayes factor BF_k = (1+g)^{(n-p_k-1)/2} [1+g(1-R_k^2)]^{-(n-1)/2} (p. 16), which they use only to compute the exact reference posterior.
- Model space: all 2^p subsets, with p = 4 only (16 models; beta=(0.2,0.1,0,0), n=100, sigma=1, p. 17). No size cap.
- Other experiments: Poisson vs negative binomial (1,040 EPL match goal counts, 2 models); Bayesian factor analysis with 2 vs 3 factors (n=143, 6 exchange-rate series, 17 vs 21 free parameters).

## 3. Sampler design
- Particle ("super-particle", p. 4): (k, theta_1, ..., theta_K) = active model index plus a latent parameter state for EVERY candidate model. For variable selection K=2^p=16 and 64 parameters per super-particle (Table 2 caption, p. 10). The memory/cost therefore scales with the NUMBER OF MODELS K (complexity O(MTNCK), p. 16); the method as stated cannot hold all 2^p models for p beyond about 20.
- Initial distribution (p. 4, 7 Algorithm 1): the PRIOR, k ~ p(k), theta_k ~ p(theta_k|k) for all k. Not data-driven.
- Path (p. 4, eq. 6): standard likelihood tempering p(theta)p(Y|theta)^{T_n} from prior (T=0) to posterior (T=1).
- Schedule (p. 4-5): ADAPTIVE: increments chosen so that the "representation ESS" (eq. 10, over all models' representations) equals eta_repr M with eta_repr=0.9. Single run, no frozen second pass; no discussion of the evidence bias caused by adaptation (no evidence is estimated).
- Reweight / resample / move (Algorithm 1-2, p. 7, 15): reweight with the particle weights (eq. 8), resample "according to W_particle" (every step), optional within-model MCMC mutation on all K models' parameters (HMC in the factor case, Gaussian random walk 0.1-0.2 in others), then an RJMCMC mutation step. Resampling scheme not stated.
- Move kernel: ANCHORED RJ proposal (p. 5-6): an independence Metropolis-Hastings between models: draw destination model l ~ J_gamma(l) = (1-gamma) M_l/M + gamma/K (population fractions mixed with uniform), draw theta_l from a weighted Gaussian KDE built from the particle population's stored representations of model l (anchor weight omega >= 1 upweights particles currently in l; bandwidth by Scott's rule), accept with ratio (eq. 16). Parameters of the two models treated as independent (Jacobian = 1, eq. 11-12). The authors note it is a Metropolized independence sampler when within-model kernels are omitted (p. 6). In the VS experiment: 20,000 particles, 5 MCMC mutation steps per RJMCMC iteration, gamma=0.5, omega=100 (p. 9). No Gibbs inclusion update, no swaps, no neighbour structure: moves are across ALL models via the KDE of the population (a "global" proposal like our independence move, but parametric-KDE over coefficient space, not a Bernoulli product over inclusion indicators).
- Islands/parallel: the particles are parallelised on a single GPU (JAX); no independent non-communicating islands. Runs repeated 10 times with different seeds only for error bars.
- Outputs: posterior model probabilities p(k|Y) as particle fractions in each model (Tables 1, 2, 3, 4), within-model posterior histograms (App. G); PSRF and ESS diagnostics. No PIPs, no Rao-Blackwellisation, no evidence estimate, no reported best model, no local search.
- Experiments, largest sizes: variable selection p=4, n=100; factor analysis n=143, p=6 series (up to 21 parameters); Poisson/NB n=1040. Competitors: HG-RJMCMC (Hastie-Green tailored), BD-RJMCMC (birth-death), T-RJMCMC (transport RJ with normalising flows, Davies et al. 2023); SMC South et al. 2019 as gold standard for the factor model. Hardware: single Quadro RTX 6000 GPU. Timing results: Table 2 (p. 10): A-RJSMC ESS/s 136 vs BD-RJMCMC 49.6 despite 106.6 s vs 28.0 s run time; Table 3 (p. 11): about 580x ESS/s over T-RJMCMC (CPU vs GPU, App. E gives an implementation-independent figure: 95 vs 78 effective samples per million density evaluations).

## 4. What they prove
- NO THEORY. No theorem, proposition, lemma or proof (checked all 20 pages). Informal statements only:
  - p. 3: RJMCMC "can be interpreted as Metropolis-Hastings on an augmented space and inherits its convergence properties under standard assumptions" (not proved).
  - p. 6: "Compared to general Metropolis-Hastings algorithms, Metropolized independence samplers enjoy stronger convergence guarantees" (qualitative; cites South et al. for a similar idea; no result stated).
  - App. B (p. 16): complexity count O(MTNCK) serial, O(TNCK) parallel; with anchored proposals O(TN(KC+MD)) parallel, D = total number of parameters (an operation count, not a bound on error).
- Types: (i) MC convergence: none; (ii) complexity: only the operation count in App. B; (iii) consistency: none; (iv) output guarantees: none. Validation is empirical (agreement with exact model probabilities, correlation > 0.99 for p=4, p. 9-10; Table 4, p. 17).
- Minor inconsistencies noted: App. F calls the method "JA-RJSMC" (p. 18); the HG-in-SMC row lacks an acceptance rate (p. 9); "ESS" in the experiments counts independent MC samples (rank-normalised, ref. [36]) and not SMC weights (p. 8).

## 5. Comparison with ours (METHOD_SUMMARY.md)
| Feature | van Assen-Hinne | Ours | Match |
|---|---|---|---|
| (a) SMC over models | Yes: tempered SMC over (model, parameters) via super-particles; RJ moves between models | SMC over inclusion vectors, marginal likelihood closed form | SIMILAR in spirit (population + tempering over a model space); DIFFERENT state/targets |
| (b) path/bridge | Likelihood tempering from the PRIOR | Geometric bridge from block-product pi_0 to posterior | DIFFERENT start (same bridge family) |
| (c) schedule | Adaptive on representation ESS, single run | Adaptive pilot, then FROZEN grid | DIFFERENT |
| (d) move set | Independence RJ proposal from a KDE of the population + optional within-model MCMC | Gibbs, uniform swap, neighbour swap, independence from pi_0 | SIMILAR only in that both use a population-fitted/global independence-type proposal; DIFFERENT otherwise (no Gibbs/swap) |
| (e) independent islands | No | 4 / 16 islands | DIFFERENT |
| (f) PIP estimator | Not reported (model probabilities by counts) | RB + list-renormalised PIPs | DIFFERENT |
| (g) evidence estimate | Not estimated | Unbiased given frozen calibration | DIFFERENT |
| (h) block-structured start | No (prior) | Yes | DIFFERENT |
| (i) reported model + certification | No | Yes | DIFFERENT |
- Scale: p = 4 predictors in the variable-selection experiment because the super-particle stores K=2^p model representations; ours p up to 10^6.
- Theory vs Theorems 1-6 / P1-P5: NONE. They prove nothing. The only qualitative statement ("Metropolized independence samplers have stronger convergence guarantees") is at most loosely related to the role of our independence move; it does not imply any of our results.

## 6. Verdict
- Novelty risk to us: NONE. Different problem (generic trans-dimensional model comparison with parameters), different state (super-particles over all models, infeasible for large p), p=4 in the only variable-selection example, no theory, no PIP or evidence output.
- Cite: yes, as related work on population-based trans-dimensional (RJ) SMC with tempering and independence-type global proposals fitted to the particle population (similar in spirit to our independence move from pi_0, and to Schafer-Chopin / South et al. independent proposals).
- Differentiation sentence: "van Assen and Hinne (2026) combine adaptive tempered SMC with population-KDE reversible-jump proposals for generic model comparison, storing a parameter state for every model and testing variable selection only for p = 4; we work on the discrete inclusion space at p up to 10^6 with a block-product start law, Gibbs/swap moves, frozen-grid unbiased evidence, and consistency theorems for the reported model."
