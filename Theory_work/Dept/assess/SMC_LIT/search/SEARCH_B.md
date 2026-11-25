# SEARCH_B: adjacent samplers, theses and theory for SMC-over-models BVS

Run date: 2026-11-24. Worker B (adjacent ground, theses, theory). Worker A covers papers that say "SMC for variable selection" explicitly; those appear here only as cross-references (marked XREF) so scores are comparable.

Scoring (against METHOD_SUMMARY.md, SMC-BVS v3.1.1-listpip): 5 = SMC over models with tempering for BVS AND theory on selection/posterior consistency or on the algorithm's output; 4 = SMC/particle over models for BVS with some theory; 3 = SMC/particle over models for BVS, no theory; 2 = adjacent sampler sharing several features, or SMC theory on binary/discrete spaces (or theory comparator for BVS samplers); 1 = background.

Verification levels: DOI = checked against Crossref unless marked "(web)" (taken from a web result, not Crossref) or "none". "Read" = I extracted and read parts of the full text; "abstract" = abstract / metadata only (full text blocked or not opened). Statements about content that I did not read in full are flagged "unverified".

## HEADLINE FINDINGS

1. No paper found that proves selection or posterior consistency for the OUTPUT of an SMC (or population/particle) sampler on the BVS model space. Nothing found that proves a polynomial-time or finite-sample complexity bound for SMC on a spike-and-slab / BVS posterior. The nearest theory is (a) generic SMC complexity theory (Schweizer 2012; Paulin-Jasra-Thiery 2019; Marion-Mathews-Schmidler 2023; Mathews-Schmidler 2024; Lee-Santana-Gijzen 2024), which treats product measures, finite spaces, mean-field Ising/Potts and Glauber dynamics on {0,1}^d but never a BVS posterior, and (b) MCMC mixing theory for BVS (Yang-Wainwright-Jordan 2016; Zhou et al. 2022; Chang et al. 2022; Zhou-Smith 2022), which gives the comparators for the planned P1 trap theorem.
2. The closest operational matches to our design that are NOT labelled "SMC for variable selection": Evolutionary Stochastic Search (population of tempered chains; "block crossover" built from the correlation structure of the covariates, which parallels our correlation blocks), Papaspiliopoulos-Rossell block-diagonal "Coolblock" (exact product-of-block marginal likelihoods, the closest precedent for our start law pi_0), Shotgun Stochastic Search / FINEMAP / BAS (list-based renormalised PIPs, the precedent for pip_T), and Paulin-Jasra-Thiery "interpolation to independence" (SMC bridge that starts from an independent/product law; Potts model, polynomial cost).
3. Listed-model renormalised PIPs have a known bias issue: Garcia-Donato & Martinez-Beneito 2013 (empirical frequencies beat renormalised estimates in large model spaces) and Clyde & Ghosh 2012 (renormalised estimates biased; Horvitz-Thompson-type correction). Our pip_T (renormalised over the returned list T of 40p+1 models) should cite and address both. Local copies exist for both (see Section E).
4. Theses with SMC over model space: Schafer (Paris-Dauphine, 2012; binary vectors, annealed SMC), Zhou (Warwick, 2014; SMC model comparison), Vuong (SFU, 2024 MSc project; annealed SMC for linear and mixed models), Cozzini (Imperial, 2011/2012; particle MCMC with binary selection indicators, mixture models), A. Lee (Oxford, 2011; SMC for sparsity-inducing priors, continuous, not model space). None contains a consistency theorem about the sampler output.
5. Also noted: Duan (NUS working paper, 2018/2019) density-tempered SMC for L0 (zero-norm) variable selection, best 20 of 1000 regressors; full text not retrievable (403), so theory claims are unverified. Anchored RJSMC (van Assen & Hinne, arXiv Oct 2026) has a BVS experiment but with p = 4 only.

## SECTION A. Candidate table

Format per row: No. | Title | Authors | Year | Venue / arXiv | DOI | Open full-text URL | what it does | SCORE | same / differs | theory.

### A1. Population-based and tempered samplers over models

A1.1 Evolutionary Monte Carlo: Applications to Cp model sampling and change-point problem
- Liang F., Wong W.H.; 2000; Statistica Sinica 10(2):317-342; DOI none (Stat. Sinica has no DOIs for this volume).
- Open: https://www.stat.purdue.edu/~fmliang/papers/2000/Sinica00.pdf (not downloaded; page from web search only)
- What: population of parallel-tempered chains with mutation (Metropolis), crossover (partial state swap) and exchange (full swap) operators; illustrated on Cp-based model selection (binary inclusion vectors) and change points.
- SCORE 2. Same: population of binary model vectors, temperature ladder, swap-type global moves. Differs: population MCMC (equal-weight chains, no importance reweighting/resampling, no evidence estimate); no adaptive schedule by ESS; no start law other than prior.
- Theory: ergodicity of the product-space chain only; nothing about selection consistency. Is it effectively SMC? No: it is population MCMC (parallel tempering family).

A1.2 Automatic Bayesian model averaging for linear regression and applications in Bayesian curve fitting
- Liang F., Truong Y.K., Wong W.H.; 2001; Statistica Sinica 11(4):1005-1029; DOI none. (Identified from the Stat. Sinica index page returned by search; not opened. Unverified details.)
- What: Evolutionary Monte Carlo used to sample the posterior over linear-regression models for BMA.
- SCORE 2. Same/differs: as A1.1. Theory: none on output (unverified).

A1.3 Evolutionary Stochastic Search for Bayesian model exploration (ESS)
- Bottolo L., Richardson S.; 2010; Bayesian Analysis 5(3):583-618; arXiv:1002.2706; DOI 10.1214/10-BA523.
- Open: https://arxiv.org/pdf/1002.2706 ; copy at papers/BottoloRichardson2010_ESS.pdf (read).
- What: EMC on the variable-selection posterior (g-prior and independent-prior variants), population of tempered chains with Fast-Scan MH local moves, four crossover operators including a novel "block crossover" defined from the correlation structure of the covariates, delayed-rejection and all-exchange operators, temperature ladder tuned by monitoring exchange acceptance (target 0.5), adaptive Metropolis-within-Gibbs for the prior-scale parameter. Compared with Shotgun Stochastic Search.
- SCORE 2. Same: population over binary inclusion vectors; tempering; swap/exchange moves; correlation-block move (parallels our correlation-block clustering and correlation-neighbour swap); parallel-friendly. Differs: population MCMC without importance resampling, no evidence estimate, no frozen schedule, estimates are equal-weight averages of the cold chain; not SMC.
- Theory: ergodicity of EMC and diminishing adaptation (Roberts-Rosenthal) only. No consistency.

