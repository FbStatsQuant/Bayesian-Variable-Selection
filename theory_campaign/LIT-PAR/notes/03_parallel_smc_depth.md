# LIT-PAR note 03: island / parallel SMC, and parallel depth of samplers

Purpose: what the literature PROVES about (a) island / parallel SMC and (b) sequential depth (span) of samplers versus work, so a "work vs depth" claim for our tempered BVS SMC (R islands x N particles, T tempering stages, Z-hat-weighted pooling) can be phrased defensibly.

Conventions. "Read" = I extracted the PDF text (pdftotext in /tmp/litpar_dl2) and the quoted text is copied from it. Quotes are verbatim (line breaks and hyphenation removed). UNVERIFIED = seen only in a search snippet or in another paper's reference list. Venues are UNVERIFIED unless a primary page was read; I did not fetch journal pages, only arXiv PDFs (plus one NSF-PAR PDF), so almost all venues below are "per the task brief / per citing paper".

Notation mapping: our width = R*N particles, our depth = T stages (plus per-stage MCMC move cost, which is a separate parallel loop over particles).

---------------------------------------------------------------------

## Part A. Island / parallel SMC

### A1. Verge, Dubarry, Del Moral, Moulines, "On parallel implementation of Sequential Monte Carlo methods: the island particle model"
- Citation as verified: Christelle Verge, Cyrille Dubarry, Pierre Del Moral, Eric Moulines. arXiv:1306.3911v1 [math.PR], 17 Jun 2013 (manuscript "Noname", Statistics and Computing template). Journal: Statistics and Computing (2015) per task brief; Lindsten et al.'s reference list (arXiv 1406.4993) cites it as "Statistics and Computing. In press." (UNVERIFIED for volume/pages).
- URL read: https://arxiv.org/pdf/1306.3911
- What is proved (read): Feynman-Kac island model with N2 islands of N1 particles; island-level process is itself a Feynman-Kac flow; fluctuation theorems (Thms 2-6) give asymptotic bias and variance, "when both N1 and N2 goes to infinity" (the abstract says non-asymptotic results and a fluctuation theorem were deferred to a forthcoming paper). Thm 1 shows the island model's unnormalised measure has gamma-bar_n(1) = gamma_n(1) (normalising constant unbiasedness carries over; text near "According to Theorem 1, gamma_p(1) = gamma_p(1)").
- Key quote (independent islands, bias vs variance): "The variance of the particle approximation is inversely proportional to N1 N2, but because the islands do not interact, the bias is independent of N2 and is inversely proportional to N1."
- Key quote (interaction trade-off): "When the N2 islands are run independently, the bias induced in each island only depends on their population size N1; when N1 is small compared to the total number N, the bias will be large (and is of course not reduced by averaging across the islands). To reduce the bias, introducing an interaction between the islands is beneficial. However, this interaction increases the variance, due to the selection step."
- Key quote (regime): "When the number of particles N1 within each island is small and the number of islands N2 is large, then the interaction is typically beneficial. On the contrary, when N2 << N1, the interaction between islands may increase the mean squared error."
- Conditions/caveats: results are for the bootstrap-type (selection/mutation) Feynman-Kac model, asymptotic in N1 (limit statements of the form lim N1*E[...] = B_n(f), lim N1*N2*Var[...] = V_n(f)), and the estimator of the normalised measure is the plain average across islands (not Z-hat-weighted). Their "independent islands" estimator therefore has O(1/N1) bias for any R; this is the reason a naive island average is not a consistent-in-R scheme.
- Relevance (i): This is the classical benchmark: unweighted averaging over independent islands keeps an O(1/N) bias. Our Z-hat-weighted pooling is a different estimator (see A3, which proves convergence in the number of islands for the Z-weighted version). Do not cite Verge et al. as supporting Z-hat pooling; cite it as the contrast. (ii) Not a depth result; no statement about the number of time steps.

