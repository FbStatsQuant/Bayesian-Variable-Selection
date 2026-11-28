# CITE_CHECK: do the papers we cite for S1–S3 contain those designs?

**Theory Dept, 2026-11-24.** This check was ordered by the owner via HQ for the simulation suite fixed in HQ_DECISIONS c55d0722 (BENCH_DESIGN REPORT §6.1, S1–S3).

**Method.** Three Claude Work Haiku checkers each opened the full paper text; abstracts and our own notes did not count as evidence. They worked from `check/CITE_BRIEF.md`. For each spec item they recorded the page, the section/example/table and a verbatim quote, with one of three verdicts:
- **EXACT**: the paper states the spec as we give it;
- **SIMILAR**: the paper is close, and the difference is stated;
- **NOT FOUND**: the spec is not in the paper.

Opus re-read the decisive quotes against the PDFs: YWJ Sec 3.4.1, Griffin Sec 4.1, Hastie Sec 3.1, and Dezeure §2.5. No disagreement needed Sonnet adjudication. The raw rows are in `check/CITE_A.tsv` (YWJ, Griffin, Liang), `check/CITE_B.tsv` (Hastie, three versions) and `check/CITE_C.tsv` (George–McCulloch, Dezeure, Zanella–Roberts, Shin).

**Page conventions.**
- "p." means the PDF page of the copy named. Printed page numbers are given where they differ.
- arXiv copies carry no journal page numbers. A pointer into one should be cited as "arXiv vN, Sec x, p. y".

## 0. Summary by design