A1.4 ESS descendants (population of tempered chains on model space): ESS++ (Bottolo, Chadeau-Hyam, Hastie et al., Bioinformatics 27(4):587-588, 2011, DOI 10.1093/bioinformatics/btq684); Bayesian detection of eQTL hot spots (Bottolo, Petretto et al., Genetics 189:1449, 2011, DOI 10.1534/genetics.111.131425); GUESS-ing polygenic associations with multiple phenotypes using a GPU-based ESS algorithm (Bottolo, Chadeau-Hyam, Hastie et al., PLoS Genetics 9:e1003657, 2013, DOI 10.1371/journal.pgen.1003657); R2GUESS (Liquet, Bottolo, Campanella, Richardson, Chadeau-Hyam, J. Stat. Software 69(2), 2016, DOI 10.18637/jss.v069.i02); MT-HESS (Lewin et al., Bioinformatics 2015, 2015); BayesSUR (Zhao, Banterle, Bottolo et al., JSS 2021); Banterle, Bottolo, Richardson et al. SUR (JRSSA 2021); Alexopoulos & Bottolo, Bayesian variable selection for Gaussian copula regression models (JCGS, arXiv:1907.08245, 2019).
- All SCORE 1-2 (software/applications of A1.3; GUESS = 2 because it adds GPU-parallel population with adaptive exchange). Found via Semantic Scholar citations of arXiv:1002.2706. Theory: none about output.

A1.5 Parallel hierarchical sampling (PHS)
- Rigat F., Mira A.; arXiv:0812.1484 (2008, titled "...a practical multiple-chains sampler for Bayesian model selection"); published as "Parallel hierarchical sampling: A general-purpose interacting Markov chains Monte Carlo algorithm", Computational Statistics & Data Analysis 56(12), 2012; DOI 10.1016/j.csda.2011.11.020.
- Open: https://arxiv.org/pdf/0812.1484 ; copy papers/Rigat2008_parallel_hierarchical_sampling.pdf (read abstract, headings).
- What: several interacting chains; proves reversibility of the joint kernel, relates to parallel tempering; examples include covariate selection in linear regression.
- SCORE 2. Same: interacting population on model space. Differs: MCMC, no SMC weights; small examples. Theory: reversibility/convergence of the joint kernel (MCMC-type).

A1.6 Bayesian variable selection via particle stochastic search (PSS)
- Shi M., Dunson D.B.; 2011; Statistics & Probability Letters 81(2):283-291; DOI 10.1016/j.spl.2010.10.011.
- Open: PMC copy https://pmc.ncbi.nlm.nih.gov/articles/PMC3029030 (my fetch was blocked by a browser check, so only the abstract/search snippets were read; full text not read here; check Worker A's note).
- What: SMC over the model space for linear and probit regression as an alternative to SSVS; searches for high-posterior models; keywords marginal inclusion probabilities, model averaging.
- SCORE 3 (XREF; Worker A territory). Same: particles are inclusion vectors, SMC. Differs: tempering path/schedule, move set and p range unverified; as published p is modest. Theory: none beyond generic SMC (unverified).
- Citation chain: S2 returned only 11 citing papers (Lopes-Tsay, Lopes-Carvalho et al. particle learning, Schreck-Fort-Le Corff 2013 MALA for BVS, Castillo et al. 2015, Ma 2015, Rockova 2018, Maity-Basu 2023, Larson et al.); none is an SMC-BVS paper not already listed.

A1.7 Particle EM for variable selection
- Rockova V.; 2018; JASA 113(524):1684-1697; DOI 10.1080/01621459.2017.1360778 (web).
- Open: paywalled (T&F); no arXiv version found.
- What: ensemble of repulsive "particles" (EM runs of the spike-and-slab-lasso family) that finds many posterior modes; output is a deterministic reconstruction of the posterior over modes; a stochastic SMC version is proposed; asymptotic argument that the number of particles needed is small under sparsity (p > n).
- SCORE 2. Same: population of particles with importance-type weights over modes; sparse regime p > n; mode-weighted posterior summary (analogue of list-renormalised summaries). Differs: particles are continuous parameter modes (EM), not models sampled via tempering; only a side-version is SMC.
- Theory: asymptotic considerations on number of particles (abstract; details unverified). Is it effectively SMC? Only the stochastic variant.

A1.8 Shotgun stochastic search for "large p" regression (SSS)
- Hans C., Dobra A., West M.; 2007; JASA 102(478):507-516; DOI 10.1198/016214507000000121.
- Open: https://sites.stat.washington.edu/people/adobra/Files/Papers/hansdobrawest2007.pdf (author copy, not downloaded).
- What: evaluates the whole neighbourhood (add/delete/swap) of the current model, samples the next model from it, keeps a list of top models, parallelisable; posterior summaries renormalised over the list.
- SCORE 2. Same: list of top models with renormalised PIPs (precedent for our pip_T and T), neighbourhood evaluation (our hill-climb / local search), parallel. Differs: single path (or few), no tempering/population weights, no evidence estimate.
- Theory: none about consistency or output (heuristic search).

A1.9 Bayesian adaptive sampling for variable selection and model averaging (BAS)
- Clyde M.A., Ghosh J., Littman M.L.; 2011; JCGS 20(1):80-101; DOI 10.1198/jcgs.2010.09049 (web).
- Local copy: Bayesian-Variable-Selection/Papers/Core_bibliography/27_2011_Clyde_Ghosh_Littman_...pdf
- What: samples models without replacement, adaptively learning marginal inclusion probabilities; estimators based on visited models (renormalised) with sampling-without-replacement corrections.
- SCORE 2. Same: model list with renormalised estimators, adaptive inclusion-probability proposal (cf. our independence move). Differs: sequential list-building, not tempered population. Theory: estimator properties in sampling terms, no selection consistency.

A1.10 Finite population estimators in stochastic search variable selection
- Clyde M., Ghosh J.; 2012; Biometrika 99(4):981-988; DOI 10.1093/biomet/ass040 (web).
- Open: paywalled; Duke repository record https://dukespace.lib.duke.edu/items/326fd88a-cf51-4d06-8182-4b899e3d165d
- What: shows that renormalising posterior probabilities over sampled models is biased and that bias can dominate MSE; proposes a ratio of Horvitz-Thompson estimators, approximately unbiased, using observed marginal likelihoods.
- SCORE 2 (directly about list-renormalised PIPs). Same: renormalised-over-visited-models summaries. Differs: sampling-frame correction for MCMC output. Theory: approximate unbiasedness of the estimator.

A1.11 On sampling strategies in Bayesian variable selection problems with large model spaces
- Garcia-Donato G., Martinez-Beneito M.A.; 2013; JASA 108(501):340-352; arXiv:1101.4368 (earlier title "Inferences in Bayesian variable selection problems with large model spaces"); DOI 10.1080/01621459.2012.742443.
- Local copy: Core_bibliography/28_2013_Garcia_Donato_...pdf ; arXiv https://arxiv.org/pdf/1101.4368
- What: compares empirical-frequency estimates from MCMC with renormalised estimates over visited models and with stochastic-search strategies; finds empirical frequencies better in the examples.
- SCORE 2. Same: renormalised vs empirical PIP question exactly as in our list-based outputs. Differs: no SMC. Theory: sampling-theory arguments, no consistency.

