# S1/S2 SPEC (Opus-H, SMC Engineering, 2026-11-25). Binding together with `../INTERFACE.md`.

## 0. OURS choices (everything not taken from a paper or an author's software)
| # | choice | where | why |
|---|---|---|---|
| O1 | **Engine = arm T, the frozen R core v3.1.1** (`method-v3.1.1-listpip`), not F2 | §6, `smc/fit_smcbvs.R` | Owls only; F2 (`p1m-freeze-F2`, C++ engine_v4) exists only as a NOTS sapphirerapids build. T is the owner-signed method (DECISIONS H-17), so no theorem bridge is needed |
| O2 | SMC-BVS `allocation = list(mem_gb = 8, hours = 1e6)` | `smc/fit_smcbvs.R` | an operational guard, not a method setting. At the 24 h default, the v3.1 LS0 worst-case admission charge refuses S1 n = 500 before any computation (projected 303,385 s on Owls). The harness wall timeout replaces it |
| O3 | X rows drawn by the exact AR(1) recursion `x_1 = z_1, x_j = ρ x_{j−1} + √(1−ρ²) z_j` | `harness/generate.R` | the papers give the law N_p(0, Σ), not a draw method. Same law; O(np) instead of an SVD square root. Realisations differ from bestsubset's `sim.xy` (S2) for the same seed. For S1 this is exactly the authors' `lrrsg()` recursion, and draws are identical (§8) |
| O4 | RNG: Mersenne-Twister/Inversion/Rejection; `set.seed(data_seed)`; draw Z (n×p, column-major), then ε (n) | `generate.R` | determinism (INTERFACE "Seeds") |
| O5 | seeds `data_seed = 5·10⁸ + 10⁶·suite + 10³·cell + rep` and `method_seed = data_seed + 10⁷·method_code` | INTERFACE | the project formula (EXPERIMENT_PLAN §2.0.1) |
| O6 | 100 data sets per setting. Neither paper uses 100: Griffin et al. use 200 sampler runs (Table 1 caption context, p.14); HTT use 10 reps (p.9 step vi) | INTERFACE / owner | owner decision |
| O7 | no validation set in S2 (HTT draw one to tune each method, p.9 step iv) | `generate.R` | each method tunes as its own author recommends (INTERFACE rule 1) |
| O8 | S2 uses beta-types 1 and 2 only (HTT also define 3 and 5) | `settings.tsv` | owner/plan (EXPERIMENT_PLAN §2.0.3) |
| O9 | `success` = the selected set equals the true support exactly | `run_one.R` | INTERFACE |
| O10 | Bayesian selection = MPM (PIP > 0.5); frequentist λ rule (lasso `lambda.min` vs `lambda.1se`) | adapters | INTERFACE (Fable-F flags the lasso choice) |
| O11 | SMC-BVS "top models with weights": the returned top store, weights renormalised over the store, `u_S = exp(F(S) − max F)/Σ` | `fit_smcbvs.R` | a list view (SPEC_LIST_PIP); the SMC PIPs and log-evidence are the method's own estimates |
| O12 | cell numbering, `setting_id`, the extra `label` and `nu_pop` columns | `settings.tsv` | bookkeeping |
| O13 | smoke combos = the mid settings of §5; smoke and grid timeouts | `smoke.R` | the manager's brief. Nothing in either paper names a "mid" setting |
| O14 | X is neither centred nor scaled, and there is no intercept, in the data | `generate.R` | neither paper standardises in its DGP (quotes §1). The authors' S1 repo scales after generating (`dataset_generation.R:28-29`). We do that in the adapters (§8) |
| O15 | S2 uses the same repo preprocessing for the Bayesian methods as S1 (HQ ruling (b)); HTT have no Bayesian methods | adapters | one preprocessing rule per method across suites; the adapters tag the S2 prior transfer as OURS (`ctrl$suite`) |

