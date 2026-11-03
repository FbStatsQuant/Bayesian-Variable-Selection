# EVIDENCE_L: theory evidence from the low-p study (PROD-L)

Companion to `EVIDENCE_H.md`, laid out like `THEORY_EXTRACTION_STRATEGY.md`: one section per row of its mapping. Each section gives what was measured, a verdict on the conjectured statement (**support**, **contradict** or **silent**), and the cases that break it.

**Data.** PROD-L, n = 200, p ∈ {20, 30}, S1–S6, c ∈ {1, 0.5}, 100 replicates. That is 2,400 cases, 2,400 primary SMC fits and 12,000 repeat fits, plus the exact posterior by full enumeration.
- **How it was computed:** every quantity comes after the fit, from `code/scoring` (`theory_measures.R`, with the TD audit on the C++ enumerator).
- **Truth:** used only in scoring.
- **Completeness:** all 2,400 cases are complete. Every truth was retained by preprocessing (`theory_status = ok`), the record's blocks equal the recomputed blocks in 2,400/2,400, both TD audits (d = 1, 2) completed in every case, and the π₀ table check difference is 0.
- **Files:** `case_theory.csv` (one row per case) and `evidence/` (the summary tables cited below).

## T37 (Thm 3): truth dominance TD(d), literal vs "toward S₀"

Audited at d = 1 and d = 2 with the full null pool and m = 0 (`evidence/td.csv`, `evidence/td_vs_outcome.csv`).

**Literal wording.** It **fails in every case**, 2,400/2,400 at both d:
- d = 1: 992,065 violating centres (991,882 in clauses a/b, plus 183 at S₀);
- d = 2: 13.78 M violating centres.

At d = 1, 97.8% of the violations in clauses a/b are explained by a null-out/truth-in swap that beats "add the missing truth" (98.6% at d = 2). This is the generic failure predicted in D18 and THEORY_MEASURES. Clause c (at S₀) fails in 183 cases: those are the cases where some single move from S₀ raises F.

**"Toward S₀" wording.** It holds strictly in 63.0% of cases at d = 1 and 53.6% at d = 2. The rate falls with weaker signal and larger p:

| p, c | d = 1 | d = 2 |
|---|---|---|
| 20, 1 | 92.3% | 83.5% |
| 20, 0.5 | 74.8% | 63.5% |
| 30, 1 | 57.7% | 46.2% |
| 30, 0.5 | 27.0% | 21.2% |

S4 and S5 are the weakest scenarios: at p = 30, c = 0.5, d = 1, the toward wording holds in 5% and 2% of their cases.

**Relation to outcome.**
- Every case where the toward TD holds strictly is a hit (the SMC HPM is the truth): 1,511 cases at d = 1, 1,286 at d = 2.
- The toward TD fails in all 184 posterior misses. This is an observed fact, not a logical necessity: the audit only covers centres in R_d and their single-move neighbourhoods. Clause c (at S₀) fails in 183 of these cases.
- It also fails in many hits: 705 at d = 1 and 930 at d = 2. In those, at some near-truth centre a move away from S₀ beats every move toward it, yet the run still returns S₀.

**First-score attribution.** Every truth model was first *scored* in the pilot phase, mostly by the initial draw or a Gibbs flip (next section). No first score is credited to local search. This is first-score attribution only: it neither tests the hypothesised local-search repair mechanism nor rules out a later role for local search.

**Verdict:**
- **Contradict** the applicability of the literal T37 condition here: its premise fails generically. A conditional theorem is not refuted merely because its premise fails.
- The toward wording is **consistent with** the proposed sufficiency implication in these runs: no counterexample among 1,511 cases (d = 1).
- It is not necessary for observed recovery: 705 hits violate it at d = 1.

A toward form of T37 is a candidate refinement for the theory phase. It needs its own assumptions and proof.

## T22 + T27 (Thm 2): start mass in the favourable and masked regimes

Source: `evidence/pi0.csv`.

**Start mass of the truth, π₀(S₀).** It spans 38 orders of magnitude. The median over cases is 5.5e-3, the p10 is 6.8e-17, and 53% of cases have π₀(S₀) < 0.01.

**By scenario.** S1 is favourable: the median π₀(S₀) is 0.28–0.76. S3–S6 at p = 20 are strongly masked, with medians from 1e-28 to 1e-6.

**Neighbourhood masses grow with d.** Median π₀(R₀) is 0.075, π₀(R₁) 0.56 and π₀(R₂) 0.87.

**Recovery by start-mass class** (`evidence/recovery_by_pi0.csv`). SMC HPM = truth by π₀(S₀) class:

