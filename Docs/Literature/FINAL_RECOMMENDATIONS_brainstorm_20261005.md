# Five candidates for SMC-based Bayesian variable selection

Brainstorm deliverable, 6 October 2026. Rules R1-R9 are in `CHECKPOINT.md`. Every number below was recomputed in this session from your engine (FD1 engine v2: X-aligned composite blocks plus the hybrid visited-set estimator) on the 500 Experiment 2 datasets, with the same seeds. Each source was read in full; the reading reports are in `reading/` and the PDFs, with SHA-256 hashes, in `sources/` (`sources/MANIFEST.json`).

## 1. Bottom line

One change to the target delivers the BVS win: replace the Bernoulli(0.2) model prior by the beta-binomial prior with h ~ Beta(1, p), and select the highest-posterior model (HPM). Everything else in the sampler is unchanged. It beats or ties the best external benchmark in all five designs and keeps the posterior exactly checkable at p = 30.

Exact-support recovery, out of 100 datasets per design:

| Procedure | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| Best external benchmark | 91 (SuSiE) | 82 (SuSiE) | 71 (PARNI) | 30 (SSL) | 64 (PARNI) |
| Current: Bernoulli(0.2), median | 88 | 79 | 72 | 29 | 65 |
| Current: Bernoulli(0.2), BFDR 5 % | 93 | 87 | 57 | 12 | 56 |
| **Candidate 1+2: Beta(1, p) prior, HPM** | **93** | **90** | **76** | **33** | **73** |
| Candidate 1, median rule (secondary) | 92 | 89 | 72 | 30 | 70 |

Benchmark source: `BVS_Benchmarks/results/bvs7_20261005_d2cc/` (primary rules, all-saved counts).

Posterior accuracy of the runs these decisions come from, measured against the exact 2^30 enumeration on all 500 datasets:

| Quantity | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| Median abs. log Z error, hybrid estimator | 3.4e-4 | 3.4e-4 | 4.7e-4 | 6.5e-4 | 4.2e-4 |
| Median PIP MAE, hybrid estimator | 8.1e-5 | 7.5e-5 | 9.5e-5 | 1.5e-4 | 9.3e-5 |
| Median-model agreement with exact | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 |

## 2. The five candidates, ranked

### Candidate 1 (target): beta-binomial model prior with h ~ Beta(1, p)

**What.** p(S) = B(|S| + 1, p − |S| + p) / B(1, p), a function of |S| only. The marginal likelihood m(S) under the control slab is unchanged and closed form.

**Why it is inference-grounded, not tuned.**
- It is the "skeptical default" of Wilson et al. (2010), Sec. 2.4.1, p. 11. It sets the global prior odds of at least one association to 1, so P(null model) = 1/2, and the marginal prior odds of any one variable to 1/p.
- It is the beta-binomial multiplicity correction of Scott & Berger (2010).
- Castillo & van der Vaart (2012), Example 2.2, p. 13, show that a beta-binomial with κ = 1, λ = n + 1 satisfies their exponential-decrease condition on model size (eq. 2.2, with D = 1/2) and the lower bound (1.2). A fixed inclusion probability satisfies (2.2) only if α_n ≲ p_n/n, the non-adaptive "oracle" (p. 13). Beta(1, 1) fails it.
- Theory boundary, stated honestly. The regression theory of Castillo, Schmidt-Hieber & van der Vaart (2015), Example 5, p. 6, covers Beta(1, p^u) only for u > 1, and needs u > 2 for its no-supersets theorem. Beta(1, p) is the u = 1 boundary. Cite it as covered in the sequence model and as the Wilson et al. default, not as a regression guarantee.
- Dissent to report. Berger, García-Donato & Pericchi (2026), Sec. 2.6, call Beta(1, k)-type priors (they name Wilson et al. 2010) "too parsimonious to be labelled objective". They recommend Half-p, Beta(1, 2) or hierarchical Beta. On our designs those objective priors do worse than Beta(1, p) (Section 4).

