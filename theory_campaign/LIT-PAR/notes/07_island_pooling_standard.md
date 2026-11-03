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