### A2. Lindsten et al. (2017) D&C-SMC, and Kuntz, Crucinio, Johansen
- Citation (a): F. Lindsten, A. M. Johansen, C. A. Naesseth, B. Kirkpatrick, T. B. Schon, J. A. D. Aston, A. Bouchard-Cote, "Divide-and-Conquer with Sequential Monte Carlo". arXiv:1406.4993v2 [stat.CO], 30 Jun 2015. Journal: JCGS 2017 (per task brief, UNVERIFIED). URL read: https://arxiv.org/pdf/1406.4993
- Citation (b): Juan Kuntz, Francesca R. Crucinio, Adam M. Johansen, "The divide-and-conquer sequential Monte Carlo algorithm: theoretical properties and limit theorems". arXiv:2110.15782. PDF header reads "Submitted to the Annals of Applied Probability"; publication in AAP 2024 per task brief (UNVERIFIED). Note the task brief's title ("...properties and limit theorems") differs slightly from the title in the PDF above. URL read: https://arxiv.org/pdf/2110.15782
- Key quotes (Lindsten, Prop. 1): "Provided that gamma_t << (x)_{c in C(t)} gamma_c (x) q_t for every t in T and an unbiased, exchangeable resampling scheme is applied to every population at every iteration, we have for any N >= 1: E[Z-hat_r] = Z_r = integral gamma_r(dx_r)." (math symbols paraphrased from the PDF).
- Key quote (Lindsten, cost): "If executed serially, the running time of D&C-SMC is O(N * |T|). However, a running time of O(N * depth(T)) can be achieved via parallelized or distributed computing (see Section 5.3)." Memory: "O(N * depth(T) * max_t |C(t)|) in the serial case, and ... O(N * |T|) in the parallel case."
- Key quote (Kuntz et al., Thm 3): "The estimators for the unnormalized targets are unbiased: THEOREM 3 (Unbiasedness of (rho_u^N)). If Assumptions 1-2 hold, then E rho_u^N(phi) = rho_u(phi), E Z_u^N = Z_u, for all N > 0, phi in B_b(E_u), u in T." Also Thm 4: bias of normalised estimators "decays linearly with the number of particles N"; Theorem 6 gives CLTs for each node (asymptotic variance decomposes into a sum over descendants).
- Key quote (Kuntz et al., depth): the tree can be lumped into a line by merging levels: "merge together all nodes in each level of the tree to obtain a line L0 -> L1 -> ... -> LT = {r} whose length equals T's depth." Parallelisation: "The computation time of Algorithm 4 can be lowered by parallelizing the for loop in lines 5-7."
- Conditions: absolute continuity / regularity assumptions (Assumptions 1-2 in Kuntz et al.), unbiased exchangeable resampling; results are for a fixed tree and N -> infinity (CLT) or any N (unbiasedness).
- Relevance (i): Unbiasedness of Z-hat is the same structural fact we use per island; D&C-SMC combines populations by multiplying and re-weighting, which is a different (merge, not pool) operation than our pooling across independent islands. No R -> infinity result for pooling in these papers. (ii) Depth is proved only as a cost statement (O(N*depth(T)) with enough processors), i.e. depth = tree height, analogous to our T; the cost claim is an algorithmic accounting statement, not a lower bound.

### A3. Whiteley, Lee, Heine (2016), "On the role of interaction in sequential Monte Carlo algorithms"
- Citation as verified: Nick Whiteley, Anthony Lee, Kari Heine, Bernoulli 22(1), 2016, 494-529, DOI 10.3150/14-BEJ666 (printed in the arXiv reprint header), arXiv:1309.2918v3. URL read: https://arxiv.org/pdf/1309.2918
- Key quote (abstract): "We are then able to phrase sufficient conditions for time-uniform convergence in terms of algorithmic control of the ESS, in turn achievable by adaptively modulating the interaction between particles. This leads us to suggest novel algorithms which are, in senses to be made precise, provably stable and yet designed to avoid the degree of interaction which hinders parallelization of standard algorithms."
- Key quote, Section 5.1 (independent copies; the most relevant passage in the whole note): "By Theorem 1 we are assured of the a.s. convergence pi_n^{sq}(phi) -> pi_n(phi) when q is fixed and s -> infinity. In words, we have convergence as the total number of bootstrap algorithms tends to infinity, even though the number of particles within each algorithm is fixed. On the other hand, simple averaging of the output from the s independent algorithms [...] is biased, in the sense that in general it is not true that, with q fixed, (sq)^{-1} sum phi(zeta_n^i) -> pi_n(phi) as s -> infinity [...]. In summary, simple averages across independent particle filters do not, in general, converge as the number of algorithms grows."
  In their setup the block-diagonal alpha matrix (their eq. (46)) makes the pooled estimator pi_n^{sq} = sum_l W_n^l * (block-l empirical measure) / sum_l W_n^l, where W_n^l (their eq. (47)) is block l's normalising-constant estimate. That is exactly Z-hat-weighted pooling of s independent SMC runs with q particles each (my reading of eqs. (46)-(49); the identification of W_n^l with a Z-estimate follows their text "Comparing (47) with (12) ... the well known lack-of-bias property of the BPF").