**Evidence.**
- Mechanism (HPM failure types, `precheck/hpm_failure_types.csv`). Superset failures, the true model plus an extra variable, fall from 12/18/11/12/19 to 2/6/4/4/8. Omissions rise modestly, from 1/1/3/2/4 to 5/4/4/12/7. Proxy swaps are essentially unchanged, at 0/0/11/41/13 versus 0/0/14/34/11, which is the data-driven ceiling identified in cycle 1.
- Not a knife-edge. HPM recovery across the Wilson et al. Table 3 grid:

| Prior | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| BB(1, p/2) | 92 | 87 | 76 | 33 | 70 |
| BB(1, p) | 93 | 90 | 76 | 33 | 73 |
| BB(1, 1.5p) | 93 | 90 | 75 | 30 | 73 |
| BB(1/2, p) | 93 | 90 | 75 | 32 | 73 |
| BB(1/8, p) | 93 | 90 | 75 | 31 | 71 |
| BB(1, 2p) | 92 | 91 | 75 | 30 | 72 |

  Sparser, theory-covered priors over-penalise and lose weak signals: Beta(1, p^1.5) gives 86/90/73/27/68 and Beta(1, p^2) gives 72/82/61/15/55.
- Split-half replication, replicates 1-50 then 51-100. Ours versus the best benchmark per design: 45 v 45, 44 v 39, 38 v 34, 12 v 13, 39 v 34; then 48 v 46, 46 v 43, 38 v 38, 21 v 19, 34 v 31. The only loss is one dataset to SSL in S4 in the first half.
- Paired exact McNemar tests on the same 100 datasets per design (wins/losses):

| Comparator | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| SuSiE | +2/−0, p = 0.50 | +9/−1, p = 0.021 | +49/−2, p < 0.001 | +33/−0, p < 0.001 | +51/−1, p < 0.001 |
| PARNI | +9/−4, p = 0.27 | +12/−1, p = 0.003 | +5/−1, p = 0.22 | +9/−5, p = 0.42 | +11/−3, p = 0.057 |
| SSL | +39/−2, p < 0.001 | +32/−5, p < 0.001 | +29/−4, p < 0.001 | +8/−5, p = 0.58 | +34/−7, p < 0.001 |

- Integrity check. Our current Bernoulli(0.2) median rule agrees with PARNI dataset by dataset, 500 of 500. Both target the same posterior, so the comparison is clean.

**How the numbers were obtained, and why that is valid.** The priors were applied by exact reweighting of the visited set V, using exact log m(S) for every scored model; Wilson et al. 2010, p. 14-15, use the same device. It was validated against direct SMC runs under a different size-only prior, Bernoulli(1/31), on 43 datasets in S2 and S4. The maximum PIP difference was 2.2e-4, and the median and HPM decisions were identical in every dataset (`precheck/compare_ywj.csv`).

**SMC implementation.**
- The prior is not a product over variables, so the composite start uses a factorised surrogate, Bernoulli(h0) with h0 = 1/(p+1).
- The bridge then tempers the prior together with the likelihood: q_φ(S) = [p_0(S) m̃(S)]^{1−φ} [p_BB(S) m(S)]^φ. Z_0 stays exactly known.
- The Gibbs log-odds gain φ times the log ratio of p_BB to p_0 for sizes k+1 versus k: a (p+1)-vector lookup.
- Cost per model is O(1). The exact enumerator only changes its log-prior line.

**Risk.** It is a change of target, so log Z values are not comparable with past campaigns. It still needs a fresh-seed confirmatory run (Section 5).

### Candidate 2 (decision): HPM over the exactly scored visited set, reported with its posterior probability

**What.**
- Select argmax over S in V of p(S) m(S). Report P(HPM | y) = p(S) m(S) / Ẑ using the hybrid evidence.
- Pre-specify the median rule under the same prior as the secondary rule.

