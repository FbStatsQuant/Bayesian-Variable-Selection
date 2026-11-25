# BENCH_DESIGN: how variable selection is benchmarked, and what our suite needs

*Theory Department, 2026-11-24. Owner's order via HQ; the advisor pointed us to JMLR 21 (2020) 19-536.*
*Inputs: a full read of 19-536 plus three Sonnet scout sweeps, `scout/S1_BVS.tsv`, `S2_FREQ.tsv` and `S3_GENOMICS.tsv`, with a fourth scout (`S4_LOCAL.tsv`) for papers the owner already had locally. It covers 89 unique papers, 88 of them read in full text. The per-paper setups are in [`PAPERS.md`](PAPERS.md), which is part of this report. The Haiku check log is in [`CHECK.md`](CHECK.md).*

---

## 0. Bottom line

1. **There is no single standard design, but there is a standard family.**
   - Rows are drawn as $x_i \sim N_p(0,\Sigma)$ with $\Sigma \in \{I,\ \rho^{|j-k|},\ \text{equicorrelated } \rho\}$.
   - The number of true signals is $s_0 \in [5,30]$, and signal strength is set on an SNR grid.
   - Each setting is repeated over 20–100 replicates.
   - The metrics are TPR/FDR, exact recovery, estimation or prediction error, and runtime.
2. **The Bayesian-sampler community has one de facto standard: the Yang–Wainwright–Jordan (YWJ) design.**
   - Covariance: AR(1), $\rho=0.6$ in the Griffin et al. (2021) variant.
   - Size: $n=500$, $p\in\{500,5000\}$, $s_0=10$.
   - Signal: $\beta^*=\mathrm{SNR}\sqrt{\sigma^2\log p/n}\,(2,-3,2,2,-3,3,-2,3,-2,3)$.
   - 8 of the papers use it, and PIP efficiency is measured against an add–delete–swap baseline.
3. **The frequentist best-subset community uses the Hastie–Tibshirani–Tibshirani (2020) grid.** It combines AR(1) $\rho\in\{0,0.35,0.7\}$, the "beta-types", and ten log-spaced SNR values $\nu=\mathrm{Var}(x^\top\beta)/\sigma^2\in[0.05,6]$.
4. **At $p\ge 10^5$, almost every paper uses real genotypes with a synthetic phenotype.**
   - Only two published designs use a synthetic $X$ at $p=10^6$: Hazimeh & Mazumder (2020), "Gaussian 1M" ($n=200$, $k=20$, $\nu=10$), and Hazimeh et al. (2022) ($n=1000$, equicorrelation 0.1).
   - **Our 1M rung ($n=200$) sits right next to Hazimeh's Gaussian 1M cell.**
   - No paper runs a structured (AR or block) synthetic $X$ at $10^6$ with $n$ in the hundreds and scores the result with selection metrics. That slot is open.
5. **Our current suite is nonstandard in three ways:**
   - it uses our own $\beta$ vector with $s_0=5$;
   - it has no SNR grid;
   - it lacks the community's metrics: TPR/FDR, PIP-MSE against a gold standard, and time-standardised relative ESS.

   The fix (§6) is cheap: add the YWJ cell, the Hastie SNR grid, an equicorrelated arm, and riboflavin/PCR real-$X$ designs. Then keep our AR and block rungs to $10^6$ as the extension.

---

## 1. The advisor's paper: JMLR 21(73):1–61, paper 19-536

Johndrow, Orenstein & Bhattacharya (2020), *Scalable approximate MCMC algorithms for the horseshoe prior*. arXiv:1705.00841; JMLR gives no DOI.

| Item | Setting |
|---|---|
| $X$ | rows $w_i\sim N_p(0,\Sigma)$, with $\Sigma=I$ or $\Sigma_{ij}=0.9^{\lvert i-j\rvert}$; $\Sigma$ is not stated for several figures |
| $\beta$ | $\beta_j=2^{(9-j)/4}$ for $j=1,\dots,23$ (from 4 down to about 0.088), else 0, so $s_0=23$ |
| noise | Gaussian, $\sigma^2=4$; the paper reports no SNR or $R^2$ (we compute $R^2\approx0.93$ for $\Sigma=I$) |
| sizes | largest $N=5000$, $p=50{,}000$; 20 random $(N,p)$ data sets per setting; an $N$-sweep over 200–2000 at $p=20{,}000$ with 10 reps |
| real data | maize GWAS (USDA Ames lines), $n=2267$, $p=98{,}385$; the data were shared privately and are not linked |
| metrics | MSE of $\beta$, coverage of 95% CIs, ESS and ESS/s, wall-clock; **no selection metrics (TPR/FDR/PIP)** |
| competitors | the authors' own exact and older samplers; lasso (maize only); no code released |

**Reading.** This is a *computation* paper. Its benchmark is scaling in $(N,p)$ and ESS per second, not selection accuracy.

Two of its pieces recur elsewhere:
- **The decaying signal** $2^{(9-j)/4}$ reappears in Biswas et al. (2022), logistic case.
- **The maize matrix** ($n=2267$, $p=98{,}385$) is reused by Biswas et al. (2022) and by Jankowiak (2023). Jankowiak pads it with iid columns up to $p=7.5\times10^5$.

The maize matrix is the de facto large-$p$ real design for Bayesian samplers.

---

## 2. Recurring synthetic designs

Each count is the number of papers (out of 89) that use the design at least once. A paper can count in several rows. The counts come from a hand-cleaned keyword tally of the scout tables, so read them as ±2.

| Design | $\Sigma$ | Papers | Typical parameters | Examples |
|---|---|---|---|---|
| Independent | $I$ | ≈30 | — | Scott–Berger 2010; Su et al. 2017; Biswas 2022; Hazimeh 2020 (1M) |
| **AR(1) / Toeplitz** | $\rho^{\lvert j-k\rvert}$ | **32** | $\rho=0.5$ (15 papers), $0.9$ (11), $0.6$ (6, the BVS-sampler line), $e^{-1}\approx0.37$ (YWJ original, Zhou 2022) | Tibshirani 1996; Fan–Li 2001; YWJ 2016; Griffin 2021; Hastie 2020; Johndrow 2020 |
| **Equicorrelated** | $\Sigma_{jk}=\rho$ | ≈23 | $\rho=0.5$ is modal; 0.25 (Johnson–Rossell 2012, Narisetty–He 2014, Song–Liang 2015); 0.6 (Ročková–George 2018); 0.8 (Dezeure 2015); 0.1 (Hazimeh 2022) | Friedman 2010 (glmnet timing); Shin 2018; Zhu 2020 |
| Block-diagonal | blocks of 10–20 | ≈11 | within-block $\rho$ from 0.5 to 0.9 | Dezeure 2015 ($20\times20$, equicorrelated); Zhou 2022 ($d=20$); Papaspiliopoulos–Rossell 2017 (10) |
| Factor | $\Lambda\Lambda^\top+I$ | 3 | 2–20 factors | Meinshausen–Bühlmann 2010; Zou–Hastie 2005; Wang–Leng 2016 |
| Adversarial | built to break a method | ≈7 | — | YWJ $\Sigma_{\rm bad}$; Zou 2006 "Model 0"; Bertsimas–Pauphilet 2020; Titsias–Yau 2017 (confounded pair); Zanella–Roberts 2019 (pair with $\rho=0.99$) |
| **Real $X$ + synthetic $\beta$** | real | ≈30 | genotypes (GTEx, UKB, WTCCC, maize), riboflavin, leukemia | §3, §5 |

