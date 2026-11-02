# Independent re-check (d): scoring and metrics

**Final verdict: REJECT.** All three original blocking defects are fixed. Of the 12 original findings, **9 are FIXED and 3 are PARTIAL**. The production registry still selects the wrong F4/F5 rule, and the re-check found an evidence-extraction regression. The claim that all 12 findings are fully resolved is not supported.

Reviewer: Sol 6.1, independent; no subagents. Completed 2026-10-28 America/Chicago (2026-10-29 UTC). Reviewed files were not edited. Paths below are relative to `CAMP/code/scoring/`, unless qualified.

## Evidence and execution scope

Evidence root: `<PC_TEMP_PATH>`.

Read only the named scoring tree, prior review/evidence, contracts, master excerpts, enum API/README, benchmark README/adaptations/config, schema, three named core R files, and `IMPL_SPEC_v2_2.md`. No SSH, real fitting, C++ compilation, cache/library searches, or unlisted project-source reads were performed. R's normal package loading was used, without inspecting package installation trees.

The original `review_checks.R` and `extra_checks.R` were copied and re-run against the current code as `replay_checks.R` / `replay_extra.R`. Adaptations are inspectable in `prepare.py`: the new registry/ref arguments and explicit partial-study mode, exact schema/hash/completion metadata, the producer's actual `final_bridge` phase label, distinct recorded repeat seeds, and filtering the original selection assertions to their tested rule now that the registry synthesizes additional rows. Mathematical oracle formulas were preserved. The original direct duplicate-main-table probe was also preserved; it still fails, as detailed under finding 6.

Final successful executions, using R 4.4.1 and one thread for OMP/BLAS/MKL and related thread settings:

| Script | Launcher PID | UTC start–finish | Exit | Inspected result |
|---|---:|---|---:|---|
| `replay_extra.R` (also runs `replay_checks.R`) | 780 | 02:56:30–02:56:52 | 0 | Original arithmetic, adversarial, DP and TD probes completed; raw observations saved. |
| `supplement.R` | 44252 | 02:59:31–02:59:48 | 0 | 23/23 assertions confirmed fixes or reproduced remaining defects. This is not a 23/23 acceptance score. |
| `discriminate_old.R` | 41592 | 03:03:39–03:03:42 | 0 | 10/10 current predicates pass; 9/10 fail against the preserved old scoring source. One-seed agreement was already NA in the old code. |
| `final_probes.R` | 37504 | 03:04:34–03:04:36 | 0 | Realistic primary-plus-cap rule identities, named-PIP error, and old/current exact-branch evidence comparison. |

All dates in this table are 2026-10-29 UTC. `*.status.json` records exact launch commands, timestamps, launcher PIDs, exit statuses, host and settings; R process PIDs are also printed in logs (Windows launcher and R PIDs can differ). Seed: **20261028**, with the inherited deterministic TD fixtures. `sessionInfo.txt` records R/package details. Startup locale warnings and the data.table build-version warning are preserved in stderr; no numerical-check warning was suppressed to obtain success.

`observations.rds`, `observations_extra.rds`, `supplement_observations.rds`, `final_probe_observations.rds`, generated study/results/output folders, `independent_assertions.csv`, and `old_discrimination.csv` preserve actual inputs and measurements. `snapshot/`, `source_hashes_before.json`, `source_integrity.csv`, and `evidence_sha256.csv` preserve source and evidence identities. Earlier harness attempts are retained as `attempt*` logs: two API/fixture adaptations, a reviewer syntax correction, a fixture-reset correction, and recognition that one old stability predicate already passed. These are distinct from final successful runs.

**Integrity check:** all **24/24 scoring files are unchanged**. Three named authority files changed concurrently: `lowp/INTERFACES.md`, `lowp/enum/lowp_enum.R`, and `lowp/enum/README.md`. Their original bytes and final versions/diffs are preserved under `snapshot/` and `concurrent_changes/`. I inspected the differences: completion/source-fingerprint/scale-set requirements are clarified and TD now rejects negative margins. The scoring API and saved probes are unaffected (all TD margins used here are nonnegative); the refined completion contract reinforces finding 10. Of the 40 snapshotted files, 37 remain identical. These external updates were not made by this reviewer.