**Why.**
- The HPM is the Bayes rule for exact-support recovery under 0-1 loss (Barbieri et al. 2021, Sec. 1).
- If P(HPM) ≥ 0.5 then HPM = MPM, which gives a free certificate. Proof: each j in the HPM has PIP_j ≥ P(HPM) ≥ 0.5, and each j outside it has PIP_j ≤ 1 − P(HPM) ≤ 0.5. The theme-A search attributes this as Prop. 2 of Dembczyński et al. (2012); that paper was not read here.
- Barbieri et al. 2021 (Sec. 3.3, p. 20) find the MPM slightly better for prediction. Berger et al. 2026 (App. A.2, p. 21) find the MPM more stable across priors. That is why the median stays as the pre-specified secondary rule.

**Evidence.**
- Under Beta(1, p), HPM recovery is 93/90/76/33/73, against 92/89/72/30/70 for the median.
- The certificate is reliable when it fires:

| | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| HPM correct when P(HPM) ≥ 0.5 | 50/50 | 46/47 | 32/35 | 4/6 | 27/31 |

- This gives a per-dataset confidence statement that no benchmark provides.

**Scaling.** V grows with N × p × stages. Keep a top-K list with exact scores. The HPM search is then the visited-set argmax and costs nothing beyond the run.

### Candidate 3 (posterior-approximation layer): exact visited-set posterior with the hybrid outside-mass correction

**What.**
- Adopt FD1's hybrid estimator as the reported evidence and PIP estimator: exact mass over V plus the SMC estimate of the mass outside V.
- Use the same exactly scored V for any model's posterior probability, for prior-sensitivity reweighting, and for Candidate 2.

**Why.**
- OPAD (Afshar, Francis & Cripps 2024, Theorem 1, eqs. 4-5) proves that, for any particle support, the KL-optimal weights are the normalised exact target values over distinct particles. Adding every scored model (OPAD+, Corollary 1) can only reduce the KL.
- Wilson et al. 2010 (p. 14-15) justify reweighting visited models to a new prior.
- OPAD's optimality is a statement about the visited support only. The mass outside V is a bias of pure renormalisation, which is why the hybrid outside-share correction is kept.

**Evidence.**
- Hybrid log Z error medians are 3.4e-4 to 6.5e-4 across designs, against 0.7e-2 to 1.0e-2 for the product estimator. That is a 15-25x improvement, consistent with FD1.
- The visited-set median decision equals the exact decision in 500 of 500 datasets.

**Action.** FD1 failed only its pre-registered plateau rule. RESULTS.md shows that the rule's test statistic was miscalibrated, because it used the SE of one share for a difference of two shares. Pre-register a corrected plateau criterion and adopt the hybrid estimator.

### Candidate 4 (reporting): BLiP resolution-adaptive discoveries from the joint particles

**What.** Spector & Janson (2025), eqs. 2.4-2.7.
- Candidate groups: singletons plus all subsets of each X-only correlation cluster (complete linkage on 1 − |cor|, cut at 0.5).
- p_G = P(some selected variable lies in G | y), computed from the posterior over V.
- One small binary linear program at q = 0.05 maximising resolution-weighted power under Bayesian FDR, with disjoint regions.

**Why.** Proxy swaps of the weak signals are at the data ceiling in S3-S5. BLiP converts many of these failures into correct statements at block resolution, such as "a signal lies in {8, 9}". Griffin (2025) and Barbieri et al. (2021, Lemma 2.3) make the same point: with correlated predictors, joint inclusion is the right decision object.

**Evidence, under Beta(1, p).**

| | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| Resolution-adjusted success: every true signal covered, no false region | 86 | 87 | 83 | 53 | 76 |
| Total false regions | 3 | 5 | 7 | 12 | 8 |

This is a different metric from exact recovery, so it complements Candidate 2 rather than replacing it. The natural comparator is SuSiE credible sets, which the benchmark thread can score on the same metric.

**Cost.** One small binary LP with at most p + Σ_clusters 2^{|cluster|} variables. The paper applies BLiP to much larger problems (App. D).

