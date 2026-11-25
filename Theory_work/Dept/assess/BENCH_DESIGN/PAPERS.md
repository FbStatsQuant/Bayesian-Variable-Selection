# BENCH_DESIGN: per-paper benchmark setups

*This file is part of [`REPORT.md`](REPORT.md). It holds 89 papers, 88 read in full text. It is generated from the scout TSVs in `scout/`, one row per paper (duplicates merged, full-text rows preferred), and its content is verbatim from those TSVs. Fields follow `SCHEMA.md`. The Haiku checkers verify these entries against the sources and log the results in [`CHECK.md`](CHECK.md).*


## BVS-sampler

### GeorgeMcCulloch1993
George E.I.; McCulloch R.E.; Variable selection via Gibbs sampling; J. Amer. Statist. Assoc.; 88(423); 881-889 (1993). **10.1080/01621459.1993.10476353**

- **X:** not stated in abstract. not stated in abstract
- **n:** not stated in abstract
- **p (max):** not stated in abstract
- **s0:** not stated in abstract
- **β / SNR:** not stated in abstract
- **Noise:** not stated in abstract; **replicates:** not stated in abstract
- **Metrics:** not stated in abstract
- **Competitors:** not stated in abstract
- **Real data:** not stated in abstract
- **Code/data:** not stated in abstract
- *Source pages:* not stated in abstract; *read level:* abstract-only (paywalled; abstract states only that SSVS places a probability distribution on the set of all models and uses the Gibbs sampler to search among promising models; DOI/volume/pages checked against Crossref); *scout file:* `S1_BVS.tsv`

### Hans2007
Hans C.; Dobra A.; West M.; Shotgun stochastic search for "large p" regression; J. Amer. Statist. Assoc.; 102(478); 507-516 (2007). **10.1198/016214507000000121**

- **X:** iid-N(0,I) (null-model scenario; p=5000; n=100); real-X(synthetic beta) (Keck brain-cancer gene expression 41 x 8408 columns; padded with iid N(0,I_41) noise columns beyond 8408); orthogonal design (Sec 4.5; theoretical; n=500). Sec 4.4: 4 true genes chosen from real 41 x 8408 expression matrix (correlated with other genes) placed as variables 1-4; for p<8408 first p columns taken then randomly permuted; for p>8408 extra columns are centred/scaled N(0,I_41) draws; response standardised to mean 0 var 1; Sec 4.5 orthogonal: x_i'x_j=0; eps=(n-1)*.005 for null coords; lambda=(n-1)*.1 for true coords
- **n:** 100 (null scenario); 41 (Sec 4.4 simulation); 500 (Sec 4.5 orthogonal calculation); 148 (real example)
- **p (max):** 25000 (Sec 4.4; p grid 1000;2500;5000;7500;8408;10000;12500;15000;17500;20000;22500;25000 read from Fig 3); 5000 (null scenario); flag p>=1e4: yes (2.5e4); no p>=1e5
- **s0:** 4 (Sec 4.4: beta=(1.3;0.3;-1.2;-0.5); two large two small); 0 (null scenario); k=3-6 (Sec 4.5)
- **β / SNR:** Sec 4.4: y=1.3x1+.3x2-1.2x3-.5x4+eps; eps variance 0.5; 41 obs so SNR low-moderate; model prior pi=4/p; tau=1; delta=3
- **Noise:** Gaussian sigma^2=0.5; **replicates:** 50 simulated responses per p (m=1..50)
- **Metrics:** iterations and elapsed minutes until true model first evaluated within neighbourhood (cap 10000 iterations; boxplots + count not found in parentheses); accumulated posterior mass in top 1e6 models vs number of model evaluations (SSS vs Gibbs vs MC3 on Keck data); expected steps to find true model (SSS vs Metropolis in orthogonal case; Fig 4)
- **Competitors:** SSS (parallel; 21 processors) vs MC3 vs one-at-a-time Gibbs sampler (equal numbers of model evaluations; Sec 4.2); fixed-dimensional Metropolis (Sec 4.5)
- **Real data:** Keck brain cancer gene expression (Rich et al 2005; n=41; p=8408): used for the simulation and for SSS vs Gibbs vs MC3 mass accumulation (pi=10/p; 40000 SSS iterations); breast cancer lymph node status (n=148; 100 low-risk vs 48 high-risk; p=4514 = 4512 genes + tumor size + ER status; binary probit regression)
- **Code/data:** software SSS (Hans-Dobra-West; Duke; paper mentions on-line technical report); data not provided in text
- *Source pages:* Sec 4.2 (p511 Fig 1); 4.3 (p511); 4.4 (pp511-512; Fig 3 p512); 4.5 (p512 Fig 4); Sec 5.1-5.2 (p513); *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Bottolo2010
Bottolo L.; Richardson S.; Evolutionary stochastic search for Bayesian model exploration; Bayesian Analysis; 5(3); 583-618 (2010). **arXiv:1002.2706; DOI 10.1214/10-BA523**

- **X:** equicorr(pairwise corr 0.5; George-McCulloch 1993 X1); block(George-McCulloch 1997 X2: multicollinear groups with corr 0.998); concatenated blocks (Nott-Green 2004 building blocks); real-X(synthetic beta) (HapMap SNP region ENm014 n=120; p=775); real-X+real-y (eQTL rat; mQTL). Ex1-Ex5 built from X1 (n x 60; X_j = X*_j + Z gives pairwise corr 0.5) and X2 (n x 15; X_j=Z_i+2Z_j with near-duplicate columns of corr 0.998); Ex2 X=[X2 X2] 300x30; Ex4 five copies of X3=[X2 X1*] -> 120x300; Ex5 200x1000 contaminated-model design; Ex6 HapMap 120x775 with natural LD blocks
- **n:** 120;300;200 (simulated); eQTL n=29; mQTL n=50
- **p (max):** 1000 (Ex5; p grid 30;60;300;775;1000); real mQTL p=10000 (flag p>=1e4)
- **s0:** Ex1: 5; Ex2: 8; Ex3: 45 (three blocks of 15 with beta=1;2;3); Ex4: 16; Ex5: 10 (model 1) plus 5 (model 2 contamination); Ex6: 10
- **β / SNR:** Ex1 gamma=(21;37;46;53;54) beta=(2.5;0.5;-1;1.5;0.5) eps sd 2; Ex2 beta=1.5 (one -1.5) eps sd 2.5; Ex3 beta blocks 0;1;2;3 sd 2; Ex4 beta in {2;-1;1.5;1;0.5} eps sd 2.5; Ex5 eps sd 0.05 with R^2 conditions; Ex6 beta~N(0;9) eps sd 0.10 (error sd ranges 0.05 to 2.5)
- **Noise:** Gaussian with sd 0.05 to 2.5 depending on example; **replicates:** 25 replicates of each of the six set-ups; 20000 sweeps after burn-in 2000; L=5 chains
- **Metrics:** marginal posterior inclusion probabilities (averaged over sweeps and replicates; IQR across replicates); posterior model size; mixing between chains; acceptance rate; comparison with SSS (Hans 2007); run time
- **Competitors:** ESS (ESSi independent prior; ESSg g-prior); SSS (Hans-Dobra-West 2007); MC3; FSMH vs MC3 local moves; block/1-point/uniform/adaptive crossover
- **Real data:** Rat eQTL (Hubner 2005; n=29; p=1421 SNPs); human mQTL metabolomics (n=50; p=10000 SNP predictors; MS bins); HapMap region ENm014 (Yoruba) 120 chromosomes -> 775 SNPs (design for Ex6)
- **Code/data:** software ESS++ (separate Bioinformatics 2011 paper); no code URL found in text
- *Source pages:* Sec 4.1 (pp 15-17; eQTL; mQTL); Sec 4.2; Appendix B.1-B.3 (pp 29-37); *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Clyde2011
Clyde M.A.; Ghosh J.; Littman M.L.; Bayesian adaptive sampling for variable selection and model averaging; J. Comput. Graph. Statist.; 20(1); 80-101 (2011). **10.1198/jcgs.2010.09049**