- Key quote (relative variance of Z): "E[Z_n^{(q,s)}] = Z_n, E[(Z_n^{(q,s)}/Z_n - 1)^2] = (1/s) E[(Z_n^{(q,1)}/Z_n - 1)^2]" and "Under certain ergodicity and regularity conditions E[(Z_n^{(q,1)}/Z_n)^2] can grow exponentially fast along observation sample paths when q is fixed and n -> infinity [23]. When that occurs, it is clear [...] that s must be scaled up exponentially fast with n in order to control the relative variance of Z_n^{(q,s)}."
- Conditions: hidden-Markov / Feynman-Kac setting, conditions (A2), (B++) for Theorem 1 (Section 5.1 says they hold for the block-diagonal choice); the exponential growth statement is for time horizon n -> infinity at fixed q, citing [23]; the results are for particle filters indexed by time n, not for tempering.
- Relevance (i): This is the primary-source support for "fixed N, R -> infinity islands pooled with Z-hat weights is consistent" (a.s. convergence of the Z-weighted pooled estimator), AND for the warning that unweighted averaging is not. It also shows the cost: the relative variance of the pooled Z-hat is (1/R) times a single island's, so if a single island's relative variance is large (e.g. exponential in the number of stages when N is small) R must be correspondingly large. (ii) Depth statement: no depth claim; the paper's concern is the cost of interaction (resampling) as the communication bottleneck. The "stable with less interaction" algorithms (alpha-SMC with ESS control) are the closest results to "few synchronisation points", but they are time-uniform results for filtering.

### A4. Lee, Yau, Giles, Doucet, Holmes (2010), GPU Monte Carlo
- Citation as verified: Anthony Lee, Christopher Yau, Michael B. Giles, Arnaud Doucet, Christopher C. Holmes, "On the utility of graphics cards to perform massively parallel simulation of advanced Monte Carlo methods". arXiv:0905.2441v3 [stat.CO], 15 Jul 2009 (first page shows authors Lee, Yau, Giles, Doucet; fifth author per task brief). JCGS 2010 per task brief (UNVERIFIED). URL read: https://arxiv.org/pdf/0905.2441
- Key quote (abstract): "On a canonical set of stochastic simulation examples including population-based Markov chain Monte Carlo methods and Sequential Monte Carlo methods, we find speedups from 35 to 500 fold over conventional single-threaded computer code."
- Key quote (SMC section): "The importance sampling step used at each time step is trivially parallelizable as it involves only the local state of a particle. The resampling step [...] comprises the construction of an empirical cumulative distribution function for the particles based on their importance weights followed by sampling from this N times [...]. While neither of these tasks is trivially parallelizable, they can benefit moderately from parallelization. However, the bulk of the speedup will generally come from the parallelization of the evolution and weighting steps. Therefore, using criteria like effective sample size [...] to avoid resampling at every time step can also improve speedup."
- Conditions: empirical, no theorem. It is a case study (population-based MCMC, SMC samplers, particle filters).
- Relevance (i): none for pooling. (ii) Supports "per-stage particle moves are embarrassingly parallel; resampling is the (milder) synchronisation point; depth = number of stages". Empirical speedups only; cite as practice, not as a proved scaling statement.

---------------------------------------------------------------------

## Part B. Tempering: communication barrier and number of stages