| π₀(S₀) | all cases | SMC HPM = truth | p = 30, c = 0.5: cases | SMC HPM = truth |
|---|---|---|---|---|
| < 0.01 | 1,273 | 91.1% | 218 | 76.6% |
| 0.01–0.1 | 383 | 89.3% | 180 | 83.9% |
| 0.1–0.5 | 410 | 95.4% | 151 | 92.1% |
| ≥ 0.5 | 334 | 96.7% | 51 | 98.0% |

Pooled over all cells the gradient is mild. Within a cell it can be large: at p = 30, c = 0.5, recovery goes from 76.6% in the lowest class to 98.0% in the highest. In every class and cell the exact HPM has the same rate, so the SMC loses nothing relative to the exact posterior, even with a tiny start mass. Low start mass goes with harder *posteriors*. The data do not show that start mass is irrelevant to difficulty or cost.

**Verdict.**
- **Support** the masked-regime claim, that a tiny start mass on the truth does not stop the SMC from delivering the exact posterior's HPM at low p.
- **Silent** on the rate statements. At p ≤ 30 the truth was scored during the pilot in every primary fit, so these data cannot show whether start mass becomes binding.

## T38 (Thm 5): HPM consistency and the polynomial-cost corollary

**Consistency.** The SMC HPM equals the exact HPM in 2,400/2,400 primary fits and in 12,000/12,000 repeat fits. HPM = truth is 92.3% overall, and it rises with signal at both p (`HEADLINE_L.md` Q2/Q4):

| p | c = 1 | c = 0.5 |
|---|---|---|
| 20 | 96.0% | 93.7% |
| 30 | 95.2% | 84.5% |

**Cost** (`evidence/cost.csv`).
- **Runtime:** median 2.7 s per fit, and essentially flat from p = 20 to p = 30 (90th percentile 3.6–5.0 s).
- **Distinct models scored:** the median goes from about 33k at p = 20 to 71k–85k at p = 30. That is about 3% of the 2^20 model space and about 0.007% of 2^30.
- **Escalation:** none; every fit stayed at tier 0.

**Verdict.**
- **Support** delivery: the SMC returns the posterior's own HPM every time.
- **Silent** on asymptotic consistency: with n fixed at 200, HPM = truth is limited by the posterior itself.
- **Silent** on the polynomial-cost corollary: two values of p cannot establish a rate. The data are consistent with sub-exponential growth: the scored count rises about 2.2× while the model space grows 1,024×.

## T21 (Thm 4): P(wrong) ≤ P(no output) + 2·E[mass off the truth] + P(truth never scored)

Source: `evidence/t21.csv`; miss class in `evidence/miss_class.csv`.

**The terms:**
- P(no output) = 0: no failed or `resource_limit` fit.
- P(truth never scored) = 0: the truth was scored in 2,400/2,400 fits.
- E[mass off the truth], from the exact posterior: 0.33–0.49 per p × c.

**The bound holds in every cell**, with large slack (overall P(wrong) 0.077 against a bound of 0.79).

**Miss class.** There are 2,216 hits, 0 search misses and 184 posterior misses. Every miss is the posterior's own: F(S₀) ≤ F(HPM). There are no ties: the gap F(S₀) − F(HPM) is −0.0017 at its closest, with median −1.10.

**Scored-set coverage** (`evidence/coverage.csv`): the share of the exact posterior mass carried by the models the SMC scored. Median 0.99995, minimum 0.9980; every case is at least 0.99, and 99.8% of cases are at least 0.999.

**Where the truth was first scored** (`evidence/truth_first.csv`): always in the pilot phase.

| First-scoring mechanism | Cases (of 2,400) |
|---|---|
| Initial draw (`init_draw`) | 1,304 |
| Gibbs flip (`gibbs_flip`) | 1,038 |
| `nswap` | 31 |
| `uswap` | 26 |
| `indep` | 1 |

First *scoring* a model does not mean a particle visited or retained it.

**Verdict:**
- **Support**, but the bound is loose here: the mass-off-truth term dominates.
- The decomposition is informative in another way. In these fits, every observed HPM truth-recovery error is a posterior error; the search contributes none. This concerns HPM recovery only, not Ẑ or PIP estimation error.

## Resource-stop vs complete-run gap

All 14,400 SMC units completed natively:
- 0 `resource_limit`, so the P5 scan was closed under D63 with nothing eligible;
- 0 escalations;
- 2 primary fits (`p0020_S4_r095_c100`, `p0030_S3_r074_c100`) and 3 repeat fits flag a failed final check with low ESS. Both flagged primaries still equal the exact HPM and the truth, with |e| ≤ 0.027.

