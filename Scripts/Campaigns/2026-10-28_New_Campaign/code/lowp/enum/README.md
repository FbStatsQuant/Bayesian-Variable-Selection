# Exact enumerator and truth-dominance audit (LOWP, `code/lowp/enum/`)

Exact posterior of the SMC-BVS v3 target over all feasible models (|S| <= K), per dataset and per response scale, plus the T37 truth-dominance audit. Contract: `../INTERFACES.md` §I2, `../LOWP_SPEC.md` §L.7. Evidence of equivalence with the SMC scorer and the review fixes: `VALIDATION.md`.

**Supported domain.** Campaign use: n = 200, p = 20 and 30 (K = p). Allowed in code: p <= 40 (counts and masks exact), original column indices <= 53 (the double `mask` column), n <= any, up to 8 scales per pass. Larger p is rejected. The C++ bitmask machinery itself would run to p = 62, but that range is not validated and not claimed.

## Files

| File | Role |
|---|---|
| `lowp_enum.cpp` | C++ (Rcpp + OpenMP): DFS enumerator `cpp_enum`, test hooks, `cpp_score_models`, `cpp_td` |
| `lowp_enum.R` | loader (vendor-hash check, compile cache), `lowp_exact`, `lowp_score_models`, `lowp_td`, `lowp_td_count` |
| `run_enum_dataset.R` | CLI: one dataset, both scales, writes `EXACT.{rds,sha256,done}` |
| `exact_contract.R` | `lowp_validate_exact(record, requested_scales, input, mode)`: the shared strict EXACT-record validator |
| `vendor/` | `v3_score.h`, `v3_util.h` copied from the core, `VENDOR_SHA256.txt` |
| `Makevars.lowp` | the core's compiler flags (`-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`); OpenMP via the Rcpp plugin |
| `tests/` | validation scripts (`t1` ... `t11`), `helpers.R`, `timing_helpers.R`, `run_with_peak.ps1`, `logs/` |

## Use

```r
source("<this dir>/lowp_enum.R")                    # needs the core folder: default ../../core/v2_2/core, or LOWP_CORE_DIR, or core_dir=
ex <- lowp_exact(X, list(c100 = y1, c050 = y2), top = 1000, threads = 8)   # list of <S> per scale; attr(ex, "run") = run record
lowp_score_models(X, y, list(c(3L, 7L, 14L)))       # F, log_m, eta, size, route via v3::Scorer::score
lowp_td(X, y, truth = c(3L, 7L, 14L), d = 1, margin = 0, max_scores = Inf, threads = 8)
lowp_td_count(p = 1000, K = 100, s0 = 14, npool = 986, d = 1)   # exact number of scorer calls, no run
```

```
Rscript run_enum_dataset.R --dataset p0030_S4_r050 --study STUDYROOT --outroot OUT --run-id RID --threads 14 [--force]
Rscript run_enum_dataset.R --dataset dev_p0020_S1_r001 --study DEVROOT --outroot OUT --run-id RID --threads 14 --development
Rscript run_enum_dataset.R ... --unsealed-test-input      # tests only: allows a missing inputs manifest
```

**Inputs and verification.** The CLI reads only `STUDY/inputs/p{pppp}/{dataset_id}.rds` (never the truth folder). The inputs manifest `STUDY/manifests/inputs_manifest_lowp.csv` is **required**: it must contain exactly one row for the dataset and the file's SHA-256 must equal its `file_sha256`; otherwise the run stops before any output. `--unsealed-test-input` (not allowed with `--development`) permits a missing manifest for tests; the output then records `extra$input_mode = "unsealed_test"` and `manifest_checked = FALSE` (sealed runs record `"sealed"`, `TRUE` and the manifest's SHA-256).

`--development` (as `smc/run_smc_case.R`): dev ids (`dev_p0020_S1_r001`) are accepted only with the flag and prod ids only without it; pass `--study <root>/dev`, which has the same layout; the dev manifest is mandatory; results go to `OUT/results/RID/p0020/dev_p0020_S1_r001/`.