The author's **147/147** suite result and updated real-p20 report were read, not independently reproduced. Running that suite as written would source/compile unlisted dependencies and rewrite reviewed reports. The dynamic review instead uses explicit mathematical scorer/setup APIs and small synthetic envelopes, as in the earlier review. Native preprocessing of a constant column and actual C++ TD execution remain outside this re-check's dynamic coverage; their new tests and named API/assembly code were inspected.

## Per-finding disposition

“Old discrimination” describes substantive behavior, rather than failure merely because an old function lacks a new argument. G13–G25 refer to `tests/regressions_review.R`.

| Original finding | Status | Re-check evidence and regression assessment |
|---|---|---|
| **1. Blocking: absent main fits leave headline denominators** | **FIXED** | Separate reference rows retain all four expected cases in H1–H3. H2 is **2/4 = 50%** on each scale; exact-HPM-vs-truth is independently **100%**. A completed repeat without a main remains a nonrecovery. With no SMC files, H1–H3 and HEADLINE are still emitted. G13 would fail the old behavior: its expected n_cases and all-missing output assertions are substantive. |
| **2. Blocking: numeric empty exact support becomes unavailable** | **FIXED** | `integer(0)` and `numeric(0)` stay empty; text-empty stays empty; NULL/NA remain unavailable. Both exact reference selections with empty truth give `status=ok, k=0, exact=TRUE, error_type=none`. G15's API-shaped numeric support and round-trip assertions catch the original bug; the numeric-empty predicate was also run against old source and fails there. |
| **3. Blocking: dropped truth zeros region mass / crashes theory row** | **FIXED** | The original retained-space oracle gives region masses **(0.5262586669022962, 0.7885557028535968, 0.9173298220617911)**, agreeing with explicit summation to about 1e-16. A completed fit preserves its theory row, `pi0_S0=0`, unavailable truth score/miss class and dropped-truth status. The G16 constant-column fixture now asserts an actual dropped index, positive feasible masses and undefined TD. The region predicate fails on old source. Documentation correctly distinguishes infeasible full truth from feasible subsets. |
| **4. Should-fix: evidence availability, counts, coverage policy** | **FIXED** | The original NA-log-Z case remains usable for HPM/PIPs but contributes no evidence. H1 reports `n_evidence=1`, bias/RMSE/median/p90 all **0.1**, and conditional coverage **1**. Two islands no longer receive sd/2; RB/plain counts are separate. Conditional lower-bound coverage is now explicitly documented. G17 catches old missing-data arithmetic and two-island SE; the latter was dynamically discriminated. **A distinct overvalidation regression is N2 below.** |
| **5. Should-fix: observed-file roster hides missing cases/methods** | **FIXED** | The manifest supplies expected cases; missing rostered truth and incomplete production grids are errors; partial mode is explicit. Entirely absent planned methods receive zero-recovery rows. A complete six-scenario grid retains **/100 and /600**, separately by scale. G14 catches the old absent-method/truth-roster behavior. This accepts the roster mechanism; the incorrect registry contents are separately blocking under N1. |
| **6. Should-fix: duplicate roots overweight or silently choose results** | **PARTIAL** | Identical SMC copies merge without changing H2; conflicting SMC bytes and repeated known seeds are refused. G18 detects the old support/SMC duplicate behavior. **Benchmark identity still compares only status/support:** opposite `diag_flag` values are declared “identical copies merged”; swapping roots changes passing-only recovery **1/1 → 0/1** with default conflict policy. Also, the original direct H2 probe still changes **n_cases 4 → 5, recovery 50% → 60%** because `case_base()` has no unique-main-key assertion. The normal scanner protects this second case in the pipeline, but the requested table invariant is absent. See `R/extract_bench.R:83` and `R/tables.R:19`. |
| **7. Should-fix: exact PIP original-index map discarded** | **FIXED** | Exact names `{1,4}` with a matching retained map now expand to **(.8,0,0,.2)** and all matching SMC PIP error summaries are zero. A map/name disagreement is rejected. G19 directly catches the old relabeling; old-source discrimination confirms it. |
| **8. Should-fix: incomplete fields manufacture PIPs/costs/equalities** | **FIXED** | Original partial named retained vectors are unavailable; malformed unnamed vectors no longer invent empty MPMs. No final stage gives NA ESS; all-NA ESS/counts stay NA; missing reference HPM/MPM gives NA equalities. Failed-fit coverage is now consistently unavailable in accuracy and theory. G20 substantively catches the old partial-PIP/ESS/equality defects; two predicates were checked against old source. **Further malformed-input gaps are N3 below.** |
| **9. Should-fix: passing-only recovery absent** | **FIXED** | H4/HEADLINE now include all-saved and passing-only counts at the same expected-case denominator. Independent flagged-success grid gives **1/100 (0/100)** and **1/600 (0/600)**. G21 detects absent old passing columns, confirmed against old source. The declared NA-flag policy is explicit. Duplicate flag handling still needs finding 6's fix. |
| **10. Should-fix: EXACT readiness not enforced** | **PARTIAL** | The pipeline now refuses no `.done`, bad hashes, wrong dataset/schema and `extra$complete=FALSE`; the original no-marker unit is unavailable. `scan_results()` still lists it by design, but the loader gates use. G22 catches the old pipeline behavior. **Completeness is not required TRUE:** `extra$complete=NULL` with top-level `complete=FALSE` is accepted; entirely unspecified completeness is accepted; a scale marked `status=partial, scope=restricted_to_scored_models` is accepted under an exact envelope. See `R/extract_exact.R:28–30,37–49`. These contradict the readiness promise and warrant tests. |
| **11. Minor: repeat eligibility/count contract** | **PARTIAL** | Known distinct seeds now have per-metric counts; the ragged case reports **3 evidence / 2 RB / 2 plain** contributors, with original PIP SDs **.0707106781 / .1414213562**. One completed + one failed fit reports counts and NA SD/agreement; one-seed agreement was already NA in old code, so that part alone is not a regression discriminator. G23's new counts and ragged-field assertions address the old reporting defect. **Missing seed identities remain eligible:** two `method_seed=NA` records produce two contributors and evidence SD **.7071067812**, despite the distinct-seed contract (`R/metrics_smc.R:96–100`). Reject or exclude unknown identities. “Attempted” is now clearly documented as files found, not a planned repeat roster. |
| **12. Minor: slow TD scores over-K centres** | **FIXED** | The original p=4, K=2, S0={1,2}, d=1 probe completes: **10 feasible centres**, **2 skipped over K**, no infeasible score call. G24 reaches strictly above K and fails on old source. Random/tied literal and toward oracles and enum-return normalization still pass. |

