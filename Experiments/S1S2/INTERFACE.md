# S1/S2 harness: interface contract (v2 manager, 2026-11-25). Binding for every builder.

Goal (owner via HQ): run S1 and S2 at every setting with 100 seeds per setting, for SMC-BVS and the 5 approved benchmarks. The output is successes/100 per setting and method. **The 100-seed grid needs the owner's GO per suite and method. GIVEN 2026-11-25 for S1 × SMC-BVS only (NOTS); benchmarks and S2 still need a GO.** Compute (updated 2026-11-25, owner decisions HQ_DECISIONS b5548635 / 0b241b1d): the Owls-only rule is deleted. The S1 100-seed SMC-BVS run goes on NOTS (Slurm arrays, `slurm/`, inside the single NOTS tree, POLICIES §8). Owls work: nice -n 19, within the Owls core cap (POLICIES rule 5), and stay lean.

## Owner rules (all builders and reviewers)
1. ZERO execution failures. Each benchmark follows its author's algorithm exactly, using the author's own software: glmnet, ncvreg, BAS, the PARNI-scheme GitHub repo (ASI) and susieR. Never reimplement anything the author ships. Use the author's recommended defaults and the tuning the source paper describes.
2. Read the sources first: the method paper (for ASI, also Griffin, Łatuszyński & Steel 2021) and the GitHub repo or CRAN docs and vignettes, including the repo's run scripts. For ASI, replicate how Griffin et al. ran it in their Sec 4.1 experiments, and pin the repo commit.
3. Every script starts with a PROVENANCE block: paper (DOI and section), software and version or commit, and each setting with its source. Anything not taken from the author is marked **OURS**.
4. Reviews check fidelity to the author's algorithm and defaults, not only that the code runs.
5. If a paper is needed but paywalled or unfetchable, do NOT guess. Give the manager the exact list (title, authors, year, DOI). Papers already on Owls (check here first):
   - `/home/fb31/Bayesian-Variable-Selection/_local/papers/` (Benchmark_methods: glmnet 2010, Tibshirani 1996; Core_bibliography: Liang–Livingstone–Griffin 2022 PARNI, Clyde–Ghosh–Littman 2011 BAS, McCreight 2025 SuSiE 2.0, Barbieri 2021 MPM, …)
   - `/home/fb31/Bayesian-Variable-Selection/_local/theory/BENCH_DESIGN/papers/` (BVS_Griffin2021.pdf, Hastie2020.pdf, BVS_SuSiE2020.pdf, BrehenyHuang2011.pdf) and `.../BENCH_DESIGN/{notes,SCHEMA.md}`
   - `/home/fb31/Bayesian-Variable-Selection/_local/theory/BENCH_METHODS_papers/` (Ormerod–You–Müller 2017, …)
   - arXiv versions are fine to fetch.

## Folder tree (repo: worktree /home/fb31/BVS-wt/P1M, branch exp/P1M; ONLY the manager commits)
```
Experiments/S1S2/
  INTERFACE.md                 this file
  specs/SPEC.md                every setting with its citation; flagged OURS choices in the first lines; engine version
  specs/settings.tsv           one row per setting (136): setting_id, suite, cell, n, p, s0, rho, snr, nu, beta_type, sigma2_rule, citation
  harness/generate.R           gen_data(setting_row, rep) -> list(X, y, beta, support, sigma2, data_seed, meta)
  harness/run_one.R            Rscript run_one.R --method M --setting ID --rep R [--out DIR]
  harness/methods.R            registry: method name -> adapter file + fit function
  harness/smoke.R              the gate: every method x 6 combos x 1 seed; writes smoke_table.tsv
  harness/aggregate.R          successes/100 per setting x method (for later)
  harness/paired.R             paired SMC-BVS vs benchmark tables (same data_md5; McNemar, Hamming sign test)
  harness/records.R            record reader shared by aggregate.R and paired.R (identity / duplicate checks)
  smc/fit_smcbvs.R             SMC-BVS adapter (manager's team)
  benchmarks/frequentist/fit_lasso_cv.R, fit_scad.R          (Fable-F)
  benchmarks/bayesian/fit_bas_mc3.R, fit_asi.R, fit_susie.R   (Fable-B; vendored PARNI code is NOT copied into git: clone it to _local, pin the commit)
```
Run outputs, package libraries and clones never go in git. They go to `ROOT=/home/fb31/Bayesian-Variable-Selection/_local/engineering/`:
- `runs/S1S2/<method>/<setting_id>/rep_<RRR>.{rds,json}`
- the R library `Rlib/` (`.libPaths(c("/home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib", .libPaths()))`; install there, pinned versions recorded)
- external repos `ext/<repo>@<commit>/`

## Seeds (deterministic, documented)
- `data_seed = 500000000 + 1000000*suite + 1000*cell + rep`, with suite ∈ {1, 2}, cell = 1..16 (S1) or 1..120 (S2), rep = 1..100. This is the EXPERIMENT_PLAN §2 formula.
- `method_seed = data_seed + 10000000*method_code`, with method_code: smcbvs 1, lasso_cv 2, scad 3, bas_mc3 4, asi 5, susie 6.
- An adapter must make its randomness (CV folds, MCMC) depend only on method_seed: call `set.seed(method_seed)` (RNGkind default Mersenne-Twister, Inversion, Rejection), or pass method_seed through to the method's seed argument.

## Adapter signature (every method)
```r
fit_<method>(X, y, method_seed, ctrl = list()) ->
  list(selected   = <integer vector, 1-based column indices, sorted>,
       pip        = <numeric length p, or NULL for frequentist>,
       runtime_sec= <elapsed wall seconds of the fit only>,
       software   = <list(name=, version= or commit=)>,
       settings   = <named list of every tuning value actually used, each tagged "author" or "OURS">,
       extra      = <method-specific list: e.g. lambda path choice; BAS/ASI/SuSiE chain or convergence info>)
```
X is n×p, numeric, unstandardized as generated. y is length n. No intercept column; the generators give mean-zero designs and no intercept, and each adapter does whatever its author does (glmnet standardizes and fits an intercept by default, etc.). An adapter MUST NOT error. On a method-level failure it returns `selected = integer(0)`, `extra$status = "failed: <msg>"`, and the harness counts it as a failure. The smoke gate requires zero failures.

Selection rule (OURS, flagged in SPEC): frequentist methods select the nonzero coefficients at the author's recommended λ (lasso: `lambda.min` vs `lambda.1se`, flagged as OURS with a reason; SCAD: the CV choice per ncvreg docs). Bayesian methods select the median probability model, PIP > 0.5.

## Per-run record (written by run_one.R)
json (small) + rds (full). Fields:
- setting_id, suite, cell, rep, method, data_seed, method_seed, n, p, s0, true support;
- selected, |selected|, TP, FP, FN, success = (selected == support exactly) (OURS);
- runtime_sec, host, R version, software/version, settings;
- pip (Bayesian), plus extra.
- For smcbvs, also: PIPs, top models with weights (≥ 20), log-evidence estimate, ESS per stage, N particles, engine tag.