### B1. Syed, Bouchard-Cote, Deligiannidis, Doucet, "Non-reversible parallel tempering: a scalable highly parallel MCMC scheme"
- Citation as verified: Saifuddin Syed, Alexandre Bouchard-Cote, George Deligiannidis, Arnaud Doucet. arXiv:1905.02939v4 [stat.CO], 26 Jul 2021. JRSSB 2022 per task brief (UNVERIFIED; the PDF header is the arXiv version). URL read: https://arxiv.org/pdf/1905.02939
- Key quote (Section 1): "We then show that for non-reversible PT the round trip rate converges to (2 + 2Lambda)^{-1}, in contrast to the reversible counterpart for which it decays to zero."
- Key quote (Theorem 3 (b),(c), as ||P_N|| -> 0): "The round trip rate for reversible PT, tau_SEO, goes to zero: tau_SEO(P_N) ~ 1/(2N + 2 Lambda) -> 0. (c) The round trip rate for non-reversible PT, tau_DEO satisfies tau_DEO(P_N) -> tau-bar = 1/(2 + 2 Lambda) > 0, where the convergence occurs with rate O(||P_N||)."
- Key quote (diminishing returns): "In general, Lambda is large when pi_0 deviates significantly from pi. Since Lambda is problem specific, this identifies a limitation of PT present even in its non-reversible flavour, namely that adding more cores to the task will never be harmful, but does have a diminishing return. The bound (2 + 2 Lambda)^{-1} could indeed be very small for complex problems."
- Key quote (number of chains): "Corollary 2 implies N r* ~ Lambda" (N = number of chains after the first, r* = optimal rejection rate under the optimal schedule). The paper also proposes "a mechanism to determine the optimal trade-off between the number of chains and the number of independent PT algorithms one should use."
- Definition: lambda(beta) is the instantaneous swap rejection rate, Lambda = integral_0^1 lambda(beta) d beta (Theorem 2 gives lambda(beta) = (1/2) E|V1 - V2| for the two potential-difference variables). Lambda is the "global communication barrier".
- Conditions: round-trip results rely on the Efficient Local Exploration (ELE) assumption, which the authors say "is not expected to hold exactly in real scenarios"; asymptotics are in the mesh ||P_N|| -> 0. PT is an MCMC scheme (all chains run in parallel forever), so N here is parallel width and the "depth" analogue is the number of PT scans, not stages.
- Relevance (i): the trade-off "number of chains N vs number of independent PT runs" is the PT analogue of our R vs N choice. (ii) Lambda is the natural problem-complexity scale: width ~ Lambda is where PT's round trip rate saturates, with the saturated rate 1/(2+2 Lambda) setting the scan-count (depth) needed per round trip.

### B2. Syed, Bouchard-Cote, Chern, Doucet, "Optimised annealed sequential Monte Carlo samplers"
- Citation as verified: Saifuddin Syed, Alexandre Bouchard-Cote, Kevin Chern, Arnaud Doucet. arXiv:2408.12057. The local copy file name says 2026 (version/venue not stated in what I read; UNVERIFIED venue). URLs read: https://arxiv.org/pdf/2408.12057 (downloaded) and the local copy /home/fb31/api_workers/LIT-PAR/Papers/Core_bibliography/02_2026_Syed_et_al_Optimized_annealed_sequential_Monte_Carlo_samplers.pdf (I read the downloaded arXiv PDF only; the two may be different versions).
- Key quote (Theorem 3, dense-schedule limit): "Suppose Assumptions 1 to 8 hold, and let Z-hat be obtained from Algorithm 1 with deterministic resampling times. Then, as T -> infinity, lim T Var[Z-hat/Z] = E(phi)/N >= Lambda^2/N, where the convergence is uniform over all choices of resampling times. Equality holds if and only if phi = phi*." (E(phi) is the kinetic energy of the schedule generator; here N is the number of particles.)
- Key quote (Section 5.2, stability regimes as Lambda -> infinity with T ~ Lambda^{alpha_T} and resample-size rho = Theta(Lambda^{alpha_rho})): "Unstable regime (alpha_rho + alpha_T < 2). When the number of annealing distributions is sparse relative to Lambda (alpha_T < 1) or particles interact too infrequently (alpha_rho < 2 - alpha_T), at least an exponential number of particles is required to obtain relative variance of Z-hat within epsilon > 0." "Stable regime (1 <= alpha_T <= 2 and alpha_rho >= 2 - alpha_T). With sufficient overlap between distributions and adequate particle interaction, only N = O(log(1+epsilon)^{-1} Lambda^{2-alpha_T}) particles are needed as Lambda -> infinity." "Strongly stable regime (alpha_T > 2). When the schedule is sufficiently dense relative to Lambda, the relative variance of Z-hat converges to zero as Lambda -> infinity, independently of N and alpha_rho. In particular, it is possible to obtain stable estimates with O(1) particles and no resampling."
- Quote (assumptions): the analysis uses an "idealised 'performance model'": Assumption 2 (temporal independence), Assumption 3 (particle independence), Assumption 4 (efficient local exploration); "While not expected to hold exactly in practice, they can be approximated and provide algorithmic design guidelines that we validate empirically".
- Also: "Z-hat is unbiased for any finite N" (any forward/backward kernels, any resampling times).
- Consequence (my arithmetic from the quoted statements, not a statement in the paper): in the stable regime T * N = Lambda^{alpha_T} * Lambda^{2 - alpha_T} = Lambda^2 up to logs, so the total work is about Lambda^2 while the depth T can be anywhere in [Lambda, Lambda^2]; the minimum depth for sub-exponential particle count is T of order Lambda (alpha_T >= 1).
- Conditions/caveats: performance-model assumptions above (not proved for real MCMC kernels, discrete spaces, or BVS); the object controlled is the relative variance of Z-hat, not posterior-expectation error; "no assumptions on the state space, the choice of annealing distributions, or forward/backward kernels" is stated for the regime classification, conditional on the performance model.
- Relevance (i): it is the cleanest published relation "number of SMC stages T vs Lambda vs particles N" and is for the same Z-hat that we use for island weights (Var(Z-hat/Z) of a single island = (relative variance), and pooled across R islands the relative variance is 1/R of that, by A3). (ii) It gives the work-vs-depth trade-off in Lambda; for BVS one would need to establish or empirically estimate Lambda for our path pi_0 -> posterior.