**Verdict:** **silent**. There is no resource-stopped fit to compare at low p, so the gap can only be studied at p ≫ n (EVIDENCE_H).

## T03 / T07 (Thm 1, Prop 1): concentration; same-size swaps

The 184 posterior misses break down by the composition of the HPM against S₀ (`evidence/miss_class.csv`):
- 94 supersets (S₀ plus nulls);
- 78 same-size swaps;
- 10 subsets;
- 2 mixed.

**By cell:**
- At p = 20, c = 1, all 24 are supersets.
- At p = 30, c = 0.5, 59 of 93 are same-size swaps. Swaps concentrate in S4, the hardest scenario: S4 has 39 of the 93 misses in that cell, 34 of them swaps; S6 adds 14 swaps.

**Truth mass.** The exact posterior mass on the truth has median 0.13 in posterior misses and 0.68 in hits.

**Verdict:**
- **Support** both mechanisms: superset errors dominate at strong signal, same-size swaps at weak signal.
- **Silent** on the rates.

## T26(i)–(ii), T12 (Thm 6, Prop 2): evidence and PIP consistency; Ẑ unbiasedness

**Ẑ unbiasedness** (`evidence/zhat_unbiased.csv`). Over all 14,400 fits, the mean relative error Ẑ/Z − 1 is −0.00011, with SE 0.00010, so it is within 1.1 SE of 0. The pooled bias is therefore small and compatible with zero; cancellation across cases cannot be excluded. The mean log error is −0.00018, with SE 0.00010. Its sign is the one Jensen's inequality gives for an unbiased Ẑ, and its size is close to the second-order approximation −Var/2 ≈ −0.00007.

**Seed noise.** The sd of log Ẑ across seeds (mean 0.011) is similar to the RMSE against the exact value (0.012). That is consistent with seed variability dominating the observed error. It does not exclude a small case-specific bias.

**Lower bound.** The 0.05·Ẑ lower bound never fails, in 14,400/14,400 fits.

**PIP consistency.**
- **RB PIPs:** the per-fit max error has mean 0.0005, with maximum 0.013 among primaries.
- **Plain PIPs:** mean 0.0020, with maximum 0.012.
- **MPM agreement with the exact MPM:** 99.9% (RB) and 99.8% (plain).
- **Comparison:** the RB estimator is about 4× more accurate than the plain one, and has lower seed spread (`tables/stability.csv`).

**Verdict:**
- **Support** T12 (Ẑ unbiasedness): the pooled mean relative error is compatible with zero.
- **Support** T26(i)–(ii) as finite-setting accuracy evidence at n = 200, p ≤ 30.
- **Silent** on consistency and rates: one n, two values of p, one computational configuration.

## Cases that break a conjectured statement
- **T37, literal wording:** its premise fails in all 2,400 cases (applicability, not refutation).
- **T37, toward wording as a necessary condition:** it fails in 705 hits at d = 1 (930 at d = 2). As a sufficient condition it has no counterexample in these runs.

No other statement listed above has a counterexample in these data.

<!-- BENCH:BEGIN -->
## Benchmarks at low p (pass C, HQ D92): exact recovery of the truth

**Data.** PROD_L_BENCH rev 2, run `20261102T2309Z_lowp_benchres`: 19,200 records (2,400 cases × 8 methods), all accepted by `accept_bench.R`, pulled and verified. They were scored with the frozen campaign scorer (`code/scoring`, registry derived from `bench_lowp` r2, including the LA-4 low-p overlay). Truth was used in scoring only. For the 11 benchmark rules below (26,400 rule × case results): not run 0, failed or not run 0.

**Rules.** These are the same headline rules as at p ≫ n: F1–F3 (lasso, elastic net, adaptive lasso) `ebic1_K37`, with CV `cv_min` reported as a disclosed sensitivity (D35/D42); F4 MCP and F5 ABESS `ebic1_K37`, their pre-registered primary (D42.4; at p ≤ 30 it equals the cap rows, LA-4 / D17); A1 SuSiE `pip05`, A2 SSL `ssl_final`, A3 horseshoe `ci95`. SMC-BVS MPM (plain) is the plain-PIP > 1/2 set of the primary fit, from `case_smc_accuracy.csv`; its RB counterpart is `pip05`, cross-checked equal to the accuracy-table RB MPM in every case.

**p = 20, c = 1** (count out of 100 per scenario, 600 pooled)