**Completion protocol (crash safe).** `EXACT.done` means "the RDS and its sidecar are complete and verified".
- A job skips only if `EXACT.done`, `EXACT.sha256` and `EXACT.rds` exist and agree (marker hash = sidecar hash = SHA-256 of the RDS) **and the record meets the whole requested contract**, i.e. `lowp_validate_exact(record, scales, input, mode)` passes with the current input, the current `input_mode` and manifest SHA-256 (an unsealed-test record is not reused once a manifest exists, and a changed manifest forces a recompute), and `source_sha256` equals the current source fingerprint; in detail: same dataset and input bytes; `source_sha256` equal to the current source fingerprint (SHA-256 of the hashes of `lowp_enum.cpp`, `lowp_enum.R`, `run_enum_dataset.R`, `Makevars.lowp`, the core's `v3_preprocess.R`, the vendored `v3_score.h`/`v3_util.h` and the core's own `cpp/v3_score.h`/`cpp/v3_util.h`); exactly the requested scale set (a `--scales c100` record is not accepted for the default two-scale request, and vice versa); all required top-level and per-scale fields; `complete` TRUE and `status` `"exact"`; `models_scored = models_expected = sum_{k<=K} choose(p,k)`; per-scale `status = "exact"`, `scope = "full"`, both heuristic labels, and normalised `size_logmass`. Otherwise it prints why ("existing EXACT.done is not valid (...): recomputing") and recomputes; `--force` recomputes unconditionally. Old records from before these fixes (joint `size_logmass`, no labels, other sources) are therefore never silently reused; keep them as historical evidence only.
- Writers of one destination are serialised by a lock directory `<dest>/.lock` (stale after 10 minutes). A job that cannot take it exits with status 3 and changes nothing. Under the lock: remove any old `.done` first; stage the RDS and sidecar under temporary names and verify them (hash, read-back); rename them into place; re-verify the committed pair; write `.done` (temporary name, rename) last; re-verify. A failure at any point leaves no `.done`, no lock and no temporary files.
- `EXACT.rds` is written uncompressed. Compile time is excluded from `runtime_s` (elapsed seconds of `lowp_exact`).
- Test-only failure injection: env `LOWP_ENUM_FAIL_AT` in {`before_rds_rename`, `after_rds_rename`, `after_sha_rename`, `before_done`}; `tests/t10_cli_completion.R`.

