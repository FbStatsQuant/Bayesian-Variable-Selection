# C-ENG — REPORT: LS0 and the e4 tie-aware DP merged into the production core

Ticket C-ENG, Theory Wave 1C. Lead: Claude Opus 5.5 (Claude Work). Branch **`w1c/ls0-merge`** (pushed to origin; head commit
in the final message). Base: `f16ce15` (main). Not merged; main untouched.

**RESULT: DONE (implemented, tested, every production change reviewed; final reviews APPROVE).** HQ-forwarded method
requirements implemented, tested and reviewed: C-PACK MR1–MR3 (§1b); C-GROW MR1, C-DLV A.2 (TDP-IMPL), C-DLV B with the
HQ_AUDIT precision, and the LS0 worst-case preflight term (§1c). Study outputs:
0 `schedule_limit` fits (§1c). Open: see §6.

## 1. What changed (production code; `git diff f16ce15 HEAD -- Scripts/SMC_BVS`)

Switch: `v3_fit(X, y, seed, allocation, ls0 = getOption("v3.ls0", TRUE))`. **Default = v3.1 (LS0 on).** `ls0 = FALSE`
(or `options(v3.ls0 = FALSE)`) reproduces the v3 fit entirely — no LS0, no NA fields, no calibration fallback (checked 48/48
on the final code, §3c). Per-item switches inside v3.1 mode: `v3.ls0_cap = "ell_n"` (LS0 cap ℓ_n instead of ℓ_n + |S̃₀|),
`v3.grid_fallback = FALSE` (v3 `schedule_limit`), `v3.ls0_tie_dp = FALSE` (v3 start-mode rule); test-only `v3.ls0_ell`
(LS0 base cap, validated whole number in [0, 10⁶]).

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
| `Scripts/SMC_BVS/core/v3_calib.R` | 28, 120–126, 141–190 | C-DLV B tier-1 fallback grid (§1c) |
| `Scripts/SMC_BVS/tests/changed_units.R`, `v2_runtime_units.R` | 2–5; 120–135 | harness assertions for the v3.1 interface (§3d) |
| `Scripts/SMC_BVS/core/README.md` | 37–61 | v3.1 merge section |
(Line numbers of `v3_core.cpp`/`v3_run.R`/`v3_fit.R` in this table refer to the first implementation commit 9b9d234; the
later wave-2 hunks are listed in §1b/§1c with HEAD numbering.)

## 1b. Method requirements forwarded by HQ (C-PACK, `Theory_work/Wave1C/C-PACK/METHOD_REQUIREMENTS.md`, council-passed)