A1.12 Bayesian block-diagonal variable selection and model averaging (Coolblock)
- Papaspiliopoulos O., Rossell D.; 2017; Biometrika 104(2):343-359; arXiv:1606.03749; DOI 10.1093/biomet/asx019 (web).
- Local copy: Core_bibliography/12_2017_Papaspiliopoulos_Rossell_...pdf ; arXiv https://arxiv.org/pdf/1606.03749
- What: exact variable selection and BMA when the Gram matrix is block diagonal (posterior model probabilities as one-dimensional integrals, cost linear in number of blocks, exponential in block size); for general designs approximates the Gram matrix by blocks (spectral clustering) and iterates to explore the model space; R package mombf.
- SCORE 2 (closest precedent for the block-product start law pi_0). Same: partition into small blocks via clustering of correlations; exact per-block model tables; product-of-blocks structure; parallel over blocks. Differs: used as an exact/heuristic solver, not as the start law of a tempered SMC; no sampling-based correction of the block approximation; our discrepancy Delta(S) path corrects it.
- Theory: exactness under block-orthogonal design; no consistency of output (unverified).

A1.13 A split-and-merge Bayesian variable selection approach for ultrahigh dimensional regression
- Song Q., Liang F.; 2015; JRSSB 77(5):947-972; DOI 10.1111/rssb.12095.
- Local copy: Core_bibliography/32_2015_Song_Liang_...pdf
- What: split the p predictors into subsets, select within each, merge selected variables and select again; embarrassingly parallel; consistency shown under mild conditions.
- SCORE 2. Same: divide-and-conquer/island structure for very large p (cf. our 16 non-communicating islands and the 10^6-p engine, but ours split particles not predictors). Differs: splits the variable set, MCMC/BSR inside. Theory: YES, selection consistency of the aggregated procedure (a guarantee on the algorithm's output, but for the two-stage split-merge scheme, not SMC).

A1.14 Bayesian subset modeling for high-dimensional generalized linear models
- Liang F., Song Q., Yu K.; 2013; JASA 108(502):589-606; DOI 10.1080/01621459.2012.761942.
- Abstract only. What: prior whose MAP model approximates the minimum extended-BIC model; posterior consistency; screening by marginal inclusion probabilities; computation by stochastic-approximation-type MCMC (keyword evidence only; unverified).
- SCORE 2. Theory: posterior consistency plus screening consistency; sampler output theory unverified.

A1.15 Scalable importance tempering and Bayesian variable selection (Tempered Gibbs sampler)
- Zanella G., Roberts G.O.; 2019; JRSSB 81(3):489-517; arXiv:1805.00541; DOI 10.1111/rssb.12316. (Related: Zanella, Informed proposals for local MCMC in discrete spaces, JASA 115, 2020, DOI 10.1080/01621459.2019.1585255, local copy 09.)
- Local copy: Core_bibliography/14_2019_Zanella_Roberts_...pdf
- What: tempers only the coordinate being updated and corrects by importance weights; avoids a temperature ladder; efficient for spike-and-slab with tens of thousands of regressors.
- SCORE 2. Same: weighted (importance) estimators on binary model space, Rao-Blackwell-like conditional probabilities. Differs: single chain, no population/evidence. Theory: efficiency / scaling analysis and ergodicity; no consistency. Planned P1 comparator.

A1.16 Rapid convergence of informed importance tempering (IIT); Importance is important
- Zhou Q., Smith A.; AISTATS 2022 (PMLR 151:10939-10965); arXiv:2107.10827; DOI none. Follow-up: Li G., Smith A., Zhou Q., "Importance is important", arXiv:2304.06251, Statistics and Computing 2026, DOI 10.1007/s11222-026-11018-0.
- Open: https://arxiv.org/pdf/2107.10827 ; copy papers/ZhouSmith2022_informed_importance_tempering.pdf (not read).
- What: spectral-gap theory for informed importance-tempering chains on discrete spaces (incl. the Zanella-Roberts scheme).
- SCORE 2 (theory comparator for P1). Theory: spectral gap / rapid convergence bounds for weighted-tempering chains.

A1.17 Adaptive MCMC for model space: Lamnisos, Griffin, Steel (JCGS 22(3):729-748, 2013, DOI 10.1080/10618600.2012.694756); Griffin, Latuszynski, Steel, "In search of lost (mixing) time" (Biometrika 108(1), 2021 [Crossref lists 2020], arXiv:1708.05678, DOI 10.1093/biomet/asaa055; "Individual adaptation", arXiv:1412.6760)
- Open: arXiv. The ASI papers explicitly say their kernels are "well suited for parallel tempering or sequential Monte Carlo implementations" and give ergodicity proofs for the adaptive chain.
- SCORE 1-2. Not SMC; these are the adaptive-MCMC kernels whose use inside SMC the authors recommend (relevant to our Gibbs/swap move set). Theory: ergodicity of adaptive MCMC, O(1) idealised mixing.

A1.18 The Hamming ball sampler
- Titsias M.K., Yau C.; JASA 112(520):1598-1611, 2017; arXiv:1504.08133; DOI 10.1080/01621459.2016.1222288. Local copy Core_bibliography/11_2017_Titsias_Yau_...pdf.
- Auxiliary-variable block move; BVS example. SCORE 1. Theory: none about selection.

A1.19 Paired-move multiple-try stochastic search for Bayesian variable selection
- Chen X., Qamar S., Tokdar S.T.; arXiv:1611.09790 (2016); DOI none. (Duke MS thesis of X. Chen 2017 covers the same method.)
- SCORE 1. MTM generalised to discrete model space; shotgun-like. Theory: none about selection.

A1.20 Rapidly mixing multiple-try Metropolis algorithms for model selection problems
- Chang H., Lee C.J., Luo Z.T., Sang H., Zhou Q.; NeurIPS 2022; arXiv:2207.00689; DOI none.
- SCORE 2 (theory comparator). Theory: spectral gap/mixing bounds for MTM on model space, including variable selection.

A1.21 Mode jumping MCMC for Bayesian variable selection in GLMM (and genetically modified MJMCMC)
- Hubin A., Storvik G.; Computational Statistics & Data Analysis 127:281-297, 2018; arXiv:1604.06398; DOI 10.1016/j.csda.2018.05.020. Follow-up: Hubin, Frommlet, Storvik, arXiv:2110.05316.
- SCORE 1-2: large jumps plus local optimisation, genetic-algorithm population in the later version; cites Bottolo et al. Theory: reversible version proves validity of the chain; no selection consistency.

A1.22 Equi-energy sampler
- Kou S.C., Zhou Q., Wong W.H.; Annals of Statistics 34(4):1581-1619, 2006; DOI 10.1214/009053606000000515.
- SCORE 1. Population of chains with energy rings; no BVS use found apart from a group-selection application (arXiv:1901.02945, "Algorithmic Bayesian Group Gibbs Selection"; unverified). Theory: ergodicity.

A1.23 Highest posterior model computation and variable selection via simulated annealing
- Maity A.K., Basu S.; NEJSDS 1(2):200-207, 2023; DOI 10.51387/23-NEJSDS40.
- Open: https://nejsds.nestat.org/journal/NEJSDS/article/45 (open access); R package sahpm.
- What: simulated annealing over the model space to find the highest-posterior model.
- SCORE 2. Same: annealing over the model space (our "reported model" is also the best-scoring model found). Differs: single-chain optimisation, no PIPs/evidence. Theory: none claimed (unverified).

A1.24 Model-based screening embedded Bayesian variable selection for ultra-high dimensional settings (SVEN)
- Li D., Dutta S., Roy V.; arXiv:2006.07561 (2020); published JCGS 31(4), 2022, DOI 10.1080/10618600.2022.2074428.
- Open: https://arxiv.org/pdf/2006.07561
- What: closed-form spike-and-slab model posterior, screening plus fast Cholesky updates to explore large model spaces; a TEMPERATURE SCHEDULE guided by the model-selection-consistency derivation to reduce multimodality; applied to a GWAS with >0.5 million markers.
- SCORE 2. Same: tempered path on the model-space posterior guided by consistency asymptotics; p up to 10^5-10^6. Differs: stochastic search / single or few chains, no SMC. Theory: strong model selection consistency of the POSTERIOR (p near-exponential in n). Not a statement about the algorithm's output.

A1.25 FINEMAP (shotgun stochastic search for fine-mapping)
- Benner C., Spencer C.C.A., Havulinna A.S., Salomaa V., Ripatti S., Pirinen M.; Bioinformatics 32(10):1493-1501, 2016; DOI 10.1093/bioinformatics/btw018 (web).
- Open: https://pmc.ncbi.nlm.nih.gov/articles/PMC4866522
- What: SSS over causal configurations from summary statistics; PIPs and model posteriors renormalised over explored configurations.
- SCORE 2 for the list-renormalised summary idea. Theory: none.

A1.26 Skinny Gibbs: a consistent and scalable Gibbs sampler for model selection (Narisetty N.N., Shen J., He X.; JASA 114(527), 2019 [Crossref year 2018 online], DOI 10.1080/01621459.2018.1482754): an approximating Gibbs sampler for BVS with strong selection consistency proved for the approximate posterior, p near-exponential in n. SCORE 2 (theory comparator: consistency for a computational surrogate, not for an SMC output). Not opened; abstract-level knowledge only. Also background: Johnson-Rossell 2012 (DOI 10.1080/01621459.2012.682536, local copy 17), Castillo, Schmidt-Hieber, van der Vaart, Ann. Statist. 43(5), 2015, DOI 10.1214/15-AOS1334 (local: Priors_and_decision_rules/Castillo_SchmidtHieber_vanderVaart2015_...pdf), SCORE 1.

### A2. SMC / particle methods on binary or model spaces found outside the "SMC for variable selection" keyword (adjacent)

A2.1 Sequential Monte Carlo on large binary sampling spaces (XREF Worker A)
- Schafer C., Chopin N.; Statistics and Computing 23:163-184, 2013; arXiv:1101.6037; DOI 10.1007/s11222-011-9299-z (Crossref lists year 2011, online-first). Local copy Core_bibliography/07_...pdf.
- SCORE 3 (XREF). Adaptive tempered SMC with parametric binary families as MCMC-free proposals; BVS (linear regression) is the motivating example. Theory: none on selection; Beskos-Jasra-Kantas-Thiery 2016 explicitly covers its adaptive scheme (see C.7).
- Citation chain (S2, 106 citing items): found Schafer thesis, Schafer TOMACS, Cozzini items, Duan 2019, Youssfi-Chopin, Zhou-Johansen-Aston, Ma 2015, Titsias-Yau, Griffin et al., Maity-Basu (via Shi-Dunson list), Afshar-Francis-Cripps OPAD, Syed et al.-type optimised annealing; none else is an SMC-over-models method.

A2.2 Particle algorithms for optimization on binary spaces
- Schafer C.; ACM Trans. Modeling and Computer Simulation 23(1), Art. 8, 2013; arXiv:1111.0574; DOI 10.1145/2414416.2414424.
- Open: https://arxiv.org/pdf/1111.0574 ; copy papers/Schafer2013_particle_optimization_binary.pdf (abstract read).
- What: unified particle framework (cross-entropy method and simulated annealing as special cases) for pseudo-Boolean optimisation with parametric binary families.
- SCORE 2 (cross-entropy on binary spaces; our "reported model" is an optimisation output). Theory: none (empirical). Also Schafer, "On parametric families for sampling binary data with specified mean and correlation", arXiv:1111.0576 (and arXiv:1008.0055), SCORE 1.

A2.3 Monte Carlo methods for sampling high-dimensional binary vectors (thesis; see Section B).

A2.4 Zhou, Johansen, Aston: Toward automatic model comparison: an adaptive SMC approach
- JCGS 25(3):701-726, 2016; arXiv:1303.3123; DOI 10.1080/10618600.2015.1060885. Local copy Core_bibliography/25_...pdf ; also papers/ZhouJohansenAston2016_adaptiveSMC_model_comparison.pdf (read: variable selection appears only as a pointer to Schafer-Chopin).
- What: adaptive SMC samplers (adaptive tempering and kernels) for posteriors over collections of models plus their parameters, with path-sampling evidence estimators; examples Gaussian mixtures and PET.
- SCORE 2. Same: adaptive ESS-based schedule, evidence estimate, MC moves. Differs: not BVS, models are mixture orders. Theory: SMC-level asymptotics for the estimators (not checked in detail).

A2.5 Scalable Bayesian model averaging through local information propagation (LIPS) (XREF Worker A, says "SMC")
- Ma L.; JASA 110(510):795-809, 2015; arXiv:1403.2397; DOI 10.1080/01621459.2014.980908. Local copy Core_bibliography/13_...pdf.
- What: sequential-Monte-Carlo-type importance sampling of models using a forward-stepwise Markov proposal built from local information propagation; dimensions 15 to 1000.
- SCORE 3. Same: particles are models, importance weights, BMA/PIP output. Differs: sequential construction of the model (not a tempered path), no MCMC moves. Theory: unbiasedness of the importance estimator only (unverified).

A2.6 Scalable Bayesian bi-level variable selection in generalized linear models (XREF)
- Youssfi Y., Chopin N.; Foundations of Data Science 2025, DOI 10.3934/fods.2024010; arXiv:2303.12462. Copy papers/Youssfi_Chopin_2023_arXiv2303.12462.pdf (Worker A's download).
- Tempered waste-free SMC over (group, within-group) inclusion; compared with the Laplace-approximation method of Rossell et al. SCORE 3. Theory: inherits Dau-Chopin waste-free results only.

A2.7 Optimized (Optimised) annealed SMC samplers
- Syed S., Bouchard-Cote A., Chern K., Doucet A.; arXiv:2408.12057; JRSSB 2026, DOI 10.1093/jrsssb/qkag082. Local copy Core_bibliography/02_2026_Syed_...pdf.
- What: schedule/adaptation for annealed SMC (OASMC, OAIS); 12 benchmark models including spike-and-slab variable selection.
- SCORE 2. Same: annealed SMC with adaptive schedule on a spike-and-slab selection target. Differs: generic methodology. Theory: schedule-optimality results, nothing about selection.

A2.8 Anchored Reversible Jump Sequential Monte Carlo
- van Assen J., Hinne M.; arXiv:2610.09930 (7 Oct 2026); DOI none.
- Open: https://arxiv.org/pdf/2610.09930 ; copy papers/AssenHinne2026_anchored_RJSMC.pdf (read).
- What: RJMCMC embedded in SMC with adaptive tempering and kernel-density "anchored" between-model proposals; experiments include BVS in linear regression with g-prior and uniform model prior, but only p = 4 covariates (16 models, exact posterior known); 20,000 particles; ESS/s about 2.7x a birth-death RJMCMC.
- SCORE 3 (SMC over models with adaptive tempering for BVS, but toy size). Differs: models carry their coefficients (trans-dimensional), no large p. Theory: none (math.ST tag but only methodology and experiments in the text I read).

A2.9 Variable selection with big data based on zero norm and via sequential Monte Carlo
- Duan J.-C.; NUS working paper, version 22 Apr 2019 (first version 23 Oct 2018); SSRN. DOI not located.
- URL https://d.nuscri.org/profiles/duanjc/index_files/files/VariableSelection-SMC_April-22-2019.pdf (HTTP 403 for my client; abstract known from search snippets only).
- What: zero-norm (best-subset) regressor selection treated as combinatorial optimisation and solved with density-tempered SMC; target example best 20 of 1000 variables; claimed immune to multicollinearity unlike L_p penalties. A later paper says "see Duan (2019) for theoretical properties".
- SCORE 3 (could be 4 if the theory is on selection or output; UNVERIFIED). Same: density-tempered SMC over inclusion vectors for p = 1000. Differs: L0 objective, not a Bayesian posterior; no PIPs/evidence. Theory: claimed, unverified. ACTION: obtain via author page or SSRN in a browser.

A2.10 A Bayesian mixture of lasso regressions with t-errors
- Cozzini A., Jasra A., Montana G.; CSDA 2014; arXiv:1205.4955 (2012); DOI 10.1016/j.csda.2014.03.018.
- Particle MCMC (SMC inside MCMC) for mixture of lasso regressions; binary variable-selection indicators in the related thesis. SCORE 2. Theory: none about selection.

A2.11 Reversible-jump SMC and transdimensional SMC: Davies L., Ley-Cooper A.Y., Sutton M., Drovandi C., "Bayesian detectability of induced polarisation in airborne electromagnetic data using reversible jump sequential Monte Carlo", arXiv:2109.00661 (2021); Davies, Salomone, Sutton, Drovandi, "Transport reversible jump proposals", arXiv:2210.12572; Andrieu C., de Freitas N., Doucet A., "Sequential MCMC for Bayesian model selection", IEEE Signal Processing Workshop on Higher-Order Statistics 1999, DOI 10.1109/HOST.1999.778709 (https://www.stats.ox.ac.uk/~doucet/andrieudefreitasdoucet_sequentialMCMCforbayesianmodelselection1999.pdf).
- SCORE 1-2 (SMC/particles across model space, not BVS-scale; the 1999 paper is the earliest SMC-for-model-selection precedent I found). Theory: none for selection.

A2.12 SMC samplers with independent MCMC proposals
- South L.F., Pettitt A.N., Drovandi C.C.; Bayesian Analysis 14(3), 2019; DOI 10.1214/18-BA1129. SCORE 1. Independence-kernel moves inside SMC (our independence move from pi_0); not BVS. Theory: none on selection.

A2.13 SMC for graph/structure spaces (adjacent, binary adjacency spaces): Bayesian learning of weakly structural Markov graph laws using SMC (Olsson, Pavlenko, Rios; EJS 13(2), 2019, DOI 10.1214/19-EJS1585) SCORE 1; Tan, Jasra, De Iorio et al., Bayesian inference for multiple Gaussian graphical models, arXiv:1603.06358, SCORE 1 (found via S2 citations of Schafer-Chopin).

A2.14 Population annealing (physics SMC on binary spin spaces)
- Machta J., "Population annealing with weighted averages", Phys. Rev. E 82, 2010, arXiv:1006.0252; Wang W., Machta J., Katzgraber H.G., "Comparing Monte Carlo methods for finding ground states of Ising spin glasses: population annealing, simulated annealing, and parallel tempering", Phys. Rev. E 92:013303, 2015, arXiv:1412.2104; DOI 10.1103/PhysRevE.92.013303 (Machta 2010: DOI 10.1103/PhysRevE.82.026704).
- SCORE 1. Same algorithmic family (resample + MCMC sweep while cooling) on {-1,1}^d. Not BVS. Cited by Mathews-Schmidler 2024.

A2.15 Background SMC machinery (not scored for BVS): Del Moral-Doucet-Jasra 2006 (local Papers/SMC/); Dau & Chopin 2022 (local 23); Le Fay, Chopin, Vihola 2026 "On the complexity of standard and waste-free SMC samplers" (local 24; not examined by me but it is SMC complexity theory and should be read for P1); Du & Guyader 2021 variance estimation adaptive SMC (local, Priors_and_decision_rules); Lee & Whiteley 2018 (local 26). SCORE 1-2.

### A3. Comparator / competitor theory for BVS posteriors (non-SMC)

A3.1 On the computational complexity of high-dimensional Bayesian variable selection
- Yang Y., Wainwright M.J., Jordan M.I.; Annals of Statistics 44(6):2497-2532, 2016; arXiv:1505.07925; DOI 10.1214/15-AOS1417.
- Open: https://arxiv.org/pdf/1505.07925 ; copy papers/YangWainwrightJordan2016_complexity_BVS.pdf (abstract read).
- What: truncated sparsity prior; variable-selection consistency AND rapid mixing (mixing time linear in p up to log) of an add/delete/swap Metropolis-Hastings chain; shows posterior concentration alone does not imply rapid mixing.
- SCORE 2 (key theory comparator; same truncation to size <= K as ours). Differs: single-flip MCMC, mixing-time theory, not SMC; conditions on design (restricted eigenvalues, beta-min).

A3.2 Dimension-free mixing for high-dimensional Bayesian variable selection
- Zhou Q., Yang J., Vats D., Roberts G.O., Rosenthal J.S.; JRSSB 84(5):1751-1784, 2022; arXiv:2105.05719; DOI 10.1111/rssb.12546. Local copy Core_bibliography/10_...pdf.
- LIT-MH informed sampler; mixing time independent of p under Yang et al. assumptions. SCORE 2 (comparator). Theory: yes (two-stage drift).

A3.3 Provably efficient posterior sampling for sparse linear regression via measure decomposition
- Montanari A., Wu Y.; arXiv:2406.19550 (2024); DOI none.
- Open: https://arxiv.org/pdf/2406.19550 ; copy papers/MontanariWu2024_sparse_regression_sampling.pdf (abstract read).
- What: decomposes the multimodal posterior (product prior, random design) into a log-concave mixture of product measures; polynomial-time sampler once n/d exceeds a constant.
- SCORE 2 (a polynomial-time posterior-sampling result for sparse regression; not SMC, not model-space BVS, random design with a constant n/d regime; different regime from p >> n). Relevant to our planned complexity claim.

A3.4 From estimation to sampling for Bayesian linear regression with spike-and-slab prior
- Jiang Q.; arXiv:2307.05558 (2023). SCORE 1-2. Gibbs sampling and stochastic localisation under posterior-contraction assumptions; guarantees stated at abstract level only. Copy papers/Jiang2023_spike_slab_sampling.pdf (not read).

A3.5 Regularization and computation with high-dimensional spike-and-slab posterior distributions (v1-v2), later "An approach to large-scale quasi-Bayesian inference with spike-and-slab priors" (v3)
- Atchade Y.F., Bhattacharyya A.; arXiv:1803.10282. SCORE 1. Forward-backward envelope of the spike-and-slab posterior; simulations suggest poor mixing with coherent designs.

## SECTION B. Theses (PhD / MSc)

B1. Monte Carlo methods for sampling high-dimensional binary vectors
- Schafer C., PhD, Universite Paris-Dauphine, 2012 (supervisor N. Chopin; CREST/ENSAE). HAL/Dauphine handle http://basepub.dauphine.fr (123456789/10860); IDEAS https://ideas.repec.org/b/dau/thesis/123456789-10860.html ; theses.fr id 2012PA090039.
- Annealed SMC for binary vectors (BVS is the application), parametric families for binary data, particle optimisation. SCORE 3. Theory: none on selection (not read; from catalogue summaries). XREF Worker A.

B2. Bayesian model comparison via sequential Monte Carlo
- Zhou Y., PhD, University of Warwick, 2014 (supervisors J. Aston, A. Johansen). https://wrap.warwick.ac.uk/62064 (open).
- Underlies Zhou-Johansen-Aston 2016. SCORE 2. Theory: SMC asymptotics for model-comparison estimators; BVS example not confirmed.

B3. The performance of annealed sequential Monte Carlo sampling as a joint variable selection and parameter estimation method in the linear (mixed) model setting
- Vuong Q., MSc project, Simon Fraser University, Spring 2024 (supervisor R. Altman). https://summit.sfu.ca/item/38207 ; copy papers/Vuong_2024_SFU_thesis_annealedSMC_VS.pdf (Worker A's download; I read the abstract, outline).
- Annealed SMC (adaptive tempering after Zhou et al.) with particles = (model, coefficients); simulation study of how n, SNR, signal proportion, correlation and random effects affect selection/estimation; small p; no theory. SCORE 3.

B4. Supervised and unsupervised model-based clustering with variable selection
- Cozzini A.M., PhD, Imperial College London, Oct 2011 (supervisors G. Montana, A. Jasra). https://spiral.imperial.ac.uk/entities/publication/2dba5148-12eb-40b1-b840-5f9556d839c8
- Latent binary indicators for variable selection; particle MCMC (SMC + conditional SMC); variable ranking by selection probability via resampling. SCORE 2 (mixture-model selection, not regression BVS). Theory: none on selection.

B5. On auxiliary variables and many-core architectures in computational statistics
- Lee A., DPhil, University of Oxford, 2011. https://ora.ox.ac.uk/objects/uuid:244040a7-f094-4d57-a78f-e154ed3b353c (PDF read at outline level: Chapter 3 "Hierarchical priors for variable selection" with an SMC "sparsity path" analysis).
- SMC over a continuous hierarchical sparsity prior (lasso-type), not over inclusion vectors. SCORE 1-2. Theory: none located.

B6. Contributions to Computational Bayesian Statistics (South L.F., PhD, QUT, 2019, supervisor C. Drovandi) and Contributions to Bayesian transdimensional algorithms (Davies L., PhD, QUT; https://eprints.qut.edu.au/244544)
- South's thesis covers SMC improvements, nested sampling via SMC, synthetic likelihood; no variable selection found. Davies: transdimensional SMC; whether a regression BVS example exists is unverified. SCORE 1.

B7. Other theses surfaced (BVS, not SMC): Nikooienejad A., Bayesian variable selection in high-dimensional genomic data (Texas A&M 2017, nonlocal priors); Xu C., Ultra-high dimensional Bayesian variable selection with lasso-type priors (SMU 2021); Chen X., Multiple-try stochastic search for Bayesian variable selection (Duke MSc 2017); Qamar S., Topics in modern Bayesian computation (Duke 2015); Hubin A. (Oslo 2018, MJMCMC). SCORE 1.

Searches for a ProQuest/HAL thesis specifically on "SMC for variable selection" returned nothing beyond B1-B4. Not found: any thesis by Youssfi or Dau (ENSAE) in the repositories searched (search-engine only; ProQuest was not directly queried).

## SECTION C. Theory on SMC (and tempering) relevant to our theorems

C.1 Non-asymptotic error bounds for sequential MCMC and stability of Feynman-Kac propagators
- Schweizer N.; arXiv:1204.2382 (2012); DOI none. Copy papers/Schweizer2012_nonasymptotic_SMC_Feynman-Kac.pdf.
- Error bounds for SMC with MCMC moves from stability of the Feynman-Kac propagator derived from mixing of the kernels. SCORE 2. Theory: yes (generic, global mixing). Not BVS.

C.2 Non-asymptotic error bounds for sequential MCMC methods in multimodal settings
- Schweizer N.; arXiv:1205.6733 (2012). Copy papers/Schweizer2012_SMC_multimodal.pdf (read the tempering/discrete mentions: bounds depend on relative-density bound, local mixing constants and mass moving between disconnected components; discusses mean-field Ising/Potts tempering). SCORE 2. Theory: yes; tempering keyword; discrete examples referenced only.

C.3 Error bounds for sequential Monte Carlo samplers for multimodal distributions
- Paulin D., Jasra A., Thiery A.; Bernoulli 25(1):310-340, 2019; arXiv:1509.08775; DOI 10.3150/17-BEJ988. Copy papers/PaulinJasraThiery2019_SMC_multimodal_error_bounds.pdf (read).
- Asymptotic-variance bounds for SMC with MCMC moves between modes; "interpolation to independence" sequence of intermediate laws (miniature copies of the system, starting from an independent/product-like law); Potts model sampled at polynomial cost while parallel tempering with standard bridges is exponential.
- SCORE 2 (SMC theory on a discrete space AND a non-geometric-from-prior path; closest conceptual precedent for our start law pi_0 and discrepancy path). Differs: Potts model, not a BVS posterior; no data-dependent start law.

C.4 Finite-sample complexity of sequential Monte Carlo estimators
- Marion J., Mathews J., Schmidler S.C.; Annals of Statistics 51(3):1357-1375, 2023; arXiv:1803.09365 (v3 Aug 2022, after a proof correction; v2 withdrawn); DOI 10.1214/23-AOS2295. Copy papers/MarionMathewsSchmidler2023_finite_sample_SMC.pdf (read abstract, section list).
- Finite-sample bounds for SMC on static spaces given the chain of target distributions and kernel mixing; examples: finite spaces, product measures (dimension scaling), log-concave targets including Bayesian logistic regression.
- SCORE 2. Same: product-measure analysis; finite spaces (our model space); complexity within a log factor of MCMC. Differs: requires global mixing of kernels at each stage (not local) in this version; no BVS.

C.5 Finite sample complexity of sequential Monte Carlo estimators on multimodal target distributions
- Mathews J., Schmidler S.C.; Annals of Applied Probability 34(1):1199-1223, 2024; arXiv:2208.06672; DOI 10.1214/23-AAP1989. Copy papers/MathewsSchmidler2024_SMC_multimodal_complexity.pdf (read: Section 5.3 mean-field Ising model on {-1,1}^d with power tempering; Section 6 compares with PT/ST, torpid mixing of PT for mean-field Potts).
- Bounds need only LOCAL mixing; SMC is a FPRAS for some multimodal problems where MCMC or PT is exponentially slow (mixtures of log-concave, mean-field Ising).
- SCORE 2 (SMC theory on a BINARY space). Same: power-tempered SMC with local-mixing kernels on a hypercube; the logical template for a complexity theorem about SMC on BVS. Differs: the target is the mean-field Ising model, not a regression posterior; no model-prior/likelihood structure; no selection consistency. No variable selection application mentioned (I searched the text).

C.6 Convergence bounds for sequential Monte Carlo on multimodal distributions using soft decomposition
- Lee H., Santana-Gijzen M.; arXiv:2405.19553 (v1 May 2024, v2 Mar 2026); DOI none. Copy papers/LeeSantanaGijzen2024_SMC_soft_decomposition.pdf (read: Section 3.1.2 verifies the assumptions for Glauber dynamics on mixtures over the hypercube {0,1}^d).
- Variance bounds for SMC depending on local mixing via soft decomposition of the target; applies to tempering and Gaussian convolution paths; discrete state spaces allowed.
- SCORE 2 (SMC theory on {0,1}^d). Same: Glauber (Gibbs single-site) dynamics on the hypercube is exactly our Gibbs inclusion move class; useful for Theorem P1 contrasts. Differs: no regression posterior.

C.7 On the convergence of adaptive sequential Monte Carlo methods
- Beskos A., Jasra A., Kantas N., Thiery A.; Annals of Applied Probability 26(2):1111-1146, 2016; arXiv:1306.6462; DOI 10.1214/15-AAP1113. Copy papers/BeskosJasraKantasThiery2016_adaptive_SMC.pdf (abstract read).
- WLLN and CLT for adaptive SMC with adaptation of kernels and of the tempering; explicitly covers Schafer & Chopin 2013 and Chopin 2002 type algorithms (Chopin, A sequential particle filter method for static models, Biometrika 89(3):539-551, 2002, DOI 10.1093/biomet/89.3.539, SCORE 1, the root of data-sequential SMC for static models).
- SCORE 2. Relevance: our pilot-then-frozen-grid design circumvents the random-temperature theory; this paper is the standard citation for what adaptive schedules cost theoretically.

C.8 Nonasymptotic analysis of adaptive and annealed Feynman-Kac particle models
- Giraud F., Del Moral P.; Bernoulli 23(1):670-709, 2017; arXiv:1209.5654; DOI 10.3150/14-BEJ680 (web). Copy papers/GiraudDelMoral2017_adaptive_annealed_FK.pdf (abstract read).
- Time-uniform concentration for annealed FK models via Dobrushin coefficients; an adaptive-temperature particle model proposed; non-asymptotic analysis of the adaptive version left open. SCORE 2. Theory: yes, generic; cited by the Schafer-Chopin citation chain (S2).

C.9 On the stability of sequential Monte Carlo methods in high dimensions (Beskos, Crisan, Jasra; arXiv:1103.3965; Ann. Appl. Probab. 24(4), 2014; DOI 10.1214/13-AAP951) SCORE 1. Cost O(d^2) for product targets; background for the product start law.

C.10 Sequential Monte Carlo samplers: Del Moral, Doucet, Jasra (JRSSB 68(3):411-436, 2006; DOI 10.1111/j.1467-9868.2006.00553.x), local Papers/SMC/. SCORE 1 (method base). On population-based simulation for static inference (Jasra, Stephens, Holmes; Statistics and Computing 17:263-279, 2007; DOI 10.1007/s11222-007-9028-9; examples are mixtures, no BVS) SCORE 1. Neal, Annealed importance sampling (Statistics and Computing 11:125-139, 2001; DOI 10.1023/A:1008923215028) SCORE 1.

C.11 Gap check (explicit negatives). Searches combining (SMC or tempering) x (spike-and-slab or BVS) x (consistency, mixing, polynomial time, complexity) returned only items listed above. Specifically NOT found: (i) a selection-consistency theorem for particle output; (ii) a mixing/complexity theorem for SMC on a BVS posterior; (iii) an "SMC for BVS is polynomial-time" result; (iv) any use of a block-product start law with a discrepancy bridge inside SMC for BVS; (v) a guarantee that "every admissible run reports S0" for any sampler. The nearest to (v) is the split-and-merge consistency of Song-Liang 2015 (statement about a two-stage procedure) and Yang et al. 2016 / Zhou et al. 2022 (consistency + mixing for single-flip chains).

## SECTION D. Ranking by match score (top of list)

Score 3 (SMC/particle over models for BVS, no theory): Schafer-Chopin 2013 (XREF); Schafer thesis 2012; Shi-Dunson 2011; Youssfi-Chopin 2025 (XREF); Ma 2015 (XREF); Vuong 2024; Duan 2019 (theory unverified); Anchored RJSMC 2026 (p = 4).
Score 2 adjacent/theory: Papaspiliopoulos-Rossell 2017; Paulin-Jasra-Thiery 2019; Mathews-Schmidler 2024; Lee-Santana-Gijzen 2024; Marion-Mathews-Schmidler 2023; Bottolo-Richardson 2010; Zhou-Johansen-Aston 2016; Syed et al. 2026; Rockova 2018; Yang-Wainwright-Jordan 2016; Zhou et al. 2022; Song-Liang 2015; Zanella-Roberts 2019; Li-Dutta-Roy SVEN; Hans et al. 2007; Clyde et al. 2011; Clyde-Ghosh 2012; Garcia-Donato & Martinez-Beneito 2013; Schweizer 2012a,b; Beskos et al. 2016; Giraud-Del Moral 2017; Montanari-Wu 2024.
No candidate reached 4 or 5. A 4 or 5 would need SMC over models for BVS plus a theorem; none found (Duan 2019 is the only open question).

## SECTION E. Local copies already in /home/fb31/Bayesian-Variable-Selection/Papers/ (relevant to this search)

Core_bibliography: 01 Liang-Livingstone-Griffin ARNI (2022); 02 Syed et al. optimised annealed SMC (2026); 07 Schafer-Chopin (2013); 08 Staerk-Kateri-Ntzoufras (2024); 09 Zanella informed proposals; 10 Zhou et al. dimension-free mixing; 11 Titsias-Yau Hamming ball; 12 Papaspiliopoulos-Rossell; 13 Ma LIPS; 14 Zanella-Roberts; 23 Dau-Chopin waste-free SMC; 24 Le Fay-Chopin-Vihola complexity of standard and waste-free SMC (2026); 25 Zhou-Johansen-Aston; 26 Lee-Whiteley; 27 Clyde-Ghosh-Littman BAS; 28 Garcia-Donato & Martinez-Beneito; 29 Wang et al. SuSiE; 30 SuSiE 2.0; 31 Hou-Atchade Laplace; 32 Song-Liang split-and-merge. SMC/: Del Moral-Doucet-Jasra 2006. Priors_and_decision_rules: Castillo-Schmidt-Hieber-van der Vaart 2015; Du-Guyader 2021; Afshar-Francis-Cripps OPAD 2024 (Optimal particle-based approximation of discrete distributions, arXiv:2412.00545).
Not local (candidates to add): Shi-Dunson 2011; Rockova 2018; Bottolo-Richardson 2010 (now in SMC_LIT/papers); Liang-Wong 2000; Hans-Dobra-West 2007; Clyde-Ghosh 2012; Yang-Wainwright-Jordan 2016 (now in papers); Paulin et al. 2019, Mathews-Schmidler 2024, Marion et al. 2023, Schweizer 2012, Lee-Santana-Gijzen 2024 (now in papers); Duan 2019; Zhou 2014 thesis; Schafer thesis.

Downloaded by Worker B into /home/fb31/SMC_Theory_Department/SMC_LIT/papers/ (outside any git repo; confirmed "not a git repository"): ZhouJohansenAston2016_adaptiveSMC_model_comparison.pdf; PaulinJasraThiery2019_SMC_multimodal_error_bounds.pdf; MathewsSchmidler2024_SMC_multimodal_complexity.pdf; MarionMathewsSchmidler2023_finite_sample_SMC.pdf; Schweizer2012_nonasymptotic_SMC_Feynman-Kac.pdf; Schweizer2012_SMC_multimodal.pdf; LeeSantanaGijzen2024_SMC_soft_decomposition.pdf; BottoloRichardson2010_ESS.pdf; YangWainwrightJordan2016_complexity_BVS.pdf; ZhouEtAl2022_dimension_free_mixing.pdf; ZhouSmith2022_informed_importance_tempering.pdf; Rigat2008_parallel_hierarchical_sampling.pdf; Schafer2013_particle_optimization_binary.pdf; Jiang2023_spike_slab_sampling.pdf; MontanariWu2024_sparse_regression_sampling.pdf; GiraudDelMoral2017_adaptive_annealed_FK.pdf; BeskosJasraKantasThiery2016_adaptive_SMC.pdf; AssenHinne2026_anchored_RJSMC.pdf. (Vuong, Youssfi-Chopin and Shi-Dunson files in that folder were put there by Worker A; the Shi-Dunson file is only 1.8 KB and is a bot-check page, not the paper.)

## SECTION F. Queries run and citation chains

Tools: WebSearch (about 45 queries), WebFetch (arXiv abs/pdf pages, repository pages), arXiv API (export.arxiv.org over https; 8 queries, narrow recall), Semantic Scholar API (heavily rate-limited, 429; 3 searches failed; 3 citation lists succeeded after back-off), Crossref API (DOI verification of about 60 titles). Generic client name "lit-search-client/1.0"; requests spaced by 3-20 s; no personal data sent.

arXiv API queries: all:"sequential Monte Carlo" AND all:"variable selection"; evolutionary Monte Carlo AND variable selection; parallel tempering AND variable selection AND Bayesian; particle AND variable selection AND stochastic search (0 hits); annealed importance sampling AND model selection; tempered AND Gibbs AND variable selection AND importance; population Monte Carlo AND variable selection (0); cross-entropy AND variable selection (0); adaptive importance sampling AND model space (0).
Semantic Scholar: citations of arXiv:1101.6037 (Schafer-Chopin), of DOI 10.1016/j.spl.2010.10.011 (Shi-Dunson), of arXiv:1002.2706 (ESS); search "particle EM variable selection spike-and-slab".
Web queries (topics): Evolutionary Stochastic Search; Marion-Mathews-Schmidler (two papers); Shi-Dunson PSS; Rockova Particle EM; Liang-Wong EMC; Schweizer (two papers); Paulin-Jasra-Thiery; Yang-Wainwright-Jordan; Zhou et al. dimension-free; SMC polynomial-time spike-and-slab; parallel tempering BVS mixing; Zanella-Roberts; Shotgun SS; Song-Liang; Clyde-Ghosh-Littman; Garcia-Donato-Martinez-Beneito; Papaspiliopoulos-Rossell; Titsias-Yau; Youssfi-Chopin; tempered waste-free SMC; Syed et al.; Jasra-Stephens-Holmes; adaptive importance sampling BVS; equi-energy / population Monte Carlo BVS; Lamnisos-Griffin-Steel; paired-move MTM; FINEMAP/DAP-G/R2GUESS; Ma LIPS; Giraud-Del Moral; population annealing; Chang et al. MTM; Beskos et al.; SMC + locally informed proposals; SMC for structure/BART; selection consistency of SMC output; Liang-Song-Yu; Maity-Basu; Zhou-Smith IIT; Schafer particle optimisation; Clyde-Ghosh 2012; Hubin-Storvik; Atchade-Bhattacharyya; Cozzini; Duan; Davies RJSMC; SVEN; Montanari-Wu; Lee-Santana-Gijzen; Jiang; Anchored RJSMC; thesis searches (theses.fr, ProQuest-style dissertation queries, Schafer, South, Zhou, Vuong, Lee, Dau/Youssfi).
Citation chains followed: forward from Schafer-Chopin 2013, Shi-Dunson 2011, Bottolo-Richardson 2010 (Semantic Scholar); backward from Mathews-Schmidler 2024 / Lee-Santana-Gijzen / Beskos et al. 2016 text; Schweizer 2012a leads to 2012b, Paulin et al. and Mathews-Schmidler; Zhou et al. 2022 and Chang et al. 2022 lead to Zhou-Smith 2022 and Li-Smith-Zhou 2023; Garcia-Donato & Martinez-Beneito leads to Clyde-Ghosh 2012; Hubin-Storvik leads to Bottolo et al. 2011.
Limitations: Semantic Scholar rate limits cut several planned citation lists (Zanella-Roberts, Marion et al., Mathews-Schmidler, Yang et al.); not run: Google Scholar, ProQuest, HAL/theses.fr direct queries (only via web search); Duan 2019 and Shi-Dunson full texts not obtained; Rockova 2018 behind paywall.
