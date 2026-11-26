# Bayesian benchmarks for S1/S2: add-delete-swap MC3 (BAS), ASI (the authors' `ASI_sampler.m` under Octave), SuSiE (susieR)

Builder: Fable-B, 2026-11-25; last revised the same day for the owner's decisions relayed by the manager: (A) BAS runs on `bas.lm`'s own default prior and model prior, 120000 + 60000 steps; all three adapters scale X and centre y; **ASI is Griffin's original `ASI_sampler.m` v3.0, run unmodified under user-space GNU Octave 10.3.0** (`fit_asi.R` with the driver `asi_octave/run_asi.m`; no shims). The PARNI-repo adapter is kept as `fit_asi_parni.R`, not registered, for comparison only. Earlier rulings of the day (shared prior with g = 9(n − 1) for BAS, τ = 0.234, an R port of the MATLAB code, PARNI's `ASI.R` as the benchmark) are withdrawn. Contract: `../../INTERFACE.md`. Nothing here is committed by the builder.

| File | What it is |
|---|---|
| `fit_bas_mc3.R` | `fit_bas_mc3(X, y, method_seed, ctrl)`: `BAS::bas.lm(method = "MCMC")`, the add-delete-swap MC3 sampler |
| `fit_asi.R` | `fit_asi(X, y, method_seed, ctrl)`: writes X, y and the 18 arguments to a temporary directory, runs the sha256-pinned, unmodified `ASI_sampler.m` in `octave-cli` through the driver, reads back the code's `prob_inclusion` |
| `asi_octave/run_asi.m` | the Octave driver (OURS): reads the files, seeds `rand` and `randn`, calls `ASI_sampler` with the 18 arguments, writes the returned fields. It holds no sampler code and sets no value |
| `fit_asi_parni.R` | `fit_asi_parni()`: the former adapter (the R `ASI()` of the PARNI repo at a pinned commit). Reference only; **not registered** in `harness/methods.R` |
| `fit_susie.R` | `fit_susie(X, y, method_seed, ctrl)`: `susieR::susie(X, y, L = 20)` |
| `test_bayesian.R` | unit test (contract, fidelity to the authors' call, sampler sha256, seed-only randomness and determinism, never-error, timing). `--full` adds n = 1000, p = 5000; `--long` runs ASI at its default length on the two SNR-3/SNR-6 cases; `--cases=<regex>` runs section 1 for the matching cases only |
| `ASI_DIFF.md` | line-by-line table: paper Algorithm 2, the original `ASI_sampler.m` (runs), the PARNI R code (reference); the decision table D-1 to D-10 the owner ruled on |

Each script opens with a PROVENANCE block (paper, DOI, section and page, software version or commit, every setting with its source and an author/OURS tag). This README is the summary. Selection for all three is the median probability model, PIP > 0.5 (OURS, fixed by the contract); the full PIP vector is returned.

## Software (authors' own, nothing reimplemented)

| Software | Version | Source | Where |
|---|---|---|---|
| BAS | 2.1.0 (CRAN, published 2026-11-23) | installed 2026-11-25 from cloud.r-project.org | `/home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib` |
| susieR | 0.14.2 (CRAN, published 2025-06-05) | same | same |
| Griffin, Łatuszyński & Steel's original ASI code (MATLAB), **the ASI benchmark** | `ASI_sampler.m` of `Version3.0.zip`; file sha256 `4705c79523f4d772625764bcb880ed04852d83d121ea94fe46ef224d3b10dddb`; zip sha256 `ce3e9c75…460f42` | `https://jimegriffin.github.io/website/Version3.0.zip` (the link named on p.16 of the paper), fetched 2026-11-25T20:58Z; byte-identical to the owner's supplement copy `_local/papers/Benchmark_methods/Griffin2021_supplement/code/Version3.0/` | `/home/fb31/Bayesian-Variable-Selection/_local/engineering/ext/griffin_asi_original/Version3.0/` with `PROVENANCE.txt` (sha256 of every file; not in git) |
| GNU Octave (runs the `.m` file; MATLAB is not on Owls) | 10.3.0, conda-forge build `pl5321hd0fbda6_4`, OpenBLAS 0.3.34 (pthreads) | installed 2026-11-25 in user space with micromamba 2.10.0 (`github.com/mamba-org/micromamba-releases`, binary sha256 `701f39c0…75e8bd`) from conda-forge; no sudo, nothing system-wide, package cache inside ROOT | env `/home/fb31/Bayesian-Variable-Selection/_local/engineering/envs/octave` (1.8 GB); package cache `/home/fb31/Bayesian-Variable-Selection/_local/engineering/envs/_conda_pkgs` (0.8 GB); micromamba at `/home/fb31/Bayesian-Variable-Selection/_local/engineering/envs/bin/micromamba`. Call `bin/octave-cli` with `OCTAVE_HOME` set to the env path (the adapter does) |
| The-PARNI-scheme, **reference only** (`fit_asi_parni.R`) | commit `3b95d669e9bcf6df9e2ba46fb89fc536922e12e2` (2026-03-14) | `https://github.com/XitongLiang/The-PARNI-scheme` | `/home/fb31/Bayesian-Variable-Selection/_local/engineering/ext/The-PARNI-scheme@3b95d669e9bcf6df9e2ba46fb89fc536922e12e2/` (not in git) |
| RhpcBLASctl | 0.23-42 (CRAN) | installed 2026-11-25 | Rlib; used only to cap BLAS/OpenMP threads |

Dependencies pulled in by susieR and BAS: mixsqp 0.3-54, irlba 2.4.1, matrixStats 1.5.0, reshape 0.8.10, plyr 1.8.9, crayon 1.5.3. R 4.6.0 on Owls.

`fit_asi.R` computes the sha256 of `ASI_sampler.m` before every run and refuses to run if it differs from the pin above; after the run it checks that Octave resolved `ASI_sampler` to that same file. The file runs under Octave as shipped: **no shims**. The only name in it that Octave lacks is `stop`, which the code calls when a quantity turns complex; MATLAB has no argument-free `stop` either, so in both systems that call ends the run with an error, and the adapter then returns `status = "failed: …"`. `fit_asi_parni.R` still `sys.source()`s three unmodified files of the PARNI clone and checks the clone's HEAD and three md5 sums.

CRAN's susieR is 0.14.2, the Wang et al. (2020) algorithm. It is not "SuSiE 2.0" (McCreight et al. 2025, in `Core_bibliography`); the task said CRAN, so 0.14.2 is what runs.

**Which ASI code runs, and why.** The paper's own code (p.16: "Code to run both algorithms is available from https://jimegriffin.github.io/website/") is MATLAB. The owner ruled that this code is the benchmark and that it runs unmodified under GNU Octave. The R implementation in the PARNI repo (Liang, Livingstone & Griffin 2022) differs from it in ten places (`ASI_DIFF.md`, D-1 to D-10) and is no longer the benchmark. A second, later archive of the same name from Steel's Warwick page (sha256 `8132160c…e911`, kept at `_local/engineering/ext/GriffinLatuszynskiSteel_version3.0_reference/`) has the same tuning constants in its `ASI_sampler.m`; it is not used.

## Protocol

**Preprocessing, all three (HQ ruling b).** Each adapter first runs `X <- scale(X); y <- scale(y, scale = FALSE)`, as the authors' repo does for the S1 design (`simulation_example.R` l.12-13, `dataset_generation.R` l.28-29), and records it in `settings$preprocess`. For ASI this is done once, on the R side: `ASI_sampler.m` neither centres nor scales (m.52, m.67, m.83, m.293-309) and adds its own unpenalised column of ones (m.67, m.72-73). The authors' two run scripts centre X and y and do not scale (`run_tecator.m` l.8-12, `run_concrete.m` l.19-23), so the centring follows them and the scaling to unit sd is OURS relative to the original code.

**BAS MC3 (owner's option (A): package defaults).** `set.seed(method_seed); fit <- BAS::bas.lm(y ~ X, method = "MCMC", MCMC.iterations = 120000, burnin.iterations = 60000)`; PIP = `fit$probne0[-1]` (MCMC frequencies, intercept dropped). Everything else is the `bas.lm` default, including the priors: `prior = "ZS-null"`, `modelprior = beta.binomial(1, 1)`, `prob.rw = 0.5`, `thin = 1`, `pivot = TRUE`, start at the null model, `renormalize = FALSE`. BAS runs 180000 MH steps and averages over all of them (item 4). The same call is used in S1 and S2.

The shipped defaults that define the method, as `formals(BAS::bas.lm)` gives them in BAS 2.1.0; none is passed, and each is recorded in `settings` with the tag "author" and the source "author (bas.lm 2.1.0 default): formals(bas.lm)$<name> = <value>":

| Argument | `formals(bas.lm)` | Meaning |
|---|---|---|
| `prior` | `"ZS-null"` | Zellner-Siow: β_γ ~ N(0, gσ²(X_γ'X_γ)⁻¹), 1/g ~ Gamma(1/2, n/2); flat intercept, p(σ²) ∝ σ⁻²; Bayes factor by Laplace approximation |
| `alpha` | `NULL` | `bas.lm` then sets 1 for `"ZS-null"` |
| `modelprior` | `beta.binomial(1, 1)` | inclusion probability ~ Uniform(0, 1): uniform on the model size |
| `include.always` | `~1` | only the intercept is forced in |
| `update` | `NULL` | not used by `method = "MCMC"` |
| `prob.rw` | `0.5` | proposal mix: flip of one coordinate with probability 0.5, else swap |

**ASI (the original `ASI_sampler.m` under Octave).** `fit_asi.R` writes the preprocessed X and y (raw doubles) and the arguments (`%.17g`) to a temporary directory under `ROOT/_local/tmp`, then runs `octave-cli --norc --no-history --quiet --no-window-system asi_octave/run_asi.m` with `OMP_NUM_THREADS = OPENBLAS_NUM_THREADS = 1`. The driver does

```
rand("state", method_seed); randn("state", method_seed);
output = ASI_sampler(data_fixed, data, target, g, gprior, mode, RB_adap, RB, hparam, tau, nu, burnin, numbofits, thin, numbofreps, heat, adap_type, updateg);
```

and writes the returned fields. PIP = `output.prob_inclusion` = `sumgamma / (numbofits * numbofreps)` (m.529, m.565): the code's own estimator, the plain mean of γ over the 4000 × 25 = 100,000 recorded draws of all chains. It is not Rao-Blackwellised, whatever `RB` is (`instructions.pdf` p.5 says otherwise; the name `RB` occurs only on line 1 of the file, and `prob_inclusion2` comes back as zeros). The temporary directory is deleted after the run. `runtime_sec` is the wall time of the Octave call; the sampler's own time and the Octave start-up + file time are in `extra` (start-up is 0.3 to 0.7 s).

The 18 arguments. Sources: [P] the Biometrika paper; [INS] `instructions.pdf` in the code folder (5 pages; it documents 15 arguments); [RUN] the authors' `run_tecator.m` / `run_concrete.m` (they pass 16); [REPO] the authors' repo script `R/simulation/simulation_example.R` @3b95d66 (an ASI run on the S1 design, used only for the three run-length values and τ); code = `ASI_sampler.m` line (m.NN).

| # | Argument | Value | Source | Tag in `settings` |
|---|---|---|---|---|
| 1 | `data_fixed` | `zeros(n, 0)`: nothing forced in (the code adds its own intercept, m.67) | code m.1, m.53, m.67; not in [INS] or [RUN] | OURS |
| 2 | `data` | `scale(X)` | [INS] p.4; scaling: preprocessing above | see `preprocess` (OURS) |
| 3 | `target` | `y − mean(y)` | [INS] p.4; centring as [RUN] | see `preprocess` |
| 4 | `g` | 9 | [P] Sec 4.1 p.11 "V_γ = 9I" | author (S2: OURS) |
| 5 | `gprior` | 0 | [INS] p.4: 1 = g-prior, "Otherwise, an independence prior … V_γ = g I"; [RUN] 0 | author |
| 6 | `mode` | 1 | [INS] p.4: 2 stores the sampled models; [RUN] 1 | author |
| 7 | `RB_adap` | 1 | [RUN]; not used by the code (the name occurs on m.1 only) | author |
| 8 | `RB` | 1 | [RUN]; not used by the code (m.1 only) | author |
| 9 | `hparam` | 10/p | [P] Sec 4.1 p.11 "h = 10/p"; [INS] p.4: length 1 = fixed h | author (S2: OURS) |
| 10 | `tau` | 0.2 | [REPO] `target_prop = 0.2`; not stated in [P] Sec 4.1 ([RUN] 0.25; [P] Sec 4.3 0.234) | author, source "authors' repo …; not stated in the Biometrika text" (S2: OURS) |
| 11 | `nu` | 1 | [RUN]; [INS] p.4 "starting values of A and D"; start ζ = ν/(hp) = 0.1 (m.92-96) | author |
| 12 | `burnin` | 2000 | [REPO] `Nb = 2000` | author, repo source (S2: OURS) |
| 13 | `numbofits` | 4000 recorded per chain (6000 iterations in all) | [REPO] `N − Nb = 4000`; [INS] p.4 "total number of samples recorded for each multiple chain" | author, repo source (S2: OURS) |
| 14 | `thin` | 1 | [RUN] `num_thin = 1`; [REPO] has no thinning; [INS] p.4 "Every thin-th iteration is recorded after the burn-in period" | author |
| 15 | `numbofreps` | 25 chains | [REPO] `n_chain = 25`; [RUN] 25; [P] Table 1 p.12 reports 5 and 25 chains | author (S2: OURS) |
| 16 | `heat` | 1 | [INS] p.5 "The version without parallel tempering occurs if heat=1"; [RUN] 1 | author |
| 17 | `adap_type` | 1 | [RUN] 1; [INS] p.5 "if adap_type=1, there is infinite adaptation" (item 7c below) | author |
| 18 | `updateg` | 0: g stays fixed at 9 | code m.438 (g is resampled only if `updateg == 1`); [P] Sec 4.1 fixes g; not in [INS] or [RUN] | OURS |

Hard-coded in `ASI_sampler.m` and left as they are: κ = 0.0001 (m.160; the paper says 0.001, Sec 2.4 p.9), ε = 0.1/p (m.49-50), ζ step 2/it^0.55 after every chain's move (m.251), logit ζ kept in [−3, 3] (m.422-427), the lower bound through the expected number of changes (m.412-420), start γ_j ~ Bernoulli(h) (m.65).

**SuSiE.** `set.seed(method_seed); fit <- susieR::susie(X, y, L = 20)` on the preprocessed X and y; PIP = `fit$pip`. All other arguments are the `susie()` defaults (standardize, intercept, estimate residual and prior variance, residual variance bounded below by var(y)/1e4 and above by Inf, `max_iter = 100`, `tol = 1e-3`, `refine = FALSE`). L = 20 in every setting. `standardize = TRUE` and `intercept = TRUE` repeat what the preprocessing already did, so the PIPs equal those on the raw input (test: max difference below 1e-6).

All three never raise an R error: bad input or a broken set-up returns `selected = integer(0)`, `pip = NULL`, `extra$status = "failed: <msg>"`. Warnings are captured in `extra$warnings`. `extra$json_summary` is a flat list of scalars (iterations, burn-in, convergence info) for the small JSON record. Randomness comes only from `set.seed(method_seed)`.

## Prior per method

Each method runs under its own prior. There is no shared prior, so the three do not target the same posterior.

| Method | Coefficient prior | Model prior | Whose choice |
|---|---|---|---|
| BAS MC3 | `"ZS-null"`: Zellner-Siow Cauchy prior (a mixture of g-priors); flat intercept, p(σ²) ∝ σ⁻² | `beta.binomial(1, 1)`: inclusion probability ~ Uniform(0, 1), so uniform on the model size | `bas.lm` defaults (BAS 2.1.0); owner's option (A) |
| ASI | prior (1): flat intercept, p(σ²) ∝ σ⁻², independent β_γ ~ N(0, 9σ²I) | γ_j ~ Bernoulli(10/p), prior mean size 10 | authors: Griffin et al. 2021 Sec 2.1 p.3 and Sec 4.1 p.11 ("We use the prior in (1) with V_γ = 9I and h = 10/p"). In S2: the same values, OURS |
| SuSiE | each single effect N(0, σ0l²), σ0l² estimated; residual variance estimated | uniform 1/p per single effect; L = 20 single effects | `susie()` defaults; L = 20 is OURS (HQ ruling), citing Wang et al. 2020 Sec 4.2 p.16 |

## OURS flags and open decisions for the manager

1. **OURS-B1, BAS priors = the package defaults (owner's option (A)).** `bas.lm` is called without `prior`, `alpha` and `modelprior`; it then uses `"ZS-null"` and `beta.binomial(1, 1)`. Both are tagged "author" in both suites. BAS cannot express the ASI prior N(0, 9σ²I): every `bas.lm` prior has covariance ∝ (X_γ'X_γ)⁻¹. Alternative considered, owner chose (A): a call matched to the ASI prior. It stays reachable and is off by default: `ctrl = list(prior = "g-prior", alpha = 9 * (n - 1), h = 10/p)` (tagged OURS when used). On the strong S1-like test case both select the same 10 variables; Σ PIP is 13.49 under the defaults and 10.68 under the matched call (max PIP difference 0.145).
2. **BAS `thin = 1`, the `bas.lm` default.** Every MH step enters the PIP average. `thin = p` would leave only 180000/p recorded states (36 at p = 5000). `iid_se_at_pip_half` = sqrt(0.25 / 180000) ≈ 0.001 is a scale reference only: the true Monte Carlo error is larger because the states are autocorrelated.
3. **BAS `pivot = TRUE`, the `bas.lm` default.** `rank_deficient` is recorded. Memory at the ruled run length, one core: 3.2 GB peak for one fit at (n, p) = (1000, 5000); 2.7 GB peak for three successive fits in one process at (50, 1000). It is higher than under the earlier g-prior call (1.2 GB) because the visited models are larger.
4. **OURS-B4, BAS run length 120000 + 60000 (manager's latest ruling), and burn-in is not discarded.** The basis is the `alg_par` of the single-chain add-delete-swap run `ADS()` in the authors' repo script (`N = 180000` in total, `Nb = 60000` of them burn-in, l.48-49). The total is the same; the use of burn-in is not. The repo's ADS discards its first 60000 iterations and starts from γ_j ~ Bernoulli(h). BAS 2.1.0 (`src/lm_mcmc_grow.c`) runs `MCMC.iterations + burnin.iterations` = 180000 steps, starts at the null model and averages over every step from step 0. So the steps in which the chain is still climbing from the null model are part of every PIP. Run as shipped and recorded (`burn_in_discarded = FALSE`, `burnin_steps_in_average = 60000`). The `bas.lm` defaults would be 3 to 28 times longer (0.5M to 5.1M steps).
5. **BAS in S2 (p > n): the PIPs depend on the seed.** With the package defaults no warning is raised for n ≤ p. But on the two S2 test cases (n = 50, p = 1000) three method seeds on the same data gave Σ PIP = 10.91, 11.19, 10.14 (SNR 6; selections {1,2,4}, {1,2,4,821}, {1,2,4,821}; largest PIP range of one variable 0.43) and 0.46, 3.01, 22.54 (SNR 0.42; nothing selected in all three). On the S1-like case the three runs agree (Σ PIP 13.49, 13.47, 13.29; same selection). So in S2 a 180000-step chain from the null model has not converged under the uniform model-size prior. Reported, not changed.
6. **ASI run length, chains and τ from the authors' repo script (HQ ruling; tagged "author" in S1 with that source).** `burnin = 2000`, `numbofits = 4000`, `numbofreps = 25`, `tau = 0.2` are the `Nb`, `N − Nb`, `n_chain` and `target_prop` of `R/simulation/simulation_example.R` @3b95d66, an R run of ASI on the S1 design by a later paper's authors (Griffin is a co-author). The published Sec 4.1 (pp.11-13), the supplement, `instructions.pdf` and the two run scripts of the original code state no iterations, burn-in or τ for this simulation (the run scripts use τ = 0.25 and 100 + 200 iterations on two real data sets; Sec 4.3 p.14 used τ = 0.234 and 500 + 2500; Table 1 p.12 ran 5 and 25 chains). So these four values are not from the original code; `settings` says so in the source of each.
7. **OURS-A2, S1 settings transferred to S2 (HQ ruling).** The S1 settings are used unchanged in S2: V_γ = 9I, h = 10/p and the run settings for ASI; BAS uses the same package-default call in both suites. No ASI paper or script covers the Hastie design. In S2 the truth has s = 5 or 10 while the prior mean size is 10. The tag is per run: the harness passes `ctrl$suite`, and when it is "S2" the `settings` tags of ASI `g`, `hparam`, `tau`, `burnin`, `numbofits`, `numbofreps` are written as OURS. The suite never changes the fit.
7a. **OURS-A9, the two undocumented arguments.** `ASI_sampler.m` takes 18 arguments (m.1). `instructions.pdf` documents 15 (no `data_fixed`, no `updateg`; its printed call also omits `RB_adap`, which its list describes) and the two run scripts pass 16, so the shipped examples do not run against the shipped function. `data_fixed = zeros(n, 0)` and `updateg = 0` are set from the code (m.53, m.67, m.438) so that nothing but the code's own intercept is forced in and g stays fixed at 9, as Sec 4.1 has it.
7b. **OURS-P, preprocessing (HQ ruling b).** Scaling X and centring y is our step in all three adapters, tagged OURS. For BAS and SuSiE it does not change the posterior beyond rounding: `bas.lm` centres X itself and the Zellner-Siow prior does not depend on column scale; `susie()` standardizes and centres by default. For ASI the scale matters, because V_γ = 9I is not scale-invariant: the original code does not scale and its run scripts only centre. S1 and S2 draw X with unit population variances, so scaling changes each column by sampling error only (a factor within about ±7% at n = 500, ±20% at n = 50).
7c. **`adap_type = 1`, and the code against its manual.** `instructions.pdf` p.5: "adap_type=1, there is infinite adaptation. If adap_type=2, adaptation is restricted to the burn-in period". The code's test is `(adap_type == 1) || ((adap_type == 0) && (it < burnin))` (m.249): the burn-in-only value is 0, and with the documented 2 nothing adapts and the proposal probabilities are 0/0. Both run scripts use 1, and so does the adapter. With 1, ζ adapts in every iteration; π is the running mean of the Rao-Blackwellised conditional probabilities during burn-in and keeps being updated with the plain γ draws afterwards (m.259-261). The paper's Sec 4.3 p.14 says "Rao–Blackwellised updates of π were only calculated during the burn-in", which matches. `ctrl$adap_type = 0` gives burn-in-only adaptation (tagged OURS); 2 is refused.
7d. **κ = 0.0001 as hard-coded.** The paper says "We use κ = 0.001" (Sec 2.4 p.9); the code has 0.0001 (m.160) and it is not an argument. The file is not edited, so 0.0001 runs (owner's decision: the `.m` as it is). ε = 0.1/p agrees with the paper (m.49-50).
7e. **ASI seed.** The driver calls `rand("state", method_seed)` and `randn("state", method_seed)` before the sampler; "state" selects Octave's Mersenne Twister and initialises it from the scalar. The sampler draws with `rand` only (`randn` only when `updateg == 1`). The same seed gives identical PIPs (tested). MATLAB would give other draws from the same seed.
7f. **ASI cost under Octave.** In burn-in the code computes the Rao-Blackwellised probabilities with two interpreted `for j = 1:p` loops per chain move (m.305-311, m.331-348). Under Octave (no JIT) this is the whole cost: see "Test results" for the measured times and the grid estimate. It is a decision for the manager and HQ, not something the adapter may change.
7g. **A killed ASI run leaves nothing behind.** By default Octave writes its whole workspace (X, y, sampler state; 40 MB at p = 5000) to `octave-workspace` in the current directory when it receives SIGTERM or SIGHUP. The driver turns that off (`crash_dumps_octave_core(false)` and the two signal variants) before it reads anything; a killed run then returns `status = "failed: Octave run failed (exit 1): fatal: caught signal Terminated …"` and the adapter deletes its temporary directory. If the R process itself is killed, its `asi_octave_<pid>_*` directory stays under `ROOT/_local/tmp` and has to be removed by hand.
8. **OURS-S1, SuSiE L = 20 for all settings (HQ ruling; package default min(10, p)).** Wang et al. 2020 Sec 4.2 (p.16 of the Owls copy) used L = 20 in their 10-effect scenario and L = 10 in their 1-to-5-effect scenario. L is not set from s0: the adapter never sees s0, and choosing L by the true number of effects would give SuSiE oracle knowledge the other methods do not get. In the tests L = 10 and L = 20 selected the same sets. `ctrl$L` overrides (recorded).
8a. **SuSiE, paper vs this run (recorded, nothing changed).** Wang et al. ran susieR 0.4.29 (Sec 4.2 p.15); this is CRAN 0.14.2. Their displayed results fixed the prior variance at 0.1 var(y) and estimated σ² (Sec 4.2 p.16; they report similar performance when both are estimated); here both are estimated, the `susie()` default. The residual-variance bounds are the defaults var(y)/1e4 and Inf.
9. **OURS-S2, SuSiE scored by PIP > 0.5.** The authors report 95% credible sets, not a median probability model. The sets are stored in `extra$credible_sets` and not used.
10. **Threads.** R on Owls starts 80 OpenBLAS threads by default. `fit_bas_mc3` and `fit_susie` cap BLAS/OpenMP threads to `ctrl$threads` (default 1, max 4) through RhpcBLASctl; the cap stays in force for the rest of that R process. `fit_asi` sets `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS` and `MKL_NUM_THREADS` to `ctrl$threads` in the environment of the Octave process (Octave's OpenBLAS is a pthreads build and would otherwise use many cores). The harness should still export `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`.

## Original ASI code vs the PARNI R code

The full line-by-line comparison and the decision table the owner ruled on are in `ASI_DIFF.md`; this section is its summary. Original: `ASI_sampler.m` in `Version3.0.zip` from jimegriffin.github.io (lines "m.NN"); **this is what `fit_asi.R` runs**, unmodified, under Octave. PARNI repo: `R/sampler/ASI.R` (lines "r.NN"), run as shipped by `fit_asi_parni.R`, reference only.

**The same in both, and as in the paper**

| Item | Original | PARNI repo |
|---|---|---|
| Proposal, eq (9): independent flips, A_j = ζ min(1, π_j/(1 − π_j)), D_j = ζ min(1, (1 − π_j)/π_j); MH acceptance | m.165-234 | r.64-69, r.241-261, r.411 |
| π_j in burn-in: running mean of Rao-Blackwellised conditional inclusion probabilities, eq (10); chains share π and ζ | m.375-404, m.96, m.159 | r.376-378 |
| ζ adapted on the logit_ε scale towards τ, eq (11), with ε = 0.1/p | m.49-50, m.251 | r.387-388 |
| Prior (1): flat intercept, V_γ = gI, fixed h; marginal likelihood g^(−p_γ/2) \|X_γ'X_γ + I/g\|^(−1/2) A^(−n/2) | m.81-83 | `log_llh_ind_L` |
| Start: γ_j ~ Bernoulli(h) in every chain | m.65 | r.123 |
| PIP = plain mean of γ over the recorded draws of all chains (neither returns a Rao-Blackwellised PIP) | m.529, m.565 | r.310, r.460 |

**Different** (the last column is what the benchmark runs since the owner's decision)

| # | Item | Original MATLAB | PARNI repo | Paper | Runs now (`fit_asi.R`) |
|---|---|---|---|---|---|
| D-1 | κ | 0.0001, hard-coded (m.160) | argument; script 0.001 | 0.001 (Sec 2.4 p.9) | 0.0001, as hard-coded (item 7d) |
| D-2 | step φ_i for ζ | 2/it^0.55, after every chain's move, only when the proposal changes a variable (m.251) | it^−0.7, once per iteration, on the mean acceptance over chains; an empty proposal counts as accepted (r.261, r.333, r.386-387) | O(i^−λ), 1/2 < λ ≤ 1 (p.7) | original |
| D-3 | start value of ζ | ν/(hp), 0.1 if above 1 (m.92-95); 0.1 for ν = 1, h = 10/p | script: 0.5 | not stated for ASI | 0.1 (ν = 1) |
| D-4 | lower bound on ζ | E = ζ · 2Σ min(π_j, 1 − π_j); if E < 1, logit ζ ← logit ζ − log E (m.412-420) | Δ = 2Σ **max**(π_j, 1 − π_j) ≈ 2p; ζ ← 1/Δ if ζΔ < 1 (r.392-398); almost never binds | Δ = 2Σ min; ζ = 1/Δ if ζΔ < 1 (p.9) | original |
| D-5 | range of ζ | logit ζ clamped to [−3, 3], ζ in about [0.047, 0.953] (m.422-427) | no clamp on the logit; `logit_e` only raises ζ below 2ε to 2ε (its upper guard tests ζ > 2(1 − ε), which cannot happen); resets after the Δ step (r.400-405). ζ ended at 0.9998 in the S1 tests | (ε, 1 − ε) | original; ζ ended at 0.95, the clamp, in the S1-like tests |
| D-6 | adaptation after burn-in | with `adap_type = 1` (both run scripts): ζ keeps adapting, π keeps updating with the plain γ draws (m.249-261) | `full_adap = FALSE`: π frozen (r.374), ζ keeps adapting (r.386-388) | Sec 4.3 p.14: "Rao–Blackwellised updates of π were only calculated during the burn-in" | original with `adap_type = 1` (item 7c); `ctrl$adap_type = 0` stops all adaptation at the end of burn-in |
| D-7 | order of updates | π and ζ updated after each chain's move (m.143-144, m.403-404) | once per iteration, from per-chain cached values (r.295-299, r.377) | "independent parallel chains which share the same" adaptive parameters (p.7) | original |
| D-8 | κ in the bound; first move | κ applied in the proposal only (m.160 vs m.412); first proposal empty (π = 0/0) | κ-shrunk π in both (r.378, r.392); starts from π = h (r.63) | π̃ = κ + (1 − 2κ)π̂ in A, D | original |
| D-9 | scaling of X | none in the sampler; run scripts centre X and y | `make_hyper_par` scales X to unit sd and centres y | not stated | scaled and centred once, in the adapter (HQ ruling b); the scaling is OURS relative to the original |
| D-10 | run settings | scripts for Tecator and concrete data only: τ = 0.25, 25 chains, 100 + 200 iterations. **No Sec 4.1 script** | script (S1 design): τ = 0.2, 25 chains, 2000 + 4000 | Sec 4.3: τ = 0.234, 500 + 2500; Sec 4.1: 5 or 25 chains, nothing else | τ = 0.2, 25 chains, 2000 + 4000, from the repo script (HQ ruling, item 6) |

So the original code states no run length and no τ for the Sec 4.1 experiments. HQ's ruling takes both, and the 25 chains, from the repo script. The original zip's run scripts call `ASI_sampler` with 16 arguments while its `ASI_sampler.m` takes 18 (`data_fixed` first, `updateg` last); `instructions.pdf` documents a 15-argument form. The scripts therefore do not match the sampler they ship with; the adapter passes all 18 (table under "Protocol").

## Other places where the code that runs differs from its documentation

| Item | Paper or manual | Code that runs |
|---|---|---|
| ASI marginal likelihood exponent | prior (1) with a flat intercept and p(σ²) ∝ σ⁻² gives −(n − 1)/2; the paper's printed Bayes-factor formulas (Sec 2.4 pp.8-9) have −n/2 | repo `log_llh_ind_L` and the original MATLAB code: −n/2, as printed |
| ASI `RB` argument | `instructions.pdf` p.5: `prob_inclusion` is the "Rao-Blackwellised estimate if RB=1 or an empirical average otherwise" | `RB` and `RB_adap` occur only on line 1 of `ASI_sampler.m`; `prob_inclusion` is always the plain mean of γ (m.529, m.565) and `prob_inclusion2` is zeros |
| ASI `adap_type` | `instructions.pdf` p.5: 2 = "adaptation is restricted to the burn-in period" | the code tests 1, or 0 with `it < burnin` (m.249); 2 adapts nothing (item 7c) |
| ASI κ | paper Sec 2.4 p.9: "We use κ = 0.001" | `ASI_sampler.m` m.160: 0.0001 (item 7d) |
| ASI argument count | `instructions.pdf`: 15 arguments; `run_tecator.m`, `run_concrete.m`: 16 | `ASI_sampler.m` m.1: 18 (item 7a) |
| BAS burn-in | `?bas.lm`: "Number of burnin iterations" | not discarded (item 4) |

## Test results (Owls, 2026-11-25, one core per process, nice 19)

`test_bayesian.R`, final files: 0 failed checks. Quick run (`--only=<m>`): BAS 74, ASI 88, SuSiE 65 checks passed (`.rc_tmp/fableB/logs/o1_bas_mc3.log`, `o2_asi_quick.log`, `o1_susie.log`). One short ASI fit through `harness/run_one.R` (S2_001, rep 1, output to scratch): status ok, tags written as in suite S2. `--full` on the option (A) state: BAS 87, SuSiE 78 (`r6_*.log`). ASI at its default length was run case by case (`--long --cases=…`, `--full --cases=…`; 0 failed). Run times vary with machine load by up to a factor of two.

ASI checks that are specific to the Octave route (all pass): the sampler file has the pinned sha256 in both copies; the driver's call is the 18-argument signature of line 1; `asi_octave/` holds only `run_asi.m`; the adapter's PIPs are identical to a direct Octave call of `ASI_sampler(zeros(n,0), scale(X), y − mean(y), 9, 0, 1, 1, 1, 10/p, 0.2, 1, 100, 200, 1, 25, 1, 1, 0)` with the same seed; `nargin('ASI_sampler')` = 18; **determinism: the same `method_seed` in two separate Octave runs gives identical PIPs, final ζ and acceptance rate**; a different seed gives different draws; an edited copy of the sampler is refused, a byte-identical copy elsewhere runs; missing Octave, sampler or temporary root, `adap_type = 2` and p = 8 return `failed: …` without an R error; no temporary directory is left.

| Case | BAS MC3 (package defaults, 180000 steps) | ASI (`ASI_sampler.m` under Octave, 2000 + 4000 iterations, 25 chains) | SuSiE |
|---|---|---|---|
| S1-like n=200 p=500 ρ=.6 SNR=3 | 6.3 s, exact support, Σ PIP 13.49 | 928.8 s, exact support, Σ PIP 10.80, acceptance 0.72, final ζ 0.952 (the clamp), R-hat 1.000 | 0.5 s, selects {10} only |
| S1-like n=200 p=500 SNR=0.5 | 2.1 s, none, Σ PIP 0.55 | demo length only (100 + 200): 50.3 s, none, Σ PIP 1.16 | 0.4 s, none |
| S2 hi-5 n=50 p=1000 ρ=.35 SNR=6 | 12.5 s, 3 TP 0 FP, Σ PIP 10.91 | 1726.5 s, 3 TP 4 FP: selects {1,2,4,54,672,755,821}, Σ PIP 11.05, acceptance 0.13, final ζ 0.085, R-hat 1.04, 4 PIPs in (0.4, 0.6) | 1.7 s, 1 TP |
| S2 hi-5 n=50 p=1000 SNR=0.42 | 4.9 s, none, Σ PIP 0.46 | demo length only (100 + 200): 85.2 s, none, Σ PIP 1.93 | 0.4 s, none (all PIP = 0) |
| S1 full n=1000 p=5000 SNR=2 | 24.4 s, exact support, Σ PIP 11.43, 3.2 GB (single-fit probe) | 10266 s (2.85 h), exact support, Σ PIP 10.30, largest null PIP 0.009, acceptance 0.30, final ζ 0.953 (the clamp), R-hat 1.000 (run as the one-core user unit `fableB-asi-full`, log `.rc_tmp/fableB/logs/o2_asi_full_default.log`; a first run was killed by a server restart at burn-in iteration 1340 after 6275 s). Demo length (100 + 200): 459.6 s, exact support, Σ PIP 10.30, acceptance 0.32, Octave process 0.11 GB | 14.9 s, 6 TP 0 FP, 0.50 GB |

ASI at the demo length of the authors' run scripts (100 + 200 iterations, 25 chains; used by the quick test): S1-like SNR 3: 51.3 s, exact support, Σ PIP 10.75; S2 SNR 6: 85.8 s, 3 TP 1 FP, Σ PIP 6.35.

**Where the ASI time goes.** Octave start-up plus file transfer is 0.3 to 0.7 s per fit; the rest is the sampler. Almost all of it is burn-in: each burn-in chain move runs two interpreted `for j = 1:p` loops for the Rao-Blackwellised probabilities (m.305-311, m.331-348), about 34 µs per variable per chain move in Octave 10.3.0. Measured per burn-in iteration (25 chains): 0.46 s at p = 500, 0.8 s at p = 1000, 4.4 to 5.2 s at p = 5000 (depending on machine load). After burn-in an iteration costs about 0.03 s at p = 500. So a default-length fit costs about 1.7 to 2.1 s × p: 15 min at p = 500, 29 min at p = 1000, 2.85 h measured at p = 5000 (n = 1000). The Octave process uses about 0.1 GB. Even a 40 × 30 problem takes 215 s at the default length.

**ASI in S2 depends on the seed, as BAS does.** The S2 SNR-6 data, method seeds +0 and +1, default length (scratch script `.rc_tmp/fableB/probe/probe_asi_s2_seed.R`): selections {1,2,4,54,672,755,821} and {1,2,4,54,672,755,821,825}; Σ PIP 11.05 and 11.30; R-hat 1.040 and 1.027; acceptance 0.130 and 0.138; final ζ 0.085 and 0.087. The largest PIP difference is 0.236 (variable 54: 0.555 against 0.792); five variables differ by more than 0.1; one crosses 0.5 (variable 825: 0.49 against 0.51). The true support is {1,…,5}; variables 3 and 5 have PIP below 0.03 in both runs. The seed +0 run, made in a separate process, reproduced the test run's numbers exactly. The PARNI adapter on the same data selected {1,2,4,54,755,821} and {1,2,4,54,755,821,825} in the earlier round (table below). Both codes and both seeds put high PIP on the same null variables (54, 755, 821), so this looks like the posterior under this prior at n = 50, with Monte Carlo noise on top, and not an adapter fault.

**The original code against the PARNI R code on the same data** (harness data S1_03, n = 500, p = 500, SNR 2, rep 1; both at 2000 + 4000 iterations, 25 chains, τ = 0.2; scratch script `.rc_tmp/fableB/probe/probe_cmp_parni_vs_m.R`):

| | Original `.m` under Octave | PARNI R `ASI()` |
|---|---|---|
| Selection (two seeds each) | {1,…,10} = the true support, both seeds | the same, both seeds |
| Σ PIP | 10.368, 10.367 | 10.368, 10.367 |
| Largest null PIP | 0.024 (variable 90) | 0.024, 0.025 |
| max abs(ΔPIP), seed to seed, same code | 0.0009 | 0.0012 |
| max abs(ΔPIP), `.m` against PARNI (four seed pairs) | 0.0006 to 0.0019 | |
| Acceptance rate; final ζ | 0.48; 0.952 (clamp) | 0.65; 0.9998 |
| R-hat of the log posterior | 1.000 | 1.000 |
| Wall time, one core | 971 s and 1182 s | 77 s and 77 s |

On this S1 cell the two codes give the same PIPs to within Monte Carlo error: the code-to-code difference is no larger than the seed-to-seed difference of either code. The differences D-1 to D-10 change the tuning (ζ, acceptance rate), not the result here. The original under Octave is 13 to 15 times slower. One data set at one S1 setting; it says nothing about S2, where both codes mix poorly (PARNI adapter on the S2 SNR-6 case: 3 TP 3 FP, R-hat 1.03; the original: next paragraph and the table above).

Earlier PARNI-adapter results on the five cases above (round r5, τ = 0.2; reference only): 101.9 s exact, Σ PIP 10.81; 66.8 s none, 1.21; 78.7 s, 3 TP 3 FP, 10.19, acceptance 0.12, R-hat 1.03; 104.2 s none, 2.29; full size 349.5 s, exact, 10.29, 0.39 GB.

The next table is from an earlier round (PARNI adapter with τ = 0.234) and is kept for reference only.

Side check of the original MATLAB code's tuning values (`ctrl = list(kappa = 1e-4, init_zeta = 0.1, phi_prop = -0.55)`, item 7d; scratch script `.rc_tmp/fableB/probe/probe_asi_orig.R`, full-length runs), against the default and against the default with another seed:

| Case | Default | Default, second seed | Original code's κ, ζ start, exponent |
|---|---|---|---|
| S1-like n=200 p=500 SNR=3 | exact support, Σ PIP 10.81, acceptance 0.65 | exact support, 10.80, 0.65; max PIP difference from default 0.003 | exact support, 10.81, 0.88; max PIP difference from default 0.001 |
| S2 hi-5 n=50 p=1000 SNR=6 | {1,2,4,54,755,821}, Σ PIP 11.24, acceptance 0.17, R-hat 1.11 | {1,2,4,54,755,821,825}, 11.72, 0.18, 1.06; max PIP difference 0.147 | {1,2,4,54,755,821}, 11.71, 0.22, 1.08; max PIP difference 0.096 |

In both cases the change from these three values is no larger than the seed-to-seed change. This checks only the three values that the repo exposes; it says nothing about D-2 (factor 2, per-chain steps), D-4, D-5 or D-6, which cannot be set.

BAS and SuSiE were also run once through `harness/run_one.R` (setting S2_001, rep 1, output to scratch) in the first round: status ok; not repeated since (their interface did not change). The Octave ASI adapter was run through it after it was built (above).

Observations worth knowing before the smoke gate:
- SuSiE misses most of the 10 adjacent, sign-alternating S1 signals at n = 200 (it selects one variable; `refine = TRUE` does not change this). At n = 500 and n = 1000 with p = 500, SNR 3, it recovered all 10 in a side check; at n = 1000, p = 5000, SNR 2 it found 6 of 10. This is the method at its defaults, not an adapter fault.
- BAS in S2 is seed-dependent at this run length (item 5).
- BAS under its defaults has a larger posterior expected model size than ASI's prior gives (Σ PIP 13.5 against 10.8 on the strong S1-like case): the two priors differ (table "Prior per method").
- ASI in S1 ends with ζ at the code's upper clamp (0.952) and an acceptance rate of 0.5 to 0.7 at p = 500, far above τ = 0.2: the target is not reachable there, in the original code as in PARNI. In the S2 SNR-6 case ζ falls to 0.09 and the acceptance rate stays below the target (0.13).

Rough cost of the 100-seed grid (not launched here), from the single fits above on a loaded machine: BAS 2 to 7 s (p = 500), 5 to 25 s (S2, p = 1000), 24 s (p = 5000), so near 50 core-hours for 13,600 fits, with up to about 3 GB per fit; SuSiE under 2 s to 15 s, near 10 core-hours. Treat these as ±50%.

**ASI under Octave is the expensive method: about 8,000 core-hours for the grid.** S1: 800 fits at p = 500 × 15 min ≈ 200 h, and 800 fits at p = 5000 × 2.85 h ≈ 2,300 h (measured at n = 1000 only; the n = 500 cells were not timed). S2: 12,000 fits at p = 1000 × 29 min ≈ 5,700 h. With 40 Owls cores that is 8 to 9 days. The cost is the burn-in of the unmodified code under an interpreter; MATLAB compiles such loops and would probably run the same file much faster (not measured; MATLAB is not available on Owls, and NOTS is excluded). The only levers that leave the file untouched are run settings (`burnin`, `numbofreps`), and those are the owner's to change: cost is proportional to `burnin × numbofreps × p`. This is reported for a decision; the adapter runs the ruled settings.

## Sources read

| Source | Read as | What it fixes |
|---|---|---|
| Griffin, Łatuszyński & Steel 2021, Biometrika 108(1):53-69, DOI 10.1093/biomet/asaa055 | the published article, supplied by the owner (`_local/papers/Benchmark_methods/Griffin_Latuszynski_Steel_2021_Biometrika_published.pdf`; PDF pages 1-17, journal page = 52 + PDF page; pages below are PDF pages). The arXiv v3 copy read first is superseded | Sec 2.1 p.3 prior (1); Sec 2.2 p.7 multiple chains, φ_i = O(i^−λ); Sec 2.4 pp.8-9 ASI, eqs (9)-(11), Algorithm 2, ε = 0.1/p, κ = 0.001; Sec 4.1 pp.11-13 prior V_γ = 9I, h = 10/p, 5 or 25 chains (Table 1 p.12), no run length or τ; Sec 4.3 p.14 τ = 0.234, 500 + 2500 iterations, RB updates in burn-in only, PIP by posterior mean of γ |
| Liang, Livingstone & Griffin 2022, Stat. Comput. 32:84, DOI 10.1007/s11222-022-10137-8 | PDF on Owls (`Core_bibliography/01_2022_...pdf`) | Sec 5.1: V_γ = I, g = 9, h = 10/p, 25 chains, adaptation ends with burn-in, 15-minute runs |
| The-PARNI-scheme repo @ 3b95d669 | clone | `README.md`, `R/make_hyper_par.R`, `R/sampler/ASI.R`, `R/sampler/other_supportive_functions.R`, `R/simulation/simulation_example.R`; source of ASI's run length, chains and τ; the R sampler itself is reference only |
| Griffin et al. 2021, supplementary material | `Griffin2021_supplement/Supplementary_1_4_20.pdf` (22 pages) | Sec 5.1 pp.9-10, Sec 5.2 p.10; no Sec 4.1 run settings |
| Griffin et al.'s original code, `Version3.0.zip` (jimegriffin.github.io; identical to the owner's supplement copy) | `ASI_sampler.m` in full (587 lines), `run_tecator.m`, `run_concrete.m`, `instructions.pdf` (5 pages); the other files by search only | **the ASI code that runs**; argument list and meaning (`instructions.pdf` pp.4-5), the example calls, the hard-coded ε, κ, step size, start values, the PIP estimator, no scaling |
| Clyde, Ghosh & Littman 2011, JCGS 20(1):80-101, DOI 10.1198/jcgs.2010.09049 | authors' preprint on Owls (`Core_bibliography/27_2011_...pdf`; preprint page numbers) | Sec 4 pp.14-15 MC3 and Random-Swap (RS), g-prior g = n, uniform model prior; Sec 4.2 p.16 RS-Thin |
| BAS 2.1.0 | `?bas.lm`, `?Bernoulli`, R and C source | defaults, `thin`, `pivot`, how burn-in and thinning are handled |
| Wang, Sarkar, Carbonetto & Stephens 2020, JRSS-B 82(5):1273-1300, DOI 10.1111/rssb.12388 (preprint DOI 10.1101/501114) | PDF on Owls (`Core_bibliography/29_2020_...pdf`, paged 1-28) | Sec 3.2.1 p.12 PIP; Sec 3.3 p.12 choice of L; Sec 4 p.13 scenarios; Sec 4.2 p.16 L = 10 / L = 20 |
| susieR 0.14.2 | `?susie`, vignettes `mwe`, `finemapping` | defaults; L = 10 in the vignettes, "no harm" in overstating L |
| McCreight et al. 2025 (SuSiE 2.0) | PDF on Owls | read; not applicable to CRAN susieR 0.14.2 |

## Missing papers (not guessed)

None now. The supplementary material of Griffin et al. (2021), the last missing item, was supplied by the owner on 2026-11-25 (`_local/papers/Benchmark_methods/Griffin2021_supplement/Supplementary_1_4_20.pdf`, 22 pages, sha256 `55340f5c…43274`) and read. It contains proofs, the Rao-Blackwellised estimate, parallel tempering, Sec 5.1 (pp.9-10: Tecator, Boston, concrete and protein data, "run for the same amount of time", 200 runs) and Sec 5.2 (p.10: extra figures for Sec 4.3). It states no iteration count, burn-in or τ for the Sec 4.1 simulation. So no author source (paper, supplement, original code) gives the Sec 4.1 ASI run length or τ.

The owner's supplement folder also holds the original code: `Code_For_Paper.zip` has the same sha256 as the website `Version3.0.zip` (`ce3e9c75…460f42`), and all 10 files of `code/Version3.0/` are sha256-identical to the website copy in `_local/engineering/ext/griffin_asi_original/Version3.0/`.

Clyde et al. (2011) was read as the authors' preprint, so its page numbers are preprint pages; the content needed (Sec 4, Sec 4.2) is there.

## ctrl options (all recorded in `settings`, tagged OURS when used)

`suite` ("S1" default, "S2") comes from the harness; it sets author/OURS tags only (ASI) or is recorded only (BAS, SuSiE). Unknown fields such as the harness's `setting_id` are ignored.

| Adapter | Options |
|---|---|
| `fit_bas_mc3` | `suite`, `prior`, `alpha`, `h`, `thin`, `pivot`, `MCMC.iterations`, `burnin.iterations`, `threads`, `rlib` |
| `fit_asi` | `suite`, `g`, `h`, `tau`, `nu`, `burnin`, `numbofits`, `thin`, `numbofreps`, `adap_type` (0 or 1), `threads`, `octave_home`, `sampler_dir` (sha256 is checked), `driver`, `tmp_root`, `keep_tmp` |
| `fit_asi_parni` (not registered) | `suite`, `g`, `h`, `N`, `Nb`, `n_chain`, `target_prop`, `kappa`, `init_zeta`, `phi_prop`, `threads`, `repo`, `rlib` |
| `fit_susie` | `suite`, `L`, `max_iter`, `threads`, `rlib` |

## How to run the test

```
cd Experiments/S1S2/benchmarks/bayesian
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 19 Rscript test_bayesian.R [--only=bas_mc3|asi|susie] [--full] [--long] [--cases=<regex>]
```

Exit status 0 means every check passed. The quick `--only` runs take about 3 minutes (BAS), 8 minutes (ASI: demo-length fits plus one default-length fit on a 40 × 30 problem) and 1 minute (SuSiE). For ASI, `--long` runs the SNR-3 and SNR-6 cases at the default length (15 and 29 minutes) and `--full` adds the n = 1000, p = 5000 fit (about 3 hours); `--cases=<regex>` runs section 1 for the matching cases only, e.g. `--only=asi --long "--cases=S2.*SNR=6$"`.
