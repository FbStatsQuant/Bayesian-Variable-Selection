# AUDIT A-CODE: is A's frozen v2 a faithful, correct implementation of master Part I?

Auditor: A-CODE (Claude Opus 5.5), 2026-10-22/23. Contract: `AUDIT_CLAUDE/AUDIT_CONTEXT.md`. No FAILED_ATTEMPTS.md exists in the deployment root.

**Verdict: SOUND WITH FIXES.** v2 is a faithful implementation of Part I. I found no critical or major finding. Every prototype-to-v2 difference is required by Part I, CHANGES.md, R-1 or R-5, and each is correctly implemented. At production budgets, v2 reproduces the verified prototype bit for bit on every statistical output (my own end-to-end runs, §5). The four minor findings below are provenance, labelling and operational items. None of them changes a selection, PIP, evidence value or diagnostic flag. v2 can be deployed. F1 should be fixed, or explicitly checked on NOTS, before outputs from two hosts are mixed.

## 0. Identities checked before review

| Item | Check | Result |
|---|---|---|
| Master Part I | `sha256sum MASTER_Methodology_and_Plan.md` | `7d77dddb…20757b6e`, matches AUDIT_CONTEXT |
| Verified prototype | `sha256sum -c prototype_core.sha256` (paths re-rooted) | 26/26 OK |
| v2 reference copy vs verified prototype | sorted per-file SHA-256 of 19 source files | byte-identical |
| Local v2 snapshot | `sha256sum SHA256SUMS manifest.json`; `sha256sum -c SHA256SUMS` | `b56100b3…` / `aa598137…`, as HANDOFF_v2; 95/95 OK |
| Owls v2 copy `/home/fb31/smcbvs_v3_deploy_20261022/A_build/v2` | same commands on Owls | same two hashes; 0 failures |
| Unchanged core files | SHA-256, prototype vs v2 | `Makevars.v3`, `v3_blocks.h`, `v3_calib.h` (RC-2), `v3_start.h`, `v3_util.h` byte-identical |

## 1. Findings