| MR | requirement (short) | implementation | test / evidence |
|---|---|---|---|
| MR1 | integrated LS0 starts from and emits `start_mode(st, cap).S` computed on the run's own `Start`; a replacement routine must return the maximiser when it is unique | `cpp_final_run`: `start_mode(st, 1000000, tie_dp)` on the setup's `Start` (built by `build_tables`/`build_start` in `cpp_setup`), then `local_search(m.S, …, emit_centre = true, …, PH_LS0)` (`cpp/v3_core.cpp:467–471`). LS0 exists only on the SMC branch (the exact branch enumerates and has no `Start`/LS0). TDP-E returns S* under exact arithmetic, hence the unique maximiser when it is unique | `numerics/out_test_ls0_normal.txt` "MR1" (centre == independent `start_mode(st, 1e6).S` on the same setup, same log γ₀) and the exact LS0 event count = 1 + n_evaluated; p = 30 regression `ls0_centre_is_mode` 48/48 |
| MR2 | if the fallback is triggered by `truncated`, keep cap ≥ 2 | `start_mode(st, cap, tie_dp = true)` throws `std::invalid_argument` for cap < 2 (`cpp/v3_start.h:272`); production cap 10⁶. With cap ≥ 2 a unique maximiser (\|E\| = 1) always returns through the enumeration path (count 1 < cap), so Lemma UM-FP's code path is unchanged | `numerics/out_test_tdp_seed*.txt` "[MR2]": cap 1 rejected 3000/3000 per seed; on the 1952 + 2009 instances with \|E\| = 1 the fallback was used 0 times at every cap ≥ 2 and the returned set was the maximiser in all; `out_test_ls0_normal.txt` "MR2" on a production setup |
| MR3 | no consistency result needs the size-then-lex rule; choose it for reproducibility | rule kept (spec #8) for reproducibility; documented in `cpp/v3_start.h:185–187` and the core README | — |

R04 (fresh Codex review of the MR2 delta and the harness edits): APPROVE, no findings (`reviews/R04_delta_review_raw.md`).

## 1c. HQ wave-2 requirements (C-GROW MR1, C-DLV A.2 TDP-IMPL, C-DLV B + HQ_AUDIT precision)

Sources: `Theory_work/Wave1C/C-GROW/METHOD_REQUIREMENTS.md`, `Theory_work/Wave1C/C-DLV/METHOD_REQUIREMENTS.md` (§A, §B),
`Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md` ("Pilot-grid and failure-branch attack", "Exact corrected statement").
Every item is behind a switch; default = new behaviour; `v3_fit(..., ls0 = FALSE)` still reproduces v3 entirely.

| req. | implementation | switch (old behaviour) | test / evidence |
|---|---|---|---|
| **C-GROW MR1** LS0 move cap ℓ^{LS0} = ℓ_n + \|S̃₀\| | `cpp_final_run`: `ls0_cap = ls0_ell + \|m.S\|` (64-bit checked addition, R05 #2) with `ls0_ell` = ℓ_n (`ro$ell`), applied only to the LS0 `local_search`; the final local search keeps ℓ_n; archive `ls0$move_cap`, `ls0$move_cap_rule` (`cpp/v3_core.cpp:403–404, 473–479`; `v3_run.R:93–101`) | `options(v3.ls0_cap = "ell_n")` | `numerics/out_test_ls0_wave2.txt`: default fit move_cap = 8 + 3; switch gives 8 with identical final search/Ẑ/PIPs; binding fixture (base cap 0): rule ℓ_n stops at `move_limit`, rule ℓ_n + \|S̃₀\| completes the same descent/HPM as the production run |
| **C-DLV A.2 TDP-IMPL** | unchanged `mode_tie_dp` (TDP-E). Same maximiser: under EX-A, E = 𝒜* (W1-N3 (b)), so TDP-E = lex-min 𝒜* = S* = W1-N3 TDP's output (checked: `out_xcheck_n3_tdp.txt` 600/600, `out_test_tdp_*` [C]). **Operations:** `mode_dp` O(Σ_b 2^{\|C_b\|} + J(K+1)(B+1)); per index i: one row refresh O(2^{\|C_{b(i)}\|}) (twice on rejection) + one reachability pass O(Σ_b (K+1)(t_b+1)) ≤ O(J(K+1)²); total O(p·(2^B + J(K+1)²)) ⊆ O(p·Σ_b(2^{\|C_b\|}+(K+1)²)). **Storage:** `mb` Σ_b(t_b+1), `arg` ≤ Σ_b 2^{\|C_b\|} codes, `M` and `reach` (J+1)(K+1), `allowed` Σ_b(t_b+1), masks J: O(Σ_b 2^{\|C_b\|} + J(K+1)). The preceding enumeration fast path stores O(J + p) (choice vector, recursion depth J, best set) and costs ≤ cap · O(J(B+1) + p log p) (every visited tight node completes to a leaf, so no dead branches; cap = 10⁶ is a constant). GUARD-W: start mode + LS0 are timed as one operation and checked at checkpoint `ls0`; no uniforms (final stream endpoints identical with LS0 on/off, `out_test_ls0_wave2.txt`; p = 30 regression `streams` identical 48/48) | `options(v3.ls0_tie_dp = FALSE)` | see (a), (b) |
| **C-DLV B** tier-1 calibration fallback (HQ precision) | `v3_cal_tier`: at tier 1, on a grid failure (the tier already stops at its first failed construction: no diagnostics after a failed preliminary, `break` after a failed rebuild — unchanged), record `fallback_grid` = the last successful tier-1 construction `g` if `g$ok` (never the failed `gn` or its partial grid), else the completed tier-1 pilot schedule (`pil$schedule`; a stopped pilot returns earlier through `fail`). `v3_calibrate`: if the run would return `schedule_limit` (status ok, no grid, tier 1), validate the fallback with `v3_check_grid` and freeze it through the ordinary `v3_frozen` (tier-1 N, L, inherited scored state; sha256) before the final run; metadata (only when the fallback fires) `calibration$grid_fallback`, `tiers[[2]]$grid_source = "fallback: …"`, `fit$flags$grid_fallback` ∈ {"last_successful_construction", "pilot_schedule"} (the failed construction stays archived in `tiers[[2]]$grids` with `ok = FALSE` and its `reason`); the `grid_failure` trigger and `checks_passed_calibration = FALSE` are kept. Other branches (tier-0 failure → escalation, blocked escalation → `resource_limit`, stops, numerical failures) unchanged (`v3_calib.R:28, 120–126, 141–190`; `v3_fit.R:126–127, 145–146`) | `options(v3.grid_fallback = FALSE)`; `ls0 = FALSE` | `out_test_ls0_wave2.txt` (failures injected by wrapping `v3_build_grid`): all constructions fail ⇒ completed fit, finite estimates, `grid_fallback = "pilot_schedule"`, frozen grid = tier-1 pilot schedule (strictly increasing 0→1), tier 1; tier-0 preliminary + tier-1 rebuild fail ⇒ `"last_successful_construction"`, frozen grid = tier-1 preliminary grid with its ρ_V/label; tier-0-only failure (v3 escalates and succeeds) and no failure ⇒ calibration, frozen record and Ẑ identical to v3 and **no** `grid_fallback` flag (flag set only when the fallback fires — R05 #1 fix); switches ⇒ `schedule_limit` as in v3. 14/14 PASS on the final code. p = 30 regression on the final code: calibration and frozen record identical to the old core 48/48, no fallback flag 48/48 (§3c) |

**Study outputs and `schedule_limit`:** `Results/2026-10-28_New_Campaign/H_existing_20261030/tables/reconciliation.csv`
lists the 2,400 study fits as 2,394 `completed` + 6 `resource_limit` (p = 500: 1199 + 1; p = 1000: 1195 + 5), i.e.
**0 fits with status `schedule_limit`**; no stored result file under `Results/` or `Scripts/Campaigns/2026-10-28_New_Campaign`
contains the string `schedule_limit` (only code, schemas and review documents do). The published outputs are therefore
unaffected by C-DLV B.

**Resource note (C-GROW MR1) and preflight (HQ item, `HQ_AUDIT/A1_propF_redteam.md` finding 1):** with cap
ℓ_n + \|S̃₀\| ≤ ℓ_n + K, LS0 performs at most **ℓ_n + K + 1 scans** of ≤ p + k(p − k) ≤ q(p) = p + p²/4 models each (was
ℓ_n + 1); the resource-envelope change itself is handled on the theory side. The SMC preflight (`v3_preflight`,
`Scripts/SMC_BVS/core/v3_fit.R:16–63`) now charges this worst case when the C-GROW cap is in force (`ls0_worst_case`):
memory component `ls0_archive` = (2s + 4)(12K + 256) + 96s + 4(8W + 4K + 96) + 4096 bytes with s = ℓ_n + K + 1 (the archive at
the conversion peak, C++ `LocalArchive` with capacity growth plus its R copy: path, scanned centres, centre, returned
models, parallel F/scan vectors, scan particles; the O(K(K+1)) words of M_G; validated against a constructed worst-case
archive, the allowance read from actual `v3_preflight` calls, for (n, p) = (60, 30), (200, 500), (200, 1000), (2000, 2000), (6, 40) — R07 #1, R08); time `ls0_worst_case$est_seconds` =
2 × s·q(p) × the measured seconds per score of a size-K model (`v3_time_scores`, 200 scores; factor 2 = declared
bookkeeping constant for cache lookup/insert and ledger/store offers — the "C" of W_G; an operational estimate, not a
rigorous runtime bound), checked against the allocation's hours in `exceeds` for the initial and the escalation preflight.
The memory estimate is evaluated first and the timing benchmark runs only if memory fits (R07 #2). Switch: `options(v3.ls0_cap = "ell_n")` or `ls0 = FALSE` ⇒ the shipped preflight exactly.
Test (`tests/test_preflight.R`, `numerics/out_test_preflight.txt`, **13/13 PASS** after the R07 fixes): p = 30 regression design (n = 100) and
the study sizes (dev generator S1–S6, n = 200, p = 500 and 1000) at 8 GiB/24 h and 2 GiB/24 h: **0 fits newly refused**
(all pass both preflights); LS0 worst case ≈ 1.2–1.9 h at p = 500 and 4.8–6.7 h at p = 1000 (this Windows machine, shared
CPU; actual LS0 time in the replay fits is seconds), extra memory ≈ 0.33 MiB; with `v3.ls0_cap = "ell_n"` / `ls0 = FALSE`
the preflight record is identical to the shipped one; an allocation of half the LS0 worst case is refused by the new
preflight and not by the shipped one. The check is one-sided (it compares the LS0 term alone with the whole allocation,
as the shipped SMC preflight has no time term for the rest of the fit). Reviews R07 (REJECT, 2 MAJOR, fixed) and R08 (below).

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
| R05 | HQ wave-2 diff 95be87e..bf093a8 (C-GROW MR1, C-DLV A.2, C-DLV B + HQ precision) | Codex gpt-6.1-sol high (fresh) | APPROVE-WITH-FIXES (2 MINOR: `grid_fallback = "none"` flag on no-failure fits; unchecked cap addition via the test override) | `R05_wave2_review_raw.md` (incl. disposition); both fixed in 0638af9 |
| R06 | R05 fix check bf093a8..0638af9 | Codex gpt-6.1-sol high (fresh) | **APPROVE, no new findings; C-GROW MR1, C-DLV A.2, C-DLV B all MET** | `R06_fix_check_raw.md` |
| R07 | preflight LS0 worst-case delta 8a27652..ef33f91 | Codex gpt-6.1-sol high (fresh) | REJECT (2 MAJOR: archive allowance below the conversion peak; benchmark ran before a certain memory rejection) | `R07_preflight_review_raw.md` (incl. disposition); both fixed in 98fac03 |
| R08 | R07 fix check ef33f91..98fac03 | Codex gpt-6.1-sol high (fresh) | APPROVE-WITH-FIXES (both R07 MAJOR RESOLVED; 1 MINOR: archive test used a copied formula) | `R08_fix_check_raw.md` (incl. disposition); fixed: test reads the production allowance; +4096 fixed bytes |
| R09 | final delta 98fac03..72785fe (R08 test fix, +4096 bytes) | Codex gpt-6.1-sol high (fresh) | **APPROVE, no findings** (mutation: allowance 0 fails all 5 archive checks) | `R09_final_delta_raw.md` |

Every production-code change is covered by a review: f16ce15..9b9d234 (R03), the MR2 guard (R04), the wave-2 diff (R05) and
its fixes (R06), the preflight term (R07), its fixes (R08) and the final constant (R09). No production code changed after 72785fe.

## 3. Tests and results (scripts in `tests/`, outputs in `numerics/`; local Windows, R 4.6.1, Rtools45, Rcpp 1.1.2)

(a) **TDP unit tests** — `tests/test_tdp.R`; `numerics/out_test_tdp_seed20261108.txt`, `numerics/out_test_tdp_seed7.txt`:
2 × 3000 random instances (integer, flat-tie and real tables; random block order; K binding; NaN above K), caps 2, 3, 4,
5, 17, 10⁶ (cap 1 is rejected with the fallback, C-PACK MR2): new `start_mode` == lex-min E (uncapped enumeration)
6000/6000 at every cap; == brute-force S* on all 4000 exact-arithmetic (integer/flat) instances; TDP-E alone == S*
4000/4000; legacy fields unchanged whenever not truncated 6000/6000; lg0 and |S| == brute force 6000/6000. The old rule is
wrong on 117/1048 and 96/991 truncated instances at cap 2 (seeds 20261108 / 7). (The first run, before MR2, also used cap
1: 190/3000 and 169/3000 old-rule errors, all corrected by the fallback.)
**W1-N3 counterexample (p = 44, K = 22, cap 10⁶):** old returns {0,2,…,38,41,42} (≠ S*), new returns S* =
{0,2,…,38,40,43}, `tie_dp_used = TRUE`, log γ₀ = 25 (TDP-E < 0.01 s; total 6–7.5 s incl. the 10⁶-set enumeration).
Family of W1-N3 L6 at all caps ≤ 2^{m+1}+1, m ≤ 8: 0/1031 mismatches. Rounding fixtures (R01 #2 2⁵⁴ example, prefix, block
sum) and boundary fixtures (K = 0, K binding inside a block, interleaved blocks, empty optimum): all as specified.
Cross-check vs W1-N3's exact reference `tdp.py` (`tests/xcheck_n3_tdp.*`, `numerics/out_xcheck_n3_tdp.txt`): 600 integer
instances, 0 mismatches (cap 2 — fallback whenever \|E\| ≥ 2 —, cap 10⁶ enumeration, lg0).

(b) **LS0 behaviour** — `tests/test_ls0.R`:
Final code (0638af9): normal 35/35, stop 9/9, numfail 5/5, paths 10/10, wave2 14/14 — 0 FAIL.
- `normal` (`numerics/out_test_ls0_normal.txt`, **35/35 PASS**; incl. C-PACK MR1/MR2 checks): integrated LS0 event count = 1 (emitted centre) +
  n_evaluated, all mechanism `local_scan`; standalone LS0 equals the integrated one; emitting vs not emitting a
  local-maximum start mode changes the standalone HPM (provenance ls0, stage 0, position 0) — omission is observable;
  `ls0_improved`/E3 formulas; LS0 cap exactly 0 (rule `"ell_n"`, base 0) with a strict improving neighbour ⇒ `move_limit`, `ls0_local_limit`, public
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
- `wave2` (`numerics/out_test_ls0_wave2.txt`, **14/14 PASS**): C-GROW MR1 cap rule and its switch; binding fixture; invalid
  `v3.ls0_ell` rejected; C-DLV B fallback with injected construction failures (both fallback sources, both switches,
  tier-0-only failure and no failure identical to v3, no flag); final stream endpoints identical with LS0 on/off.

(c) **Regression, S1–S6** — `tests/run_batch.R`, `tests/compare_regress.R`; first run (code 9b9d234)
`numerics/out_regress_p30.txt` + `regress_logs/`; **rerun on the final code (0638af9) for LS0 off/on**
`numerics/out_regress_p30_final.txt` + `regress_logs_final/` (old and prototype fits reused; identical results on every
check below; plus: no `grid_fallback` flag/field 48/48, LS0 `move_cap` = ℓ_n + |S̃₀| 48/48, LS0 moves < ℓ_n 48/48 so the
C-GROW cap never binds and the prototype comparison stays exact): study covariances S1–S6 and the generator's p = 30 truth pattern, n = 100, replicates 1–4,
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
S5 r002) — `tests/run_replay.R`, `tests/compare_replay.R`, `numerics/out_replay_p500.txt`: production settings, default
allocation, new core (commit 9b9d234 binary: LS0 cap ℓ_n, before C-GROW) vs the O-LS0 prototype integration
(`cpp_final_run_ls0` on the old core), same data and seed (generator SHA-256 equals the pinned
36b03c8c…a8c6). **All 3 designs: 16/16 checks PASS each (48/48)** — status, islands/Ẑ/PIPs/MPM, final streams,
calibration + frozen record, final local search, HPM + provenance, all three stores, near ties, LS0 archive, start mode,
counters (prototype `local` row = new `local` + `ls0`), cache statistics, HPM before LS0, E1/E2/low-ESS, E3 = final search
only. All completed; start mode unique (ties 1, not truncated) in all 3; LS0 never changed the HPM (`ls0_improved` FALSE,
consistent with O-LS0's 0/2,394). LS0: S1 no_improvement after 10 moves (59,290 scores), S4 no_improvement after 7 (51,297),
**S5 move_limit at 10** (start mode {74}, 37,994 scores) — so in S5 the fit reports `ls0_local_limit`/`local_limit` TRUE
with output returned (#6/#10), and the certificate comes from the final search. Wall time per fit 30–86 min on this shared
Windows machine. **C-GROW cap on the binding design** (`tests/replay_s5_cap.R`, `numerics/out_replay_s5_cap.txt`; final
core, standalone LS0, whose path equals the integrated one): cap ℓ_n reproduces the replay fit's LS0 path exactly; cap
ℓ_n + |S̃₀| = 11 makes one more move (still `move_limit`, 43,873 scores), best LS0 model F = −185.95 < the fit's HPM
F = −124.71 ⇒ with the default C-GROW cap the reported HPM of this fit is unchanged. The full replay was not re-run on the
final binary (the post-9b9d234 changes are the cap rule just checked, the MR2 guard, the tier-1 fallback which did not
fire, and the preflight term).

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
`B2_new_ls0off_v31harness/`, `C2_new_ls0on_v31harness/`). **Final code (0638af9): B3 (ls0 off) and C3 (ls0 on) 28/28 on
seeds 1–3, summarize PASS** (`rerun_final.log`, `B3_final_ls0off/`, `C3_final_ls0on/`); no harness calibration reached the
former `schedule_limit` branch (0 occurrences in the raw results of A and C3), so the C-DLV B fallback did not fire there. Caveat (helper): the harness builds `ro` by hand without `ls0`, so
it does not execute LS0 itself; LS0 is covered by (b), (c), (c2). Only 3 of the 32 seed indices; not the Owls 32-seed gate.
`build/check_smokes.R` inspects saved Owls smoke records (`runs/*/exit_status.txt`, adapter outputs) that do not exist
locally, so it was not run; the public-path tests in (b) `paths` exercise the same adapter contract on local fits.

## 4. Files produced
`PLAN.md` (v1.3), `LOG.md`, `CHECKPOINT.md`, `REPORT.md`, `lemmas/TDP_E.md`, `reviews/R01_*` … `R06_*`, `reviews/CITECHECK.txt`,
`tests/` (ceng_load.R, ceng_exports.cpp, test_tdp.R, test_ls0.R, run_batch.R, compare_regress.R, proto_load.R,
o_ls0_exports.cpp [verbatim prototype], run_replay.R, compare_replay.R, xcheck_n3_tdp.R/.py, check_final_flags.R, replay_s5_cap.R,
test_preflight.R),
`numerics/` (outputs above; `existing_suite/` = harness evidence, 11+ MB).

## 5. Notes for HQ
- The ls0 switch also gates the #15 NA fields and the C-DLV B fallback, so `ls0 = FALSE` is exactly v3 (including stop
  outputs and `schedule_limit`).
- C-DLV B changes a shipped component (calibration) on the former `schedule_limit` event only, by HQ decision; 0 study fits
  were in that event.
- The existing harness calls `v3_calibrate` directly; with the default `grid_fallback = TRUE` a former `schedule_limit`
  seed would now continue to the calibrated final run (R05 note). Seeds 1–3 never reach it; for a v3 baseline pass
  `grid_fallback = FALSE` (or `options(v3.grid_fallback = FALSE)`).
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
- The merged-LS0 replay used the dev generator's S1 r001, S4 r001, S5 r002 at p = 500, c100 (the study's production
  datasets are not in the repository), on the 9b9d234 binary; the full replay on the final binary and at p = 1000 is not done.
- The certificate card (L1 etc.), stacking/c₄ search, concurrency layer and NA fields for `schedule_limit` statuses not
  produced by this core are outside this ticket.
- Owls/NOTS execution (production-size timing, `build/check_smokes.R` on saved smoke records) not done (local only).