- **X:** iid-N(0,1) columns (centered) with one near-duplicate pair (col 9 vs col 2 correlation approx 0.99). Simulation (Sec 4): all columns except the ninth generated as independent N(0,1) then centered; ninth column constructed so its correlation with column 2 is approx 0.99 (generating formula not stated); Zellner g-prior g=n; p(alpha,phi|gamma) prop 1/phi; uniform prior over models p(M)=1/2^p; marginal likelihood (18); posterior inclusion probs approx 0.5 for variables 2 and 9 giving bimodal model posterior; model space 2^15=32768 enumerated for exact truth. Real data: US Crime (Vandaele 1978; 15 predictors; continuous variables log-transformed; g=n; uniform model prior); Protein activity (Clyde & Parmigiani 1998; categorical coded by indicators; all main effects + 2-way interactions + quadratic terms for continuous variables; max pairwise correlation 0.99 with 17 pairs above 0.95; g=n=96)
- **n:** 100 (simulation); US Crime n not stated; 96 (protein)
- **p (max):** 15 (simulation; US Crime also 15); 88 (protein real data; model space 2^88)
- **s0:** 5 nonzero betas in the 15-vector (positions 1;2;3;4;9); 10 zero
- **β / SNR:** alpha=2; beta=(-0.48; 8.72; -1.76; -1.87; 0; 0; 0; 0; 4.00; 0; 0; 0; 0; 0; 0) (fixed; signs mixed; nonzero at positions 1-4 and 9); phi=1; no SNR or R^2 convention stated
- **Noise:** Gaussian linear model; error precision phi=1 (i.e. sigma^2=1) as stated; error distribution not otherwise spelled out in Sec 4; **replicates:** 100 (text: BAS vs SRSWOR 'based on 100 repetitions'; MCMC 'running each algorithm 100 times with different seeds'; Tables 1-2 say '100 simulated data sets' / '100 replicates'; whether one fixed data set with 100 seeds or 100 new data sets is not explicit); protein: 10 repeats of each procedure; US Crime: not stated (BAS run 2^15 iterations = full enumeration)
- **Metrics:** Sim: total posterior probability of unsampled models (Figs 2-3; boxplots); bias and RMSE of marginal inclusion probabilities pi_j, model probability I(gamma) and mean mu of Y (Tables 1-2) with sampled runs compared to exact enumeration; US Crime: trace of log marginal likelihoods; number of unique models visited (2994 for RS-Thin vs all 32768 for BAS); unsampled mass 0.037; Protein: distribution of log marginal likelihood of sampled models over 10 runs (Fig 5); pairwise scatter of PIPs (Fig 6); MPM (21 vars) and HPM (28 vars) sizes and log marginals; leave-one-out CVRootMSE of BMA over top 10000 models (Table 3)
- **Competitors:** SRSWOR (simple random sampling without replacement); MC3 (Madigan-York add/delete one coordinate); RS (random-swap MC3 + swap proposal; omega=1/2); RS-Thin (RS run p times longer saving every pth draw); each with Monte-Carlo (MC) and re-normalized (RM) estimators; BAS variants (eplogp p-value calibration; uniform; RST-MC and RST-RM initial inclusion probs); SSVS CVRootMSE 0.527 quoted from Clyde & Parmigiani 1998; Nott-Kohn AMCMC not included
- **Real data:** US Crime (Vandaele 1978; n not stated; p=15); Protein activity (Clyde & Parmigiani 1998; n=96; p=88)
- **Code/data:** Supplemental materials: R package BAS (BAS_0.90.tar.gz; CRAN; http://www.stat.duke.edu/~clyde/BAS; includes protein data); Data and Code zip (code-rev2.zip: simulated and real data; C and R MCMC code; post-processing and figures); proofs+pseudocode.pdf
- *Source pages:* Sec 4 simulated data (manuscript pp 13-17) incl 4.1 (p15) 4.2 (p16) Tables 1-2 (pp17-18); Sec 5 US Crime (pp17-19); Sec 6 protein (pp19-21) Table 3 (p21); Sec 7 discussion (pp22-23); supplemental materials list (p24); page numbers are those of the author-manuscript PDF not the JCGS journal pages; *read level:* full-text; *scout file:* `S4_LOCAL.tsv`

### GuanStephens2011
Guan Y; Stephens M. Bayesian variable selection regression for genome-wide association studies and other large-scale problems. Ann Appl Stat 5(3) 1780-1815 (2011). **10.1214/11-AOAS455 (arXiv 1110.6019)**

- **X:** iid-binomial SNPs (indep); real-X(synthetic beta); binary/SNP-genotypes. 10K: 10000 independent SNPs, MAF~U[0.05,0.5], x_ij~Bin(2,f_j). 317K: real Illumina 317K chip genotypes of 980 PARC individuals; 550K: real Illumina 610K+13680 i-Select chip 988 individuals (550K SNPs after QC); missing genotypes replaced by HMM posterior mean (BIMBAM). Chromosome 22 subset of 550K (9041 correlated SNPs) used for the power comparison
- **n:** 1000 and 6000 (10K sim); 980 (317K); 988 (550K); 1968 merged (CRP)
- **p (max):** 1e4; 3.17e5; 5.5e5 (real genotypes with synthetic phenotypes); real CRP data 530691
- **s0:** 30 causal SNPs
- **β / SNR:** 30 random causal SNPs; effects iid N(0,1) or double-exponential DE(1) (DE shown); tau set to achieve target PVE; PVE 0.01-0.50 step 0.01 (50 phenotype sets each); PVE=0.25 for 100-dataset power study; PVE=0.3 vs null PVE=0
- **Noise:** Gaussian; **replicates:** 50 phenotype sets (PVE grid); 100 data sets (power/ROC, 10K and chr22 9041 SNPs); 10 null sets
- **Metrics:** PVE posterior accuracy (90% CI coverage 85%); TP vs FP trade-off curves summed over 100 data sets; relative prediction gain; PIP calibration; runtime (minutes to ~1 day on 1 core; BVSR 1M iters on 10K, 2M on 317K/550K)
- **Competitors:** single-SNP Bayes factors; LASSO (lars package)
- **Real data:** PARC GWAS C-reactive protein: 1968 individuals x 530691 SNPs after imputation (BIMBAM) and MAF>=0.01; phenotype adjusted for age sex smoking BMI and quantile normalised (data not public)
- **Code/data:** piMASS software (Guan lab website bcm.edu/cnrc/mcmcmc/pimass); PARC data not public
- *Source pages:* Sec 5.1-5.8 (pp 13-25); *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Carbonetto2012
Carbonetto P.; Stephens M.; Scalable variational inference for Bayesian variable selection in regression and its accuracy in genetic association studies; Bayesian Analysis; 7(1); 73-108 (2012). **10.1214/12-BA703**

- **X:** binary/SNP-genotypes (independent SNPs: x_ik~Binomial(2;f_k) with MAF f_k~U[0.05;0.5]); real-X(synthetic beta) (1037 SNPs in IL27 region from WTCCC T1D cohort; real LD correlation). Sim 1: independent SNP genotypes; Sim 2: real WTCCC genotypes of ~10 Mb region around IL27 (1037 SNPs) with n=2000 subsampled from 4901 individuals; hyperparameter priors: p(sigma^2) propto 1/sigma^2; pi~Beta(0.02;1) in simulations; logit10 pi normal prior mean -5 in the Crohn's case study
- **n:** 500 (Sim 1); 2000 (Sim 2); 4686 (Crohn's: 1748 cases; 2938 controls)
- **p (max):** 1037 (Sim 2: 1037 SNPs); 1000 (Sim 1); real GWAS p=442001 (flag p>=1e5 real data)
- **s0:** 20 (m=20 random SNPs; both sims)
- **β / SNR:** m=20 SNPs with nonzero effects chosen uniformly at random; beta_k iid N(0,1); sigma=3 (genetic factors explain about half the variance; h2~0.5); true pi=0.02
- **Noise:** Gaussian sigma=3; **replicates:** 50 trials for each simulation study
- **Metrics:** accuracy of variational vs MCMC posterior inclusion probabilities (scatter); posterior means of hyperparameters (log10 sigma^2; log10 sigma_beta^2; log10 pi) variational vs MCMC; computation time (minutes to a day); expected counts of selected variables
- **Competitors:** Variational inference (varbvs); MCMC (full Gibbs-type sampler) as reference
- **Real data:** Crohn disease WTCCC 2007 GWAS (n=4686: 1748 cases; 2938 controls; p=442001 SNPs; logistic model): variational vs MCMC hyperparameters and top associations
- **Code/data:** MATLAB and R implementations (varbvs; github.com/pcarbo/varbvs); data from WTCCC (controlled access)
- *Source pages:* Sec 5.1 (pp 83-87); Sec 5.2 (pp 89-93) Tables 1-4; Sec 6 (pp 93-100); *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Schafer2013
Schafer C.; Chopin N.; Sequential Monte Carlo on large binary sampling spaces; Statistics and Computing; 23(2); 163-184 (2013). **10.1007/s11222-011-9299-z (arXiv:1101.6037)**

- **X:** real-X+real-y (no synthetic design; real datasets augmented with interactions/polynomials/logs to create collinearity). Boston: 13 columns + first-order interactions + squares (except chas) + constant -> 104 predictors; Concrete: 8 covariates + logs -> 13 + all interactions + constant = 79 predictors; Protein: factors expanded; interactions + constant -> 88 predictors (some constant zero columns dropped); variants with and without main-effect (hierarchy) restrictions
- **n:** 506;1030;96
- **p (max):** 104 (real; no synthetic p grid; also a separate toy p-range in Sec 5.3 comparisons)
- **s0:** unknown (real data; truth not available; reference = long MCMC run of days)
- **β / SNR:** none (no true beta); hierarchical Bayesian prior on gamma as in Sec 2; reference PIPs from MCMC run for a few days
- **Noise:** Gaussian linear regression (log response for Boston); **replicates:** 200 runs of each algorithm per dataset
- **Metrics:** spread of Monte Carlo PIP estimates across 200 runs (box-plots: 80% white box; outliers black); averaged key indicators in Tables 3-8; number of evaluations of pi; run time
- **Competitors:** SMC (proposed; logistic conditionals model); standard metropolised Gibbs MCMC (Liu 1996; bit-flip count truncated geometric mean 2); Adaptive MCMC (Nott-Kohn 2005); SMC vs MCMC with and without main-effect restrictions
- **Real data:** Boston Housing (n=506;p=104 after expansion); Concrete Compressive Strength (n=1030;p=79); Protein activity (Clyde-Parmigiani 1998; n=96;p=88)
- **Code/data:** Python 2.6 (SciPy) implementation; csv-format data; R scripts generated for plots only; datasets freely available (StatLib; UCI; BAS package); no repo URL found in text
- *Source pages:* Sec 6.1-6.5 (pp 21-26); Figs 3-8 and Tables 3-8; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Rockova2014
Rockova V.; George E.I.; EMVS: the EM approach to Bayesian variable selection; J. Amer. Statist. Assoc.; 109(506); 828-846 (2014). **10.1080/01621459.2013.869223**

- **X:** AR1(rho=0.6); equicorr(rho=0.8 within 3 groups; zero between); real-X+real-y (yeast cell-cycle motif counts). Illustrative: rows N_p(0;Sigma) Sigma_ij=0.6^|i-j|; structured-prior example: three equicorrelated groups of 33 predictors rho=0.8 within group; timing study rows N_p(0;Sigma) with rho=0.6 rescaled ||x_i||<=1 (SDCA)
- **n:** 100 (illustrative; structured example); 500;2000 (timing); real n=1568 genes
- **p (max):** 1000 (illustrative p=1000); 99 (structured example); real p=8192 motifs
- **s0:** 3 (beta=(1;2;3;0...)); 33 (structured example group); timing beta=(2;3;4;0...)
- **β / SNR:** beta=(1;2;3;0;...;0); sigma^2=3 (illustrative); sigma^2=5 and beta_i=2 for first 33 coordinates (structured example)
- **Noise:** Gaussian sigma^2=3 (illustrative); sigma^2=5 (structured); **replicates:** single simulated dataset in the EMVS illustration (not replicated); comparison with MH sampler run for same wall time; structured example described without replication count in text read
- **Metrics:** posterior-mode path over v0 grid (51 values; spike-and-slab regularisation diagram); iterations to EM convergence (4 iterations); log g0(gamma) of visited models; number of true variables recovered; MH acceptance rate (0.0001); run time vs stochastic search
- **Competitors:** EMVS (dynamic posterior exploration over v0); MH stochastic search with one-step random-scan proposal; also compared with LASSO; SCAD; group lasso in other chapters
- **Real data:** Yeast cell-cycle transcription motifs (Spellman 1998; Li-Zhang 2010; n=1568 genes; p=8192 7-mer motifs; response = PC1 of 18 time points): motif selection with beta-binomial and MRF structured priors
- **Code/data:** R package EMVS on CRAN; no repo in thesis text
- *Source pages:* Thesis Ch.3: Sec 3.4 (pp 47-52); 3.4.3 speed comparison (p51); 3.7.3 (p65); 3.8.1 timing (p69); 3.9 motifs (pp 71-76); *read level:* full-text (thesis chapter; JASA paywalled); *scout file:* `S1_BVS.tsv`

### SongLiang2015
Song Q.; Liang F.; A split-and-merge Bayesian variable selection approach for ultrahigh dimensional regression; J. R. Stat. Soc. Ser. B; 77(5); 947-972 (2015). **10.1111/rssb.12095**

- **X:** multivariate normal; equicorrelated within a block (rho=0.25 default; 0.9 stress test); remaining columns independent in Ex 2 and massive example; unit variance columns. Ex 1 (Sec 4.1.1): X multivariate normal; each column variance 1; correlation between ALL different columns 0.25 (also 0.9 in a stress run); P_n=n^1.5. Ex 2 (4.1.2): first 100 columns mutually correlated with equal correlation 0.25 and independent of the remaining 900 mutually independent columns. Massive example (4.2): multivariate normal; 2000 predictors equally correlated with rho=0.25 and the rest uncorrelated; five true predictors lie among the 2000 correlated ones. Supplement S4 (horseshoe comparison): multivariate normal; pairwise correlation 0.25; unit variance per predictor. Prior/tuning: r_n=P_n^(1-gamma) with gamma=0.75 (Ex 1 uses r_n=sqrt(n); rbar_n=2 sqrt(n)); lambda_s=|s|^-gamma; a0=b0=1; tau=0.01; alpha1=0.15 (stage 1 FDR); alpha2=0.01 (stage 2 FDR); SAMC sampler with gain a_k=k0/max(k0;k)
- **n:** Ex 1: n=20 to 120 per setting (Fig 1 shows n=38;50;63;75;88;100;113; Fig 3 rho=0.9 uses n=30 to 125 with n=38..125 shown); Ex 2: 150; massive: 100; supplement S4: 500; real: 50 (metabolic QTL); 60 (mouse PCR)
- **p (max):** 500000 (massive example 4.2; split into 1000 subsets of s=500 predictors); other: Ex 1 P_n=n^1.5 (about 1315 at n=120; about 1398 at n=125 by computation); Ex 2 1000 (50 subsets of s=20); S4 500; real 10000 (SNPs) and 22575 (genes)
- **s0:** Ex 1: 5 (first five columns); Ex 2: 3 (first three columns); massive: 5 (within the 2000 correlated predictors); S4: 5 (5 nonzero coefficients; which columns not stated)
- **β / SNR:** Ex 1: beta=(0.7;0.9;1.1;1.3;1.5) on first five columns (all positive); Ex 2: (1.5;3.0;4.5) on first three columns; massive: (0.2;0.3;0.4;0.5;0.6) on five of the 2000 correlated predictors (which five not stated); S4: (0.7;0.9;1.1;1.3;1.5); no SNR or R^2 convention stated
- **Noise:** Ex 1: sigma*=1; Ex 2: not stated (no sigma given in the Ex 2 text); massive: sigma*^2=0.25; S4: sigma^2=1; Gaussian linear regression (noise distribution implicit); **replicates:** 100 simulated data sets for each setting in Ex 1 (each n; and rho=0.9 variant) Ex 2 and massive example; S4: 100 data sets; real data single data set (SAM applied once)
- **Metrics:** Ex 1: marginal inclusion probabilities of the five true predictors and one false predictor (Figs 1 and 3) and probability that MAP model equals true model with 95% CI (Fig 2); Ex 2: stage-1 selected size (166.6) correlated predictors retained (98.2) stage-2 size (3.2) true predictors selected (3.0) (Table 1); massive: model size |xi|; |xi cap t|; false selection rate fsr=|xi minus t|/|xi|; negative selection rate nsr=|t minus xi|/|t|; MSE ||beta_hat_xi - beta*||^2 (Table 2); CPU time (about 16 h serial per data set; about 0.5 h on 100 cores); real data: leave-one-out CV squared error of fixed selected models (median or mean) and MAP_i models along paths (Figs 4-5); S4: L2 estimation error of beta against time (Fig S1)
- **Competitors:** Massive example: lasso (glmnet; 10-fold CV); elastic net (glmnet; 10-fold CV); SIS-SCAD; ISIS-SCAD (R package SIS). Real data: SIS-SCAD; ISIS-SCAD; lasso; SIS-lasso; ISIS-lasso along regularisation paths. S4: horseshoe prior via Gibbs sampler (Gibbs also tried on P_n=500000: about 24 h for a couple of iterations). Ex 1-2: no competitor
- **Real data:** Metabolic quantitative trait loci (Dumas et al. 2007; Kindmark et al. 2008; data from L. Bottolo; response one metabolite bin as in Bottolo and Richardson 2010): n=50; p=10000 preselected SNPs (SAM: 20 subsets s=500; stage 1 kept 536; stage 2 chose 2 SNPs); Polymerase chain reaction mouse (Lan et al. 2006; GEO GSE3330; response PEPCK): n=60 (31 female; 29 male F2 mice); p=22575 genes (45 subsets s=502; stage 1 kept 1113; stage 2 chose 6 genes with r_n=P_n^0.3)
- **Code/data:** Not stated for code (no URL in main text; on-line supplementary material gives proofs; SAMC implementation description; horseshoe comparison); PCR data public at GEO GSE3330; metabolic QTL data supplied by Bottolo (no public link stated)
- *Source pages:* Sec 3.2 hyperparameters (pp959-960); Sec 4.1.1 Ex 1 (pp960-962) Figs 1-3 (pp961-963); Sec 4.1.2 Ex 2 (pp962-964) Table 1 (p964); Sec 4.2 massive (pp964-965) Table 2 (p965); Sec 5.1 (pp965-967) Fig 4 (p966); Sec 5.2 (p967) Fig 5 (p967); Sec 6 time complexity (p968); Sec 7 horseshoe remark (p970); Supplement S4 (supplement pp17-18) and S2 SAMC; *read level:* full-text; *scout file:* `S4_LOCAL.tsv`

### Yang2016
Yang Y.; Wainwright M.J.; Jordan M.I.; On the computational complexity of high-dimensional Bayesian variable selection; Annals of Statistics; 44(6); 2497-2532 (2016). **10.1214/15-AOS1417 (arXiv:1505.07925)**

- **X:** iid-N(0,I); Toeplitz(Sigma_jk=exp(-|j-k|)); special correlated design Sigma_bad (first row/col mu=1/(2 sqrt p) rest identity; Wainwright lasso-failure example). Rows iid; this is the origin of the widely copied Yang-Wainwright-Jordan benchmark. Sigma_jk=e^{-|j-k|} is AR(1) with rho=0.37
- **n:** 500;1000 in Tables 1-2 (text states n in {300;900} and p in {500;5000}); n=300 for Sigma_bad
- **p (max):** 5000 (p grid 1000;5000; text also 500); p=80 for Sigma_bad
- **s0:** 10 (s*=10); 20 for Sigma_bad (n,p,s*)=(300,80,20)
- **β / SNR:** beta*=SNR*sqrt(sigma^2 log p/n)*(2,-3,2,2,-3,3,-2,3,-2,3,0,...,0); SNR in {0.5;1;2;3}; sigma^2=1; prior g=p^3; s0=100
- **Noise:** Gaussian sigma^2=1; **replicates:** 20 simulated datasets per setting (6 chains each: 3 near null, 3 at true model; 20p iterations); 100 replicates for Sigma_bad Lasso comparison
- **Metrics:** Gelman-Rubin scale factor <1.5 on R^2_gamma (proportion of successful trials SP); log posterior difference highest model minus true model (H-T) and null minus true (N-T); iterations to convergence in units of p; log ratio of posterior prob of selected vs true model
- **Competitors:** Random-walk add-delete-swap Metropolis-Hastings (theory-focused); Lasso (CV) on Sigma_bad
- **Real data:** none
- **Code/data:** no code reference found in text
- *Source pages:* Sec 3.4 (pp 10-15) Tables 1-2 Figs 1-2; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Titsias2017
Titsias M.K.; Yau C.; The Hamming ball sampler; J. Amer. Statist. Assoc.; 112(520); 1598-1611 (2017). **arXiv:1504.08133; DOI 10.1080/01621459.2016.1222288**

- **X:** other (two perfectly confounded relevant columns among noisy redundant inputs); real-X+real-y (eQTL; SI only). Main text gives only: N=100 responses, D=1200 covariates, two relevant covariates (x11 and x611) that are perfect confounders (only one needed) -- constructed for multimodality (true PIPs 0.5 each); other covariates noisy redundant inputs; g=N; beta prior Beta(0.001;1) on inclusion; details of X generation in SI D (SI not in the arXiv v2 PDF I opened)
- **n:** 100 (simulated); eQTL n not given in main text
- **p (max):** 1200 (simulated); 10000 covariates in real eQTL example (SI D.3; flag p>=1e4)
- **s0:** 2 true covariates (perfect confounders)
- **β / SNR:** not stated in main text (SI D); two relevant covariates fully explain response
- **Noise:** Gaussian with sigma^2 inverse-gamma prior (0.1;0.1); **replicates:** single simulated dataset per example; MCMC traces (replicate count not stated in main text)
- **Metrics:** running marginal PIPs of the two relevant variables vs expected 0.5; CPU time; integrated autocorrelation time; log joint density traces
- **Competitors:** block Gibbs samplers BG1-3; Hamming ball samplers HB1-3 (K=10; radii m=1-3)
- **Real data:** real eQTL example with 10000 covariates and real tumour deconvolution (both only in SI; not read)
- **Code/data:** code not stated in main text
- *Source pages:* Sec 2.2 (pp 5-7) Fig 3; Sec 4.2 (pp ~13); SI not in the PDF read; *read level:* full-text (main text only; SI D.1-D.3 not available in arXiv v2 PDF); *scout file:* `S1_BVS.tsv`

### Narisetty2019
Narisetty N.N.; Shen J.; He X.; Skinny Gibbs: a consistent and scalable Gibbs sampler for model selection; J. Amer. Statist. Assoc.; 114(527); 1205-1217 (2019). **10.1080/01621459.2018.1482754**

- **X:** equicorr(rho=0.25 for all pairs; rho1=rho2=rho3=0 or 0.25); block-type(active-active rho1; active-inactive rho2; inactive-inactive rho3); iid-N(0,I); real-X+real-y (mouse PCR; Lymph). Logistic-regression responses; first |t| columns active; Gibbs prior tau0n^2=1/n; tau1n^2=max(p^2.1/(100n);1); K=max(10;log n); max model size max(30;sqrt n); CPU timing study uses iid design with p=50..1000
- **n:** 100;200
- **p (max):** 1000 (p grid 50;250;1000; CPU timing p=50 to 1000 step 50)
- **s0:** 4 or 8 (two sparsity levels)
- **β / SNR:** beta_t=(-1.5;2;-2.5;3) for |t|=4; beta_t=(-1.5;1.714;-1.929;2.143;-2.357;2.571;-2.786;3) for |t|=8 at p=1000 (Table 3); (-2;2.143;-2.286;2.429;-2.571;2.714;-2.857;3) for |t|=8 at p=50;250 (Table 2) (timing study uses (1.5;2;2.5;3)); logistic link
- **Noise:** Bernoulli with logistic link (no Gaussian noise); **replicates:** 100 randomly generated datasets per setting (10 Gibbs chains each; burn-in 2000 (5000 for Table 3 p=1000); length 5000); 10 datasets for CPU timing
- **Metrics:** TP; TPs (true positives at known sparsity); FP; exact recovery Z=t; inclusion Z contains t; Zs=t; CPU time vs p; 10-fold CV squared-error prediction error; marginal posterior probabilities from two chains
- **Competitors:** Skinny Gibbs; BASAD (full Gibbs); BSR (Liang 2013 Bayesian subset regression); varbvs variational Bayes; adaptive Lasso; SCAD; MCP
- **Real data:** Mouse PCR GPAT (Lan 2006; n=60; 22575 genes screened to 99 + gender -> p=100; binary response GPAT<Q(0.4)); Lymph node (Hans 2007; n=148; p=4514: 4512 genes + tumour size + ER status; binary risk)
- **Code/data:** R implementation referenced; data GEO GSE3330
- *Source pages:* Sec 4 (pp 21-27) Tables 1-3 (pp 24-29); Sec 4.1 Fig 2; Sec 5.1-5.2 (pp 29-33); *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Zanella2019
Zanella G.; Roberts G.; Scalable importance tempering and Bayesian variable selection; J. R. Stat. Soc. B; 81(3); 489-517 (2019). **10.1111/rssb.12316 (arXiv:1805.00541)**

- **X:** block(3 correlated variables x2 batches; rho=0.9); equicorr-pair(rho=0.99 between X1,X2 only); iid-N(0,I); real-X+real-y (DLD; TGFB172; TGFB). Scenario 1: two strongly correlated vars Sigma12=0.99 else 0; Scenario 2: Sigma_ij=0.9 for i,j in {1,2,3} or {4,5,6} else 0; Scenario 3: Sigma=I; unit variances; prior h=5/p; c=1e3 in simulations (c=n and c=p^2 for real data)
- **n:** 50;200;500 (simulated; (p,n) grid (100,50),(200,200),(1000,500)); real: 192;262
- **p (max):** 1000 (simulated; p grid 100;200;1000); real TGFB p=10172 (flag p>=1e4)
- **s0:** scenario 1: 1 nonzero (beta0=(1,0,...)); scenario 2: 6; scenario 3: 10
- **β / SNR:** beta*=sqrt(sigma^2 log p/n)*SNR*beta0 with beta0 = (1,0..); (3,3,-2,3,3,-2,0..); (2,-3,2,2,-3,3,-2,3,-2,3,0..); sigma^2=1; SNR=0.5;1;2;3
- **Noise:** Gaussian sigma^2=1; **replicates:** 50 runs of each algorithm per simulated dataset to estimate variance of PIP estimators; 20 independent runs per real dataset
- **Metrics:** relative efficiency of PIP estimators (ESS/CPU time ratio vs Gibbs sampler; median over variables); PIP agreement across independent runs (scatter); CPU time
- **Competitors:** Gibbs sampler (Metropolised); TGS; wTGS; Hamming ball sampler (Titsias-Yau); also comparison with R packages (Supp B.6)
- **Real data:** DLD (n=192; p=57; RNA-seq; Yuan 2016); TGFB172 (n=262; p=172); TGFB (n=262; p=10172; Calon 2012 colon cancer microarray gene expression)
- **Code/data:** code https://github.com/gzanella/TGS; real data from supplement of Rossell-Telesca 2017 and Rossell-Rubio
- *Source pages:* Sec 5.1 Fig 4 (p21); Sec 5.2 (pp 22-24) Tables 1-2; Sec 5.3 (pp 25-26) Fig 6; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Griffin2021
Griffin J.E.; Latuszynski K.; Steel M.F.J.; In search of lost (mixing) time: adaptive Markov chain Monte Carlo schemes for Bayesian variable selection with very large p; Biometrika; 108(1); 53-69 (2021). **10.1093/biomet/asaa055 (arXiv:1708.05678)**

- **X:** AR1(rho=0.6); real-X (Tecator; Boston; concrete; protein; mouse PCR gene expression; mouse SNP). Sec 4.1 follows Yang-Wainwright-Jordan 2016: rows x_i~N(0,Sigma), Sigma_jk=0.6^|j-k|
- **n:** 500;1000 (simulated); real: 172;506;1030;96;60;993
- **p (max):** 5000 (simulated; p grid 500;5000); real: 22576 (PCR mouse, n=60; also Tecator p=100; Boston p=104; concrete p=79; protein p=88) and 79748 SNPs (mouse, n=993)
- **s0:** 10
- **β / SNR:** beta*=SNR*sqrt(sigma^2 log p/n)*(2,-3,2,2,-3,3,-2,3,-2,3,0,...,0); SNR=0.5;1;2;3; sigma^2=1; prior Vgamma=9I, h=10/p
- **Noise:** Gaussian N(0,1); **replicates:** 200 runs of each algorithm per setting (to estimate variance of PIPs); 3 independent runs on very-large-p real data
- **Metrics:** relative time-standardised ESS of PIPs r_{A,B}=(ESS_A/t_A)/(ESS_B/t_B) estimated from variance of PIP estimates over 200 runs; agreement of PIPs across independent runs (pairwise scatter); acceptance rate; run time
- **Competitors:** add-delete-swap MH; EIA; ASI (proposed); multiple chain versions; parallel tempering; Hamming ball sampler; Schafer-Chopin SMC; Ji-Schmidler adaptive sampler; LASSO-initialised ADS
- **Real data:** Tecator (n=172,p=100); Boston Housing (n=506,p=104; Schafer-Chopin version with interactions); concrete (n=1030,p=79); protein (n=96,p=88); mouse PCR1-3 (Bondell-Reich; n=60,p=22576); mouse SNP testis weight (Carbonetto 2017; n=993; p=79748)
- **Code/data:** code https://warwick.ac.uk/go/msteel/steel_homepage/software/version3.0.zip; data from cited sources
- *Source pages:* Sec 4.1 (pp 13-15) Table 1; 4.2-4.4 (pp 15-18); *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Wan2021
Wan K.Y.Y.; Griffin J.E.; An adaptive MCMC method for Bayesian variable selection in logistic and accelerated failure time regression models; Stat. Comput.; 31(1); article 6 (2021). **10.1007/s11222-020-09974-2**

- **X:** AR1(rho=0.6); real-X+real-y (microarray cancer data). Sec 4.1: logistic version of Yang et al. 2016 design: x_i~N(0;Sigma) Sigma_jk=0.6^|j-k|; y from logistic link of eta=X beta; real data columns scaled to sd 1 (logistic sets); not standardised in AFT sets; all samplers 105000 iterations with burn-in 5000
- **n:** 500;1000 (simulation); 31;62;72;136 (logistic real); 235;614 (AFT real)
- **p (max):** 5000 (simulation grid p=500;5000; flag p>=1e4: real Prostate p=10150)
- **s0:** 10 (first 10 coefficients nonzero)
- **β / SNR:** beta = SNR*(2;-3;2;2;-3;3;-2;3;-2;3;0...0) with SNR in {0.5;1;2;3}
- **Noise:** Bernoulli/logistic (simulation); AFT survival models with censoring 43.4 percent / 78.1 percent (real; error distribution not checked); **replicates:** single simulated dataset per (n;p;SNR) cell (replication count not stated in text read)
- **Metrics:** median over j of ESS of gamma_j; time-normalised ESS (ESS/time) relative to ADS-DA baseline; ESS
- **Competitors:** ASI (adaptively scaled individual) vs ADS (add-delete-swap) each with Polya-gamma data augmentation; Laplace approximation; correlated pseudo-marginal (CPM)
- **Real data:** Arthritis (Sha et al 2003; n=31; p=755); Colon Tumor (Alon 1999; n=62; p=1224); Leukemia (Armstrong 2002; n=72; p=3571); Prostate (Singh 2002; n=136; p=10150); DLBCL (Rosenwald 2002; n=235; p=7399; 43.4 pct censored); Breast cancer (van't Veer 2002; n=614; p=3378; 78.1 pct censored): time-normalised ESS of PIPs
- **Code/data:** not stated in text read (check supplement)
- *Source pages:* Sec 4 (p7); 4.1 Table 1 (p8); Tables 2-3 (p9); 4.2 Table 4 (p9); *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Biswas2022
Biswas N.; Mackey L.; Meng X.-L.; Scalable spike-and-slab; Proc. 39th ICML (PMLR 162); 2021-2040 (2022). **arXiv:2204.01668**

- **X:** iid-N(0,I) (columns scaled to mean 0 and sd 1); real-X (microarray; GWAS maize; PCR; lymph node; malware). X_ij iid N(0,1), column-standardised; no correlation structure in synthetic data
- **n:** 100 (Fig1 left; Fig 3); varying n<=p with p=1000 (Fig1 centre); n=10s (Fig1 right; p=100s for logistic study); n=1000 (50000-covariate runtime datasets); n=200 (Fig 6)
- **p (max):** 50000 (synthetic runtime datasets; n=1000); varying p>=n in Figs 1 and 3 (axes up to 1e4); real up to 98385 (Maize GWAS)
- **s0:** s=10 (Fig 1 left/centre); varying s>=1 (right); s=5 (Fig 3 binary); s=10 (Fig 6)
- **β / SNR:** Linear: beta*_j=2*1{j<=s}; sigma*=2; binary/logistic: beta*_j=2^{(9-j)/4}*1{j<=s} (exponentially decaying); y_i=1{ytilde_i>0}; ytilde~Logistic(x_i'beta;1)
- **Noise:** Gaussian sigma*=2 (linear); logistic/probit binary responses; **replicates:** 20 independently generated datasets with 1 s.e. error bars (Fig 3); 10 independent chains (Fig 6); one chain per dataset in Fig 1
- **Metrics:** TPR; FDR (from marginal posterior inclusion probs pi_j); per-iteration runtime; speed-up vs SOTA sampler; ESS (appendix for real data); coupling/mixing diagnostics (p_t)
- **Competitors:** S3 (proposed); SOTA exact Gibbs samplers (Bhattacharya 2016 style; Polson PG); Skinny Gibbs (Narisetty 2019)
- **Real data:** Gordon microarray (n=181;p=12533); Borovecki (n=31;p=22283); Chowdary (n=104;p=22283); Chin (n=118;p=22215); Malware (n=373;p=503); PCR GWAS mouse (n=60;p=22575; GSE3330); Lymph Node (n=148;p=4514; Hans 2007); Maize GWAS (n=2266;p=98385; Romay 2013)
- **Code/data:** code www.github.com/niloyb/ScaleSpikeSlab (R and Python)
- *Source pages:* Sec 2.3 Fig 1 (p~4); Sec 3 Figs 2-3 (p~6-7); Sec 4 Table 2 (p~7-8); Appendix D (dataset details) p~17-18; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Liang2022
Liang X.; Livingstone S.; Griffin J.; Adaptive random neighbourhood informed Markov chain Monte Carlo for high-dimensional Bayesian variable selection; Statistics and Computing; 32(5); article 84 (2022). **10.1007/s11222-022-10137-8 (arXiv:2110.11747)**

- **X:** AR1(rho=0.6); real-X (Tecator; Boston; concrete; protein; mouse PCR; mouse SNP). Yang-Wainwright-Jordan 2016 design: rows ~N(0,Sigma) Sigma_ij=0.6^|i-j|; prior V_gamma=I; g=9; h=10/p
- **n:** 500;1000
- **p (max):** 50000 (p grid 500;5000;50000) -> flag p>=1e4; real up to p=79748
- **s0:** 10
- **β / SNR:** beta*=SNR*beta_tilde*sqrt(sigma^2 log p/n); beta_tilde=(2,-3,2,2,-3,3,-2,3,-2,3,0,...); SNR=0.5;1;2;3
- **Noise:** Gaussian N(0,sigma^2 I); **replicates:** 24 simulated settings (4 SNR x 2 n x 3 p); each algorithm run repeatedly for 15 min wall-clock (exact repeat count not stated in main text)
- **Metrics:** MSE of PIP estimates vs gold-standard PIPs (from very long weighted tempered Gibbs sampler) relative to Add-Delete-Swap; trace plots of log posterior model probability; expected squared jumping distance; acceptance rate; run time
- **Competitors:** Add-Delete-Swap; ASI (Griffin 2021); PARNI-KW; PARNI-RM; weighted tempered Gibbs as gold standard
- **Real data:** 8 real datasets reused from Griffin 2021: Tecator (n=172,p=100); Boston (n=506,p=104); Concrete (n=1030,p=79); Protein (n=96,p=88); mouse PCR1-3 (n=60,p=22575 genes); mouse SNP (n=993,p=79748)
- **Code/data:** code https://github.com/XitongLiang/The-PARNI-scheme.git
- *Source pages:* Sec 5.1 (pp 15-16) Table 1; Sec 5.2 (pp 16-18) Tables 2-3; Supp C; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Zhou2022
Zhou Q.; Yang J.; Vats D.; Roberts G.O.; Rosenthal J.S.; Dimension-free mixing for high-dimensional Bayesian variable selection; J. R. Stat. Soc. B; 84(5); 1751-1784 (2022). **10.1111/rssb.12546 (arXiv:2105.05719)**

- **X:** iid-N(0,I) rows; AR1-type Toeplitz(rho=e^{-|j-k|}, i.e. rho=0.37 per step); block(size d=20, within-block Sigma_jk=e^{-|j-k|/3}). Study I follows Yang-Wainwright-Jordan 2016 design: rows iid MN(0,Sigma); Study II: block-diagonal Sigma_{d,p} with d=20 blocks, rho_|j-k|=exp(-|j-k|/3); real GWAS X (SNP genotypes)
- **n:** 500;1000 (n=500,p=1000 and n=1000,p=5000 in study I; n=1000,p=5000 in study II); GWAS n=5418
- **p (max):** 328129 (real GWAS); synthetic max p=5000; p grid 1e3;5e3;3.3e5(real)
- **s0:** 10 (study I; first 10 coords); 100 (study II; gamma* uniform among size-100 sets)
- **β / SNR:** Study I: beta*_[10]=SNR*sqrt(log p/n)*(2,-3,2,2,-3,3,-2,3,-2,3); SNR=1,2,3; study II: beta_gamma*~N(0,sigma_beta^2 I_100) with sigma_beta=0.1..0.5 (designed to induce multimodality; worst at 0.2)
- **Noise:** Gaussian z~N(0,I_n) (sigma=1); **replicates:** 100 data sets per setting (study I); 20 data sets per setting (study II); 5 independent runs (GWAS)
- **Metrics:** success of finding MAP model gamma_max; iterations H_max to hit gamma_max; wall time t_max; MSE of beta (Rao-Blackwellised); acceptance rate; number of local modes; ESS of T1=||beta_hat(gamma)-beta*||^2 and T2=||X beta||^2; ESS/time; PIP
- **Competitors:** RW-MH; LIT-MH-1; LIT-MH-2; LB-MH-1; LB-MH-2 (Zanella locally balanced)
- **Real data:** GWAS glaucoma CDR (dbGaP phs000308 GLAUGEN + phs000238 NEIGHBOR; n=5418; p=328129 SNPs): PIPs; top-10 signals; ESS(T2)/time
- **Code/data:** code http://web.stat.tamu.edu/~quan/code/lit_mh.tgz; GWAS data via dbGaP
- *Source pages:* Sec 5 (pp 20-25) incl. Table 1 (p22) Table 2 (p24); Sec 6 (pp 25-27) Table 3-4; supplement S4, S6; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Jankowiak2023
Jankowiak M.; Bayesian variable selection in a million dimensions; Proc. AISTATS 2023 (PMLR 206) (2023). **arXiv:2208.01180**

- **X:** real-X(synthetic beta) (maize SNP genotypes Romay 2013; plus appended iid N(0,1) covariates); binary/SNP-genotypes; other (two highly correlated covariates; Binomial responses); real-X+real-y (DepMap RNA expression; hospital data). Semi-synthetic: maize genotype matrix (N=2267; P=98385) -> for P>98385 append iid unit-Normal columns; response from 20 causal covariates chosen one from each of 20 blocks among pairs with |corr| in [0.5;0.9]
- **n:** 2267 (maize); 907 (DepMap); 100;907;4000 (runtime study); 32-512 (PG-wTGS toy); 1798 (hospital); 30 regions (viral)
- **p (max):** 750000 (P from 1.5e5 to 7.5e5 with Subset wTGS; maize base P=98385); flag p>=1e5 (no p=1e6 run in text; title refers to a million dimensions; wTGS full infeasible beyond; ASI not competitive); other: 17273 (DepMap); 69092 (runtime study); 3000 (viral)
- **s0:** 20 causal covariates (large-P semi-synthetic); 2 (correlated-pair Binomial toy); 3-10 causal mutations (viral P=3000)
- **β / SNR:** beta* drawn U([-1;-0.1] union [0.1;1]) for 20 non-zero; sigma0=0.5 (main) or 2.5 (supp Fig 6); viral effects U([-0.10;-0.02] union [0.02;0.10]); prior inclusion h; Beta(0.25;250) prior on h in viral expt
- **Noise:** Gaussian sigma0=0.5 or 2.5; Binomial (counts C_n=10) with Polya-Gamma; negative binomial (hospital data); **replicates:** 5 train/test splits (95% CIs across splits for P up to 7.5e5); 20 chains x 50k its vs 10 reference chains of 500k its (DepMap); 10 reference chains
- **Metrics:** relative statistical efficiency of PIP estimators (Subset wTGS vs wTGS); iterations per second; sensitivity and precision at PIP>0.5; held-out RMSE; runtime on NVIDIA T4 GPU for 50k samples (35 min at P=7.5e5); mean absolute PIP error in top hits; inferred inclusion prob h vs number of true causal mutations
- **Competitors:** wTGS; Subset wTGS (proposed; anchor set A); PG-wGS; PG-TGS; PG-wTGS; ASI (Griffin; Wan-Griffin for PG)
- **Real data:** maize SNP genotypes (Romay 2013; N=2267; P=98385; semi-synthetic response); DepMap CRISPR essentiality (N=907 cell lines; P=17273 gene expressions; DUSP4 and HNF1B knockouts binarised at 20% quantile); hospital length-of-stay (N=1798; 3 covariates + 97 noise); simulated SARS-CoV-2-like viral transmission (P=3000)
- **Code/data:** code https://github.com/BasisResearch/millipede (PyTorch; GPU)
- *Source pages:* Sec 7 (Sec 7.1-7.4; Figs 1-5); Supp A.16-A.17; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Liang2023
Liang X.; Livingstone S.; Griffin J.; Adaptive MCMC for Bayesian variable selection in generalised linear models and survival models; Entropy; 25(9); 1310 (2023). **10.3390/e25091310 (arXiv 2308.00869)**

- **X:** AR1(rho=0.6); binary/SNP-genotypes (SLE case/control GWAS); real-X+real-y (gene-expression survival data). Simulation (App D; Sec 5.1): rows N(0;Sigma) Sigma_ij=0.6^|i-j|; logistic data y~Bern(logit^-1(X beta)); survival times from generalised gamma with sigma=0.8; q=-2 (as in Griffin et al 2021); Cox PH and Weibull models fit; hyper-params sigma_alpha^2=100; g=1; h=10/500
- **n:** 500 (simulation; two datasets); 10995 (SLE; 4035 cases + 6959 controls); 272;1903;226;130 (survival sets)
- **p (max):** 500 (simulation); real: SLE chromosomes p=5771; 9306; 32290; 42430 (flag p>=1e4: chr 3 and 11); survival gene sets p=1554; 662; 54675 (GSE31210; p>=1e4); 22283 (GSE4573; p>=1e4)
- **s0:** 10 (beta=(2;-3;2;2;-3;3;-2;3;-2;3;0...0))
- **β / SNR:** beta_1..10 = (2;-3;2;2;-3;3;-2;3;-2;3); signal level only via these coefficients (no explicit SNR)
- **Noise:** Bernoulli (logistic); generalised-gamma survival with censoring details in App D / earlier papers; **replicates:** Sec 5.1: two simulated datasets (500 x 500) (logistic; Cox; Weibull) with trace plots; real data: 10 repetitions of 1 h runs for SLE; PIP gold standard = PARNI-CPM run for ~12 h
- **Metrics:** trace plot of log posterior model probability and CPU time (Sec 5.1); average MSE of PIP estimates over all p covariates relative to long-run gold standard (12 h PARNI-CPM); relative efficiency = ratio of average MSE vs baseline
- **Competitors:** PARNI-adaptiveALA; PARNI-LA; PARNI-ALA; add-delete-swap (ADS thinned; ADS-DA; ADS-CPM); PARNI-DA; PARNI-CPM
- **Real data:** SLE GWAS (4035 cases; 6959 controls; chromosomes 1;3;11;21 with 5771;42430;32290;9306 SNPs; 5 fixed covariates gender + PC1-PC4); NKI breast cancer survival (n=272; 1554 genes + 5 clinical); METABRIC (n=1903; 662 gene/mutation covariates); GSE31210 lung (n=226; p=54675); GSE4573 lung (n=130; p=22283); all used for PIP-MSE efficiency (Cox; Weibull)
- **Code/data:** https://github.com/XitongLiang/The-PARNI-scheme.git; real data public (NKI data.world; METABRIC cBioPortal; GEO GSE31210 and GSE4573; SLE data from earlier studies)
- *Source pages:* Sec 5.1 (p12-13; Fig 1); Sec 5.2 (p13-15; Tables 1-2); Sec 5.3 (p15-16; Tables 3-4); App D (p18); *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Staerk2024
Staerk C.; Kateri M.; Ntzoufras I.; A Metropolized adaptive subspace algorithm for high-dimensional Bayesian variable selection; Bayesian Analysis; 19(1); 261-291 (2024). **arXiv:2105.01039; DOI 10.1214/22-BA1351**

- **X:** AR1(rho=0.9 illustrative; rho=0.3;0.9;0.99 low-dim; rho=0.6 high-dim) (all called Toeplitz rho^|k-l|); real-X (Tecator; PCR mouse; Golub leukemia). Toeplitz Sigma_kl=rho^|k-l|; g-prior g=n (low-dim) and g=9 with omega=10/p (high-dim); EBIC gamma=1 for real PCR/leukemia
- **n:** 60 (illustrative and low-dim); 500;1000 (high-dim); real: 172;60;72
- **p (max):** 5000 (high-dim; p grid 500;5000); real PCR p=22575; Golub p=3571 (after preprocessing; 6817 raw)
- **s0:** 5 (illustrative: S0={1..5}); random s0 in {0..10} (low-dim); 10 (high-dim)
- **β / SNR:** Illustrative: beta0=(0.4;0.8;1.2;1.6;2.0;0...); low-dim: active set random; beta_j~U(-2,2); high-dim: Yang-Wainwright-Jordan beta0=SNR*sqrt(log p/n)*(2;-3;2;2;-3;3;-2;3;-2;3;0...) with SNR=0.5;1;2;3; sigma=1
- **Noise:** Gaussian sigma^2=1; **replicates:** Low-dim: 200 datasets per setting; high-dim: 1 dataset per setting with 200 algorithm runs; real: 25 independent chains each
- **Metrics:** time-standardised relative ESS of PIP r_A,B vs add-delete-swap MC3 (variance of PIP estimates across runs); acceptance rate; PIP stability across chains; proposal-probability convergence; MSE of PIPs; run time
- **Competitors:** MAdaSub serial; MAdaSub parallel; add-delete-swap MC3; ASI/AdaptMC (Griffin 2021); locally informed sampler (Zanella); Hamming ball
- **Real data:** Tecator (n=172;p=100); PCR mouse gene expression (Lan 2006; n=60;p=22575; JRSSB datasets of Song-Liang 2015); Golub leukemia (n=72;p=3571 after Dudoit preprocessing; logistic regression)
- **Code/data:** code https://github.com/chstaerk/MAdaSub
- *Source pages:* Sec 5.1 (pp 14-15); 5.2 (p18-19); 5.3 (p20-21) Table 1; Sec 6.1-6.2 (pp22-28); *read level:* full-text; *scout file:* `S1_BVS.tsv`


## BVS-prior

### Ishwaran2005
Ishwaran H.; Rao J.S.; Spike and slab variable selection: frequentist and Bayesian strategies; Annals of Statistics; 33(2); 730-773 (2005). **arXiv:math/0505633; DOI 10.1214/009053604000001147**

- **X:** AR1(rho=0 and rho=0.9) (Breiman 1992 recipe; E x_j x_k = rho^|j-k|); real-X+real-y (diabetes). Breiman simulations: x_i ~ N(0,Sigma) Sigma_jk=rho^|j-k|; rho in {0;0.90}; configs (A) n=200;K=100 (B) n=800;K=400
- **n:** 200;800 (442 in diabetes)
- **p (max):** 400 (K; p grid 100;400); diabetes quadratic model p=64
- **s0:** (A) 45 nonzero (9 clusters of 5 adjacent variables at every 10th variable); (B) 105 nonzero (15 clusters of 7 adjacent variables centred at every 25th variable; 295 zero)
- **β / SNR:** (B) beta_{25+j}=|h-j|^1.25 for |j|<h; h=4; (A) all 45 nonzero set equal; coefficients rescaled by common constant so theoretical R^2=0.75; eps~N(0;1)
- **Noise:** Gaussian N(0;1); **replicates:** 100 independent replications for each of the 4 experiments
- **Metrics:** TotalMiss (total misclassified variables); FDR; FNR; k_hat (average selected size); Perf = 1 - ||X beta_hat - X beta0||^2/||X beta0||^2
- **Competitors:** Zcut (rescaled spike-and-slab; alpha=0.10); svsForwd; OLS-hard; OLSForwd
- **Real data:** Diabetes (Efron-Hastie-Johnstone-Tibshirani 2004; n=442; quadratic model p=64: 10 baseline + 45 interactions + 9 squares); top-10 variables by posterior mean; Z-statistic table
- **Code/data:** no code reference found in text
- *Source pages:* Sec 8 (pp 31-34) Table 2; Sec 7 (pp 29-31) Table 1; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Liang2008
Liang F.; Paulo R.; Molina G.; Clyde M.A.; Berger J.O.; Mixtures of g priors for Bayesian variable selection; J. Amer. Statist. Assoc.; 103(481); 410-423 (2008). **10.1198/016214507000001337**

- **X:** orthogonal (X'X = I_p as in Cui-George 2007; extracted text garbled "XrX = lp" - read as identity); real-X+real-y (crime data; ozone data). Simulation: Y = 1_n*alpha + X*beta + eps; alpha=2; X'X=I_p so all 2^15 models enumerable (no MCMC); crime data 15 predictors (2^15=36768 models); ozone 8 meteorological variables + interactions + squares = 44 predictors (stochastic search with BAS)
- **n:** 100 (simulation); 47 (crime); 330 (ozone; 165 train/165 validation by random 50/50 split)
- **p (max):** 15 (simulation; deliberately small for enumeration); 44 (ozone)
- **s0:** p_gamma = 0..15 (all true model sizes); ozone n/a
- **β / SNR:** beta_gamma ~ N(0; g/(p_gamma) ... as printed 'N(0; g/(p) I)' garbled; g=5 (weak signal) and g=25 (strong signal) following Cui-George 2007; remaining coefficients 0
- **Noise:** Gaussian sigma^2=1; **replicates:** 1000 per (g; p_gamma) setting
- **Metrics:** MSE(m)=||X beta - X beta_hat(m)||^2 (average over reps; oracle MSE p_gamma+1; full p+1); marginal inclusion probabilities (crime); out-of-sample RMSE with HPM/MPM/BMA (ozone)
- **Competitors:** Oracle OLS; full OLS; BIC; AIC; BRIC (g=max(n;p^2)); EB-local; EB-global; Zellner-Siow null-based (ZS-N) and full-based (ZS-F); hyper-g (a=3; also a=4) with uniform model prior; HPM vs MPM vs BMA
- **Real data:** Crime data of Vandaele 1978 (n=47; p=15; Raftery et al 1997; Fernandez et al 2001): posterior inclusion probabilities under 10 priors; Ground-level ozone (Breiman-Friedman 1985; n=330; p=44 with interactions and squares): out-of-sample RMSE
- **Code/data:** R package BAS (CRAN); data from Vandaele 1978 and Breiman-Friedman 1985; no replication code in text
- *Source pages:* Sec 5 (p. 418; Table 1 p. 418; Fig 1); Sec 6.1-6.2 (pp. 418-420; Tables 2-3); App C describes ozone variables; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Scott2010
Scott J.G.; Berger J.O.; Bayes and empirical-Bayes multiplicity adjustment in the variable-selection problem; Annals of Statistics; 38(5); 2587-2619 (2010). **arXiv:1011.2333; DOI 10.1214/10-AOS792**

- **X:** iid-N(0,I). Table 1: m=100 design of iid N(0,1) covariates (m = number of covariates here); first 1, 10, 40, 90 noise variables added to 10 real ones (m=11;20;50;100); Sec 6: random m x n design iid N(0,1); true gamma drawn Bernoulli(p) with p~U(0,1); beta_gamma from Zellner-Siow prior; Zellner-Siow marginal likelihoods; model space enumerated for m<=20 else feature-inclusion stochastic search (5 million iterations)
- **n:** n not stated for Table 1 data (sample size not found in lines read); Sec 6.1: n=16;30;60;120 (m=14 covariates); real: n=30 countries (m=22)
- **p (max):** 100 (m, number of covariates; Table 1: 11;20;50;100); m=14 in enumerated simulation study (2^14=16384 models); real m=22
- **s0:** 10 (Table 1); random (Sec 6; |gamma| ~ Binomial(14;p))
- **β / SNR:** Table 1: 10 real regression coefficients non-zero; remaining zero (values not given in lines read); Sec 6: beta drawn from Zellner-Siow prior; Y~N(X beta; I) (unit variance)
- **Noise:** Gaussian sigma^2=1; **replicates:** 75000 simulated data sets for each of 4 sample sizes (Sec 6.1); 75000 for each of 3 non-uniform p priors (Sec 6.2); one data set for Table 1
- **Metrics:** posterior inclusion probabilities (x100); number of false positives (PIP>0.5); distribution of EB estimate p-hat (collapse to 0 or 1 fraction); EB vs FB PIP differences
- **Competitors:** Uncorrected (p=1/2 prior); fully Bayes (uniform prior on p); oracle Bayes; empirical Bayes (maximum marginal likelihood p-hat)
- **Real data:** GDP growth regression (Sala-i-Martin-Doppelhofer-Miller 2004 subset; n=30 countries; 22 covariates = top 10 BACE + 12 random; exact enumeration); also Sec 6.5 other example not read
- **Code/data:** no code reference found in text
- *Source pages:* Sec 3 Table 1 (p9); Sec 6.1-6.2 (pp 22-24) Figs 3-5; Sec 6.4 Table 3; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Johnson2012
Johnson V.E.; Rossell D.; Bayesian model selection in high-dimensional settings; J. Amer. Statist. Assoc.; 107(498); 649-660 (2012). **10.1080/01621459.2012.682536**

- **X:** iid-N(0,I); equicorr(rho=0.25). X=Z C^{1/2}; Z iid N(0,1); C has unit diagonal and constant off-diagonal rho in {0;0.25}; rho chosen from microarray GSE5206 and GSE2109 mean absolute gene correlations 0.16-0.18; max sample correlation exceeds 0.5 (p=100) and 0.4 (p=500); columns variance 1; beta-binomial model prior (Scott-Berger) with zeta0=zeta1=1
- **n:** 10 to 500 (p=n)
- **p (max):** 500 (p=n grid up to 500; so p/n=1 only)
- **s0:** 5
- **β / SNR:** beta_t = (0.6;1.2;1.8;2.4;3.0) rest 0 (design reused by Narisetty-He 2014); sigma^2=1.0;1.5;2.0
- **Noise:** Gaussian sigma^2 in {1.0;1.5;2.0}; **replicates:** SCAD and LASSO: 10000 simulated datasets; Bayesian nonlocal priors and BIC: 1000 datasets; intrinsic prior: 500 datasets; MCMC 500 burn-in + 5000 updates each
- **Metrics:** average posterior probability p(t|y) of true model vs n; probability P(t_hat = t) of selecting exactly the true model (posterior mode vs SCAD/LASSO support); out-of-sample prediction RMSE; total-variation coupling diagnostics (Johnson 1996/1998)
- **Competitors:** pMOM (r=1;2); piMOM; intrinsic prior (Casella 2009); BIC; SCAD (ncvreg); LASSO (parcor; 10-fold CV)
- **Real data:** No real data analysis in main text (abstract and Sec 4 simulation only; Sec 5 Discussion)
- **Code/data:** R package mombf; R code in article supplement
- *Source pages:* Sec 4 (pp 653-656) Figs 2-4; JASA pagination; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Zhou2013
Zhou X; Carbonetto P; Stephens M. Polygenic modeling with Bayesian sparse linear mixed models. PLoS Genet 9(2) e1003264 (2013). **10.1371/journal.pgen.1003264**

- **X:** real-X(synthetic beta); real-X+real-y; binary/SNP-genotypes. Real genotypes: about 300,000 SNPs in 3,925 Australian individuals (height cohort); causal SNPs are included among the typed SNPs (so true PVE of typed markers known). Real LD
- **n:** 3925 (sim and height); 1868 (lipids); ~14000 cases + ~3000 controls (WTCCC); HS mice (n and p numbers lost in HTML text)
- **p (max):** ~3e5 (sim); ~5.5e5 (lipids); ~4.5e5 (WTCCC)
- **s0:** Scenario I: 10;100;1000;10000 causal SNPs; Scenario II: 10 or 100 moderate/medium-effect SNPs plus 10000 small-effect polygenic SNPs
- **β / SNR:** Scenario I: effects ~ N(0,1) for S causal SNPs; Scenario II: two groups (small number of moderate effect plus 10000 small effects); Gaussian errors to give true PVE=0.2 or 0.6
- **Noise:** Gaussian; **replicates:** 20 per setting; WTCCC 20 random 80/20 splits per disease; mouse 40 splits (20 intra-family 20 inter-family)
- **Metrics:** RMSE of PVE estimates; relative prediction gain (RPG); correlation; AUC and Brier score (WTCCC); RMSE (mouse); computation time (Table 4; 2.1M MCMC iterations)
- **Competitors:** LMM (GCTA-like); BVSR; for mouse also LMM-Bayes; Bayesian Lasso (BLR); BayesA-Flex; BayesC (GenSel); BSLMM-EB
- **Real data:** Height 3925 x ~300K SNPs; lipids HDL LDL TC TG 1868 x ~550K SNPs (PARC); WTCCC1 seven diseases ~450K SNPs; heterogeneous stock mice (Valdar 2006) CD8 MCH BMI and binary traits
- **Code/data:** GEMMA (stephenslab.uchicago.edu/software.html; github genetics-statistics/GEMMA); WTCCC via application; HS mice public
- *Source pages:* Results sections: Simulations PVE Estimation; Simulations Phenotype Prediction; WTCCC; HS mice; Tables 3-4; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Narisetty2014
Narisetty N.N.; He X.; Bayesian variable selection with shrinking and diffusing priors; Annals of Statistics; 42(2); 789-817 (2014). **arXiv:1405.6545; DOI 10.1214/14-AOS1207**

- **X:** equicorr(rho=0.25); block(active-active rho1=0.25; inactive-inactive rho3=0.75; active-inactive rho2=0.5); Wishart-centred-at-I covariance (Bondell-Reich 2012); real-X+real-y (mouse PCR). Cases 1-5: unit variance; compound symmetry rho=0.25; case 4 block-type structure; case 6: covariance drawn from Wishart centred at identity with p d.f.; BASAD tuning tau0n^2=sigma_hat^2/(10n); tau1n^2=sigma_hat^2 max(p_n^2.1/(100n); log n); K=max(10;log n)
- **n:** 100;200 (p=n cases; n,p) = (100,100);(200,200);(100,500);(200,1000);(100,50);(200,50)
- **p (max):** 1000 (n,p)=(200,1000); p grid 50;100;200;500;1000; real: screened to p=200 and 400 from 22575
- **s0:** 5 (cases 1-4); 25 (case 5); 3 (case 6)
- **β / SNR:** Case 1-2: beta_t=(0.6;1.2;1.8;2.4;3.0); case 3: all 0.6 (low signal); case 5: 25 equally spaced values between 1 and 3; case 6: three active coefficients ~U(0;3); sigma not stated in sections read
- **Noise:** Gaussian; **replicates:** 500 data sets per model when n>=p; 200 when p>n
- **Metrics:** pp0 and pp1 (avg posterior probs of inactive/active); exact model recovery proportion Z=t; proportion Z contains t; FDR; MSPE on n new test observations
- **Competitors:** BASAD (proposed; median probability model); BASAD.BIC; piMOM (Johnson-Rossell 2012; p<=n only); BCR.Joint (Bondell-Reich 2012); SpikeSlab (Ishwaran-Rao 2005); Lasso.BIC; EN.BIC; SCAD.BIC
- **Real data:** Mouse PCR (Lan et al 2006; n=60 arrays; p=22575 genes; GSE3330); screened by marginal correlation to p=200 and 400; responses PEPCK and GPAT; 100 random 55/5 train-test splits; MSPE
- **Code/data:** R function on authors website (BASAD); GEO GSE3330
- *Source pages:* Sec 8 (pp 17-22) Tables 1-6; Sec 9 (pp 25-26) Fig 1; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Moser2015
Moser G; Lee SH; Hayes BJ; Goddard ME; Wray NR; Visscher PM. Simultaneous discovery, estimation and prediction analysis of complex traits using a Bayesian mixture model. PLoS Genet 11(4) e1004969 (2015). **10.1371/journal.pgen.1004969**

- **X:** real-X(synthetic beta); iid-uncorrelated SNPs (supplement); binary/SNP-genotypes. Main: real genotypes 287,854 SNPs on 3,924 individuals (height cohort); supplementary: simulated 20,000 uncorrelated SNPs x 5,000 individuals. Columns centred and scaled to unit variance
- **n:** 3924 (real-genotype sim); 5000 (uncorrelated sim); WTCCC cases and 3000 controls
- **p (max):** 287,854 (real-genotype sim); 2e4 (uncorrelated sim)
- **s0:** 3,000 causal in 3 groups: 10 moderate (variance 1e-2); 310 small (1e-3); 2,680 polygenic (1e-4); uncorrelated sim: 10;100;1000;10000;20000 effects (normal or gamma shape 0.44 scale 1.66)
- **β / SNR:** effects ~ N(0, 1e-2;1e-3;1e-4 by group); h2 = 0.2;0.5;0.8 (0.5 in uncorrelated sims); BayesR prior mixture matches the simulation
- **Noise:** Gaussian; **replicates:** 50 replicates per case (boxplots); 20 random 80/20 splits per WTCCC trait
- **Metrics:** TPR vs FPR for identification of 250kb regions containing causal SNPs; SNP-heritability estimate bias/SD; prediction correlation (80/20 split); variance partition by mixture component; runtime
- **Competitors:** BSLMM (GEMMA); LMM; GPRS (genomic profile risk score); single-SNP GWAS
- **Real data:** WTCCC1 seven diseases (BD CAD CD HT RA T1D T2D) with shared controls; estimated h2 on liability scale and prediction AUC
- **Code/data:** BayesR Fortran software (cnsgenomics.com/software); WTCCC via application; chain length 50,000 with 20,000 burn-in
- *Source pages:* Results: Simulated Data using Real Genotypes (Figs 1-3); Methods Implementation; S-figures for uncorrelated sims; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Bhattacharya2016
Bhattacharya A.; Chakraborty A.; Mallick B.K.; Fast sampling with Gaussian scale mixture priors in high-dimensional regression; Biometrika; 103(4); 985-991 (2016). **10.1093/biomet/asw042 (arXiv:1506.04778)**

- **X:** iid-N(0,I); equicorr(rho=0.5); Toeplitz(rho=0.9; |j-j'|). Rows x_i iid N_p(0;Sigma): (i) Sigma=I_p; (ii) compound symmetry Sigma_jj'=0.5; coverage study also Toeplitz Sigma_jj'=0.9^|j-j'|; the sampler is a horseshoe (global-local shrinkage; not spike-and-slab) Gibbs sampler
- **n:** 200 (n=200 in estimation study; coverage study 'similar scenario')
- **p (max):** 5000 (p grid 2500;5000 estimation; 500;1000 coverage); timing: sampler compared at p=500 and p=5000 with n=100 (speed-up factor >250 at p=5000)
- **s0:** 5
- **β / SNR:** Non-zero beta in two strengths: (a) +/-{1.5;1.75;2;2.25;2.5} (b) +/-{0.75;1;1.25;1.5;1.75} with random signs; sigma=1.5
- **Noise:** Gaussian sigma=1.5; **replicates:** 100 simulation replicates per setting (24 settings in total)
- **Metrics:** l1 error ||bhat-beta0||_1; l2 error; prediction error ||X bhat - X beta0||_2; frequentist coverage and length of 95% credible/confidence intervals (signal vs noise coordinates); sampler run time (6000 Gibbs iterations)
- **Competitors:** Horseshoe prior (posterior mean and median) with fast sampler vs SCAD; MCP (ncvreg 10-fold CV); debiased-lasso intervals (van de Geer 2014; Javanmard-Montanari 2014)
- **Real data:** none (simulation only)
- **Code/data:** MATLAB code https://github.com/antik015/Fast-Sampling-of-Gaussian-Posteriors.git
- *Source pages:* Sec 2 (p4-5); Sec 3 (pp 5-8) Figs 1-2 Table 1; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Papaspiliopoulos2017
Papaspiliopoulos O.; Rossell D.; Bayesian block-diagonal variable selection and model averaging (arXiv title: Scalable Bayesian variable selection and model averaging under block orthogonal design); Biometrika; 104(2); 343-359 (2017). **10.1093/biomet/asx019 (arXiv:1606.03749)**

- **X:** orthogonal design; block(size 10; rho=0.5 within block); block(rho=0.9 within block); AR1(rho=0.9); equicorr(rho=0.5); real-X+real-y (TGFB colon cancer). Sec 5.3: columns normalised x_j'x_j/n=1; blocks of 10; within-block correlation 0.5; Sec 5.5 (n=100;p=500): compound symmetric sigma_ij=0.5; AR sigma_ij=0.9^|i-j|; block sigma_ij=0.9 same block; Zellner and product-moment priors; prior p(gamma_j=1)=1/p
- **n:** 100;150;510;262 (real)
- **p (max):** 500 (p grid 100;500)
- **s0:** 5 (beta_8=0.5,beta_9=0.75,beta_10=1 in block 1; beta_19=0.75,beta_20=-1 in block 2)
- **β / SNR:** fixed coefficients beta_8=0.5; beta_9=0.75; beta_10=1; beta_19=0.75; beta_20=-1; phi=1 (sigma^2=1); same beta in Sec 5.5
- **Noise:** Gaussian sigma^2=phi=1; **replicates:** 1 dataset for Sec 5.3 illustrations; 1000 independent datasets per covariance structure in Sec 5.5
- **Metrics:** posterior mode and model probabilities; proportion of sims where block-search mode has posterior prob >= Gibbs mode or >= truth; runtime
- **Competitors:** Coolblock block search vs Gibbs (mombf modelSelection)
- **Real data:** TGFB colon cancer gene expression (n=262; 10 genes selected for TGFB response; subgroup analysis by cancer stage; Calon 2012)
- **Code/data:** R package mombf; R code in Supplement to the article
- *Source pages:* Sec 5.1-5.5 (pp 14-17) Table 1; Supp. Figs; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Zhu2017
Zhu X; Stephens M. Bayesian large-scale multiple regression with summary statistics from genome-wide association studies. Ann Appl Stat 11(3) 1561-1592 (2017). **10.1214/17-AOAS1046**

- **X:** real-X(synthetic beta); binary/SNP-genotypes. WTCCC 1458 UK Blood Service Control Group individuals; 12,758 SNPs on chromosome 16; IL27 region test with 982 SNPs (+-5Mb) and a 1480-individual WTCCC 1958 Birth Cohort as LD reference (sample LD vs shrinkage estimate of R)
- **n:** 1458
- **p (max):** 12,758 (chr16); 982 (IL27 region); real height GWAS summary data: ~1.06 million SNPs, N=253,288
- **s0:** 50 causal (PVE scenarios 1.1-1.2); T=10;100;1000 causal (scenarios 2.1-2.2; plus 10,000 small effects); 10 causal (IL27 region)
- **β / SNR:** effects N(0,1); polygenic small effects N(0,0.001^2); true PVE 0.05-0.5 step 0.05 (scen 1); PVE 0.2 and 0.6 (scen 2); PVE 0.2 (0.02;0.002 in supp) for IL27 region
- **Noise:** Gaussian; **replicates:** 50 per PVE (scen 1); 20 per parameter combination (scen 2); 20 datasets for IL27 region
- **Metrics:** PVE estimation bias and relative RMSE; agreement of 200-kb region expected number of included SNPs (sum of PIPs) between RSS-BVSR and GEMMA-BVSR; TP vs FP trade-off; runtime (Suppl Fig 5)
- **Competitors:** GEMMA-BVSR; GEMMA-BSLMM (full-data); RSS-P (sample LD) vs RSS (shrinkage LD)
- **Real data:** Adult height GWAS summary statistics (Wood et al 2014; GIANT; 253,288 individuals; ~1.06 million SNPs) analysed genome-wide: 1,064,575 SNPs retained after QC; LD from 379 European 1000G individuals; run per chromosome (22 in parallel) with 2 million MCMC iterations; CPU 1-36 h per chromosome (RSS-BVSR); total autosomal PVE 52.4 percent
- **Code/data:** https://github.com/stephenslab/rss
- *Source pages:* Sec 4 Simulations (4.1-4.3, Figures 1-4, Table 1); Sec 6 height analysis; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Rockova2018
Rockova V.; George E.I.; The spike-and-slab LASSO; J. Amer. Statist. Assoc.; 113(521); 431-444 (2018). **10.1080/01621459.2016.1260469**

- **X:** equicorrelated Gaussian (rho=0.6 off-diagonal; unit variance). Only one simulated example (Sec 5.1): X drawn from multivariate Gaussian mean 0_p with Sigma_ij=0.6 for i!=j and Sigma_ii=1; columns treated as centered and standardized with ||X_j||^2=n (Sec 1); Y centered (no intercept); no real-data section in this manuscript. Settings: slab penalty lambda1=0.1; theta updated every M=10 coordinates; spike ladder lambda0 in {lambda1+5k: k=1..10}; NSCA variant; start beta*=0_p; adaptive prior theta~Beta(1,p)
- **n:** 100
- **p (max):** 1000
- **s0:** 8 (q=8 nonzero coefficients placed at 8 random directions/coordinates)
- **β / SNR:** beta0 nonzero values (1/sqrt(3))*{-2.5; -2; -1.5; -1; 1; 1.5; 2; 2.5} assigned to q=8 random directions (4 negative; 4 positive); all other coefficients 0; no SNR or R^2 convention stated
- **Noise:** eps ~ N_n(0; I) with known variance sigma^2=1 (Sec 1 model 1.1); **replicates:** one data set ('this dataset'); no replicates stated
- **Metrics:** Qualitative: solution paths in lambda0 (Fig 2; Fig 3) coloured by true/false discoveries; counts of false positives/negatives read off the path (oracle theta=8/1000: no false positives and two false negatives; MCP-CV best solution: 6 coefficients identified correctly with one false positive and slightly increased bias); no formal numeric metric table
- **Competitors:** SSL with non-adaptive theta=0.5 (over-estimates nonzero fraction); SSL with oracle theta=8/1000; adaptive NSSL theta~B(1,p); EMVS implementation noted as giving very similar paths; SparseNet (Mazumder et al. 2011) with MCP penalty using cross-validation over a (lambda,gamma) grid (best gamma=4.185; also gamma approx 1 and 8.562 shown)
- **Real data:** none (no real-data analysis in this manuscript)
- **Code/data:** not stated
- *Source pages:* Sec 1 model (1.1) (p3); Sec 3.2 calibration remark referring to the simulated example (p16); Sec 5 path-following (pp19-20); Sec 5.1 'Spike-and-Slab LASSO in Action' with Figs 2-3 (pp21-22); Sec 7 discussion (pp29-30); page numbers are those of the author-manuscript PDF; Secs 6 and 8 theory/proofs checked for further simulation (none found); *read level:* full-text; *scout file:* `S4_LOCAL.tsv`

### Shin2018
Shin M.; Bhattacharya A.; Johnson V.E.; Scalable Bayesian variable selection using nonlocal prior densities in ultrahigh-dimensional settings; Statistica Sinica; 28(2); 1053-1078 (2018). **arXiv:1507.07106; DOI 10.5705/ss.202016.0167**

- **X:** equicorr(rho=0.5); AR1(rho=0.5); iid-N(0,I); real-X+real-y (mouse PCR; Boston + 1000 noise columns). Case 1 compound symmetry Sigma_jj'=0.5; Case 2 Sigma_jj'=0.5^|j-j'|; Case 3 Sigma=I; covariates standardised; uniform model prior; piMoM r=1; tau_{n,p}=log n log p in timing study
- **n:** 400 (n=400 PR curves); 150-400 (Fig 3); 200 (S5 vs SSS timing); 60 (PCR); 506 (Boston)
- **p (max):** 20000 (PR curves p=10000 and 20000; Fig 3 p=20000; S5 timing p up to 2000+); flag p>=1e4
- **s0:** 5
- **β / SNR:** t={1,2,3,4,5}; beta0=(0.50;0.75;1.00;1.25;1.50) with random signs (prob 1/2); sigma=1.5
- **Noise:** Gaussian sigma=1.5; **replicates:** 100 independent replicates per setting (PR); 100 simulated datasets (S5 vs SSS timing); 100 random splits (PCR)
- **Metrics:** precision-recall curves (area under PR curve; MAP model); posterior probability of the true model vs n; number of models with posterior odds >0.001 relative to MAP; computation time and number of models visited before MAP; MSPE; selected model size; MS-O/MS-N (mean model size of original/noise vars); FS-O; TS-O
- **Competitors:** peMoM and piMoM nonlocal priors (S5 algorithm); Zellner g-prior; Lasso; adaptive Lasso; SCAD; MCP; reduced reciprocal lasso; BASAD excluded (too slow); SSS
- **Real data:** Mouse PCR (Lan 2006; n=60; p=22575 genes; SCD1 response; 55/5 train-test splits repeated 100 times; MSPE); Boston housing (n=506; 10 continuous predictors + 1000 N(0,1) noise variables -> p=1010; simulation test size 100)
- **Code/data:** R package BayesS5 on CRAN
- *Source pages:* Sec 3.1 (pp 7-9) Fig 2; Sec 3.2 (p10) Fig 3; Sec 7.3 (p22) Fig 4; Sec 8.1-8.2 (pp 22-26) Tables 2-3; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### LloydJones2019
Lloyd-Jones LR; Zeng J; Sidorenko J; Yengo L; Moser G; Kemper KE; et al. Improved polygenic prediction by Bayesian multiple regression on summary statistics. Nat Commun 10 5086 (2019). **10.1038/s41467-019-12653-0**

- **X:** real-X(synthetic beta); binary/SNP-genotypes. UK Biobank: 348,580 unrelated Europeans; genome-wide sim uses 1,094,841 HapMap3 variants (from 1,365,446 HM3 SNPs filtered MAF>0.01; strand ambiguous removed; long-range LD incl MHC removed) and a random subset of 100,000 individuals; two independent 10,000-individual tuning and validation sets; preliminary sim on chr21+22 with 100,000 individuals; LD matrix shrinkage using 1000G genetic map
- **n:** 100,000 (genome-wide sims); 348,580 (real-data 5-fold CV; trait-specific n 27K-347K)
- **p (max):** 1,094,841 (individual-level BayesR run at this p with n=100,000); real data 1.1M HM3 variants
- **s0:** 10,000 causal (2500;5000;2500 from N(0,0.01 s2);N(0,0.1 s2);N(0,s2) = BayesR 4-component mixture) or 50,000 causal ~N(0,1); redrawn each replicate
- **β / SNR:** h2=0.1;0.2;0.5 (residual variance scaled; GCTA simulate); case-control via liability threshold prevalence 0.05 with h2=0.2 or 0.5
- **Noise:** Gaussian / liability threshold; **replicates:** 10 per scenario (8 scenarios)
- **Metrics:** prediction R2 / AUC in 10,000 validation set; calibration slope; h2_SNP estimation bias; CPU time (SBayesR 2-4 h; 44GB) and memory; MCMC chain length (10,000 iters SBayesR/BayesR; 2 million for RSS)
- **Competitors:** BayesR (individual-level); RSS; LDpred (tuned) and LDpred-inf; SBLUP; P+T; for h2: LDSC; HEreg; S-PCGC
- **Real data:** UK Biobank 12 traits 5-fold CV (HEIGHT n=347,106; BMI 346,738; T2D 274,271; etc); external GWAS meta-analysis (n~700,000 height and BMI) predicting into two independent data sets
- **Code/data:** GCTB software (cnsgenomics.com/software/gctb); UKB by application
- *Source pages:* Results: Genome-wide simulation study; Real data 5-fold CV; Methods; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Johndrow2020
Johndrow J.; Orenstein P.; Bhattacharya A.; Scalable approximate MCMC algorithms for the horseshoe prior; Journal of Machine Learning Research; 21(73); 1-61 (2020). **arXiv:1705.00841 (earlier preprint version; JMLR page lists no DOI)**

- **X:** iid-N(0,I);AR1(rho=0.9). w_i ~ N_p(0;Sigma); Sigma=I or Sigma_ij=0.9^|i-j| (text also says stationary variance 1/(1-phi^2): ambiguous); no column scaling stated; Sigma not stated for several runs (Figs 1;3;5;6;S3;S4)
- **n:** 1000-5000 random (Sec 5.3;Fig S2); 5000 at largest; also 200-2000 (N-sweep at p=20000); 2000 (Fig 1); 1000 (Sec 4.2); 200-1000 (Secs 5.2;6); real data 2267
- **p (max):** 5e4 nominal (N=5000;p=50000; Fig S4); largest realised random p=47985; grid not fixed: 5e3;1e4;2e4;5e4; real data p=98385
- **s0:** 23
- **β / SNR:** beta_j=2^((9-j)/4) for j=1..23 (4 down to 0.088; all positive; first 23 positions) else 0; sigma=2; R^2 ~0.93 for Sigma=I (my computation; paper reports no SNR/R2)
- **Noise:** Gaussian sigma^2=4 (sigma=2); **replicates:** 20 random (N;p) data sets per setting (Secs 5.2;5.3;6;Fig S2); 10 per N in MSE-vs-N sweep (Fig 6); single data set for Figs 1;2;3;S3;S4
- **Metrics:** MSE of beta (posterior time average); coverage of 95% credible intervals; sigma coverage; ESS and ESS/s (mcmcse OBM n^(1/3)); ACF of log xi; wall-clock and log t on log N+log p regression; KS and correlation of means/variances exact vs approx; TV/W2 approximation bounds; no TPR/FDR/PIP
- **Competitors:** own exact 'new' sampler; own 'old' (Polson-Scott-Windle 2014 + Bhattacharya 2016); approximate sampler (delta=1e-4); Lasso (10-fold CV; maize only)
- **Real data:** maize GWAS USDA Ames inbred lines (n=2267; p=98385 SNPs; response growing degree days to silking): ESS/s and posterior marginals vs Lasso; no prediction or selection scoring
- **Code/data:** no code or data URL in paper or JMLR page; hardware: multicore 12 threads (Sec 5.2); maize data shared by Liu and Zhou (not linked)
- *Source pages:* pp.9-10 (Figs 1-2); p.19 eq 21; pp.19-20 (Fig 3;Table 1); pp.20-24 (Tables 2-4;Fig 4); pp.24-26 (Figs 5-6); pp.25-27 (Figs 7-9); pp.x-xii (Figs S2-S4); *read level:* full-text; *scout file:* `S0_19-536.tsv`

### Rossell2021
Rossell D.; Abril O.; Bhattacharya A.; Approximate Laplace approximations for scalable model selection; J. R. Stat. Soc. Ser. B; 83(4); 853-879 (2021). **10.1111/rssb.12466 (arXiv 2012.07429)**

- **X:** equicorr(rho=0.5); iid-N(0,I); random correlation matrix (V = corr(W'W); W iid N(0;1)); real-X+real-y (poverty CPS data; colon cancer). 5.1: logistic and Poisson regression z_i~N(0;Sigma) Sigma_ii=1 Sigma_ij=0.5 with beta*=(0;...;0;0.5;1); 5.2.1: z_i~N(0;I) or N(0;V) with beta*=(0.4;0.6;1.2;0.8;0;...;0); 5.2.2: non-linear y=sin(-x1+.1)+sin(2.5 x2)+eps with 5 or 50 covariates equicorrelated 0.5 expanded with 5-dim cubic splines (J=10 or 100 groups; p=30 or 300); group priors; models explored by augmented Gibbs (mombf) when >1e6 models
- **n:** 100;500;1000;5000 (p=10 fixed); 500 (p=5;10;25;50); 50;200;500 (5.2.1); n not extracted for 5.2.2 (see Fig 4); real poverty n=89755; colon n=260
- **p (max):** 300 (non-linear; J=100 groups); 50 (logistic/Poisson grid 5;10;25;50); real poverty p=1469 with interactions (p=60 main effects); colon p=175; no p>=1e4
- **s0:** 2 (logistic/Poisson; beta*=(0..0;0.5;1)); 4 (5.2.1); 2 truly active covariates (5.2.2)
- **β / SNR:** as listed (beta values fixed; no SNR)
- **Noise:** 5.2.2: Gaussian N(0;1); logistic/Poisson responses; AFT log-normal in 5.4; **replicates:** 150 simulations in 5.2.2 (Fig 4); other settings not stated in text read
- **Metrics:** CPU time; proportion of correct model selection (5.2.2); posterior inclusion probability accuracy vs LA; correlation of posterior model probabilities (ALA vs LA)
- **Competitors:** Laplace approximation (LA); ALA (default and 1-2 Newton steps); exact g-Zellner; group LASSO; group SCAD; group MCP
- **Real data:** Poverty line (CPS 2010/2019; n=89755; p=60 main effects; p=1469 with all pairwise interactions; logistic BVS) and colon cancer survival (n=260; p=175)
- **Code/data:** R package mombf; code at https://github.com/davidrusi/paper_examples/tree/main/2020_Rossell_Abril_Bhattacharya_ALA
- *Source pages:* Sec 5 intro; 5.1; 5.2.1; 5.2.2 (Fig 4); 5.3; 5.4 (arXiv v2 numbering); *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Ray2022
Ray K.; Szabo B.; Variational Bayes for high-dimensional linear regression with sparse priors; J. Amer. Statist. Assoc.; 117(539); 1270-1281 (2022). **10.1080/01621459.2020.1847121 (arXiv:1904.07150)**

- **X:** iid-N(0,I); equicorr(rho=0.3;0.7) (suppl A.5); real-X+real-y (ozone interactions). Main Sec 5.2: X_ij iid N(0,1) (supp: variance 2 variant); supp A.5 Sigma_jk=rho off-diagonal; ozone design column-centred and scaled to Euclidean norm sqrt(n) plus intercept
- **n:** 100;200;500 (supp); real n=203
- **p (max):** 1000 (main text grid 400;1000;800); supp 300;500;800; real p=134
- **s0:** Main: s=20; 3 (caption; text says 40); 5; 20; supp: 15;50;20
- **β / SNR:** Main: nonzero theta_i=A with A=log n; (1,2,3); U(-5,5); 2 log n; signal located at end/beginning/middle of coefficient vector; noise sd varsigma=5;1;0.2;5 (n,p,s,varsigma)=(100,400,20,5);(100,1000,3,1);(200,800,5,0.2);(100,400,20,5)
- **Noise:** Gaussian N(0,varsigma^2); noise sd unknown and estimated (selectiveInference); misspecified noise in supp A.4; **replicates:** 100 runs (main); 200 runs (supp)
- **Metrics:** l2 error; FDR; TPR; runtime; 10-fold CV prediction error on ozone; number selected
- **Competitors:** sparsevb (proposed); varbvs; EMVS; SSLASSO; ebreg (fractional-likelihood empirical Bayes MCMC)
- **Real data:** Ozone interaction data (Breiman-Friedman; n=203; p=134 pairwise interactions of 9 meteorological and 3 time variables): 10-fold CV error
- **Code/data:** R package sparsevb
- *Source pages:* Sec 5.2 (pp 15-17) Table 2; Supp A.1-A.5 Tables 3-7; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Kim2024
Kim Y; Wang W; Carbonetto P; Stephens M. A flexible empirical Bayes approach to multiple linear regression and connections with penalized regression. JMLR 25(185) (arXiv v3 Jun 2024) (2024). **arXiv:2208.10910**

- **X:** three designs: (1) iid N(0,1); (2) equicorrelated rho in [0,1] (rho=0.5 and 0.95 shown); (3) real GTEx genotype matrices (SNPs within 1 Mb of a gene TSS; MAF>=5%; from Wang et al. 2020; 20 random data sets; centered and scaled). simulated designs n=500 and p in {200;1000;10000} (Experiment 4 varies p; low/medium/high dimension); genotype designs n=287 with p from 4012 to 8760; test set same size as training set
- **n:** 500
- **p (max):** 10000
- **s0:** s=20 non-zero coefficients by default (Exp 1 varies s from 1 to p; positions uniform at random); coefficients N(0,1) by default (Exp 3: uniform; Laplace; t_1/t_2/t_4/t_8; point mass)
- **β / SNR:** PVE=0.5 default; Exp 2 varies PVE; sigma^2=Var(Xb)(1-PVE)/PVE
- **Noise:** Gaussian default; Exp 5 uses uniform; Laplace; t_df noise rescaled to target PVE; **replicates:** 20 per setting
- **Metrics:** out-of-sample prediction error (RMSE-scaled relative to null predictor); runtime; no selection metrics (no FDR or PIP evaluation)
- **Competitors:** ridge; Lasso; Elastic Net; SCAD; MCP; L0Learn; SSLasso; Trimmed Lasso; BayesB and Bayesian Lasso (BGLR); varbvs; SuSiE
- **Real data:** none beyond GTEx genotypes for X (phenotypes simulated)
- **Code/data:** https://github.com/stephenslab/mr.ash.alpha; https://github.com/stephenslab/mr-ash-workflow
- *Source pages:* Section 5.1-5.3 (pp. 20-29); Table 1; Figs 2-4; *read level:* full-text (arXiv PDF); *scout file:* `S3_GENOMICS.tsv`


## freq-penalised

### Tibshirani1996
Tibshirani R. Regression shrinkage and selection via the lasso; Journal of the Royal Statistical Society Series B 58(1):267-288 (1996). **10.1111/j.2517-6161.1996.tb02080.x**

- **X:** AR1(rho=0.5); equicorr(rho=0.5). Examples 1-3: x_i~N(0;Sigma) Sigma_ij=0.5^|i-j|; Example 4: x_ij=z_ij+z_i (z indep N(0;1)) giving pairwise correlation 0.5 (compound symmetry); predictors standardised; tuning by 5-fold CV / generalized CV
- **n:** n=20 (Ex 1-3; p=8); n=100 (Ex 4; p=40); prostate cancer n not extracted
- **p (max):** 40 (Ex 4: p=40)
- **s0:** s=3 (Ex1: beta=(3;1.5;0;0;2;0;0;0)); s=8 (Ex2: all 0.85); s=1 (Ex3: beta=(5;0;...;0)); s=20 (Ex4: blocks of 10 zeros; 10 twos; 10 zeros; 10 twos)
- **β / SNR:** Ex1 sigma=3 (SNR~5.7); Ex2 beta_j=0.85 sigma=3 (SNR~1.8); Ex3 beta=(5;0..) sigma=2 (SNR~7); Ex4 beta in {0;2} blocks and noise sd 15 (SNR~9); signal level controlled by sigma
- **Noise:** Gaussian N(0;sigma^2); **replicates:** 50 data sets per example in the setup text (mean squared errors reported 'over 200 simulations' in Ex1 text; inconsistency in paper)
- **Metrics:** median mean-squared error (ME) of fit; average number of zero coefficients; most frequently selected models (Table 4); standard errors by bootstrap
- **Competitors:** least squares; lasso (CV and generalized CV); non-negative garotte; best subset (leaps; 5-fold CV); ridge regression
- **Real data:** Prostate cancer (Stamey et al. 1989; 8 predictors; lpsa response): coefficient paths and standard errors
- **Code/data:** none (S-Plus era)
- *Source pages:* Sec 7 Simulations pp 273-275 (7.1 Outline; 7.2 Ex 1; 7.3 Ex 2; 7.4 Ex 3; 7.5 Ex 4; Tables 3-8); Sec 3 prostate example; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### FanLi2001
Fan J; Li R. Variable selection via nonconcave penalized likelihood and its oracle properties; Journal of the American Statistical Association 96(456):1348-1360 (2001). **10.1198/016214501753382273**

- **X:** AR1(rho=0.5); iid-N(0;I) (+Bernoulli(0.5) columns in logistic example). Ex 4.1: x~N(0;Sigma) Sigma_ij=0.5^|i-j| (model of Tibshirani 1996); Ex 4.2 same design with errors N(0;1) contaminated by 10% standard Cauchy outliers; Ex 4.3 logistic: first six components as Ex 4.1 and last two iid Bernoulli(0.5); all covariates standardised; SCAD a=3.7; lambda by 5-fold CV and GCV (similar)
- **n:** n=40 (sigma=3); n=40 (sigma=1); n=60 (sigma=1) (Ex 4.1; p=8); n=60 (Ex 4.2); n=200 (Ex 4.3; p=8); burns data n=981
- **p (max):** 13 (burns data with quadratics and interactions: 13 covariates; simulations p=8)
- **s0:** s=3 (beta=(3;1.5;0;0;2;0;0;0))
- **β / SNR:** beta=(3;1.5;0;0;2;0;0;0) fixed; noise sigma=3 or 1 (SNR ~ 5.7 for sigma=3 by Tibshirani 1996 formula; not stated in this paper); oracle estimator included
- **Noise:** Gaussian N(0;1)*sigma; Cauchy-contaminated (10%); logistic; **replicates:** 100 simulated datasets per setting
- **Metrics:** median relative model error (MRME %) vs least squares; average number of zero coefficients (correct vs incorrect); standard error accuracy via sandwich formula (true vs estimated SD)
- **Competitors:** SCAD (two a tuning variants SCAD1 GCV-a vs a=3.7); LASSO (L1 penalty); hard thresholding; ridge; best subset; nonnegative garrote; oracle; OLS
- **Real data:** Burns data (General Hospital Burn Center USC; n=981; binary survival; age; sex; log(burn area+1); oxygen; quadratic and interaction terms) with SCAD/LASSO/best subset AIC/BIC (Ex 4.4)
- **Code/data:** MATLAB code; not stated as public
- *Source pages:* Sec 4.3 Simulation Study (Ex 4.1 Table 1; Ex 4.2 Tables 3-4; Ex 4.3 Tables 5-6); Ex 4.4 burns data Table 7 (pp 1356-1358); *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### ZouHastie2005
Zou H; Hastie T. Regularization and variable selection via the elastic net; Journal of the Royal Statistical Society Series B 67(2):301-320 (2005). **10.1111/j.1467-9868.2005.00503.x**

- **X:** AR1(rho=0.5); equicorr(rho=0.5); factor (grouped predictors: 3 latent factors + eps sd 0.1). Ex1 and Ex2: corr(i;j)=0.5^|i-j| (as lasso paper Ex 1-2); Ex3: equicorrelated 0.5 with 4 blocks; Ex4 grouped: x_i=Z_g+eps_i with Z1 for i=1..5; Z2 for 6..10; Z3 for 11..15 (eps~N(0;0.01)); 25 iid N(0;1) noise predictors; training/validation/test splits with validation used for tuning; idealised grouping example (n=100; 6 variables; Z~U(0;20))
- **n:** n=20/20/200 train/val/test (Ex1-2; p=8); 100/100/400 (Ex3; p=40); 50/50/400 (Ex4; p=40); idealised n=100; leukaemia n=72
- **p (max):** 7129 (leukaemia gene data p=7129; simulations p<=40)
- **s0:** Ex1 s=3 (beta=(3;1.5;0;0;2;0;0;0)); Ex2 s=8 (all 0.85); Ex3 s=20 (blocks of 10 zeros/twos); Ex4 s=15 (three groups of 5 with beta=3)
- **β / SNR:** Ex1 sigma=3; Ex2 beta_j=0.85 sigma=3; Ex3 beta blocks (0;2;0;2) sigma=15; Ex4 beta=3 on 15 grouped predictors; sigma=15
- **Noise:** Gaussian N(0;1)*sigma; **replicates:** 50 data sets per example (50 replications)
- **Metrics:** median test mean-squared error; number of selected variables (grouping effect); solution-path comparisons
- **Competitors:** lasso; ridge; naive elastic net; elastic net (LARS-EN; 2-D tuning grid with lambda2 in 0;0.01;0.1;1;10;100)
- **Real data:** Prostate cancer (Stamey 1989; 8 predictors); leukaemia microarray (Golub 1999; 7129 genes; 72 samples: 38 train (27 ALL; 11 AML) and 34 test) for classification and gene selection (elastic net lambda=0.01)
- **Code/data:** LARS-EN R package elasticnet; data from Golub 1999
- *Source pages:* Sec 5 pp 312-313 (Examples 1-4; Table 2); idealised grouping example p313; Sec 4 prostate p311; Sec 6 microarray p314+; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Zou2006
Zou H. The adaptive lasso and its oracle properties; Journal of the American Statistical Association 101(476):1418-1429 (2006). **10.1198/016214506000000735**

- **X:** AR1(rho=0.5; 0.75); other (Model 0: 4x4 C matrix with rho1=-0.39; rho2=0.23 making lasso path inconsistent). Model 0 x~N(0;C) with C from Corollary 1 (rho1=-0.39; rho2=0.23); Models 1-2 corr(j1;j2)=0.5^|j1-j2|; logistic example corr 0.75 (rho between xi and xj; Hunter-Li 2005 model); weights from OLS (gamma in 0.5;1;2 chosen by 2-D CV); tuning by 5-fold CV
- **n:** n=60; 120 or 300 (Model 0; p=4); n=20 or 60 (Model 1; p=8); n=40 or 80 (Model 2; p=8); n=200 (logistic; p=9); test sets of 10000
- **p (max):** 9 (logistic example p=9; Models 1-2 p=8; Model 0 p=4)
- **s0:** Model 0 s=3 (beta=(5.6;5.6;5.6;0)); Model 1 s=3 (beta=(3;1.5;0;0;2;0;0;0)); Model 2 s=8 (beta_j=0.85); logistic s=3 beta=(3;0;0;1.5;0;0;7;0;0)
- **β / SNR:** Model 1: sigma=1;3;6 giving SNR~21.25;2.35;0.59; Model 2: sigma=1;3;6 giving SNR 14.46;1.61;0.40 (printed values); Model 0 sigma in (9;5) paired with n=60;120; SNR=beta'C beta/sigma^2
- **Noise:** Gaussian N(0;sigma^2); logistic Bernoulli; **replicates:** 100 datasets per setting
- **Metrics:** probability that solution path contains the true model (Model 0); relative prediction error RPE=E[(yhat-x'beta)^2]/sigma^2; median RPE; median number of selected variables (Table 3); misclassification RPE relative to Bayes error (logistic); standard errors of adaptive lasso estimates (Table 4)
- **Competitors:** lasso (LARS); adaptive lasso (LARS on reweighted); SCAD (LQA algorithm); nonnegative garotte (QP)
- **Real data:** none (p<n only; high-dim discussed only via ridge-initial weights in Sec 4.2)
- **Code/data:** none stated
- *Source pages:* Sec 3.3-3.4 / Sec 4 'Numerical experiments' (Model 0 Table 1; Models 1-2 Table 2; Table 3; Table 4); logistic example Fig 2 (Sec 3.5-ish); Sec 4.2 high-dimensional discussion; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Hoggart2008
Hoggart CJ; Whittaker JC; De Iorio M; Balding DJ. Simultaneous analysis of all SNPs in genome-wide and re-sequencing association studies. PLoS Genet 4(7) e1000130 (2008). **10.1371/journal.pgen.1000130**

- **X:** real-LD haplotype simulation (FREGENE forward-time coalescent-like population); binary/SNP-genotypes. FREGENE 20 Mb sequence in population of 10K individuals (human-like mutation/crossover/gene-conversion); marker SNPs sampled with approx uniform MAF at one SNP per 5 kb = 80K SNPs per 400 Mb genome (20 equal chromosomes, causal variants only on one); whole-genome study: 120 independent 20Mb chromosomes = 480K SNPs; resequencing study: all 192K polymorphic sites of one 20 Mb region
- **n:** 2000 (1000 cases + 1000 controls) in main and GWA sims; real T2D: 694 cases + 654 controls
- **p (max):** 480,000 SNPs (whole-genome simulation; 10 causal); 192,000 (resequencing); 80,000 (main); real T2D 300,535 SNPs
- **s0:** 6 causal variants per dataset (main; 500 datasets, 3000 causal total); 10 causal (480K sim); 6 causal (reseq, 10 datasets)
- **β / SNR:** multiplicative allelic risk ratios; two causal SNPs at each MAF 2%;5%;15% with risk ratios chosen for ATT power about 25% and 75% at threshold 1e-5; disease prevalence 12%; 480K sim: MAF 15% RR=2 for all ten
- **Noise:** Bernoulli case-control; **replicates:** 500 data sets (main); 1 whole-genome dataset (480K); 10 resequencing datasets; null: 1,000 permutations on 2K individuals x 80K SNPs
- **Metrics:** causal variants tagged (r2>0.05 with a selected SNP); false positives (clustered within 0-100 kb counted once); per-SNP type-I error under null permutations; number of SNPs selected
- **Competitors:** Armitage trend test (single SNP); NEG vs DE shrinkage priors (penalised logistic regression with stochastic search; posterior mode)
- **Real data:** Type 2 diabetes GWAS (Hap300 BeadArray): 694 cases + 654 controls, 300,535 SNPs after QC; best model 26 SNPs tagging 25 loci incl 5 replicated
- **Code/data:** software described in paper (HyperLasso; availability URL not captured in text read)
- *Source pages:* Results: Main Simulation Study; Null Simulation; Whole Genome Simulation Study; Re-Sequencing Simulation Study; T2D analysis; Methods Simulation Study; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Meinshausen2009
Meinshausen N; Meier L; Buhlmann P. P-values for high-dimensional regression; Journal of the American Statistical Association 104(488):1671-1681 (2009). **10.1198/jasa.2009.tm08647; arXiv:0811.2177**

- **X:** AR1(rho=0.5); real-X(synthetic beta). (A) rows N(0;Sigma) Cov(X_j;X_k)=0.5^|j-k|; (B) same with p=1000; (C) real riboflavin Bacillus subtilis design (n=71; p=4088; log gene expressions) with artificial sparse beta; screening S_fixed (floor(n/6) variables most often on lasso path); S_cv (lasso CV); S_adap (adaptive lasso CV); B=50 sample splits; gamma_min=0.05
- **n:** n=100 (p=100; 1000; also p=200 in Table 1); n=71 real design (p=4088)
- **p (max):** 4088 (A p=100; B p=1000; C p=4088)
- **s0:** |S|=5 or 10
- **β / SNR:** Uniform sampling: |S| random coefficients =1; varying-strength: random support with values 1..|S|; SNR in {0.25;1;4;16} (population R^2 0.2;0.5;0.8;0.94) with sigma^2 adjusted each run
- **Noise:** Gaussian with sigma^2 set from SNR; **replicates:** 50 simulations per setting
- **Metrics:** FWER P(false positives>0); average number of true positives E(TP); E(false positives)
- **Competitors:** single-split (Wasserman-Roeder); multi-split p-values; adaptive lasso (Zou 2006) alone; lasso variants as screening
- **Real data:** Riboflavin (n=71; p=4088) used as real design with synthetic beta (setting C); Sec 4.3 real motif regression (Conlon et al 2003; n=287 DNA segments; p=195 motifs): multi-split finds 1 significant motif at 5%
- **Code/data:** R implementation (later R package hdi)
- *Source pages:* Sec 4.1 Simulations pp 11-12 (A-C); Fig 2-3; Table 1 (adaptive lasso comparison); Sec 4.3 motif regression; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### MeinshausenYu2009
Meinshausen N; Yu B. Lasso-type recovery of sparse representations for high-dimensional data; Annals of Statistics 37(1):246-270 (2009). **10.1214/07-AOS582; arXiv:0806.0145**

- **X:** other (sine-dictionary frequency detection; deterministic design violating irrepresentable condition). Single illustrative design: predictors are sin functions with frequencies evenly spaced from 1/200 to 1/2 (spacing 1/600) at n=200 evenly spaced times; two adjacent true frequencies 0.0545 and 0.0555; irrepresentable condition violated at the midpoint resonance frequency; authors state they deliberately use 'instead of extensive numerical simulations'
- **n:** n=200
- **p (max):** about 300 (computed from grid 1/200 to 1/2 with spacing 1/600; p not stated explicitly)
- **s0:** s=2
- **β / SNR:** beta_w1=beta_w2=1 (phases zero); sigma=0.2 for the periodogram example
- **Noise:** Gaussian sigma=0.2 (Fig 1) and varied; **replicates:** not extracted (shaded area covers 90% of simulations)
- **Metrics:** probability each frequency is selected along lasso path; l2 distance ||beta-beta_hat|| separately for signal and noise variables; regularisation-path coefficient magnitudes
- **Competitors:** lasso only (illustration)
- **Real data:** none
- **Code/data:** none
- *Source pages:* Sec 4 pp 20-22 Figs 1-3; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Wasserman2009
Wasserman L; Roeder K. High-dimensional variable selection; Annals of Statistics 37(5A):2178-2201 (2009). **10.1214/08-AOS646; arXiv:0704.1139**

- **X:** iid-N(0;I); AR1(rho=0.5) (chain X_j+1=rho X_j+sqrt(1-rho^2) eps); other (unfaithful model rho=0.95); binary/SNP-genotypes (real MrOS SNPs). Models A (null; iid); B (triangle; iid); C (correlated triangle; X_{j+1}=rho X_j+(1-rho^2)^{1/2}eps*; rho=0.5); D (unfaithful: X2=rho X1+tau eps; X3=rho X1+tau eps; X4=rho X2+tau eps; tau=0.01; rho=0.95); covariates standardised; max model size k_n=sqrt(n); screen-and-clean with 3 splits or 2 splits; leave-one-out CV
- **n:** n=100 (p=100 and 1000); n=100 and 1000 for model D (p=10); real n=860
- **p (max):** 1000 (p=100; 1000; real model 2066 coefficients)
- **s0:** Model A s=0; B and C s=10 (beta_j=delta(10-j) j=1..10); D s=2 (beta1=-beta2=10)
- **β / SNR:** Triangle beta_j=delta(10-j) with delta=0.5 (p=100) or 1.5 (p=1000); null model; unfaithful beta1=-beta2=10; unit noise
- **Noise:** Gaussian N(0;1); **replicates:** not stated in text read (Table 1 reports size and power averaged; replication count not found)
- **Metrics:** size (type-I error / FWER-type); power pi_av (average fraction of true variables detected); false positive rate
- **Competitors:** lasso screen-and-clean (LOO-CV); forward stepwise screening; marginal regression screening; two-stage adaptive lasso split-sample comparator (Table 2)
- **Real data:** MrOS osteoporotic fractures in men (n=860; 296 SNPs spanning 30 candidate genes for bone mineral density; with 2 SNPs per gene interactions 2066 coefficients: 296 main + 1770 interactions); phenotype modified to plant signal in 3 SNPs
- **Code/data:** none stated
- *Source pages:* Sec 5 Application p10; Sec 6 Simulations pp 10-12 Tables 1-2; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Wu2009
Wu TT; Chen YF; Hastie T; Sobel E; Lange K. Genome-wide association analysis by lasso penalized logistic regression. Bioinformatics 25(6) 714-721 (2009). **10.1093/bioinformatics/btp041**

- **X:** (a) synthetic: latent multivariate normal thresholded at first quartile to give SNP coding -1/0/1; only first 10 predictors correlated (rho grid incl. 0); (b) coeliac genotypes (British, van Heel 2007) with simulated phenotype. synthetic p up to 100000 (also 5000; 50000 with n=2000) with n around 500-2000 (exact grid in Table 1, lost in text conversion); coeliac p=310,637 SNPs n=2200 (778 cases; 1422 controls); 32 SNPs MAF<1% dropped
- **n:** 2200
- **p (max):** 310637
- **s0:** synthetic: 5 true main effects (beta_j=1) plus 2 interactions (eta12=eta34=0.5); coeliac simulation: 4 main effects (gender + 3 SNPs) and 2 interactions
- **β / SNR:** large fixed effects (mu=1; beta_j=1) chosen to be detectable in small samples; coeliac simulation mu=-3; beta=1; eta=2 (logistic scale)
- **Noise:** logistic / case-control outcome; synthetic example described as model (8) with marginal and two-way interaction effects; **replicates:** 50 random replicates per setting (both synthetic and coeliac-based)
- **Metrics:** number of true predictors recovered at stage 1 and 2; FDR vs lambda1 plot; LOO indices vs univariate p-values; computing time with and without score swindle
- **Competitors:** univariate tests (per-SNP logistic p-values); no other multivariate selector
- **Real data:** British coeliac disease GWAS (van Heel 2007; 310,637 SNPs; 2200 subjects; WTCCC-era data under access agreement)
- **Code/data:** Mendel 9.0 (UCLA Human Genetics); supplementary on Bioinformatics site
- *Source pages:* Sections 3 (Analysis of simulated data) and 4.1-4.2 (coeliac data and simulation); Table 1 caption; *read level:* full-text (PMC HTML); tables partly garbled; *scout file:* `S3_GENOMICS.tsv`

### Friedman2010
Friedman J; Hastie T; Tibshirani R. Regularization paths for generalized linear models via coordinate descent; Journal of Statistical Software 33(1):1-22 (2010). **10.18637/jss.v033.i01**

- **X:** equicorr(rho=0;0.1;0.2;0.5;0.9;0.95); other (sparse features 95% zeros). Gaussian data with every pair X_j;X_j' having the same population correlation rho; Y=sum X_j beta_j + k Z with Z~N(0;1) and k chosen so SNR=3.0; logistic outcome via p=1/(1+exp(-y)) and z~Bernoulli(p); sparse-feature design with 95% zeros (Table 3); this is the canonical glmnet timing design
- **n:** N=1000 or 5000 (p=100); N=100 (p=1000;5000;20000;50000 for linear; p=1000;5000;100000 for logistic dense); N=100000 (p=100); N=10000 (p=100) and N=100 (p=10000) sparse
- **p (max):** 1e5 (p grid 100;1000;5000;1e4;2e4;5e4;1e5; real NewsGroup p=777811)
- **s0:** no sparsity pattern (beta_j dense decaying); 10 true predictors in Fig 2 CV illustration (N=1000; p=100)
- **β / SNR:** beta_j=(-1)^j exp(-2(j-1)/20) alternating signs exponentially decaying (all p coefficients nonzero); SNR=3.0
- **Noise:** Gaussian with k set for SNR=3; binomial; **replicates:** timings averaged over 3 runs
- **Metrics:** CPU time in seconds (glmnet naive vs covariance updating vs lars vs l1logreg vs BBR vs LPL); cross-validation error curves (Fig 2)
- **Competitors:** lars; l1logreg (interior point); BBR/BMR (Bayesian binary regression); LPL (Lange); SGD-like tools in Table 5 (Leukemia benchmark vs other packages)
- **Real data:** Cancer (Ramaswamy 2002; 14 classes; N=144; p=16063); Leukemia (Golub 1999; N=72; p=3571 preprocessed by Dettling 2004); InternetAd (N=2359; p=1430; 1% nonzero); NewsGroup (N=11314; p=777811; 0.05% nonzero; binary tri-gram features)
- **Code/data:** R package glmnet (CRAN); code in paper
- *Source pages:* Sec 5.1 pp 12-13 (Table 1; design and SNR=3); Sec 5.2 pp 13-14 (Tables 2-3); Sec 5.3 p15 (Table 4 real data); Table 5; Fig 2 p17; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### MeinshausenBuhlmann2010
Meinshausen N; Buhlmann P. Stability selection (with discussion); Journal of the Royal Statistical Society Series B 72(4):417-473 (2010). **10.1111/j.1467-9868.2010.00740.x; arXiv:0809.2932**

- **X:** iid-N(0;I); block(10 blocks; rho=0.5; interleaved indices mod 10); Toeplitz(rho=0.99); factor(2 and 10 factors); real-X(synthetic beta). (A) iid N(0;1); (B) Sigma_km=0.5 if k mod 10 = m mod 10 else 0; (C) Sigma_km=0.99^|k-m|; (D) X_k=f_k1 phi1+f_k2 phi2+eta_k with iid N(0;1); (E) same with 10 factors; (F) motif regression real X; (G) riboflavin real X; columns scaled to unit norm; real-X scenarios use real design but synthetic beta
- **n:** n=100 or 1000 (A); 200 or 1000 (B;C;D;E); 2587 (F); 158 (G; elsewhere in paper n=115); p=1000 for A-E
- **p (max):** 1e3 (A-E p=1000; F p=660; G p=4088; also p=n=200 toy example)
- **s0:** s=4;10;20;50 (A-E); s=1..12 (F;G)
- **β / SNR:** beta_k iid Uniform[0;1] on random support S (A-E); N(0;1) random on S (F;G); sigma^2/n noise with SNR 0.5 or 2 (A-E) and 0.5;1;2 (F;G); classification: Bayes misclassification rate 1/8 or 1/3
- **Noise:** Gaussian N(0;sigma^2/n) (regression); logistic (classification); **replicates:** 100 runs per scenario (64 scenarios for A-E); 20 runs per setting for F;G (72 settings)
- **Metrics:** probability that top ceil(gamma s) selected variables (gamma=0.1;0.4) are all true (without error); expected number of false selections E(V) vs bound (q_Lambda=sqrt(0.8p); pi_thr=0.6 -> E(V)<=2.5); power; number of false positives vs CV
- **Competitors:** lasso; randomised lasso; stability selection (subsampling; randomised); OMP; randomised OMP; cross-validated lasso
- **Real data:** Riboflavin (Bacillus subtilis; n=115 or 158; p=4088) response used for real analysis in Sec 2.2; Motif regression yeast (n=2587; p=660); also used with real X and synthetic beta for error-bound check; graphical modelling real data (Sec 3)
- **Code/data:** riboflavin data from DSM Nutritional Products (now in R package hdi); R package stabs
- *Source pages:* Sec 4 Numerical Results pp 18-21 (scenarios A-G); Sec 2.2 riboflavin p5; Sec 3.2 randomised-lasso toy example; Figs 5-7; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Zhang2010
Zhang C-H. Nearly unbiased variable selection under minimax concave penalty; Annals of Statistics 38(2):894-942 (2010). **10.1214/09-AOS729; arXiv:1002.4734**

- **X:** other (greedy sequentially sampled groups of highly correlated columns); AR1(rho=0.9;0.1). Exp 1-3: pool of 600 (or 6000) random columns (exponential minus chi2_1 entries; centred; length sqrt(n)); columns sampled in groups of 10 (or 50) most-correlated vectors by greedy sequential sampling; Exp 5: Gaussian rows with corr sigma_jk=sigma_12^|k-j| (0.9 high; 0.1 low); columns normalised to ||x_j||^2=n
- **n:** n=300 (p=200; 2000); n=600 (p=3000)
- **p (max):** 3000 (Exp 1-2 p=200; Exp 3-4 p=2000; Exp 5 p=3000)
- **s0:** d0=10;20;40 (Exp 1); d0=30 (Exp 3-4); 5 blocks of (1;2;3;4;3;2;1) (Exp 5)
- **β / SNR:** beta_j=+-beta* on support (beta*/sigma=1/2 in Exp 1; beta*~10 lambda_univ); Exp 5 beta* scales so ||X beta||^2/n=3
- **Noise:** Gaussian N(0;I_n) sigma=1; **replicates:** 100 replications per setting (X; support; signs; noise redrawn each replication in Exp 1-3; every 10 replications in Exp 4-5)
- **Metrics:** correct selection indicator CS=I(A_hat=A0) (exact support recovery); number of PLUS steps k; SE of beta and mu estimators; MSE of sigma-hat; computational complexity
- **Competitors:** lasso; SCAD+ (PLUS algorithm local solution); MC+ with various gamma
- **Real data:** none
- **Code/data:** PLUS algorithm in R package plus (CRAN)
- *Source pages:* Sec 2.2 pp 8-9 Table 1; Sec 6.1 pp 27-29 Tables 3-4 (Exps 2-3); Sec 6.4 Figs 5-6 (Exps 4-5); *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### BrehenyHuang2011
Breheny P; Huang J. Coordinate descent algorithms for nonconvex penalized regression, with applications to biological feature selection. The Annals of Applied Statistics 5(1) 232-253 (2011). **10.1214/10-AOAS388**

- **X:** iid-N(0,I); equicorr(rho=0.9) (timing only); real-X(synthetic beta). Section 5.1 timing: X iid N(0,1) or equicorrelated rho=0.9, y pure noise (N(0,1) or Bernoulli(0.5)), n=1000, gamma=1/c* for convexity, 100 data sets per p; Section 5.2 Setting 1: iid N(0,1) X; Setting 2: design matrices held fixed at the real genetic-association (n=800,p=532) and microarray (n=38,p=7129) data
- **n:** n=1000 (timing); n=100 linear and n=400 logistic (Setting 1); n=800 and n=38 (Setting 2)
- **p (max):** p grid for timing (Fig 3) and Setting 1 (Fig 4) not stated in text (figure axes only; not extracted); Setting 2 max p=7129
- **s0:** Setting 1: 4 nonzeros (two +s and two -s) with s varied; Setting 2: 5 nonzeros in the SNP design (532) and 100 nonzeros in the microarray design (7129)
- **β / SNR:** Setting 1: beta = +s;+s;-s;-s with s varied; unit-variance noise (SNR varies with s). Setting 2 genetic: 5 values from Exp(rate 3) with random signs placed at random SNPs; microarray: 100 values N(0, sd 3) placed at random features; logistic responses via link in eq (3.1)
- **Noise:** Gaussian sigma=1 (linear); Bernoulli (logistic); **replicates:** 100 data sets (Setting 1 and timing); 500 data sets (Setting 2)
- **Metrics:** run time of whole path (CD vs LLA); relative MSE to lasso (ratio of medians); misclassification error; model size; percent of selected variables truly nonzero
- **Competitors:** MCP; SCAD; lasso (glmnet) with 10-fold CV; LLA vs coordinate descent algorithms
- **Real data:** Age-related macular degeneration case-control SNPs (n=800 [400 cases 400 controls]; p=532 markers in 30 genes); Golub leukemia (n=38 train + 34 test; p=7129)
- **Code/data:** ncvreg R package on CRAN; data sets described in Section 6 (no URL stated in text)
- *Source pages:* Section 5.1 pp. 15-16; Section 5.2 pp. 16-19 (Fig 3 Fig 4 Table 1); Section 6 pp. 19-21 (Table 2 Fig 5); *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Javanmard2014
Javanmard A; Montanari A. Confidence intervals and hypothesis testing for high-dimensional regression; Journal of Machine Learning Research 15(82):2869-2909 (2014). **arXiv:1306.3171 (JMLR v15 javanmard14a)**

- **X:** other (circulant banded Sigma); real-X+real-y. Rows iid N(0;Sigma) with circulant symmetric Sigma: Sigma_jj=1; 0.1 for k in j+1..j+5 (and wraparound); 0 otherwise (eq 59); design held FIXED across the 20 realisations; lasso lambda=4 sigma_hat sqrt(2 log p / n) with scaled-lasso sigma_hat; mu=2 sqrt(log p/n); alpha=0.05
- **n:** (n;p) = (1000;600) and (2000;1500) (note n>p); real riboflavin n=71
- **p (max):** 4088 (real riboflavin p=4088; synthetic p=600 and 1500; no p=2000)
- **s0:** s0=10;30 (n=1000;p=600); s0=25;50 (n=2000;p=1500)
- **β / SNR:** theta_0i=b on uniformly random support with b in {0.1;0.25;0.5}; unit noise N(0;1); no SNR defined
- **Noise:** Gaussian N(0;1); **replicates:** 20 independent realisations of the noise with fixed design and coefficients
- **Metrics:** average CI length (overall; active S; inactive S^c); coverage (overall; S; S^c); false positive rate FP and true positive rate TP at alpha=0.05; QQ-plot of z-scores
- **Competitors:** debiased lasso (this method); multisample-splitting (Meinshausen-Meier-Buhlmann 2009); ridge-type projection (Buhlmann 2013)
- **Real data:** Riboflavin (n=71; p=4088; from Buhlmann-Kalisch-Meier 2014): lasso lambda=0.036 selects 30 genes; debiased p-values with FWER 5% find 2 genes (YXLD-at; YXLE-at) vs 1 for multisample-splitting and 0 for ridge projection
- **Code/data:** code not stated in the arXiv version (R package glmnet used; later hdi)
- *Source pages:* Sec 5.1 pp 19-21 (Tables 1-2); Sec 5.2 p22 real data; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Bogdan2015
Bogdan M; van den Berg E; Sabatti C; Su W; Candes EJ. SLOPE: adaptive variable selection via convex optimization; Annals of Applied Statistics 9(3):1103-1140 (2015). **10.1214/15-AOAS842; arXiv:1407.3824**

- **X:** iid-N(0;1/n); binary/SNP-genotypes; other (correlated test statistics Sigma_ij=0.5; orthogonal). Sec 1.3.3: X iid N(0;1/n); Sec 3.1 correlated multiple-means (variance components sigma_tau^2=sigma_z^2=2.5 -> rho=0.5; X=Sigma^{-1/2}); Sec 3.2: Gaussian designs n=5000 with p=2n or n/2; Sec 3.2.4 idealised GWAS: independent SNPs with MAF~U(0.1;0.5) coded -1/0/1 (aa/aA/AA) centred and unit-norm columns; extra sims with dominant effects and violations of assumptions; orthogonal n=p=5000 (Fig 1)
- **n:** n=p=5000 (Fig 1;2; GWAS sim); n=5000 (p=2500 or 10000); prox timing p up to 1e7; sequence estimation previously with p=2048^2=4194304 and n=p/5; real n=5375
- **p (max):** 1e7 (prox timing only; Table 1 p=1e5;1e6;1e7); regression sims p<=1e4; mention p=4194304 (n=p/5) in earlier paper
- **s0:** k=0..50 (n=p=5000); k=0..100 (p=2n or n/2); k=0..80 (multiple means)
- **β / SNR:** non-null coefficient beta=sqrt(2 log p)~4.1 (barely above max null) in Sec 1.3.3; 5 sqrt(2 log p) in Sec 3.2 Gaussian designs; 1.2 sqrt(2 log p)~4.95 in GWAS sim; sigma=1 known (or estimated 'scaled' SLOPE)
- **Noise:** Gaussian N(0;1); **replicates:** 500 independent replicates per k
- **Metrics:** FDR (target q=0.1); power; relative squared error ||X b - X beta||^2/||X beta||^2; FDP distribution; runtime of prox (Table 1)
- **Competitors:** SLOPE (BH-type lambda sequence; Gaussian lambda_G; scaled SLOPE with unknown sigma); lasso with lambda_Bonf; lasso with lambda_CV (10-fold); BH on marginal tests; OLS debiasing after selection
- **Real data:** Resequencing study of 17 genomic regions in ~6000 Finnish individuals (Service et al. 2014): HDL cholesterol; after pruning n=5375 subjects; p=777 variants (MAF 2e-4 to 0.5); selection of HDL-associated variants
- **Code/data:** C/Matlab/R at http://www-stat.stanford.edu/~candes/SortedL1; R package SLOPE (CRAN)
- *Source pages:* Sec 1.3.3 pp 10-12 Fig 2; Sec 2 Table 1 p16; Sec 3.1 pp 18-19; Sec 3.2 pp 21-24 Fig 5; Sec 3.2.4 pp 27-29; Sec 3.3 pp 29-34 real HDL data; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Su2017
Su W; Bogdan M; Candes E. False discoveries occur early on the Lasso path; Annals of Statistics 45(5):2133-2150 (2017). **10.1214/16-AOS1521; arXiv:1511.01957**

- **X:** iid-N(0;I). X entries iid N(0;1) (Fig 1; 6; 7; AMP-regime Fig 5 with delta=n/p=1); theory in the linear-sparsity regime k/p=eps with n/p=delta fixed
- **n:** n=1010 (p=1000; Fig 1); n=p=1000 and n=p=5000 (Fig 5); n=250 (p=1000; Fig 6); n=p=1000 (Fig 7)
- **p (max):** 5e3 (n=p=5000 in noiseless illustration; typical p=1000)
- **s0:** k=200 (Fig 1); k=eps p with eps=0.2 (Fig 5); k=18 (Fig 6); k=5..150 (Fig 7)
- **β / SNR:** Fig 1 beta_1..200=4 with unit-normal errors (high SNR); Fig 5 prior Pi in {0 w.p. 1-eps; 50} or mixture {50;0.1} with prob pi0 in 0.3;0.5;0.7;0.9 noiseless sigma=0; Fig 6 beta=2.5 sqrt(2 log p)~9.3 on 18 coords sigma^2=1 or 0; Fig 7 beta=50 on k coords sigma^2=1
- **Noise:** Gaussian sigma^2=1 or noiseless sigma=0; **replicates:** 10 lasso paths (Fig 5a); 100 replicates (Fig 5b; Fig 7); 500 independent experiments (Fig 6)
- **Metrics:** TPP vs FDP trade-off along the lasso path; rank of first false discovery; probability of exact recovery (75% in noiseless Fig 6 setting)
- **Competitors:** lasso path only; least squares ordering (Fig 1); AMP-theory boundary (Donoho-Tanner-type curve)
- **Real data:** none
- **Code/data:** not stated in paper
- *Source pages:* Sec 1 Fig 1 p3 (n=1010;p=1000); Sec 2.4 Fig 5 pp 9-10; Sec 4 (Figs 6-7; discussion of n>=(2+o(1))k log p); *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Qian2020
Qian J; Tanigawa Y; Du W; Aguirre M; Chang C; Tibshirani R; Rivas MA; Hastie T. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. PLOS Genetics 16(10) e1009141 (2020). **10.1371/journal.pgen.1009141**

- **X:** real-X+real-y; binary/SNP-genotypes. No simulation study in the paper. Real UK Biobank genotypes coded 0/1/2/NA; adjustment covariates age sex and top 10 PCs; random split 60/20/20 train/validation/test
- **n:** n=337199 White British unrelated individuals (train+validation 269927 in PRS-CS/SBayesR step; test about 60000+)
- **p (max):** p=805426 measured variants (real data; flag >=1e5 but < 1e6; BASIL screens in batches against a larger-than-RAM matrix)
- **s0:** not applicable (real data). Selected model sizes: height lasso 47673 SNPs (R2test 0.6999) and relaxed lasso 13395 (R2test 0.6727); height with refitting lasso 45653 (R2test 0.7127)
- **β / SNR:** not applicable (real phenotypes: height; BMI; asthma; high cholesterol). Heritability context only: height narrow-sense h2 70-80% quoted from literature
- **Noise:** Gaussian linear model for height and BMI; penalised logistic for asthma and high cholesterol (case rate about 12%); **replicates:** one train/validation/test split; test SE of R2 about 0.001 by delta method; no replicates
- **Metrics:** R2 (continuous); AUC (binary); model size; correlation of fit with truth; proportion of residual variance explained (h2test); run time/memory discussed (BASIL algorithm; Table 4 timing of SNP matrix times residual matrix in ms)
- **Competitors:** lasso; relaxed lasso; elastic net (alpha 0.001;0.1;0.5;0.9); sequential LR on top-k univariate SNPs; one-step PLS-like truncated model (K=10000 and 100000); P+T; clumping; PRS-CS; SBayesR; prescreened lasso
- **Real data:** UK Biobank (n=337199; p=805426 variants): height; BMI; asthma; high cholesterol, prediction R2/AUC and number of selected SNPs
- **Code/data:** snpnet R package https://github.com/junyangq/snpnet; experiment scripts on GitHub (scripts_snpnet_paper); UK Biobank data restricted-access (application required)
- *Source pages:* Section 'UK Biobank analysis' (pp. 9-17 of 31); Fig 2-5; Tables 1-3; Methods (Table 4 timing); *read level:* full-text; *scout file:* `S2_FREQ.tsv`


## best-subset

### Bertsimas2016
Bertsimas D; King A; Mazumder R. Best subset selection via a modern optimization lens; Annals of Statistics 44(2):813-852 (2016). **10.1214/15-AOS1388; arXiv:1507.03133**

- **X:** AR1(rho=0.5;0.8;0.9); iid-N(0;I); real-X(synthetic beta). Example 1 Sigma_ij=rho^|i-j|; Examples 2-4 Sigma=I; X columns standardized to unit l2 norm; semi-synthetic Leukemia: top-1000 features most correlated with y; synthetic response
- **n:** n=50 (p=1000); n=30 (p=1000;2000); n=500 (p=100;1000); n=350 (diabetes p=64); n=1000 (p=50); n=72 (leukemia p=1000)
- **p (max):** 2000 (grid 50;64;100;500;1000;2000)
- **s0:** Ex1 k0=5 or 10 equi-spaced ones; Ex2 k0=5 ones; Ex3 k0=10 equally spaced in [0.5;10]; Ex4 k0=6 equally spaced in [-10;10]; leukemia semi-synthetic k0=5 ones SNR=7
- **β / SNR:** SNR=Var(x'beta)/sigma^2; SNR values 1;3;7 etc; sigma^2 set from SNR
- **Noise:** Gaussian (LAD variant also considered); **replicates:** 10 random instances per setting
- **Metrics:** prediction accuracy (relative); number of nonzeros; MIO optimality gap; upper-bound quality; computation time (up to 66 min per problem per k for p>=2000)
- **Competitors:** MIO (Gurobi); discrete first-order method; lasso (glmnet); Sparsenet; stepwise; debiased lasso; LAD-lasso
- **Real data:** Diabetes with all 2nd-order interactions (n=350 subsample; p=64); Leukemia (n=72; p>3000 reduced to 1000; semi-synthetic y)
- **Code/data:** Matlab/Gurobi; leukemia data from http://stat.ethz.ch/~dettling/bagboost.html
- *Source pages:* Sec 5.1 pp 25-27 (printed p26); Sec 5.3-5.4 Figs 8-10; Tables 3-8 appendix; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### BertsimasPauphilet2020
Bertsimas D; Pauphilet J; Van Parys B. Sparse regression: scalable algorithms and empirical performance; Statistical Science 35(4):555-578 (2020). **10.1214/19-STS701; arXiv:1902.06547**

- **X:** Toeplitz(rho=0.2;0.7); other (hard non-incoherent Sigma: identity with theta in (k+1)th row/col); real-X(synthetic beta) (TCGA lung cancer gene expression). Sigma_ij=rho^|i-j| (mutual incoherence holds); hard design: unit diagonal; theta in first k entries of (k+1)th row and column; theta a scalar in a range given in Sec 3.4; real X = TCGA lung n=1145 p=14858 standardised
- **n:** n varies (e.g. n=500..3700 for p=20000; n/p ratio sweeps; n=1000 with p=5000 in appendix); real X n=1145 (974 train/val; 171 test)
- **p (max):** 2e4 (regimes p=2000;10000;20000; scalability claimed to p=1e5 and n=1e4 p=1e6; p=5000 in appendix)
- **s0:** k_true=100 (p=2e4); 50 (p=1e4); 10 (p=2e3); 50 (appendix p=5000)
- **β / SNR:** w_true in {-1;0;1} random signs with exactly k_true nonzeros (hard design: all 1/sqrt(k)); sqrt(SNR)=||X w||_2/||eps||_2 as printed (i.e. variance-ratio SNR) with PVE=SNR/(1+SNR) per Hastie et al; SNR in {6; 1; 0.05} paired with p in {2e4;1e4;2e3} (Table 2); for TCGA real-X 10 log-spaced SNR 0.05-6 (Table 4)
- **Noise:** Gaussian scaled to SNR; **replicates:** 10 data sets per setting
- **Metrics:** accuracy A = TPR; false detection rate FDR; out-of-sample MSE; computation time relative to glmnet lasso; AUC and induced sparsity (classification)
- **Competitors:** CIO (convex integer optimisation cutting planes; Gurobi); SS (Boolean relaxation sub-gradient; Julia SubsetSelection); lasso; elastic net (glmnet); MCP; SCAD (ncvreg)
- **Real data:** TCGA lung cancer gene expression (n=1145; p=14858): synthetic Y at 10 SNR levels (Table 4) and real binary classification adenocarcinoma vs squamous (594 vs 551; 15% test; 10 splits; Table 7)
- **Code/data:** Julia package SubsetSelection; cutting-plane code on GitHub (footnote 1 of paper)
- *Source pages:* Sec 3.1 data generation p 10; Sec 3.2 metrics pp 10-11; Table 2 p 11; Sec 3.4 hard design; Sec 3.5 real X Table 4 p 21; Sec 4.4 real classification; Appendix B-C; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### BertsimasVanParys2020
Bertsimas D; Van Parys B. Sparse high-dimensional regression: exact scalable algorithms and phase transitions; Annals of Statistics 48(1):300-323 (2020). **10.1214/18-AOS1804; arXiv:1709.10029**

- **X:** Toeplitz(rho=0;0.1;varied). Sigma(i;j)=rho^|i-j|; rows x_i~N(0;Sigma) iid; rho=0.1 (lightly correlated) in Table 1; rho=0 in phase-transition Fig 1; nonlinear-kernel example with 16 extra uncorrelated regressors
- **n:** n up to 1e5 (p=2e5); n varied around phase transition n~120-152 for p=2000; n in sweeps up to ~500-1000+ with p=5000;10000;15000
- **p (max):** 2e5 (p=5e4;1e5;2e5 in Table 1; 2000 phase transition; 5000;10000;15000 in sensitivity study)
- **s0:** k=10;20;30 (Table 1); k=10 (Fig 1); k in 10;15;20 (Table 2 nominal 10)
- **β / SNR:** w_true has exactly k nonzeros at uniformly random indices with values uniform in {-1;+1}; noise N(0;sigma^2) scaled to SNR (sqrt(SNR)=||S||_2/||E||_2 as printed?); SNR in {3;7;20} nominal 20 (noisy) and noiseless case
- **Noise:** Gaussian; **replicates:** 50 independent synthetic datasets (phase-transition Fig 1); single instances for timing tables
- **Metrics:** accuracy A% (percent of true support recovered); false alarm rate F%; solution time (15 min limit in Fig 1); empirical phase transition in n for exact recovery
- **Competitors:** exact cutting-plane (Julia; Gurobi) vs lasso heuristic (glmnet); relaxations
- **Real data:** none for linear experiments; nonlinear kernel simulation f=160 features with SNR=20
- **Code/data:** Julia code (SubsetSelection / cutting-plane; as in Bertsimas-Pauphilet-Van Parys 2020)
- *Source pages:* Sec 4.1 data description p~13 (lines on synthetic data); Table 1 p 14 (p up to 2e5; n=1e5); Fig 1 p 15 (50 datasets; p=2000); Table 2 p 16; Sec 4.4 sensitivity; Sec 6 nonlinear example (24); *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Hastie2020
Hastie T; Tibshirani R; Tibshirani RJ. Extended comparisons of best subset selection; forward stepwise selection; and the lasso (arXiv tech-report version of: Best subset; forward stepwise or lasso? Analysis and recommendations based on extensive comparisons; Statistical Science 35(4):579-592) (2020). **10.1214/19-STS733; arXiv:1707.08692**

- **X:** AR1(rho=0;0.35;0.7). rows iid N_p(0;Sigma); Sigma_ij=rho^|i-j|; validation set of size n same distribution used for tuning; follows Bertsimas-King-Mazumder 2016 but wider SNR grid
- **n:** n=100 (low; p=10); n=500 (medium; p=100); n=50 (high-5; p=1000); n=100 (high-10; p=1000)
- **p (max):** 1e3 (p grid 10;100;1000;1000)
- **s0:** s=5;5;5;10
- **β / SNR:** beta-type 1: s ones at roughly equally-spaced indices; type 2: first s ones; type 3: first s equally spaced from 10 to 0.5; type 5: first s ones then beta_i=0.5^(i-s) decaying (weak sparsity); SNR nu=Var(x'beta)/sigma^2 on 10-value log grid 0.05 0.09 0.14 0.25 0.42 0.71 1.22 2.07 3.52 6.00 (PVE 0.05-0.86); sigma^2=beta'Sigma beta/nu
- **Noise:** Gaussian; sigma^2 set from SNR; **replicates:** 10 repetitions per setting (20 for the PVE figure)
- **Metrics:** relative risk (out-of-sample); relative test error; PVE; number of nonzeros; computation time; (support recovery only discussed)
- **Competitors:** lasso; relaxed lasso; forward stepwise; best subset (Gurobi MIO with 3-min limit per k)
- **Real data:** none (simulation only)
- **Code/data:** R code https://github.com/ryantibs/best-subset/ (bestsubset R package)
- *Source pages:* Sec 3.1 Setup pp 8-10; Sec 3.2 Gurobi budget pp 10-11; Sec 2.2 SNR/PVE definition; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Hazimeh2020
Hazimeh H; Mazumder R. Fast best subset selection: coordinate descent and local combinatorial optimization algorithms; Operations Research 68(5):1517-1537 (2020). **10.1287/opre.2019.1919; arXiv:1803.01454**

- **X:** equicorr(rho=0.3;0.9); AR1(rho=0.5;0.9); iid-N(0;I); real-X+real-y. Constant correlation Sigma_ij=rho; Exponential correlation Sigma_ij=rho^|i-j|; validation set (fixed design y'=X beta+eps') for tuning plus oracle and random-design tuning in supplement; Gaussian 1M: iid N(0;1) entries; real data augmented with random column-permutation probes
- **n:** n=100-1000 swept (p=1000); n=250 (p=1000); n=500 (p=2000); n=1000 (p=5e4 and 1e5); n=200 (p=1e6 Gaussian 1M); real: n=200 p=104000; n=2500 p=17580 (and 174755); n=5000 p=55537
- **p (max):** 1e6 (p grid 1e3;2e3;5e4;1e5;1e6; real up to 1.7e5)
- **s0:** k=20 (p=1000); 25 (p=1000 rho=0.9); 100 (p=5e4); 50 (p=1e5); 20 (p=1e6)
- **β / SNR:** k equi-spaced nonzeros all equal 1; SNR=Var(X beta)/sigma^2 swept 0.01-100 (also fixed SNR=5; 10; 100; 300); R2=SNR/(SNR+1)
- **Noise:** Gaussian; **replicates:** 20 random datasets per setting (Sec 5.3-5.4); 10 for large p (Sec 5.6) and for local-search comparison
- **Metrics:** prediction error ||Xbeta_hat-Xbeta0||^2/||Xbeta0||^2; L_inf estimation error; TP; FP; support size; full support recovery probability; objective value; training time
- **Competitors:** L0Learn (CD + local search L0; L0L1; L0L2); lasso; relaxed lasso; elastic net (glmnet); MCP (ncvreg); forward stepwise; IHT; MIO subproblems via Gurobi
- **Real data:** House Prices (Boston + pairwise interactions + 1000 permuted-column probes; n=200; p=104000); Amazon Grocery reviews TF-IDF (n=2500; p=17580; augmented p=174755); US Census Planning Database (n=5000; p=55537 with probes); Gaussian 1M (n=200; p=1e6; k=20; SNR=10) - used for timing and test performance vs sparsity
- **Code/data:** L0Learn on CRAN and https://github.com/hazimehh/L0Learn
- *Source pages:* Sec 5.1 pp 20-22 (setup/measures); Sec 5.3-5.4 pp 23-27; Sec 5.5 pp 28-29; Sec 5.6 pp 30-32 incl Table 1; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Zhu2020
Zhu J; Wen C; Zhu J; Zhang H; Wang X. A polynomial algorithm for best-subset selection problem; PNAS 117(52):33117-33123 (2020). **10.1073/pnas.2014241117**

- **X:** AR1(rho=0.5); iid-N(0;I); equicorr(rho=0.8). Low-dim: Sigma_ij=0.5^|i-j| (model from Fan-Li/Tibshirani style; ref 6); High-dim: Sigma=I or Sigma_ij=0.8 for i!=j; tuning by SIC (and CV) with smax=[n log p log log n]; SCAD gamma=3.7; MCP gamma=3
- **n:** n=40 or 60 (low-dim p=8; and p from 20 to 40 for timing); n=500 (high-dim)
- **p (max):** 2500 (p grid 500;1500;2500)
- **s0:** s=3 (beta=(3;1.5;0;0;2;0;0;0)); s=10 (3 strong; 4 moderate; 3 weak)
- **β / SNR:** Low-dim: beta=(3;1.5;0;0;2;0;0;0) with (n;sigma)=(40;3);(40;1);(60;1); High-dim: 10 random active coefficients drawn N(0;SD^2) with SD=10 (3 strong); 5 (4 moderate); 2 (3 weak); sigma^2=1
- **Noise:** Gaussian sigma=3 or 1 (low-dim); sigma^2=1 (high-dim); **replicates:** 100 synthetic datasets
- **Metrics:** TPR; TNR; relative error ||beta_hat-beta||/||beta||; sparsity-level error s_hat-s*; runtime
- **Competitors:** ABESS (splicing + SIC); exhaustive ASR (all-subset regression); lasso (glmnet); SCAD; MCP (ncvreg); CV and SIC tuning
- **Real data:** none in main text (SI Appendix has extra simulations)
- **Code/data:** abess R/Python package (GitHub abess-team/abess)
- *Source pages:* Section Simulation: Low-dimensional case Table 1; High-dimensional case Fig 2; Fig 1 timing; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Hazimeh2022
Hazimeh H; Mazumder R; Saab A. Sparse regression at scale: branch-and-bound rooted in first-order optimization; Mathematical Programming 196(1-2):347-388 (2022). **10.1007/s10107-021-01712-4; arXiv:2004.06152**

- **X:** equicorr(rho=0.1); block(k0 blocks; AR1 within block; rho up to 0.9); real-X+real-y. Default Sigma_ij=0.1 for i!=j (constant correlation); feature-correlation study: block-diagonal Sigma with k0 blocks of equal size each Sigma^(l)_ij=rho^|i-j| (exponentially decaying within block) rho values incl 0.8 and 0.9; y and X columns mean-centred and unit-l2 normalised; Gurobi/MOSEK/GRB baselines
- **n:** n=1000 (p=1e3;1e4;1e5;1e6); n=100..1e5 (p=1e4; sample-size study); real Riboflavin n=71
- **p (max):** 8.3e6 (p grid 1e3;1e4;1e5;1e6; real riboflavin with all pairwise interactions p=8362004)
- **s0:** k0=10 (default); k0 in 10;15;20;25 (sparsity study at p=1e4)
- **β / SNR:** k0 equi-spaced nonzeros all equal 1; SNR=Var(X beta)/sigma^2=5 by default ('relatively difficult but allows full support recovery'); SNR in 0.5;1;2;3;4;5 (n=p=1000; Table 2)
- **Noise:** Gaussian sigma^2 set from SNR; **replicates:** not stated (running-time tables; 2 h time limit per instance)
- **Metrics:** running time to optimality; optimality gap after time limit; number of BnB nodes; (statistical metrics not the focus)
- **Competitors:** L0BnB (BnB with coordinate-descent/active-set first-order node solves); MIP solvers Gurobi (GRB) and MOSEK (MSK); Bertsimas-Van Parys cutting-plane (B) solver; also L0Learn warm starts
- **Real data:** Riboflavin (n=71; p=4088) augmented with all pairwise interactions to p=8362004; 5-fold CV via L0Learn for lambda choice; run time vs support size up to 15 nonzeros (Fig 2)
- **Code/data:** L0BnB Python package on GitHub (data generator provided)
- *Source pages:* Sec 4.1 pp 20-21 (setup; data generation); Sec 4.2.1 p21 Table 1 (p to 1e6); Sec 4.2.2 Table 2; Sec 4.3 Tables 3-4 (n; correlation; sparsity); Sec 4.4 Fig 2 (riboflavin p=8.3e6); Appendix C; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Zhu2022abess
Zhu J; Wang X; Hu L; et al. abess: a fast best-subset selection library in Python and R; Journal of Machine Learning Research 23(202):1-7 (2022). **arXiv:2110.09697**

- **X:** real-X+real-y; other. No simulation study in this short software paper; only a usage example generate.data(n=300; p=1000; beta=c(3;-2;0;0;2;0...)) in Fig 2; performance comparison is on real data only
- **n:** n=300 (usage example); real: 3895; 118; 7074; 217
- **p (max):** 1e3 (usage example); real data up to p=85400
- **s0:** 3 (usage example)
- **β / SNR:** usage example beta=(3;-2;2;0...); no SNR specified
- **Noise:** Gaussian (default generate.data); **replicates:** 20 randomly drawn test sets (Table 2)
- **Metrics:** test MSE (regression); AUC (classification); number of nonzeros NNZ; runtime; explained variance for sparse PCA
- **Competitors:** scikit-learn l1 (LassoCV/LogisticRegressionCV); celer; scikit-learn l0 (OMP); elasticnet R package for SPCA
- **Real data:** Superconductivity (n=3895; p=85400 after feature expansion); Cancer gene expression Chin et al. 2006 (n=118; p=22215); Musk (n=7074; p=166); SPCA genetic data Christensen et al. 2009 (n=217; p=1413)
- **Code/data:** https://github.com/abess-team/abess; PyPI abess; CRAN abess
- *Source pages:* Sec 3 Fig 2 p3; Sec 4 Tables 2-3 p4; *read level:* full-text; *scout file:* `S2_FREQ.tsv`


## knockoffs

### BarberCandes2015
Barber RF; Candes EJ. Controlling the false discovery rate via knockoffs; Annals of Statistics 43(5):2055-2085 (2015). **10.1214/15-AOS1337; arXiv:1404.5609**

- **X:** iid-N(0;I); AR1(rho=0 to 0.9); real-X(synthetic beta) (HIV NNRTI sparse binary design); binary/SNP-genotypes. Sec 3.3.1: X iid N(0;1) then columns normalised; Sec 3.3.2: rows N(0;Theta_rho) with Theta_jk=rho^|j-k| rho=0;0.1;...;0.9 and columns normalised; Sec 4.1: real sparse binary mutation matrix X (747x319 NNRTI); knockoff via equi-variant or SDP construction; statistics from lasso path (signed max lambda)
- **n:** n=3000 (p=1000); n=747 (p=319 semi-real); real HIV data n=634-846
- **p (max):** 1e3 (p=1000; real p up to 319)
- **s0:** k=30 (default); k=10..200 swept; k=20 (semi-real)
- **β / SNR:** beta_j random sign +-A on random support with A=3.5 (approx expected max |X_j'z| under null); A varied 2.8 to 4.2; Sec 4.1 beta_j~3.5 N(0;1) on k=20; unit noise
- **Noise:** Gaussian N(0;1); semi-real: heavy-tailed noise resampled from residual of HIV drug response (excess kurtosis 9.24) rescaled to variance 1; **replicates:** 600 trials (main); 200 trials (sweeps over k;A;rho); 1000 trials (heavy-tailed noise)
- **Metrics:** FDR (nominal q=20%); power (TPR); mean over trials
- **Competitors:** knockoff; knockoff+ (equi-variant and SDP constructions); BHq (Benjamini-Hochberg on OLS p-values; also log-factor and whitened-noise variants)
- **Real data:** HIV-1 drug resistance (Rhee et al.): PI n=846 p=209; NRTI n=634 p=287; NNRTI n=745 p=319 (design binary mutation indicators; response log-fold drug resistance; validated against treatment-selected mutation panels); Sec 4
- **Code/data:** R package knockoff (CRAN) and Matlab package
- *Source pages:* Sec 3.3.1 p18-19; Sec 3.3.2 pp 19-21 Figs 3-5; Sec 4 pp 23-26 HIV; Sec 4.1 simulation heavy-tailed noise; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Candes2018
Candes E; Fan Y; Janson L; Lv J. Panning for gold: model-X knockoffs for high-dimensional controlled variable selection; Journal of the Royal Statistical Society Series B 80(3):551-577 (2018). **10.1111/rssb.12265; arXiv:1610.02351**

- **X:** AR1(rho varied up to 0.9; 0.3; 0.5); iid-N(0;1/n); real-X+real-y; binary/SNP-genotypes. Sec 5: X_ij~N(0;1/n) iid or iid rows with AR(1) columns with autocorrelation on x-axis (marginal var 1/n); Gaussian knockoffs via SDP/ASDP; Sec 5.3 comparison with conditional randomisation test n=400 p=600 AR(1) rho=0.3 binomial; Sec 6 robustness (estimated covariance; overfitting; AR(1) rho=0.3 n=800 p=1500 binomial); Sec 7 real WTCCC SNPs: Gaussian knockoffs using Wen-Stephens shrunk covariance (HapMap CEU genetic distances) per chromosome on clustered SNP representatives (cluster correlation cut 0.5); Sec 6.3 semi-synthetic: real WTCCC chr-1 SNPs (29258 covariates; ~1400 unique samples+1000 shared; 14708 pooled samples from 7 disease/control groups) with simulated logistic response 60 nonzero (amplitude varied; 10 conditional models per amplitude)
- **n:** n=3000 (p=1000 and 6000); n=500 (p=200; null p-value study); n=5000 (p=2000); n=300 (p=1000); n=400 (p=600); n=800 (p=1500); WTCCC n=4913 (p=377749)
- **p (max):** 3.8e5 (real; WTCCC Crohn SNPs p=377749); simulations up to p=6000
- **s0:** ||beta||_0=60 (n=3000); 40 (n=400); 20 (n=500 null study); 50 (n=800); E||beta||_0=60 (n=300)
- **β / SNR:** nonzero beta equal magnitude random signs on random locations (amplitude varied along x-axis); Gaussian noise sigma^2=1; binomial logit model for binary responses; sparse random beta N(0;sd) with E|supp|=60 in misspecification study
- **Noise:** Gaussian N(0;1); binomial logistic; **replicates:** 200 replications per point (10000 replications in null p-value study; 200 in most figures)
- **Metrics:** FDR; power (TPR); null p-value distribution (non-uniformity of MLE p-values); runtime; sensitivity to estimated covariance
- **Competitors:** MX knockoffs with LCD (lasso coefficient difference) statistic; fixed-X knockoffs; BHq on marginal p-values; BHq on MLE p-values (n>p); conditional randomisation test (small case)
- **Real data:** WTCCC Crohn's disease case-control (1917 cases + 2996 controls; p=377749 SNPs; chromosome-wise knockoffs with SNP clustering to representatives; target FDR 10%; 10 reruns; 18 discoveries vs 9 in original WTCCC analysis)
- **Code/data:** R package knockoff (CRAN); Appendix F data preprocessing
- *Source pages:* Sec 5 (5.1-5.3) pp 11-15 Figs 1-6; Sec 5.4 correlation Fig 7; Sec 6 Fig 8-9; Sec 7 genetic analysis Crohn pp 22-26; Appendix C and F; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Sesia2019
Sesia M; Sabatti C; Candes EJ. Gene hunting with hidden Markov model knockoffs; Biometrika 106(1):1-18 (2019). **10.1093/biomet/asy033; arXiv:1706.04677**

- **X:** other (discrete Markov chain K=5); other (HMM K=9 latent clock chain); binary/SNP-genotypes. 6.1 Markov chain: p=1000; states {-2..2}; Q_j(k|l)=1/K+gamma_j(1-1/K) if k=l; gamma_j~U[0;0.5]; 6.2 HMM: latent chain 'clockwise' K=9 stay prob 0.9 move 0.1; emissions gamma=0.35; 6.3 real WTCCC chr-1 SNPs 29258 (14708 individuals) pruned by clustering (corr<=0.5) to 5260 representatives; HMM fit by fastPHASE K=12 on 10 folds; Sec 7 real GWAS: single-linkage SNP clustering (max corr<=0.5) then representative chosen on 20% holdout
- **n:** n=1000 (p=1000; Markov and HMM sims); n=14,708 genotyped individuals (1000 held out for representative selection) (real chr-1 SNPs p=5260 after clustering); real GWAS n=4644-5302 (NFBC) and 4913 (WTCCC)
- **p (max):** 3.8e5 (real GWAS WTCCC p=377749; NFBC p=328934 pre-clustering; 59005 and 71145 post-clustering); sims p=1000
- **s0:** 60 nonzero (all simulations)
- **β / SNR:** Y|X~Bernoulli(logit(X'beta)) with beta_j=a/sqrt(n) on 60 support variables (signal amplitude a varied e.g. a=10 Markov; a=6 HMM); lasso (l1 logistic; CV) feature importance W_j=|b_j(lambda_CV)|-|b_{j+p}(lambda_CV)|; FDR target alpha=0.1
- **Noise:** Bernoulli/binomial logistic (binary response); quantitative traits (NFBC) analysed with lasso after log-transform and PC adjustment; **replicates:** 100 independent replications (Figs 5;8); 10 folds x 10 repeats = 100 point estimates (real-SNP sim Fig 11)
- **Metrics:** power; FDP/FDR (target 10%); number of discoveries; replication of findings against larger meta-analyses; robustness to estimated HMM parameters (misspecification nu)
- **Competitors:** HMM knockoffs (true parameters and fastPHASE-estimated); Gaussian knockoffs (Candes et al 2018) in some comparisons; marginal/conventional GWAS (WTCCC 2007)
- **Real data:** NFBC (n=4644-5302 per trait HDL LDL TG height; p=328934 -> 59005 clusters); WTCCC Crohn disease (1917 cases + 2996 controls; p=377749 -> 71145); also UK Biobank mention
- **Code/data:** software KnockoffZoom/SNPknock R package (CRAN SNPknock)
- *Source pages:* Sec 6.1-6.3 pp 14-21 (Figs 5-11; Tables 1-3); Sec 7.1 pp 22-24 (datasets; Table 4); *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Sesia2021
Sesia M; Bates S; Candes E; Marchini J; Sabatti C. False discovery rate control in genome-wide association studies with population structure. Proc Natl Acad Sci USA 118(40) e2105841118 (2021). **10.1073/pnas.2105841118**

- **X:** real-X(synthetic beta); binary/SNP-genotypes (phased haplotypes). UK Biobank phased haplotypes of 489,000 individuals (487,297 genotyped and phased subjects; includes related individuals and diverse ancestries) at 592,000 genotyped SNPs on chromosomes 1-22; autosomes partitioned into contiguous groups by complete-linkage clustering at seven resolutions (single SNP up to 425 kb); HMM-type haplotype knockoffs
- **n:** ~489,000 (all UKB); subsets for ancestry/relatedness robustness
- **p (max):** 592,000 SNPs (genome-wide simulation with real genotypes)
- **s0:** 4,000 causal variants in 2,000 loci of 100 kb (2 causal per locus) uniformly across the genome
- **β / SNR:** homoscedastic linear model; total heritability varied as a control parameter (values read from Fig 4 not captured in text); effect-size distribution not recovered from main text (see SI)
- **Noise:** Gaussian; **replicates:** not stated in main text (curves over heritability grid)
- **Metrics:** power = proportion of 2,000 causal loci covered by at least one discovery; FDP (fraction of findings with no causal variant); resolution (median width of findings); number of true discoveries at multiple resolutions
- **Competitors:** BOLT-LMM (FWER 5e-8; heuristic FDR; oracle FDP calibration) with PLINK clumping
- **Real data:** UKB 4 continuous traits (height BMI platelets SBP) and 4 diseases (CVD respiratory hyperthyroid diabetes); 487,000 samples; 208-kb resolution at FDR 10%; comparison with GWAS Catalog Japan Biobank FinnGen
- **Code/data:** https://msesia.github.io/knockoffgwas/ (C++ program + R; takes BGEN haplotypes); UKB by application 27837
- *Source pages:* Results: Application to the UK Biobank Data: Preprocessing; Analysis of Simulated Phenotypes (Fig 3-4); Analysis of UK Biobank Phenotypes (Table 1); Materials and Methods; *read level:* full-text (SI Appendix not read); *scout file:* `S3_GENOMICS.tsv`


## screening

### FanLv2008
Fan J; Lv J. Sure independence screening for ultrahigh dimensional feature space (with discussion); Journal of the Royal Statistical Society Series B 70(5):849-911 (2008). **10.1111/j.1467-9868.2008.00674.x; arXiv:math/0612857**

- **X:** iid-N(0;I); other (Sim II: sprandsym covariance block + shifted copies); equicorr(rho=0;0.1;0.5;0.9). Sim I iid N(0;1); Sim II first s predictors N(0;A) with A random SPD (sprandsym; condition number n/log n); X_i=Z_i+r X_{i-s} (i=s+1..2s) and X_i=Z_i+(1-r)X_1 (i>2s) with r=1-4logn/p or 1-5logn/p; ISIS examples I-III: sigma_ii=1 sigma_ij=rho (equicorr) with rho in 0;0.1;0.5;0.9 and X4 built to be marginally uncorrelated with Y (Y=5X1+5X2+5X3-15 sqrt(rho)X4+eps) and X5 weak; leukemia real
- **n:** n=200 (p=1000); n=800 (p=20000); ISIS: n=20;50;70 with p=100;1000
- **p (max):** 2e4 (grid 100;1000;20000; max-correlation illustration p=1000 vs 5000)
- **s0:** s=8 (n=200); s=18 (n=800); II: s=5;8;14; ISIS: 3;4;5
- **β / SNR:** Sim I nonzero beta=(-1)^u(a+|z|) with u~Bern(0.4); z~N(0;1); a=4logn/sqrt(n) (n=200) or 5logn/sqrt(n) (n=800); sigma=1.5; ||beta||=6.795;8.908; Sim II sigma=(1;1.5;2) and a=2logn/sqrt(n) or 4logn/sqrt(n); ||beta||=3.3;6.8;7.3; ISIS examples beta=(5;5;5;...) sigma=1
- **Noise:** Gaussian sigma=1 to 2; **replicates:** 200 data sets per model (Tables 1;2;4-6); 500 simulations for Figs 5-6 (min model size)
- **Metrics:** minimum model size needed to include true model (sure screening); median selected model size; median estimation error ||beta_hat-beta||_2; probability SIS/lasso/ISIS include the true model
- **Competitors:** Dantzig selector; lasso (LARS); SIS-SCAD; SIS-DS; SIS-DS-SCAD; SIS-DS-AdaLasso; ISIS (iterative SIS)
- **Real data:** Leukemia (Golub 1999; 7129 genes; n=72; 38 train 34 test) for classification via SIS-SCAD-LD and SIS-SCAD-NB; also colon/other in Sec 3.3.3
- **Code/data:** none stated
- *Source pages:* Sec 3.3 pp 14-18 (Sim I-II; Tables 1-2; Leukemia 3.3.3); Sec 4.2 pp 20-24 (ISIS examples I-III; Tables 4-6); Fig 1 p4 and Fig 4; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Wang2016
Wang X; Leng C. High dimensional ordinary least squares projection for screening variables; Journal of the Royal Statistical Society Series B 78(3):589-611 (2016). **10.1111/rssb.12127; arXiv:1506.01782**

- **X:** iid-N(0;I); equicorr(rho=0.3;0.6;0.9); AR1(rho=0.3;0.6;0.9); factor(k=2;10;20); block (group structure; delta^2=0.01;0.05;0.1); other (extreme correlation). Six examples from Fan-Lv 2008/Wang 2009/Zou-Hastie 2005/Meinshausen-Buhlmann 2010: (i) independent; (ii) compound symmetry rho; (iii) AR cov=rho^|i-j| (Tibshirani modified); (iv) factor model x_i=sum phi_j f_ij+eta_i; (v) group: x_{1+3m}=z1+N(0;delta^2) etc.; 15 true variables in three groups (m=0..4); (vi) extreme correlation: important x_i=(z_i+w_i)/sqrt2; unimportant x_i=(z_i+sum_{j<=5} w_j)/2 and two near-copies of each true predictor (eps var 0.01); screening by selecting sub-model of size n
- **n:** (p;n)=(1000;100) and (10000;200); Simulation II n=50..500 with p=4 floor(exp(n^(1/3))) (up to ~1.1e4) or 20 floor(exp(n^(1/4))) for example vi; real n=120
- **p (max):** 1.9e4 (p=1000; 10000; Simulation II p up to ~1.1e4; real Scheetz data p=18976 reduced to top 5000 by variance)
- **s0:** s=5 (ii-iii-iv-vi: beta_i=5 for i=1..5; or beta1=3;beta4=1.5;beta7=2 for AR); s=15 (group; beta=3); (i) beta=(-1)^u(|N(0;1)|+4logn/sqrt(n)) u~Ber(0.4); Simulation II s=floor(n^(1/4))*(1.5 or 1)
- **β / SNR:** R^2=var(x'beta)/var(y) set to 50% (low) or 90% (high) by adjusting sigma^2; Simulation I; also x5 marginally uncorrelated with y example y=5x1+5x2+5x3+5x4-20 rho x5+eps
- **Noise:** Gaussian N(0;sigma^2) with sigma^2 from R^2; **replicates:** 200 data sets (p=1000); 100 data sets (p=10000); 50 data sets per n in Simulation II; 200 for the x5 example
- **Metrics:** probability of including the true model in sub-model of size n (coverage); #FNs; #FPs; coverage %; exact recovery % (min_{S}|b|>max_{not S}|b|); model size; ||beta_hat-beta||_2; computation time (Table 2 for p=10000 n=200)
- **Competitors:** HOLP; SIS (Fan-Lv); RRCS (robust rank correlation); ISIS; forward regression FR; tilting; (Table 2: lasso; SCAD; ISIS-SCAD; SIS-SCAD post-screening models)
- **Real data:** Scheetz et al. 2006 rat eye tissue gene expression (n=120; 18976 probe sets -> top 5000 highest-variance genes); response TRIM32 gene expression; 'A real data application' Sec 4.5
- **Code/data:** R packages SIS and tilting used; own R code for forward regression; own R code for forward regression and fast XtY; HOLP code availability not verified
- *Source pages:* Sec 4.1 pp 12-15 (six examples; Tables 1-2); Sec 4.2 pp 16-17 (Fig 3); Sec 4.3-4.4 timing; Sec 4.5 pp 20-21 real data; *read level:* full-text; *scout file:* `S2_FREQ.tsv`


## fine-mapping/GWAS

### Hormozdiari2014
Hormozdiari F; Kostem E; Kang EY; Pasaniuc B; Eskin E. Identifying causal variants at loci with multiple signals of association. Genetics 198(2) 497-508 (2014). **10.1534/genetics.114.167908**

- **X:** real-LD-based z-score simulation (multivariate normal from WTCCC CAD LD); HapGen-simulated haplotypes (1000 Genomes EUR); binary/SNP-genotypes. (i) summary-statistic simulation: 35 SNPs in 200kb windows around rs10962894 and rs4740698 (WTCCC CAD), z-scores drawn from multivariate normal with LD covariance, causal-SNP power 50% at alpha=1e-8; (ii) HapGen from 1000G European, regions of 50 SNPs, 1-3 causal SNPs implanted, case-control, t-test marginal statistics
- **n:** not stated for HapGen case-control (sample-size effect in Fig S1)
- **p (max):** 50 SNPs per region (35 in z-score simulation)
- **s0:** 1;2;3 causal SNPs (max 6 assumed by method)
- **β / SNR:** noncentrality parameter set so power at causal SNP = 50% at genome-wide significance alpha=1e-8; Fisher polygenic NCP~N(0,sigma^2) option
- **Noise:** MVN z-scores / case-control sampling; **replicates:** 1000 simulation panels (z-score sim); HapGen simulations count not recovered in text read
- **Metrics:** recall rate (fraction of simulations where all true causal SNPs are in the rho=95% causal set); size of causal set; rank of causal SNP
- **Competitors:** top-k by association; conditional method (CM); single-causal posterior (1-Post; Maller 2012); extended ECM and E1-Post
- **Real data:** CHI3L2 locus (gene expression phenotype; Malo 2008 statistics; HapMap CEU 57 individuals LD)
- **Code/data:** CAVIAR software (github fhormoz/caviar)
- *Source pages:* Results: Simulations sections (Figures 1-5), CHI3L2 section, Materials and Methods; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Kichaev2014
Kichaev G; Yang WY; Lindstrom S; Hormozdiari F; Eskin E; Price AL; Kraft P; Pasaniuc B. Integrating functional data to prioritize causal variants in statistical fine-mapping studies. PLoS Genet 10(10) e1004722 (PAINTOR) (2014). **10.1371/journal.pgen.1004722**

- **X:** genotypes simulated with HAPGEN from 1000 Genomes; 100 risk loci of 10 Kb each (also variable locus sizes up to 100 Kb in Table 3); expedited variant draws Z-scores directly from MVN with reference LD. N=10,000 samples; 100 loci; SNPs per locus not stated in the text read (10 Kb loci); 64 loci on average harbor a causal variant; 3 synthetic annotations covering 2.2%, 2.2%, 30.7% of SNPs with causal enrichment 9.5, 5.7, 3.65
- **n:** 10000
- **p (max):** not stated (100 loci x 10 Kb each; 100 Kb loci in masking and size experiments)
- **s0:** logistic prior giving about 100 causal variants in total across 100 loci (109.2 true causals per simulation in the credible-set table)
- **β / SNR:** variance explained by the 100 loci fixed at 0.25 (value read from text of Table/Fig 3 methods); multiple causal SNPs per locus allowed
- **Noise:** summary Z-scores from MVN approximation with LD (Z ~ N(Sigma*lambda; Sigma)); **replicates:** 500 simulations (Table 1 and rho-level confidence sets); loci-size experiment used Z-score shortcut
- **Metrics:** average number of SNPs per locus to select to find 50% and 90% of causal variants; rho-level (90%,95%,99%) causal set sizes; enrichment estimation accuracy; utility (benefit-cost) curves
- **Competitors:** PAINTOR single-causal and no-annotation variants; fgwas (with and without annotations); CAVIAR; marginal p-value ranking; CAVIARBF-style approaches in Table S1
- **Real data:** Teslovich 2010 lipid GWAS meta-analysis (HDL/LDL/TC/TG) 37+ risk loci with dense imputation; 450 ENCODE cell-type annotations
- **Code/data:** PAINTOR software (Pasaniuc lab; github.com/gkichaev/PAINTOR_V3.0 is a later version, not verified in this paper text)
- *Source pages:* Results (simulations); Methods (simulation setup; Z-score model); Table 1-3; *read level:* full-text (PMC HTML); *scout file:* `S3_GENOMICS.tsv`

### Chen2015
Chen W; Larrabee BR; Ovsyannikova IG; Kennedy RB; Haralambieva IH; Poland GA; Schaid DJ. Fine mapping causal variants with an approximate Bayesian method using marginal test statistics. Genetics 200(3) 719-736 (2015). **10.1534/genetics.115.176107**

- **X:** real-LD haplotype simulation (HAPGEN2 from 1000G CEU); binary/SNP-genotypes; also independent-SNP control sim. HAPGEN2 with 1000 Genomes CEU reference; each dataset a random region of 35 common SNPs (MAF>0.05) on chr8; 2000 individuals (1000 cases + 1000 controls for binary traits); LD from simulated data
- **n:** 2000
- **p (max):** 35 SNPs per region (timing study varies p up to a few hundred with l=3-5)
- **s0:** 1 to 5 causal SNPs chosen randomly
- **β / SNR:** beta~N(0,1) quantitative or N(0,0.5^2) binary; accepted only if marginal noncentrality parameters in (30.457,61.856) i.e. power 0.527-0.992 at alpha=5e-8
- **Noise:** Gaussian (quantitative) / Bernoulli (binary); **replicates:** 100 simulated data sets per number of causal SNPs
- **Metrics:** proportion of causal SNPs included vs number of top-PIP SNPs selected; average number of SNPs needed to include 50 pct and 90 pct of causal SNPs (Table 1); confidence-set coverage; runtime vs p (Fig 7)
- **Competitors:** BIMBAM; PAINTOR; ENET (elastic net); LASSO (lars)
- **Real data:** Smallpox vaccine IFN-alpha GWAS: San Diego cohort (488 Caucasian, Illumina HumHap550 imputed 1000G) and US cohort (713, Omni2.5S) region fine-mapping
- **Code/data:** CAVIARBF R/C++ package (github; Chen)
- *Source pages:* Methods: Data simulation and evaluation; Results Fig 2 Table 1, Fig 7 timing; real-data section; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Benner2016
Benner C; Spencer CCA; Havulinna AS; Salomaa V; Ripatti S; Pirinen M. FINEMAP: efficient variable selection using summary data from genome-wide association studies. Bioinformatics 32(10) 1493-1501 (2016). **10.1093/bioinformatics/btw018**

- **X:** real-X(synthetic beta); binary/SNP-genotypes. Real genotypes of 18,834 individuals (National FINRISK); 500kb region around rs11591147 (PCSK9) with 1920 polymorphic SNPs (|r|<0.99); sub-regions of m SNPs; causal SNPs chosen among variants with high-LD proxies (|r|>0.5) to stress search; summary stats (z-scores, correlation matrix) from the simulated data
- **n:** 18834
- **p (max):** 1920 SNPs in region (m=750;1000;1250;1500 in scenario A; m=150 in scenario B); real data 363 and 8612 SNPs
- **s0:** 5 causal SNPs (scenarios A and B)
- **β / SNR:** effect sizes set so single-SNP power at 5e-8 is about 0.5; sigma^2=1-sum 2 f_c(1-f_c) beta_c^2 (unit phenotype variance); causal SNPs random among those with correlated proxies
- **Noise:** Gaussian; **replicates:** 500 datasets per (m,K) combination in scenarios A and B (2500 datasets in total in scenario B (K=1..5))
- **Metrics:** processing time (log10 scale); max abs difference of single-SNP inclusion probabilities vs CAVIARBF; proportion of causal SNPs captured among top-ranked SNPs by PIP
- **Competitors:** CAVIARBF (exhaustive search); PAINTOR; CAVIAR (discussed)
- **Real data:** 4q22/SNCA Parkinson (UKPDC and WTCCC2): 2Mb 363 genotyped SNPs; 15q21/LIPC HDL-C FINRISK n=19115: 6Mb 8612 SNPs
- **Code/data:** FINEMAP software (www.christianbenner.com); FINRISK data restricted
- *Source pages:* Sec 4 Results (simulation scenarios A and B); Sec 4.3-4.4 real data; Discussion; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Wen2016
Wen X; Lee Y; Luca F; Pique-Regi R. Efficient integrative multi-SNP association analysis via deterministic approximation of posteriors. Am J Hum Genet 98(6) 1114-1129 (2016). **10.1016/j.ajhg.2016.03.029**

- **X:** real-X(synthetic beta); binary/SNP-genotypes. Real GEUVADIS genotypes of 343 European individuals; Sim 1 (enrichment): 1,500 random genes x 50 cis-SNPs each with 20% annotated by a binary feature, QTN status Bernoulli with logit(-4+alpha1*d); Sim 2 (exactness check): p=15 neighbouring cis-SNPs per gene so that 2^15 models can be enumerated
- **n:** 343
- **p (max):** 50 SNPs per gene (sim 1); 15 (sim 2); real data: 100 kb bins around TSS (GEUVADIS) and 2Mb cis regions (GTEx 44 tissues)
- **s0:** sim 2: 1-5 QTNs uniformly; sim 1: random with prior prob exp(-4+a1 d)/(1+exp(-4+a1 d))
- **β / SNR:** QTN effect ~ N(0,0.6^2); residual variance 1; enrichment alpha1 varied 0.00-1.00
- **Noise:** Gaussian sigma^2=1; **replicates:** 100 datasets per alpha1 value (sim 1); 1250 datasets (sim 2)
- **Metrics:** bias and SE of enrichment estimate alpha1; ratio C*/C of approximate vs exact normalising constant; RMSE of approximate PIPs vs exact; runtime (EM 21 min vs MCMC 84 h on 11,838 genes)
- **Competitors:** exact Bayesian enumeration; adaptive DAP vs DAP-1; MCMC; best-case logistic regression on true status
- **Real data:** GEUVADIS cross-population eQTL (re-analysis, 11,838 genes); GTEx cis-eQTL 44 tissues with TF-binding annotations
- **Code/data:** DAP software github.com/xqwen/dap; data portals GEUVADIS and GTEx
- *Source pages:* Results: Simulation Studies (Fig 1-2; Tables 1-2); Real data applications; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Wang2020
Wang G.; Sarkar A.; Carbonetto P.; Stephens M.; A simple new approach to variable selection in regression with application to genetic fine mapping (SuSiE); J. R. Stat. Soc. B; 82(5); 1273-1300 (2020). **10.1111/rssb.12388 (bioRxiv 10.1101/501114)**

- **X:** real-X(synthetic beta) (GTEx genotypes n=574; real LD). Real GTEx human genotype matrices for 150 randomly chosen genes: SNPs near transcribed region; median number of other variables with |corr|>0.9 is 8 (mean 26) and >0.99 is 1; scenario 1: p=1000 SNPs; scenario 2: p=3000 to 12000 SNPs; SuSiE L=10 (scenario 1) and L=20 (scenario 2); sigma_0l^2=0.1 var(y) fixed; X columns standardised
- **n:** 574 (simulations); 87 (splice QTL real data); 100000 (timing: n=1e5;p=500); 1000 (timing: n=1000;p=50000)
- **p (max):** 12000 (scenario 2; p grid 1000;3000-12000); timing demonstration p=50000 (n=1000)
- **s0:** S in {1;...;5} (scenario 1); S=10 (scenario 2)
- **β / SNR:** S effect indices uniform at random; b_j~N(0;0.6^2); sigma^2 solved to achieve PVE phi=var(Xb)/(sigma^2+var(Xb)) in {0.05;0.1;0.2;0.4} (scenario 1); S=10; phi=0.3 (scenario 2)
- **Noise:** Gaussian with sigma^2 set from target PVE phi; **replicates:** Scenario 1: 2 replicates per gene per (S;phi) combination = 6000 datasets (150 genes x 5 x 4 x 2); scenario 2: 2 per gene = 300 datasets
- **Metrics:** power and FDR of PIPs (PIP-threshold); credible set (CS) coverage; CS size (purity); power of CSs; calibration; run time
- **Competitors:** SuSiE (L=10;20); DAP-G; CAVIAR (S<=3 only); FINEMAP (S<=3 only); hierarchical testing (Mandozzi-Buhlmann); lasso (timing)
- **Real data:** Splice QTL (Li et al 2016; 87 Yoruban LCLs; 77345 intron ratios; ~600 SNPs per intron within 100kb; n=87;p~600)
- **Code/data:** R package susieR https://github.com/stephenslab/susieR; analysis code on github stephenslab
- *Source pages:* Sec 4 (pp 13-17) Figs 1-3 Table 2; Sec 5 (p19-20); appendix D; *read level:* full-text; *scout file:* `S1_BVS.tsv`

### Weissbrod2020
Weissbrod O; Hormozdiari F; Benner C; Cui R; Ulirsch J; Gazal S; et al. Functionally informed fine-mapping and polygenic localization of complex trait heritability. Nat Genet 52(12) 1355-1363 (2020). **10.1038/s41588-020-00735-5**

- **X:** real-X(synthetic beta); binary/SNP-genotypes. Real UK Biobank genotypes N=337,491 unrelated British; genome-wide 18,212,157 imputed SNPs (MAF>=0.001; INFO>=0.6; includes indels) used for estimating priors; 10 loci of 3Mb on chr1 with 1,468-27,784 SNPs each fine-mapped; summary statistics from N=320K; in-sample LD via LDstore; mismatched-LD sims use up to N=44K targets and reference panels
- **n:** 337491 (320K sumstats); up to 44K (mismatched LD sims); 293K subset
- **p (max):** 1.82e7 (genome-wide SNPs for prior-estimation); 27,784 per fine-mapped locus (3Mb)
- **s0:** 10 causal SNPs per locus (0.05% of heritability jointly); genome-wide causal proportion 0.5%
- **β / SNR:** trait heritability h2=25%; genome-wide proportion causal 0.5%; effect variance var[beta_i|a_i] from baseline-LF v2.2.UKB annotation model (tau from meta-analysis of 16 UKB traits); SNP causal with probability proportional to var[beta_i|a_i]
- **Noise:** Gaussian (summary statistics); **replicates:** not recovered from main text (aggregated over simulated loci; Supplementary Note)
- **Metrics:** calibration (FDR among PIP>thr, estimated as 1-thr; aggregated); power (number of variants with PIP>0.95); computational cost; Wald test with jackknife over datasets
- **Competitors:** SuSiE; FINEMAP; CAVIARBF (max 1 or 2 causal); fastPAINTOR; PolyFun+SuSiE; PolyFun+FINEMAP (10 methods in Table 1)
- **Real data:** UK Biobank 49 traits (avg N=318K) with BOLT-LMM sumstats; 2,763 overlapping 3Mb loci genome-wide; 3,025 fine-mapped variant-trait pairs PIP>0.95
- **Code/data:** https://github.com/omerwe/polyfun; susieR; FINEMAP; UKB sumstats public
- *Source pages:* Results: Main simulations; Simulations with mismatched reference LD (Table 3); Methods: Main fine-mapping simulations; Mismatched reference LD sims; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Zou2022
Zou Y; Carbonetto P; Wang G; Stephens M. Fine-mapping from summary data with the Sum of Single Effects model. PLoS Genet 18(7) e1010299 (2022). **10.1371/journal.pgen.1010299**

- **X:** real-X(synthetic beta); binary/SNP-genotypes. UK Biobank imputed genotypes; 200 random autosomal regions of about 1000 SNPs each (390 kb average; on average 30 SNPs with r>0.9 and 14 with r>0.99 to another SNP); X = genotypes of 50,000 random UKB samples; LD matrix options: in-sample (50k) or out-of-sample from non-overlapping reference panels of 500 or 1000 individuals; toy allele-flip example with 1002 SNPs
- **n:** 50000 (PVE 0.5%); 2500 (PVE 10%); 800 (PVE 30%)
- **p (max):** about 1000 per region (390kb avg)
- **s0:** 1;2;3 causal variants
- **β / SNR:** total PVE 0.5% (main), 10% (N=2500), 30% (N=800) so that all settings have similar power; effect sizes from multiple regression model (1)
- **Noise:** Gaussian; **replicates:** 200 regions x 3 values of S = 600 datasets per PVE setting
- **Metrics:** power vs FDR curves (PIP threshold varied; points at 0.95); 95% CS coverage; CS power; median CS size; median purity (min abs correlation); runtime Table 2
- **Competitors:** FINEMAP; DAP-G; CAVIAR; SuSiE (individual-level, in-sample baseline); variants L=true vs larger, estimated vs fixed residual variance, refinement on/off
- **Real data:** none for benchmarking (only toy allele-flip illustration)
- **Code/data:** https://github.com/stephenslab/dsc_susierss (also on Zenodo); UK Biobank genotypes by application
- *Source pages:* Results: Simulations using UK Biobank genotypes; Fig 2-6; Table 2; Data Availability; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Cui2024
Cui R; Elzur RA; Kanai M; Ulirsch JC; Weissbrod O; Daly MJ; Neale BM; Fan Z; Finucane HK. Improving fine-mapping by modeling infinitesimal effects. Nat Genet 56(1) 162-169 (2024). **10.1038/s41588-023-01597-3**

- **X:** real-X(synthetic beta); binary/SNP-genotypes. UK Biobank imputed genotypes: ideal sims use true-genotype draws from imputed probabilities (to mimic imputation noise, GWAS then run on dosages) for 149,630 (or 366K/100K) white British individuals; causal variants drawn from 6.6 million common (MAF>=1%) imputed variants genome-wide; BOLT-LMM GWAS; loci fine-mapped in 3Mb windows; misspecification sims add non-sparse effects/stratification/missing causal/non-uniform causal probs
- **n:** 149,630 (misspecification sims); 366K and two 100K subsamples (RFR ideal sims)
- **p (max):** 6.6e6 common imputed variants genome-wide (causal variants drawn from these; fine-mapping done per 3Mb locus)
- **s0:** 1000 causal (ideal RFR sims) or 700 (N=150K ideal); misspecified: 1434 sparse large-effect variants from SuSiE posterior for UKB height plus non-sparse x%=0.5;1;5 of variants
- **β / SNR:** total SNP heritability 0.5; ideal: beta~N(0,0.5/1000) on standardized genotypes and error N(0,0.5); non-sparse effects variance proportional to [2p(1-p)]^alpha with alpha=-0.38; non-sparse share of heritability 58;75;83;100 percent (1% coverage), 0.5% and 5% coverage settings
- **Noise:** Gaussian; **replicates:** ideal RFR: two sets at each of N=366K and N=100K; 10 misspecification simulation sets (Table 1 caption: ten sets) (Table 1) over whole genome loci
- **Metrics:** Replication Failure Rate (down-sampling PIP>0.9 at N=100K vs PIP<0.1 at 366K); calibration of PIP bins with Wilson CI; recall of simulated large effects among top-N PIP variants; runtime; PRS performance; functional enrichment
- **Competitors:** SuSiE; FINEMAP; COJO-ABF; ABF; SuSiE-inf; FINEMAP-inf; minPIP and minPIP-inf
- **Real data:** 10 UKBB quantitative traits (Height eBMD Plt HbA1c RBC ALP IGF1 LDLC Lym eGFR) N=366K vs 100K down-sampling
- **Code/data:** results Zenodo 10.5281/zenodo.7055906; software github.com/FinucaneLab/fine-mapping-inf; analysis code github.com/cuiran/improve-fine-mapping; UKB genotypes by application
- *Source pages:* Results: Simulations (Fig 2-3 Table 1); Methods: Large-scale simulations with misspecification; Simulated genotypes; Causal variants simulation; ideal simulations for RFR; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### McCreight2025
McCreight A; Cho Y; Li R; Nachun D; Gan H; Carbonetto P; Stephens M; Denault W; Wang G. SuSiE 2.0: improved methods and implementations for genetic fine-mapping and phenotype prediction. bioRxiv preprint (2025). **10.1101/2025.11.25.690514**

- **X:** real UK Biobank genotypes; 150 randomly sampled LD blocks across chr1-22; MAF>1%, missing<5% (mean imputation); standardized. n=1000 and p=5000 per block (main); runtime study p=500;1000;2500 (RSS with regularized LD); regional only, no genome-wide p
- **n:** 1000
- **p (max):** 5000
- **s0:** sparse: K=1-5 causal (beta_j=1, uniformly random positions); complex: 3 sparse + 5-10 oligogenic (2-component Gaussian mixture) + polygenic background (about 15 variants or all remaining variants)
- **β / SNR:** sparse: per-SNP h2=0.03 so total h2={0.03;0.06;0.09;0.12;0.15} for K=1..5 (text lists four values); complex: total PVE h2g=0.25 split 50% sparse/35% oligogenic/15% polygenic (scenarios 2 and 1), or 50/15/35 (extensive infinitesimal)
- **Noise:** Gaussian N(0;sigma^2 I) with sigma^2 set to hit target h2; **replicates:** 150 data sets per scenario (one per sampled LD block)
- **Metrics:** 95% CS power and FDR (top-N-as-causal for complex designs); variant-level ROC at 5% FPR; PIP calibration; 5-fold CV prediction R2 (TWAS proxy); CS size and purity; runtime (SuSiE-RSS v1 vs v2)
- **Competitors:** SuSiE; SuSiE-ash (new); SuSiE-inf; attainable coverage (SparsePro) and Bayesian LP tested in supplement
- **Real data:** ROSMAP (Religious Orders Study and Memory and Aging Project) molecular QTL data analysed with xqtl-protocol and pecotmr (details not in the main text read)
- **Code/data:** https://github.com/stephenslab/susieR; https://github.com/StatFunGen/simxQTL; https://github.com/alexmccreight/susieR2.0-paper; https://github.com/StatFunGen/xqtl-protocol; https://github.com/StatFunGen/pecotmr
- *Source pages:* Results; Supplementary Notes S.4 Simulation Study Details; Figs 1 S1-S6 captions (bioRxiv full-text HTML); *read level:* full-text (HTML); real-data section only skimmed; *scout file:* `S3_GENOMICS.tsv`


## review/benchmark

### FanLv2010
Fan J; Lv J. A selective overview of variable selection in high dimensional feature space (invited review). Preprint arXiv:0910.1122 (Sept 2009); journal version not checked against the paper text (2009). **arXiv:0910.1122**

- **X:** iid-N(0,I) (spurious-correlation illustration); equicorr(rho) (analytical examples only). Fig 1 (Section 1): spurious correlation of Z1 with other variables, n=50, p=1000 and p=10000, 1000 simulations, max absolute sample correlation and max absolute multiple correlation with 5 other variables via stepwise addition. Section 4.5: analytical equicorrelation counterexamples (hidden signature variable; false-positive example); Section 5.5: irrepresentable-condition example
- **n:** n=50 (Fig 1)
- **p (max):** 1e3;1e4 (Fig 1 spurious-correlation only)
- **s0:** not applicable (review; no regression benchmark)
- **β / SNR:** not applicable (review). Equicorr examples: Y depends on x via X1+...+XJ - J*rho*X(J+1), and Y=rho*X0+X1+...+XJ+eps
- **Noise:** not stated for Fig 1; **replicates:** 1000 simulations (Fig 1)
- **Metrics:** distribution of max absolute sample/multiple correlation (Fig 1); otherwise theory
- **Competitors:** reviewed: penalised likelihood (lasso; SCAD; MCP; adaptive lasso; Dantzig); SIS/ISIS; screening then penalise
- **Real data:** none (review; no real data set analysed)
- **Code/data:** none stated
- *Source pages:* Section 1 and Fig 1 (p. 2-3); Section 4.5 (pp. 23-24); Section 5.5; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Buhlmann2014
Buhlmann P; Kalisch M; Meier L. High-dimensional statistics with a view toward applications in biology. Annu Rev Stat Appl 1 255-278 (author preprint dated 23 May 2013) (2014). **10.1146/annurev-statistics-022513-115545**

- **X:** real-X+real-y. Riboflavin: gene expression of Bacillus subtilis, log-expression of 4088 genes normalised with affy default; n=71 homogeneous fed-batch samples from different engineered strains and fermentation conditions (dataset 'riboflavin'); grouped version riboflavinGrouped n=111 in N=28 strain groups (2-6 time points each)
- **n:** 71 (riboflavin); 111 (riboflavinGrouped)
- **p (max):** 4088
- **s0:** unknown (real); multi sample-splitting finds 1 FWER-significant gene (YXLD_at); stability selection finds more
- **β / SNR:** n/a (review with real-data illustration)
- **Noise:** n/a; **replicates:** n/a (50-100 random sample splits for p-value aggregation)
- **Metrics:** FWER-adjusted p-values; stability selection E[V]; selection frequency
- **Competitors:** multi sample-splitting; ridge projection estimator; stability selection with lasso; (mixed model for grouped data)
- **Real data:** riboflavin (n=71 p=4088; response log riboflavin production rate); riboflavinGrouped (n=111; p=4088; 28 groups)
- **Code/data:** R package hdi on CRAN (data riboflavin); also supplemental section A.1 of the paper
- *Source pages:* Section 1 Example (riboflavin); Sec 3.4 summary; grouped example in mixed-models section; *read level:* full-text (author preprint of Annu Rev paper); *scout file:* `S3_GENOMICS.tsv`

### Dezeure2015
Dezeure R; Buhlmann P; Meier L; Meinshausen N. High-dimensional inference: confidence intervals; p-values and R-software hdi; Statistical Science 30(4):533-558 (2015). **10.1214/15-STS527; arXiv:1408.4026**

- **X:** Toeplitz(rho=0.9 for Sigma); other (Exp.decay: Sigma^-1_jk=0.4^(|j-k|/5)); equicorr(rho=0.8); real-X(synthetic beta) (RealX riboflavin); block(size 20; equicorr rho varied). Toeplitz Sigma_jk=0.9^|j-k| (banded inverse); Exp.decay (Sigma^-1)_jk=0.4^(|j-k|/5) (banded Sigma); Equi.corr Sigma_jk=0.8; RealX: riboflavin Bacillus subtilis n=71 p=4088 reduced to p=500 by highest empirical variance; Block Equi.corr: block-diagonal with 20x20 equicorr blocks (group test); rows N_p(0;Sigma)
- **n:** n=100 (p=500); n in 100;200;400 (GLM comparison; p=500); riboflavin n=71
- **p (max):** 500 (p fixed; riboflavin p=4088 in real analysis)
- **s0:** s0=3 or 15 (linear); s0=3 (GLM; groups; CIs)
- **β / SNR:** 6 coefficient schemes: U(0;2); U(0;4); U(-2;2); fixed 1; 2 or 10; positions random (or first s0 columns in supplement); GLM: U(0;1);U(0;2);U(0;4); group test U[0;2];U[0;4];U[0;8]; beta-min not imposed
- **Noise:** N(0;1) (linear); binomial (GLM); **replicates:** 50 independent (X;beta;active-set positions) draws per (design;s0;coef-type) combination; each with 100 simulated responses for power/FWER; 100 CIs for coverage
- **Metrics:** power (avg P[reject H0j] over S0); family-wise error rate FWER (alpha=0.05); average number of false positives AVG(V); CI coverage and length; group-test power
- **Competitors:** multi sample-splitting; ridge projection (bias-corrected); desparsified lasso (LDPE/ZZ/JM variants); bootstrapped lasso proj; Jm2013 (Javanmard-Montanari; own implementation); covariance test; stability selection-type; group-bound
- **Real data:** Riboflavin (n=71 in hdi version; p=4088); semi-real example Fig 8 with real X and synthetic coefficients; vitamin gene expression example in R demo
- **Code/data:** R package hdi (CRAN); data riboflavin in hdi
- *Source pages:* Sec 2.5 pp 11-14 (2.5.2 Data used; 2.5.3 p-values; 2.5.4 CIs); Sec 3.3 p14; Sec 4 group inference; Figs 2-9; *read level:* full-text; *scout file:* `S2_FREQ.tsv`

### Heinze2018
Heinze G; Wallisch C; Dunkler D. Variable selection - A review and recommendations for the practicing statistician. Biometrical Journal 60(3) 431-449 (2018). **10.1002/bimj.201700067**

- **X:** iid-N(0,I) (2-variable illustration only); real-X+real-y. Fig 1: 50 simulated data sets of size N=50 with two standard normal predictors with correlation rho=0.5, to show conditional bias after selection with p-value threshold 0.157. Low-dimensional guidance paper (k<n); no high-dimensional benchmark
- **n:** N=50 (Fig 1); n=251 body fat data
- **p (max):** 2 (simulation illustration); 13 (body fat data); not high-dimensional
- **s0:** not applicable
- **β / SNR:** not applicable (illustration only); EPV (events per variable) rule discussed; recommends resampling stability analysis
- **Noise:** not stated; **replicates:** 50 data sets (Fig 1)
- **Metrics:** bootstrap inclusion frequency; relative conditional bias; root mean squared difference (RMSD) of bootstrap estimates; model selection frequencies; pairwise inclusion frequencies
- **Competitors:** backward elimination (AIC; significance 0.157); forward selection; lasso; best subset (as reviewed); resampling stability
- **Real data:** Johnson (1996) body fat data (n=251 men; 13 predictors) worked example with bootstrap stability analysis
- **Code/data:** Supporting Information on journal site (Table S2); R packages listed in Section 4 table
- *Source pages:* Abstract; Section 2 (Fig 1; Table 2); worked example (Section 3/body fat; Tables 5-6); *read level:* full-text; *scout file:* `S2_FREQ.tsv`


## other

### Scheetz2006
Scheetz TE; Kim KYA; Swiderski RE; Philp AR; Braun TA; Knudtson KL; et al. Regulation of gene expression in the mammalian eye and its relevance to eye disease. Proc Natl Acad Sci USA 103(39) 14429-14434 (2006). **10.1073/pnas.0602562103**

- **X:** real-X+real-y (data-source paper; VS use: response TRIM32 probe regressed on other probes). Whole-eye Affymetrix RAE230A expression of 120 F2 rats (SR/JrHsd x SHRSP intercross, 12-week-old males); >31,000 probes, 18,976 with sufficient signal and >=2-fold variation (the 'eye data'; later VS papers use about 18,975 probes as predictors with TRIM32 probe as response, or the flare-package version with 200 pre-screened probes); 399 genetic markers genotyped for eQTL linkage
- **n:** 120
- **p (max):** 18,976 expressed probes (>31,000 on array); 399 markers
- **s0:** unknown (real data); eQTL: 1,300 probes linked at alpha=0.001
- **β / SNR:** n/a (real data)
- **Noise:** n/a; **replicates:** n/a
- **Metrics:** n/a in source paper (ANOVA linkage; empirical FDR 2%)
- **Competitors:** n/a
- **Real data:** GEO GSE5680 (120 arrays) Expression data for an eQTL experiment in rat eye; used downstream in many VS papers (verified via web search summaries of arXiv 1311.6636, 2103.16438, 2305.04182, 1209.2160 but those papers not read in full)
- **Code/data:** GEO GSE5680 public; R packages flare (eyedata, p=200) and others
- *Source pages:* Results and Methods sections on 120 F2 rats; GEO series page GSE5680; *read level:* full-text (data-source paper and GEO record; downstream VS use not read in full); *scout file:* `S3_GENOMICS.tsv`

### Valdar2006
Valdar W; Solberg LC; Gauguier D; Cookson WO; Rawlins JNP; Mott R; Flint J. Genetic and environmental effects on complex traits in mice. Genetics 174(2) 959-984 (companion of the Nat Genet 38:879 HS-mice GWAS paper) (2006). **10.1534/genetics.106.060004**

- **X:** real-X+real-y (heterogeneous stock mice; genotype data described in the Nat Genet companion paper not opened). 2448 genetically heterogeneous stock (HS) mice (1220 F; 1228 M) descended from 8 inbred strains (A/J AKR/J BALB/cJ CBA/J C3H/HeJ C57BL/6J DBA/2J LP/J) via the Northport HS colony after 50 pseudo-random generations; pedigree-based relationship matrix (85 families in Zhou 2013); this Genetics paper reports phenotypes/covariates/heritability from pedigree not SNP data
- **n:** 2448
- **p (max):** not given in this paper (genotyped markers in Nat Genet companion; Zhou 2013 used a subset with n about 1000-2000 per phenotype split)
- **s0:** n/a
- **β / SNR:** 88 phenotypes; pedigree heritability estimated per phenotype (listed in order in Table 5); 15 covariates (sex age cage weight etc)
- **Noise:** real data; **replicates:** n/a
- **Metrics:** heritability h2 and common-environment effect from mixed model; covariate effects
- **Competitors:** n/a
- **Real data:** HS mice (n=2448; 88 traits) - widely reused testbed for genomic prediction/BVS (CD8 MCH BMI in Zhou 2013 BSLMM paper; Valdar 2006 Nat Genet GWAS paper)
- **Code/data:** phenotype/genotype data from the Wellcome Trust Centre (mus.well.ox.ac.uk) per Nat Genet paper (URL not in text read)
- *Source pages:* Introduction; Materials and Methods: Animals; Phenotypes and covariates; Table 2 and Table 5; *read level:* full-text (Genetics companion paper only; the Nat Genet GWAS paper with SNP data was not opened); *scout file:* `S3_GENOMICS.tsv`

### Atwell2010
Atwell S; Huang YS; Vilhjalmsson BJ; Willems G; Horton M; Li Y; et al. Genome-wide association study of 107 phenotypes in Arabidopsis thaliana inbred lines. Nature 465 627-631 (2010). **10.1038/nature08800**

- **X:** real-X+real-y (inbred lines; binary SNP genotypes; heavily structured population). 199 A. thaliana inbred lines (core set of 95 plus second set of 96 flowering-focused; different subsets per phenotype); custom Affymetrix 250K SNP chip; 216,130 SNPs called (error 1.6%); one SNP per ~500bp; LD extent comparable to humans; strong population structure/relatedness
- **n:** ~95-199 (199 lines overall; per-phenotype n about 96 or 192)
- **p (max):** 216,130 SNPs (250,000 on chip)
- **s0:** real data; e.g. six phenotypes with single strong peaks (FRI expression; R-gene responses RPM1 RPS2 RPS5; ACD6 lesioning)
- **β / SNR:** n/a; heritabilities 42% (aphid number) to >99%; 107 phenotypes: 23 flowering related; 23 defence; 18 element concentrations; others
- **Noise:** real data; **replicates:** n/a (simulation studies in supplement indicate power to detect similar alleles about 30-40 percent at this sample size)
- **Metrics:** Wilcoxon / Fisher / EMMA mixed-model p-values; peaks above 1e-4..1e-9; enrichment of a priori candidate genes
- **Competitors:** Wilcoxon test vs EMMA mixed model
- **Real data:** 107 phenotypes in 199 lines x 216K SNPs ('Atwell' data; FT10/flowering-time phenotypes widely reused as small-n large-p testbed; GWAPP/AraPheno host the data)
- **Code/data:** data in Supplementary; hosted at arapheno.1001genomes.org / easyGWAS (hosting URLs not in text read)
- *Source pages:* Results paragraphs on genotyped sample and phenotypes; Methods summary (genotyping and analysis); *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Bloom2013
Bloom JS; Ehrenreich IM; Loo WT; Lite TLV; Kruglyak L. Finding the sources of missing heritability in a yeast cross. Nature 494 234-237 (2013). **10.1038/nature11867**

- **X:** real-X+real-y (BYxRM yeast cross; binary segregant genotypes). Panel of 1008 prototrophic haploid segregants from a BY (lab) x RM (wine) cross; parents sequenced to define 30,594 high-confidence SNPs; per-segregant genotypes by multiplexed short-read sequencing
- **n:** 1008
- **p (max):** 30,594 SNPs (number of distinct markers after collapsing identical genotype patterns not stated in text read)
- **s0:** real: 591 QTL over 46 traits at 5% empirical FDR via stepwise forward search; 5-29 QTL per trait (median 12)
- **β / SNR:** real traits: broad-sense H2 and narrow-sense h2 estimated for 46 traits (colony size growth under different conditions); detected QTL explain 72-100% (median 88%) of h2 under 10-fold CV
- **Noise:** real data; **replicates:** n/a; 10-fold cross-validation; subsampling of panel (100 vs 1000 segregants) to illustrate sample-size dependence
- **Metrics:** heritability (H2 and h2 via genomic relatedness); QTL count at empirical FDR 5%; fraction of h2 explained (10-fold CV); pairwise QTL-QTL interactions at LOD 6.2 (FDR 10%)
- **Competitors:** single-marker linkage; stepwise forward-search multiple regression
- **Real data:** 46 growth traits in 1008 BYxRM segregants (genotypes + phenotypes in Supplementary; later used as variable-selection testbed with n~1000 and p in the thousands)
- **Code/data:** Supplementary Tables/ data from the Nature paper and the Kruglyak lab site (exact URL not shown in text read)
- *Source pages:* Main text Results paragraphs 3-9 and Figures 1-3; Methods (crosses/genotyping); *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Ge2019
Ge T; Chen CY; Ni Y; Feng YA; Smoller JW. Polygenic prediction via Bayesian regression and continuous shrinkage priors. Nat Commun 10 1776 (2019). **10.1038/s41467-019-09718-5**

- **X:** real-X(synthetic beta); binary/SNP-genotypes. UK Biobank unrelated white British; 819,941 HapMap3 SNPs after QC (MAF>=1%; missing<1%; INFO>=0.8; HWE p>1e-10; no ambiguous A/T C/G); external LD reference 1000G European N=503 (also in-sample LD N=6000 variant); validation set 3000 and independent test set 3000
- **n:** training N = 10,000; 20,000; 50,000; 100,000; validation 3000; test 3000
- **p (max):** 819,941 (HapMap3 SNPs; all used in simulations)
- **s0:** point-normal with 100;1000;10000;100000 causal variants; normal mixture 10 + 1000 + 10000 SNPs explaining 10%;20%;70% of h2
- **β / SNR:** total heritability h2=0.5 (secondary 0.2 and 0.8); effects point-normal; secondary: point-t (df 4); point-gamma (shape 2); phenotype=sum of all SNP effects plus Gaussian noise; GWAS marginal OLS
- **Noise:** Gaussian; **replicates:** 20 per setting
- **Metrics:** prediction R2 in test set; calibration slope (regression of true phenotype on PRS); MCMC convergence (1000 iters 500 burn-in in sims)
- **Competitors:** unadjusted PRS; P+T (clumping + thresholding); LDpred; LDpred-inf; PRS-CS; PRS-CS-auto
- **Real data:** Partners HealthCare Biobank (19,136 unrelated Europeans; 6 diseases + 6 quantitative traits) with public GWAS summary statistics; also UK Biobank; no variable-selection benchmark
- **Code/data:** PRS-CS software (github getian107/PRScs); UKB by application
- *Source pages:* Results: Simulations (Fig 1); Methods: Simulations; UK Biobank genetic data; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

### Prive2020
Prive F; Arbel J; Vilhjalmsson BJ. LDpred2: better, faster, stronger. Bioinformatics 36(22-23) 5424-5431 (2020). **10.1093/bioinformatics/btaa1029**

- **X:** real-X(synthetic beta); binary/SNP-genotypes (dosages). UK Biobank imputed dosages; 362,320 genetically homogeneous individuals (PC-based Mahalanobis filter) and 1,117,493 HapMap3 variants (list from PRS-CS); 300,000 individuals for GWAS summary stats, 10,000 for LD matrix and hyper-parameter selection, 52,320 test; liability threshold model; simulation function snp_simuPheno (bigsnpr)
- **n:** 300,000 GWAS (also 10K;20K;50K;120K in one scenario); 10,000 validation; 52,320 test
- **p (max):** 1,117,493 HapMap3 variants (all used)
- **s0:** 300; 3000; 30,000; 300,000 causal anywhere on genome; 300 or 3000 in HLA region (chr6 25.5-33.5Mb); mixture 300 HLA (20%) + 10,000 anywhere (20%)
- **β / SNR:** liability threshold model, prevalence 15%; h2=0.4 (0.3 for HLA-only scenarios); weights w_j~N(0,h2/|S|) on standardized dosages; eps~N(0,1-h2)
- **Noise:** Gaussian liability; binary phenotype; **replicates:** 10 per scenario (7 scenarios; bootstrap CI of mean AUC from 10,000 resamples)
- **Metrics:** AUC on test set (and ratio to max achievable AUC); runtime
- **Competitors:** LDpred1 (inf and grid); LDpred2 variants (inf, grid, sparse, auto; per-chromosome vs genome-wide); C+T; SCT; lassosum; PRS-CS; SBayesR (real data)
- **Real data:** UK Biobank 8 case-control traits with external published GWAS summary stats (10,000 validation; 352,320 test)
- **Code/data:** https://github.com/privefl/bigsnpr ; https://github.com/privefl/paper-ldpred2
- *Source pages:* Sec 3.1 Simulation analyses; Table 1; Sec 4.2 Simulations; Fig 1-2; *read level:* full-text; *scout file:* `S3_GENOMICS.tsv`

