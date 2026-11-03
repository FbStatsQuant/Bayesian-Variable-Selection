# LIT-PAR notes 04: data-splitting Bayes, scalable/variational BVS, GPU/parallel samplers, sequential benchmarks

Scope: test of "BVS methods with strong guarantees are sequential; parallel-friendly methods with guarantees break under correlated designs".
Our setting: n = 200, p in {500, 1000}, strongly correlated X, linked-hub family (true predictors masked: marginally weak, jointly strong),
target = exact posterior over S subset of {1..p} (g-prior, beta-binomial model prior).
All arXiv PDFs downloaded to /tmp/litpar_dl3 and extracted with pdftotext -layout (math in quotes is as pdftotext rendered it, so symbols are
sometimes garbled, e.g. "ps20" = p s_0^2; a cleaned reading follows where needed). Nothing downloaded was executed.
Marking: READ = full text read/grepped by me; ABSTRACT-ONLY = only abstract/landing page; UNVERIFIED = second-hand only.

Bottom line first (details per entry below):
1. No data-splitting Bayes paper found (CMC, WASP, M-posterior) proves anything for discrete model spaces / variable selection with p > n. The only
   data-splitting BVS *theory* is Zhang-Lam-Lin (2018): fixed small D (simulation: N = 5000, D = 10), asymptotics in N with R subsets, entropy/prior-mass
   conditions, no design-correlation condition stated and no p > n regime. The p>n distributed BVS paper (Li et al. 2022) has NO theorem (empirical only).
2. Every method with a *design-conditioned* guarantee that I could read is either a sequential chain (Yang-Wainwright-Jordan; Zhou et al. LIT-MH) or
   a sequential coordinate-ascent variational scheme (Ray-Szabo CAVI; IBSS) - and the variational ones target an APPROXIMATION, not the exact posterior.
3. Parallel-friendly methods that are *exact* (tempered Gibbs / wTGS, Griffin et al. adaptive MCMC, SMC) have only validity/ergodicity/SLLN results
   or a relative bound vs Gibbs (TGS), none of which gives a design-dependent mixing bound.
4. The sequential benchmark's own design conditions (YWJ/Zhou Condition 1) are about the posterior landscape and are exactly what masking would violate.

---------------------------------------------------------------------------------------------------------------------------------

## 1. Data-splitting Bayes

### 1a. Scott, Blocker, Bonassi, Chipman, George, McCulloch (2016) "Bayes and big data: the consensus Monte Carlo algorithm"
- Citation (verified via Google Research landing page): Int. J. Management Science and Engineering Management 11 (2016) 78-88;
  DOI 10.1080/17509653.2016.1142191. URL read: https://research.google/pubs/bayes-and-big-data-the-consensus-monte-carlo-algorithm/ (WebFetch: abstract,
  venue only). Full text NOT obtained (the research.google/pubs/archive link returned HTML, not a PDF; T&F page paywalled/not tried). STATUS: ABSTRACT-ONLY.
- PARALLEL: "Consensus Monte Carlo operates by running a separate Monte Carlo algorithm on each machine" (abstract excerpt); draws are then averaged across
  machines. Embarrassingly parallel over data shards; one combination step.
- TARGET: approximation. Abstract: "Depending on the model, the resulting draws can be nearly indistinguishable from the draws" of a single-machine run.
- GUARANTEES: none seen in abstract; examples are simple models with known solutions, hierarchical models, BART. (From general knowledge, the averaging
  rule is exact only for Gaussian subposteriors - UNVERIFIED here, not read in the paper.)
