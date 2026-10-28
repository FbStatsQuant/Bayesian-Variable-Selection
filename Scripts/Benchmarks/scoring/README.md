# Scoring and aggregate tables (thread S, 2026-10-19)

Brief: `thread_briefs/BRIEF_SCORING.md` (with `VERIFY_CONTEXT.md`). Protocol: miscellaneous operations. Implements master §IV.1.2 (scoring columns) and §IV.1.3 (T1–T6, S-tables). **All numbers are provisional**: the scoring code and the method code are AI-written and unreviewed (G5); the tables are pending the independent recount (G9).

## Locations

| What | Where |
|---|---|
| Code (NOTS) | `/projects/ml75/fb31/BVS/bench20261019/scoring/code/` (identical by SHA-256 to `code/` here) |
| Outputs per run (NOTS) | `$STUDY/scoring/out/<run_id>/`; dev runs under `$STUDY/scoring/out/dev/<method folder>/<dev run id>/` |
| Logs (NOTS) | `$STUDY/scoring/logs/S_score_<jobid>.out` |
| Local copies of the small outputs | `out/<run_id>/` (everything except `scored_rows.csv`, which stays on NOTS) |

## Code

| File | Role |
|---|---|
| `code/registry.R` | closed lists from the master: method ids, rule ids and roles (item f of §III.3.1–§III.3.8), status, flag and info codes, the §IV.1.2 columns |
| `code/score.R` | scoring step for one run: coverage, sidecar hashes, provenance, row checks, truth join and verification, truth columns, PIP columns (A1, SuSiE-L100), A3 `crn_mismatch` |
| `code/aggregate.R` | T1–T6, S-tables, caps, code counts and `summary.md` for one scored run |
| `code/combine.R` | combined tables across the eight runs, `summary_combined.md`, `SUMMARY.md` |
| `code/score_derived.R` | post-hoc derived rule `ebic1_K37` (F5, F4, F4_SCAD) as a separate labelled S-table |
| `code/tests/test_scoring.R` | unit tests on hand-made fixtures (50 checks) |
| `code/slurm/score_job.slurm` | the SLURM job (tests, dev runs, production runs) |

## Outputs per run (`$STUDY/scoring/out/<run_id>/`)

| File | Content |
|---|---|
| `scored_rows.csv` | every rule row with the §IV.1.2 columns; truth columns filled |
| `coverage.csv` | one row per expected (case, method_id): complete / incomplete / missing, files present, sidecar check, row count |
| `problems.csv` | every failed check (check, case, method, rule, detail); empty = all checks passed |
| `files_extra.csv` | files that belong to no expected (case, method_id) |
| `truth_signals.csv` | per p: signal a01–a14, index, β (verified identical across datasets) |
| `rules_long.csv` | every (method, rule, p, scenario/pooled): denominators, failures, exact all-saved / passing-only / among successful, FP/FN sums and means, error types |
| `T1.csv` | primary rules (+ `ebic1` companion for F1–F3) |
| `T2.csv` | failed / timeout / not_run / missing counts, primary rule |
| `T3.csv` | mean FP and FN (over successful rows; sums and n given) and error-type counts, primary rule |
| `T4_by_variable.csv`, `T4_by_group.csv` | selection frequency of each active variable, primary rule; grouped by abs(β) and S6 ρ (the two groupings coincide by design, §II.3) |
| `T5.csv` | runtime median, p95 (type-7 quantile), max per (p, method), one value per fit |
| `T6.csv`, `codes_by_rule.csv`, `caps.csv` | status, `converged`, `diag_flag` and code counts per (method, rule, p, scenario); `ebic_at_largest` cap hits |
| `S_tables.csv` | T1 layout for every S0 and S1 rule |
| `summary.md` | short Markdown summary |
| `posthoc_ebic1_K37/` (F5, F4 runs only) | post-hoc rule: `scored_rows_posthoc.csv`, `S_table_posthoc.csv`, `changes_vs_ebic1.csv`, `problems_posthoc.csv`, `summary_posthoc.md`; never in T1 |
| `code_sha256.txt`, `outputs_sha256.txt` | code and output hashes |

Combined across the eight runs: `$STUDY/scoring/out/combined/` (the same tables with a `run_id` column, `summary_combined.md`, `SUMMARY.md`); local copy of SUMMARY.md: `SUMMARY.md`.

Real-valued columns (means, rates, runtimes, PIPs) are written with 17 significant digits (`%.17g`), unquoted, beside the integer sums and counts. `files_extra.csv` labels dev canary bundles (`kind = dev_canary`, excluded) apart from orphans.

## Conventions (stated so the recount can compare exactly)

- Denominator: expected cases per cell from the inputs manifest (100 per (p, scenario), 600 pooled per p). Failed, timed-out, not-run and missing fits count as non-recovery; `n_fail_total` = failed + timeout + not_run + missing.
- Failed rows: `exact = FALSE`, `error_type = failed`, `tp/fp/fn/sel_*` = NA; `support_audit` is never scored.
- `exact_passing`: exact and `diag_flag = FALSE`; same denominator. `exact_among_success`: exact / (ok + warning rows).
- Mean FP / FN: over successful rows only (sum and n reported).
- T4: a failed or missing fit counts as "not selected"; denominator = expected cases.
- A1 / SuSiE-L100 PIP columns are filled on every rule row of the fit from the RDS PIP vector; `max_pip_null` = max PIP over the 486 / 986 null variables.
- A3 `crn_mismatch`: implemented; under D3 (c = 1 only) each dataset has one A3 fit, so it cannot fire.