Engine: **SMC-BVS v3.1.1, R core, tag `method-v3.1.1-listpip`** = commit `15a6d841c57fa9b66bfa46223336ebbec61f8049`, core tree `61b0a5822019b2737fe415ff15625e410f3227b2` (= DECISIONS H-17 "core tree 61b0a582"), LS0 on (v3.1 default). The tree is exported unedited to `ROOT/ext/smcbvs_core@7100bb3b/` and compiled with its own `Makevars.v3`. Engine tag string in records: `method-v3.1.1-listpip (commit 15a6d841, core tree 61b0a582; R core v3.1.1, ls0 = TRUE)`.

Settings: **136** = S1 16 + S2 120 (`settings.tsv`).

**Preprocessing (HQ ruling (b), 2026-11-25; detail in §8):**

| methods | what they get | who does it |
|---|---|---|
| ASI, BAS-MC3, SuSiE (Bayesian adapters) | `X <- scale(X)`; `y <- scale(y, scale = FALSE)` | the adapter, as in The-PARNI-scheme@3b95d669 `R/simulation/dataset_generation.R:28-29` and `simulation_example.R:11-12` |
| SMC-BVS | raw X, y. `v3_fit` itself centres and scales every X column and y (`v3_preprocess`, M §4.4). This equals the repo preprocessing to ≤ 1.8e-15 (`generator_check.md`), so the adapter adds nothing | the engine |
| lasso (glmnet), SCAD (ncvreg) | raw X, y. glmnet standardises internally (`standardize = TRUE`) and fits an intercept; ncvreg standardises internally and fits an intercept | the package (author defaults) |

## 1. Sources and exact text

**S1.** Griffin, J. E., Łatuszyński, K. G. & Steel, M. F. J. (2021). In search of lost mixing time: adaptive Markov chain Monte Carlo schemes for Bayesian variable selection with very large p. *Biometrika* 108(1), 53–69, doi:10.1093/biomet/asaa055. Read from arXiv:1708.05678**v3** (7 May 2019), the PDF on Owls (`_local/theory/BENCH_DESIGN/papers/BVS_Griffin2021.pdf`). Page numbers are the arXiv v3 pages.
- p.13, Sec 4.1, para 1: *"We consider the simulated data example of Yang et al. (2016). They assume that there are n observations and p regressors and the data is generated from the model Y = Xβ* + e where e ∼ N(0, σ²I) for σ² = 1. The first 10 regression coefficients are non-zero and we use β* = SNR √(σ² log p / n) (2, −3, 2, 2, −3, 3, −2, 3, −2, 3, 0, …, 0)ᵀ ∈ ℝᵖ. The i-th vector of regressors is generated as xᵢ ∼ N(0, Σ) where Σ_jk = ρ^|j−k|. In our examples, we use the value ρ = 0.6 which represents a relative large correlation between the regressors."*
- p.14, Table 1: rows (n, p) = (500, 500), (500, 5000), (1000, 500), (1000, 5000); columns SNR = 0.5, 1, 2, 3.
- p.14, para 1 (for the benchmark adapters, not the DGP): *"We use the prior in (2) with V_γ = 9I and h = 10/p, implying a prior mean model size of 10."* Model (1), p.4: `y = α1ₙ + X_γβ_γ + e` (an intercept with a flat prior).
- Not stated: any centring or scaling of X. The nonzero positions are explicitly the first 10.