| method | rule | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 |
|---|---|---|---|---|---|---|---|---|
| SMC-BVS HPM | `hpm` | 96 | 98 | 97 | 95 | 95 | 95 | **576** |
| SMC-BVS MPM (RB) | `pip05` | 96 | 98 | 97 | 95 | 94 | 96 | **576** |
| SMC-BVS MPM (plain) | `mpm_plain` | 96 | 98 | 97 | 95 | 94 | 96 | **576** |
| Exact-posterior HPM | `hpm` | 96 | 98 | 97 | 95 | 95 | 95 | **576** |
| Exact-posterior MPM | `mpm` | 96 | 98 | 97 | 95 | 94 | 96 | **576** |
| Lasso | `ebic1_K37` | 89 | 93 | 94 | 75 | 93 | 97 | **541** |
| Elastic net | `ebic1_K37` | 89 | 93 | 92 | 39 | 91 | 98 | **502** |
| Adaptive lasso | `ebic1_K37` | 88 | 91 | 88 | 91 | 84 | 92 | **534** |
| MCP | `ebic1_K37` | 88 | 91 | 88 | 91 | 84 | 92 | **534** |
| ABESS | `ebic1_K37` | 88 | 91 | 88 | 91 | 84 | 92 | **534** |
| SuSiE | `pip05` | 91 | 90 | 99 | 99 | 99 | 97 | **575** |
| SSL | `ssl_final` | 99 | 100 | 99 | 97 | 97 | 98 | **590** |
| Horseshoe | `ci95` | 94 | 99 | 95 | 96 | 95 | 94 | **573** |
| Lasso (CV sensitivity) | `cv_min` | 0 | 1 | 0 | 0 | 3 | 1 | **5** |
| Elastic net (CV sensitivity) | `cv_min` | 0 | 1 | 0 | 0 | 1 | 0 | **2** |
| Adaptive lasso (CV sensitivity) | `cv_min` | 12 | 28 | 22 | 41 | 30 | 23 | **156** |

**p = 20, c = 0.5** (count out of 100 per scenario, 600 pooled)

| method | rule | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 |
|---|---|---|---|---|---|---|---|---|
| SMC-BVS HPM | `hpm` | 96 | 97 | 96 | 87 | 92 | 94 | **562** |
| SMC-BVS MPM (RB) | `pip05` | 96 | 98 | 94 | 78 | 92 | 94 | **552** |
| SMC-BVS MPM (plain) | `mpm_plain` | 96 | 98 | 94 | 78 | 91 | 94 | **551** |
| Exact-posterior HPM | `hpm` | 96 | 97 | 96 | 87 | 92 | 94 | **562** |
| Exact-posterior MPM | `mpm` | 96 | 98 | 94 | 79 | 92 | 94 | **553** |
| Lasso | `ebic1_K37` | 89 | 92 | 80 | 52 | 79 | 90 | **482** |
| Elastic net | `ebic1_K37` | 89 | 92 | 71 | 37 | 75 | 85 | **449** |
| Adaptive lasso | `ebic1_K37` | 88 | 91 | 86 | 80 | 84 | 92 | **521** |
| MCP | `ebic1_K37` | 88 | 91 | 86 | 77 | 84 | 91 | **517** |
| ABESS | `ebic1_K37` | 88 | 91 | 87 | 75 | 84 | 91 | **516** |
| SuSiE | `pip05` | 90 | 91 | 98 | 80 | 95 | 96 | **550** |
| SSL | `ssl_final` | 99 | 100 | 98 | 85 | 95 | 97 | **574** |
| Horseshoe | `ci95` | 95 | 99 | 89 | 57 | 89 | 91 | **520** |
| Lasso (CV sensitivity) | `cv_min` | 0 | 1 | 0 | 0 | 3 | 1 | **5** |
| Elastic net (CV sensitivity) | `cv_min` | 0 | 1 | 0 | 0 | 3 | 0 | **4** |
| Adaptive lasso (CV sensitivity) | `cv_min` | 11 | 25 | 17 | 27 | 22 | 18 | **120** |

**p = 30, c = 1** (count out of 100 per scenario, 600 pooled)