**Signal conventions.** There are four, and they do not agree. This is the main source of non-comparability.

| Convention | Definition | Papers |
|---|---|---|
| (a) YWJ scaling | $\beta^*=\mathrm{SNR}\cdot\sqrt{\sigma^2\log p/n}\cdot(2,-3,2,2,-3,3,-2,3,-2,3,0,\dots)$, with $\mathrm{SNR}\in\{0.5,1,2,3\}$ and $\sigma=1$ | 8: YWJ 2016, Zanella–Roberts 2019, Griffin 2021, Wan–Griffin 2021, Liang 2022, Zhou 2022, Liang 2023, Staerk 2024 |
| (b) Variance-ratio SNR | $\nu=\mathrm{Var}(x^\top\beta)/\sigma^2$ and $\mathrm{PVE}=\nu/(1+\nu)$, with $\sigma^2$ solved from $\nu$; Hastie's grid is $\nu\in\{0.05,0.09,0.14,0.25,0.42,0.71,1.22,2.07,3.52,6.00\}$ | ≈9: Bertsimas 2016; Hastie 2020; Hazimeh 2020/2022; Bertsimas–Pauphilet 2020; Meinshausen 2009 ($\nu\in\{0.25,1,4,16\}$); Friedman 2010 ($\nu=3$); Wang–Leng 2016 ($R^2\in\{0.5,0.9\}$); Ishwaran–Rao 2005 ($R^2=0.75$) |
| (c) PVE / $h^2$ with random effects | $b_j\sim N(0,\tau^2)$ at random positions, with $\sigma^2$ set for the target PVE (SuSiE uses $\{0.05,0.1,0.2,0.4\}$) | ≈14, the genomics line: SuSiE, Guan–Stephens, Zhou 2013, Kim 2024, and others |
| (d) Fixed vectors | Tibshirani's $(3,1.5,0,0,2,0,0,0)$ (5 papers); $(0.6,1.2,1.8,2.4,3.0)$ (Johnson–Rossell, Narisetty–He); equal amplitude with random signs, $\pm A$ (knockoffs with $A=3.5$; best-subset $\pm1$; ≈7 papers); decaying $2^{(9-j)/4}$ (Johndrow, Biswas) | — |

**Sparsity, sample size and replicates.**
- **Sparsity:**
  - $s_0=5$ is the commonest choice at low and moderate $p$.
  - $s_0=10$ is used by YWJ, Hastie's high-10 setting and Hazimeh 2022.
  - $s_0$ of 20–60 appears in knockoffs and GWAS BVSR.
  - Fine-mapping uses 1–5 signals per region, and polygenic work uses $10^3$–$10^5$.
- **Sample size:** $n$ is 100–1000 whenever $p\le5000$. The sampler papers use $n\in\{500,1000\}$.
- **Replicates:**

  | Line of work | Usual replicates |
  |---|---|
  | Selection-accuracy papers | 50–200 data sets (100 is the mode) |
  | Sampler-efficiency papers | 1 data set × 50–200 independent runs (Schäfer–Chopin, Zanella–Roberts, Griffin, Staerk), or 20 data sets × several chains (YWJ) |
  | Best-subset papers | 10 |
  | Fine-mapping papers | 150–6000 data sets |

**Where our design sits.** Our design uses $\beta^*=a(1,-0.8,0.9,-0.7,0.6)$ with well-separated truths, so $\nu\approx a^2\sum\beta_j^2$. The table maps it onto the conventions above.

| Cell | $\nu$ | PVE | $\beta_{\min}/(\sigma\sqrt{\log p/n})$ at $n=200$, $p=10^6$ | YWJ-equivalent SNR (by $\beta_{\min}$) |
|---|---|---|---|---|
| ours, strong ($a=1$) | 3.30 | 0.77 | 2.28 | ≈1.1 |
| ours, weak ($a=0.6$) | 1.19 | 0.54 | 1.37 | ≈0.7 |
| YWJ, $n=500$, $p=5000$, SNR = 1 / 2 / 3 (AR 0.6) | 0.44 / 1.75 / 3.94 | 0.30 / 0.64 / 0.80 | 2 / 4 / 6 (at its own $n,p$) | 1 / 2 / 3 |
| Hazimeh "Gaussian 1M" ($k=20$, $\nu=10$) | 10 | 0.91 | 2.69 | ≈1.3 |

For YWJ, $\beta_{\min}/\sqrt{\log p/n}=2\cdot\mathrm{SNR}$ by construction. By total signal ($\nu$), our strong cell is easy (about YWJ SNR 3). By the smallest signal, it is moderate (about YWJ SNR 1).

---

## 3. Canonical real datasets

| Dataset | $n$ | $p$ | Access | Used by (papers in this survey) |
|---|---|---|---|---|
| **Riboflavin** (*B. subtilis*) | 71 | 4,088 | public, R package `hdi` | 6: Meinshausen–Meier–Bühlmann 2009 (real $X$ + synthetic $\beta$); Meinshausen–Bühlmann 2010; Bühlmann 2014; Javanmard–Montanari 2014; Dezeure 2015; Hazimeh 2022 (with pairwise interactions, $p=8.36\times10^6$) |
| **PCR mouse** (Lan 2006, GSE3330) | 60 | 22,575 | public (GEO) | 8: Narisetty–He 2014; Song–Liang 2015; Shin 2018; Narisetty 2019; Griffin 2021; Liang 2022; Biswas 2022; Staerk 2024 |
| **Leukemia** (Golub 1999) | 72 | 7,129 (3,571 after preprocessing) | public | 7: Zou–Hastie 2005; Fan–Lv 2008; Friedman 2010; Breheny–Huang 2011; Bertsimas 2016; Wan 2021; Staerk 2024 |
| Boston housing + interactions | 506 | 104 | public | 5: Schäfer–Chopin 2013; Griffin 2021; Liang 2022; Shin 2018 (+1000 noise columns); Hazimeh 2020 (+probes, $p=104{,}000$) |
| Concrete / Protein | 1030 / 96 | 79 / 88 | public | 3: Schäfer–Chopin 2013; Griffin 2021; Liang 2022 |
| Tecator | 172 | 100 | public | 3: Griffin 2021; Liang 2022; Staerk 2024 |
| Lymph node (Hans 2007) | 148 | 4,514 | public | 3: Hans 2007; Narisetty 2019; Biswas 2022 |
| **Maize GWAS** (Romay 2013) | 2,267 | 98,385 | shared or panzea (verify) | 3: Johndrow 2020; Biswas 2022; Jankowiak 2023 (padded to $7.5\times10^5$) |
| Mouse SNP, testis weight | 993 | 79,748 | public (Carbonetto 2017) | 2: Griffin 2021; Liang 2022 |
| TGFB colon cancer | 262 | 10,172 | public (supplement) | 2: Zanella–Roberts 2019; Papaspiliopoulos–Rossell 2017 |
| Scheetz rat eye (GSE5680) | 120 | 18,976 | public | Wang–Leng 2016, plus downstream papers we did not read |
| Ozone / Crime / Diabetes / Prostate | 203–442 / 47 | 8–134 | public | Liang 2008; Ray–Szabó 2022; Ishwaran–Rao 2005; Bertsimas 2016; Tibshirani 1996; Zou–Hastie 2005 |
| Bloom yeast BY×RM | 1,008 | 30,594 | public | data-source paper; a realistic $n\sim10^3$, $p\sim3\times10^4$ test bed |
| Atwell *Arabidopsis* | ≈96–199 | 216,130 | public (AraPheno) | data-source paper; **the only public design with $n$ in the hundreds and $p$ in the hundreds of thousands** |
| HS mice (Valdar 2006) | ≈2,000 | — | public | Zhou 2013 |
| WTCCC | ≈2–5k per disease | 3–4.4×10⁵ | **restricted** | 6: Carbonetto–Stephens 2012; Zhou 2013; Moser 2015; Zhu–Stephens 2017; Candès 2018; Sesia 2019 |
| UK Biobank | $10^5$–$5\times10^5$ | $10^6$–$1.8\times10^7$ | **restricted** | 9: Qian 2020; Ge 2019; Lloyd-Jones 2019; Privé 2020; Weissbrod 2020; Sesia 2021; Zou 2022; Cui 2024; McCreight 2025 |
| GTEx genotypes | 287–574 | $10^3$–$1.2\times10^4$ | **restricted** (dbGaP) | Wang 2020 (SuSiE); Kim 2024 |

