# LIT-PAR notes 05: SMC finite-sample complexity; BB-SSL

## Mathews & Schmidler (2024), "Finite sample complexity of sequential Monte Carlo estimators on multimodal target distributions",
## Ann. Appl. Probab. 34(1):1199-1223 (doi 10.1214/23-AAP1989 per search snippet, venue UNVERIFIED from journal page); arXiv:2208.06672v1 (READ, PDF).
- Abstract (quoted): "We prove finite sample complexities for sequential Monte Carlo (SMC) algorithms which require only local mixing
  times of the associated Markov kernels. ... The lack of global mixing is addressed by sequentially controlling the bias introduced by
  SMC resampling procedures. ... SMC provides a fully polynomial time randomized approximation scheme for some difficult multimodal
  problems where the corresponding Markov chain sampler is exponentially slow."
- Setting: partition A = {A_j : j = 1..p} of the state space (any partition; typically modes); bridge mu_0..mu_V; Assumption A1 (quoted):
  "mu_v(x)/mu_{v-1}(x) = (z_{v-1}/z_v) w_v(x) <= ZW". mu_star := min_v min_j mu_v(A_j) ("minimum probability of all partition elements
  across all steps"). Analysed algorithm: iid start from mu_0, reweight, resample, t steps of the RESTRICTED kernels (local moves).
- THEOREM 1 (quoted shape): if |f| <= 1, (A1), eps in (0,1/2), "N > (1/eps^2) max{ 3456 (V W Z / mu_star^2?) log(64 V p / mu_star) , ...}"
  [constants garbled in pdftotext; dependence is polynomial in V, W, Z, 1/mu_star] and "t > max_j max_v tau_{v,j}(eps/(16NV), 7)"
  (locally-warm mixing time of the restricted kernel on A_j), then w.p. >= 3/4 the SMC average is within relative eps of E_pi f.
  "Theorem 1 provides bounds on the total number of Markov transition steps N V t".
- WORK/DEPTH reading (ours): work = N V t; sequential depth (with N particles in parallel) = V t; width = N. Depth depends only on
  LOCAL mixing times and the number of stages V; the price of no global mixing is paid in WIDTH (N ~ poly(1/mu_star)).
- RELEVANCE: this is the generic theorem template that could carry our "depth = stage count x local mixing, width = R N" claim.
  Its crux condition is mu_star: every partition element (mode) must keep non-negligible mass at EVERY stage, including mu_0.
  In BVS with a masked start (our O-STAGES "masked" regime; API-POS "masking is a property of the start"), the true model's basin has
  exponentially small mass under pi_0 => mu_star tiny => the generic bound gives exponential width. So the generic theorem does NOT give
  our masked-regime result; it does give a template for the favourable regime (pi_0 puts mass >= poly on the truth's basin).
  THREAT level: medium. It makes "SMC needs only local mixing + bounded stage ratios" STANDARD; our BVS-specific contribution must be
  (a) verifying A1/mu_star/local mixing for BVS posteriors under explicit design conditions, (b) the masked regime.
  OVERLAP: T38 (a) favourable regime and T32(i) cost (ours) are BVS instances of this template — must cite.

## Marion, Mathews, Schmidler, "Finite sample complexity of sequential Monte Carlo estimators", arXiv:1803.09365v3 (READ abstract;
## header says "Submitted to the Annals of Statistics"; final venue UNVERIFIED).
- Abstract (quoted): "We present bounds for the finite sample error of sequential Monte Carlo samplers on static spaces. Our approach
  explicitly relates the performance of the algorithm to properties of the chosen sequence of distributions and mixing properties of
  the associated Markov kernels. ... We obtain bounds for the complexity ... including finite spaces, product measures, and log-concave
  distributions including Bayesian logistic regression. The bounds obtained are within a logarithmic factor of similar bounds
  obtainable for Markov chain Monte Carlo." Intro: "SMC algorithms are well-suited for parallel comput[ation]".
- Requires GLOBAL mixing of each stage kernel (contrast with 2208.06672). Generic; no BVS application.

## Nie & Rockova (2023), "Bayesian Bootstrap Spike-and-Slab LASSO", JASA (per arXiv/CRAN; journal page not opened); arXiv:2011.14279 (READ, PDF).
- Method: independent MAP optimisations of SSL on randomly reweighted data with jittered prior centres; each draw is an independent job
  ("BB-SSL is (a) unapologetically parallelisable, and (b) it does not require costly matrix [operations]").
  Depth = one SSL coordinate-ascent optimisation (sequential over coordinates/iterations); width = #draws.
- Target: a pseudo-posterior (bootstrap distribution of MAPs), NOT the posterior; no model-space posterior probabilities or evidence.
- Thm 4.2/4.3 (regression; quoted conditions): p > n, SSL prior with (1-theta)/theta ~ p^eta, lambda_0 ~ p^gamma; weights with E w_i = 1,
  bounded away from 0 and infinity, Var(w_i) <~ 1/log n; "(5) max_{i!=j} |x_i^T x_j| <~ lambda_0^2 / n" plus a restricted-norm condition
  on X_B^T P_A X_B / n for disjoint |A| = |B| = k; then pseudo-posterior model size <= q(1+K) and "the BB-SSL posterior concentrates at
  the near-minimax rate" ||beta - beta_0||^2 <~ q(1+K) log p / n.
- Design condition = low MUTUAL COHERENCE (pairwise correlations small) => fails for LH / strongly correlated S-scenarios.
  Confirms Felipe's belief for this method: parallel + guarantees, but guarantees need weakly correlated designs and target is approximate.
