# FAILED_ATTEMPTS — what has been tried for selection and did not beat the median/HPM (do not retry as is)

Sources: `Others/2_BVS_brainstorm_20261005/` (FINAL_RECOMMENDATIONS.md Sec. 4, precheck/rules*_results.csv),
`SMC_BVS_Manuscript.tex` (cycle 1 and earlier), `Others/1_Latest_work_cycle1_and_next/cycle1_diagnosis/`.
Counts are exact recovery out of 100 for S1..S5 (exact posterior or V-reweighted SMC; SMC = exact here) unless stated.

| Idea | Result | Why it failed (as diagnosed) |
|---|---|---|
| BFDR 1/5/10 % (Bernoulli 0.2) | 1 %: 81/79/34/2/42; 5 %: 93/87/57/12/56; 10 %: 80/78/69/21/58 | wins S1–S2 (removes noise extras); collapses in S3–S5 because weak signals have split mass (PIP ~0.77), so including both pushes mean(1−PIP) above q |
| BFDR under any other size prior | same pattern | same arithmetic |
| Expected-F1 maximiser / GFM (Waegeman 2014) | 81/78/63/21/43 (rates, 181 datasets) | trades exactness for partial credit |
| Non-marginal block decisions (Chandra & Bhattacharya 2019) | 83/78/73/18/57 | reduces to a size-tilted block-MAP |
| Block-MAP on X-clusters (cycle 1, rho=.85, 20 sets) | 8/20 vs HPM 9/20 | same ceiling |
| Adaptive threshold / posterior benchmarking (Li, Tokdar, Xu 2025) | 75/84/68/34/60 | worse S1, S3, S5 |
| Size-first then best model; optimal predictive model (Barbieri et al. eq 1.2) | S1 0.12 and 0.34 (65 sets) | strong over-selection (multiplicity inflates size posterior under Bernoulli(0.2)) |
| EB inclusion probability h | h-hat 0.20–0.22 everywhere | no change from h = 0.2 |
| Independent slab Lambda = I/tau | HPM 77/81/71/18/38 (rates) | neutral to worse; cycle-1 lead (12/20 vs 9/20) did not replicate |
| Objective size priors Beta(1,2), Half-p, BB(1,1) | HPM at best 87/82/74/33/64 | not sparse enough to kill multiplicity supersets |
| Matryoshka theta=1; Bernoulli(1/(p+1)) | HPM 90/90/75/30/69; 89/90/74/30/69 | close to BB(1,p), lose S1 (omissions) |
| Sparser theory priors Beta(1,p^1.5), Beta(1,p^2) | HPM 86/90/73/27/68; 72/82/61/15/55 | over-penalise, omit weak signals |
| Block-exact Gibbs / Hamming-ball kernel (Titsias & Yau) | no Z/PIP/decision change at p=30 | the bridge is not mixing-limited at p=30 |
| pMOM non-local prior, cap |S|<=8 (cycle 1, 20 sets, rho=.85) | HPM 8/20 vs 9/20; Z errors −73 %, −56 %, −41 % | ceiling unchanged; capped target breaks the composite start (Z) |
| Predictive projection (p=20) | 8/30 | over-selects |
| Central coefficient intervals; factor-adjusted target | 0/20; 0/20 | wrong object |
| Resolution ladder (cycle 1) | full resolution 0/20 | reports blocks whole |
| Credible groups (singletons) | 2/20 fully resolved | wrong object for exact recovery |
| F1 extensions (cond. RB-F1, pair moves, Beta prior) | 9/20 in all arms | ceiling |

Data ceiling (cycle 1, rho = .85): the truth is the best-fitting size-5 subset in only 11/20 datasets; 10 of 11 HPM failures
are likelihood-driven proxy swaps of the weak signals 8 (beta .6) and 19 (beta .5). Across 200 earlier fresh datasets the exact
HPM equals the truth in 50.5 %.
| BB(1,p) model prior + HPM (Phase 2, 2026-10-13; in-engine, exact start) | S1–S6 431/600 vs Bern-HPM 400, but W1–W6 63/600 vs 128 (pre-registered hedge fired) | multiplicity correction removes false inclusions but the inclusion cost log((1+k)/(59−k)) (−4.1 to −2.4 nats at k ≤ 4) drops weak true signals; omission rate higher in every signal bin |