---

## 4. Standard metrics

| Family | Metric | Who uses it |
|---|---|---|
| Selection | TPR (power) and FDR (or FDP) at a threshold (PIP $>0.5$, MPM, or target $q$) | ≈25 papers: knockoffs, best-subset, BVS-prior, fine-mapping |
| | Exact recovery $\Pr(\hat S=S_0)$ | Johnson–Rossell 2012; Narisetty–He 2014; Narisetty 2019; Zhang 2010; Hazimeh 2020; Bertsimas–Van Parys 2020; Su 2017; Rossell 2021 |
| | FP and FN counts, model size | most frequentist papers |
| | Precision–recall or ROC curves | Shin 2018; Guan–Stephens 2011; Moser 2015; McCreight 2025 |
| | Sure-screening coverage | Fan–Lv 2008; Wang–Leng 2016 |
| Posterior / sampler | **PIP-MSE against a long-run gold standard** | Liang 2022, 2023; Staerk 2024 |
| | **Time-standardised relative ESS of PIP estimates**, $r_{A,B}=(\mathrm{ESS}_A/t_A)/(\mathrm{ESS}_B/t_B)$, estimated from the PIP variance over 50–200 independent runs and taken relative to an add–delete–swap baseline | Zanella–Roberts 2019; Griffin 2021; Wan 2021; Zhou 2022; Staerk 2024 |
| | Spread of PIPs over 200 runs | Schäfer–Chopin 2013 (the SMC precedent) |
| | Posterior probability of the true model; time to hit the MAP model | Johnson–Rossell 2012; Shin 2018; Zhou 2022; Hans 2007; YWJ 2016 (Gelman–Rubin) |
| | PIP calibration | Guan–Stephens 2011; SuSiE line; Weissbrod 2020; Cui 2024 |
| | Credible-set coverage, size and purity | SuSiE line: Wang 2020; Zou 2022; McCreight 2025 |
| Estimation / prediction | $\ell_2$ (or $\ell_1$) error of $\hat\beta$ | Bhattacharya 2016; Ray–Szabó 2022; Fan–Lv 2008; Zhu 2020 |
| | Relative risk or relative test error | Hastie 2020; Bertsimas 2016 |
| | Out-of-sample MSE, $R^2$ or AUC | most real-data analyses |
| | CI coverage and length | Johndrow 2020; Bhattacharya 2016; Dezeure 2015; Javanmard–Montanari 2014 |
| Cost | Runtime, ESS/s, iterations per second | nearly all papers |

**What we already have that is uncommon:**
- reliability curves and Brier scores for PIPs (only the genomics papers calibrate PIPs);
- Hellinger distance to the posterior;
- evidence diagnostics.

**Gaps we must close:**
- TPR/FDR and exact recovery;
- PIP-MSE against a gold standard;
- relative time-standardised ESS;
- $\ell_2$ error and prediction error.

---

## 5. Large-$p$ designs ($p\ge10^4$)

**A. Synthetic $X$**

| Paper | $X$ | $n$ | $p$ | $s_0$ | Signal | Selection metrics? |
|---|---|---|---|---|---|---|
| **Hazimeh & Mazumder 2020** (L0Learn) | iid $N(0,1)$ | 200 | **$10^6$** | 20 | $\nu=10$, equal ones, equally spaced | yes (TP/FP, support recovery) |
| | equicorrelated / AR | 1000 | $5\times10^4$, $10^5$ | 100, 50 | $\nu$ swept | yes |
| **Hazimeh, Mazumder & Saab 2022** (L0BnB) | equicorrelated $\rho=0.1$ | 1000 | $10^3$–**$10^6$** | 10 | $\nu=5$ | timing and optimality gap |
| Bertsimas & Van Parys 2020 | Toeplitz $\rho=0.1$ | up to $10^5$ | $2\times10^5$ | 10–30 | $\pm1$, SNR $\{3,7,20\}$ | accuracy and false-alarm rates |
| Bertsimas, Pauphilet & Van Parys 2020 | Toeplitz $\rho\in\{0.2,0.7\}$ | 500–3700 | $2\times10^4$ | 100 | $\pm1$, $\nu$ grid | TPR, FDR |
| Johndrow et al. 2020 (19-536) | iid / AR 0.9 | ≤5000 | $5\times10^4$ | 23 | $2^{(9-j)/4}$, $\sigma=2$ | no |
| Liang, Livingstone & Griffin 2022 | **YWJ, AR 0.6** | 500, 1000 | **$5\times10^4$** | 10 | YWJ SNR $\{0.5,1,2,3\}$ | PIP-MSE |
| Biswas, Mackey & Meng 2022 | iid | 1000 | $5\times10^4$ | 10 | $\beta_j=2$, $\sigma=2$ | TPR, FDR |
| Shin, Bhattacharya & Johnson 2018 | equicorrelated / AR 0.5 / iid | 400 | $2\times10^4$ | 5 | $(0.5,\dots,1.5)$, random signs, $\sigma=1.5$ | PR curves |
| Fan & Lv 2008 | iid | 800 | $2\times10^4$ | 18 | $a=5\log n/\sqrt n$ | screening coverage |
| Wang & Leng 2016 | iid / equicorrelated / AR / factor | 200 | $10^4$ | 5 | $R^2\in\{0.5,0.9\}$ | screening coverage |
| Kim et al. 2024 (Mr.ASH) | iid / equicorrelated | 500 | $10^4$ | 20 | PVE 0.5 | prediction only |
| Friedman, Hastie & Tibshirani 2010 | equicorrelated | 100 | $5\times10^4$ ($10^5$ logistic) | dense | $\nu=3$ | timing only |
| **Song & Liang 2015** | equicorrelated $\rho=0.25$ on the first 2,000 columns, independent elsewhere | 100 | **$5\times10^5$** | 5 | $\beta=(0.2,\dots,0.6)$, $\sigma^2=0.25$ | yes (100 data sets) |
| Hans, Dobra & West 2007 | real 8,408 columns + iid padding | 41 | $2.5\times10^4$ | 4 | $\sigma^2=0.5$ | time to find $S_0$ |

