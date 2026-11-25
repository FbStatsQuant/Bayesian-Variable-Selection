# BENCH_METHODS: which competitors does the variable-selection literature run?

*Theory Department, 2026-11-25. This was ordered by the owner via HQ; it is literature work only, and nothing was run.*

**Question.** Which comparison methods recur in Bayesian and frequentist variable-selection papers, and which 5 (at most 6) should our paper run on S1–S3, where p ≤ 5000?

**Evidence.** We read 163 papers and built a method × paper matrix (`MATRIX.csv`).
- **Corpus.** 154 of the papers run a method comparison, and 161 were read in full.
  - The BENCH_DESIGN corpus contributes 89 papers and SMC_LIT 10.
  - Targeted sweeps of 2010–2026 papers add 33 Bayesian and 31 frequentist papers. Most come from JASA (29), AoS (21), JRSS-B (19), Biometrika (9), JMLR (8), BA (7) and JCGS (4).
- **What counts.** A method counts for a paper only if the paper **runs** it in a simulation or real-data comparison, judged from the full text.
- **Verification.** Haiku checkers verified 72 cells against the papers (`CHECK.md`).
  - 7 cells were wrong, and Opus corrected them all after re-reading the papers. A further 2 wrong cells in a flagged paper were corrected too.
  - The errors were all in low-count Bayesian cells: a gold standard or ablation recorded as a competitor, a missed real-data run, and three wrong cells in one paper (Staerk 2024).
  - No error was found in the 17 sampled cells of the high-count methods (lasso, SCAD, MCP, Gibbs, add-delete-swap).
- **Paywalled papers.** Two papers could not be read in full, so their cells are marked `~` (`PAYWALLED.md`).

**Count definitions.**
- **n** = the number of papers that run the method *as a competitor*. Papers that propose the method do not count.
- **B/F** = how many of those papers are Bayesian (B) or frequentist (F).
- **≥2015** = how many of those papers date from 2015 or later.

**Software** comes from a documentation audit made on 2026-11-25 (`SOFTWARE.tsv`); the CRAN status of 16 packages was spot-checked by Opus. "Scales" means usable at p = 5000 with n ≤ 1000.

## 1. Frequentist methods, ranked by n

| # | Method | n (B/F) | ≥2015 | Example papers (competitor) | Software | Scales | Rec. |
|---|---|---|---|---|---|---|---|
| 1 | **Lasso** | **59** (26/33) | 34 | Kim 2024 JMLR; Mazumder 2023 Oper Res; Xing 2023 JASA; Song–Liang 2015 JRSSB; Rossell 2021 JRSSB | glmnet (CRAN, 2026-10, maintained) | yes | **MUST** |
| 2 | **SCAD** | **22** (13/9) | 13 | Kim 2024 JMLR; Rossell 2021 JRSSB; Narisetty 2019 JASA; Moran 2019 BA | ncvreg (CRAN, 2025-11; commits 2026-08) | yes | **MUST** |
| 3 | Forward stepwise / OMP | 15 (4/11) | 7 | Hastie 2020 Stat Sci; Hazimeh 2020 Oper Res; Zhu 2022 JMLR | bestsubset `fs()` (GitHub); leaps (stable, 2024) | likely | SHOULD (expected on S2, the Hastie grid) |
| 4 | MCP | 14 (8/6) | 12 | Kim 2024 JMLR; Rossell 2021 JRSSB; Hazimeh 2020 Oper Res; Ročková 2018 JASA | ncvreg (the same call as SCAD) | yes | **SHOULD, first alternate** |
| 5 | Adaptive lasso | 13 (7/6) | 7 | Narisetty 2019 JASA; Shin 2018 Stat Sinica; Kowal 2022 JMLR | glmnet with `penalty.factor` | yes | OPTIONAL |
| 6 | Elastic net | 11 (6/5) | 7 | Kim 2024; Mazumder 2023; Hazimeh 2020 | glmnet | yes | OPTIONAL |
| 7 | Marginal testing / screening | 11 (5/6) | 5 | Candès 2018 JRSSB; Xing 2023 JASA (mostly the GWAS and FDR literature) | base R | yes | OPTIONAL |
| 8 | Multi-sample-splitting | 7 (0/7) | 4 | Dezeure 2015 Stat Sci; Dai 2023 JASA | hdi (**archived** on CRAN 2026-07) | yes | OPTIONAL (inference papers only) |
| 9 | Ridge | 7 (3/4) | 4 | Kim 2024; Mazumder 2023 | glmnet | yes | OPTIONAL (no selection) |
| 10 | SIS / ISIS | 6 (3/3) | 2 | Song–Liang 2015 JRSSB; Wang–Leng 2016 JRSSB | SIS (CRAN, 2026-03) | yes | OPTIONAL (a screening step, not a selector) |
| 11 | Relaxed lasso | 6 (1/5) | 5 | Hastie 2020; Hazimeh 2020; Mazumder 2023 | glmnet `relax=TRUE` | yes | OPTIONAL (a cheap add-on on S2) |
| 12 | Best subset by MIO | 5 (0/5) | 4 | Hastie 2020; Hazimeh 2020/2022 | bestsubset + **Gurobi licence** | no (a time limit per k) | OPTIONAL |
| 13 | Knockoffs | 2 as competitor (10 in all; proposed in 8) | 2 | Dai 2023 JASA; Xing 2023 JASA | knockpy (2025); knockoff R (2022, unmaintained) | model-X has O(p³) cost | OPTIONAL (FDR-control papers) |
| — | L0Learn, abess, stability selection, SLOPE, sqrt-lasso, debiased lasso | ≤ 3 each | | Hazimeh 2020; Zhu 2020 PNAS; Shah 2013 JRSSB | L0Learn unmaintained (2023); abess, stabs and SLOPE maintained | yes / likely | OPTIONAL |