**S2.** Hastie, T., Tibshirani, R. & Tibshirani, R. (2020). Best subset, forward stepwise or lasso? Analysis and recommendations based on extensive comparisons. *Statistical Science* 35(4), 579–592, doi:10.1214/19-STS733. Read from arXiv:1707.08692**v2** (29 Jul 2017), the PDF on Owls (`.../papers/Hastie2020.pdf`), Sec 3.1 "Setup", pp. 8–10.
- p.8–9, steps i–iii: *"i. we define coefficients β₀ ∈ ℝᵖ according to s and the beta-type …; ii. we draw the rows of the predictor matrix X ∈ ℝ^{n×p} i.i.d. from N_p(0, Σ), where Σ ∈ ℝ^{p×p} has entry (i, j) equal to ρ^|i−j|; iii. we draw the response vector Y ∈ ℝⁿ from N_n(Xβ₀, σ²I), with σ² defined to meet the desired SNR level, i.e., σ² = β₀ᵀΣβ₀/ν"*. So **σ² uses the population Σ**, not the sample covariance.
- p.9, "Coefficients": *"beta-type 1: β₀ has s components equal to 1, occurring at (roughly) equally-spaced indices between 1 and p, and the rest equal to 0; beta-type 2: β₀ has its first s components equal to 1, and the rest equal to 0"*.
- p.10, "Configurations": *"high-5: n = 50, p = 1000, s = 5; high-10: n = 100, p = 1000, s = 10"*; *"ten values for the SNR ranging from 0.05 to 6 on a log scale, namely 0.05 0.09 0.14 0.25 0.42 0.71 1.22 2.07 3.52 6.00"*. ρ ∈ {0, 0.35, 0.7}: p.10, the same paragraph (*"In each setting, we also considered three values for the predictor autocorrelation ρ, namely 0, 0.35, and 0.7."*).
- The authors' code fixes "roughly equally spaced": R package `bestsubset`, github.com/ryantibs/best-subset @ `796e81713634aef8b66363f9740efed5df3ba213` (master, 2023-07-24), `bestsubset/R/sim.R` (sha256 `e497edec…4c34b`), `sim.xy`: `beta[round(seq(1,p,length=s))] = 1` (type 1), `beta[1:s] = 1` (type 2), `vmu = t(beta) %*% Sigma %*% beta; sigma = sqrt(vmu/snr)`. We use these lines verbatim. With R's `round` (half to even), the type-1 positions are **{1, 251, 500, 750, 1000}** for s = 5 and **{1, 112, 223, 334, 445, 556, 667, 778, 889, 1000}** for s = 10.
- Not stated: any centring or scaling of X in the DGP (`sim.xy` does none). Each fitting method standardises internally.

## 2. S1 (16 settings): Griffin et al. 2021 Sec 4.1, exact
| item | value |
|---|---|
| X rows | i.i.d. N_p(0, Σ), Σ_jk = 0.6^|j−k|; raw, no centring or scaling |
| β* | SNR·√(σ² log p / n)·(2, −3, 2, 2, −3, 3, −2, 3, −2, 3, 0, …, 0); support = {1, …, 10}; natural log |
| σ² | 1 (`sigma2_rule = fixed_1`) |
| (n, p) | (500, 500), (500, 5000), (1000, 500), (1000, 5000) |
| SNR | 0.5, 1, 2, 3 |
| cells | S1_01…S1_16: cell = 4·(k − 1) + j, k = the (n, p) row of Table 1, j = the SNR column |
| derived ν_pop = β*ᵀΣβ*/σ² | (500,500): 0.080 / 0.319 / 1.277 / 2.874; (500,5000): 0.109 / 0.438 / 1.750 / 3.938; (1000,500): 0.040 / 0.160 / 0.639 / 1.437; (1000,5000): 0.055 / 0.219 / 0.875 / 1.969 |

## 3. S2 (120 settings): Hastie, Tibshirani & Tibshirani 2020 Sec 3.1, exact
| item | value |
|---|---|
| X rows | i.i.d. N_p(0, Σ), Σ_ij = ρ^|i−j|, ρ ∈ {0, 0.35, 0.7}; raw |
| (n, p, s) | high-5 (50, 1000, 5); high-10 (100, 1000, 10) |
| β₀ | type 1: ones at `round(seq(1, p, length = s))`; type 2: ones at 1..s |
| σ² | β₀ᵀΣβ₀/ν with the population Σ (`sigma2_rule = pop_Sigma_over_nu`) |
| ν | 0.05, 0.09, 0.14, 0.25, 0.42, 0.71, 1.22, 2.07, 3.52, 6.00 |
| cells | S2_001…S2_120: cell = 30·(2(c − 1) + (t − 1)) + 10·(r − 1) + k, with c = config (high-5, high-10), t = beta-type, r = ρ index, k = ν index |

## 4. settings.tsv
Columns: `setting_id, suite, cell, n, p, s0, rho, snr, nu, beta_type, sigma2_rule, citation` (the INTERFACE columns), then `label, nu_pop` (O12). S1: `snr` = Griffin's SNR, `nu = NA`, `beta_type = griffin`. S2: `snr = NA`, `nu` = HTT's ν, `beta_type ∈ {1, 2}`. `nu_pop` = β*ᵀΣβ*/σ² for both. It is written by `harness/make_settings.R`.

