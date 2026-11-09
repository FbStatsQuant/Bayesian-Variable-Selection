# C-ENG — REPORT: LS0 and the e4 tie-aware DP merged into the production core

Ticket C-ENG, Theory Wave 1C. Lead: Claude Opus 5.5 (Claude Work). Branch **`w1c/ls0-merge`** (pushed to origin; head commit
in the final message). Base: `f16ce15` (main). Not merged; main untouched.

**RESULT: DONE (implemented, tested, code reviews APPROVE).** HQ-forwarded method requirements C-PACK MR1–MR3 implemented
and tested (§1b). Open: see §6.

## 1. What changed (production code; `git diff f16ce15 HEAD -- Scripts/SMC_BVS`)

Switch: `v3_fit(X, y, seed, allocation, ls0 = getOption("v3.ls0", TRUE))`. **Default = v3.1 (LS0 on).** `ls0 = FALSE`
(or `options(v3.ls0 = FALSE)`) reproduces the v3 fit (checked 48/48, §3c). Test-only options: `v3.ls0_tie_dp = FALSE`
(v3 start-mode rule inside LS0), `v3.ls0_ell` (LS0 move cap; hook for an HQ ℓ_n schedule — none received).

| file | lines (new numbering) | change |
|---|---|---|
| `Scripts/SMC_BVS/core/cpp/v3_start.h` | 178–304 | `start_mode` refactored into `mode_dp` (identical arithmetic) + enumeration fast path (unchanged); new `mode_tight`, `mode_tie_dp` (**TDP-E**, e4 fallback); `start_mode(st, cap = 1e6, tie_dp = true)`: on truncation (count ≥ cap) and `tie_dp`, result := TDP-E; `ModeResult.tie_dp_used`; root-feasibility check throws instead of returning an empty model |
| `Scripts/SMC_BVS/core/cpp/v3_ledger.h` | 8–18 | phase `PH_LS0` ("ls0") appended last (no index shift) |
| `Scripts/SMC_BVS/core/cpp/v3_engine.h` | 376–381 | `local_search(..., iter, phase = PH_LOCAL)` — phase label argument |
| `Scripts/SMC_BVS/core/cpp/v3_runtime.h` | 32–33 | `local_event(tier, iter, phase = PH_LOCAL)` |
| `Scripts/SMC_BVS/core/cpp/v3_core.cpp` | 56–62, 363–369, 394–402, 412–413, 458–475, 504, 510 | `counter_matrix`/`ledger_to_list` serialise the `ls0` row only when LS0 is on (calibration never); `cpp_final_run` reads `ro$ls0`, `ro$ls0_tie_dp`, `ro$ls0_ell`; after the final local search + its guard check, on a completed run: `hpm_before_ls0`, `start_mode`, `local_search(S̃₀, ls0_ell, tier, emit_centre = true, -1, PH_LS0)`, guard checkpoint `"ls0"`; outputs `ls0`, `hpm_before_ls0`, `start_mode`, `seconds_ls0` only when on |
| `Scripts/SMC_BVS/core/v3_run.R` | 84–108, 128–135, 142, 180–195, 201–202, 211, 218–221 | `v3_run_settings(..., ls0)`; `V3_ESTIMATE_FIELDS`, `v3_unavailable_estimates()` (#15); assembly: `ls0` archive, `start_mode`, `hpm_before_ls0`; **E3 from the HPM before LS0**; `local_certified` = final-certified ∧ HPM = final endpoint, OR LS0-certified ∧ HPM = LS0 endpoint (`local_certified_by`); `local_limit` = final OR LS0 cap (`final_local_limit`, `ls0_local_limit`); flags `ls0_improved` (strict F increase), `ls0_hpm_changed`; NA fields on the no-output branch; `timings$ls0` |
| `Scripts/SMC_BVS/core/v3_fit.R` | 49–51, 63, 137 | `ls0` argument; NA estimate fields on every return with `estimates_available` not TRUE (v3.1 mode) |
| `Scripts/SMC_BVS/study/adapter.R` | 185–190, 198, 202, 209 | `smcbvs_estimate()`: a scalar NA estimate marker = unavailable (pre-v3.1 cores omit the field) |
| `Scripts/SMC_BVS/core/README.md` | 37–60 | v3.1 merge section |

## 1b. Method requirements forwarded by HQ (C-PACK, `Theory_work/Wave1C/C-PACK/METHOD_REQUIREMENTS.md`, council-passed)

| MR | requirement (short) | implementation | test / evidence |
|---|---|---|---|
| MR1 | integrated LS0 starts from and emits `start_mode(st, cap).S` computed on the run's own `Start`; a replacement routine must return the maximiser when it is unique | `cpp_final_run`: `start_mode(st, 1000000, tie_dp)` on the setup's `Start` (built by `build_tables`/`build_start` in `cpp_setup`), then `local_search(m.S, …, emit_centre = true, …, PH_LS0)` (`cpp/v3_core.cpp:467–471`). LS0 exists only on the SMC branch (the exact branch enumerates and has no `Start`/LS0). TDP-E returns S* under exact arithmetic, hence the unique maximiser when it is unique | `numerics/out_test_ls0_normal.txt` "MR1" (centre == independent `start_mode(st, 1e6).S` on the same setup, same log γ₀) and the exact LS0 event count = 1 + n_evaluated; p = 30 regression `ls0_centre_is_mode` 48/48 |
| MR2 | if the fallback is triggered by `truncated`, keep cap ≥ 2 | `start_mode(st, cap, tie_dp = true)` throws `std::invalid_argument` for cap < 2 (`cpp/v3_start.h:272`); production cap 10⁶. With cap ≥ 2 a unique maximiser (\|E\| = 1) always returns through the enumeration path (count 1 < cap), so Lemma UM-FP's code path is unchanged | `numerics/out_test_tdp_seed*.txt` "[MR2]": cap 1 rejected 3000/3000 per seed; on the 1952 + 2009 instances with \|E\| = 1 the fallback was used 0 times at every cap ≥ 2 and the returned set was the maximiser in all; `out_test_ls0_normal.txt` "MR2" on a production setup |
| MR3 | no consistency result needs the size-then-lex rule; choose it for reproducibility | rule kept (spec #8) for reproducibility; documented in `cpp/v3_start.h:185–187` and the core README | — |

R04 (fresh Codex review of the MR2 delta and the harness edits): APPROVE, no findings (`reviews/R04_delta_review_raw.md`).

Spec mapping (`NBH/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md`): #8 LS0 (when, centre, rules, no uniforms, all scored
models join the stores, provenance `ls0`, `ls0_improved`, no E3, e4); #6 GUARD-W (LS0 stop / numerical failure in LS0 ⇒ no
output; capped LS0 is not a stop); #9 (flags/near ties recomputed on the returned model; store = top_c(old ∪ added)); #10
(certificate on the returned Ŝ; L1 card itself not implemented — spec-only POST HOC); #15 (exact-name NA fields).
Interpretations fixed with the reviewers (R01 Q1–Q4): public `local_limit` = either cap; E1 on the post-LS0 HPM; ℓ_LS0 =
production ℓ; e4 = TDP-E (below).