## 2. Bayesian methods, ranked by n

| # | Method | n | ≥2015 | Example papers (competitor) | Software | PIPs | Scales | Rec. |
|---|---|---|---|---|---|---|---|---|
| 1 | **Add-delete-swap MH (MC3)** | **13** | 6 | Griffin 2021 Biometrika; Zhou 2022 JRSSB; Liang 2022 Stat Comput; Staerk 2024 BA; Ročková 2014 JASA; Clyde 2011 JCGS | BAS `method="MCMC"` (CRAN 2026-11, maintained); ADS in the PARNI repo | yes | yes | **MUST** |
| 2 | Componentwise Gibbs / SSVS | 11 | 6 | Zanella 2019 JRSSB; Titsias 2017 JASA; Biswas 2022 ICML; Schäfer 2013 Stat Comput | BoomSpikeSlab (CRAN 2025) | yes | likely | OPTIONAL (the same class as MC3) |
| 3 | Horseshoe (MCMC or approximate) | 8 | 8 | Ray 2020 NeurIPS; Kowal 2022 JMLR; Mazumder 2023 Oper Res | bayesreg (2024); horseshoe **archived**; Johndrow code MATLAB-only | **no** | likely | OPTIONAL (selects through credible intervals) |
| 4 | varbvs | 5 | 5 | Narisetty 2019 JASA; Ray 2022 JASA; Kim 2024 JMLR | varbvs (CRAN; last release 2023-05, unmaintained) | yes | yes | **SHOULD, alternate** |
| 5 | EMVS | 5 | 5 | Ray 2022 JASA; Ročková 2018 (Particle EM) JASA; Ormerod 2017 EJS | EMVS **archived** (2022) | no (conditional only) | unknown | OPTIONAL |
| 6 | Spike-and-slab lasso | 4 | 4 | Ray 2022 JASA; Kim 2024 JMLR; Mazumder 2023 | SSLASSO (CRAN 2025-11) | **no** | yes | OPTIONAL (the strongest point-estimate Bayesian option) |
| 7 | wTGS | 3 | 3 | Liang 2022 Stat Comput; Jankowiak 2023 AISTATS; Staerk 2024 BA | scaleBVS / TGS (GitHub only, last 2021) | yes (Rao–Blackwellised) | yes | **SHOULD, alternate** |
| 8 | Nonlocal priors (mombf) | 3 | 2 | Narisetty 2014 AoS; Papaspiliopoulos 2017 Biometrika | mombf **archived** 2026-09 (GitHub v4) | yes | likely | OPTIONAL |
| 9 | BMS; spikeslab (Ishwaran–Rao); RJMCMC | 3 each | | Ma 2015 JASA; Narisetty 2014 AoS | spikeslab unmaintained, no PIPs | | | OPTIONAL |
| 10 | **ASI (adaptive MCMC)** | 2 (+ proposed in 2) | 2 | Liang 2022 Stat Comput; Jankowiak 2023 AISTATS | The-PARNI-scheme repo (R/Python, 2026-03, maintained) | yes (Rao–Blackwellised) | yes (p = 50,000 in Liang 2022) | **MUST** |
| 11 | **SuSiE** | 2 (+ proposed or extended in 4) | 2 | Kim 2024 JMLR; Weissbrod 2020 Nat Genet | susieR (CRAN; GitHub 2026-11, maintained) | yes, plus credible sets | yes (p ≈ 10⁴ in Kim 2024) | **MUST** |
| 12 | BAS (sampling without replacement), HBS, Skinny Gibbs, BASAD, S5, SAM | ≤ 2 each | | Griffin 2021 (HBS); Ray 2020 (Skinny Gibbs) | BAS-exact infeasible at p=5000; Skinny Gibbs and SAM have no public code; BASAD and BayesS5 unmaintained | | | OPTIONAL |
| — | Schäfer–Chopin SMC | 1 (Griffin 2021) | | — | Python export only (2015), not maintained | yes | **no** (p ≤ 104 in the original) | OPTIONAL: cite as the closest SMC precedent, do not run |

