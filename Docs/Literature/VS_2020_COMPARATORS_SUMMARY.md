# 2020 variable-selection papers and what they benchmarked against (compiled 2026-10-06)

Every entry was read in full text (empirical sections); detailed evidence with verbatim quotes and
section/table/figure locations is in `notes/A_local_2020_papers.md`, `notes/B_knockoff_2020_papers.md`,
`notes/C_bayes_opt_2020_papers.md`. Years verified via Crossref.

| # | Paper (2020) | Proposed method | Comparators actually run | Where | Metrics |
|---|---|---|---|---|---|
| 1 | Hastie, Tibshirani & Tibshirani, *Stat. Sci.* 35(4) | none (neutral comparison) | Best subset (Gurobi MIO), forward stepwise, lasso (glmnet), simplified relaxed lasso; validation-set tuning. L0Learn & SparseNet supplement only | Sec. 3, Table 1, Figs 5-8 | relative test error, PVE, #nonzeros, F-score, time |
| 2 | Bertsimas, Pauphilet & Van Parys, *Stat. Sci.* 35(4) | Boolean relaxation sub-gradient (SS); own cutting-plane MIO (CIO) | Lasso, ENet (glmnet); MCP, SCAD (ncvreg); stepwise explicitly excluded | Sec. 3-4, Table 7 | TPR, FDR, MSE/AUC, time |
| 3 | Wang, Sarkar, Carbonetto & Stephens, *JRSS-B* 82(5) (SuSiE) | SuSiE/IBSS | PIPs: CAVIAR, FINEMAP, DAP-G; credible sets: DAP-G, hierinf; lasso only for run time | Sec. 4.2-4.3, Figs 2-3, Tables 2-3 | PIP calibration, power-FDR, CS coverage/power/size/purity, time |
| 4 | Zhu, Wen, Zhu, Zhang & Wang, *PNAS* 117(52) (ABESS) | best-subset by splicing + SIC | exhaustive all-subsets+SIC; LASSO (glmnet); SCAD (gamma=3.7), MCP (gamma=3) (ncvreg); each tuned by SIC and CV | Table 1, Figs 1-2 | TPR, TNR, rel. error, size error, time |
| 5 | Hazimeh & Mazumder, *Oper. Res.* 68(5) (L0Learn) | L0/L0L1/L0L2 CD + local swaps | Lasso, relaxed lasso, elastic net (glmnet), MCP (ncvreg), forward stepwise, IHT; ridge in SNR study | Sec. 5, Figs 2-5, Tables 1-2 | TP/FP, support size, prediction error, recovery prob., time |
| 6 | Piironen, Paasiniemi & Vehtari, *EJS* 14(1) (projpred) | projection predictive selection | Lasso, relaxed lasso, elastic net (alpha=0.7, 0.3), ridge (glmnet, 10-fold CV); illustrative marginal rules (Gaussian, RHS, spike-and-slab PIP>0.5) | Sec. 2.3, 7.3-7.4 | MLPD, MSE/accuracy, #features, time |
| 7 | Bertsimas & Van Parys, *Ann. Stat.* 48(1) | exact cutting-plane sparse ridge regression | Lasso (glmnet) only | Sec. 4.2, Table 1, Fig. 1 | A% (TPR), F% (FDP), time |
| 8 | Ray, Szabó & Clara, *NeurIPS 33* | spike-and-slab VB (Laplace slab), logistic | VB-Gauss (own), varbvs, SkinnyGibbs, BinaryEMVS, BhGLM (bmlasso), rstanarm horseshoe | Sec. 5 Table 1, Supp. Table 3 | TPR, FDR, L2 error, MSPE, time |
| 9 | Sesia, Katsevich, Bates, Candès & Sabatti, *Nat. Commun.* 11:1093 (KnockoffZoom) | multi-resolution group knockoffs | BOLT-LMM (+PLINK clumping), LMM oracle, LMM+BH, LMM+Simes-BH, BOLT-LMM->CAVIAR, BOLT-LMM->SuSiE | Results; Supp. Notes 7-8 | power, FDP/FDR, resolution width, reproducibility |
| 10 | Huang & Janson, *Ann. Stat.* 48(5) | conditional knockoffs | unconditional model-X knockoffs with known F_X (SDP Gaussian; SCIP Markov chain; Ising) only | Sec. 3, App. D | power, FDR |

Caveats: #2 (arXiv v2), #5 (arXiv v3), #7 (arXiv v1 2017) read from preprints; journal versions not
checked. Excluded: Zanella 2020 JASA (no variable-selection experiment), Johndrow et al. 2020 JMLR
(no selection metrics). Alternates: Romano, Sesia & Candès "Deep Knockoffs" (JASA 115(532), online 2019);
Fan et al. "IPAD" (JASA 115(532), online 2019).
