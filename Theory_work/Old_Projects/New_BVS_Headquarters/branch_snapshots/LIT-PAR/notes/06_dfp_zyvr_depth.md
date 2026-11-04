# LIT-PAR notes 06: Gutierrez-Guhaniyogi DFP; ZYVR as parallel-depth counterexample; our own depth

## Gutierrez & Guhaniyogi (2022), "Bayesian Dynamic Feature Partitioning in High-Dimensional Regression with Big Data",
## Technometrics (2022; venue per search result + UCSC report; journal page not opened). READ: UCSC tech report UCSC-SOE-21-04 (May 24 2021),
## https://tr.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-21-04.pdf
- Method DFP: streaming data shards; parameters partitioned into groups; each group's "DFP pseudo conditional posterior"
  f(Theta_G | Theta^_{-G}, S^(t)) conditions on POINT ESTIMATES of the other groups from time t-1, so groups are sampled in parallel.
- Guarantee (abstract, quoted): "pseudo posterior densities over time being arbitrarily close to the full posterior as the data size
  grows, as shown in the supplementary material." Text (quoted): "The theoretical results in the supplementary material prove desirable
  performance of the proposed algorithm when the sequence of estimators Theta^(t) is consistent in estimating the true parameters as
  t -> infinity. In practice, we found this assumption can be validated empirically". Supplement not read.
- Target: pseudo-posterior (plug-in conditionals), approximate; guarantee is asymptotic in data size and CONDITIONAL on consistency of
  the plug-in estimates (which under strong correlation / p >> n at fixed n is exactly what fails). Regime: large n streaming.
- Our designs: fixed n = 200; not applicable. Complementary/unrelated to the exact-posterior claim.

## Zhou, Yang, Vats, Roberts, Rosenthal (2022) JRSSB 84(5) "Dimension-free mixing for high-dimensional Bayesian variable selection"
## READ: local Papers/Core_bibliography/10_*.pdf (arXiv 2105.05719).
- Thm 1 (quoted): "Suppose that n = O(p), s0 log p = O(n) and kappa = O(s0). If Condition 1 holds for c0 = 2 and 4 <= c1 <= n kappa1 - kappa,
  then, for sufficiently large n, we have T_mix <= 800 max{ n kappa1 / c1 , 3 s0 }." (T_mix from any start in M(s0)).
- Condition 1 (quoted): "(1a) For any overfitted gamma in M(s0) and j not in gamma, B(gamma, gamma ∪ {j}) <= p^{-c0}. (1b) For any underfitted
  gamma in M(s0), there exists some j in gamma* \ gamma ... such that B(gamma, gamma ∪ {j}) >= p^{c1}. (1c) [swap version at |gamma| = s0]."
  A POSTERIOR-LEVEL condition (no greedy-blocking local modes), implied by YWJ-type design conditions; not a design condition per se.
- Parallelism (quoted, Sec 7.4): "As noted in Zanella [2020], one can further boost LIT-MH using parallel computing [Lee et al., 2010]:
  the calculation of pi_n(gamma')/pi_n(gamma) for each gamma' in N(gamma) can be easily parallelized."
- DEPTH reading (ours, elementary): one LIT-MH iteration = score all |N(gamma)| = O(p s0) neighbours (parallel, width O(p s0)), then a
  normalisation/selection (a reduction, depth O(log p)). Hence LIT-MH has sequential DEPTH O(T_mix log p) = O(n log p) score-rounds,
  INDEPENDENT of p up to the log, with PROVED mixing under Condition 1. API-POS (theory/API-POS REPORT §1 item 2) found that Condition 1(b)
  holds on LH in the iid realisation with ZYVR's own priors (PROOF SKETCH), but not for the paper's target prior (g = n, kappa_eff ~ 1, cap K).
- => STRONGEST COUNTEREXAMPLE CANDIDATE to the literal gap claim "parallel-friendly methods with guarantees break under correlated designs":
  a single informed chain whose per-step work is embarrassingly parallel, with a proved dimension-free iteration count, under a condition
  that holds on (a version of) our own correlated LH family. Qualifications: (i) it is ONE chain: depth O(n) iterations is not O(1);
  (ii) Condition 1 is unimodality-like (fails under genuine posterior multimodality, e.g. S-ELS posterior misses / competing models);
  (iii) no unbiased evidence; (iv) the authors themselves state the parallelism only as a remark — no paper we found analyses depth.

## OUR OWN DEPTH (self-critique; from METHODOLOGY_v3 §6.5, §8 and O-STAGES REPORT §1 item 5)
- A v3 move round is "the list of m = p + B + 2 labelled elementary steps -- the p Gibbs coordinate updates, one uniform swap, B neighbour
  swaps, one independence proposal -- applied in a uniformly random order" per particle. Within a particle these are SEQUENTIAL
  (each Gibbs update conditions on the current state; all coordinates interact through m(S), so chromatic parallel Gibbs is not valid).
- O-STAGES: cost term N_n T_n (p + B + 2). So the per-particle sequential depth is T_n x (rounds per stage) x (p + B + 2) score evaluations,
  i.e. Theta(p) per round, NOT O(1). Width = R x N particles (+ the tables: depth O(2^B) per block, all blocks parallel; width p 2^B / B).
- Therefore the claim "sequential depth = stage count T" is TRUE only if a round counts as one unit of depth. Counting score evaluations,
  v3's depth is Theta(T p L); parallelised LIT-MH's is O(n log p). For p >> n, a referee can say our depth is WORSE in p than a parallelised
  informed chain with a proved bound.
- Possible fixes (method change, outside this task to decide): replace the systematic Gibbs sweep by moves whose work is parallel within a
  particle (informed / locally-balanced proposals scoring all p neighbours at once, Zanella 2020; tempered Gibbs, Zanella-Roberts 2019),
  so that a round has depth O(log p); then depth = O(T x rounds x log p) and the claim "depth = stage count (up to log p)" becomes true.
  Or phrase the claim as "depth in STAGES" with the per-stage depth stated honestly as O(p) score evaluations per round.

## Schäfer & Chopin (2013), "Sequential Monte Carlo on large binary sampling spaces", Statistics and Computing 23:163-184
## READ: local Papers/Core_bibliography/07_*.pdf (arXiv 1101.6037v4).
- SMC tempering (from uniform/prior to posterior) on {0,1}^p for BVS, with a GLOBAL independence MH kernel whose proposal is a parametric
  binary family (logistic conditionals) fitted to the particle cloud; adaptive stage selection by ESS.
- Parallelism (quoted): "global methods have the property to be easily parallelisable"; "the Sequential Monte Carlo algorithm can be
  parallelised in the sense that we can, on suitable hardware, run many evaluations of pi in parallel during the move step ... No analogue
  speed-up can be performed in the context of Markov chains. We have processed variable selection problems from genetics with about a
  thousand covariates within a few hours running a parallelised version of the algorithm on a 64-CPU cluster."
- Per-particle depth of one independence move = 1 score (after a global proposal fit) => depth ~ (#stages x #moves), roughly p-free per move.
- Theory: none for the BVS sampler (no theorem found; only standard SMC consistency). Evidence: multimodal, correlated test problems
  (constructed), where local MCMC gets trapped.
- THREAT: "parallel SMC with tempering for BVS targeting the exact posterior" is NOT new (2013). Our novelty must be (a) the exact
  correlation-block start + bridge, (b) theorems (T38, T31(i), O-STAGES), (c) the depth/width accounting. The quoted claim
  "No analogue speed-up ... in the context of Markov chains" is contradicted by informed proposals (ZYVR Sec 7.4, Zanella 2020):
  do not repeat it in our paper.
