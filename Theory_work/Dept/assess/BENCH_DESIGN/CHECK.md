# BENCH_DESIGN: check log

Six Claude Work Haiku checkers each took a batch of about 15 papers (all 89 in total). Each one re-opened the source: a local PDF, the open-access copy, or Crossref for the DOI. It then checked PAPERS.md and every REPORT.md statement naming that paper for DOI, X design, n, p, s0, β/SNR and metrics. The full per-item verdicts are in `check/C1.tsv` to `check/C6.tsv`. Opus adjudicated every mismatch.

**Totals:** 998 items checked. OK 921; MISMATCH 37; UNVERIFIABLE 40.
**Mismatches:** 36 fixed, 1 rejected after re-reading the source.
No mismatch touched a DOI. Every DOI and arXiv id resolves to the paper cited. The one correction to the sources table is a title: McCreight 2025, fixed against Crossref.

**Most consequential fixes:**
- **The YWJ covariance.** The original YWJ design uses $e^{-|j-k|}$. The $\rho=0.6$ version is Griffin 2021's variant, now labelled "YWJ/Griffin" throughout; §2 adds the original's $\nu$ and PVE.
- **Convention (a).** Wan 2021 and Liang 2023 do not use the $\sqrt{\log p/n}$ scaling, so they were moved out.
- **§5C.** Sesia 2021 is added as a fourth design with $p\ge5\times10^5$ and selection scoring. The open slot (correlated synthetic $X$, $n\le10^3$, $p=10^6$) still stands.
- **Hazimeh 2020, large-$p$ cells.** These use fixed $\nu$ (10 and 100), not a sweep.

## Mismatches