**Reading the counts.**
- **Lasso.** It is the universal baseline, run by 26 of the 93 Bayesian papers that run a comparison.
- **Bayesian samplers.** The samplers compete mostly with each other. ADS and Gibbs are the default baselines, and in the papers closest to ours (about 48 sampler, VB and SMC papers) the most-run competitors are lasso 13, ADS 12, Gibbs 9, SCAD 8, MCP 6, varbvs 5 and EMVS 4.
- **Modern methods.** These have low counts because they are recent: ASI 2021, PARNI 2022, wTGS 2019 and SuSiE 2020. They are what a 2026 referee will ask for.

## 3. Recommended final set: 5 competitors (3 Bayesian, 2 frequentist)

| # | Method | Camp | Run with | Why it made the cut |
|---|---|---|---|---|
| 1 | **Lasso (CV)** | F | glmnet | The most-run competitor by far (59 papers, 26 of them Bayesian); any referee expects it. |
| 2 | **SCAD** | F | ncvreg | The most-run nonconvex selector (22 papers, 13 of them Bayesian). It covers the folded-concave family that has oracle selection properties. |
| 3 | **Add-delete-swap MH (MC3)** | B | BAS (`method="MCMC"`) or ADS in the PARNI repo | The standard baseline sampler of every γ-sampler paper (13). It gives PIPs under the same prior as ours, so it is a direct comparison of PIP accuracy and mixing. |
| 4 | **ASI** (Griffin et al. 2021) | B | The-PARNI-scheme repo | The state-of-the-art adaptive sampler on γ, with Rao–Blackwellised PIPs and a maintained repo, tested to p = 50,000. S1 is literally its paper's design (CITE_CHECK), so it is the natural reference on S1. |
| 5 | **SuSiE** | B | susieR | The dominant modern fast PIP method: maintained, scalable, with PIPs and credible sets. It is the approximate (variational) competitor to our exact-target SMC. |

**If a 6th slot is used: PARNI** (Liang et al. 2022). It is the successor to ASI and is in the same repo, so it costs no extra integration.

**Next in line (alternates).**
1. **MCP** (ncvreg, the same call as SCAD). Its 14 uses include 12 since 2015, so it is the recent favourite among nonconvex penalties.
2. **wTGS** (Zanella–Roberts 2019). It is the main Gibbs-type state-of-the-art sampler (3 uses), but its code is GitHub-only and unmaintained.
3. **varbvs.** It is the most-used variational BVS competitor (5 uses) and returns PIPs, but it is unmaintained since 2023.

**Deliberately not chosen.**
- Gibbs/SSVS duplicates MC3.
- The horseshoe, EMVS and SSLASSO return no PIPs, and the horseshoe and EMVS packages are archived.
- Best subset by MIO needs Gurobi and does not scale to p = 5000.
- Knockoffs, sample-splitting and the debiased lasso answer an FDR or inference question rather than estimating PIPs.
- The Schäfer–Chopin SMC has no maintained code and was built for p ≤ 104. We cite it, but do not run it.

## 4. Caveats

- **Representativeness.** The counts mix two sources. The BENCH_DESIGN corpus was built to survey designs, and the targeted sweeps follow citation chains. The counts are therefore indicative of what referees expect, not a random sample.
- **Genetics.** Papers from genetics (fine-mapping and GWAS tools, clumping and thresholding) are kept in the matrix but are not candidates for the final set.
- **Paywalled papers.** Liang–Song–Yu 2013 and Wang 2009 were not read in full; they contribute only 5 cells, marked `~`. One cell (Weissbrod 2020, SuSiE) could not be re-verified because the full text was unreachable, but it is from a full-text read.
- **Software facts.** They come from the CRAN, GitHub and PyPI pages as of 2026-11-25. Nothing was installed or run, because the compute break holds.

**Files** (in `assess/BENCH_METHODS/`):
- `MATRIX.csv`, the method × paper matrix with roles P, C, G and V, a `~` for papers not read in full, and the camp and year of each paper;
- `counts.tsv`;
- `PAPERS.md`;
- `CHECK.md` and `check/`;
- `PAYWALLED.md`;
- `SOFTWARE.tsv`;
- `SCHEMA.md`;
- `rows/`, the raw worker rows plus the Opus fixes, with `drops.tsv` and `aliases.tsv`.