## New findings and required corrections

### N1 — Blocking: scoring registry does not match the current benchmark rule identities/roles

**Locations:** `registry_lowp.csv:12–13`, `METRICS.md:40`, `R/metrics_selection.R:45–53`; authority `CAMP/code/bench_lowp/ADAPTATIONS.md:8` (LA-4) and the user's explicit current-registry instruction.

| Benchmark methods | Required primary ID | Scoring primary ID | Result |
|---|---|---|---|
| F1, F2, F3 | `cv_min` | `cv_min` | Matches |
| F4, F5 | `ebic1_K37` | `ebic1` | **Mismatch** |
| A1 | `pip05` | `pip05` | Matches |
| A2 | `ssl_final` | `ssl_final` | Matches |
| A3 | `ci95` | `ci95` | Matches |

The named benchmark config contains frozen upstream base registries; LA-4 explicitly overlays the K37/cap roles. Scoring has not applied that overlay. Its expected registry also lacks the named K37 companion identities and the additional LA-4 S0 rows; optional rows may be stored without being required, but their expected coverage/roles must be intentional and documented. No unlisted benchmark runner/registry source was read.

**Observed consequence:** successful `F4/ebic1_K37` and `F5/ebic1_K37` rows are `in_registry=FALSE, in_h4=FALSE`. If these are the available primary rows, H4 manufactures `ebic1 not_run` and reports **0/1**. With realistic additional identical cap rows, H4 instead reports the **S0 `ebic1` cap**, excluding the actual K37 primary. Identical values at p≤30 do not resolve the identity/role violation; LA-4 explicitly keeps them distinct.

