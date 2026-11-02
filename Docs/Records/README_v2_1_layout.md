# Bayesian Variable Selection

Local-to-global Bayesian variable selection (SMC-BVS): a sequential Monte Carlo sampler over models with a Beta-Binomial BB(1, p) size prior, reporting the highest posterior model (HPM). The current method is SMC-BVS v3, code version v2.1 (the code of the 2,400-fit production run, 2026-10-23).

This repository holds the code, the current documents, the small final result tables, and the reference papers. Data and per-seed simulation outputs are not stored here (they stay on the PC and on NOTS). Code is written here and deployed to NOTS for large runs.

## Layout

```
BVS_GH/
├── Scripts/            code
│   ├── SMC_BVS/        the method (v3, version v2.1) and its tooling
│   ├── Benchmarks/     the competing methods and their scoring
│   ├── Data_generators/
│   └── Exact/          exact-posterior references for small p
├── Results/            final summary tables and figures (no per-seed outputs)
├── Docs/               methodology, theory, run records, history, literature notes
├── Papers/             reference papers
└── Others/             miscellaneous
```

### Scripts/

| Folder | Contents |
|---|---|
| `SMC_BVS/core/` | Method core: R driver files (`v3.R` entry, `v3_fit.R`, preprocessing, setup, calibration, final run, exact branch) and the C++ engine in `cpp/` |
| `SMC_BVS/study/` | `adapter.R` and `run_case.R`: run one dataset through the method |
| `SMC_BVS/tests/` | v2.1 regression suite (32-seed comparison against the prototype core) |
| `SMC_BVS/smoke/` | Smoke test and adapter contract test |
| `SMC_BVS/build/` | Build, freeze and NOTS launch scripts |
| `SMC_BVS/reference/` | `prototype_core/` used by the regression suite, `CHANGES.md` (v2 to v2.1), rulings |
| `SMC_BVS/nots_runner/` | NOTS production runner (`submit.sh`, `task.sh`, `poll.py`, `reconcile.py`, `rerun.sh`), sha256-verified transfer tools, and the 2,400-unit production table |
| `SMC_BVS/analysis/` | Scoring and analysis pipeline that produced `Results/SMC_BVS_v3_production` (`run_pipeline.py`, `score_campaign2.py`, `make_results.py`, contracts, fixtures and tests) |
| `Benchmarks/<method>/` | Code of each benchmark's final production run in the n = 200 study: Lasso, ElasticNet, AdaptiveLasso, MCP_SCAD, ABESS, SuSiE, SSL, Horseshoe |
| `Benchmarks/scoring/` | Benchmark scoring, aggregation and pairing code (`registry.R`, `score.R`, `aggregate.R`, `combine.R`, `pair.R`) and derived rules |
| `Benchmarks/PARNI/` | PARNI implementation (p = 30 study; not in the final eight) |
| `Data_generators/` | Generators and verifiers of the n = 200 dev, production and holdout datasets |
| `Exact/stratified_enumerator/` | Stratified exact enumeration of all 2^30 models (p <= 30) |
| `Exact/exact_reference_p30/` | Exact posterior reference of the p = 30 study |
| `Exact/best_subset_bic/` | Exact BIC best-subset method |
| `Exact/oracle_p20/` | Independent Python oracle (exact, p <= 20) used to verify the v3 engine |
| `Exact/tinyp_check/` | Tiny-p check of SMC against exact enumeration |

Usage of the core:

```r
source("Scripts/SMC_BVS/core/v3.R")
fit <- v3_fit(X, y, seed, allocation = list(mem_gb = 8, hours = 24))
```

The scripts are copies of the frozen production code. Some of them still contain the paths of the machine they ran on (NOTS or the PC), so set paths before rerunning.

### Results/

| Folder | Contents |
|---|---|
| `SMC_BVS_v3_production/` | SMC-BVS v3 on the n = 200 study, p = 500 and p = 1000 (2,400 fits), scored 2026-10-28: `HEADLINE_TABLES.md` (exact recovery against all benchmarks), per-p results tables, figures, runtime, scoring config, independent recount scripts |
| `Benchmarks_n200/c100/`, `c050/` | Final benchmark tables of the n = 200 study at signal scale c = 1 and c = 0.5 (`SUMMARY.md`, `T1`-`T6`, `S_tables.csv`, `rules_long.csv` and the corrected `rules_long_v7.csv`; c050 also has the c100-vs-c050 pairing and the horseshoe long-chain sensitivity) |
| `p500_comparison/` | Earlier ten-method comparison at p = 500 (BB+HPM, the mixture challenger and eight benchmark rules on 3,000 datasets): summary tables and the comparison scripts |

Headline (exact recovery of the true model, out of 600 datasets, c = 1, p500 / p1000): SMC-BVS v3 (HPM) 559 / 560, SuSiE 585 / 582, spike-and-slab LASSO 569 / 582, horseshoe 574 / 575, SCAD 454 / 417, MCP 377 / 235, ABESS 365 / 323, Lasso, elastic net and adaptive Lasso 0. At c = 0.5, SMC-BVS v3 (HPM) is best: 370 / 340, against 303 / 255 for spike-and-slab LASSO and 220 / 205 for SuSiE. See `Results/SMC_BVS_v3_production/HEADLINE_TABLES.md`.

### Docs/

| Folder | Contents |
|---|---|
| `Methodology/` | `METHODOLOGY_v3.md` (the method spec the code implements), `SPEC_anyXY_v2.md`, and the master methodology and plan (`MASTER_Methodology_and_Plan.{md,tex,pdf}` with its evidence notes) |
| `Theory/` | v3 theory writeup (`THEORY.pdf`, `THEORY.tex`), `THEOREM_MAP.md`, rulings, status; `theorems/` (36 conjecture statements); `proofs/` (`COLLECTED_PROOFS_v2.pdf`, `LOCKED_PROOFS.md`, `PROOFS_STATUS.md`, each theorem's statement, and the final proof of the 9 theorems not in the collected document) |
| `Records/` | Run records worth consulting: `LEVERS.md`; the n = 200 benchmark study run ledger, c = 0.5 pre-registration and plan, verification reports; the SMC-BVS v3 deployment outputs, handoff, go decision, NOTS readiness, rulings and audit summary |
| `History/` | Earlier campaigns that led to the method: the selection campaign behind BB(1, p) + HPM (2026-10-13) and the p = 30 benchmark study against the exact posterior (2026-10-07) |
| `Literature/` | Literature conclusions: final recommendations of the method brainstorm, benchmark choice reports, the benchmark selection note, the five-candidates report |

### Papers/

| Folder | Contents |
|---|---|
| `SMC/` | Del Moral, Doucet and Jasra (2006), Sequential Monte Carlo samplers |
| `Core_bibliography/` | The numbered core bibliography (29 PDFs, `INDEX.txt`; #03 Krishna 2009 only as web text, #21 not available) |
| `Priors_and_decision_rules/` | Size priors, posterior contraction and decision rules behind BB(1, p) + HPM (Wilson et al. 2010, Castillo and van der Vaart 2012, Castillo, Schmidt-Hieber and van der Vaart 2015, Barbieri and Berger 2004, Müller, Parmigiani and Rice 2007, and others) |
| `Benchmark_methods/` | Primary papers of the benchmarks: Lasso, elastic net, adaptive Lasso, glmnet, spike-and-slab LASSO, ABESS, horseshoe (SuSiE is #29 in the core bibliography) |