---------------------------------------------------------------------

## Part C. Parallel depth of sampling in theoretical CS (model of computation matters)

For each: model, depth bound, condition.

### C1. Feng, Sun, Yin, "What can be sampled locally?"
- Citation as verified: Weiming Feng, Yuxin Sun, Yitong Yin. arXiv:1702.00142v3 [cs.DS], 8 Sep 2022. Venue PODC 2017: confirmed only via Fischer and Ghaffari's text ("LubyGlauber algorithm by Feng, Sun, and Yin [PODC'17]"), i.e. second-hand. URL read: https://arxiv.org/pdf/1702.00142
- Model: LOCAL model of distributed computing (rounds of message passing on the graph; unlimited local computation); sampling a Gibbs distribution on a Markov random field on a graph with n vertices, max degree Delta.
- Key quote: "The algorithms achieve respective mixing times O(Delta log n) and O(log n) under typical mixing conditions, where n is the number of vertices and Delta is the maximum degree of the graph. We show that the time bound Theta(log n) is optimal for distributed sampling. We also show a strong Omega(diam) lower bound: in particular for sampling independent set in graphs with maximum degree Delta >= 6."
- Condition: "typical mixing conditions" (Dobrushin-type uniqueness conditions for the respective algorithms; exact constants not extracted). The Omega(diam) lower bound is for a non-uniqueness regime.
- Relevance: gives the only truly proved LOWER bounds: Omega(log n) rounds in the uniqueness regime, Omega(diam) beyond it, in the LOCAL model. These are about network locality, not shared-memory depth; do not transfer to a PRAM-style claim.

### C2. Feng, Hayes, Yin, "Distributed Metropolis sampler with optimal parallelism"
- Citation as verified: Weiming Feng, Thomas P. Hayes, Yitong Yin. arXiv:1904.00943v2 [cs.DS], 14 Jul 2019 (note: my first guess 2007.15294 was wrong; the correct ID is 1904.00943). Venue SODA 2021 (pp. 2121-2140) per search snippet only, UNVERIFIED. URL read: https://arxiv.org/pdf/1904.00943
- Model: fully asynchronous message-passing; simulates sequential single-site Metropolis chains exactly.
- Key quote: "if a natural Lipschitz condition is satisfied by the Metropolis filters, our algorithm can simulate N-step Metropolis chains within O(N/n + log n) rounds of asynchronous communications, where n is the number of variables. For sequential single-site dynamics, whose mixing requires Omega(n log n) steps, this achieves an optimal linear speedup. For several well-studied important graphical models, including proper graph coloring, hardcore model, and Ising model, our condition for linear speedup is weaker than the respective uniqueness (mixing) conditions."
- Relevance: a speedup of the simulation of a given chain (n-fold fewer rounds), not an improvement of mixing time; note the explicit additive log n term (a depth floor). Condition is a Lipschitz condition on the Metropolis filter (locality), not log-concavity.

### C3. Anari, Hu, Saberi, Schild, "Sampling arborescences in parallel"
- Citation as verified: Nima Anari, Nathan Hu, Amin Saberi, Aaron Schild. arXiv:2012.09502v1 [cs.DS], 17 Dec 2020. Venue ITCS 2021 (12th ITCS, LIPIcs 185, article 83, doi 10.4230/LIPIcs.ITCS.2021.83): from the reference lists of two later PDFs I read (arXiv 2401.09016 and the STOC 2023 author copy), so second-hand. URL read: https://arxiv.org/pdf/2012.09502
- Model: PRAM-style parallel computation; NC / RNC (polylog depth, polynomial processors).
- Key quote: "However, the classic reduction from sampling to counting seems to be inherently sequential. This raises the question of designing efficient parallel algorithms for sampling. We show that sampling arborescences can be done in RNC."
- Condition: exact structure (determinant counting oracle in NC); not a general MCMC statement.
- Relevance: shows that polylog depth is possible for specific combinatorial distributions even though the standard sampling-to-counting reduction needs n sequential steps. No general statement about binary model spaces.