**B. Real genotype $X$ + synthetic $\beta$ (the dominant large-$p$ protocol)**

| Paper | $X$ source | $n$ | $p$ | $s_0$ | Signal |
|---|---|---|---|---|---|
| **Jankowiak 2023** | maize + iid padding | 2,267 | **$7.5\times10^5$** | 20 | $U([-1,-0.1]\cup[0.1,1])$, $\sigma=0.5$ |
| **Guan & Stephens 2011** | PARC chips | ≈980 | $3.17\times10^5$, $5.5\times10^5$ | 30 | PVE 0.01–0.5 |
| Zhou, Carbonetto & Stephens 2013 | height cohort / PARC / WTCCC | 3,925 | ≈$3$–$5.5\times10^5$ | 10–$10^4$ | PVE 0.2, 0.6 |
| Hoggart et al. 2008 | FREGENE simulated haplotypes | 2,000 | $4.8\times10^5$ | 10 | risk ratio 2 |
| Moser et al. 2015 | height cohort | 3,924 | 287,854 | 3,000 | $h^2\in\{0.2,0.5,0.8\}$ |
| Lloyd-Jones 2019 / Ge 2019 / Privé 2020 | UKB HapMap3 | $10^4$–$3\times10^5$ | ≈$0.8$–$1.1\times10^6$ | $10^2$–$3\times10^5$ | $h^2$ 0.1–0.5 (prediction) |
| Sesia et al. 2021 | UKB | ≈489k | 592,000 | 4,000 | heritability grid (knockoffs) |

**C. The gap.** Only three designs have both $p\ge 5\times10^5$ and selection scoring:
- Hazimeh 2020 (Gaussian 1M): iid $X$, $n=200$.
- Song–Liang 2015: $p=5\times10^5$, $n=100$, with correlation confined to 2,000 columns.
- Jankowiak 2023 (padded maize): real $X$, $n=2267$.
- **No published design uses a correlated synthetic $X$ (AR or block) with $n\le10^3$ at $p=10^6$.** Our AR and block 1M cells fill exactly this slot.

---

## 6. Recommendations for our suite

**Current suite** (EXPERIMENT_PLAN):
- **Designs:** IND, AR 0.6 (primary), BLK (20 columns, $\rho=0.5$) and FAC (equicorrelated 0.3, contingent).
- **Signal:** $s_0=5$ with $\beta^*=a(1,-0.8,0.9,-0.7,0.6)$, $a\in\{1,0.6\}$, $\sigma=1$.
- **Sizes:** $n\in\{100,\dots,800\}$; rungs at $10^4$, $10^5$ and $10^6$.
- **Competitors:** lasso, MCP/SCAD, L0Learn, SuSiE.
- **Real data:** riboflavin.

### 6.1 Must include, to be standard

| # | Add | Exact spec | Why |
|---|---|---|---|
| **S1** | **YWJ cell** | $x_i\sim N(0,\Sigma)$, $\Sigma_{jk}=0.6^{\lvert j-k\rvert}$; $n\in\{500,1000\}$; $p\in\{500,5000\}$; $s_0=10$ (first 10 coordinates); $\beta^*=\mathrm{SNR}\sqrt{\log p/n}\,(2,-3,2,2,-3,3,-2,3,-2,3)$; $\mathrm{SNR}\in\{0.5,1,2,3\}$; $\sigma=1$ | It is the sampler community's standard (8 papers). The Griffin/Liang/Zanella code is public, so we can run the competitors ourselves. Note that YWJ's original uses $e^{-\lvert j-k\rvert}$ ($\rho\approx0.37$); label our cell "YWJ/Griffin, $\rho=0.6$". |
| **S2** | **Hastie et al. grid** | AR(1) $\rho\in\{0,0.35,0.7\}$; $(n,p,s)\in\{(50,1000,5),(100,1000,10)\}$; beta-types 1 and 2 (3 optional); the 10-point $\nu$ grid from 0.05 to 6 | It is the frequentist standard, and it gives an SNR curve instead of two points. |
| **S3** | **Equicorrelated** | $\Sigma_{jk}=0.5$ (the standard), plus 0.8 (Dezeure, hard); $s_0\in\{5,10\}$ | Upgrades our contingent FAC arm (0.3) to the common setting. |
| **S4** | **Real $X$ + synthetic $\beta$ (riboflavin)** | Dezeure 2015 protocol: riboflavin $X$ ($n=71$; their $p=500$ top-variance columns, plus the full 4,088); $s_0\in\{3,15\}$; $\beta$ from $U(0,2)$, $U(0,4)$, $U(-2,2)$ or fixed $\{1,2,10\}$ at random positions; $\sigma=1$ | The standard semi-real design. We already ship riboflavin. |
| **S5** | **Real data used by the samplers** | PCR mouse (GSE3330, $n=60$, $p=22{,}575$); Schäfer–Chopin's Boston ($p=104$), concrete (79) and protein (88); Tecator (100) | These are where our closest prior art (Schäfer–Chopin 2013 SMC) and the ASI/PARNI papers report. A long-run gold standard is feasible for all of them. |
| **S6** | **Standard metrics** | TPR, FDR and exact recovery for the reported model $\hat S$ and the MPM; PIP-MSE against a gold standard; $r_{A,B}$ relative to add–delete–swap; $\ell_2$ error; out-of-sample prediction error; runtime | Lets us state results in the field's units. Keep our sup-PIP error, Brier/reliability, Hellinger and evidence metrics as extras. |
| **S7** | **Replicates** | ≥50 data sets per cell for selection rates (100 if cheap), with Monte Carlo standard errors; for efficiency, 1 data set × ≥50 independent runs | Matches the norms in §2. |
| **S8** | **Report SNR three ways** | For every cell: $\nu$, PVE, and $\beta_{\min}/(\sigma\sqrt{\log p/n})$ | Makes our cells comparable to all four conventions. |
| **S9** | **Competitors** | Add add–delete–swap MC3 (baseline), ASI (Griffin 2021), PARNI (Liang 2022) and wTGS (Zanella–Roberts 2019), all with public code, plus varbvs. Run the Schäfer–Chopin SMC if its scripts can be obtained. | These are the Bayesian baselines reviewers will expect. Our frequentist set (glmnet, ncvreg, L0Learn, SuSiE) is already standard. |

### 6.2 Extension to $p=10^6$