## 5. Smoke combos (mid settings; O13)
S1 SNR = 2 at each (n, p): **S1_03** (500, 500), **S1_07** (500, 5000), **S1_11** (1000, 500), **S1_15** (1000, 5000). S2, ρ = 0.35, beta-type 1, ν = 0.71: **S2_016** (high-5), **S2_076** (high-10). Rep 1 only. The papers name no "mid" setting. SNR = 2 is where Griffin et al. report the largest ASI gains (p.15), and ν = 0.71 is the middle of HTT's grid (the 6th of 10 values, PVE 0.42).

## 6. SMC-BVS engine (O1, O2)
- **Arms** (EXPERIMENT_PLAN §2.0.7). T = the frozen v3.1 core: law N = max(2500, n, p), R′ = 4 islands, the coded calibration with escalation (tier 1 = 4×N, H, T), LS0. F2 = the C++ production engine `p1m-freeze-F2`: fixed N = 2,500, R′ = 16, I_max 0. F2 is built only on NOTS (sapphirerapids ISA; §6A.7: "An Owls build is unverified"). This turn is Owls-only and must not do p = 1M work, so **F2 is out and T is used**. T is also the object the theorems cover, so no T/F2 bridge is needed for S1/S2 claims.
- **Interface**: `v3_fit(X, y, seed = method_seed, allocation)`; nothing else is passed and no `options(v3.*)` is set. Selection = `fit$mpm` (PIP > 0.5 on `pip_primary`). Logged: `pip` (length p), the top 50 models with list weights, `log_Z`, `log_Z_r`, `log_Z_rel_m0`, `stage_table` (ESS per stage, all phases), `N_particles` (= the tier's N), the tier and escalation flag, flags, timings, peak memory, preflight, the list-PIP fields, and the engine tag.
- **Cost risk**: T is single-threaded; plan §6A.3 estimates 13.8 NOTS core-h per fit at p = 5,000 (≈ 132 Owls core-h on the riboflavin anchor). The smoke timings replace those estimates (`RUNTIME_ESTIMATE.md`).

## 7. Records
`ROOT/runs/S1S2/<method>/<setting_id>/rep_<RRR>.{json,rds}` (`ROOT = /home/fb31/Bayesian-Variable-Selection/_local/engineering`). The json holds the INTERFACE fields, the SNR three ways (`snr`, `nu_pop`, `nu_sample` = Var_n(Xβ)/σ², `pve_pop`), the data md5 and an SMC summary. The rds adds `pip` and `extra`. Generator check: `generator_check.md`.

## 8. Preprocessing and benchmark tuning (HQ rulings after the GitHub sweep, 2026-11-25)
**S1 reference design.** XitongLiang/The-PARNI-scheme @ `3b95d669e9bcf6df9e2ba46fb89fc536922e12e2` (Griffin is a co-author), `R/simulation/dataset_generation.R` + `R/simulation/linear regression random sample generator.R` (`lrrsg`). Our S1 generator reproduces `lrrsg()` **bit for bit** for the same seed (X, β and y; all 16 settings, reps 1–2; `generator_check.md` §"S1 generator against …"). That holds because both use the same AR(1) recursion, the same draw order, σ² = 1 and natural log p, with positions 1..10. Our generator still returns raw X and y (INTERFACE). The repo's `scale()` step belongs to the Bayesian adapters.

**ASI** (owner decision 2026-11-25): Griffin's original **`ASI_sampler.m` v3.0, run unmodified** under user-space GNU Octave (`ROOT/envs/`, installed by Fable-B; Octave version **PENDING**; sampler sha256 **PENDING**). PARNI's `ASI.R` is no longer the benchmark. Settings: V_γ = 9I and h = 10/p (paper, Sec 4.1 p.14); burn-in 2,000 + 4,000 recorded (repo example `simulation_example.R:67-68`); τ = 0.2 (repo, l.74); 25 chains (l.76), heat 1, ASI adaptation; κ, ε and ζ as `ASI_sampler.m` hard-codes them (values **PENDING** from Fable-B). Tag: "authors' code; repo example run length/τ; not stated in Biometrika text". The ASI smoke cells will be rerun through the Octave adapter.

**BAS-MC3** (Fable-B's adapter): author defaults, run length 120,000 + 60,000 (manager, 2026-11-25; exact values **PENDING from Fable-B**). The earlier 180,000 + 60,000 repo-ADS ruling is superseded.

**SMC-BVS:** no change. The engine's own standardisation already covers the ruling (§0 Preprocessing). The smoke fits ran on raw X and y, which is the intended input, so no rerun is needed.

## 9. Prior per method (owner decision (A), 2026-11-25: each method runs its own author's prior; nothing is shared between methods)

| method | prior as run | source |
|---|---|---|
| SMC-BVS | slab β_S ~ N(0, n σ² (X_SᵀX_S + I)⁻¹) (g = n plus a ridge term), on X and y standardised by the engine; σ² ~ IG(0.01, 0.01); γ ~ BB(1, p) truncated to \|S\| ≤ min(p, ⌊n/2⌋); no intercept parameter (centring) | engine default, v3.1.1, no edits; details and file:line below |
| ASI | V_γ = 9I, h = 10/p (prior (2): independent normal slab on scaled X, flat intercept, p(σ²) ∝ σ⁻²) | Griffin et al. 2021 Sec 4.1 p.14; run by Griffin's `ASI_sampler.m` v3.0 under Octave (version, sha256 PENDING) |
| BAS-MC3 | `bas.lm` 2.1.0 shipped defaults for `prior` and `modelprior`: **exact values PENDING from Fable-B** | BAS 2.1.0 (author defaults) |
| SuSiE | susieR 0.14.2 defaults; **L = 20 (OURS)** | susieR defaults |
| Lasso-CV | glmnet defaults (no prior) | glmnet 5.2 |
| SCAD | ncvreg defaults (no prior) | ncvreg 3.16.0 |

**SMC-BVS prior as run** (`v3_fit(X, y, seed, allocation)`, v3.1.1; files in `Scripts/SMC_BVS/core/` at tag `method-v3.1.1-listpip`, identical to `ROOT/ext/smcbvs_core@7100bb3b/`):
- **Data:** every X column and y are centred and scaled to sample SD 1 (`v3_preprocess.R:35-68`, `v3_standardise`; l.123 for y). There is **no intercept parameter**. Centring stands in for it, and the likelihood keeps n (not n − 1) degrees of freedom (`cpp/v3_score.h:57`, ν = a₀ + n/2).
- **Slab β_S | σ², S:** a ridge-stabilised g-prior with g = n: **β_S ~ N(0, n σ² (X_SᵀX_S + I)⁻¹)**. Read from the marginal: H = (n+1)G_S + I, A = G_S + I (`cpp/v3_score.h:175-182`), Q_S = yᵀy − n zᵀH⁻¹z (l.217), log m(S) = log C_n − ½(log|H| − log|A|) − ν log(2b₀ + Q_S) (l.223). The closed form under that prior equals this to 3·10⁻¹¹ (`harness/check_smcbvs_prior.R`, direct integral over σ²). On standardised X, X_SᵀX_S ≈ (n−1)I gives a prior covariance ≈ σ²I, i.e. **an effective prior variance of about 1·σ² per coefficient**.
- **σ²:** Inverse-Gamma(a₀ = 0.01, b₀ = 0.01) (`cpp/v3_score.h:14`, l.57-59), a proper approximation to p(σ²) ∝ σ⁻² that acts on the standardised y.
- **Model prior:** **beta-binomial BB(1, p)** on γ, w(k) = ½ / C(2p−1, k) per model of size k (`cpp/v3_score.h:15, 65`), truncated to |S| ≤ K = min(p, ⌊n/2⌋) and renormalised (l.40, 66-70). The prior mean model size is p/(p+1) ≈ 1.

## 10. Theory diagnostics in every run record (manager brief 2026-11-25; code: `harness/diagnostics.R`, `run_one.R`, hook `diag_smcbvs` in `smc/fit_smcbvs.R`)
All definitions are OURS. They are computed by the harness **after** the fit; adapters never see S0 while fitting. Seeds are stored, never X or y. Small fields go in the json, heavy ones only in the rds. A diagnostics error never fails a record.

| json field | definition |
|---|---|
| `diag_data.beta_min`, `.beta_min_ratio` | min over S0 of abs(β_j) (raw-X scale); ratio = beta_min / (σ·sqrt(log p / n)), with σ the true SD |
| `diag_data.lambda_min_S0` | smallest eigenvalue of X_S0ᵀX_S0 / n, with X scaled by `scale()` (centred, sample SD n − 1) |
| `diag_data.max_abs_corr_null_true` | max abs(cor(X_j, X_k)) over j ∉ S0, k ∈ S0 |
| `diag_data.sigma2`, `.snr_realised` | true σ²; Var_n(Xβ)/σ² (also in `snr_three_ways`) |
| `diag_post.min_true_pip`, `.max_null_pip`, `.n_null_pip_gt_half`, `.sum_pip` | from the method's PIP vector |
| `diag_post.pi_S0` | posterior weight of S0 in the method's model list (0 if not in the list); null when the method returns no list |
| `diag_post.gap_logpost`, `.best_rival` | logpost(S0) − logpost(best model ≠ S0 in the list); "(empty model)" = the null model |
| `diag_post.mass_size_gt_2s0` | list weight on models with abs(γ) > 2·s0 |
| `diag_post.models_source` | which list: SMC-BVS = the engine's whole top store (best visited models by F), weights exp(F − max F) renormalised over the store (list view, not the particle estimate); BAS / SuSiE adapters return no list today, so these three fields are null |
| `diag_post.sigma_hat` | {value, which}. SMC-BVS: sqrt E[σ² ∣ y, MPM] under the engine prior = (b0 + Q/2)/(a0 + n/2 − 1), a0 = b0 = 0.01, on the engine's standardised y, rescaled to y. SuSiE: sqrt(fit$sigma2). BAS: not returned by the adapter |
| `diag_post.logpost_S0`, `.logpost_selected`, `.logpost_hpm` (SMC-BVS) | F = log prior + log marginal from the engine's own scorer `v3_score` (v3_setup.R:16) on the engine's own preprocessed data; NA if abs(S0) > K |
| `diag_post.hpm_F_check` (SMC-BVS) | scorer F(HPM) − the fit's hpm_F; 0 up to rounding (a check that the scorer and the fit agree) |
| `failure_type` | "none" if the MPM equals S0; for SMC-BVS "search" if F(S0) > F(MPM), else "statistical"; "other" for a failed fit; "unclassified (no scorer)" for methods without a scorer |
| `eflag_any`, `eflags` (SMC-BVS) | engine E-checks that fired: E1 (an island best more than 1 below the global HPM), E2 (sd of the island log Z > 1), E3 (the final local search raised the global best), low_empirical_ESS (some stage ESS < N/2), all from v3_run.R:182-204; plus "status:<v3 status>" when the engine did not complete. `eflag_any` = any of them (= not checks_passed_final) |
| `summary.engine_warnings` (SMC-BVS) | recorded, not E-flags: local-search move caps, truncated near-tie list, unconverged grid, tier escalation, calibration triggers |
| `summary.min_ess_over_N` (SMC-BVS) | min over the final (inference) run of ESS / N, N = particles per island of the frozen tier; the stage, island and φ are in the rds (`extra$ess_min`) |
| `summary.log_Z`, `.log_Z_r_sd`, `.log_Z_r_range` (SMC-BVS) | log evidence and the spread of the 4 island estimates |
| `diag_sec` | seconds spent on diagnostics (the scorer's Gram is O(np²)) |

rds only (SMC-BVS): full PIP; `extra$stage_table` (every stage: phase, tier, island, stage, φ, ESS, `ess_over_N` (final run), log increment, cumulative log Z, distinct models resampled / moved, acceptance rates per kernel); `extra$top_models` (top 50: model, F, list weight, size); `extra$list_size_mass` (list weight by model size over the whole store); `extra$log_Z_r`; `extra$flags` (all engine flags); `extra$timings`. The engine does not record mean model size or a resample flag per stage. `harness/rediag.R` backfills these fields into a record written before them, without refitting; its model list is the 50 models saved in the record (flagged `diag_backfill`).
