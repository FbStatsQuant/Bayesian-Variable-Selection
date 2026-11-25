# BENCH_DESIGN extraction schema (one row per paper)

Write rows to your scout file as a TSV (tab-separated, header below, one line per paper; no tabs/newlines inside cells; use ";" inside cells).
Header:
key	citation	year	doi_or_arxiv	open_url	field	X_design	X_detail	n	p_max	s0	beta_SNR	noise	replicates	metrics	competitors	real_datasets	code_data	source_pages	read_level

Field meanings:
- key: FirstAuthorYear (e.g. Johndrow2020).
- citation: authors (all, or first 3 + "et al."), title, journal/venue, volume(issue), pages.
- doi_or_arxiv: DOI (preferred; 10.xxxx/...) or arXiv id. Must be checked against the paper/publisher, not guessed.
- open_url: an open full-text URL you actually opened (arXiv/PMC/author page), else "none".
- field: BVS-sampler | BVS-prior | freq-penalised | best-subset | knockoffs | screening | fine-mapping/GWAS | review/benchmark | other.
- X_design: one or more of iid-N(0,I) | AR1(rho=...) | block(size, rho) | equicorr(rho) | Toeplitz | factor | real-X(synthetic beta) | real-X+real-y | binary/SNP-genotypes | other. List ALL simulation designs in the paper.
- X_detail: anything needed to reproduce (rho values, block sizes, column scaling).
- n; p_max (largest p in any simulation; also list the p grid if several, e.g. "1e3;1e4;1e5"); s0 (true model size(s)).
- beta_SNR: how true coefficients are set (fixed values, random signs, decaying, beta_min) and the signal level (SNR, R^2, PVE/heritability h^2, sigma).
- noise: Gaussian sigma^2 / heavy-tailed / other.
- replicates: number of simulated data sets per setting.
- metrics: e.g. TPR/power, FDR/FDP, MCC, F1, Hamming, exact recovery P(S_hat=S0), PIP calibration, AUC/ROC/PR, coverage, CS coverage/size (SuSiE), estimation error ||beta_hat-beta||, prediction MSE, runtime, ESS/ESS-per-second, mixing diagnostics.
- competitors: methods compared.
- real_datasets: name (n, p) and what is done with it.
- code_data: code/data availability (URL or package).
- source_pages: the page/section/table numbers in the paper where you read the setup (so a checker can re-open it).
- read_level: full-text (you read the simulation and data sections in the paper itself) | abstract-only (state why). Rows must come from the paper text, never from memory.