| # | Cell | Spec | Status in the literature |
|---|---|---|---|
| **L1** | **Hazimeh "Gaussian 1M", verbatim** | iid $N(0,1)$; $n=200$; $p=10^6$; $k=20$ equally spaced ones; $\nu=10$ ($\sigma^2=2$) | Published, with L0Learn as the authors' own competitor. Our 1M engine already runs $n=200$. **The highest-value single cell.** |
| **L2** | Hazimeh 2022 | equicorrelated $\rho=0.1$; $n=1000$; $p\in\{10^4,10^5,10^6\}$; $k=10$; $\nu=5$ | Published (timing only), so we add selection metrics. |
| **L3** | **YWJ scaled up** | S1 with $p\in\{5\times10^4,10^5,10^6\}$, $n\in\{500,1000\}$, $\mathrm{SNR}\in\{1,2\}$ | Liang 2022 stops at $5\times10^4$, so this continues the standard into new territory. |
| **L4** | Our AR 0.6 and BLK at 1M | as planned ($n=200$, $s_0=5$), but reported in S8 units | The open slot from §5C (correlated synthetic, $n\le10^3$). |
| **L5** | Real genotype $X$ + synthetic $\beta$ | **public sources only:** Atwell *Arabidopsis* ($n\approx199$, $p=216{,}130$); Bloom yeast ($n=1008$, $p=30{,}594$); optionally maize ($n=2267$, $p=98{,}385$) padded with iid columns to $10^6$ as in Jankowiak (first confirm the maize data can be downloaded). Use the Guan–Stephens protocol: $s_0\in\{10,30\}$, $b_j\sim N(0,1)$ at random positions, $\sigma^2$ set for PVE $\in\{0.1,0.3,0.5\}$. | The field's dominant large-$p$ protocol. Avoid UKB, WTCCC and GTEx: they are restricted, and our repo is public. |

### 6.3 What to do with the stopped AR-0.6 replicate block

Restart it as **S1 at $p=5000$** (≥20 data sets × SNR $\{0.5,1,2,3\}$, $n\in\{500,1000\}$). Then step up in $p$ (L3) and run L1.

Keep our $s_0=5$ strong and weak cells as a secondary family. They are not a standard, but they are well defined and already in the theory (our A7 results, Thms 1–4, quote $\beta_{\min}$). Report them in S8 units so readers can place them.

---

## 7. Gaps, caveats, paywalled papers

**Paywalled must-haves:**

| Paper | DOI | Status |
|---|---|---|
| George & McCulloch (1993), *Variable selection via Gibbs sampling*, JASA 88(423):881–889 | 10.1080/01621459.1993.10476353 | abstract only; no open or local copy |
| Ročková & George (2014), *EMVS*, JASA 109(506):828–846 | 10.1080/01621459.2013.869223 | the thesis chapter was read instead; the journal version was not |

**Paywalled, but read in full from local copies on Owls** (scout S4): Clyde, Ghosh & Littman 2011 (10.1198/jcgs.2010.09049); Ročková & George 2018, *The spike-and-slab LASSO* (10.1080/01621459.2016.1260469), read from the author manuscript dated 7 August 2015; Song & Liang 2015 (10.1111/rssb.12095), with its supplement.

**Not covered:** Rossell & Telesca 2017; Nikooienejad, Wang & Johnson 2016; Bondell & Reich 2012; Lamnisos, Griffin & Steel 2013; Nott & Kohn 2005; Zanella 2020 (informed proposals); BGLR; BOLT-LMM. These are Bayesian-prior and sampler papers whose designs, from what we know of them, follow §2 patterns. They do not change the recommendations.

**Weaker evidence:**
- Wu 2009: the tables were garbled in text conversion, so its $(n,p)$ grid is incomplete.
- Titsias–Yau 2017: the simulation details live in a supplement we did not read.
- Scheetz, Atwell, Bloom and Valdar are data-source papers, not benchmarks.
- Bühlmann et al. 2014 was read from the author preprint.

---

## 8. Sources

Read levels: F = full text, A = abstract only. Fields: S = BVS sampler, P = BVS prior, F = frequentist penalised, B = best subset, K = knockoffs, Sc = screening, G = fine-mapping/GWAS, R = review/benchmark, O = other.