| method | rule | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 |
|---|---|---|---|---|---|---|---|---|
| SMC-BVS HPM | `hpm` | 95 | 95 | 97 | 89 | 97 | 98 | **571** |
| SMC-BVS MPM (RB) | `pip05` | 94 | 95 | 97 | 90 | 97 | 98 | **571** |
| SMC-BVS MPM (plain) | `mpm_plain` | 94 | 95 | 97 | 90 | 97 | 98 | **571** |
| Exact-posterior HPM | `hpm` | 95 | 95 | 97 | 89 | 97 | 98 | **571** |
| Exact-posterior MPM | `mpm` | 94 | 95 | 97 | 90 | 97 | 98 | **571** |
| Lasso | `ebic1_K37` | 90 | 92 | 84 | 45 | 88 | 79 | **478** |
| Elastic net | `ebic1_K37` | 90 | 95 | 68 | 13 | 78 | 72 | **416** |
| Adaptive lasso | `ebic1_K37` | 89 | 86 | 93 | 80 | 89 | 94 | **531** |
| MCP | `ebic1_K37` | 89 | 88 | 93 | 78 | 89 | 95 | **532** |
| ABESS | `ebic1_K37` | 89 | 87 | 92 | 77 | 89 | 95 | **529** |
| SuSiE | `pip05` | 85 | 90 | 100 | 98 | 99 | 98 | **570** |
| SSL | `ssl_final` | 100 | 98 | 98 | 93 | 99 | 98 | **586** |
| Horseshoe | `ci95` | 94 | 95 | 97 | 86 | 98 | 98 | **568** |
| Lasso (CV sensitivity) | `cv_min` | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| Elastic net (CV sensitivity) | `cv_min` | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| Adaptive lasso (CV sensitivity) | `cv_min` | 9 | 16 | 25 | 28 | 24 | 25 | **127** |

**p = 30, c = 0.5** (count out of 100 per scenario, 600 pooled)

| method | rule | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 |
|---|---|---|---|---|---|---|---|---|
| SMC-BVS HPM | `hpm` | 94 | 91 | 94 | 61 | 86 | 81 | **507** |
| SMC-BVS MPM (RB) | `pip05` | 93 | 91 | 90 | 53 | 85 | 79 | **491** |
| SMC-BVS MPM (plain) | `mpm_plain` | 93 | 91 | 90 | 53 | 84 | 79 | **490** |
| Exact-posterior HPM | `hpm` | 94 | 91 | 94 | 61 | 86 | 81 | **507** |
| Exact-posterior MPM | `mpm` | 93 | 91 | 90 | 53 | 84 | 79 | **490** |
| Lasso | `ebic1_K37` | 89 | 83 | 52 | 13 | 56 | 58 | **351** |
| Elastic net | `ebic1_K37` | 89 | 80 | 43 | 9 | 49 | 55 | **325** |
| Adaptive lasso | `ebic1_K37` | 89 | 85 | 90 | 55 | 81 | 80 | **480** |
| MCP | `ebic1_K37` | 89 | 86 | 90 | 49 | 82 | 82 | **478** |
| ABESS | `ebic1_K37` | 89 | 85 | 86 | 50 | 83 | 79 | **472** |
| SuSiE | `pip05` | 83 | 89 | 94 | 55 | 88 | 79 | **488** |
| SSL | `ssl_final` | 96 | 93 | 89 | 58 | 86 | 79 | **501** |
| Horseshoe | `ci95` | 93 | 88 | 62 | 15 | 63 | 46 | **367** |
| Lasso (CV sensitivity) | `cv_min` | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| Elastic net (CV sensitivity) | `cv_min` | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| Adaptive lasso (CV sensitivity) | `cv_min` | 7 | 11 | 14 | 16 | 12 | 17 | **77** |

**Flags (reported, not interpreted; HQ decides on any audit).**
- SSL recovers the truth more often than the exact-posterior HPM in: p = 20, c = 1, p = 20, c = 0.5, p = 30, c = 1 (pooled 2251 vs 2216 of 2,400). The exact posterior is that of the SMC-BVS model, not an oracle, so another prior can recover more often.
- Near-zero recovery (< 5% of 2,400): Lasso (CV sensitivity) (12), Elastic net (CV sensitivity) (8). This is the CV behaviour found organic at p ≫ n (BENCH-AUDIT, D42.1); the headline rule is `ebic1_K37`.

**ABESS exact size-k check (D54.3).** the ebic1_K37 (headline) ABESS support is the exact best subset of its size (by RSS, ties allowed) in 2,375/2,400 fits; in the other 25 (max relative RSS gap 0.027) the exact best subset would have recovered the truth in 9 and ABESS recovered it while the best subset would not in 2, so replacing each suboptimal support by the exact best subset of the same size (holding the selected sizes fixed; EBIC selection over an exact path was not recomputed) would change ABESS's /2,400 count by +7. Over the whole stored path (sizes 1–p), 15,712 of 60,000 size-k supports are not RSS-optimal, 98.8% of them at sizes above the true size. Details: `abess_check/ABESS_CHECK.md`.

Per-scenario counts with passing-only columns: `tables/Q4_recovery.csv`. Case-level rows: `score_final_bench/case_selection.csv`.
<!-- BENCH:END -->