### C4. Anari, Huang, Liu, Vuong, Xu, Yu, "Parallel discrete sampling via continuous walks"
- Citation as verified: Nima Anari, Yizhi Huang, Tianyu Liu, Thuy-Duong Vuong, Brian Xu, Katherine Yu. STOC 2023 (ACM DOI 10.1145/3564246.3585207, from a search snippet; UNVERIFIED). I read the author PDF at https://par.nsf.gov/servlets/purl/10488668 (NSF PAR record 10488668). I did NOT find an arXiv ID (my guess 2211.08574 was wrong, that ID is an unrelated math-phys paper). Note: the task brief wrote "Anari, Chen, Gupta?"; the verified author list is the six names above.
- Model: parallel (PRAM-type) algorithms, RNC and quasi-RNC.
- Key quote: "We show that determinantal point processes can be sampled via RNC algorithms, that is in time log(n)^{O(1)} using n^{O(1)} processors. For a wider class of distributions, we show our framework yields Quasi-RNC sampling, i.e., log(n)^{O(1)} time using n^{O(log n)} processors."
- Setting/conditions: discrete distributions mu on the hypercube {+-1}^n (the same kind of space as our {0,1}^p up to relabelling) for which convolution with spherical Gaussians gives "well-conditioned log-concave distributions, as long as the variance of the Gaussian is above an O(1) threshold"; the examples are DPPs and (quasi-RNC) non-symmetric DPPs and Eulerian tours. The reduction needs a parallel counting oracle (Laplace-transform / partition-function evaluation), so it does not give a generic sampler for arbitrary posteriors.
- Relevance: strongest published evidence that polylog depth is achievable on a hypercube for structured distributions; BVS posteriors with Zellner-type marginal likelihoods are not covered by any theorem here. For our claim this is a context citation ("depth polylog(p) is possible only for special structure"), not a result we inherit.

### C5. Anari, Chewi, Vuong, "Fast parallel sampling under isoperimetry"
- Citation as verified: Nima Anari, Sinho Chewi, Thuy-Duong Vuong. arXiv:2401.09016v1 [cs.DS], 17 Jan 2024. COLT 2024, PMLR 247, pp. 161-185 per search snippet (proceedings.mlr.press/v247/anari24a), UNVERIFIED. URL read: https://arxiv.org/pdf/2401.09016
- Model: parallel rounds of gradient evaluations (queries to V where pi proportional to exp(-V) on R^d), counting rounds as depth and total queries as work.
- Key quote: "We show how to sample in parallel from a distribution pi over R^d that satisfies a log-Sobolev inequality and has a smooth log-density, by parallelizing the Langevin (resp. underdamped Langevin) algorithms. We show that our algorithm outputs samples from a distribution pi-hat that is close to pi in Kullback-Leibler (KL) divergence (resp. total variation (TV) distance), while using only log(d)^{O(1)} parallel rounds and O~(d) (resp. O~(sqrt(d))) gradient evaluations in total."
- Application: "RNC sampling-to-counting reductions for families of discrete distribution on the hypercube {+-1}^n that are closed under exponential tilts and have bounded covariance."
- Condition: log-Sobolev inequality plus smoothness (continuous space); the hypercube application needs closure under exponential tilts and bounded covariance.
- Relevance: example of a depth-polylog / work-near-linear tradeoff stated as a theorem under an isoperimetry (LSI) condition; the BVS posterior is discrete and generally multi-modal, so LSI constants would be exponential; no direct transfer.

