# SMC-BVS: where we are and what is left (briefing, 2026-10-28)

For Felipe, from HQ. Every number here traces to a file listed in §7. Paths start at the project root (`Local_to_global_Bayesian/`) unless they start with `NOTS_BVS/` (= `<PC_NB_ARCHIVE>\`). Reviews of this briefing are in `review/` (§7).

## 0. Bottom line

- **The main simulation study is done.**
  - SMC-BVS v3 ran on all 2,400 planned datasets: 6 scenarios × p ∈ {500, 1000} × 100 replicates × c ∈ {1, 0.5}.
  - Every benchmark ran on the same datasets.
  - 2,394 SMC fits finished; 6 were stopped by the time guard, all in S5. Those 6 count as misses.
- **Results.**
  - **Strong signal (c = 1).** SMC-BVS recovers the exact true model in 559 and 560 of 600 datasets. That is 2–4 percentage points behind SuSiE, SSL and the horseshoe, and 5–6 behind SSL-RS.
  - **Weak signal (c = 0.5).** SMC-BVS is clearly best: 370 and 340 of 600, against 303 and 255 for the next best, SSL.
  - **Cost.** It is by far the slowest method: a median of 8–9 minutes per fit at p = 500 and 22–23 minutes at p = 1000.
- **Theory: 12 of 36 conjectured theorems fully proved, 8 partly, 16 not at all.** None is formally adopted yet.
  - The proofs describe the method that actually ran, with two caveats (§2, §5).
  - At n = 200 the *statistical* theorems are long-run (asymptotic) statements, not numerical guarantees.
  - The *exact* results hold at n = 200, but for the run as designed to finish, not for "the fits that happened to finish". These are what the outputs mean, the decision rules, and why the HPM can be right before the sampler has mixed.
- **Biggest open gap.** There is no proof, without strong assumptions, that the true model gets scored at some point during a run.
- **Not done yet:**
  - the intermediate signal scales (c = 0.75, 0.35, 0.25);
  - Regime L, the p = 30 check of evidence and PIP accuracy against exact enumeration;
  - any real-data example;
  - formal close-out of the benchmark verification gates (§3.3).
- **Decisions you need to make** are in §6.1.

---

## 1. Simulated data

Source: master Part II (`01_Methodology_and_Theory/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md`, lines 609–788). Data generation: `02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/RUNS.md` line 5 (job 2277158; all G2 checks passed).

**One dataset** (n = 200 every time):
1. Draw 200 rows from N_p(0, Σ_s), where Σ_s is the scenario's correlation matrix.
2. Centre each column of X and scale it to SD 1.
3. Set y = c·Xβ + ε, with ε ~ N(0, I). So σ = 1.

**The truth.** The same 14 active variables (⌊√200⌋) and coefficients in every dataset.
- **Coefficients:** the pattern (1.4, −1.0, 1.8, −1.2, 0.8, −1.6) cycled, i.e. 1.4, −1.0, 1.8, −1.2, 0.8, −1.6, 1.4, −1.0, 1.8, −1.2, 0.8, −1.6, 1.4, −1.0.
- **Placement:** each signal sits alone in its own block of 5 variables, and the active blocks are evenly spaced.
- **Indices:** the active indices are 3, 37, …, 457 at p = 500 and 3, 67, …, 847 at p = 1000.
- **p = 500 versus p = 1000:** the signal positions differ, but every signal keeps the same strength and the same correlation partner. Statistically, only the number of null variables changes.
- **Seeds:**
  - data seed = base + 10,000·s + r (base 1,410,000 for p = 500, 1,510,000 for p = 1000);
  - CV-fold bases are 3,410,000 and 3,510,000;
  - method seed = data seed + 4,000,000, the same at every c.

**The six scenarios:**

| | Correlation of X | What it tests |
|---|---|---|
| S1 | Independent | Baseline |
| S2 | AR(1), 0.5^\|j−k\| | Neighbouring variables partly substitute for each other |
| S3 | 0.7 within blocks of 5 | Each signal has 4 correlated null look-alikes |
| S4 | 0.85 within blocks | The same, harder to tell apart |
| S5 | 0.7 within blocks, 0.3 between all blocks | Everything is correlated; the hardest case for the start and the search |
| S6 | Block ρ cycles 0.4, 0.5, …, 0.9; 0 between blocks | Correlation strength varies by block |

**Signal scale c.** X and ε are drawn once per dataset and reused at every c (y_c = c·Xβ + ε), so the c = 1 and c = 0.5 results are paired.
- Nominal SNR (c²·β′Σβ): 24.6 at c = 1 and 6.2 at c = 0.5; S5 is lower, at 17.4 and 4.4.
- At c = 0.5 the smallest coefficient is 0.4.

**Fairness rules.**
- Every method saw the same (X, y) and the same 10 CV folds.
- No method saw the truth, its size or the blocks.
- The truth is in a sealed folder that fitting jobs cannot read.

**Designed but never run:**
- c = 0.75, 0.35 and 0.25 (the response columns exist; nothing was fitted to them);
- Regime L (p = 30, 5 signals, all 2³⁰ models enumerated exactly). Its data were never generated.

---

## 2. Methodology: SMC-BVS v3 as it actually ran

Sources:
- master Part I (lines 122–588);
- `01_Methodology_and_Theory/Methodology/SMC_BVS_v3_20261019/METHODOLOGY_v3.md`;
- the code in `02_Experiments/H_2026-10-22_smcbvs_v3_deploy/E_ops_claude/v2_1/code/`, byte-identical to what ran on NOTS.

The full fact sheet with line citations is `work/METHOD_FACTS.md`.

### The target (the posterior it samples)

X and y are centred and scaled; no intercept is fitted.
- **Coefficients:** a g-prior with g = n plus a unit ridge, β_S ~ N(0, nσ²(X_SᵀX_S + I)⁻¹).
- **Noise:** σ² ~ InvGamma(0.01, 0.01).
- **Model size:** a Beta-Binomial(1, p) prior, which strongly favours small models. Going from k to k+1 variables costs log[(2p−k−1)/(k+1)] nats, about 6.9 nats for the first variable at p = 500.
- **Cap:** no model may have more than K = min(p, ⌊n/2⌋) = 100 variables.
- **Score:** every model S gets an exact closed-form score F(S) = log prior + log marginal likelihood.

### The algorithm, in the order it runs

1. **Blocks.** Cluster the variables by correlation into blocks of at most B = 14, where B = min(⌊√n⌋, ⌊√p⌋, 16). Score every sub-model inside each block exactly.
2. **Start law π₀.** Multiply the size prior and the block scores. This gives a cheap, block-wise approximation to the posterior that can be sampled exactly and whose normaliser is known exactly.
3. **Tempering bridge.** Move a particle population from π₀ (φ = 0) to the true posterior (φ = 1) through the laws π₀·exp(φ·d), where d corrects for interactions between blocks.
   - A pilot picks each step so that the empirical ESS stays near 90%; a forced minimum step can override this.
   - The final grid is then rebuilt so that an ESS computed on a candidate set of already-scored models stays ≥ 90%. This is not a guarantee on the full-space ESS.
4. **Moves at each step.** p Gibbs updates, 1 uniform swap attempt, 14 swap attempts between correlated neighbours, and 1 independence proposal from π₀. Multinomial resampling happens at every step.
5. **Calibration** (random streams 0–9). A pilot plus up to ℓ = 10 (p = 500) or 11 (p = 1000) rebuilds, each checked with 4 diagnostic islands of H = 512 particles and followed by a local search.
   - **Escalation:** calibration is redone once with 4× the particles, pilot size and step ceiling (H = 2,048, final N = 10,000, step ceiling 4,000 instead of 1,000) if any trigger fires:
     - **E1:** some island's best score is more than 1 nat below the overall best;
     - **E2:** the SD of the four log-evidence estimates exceeds 1 nat;
     - **E3:** a local search improves the best model;
     - **a forced pilot step;**
     - **a grid failure or `local_limit`.**
   - Only calibration can trigger escalation. It happened in 208 of 2,400 fits.
6. **Final run** (streams 10–13). Four fresh islands of N = 2,500 particles each (10,000 if escalated) run on the frozen grid, then do 8 burn-in and 4 measured rounds at φ = 1. E1–E3 and low ESS are recomputed, but now only as flags.
7. **Local search.** From the best model, score every single add, drop and swap, and move to the best strict improvement. It takes at most ℓ moves, followed by one extra scan. It runs after the pilot, after each set of diagnostic islands, and after the final run.
8. **Outputs.**
   - **HPM:** the best-scoring model ever scored anywhere in the run. This is the reported selection.
   - **PIPs:** Rao–Blackwellised PIPs from the 4 measured rounds, and the PIP > 0.5 model.
   - **Evidence:** the estimate Ẑ, with a 95% lower bound.
   - **Flags:** E1, E2, E3, lowESS, `cut_group` and `escalated`.
   - **Status:** ok or `resource_limit`. A stopped fit keeps an audit-only support but has no PIPs or evidence.

### Compute

- One CPU per fit; the four islands run one after another.
- **Time limits:** 6,300 s (p = 500) and 24,000 s (p = 1000). The guard checks at fixed points whether the next operation would overrun, judging by how long the last one took. This is not a hard guarantee.
- **Median runtime per fit:** 486 / 522 s at p = 500 (c = 1 / 0.5), and 1,337 / 1,405 s at p = 1000.
- **Retries:** SMC-BVS got no retry for stopped fits. Benchmarks got one doubled-time retry on timeout (`E_ops_claude/GO_2400.md` C5).

### Constants

Your rule is no arbitrary constants. The main declared constants (not derived from n and p) are listed below. Numerical tolerances and cache/store multipliers are further implementation constants.
- the IG(0.01, 0.01) noise prior and the unit ridge;
- the 90% ESS targets;
- the 1-nat E1/E2 thresholds;
- the 0.5N low-ESS flag;
- the 4× escalation;
- 4 islands, 4 measured rounds;
- the floors 2,500 (particles), 512 (pilot) and 1,000 (step ceiling);
- 60 bisection halvings;
- the cap of 16 in B.

These are derived from n and p: g = n, K, B (below its cap), ℓ, the 8 burn-in rounds, the neighbour threshold √(2 log p/n), and the store sizes.

### Where the method and the theory differ

- **Stopped fits.** The theorems assume the run always finishes; 6 fits were stopped.
- **Best scored ≠ posterior's best.** The reported HPM is the best model *scored*, not the posterior's true best model. Theorem T21 links the two, conditionally.
- **Secondary PIP.** The theory still mentions a secondary PIP that the code no longer computes. This is a wording fix.
- **`cut_group`.** It fired in 2,398 of 2,400 fits, so it discriminates almost nothing in this study.

---

## 3. Benchmarks

Sources:
- master Part III (lines 843–2308);
- `Benchmark_Study_20261019/PREREG_c050.md`: the c = 0.5 rules, frozen before any c = 0.5 output was scored;
- the cited fact sheet, `work/BENCH_FACTS.md`.

All benchmarks ran on the same 1,200 datasets per scale, with no failed or missing fits.

### 3.1 The panel

There are 12 benchmark arms (the 8 pre-declared methods plus 4 variants), giving 50 method–rule pairs in the result files.

| Method | How it works (one line) | How it was run | Selection rule |
|---|---|---|---|
| F1 Lasso | ℓ1 penalty that zeroes small coefficients | glmnet 5.1, 10-fold CV on the shared folds | λ with the lowest CV error (`cv_min`) |
| F2 Elastic net | Lasso + ridge, so correlated variables enter together | glmnet 5.1, joint CV over α ∈ {.1, .25, .5, .75, .9} and λ | `cv_min` |
| F3 Adaptive lasso | Lasso with per-variable weights from a ridge pilot fit | glmnet 5.1 with `penalty.factor`; ridge κ by CV | `cv_min` |
| F4 MCP (and SCAD variant) | Non-convex penalty: shrinks small coefficients, leaves large ones nearly unshrunk | ncvreg 3.16.0, γ = 3 (SCAD a = 3.7), deep λ path | EBIC(γ=1) over the path; also EBIC restricted to models of size ≤ 37 (`K37`) |
| F5 ABESS | Best-subset search by swapping variables in and out, for each size 0–100 | abess 0.4.11 | EBIC(γ=1); also `K37` |
| A1 SuSiE | Variational Bayes: the signal is a sum of L single-variable effects; gives PIPs | susieR 0.14.2, L = 50 (variants: L = 100, and `refine = TRUE`) | PIP > 0.5 |
| A2 SSL | Posterior mode under a spike-and-slab Laplace prior, θ ~ Beta(1, p) | SSLASSO 1.2.3.9001, adaptive, unknown variance, λ0 ladder from 1 to n | Support at the end of the ladder |
| SSL-RS (supplementary) | The same SSL with the Ray–Szabó setting (λ1 = 0.01, ladder from 1 to p) | as A2 | as A2 |
| A3 Horseshoe | Continuous global-local shrinkage, sampled by MCMC | bayesreg 1.3, 10,000 burn-in + 15,000 kept draws (thin 5) | 95% credible interval excludes 0 |

### 3.2 What you need to know to read the tables

- **Lasso, elastic net and adaptive lasso score 0 everywhere.**
  - CV tunes them for prediction, so they keep (nearly) all 14 true variables plus, on average, 30–80 extra ones.
  - On the same paths EBIC sometimes picks the exact truth (e.g. lasso `ebic1` scores 111 and 89 of 600 at c = 1), but EBIC is not their primary rule.
- **MCP / SCAD.** The very deep λ path produces near-saturated models, and this creates a false EBIC minimum near size 100.
- **ABESS.**
  - Plain EBIC over sizes up to 100 can also over-select.
  - `K37`, i.e. sizes ≤ ⌊n/log n⌋, limits the size. It does not fix ABESS's search, which is a heuristic (§3.3).
  - `K37` was pre-registered at c = 0.5. At c = 1 it is labelled *post hoc*, because it was chosen after the c = 1 results were seen.
- **SuSiE variants.** SuSiE-refine was added after c = 1 was seen. It never lowered the ELBO, and it adds a little at c = 0.5. SuSiE L = 100 gives essentially the same results as L = 50.
- **SSL-RS** is best at c = 1 (593 and 592 of 600) but collapses at c = 0.5 (32 / 600).
  - Its ladder end point sets a detection threshold of about 0.39–0.41, right at the weakest effect, 0.4.
  - The audit judged this expected behaviour of that setting, not a code bug. That is why the arm is "supplementary".
- **Horseshoe.** 70 fits had a low-ESS flag, all at p = 1000. An 8× longer chain cleared most of them and barely changed the totals (575 → 577 and 136 → 139). That run is reported alongside, never substituted.
- **Not shown here.** The pre-registration also asks for side-by-side `cv_1se`/`K37` rows for F1–F3 and for SCAD (SCAD `K37` at c = 0.5: 96 / 59). The paper tables must include them; the compact tables below do not.
- **Benchmark runtimes are inflated.** The glmnet runs used very strict settings (`thresh` 1e-16 and a deep grid), which inflate their runtimes 20–100× compared with normal use.

### 3.3 Verification status of the benchmark results (open items)

| Gate | c = 1 | c = 0.5 |
|---|---|---|
| G9 independent recount | PASS | Recovery matches on 120,000 / 120,000 rows. A publication-only defect (168 NA cells) was fixed in scoring v7 and checked numerically, but **the formal re-issued verdict is missing** |
| G5 Bayesian (A1–A3, refine) | PASS | PASS |
| G5 frequentist (F1–F5) | **Not certified.** F1–F4 only "partial" (non-primary coefficients were never saved). **F5 fails check 4**: an independent search beat 2,560 of 4,848 ABESS path supports and 7 of 48 selected `ebic1` supports | **Not certified.** Same pattern; F5 beaten in 1,477 of 2,424 path supports and 109 of 168 selected-rule rows |

**What the F5 failure means.** ABESS is a heuristic search: it does not always find the best subset of each size. This is not a scoring bug.

**What happens next.** By the master's rule the benchmark numbers stay "provisional" until G5 and G9 pass. The scoring and verifier code is still logged as "unreviewed". None of this changes any count in §4: the gates need to be closed or disclosed, not rerun.

---

## 4. Results

Each count is the number of datasets, out of 100 per scenario (totals out of 600), in which the method recovered exactly the true 14-variable model. A stopped SMC fit counts as a miss.

Sources:
- `NOTS_BVS/smcbvs_v3_deploy_20261022/F_analysis/HEADLINE_TABLES.md`;
- `score_p0500_20261028T1404Z/` (SMC p = 500 and all benchmarks) and `score_p1000_20261028T1404Z/` (SMC p = 1000);
- independent checks: a recount of all 48 SMC cells, and a review recomputation of every cell (`review/SOL_NUMBERS_REVIEW.md`), with 0 mismatches.

### 4.1 Strong signal, c = 1

| Method | p500: S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000: S1 | S2 | S3 | S4 | S5 | S6 | **/600** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SMC-BVS (HPM)** | 95 | 96 | 94 | 91 | 89 | 94 | **559** | 95 | 95 | 97 | 93 | 84 | 96 | **560** |
| SMC-BVS (PIP > 0.5) | 92 | 97 | 93 | 93 | 90 | 94 | 559 | 94 | 95 | 97 | 94 | 85 | 96 | 561 |
| SSL-RS (suppl.) | 100 | 100 | 100 | 95 | 99 | 99 | **593** | 100 | 100 | 99 | 94 | 100 | 99 | **592** |
| SuSiE | 99 | 98 | 97 | 95 | 98 | 98 | 585 | 100 | 96 | 98 | 95 | 94 | 99 | 582 |
| SuSiE-refine (post hoc) | 99 | 98 | 97 | 95 | 98 | 98 | 585 | 100 | 96 | 98 | 95 | 93 | 99 | 581 |
| Horseshoe | 92 | 98 | 100 | 87 | 98 | 99 | 574 | 91 | 95 | 100 | 91 | 98 | 100 | 575 |
| SSL | 99 | 99 | 97 | 84 | 93 | 97 | 569 | 100 | 96 | 98 | 92 | 97 | 99 | 582 |
| SCAD (EBIC) | 68 | 79 | 78 | 78 | 78 | 73 | 454 | 56 | 67 | 79 | 75 | 61 | 79 | 417 |
| MCP (EBIC, K37, post hoc) | 69 | 79 | 77 | 44 | 78 | 70 | 417 | 66 | 74 | 80 | 32 | 69 | 65 | 386 |
| MCP (EBIC) | 39 | 69 | 77 | 44 | 78 | 70 | 377 | 18 | 28 | 60 | 32 | 49 | 48 | 235 |
| ABESS (EBIC, K37, post hoc) | 68 | 77 | 71 | 26 | 76 | 49 | 367 | 63 | 72 | 76 | 24 | 67 | 54 | 356 |
| ABESS (EBIC) | 66 | 77 | 71 | 26 | 76 | 49 | 365 | 40 | 63 | 76 | 24 | 66 | 54 | 323 |
| Lasso / elastic net / adaptive lasso (CV) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Paired difference on the same datasets** (SMC-BVS rate minus the other method's rate, ± Monte Carlo standard error):

| Comparator | p = 500 | p = 1000 |
|---|---|---|
| SuSiE | −0.043 ± 0.009 (real) | −0.037 ± 0.009 (real) |
| SSL | −0.017 ± 0.011 (within noise) | −0.037 ± 0.009 |
| Horseshoe | −0.025 ± 0.012 (borderline) | −0.025 ± 0.010 |

**How SMC-BVS fails at c = 1.**
- Completed wrong answers:
  - p = 500: 36 are "truth + extra variables" and 4 are mixed (at least one extra and at least one missing);
  - p = 1000: 34 and 3.
- **It never misses a true variable without also adding one.** Its errors are over-inclusion, spread over all scenarios. S5 is the worst, with 11 and 16 misses including stops.
- **Stops (1 and 3).** In their audit-only output, three of the four c = 1 stopped fits had already found exactly the true model before the time guard stopped them. They still count as misses.

### 4.2 Weak signal, c = 0.5

| Method | p500: S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000: S1 | S2 | S3 | S4 | S5 | S6 | **/600** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SMC-BVS (HPM)** | 79 | 84 | 64 | 25 | 59 | 59 | **370** | 71 | 75 | 67 | 35 | 31 | 61 | **340** |
| SMC-BVS (PIP > 0.5) | 74 | 83 | 63 | 18 | 53 | 47 | 338 | 70 | 76 | 63 | 24 | 32 | 56 | 321 |
| SSL | 80 | 84 | 53 | 9 | 42 | 35 | 303 | 67 | 64 | 43 | 15 | 28 | 38 | 255 |
| ABESS (EBIC, K37, prereg.) | 67 | 72 | 34 | 4 | 48 | 31 | 256 | 54 | 64 | 42 | 3 | 23 | 28 | 214 |
| ABESS (EBIC) | 65 | 72 | 34 | 4 | 48 | 31 | 254 | 36 | 55 | 42 | 3 | 22 | 28 | 186 |
| SuSiE-refine (prereg.) | 66 | 71 | 43 | 17 | 6 | 46 | 249 | 49 | 57 | 49 | 22 | 3 | 32 | 212 |
| MCP (EBIC, K37, prereg.) | 62 | 71 | 42 | 1 | 45 | 19 | 240 | 49 | 59 | 45 | 1 | 20 | 18 | 192 |
| SuSiE | 65 | 70 | 34 | 9 | 3 | 39 | 220 | 49 | 57 | 47 | 21 | 0 | 31 | 205 |
| MCP (EBIC) | 38 | 58 | 42 | 1 | 45 | 19 | 203 | 13 | 26 | 34 | 1 | 18 | 10 | 102 |
| Horseshoe | 74 | 69 | 18 | 0 | 10 | 14 | 185 | 60 | 50 | 11 | 0 | 11 | 4 | 136 |
| SCAD (EBIC) | 28 | 24 | 9 | 2 | 15 | 17 | 95 | 22 | 18 | 2 | 0 | 6 | 7 | 55 |
| SSL-RS (suppl.) | 10 | 7 | 5 | 4 | 1 | 5 | 32 | 10 | 13 | 4 | 1 | 3 | 1 | 32 |
| Lasso / elastic net / adaptive lasso (CV) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Paired difference, SMC-BVS minus the other method** (all clearly real):

| Comparator | p = 500 | p = 1000 |
|---|---|---|
| SSL | +0.112 ± 0.019 | +0.142 ± 0.019 |
| SuSiE-refine | +0.202 ± 0.020 | +0.213 ± 0.020 |
| SuSiE | +0.250 ± 0.021 | +0.225 ± 0.021 |
| Horseshoe | +0.308 ± 0.020 | +0.340 ± 0.020 |

**Where SMC-BVS still struggles.**
- **S4 (25 and 35 of 100).** A signal and its 0.85-correlated look-alikes are hard to separate. Every method struggles here, and SMC-BVS is still the best.
- **S5 at p = 1000 (31 of 100).**
- **The kind of error.** Completed wrong answers are mostly "mixed": 131 and 127 fits had at least one extra variable and at least one missing one. Our guess is that a look-alike was picked in place of a true variable, but this has not been checked. There were 49 and 84 pure misses.
- **HPM versus PIP > 0.5.** The HPM beats PIP > 0.5 (370 vs 338, 340 vs 321). This is consistent with T07, under which the HPM is the right rule for exact recovery. It is not a proof that it must win here.

### 4.3 Runtime, stops and flags

- **Median seconds per fit (c = 1, p = 500 / 1000):**
  - SMC-BVS 486 / 1,337;
  - horseshoe 323 / 690;
  - SuSiE-refine 90 / 138;
  - CV lasso family 34–115 (inflated, §3.2);
  - SSL 3.1 / 12.8;
  - SuSiE 1.5 / 2.7;
  - MCP, SCAD and ABESS ≤ 2.2.
- **Relative cost.** Across both scales, SMC-BVS's median is about 250–500× SuSiE's and 85–160× SSL's.
- **Stopped fits:** 6 of 2,400 (`resource_limit`), all in S5.
  - c = 1: 1 at p = 500 and 3 at p = 1000. Three of these had the truth in their audit-only output; the fourth had the truth plus one extra variable.
  - c = 0.5: 2 at p = 1000, both wrong.
  - No timeouts, no crashes.
- **The warning flags do not identify the wrong answers.**
  - At c = 1, p = 500, all 34 flagged fits were correct.
  - At c = 0.5, p = 1000, flagged fits were right 6 of 14 times, against 334 of 586 unflagged.
  - E1 and E3 never fired in the final run.
  - `cut_group` fired in 2,398 of 2,400 fits.

---

## 5. Potential theoretical results

**Where we stand.** 36 conjectures were written for v3 (`01_Methodology_and_Theory/Theory_architecture_v3/theorems/`).
- 12 are fully proved, 8 partly proved, and 16 not proved.
- The proved parts sit in 21 locked proof entries, hash-checked. "Locked" means reviewed and frozen, not adopted. Nothing is adopted until you say so.
- Full audit: `01_Methodology_and_Theory/Theory_architecture_v3/INVENTORY_20261028/THEORY_INVENTORY.md`.

**What it means overall.** The theory has two halves:
- the **statistical half** asks whether the posterior favours the truth;
- the **computational half** asks whether the algorithm finds, scores and reports what the posterior favours.

The two are joined by one fact: SMC-BVS reports the best model it *ever scored*. Theorem T21 turns this into a bound. The chance that the reported model is wrong is at most:
- the chance of no output,
- plus twice the expected posterior mass off the truth,
- plus the chance that the truth was never scored.

So the right answer needs (a) a posterior that favours the truth and (b) the truth to be scored at least once. Full convergence of the sampler is not required, which explains why the HPM works well before the sampler has fully mixed.

**What holds at n = 200 and what doesn't:**
- **The exact results hold**: what the outputs mean, the decision rules, and the correctness of the sampler.
  - The distributional ones (unbiasedness, coverage, miss probabilities) describe the run *as designed to finish*. They do not automatically carry over to "the fits that happened to finish", and the final flags certify nothing.
- **The statistical consistency theorems (T02(ii), T03, part of T04) are long-run only.**
  - They need an eigenvalue condition (SE) that is *impossible* here: rank ≤ 199, against subsets of up to 215–229 columns.
  - T03 also needs squared signal sizes ≥ 55, while ours are 0.64 (c = 1) and 0.16 (c = 0.5).
  - T01, T06, T07 and T04's fallback do not use these conditions.
- **So the 2,400-fit results stand on their own.** The theory explains *why* the method works, not *how often*.

Ranked by how much each matters for a top paper, combining the Fable and Astra advice (`consult/`), from most to least important. Status key: ✔ fully proved, ◐ partly proved, ✘ not proved.

**Tier A: headline (main text of the paper)**

| # | Theorem | Status | What it says | What it means for SMC-BVS at n = 200 |
|---|---|---|---|---|
| 1 | T21 HPM composition | ✔ (one discovery route, (e), needs the unproved H24) | P(no output or wrong HPM) ≤ P(no output) + 2·E[posterior mass off the truth] + P(output but truth never scored). It gives sufficient conditions, not an "only if" | Exact. It is the bridge between the posterior and the report, and the core of the paper's story |
| 2 | T12 Frozen-run identities | ✔ | For the frozen calibrated run, the evidence estimate Ẑ is exactly unbiased, and so is Ẑ × PIP (the PIP alone is not) | Exact, for the run as designed to finish; not conditional on completion. It makes Ẑ meaningful |
| 3 | T11 Scoring ledger | ◐ (iii) | Given successful calibration, a model fixed before the final run's randomness, with start probability π₀, is absent from all Q_f ≥ 140,000 final iid start draws with probability exactly (1−π₀)^Q_f | Exact, for the potential uninterrupted final run. If π₀(truth) ≥ 2.1·10⁻⁵, the truth is scored with probability ≥ 95% (a lower bound; there are other chances to score it). Unknown: whether π₀ is that large |
| 4 | T07 Size-prior ceiling and decision rules | ✔ | For the true posterior, the HPM is the Bayes rule for exact recovery and PIP > 0.5 for counting errors. A size-only prior cannot change the ranking of two models *of the same size* | Exact. It justifies reporting the HPM, and says that re-tuning BB(1, p) cannot fix a same-size swap (a look-alike in place of a true variable). It *can* change truth versus truth + extras, which have different sizes |
| 5 | **T24 Terminal repair** | ✘ **(top open target)** | Starting from a particle near the truth, the chance that H final rounds never score the truth is ≤ (1−a)^H + H·η, under the new conditions LK, EXIT, GAIN plus T03's | Would replace T21's assumed event H24 with a conditional probability bound on not scoring the truth. A nearby (eligible) particle, a completed run, posterior concentration and output availability are still separate requirements. The single result that would lift the paper's tier. Moderate risk that it is false as stated |
| 6 | T03 Selection consistency | ✔ (asymptotic) | With enough data and signal, the posterior concentrates on the true model (HPM = PIP model = truth) | Long-run only: its conditions fail at n = 200. It explains the mechanism, not the 559 / 600 |
| 7 | T09 Kernel validity | ✔ | The start sampler is exact, and every move keeps its target distribution; it also gives a mixing bound | Exact: the algorithm is mathematically correct. Its mixing constant may be exponentially small, so there is no practical speed guarantee |
| 8 | T02 Dimension and supersets | ✔ (asymptotic) | Big models and "truth + extras" get vanishing posterior mass | Vacuous at n = 200, but it points at the real failure mode: ~90% of the completed c = 1 misses are truth + extras |
| 9 | T22 Start aggregation | ◐ (i)–(iv); (iii) needs EXP′ and NL | The block-wise start puts provable mass on a reference model; under favourable conditions it concentrates on the truth | The deterministic bounds hold; the concentration rate is vacuous here. A key input to "the truth gets scored" |

**Tier B: supporting (supplement, cited in the main text)**

| # | Theorem | Status | What it says | What it means |
|---|---|---|---|---|
| 10 | T01 Contrast reduction | ✔ | After standardising y, the posterior is still a standard posterior, with a data-dependent scale | It makes every statistical theorem apply to the method actually shipped |
| 11 | T06 Identifiability and ties | ✔ | Two models tie in score for every response exactly when X_S X_Sᵀ = X_T X_Tᵀ, and no method can separate them. Accidental ties have probability 0 under conditions G and NIS; duplicate columns can tie | A ceiling for every method (e.g. S4 at c = 0.5) |
| 12 | T23 Basin prefix (PIP accuracy) | ◐ (ii) | An island's PIP error, measured against the truth's 0/1 pattern, ≤ the share of particle-rounds away from the truth + a term bounded by the posterior odds against the truth | An exact pathwise bound, but the second term need not be small at n = 200. Turning it into a number needs BASIN (open) |
| 13 | T13 Restricted ESS | ✔ | The grid check only sees models already scored; T13 measures exactly how that blind spot can mislead | Passing the internal checks ≠ accuracy |
| 14 | T20 Local search | ◐ (i)–(ii) | `local_certified` = no better neighbour among those checked. If the truth is the unique peak, a completed scan from a neighbour scores it | The exact meaning of a reported flag; not a global certificate |
| 15 | T31 Certificates | ◐ (i) | 0.05·Ẑ is a 95% lower bound on the evidence (Markov's inequality) | Holds for the run as designed to finish; very conservative |
| 16 | T34 Statuses | ✘ (cheap) | What each output status (ok, `resource_limit`, …) guarantees | Formalises the 6 stopped fits; part of the restatement pass in §6.2 |
| 17 | T27 Cancellation budget | ◐ (i) | If d true variables mask each other (conditions H2, H3, a sequential ratio law, and other assumptions), the start gives the truth mass p⁻ᵈ n⁻ᵈ/² · exp(O_P(1)) | It names the hard regime and is a candidate explanation of weak-signal misses. The random multiplier and the assumptions are not established here, and ≈ 10⁻⁴ for d = 1 is only illustrative |
| 18 | T10 Addition floor | ✔ | Below the cap, adding any variable always has a positive (polynomially small) chance | Every model is reachable, but not necessarily within the budget |
| 19 | T14 First-moment evidence | ◐ (i) | The evidence error is small when the tempered laws stay near one model | Needs a premise not established here |
| 20 | T15 Occupancy | ✔ | The *expected* share of particles in a bad region ≤ its posterior mass / c + P(Ẑ/Z < c), with a matching tail bound | A probability statement, not a bound on a realised population; the evidence-tail input is open |
| 21 | T04 Contraction | ✔ (asymptotic) | Predictions and the noise level are estimated well even when variables can't be identified | Rates uninformative at n = 200; the method reports no coefficients |

**Tier C: technical (supplement or a remark)**

| # | Theorem | Status | What it says | What it means |
|---|---|---|---|---|
| 22 | T33 Numerical margins | ✘ | On a common scored set, the top model is preserved if its gap exceeds twice the numerical score error | One robustness sentence; also gives the tolerance for the truth-score check (§6.3) |
| 23 | T32 Resource counts | ✘ | Explicit compute and memory counts | One complexity sentence |
| 24 | T25 Crossing evidence | ◐ (iv) | The evidence variance is bounded if the one-step stability condition PW2 holds | Adds nothing beyond PW2, which is the real open problem |
| 25 | T28 Evidence loss | ✘ | If calibration misses a hidden region, Ẑ can badly underestimate Z despite being unbiased | An honest failure mode. Untested: without Regime L we have no exact reference |
| 26 | T29 HPM / PIP loss | ✘ | If every scoring route avoids a region, the HPM cannot land there; a PIP failure needs extra reward conditions | Wording for the limitations section. A scored truth can still lose to a higher-scoring model |
| 27 | T16 Frozen limits | ✘ | As particles → ∞, the estimates converge (standard SMC limit theory) | Idealised; says nothing for 4 islands |
| 28 | T26 No-switch consistency | ✘ | Under all assumptions together, Ẑ, the PIPs and the HPM are all consistent | Needs SE (impossible here) plus open conditions |
| 29 | T17 Reflection coupling | ✘ | A comparison device for T18, T19, T25 and T28 | No claim of its own |
| 30 | T18 Reflected pair | ✘ | Exact evidence variance in a two-state toy model | A device |
| 31 | T36 Pilot finite comparison | ✘ | The large-pilot limit of the step-size rule | A remark |

**Tier D: drop or defer**

| # | Theorem | Status | What it says | Why defer |
|---|---|---|---|---|
| 32 | T30 Pilot discovery | ✘ | Given an eligible pilot particle, the chance that calibration misses the truth is bounded by T24's expression; under further asymptotic assumptions it tends to 0 | Stands or falls with T24 |
| 33 | T19 Working-set bounds | ✘ | Conservative error bounds for runs that stay in a working set | Constants useless at this n |
| 34 | T35 Bisection obstruction | ✘ | Under a mass-qualified STIFF condition, every tested positive step of the 60-halving grid search fails | `grid_unconverged` occurred in only 4 of 2,400 fits; the production version is unverified |
| 35 | T05 Orthogonal threshold | ✘ | A sharp recovery threshold under orthogonal designs | Needs p < n; not our setting |
| 36 | T08 Oracle BvM | ✘ | Coefficient posteriors are asymptotically normal given the true model | The method reports no coefficients |

---

## 6. Recommendations

Both consultants worked independently and then signed off on this section:
- advice: `consult/FABLE_ADVICE.md` (Fable 5.1) and `consult/ASTRA_ADVICE.md` (Astra);
- sign-offs: `review/FABLE_SIGNOFF.md` and `review/ASTRA_SIGNOFF.md`. Both are "endorse with changes"; the changes are applied below.

They agree on the core. **Keep the method frozen.** Any change to the sampler forces a 2,400-fit rerun and the whole verification chain again. The previous 2,400 fits used about 780 recorded fit-hours. Put the next effort into a few targeted checks and one big proof.

### 6.1 Decisions for you now

1. **Adopt the locked theory or not.** Do the 21 locked entries (12 full and 8 partial results) become the paper's theory, with the restatement in §6.2 item 1?
2. **Choose the paper's ambition.**
   - (a) **Submit a computational-Bayesian paper soon**, to JCGS or *Bayesian Analysis*. This is both consultants' default.
   - (b) **Hold for T24** and aim for JASA or JRSS-B. This is a gamble: the proof is hard, could be false as stated, and even if proved still leaves conditions to check.
3. **Authorise extra runs (§6.3), in two stages.**
   - Stage 1: the truth-score check, an enumeration timing pilot, and c = 0.75 at p = 500.
     - The c = 0.75 panel is estimated at 155–170 fit-hours from the two measured scales; its actual cost is unknown.
     - The truth scoring and the pilot are extra, and their cost is unmeasured.
   - Stage 2: Regime L at the size the pilot supports. Its cost is unknown until the pilot runs.

### 6.2 What to prove next (in order)

1. **Restatement pass.** No new mathematics; days of work; no risk.
   - Restate T11(iii), T12, T14, T15, T23, T25, T27(i) and T31 for "the run as designed to finish", plus a separate "output available" event, and write T34.
   - This makes the scope honest about the 6 stopped fits. It does not create guarantees for "the fits that happened to finish".
   - In the same pass, fix the T13 wording and drop T12's secondary-PIP clause.
2. **The discovery theorem, in two time-boxed steps.**
   - **Step 1** (Astra; cheap): finish T11's remaining clauses.
   - **Step 2**: T24. It would give a conditional bound on the chance of *not* scoring the truth, given an eligible particle, a completed run, and its conditions (LK, EXIT, GAIN). Combined with T21, this still needs posterior concentration and output availability. It is the biggest payoff, with low-to-medium feasibility.
   - Fable warns that a restricted T22 regime with hypotheses that cannot be checked at n = 200 must not eat T24's time.
   - This is the natural job for the Fable deep theory audit, if you order it.
3. **Finite-n T02/T03 on capped models** (size ≤ K + s₀ = 114). This would remove the rank-199 impossibility, but it needs a new proof and premise checks. The beta-min condition would still fail by about 100× in squared signal, so T03 would still say nothing numerical at n = 200. The gain is in form only. Medium feasibility.
4. **Defer BASIN** (PIP accuracy) and **PW2** (evidence variance). Neither has a route to verification at n = 200.

### 6.3 Extra simulations

**Needed** (both consultants):

1. **Truth-score check.**
   - **What:** for each of the 565 completed wrong answers (77 at c = 1, 488 at c = 0.5), score the true model with the production scorer and compare it with the reported HPM. Audit the 6 stopped fits separately, from their audit-only outputs.
   - **Decision rule, fixed in advance:** let Δ = score(truth) − score(HPM), and fix a numerical tolerance τ ≥ 0 before looking.
     - Δ > τ: a **search (or numerical) failure**;
     - Δ < −τ: a **posterior preference** for the HPM. This does not rule out a search failure as well;
     - otherwise: a **tie / indeterminate**.
     - Also audit preprocessing and numerical stability.
     - τ needs its own justification, because T33, the score-error result, is unproved.
   - **Why:** it answers the first question any referee will ask: was the failure in the search or in the posterior?
   - **Cost:** one score per miss, no refits. Probably hours, but not measured.
2. **Regime L, reduced.**
   - **What:** p = 30, S1–S6, c ∈ {1, 0.5}, against exact enumeration of all 2³⁰ ≈ 1.07·10⁹ models per dataset.
   - **Why:** without it the paper has no evidence that the PIPs and Ẑ are *accurate*; T12 says unbiased, not accurate.
   - **Size:** time one enumeration on Owls first, then choose 60 datasets (Astra) or 240 (Fable). Run several SMC seeds per dataset; they are nearly free once a dataset is enumerated. Pre-state the rule for adding cases.
3. **One intermediate scale, c = 0.75.** The story is a crossover. One point between the two scales helps locate it, though it cannot pin down exactly where it is.
   - **Minimum:** p = 500 only, with SMC-BVS, SuSiE, SSL, SSL-RS and the horseshoe. Pre-register it.
   - **Fuller option (Astra):** c = 0.75 and 0.35 at both p, plus c = 0.25 at 25 replicates. That is about 840–920 SMC fit-hours, and it is the stronger defence against "you chose the scales".
4. **Cost table.** Already measured; no new runs.

**Disputed between the consultants; HQ's view in brackets:**

5. **Sensitivity panel** (Astra yes, Fable no). About 120 existing datasets: repeat with new seeds and a bigger budget, and vary the prior one setting at a time (g, the slab). That is roughly 39 fit-hours per variant. [HQ: do a small version. Referees will ask about the prior, and "standard choice" is a weak answer.]
6. **A same-target comparator** (Astra yes, Fable no). For example, plain MCMC on the *same* posterior, on a small panel. It separates "the posterior is better" from "the SMC search is better" on the wins; the truth-score check does not answer that. [HQ: decide on cost after piloting one fit.]
7. **Real data** (both say supplement only). Astra wants a resampling-stability, prediction and uncertainty assessment, which is more than one fit; Fable wants a single illustrative fit. [HQ: one dataset, with Astra's stability check.]

**Not needed:** more competitors.

### 6.4 Minimal method changes (no rerun of the 2,400 fits)

- **Sampler, prior and moves:** no change.
- **`cut_group`:** drop it from the reports, or redefine it. A new definition can be computed offline from X and the blocks without refitting, but it needs a definition first.
- **Stopped fits:** keep the guard and count the 6 as misses, as the tables already do. From now on, log the phase at which a fit stopped. Optionally rerun the 6 with double the time, as a labelled sensitivity analysis (matching the benchmarks' one retry). Three of the four c = 1 stops had already reached the truth.
- **Flags:** say plainly that they do not certify a fit (§4.3).

### 6.5 Assembling the paper

- **Story.** SMC-BVS is an exact-target Bayesian selector with a finite-sample account of what its outputs mean, for the run as designed to finish.
  - At strong signal it is within 2–4 points of the best fast methods.
  - At weak signal it leads the four Bayesian competitors by 11–34 percentage points, paired.
  - It is about 85–500× slower than SuSiE or SSL (ratio of medians).
  - The theory explains mechanisms, not the n = 200 numbers. Say so first.
- **Main text:**
  - the target, with T01 in brief;
  - the "what the outputs mean" block: T21, T11(iii), T12 and T07;
  - T09 in one sentence;
  - T03 and T02 stated informally, as long-run results.
- **Supplement:** all other proved results and the proofs. Unproved conjectures stay out, except T24 and T27 as named open questions.
- **Likely referee objections, and the answers ready for them:**

  | Objection | Answer |
  |---|---|
  | Slower, and loses at c = 1 | Paired differences, the crossover plot, the cost table |
  | Asymptotic theory is irrelevant at n = 200 | Say so up front; lead with the exact results |
  | No evidence that the PIPs and Ẑ are right | Regime L |
  | Two scales, one n, one sparsity level | c = 0.75 (or the fuller grid); a design-limits paragraph |
  | Competitor tuning | The pre-registration, the post-hoc labels, the full `cv_1se`/`K37` rows |
  | "Best scored" is not the posterior mode | T21 plus the truth-score check |
  | Hidden failures | The 6 stops reported as misses, with a status table |

### 6.6 Housekeeping still open

- **Benchmark gates (§3.3).**
  - Re-issue the G9 c = 0.5 verdict.
  - Decide how to report G5 frequentist at both scales. Simplest: disclose F1–F4 as "partial" and ABESS as a heuristic.
- **NOTS copy of the SMC results.** Delete it; the laptop copy is sha256-verified. Waiting on your OK.
- **Wave-3 proofs.** Their OpenAI external review is still queued.

---

## 7. Where to check everything

| Claim | File |
|---|---|
| Design, method, benchmarks (spec) | `01_Methodology_and_Theory/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md` (Part I 122–588, Part II 589–842, Part III 843–2308) |
| Production code | `02_Experiments/H_2026-10-22_smcbvs_v3_deploy/E_ops_claude/v2_1/code/` |
| SMC run record (2,400 fits, the 6 stops, sha256) | `02_Experiments/H_2026-10-22_smcbvs_v3_deploy/E_ops_claude/OUTPUTS.md`; launch rules `GO_2400.md` |
| Benchmark runs, pre-registration, verification | `02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/` (`RUNS.md`, `PREREG_c050.md`, `verify/`) |
| All result tables | `NOTS_BVS/smcbvs_v3_deploy_20261022/F_analysis/` (`HEADLINE_TABLES.md`; `score_p0500_…/results/` for SMC p500 and all benchmarks; `score_p1000_…/results/` for SMC p1000; `independent_recount/`) |
| Theory status, alignment, intuition | `01_Methodology_and_Theory/Theory_architecture_v3/INVENTORY_20261028/THEORY_INVENTORY.md`; theorem files in `Theory_architecture_v3/theorems/` |
| Fact sheets, merged tables, consultant advice | `04_Reports_and_Presentations/STATUS_BRIEFING_20261028/work/` (`METHOD_FACTS.md`, `BENCH_FACTS.md`, `TABLES.md`) and `consult/` |
| Reviews of this briefing | `review/SOL_NUMBERS_REVIEW.md` (numbers), `review/TERRA_METHOD_THEORY_REVIEW.md` (method and theory), `review/FABLE_SIGNOFF.md`, `review/ASTRA_SIGNOFF.md`; final re-check `review/RECHECK.md` |
