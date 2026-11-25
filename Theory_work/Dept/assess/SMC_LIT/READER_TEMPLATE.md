# Reader notes template (one file per paper: /home/fb31/SMC_Theory_Department/SMC_LIT/notes/<KEY>.md)

## 0. Bibliographic
Title; authors; year; venue; DOI; arXiv id/version read; file(s) read (main, appendix, supplement) and their page counts.

## 1. Coverage log (proof that the WHOLE paper was read)
List every section, appendix and supplement section with its page range and one line on its content. If any part could not be obtained (e.g. a supplement), say so explicitly and say what you tried.

## 2. Model and prior
Likelihood (linear / GLM / other), model space (all subsets? size cap?), model prior, coefficient prior (g-prior? spike-and-slab? which), variance prior, marginal likelihood closed form or not.

## 3. Sampler design
Particles (what is a particle), initial distribution (prior? something data-driven?), the sequence of targets (tempering of likelihood? geometric bridge? data-sequential?), schedule (fixed / adaptive ESS / other), reweighting and resampling, MCMC move kernels (Gibbs, swaps, independence proposals, parametric proposal families such as logistic-conditional or Bernoulli products), parallel/independent runs or islands, outputs (how PIPs are estimated: raw particle frequencies, Rao–Blackwellised, renormalised over visited models; evidence estimates; a reported/best model; local search). Largest p and n in their experiments, and competitors.

## 4. What they prove
Every theorem/proposition/lemma: a faithful statement (LaTeX), its assumptions, the asymptotic regime (fixed p? p growing? n?), and its type: (i) Monte Carlo convergence/CLT/unbiasedness of the sampler for a fixed data set; (ii) complexity/mixing bounds; (iii) posterior consistency / selection consistency / rates (statistical); (iv) guarantees on the algorithm's output (e.g. the reported model equals the truth). If they prove nothing, say "no theory" and quote any informal claims.

## 5. Comparison with ours (read /home/fb31/SMC_Theory_Department/SMC_LIT/METHOD_SUMMARY.md)
Table, feature by feature: (a) SMC over models; (b) path/bridge; (c) adaptive vs frozen schedule; (d) move set; (e) independent islands; (f) PIP estimator (Rao–Blackwellised / list-renormalised); (g) evidence estimate and its unbiasedness; (h) block-structured start law; (i) reported model + local search certification. SAME / SIMILAR / DIFFERENT for each, with one line.
Then theory vs our Theorems 1–6 and planned P1–P5: which of ours does any of their results overlap, imply, or contradict? Be precise; "none" is an acceptable answer.

## 6. Verdict
Novelty risk to us: NONE / PARTIAL OVERLAP / DIRECT OVERLAP, with a 2–3 line justification. What we must cite, and the one-sentence differentiation we would write in the paper.

Rules: be faithful; quote page numbers for every claim; do not guess what you did not read. Read PDFs with the Read tool using the `pages` parameter (max 20 pages per call) until every page is covered. Never copy PDFs into any git repository. Write the notes file incrementally.