### C6. Holden Lee, "Parallelising Glauber dynamics"
- Citation as verified: Holden Lee, arXiv:2307.07131v4 [cs.DS], 10 Jul 2024. Venue APPROX/RANDOM 2024 per a search snippet (LIPIcs.APPROX/RANDOM.2024.49 link), UNVERIFIED. URL read: https://arxiv.org/pdf/2307.07131. Task brief wrote "Liu & Yin / Lee?"; the verified author is Holden Lee alone.
- Model: parallel algorithm with running time (depth) measured in parallel steps; Glauber dynamics over product spaces.
- Key quote: "We show that k-Glauber dynamics, which resamples a random subset of k coordinates, mixes k times faster in chi^2-divergence, and assuming approximate tensorization of entropy, mixes k times faster in KL-divergence. [...] For the Ising model mu_{J,h}(x) proportional to exp(1/2 <x,Jx> + <h,x>) with ||J|| < 1 - c (the regime where fast mixing is known), we show that we can implement each step of Theta~(n/||J||_F)-Glauber dynamics efficiently with a parallel algorithm, resulting in a parallel algorithm with running time O~(||J||_F) = O~(sqrt(n))."
- Condition: operator norm of the interaction matrix below 1 - c (high temperature); mixed p-spin at high temperature gives O~(sqrt(n)). So the depth is sqrt(n), not polylog, for Ising in the fast-mixing regime.
- Relevance: concrete known depth for parallelising local-update MCMC on a binary space (sqrt(n)), in a fast-mixing regime. Our BVS posterior is not covered.

### C7. Fischer and Ghaffari, "A simple parallel and distributed sampling technique: local Glauber dynamics"
- Citation as verified: Manuela Fischer, Mohsen Ghaffari. arXiv:1802.06676v2 [cs.DS], 15 May 2018. Venue DISC 2018 per search snippet only (LIPIcs.DISC.2018.26), UNVERIFIED. URL read: https://arxiv.org/pdf/1802.06676
- Key quote: "Concretely, we present a Markov chain that mixes in O(log n) rounds when Dobrushin's condition for the Gibbs distribution is satisfied. This improves over the LubyGlauber algorithm by Feng, Sun, and Yin [PODC'17], which needs O(Delta log n) rounds."
- Model: parallel/distributed rounds (local model); condition: Dobrushin.
- Relevance: same type of statement as C1; shows depth O(log n) under uniqueness-type conditions.

### C8. Miao and Yin (2026), "Sampling matchings in near-linear time"
- Citation as verified: Tianshun Miao, Yitong Yin, arXiv:2609.21936v1 [cs.DS], 18 Sep 2026 (seen as a preprint; not peer reviewed as far as I can tell). URL read: https://arxiv.org/pdf/2609.21936
- Key quote: "(ii) Work-efficient parallel sampling. We simulate the same Glauber dynamics in parallel using O~_lambda(m + n) work and O~_lambda(min{Delta, m^{1/3}, sqrt(n)}) depth with high probability."
- Condition: monomer-dimer model on graphs, fixed activity lambda. Work-efficient (work matches the sequential bound up to log factors) with sublinear depth. This is the only "work and depth stated together" result I found for a non-product-space Gibbs sampler.
- Relevance: provides phrasing precedent: "O~(work) work and O~(depth) depth with high probability".

---------------------------------------------------------------------

## What I could not cover (be honest in the paper)
- "Adaptive complexity of sampling" and 2024-2026 parallel-sampling-depth results beyond the items above: one search only; no further results read. I make no claim of completeness for Part C.
- No source found (in the PDFs I read) proving anything about parallel depth of SMC samplers or tempering for discrete posterior/BVS spaces specifically. The nearest are Syed et al. (B2, performance-model assumptions) and the Anari et al. hypercube papers (C4, C5; structured distributions).
- Venues (JCGS, JRSSB, AAP, Stat. Comput., SODA, COLT, STOC, APPROX/RANDOM, DISC) were not checked on journal/proceedings pages. Re-check before the bibliography is finalised.

---------------------------------------------------------------------

## Implications for phrasing a work-vs-depth claim