| ID | Severity | Location | Claim / issue | Evidence | Fix |
|---|---|---|---|---|---|
| F1 | minor | `code/study/adapter.R:167` (`files <- sort(unique(files))`) | The aggregate `source_sha256` / `v3_source_sha256` is presented as the code identity, but it depends on the host's collation locale. | The per-file hashes in both v2 smoke RDS records equal the local v2 snapshot (22/22, `identical()` TRUE). Re-aggregating in the recorded order reproduces `ebfb67d7…` exactly. Sorting on another machine gives `8c549299…`. The Owls order (`…v3_setup.R core/v3.R study/adapter.R study/README.md…`) is locale collation, not C-locale byte order. | Use `sort(files, method = "radix")`, or pin `LC_COLLATE` in the job environment. Until then, a NOTS job under a different locale records a different source hash for identical code. Resume then refuses the unit, which fails safe, but cross-host provenance shows a false mismatch. At minimum, check on NOTS that the aggregate equals `ebfb67d7…`. |
| F2 | minor | `code/core/v3_fit.R` exact branch: `fit$log_Z_lower95 <- log(0.05) + e$log_Z` | This is an addition the prototype does not have. Part I §I.6 defines the 0.05·Ẑ Markov bound for the SMC estimator; on the exact branch log Z is exact, so a "95% lower bound" is mislabelled. | Diff hunk v3_fit.R H7 (§2). It is not used by the rule rows or by R-1. | Drop the field on the exact branch, or label it "not applicable (exact)". The study is unaffected, because every study fit takes the SMC branch. |
| F3 | minor | `adapter.R:382-383` | An R-level `cannot allocate` / `bad_alloc` error leaves the unit without `.done`, so reconciliation later writes `not_run`/`timeout`. R-1 does not state this case. The README says this matches "benchmark infrastructure-failure handling". | It agrees with master §IV.2.4: OOM is an infrastructure failure with one resubmission at doubled memory. The benchmark code, however, has no such handler: `grep -rn "cannot allocate\|bad_alloc"` over `Benchmark_Study_20261019/code` returns nothing, so the benchmark's outer `tryCatch` records `failed`. Only the T2 failure category can change, and only if an OOM occurs. The T1 denominator is unchanged. | Lead to confirm or record this in R-1. No code change needed if confirmed. |
| F4 | minor (verification gap; closed by this audit) | `tests/worker.R` | A's 32-seed regression compares components and orchestration under substituted tiny budgets (H=9, T_e=64, L=1, ell=2–3, N=7–9). The public `v3_fit` at production budgets is never compared with the prototype's `v3_fit`. | `worker.R:43-45, 91-97`. | Closed here by three end-to-end production-budget comparisons, all identical (§5). Recommend adding such a case to A's suite. |
| F5 | minor (operations; outside A's code) | C_ops PILOT.md proposal (native `--hours 24` with external 30/90-min unit limits) | Part I §I.1 says to use the job's declared wall-time allocation. With hours = 24, the in-run guard can never fire before an external kill, so slow fits end as `timeout` (reconciliation) instead of `resource_limit` with partial results. | PILOT.md, "Provisional external unit limits" paragraph. | Lead and launcher decision: pass `--hours` equal to the real unit limit, or record why not. Either way the fit counts as non-recovery. |

Informational, no action needed: the adapter also reads `$STUDY/manifests/*inputs*.csv`. Its columns are only input hashes and seeds (header checked); the truth manifests are separate files that the adapter cannot select. The core needs a writable `code/core/.cpp_cache` on first compile; the prototype has the same requirement.

## 2. Every prototype-to-v2 diff hunk, with verdict

Method: `diff -u --strip-trailing-cr` for each file. `v3_score.h` and `v3_engine.h` differ in line endings only, apart from the hunks listed. I read every hunk in full. "OK" means the hunk is required by the cited authority and correctly implemented.

**v3.R**
- H1, default `V3_CORE_DIR` path. Path only. OK.
- H2, `v3_observer.R` no longer sourced. Part I scope (no profiling observer). OK.

**v3_exact.R**
- H1, `v3_reference` removed. Part I scope (no exact-reference oracle). OK.

**v3_preprocess.R**
- H1, anchored two-pass centring when `max|x/mx − mean| ≤ √ε`. R-5 B-N1. In that branch every entry lies within 3·10⁻⁸ relative of ±max, so `x − x[1]` is exact (Sterbenz). Ordinary columns keep the prototype arithmetic: bit-identical in the regression and in §5. The residual 1.9e-9 coordinate error was accepted by R-6. OK.
- H2, strict input validation: no data.frame or vector coercion, `y` with a `dim` is rejected, `typeof` is checked. R-5 B-N2 and Part I §I.1 step 1. OK.
- H3, `storage.mode(y) <- "double"` and `unname(y)`. Representation only. OK.
- H4, `stable_centering` map recorded only on the fallback path. Record only. OK.

**v3_setup.R**
- H1, scorer test hooks removed from `v3_context`. Excluded test controls. OK.
- H2, `v3_log1mexp`, `v3_start_logdeficit` and `v3_start_mode` removed. Profiling helpers. OK.
- H3, `B_override` removed; B = `budgets$B`. Part I §I.8 "Excluded switches"; C.R17. OK.

**cpp/v3_score.h**
- H1, failure hooks removed; mutable route, Q-recompute and failure counters added. These supply the §I.6 required record "numerical fallback routes". Factorisation, Q, log m, QR and η arithmetic are textually unchanged. OK.

**cpp/v3_ledger.h**
- H1, `DumpRec`, the dump map and the Observer pointer removed. Profiling (C.R15). OK.
- H2, `Ledger::event` moved from `v3_observer.h`. Verbatim apart from the dump block (compared line by line). OK.

**cpp/v3_holder.h and cpp/v3_runtime.h (new)**
- `Holder` moved verbatim out of `v3_core.cpp` (`diff` empty). OK.
- `RuntimeGuard`: one steady clock for the whole fit; the check is `elapsed + operation > allocation`, strictly; every checkpoint is recorded. Part I §I.1 / RULINGS_3 N6. OK.

**cpp/v3_engine.h**
- H1–H2, `PrescribedSource`, `Tracer` and `RecordingSource` removed. No trace replay. OK.
- H3, `IslandResult` gains phase/tier/iter/island/partial metadata; `offspring` removed. Metadata. OK.
- H4–H6, Engine fields: guard added; observer, tracer and prescribed orders/draws removed; `draw_start` always uses the exact π₀ draw. OK.
- H7, the four step functions: only observer and tracer lines removed. All `vs->u(...)` calls, their order, and the acceptance arithmetic are unchanged. OK.
- H8–H9, `draw_order`, `one_round`, `population_round`: prescribed and observer branches removed. Fisher–Yates is unchanged. OK.
- H10, resampler: `lower_bound` is replaced by a guide table. RULINGS_2 G2 and RULINGS_3 N3. The weight arithmetic and the `denorm_min` guard are unchanged. Proof of equivalence: W is nondecreasing and W_N = 1 > u_eff, because u ∈ [0,1). The forward loop ends at a k with W_k ≥ u_eff. The backward loop moves to k−1 only while W_{k−1} ≥ u_eff. It therefore ends at the first such k, which is exactly `lower_bound`, whatever bucket rounding gives. N uniforms are consumed and no extra draw is made. OK.
- H11–H12, `run_island` signatures and island metadata; init-draw tracer removed. OK.
- H13, stage loop: a per-stage timer and a guard check after each bridge stage, with a partial return. N6. OK.
- H14, `local_search`: only the observer line removed. The certificate logic (`no_improvement` sets `local_certified`) is unchanged. OK.

**cpp/v3_core.cpp**
- H1–H2, `Holder` include; `elem_name` and the hooks in `cpp_context` removed. OK.
- H3 and H13, certificate label "heuristic (not a validated interval bound)" in `cpp_score` and `cpp_enumerate`. Part I §I.2. The numeric η and margins are unchanged (the e2e exact case is identical). OK.
- H4, timing probe: cyclic window of exactly k* distinct columns. R-5 B-O2. Affects only the exact-branch time projection. OK.
- H5, `B_MAX` 20 → 16. M §3 B* = 16. OK.
- H6–H7, `cpp_start_mode`, the observer start quantities and `Observer::to_list` removed. Profiling. OK.
- H8–H10, `island_to_list` metadata; ledger dump and `tracer_to_list` removed; `RunOpts` local; `ingest_tables` without the observer. OK.
- H11, `cpp_final_run`:
  - Signature now carries runtime instead of observer, init_states, variates and trace.
  - Inherited rescoring moved inside `try` (R-5 containment). It uses its own scorer and no cache, after `ingest_tables` as before, so ledger order is unchanged.
  - Per-island stream record added.
  - A partial island gives `resource_limit` and stops.
  - The final local search runs only when completed, followed by a guard check.
  - On `NumericalFailure` only, the calibration HPM and its provenance are restored from the inherited record without rescoring.
  - OK.
- H12, `cpp_replicate`, `cpp_resample_sample`, the step and round samplers, `cpp_local_search`, `cpp_reference`, `cpp_pilot_schedule` and the observer new/report functions removed. Testing and profiling interfaces. OK.
- H14–H16, `CalState` gets the runtime guard; pilot and diagnostic runs return partial archives on a guard stop; a guard check follows each calibration local search. N6. OK.
- H17, `cpp_cal_V` catches `NumericalFailure` and returns `status = numerical_failure` (R-5 containment). A partly rescored V is never used. OK.
- H18, new exports:
  - `cpp_runtime_*` (N6).
  - `cpp_cut_group` (D4): uncapped `|r| ≥ √(2 log p/n)` graph from the standardised Gram, union-find, no forced partner, spans counted on the composite-start blocks `st.blk`, members as sorted original indices, NA on the exact branch.
  - `cpp_numerical_routes`.
  - OK.

**v3_calib.R**
- H1, `v3_pilot_schedule` test interface removed. OK.
- H2, `v3_cal_settings` fixed at H_e, T_e, L, Hm = 4 and ℓ from the budgets; all overrides removed. Part I §I.5/§I.8. OK.
- H3–H4, `fail()` preserves partial archives; pilot archive with `stage_record` and partial labels; failure checked after archiving. OK.
- H5, `switch_no_candidate_grid` (E4 arm) removed. Profiling. OK.
- H6, `build()`: a V `numerical_failure` goes to `fail`; a guard check follows each grid construction (N6); `rho_appended` is archived. OK.
- H7, diagnostic loop: the iteration is archived before the status check. E1/E2 are now assigned after each completed iteration rather than read from the last iteration after the loop. These are equivalent on the success path; on a failed rebuild, the last completed diagnostic is kept, which the prototype convention in §I.5 implies. OK.
- H8, on convergence `g <- gn` with an identical temperature vector. Only metadata changes. OK.
- H9–H12:
  - Calibration cache is 500p (R-5 B-O1).
  - The `calibration_seed` and `escalate` overrides are removed.
  - Flags are always assembled. `checks_passed_calibration` is NA only when the last tier failed; it is identical on success.
  - Calibration stage table and frozen ρ metadata are added outside the frozen hash (the frozen sha256 is identical in §5).
  - The observer calibration view is removed.
  - OK.

**v3_run.R**
- H1, `v3_randomness`: stream map 0–13, seeding and variate-order documentation. Part I §I.4 ("save that function and PRNG convention"). OK.
- H2, `v3_stage_table`: the §I.6 per-stage record with phase/tier/iter/island/grid labels, ρ_V and the specified denominators `max(·,1)`. OK.
- H3, `v3_run_settings` fixed: N_e, L, 4 measured rounds, 4 islands, ℓ, cache 500p. OK.
- H4, assembly: streams, stage records, local-search labels; the failure path keeps `partial_final` and sets both certificates FALSE. OK.
- H5, `pip_secondary` removed. DP2 D2. OK.
- H6, `local_certified <- isTRUE(ls$local_certified) && identical(hpm, ls$returned)`. RULINGS_2 finding 8 / §I.6. OK.
- H7–H8, dump, resampler trace, `v3_replicate_final`, `v3_trace`, the samplers and the `v3_local_search` wrapper removed; `v3_final_run` simplified. OK.

**v3_fit.R**
- H1, `v3_preflight`: SMC memory only. Every term matches §I.1 exactly: `8(3np+3p²) + 16⌈p/B⌉2^B + 8⌈p/B⌉(K+1)(B+1) + 29·2^⌈log₂(2C)⌉ + 4CK + (80p+1)(4K+64) + 2N(8W+4K+96)`, with C = 500p and N = 4^e N₀. Exact branch: `8(3np+p²) + 8(40p+1)(k*+8) + 32p` and E × s(k*), with the N4 label. G1/N4/N5. OK.
- H2, `v3_summary_json` / `out_dir` removed. Persistence moves to the caller. OK.
- H3–H6:
  - The signature is `(X, y, seed, allocation)`.
  - An invalid seed returns `invalid_input`.
  - The allocation is normalised. A malformed allocation raises an R error; it is an interface error, and the adapter validates the allocation first.
  - The runtime guard starts at fit start.
  - `branch_run = branch_decision` (no `force_smc`).
  - OK.
- H7, exact branch: provenance `exact/enumeration` (R-5 B-O5); no secondary PIP; `near_tie_F` retained; `log_Z_lower95` added (finding F2). OK except F2.
- H8–H11, `cut_group` after setup (D4); preflight before tier 1 recorded as `preflight_escalation`; calibration failure path; final stage table, flags and `cut_group` binding. OK.

Removed files: `v3_observer.R` and `cpp/v3_observer.h`, which are profiling only. Part I scope and C.R11. OK.

**Unexplained statistical changes: none.**

## 3. Study layer (`code/study/adapter.R`, `run_case.R`; launcher `build/launch.sh`)

| Requirement (§IV.1.2/§IV.1.4, R-1) | Finding | Evidence |
|---|---|---|
| Inputs only from `$STUDY/inputs`; never truth or holdout | Met. Only `inputs/pPPPP/<dataset_id>.rds` and an inputs manifest under `$STUDY/manifests` are read. Paths with a `truth` or `holdout` component are refused, both lexically and after canonicalisation. The file hash is checked against the manifest before `readRDS`. | adapter.R:26-35, 124-161. The generator writes truth to separate `truth/` files; the input record fields are X, Y, foldid, IDs, seeds and scales (`gen_prod_data.R:45-49`). |
| Method seed = data seed + 4,000,000 | Met. The bases match master §II.7 (prod 1,410,000/1,510,000; dev 2,410,000/2,510,000; fold 3,410,000/3,510,000, dev fold 4,410,000/4,510,000). The seed is cross-checked against the input record and the manifest. | adapter.R:88-95, 144-147. Smoke rows: 2420001→6420001, 2520001→6520001; C pilot: 2450001→6450001, 2550001→6550001. |
| Hash fields | Met. `inputs_sha256` is the on-disk RDS; `x_sha256` and `y_sha256` are float64 little-endian hashes of the stored arrays before standardisation, using the same function as the benchmark generator (`gen_dev_data.R:44-47`). The fold hash is validated, but NA on the rows per R-1. | adapter.R:14-16, 154-158, 294 |
| Two rule rows | Met. `hpm`/`primary` and `pip05`/`S0`, in that order. The MPM is checked to equal strict primary PIP > 0.5. | adapter.R:102-104, 207-208, 267 |
| Failure semantics | Met, except the F3 note. `exact`/`completed` give `ok`, or `warning` iff an R condition was captured. Every other native status gives `failed`. A failed row has `k` and `support` NA, with any returned support in `support_audit`. `converged` is NA. `diag_flag` follows R-1 (a)–(d), including on failed fits, with `local_limit` OR-ed over every archived search. Informational codes never set the flag. The adapter never writes `timeout` or `not_run`. | adapter.R:239-299; README "Binding status" |
| Launcher (`build/launch.sh`) | Owls only; nice 19; `ulimit -v` 2 GiB; refuses to overwrite; load and memory admission check. Operational; no statistical effect. | launch.sh |

## 4. Regression rerun on Owls (run once), and the normalisation question

Command, run as `nice -n 19` with `ulimit -v 2097152`, one sequential process, under `source build/env.sh` (R 4.6.0 / GCC 11.5.0 asserted):

```sh
bash /home/fb31/smcbvs_v3_deploy_20261022/A_build/v2/tests/run_all_seeds.sh \
  /home/fb31/smcbvs_v3_deploy_20261022/A_build/v2/reference/prototype_core \
  /home/fb31/smcbvs_v3_deploy_20261022/A_build/v2/code/core \
  ~/smcbvs_v3_deploy_20261022/AUDIT_CLAUDE/A_CODE/regression_v2_acode
```

I did not use `launch.sh` because it forces outputs under `A_build/runs`. `run_all_seeds.sh` is the same suite invocation that `job.sh tests` makes.

Result:
- Started 2026-10-23T00:57:52Z, finished 01:01:00Z (wall 3:08.29, peak RSS 517192 KiB).
- `suite_exit_status = 0`; `SUITE_SUMMARY.md` says "Overall: PASS", **32/32 seeds**.
- Every seed shows `prototype 0 / production 0 / comparison 0` and `Checks: 28 Failures: 0` (32 × 28 = 896 checks, as in HANDOFF_v2).
- My seed-1 `REPORT.md` is byte-identical to A's saved `evidence/owls/v2/runs_v2regression_tests_seed_1_REPORT.md` (`diff` empty).

Hashes:

| File | SHA-256 |
|---|---|
| `SUITE_SUMMARY.json` | `4899ad47…ae49478` |
| `SUITE_SUMMARY.md` | `db86b658…eb1fc5` |
| seed-1 and seed-32 `REPORT.md` | `6f7723f2…fa96a` |

Scratch deleted afterwards.

**Does any normalisation hide a real difference? No.** From `tests/compare.R`:
- **Cache capacity.** `normalize_calibration_capacity` replaces only `calibration_full$cache[["capacity"]]`, after first asserting that both capacities are exactly the expected 500p and max(500p, 2¹⁵). Hits, misses, inserts and clears are still byte-compared, and a mutation test (`compare.R:113-120`) shows that a +1 change in any counter fails. Both sides' direct final runs receive the same `ro$cache_capacity` (`worker.R:45`).
- **Can capacity change results structurally?** No. Stores are idempotent top-k sets (`TopStore::offer` deduplicates, and a re-offer after eviction is rejected because the worst entry only improves), and they are offered at each model's first fresh score. HPM is a running maximum. `island_best` updates on every event. Capacity therefore affects only cache and fresh-score counters and runtime.
- **Empirical confirmation.** In §5, v2 cleared its cache 6 and 54 times against the prototype's 1 and 33, and every statistical output was identical.
- **Other projections.** The other normalisations are:
  - removal of additive metadata (phase/tier/iter/island/stream, `partial` after asserting FALSE, calibration `stage_table`, ρ labels, timings, `stage_record`);
  - mapping of the two certificate label strings, with the numbers retained;
  - name-order sorting, with field sets still strict;
  - in `final`: dropping the stream documentation, keeping only shared stage-table columns, dropping `pip_secondary` after asserting it is present in the prototype and absent in v2, and replacing `local_certified` with the Part I rule computed from the prototype's own output.
  
  Island numerics remain compared through `raw_final`, `final_inherited`, `calibrated_final`, `micro` and `pilot_micro`. None of these projections masks a numeric or statistical field.

## 5. Independent end-to-end check at production budgets (my own, Owls, single cases)

Gap F4 means the regression never runs `v3_fit` at production budgets against the prototype. I copied both cores into my scratch and ran each implementation's public `v3_fit(X, y, seed, allocation = list(mem_gb = 2, hours = 24))`, with the prototype at its production defaults, on three synthetic cases. Each case is block-correlated Gaussian X (ρ = 0.6, blocks of 5), with active set {1, 7, 13, 20}. I then compared outputs with `identical()`:

| Case | Branch | Checks identical | Highlights |
|---|---|---|---|
| n=200, p=30, data seed 20261031, method seed 777 (the §I.7 Regime-L shape: K=30, B=5) | SMC | 52/52 | HPM {1,7,13,20}; log Z = −181.499276418286; tier 0, 9 stages. Cache: prototype capacity 32768 with 1 clear, v2 capacity 15000 with 6 clears. Logical score counts identical; fresh counts differ, as expected. `cut_group` TRUE. 121 guard checkpoints. |
| n=120, p=48, data seed 20261032, method seed 4242 (B=6) | SMC | 52/52 | log Z = −124.059628858122; 17 stages. Cache: 33 clears vs 54. |
| n=20, p=12, data seed 20261033, method seed 99 | exact | 26/26 | `exact$log_Z`, PIPs, HPM, `hpm_F`, models scored, margin, η and certificate bound all identical. v2 provenance `exact enumeration`; `cut_group` NA. |

The SMC comparisons cover:
- status, budgets, B, HPM and `hpm_F` bits, primary PIP bits, MPM;
- pooled and per-island log Z bits, per-stage increments, `pip_r`, RB accumulators;
- final and frozen grid, frozen sha256, tier, blocks, neighbours, log Z̄₀;
- E1/E2/E3, low ESS, `checks_passed_final`, escalated, `grid_unconverged`, forced steps, `checks_passed_calibration`, `local_limit`;
- island bests, both leader stores, top store, near ties and truncation;
- local-search path and returned model, `local_certified` = Part I rule;
- logical score counts, terminal table, shared final stage-table columns;
- per-tier pilot schedule, grid, triggers, rebuild count and diagnostic log Ẑ_r.

`OVERALL IDENTICAL` in all three cases (COMPARE.txt SHA-256 `f1ebf44a…`, `222ab2b5…`, `7e9bebf6…`). These cases do not exercise escalation to tier 1. Escalation and the tier-1 pilot and diagnostics are covered by A's regression at tiny budgets.

## 6. Saved smoke records (inspected, not rerun)

**A's v2 smokes**, in `C:/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/A_build/`:
- The archive `v2_smokes_pass.tar.gz` and both RDS files match HANDOFF_v2 (`de13c86f…`, `19c0f1c3…`, `5a30a04b…`).
- p500 / p1000:
  - Settings: N = 2500, L = 8, ℓ = 10/11, cache 250000/500000; calibration H = 512, T_e = 1000, tier 0.
  - Status `completed`. MPM equals strict PIP > 0.5. `pip_primary` equals `rowMeans(pip_r)`. Pooled log Z recomputes exactly (−81.8117680282139 / −87.5937389046695).
  - All final ρ_V values are at least 0.90, one per frozen interval (35 / 31).
  - `local_certified` TRUE with returned == HPM.
  - Cut-group threshold equals √(2 log p/n). One guard checkpoint per stage row (587 / 769), plus grid and local-search checkpoints.
  - Routes: Cholesky only.
  - Rule rows: hpm/primary and pip05/S0, `ok`; `diag_codes = cut_group`; `diag_flag` FALSE.

**C's pilot** (`pilot/smoke_v2_20261022T2315Z/…`):
- All four RDS and CSV hashes match PILOT.md.
- In both fits, E1, E2, E3, low-ESS and `checks_passed_final` recompute exactly from the stored quantities.
- For p1000 S4: sd(log Ẑ_r) = 1.2436535544 > 1, so E2 = TRUE and `checks_passed_final` = FALSE. Both rows are correctly `ok` with `diag_flag` TRUE and `final_check_E2;cut_group`, as R-1 requires.
- This is a genuine method diagnostic on one of the two dev fits, not a code defect.

## 7. Not verified

- **Owls only.** NOTS build and regression (GCC 14.3 / R 4.5.2) were not run (no NOTS per contract), so bit-identity on NOTS remains to be shown. F1 is relevant there.
- **Not re-tested.** I did not rerun the adapter contract tests (76 checks) or B's oracles. The adapter was reviewed by reading the code and against the saved smoke and pilot rows.
- **Guard paths read, not executed.** The runtime-guard stop paths and the containment failure paths were reviewed in code and are covered by A's v2 units, which passed in my rerun. I did not trigger them at production budgets.

## Final verdict

**SOUND WITH FIXES.**
- **No unexplained differences.** Every prototype-to-v2 difference is required by Part I, CHANGES.md, R-1 or R-5, and each is correctly implemented. No statistical change is unexplained.
- **Evidence.**
  - The prototype regression passes 32/32 on rerun.
  - Its normalisations hide nothing.
  - At production budgets, v2 is bit-identical to the verified prototype on all statistical outputs, including under different cache-clear histories.
- **Study layer.** The study layer reads only inputs, applies the specified seed and hash definitions, writes the two R-1 rule rows and implements the R-1 failure semantics.
- **Fixes.** The four fixes are minor:
  - F1: make the source-hash ordering locale-independent, or check it on NOTS before mixing hosts.
  - F2: relabel or drop the exact-branch lower bound.
  - F3: the lead confirms the OOM-as-infrastructure handling.
  - F5: the lead or launcher aligns `--hours` with the real unit limit.
  
  None of them blocks deployment of the method code.