- Discrete model spaces: abstract does not mention discrete parameters or model selection. Averaging draws of an indicator vector gamma in {0,1}^p is not
  meaningful as a posterior over models (our remark, not the paper's).
- Plausible at n=200, p=1000 with correlation? Nothing to check; splitting n=200 into K shards leaves n/K << p per shard.

### 1b. Srivastava, Li, Dunson (2018) "Scalable Bayes via barycenter in Wasserstein space" (WASP), JMLR 19(8)  [journal volume/issue from memory: UNVERIFIED]
- arXiv:1508.05880. READ: https://arxiv.org/pdf/1508.05880 (pdftotext, 4988 lines; title/authors verified on page 1). Earlier AISTATS 2015 version
  (Srivastava, Cevher, Tran-Dinh, Dunson) NOT separately read.
- PARALLEL: data randomly split into k subsets; subset posteriors computed independently (stochastic approximation: subset likelihood raised to power gamma
  = k so subset posterior has variance of the same order), then combined by a Wasserstein-2 barycenter (a linear program). Depth: subset MCMC (any) + one LP.
- TARGET: approximation (a barycenter of subset posteriors), asymptotically close to full posterior as m -> infinity.
- GUARANTEES (Theorem 3.4, quoted): "If Assumptions (A1)-(A4) hold for the jth subset posterior Pi_m(. | Y[j]) (j = 1, ..., k), then there exists a constants
  universal C1 > 0 independent of j, such that as m -> infinity, E W_2^2(Pi_m(.|Y[j]), delta_theta0(.)) <= C1 (log^2 m / m)^alpha1" (eq. 12, subset size m).
  Conditions: (A3) is an entropy condition, a compact parameter support is assumed ("we have assumed a compact support in..."), i.i.d. within subset required.
  Paper admits: "If any of the assumptions (A1)-(A4) fail, then the subset posterior distributions may approximate the full data posterior distribution
  poorly". Theorem 3.1 (linear model) has the condition "Omega_0 - a_n I_p < (1/n) X^T Sigma^{-1} X < ..." with a_n, b_m = o(1), i.e. the design Gram matrix
  of every subset must be close to a fixed positive-definite limit with p FIXED (fixed-p, large-n regime).
- Discrete model spaces: NOT handled. The theory is Wasserstein convergence of continuous parameters theta in R^p to a point mass; no discrete model
  space/variable-selection result. The paper's only "discrete" content is a discrete mixture prior (DP) with off-the-shelf samplers (line ~232) and a
  discrete barycenter *grid* (LP support), neither is model selection. The Discussion says (quoted) "it is of interest to study more deeply the impact of the
  partitioning schemes and attempt to develop approaches that deal with not only large sample sizes but also high-dimensional data."
- Plausible at n=200, p=1000? No: guarantees need m -> infinity with fixed p; at m = n/k << p the premise fails.

### 1c. Minsker, Srivastava, Lin, Dunson (2014/2017) "Robust and scalable Bayes via a median of subset posterior measures", JMLR 18(124)  [volume from memory: UNVERIFIED]
- arXiv:1403.2660. READ: https://arxiv.org/pdf/1403.2660 (pdftotext, 2718 lines).
- PARALLEL: subset posteriors in parallel; combine by geometric median in an RKHS (M-posterior).
- TARGET: approximation (robust aggregate), not the full posterior.
- GUARANTEES: Thm 2.1 (geometric median, Minsker 2013): if each of >= (1-kappa)m subset estimators satisfies Pr(d(theta_j, theta0) > eps) <= 1/4 then
  "Pr d(theta*, theta0) > 3 eps <= [e^{(1-kappa) psi(...)}]^{-m}" (metric-space median). Thm 3.1 (subset posterior contraction): needs "(1) the packing number
  satisfies log M(eps_l, Theta_l, rho) <= l eps_l^2, (2) Pi(Theta \ Theta_l) <= exp(-l eps_l^2 (C+4)), (3) [KL prior-mass condition]" for i.i.d. data of subset size l.
- Discrete model spaces: the text only says (line ~166) that stochastic-approximation MCMC methods "fail to accommodate discrete-valued parameters and
  multimodality" as a motivation, and Remark 2.3 discusses discrete measures P, Q only as kernel-embedding objects. No variable selection theory.
  The median's guarantee is for the *metric-space* median, so it could in principle apply to a space of model-probability vectors - but this paper does not do it.
- Plausible at n=200, p=1000? Entropy/prior-mass conditions are per subset with subset size l -> infinity; no design/correlation condition appears
  (i.i.d. observations; X not discussed), so nothing here can certify masked designs.

### 1d. Zhang, Lam, Lin (2018) "Robust and Parallel Bayesian Model Selection", Comput. Stat. Data Anal. 127:229-247 (venue per IDEAS/RePEc search listing)
- arXiv:1610.06194. READ: https://arxiv.org/pdf/1610.06194 (pdftotext, 1156 lines). Authors per search result (Zhang, Lam, Lin) - author names UNVERIFIED from the PDF text I grepped (I read title/abstract/theorems, not the byline).
- PARALLEL: split observations into R roughly equal subsets; run model selection (BMA, AIC, BIC, median probability model, spike-and-slab MCMC) independently
  per subset; aggregate posterior model probabilities (or inclusion probabilities) by geometric median. Sequential depth = per-subset inference + one median.
- TARGET: aggregate of subset posteriors; a different object than the full-data posterior (it is a robust estimator of the model probabilities).
- GUARANTEES (quoted): Theorem 1 (posterior contraction, Hellinger): "Assume that there is a sequence eps_N such that eps_N -> 0 and N eps_N^2 -> infinity ... and a
  set S_N in S so that 1. log D(eps_N/2, P_{S_N}, d_H) <= N eps_N^2. 2. Pr(S \ S_N) <= e^{-N eps_N^2 (C+4)}. 3. [KL prior mass]". Theorem 2 (BMA, non-nested models): needs
  "for sufficiently small eps > 0, d(P_theta, P_0) > eps for any theta in S_{-1} := {(M_k, beta, sigma^2) : k != 1}" - i.e. the true model M_1 is separated
  from every other model and non-nested. Theorem 3 (concentration improvement): with s = N/R, for sufficiently large s, the geometric-median model
  probability concentrates with failure probability exponentially small in R. Theorem 4: robustness to contaminated subsets.
- Discrete model spaces: YES, this is the only paper in group 1 that aggregates posterior model probabilities. But: the candidate model set is finite and fixed
  (K models) and the asymptotics are in N with s = N/R -> infinity; Condition "non-nested" excludes the usual BVS lattice, where models containing the truth are
  nested supersets. The paper itself notes Theorem 2 "can be modified to handle the case where multiple models contain" the truth (line ~579; modification not read).
- EVIDENCE: simulations use "a 5000 x 10 matrix ... 3 true predictors" (D = 10, R = 10 or 50). No correlated design, no p > n.
- Plausible at n=200, p=1000? No. Theory is s = N/R -> infinity with D fixed; with n = 200 and R >= 2, s <= 100 << p, and no
  eigenvalue/coherence condition is stated, so it cannot cover correlated/masked designs.

### 1e. Li, Kang, Liu, Wu (2022) "Distributed Bayesian posterior voting strategy for massive data", Electronic Research Archive 30(5):1936-1953, DOI 10.3934/era.2022098
- READ: https://aimspress.com/aimspress-data/era/2022/5/PDF/era-30-05-098.pdf (pdftotext, 1052 lines; header verified).
- PARALLEL: data stored across nodes, "each computing resource containing a disjoint subset of data"; local hierarchical-Bayes selection per node; weighted majority
  voting (BVSaC) to combine. Depth = one local Bayes fit + one vote.
- TARGET: approximation; selection set by voting, not a posterior over models.
- GUARANTEES: NONE FOUND. grep for Theorem/Assumption returned no hits; the paper appears purely empirical. Abstract claims only that it "performed as well as
  the whole sample hierarchical Bayes method in terms of the accuracy of variable selection and estimation" in simulations.
- EVIDENCE under correlation: AR(1) design Sigma_{jj'} = rho^{|j-j'|}, rho in {0.1, 0.5, 0.9}, N = 10^4, K in {1,10,20,50}. Quoted (Section 4.1): "(K, p) = (50, 500), the
  sample size of each subdataset (n_k = 200) was much smaller than p, and the proposed approach performed well when the within covariate correlation was weak (e.g.,
  rho = 0.1). With the increase of rho, the number of selected noise variables increased, and the specificity of the model selection decreased." And at rho = 0.9
  "the model sensitivity decreased with increasing values of omega". So the (only) correlated-design evidence is a DEGRADATION with rho, for AR(1) (not masked) designs.
- Plausible at n=200? Local n_k = 200 appears in their sims but total N = 10^4; our total n is 200, so splitting is not comparable.

### 1f. Other searches
- "divide and conquer Bayesian variable selection data splitting theory 2019-2026": NOT FOUND any further paper with a variable-selection consistency theorem under
  design-correlation conditions. Search surfaced Qian (2023, BJPS) "Divide-and-conquer Metropolis-Hastings samplers with matched samples" (general recombination, targets
  expectations; ABSTRACT-ONLY listing, UNVERIFIED, not read) - not model-space specific.
- Feature-splitting (SaM, DECO etc.) are covered in 02_feature_splitting.md.

---------------------------------------------------------------------------------------------------------------------------------

## 2. Johndrow, Orenstein, Bhattacharya (2020) "Scalable approximate MCMC algorithms for the horseshoe prior", JMLR 21(73):1-61
- Citation verified via search listing https://jmlr.org/papers/v21/19-536.html (landing page found by search; text content read only through the arXiv version).
  arXiv:1705.00841 (v2/v3), whose title is the earlier "Bayes Shrinkage at GWAS scale: Convergence and Approximation Theory of a Scalable MCMC Algorithm for the Horseshoe Prior".
  READ: https://arxiv.org/pdf/1705.00841 (pdftotext, 3238 lines; file stamp "lg-algos-arXiv-v2.tex date: October 16, 2018"). The JMLR text may differ in numbering.
- IMPORTANT: this is a CONTINUOUS shrinkage prior (beta_j, local scale eta_j), not a model-space posterior over S. It does not target the beta-binomial g-prior model posterior.
- PARALLEL: single Markov chain; the speedup is a cheaper per-step matrix product (thresholding of the local-scale matrix, delta) and "multicore hardware with 12 threads" for linear algebra.
  Not a parallel-in-chain algorithm; sequential depth = number of MCMC iterations (their ESS does not grow with p, empirically).
- TARGET: two algorithms: an exact blocked Metropolis-within-Gibbs; and an approximate one (threshold delta). Abstract: "Versions of the approximation algorithm that gradually
  decrease the approximation error as the chain extends are shown to be exact."
- GUARANTEES (quoted): Theorem 3.5: "Let P be the Markov transition operator with update rule given by (4). Then for any c < 1/2 1. The function V(eta, beta, sigma^2, xi) = ... is a Lyapunov function of P,
  even if no truncation of the prior on eta is used (i.e. b = 0 in (2)). 2. If b > 0 in (2), P is geometrically ergodic in the sense of (12)." Remark 3.6: "If p <= N and W is full-rank, then P is geometrically
  ergodic without any truncation". Theorem 3.13 (approximate kernel): "sup_x ||delta_x P~ - delta_x P||_TV <= C sqrt(delta) + O(delta)" with C "depending on W, z" (W = design-derived matrix; explicit
  dependence on design conditioning not stated in the part I read), V is also a Lyapunov function and "if b > 0 in (4), then P~ is geometrically ergodic". No rate (spectral gap/mixing time) as a function of n, p or of design correlation is given; geometric ergodicity is qualitative (constant alpha-bar not quantified).