### Candidate 5 (large-p certification): single-run Monte Carlo standard errors from the Eve genealogy

**What.**
- Carry one integer vector, the Eve index, through resampling.
- Compute the Lee-Whiteley / Du-Guyader estimator (Du & Guyader 2021, eq. 9, p. 13) for every PIP and model probability, and for log Z.

**Why.** At large p there is no enumerator. This is the scalable substitute for the exact check: a per-dataset Monte Carlo SE that can flag decisions lying within 2 SE of a threshold.

**Evidence** (`precheck/eve_*.csv`). N = 2000; 10 seeds per dataset; S2 replicates 1-10 and S4 replicates 1-7.
- Multinomial resampling: the ratio of estimated to empirical variance is 1.01 (S2) and 0.79 (S4) for log Z, and 1.09 and 0.97 for PIPs.
- Systematic resampling, as in your engine: PIP SEs remain calibrated (ratio 1.13), but the log Z estimator becomes negative and is unusable. The paper's proofs assume multinomial selection (p. 13, p. 29).

**Recommendation.** Use the PIP and model-probability SEs as is. For log Z SEs, either switch the final stages to multinomial resampling or run a few independent replicates.

## 3. How the five fit together

The proposed execution has five parts:
- **Target:** Candidate 1.
- **Sampler:** your engine with X-aligned blocks, unchanged.
- **Estimation layer:** exact visited set plus hybrid correction (Candidate 3).
- **Decision:** HPM with its certificate, median pre-specified as secondary (Candidate 2).
- **Companion outputs:** BLiP regions (Candidate 4) and single-run SEs (Candidate 5).

Candidates 1-2 carry the BVS win. Candidates 3 and 5 carry the posterior-approximation claims at small and large p. Candidate 4 makes the S3-S5 ceiling cases honest.

## 4. Tested and not recommended

Each idea below was implemented and scored on the same 500 datasets (`precheck/rules*_results.csv`), with the prior as stated.

| Idea (source) | Result |
|---|---|
| Exact expected-F1 maximiser, GFM (Waegeman et al. 2014), Bern(0.2) | 81/78/63/21/43 on 181 datasets as rates (below median) |
| Non-marginal block decisions (Chandra & Bhattacharya 2019) | at or below median; reduces to a size-tilted block-MAP |
| Adaptive PIP threshold with posterior benchmarking (Li, Tokdar & Xu 2025) | 75/84/68/34/60 under Bern(0.2): worse in S1, S3, S5 |
| Size-first then best model; optimal predictive model (Barbieri et al. eq. 1.2) | strongly over-select (S1 exact recovery rates 0.12 and 0.34 on 65 datasets) |
| BFDR 5 % / 10 % under any prior | best in S1-S2 under Bern(0.2), collapses in S3-S5 (57/12/56) |
| EB inclusion probability (Castillo & Roquain 2020 analogue) | ĥ ≈ 0.20-0.22 on every design, so no change |
| Independent slab Λ = I/τ (cycle-1 lead) | neutral (HPM 77/81/71/18/38 as rates on 181 datasets) |
| Objective-school priors Beta(1,2), Half-p, BB(1,1) (Berger et al. 2026) | HPM 87/82/74/33/64 at best: lose S1 and S5 |
| Matryoshka doll θ = 1 (Womack et al. 2025); Bern(1/(p+1)) (Yang, Wainwright & Jordan 2016) | HPM 90/90/75/30/69 and 89/90/74/30/69: close to Candidate 1 but lose S1 |
| Exact block-Gibbs / Hamming-ball kernel (Titsias & Yau 2017), N = 1000 | vs cost-matched 6 single-site sweeps: median log Z error 0.021 v 0.024 (S4, 35 runs), 0.016 v 0.024 (S5, 19 runs); PIP error equal; no decision change. Optional at large p only |

