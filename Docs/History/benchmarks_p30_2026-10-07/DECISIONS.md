# Decision log — benchmark campaign, methods 3 (exact best subset + BIC), 5 (SuSiE), 6 (PARNI)

Every entry: date, decision, the source it follows, why. Later entries supersede earlier ones.
Scope statement from the user (2026-10-07): first round of competitor simulations to learn which benchmarks
SMC-BVS has to beat; the architecture may be revised afterwards; every step must be traceable.

## 2026-10-07 — scope and sources

- **Authoritative spec**: `Methodology/SMC_Composite_Likelihood_Methodology.tex`, Sections "Simulation
  scenarios" (S1–S6, seeds) and "Benchmark methods" (six benchmarks, comparison conventions). It supersedes
  the eight-method list discussed on 2026-10-06.
- **Primary sources read in full** (copies in `tmp/pdfs/benchmark_refs_20261007/` and the project's `Papers/`):
  Hocking & Leslie 1967 (Technometrics 9:531); Furnival & Wilson 1974 (Technometrics 16:499); Schwarz 1978
  (Ann. Statist. 6:461); Wang, Sarkar, Carbonetto & Stephens 2020 (JRSS B 82:1273); Liang, Livingstone &
  Griffin 2022 (Stat. Comput. 32:84, arXiv:2110.11747) plus their reference code
  (github.com/XitongLiang/The-PARNI-scheme, cloned to `tmp/external/parni_ref_20261007/`).
- **Language**: R, as the frozen SMC engine. The three methods and the shared layer are R; no Python.

## 2026-10-07 — data and shared layer

- **Seeds**: methodology rules, `s_kr = 108000 + 1000 (k-1) + r` (S1–S5), `s_6r = 107000 + r` (S6).
  Replicates `r = 1..100` in every scenario including S6 (the methodology documents 200 for the historical S6
  campaign; this campaign uses 100 per the user's "100 seeds per benchmark").
- **Data generation**: the engine recipe, call order preserved; verified bitwise identical to Experiment 1
  (S1–S5) and to the heterogeneous_1v1 campaign (S6) by `data/scripts/tests/test_common.R`.
- **Exact reference**: computed once per dataset in the data stage with the frozen engine's compiled
  enumerator (all 2^30 models), stored in `data/exact/`, fingerprint-bound to the dataset. Methods read it only
  after fitting. Reason: PIP error for PARNI/SuSiE and the "exact decision" columns for every method need it;
  computing it once avoids six repeats of an 8-minute job.
- **Frozen engine**: byte-identical copy of `Others/1_Latest_work_cycle1_and_next/scripts/engine/` (01–04 .R and
  `exact_reference.cpp`), hashes in `data/scripts/engine/SHA256SUMS`, same hashes as Experiment 1.
- **Decision rule shared by PIP methods**: `{j : PIP_j > 0.5}` (strict), the engine's MPM convention.
- **Result contract**: `data/scripts/common/03_bench_contract.R`; one row schema for all six methods
  (`02_evaluate.R`), so Lasso / elastic net / SSL can be added without touching the evaluation.

## 2026-10-07 — method 3: exact best subset with BIC

- **Search**: `leaps::regsubsets(method = "exhaustive", intercept = FALSE, nvmax = 30, nbest = 1)`, the
  Furnival–Wilson leaps-and-bounds (exact RSS optimum per size). No size cap (`nvmax = p`), so the BIC minimum is
  the unrestricted optimum; `kmax_used = 30` is still recorded as the methodology asks.
- **Criterion**: `BIC(k) = n log(RSS_k/n) + k log n`, k = 0..30, empty model eligible, ties to smaller k.
  Source: methodology formula; Schwarz 1978 (penalty ½ k log n on the log-likelihood).
- **Verification per dataset** (recorded in the row): RSS recomputed by QR vs leaps (1e-8); sizes 1..6
  re-solved by an independent exact enumeration; single-swap optimality at every size; monotone RSS path.
  Lineage: `heterogeneous_1v1/scripts/benchmarks/best_subset.R`, reduced to the single BIC rule
  (EBIC and size-oracle rows dropped: not in the methodology).

## 2026-10-07 — method 5: SuSiE

- **L = 10**: Wang et al. Sec. 4.2 used L = 10 on 1–5 true effects; Sec. 3.3 shows robustness to
  overstating L. Our truths have 5 or 6 signals; L is not derived from them.
- **Variances**: residual variance and per-effect prior variances estimated (susieR defaults; paper Sec.
  3.1.3 and 4.2). Initial `scaled_prior_variance = 0.2` (susieR default).
- **Credible sets**: coverage 0.95, purity `min_abs_corr = 0.5` (paper Sec. 3.2.2). Recorded as a separate
  outcome; never used for the point selection.
- **No intercept, no re-standardisation**: methodology; X is already standardised by the generator. susieR's
  documentation calls `intercept = FALSE` "not recommended" in general; here it is mandated by the design.
- **Variants**: `paper` = IBSS as published (`refine = FALSE`, the primary row); `refine` = susieR's later
  refinement step against poor local optima (`refine = TRUE`), kept as a tuning sensitivity, not an extra benchmark.
- **Prior expectation from cycle 1** (`DESIGN_AND_BENCHMARKS.md`): on the S4-type design SuSiE recovered the
  support in 0/100 datasets because the opposite-sign pair (2, 3) is invisible to single-effect regressions.

## 2026-10-07 — method 6: PARNI

- **Target**: the control posterior of the methodology, through the engine's `log_marginal_likelihood()` and
  `log_model_prior()`. The authors' code supports only a g-prior or an independent prior with an improper
  σ² prior and centred y, so it cannot target this posterior; the sampler mechanics were ported instead
  (`Benchmarks/PARNI/scripts/parni.R`, header documents the mapping to the paper's equations).
- **Adaptation**: Kiefer–Wolfowitz for ω (paper: PARNI-KW "generally performs better" than RM; recommended in
  the discussion), `a_i = i^-1`, `c_i = i^-0.5`, ε-logit with `ε = 0.1/p`; Rao-Blackwellised PIPs for the
  neighbourhood (reference `use_rb = TRUE`), floor/ceiling `κ = 0.001`.
- **Balancing function**: Hastings `min(1, t)` (used throughout the paper's Sec. 5).
- **Chains / iterations**: 25 chains sharing the adaptive parameters (paper Sec. 5); `N = 3000`, `Nb = 1000`
  (the authors' published example script `R/simulation/simulation_example.R`).
- **Adaptation stops at burn-in** for both π and ω (paper Sec. 5: "all the adaptations terminate after the
  period of burn-in"; the reference code keeps adapting ω — we follow the paper's text; after burn-in every
  chain uses the centre ω). Recorded in `extra$adapt_after_burnin = FALSE`.
- **Estimates**: plain PIP (post-burn-in average of γ; the reference's `estm_PIPs`) drives the shared
  decision rule; Rao-Blackwell PIP (post-burn-in average of the conditional inclusion probabilities) reported
  alongside, mirroring the SMC rows (plain vs RB).
- **Repeats**: 5 independent runs per dataset, seeds `s + 300000 + 1e6 (m-1)`, for the run-to-run
  variability the methodology asks for.
- **Validation**: toy p = 8 vs exact enumeration, plain MAE 0.0066 / RB MAE 0.0042 (quick run);
  S1 r001 at p = 30 vs the exact 2^30 reference, plain MAE 5.5e-4 / RB MAE 1e-5 in 21 s per repeat.

## 2026-10-07 — deployment

- **Layout** (user's screenshot of NOTS): `~/projects/BVS/data/` (shared datasets + exact references) and
  `~/projects/BVS/Benchmarks/<Exact_best_sub|SuSIE|PARNI|Lasso|Elastic_net|SSL>/`. Laptop mirror:
  `Experiment/Experiment_ 2/`.
- **Gate**: code may be copied to NOTS and smoke-tested there; the production arrays are submitted only on
  the user's explicit go.

## 2026-10-07 (evening) — integration with the shared framework found on NOTS

- **Finding**: `~/projects/BVS` was not empty. Another agent had built, on Oct 4–7, a shared benchmark framework
  (`Benchmarks/shared/`, `slurm/`, `tests/`, sealed `data/` with SHA-256 manifests, `data_S6/`, `library_portable/`)
  and the Lasso, elastic-net and SSL methods, and was running their smoke jobs. Its datasets are bitwise the values my
  generator produces (checked on S1 r001 and S6 r001).
- **Decision**: adopt their contract instead of deploying my standalone architecture. Each of my methods is a
  `fit.R` with `fit_method(X, y, foldid, seed, control)` plus `tests.R` (`run_method_tests()`), `run.slurm`,
  `METHOD.md`, under `Benchmarks/<Exact_best_sub|SuSIE|PARNI>/`. The standalone architecture is kept as
  `standalone_v0/` for its tests and validation records.
- **Registry**: `shared/design.R` `benchmark_methods` gets `PARNI = 6L, SuSIE = 7L, Exact_best_sub = 8L` (6 and 7 are
  the indexes the other agent's comment reserved for PARNI and SuSiE; 8 is new, best subset is deterministic);
  `slurm/run_method.sh` and `slurm/submit_campaign.sh` accept the three folders. Backups kept next to the files.
- **leaps** 3.2 installed into `library_portable` (not present there; pure Fortran; nothing else modified).
- **PARNI inside the contract**: the five repeats run inside one `fit_method` call (one task per dataset, as the
  framework expects). Primary = repeat 1 plain PIP > 0.5 (the single run a practitioner would do, comparable to one
  SMC fit); repeats 2–5 and the RB rule are `sensitivity` supports; all PIP vectors are in `diagnostics`. Repeat seeds
  `seed + 100000 (m − 1)` (stay inside PARNI's seed band; no collision with SuSIE's index-7 band).
  `converged` = bookkeeping ∧ max SD of plain PIPs across repeats ≤ 0.05 ∧ max |plain − RB| ≤ 0.05 per repeat.
  `beta` = model-averaged posterior mean ∑_S w_S A_S⁻¹X_S'y over post-burn-in visits.
- **Exact reference** as a separate stage `Benchmarks/Exact_reference/` (not a method): `compute_exact.R` per sealed
  dataset, `compare_to_exact.R` joins any method's fits with the exact posterior (PIP error, exact-MPM/HPM agreement,
  per-scenario ceilings). The other agent's `metrics.csv` has no exact-reference columns; this stage adds them without
  touching their files.
- **Earlier release check**: the Oct 4 release's PARNI (`bvsparni`) targets the same control posterior with RM
  adaptation, four independently adapting chains and 5,000 + 80,000 iterations; its SuSiE used `refine = TRUE`,
  `max_iter = 1000`. Mine follow the papers' own settings (see the method notes); both are recorded.
- **Local verification before pushing**: their `shared/run_tests.R` passes for all three methods (their shared test
  fails locally only because my laptop's R 4.4.1/BLAS does not reproduce the sealed X bit for bit; it passes on NOTS);
  their `shared/run_task.R` ran all three methods end to end on S1 r001 (receipts, metrics, fits).
- **Smoke on NOTS** submitted 22:36Z: tests job 2046779, smoke arrays 2046780–2046782 (`runs/smoke_mine_20261007T223549Z`),
  exact smoke 2046783. Production arrays are NOT submitted until the user says so.
