# CONF-2b review 1: disposition (CONF-2b manager, 2026-10-29)

Review: `CONF2B_REVIEW1_sol.md`. Sol's verdicts:

| Deliverable | Verdict |
|---|---|
| merge | ACCEPT WITH FIXES |
| P5 | REJECT (F1) |
| regression | ACCEPT WITH FIXES |
| cmp2 D20 | ACCEPT |
| pilot | ACCEPT WITH FIXES |

**All seven findings are accepted and fixed.** No numerical path changed, and the core is untouched (still byte-identical to v2.2).

| # | Severity | Fix | Where | Test evidence |
|---|---|---|---|---|
| F1 | blocking | Identity, completion and (for P5) the primary binding are re-checked **under the unit lock**. A unit committed by another caller meanwhile is returned as skipped: no core call, no overwrite. This covers the primary and the rerun path. | `code/core/v2_2_1/study/adapter.R` | harness lane G (`conformance/work/v2_2_1_regression/results/g_*.csv`) |
| F2 | should-fix | Regime H checks `n`/`kind`/`scales` unconditionally (a named NULL is refused, as in v2.2). Regime L keeps "when present". Lookups use `[[ ]]`. | `study/adapter.R` | lane G |
| F3 | should-fix | A rerun counts only if bound to its primary: identity columns, ×2 allocation with a consistent hash, `record$p5` naming the primary's `.sha256` lines, and CSV status = RDS status. Otherwise its state is `invalid_inspect`, with `retry_problem`. An inconsistent primary makes the scan refuse (exit 1). | `tools/p5_scan.R` | lane G |
| F4 | should-fix | A skipped unit returns its saved `native_status` and stop phase, so the CLI prints them on resume. | `study/adapter.R` | lane G |
| F5 | should-fix | The a2 classifier keeps type, shape and finiteness checks on the two exempt stop timings. The different-checkpoint exception requires `resource_limit` + `runtime_guard` on both sides, no additions and equal fit names. Rows are labelled timing-excluded, not identity evidence. Sol's negative controls are added. | `conformance/work/v2_2_1_regression/scripts/a2_compare.R` | lane G / a2 |
| F6 | should-fix | The frozen-tree check refuses a symlinked tree root and any symlink or special entry outside `core/.cpp_cache/` (file links, directory links, links replacing listed files, a linked cache). | `code/lowp/pilot/frozen_check.sh` | `code/lowp/pilot/tests/test_shell.sh` (new symlink cases) |
| F7 | minor | Every rerun artefact counts (`retry_artefacts`). New states `locked` and `invalid_inspect`, and a new column `launchable` (only these rows may be launched). The summary line appends `launchable=`, `locked=`, `invalid_inspect=` after its unchanged first six fields. | `tools/p5_scan.R` | lane G |

**Manifest after the fixes.**
- `code/core/v2_2_1.SHA256SUMS`: 27 files; sha256 fda7c3f3a8e02f28bde82c3aa67aa243ec1eb1fb33a3e9e49e4ee44d1013789c (after the F3 both-directions follow-up; first fix round 5ce83d63…f0c7).
- `code/core/v2_2_1.diff`: 518 lines; sha256 807d16509b70fd99e5ad1e370dbdd2992ec9808eed3fa3ba52f8e6e2dea19e06.
- `CHANGES_v2_2_1.md` has a "Review fixes" section.

**Rerun after the fixes.** The tree copy is refreshed. a3 (v2.2.1), a4, (b) merged and c1–c6 are rerun. a1/a2 are core-only and stay valid; a2 is reclassified under F5. The results are in the regression section of `conformance/REGRESSION.md`, as updated after the rerun.

## Follow-ups found by the fix tests (lane G)

- **F3, first fix one-sided.** The scan compared the CSV with the RDS status only when the CSV said `resource_limit`. Now every unit's RDS is read and compared in both directions (`native_status`, else `fit$status`).
- **F5, first rule too strict.** "Equal top-level names" failed the legitimate 0.0003 pair, which stopped later and so carries more partial-result fields. Now each side's full layout must equal one that v2.2 emits in the corpus.
- **Lane G result.** F1 23/23, F2 24/24, F3/F7 26/26, F4 22/22.
- **F1 mutation.** Against the pre-fix adapter, the primary-race checks fail (`work/v2_2_1_regression/out/mutation_prefix_F1/`).
- **Pilot.** Shell 54/54 (8 symlink cases), negative 88/88. The fabricated fixture now carries `v3_status`, as the adapter writes it. One case's expectation changed: an inconsistent unit makes the scan refuse instead of counting as eligible.
- **PROD-H.** The F6 check was ported to `runner/frozen_check.sh`. Its suites pass: Python 30/30, shell 111/111, CLI parser 6/6, syntax 25/25.