**e4 / TDP-E** (`lemmas/TDP_E.md`): returns lex-min of the enumeration's tie set E (sets whose per-block choices attain the
per-block maxima and the DP maxima exactly) by index-by-index feasibility over tight DP edges, never listing E. In binary64
under the stated hypotheses this equals the uncapped enumeration's result for every cap; under exact arithmetic E = 𝒜*
so it returns the prescribed S* (W1-N3). It does **not** claim lexicographic optimality over all rounded log γ₀
maximisers (R01 #2 example; neither the old fast path nor the fallback provides that). When the enumeration is not
truncated the legacy result fields (S, lg0, ties, truncated) are unchanged.

## 2. Review trail (verbatim replies in `reviews/`)

| id | what | reviewer | verdict | file / disposition |
|---|---|---|---|---|
| R01 | PLAN v1.0 vs spec/code | Codex gpt-6.1-sol high (fresh) | REJECT (1 BLOCKER, 4 MAJOR, 2 MINOR) | `R01_plan_review_raw.md`; all accepted → PLAN v1.1 (`R01_disposition.md`) |
| R02 | PLAN v1.1 + TDP_E.md re-check | Codex gpt-6.1-sol high (fresh) | REJECT on plan text; R01 #1–#7 all RESOLVED; 2 MAJOR, 2 MINOR | `R02_plan_recheck_raw.md`; adapter already fixed in code; public-path gate added; wording fixed → PLAN v1.2 (`R02_disposition.md`) |
| R03 | code diff f16ce15..9b9d234 | Codex gpt-6.1-sol high (fresh) | **APPROVE, no findings** | `R03_code_review_raw.md` (source review + in-memory R checks; did not rebuild) |
| R04 | post-R03 deltas: MR2 guard (9b9d234..36c0cfe) + harness assertion edits | Codex gpt-6.1-sol high (fresh) | **APPROVE, no findings** | `R04_delta_review_raw.md` (MR1/MR2 checked against C-PACK text) |

After R03 the only production-code change is the MR2 guard (4 lines in `cpp/v3_start.h`), reviewed in R04. The harness edits
(two assertions in `Scripts/SMC_BVS/tests`) were reviewed in R04. Per the brief a second full review was required only if the
first found something major; it did not.

## 3. Tests and results (scripts in `tests/`, outputs in `numerics/`; local Windows, R 4.6.1, Rtools45, Rcpp 1.1.2)

(a) **TDP unit tests** — `tests/test_tdp.R`; `numerics/out_test_tdp_seed20261108.txt`, `numerics/out_test_tdp_seed7.txt`:
2 × 3000 random instances (integer, flat-tie and real tables; random block order; K binding; NaN above K), caps 1, 2, 3,
5, 17, 10⁶: new `start_mode` == lex-min E (uncapped enumeration) 6000/6000 at every cap; == brute-force S* on all 4000
exact-arithmetic (integer/flat) instances; TDP-E alone == S* 4000/4000; legacy fields unchanged whenever not truncated
6000/6000; lg0 and |S| == brute force 6000/6000. The old rule is wrong on 190/3000 and 169/3000 instances at cap 1.
**W1-N3 counterexample (p = 44, K = 22, cap 10⁶):** old returns {0,2,…,38,41,42} (≠ S*), new returns S* =
{0,2,…,38,40,43}, `tie_dp_used = TRUE`, log γ₀ = 25 (TDP-E < 0.01 s; total 6–7.5 s incl. the 10⁶-set enumeration).
Family of W1-N3 L6 at all caps ≤ 2^{m+1}+1, m ≤ 8: 0/1031 mismatches. Rounding fixtures (R01 #2 2⁵⁴ example, prefix, block
sum) and boundary fixtures (K = 0, K binding inside a block, interleaved blocks, empty optimum): all as specified.
Cross-check vs W1-N3's exact reference `tdp.py` (`tests/xcheck_n3_tdp.*`, `numerics/out_xcheck_n3_tdp.txt`): 600 integer
instances, 0 mismatches (cap 1 fallback, cap 10⁶ enumeration, lg0).

(b) **LS0 behaviour** — `tests/test_ls0.R`:
- `normal` (`numerics/out_test_ls0_normal.txt`, **33/33 PASS**): integrated LS0 event count = 1 (emitted centre) +
  n_evaluated, all mechanism `local_scan`; standalone LS0 equals the integrated one; emitting vs not emitting a
  local-maximum start mode changes the standalone HPM (provenance ls0, stage 0, position 0) — omission is observable;
  `ls0_improved`/E3 formulas; ℓ_LS0 = 0 with a strict improving neighbour ⇒ `move_limit`, `ls0_local_limit`, public
  `local_limit` TRUE, status completed with estimates; **equal-F HPM tie change by LS0** (duplicated columns 6:=7,
  15:=16; four models with bitwise-equal F): `ls0_hpm_changed` TRUE, `ls0_improved` FALSE, provenance `ls0`, E3 not fired,
  final-search tie change leaves the HPM ≠ the final search's endpoint, certificate from LS0 (`local_certified_by = "ls0"`);
  switch-off on the same fixture: no LS0 fields, v3 counter layout, islands identical, HPM = pre-LS0 HPM.
- `stop` (`numerics/out_test_ls0_stop.txt`, **9/9 PASS**; testing copy whose guard trips at checkpoint `ls0`):
  `resource_limit`, `estimates_available` FALSE, `fit[["log_Z", exact = TRUE]]` and `fit$log_Z` NA, all 8 fields NA,
  guard record shows `ls0` exceeded, LS0 archive kept, adapter maps it to unavailable PIPs.
- `numfail` (`numerics/out_test_ls0_numfail.txt`, **5/5 PASS**; NumericalFailure injected at LS0's 5th score):
  `numerical_failure`, all estimate fields NA, `hpm_incomplete`.
- `paths` (`numerics/out_test_ls0_paths.txt`, **10/10 PASS**): local analogue of API-AUDIT's forced-stop table: 10/10
  public `v3_fit` stops at 0.05 s (checkpoint `bridge_stage`, pilot) are `resource_limit`, unavailable, `hpm_incomplete`,
  8/8 fields NA, `fit$log_Z` NA (not `log_Zbar0`), adapter OK; y_constant, no_predictors, preflight stop, invalid seed:
  NA fields (+ adapter); exact branch: finite estimates, no LS0; completed fit: adapter MPM = PIP > .5; switch-off stop =
  v3 output.

(c) **Regression, S1–S6** — `tests/run_batch.R`, `tests/compare_regress.R`; `numerics/out_regress_p30.txt`, logs
`numerics/regress_logs/`: study covariances S1–S6 and the generator's p = 30 truth pattern, n = 100, replicates 1–4,
scales 1 and 0.5 (48 datasets; local inputs, not study data), all on the SMC branch, all completed. Old core (f16ce15) vs
new core LS0 off vs new core LS0 on vs O-LS0 prototype (`cpp_final_run_ls0`, `origin/theory/O-LS0` 02348e2):
- LS0 off == old, every field except timings/peak memory: **48/48**.
- LS0 on: stage records, Ẑ, PIPs, MPM, streams, calibration, frozen, island bests, final local search: identical
  **48/48**; E2/low-ESS identical; E3 identical (LS0 does not fire E3) 48/48; final-search `local_limit` identical 48/48;
  HPM unchanged 48/48 (`ls0_improved` 0, consistent with O-LS0's 0/2,394); LS0 counters = archive (centre emitted) 48/48;
  other counter rows identical 48/48; top store: every new-only model is an LS0 centre or neighbour, and every old model
  ranked above the new store's worst is retained, 48/48 (top_c(old ∪ added), #9); start mode never truncated.
- **Merged-LS0 replay vs the O-LS0 prototype** (same data/seed; provenance phase local/iter −2 normalised to ls0/−1; the
  prototype's `local` row = new `local` + `ls0` rows): status, islands/Ẑ/PIPs, HPM + provenance, all three stores, LS0
  archive, start mode, counters, cache statistics, HPM before LS0: identical **48/48**.

(c2) **Replay designs at production size** (SPEC §6 item 2; dev generator, p = 500, n = 200, c100: S1 r001, S4 r001,
S5 r002) — `tests/run_replay.R`, `tests/compare_replay.R`, `numerics/out_replay_p500.txt`: PENDING (filled below).

(d) **Existing tests** — `Scripts/SMC_BVS/tests` (prototype-vs-production bit-comparison harness), run locally on Windows
for seed indices 1–3 by a Sonnet helper (`numerics/existing_suite/REPORT_suite.md`; substitutions: no Owls hostname/nice
check, `python` for `python3`, `prepare.py` wrapped for `os.getpriority`/`lscpu`, short compile-cache path for MAX_PATH;
same Windows toolchain for both sides). Original core (A): 28/28 compare checks per seed, summarize PASS. New core,
original harness: B (ls0 off) and C (ls0 on) fail only `production_api_has_no_test_controls` (new formal `ls0`) and, in C,
`v2_inherited_rescore_failure_…` (new `ls0` counter row and NA estimate markers on a failed return) — both expected v3.1
interface changes; all 26 bit-for-bit checks pass. Harness assertions updated minimally for the v3.1 interface
(`Scripts/SMC_BVS/tests/changed_units.R:2–5`, `v2_runtime_units.R:120–135`; the `ls0` row is dropped only after checking it
is all zero; NULL or scalar NA accepted as "unavailable"; R04 APPROVE). Rerun with the updated harness on the MR2 core:
**B2 (ls0 off) 28/28 and C2 (ls0 on) 28/28 on each of seeds 1–3, summarize PASS** (`numerics/existing_suite/rerun_v31.log`,
`B2_new_ls0off_v31harness/`, `C2_new_ls0on_v31harness/`). Caveat (helper): the harness builds `ro` by hand without `ls0`, so
it does not execute LS0 itself; LS0 is covered by (b), (c), (c2). Only 3 of the 32 seed indices; not the Owls 32-seed gate.
`build/check_smokes.R` inspects saved Owls smoke records (`runs/*/exit_status.txt`, adapter outputs) that do not exist
locally, so it was not run; the public-path tests in (b) `paths` exercise the same adapter contract on local fits.

## 4. Files produced
`PLAN.md` (v1.2), `LOG.md`, `CHECKPOINT.md`, `REPORT.md`, `lemmas/TDP_E.md`, `reviews/R01_*`, `R02_*`, `R03_*`,
`tests/` (ceng_load.R, ceng_exports.cpp, test_tdp.R, test_ls0.R, run_batch.R, compare_regress.R, proto_load.R,
o_ls0_exports.cpp [verbatim prototype], run_replay.R, compare_replay.R, xcheck_n3_tdp.R/.py), `numerics/` (outputs above).

## 5. Notes for HQ
- The ls0 switch also gates the #15 NA fields, so `ls0 = FALSE` is exactly v3 (including stop outputs).
- Windows note: `long` is 32-bit on Windows; production cap 10⁶ fits, but a cap above 2³¹−1 would overflow there (Linux
  production unaffected).
- Parallel R processes sharing one sourceCpp cache fail to load on Windows (observed); the core's cache logic is unchanged
  (it targets Linux clusters).

## 6. Not done / open
- `source_manifest.json` not refreshed (its updater `build/update_core_manifest.py` targets the deployment layout and LF
  checkouts); refresh on an LF checkout before deployment. Any copy that pins source hashes (e.g. O-LS0's `ls0_core.R`)
  will reject the new core until then.
- The frozen study core `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/` is NOT changed (frozen snapshot); a
  port is mechanical (same hunks; it additionally has plain PIPs and the scored-set registry).
- The original API-AUDIT 10 forced-stop fits are not replayed (their inputs/scripts are not in the repository); a local
  analogue is in (b) `paths`.
- `build/check_smokes.R` and the 32-seed harness gate on Owls: not run (local only); seeds 1–3 run locally (§3d).
- The certificate card (L1 etc.), stacking/c₄ search, concurrency layer and NA fields for `schedule_limit` statuses not
  produced by this core are outside this ticket.
- Owls/NOTS execution (production-size timing, `build/check_smokes.R` on saved smoke records) not done (local only).
