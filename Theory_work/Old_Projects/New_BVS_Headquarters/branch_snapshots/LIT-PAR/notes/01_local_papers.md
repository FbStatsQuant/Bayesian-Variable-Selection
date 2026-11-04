# LIT-PAR notes 01: local PDFs read (Papers/Core_bibliography)

## Papaspiliopoulos & Rossell (2017), "Bayesian block-diagonal variable selection and model averaging", Biometrika 104(2); arXiv:1606.03749v2
File read: Papers/Core_bibliography/12_2017_Papaspiliopoulos_Rossell_*.pdf (pdftotext).
- Abstract (quoted): "We propose a scalable algorithmic framework for exact Bayesian variable selection and model averaging in linear
  models under the assumption that the Gram matrix is block-diagonal, and as a heuristic for exploring the model space for general
  designs. ... The overall computational cost scales linearly with the number of blocks, which can be processed in parallel, and
  exponentially with the block size ... For general designs, we approximate the Gram matrix by a block-diagonal using spectral
  clustering and propose an iterative algorithm that capitalizes on the block-diagonal algorithms to explore efficiently the model space."
- Sec. 4.1 (quoted): "the algorithm does a heuristic optimisation on a well-defined objective function over the model space ...
  if X^T X is really block-diagonal and Zellner's prior is used for the coefficient, Algorithm 3 returns the correct Bayesian best subsets."
  Also: "If X^T X is not block-diagonal M may not contain all best subsets anymore".
- Props 3.3, 3.4: best model of each size under Zellner prior, block-diagonal Gram. Exactness REQUIRES exact block-diagonality of X^T X.
- Relevance: closest precursor to OUR START (correlation-clustered blocks, exact per-block enumeration, parallel over blocks).
  Differences: they cluster by spectral clustering and use blocks as a search heuristic for general designs (no guarantee);
  we use the block product as an exactly-sampleable start pi_0 and bridge to the exact posterior by SMC (Z-hat unbiased).
  THREAT to any novelty claim about the start/blocks themselves; COMPLEMENTARY (we supply what they lack off block-diagonality).
  Under our designs (LH, S1-S6) X^T X is not block-diagonal (cross-block correlations exist, and the composite start uses full-y
  block scores, not a block-diagonal Gram), so their exactness theorem does not apply.

## Ma (2015), "Scalable Bayesian model averaging through local information propagation", JASA 110; arXiv:1403.2397v2
File read: Papers/Core_bibliography/13_2015_Ma_*.pdf.
- Method LIPS: probabilistic forward-stepwise (pFS) latent Markov process gamma(0),...,gamma(p) (Thm 1 Markov property; Thm 2 every
  model-space measure has a pFS representation; Thm 3 information propagation gives exact posterior pFS transitions, intractable in high-d).
  SMC with k-step look-ahead proposals; importance weights; Horvitz-Thompson estimator.
- Islands (quoted): "one can divide the N total number of particles into L 'islands' ... The L islands can be generated either on L CPU
  cores in an (embarrassingly) parallel fashion".  Discussion: "LIPS requires a large number of short chains to obtain reliable estimates,
  and thus is easily parallelizable."
- Guarantees: exactness of the representation (Thms 1-3); estimator consistency as N -> infinity is standard importance sampling.
  No rate, no correlation condition. Text near Fig. 7 (quoted): "with so few particles, the models that LIPS samples become very variable
  due to the high predictor correlation, and so the corresponding PIP estimates are unreliable."
- Sequential depth: the pFS process has up to p steps per particle (t = 0..p), so depth is O(p) (each step is parallel across particles).
- Relevance: a PRIOR EXAMPLE of an exact-target, embarrassingly parallel (islands) SMC for BMA, with correlation fragility reported by the
  author. Partial THREAT to "parallel + exact target is new"; our distinguishing points must be depth (T stages vs p steps) and guarantees.

## Zhou, Yang, Vats, Roberts, Rosenthal (2022) dimension-free mixing (arXiv:2105.05719): sequential informed MCMC; not parallel. (Already in our refs.)
## Le, Fay, Chopin, Vihola (2026) complexity of standard and waste-free SMC (local file 24): "SMC samplers are 'embarrassingly parallel'";
   assumes number of parallel chains M fixed (line ~428). Relevant to work/depth phrasing: complexity bounds are WORK bounds.
