# BENCH_METHODS: shared schema for workers

## Goal

The owner wants to know which comparison methods (competitors) recur in the variable-selection literature. Both camps count: Bayesian and frequentist. We need evidence of **how often** each method is run in **simulation comparisons**, and in **which papers**.

Our paper's setting is Gaussian linear regression with p up to 5000, with n in the hundreds to a thousand, and p ≫ n.

## Rules

1. **Evidence.** A method counts for a paper only if the paper **runs** it in its simulation study (or its real-data comparison). Methods that are only cited do not count. Use the paper's full text. Record the location (section, table or figure) where the method appears in the comparison.
2. **Role** of each method in each paper:
   - `proposed`: the paper's own new method or methods;
   - `competitor`: run for comparison;
   - `gold`: used only as a gold-standard or reference posterior;
   - `variant`: an ablation or variant of the proposed method.
3. **Method keys.** Use the canonical keys below. If a method has no key, invent one as `NEW:<SHORTNAME>` and describe it in the `raw_name` field.
4. **Files.**
   - Never copy PDFs into any git repository.
   - New PDFs you download go in `/home/fb31/SMC_Theory_Department/BENCH_METHODS_papers/`.
   - Do not edit files that other workers own.
5. **Paywalled papers.** If you cannot get the full text (journal paywalled and no arXiv, author or PMC copy), record the paper with `read_level=PAYWALLED` and give its DOI. Do not guess its competitors from the abstract.

## Canonical method keys

### Bayesian MCMC and search

| Key | Method |
|---|---|
| `MC3_ADS` | Add-delete-swap or MC3 Metropolis–Hastings on γ (Madigan–York, Brown et al., YWJ random-walk) |
| `GIBBS_GAMMA` | Componentwise Gibbs on γ (SSVS George–McCulloch 1993, Kuo–Mallick, Dellaportas) |
| `SSS` | Shotgun stochastic search (Hans et al. 2007) |
| `S5` | Simplified shotgun stochastic search with screening (Shin et al. 2018; BayesS5) |
| `BAS` | Bayesian adaptive sampling (Clyde et al. 2011; R package BAS) |
| `ESS` | Evolutionary stochastic search, ESS++ or GUESS (Bottolo–Richardson 2010) |
| `PIMASS` | piMASS (Guan–Stephens 2011) |
| `PT` | Parallel tempering or population MCMC, when not ESS |
| `HBS` | Hamming-ball sampler (Titsias–Yau 2017) |
| `TGS` | Tempered Gibbs sampler |
| `WTGS` | Weighted TGS (Zanella–Roberts 2019) |
| `ASI` | Adaptive MCMC of Griffin et al. 2021 (ASI, EIA, exploratory individual adaptation) |
| `PARNI` | PARNI (Liang et al. 2022) |
| `LIT_MH` | Locally informed or thresholded MH (Zhou et al. 2022) and other informed proposals |
| `SAM` | Split-and-merge (Song–Liang 2015) |
| `SKINNY` | Skinny Gibbs (Narisetty et al. 2019) |
| `BASAD` | BASAD, shrinking-and-diffusing priors (Narisetty–He 2014) |
| `SMC_SC` | Schäfer–Chopin SMC (2013) |
| `SMC_OTHER` | Other SMC or particle samplers for BVS (Shi–Dunson, Ma LIPS) |
| `RJMCMC` | Reversible jump |
| `NLP_MOMBF` | Nonlocal priors, MOM/iMOM (Johnson–Rossell 2012; R package mombf), excluding S5 |
| `BMS` | R package BMS (Zeugner–Feldkircher) |
| `SPIKESLAB_IR` | spikeslab package or rescaled spike-and-slab (Ishwaran–Rao 2005) |
| `BVS_GPRIOR_OTHER` | Other g-prior or hyper-g samplers (e.g. BVS R package, Liang et al. 2008 hyper-g used as competitor) |