| Design | Cite as | Verdict |
|---|---|---|
| **S1**: AR Σ=0.6^{\|j−k\|}; n∈{500,1000}; p∈{500,5000}; β*=SNR·√(σ² log p/n)·(2,−3,2,2,−3,3,−2,3,−2,3,0,…); SNR∈{0.5,1,2,3}; σ²=1 | **Griffin, Łatuszyński & Steel (2021), Sec 4.1 + Table 1**, which states "We consider the simulated data example of Yang et al. (2016)" | **EXACT** (every item, in Griffin) |
| S1 origin | Yang, Wainwright & Jordan (2016), Sec 3.4.1 | **SIMILAR.** The β pattern, scaling, SNR grid and σ²=1 are EXACT. Σ is **e^{−\|j−k\|}** (ρ≈0.37), not 0.6^{\|j−k\|}; 0.6 does not appear in YWJ. YWJ's n and p are internally inconsistent: the text says n∈{300,900}, p∈{500,5000}; the tables say n∈{500,1000}, p∈{1000,5000}. |
| S1 at larger p (optional) | Liang, Livingstone & Griffin (2022), Sec 5.1 | **EXACT** for Griffin's design, extended to p=50,000 |
| **S2**: AR ρ^{\|i−j\|}, ρ∈{0,0.35,0.7}; (n,p,s)∈{(50,1000,5),(100,1000,10)}; beta-types 1,2,3,5; 10-point ν grid 0.05–6 | **Hastie, Tibshirani & Tibshirani (2020)**, Sec 3.1 "Setup", pp. 9–10 | **EXACT** (every item) in arXiv:1707.08692 v1 and v2, and in the authors' journal-title version. The typeset Stat. Sci. pages could not be opened (see §2). |
| **S3**, ρ=0.8 equicorrelation | **Dezeure, Bühlmann, Meier & Meinshausen (2015)**, §2.5 "Equi.corr" | **EXACT** for Σ_jk=0.8 (j≠k), at n=100, p=500, s0∈{3,15}. Those sizes differ from S3's. |
| **S3**, ρ=0.5 equicorrelation | **Shin, Bhattacharya & Johnson (2018)**, Sec 3.1 Case (1) | **EXACT** for compound symmetry Σ_jj'=0.5, at n=400, p∈{10⁴, 2·10⁴}, s0=5 |
| S3, ρ≈0.5 (classical) | George & McCulloch (1993), Example 4.2 | **SIMILAR.** It uses a common-factor construction X_i=X_i*+Z, which gives pairwise correlation "about .5", not a stated Σ; n=120, p=60, s0=45. |
| S3 size (S1's n,p) and s0=10 | none | **NOT FOUND in any paper.** This is an HQ default and must be described as our choice. |

## 1. S1: Yang–Wainwright–Jordan 2016 and Griffin–Łatuszyński–Steel 2021

**YWJ 2016**
- Ann. Statist. 44(6) 2497–2532, DOI 10.1214/15-AOS1417.
- Checked copy: arXiv 1505.07925v1, the only arXiv version. The journal page did not resolve for the checker.

| Item | Verdict | Location | Verbatim |
|---|---|---|---|
| β pattern, s*=10 | EXACT | p.12, Sec 3.4.1 | "we choose a design vector β* ∈ R^p with true sparsity s* = 10, taking the form β* = SNR √(σ² log p / n) (2, −3, 2, 2, −3, 3, −2, 3, −2, 3, 0, ···, 0)^T" |
| √(σ² log p/n) scaling | EXACT | p.12, Sec 3.4.1 | same formula |
| SNR grid | EXACT | p.12, Sec 3.4.1 | "SNR ∈ {0.5, 1, 2, 3}" |
| Σ | **SIMILAR** | p.12, Sec 3.4.1 | "Correlated design: Y ∼ N(Xβ*, σ²I_n) with x_i ∼ N(0, Σ) i.i.d. and Σ_jk = e^{−\|j−k\|}". This is AR with ρ=e^{−1}≈0.368, not 0.6. The paper also has an independent design, Σ=I. |
| n | **SIMILAR (internally inconsistent)** | text p.12, Sec 3.4.1; Tables 1–2, pp.13–14 | The text says "sample sizes n ∈ {300, 900}". The Table 2 caption says "sample size n ∈ {500, 1000}". |
| p | **SIMILAR (internally inconsistent)** | text p.12; Tables 1–2, pp.13–14 | The text says "number of covariates p ∈ {500, 5000}". The tables use p ∈ {1000, 5000}. |
| σ² | EXACT | p.12 | "setting the noise variance σ² = 1" |

**Griffin et al. 2021**
- Biometrika 108(1) 53–69, DOI 10.1093/biomet/asaa055.
- Checked copy: arXiv 1708.05678v3. The OUP journal text is paywalled; the checker saw only summary-level confirmation.

| Item | Verdict | Location | Verbatim |
|---|---|---|---|
| Attribution to YWJ | EXACT | p.13, Sec 4.1 | "We consider the simulated data example of Yang et al. (2016)." |
| β pattern, scaling, σ² | EXACT | p.13, Sec 4.1 | "e ∼ N(0, σ²I) for σ² = 1. The first 10 regression coefficients are non-zero and we use β* = SNR √(σ² log p / n) (2, −3, 2, 2, −3, 3, −2, 3, −2, 3, 0, …, 0)^T" |
| Σ = 0.6^{\|j−k\|} | EXACT | p.13, Sec 4.1 | "x_i ∼ N(0, Σ) where Σ_jk = ρ^{\|j−k\|}. In our examples, we use the value ρ = 0.6" |
| n ∈ {500, 1000} | EXACT | p.14, Table 1 rows | Table 1 (n, p) rows: n = 500, 1000 |
| p ∈ {500, 5000} | EXACT | p.14, Table 1 rows; text p.14 | "…for p = 500 and … for p = 5000" |
| SNR ∈ {0.5, 1, 2, 3} | EXACT | p.14, Table 1 header | SNR columns 0.5, 1, 2, 3 |

**Liang et al. 2022 (optional)**
- Stat. Comput. 32:84.
- Checked copy: arXiv 2110.11747v3.
- Every item is EXACT on p.15, Sec 5.1: "Σ_ij = 0.6^{\|i−j\|}", n ∈ {500, 1,000}, p ∈ {500, 5,000, 50,000}, "β* = SNR β̃ √(σ² log p / n)", SNR ∈ {0.5, 1, 2, 3}.

**What Writing should write.** Cite S1 as "the design of Griffin et al. (2021, Sec. 4.1), adapted from Yang et al. (2016, Sec. 3.4.1)".
- Do NOT write "YWJ's AR(0.6) design". YWJ uses e^{−|j−k|}.
- Do NOT attribute n∈{500,1000}, p∈{500,5000} to YWJ.

## 2. S2: Hastie–Tibshirani–Tibshirani 2020

There are three versions:
- **arXiv:1707.08692**: v1 and v2. v2 is the latest (29 Jul 2017; 53 pp; "Extended comparisons of best subset selection, forward stepwise selection, and the lasso").
- **Authors' journal-title version**: "Best Subset, Forward Stepwise, or Lasso? Analysis and Recommendations Based on Extensive Comparisons", 19 pp, built 20 May 2018, hosted at stat.cmu.edu/~ryantibs/papers/bestsubset.pdf.
- **Typeset journal**: Statist. Sci. 35(4) 579–592, DOI 10.1214/19-STS733. Project Euclid refuses automated access (an Incapsula block), so the typeset pages were **not** verified.

| Item | arXiv v2 (and v1) | Journal-title version (CMU 2018) | Verbatim (v2) |
|---|---|---|---|
| Σ_ij = ρ^{\|i−j\|} | EXACT, p.9 Sec 3.1 step ii | EXACT, p.9 Sec 3.1 | "we draw the rows of the predictor matrix X ∈ R^{n×p} i.i.d. from N_p(0, Σ), where Σ ∈ R^{p×p} has entry (i, j) equal to ρ^{\|i−j\|}" |
| ρ ∈ {0, 0.35, 0.7} | EXACT, p.10 | EXACT, p.10 | "we also considered three values for the predictor autocorrelation ρ, namely 0, 0.35, and 0.7." |
| (50, 1000, 5) | EXACT, p.10 | EXACT, p.10 | "high-5: n = 50, p = 1000, s = 5;" |
| (100, 1000, 10) | EXACT, p.10 | EXACT, p.10 | "high-10: n = 100, p = 1000, s = 10." |
| low/medium settings (not in S2) | in both, p.10 | in it, p.10 | "low: n = 100, p = 10, s = 5; medium: n = 500, p = 100, s = 5;" |
| beta-types 1, 2, 3, 5 | EXACT, p.9 | EXACT, p.9 | "beta-type 1: β0 has s components equal to 1, occurring at (roughly) equally-spaced indices between 1 and p…"; type 2 "first s components equal to 1"; type 3 "first s components taking nonzero values equally-spaced between 10 and 0.5"; type 5 "first s components equal to 1, and the rest decaying exponentially to 0, specifically, β0i = 0.5^{i−s}". Type 4 of Bertsimas et al. is deliberately omitted (p.9). |
| ν grid | EXACT, p.10 | EXACT, p.10 | "ten values for the SNR ranging from 0.05 to 6 on a log scale, namely 0.05 0.09 0.14 0.25 0.42 0.71 1.22 2.07 3.52 6.00" |
| ν definition | EXACT, p.5 and p.9 step iii | EXACT | "SNR = Var(f(x0))/Var(ε0)" (p.5); "σ² = β0ᵀΣβ0/ν" (p.9) |
| tuning | EXACT, p.10 | EXACT, p.10 | "minimizing prediction error on an external validation set of size n" |
| repetitions | 10 (p.9, step vi) | 10 (p.9) | "we repeat steps ii–v a total of 10 times". Some figure and table captions say 20 (Figs 2–3, Table 1 caption); this is a minor inconsistency. |

**Which version.** v1, v2 and the CMU journal-title version agree on every S2 item; v1 and v2 differ only in the FS/best-subset k-grid. Fig 3 (p.5) is an illustration at n=200, p=100 with 20 SNR values; it is not the S2 grid. **What Writing should write:** cite the arXiv v2 page pointers (Sec 3.1, pp.9–10). If the Stat. Sci. version is cited, say "Sec 3.1", without journal page numbers, until someone checks the typeset pages by hand.

## 3. S3: equicorrelated

**Dezeure et al. 2015**
- Statist. Sci. 30(4) 533–558.
- Checked copy: the IMS reprint on arXiv, 1408.4026v2, with the journal's text. Journal page = 532 + PDF page.

| Item | Verdict | Location | Verbatim |
|---|---|---|---|
| Σ_jk = 0.8 | EXACT | §2.5 "A Broad Comparison", PDF p.11 (journal p.543) | "Equi.corr: Σ_jk ≡ 0.8 for all j ≠ k, Σ_jj ≡ 1" |
| n, p | EXACT (differ from S3) | same | "The sample size and dimension are fixed at n = 100 and p = 500, respectively." |
| s0 | EXACT (differs from S3) | same | "one of two levels s0 ∈ {3, 15}" |
| ρ = 0.5 | NOT FOUND | — | Block-equicorrelation figures (§4, pp.18–19) vary ρ, but 0.5 is not a stated design. |

**Shin et al. 2018**
- Statist. Sinica 28(2) 1053–1078.
- Checked copy: arXiv 1507.07106v4, the latest version. The journal text was not read.
- All items are EXACT, Sec 3.1, pp.8–9:
  - "Case (1): compound symmetry design; Σ_jj' = 0.5, if j ≠ j'";
  - "Case (2): autoregressive correlated design; Σ_jj' = 0.5^{|j−j'|}";
  - "(n, p) = (400, 10000) and (n, p) = (400, 20000)";
  - "t = {1, 2, 3, 4, 5}";
  - "β_t0 = (0.50, 0.75, 1.00, 1.25, 1.50)^T … signs … randomly determined with probability one-half";
  - "σ = 1.5".

**George & McCulloch 1993**
- JASA 88(423) 881–889.
- Checked copy: the journal scan. Example 4.2 is on journal p.886 (PDF p.7).
- All items are EXACT as a description of Ex 4.2:
  - "We constructed p = 60 predictors, X1, …, X60, of length n = 120. These were obtained as X_i = X_i* + Z, where X_1*, …, X_60* iid N_120(0, 1) independently of Z ∼ N_120(0, 1). This induced pairwise correlations of about .5."
  - β = 0 (1–15), 1 (16–30), 2 (31–45), 3 (46–60).
  - "σ = 2".
- As support for an equicorrelated Σ with ρ=0.5 it is **SIMILAR**: the population correlation is exactly 1/2 by construction, but the paper states "about .5" and never writes Σ.

**Zanella & Roberts 2019 (optional)**
- JRSSB 81(3) 489–517.
- Checked copy: arXiv 1805.00541v2.
- All items are EXACT, Sec 5.2 and Table 1, pp.22–23:
  - Scenario 1: "Σ_12 = Σ_21 = 0.99, Σ_ij = 0 otherwise";
  - Scenario 2: "Σ_ij = 0.9 if i, j ∈ {1,2,3} or i, j ∈ {4,5,6}";
  - Scenario 3 is the YWJ β pattern and scaling with Σ = I and SNR ∈ {0.5, 1, 2, 3};
  - (p, n) ∈ {(100,50), (200,200), (1000,500)}.
- This is **not** a full equicorrelated design: the correlation is pairwise or block-wise only. Cite it for local strong correlation, not for S3.

**What Writing should write.** Cite S3 as "equicorrelated designs as in Dezeure et al. (2015, §2.5; ρ = 0.8) and Shin et al. (2018, Sec. 3.1; ρ = 0.5), cf. George & McCulloch (1993, Ex. 4.2)". State that **n, p and s0 for S3 are our choice**, because no cited paper uses S1's (n, p) with equicorrelation.

## 4. Caveats

- **Journal pagination.** Only George–McCulloch (journal scan) and Dezeure (IMS reprint) were checked against journal pagination. Every other check used the arXiv text. YWJ, Griffin, Hastie, Shin and Zanella–Roberts journal pages are unverified; Project Euclid and OUP block automated access.
- **Which version to cite.** When Writing cites page pointers, it should cite the arXiv version they come from, or give section numbers only.
- **PDFs.** No PDFs were committed.
