# LIT-PAR notes 02: feature-splitting methods

## Song & Liang (2015) SaM, JRSSB 77(5):947-972, doi 10.1111/rssb.12095
Full paper NOT accessible (paywalled; no arXiv found). Theorem statements READ from Liang's own lecture slides:
https://www.stat.purdue.edu/~fmliang/STAT598Purdue/partI4.pdf (author-hosted; slides "Revisit of Computational Strategies:
split-and-merge"). Status: primary-author source, but slides, not the paper; exact constants should be checked against the paper.
- Method (slides): "1. Split P_n predictors into K_n groups s_1..s_Kn, max|s_i| <= s. 2. Stage I: Select predictors from each subset
  D_n^{s_i} = {y, X_{s_i}} at a FDR level alpha_1 ... 3. Stage II: Merge ... Perform Bayesian variable selection on the aggregated
  dataset D_n^{S~} = {y, X_{S~}} at a FDR level alpha_2". Subset posteriors computed by SAMC (adaptive MCMC) - each worker is sequential MCMC.
- Thm 1-2 (posterior consistency, correctly specified, full data): Hellinger-ball contraction under rate conditions (6)-(12) and
  moment condition (A1).
- (B1) Identifiability (quoted): "A predictor x_k is said to be identifiable among all other predictors, if, for any 1 <= j_1..j_{r̄n} <= P_n
  (j_i != k) and b_i in R, E exp{-(x_k + sum b_i x_{j_i})^2} <= 1 - delta_n, and delta_n >> eps_n^2" ... "It controls the severeness of
  multicollinearity". Thm 3 (sure screening): identifiable true predictor has posterior inclusion -> 1.
- Thm 4-5 (MISSPECIFIED subset, the Stage-I guarantee): posterior on subset s concentrates on the KL projection f_0;
  Thm 5 (quoted): "If x_s does not have exact multicollinearity ... then ... pi(s~ ⊂ xi | D_n^s) -> 1", where s~ = "the subset of s
  corresponding to nonzero entries of beta_0" (beta_0 = KL/least-squares projection of the truth onto span(X_s)).
- CORRELATION CONDITION IMPLICIT IN THE SCREENING GUARANTEE: a true predictor j in subset s is retained only if its coefficient in the
  POPULATION PROJECTION onto X_s is nonzero. If correlation with true predictors in OTHER subsets cancels its within-subset projection
  coefficient (masking / unfaithfulness across the split), Stage I discards it and Stage II cannot recover it; Stage II's posterior is
  the posterior restricted to S~, not the full posterior. Stage-II consistency therefore needs S_0 ⊆ S~, i.e. every true predictor has a
  nonzero projection coefficient within its own subset (a cross-split "faithfulness" condition). [Our reading of Thm 5; CHECK in paper.]
- Asymptotic in n; no finite-n bound; no computational (mixing) guarantee for SAMC on each subset.
- DECO paper's critique (quoted, Wang-Dunson-Leng 2016 p.2): "the screening step taken on each subset might select a large number of
  unimportant but correlated variables (Song and Liang, 2014), so the split-and-merge procedure could be ineffective in reducing the
  model dimension."
- LH relevance: in a linked-hub design where the truth is masked at the marginal/subset level, a random split separating hub and partner
  makes the within-subset projection coefficient of a true variable ~ 0 -> screened out. Correlation-clustered splitting (keeping LH
  pairs together, as our blocks do) would avoid this, but SaM's theory does not assume or analyse clustering.

## Wang, Dunson, Leng (2016) DECO, NeurIPS 29; arXiv:1602.02575 (read: arXiv PDF v1, pdftotext)
- Method: global decorrelation X~ = sqrt(p)(XX^T + r1 I)^{-1/2} X, Y~ likewise (Stage 1, needs XX^T: one global O(n^2 p) step and a
  synchronisation), then lasso on each feature subset in parallel, then optional refinement.
- Motivation (quoted): "A partition of the feature space would succeed only when the features across the partitioned subsets were
  mutually independent. Otherwise, it is highly likely that any model posed on the subsets is mis-specified and the results are biased
  regardless of the sample size."
- Thm 2 (s-sparse; quoted shape): with lambda_n = A sigma_0 sqrt(log p / n), "if p > c0 n for some c0 > 1 and 64 C0^2 A^2 s^2 log p / n <= 1",
  then w.p. >= 1 - 8p^{1-C1A^2} - 18 p e^{-Cn}: ||b^-b*||_inf <= (5C0 A sigma_0/8) sqrt(log p/n), sign consistency.
  Assumptions: X ~ N(0, Sigma) random Gaussian design, sub-Gaussian noise; constants via Lemma 7 (Wang et al. 2015b) where
  "c_*, c^* are the smallest and largest eigenvalues of Sigma". So "(almost) no assumptions" = no irrepresentable condition, but
  bounded spectrum of Sigma enters every constant; sigma_0^2 = var(Y) (not sigma^2) appears in the rate.
- Target: lasso point estimate (frequentist). No posterior, no model-space uncertainty.
- Our designs: fixed design, n = 200, s^2 log p / n is not small; LH/strongly correlated designs have small lambda_min(Sigma).
  Complementary (point estimation), not a threat to an exact-posterior claim.

## Coats, Davies, Gupta (2026) "A Bayesian Bi-Directional Splitting Framework for Variable Selection in Large Datasets", arXiv:2609.20000v1 (17 Sep 2026)
Read: arXiv PDF. Row+column splitting, SaM-like screening per batch, two-phase consensus. No theory (no theorem found by grep).
Evidence (quoted, Fig. 5 caption): "Simple splitting performs well up until around rho = 0.6, beyond which the F1 score drops
dramatically. Shuffling, on the other hand, is considerably more robust" (Toeplitz correlation). Simple (contiguous) splitting F1
"dropped from around 1 for lower correlations, to 0.126 for the highly correlated case" (rho = 0.99). They also say (Sec 3, quoted): "It may be
beneficial, where possible, to allocate highly correlated columns of X to separate sub matrices in order to mitigate potential
adverse effects of multicollinearity." NOTE: the OPPOSITE of our correlation-clustered blocks (and the opposite of what masking needs:
separating a masked pair destroys the joint signal). => 2026 empirical confirmation that
feature-split BVS is correlation-fragile; no guarantees. Its related-work states "Methods that combine row-wise and column-wise
partitioning within a unified D&C framework for variable selection remain comparatively underexplored."