| # | Key | Citation | Year | DOI / arXiv | Field | Read |
|---|---|---|---|---|---|---|
| 1 | Atwell2010 | Atwell S; Huang YS; Vilhjalmsson BJ; Willems G; Horton M; Li Y; et al. Genome-wide association study of 107 phenotypes in Arabidopsis thaliana inbred lines. Nature 465 627-631 | 2010 | 10.1038/nature08800 | O | F |
| 2 | BarberCandes2015 | Barber RF; Candes EJ. Controlling the false discovery rate via knockoffs; Annals of Statistics 43(5):2055-2085 | 2015 | 10.1214/15-AOS1337; arXiv:1404.5609 | K | F |
| 3 | Benner2016 | Benner C; Spencer CCA; Havulinna AS; Salomaa V; Ripatti S; Pirinen M. FINEMAP: efficient variable selection using summary data from genome-wide association studies. Bioinformatics 32(10) 1493-1501 | 2016 | 10.1093/bioinformatics/btw018 | G | F |
| 4 | Bertsimas2016 | Bertsimas D; King A; Mazumder R. Best subset selection via a modern optimization lens; Annals of Statistics 44(2):813-852 | 2016 | 10.1214/15-AOS1388; arXiv:1507.03133 | B | F |
| 5 | BertsimasPauphilet2020 | Bertsimas D; Pauphilet J; Van Parys B. Sparse regression: scalable algorithms and empirical performance; Statistical Science 35(4):555-578 | 2020 | 10.1214/19-STS701; arXiv:1902.06547 | B | F |
| 6 | BertsimasVanParys2020 | Bertsimas D; Van Parys B. Sparse high-dimensional regression: exact scalable algorithms and phase transitions; Annals of Statistics 48(1):300-323 | 2020 | 10.1214/18-AOS1804; arXiv:1709.10029 | B | F |
| 7 | Bhattacharya2016 | Bhattacharya A.; Chakraborty A.; Mallick B.K.; Fast sampling with Gaussian scale mixture priors in high-dimensional regression; Biometrika; 103(4); 985-991 | 2016 | 10.1093/biomet/asw042 (arXiv:1506.04778) | P | F |
| 8 | Biswas2022 | Biswas N.; Mackey L.; Meng X.-L.; Scalable spike-and-slab; Proc. 39th ICML (PMLR 162); 2021-2040 | 2022 | arXiv:2204.01668 | S | F |
| 9 | Bloom2013 | Bloom JS; Ehrenreich IM; Loo WT; Lite TLV; Kruglyak L. Finding the sources of missing heritability in a yeast cross. Nature 494 234-237 | 2013 | 10.1038/nature11867 | O | F |
| 10 | Bogdan2015 | Bogdan M; van den Berg E; Sabatti C; Su W; Candes EJ. SLOPE: adaptive variable selection via convex optimization; Annals of Applied Statistics 9(3):1103-1140 | 2015 | 10.1214/15-AOAS842; arXiv:1407.3824 | F | F |
| 11 | Bottolo2010 | Bottolo L.; Richardson S.; Evolutionary stochastic search for Bayesian model exploration; Bayesian Analysis; 5(3); 583-618 | 2010 | arXiv:1002.2706; DOI 10.1214/10-BA523 | S | F |
| 12 | BrehenyHuang2011 | Breheny P; Huang J. Coordinate descent algorithms for nonconvex penalized regression, with applications to biological feature selection. The Annals of Applied Statistics 5(1) 232-253 | 2011 | 10.1214/10-AOAS388 | F | F |
| 13 | Buhlmann2014 | Buhlmann P; Kalisch M; Meier L. High-dimensional statistics with a view toward applications in biology. Annu Rev Stat Appl 1 255-278 (author preprint dated 23 May 2013) | 2014 | 10.1146/annurev-statistics-022513-115545 | R | F |
| 14 | Candes2018 | Candes E; Fan Y; Janson L; Lv J. Panning for gold: model-X knockoffs for high-dimensional controlled variable selection; Journal of the Royal Statistical Society Series B 80(3):551-577 | 2018 | 10.1111/rssb.12265; arXiv:1610.02351 | K | F |
| 15 | Carbonetto2012 | Carbonetto P.; Stephens M.; Scalable variational inference for Bayesian variable selection in regression and its accuracy in genetic association studies; Bayesian Analysis; 7(1); 73-108 | 2012 | 10.1214/12-BA703 | S | F |
| 16 | Chen2015 | Chen W; Larrabee BR; Ovsyannikova IG; Kennedy RB; Haralambieva IH; Poland GA; Schaid DJ. Fine mapping causal variants with an approximate Bayesian method using marginal test statistics. Genetics 200(3) 719-736 | 2015 | 10.1534/genetics.115.176107 | G | F |
| 17 | Clyde2011 | Clyde M.A.; Ghosh J.; Littman M.L.; Bayesian adaptive sampling for variable selection and model averaging; J. Comput. Graph. Statist.; 20(1); 80-101 | 2011 | 10.1198/jcgs.2010.09049 | S | F |
| 18 | Cui2024 | Cui R; Elzur RA; Kanai M; Ulirsch JC; Weissbrod O; Daly MJ; Neale BM; Fan Z; Finucane HK. Improving fine-mapping by modeling infinitesimal effects. Nat Genet 56(1) 162-169 | 2024 | 10.1038/s41588-023-01597-3 | G | F |
| 19 | Dezeure2015 | Dezeure R; Buhlmann P; Meier L; Meinshausen N. High-dimensional inference: confidence intervals; p-values and R-software hdi; Statistical Science 30(4):533-558 | 2015 | 10.1214/15-STS527; arXiv:1408.4026 | R | F |
| 20 | FanLi2001 | Fan J; Li R. Variable selection via nonconcave penalized likelihood and its oracle properties; Journal of the American Statistical Association 96(456):1348-1360 | 2001 | 10.1198/016214501753382273 | F | F |
| 21 | FanLv2008 | Fan J; Lv J. Sure independence screening for ultrahigh dimensional feature space (with discussion); Journal of the Royal Statistical Society Series B 70(5):849-911 | 2008 | 10.1111/j.1467-9868.2008.00674.x; arXiv:math/0612857 | Sc | F |
| 22 | FanLv2010 | Fan J; Lv J. A selective overview of variable selection in high dimensional feature space (invited review). Preprint arXiv:0910.1122 (Sept 2009); journal version not checked against the paper text | 2009 | arXiv:0910.1122 | R | F |
| 23 | Friedman2010 | Friedman J; Hastie T; Tibshirani R. Regularization paths for generalized linear models via coordinate descent; Journal of Statistical Software 33(1):1-22 | 2010 | 10.18637/jss.v033.i01 | F | F |
| 24 | Ge2019 | Ge T; Chen CY; Ni Y; Feng YA; Smoller JW. Polygenic prediction via Bayesian regression and continuous shrinkage priors. Nat Commun 10 1776 | 2019 | 10.1038/s41467-019-09718-5 | O | F |
| 25 | GeorgeMcCulloch1993 | George E.I.; McCulloch R.E.; Variable selection via Gibbs sampling; J. Amer. Statist. Assoc.; 88(423); 881-889 | 1993 | 10.1080/01621459.1993.10476353 | S | A |
| 26 | Griffin2021 | Griffin J.E.; Latuszynski K.; Steel M.F.J.; In search of lost (mixing) time: adaptive Markov chain Monte Carlo schemes for Bayesian variable selection with very large p; Biometrika; 108(1); 53-69 | 2021 | 10.1093/biomet/asaa055 (arXiv:1708.05678) | S | F |
| 27 | GuanStephens2011 | Guan Y; Stephens M. Bayesian variable selection regression for genome-wide association studies and other large-scale problems. Ann Appl Stat 5(3) 1780-1815 | 2011 | 10.1214/11-AOAS455 (arXiv 1110.6019) | S | F |
| 28 | Hans2007 | Hans C.; Dobra A.; West M.; Shotgun stochastic search for "large p" regression; J. Amer. Statist. Assoc.; 102(478); 507-516 | 2007 | 10.1198/016214507000000121 | S | F |
| 29 | Hastie2020 | Hastie T; Tibshirani R; Tibshirani RJ. Extended comparisons of best subset selection; forward stepwise selection; and the lasso (arXiv tech-report version of: Best subset; forward stepwise or lasso? Analysis and recommendations based on extensive comparisons; Statistical Science 35(4):579-592) | 2020 | 10.1214/19-STS733; arXiv:1707.08692 | B | F |
| 30 | Hazimeh2020 | Hazimeh H; Mazumder R. Fast best subset selection: coordinate descent and local combinatorial optimization algorithms; Operations Research 68(5):1517-1537 | 2020 | 10.1287/opre.2019.1919; arXiv:1803.01454 | B | F |
| 31 | Hazimeh2022 | Hazimeh H; Mazumder R; Saab A. Sparse regression at scale: branch-and-bound rooted in first-order optimization; Mathematical Programming 196(1-2):347-388 | 2022 | 10.1007/s10107-021-01712-4; arXiv:2004.06152 | B | F |
| 32 | Heinze2018 | Heinze G; Wallisch C; Dunkler D. Variable selection - A review and recommendations for the practicing statistician. Biometrical Journal 60(3) 431-449 | 2018 | 10.1002/bimj.201700067 | R | F |
| 33 | Hoggart2008 | Hoggart CJ; Whittaker JC; De Iorio M; Balding DJ. Simultaneous analysis of all SNPs in genome-wide and re-sequencing association studies. PLoS Genet 4(7) e1000130 | 2008 | 10.1371/journal.pgen.1000130 | F | F |
| 34 | Hormozdiari2014 | Hormozdiari F; Kostem E; Kang EY; Pasaniuc B; Eskin E. Identifying causal variants at loci with multiple signals of association. Genetics 198(2) 497-508 | 2014 | 10.1534/genetics.114.167908 | G | F |
| 35 | Ishwaran2005 | Ishwaran H.; Rao J.S.; Spike and slab variable selection: frequentist and Bayesian strategies; Annals of Statistics; 33(2); 730-773 | 2005 | arXiv:math/0505633; DOI 10.1214/009053604000001147 | P | F |
| 36 | Jankowiak2023 | Jankowiak M.; Bayesian variable selection in a million dimensions; Proc. AISTATS 2023 (PMLR 206) | 2023 | arXiv:2208.01180 | S | F |
| 37 | Javanmard2014 | Javanmard A; Montanari A. Confidence intervals and hypothesis testing for high-dimensional regression; Journal of Machine Learning Research 15(82):2869-2909 | 2014 | arXiv:1306.3171 (JMLR v15 javanmard14a) | F | F |
| 38 | Johndrow2020 | Johndrow J.; Orenstein P.; Bhattacharya A.; Scalable approximate MCMC algorithms for the horseshoe prior; Journal of Machine Learning Research; 21(73); 1-61 | 2020 | arXiv:1705.00841 (earlier preprint version; JMLR page lists no DOI) | P | F |
| 39 | Johnson2012 | Johnson V.E.; Rossell D.; Bayesian model selection in high-dimensional settings; J. Amer. Statist. Assoc.; 107(498); 649-660 | 2012 | 10.1080/01621459.2012.682536 | P | F |
| 40 | Kichaev2014 | Kichaev G; Yang WY; Lindstrom S; Hormozdiari F; Eskin E; Price AL; Kraft P; Pasaniuc B. Integrating functional data to prioritize causal variants in statistical fine-mapping studies. PLoS Genet 10(10) e1004722 (PAINTOR) | 2014 | 10.1371/journal.pgen.1004722 | G | F |
| 41 | Kim2024 | Kim Y; Wang W; Carbonetto P; Stephens M. A flexible empirical Bayes approach to multiple linear regression and connections with penalized regression. JMLR 25(185) (arXiv v3 Jun 2024) | 2024 | arXiv:2208.10910 | P | F |
| 42 | Liang2008 | Liang F.; Paulo R.; Molina G.; Clyde M.A.; Berger J.O.; Mixtures of g priors for Bayesian variable selection; J. Amer. Statist. Assoc.; 103(481); 410-423 | 2008 | 10.1198/016214507000001337 | P | F |
| 43 | Liang2022 | Liang X.; Livingstone S.; Griffin J.; Adaptive random neighbourhood informed Markov chain Monte Carlo for high-dimensional Bayesian variable selection; Statistics and Computing; 32(5); article 84 | 2022 | 10.1007/s11222-022-10137-8 (arXiv:2110.11747) | S | F |
| 44 | Liang2023 | Liang X.; Livingstone S.; Griffin J.; Adaptive MCMC for Bayesian variable selection in generalised linear models and survival models; Entropy; 25(9); 1310 | 2023 | 10.3390/e25091310 (arXiv 2308.00869) | S | F |
| 45 | LloydJones2019 | Lloyd-Jones LR; Zeng J; Sidorenko J; Yengo L; Moser G; Kemper KE; et al. Improved polygenic prediction by Bayesian multiple regression on summary statistics. Nat Commun 10 5086 | 2019 | 10.1038/s41467-019-12653-0 | P | F |
| 46 | McCreight2025 | McCreight A; Cho Y; Li R; Nachun D; Gan H; Carbonetto P; Stephens M; Denault W; Wang G. SuSiE 2.0: improved efficiency and calibration for genetic fine-mapping and prediction. bioRxiv preprint | 2025 | 10.1101/2025.11.25.690514 | G | F |
| 47 | Meinshausen2009 | Meinshausen N; Meier L; Buhlmann P. P-values for high-dimensional regression; Journal of the American Statistical Association 104(488):1671-1681 | 2009 | 10.1198/jasa.2009.tm08647; arXiv:0811.2177 | F | F |
| 48 | MeinshausenBuhlmann2010 | Meinshausen N; Buhlmann P. Stability selection (with discussion); Journal of the Royal Statistical Society Series B 72(4):417-473 | 2010 | 10.1111/j.1467-9868.2010.00740.x; arXiv:0809.2932 | F | F |
| 49 | MeinshausenYu2009 | Meinshausen N; Yu B. Lasso-type recovery of sparse representations for high-dimensional data; Annals of Statistics 37(1):246-270 | 2009 | 10.1214/07-AOS582; arXiv:0806.0145 | F | F |
| 50 | Moser2015 | Moser G; Lee SH; Hayes BJ; Goddard ME; Wray NR; Visscher PM. Simultaneous discovery, estimation and prediction analysis of complex traits using a Bayesian mixture model. PLoS Genet 11(4) e1004969 | 2015 | 10.1371/journal.pgen.1004969 | P | F |
| 51 | Narisetty2014 | Narisetty N.N.; He X.; Bayesian variable selection with shrinking and diffusing priors; Annals of Statistics; 42(2); 789-817 | 2014 | arXiv:1405.6545; DOI 10.1214/14-AOS1207 | P | F |
| 52 | Narisetty2019 | Narisetty N.N.; Shen J.; He X.; Skinny Gibbs: a consistent and scalable Gibbs sampler for model selection; J. Amer. Statist. Assoc.; 114(527); 1205-1217 | 2019 | 10.1080/01621459.2018.1482754 | S | F |
| 53 | Papaspiliopoulos2017 | Papaspiliopoulos O.; Rossell D.; Bayesian block-diagonal variable selection and model averaging (arXiv title: Scalable Bayesian variable selection and model averaging under block orthogonal design); Biometrika; 104(2); 343-359 | 2017 | 10.1093/biomet/asx019 (arXiv:1606.03749) | P | F |
| 54 | Prive2020 | Prive F; Arbel J; Vilhjalmsson BJ. LDpred2: better, faster, stronger. Bioinformatics 36(22-23) 5424-5431 | 2020 | 10.1093/bioinformatics/btaa1029 | O | F |
| 55 | Qian2020 | Qian J; Tanigawa Y; Du W; Aguirre M; Chang C; Tibshirani R; Rivas MA; Hastie T. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. PLOS Genetics 16(10) e1009141 | 2020 | 10.1371/journal.pgen.1009141 | F | F |
| 56 | Ray2022 | Ray K.; Szabo B.; Variational Bayes for high-dimensional linear regression with sparse priors; J. Amer. Statist. Assoc.; 117(539); 1270-1281 | 2022 | 10.1080/01621459.2020.1847121 (arXiv:1904.07150) | P | F |
| 57 | Rockova2014 | Rockova V.; George E.I.; EMVS: the EM approach to Bayesian variable selection; J. Amer. Statist. Assoc.; 109(506); 828-846 | 2014 | 10.1080/01621459.2013.869223 | S | F |
| 58 | Rockova2018 | Rockova V.; George E.I.; The spike-and-slab LASSO; J. Amer. Statist. Assoc.; 113(521); 431-444 | 2018 | 10.1080/01621459.2016.1260469 | P | F |
| 59 | Rossell2021 | Rossell D.; Abril O.; Bhattacharya A.; Approximate Laplace approximations for scalable model selection; J. R. Stat. Soc. Ser. B; 83(4); 853-879 | 2021 | 10.1111/rssb.12466 (arXiv 2012.07429) | P | F |
| 60 | Schafer2013 | Schafer C.; Chopin N.; Sequential Monte Carlo on large binary sampling spaces; Statistics and Computing; 23(2); 163-184 | 2013 | 10.1007/s11222-011-9299-z (arXiv:1101.6037) | S | F |
| 61 | Scheetz2006 | Scheetz TE; Kim KYA; Swiderski RE; Philp AR; Braun TA; Knudtson KL; et al. Regulation of gene expression in the mammalian eye and its relevance to eye disease. Proc Natl Acad Sci USA 103(39) 14429-14434 | 2006 | 10.1073/pnas.0602562103 | O | F |
| 62 | Scott2010 | Scott J.G.; Berger J.O.; Bayes and empirical-Bayes multiplicity adjustment in the variable-selection problem; Annals of Statistics; 38(5); 2587-2619 | 2010 | arXiv:1011.2333; DOI 10.1214/10-AOS792 | P | F |
| 63 | Sesia2019 | Sesia M; Sabatti C; Candes EJ. Gene hunting with hidden Markov model knockoffs; Biometrika 106(1):1-18 | 2019 | 10.1093/biomet/asy033; arXiv:1706.04677 | K | F |
| 64 | Sesia2021 | Sesia M; Bates S; Candes E; Marchini J; Sabatti C. False discovery rate control in genome-wide association studies with population structure. Proc Natl Acad Sci USA 118(40) e2105841118 | 2021 | 10.1073/pnas.2105841118 | K | F |
| 65 | Shin2018 | Shin M.; Bhattacharya A.; Johnson V.E.; Scalable Bayesian variable selection using nonlocal prior densities in ultrahigh-dimensional settings; Statistica Sinica; 28(2); 1053-1078 | 2018 | arXiv:1507.07106; DOI 10.5705/ss.202016.0167 | P | F |
| 66 | SongLiang2015 | Song Q.; Liang F.; A split-and-merge Bayesian variable selection approach for ultrahigh dimensional regression; J. R. Stat. Soc. Ser. B; 77(5); 947-972 | 2015 | 10.1111/rssb.12095 | S | F |
| 67 | Staerk2024 | Staerk C.; Kateri M.; Ntzoufras I.; A Metropolized adaptive subspace algorithm for high-dimensional Bayesian variable selection; Bayesian Analysis; 19(1); 261-291 | 2024 | arXiv:2105.01039; DOI 10.1214/22-BA1351 | S | F |
| 68 | Su2017 | Su W; Bogdan M; Candes E. False discoveries occur early on the Lasso path; Annals of Statistics 45(5):2133-2150 | 2017 | 10.1214/16-AOS1521; arXiv:1511.01957 | F | F |
| 69 | Tibshirani1996 | Tibshirani R. Regression shrinkage and selection via the lasso; Journal of the Royal Statistical Society Series B 58(1):267-288 | 1996 | 10.1111/j.2517-6161.1996.tb02080.x | F | F |
| 70 | Titsias2017 | Titsias M.K.; Yau C.; The Hamming ball sampler; J. Amer. Statist. Assoc.; 112(520); 1598-1611 | 2017 | arXiv:1504.08133; DOI 10.1080/01621459.2016.1222288 | S | F |
| 71 | Valdar2006 | Valdar W; Solberg LC; Gauguier D; Cookson WO; Rawlins JNP; Mott R; Flint J. Genetic and environmental effects on complex traits in mice. Genetics 174(2) 959-984 (companion of the Nat Genet 38:879 HS-mice GWAS paper) | 2006 | 10.1534/genetics.106.060004 | O | F |
| 72 | Wan2021 | Wan K.Y.Y.; Griffin J.E.; An adaptive MCMC method for Bayesian variable selection in logistic and accelerated failure time regression models; Stat. Comput.; 31(1); article 6 | 2021 | 10.1007/s11222-020-09974-2 | S | F |
| 73 | Wang2016 | Wang X; Leng C. High dimensional ordinary least squares projection for screening variables; Journal of the Royal Statistical Society Series B 78(3):589-611 | 2016 | 10.1111/rssb.12127; arXiv:1506.01782 | Sc | F |
| 74 | Wang2020 | Wang G.; Sarkar A.; Carbonetto P.; Stephens M.; A simple new approach to variable selection in regression with application to genetic fine mapping (SuSiE); J. R. Stat. Soc. B; 82(5); 1273-1300 | 2020 | 10.1111/rssb.12388 (bioRxiv 10.1101/501114) | G | F |
| 75 | Wasserman2009 | Wasserman L; Roeder K. High-dimensional variable selection; Annals of Statistics 37(5A):2178-2201 | 2009 | 10.1214/08-AOS646; arXiv:0704.1139 | F | F |
| 76 | Weissbrod2020 | Weissbrod O; Hormozdiari F; Benner C; Cui R; Ulirsch J; Gazal S; et al. Functionally informed fine-mapping and polygenic localization of complex trait heritability. Nat Genet 52(12) 1355-1363 | 2020 | 10.1038/s41588-020-00735-5 | G | F |
| 77 | Wen2016 | Wen X; Lee Y; Luca F; Pique-Regi R. Efficient integrative multi-SNP association analysis via deterministic approximation of posteriors. Am J Hum Genet 98(6) 1114-1129 | 2016 | 10.1016/j.ajhg.2016.03.029 | G | F |
| 78 | Wu2009 | Wu TT; Chen YF; Hastie T; Sobel E; Lange K. Genome-wide association analysis by lasso penalized logistic regression. Bioinformatics 25(6) 714-721 | 2009 | 10.1093/bioinformatics/btp041 | F | F |
| 79 | Yang2016 | Yang Y.; Wainwright M.J.; Jordan M.I.; On the computational complexity of high-dimensional Bayesian variable selection; Annals of Statistics; 44(6); 2497-2532 | 2016 | 10.1214/15-AOS1417 (arXiv:1505.07925) | S | F |
| 80 | Zanella2019 | Zanella G.; Roberts G.; Scalable importance tempering and Bayesian variable selection; J. R. Stat. Soc. B; 81(3); 489-517 | 2019 | 10.1111/rssb.12316 (arXiv:1805.00541) | S | F |
| 81 | Zhang2010 | Zhang C-H. Nearly unbiased variable selection under minimax concave penalty; Annals of Statistics 38(2):894-942 | 2010 | 10.1214/09-AOS729; arXiv:1002.4734 | F | F |
| 82 | Zhou2013 | Zhou X; Carbonetto P; Stephens M. Polygenic modeling with Bayesian sparse linear mixed models. PLoS Genet 9(2) e1003264 | 2013 | 10.1371/journal.pgen.1003264 | P | F |
| 83 | Zhou2022 | Zhou Q.; Yang J.; Vats D.; Roberts G.O.; Rosenthal J.S.; Dimension-free mixing for high-dimensional Bayesian variable selection; J. R. Stat. Soc. B; 84(5); 1751-1784 | 2022 | 10.1111/rssb.12546 (arXiv:2105.05719) | S | F |
| 84 | Zhu2017 | Zhu X; Stephens M. Bayesian large-scale multiple regression with summary statistics from genome-wide association studies. Ann Appl Stat 11(3) 1561-1592 | 2017 | 10.1214/17-AOAS1046 | P | F |
| 85 | Zhu2020 | Zhu J; Wen C; Zhu J; Zhang H; Wang X. A polynomial algorithm for best-subset selection problem; PNAS 117(52):33117-33123 | 2020 | 10.1073/pnas.2014241117 | B | F |
| 86 | Zhu2022abess | Zhu J; Wang X; Hu L; et al. abess: a fast best-subset selection library in Python and R; Journal of Machine Learning Research 23(202):1-7 | 2022 | arXiv:2110.09697 | B | F |
| 87 | Zou2006 | Zou H. The adaptive lasso and its oracle properties; Journal of the American Statistical Association 101(476):1418-1429 | 2006 | 10.1198/016214506000000735 | F | F |
| 88 | Zou2022 | Zou Y; Carbonetto P; Wang G; Stephens M. Fine-mapping from summary data with the Sum of Single Effects model. PLoS Genet 18(7) e1010299 | 2022 | 10.1371/journal.pgen.1010299 | G | F |
| 89 | ZouHastie2005 | Zou H; Hastie T. Regularization and variable selection via the elastic net; Journal of the Royal Statistical Society Series B 67(2):301-320 | 2005 | 10.1111/j.1467-9868.2005.00503.x | F | F |
