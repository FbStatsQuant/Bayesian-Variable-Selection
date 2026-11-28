# Our method (SMC-BVS, method-v3.1.1-listpip) and our theory, for literature comparison

## Model and prior
- Gaussian linear regression, intercept removed by centring; columns standardised. Model space: all S ⊆ [p] with |S| ≤ K = min(p, floor(n/2)). Regime of interest: p ≫ n (p ≤ n^A), up to p = 10^6 in experiments.
- Model prior: beta-binomial BB(1, p) on the size (Scott–Berger-type multiplicity correction), truncated to |S| ≤ K.
- Coefficients: g-prior with g = n plus a unit ridge, θ_S | S, σ² ~ N(0, n σ² (X_S'X_S + I)^{-1}); σ² ~ IG(0.01, 0.01). Closed-form marginal likelihood m(S); log score F(S) = log prior + log m(S). Target = posterior over models π(S|y) ∝ e^{F(S)}.

## Sampler (SMC over the discrete model space)
- Particles are models S (binary inclusion vectors). N = 2,500 particles per island (setting), 4 independent islands (16 non-communicating islands in the p = 10^6 engine).
- Start law π_0: NOT the prior. The predictors are partitioned into small correlation blocks (≤ 16 predictors, complete-linkage clustering of sample correlations); π_0 ∝ size prior × product over blocks of exact block marginal-likelihood tables h_k(S ∩ C_k) = m(S ∩ C_k)/m(∅). Exact sampling from π_0; a start mode (argmax of π_0).
- Tempering path: geometric bridge from π_0 to the posterior through the "discrepancy" Δ(S) = log m(S)/m(∅) − Σ_k log h_k(S∩C_k): π_ξ ∝ γ_0 e^{ξΔ}, ξ from 0 to 1. Annealed / tempered SMC sampler (Del Moral–Doucet–Jasra 2006 style): reweight by e^{(ξ_t − ξ_{t−1})Δ}, multinomial resampling, MCMC moves.
- Schedule: an adaptive ESS-based pilot run picks the temperatures, then the grid is FROZEN and the final islands run on the fixed grid (so the evidence estimate is unbiased conditional on the calibration).
- MCMC moves at each temperature (rounds): Gibbs inclusion update of every j, uniform swap, correlation-neighbour swap (neighbour graph from |r_jl| > sqrt(2 log p / n)), and an independence move proposing from π_0.
- Outputs: PIPs as Rao–Blackwellised averages of the Gibbs inclusion probabilities over particles and measured rounds, equal-weight mean over islands; median probability model; evidence estimate Ẑ = mean of island estimates (product of mean incremental weights); a "reported model" Ŝ = best-scoring model ever scored, after deterministic local searches (add/delete/swap hill-climb), with a "certified" flag if no neighbour improves; a returned list T of the best 40p+1 models scored, with LIST-RENORMALISED PIPs pip_T(j) = Σ_{S∈T, S∋j} e^{F(S)} / Σ_{S∈T} e^{F(S)}, the list median model, and log Z_T.

## Our theory (A7 spec; what to compare against)
Proved:
1. Thm 1 (posterior concentration, random sub-Gaussian design): 1 − π(S0|y) = O_P(sqrt(log n / n)); P(HPM = MPM = S0) → 1; max_j |PIP_j − 1{j∈S0}| = O_P(sqrt(log n / n)). p growing (p ≤ n^A), beta-min, sparsity.
2. Thm 2 (distribution-level consistency): Hellinger contraction of the posterior predictive law to the truth at rate sqrt(M log n / n), with explicit exponential-in-log n probability bounds.
3. Thm 3 (the reported model equals the true model): on data events of probability → 1, EVERY admissible run that produces output reports Ŝ = S0, whatever its seed and calibration outcome (a statement about the ALGORITHM'S OUTPUT as coded, not only about the posterior), plus delivery (the run produces output with probability 1). Uses a "visibility"/leakage assumption about the start law and moves.
4. Thm 4 (certified screening, fixed design, no beta-min): a certified reported model of size ≤ k_n misses a true predictor with probability → 0.
5. Prop 5 (unbiased evidence): each island's evidence estimate is unbiased conditional on the frozen calibration, for every data set.
6. Thm 6 (sharpness): the sqrt(log n / n) rate of the posterior miss cannot be improved (every-design upper bound on π(S) and witness-design lower bound).
Planned: P1 trap theorem (single-flip chains and the Zanella–Roberts weighted tempered Gibbs sampler mix slowly on a multimodal design family where our consistency still holds); P2 coverage at p = 10^7; P3 raw-scale search bridge (list mass); P4 aggregated leak; P5 fixed-p KL-projection misspecification result.

## What counts as "similar to ours"
Any paper doing variable selection (linear-regression or GLM model space, spike-and-slab, binary inclusion vectors) with SMC / particle / sequential importance sampling / population Monte Carlo / annealed or tempered importance sampling over models. The closer the match on (a) SMC over models, (b) tempering/annealing path, (c) adaptive schedule, (d) MCMC move set incl. swaps/Gibbs, (e) independent islands, (f) Rao–Blackwellised or list-renormalised PIPs, (g) evidence estimate, (h) THEORY (MC convergence of the sampler vs posterior/selection consistency vs guarantees for the algorithm's output), the higher the match score.