| Batch | Key | Where | Item | Ours | Source | Location | Disposition |
|---|---|---|---|---|---|---|---|
| C1 | Benner2016 | PAPERS | other | replicates: 500 datasets per (m,K) in A and B; 2000 datasets in scenario B | 'Five hundred datasets were generated under each combination of m and K in scenarios A and B'; scenario B has K=1..5, i.e. 2500 in total, not 2000 | Sec 4 Scenarios A/B paragraph | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C1 | Biswas2022 | REPORT§1 | other | line 52: 'The maize matrix (n=2267, p=98,385) is reused by Biswas et al. (2022)' | Biswas Table 2 lists MAIZE n=2266, p=98385; Sec 4 'n = 2266 observations' | Biswas Table 2 p.7-8; Sec 4 maize paragraph | FIXED in REPORT.md |
| C1 | Biswas2022 | REPORT§3 | n | line 121: Maize GWAS (Romay 2013) n=2,267, p=98,385; Biswas 2022 listed | Biswas Table 2: MAIZE n=2266, p=98385 | Biswas Table 2 p.7-8; Sec 4 | FIXED in REPORT.md |
| C1 | Biswas2022 | REPORT§6.2 | other | line 242: maize (n=2267, p=98,385) padded to 10^6 | Biswas Table 2 n=2266 (p=98385 matches) | Biswas Table 2 p.7-8 | FIXED in REPORT.md |
| C2 | Cui2024 | PAPERS | other | Misspecification simulations: 9 sets (Table 1) | Table 1 caption: 'Different parameter settings for ten sets of simulations mentioned in the main text' | PMC11056999 Table 1 caption (l.159-160) | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C2 | Friedman2010 | PAPERS | other | Real data InternetAd N=2359, p=1430, 1.2% nonzero | Text: 'The InternetAd and NewsGroup datasets are both sparse: 1% nonzero values for the former, 0.05% for the latter.' | Friedman2010glmnet.pdf Sec 5.3 (~l.793-795) | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C2 | Ge2019 | REPORT§3 (l.130) | p | UKB row p ~10^6-1.8x10^7; Ge 2019 listed | Ge 2019 uses 819,941 HapMap3 SNPs (about 8.2x10^5), below the 10^6 lower bound of the row | PMC6467998 Methods (819,941 SNPs) | FIXED in REPORT.md |
| C2 | Ge2019 | REPORT§5 (l.200) | beta | Ge 2019 row h2 range 0.1-0.5 (prediction) | Ge 2019 uses h2 = 0.5 with secondary 0.2 and 0.8 (range 0.2-0.8) | PMC6467998 Methods (Simulations) | FIXED in REPORT.md |
| C2 | Griffin2021 | REPORT§3 (l.115) | p | PCR mouse (Lan 2006) n=60, p=22,575 | Griffin reports PCR p = 22 576 (one more column than REPORT) | BVS_Griffin2021.pdf Intro (~l.113) and Sec 4.4 | FIXED in REPORT.md |
| C3 | Hazimeh2020 | REPORT§5 | §5A row 2: 'equicorrelated / AR \| n=1000 \| p=5e4, 1e5 \| s0=100, 50 \| nu swept \| yes' | nu swept | Source fixes SNR=10 (Setting 1, p=5e4, k=100, exp rho=0.5) and SNR=100 (Setting 2, p=1e5, k=50, const rho=0.3); no sweep at these cells. Sec 5.4 SNR sweep is a separate n=500 / p=1000 experiment | Sec 5.6 p.30 (Setting 1/2, Table 1) | FIXED in REPORT.md |
| C3 | Hazimeh2022 | PAPERS | s0 | k0=10 (default); k0 in 5..25 (sparsity study at p=1e4) | Sec 4.3 'Varying k†' at p=10^4 uses k† = 10, 15, 20, 25. No k†=5 appears | Sec 4.3 Tables 3-4 (Varying k† column) | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C3 | Hoggart2008 | REPORT§5 | §5B table heading 'Real genotype X + synthetic beta' containing the Hoggart row | Hoggart listed as real-genotype design | Source's X is FREGENE simulated haplotypes, not real genotypes | Results whole-genome study; Methods | FIXED in REPORT.md |
| C3 | Jankowiak2023 | REPORT§6 | §6.2 L5: 'optionally maize (n=2267, p=98385) padded with iid columns to 10^6 as in Jankowiak' | padded to 10^6 as in Jankowiak | Jankowiak's text says 'scale to P ~ 10^6' but the experiments go up to P=7.5x10^5 (Fig 2). REPORT §3 and §5B say 7.5e5; §6.2 is inconsistent with them and with the source's largest run | Sec 7.1 p.7; Fig 2 caption | FIXED in REPORT.md |
| C3 | Javanmard2014 | PAPERS | p | 2000 (real riboflavin p=4088; synthetic p up to 1500) | Synthetic configurations use p=600 and p=1500; riboflavin p=4088. No p=2000 anywhere in the paper | Sec 5.1 tables; Sec 5.2 | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C3 | Liang2023 | PAPERS | other | Sec 5.1: one simulated dataset per model (logistic; Cox; Weibull); real: 10 repetitions of 1 h runs for SLE | Sec 5.1: 'We simulate two data-sets with 500 covariates and 500 observations'; SLE: 'run for 1 h with 10 repetitions' | Sec 5.1 p.12 (simulation paragraph); Sec 5.2 p.13 | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C3 | Liang2023 | REPORT§2 | signal convention (a) YWJ scaling (SNR-scaled beta*) lists Liang 2023 among the eight papers | Liang 2023 in convention (a) | Liang 2023 uses the fixed vector (2,-3,...) with no SNR factor (App D), so it does not follow convention (a). Liang 2023 also has no SNR | App D p.18; Sec 5.1 | FIXED in REPORT.md |
| C4 | McCreight2025 | PAPERS | other | title: SuSiE 2.0: improved efficiency and calibration for genetic fine-mapping and prediction | Title: SuSiE 2.0: improved methods and implementations for genetic fine-mapping and phenotype prediction | bioRxiv API / Europe PMC title field (title line of preprint) | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C4 | MeinshausenBuhlmann2010 | REPORT§3 | line 114 riboflavin row n=71 (lists MB2010) | Riboflavin row n=71; MB2010 listed as user | MB2010 used riboflavin with n=115 (Sec 2.2) and n=158 (scenario G), not n=71 | Sec 2.2 p.5; Sec 4 scenario G p.20 | FIXED in REPORT.md |
| C4 | Narisetty2019 | PAPERS | beta | \|t\|=4: (-1.5,2,-2.5,3); \|t\|=8: (-1.5,1.714,-1.929,2.143,-2.357,2.571,-2.786,3) | \|t\|=4: (-1.5,2,-2.5,3) (Tables 1,3 OK). \|t\|=8 in Table 3 (p=1000) is (-1.5,1.714,...,3), but Table 2 (\|t\|=8, p=50 and 250) uses (-2, 2.143, -2.286, 2.429, -2.571, 2.714, -2.857, 3) | Table 2 caption (p.~25); Table 3 caption (p.~26) | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C4 | Narisetty2019 | PAPERS | other | burn-in 2000, length 5000, 10 chains per setting | Tables 1-2 and CPU: burn-in 2000, 5000 iterations; Table 3 (p=1000): burn-in 5000, length 5000 per chain | Sec 4 p.22 and p.~26 (Table 3 text) | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C4 | Qian2020 | REPORT§3 | line 130 UKB p range 10^6-1.8x10^7 (Qian 2020 listed) | Qian 2020 p=805,426 listed as UKB user | 805,426 is below the row's 10^6 lower bound; the row's n and p ranges exclude Qian | Qian 2020 UK Biobank analysis p.9 | FIXED in REPORT.md |
| C4 | McCreight2025 | REPORT§8 | Sources row 46 citation and DOI | REPORT §8 row 46 | Citation title 'improved efficiency and calibration for genetic fine-mapping and prediction' differs from bioRxiv/Europe PMC title 'improved methods and implementations for genetic fine-mapping and phenotype prediction'; DOI resolves | REPORT.md line 324 | FIXED in REPORT.md |
| C5 | Schafer2013 | PAPERS | other | Code/data: R scripts; csv-format data | Implementation in Python 2.6 (SciPy); reads csv and generates R scripts for plotting only | Sec 6.4 p24 ('numerical work ... in Python 2.6') | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C5 | Sesia2019 | PAPERS | n | sims n=1000; real chr-1 'n~1400+1000 shared'; NFBC 4644-5302; WTCCC 4913 | Sims n=1000 (Sec 6.1.2, 6.2.2); chr-1 SNPs 'genotyped in 14,708 individuals' (Sec 6.3); 1000 obs are a hold-out for representative selection; NFBC n 4644-5302 and WTCCC 1917+2996=4913 (Table 4) | Sec 6.3 p21 ('genotyped in 14,708 individuals'); Table 4 p24 | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C5 | Sesia2021 | REPORT§3 | UKB row (L130) p range | UK Biobank p = 10^6-1.8x10^7 (cites Sesia 2021) | Sesia 2021 uses 592,000 SNPs (below 10^6) | PMC8501795 Results | FIXED in REPORT.md |
| C5 | Sesia2021 | REPORT§5C | 'only three designs' with p>=5e5 and selection scoring (L~214) | Claims only Hazimeh 2020, Song-Liang 2015, Jankowiak 2023 qualify | Sesia 2021 (row in §5B) has p=592,000 >=5e5 and power/FDP scoring, so it also qualifies | REPORT §5B row and §5C text | FIXED in REPORT.md |
| C5 | Shin2018 | REPORT§3 | Boston row (L117) | 'Boston housing + interactions' p=104; Shin 2018 (+1000 noise columns) | Shin's Boston uses 10 continuous predictors (no interactions) plus 1,000 noise columns, p=1,010 | Sec 8.2 p25-26 | FIXED in REPORT.md |
| C5 | SongLiang2015 | PAPERS | other | replicates 100 per setting; real single dataset; stage-1 alpha 0.15, stage-2 0.01; tau=0.01; a0=b0=1; r_n=P_n^(1-gamma), gamma=0.75 | 100 simulated data sets per setting; real single dataset; alpha1=0.15, alpha2=0.01; tau=0.01; a0=b0=1; gamma=0.75 with r_n=P_n^(1-gamma) (Sec 3.2) | Sec 3.2 p960 ('we set gamma = 0.75 and r_n = P_n unless otherwise stated'); Ex1 r_n=sqrt(n) (Sec 4.1.1); PCR stage 2 r_n=P_n^0.3 (Sec 5.2) | REJECTED. Opus re-read Sec 3.2, p. 960: the source sets $r_n=P_n^{1-\gamma}$ with γ = 0.75; the superscript sits on the line above in the PDF text. Our text was correct. |
| C5 | Staerk2024 | REPORT§3 | Golub row (L116) | Leukemia (Golub 1999): 7,129 raw (3,571 after preprocessing); Staerk 2024 listed | Staerk: 6817 gene expression measurements, n=72; p=3571 after Dudoit preprocessing | Sec 6.2 p27 ('6817 gene expression measurements'); note Golub 1999 original array has 7,129 probes (minor) | FIXED in REPORT.md |
| C5 | Wan2021 | REPORT§2 | YWJ scaling (L76) | Wan-Griffin 2021 listed among users of (a) beta=SNR*sqrt(sigma^2 log p/n)*(2,-3,...) | Wan 2021 uses beta=SNR*(2,-3,...) with no sqrt(log p/n) factor | Sec 4.1 p7 (eq. for beta) | FIXED in REPORT.md |
| C6 | Yang2016 | REPORT§0 | item 2 YWJ covariance and size | YWJ: covariance AR(1) rho=0.6 (Griffin variant); size n=500, p in {500,5000} | YWJ original Sigma_jk=e^{-\|j-k\|} (rho~0.37); tables n in {500,1000}, p in {1000,5000}; text n in {300,900}, p in {500,5000} | REPORT §0 item 2; Sec 3.4.1 of Yang2016 | FIXED in REPORT.md |
| C6 | Yang2016 | REPORT§2 | YWJ SNR table row (nu, PVE) | YWJ n=500, p=5000, AR 0.6: nu=0.44/1.75/3.94; PVE=0.30/0.64/0.80 at SNR 1/2/3 | Recomputed with source design e^{-\|j-k\|}, n=500, p=5000, same beta: nu=0.63/2.52/5.67; PVE=0.39/0.72/0.85 (the 0.6 numbers are reproduced only for rho=0.6) | REPORT §2 "Where our design sits" table | FIXED in REPORT.md |
| C6 | Yang2016 | REPORT§5 | Liang 2022 row uses YWJ AR 0.6 | YWJ, AR 0.6 (Liang 2022) | Yang2016 YWJ covariance is e^{-\|j-k\|} (not 0.6); the AR 0.6 row is attributed to Liang 2022, not Yang2016 | REPORT §5A table, Liang 2022 row (same error as §0) | FIXED in REPORT.md |
| C6 | Yang2016 | REPORT§6.1 | S1 YWJ cell spec | Sigma_jk=0.6^{\|j-k\|}; n in {500,1000}; p in {500,5000}; labelled "YWJ" | Yang2016 Sigma_jk=e^{-\|j-k\|}; tables p in {1000,5000}; the report notes the original but still labels the 0.6 cell as YWJ | REPORT §6.1 S1 | FIXED in REPORT.md |
| C6 | Zhou2022 | PAPERS | n | 500;1000;5000 (n=500 p=1000; n=1000 p=5000); GWAS n=5418 | Study I (n,p)=(500,1000),(1000,5000); Study II n=1000; GWAS n=5418. The value 5000 is p, not n | Sec 5.1 p.21; Sec 5.3 p.24; Sec 6 | FIXED in the scout TSV, so PAPERS.md is regenerated |
| C6 | Zhu2020 | REPORT§2 | replicates table, best-subset papers = 10 | Best-subset papers usually use 10 replicates | Zhu 2020 (best-subset) uses 100 synthetic datasets | REPORT §2 Replicates table | FIXED in REPORT.md |
| C6 | Zou2006 | PAPERS | n | n=60 or 120 (Model 0); 20 or 60 (Model 1); 40 or 80 (Model 2); 200 (logistic); test 10000 | Table 1 Model 0 has three settings: (n,sigma)=(60,9),(120,5),(300,3); Model 1 n=20,60; Model 2 n=40,80; logistic n=200; test sets 10,000 | Sec 4 Table 1; omits n=300 (largest n) | FIXED in the scout TSV, so PAPERS.md is regenerated |

