# LOWP interfaces (binding between lowp/, bench_lowp/, scoring/)

All paths are relative to a study root `STUDY` (local test root or `/home/fb31/projects/BVS/New_Campaign` + `/scratch/fb31/New_Campaign` on NOTS). IDs: `dataset_id = p{pppp}_S{s}_r{rrr}`, `case_id = {dataset_id}_{scale_key}`, `scale_key ∈ {c100, c050}`. Supports are sorted 1-based original indices; text encoding `"3;7;14"`, empty model `""`, missing `NA`.

## I1. Inputs (written by `lowp/R/lowp_seal.R`)

`inputs/p{pppp}/{dataset_id}.rds`: list(`X` n×p double, no attributes; `Y` n×5 with colnames c100,c075,c050,c035,c025; `foldid` int[200]; `dataset_id`; `n`; `p`; `kind`; `scenario`; `replicate`; `scales`; `data_seed`; `fold_seed`; `method_seed`). Dev ids carry the prefix `dev_` (`dev_p0020_S1_r001`) and live under `dev/`.
`truth/p{pppp}/{dataset_id}.rds`: list(`dataset_id`, `active` int, `beta` double[s0] (coefficients of `active`, not a length-p vector), `signal` double[n], `eps` double[n], `scenario`).
`manifests/inputs_manifest_lowp.csv`: dataset_id, p, scenario, replicate, data_seed, fold_seed, method_seed, file, file_sha256, x_sha256, y_c100_sha256 … y_c025_sha256, fold_sha256.
`manifests/truth_manifest_lowp.csv`: dataset_id, file, file_sha256, signal_sha256, eps_sha256, active (text), beta (text).
Float64 hash = SHA-256 of `writeBin(as.double(as.vector(x)), raw(), endian = "little")` (`digest(serialize = FALSE)`), as benchmark `common.R`.

## I2. Exact enumerator output (written by `lowp/enum/run_enum_dataset.R`)

`results/{run_id}/p{pppp}/{dataset_id}/EXACT.rds` (+ `.sha256`, `.done`), one file per dataset holding both scales (one enumeration pass serves both scales). `source_sha256` fingerprints the enum sources, the vendored headers, the core's `v3_score.h`/`v3_util.h` and preprocessing; a resume reuses a record only if the fingerprint, scale set, required fields and full coverage all match:

```
list(schema = "lowp_exact_v1", dataset_id, p, n, K, source_sha256, v3_score_sha256, runtime_s, host, started_utc, finished_utc,
     models_scored, models_expected, complete, threads,
     extra = list(input_mode = "sealed" | "unsealed_test", manifest_sha256, manifest_checked, status, ...),
     scales = list(c100 = <S>, c050 = <S>))
<S> = list(
  log_Z,            # full working scale (includes log m(∅)), standardised working model (§I.6)
  log_m0, log_Z_rel_m0,
  pip,              # double[p], names "1".."p"
  hpm, hpm_F, hpm_size, hpm_eta, second_F, margin, certificate_bound, global_certified,
  mpm,              # int, PIP > 0.5
  size_logmass,     # double[K+1]: log P(|S| = k | y), k = 0..K (log-sum-exp = 0)
  size_logjoint,    # double[K+1]: log sum_{|S|=k} exp F(S) (log-sum-exp = log_Z)
  status, scope,    # "exact"/"partial"; "full"/"restricted_to_scored_models" (production CLI refuses partial)
  certificate_bound_kind, hpm_eta_kind,   # "heuristic (not a validated interval bound)"
  certified_over_scored_models,
  top,              # data.frame(rank, F, size, model (text), mask (double, bit j-1 = variable j)), top 1000 by F with §I.6 tie order
  numerics = list(n_rescale, n_fallback_v3, max_abs_dF_recheck, recheck_count, q_recomputed))
```

R API (sourced from `lowp/enum/lowp_enum.R`):
- `lowp_exact(X, Ylist, top = 1000, threads = 1)` → list of `<S>` per element of `Ylist` (named by scale key). X and each y are preprocessed with the core's `v3_preprocess` exactly as `v3_fit`.
- `lowp_score_models(X, y, models)` → data.frame(model, size, F, log_m, eta): F(S) for arbitrary models (list of int vectors), identical arithmetic to the SMC scorer (calls `v3::Scorer::score`).
- `lowp_td(X, y, truth, d, null_pool = NULL, margin = 0)` → TD(d, m) audit of T37 (definition in `scoring/THEORY_MEASURES.md`): per-clause counts of centres, violations, minimum margin, and the violating centres.

## I3. SMC-BVS low-p output (written by `core/v2_2_1/study/run_case.R`, regime L of the single v2.2.1 study layer; the former fork `lowp/smc/` is retired, CODE_LEDGER 2026-10-29)

`results/{run_id}/p{pppp}/{case_id}/SMCBVS[_rep{m}].{rds,csv,sha256,done}`, the study-adapter envelope of `code/core/v2_2/study/SCHEMA.md` with `regime = "L"`, `study = "newcampaign_lowp"`, and `method_seed` = data seed + 4,000,000 (+ 1,000·m for repeat m). `record$fit` is the full native return. Scoring reads native fields through one function, `scoring/R/extract_smc.R::extract_smc(record)`, which is the only place that knows field names (PROVISIONAL until `conformance/OUTPUT_FIELDS.md` exists).

## I4. Benchmark low-p output (written by `bench_lowp/run_bench_case.R`)

`results/{run_id}/p{pppp}/{case_id}/{method_id}.{rds,csv,sha256,done}` with the master §III.3.0 rule frame (`rule_id, role, status, support, support_audit, k, converged, diag_flag, diag_codes`, …) plus `runtime_s`, `adaptation_ids` (semicolon list of ADAPTATIONS.md rule ids applied).

## I5. Scoring outputs (written by `scoring/`)

`analysis/lowp/` tables (CSV + one Markdown summary): `case_smc_accuracy.csv` (one row per SMC fit), `case_selection.csv` (one row per case × method × rule), `case_theory.csv` (one row per case), and the headline tables `H1_logZ.csv`, `H2_hpm.csv`, `H3_pip.csv`, `H4_recovery.csv`, plus `HEADLINE.md`.
