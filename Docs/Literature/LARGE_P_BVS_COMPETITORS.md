# Large-p fully Bayesian variable selection: competitor check (2026-11-19)

A Sonnet literature check, read from the primary PDFs. For the paper's related-work section and its claims. Not exhaustive: re-check before claiming "first" or "only".

## millipede / Subset wTGS (Jankowiak, AISTATS 2023; arXiv 2208.01180; github.com/BasisResearch/millipede)
- **Model:** spike-and-slab, a Normal slab, an Inverse-Gamma noise prior; linear (plus Polya-Gamma binomial / negative binomial). Output: importance-weighted samples, so PIPs. **No evidence (marginal likelihood) estimate.**
- **Scale:** the largest run is P about 7.5e5 (maize SNPs plus appended N(0,1) noise columns), n = 2267; 50k samples in about 35 min on one T4 GPU; cost per iteration O(subset size); GPU memory is the bottleneck.
- **Precision evidence:** empirical only. Semi-synthetic ground truth (20 causals) gives "high" sensitivity and precision at PIP > 0.5, read from a figure. The reference PIPs come from 10 long wTGS chains (self-referential). No exact or brute-force posterior comparison; no PIP error bound.
- **Theory:** Prop. 1 is almost-sure convergence as T -> infinity (reversibility plus irreducibility plus the LLN). No rate, no finite-run bound, no statistical consistency of the output.
- **Limits:** GPU memory; assumes |gamma| << P; adaptation can be poor in highly correlated designs (anti-correlated PIP errors for near-duplicate covariates); "no compelling need" for precise low PIPs.

## Zanella & Roberts (JRSS-B 2019; arXiv 1805.00541), TGS / wTGS
Mixing theory: the importance-weight variance is robust; TGS asymptotic variance <= b^2 x Gibbs; relaxation times in a stylised collinear/orthogonal g-prior design (m fixed, p -> infinity), partly conjectured. Nothing on statistical consistency.

## Others
- S^3 (Biswas, Mackey & Meng, ICML 2022; arXiv 2204.01668): exact spike-and-slab Gibbs with fast linear algebra, up to p about 1e5 (maize); convergence complexity "not addressed"; no exact-posterior check.
- SMC for BVS: Schafer & Chopin 2013 (p about 100s). No SMC BVS at p >= 1e5 with an accuracy claim was found.
- Out of scope, by the owner's ruling: genetics summary-statistic tools (problem-specific shortcuts) and variational BVS (a different philosophy).

## Our differentiating claim (defensible)
Not "faster" or "larger" (millipede reaches comparable p on a GPU). It is the pairing of:
(1) proved output-level consistency, in selection and in Hellinger distance;
(2) an empirical match to an exact version of the same sampler at p = 1e4, including the weak-signal regime;
(3) an evidence estimate;
(4) bit-reproducible, checkpointed CPU runs;
plus 1M in about 2 h wall on CPUs.