Read but not tested, as supporting references only:
- **Kowal 2022:** the acceptable family, likely to drop weak signals.
- **Persistent sampling (Karamanis & Seljak 2025):** a continuous-space method, and it loses unbiasedness of Z.
- **Papaspiliopoulos & Rossell 2017:** a φ-conditional composite start, a possible efficiency upgrade.
- **Exact SuSiE target (Wang et al. 2020; Denault et al. 2025):** closed form but costly, and it explains SuSiE rather than beating it.

## 5. Caveats and the confirmatory step

1. **Selection on the same data.** Candidate 1 was identified among about 30 prior-and-rule combinations on the 500 datasets used to score it. Four things mitigate this but do not replace a fresh test:
   - it is a published default;
   - neighbouring priors behave the same way;
   - split halves replicate;
   - the mechanism is identified.

   Pre-register "Beta(1, p) prior, HPM primary, median secondary, BLiP q = 0.05 companion" and run fresh seeds, both through your SMC with the prior inside the engine and through the benchmark thread on the same datasets.
2. **Validation of the reweighting.** Reweighting was validated against direct SMC for a Bernoulli prior. The beta-binomial target still needs its engine implementation (Candidate 1 recipe) and an exact-enumeration check at p = 30. The enumerator only needs a new log-prior line.
3. **Theory.** The regression guarantees cover Beta(1, p^u) only for u > 1. Our default sits at the boundary, which must be cited as such. The objective-prior school disagrees on parsimony grounds (Berger et al. 2026).
4. **S4.** Every method, ours included, stays near 30/100 on exact recovery in S4. Candidate 4 is the honest output there, at 53/100 resolution-adjusted.

## 6. Sources (all in `sources/`, reading reports in `reading/`)

| # | Source | Read | Role |
|---|---|---|---|
| 1 | Wilson, Iversen, Clyde, Schmidler, Schildkraut (2010) AoAS 4(3) | in full by Claude | Beta(1, p) default; reweighting |
| 2 | Scott & Berger (2010) AoS 38(5) | on disk (Papers/04); cited via Wilson and Barbieri | multiplicity via beta-binomial |
| 3 | Castillo & van der Vaart (2012) AoS 40(4) | in full (agent report) | size-prior theory, Example 2.2 |
| 4 | Castillo, Schmidt-Hieber & van der Vaart (2015) AoS 43(5) | in full (agent report) | regression theory, boundary u = 1 |
| 5 | Berger, García-Donato & Pericchi (2026) arXiv 2603.19728 | in full by Claude | dissent; objective priors |
| 6 | Barbieri, Berger, George & Ročková (2021) BA 16(4) | in full by Claude | MPM vs HPM, joint inclusion |
| 7 | Dembczyński et al. (2012) Mach. Learn. 88 | not read (publisher returned HTML); certificate proved directly instead | attribution only |
| 8 | Afshar, Francis & Cripps (2024) arXiv 2412.00545 (OPAD) | in full by Claude | exact visited-set weights |
| 9 | Spector & Janson (2025) JASA 120 (BLiP) | main text and App. A-D by Claude | Candidate 4 |
| 10 | Griffin (2025) BA 20(4) | in full by Claude | block-level reporting |
| 11 | Du & Guyader (2021) AAP 31; Lee & Whiteley (2018) | Du & Guyader in full (agent report) | Candidate 5 |
| 12 | Titsias & Yau (2017) JASA 112 | main text by Claude | kernel (tested) |
| 13 | Waegeman et al. (2014); Chandra & Bhattacharya (2019); Li, Tokdar & Xu (2025); Kowal (2022); Womack et al. (2025); Yang, Wainwright & Jordan (2016); Castillo & Roquain (2020); Karamanis & Seljak (2025); Papaspiliopoulos & Rossell (2017); Wang et al. (2020); Denault et al. (2025) | in full (agent reports) | tested or supporting |

Missing PDF to supply if you want it on disk: Dembczyński, Waegeman, Cheng & Hüllermeier (2012), Machine Learning 88, 5-45, doi:10.1007/s10994-012-5285-8. The publisher served an HTML page instead of the PDF.