**Required:** align the default expected registry and documentation with the effective benchmark registry, including F4/F5 `ebic1_K37` primary; keep cap rules secondary and validate observed roles against the registry. Add a test using actual F/A IDs with both primary and cap rows. G13–G25 use a fixture registry and do not test this production alignment.

### N2 — Should-fix: four-island validation discards genuine exact-branch evidence

**Locations:** `R/extract_smc.R:124,147–149`; producer `CAMP/code/core/v2_2/core/v3_fit.R:124–134`.

The production native exact branch supplies `log_Z`, primary PIPs and HPM, and does **not** supply `log_Z_r`. Requiring four finite islands to retain pooled evidence changes this valid record to `ok=TRUE, evidence_ok=FALSE, log_Z=NA`. A producer-shaped fixture with finite exact evidence **−96.73973510983589** has old error **0** and current error **NA**. H1 loses its evidence contributor even though the quantity is known exactly. This is an observed regression against the preserved old extractor, not a missing optional field assumption.

**Required:** separate pooled-evidence validity from island/SE validity, handling native `exact` explicitly. Retain its pooled log Z, error and lower-bound comparison; keep inapplicable island quantities unavailable. Test the real exact-branch shape, including absent plain PIPs. G17 currently treats missing/short islands as invalidating every evidence quantity and misses this branch.

### N3 — Should-fix: full-vector index validation and exact probability validation remain incomplete

**Locations:** `R/extract_smc.R:116–118`, `R/extract_exact.R:44–49`; `FIELD_MAP.md` validation note.

The full adapter-PIP fast path validates numeric length/range but neither validates nor orders names. A named full vector with names **4,3,2,1** is accepted in that order; positional error calculation gives **max error .3** against its correctly mapped reference, although the correct error is **0**. Full vectors need a canonical original-index order, or rejection of noncanonical maps. The exact extractor separately accepts PIP **1.8** because it only rejects missing values after expansion, with no finite/[0,1] check. The validation documentation overstates the guarantees.

**Required:** canonicalize/validate full-length original-index vectors, check confirmed dropped entries, and apply finite probability validation to exact PIPs too. Add full-vector permutation/duplicate-name and nonfinite/out-of-range exact fixtures. These are additional cases beyond the repaired original partial-retained-vector probes.

## FIELD_MAP and test assessment

**The v2.2 addition paths and meanings match `IMPL_SPEC_v2_2.md` and the named assembly/schema files.** Plain retained PIPs, island matrices, strict plain MPM and adapter full vectors are mapped to the specified fields. Registry mass is correctly derived from `instrumentation$scored$log_sum_exp_F`, distinct count from `$n_distinct`, and scored-set first-event fields from `$scored_set`, using retained-position bitmask keys. The p≤64 exact-registry and p≤32 scored-set qualifications are consistent. Truth lookup remains post-fit; no supplied fitting source reads truth. `truth_trace` is correctly marked provisional. `field_map_runtime.csv` preserves the extractor's actual map. The validation-policy qualification is N3; exact-branch evidence handling is N2. This does not certify unlisted C++ internals.

The updated tests are substantially stronger. G13/14/18/22 would fail the old denominator/roster/duplicate/readiness behavior for reasons established by the original probes and source inspection. Nine representative predicates from G15–G24 were also executed successfully on current source and unsuccessfully on old source; the tenth, one-seed agreement NA, already passed before. G25's PPV and posterior-miss assertions formalize behavior that the independent first review already found correct. Its standalone lexicographic helper assertion does not itself exercise fixture ordering or the production tie resolver. The real-p20 integration script now asserts its key checks, but it still uses a constructed envelope rather than exercising the adapter writer end to end.

Ordinary log-Z scale arithmetic, lower-bound direction/boundary, four-island SE, nonzero true/null PIP splits, empty support semantics, independent block DP, tie-aware HPM classification, literal/toward TD and paired-scale separation remain correct in the inspected outputs. Full acceptance requires N1–N3 and the partial remnants of findings 6/10/11 to be addressed and re-checked. **REJECT.**
