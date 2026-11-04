# LIT-PAR notes 07: Z-weighted pooling of independent SMC runs is STANDARD (threat to novelty of T31(i))

## Dai, Heng, Jacob, Whiteley (2022), "An invitation to sequential Monte Carlo samplers", JASA 117(539) (venue per arXiv comments;
## journal page not opened). READ: arXiv:2007.11936v3 (17 Jun 2022), Sec 4.2 "Independent systems of fixed size".
- Quoted: "Consider R independent SMCS runs, with a fixed number of particles N. The runs can be executed on parallel machines ...
  We can obtain consistent approximations of pi and Z as R -> infinity, even though N is fixed (e.g. Whiteley et al. 2016, Rainforth et al.
  2016). Since the normalizing constant estimator is unbiased, we can directly average (Z^{N,r}) to obtain a consistent estimator of Z
  as R -> infinity." Then, via Andrieu, Doucet, Holenstein (2010): "a self-normalized importance sampling estimator after
  Rao-Blackwellizing the index k is thus pi-bar^R(phi) = sum_r Z^{N,r} pi^{N,r}(phi) / sum_r' Z^{N,r'}, which approximates pi(phi) as
  R -> infinity, for any fixed N. Its asymptotic variance can be estimated consistently as R -> infinity to construct confidence intervals".
  Also: "independent SMCS can be run on parallel machines without communication; results can be refined with more independent runs
  without hitting memory limits". "More advanced schemes where 'islands' of particles are allowed to communicate have been studied in
  e.g. Vergé et al. (2015), Whiteley et al. (2016)."
- IMPLICATION: our T31(i) ("Z-weighted pooling consistent as islands R -> infinity at fixed N") is exactly eq. (4.8) here; it is a known
  consequence of unbiasedness of Z^ (Del Moral 2004) and the PMCMC extended-target identity (Andrieu-Doucet-Holenstein 2010).
  T31(i) must be cited as standard; its only possible novelty is verifying the hypotheses for v3 as run (frozen calibration =>
  unbiasedness: P6/P7), i.e. the "given the frozen calibration" clause, which IS method-specific.
- Ma (2015) LIPS (notes 01) already used islands with averaged Horvitz-Thompson estimates for BMA.

## Liang, Lohani, Lukens, Kirby, Searles, Law, "SMC Is All You Need: Parallel Strong Scaling", arXiv:2402.06173v2 (2 Jun 2024);
## v3 (Aug 2025) retitled "Comparison of parallel SMC and MCMC for Bayesian deep learning" (per arXiv listing; v3 not read). Peer review UNVERIFIED.
READ: v2 PDF.
- pSMC = P non-communicating SMC islands, estimator (6) = sum_p F^{N,p}(phi) / sum_p F^{N,p}(1) (Z-weighted island pooling).
- Thm 3.1 (quoted): "Given Assumptions C.1 and C.2, for suitable values of (M, N, J) there exists a C_phi > 0 ... such that for any P in N,
  E[(phi^pSMC - pi(phi))^2] <= C_phi / (N P)." Assumptions (quoted): C.1 "C^{-1} < f_j(theta), L(theta) <= C" (bounded likelihood/weights);
  C.2 "there exists a rho in (0,1) such that for any (u,v) ... integral_A M_j(u,du') >= rho integral_A M_j(v,dv')" (uniform Doeblin mixing
  of EVERY kernel). Text: "Only standard assumptions are required, which essentially state that the likelihood is bounded above and below
  and the MCMC kernel is strongly mixing".
- Table 1: pSMC time cost COST(d,m) COST_over(d,m) N (independent of P), MSE C_SMC(d,m)/(NP): "parallel strong scaling" = fixed wall time,
  error -> 0 as processors P -> infinity.
- THREAT: the work/depth framing "fixed depth, width R -> infinity, error O(1/(NR))" for Z-weighted islands is PUBLISHED (2024) as a generic
  claim, under global-mixing assumptions. Our paper must cite it and position the contribution as: (a) BVS-specific constants
  (C_phi depends on dimension through rho and C; for BVS on {0,1}^p a uniform Doeblin rho is typically exponentially small in p),
  (b) depth given by the stage count with explicit O-STAGES laws, (c) a regime (masked start) where C_phi-type constants are analysed.
  Our designs: Assumption C.2 with p-free rho fails for BVS posteriors with strong correlation (it would imply O(1) global mixing).