### Bayesian optimisation, variational and shrinkage

| Key | Method |
|---|---|
| `EMVS` | EMVS (Ročková–George 2014) |
| `SSLASSO` | Spike-and-slab lasso (Ročková–George 2018; SSLASSO package) |
| `VARBVS` | Variational BVS (Carbonetto–Stephens 2012; varbvs) |
| `SUSIE` | Sum of single effects (Wang et al. 2020; susieR) |
| `MRASH` | mr.ash (Kim et al. 2024) |
| `VB_OTHER` | Other variational spike-slab methods (Ray–Szabó 2022 sparsevb, Huang et al., Ormerod et al.) |
| `HORSESHOE` | Horseshoe MCMC (Carvalho–Polson–Scott; horseshoe, bayesreg, bhs), including Johndrow's approximate MCMC |
| `GLOBAL_LOCAL_OTHER` | Other continuous shrinkage priors: Bayesian lasso, Dirichlet–Laplace, R2D2, horseshoe+, NEG |
| `BAYES_FINEMAP` | Genetics fine-mapping tools (FINEMAP, CAVIAR, CAVIARBF, DAP-G, PAINTOR) |
| `BAYES_GWAS` | Genome-wide BVS tools (BSLMM/GEMMA, BayesR, GCTB, BOLT, LDpred) |

### Frequentist

| Key | Method |
|---|---|
| `LASSO` | Lasso, typically glmnet, with CV or any tuning |
| `ADALASSO` | Adaptive lasso |
| `ENET` | Elastic net |
| `RELAXED_LASSO` | Relaxed lasso |
| `SCAD` | SCAD (ncvreg, ncpen) |
| `MCP` | MCP (ncvreg, plus) |
| `SIS` | SIS or ISIS (Fan–Lv 2008) |
| `HOLP` | HOLP (Wang–Leng 2016) |
| `FSTEP` | Forward stepwise, forward regression or OMP |
| `STEPWISE_IC` | Stepwise, backward or all-subsets selection with AIC, BIC or Cp; EBIC |
| `BEST_SUBSET_MIO` | Best subset via mixed-integer optimisation (Bertsimas et al.) |
| `L0LEARN` | L0Learn (Hazimeh–Mazumder) |
| `ABESS` | abess or splicing (Zhu et al.) |
| `STABSEL` | Stability selection (Meinshausen–Bühlmann 2010) |
| `KNOCKOFF` | Knockoffs: fixed-X or model-X |
| `SLOPE` | SLOPE |
| `DEBIASED` | Desparsified or debiased lasso (van de Geer et al., Zhang–Zhang, Javanmard–Montanari) |
| `MS_SPLIT` | Single or multi sample-splitting (Wasserman–Roeder, Meinshausen et al. 2009) |
| `SQRT_LASSO` | Square-root or scaled lasso |
| `DANTZIG` | Dantzig selector |
| `TLP_OTHER_NONCONVEX` | Other nonconvex penalties: TLP, SparseNet, bridge, L1/2 |
| `RIDGE` | Ridge regression |
| `MARGINAL` | Univariate marginal testing or screening |
| `RF_ML` | Random forests or other machine-learning selectors |

## Output formats

Use TSV with `;` inside fields, never tabs or newlines.

**Rows file** (`rows/<worker>_methods.tsv`), one row per (paper, method):

`paper_key	method_key	raw_name	role	location	note`

**Papers file** (`rows/<worker>_papers.tsv`), one row per paper:

`paper_key	authors	year	title	venue	doi	arxiv	read_level	has_sims	p_max	local_pdf	note`

- `read_level`: `full-text`, `PAYWALLED` or `partial`.
- `venue`: use short names (JASA, JRSSB, AoS, Biometrika, JMLR, JCGS, BA, Stat Comput, EJS, Stat Sci, Stat Sinica, Bioinformatics, AJHG, Nat Genet, PLoS Genet, arXiv).