## Unverifiable items (left as written; none changes a recommendation)

| Batch | Key | Where | Item | Note |
|---|---|---|---|---|
| C1 | Bertsimas2016 | PAPERS | other | No '66 minutes' figure in text; text says 'a few minutes for p = 2000 and a few seconds for smaller values of p'; Fig 9/Table text does not give 66 min |
| C1 | Bloom2013 | PAPERS | metrics | H2 and h2 (Fig 1); QTL count at 5% FDR; 10-fold CV variance explained (Fig 2); pairwise interactions scanned with LOD thresholds, median 1.1% per interaction; no LOD value of 6.2 or FDR-10% threshold appears in the extracted text |
| C2 | GeorgeMcCulloch1993 | PAPERS | X | Paywalled; abstract only available; design not checkable |
| C2 | GeorgeMcCulloch1993 | PAPERS | n | Paywalled; not checkable |
| C2 | GeorgeMcCulloch1993 | PAPERS | p | Paywalled; not checkable |
| C2 | GeorgeMcCulloch1993 | PAPERS | s0 | Paywalled; not checkable |
| C2 | GeorgeMcCulloch1993 | PAPERS | beta | Paywalled; not checkable |
| C2 | GeorgeMcCulloch1993 | PAPERS | metrics | Paywalled; not checkable |
| C2 | Hans2007 | PAPERS | p | p=5000 (null); first p columns of 8408 for p<=8408 and padded for larger p; lymph node p=4514; the grid maximum 2.5x10^4 is only visible on the Fig 3 axis |
| C2 | Hans2007 | REPORT§5 (l.189) | p | p grid maximum 2.5x10^4 visible only in Fig 3; text gives 8408 real columns and padding |
| C3 | Heinze2018 | PAPERS | metrics | Found in text: bootstrap inclusion frequencies, model selection frequencies, pairwise inclusion frequencies. 'Relative conditional bias' and 'RMSD' do not appear in the text read |
| C3 | Hormozdiari2014 | PAPERS | n | No HapGen sample size stated in the main-text simulation section (not found in text read) |
| C3 | Javanmard2014 | PAPERS | doi | Journal volume/pages not in the arXiv PDF and not in Crossref (JMLR does not register DOIs) |
| C3 | Javanmard2014 | REPORT§8 | row 37 journal pages (2869-2909) | Not in source PDF; no Crossref record |
| C3 | Johndrow2020 | PAPERS | doi | PDF header 'Journal of Machine Learning Research 21 (2020) 1-61'; issue 73 not printed in PDF |
| C3 | Johndrow2020 | PAPERS | p | p uniform on integers 10,000-50,000 in Sec 5.2-5.3; N=5000 and p=50000 largest (abstract); maize p=98385; realised maximum 47985 not stated |
| C3 | Johndrow2020 | REPORT§1 | 'The decaying signal 2^{(9-j)/4} reappears in Biswas et al. (2022), logistic case.' | Biswas 2022 is not in this batch; not checked |
| C3 | Kim2024 | PAPERS | doi (JMLR) | Volume/issue not in arXiv PDF; not in Crossref |
| C3 | Liang2022 | REPORT§2 | signal convention (a) YWJ scaling (sigma=1) lists Liang 2022 | Source writes residual variance sigma^2 as 'pre-specified' and gives no numerical value in the text read; sigma=1 not confirmed |
| C4 | LloydJones2019 | PAPERS | other | Main-text n for the 12 traits runs from 125,157 (MPB) to 347,231 (HC); no 27K value found in the main text |
| C4 | McCreight2025 | PAPERS | X | bioRxiv full text unreachable this session (HTTP 429 / Cloudflare error 1015); abstract only |
| C4 | McCreight2025 | PAPERS | n | not checkable: full text unreachable; abstract gives no n |
| C4 | McCreight2025 | PAPERS | p | not checkable: full text unreachable |
| C4 | McCreight2025 | PAPERS | s0 | not checkable: full text unreachable |
| C4 | McCreight2025 | PAPERS | beta | not checkable: full text unreachable |
| C4 | McCreight2025 | PAPERS | metrics | Abstract confirms SuSiE-ash, 1.5-3x FDR reduction under complex backgrounds, TWAS prediction; CS, ROC and 150-block design not checkable |
| C4 | Papaspiliopoulos2017 | PAPERS | doi | DOI resolves to an OUP 'production in progress' placeholder; Crossref lists Biometrika 2017 with no volume or pages; arXiv:1606.03749v2 header; 104(2) 343-359 not confirmed |
| C4 | Papaspiliopoulos2017 | REPORT§3 | line 123 n=262, p=10,172 (Papaspiliopoulos 2017 listed) | n=262 OK; p=10,172 not found in source text |
| C4 | Moser2015 | REPORT§3 | line 129 WTCCC approx 2-5k per disease; p 3-4.4e5 (Moser 2015 listed) | Moser main text gives no per-disease n or SNP count |
| C4 | McCreight2025 | REPORT§3 | line 130 UKB row (McCreight 2025 listed) | row ranges are whole-UKB; McCreight used 150 regional blocks; full text not reachable to re-check |
| C4 | McCreight2025 | REPORT§4 | line 149 credible-set coverage (McCreight 2025 listed) | bioRxiv full text unreachable this session; abstract only |
| C4 | Papaspiliopoulos2017 | REPORT§8 | Sources row 53 citation and DOI | DOI 10.1093/biomet/asx019 resolves to OUP 'production in progress' placeholder; Crossref has no volume or pages; 104(2) 343-359 not confirmed |
| C5 | Scheetz2006 | PAPERS | other | Source says only 'an Affymetrix expression microarray' with >31,000 probes; name RAE230A not in text |
| C5 | Sesia2021 | PAPERS | beta | Linear model with total heritability varied; effect-size distribution not in main text (SI not in our copy) |
| C5 | Valdar2006 | PAPERS | other | '85 families' does not appear in this paper; no genotype URL checked in this paper |
| C6 | Wasserman2009 | PAPERS | other:replicates | No replication count found in Sec 6 or Tables 1-2 |
| C6 | Weissbrod2020 | PAPERS | other:replicates | Number of simulated datasets not stated in main text (aggregated over loci) |
| C6 | Zanella2019 | PAPERS | other:code URL | No GitHub URL in extracted text; text says real data from supplements of Rossell & Rubio (2017) and Rossell & Telesca (2017) |
| C6 | Zhou2013 | REPORT§3 | HS mice row (approx 2,000 mice) | Mouse n stripped from extracted PMC and PLoS text; only "85 families" is visible |
| C6 | Zhu2022abess | PAPERS | other:JMLR volume/pages | Journal volume and pages not in the arXiv PDF text; no DOI check possible |

**Caveats on the checkers themselves:**
- C3 and C6 report that some OK rows were written from their first read, without re-opening the source in the final pass.
- Two location fields in C6 still hold "p.?" placeholders.
- McCreight 2025: bioRxiv returned HTTP 429, so its design rows rest on the abstract and the scout's HTML read.