Compile cache: env `LOWP_ENUM_CACHE` (default a folder under `tempdir()`); it never goes inside the study tree. On NOTS set it to scratch. The cache key hashes the C++ source, the vendored headers, `Makevars.lowp` and the R version; concurrent jobs build once under a lock (same scheme as the core's `v3_compile`).

## What it computes

- Preprocessing: `v3_preprocess` from the core on (X, y) for each scale (as `v3_fit`); constant columns are dropped and the original-index map is kept (`pip` names, `hpm`, `mpm`, `model`, `mask` all use original indices). Statuses other than `ok` stop the run.
- Score F(S) = logprior[|S|] + log m(S) with `v3::Data` from `data_init`, K = min(p, n/2). The DFS appends one row to the lower Cholesky factors of H and A per included variable with the operation order of `chol_inplace`, `forward_solve` and `finish_from_factors`, so F and η are bit-identical to `Scorer::score` (empirical evidence in `VALIDATION.md`; this is a statement about F and η, not about the aggregates). Models with Q < 1e-8 y'y, non-finite log m or a failed pivot (and every descendant of a failed pivot) are rescored by `Scorer::score`; counted in `numerics`.
- Streaming aggregates per scale: log Z (long-double log-sum-exp with running max; weights are `exp` in double accumulated in long double, so log Z and PIPs agree with the core's `cpp_enumerate` to rounding, not bit for bit), PIP numerators (subtree sums, one add per node), **posterior** mass by size `size_logmass[k] = log P(|S| = k | y)` (sums to 1 on the probability scale, i.e. log-sum-exp = 0), the joint log mass `size_logjoint[k] = log sum_{|S|=k} exp F(S)` (log-sum-exp = log_Z), HPM with the master §I.6 tie rule (F, then smaller size, then lexicographic; bitmasks, checked against `v3::hpm_better`), the two largest F + η for the certificate, a bounded top-1000 store in the TopStore order. `second_F`, `margin`, `certificate_bound`, `global_certified` as `cpp_enumerate`.
- **Certificate labels.** η and `certificate_bound` are the core's heuristic numerical-error quantities, not interval bounds. Every scale record carries `certificate_bound_kind` and `hpm_eta_kind`, both `"heuristic (not a validated interval bound)"` (master §I.2, §I.3). `global_certified = TRUE` only says F(HPM) − η(HPM) > max over all other feasible models of F + η under that heuristic; it is not a rigorous proof.
- **Complete vs partial.** `status` is `"exact"` only if every feasible model (|S| <= K) was scored exactly once (`models_scored == models_expected`). Test hooks `task_subset` / `prefix_fraction` give `status = "partial"` with a warning: `scope = "restricted_to_scored_models"`, `global_certified = FALSE`, and log_Z, PIPs, size masses, HPM, `margin` and the certificate refer to the scored models only (`certified_over_scored_models` holds the restricted comparison). The CLI refuses anything but `"exact"`.
- Parallelism: tasks = include/exclude pattern of the first `task_bits` variables (default min(p, 10) = 1,024 tasks for p >= 10; `task_bits` is validated to 0..20); OpenMP dynamic schedule; finished tasks are merged in task order (a merge of task t waits for tasks < t), so outputs are identical for any thread count at a fixed split (a different split can change last bits of sums).
- **Memory.** Per-thread workspace is O(p²) and the top store is bounded, so with the **default split** (1,024 tasks) and no collection hook the footprint is the per-thread workspace plus the **pending task results**: a finished task waits until all earlier tasks have been merged, and each pending result holds, per scale, a top store (<= 1000 entries) plus O(p + K) accumulators; the worst case is therefore bounded by (number of tasks) × scales × (top + p + K) entries, about 50 MB at the default split, not by threads alone (the reorder queue is not capped). Measured: 83 MB peak working set for the whole R process at p = 30 with 14 threads, about 2 MB above the 81 MB R baseline. `task_bits` near p, or the `collect_F` hook (2^p doubles per scale), is not memory-bounded and is for tests at small p.
- Self-check in production: every 1009th node of each task is rescored by `Scorer::score`; `numerics$recheck_count`, `recheck_mismatch_F`, `recheck_mismatch_eta` and `max_abs_dF_recheck` report it (expected mismatches: 0).
- `numerics` fields: `n_rescale` (running-max rescalings), `n_fallback_v3` (models rescored by `Scorer::score`), `n_fallback_slow_subtree`, `q_recomputed` (Q-rule rescorings), `n_fallback_nonfinite`, `recheck_*`.

### Output record of one scale (`<S>`, §I2) -- fields added or changed in this version

| Field | Status |
|---|---|
| `size_logmass` | **changed**: log posterior mass of size k (log-sum-exp = 0); was the joint mass |
| `size_logjoint` | new: the previous joint quantity (log-sum-exp = `log_Z`) |
| `certificate_bound_kind`, `hpm_eta_kind` | new: `"heuristic (not a validated interval bound)"` |
| `status` | new: `"exact"` or `"partial"` |
| `scope` | new: `"full"` or `"restricted_to_scored_models"` |
| `certified_over_scored_models` | new: the certificate comparison over the scored models (equals `global_certified` when complete) |
| `global_certified` | now FALSE for any partial run |

Run record `attr(ex, "run")`: new `models_expected`, `complete`; `status` may be `"partial"`. EXACT envelope: `models_expected` and `complete` are written at the top level (as INTERFACES §I2) and also kept in `extra`; `extra` also has `input_mode`, `manifest_sha256`, `manifest_checked`, `status`. `source_sha256` is the source fingerprint defined under the completion protocol (it now also covers the core's own scorer headers).

## `exact_contract.R::lowp_validate_exact` (shared, stable signature)

```r
source("<enum dir>/exact_contract.R")          # base R only
v <- lowp_validate_exact(record, requested_scales = c("c100", "c050"), input = NULL, mode = c("sealed", "unsealed_test"))
v$ok; v$reasons                                  # list(ok = logical(1), reasons = character())  (one reason per failed check)
```

The single strict check of the EXACT record contract (INTERFACES §I2); used by `run_enum_dataset.R` for the resume decision and the pre-publish and post-commit checks, and meant to be called by the scoring and pilot code. The signature is stable (an optional fifth argument `exact_scale_set = FALSE` exists; the CLI passes TRUE so a record must hold exactly the requested scales, consumers normally leave FALSE and name the scales they need).

- `record`: `readRDS("EXACT.rds")`. `requested_scales`: each must be present. `input`: `NULL`, or a list with `X` (the original n × p input matrix) and optionally `dataset_id`, `file_sha256` (SHA-256 of the input file) and `manifest_sha256`; every element given is compared with the record. `mode`: the record's `extra$input_mode` must equal it; a `"sealed"` record must carry `manifest_checked = TRUE` and 64-hex `manifest_sha256` and `input_file_sha256`.
- Checks: schema `lowp_exact_v1`; dataset id; all required top-level, `extra` and per-scale fields; `n`, `p` (original columns), `K = min(p_retained, floor(n/2))` and `models_expected = sum_{k<=K} choose(p_retained, k) > 0`, where `p_retained` is the length of `extra$retained_columns` (constant columns are dropped, so p = 20 with one constant column gives 19 retained and 2^19 models); with `input`, `n`, `p` and the retained map must equal the input's (non-constant columns); both completeness copies (`complete`, `extra$complete`) TRUE, `extra$status` `"exact"`, `models_scored == models_expected` (top level and `extra`); each requested scale `status = "exact"`, `scope = "full"`, both heuristic labels, finite `log_Z`/`log_m0`/`hpm_F`/`hpm_eta`/`second_F`/`certificate_bound`, `margin >= 0`, `pip` numeric of length `p_retained` in [0, 1] named by the retained columns, `hpm` a sorted subset of the retained columns with `hpm_size = length(hpm)` (**`integer(0)` is valid**), `mpm = {pip > 0.5}`, `size_logmass` of length K+1 with `|log-sum-exp| <= 1e-10`, `size_logjoint` with log-sum-exp = `log_Z`, `top` with `min(1000, models_expected)` rows in the §I.6 order (F decreasing, then smaller size, then lexicographic), distinct, whose `model` text, `mask` and `size` agree and whose first entry equals the HPM (support, size, mask, `hpm_F`) with `second_F = top$F[2]`; cross-field identities `size_logjoint[k] = size_logmass[k] + log_Z` (1e-9, matching -Inf), `log_Z_rel_m0 = log_Z - log_m0`, `log_Z >= hpm_F` and `log_Z >=` log-sum-exp of the listed top F; `sum(pip) = sum_k k exp(size_logmass[k])` (1e-8·p_retained) and PIP feasibility given the listed top models (`share_j <= PIP_j <= share_j + unlisted mass`, 1e-9), and `numerics` with zero score re-check mismatches.
- Not checked (the validator does not know it): the source fingerprint. Callers compare `record$source_sha256` with their own fingerprint (the CLI does). Passing the validator says the record is a complete, internally consistent I2 record for that input; it is not a scientific accuracy statement.

## `lowp_td` (T37)

Inputs are validated before any counting: `d` a single integer in 0..1000, `margin` a finite number >= 0 (T37 defines TD(d, m) for m >= 0; negative margins are rejected in R and C++), `truth` (non-empty, at most min(K, 40)) and `null_pool` unique integer indices of retained columns, disjoint, `threads` 1..1024, `max_scores` a number >= 0 (Inf allowed); the same checks (d >= 0, finite margin, no duplicates, caps on the number of pool subsets and centres) are repeated in C++. A run is refused when the exact score count is not exactly representable (>= 2^53) or the closed-form count disagrees with the number actually used.

Centres U ∪ P (U ⊆ S₀, P ⊆ pool, |P| <= d, size <= K). Feasible moves: every addition (only if |S| < K), every deletion, every swap (swaps keep the size, so they are feasible at |S| = K). With a restricted `null_pool` the result concerns that restricted centre region only (`r$region`).

- **literal** (T37 wording; the top-level fields of the result): clause (a) S ⊉ S₀: margin = best gain among additions of a missing true variable minus the best gain among all other moves (excluding exactly that one move; ties give margin 0). Clause (b) S ⊋ S₀: same with deletions of null variables. Clause (c) S = S₀: margin = minus the best gain over all moves. Known property: at a centre that misses a truth j and contains a null l, the swap (l out, j in) generally beats "add j", so clause (a) fails whenever such a swap exists (see `VALIDATION.md`).
- **toward** (`r$toward`, same structure): at S ≠ S₀, margin = (best gain among moves that strictly reduce |S Δ S₀|: add a truth, delete a null, swap null-out/truth-in) minus (best gain among moves that do not); clause (c) as literal.
- TD(d, m) holds iff all margins >= m (`td_holds`, and `td_holds_strict` for > m), for each variant (`r$toward$td_holds`, ...). If no target/reducing move is feasible the margin is -Inf; if there is no other move it is +Inf.
- Output: per clause `n_centres`, `n_violating` (margin < m), `n_violating_strict` (margin <= m), `min_margin`, `min_centre`; `violators` (all centres with margin <= m: centre, clause, size, margin, g*, o*, the two moves, `o_label` = type of the best competing move); `r$diagnosis` (literal violators by clause and `o_label`); `scores_used`; `scores_needed` and `count_exact` (closed form, computed before running; if it exceeds `max_scores` only the dry-run record is returned); `keep_all = TRUE` adds the per-centre table (and `r$toward$centres`).
- A "score" is one `Scorer::score` call; no de-duplication across centres; per-centre cost 1 + k + k(p−k) + [k<K](p−k). Centres are processed with OpenMP, each thread with its own `Data` copy.

## Limits

Supported domain as stated at the top. Fallbacks to `Scorer::score` have never fired on real or synthetic data (see `VALIDATION.md`); they are tested through hooks only. The duplicate-column components of `v3_preprocess` are not computed (`dup_components = FALSE`).