- EVIDENCE under correlation: simulations with AR(1) design with autocorrelation 0.9, N sampled in [1000,5000], p in [10^4, 5*10^4]; quoted: "There is apparently little difference in ne when the
  design matrix is correlated compared to independent design." (effective sample size, empirical only; AR(1), not masked).
- Plausible at n=200, p=1000? Theory says nothing quantitative; p > N requires the truncation b > 0. Not an exact-S-posterior method in any case.

---------------------------------------------------------------------------------------------------------------------------------

## 3. SuSiE / IBSS: Wang, Sarkar, Carbonetto, Stephens (2020) "A simple new approach to variable selection in regression, with application to genetic fine-mapping", JRSS-B 82(5):1273-1300, DOI 10.1111/rssb.12388
- Citation verified via search results (OUP landing https://academic.oup.com/jrsssb/article-abstract/82/5/1273/7056114; bioRxiv 10.1101/501114; no arXiv version found).
  READ: JRSS-B PDF copy hosted at https://ibg.colorado.edu/cdrom2025/4.4.FinemappingColocalization_RanCui/refs/JRSS_Wang_2020_susie.pdf (pdftotext, 1321 lines; third-party course-hosted copy of the published paper). The bioRxiv PDF fetch returned non-PDF text and was not read.
- PARALLEL: IBSS (Algorithm 1) is a loop "for l in 1, ..., L do: r_l <- y - X sum_{l'!=l} b_l'; fit SER to r_l; b_l <- alpha_l o mu1_l", repeated "until convergence criterion satisfied".
  That is sequential coordinate ascent over the L effects (each update needs the previous ones); within one SER fit the p per-variable Bayes factors are independent, so each step is
  vectorisable (our remark). Sequential depth = (#sweeps) x L; no bound on #sweeps proved.
- TARGET: approximation. Corollary 1 (quoted): "IBSS (algorithm 1) is a co-ordinate ascent algorithm for maximizing the ELBO F over q satisfying approximation (3.7). Equivalently, it is a co-ordinate ascent
  algorithm for minimizing the KL divergence D_KL(q, p_post) over q satisfying approximation (3.7), where p_post is the true posterior distribution under SuSiE." The target is the SuSiE posterior (not the g-prior / beta-binomial model posterior), and q is a product of L single-effect factors.
- GUARANTEES: Proposition 2 (quoted): "Provided that 0 < sigma, sigma_0 < infinity and pi_j > 0 for all j = 1, ..., p, the sequence of iterates q that are generated by the IBSS method ... converges to a limit point that is a stationary point of F."
  Only convergence to a stationary point (possibly local optimum, no rate, no global optimality). NO consistency, contraction, or credible-set coverage theorem. The paper states: "95% credible sets are not designed, or guaranteed, to have a frequentist coverage of 0.95 (Fraser, 2011)."
- Theory papers on SuSiE (2023-2026): NOT FOUND. Searches ("SuSiE theoretical guarantees", "sum of single effects consistency", posterior consistency/credible set theory) returned only software docs and applied/extension papers.
  Seen in search snippets only (UNVERIFIED, not opened): a Cox-model SuSiE paper (arXiv 2506.06233) said to note that IBSS "can be rigorously justified as optimizing a variational approximation" only for the Gaussian case; a 2025 bioRxiv on small-sample calibration (10.1101/2025.05.16.654543).
- EVIDENCE under correlation: designed for it: intro says variants can have "sample correlations exceeding 0.99, or even equalling 1"; the genotype matrices have "the median number of other variables with which its correlation exceeds 0.9 is 8".
  Section 4.1 is a *masking-like* example (read): "the variable with the strongest marginal association (SMA) with y is not one of the actual effect variables ... Standard forward selection ... would select the wrong (SMA) variable in the first step; ... after 10 iterations ... IBSS yields two high purity credible sets, neither containing the SMA". Evidence is an illustrative example and simulations, with credible sets "slightly below 0.95, and in most cases above 0.90" coverage, not a proof.
- Plausible at n=200, p=1000? Convergence statement holds for any design (no design condition), but it is only to a stationary point of the variational objective; accuracy vs the exact model posterior under masking is empirical. Note the IBSS mean-field-over-effects form cannot represent the posterior dependence among effects (our remark; in the paper's own words the VA "is different from previous 'fully factorized'" ones).

---------------------------------------------------------------------------------------------------------------------------------

## 4. Variational BVS with guarantees

### 4a. Ray & Szabo (2022) "Variational Bayes for high-dimensional linear regression with sparse priors", JASA 117(539):1270-1281  [volume/pages from memory: UNVERIFIED]
- arXiv:1904.07150. READ: https://arxiv.org/pdf/1904.07150 (pdftotext, 2638 lines).
- PARALLEL: mean-field spike-and-slab VB solved by coordinate-ascent (CAVI): "In CAVI, we sequentially update the parameters gamma_i, sigma_i, mu_i, i = ..."; paper shows CAVI is sensitive to update order and proposes a
  prioritised order (inherently sequential). Depth = #sweeps x p coordinate updates (updates within a sweep depend on each other).
- TARGET: approximation: a mean-field VB posterior (and "Q-hat", "Q-tilde" families); not the exact posterior. Abstract: "oracle inequalities are derived for the mean-field VB approximation".
- GUARANTEES: Definition 1 (quoted): "A model S subset {1,...,p} has compatibility number phi(S) = inf { ||X theta||_2 |S|^{1/2} / (||X|| ||theta_S||_1) : ||theta_{S^c}||_1 <= 7 ||theta_S||_1, theta_S != 0 }." Definition 2 (uniform compatibility for sparse vectors): phi(s) = inf{||X theta||_2 |S_theta|^{1/2}/(||X|| ||theta||_1) : 0 != |S_theta| <= s}.
  Definition 3: smallest scaled sparse singular value phi~(s) = inf{||X theta||_2/(||X|| ||theta||_2): 0 != |S_theta| <= s}. Text: "We shall require that these numbers are bounded away from zero for s a multiple of the true model size."
  Theorem 1 (Recovery, quoted shape): under prior (3) satisfying (4),(5) and lambda = O(||X|| sqrt(log p / s_n)), sup over theta0 in Theta_{rho_n,s_n} := {phi(S0) >= c0, |S0| <= s_n, psi~_{rho_n}(S0) >= c0} of E_{theta0} Pi~{ ||X(theta - theta0)||_2 >= M rho_n^{1/2} sqrt(|S0| log p) / (psi_{rho_n}(S0) phi(S0)) } -> 0 (and analogous l1, l2 bounds),
  for any rho_n -> infinity, "where M > 0 depends only on the prior." (psi_M(S) = phi((2 + 4M/A^4)(1 + 16 lambda/(phi(S)^2 lambda-bar))|S|), i.e. the sparse compatibility at a constant multiple of |S0|.)
  The guarantee is contraction in prediction / l1 / l2 loss around theta0 - NOT model-selection (S) consistency or inclusion-probability accuracy; the stated remark is that Theorem 1 "does not imply that the VB posterior..." (line ~419; remainder not read in full).
  Design examples where the constants are bounded away from zero (quoted): "diagonal matrices, orthogonal designs, i.i.d. (including Gaussian) random matrices and matrices satisfying the 'strong irrepresentability condition' of [49]."
- EVIDENCE: simulations n = 100, p = 200, s = 20, X_ij ~ N(0,1) (i.i.d.) - no strongly correlated designs read.
- Plausible at n=200, p=1000, strongly correlated/masked? The compatibility constants phi(S0), phi~(c|S0|) must be bounded below by a constant; with strong correlation (e.g. correlation 0.99 between hub and partner), phi~(2) <= about sqrt(1 - rho) -> small, so the contraction rate degrades (our calculation, rate scales with 1/phi). Masked linked-hub truths have a non-identifiable-ish sparse subspace: some sparse eigenvalue is near 0. Not a certificate for our designs, and again an approximation.

### 4b. Yang, Pati, Bhattacharya (2020) "alpha-variational inference with statistical guarantees", Ann. Statist. 48(2):886-905, DOI 10.1214/19-AOS1827 (venue verified via search listing)
- arXiv:1710.03266. READ: https://arxiv.org/pdf/1710.03266 (pdftotext, 2801 lines).
- PARALLEL: no algorithm contribution beyond the mean-field/CAVI-type VB in the cited literature; a statistical (risk-bound) paper.
- TARGET: approximation (alpha-fractional VB, alpha < 1 requires only a prior-mass condition; alpha = 1 needs testing conditions).
- GUARANTEES: Corollary 4.2 (spike-and-slab linear regression with mean-field q over (sigma, (z_j, beta_j))): "Suppose p_{beta|z*} is continuous and thick at beta*_{z*}, and p_sigma is continuous and thick at sigma*. If s log d / n -> 0 as n -> infinity, then it holds with probability tending to one ... [integral h^2 ... q-hat] ^{1/2} <~ sqrt( s/(n min{alpha,1-alpha}) log(dn) )" (Hellinger-type risk on the likelihood scale).
  Quoted comment: "Corollary 4.2 implies a convergence rate sqrt(n^{-1} s log(dn)) of the variational-Bayes estimator beta-hat under the restricted eigenvalue condition [5]". The explicit design assumption in the appendix (supplement, line ~2608, quoted): "we make the sparse eigenvalue assumption that there exists some sufficiently large C > 0, such that for any Cs sparse vector u, n^{-1}||Xu||^2/||u||^2 >= mu > 0" (used to verify Assumption T for the alpha = 1 case).
  Model-selection consistency not claimed.
- EVIDENCE: n = 100 linear regression simulation referenced (Section B.1, line ~1352); no masked design.
- Plausible at n=200, p=1000, strongly correlated? Sparse-eigenvalue lower bound mu must be a constant at sparsity C*s; a block with correlation near 1 gives mu -> 0 even at sparsity 2, so the rate constant degrades; the result concerns prediction risk, not S.

---------------------------------------------------------------------------------------------------------------------------------

## 5. GPU / vectorised / parallel BVS samplers, and the sequential benchmark

### 5a. Zanella & Roberts (2019/2021) "Scalable importance tempering and Bayesian variable selection", JRSS-B 81(3):489-517 (venue from memory: UNVERIFIED; arXiv:1805.00541)
- READ: https://arxiv.org/pdf/1805.00541 (pdftotext, 1553 lines).
- PARALLEL: tempered Gibbs sampler (TGS / wTGS): at each iteration all p modified conditionals Z(x) = sum_i ... are evaluated, then coordinate i is picked proportional to its
  weight; importance weight w(x) = 1/Z(x). The p conditionals are computed in one vectorised pass; the *chain itself is sequential*. Paper's quoted costs: "cost per iteration of TGS and wTGS is of order O(np + |gamma|p) ... For comparison, the cost per iteration of GS is O(n|gamma| + |gamma|^2) ... relative additional cost of TGS over GS is O(p/|gamma|)". The paper does not claim GPU use; it explicitly contrasts with "classical simulated and parallel tempering".
- TARGET: EXACT posterior (importance-weighted ergodic averages of the original target f; validity via Meyn-Tweedie).
- GUARANTEES: Theorem 1 (quoted): "For every h in L2(X, f) we have var(h, TGS) <= b^2 var(h, GS) + b^2 var_f(h)." (b = user-chosen constant bounding the modification of the conditionals; "TGS cannot perform worse than standard GS by more than a constant factor that can be chosen by the user"). Condition (2): "Z(x) is bounded away from 0, and bounded above on compact sets."
  This is a RELATIVE statement vs. systematic-scan Gibbs: no absolute mixing-time bound, no design condition (so nothing proved that TGS mixes under correlated designs, only that it is not much worse than GS, and the paper itself says "GS and TGS will perform similarly" for some correlation structures).
- EVIDENCE under correlation: bivariate Gaussian rho = 0.999 example (TGS mixing "uniformly bounded regardless of the correlation structure" there, line ~469, for the specific g = f^(beta), beta = 1 - rho^2 choice; GS diverges); BVS simulations (read headings only).
- Plausible at n=200, p=1000 masked? Applies (any X), exact target, but no guarantee beyond "not worse than GS by factor b^2"; GS can be slow with masked pairs.

### 5b. Jankowiak (2022/2023) "Bayesian Variable Selection in a Million Dimensions", AISTATS 2023  [venue from memory: UNVERIFIED]; arXiv:2208.01180
- READ: https://arxiv.org/pdf/2208.01180 (pdftotext, 2054 lines; title/author verified).
- PARALLEL: Subset wTGS: cost per iteration "sublinear in P" (abstract: "an efficient MCMC scheme whose cost per iteration is sublinear in P"), implemented in PyTorch on GPU; quoted: "most of the necessary tensor ops are highly-parallelizable and very efficiently implemented on modern hardware." Chain still sequential. Runtimes reported: 50k MCMC samples for P = 7.5x10^5 in ~35 minutes on a Tesla T4.
- TARGET: asymptotically exact in the sense of weighted consistency: Proposition 1 (quoted): "The Subset wTGS estimator sum_t rho^(t) h(gamma^(t)) -> E_{p(gamma|D)}[h(gamma)] as T -> infinity almost surely for every test function h". LLN only; no rate; no design condition.
- EVIDENCE: Section 7.2 "PG-wTGS and correlated covariates": binomial regression, two covariates (i in {1,2}) "highly correlated and each alone can explain the response ... 32 <= N <= 512, 32 <= P <= 4096". Also correlated real data (cancer P = 17273). Empirical only; the paper reports PG-wGS "does poorly on all datasets" and notes ASI issues. The two-correlated-covariates mode-switching example is related to, but easier than, masking (each alone explains y, whereas masked variables are marginally weak).
- Plausible at n=200, p=1000 masked? Not tested; no guarantee.

### 5c. Griffin, Latuszynski, Steel (2021) "In search of lost mixing time: adaptive MCMC schemes for Bayesian variable selection with very large p", Biometrika 108(1) [venue from memory: UNVERIFIED]; arXiv:1708.05678
- READ: https://arxiv.org/pdf/1708.05678 (v3, May 2019; pdftotext, 1822 lines).
- PARALLEL: adaptive non-local proposals; abstract: "easily implementable on multi-core architectures and are well suited for parallel tempering or sequential Monte Carlo implementations"; conclusion: "We have only considered serial implementations of our algorithms in this paper ... naturally parallelizable across the multiple chains but work is needed on efficient updating of the shared adaptive parameters."
- TARGET: exact (adaptive MCMC for the spike-and-slab posterior).
- GUARANTEES: Theorem 1 (quoted): "Consider the target pi_p(gamma) of (14), ... Then ergodicity (17) and the strong law of large numbers (18) hold for each of the algorithms: EIA, ASI and their multiple chain acceleration versions." (via simultaneous uniform ergodicity + diminishing adaptation; qualitative.) Design assumption: none quantitative.
- EVIDENCE: motivation is that "in large p small n settings, the majority of the p variables will be approximately uncorrelated a posteriori" (so strongly correlated *relevant* variables are the hard case); parallel tempering is "most helpful" for multimodal examples.

### 5d. Schafer & Chopin (2013) "Sequential Monte Carlo on large binary sampling spaces", Stat. Comput. 23:163-184; arXiv:1101.6037 (venue from memory)
- READ (selectively): https://arxiv.org/pdf/1101.6037. No Theorem/Proposition on consistency found by grep.
- PARALLEL (quoted, discussion): "the Sequential Monte Carlo algorithm can be parallelised in the sense that we can, on suitable hardware, run many evaluations of pi in parallel during the move step ... No analogue speed-up can be performed in the context of Markov chains. We have processed variable selection problems from genetics with about a thousand covariates within a few hours running a parallelised version of the algorithm on a 64-CPU cluster."
  Sequential depth = number of tempering steps (adaptive; data-dependent), each step parallel over particles.
- TARGET: SMC approximation (weighted particles) to the exact posterior; unbiased normalising constant (standard SMC fact, not checked in text). Guarantees: none proved for design conditions; the paper is methodological. (The "g-prior" is mentioned only as used in Clyde et al. (2011); this paper's BVS example is a logistic regression, per the "logistic" mentions - not fully verified.)
- EVIDENCE: hard "difficult instances" empirically; no design-conditioned theory. (SMC-for-BVS 2020-2026 papers with theory: NOT FOUND; one search returned only Schafer-Chopin and Griffin et al.)

### 5e. GPU / massively parallel exact BVS 2018-2026
- Search "GPU Bayesian variable selection": only Jankowiak (5b) is a BVS-specific GPU paper found. Others found were generic (Lee et al. 2010 GPU Monte Carlo arXiv:0905.2441; a 2020 BayesXII CPU paper; a 2026 LAFI talk) - ABSTRACT/LISTING-ONLY, UNVERIFIED, not BVS-specific. A paper combining (exact model posterior) + (GPU/many-chain parallel) + (design-conditioned theory): NOT FOUND.
- Parallel tempering for BVS with theory: NOT FOUND (only empirical use in Griffin et al.).

### 5f. Yang, Wainwright, Jordan (2016) "On the computational complexity of high-dimensional Bayesian variable selection", Ann. Statist. 44(6):2497-2532 [venue from memory: UNVERIFIED]; arXiv:1505.07925
- READ: https://arxiv.org/pdf/1505.07925 (pdftotext, 2557 lines; title/authors verified).
- Model (read): Zellner g-prior with beta_gamma | gamma ~ N(0, g phi^{-1}(X_gamma^T X_gamma)^{-1}), precision prior 1/phi, sparsity prior pi(gamma) proportional to (1/p)^{kappa|gamma|} I[|gamma| <= s0] (truncated at s0; NOT the beta-binomial exactly but close in spirit). g ~ p^{2 alpha} (Assumption C). So their target resembles ours: g-prior, model posterior.
- PARALLEL/ALGORITHM: single-flip/swap Metropolis-Hastings (a shotgun-stochastic-search-like local move chain). Sequential. Cost per move O(...) in n and |gamma|; number of iterations bounded as below.
- TARGET: exact posterior pi_n(gamma | Y) (chain stationary for it).
- GUARANTEES (quoted): Assumption B (design): "The design matrix has been normalized so that ||X_j||_2^2 = n for all j ... Lower restricted eigenvalue (RE(s)): min_{|gamma| <= s} lambda_min( (1/n) X_gamma^T X_gamma ) >= nu, and Sparse projection condition (SI(s)): E_Z[ max_{|gamma|<=s} max_{k in [p]\gamma} (1/sqrt(n)) <(I - Phi_gamma) X_k, Z> ] <= (1/2) sqrt(L nu log p)" with Phi_gamma the projection onto span{X_j, j in gamma}.
  "The sparse projection condition can always be satisfied by choosing L = O(s0)"; paper notes L = 4 nu^{-1} s0 always works. Assumption D(s0) (sandwich): "(2 nu^{-2} omega(X) + 1) s* <= s0 <= ..." with omega(X) := max_gamma |||(X_gamma^T X_gamma)^{-1} X_gamma^T X_{gamma*\gamma}|||_op^2 (a collinearity measure between a model and the true variables outside it).
  Theorem 1 (posterior concentration): under A, B (s = K s*), C, D(s*), and beta-min threshold C_beta^2 >= c0 (L + L-tilde + alpha + kappa) sigma0^2 log p / n: "then we have pi_n(gamma* | Y) >= 1 - c1 p^{-1} with probability at least 1 - c2 p^{-c3}."
  Theorem 2 (quoted): "there are universal constants c1, c2 such that, for any epsilon in (0,1), the epsilon-mixing time of the Metropolis-Hastings chain (3) is upper bounded as tau <= c1 p s0^2 c2^alpha [ (n + s0) log p + log(1/epsilon) ] + 2 with probability at least 1 - 4 p^{-c1}" (pdftotext rendering: "c1 ps20 c2 alpha (n + s0) log p + log(1/eps) + 2"; reading as c1 p s_0^2 c_2^alpha ((n+s_0) log p + log(1/eps))). Linear in p, quadratic in s0. They additionally need a high/low SNR condition (9a)/(9b) on every beta_j* and say, quoted: "Based on our simulations, we suspect that the Markov chain might be slowly mixing in this regime [intermediate signals], but we do not have a proof."
  Remark in Zhou et al. (below): "Yang et al. [2016] assumed that s0 log p <= n/32."
- EVIDENCE: simulations with n up to 500, p up to 1000 (table at line ~680), also a lasso failure example (line ~560, not read in detail).
- Plausible at n=200, p=1000, strongly correlated/masked? Consider the stated constants: s0 log p <= n/32 gives, for n = 200, p = 1000, s0 <= 200/(32 * 6.91) = 0.9 < 1, i.e. no s0 >= 1 satisfies the literal constant (arithmetic is ours; the theorem is stated with unspecified universal constants, so this is a statement about the literal remark, not about the theorem's truth). RE(s) needs lambda_min of every s-subset Gram >= nu > 0 with s = K s0: strong correlation within a hub block drives lambda_min -> 0 (nu small makes L, mixing bound and beta-min threshold large). omega(X) is large exactly when a model's span nearly contains the omitted true variables (the masking mechanism), forcing s0 >= 2 nu^{-2} omega(X) s* to blow up. So the theorem plausibly does NOT give usable bounds for linked-hub designs at n = 200.

### 5g. Zhou, Yang, Vats, Roberts, Rosenthal (2022) "Dimension-free mixing for high-dimensional Bayesian variable selection", JRSS-B 84(5):1751-1784, DOI 10.1111/rssb.12546 (venue verified via search listing); arXiv:2105.05719 (v3, 23 Apr 2022; v1 titled "A local MCMC algorithm for variable selection with dimension-free mixing time")
- READ: https://arxiv.org/pdf/2105.05719 (pdftotext, 2703 lines).
- PARALLEL: LIT-MH (locally informed and thresholded MH): informed proposal over all p neighbours. Costs (quoted): with X^T X, X^T y precomputed "each addition or deletion move has complexity O(p|gamma|^2) for LIT-MH and complexity O(|gamma|^2) for RW-MH". The per-iteration all-p evaluation is parallelisable (our remark); the chain is sequential. Sequential depth: Tmix <= 800 max{n kappa1 / c1, 3 s0} iterations, independent of p.
- TARGET: exact posterior pi_n on M(s0) = models with |gamma| <= s0 (same g-prior-type model as YWJ; prior pi(gamma) with kappa = kappa0 + kappa1 penalties, not beta-binomial exactly).
- GUARANTEES (quoted): CONDITION 1: "There exist gamma* in M(s0) and constants c0, c1 > 0 (not depending on gamma) such that ... (1a) For any overfitted gamma in M(s0) and j not in gamma, B(gamma, gamma U {j}) <= p^{-c0}. (1b) For any underfitted gamma in M(s0), there exists some j in gamma* \ gamma, which may not be unique, such that B(gamma, gamma U {j}) >= p^{c1}. (1c) For any underfitted gamma with |gamma| = s0, there exist some j in gamma* \ gamma and k in gamma \ gamma* ... such that B(gamma, (gamma U {j}) \ {k}) >= p^{c1}." (B = Bayes factor.)
  THEOREM 1 (quoted): "Suppose that n = O(p), s0 log p = O(n) and kappa = O(s0). If Condition 1 holds for c0 = 2 and 4 <= c1 <= n kappa1 - kappa, then, for sufficiently large n, we have T_mix <= 800 max{ n kappa1 / c1, 3 s0 }."
  Remark 2 (quoted): "The assumptions we have made in Theorem 1 are mild and are essentially the same as those of Yang et al. [2016]." And "Condition 1 essentially assumes that pi_n is unimodal on M(s0)" (paraphrase of their line ~378: "Thus, Condition 1 essentially assumes that pi_n is unimodal on M(s0) with respect to the ..." sentence truncated in my read). They say Condition 1 holds w.h.p. under YWJ's assumptions ("proved in Yang et al. [2016, Lemma 4]"); they treat X as fixed in the mixing proof.
  Text about underfitting (quoted): "If gamma is underfitted ... the analysis becomes much more complicated due to the correlation among the covariates ... a known result from forward-backward stepwise selection [An et al., 2008] guarantees that an underfitted model will eventually become overfitted ... as long as the sample size n and beta_min in (8) are sufficiently large relative to the collinearity in X."
- EVIDENCE: Section 5 simulations (not read in detail; they include correlated designs per my skim only - UNVERIFIED).
- Plausible at n=200, p=1000, strongly correlated/masked? Condition 1(1b) is the crux: from any underfitted gamma, SOME missing true variable must have Bayes factor >= p^{c1} for adding it. For a masked linked-hub truth, at gamma = empty (underfitted) each true variable is marginally weak, so the Bayes factor of adding any single true variable alone is NOT large; the strong gain is only from adding the hub+partner jointly (a 2-step uphill with a valley). So 1(b) is expected to FAIL for masked designs (our inference; the paper does not say this). The condition is posterior-landscape unimodality; with n = 200 the constants "sufficiently large n" and s0 log p = O(n) are unlikely to hold safely either (p^{c1} with c1 >= 4 at p = 1000 means Bayes factor >= 10^12).

---------------------------------------------------------------------------------------------------------------------------------

## Cross-cutting assessment (for the claim under test)
- "Sequential with strong guarantees": SUPPORTED by what I read: the only guarantees with explicit design conditions and a number-of-iterations bound are for sequential MH chains (YWJ: ~ p s0^2 (n+s0) log p iterations; Zhou et al.: ~ max(n kappa1 / c1, 3 s0) iterations, each iteration O(p|gamma|^2) work). Their design conditions (RE(s) plus sparse projection / Condition 1 unimodality) are not design-agnostic: they exclude strong collinearity and plausibly exclude masking (1b). So "strong guarantees" is itself conditional on benign correlation; the claim that guarantee-bearing sequential methods are fine under correlated designs is NOT supported by theory.
- "Parallel-friendly methods with guarantees": data-splitting (WASP, M-posterior, CMC) guarantees are fixed-p, per-shard-n -> infinity, i.i.d./entropy conditions and say nothing about discrete model spaces; the only data-splitting BVS theory (Zhang et al. 2018) is fixed small D and non-nested models. Feature-splitting is in note 02 (SaM needs cross-split faithfulness; DECO needs random Gaussian design with eigenvalue bounds). Exact parallel-in-computation samplers (wTGS/GPU, adaptive MCMC with multiple chains, SMC) have only qualitative (ergodicity/SLLN/relative-to-Gibbs) guarantees, which hold under any design but give no mixing rate. So "parallel-friendly + guarantees + exact + correlated-robust" combination is NOT FOUND in the literature I read.
- Caveat: "breaks under correlated designs" is shown here by (i) theory conditions that fail (our inference) and (ii) one empirical degradation for data-splitting (Li et al. 2022, AR(1) rho = 0.9), not by a published negative result.
- Variational methods (Ray-Szabo, Yang-Pati-Bhattacharya, SuSiE) are approximations; their conditions (compatibility / sparse eigenvalue) are bounded below only for benign designs; under 0.99 correlations the constants degrade; SuSiE has only a stationary-point convergence proposition.

## Sources actually read
All pdftotext-extracted from /tmp/litpar_dl3 (arXiv PDFs) unless noted:
- https://arxiv.org/pdf/1508.05880 (WASP, Srivastava-Li-Dunson), selected passages and theorem statements
- https://arxiv.org/pdf/1403.2660 (Minsker et al. M-posterior), Thm 2.1, 3.1, intro passages
- https://arxiv.org/pdf/1610.06194 (Robust and Parallel Bayesian Model Selection), abstract, Thm 1-3, simulation setup
- https://aimspress.com/aimspress-data/era/2022/5/PDF/era-30-05-098.pdf (Li et al. 2022), abstract, simulation section
- https://arxiv.org/pdf/1705.00841 (Johndrow et al.), abstract, Thm 3.5, 3.13, Assumption 3.7-3.8, simulation passage
- https://ibg.colorado.edu/cdrom2025/4.4.FinemappingColocalization_RanCui/refs/JRSS_Wang_2020_susie.pdf (SuSiE JRSS-B), Algorithm 1, Cor. 1, Prop. 2, Sec 4.1, coverage passage
- https://arxiv.org/pdf/1904.07150 (Ray-Szabo), Definitions 1-3, Theorem 1, CAVI passage
- https://arxiv.org/pdf/1710.03266 (Yang-Pati-Bhattacharya), Corollary 4.2, sparse-eigenvalue assumption in appendix
- https://arxiv.org/pdf/1505.07925 (Yang-Wainwright-Jordan), model (5a-d), Assumptions A-D, Thm 1, Thm 2
- https://arxiv.org/pdf/2105.05719 (Zhou et al.), Condition 1, Thm 1, Remark 2, cost passage
- https://arxiv.org/pdf/1805.00541 (Zanella-Roberts), cost passages, Theorem 1, intro summary
- https://arxiv.org/pdf/2208.01180 (Jankowiak), abstract, Prop. 1, complexity/GPU passages, Sec 7.2
- https://arxiv.org/pdf/1708.05678 (Griffin et al.), abstract, Theorem 1, conclusion
- https://arxiv.org/pdf/1101.6037 (Schafer-Chopin), parallelisation discussion passage only
- https://research.google/pubs/bayes-and-big-data-the-consensus-monte-carlo-algorithm/ (Scott et al., landing page via WebFetch; abstract only)
Seen only in search-result snippets / listings (UNVERIFIED beyond that): JMLR landing pages (jmlr.org/papers/v21/19-536.html), OUP JRSS-B abstract page, Project Euclid AoS page for YPB, IDEAS/RePEc listing for Zhang-Lam-Lin, Qian (2023, BJPS) divide-and-conquer MH, arXiv:2506.06233 (Cox SuSiE), bioRxiv 2025.05.16.654543, arXiv:0905.2441. Journal volume/page numbers marked "from memory" above were not verified in this session. Not obtained: Scott et al. full text; Song-Liang SaM paper (see note 02).
