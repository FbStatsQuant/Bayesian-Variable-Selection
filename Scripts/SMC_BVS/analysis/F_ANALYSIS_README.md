# F_analysis_claude: Campaign 2 scoring and analysis

This folder holds a copy of D's pipeline (`../D_analysis/pipeline`, read-only), with the fixes below. The full diff is in `DIFF_vs_D_pipeline.patch`. The benchmark scoring code (`score.R`, `aggregate.R`, `registry.R`, `combine.R`) is used unchanged: it is copied and hash-pinned at every run.

## One command (Phase 2)

```
python pipeline/score_campaign2.py --smc-results <laptop>/.../results/<run_id> --ops-outputs ../E_ops_claude/OUTPUTS.md --work <new dir>
```

- `--smc-results` is the A-runner results root, laid out as `<run_id>/pXXXX/<case_id>/SMCBVS.{csv,rds,sha256,done}`. Its folder name is the run ID. Both scales are read from it unless `--smc-results-c050` is given.
- Every other path is an argument; the defaults point to the laptop copies of the benchmark study and D's reproduction outputs.
- It runs three steps:
  1. `prepare_assessment_config.py`, for the full design (r1..100);
  2. `run_pipeline.py`, which validates every SMC bundle (sidecars, provenance, seeds, X/Y hashes, R-1, native consistency) **before** opening any truth, then scores it with the benchmark `score_fit_rows`, joins all benchmark rows, and writes the tables and MCSEs;
  3. `make_results.py`, which writes the RESULTS tables and figures.
- Outputs go under `--work`; keep that outside OneDrive (`C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\F_analysis\`).

## Mock suite (regression)

```
python pipeline/run_local.py --evidence-root <dir> [--reproduction-root ../D_analysis/reproduction] [--benchmark-scoring <...>/scoring]
```

## Changes from D (why)

| File | Change |
|---|---|
| `native_contract.R` | **D-F1:** the heuristic-bound label is required only if `global_certified` is TRUE. It accepts A's native label `heuristic (not a validated interval bound)`. |
| `mutate_fixture.R`, `verify_fixture.py`, `freeze_evidence.py` | D-F1 regressions: label missing on a certified fit → rejected; label missing on an uncertified fit → passes all checks. Work and reproduction paths are now arguments. |
| `run_pipeline.py` | The design selector accepts r1..10 (Amendment 1) or r1..100 (Campaign 2; 1,200 datasets, 2,400 cases), and nothing else. Runtime indexing is O(rows); the old version was O(cases × rows). TP is added beside FP/FN. Outputs may go anywhere (relocatable). |
| `prepare_assessment_config.py` | `--design full|amendment1`; no output-location restriction. |
| `run_local.py` | All paths are arguments. D's freeze step (which rewrites D-era docs) runs only with `--freeze`. |
| `make_results.py` (new) | Results tables and figures from the pipeline outputs, with no rescoring. |
| `score_campaign2.py` (new) | The one-command wrapper. |

## Phase 1 evidence

- `phase1_devsmoke/`: the real A v2 dev smokes scored with truth; the dev truth comes from the unchanged generator. Independent recount: 38/38.
- Mock suite: 245/245 checks pass. The evidence is in `...\F_analysis\validation\`.
- Full-design dry run, with all 1,200 benchmark datasets and no SMC output:
  - benchmark cells equal the published SUMMARY;
  - both combined `rules_long` tables reproduce cell-for-cell;
  - every SMC cell is 100/100 (or 600/600) missing.