- Define the model explicitly: work = total particle-move evaluations W = R*N*T*(cost per move); depth (span) = T stages times the per-stage critical path (the move cost per particle, plus the resampling/normalisation reduction, O(log N) in a PRAM-style reduction). Say the claim is about this idealised model; the cited TCS results use LOCAL or PRAM/NC models (C1-C8) and do not transfer automatically.
- Safe, citable facts: (1) each island's Z-hat is unbiased for any N (A2 Lindsten Prop 1 and Kuntz Thm 3 for D&C-SMC, B2 for annealed SMC; our own proof is separate); (2) pooling R independent islands by Z-hat weights is consistent as R -> infinity at fixed N, whereas unweighted island averaging is not (A3, Whiteley-Lee-Heine Sec. 5.1; A1 gives the O(1/N1) bias of independent islands in the plain-average estimator).
- The relative variance of the pooled Z-hat is exactly 1/R of a single island's (A3, eq. (50)); if a single island's relative variance is large, R must grow accordingly. Whiteley et al. warn that for fixed q it can grow exponentially with n in filtering; for tempering the analogue is governed by Lambda (B2).
- For the T-vs-N trade-off, cite Syed et al. (B2) as an idealised-model result only: relative variance of Z-hat is about Lambda^2/(T*N) in the dense limit, depth T of order Lambda is the minimum for sub-exponential particle counts, and T between Lambda and Lambda^2 gives total work T*N of about Lambda^2 (the last point is my arithmetic from the quoted regimes). State the Assumptions 1-8 caveat (efficient local exploration, independence across time and particles).
- Do not claim a lower bound on depth T for BVS: the only proved depth lower bounds I found are Omega(log n) / Omega(diam) in the LOCAL model for Gibbs sampling (C1), which do not apply to a shared-memory model with exactly sampleable pi_0. A claim of the form "depth = T, and T needs to grow with the barrier Lambda for stable Z-hat" is supported by B2 under its assumptions; frame it as a sufficient condition / scaling heuristic unless we prove it for our path.
- Distinguish "depth reduction by structure" (RNC / polylog depth for DPPs, arborescences, Eulerian tours: C3, C4, C5; these use parallel counting oracles) from our setting; make clear our sampler gets its parallelism from independent islands and per-particle moves, not from a counting oracle.
- If we say "linear speedup in width", the closest published precedent for the phrasing is Feng-Hayes-Yin (C2: simulate N-step chains in O(N/n + log n) rounds) and Miao-Yin (C8: O~(m+n) work with sublinear depth); both state work and depth separately with an additive depth floor, which is the style a referee will accept. Note width only buys depth reduction up to the floor (here T, which cannot be parallelised across stages because stage t needs stage t-1's output).
- PT (B1) gives an alternative scaling statement: parallel width of about Lambda chains saturates the round-trip rate at 1/(2+2*Lambda), "adding more cores ... will never be harmful, but does have a diminishing return". Use it to motivate that R*N beyond a problem-dependent threshold buys no more depth reduction, but note PT is MCMC and its round-trip result uses the ELE assumption.
- Do not describe D&C-SMC (A2) as a precedent for island pooling: it merges sub-populations over a tree and the cost statement O(N*depth(T)) is accounting; there is no published R -> infinity pooling theorem there.

---------------------------------------------------------------------

## Sources actually read
(PDFs downloaded to /tmp/litpar_dl2 and text-extracted with pdftotext via owls_run; nothing executed.)
- https://arxiv.org/pdf/1306.3911 (Verge et al., island particle model)
- https://arxiv.org/pdf/1406.4993 (Lindsten et al., D&C-SMC)
- https://arxiv.org/pdf/2110.15782 (Kuntz, Crucinio, Johansen)
- https://arxiv.org/pdf/1309.2918 (Whiteley, Lee, Heine)
- https://arxiv.org/pdf/0905.2441 (Lee et al., GPUs)
- https://arxiv.org/pdf/1905.02939 (Syed et al., NRPT)
- https://arxiv.org/pdf/2408.12057 (Syed et al., optimised annealed SMC)
- https://arxiv.org/pdf/1702.00142 (Feng, Sun, Yin)
- https://arxiv.org/pdf/1904.00943 (Feng, Hayes, Yin)
- https://arxiv.org/pdf/2012.09502 (Anari, Hu, Saberi, Schild)
- https://par.nsf.gov/servlets/purl/10488668 (Anari et al., STOC 2023 author copy)
- https://arxiv.org/pdf/2401.09016 (Anari, Chewi, Vuong)
- https://arxiv.org/pdf/2307.07131 (Holden Lee)
- https://arxiv.org/pdf/1802.06676 (Fischer, Ghaffari)
- https://arxiv.org/pdf/2609.21936 (Miao, Yin)

Seen only in search snippets (UNVERIFIED, used only for venue and arXiv-ID lookup): ar5iv/arxiv abs pages for 1904.00943 and 2401.09016, proceedings.mlr.press/v247/anari24a, doi.org/10.1145/3564246.3585207, drops.dagstuhl.de entries for DISC 2018 and APPROX/RANDOM 2024.

Guessed arXiv IDs that turned out wrong (do not reuse): 2007.15294 (is a math-ph paper), 2211.08574 (is a Yang-Mills paper).
