# Regression: v2.2 against v2.1 (local)

CONF, 2026-10-28/29. Workers: Claude Sonnet 5.5, independent of the implementer (Terra).
- Round 1: `work/regression/`.
- Round 2 (current code, hardened comparator): `work/regression2/REGRESSION2_EVIDENCE.md`.
- Reviews: `review/REGRESSION_REVIEW_sol.md` (round 1, ACCEPT WITH FIXES) and `review/REGRESSION2_REVIEW_sol.md` (re-check).

## Result

**PASS, within the following guarantee.** v2.2 draws no extra random numbers, and no new value feeds any decision. Whenever both versions execute the same operations, every pre-existing output of v2.2 is bit-identical to v2.1, and the only additions are the allowlisted new fields, appended after all old ones.

Disclosed limits:
1. The runtime guard reads wall-clock time, so stop points near an allocation are timing-dependent. This holds even between two runs of the same version. Same-allocation stop outcomes are therefore not certified identical.
2. Escalation, `schedule_limit`, `numerical_failure` and a real escalation-preflight stop were not produced locally. The NOTS job `jobs/CONF_NOTS_IDENTITY` covers escalation and the production platform.
3. The p = 30 reference is a size ≤ 12 enumeration.

Code state tested: `code/core/v2_2/` per `code/core/v2_2.SHA256SUMS`. This includes the two post-review fixes: the plain-PIP fields are appended after every v2.1 field, and CalState retains the registry owner.

## Comparator (round 2, `work/regression2/cmp2.R`)

- **Leaves.** `identical(num.eq = FALSE, single.NA = FALSE, attrib.as.set = FALSE)`, plus a byte-wise comparison of double/complex payloads, so signed zeros and NaN payloads are distinguished. `typeof` is checked for every container. Attributes are compared recursively and in order.
- **Additions allowlist.** Only these additions are allowed, at their exact container paths:
  - top level: `pip_plain_r`, `pip_plain`, `mpm_plain`, `instrumentation`, appended in that order;
  - every island list: `pip_plain`, `plain_acc`, `plain_round`, appended;
  - study record: `pip_plain`, `mpm_plain`, `instrumentation`, appended.

  The v2.1 name vector of every named list must be a prefix of v2.2's. Pre-existing unnamed lists, vectors and data frames may not change length or columns. So an extra guard checkpoint, near tie or local-search event counts as a difference.
- **Exemptions, by exact path, with type, length, names and attributes still compared.**
  - Wall-clock leaves: `timings`, the specific `seconds*` elements, `peak_memory_kb`, and the guard's elapsed, operation and projected seconds.
  - Exact-branch-only `preflight$est_seconds` and `seconds_per_score`. On SMC fits these are compared and identical NA. On the exact branch they feed `preflight$exceeds`, which is compared.
  - Study provenance: timestamps, `runtime_s`, `run_id`, source hashes, `adapter_version`, host and slurm fields, and the `environment` and `code` subtrees (shape only; `code$files` may gain only `v3_registry.h`).
  - The p = 500 input path strings, because the inputs were copied; their content hashes are compared.
- **Self-test.** 55 asserted mutations in round 2, 97 in round 3; the script exits non-zero on any miss. Among them: 1 ulp, 0 vs −0, a NaN payload, attribute order, an appended checkpoint or near tie, an unexpected field, an allowed field in the wrong position, a dropped field, and a changed exempt-subtree shape. **PASS.**
- **Re-run of round 1's saved pairs under `cmp2`.** Exactly one difference appears: the old mid-list position of the plain-PIP fields, which is now fixed. This confirms that the comparator catches it.
- **Round 3 (after the re-check, `REGRESSION2_REVIEW_sol.md` N2, N3 and N7).** Three comparator repairs:
  - an empty named baseline list can no longer hide an addition;
  - the `names` attribute's position is compared in order;
  - `record$code$files` gets a strict shape check (unique names, the registry header at its sorted position, 64-hex hashes), with explicit `cross` and `identity` modes.

  The self-test now asserts **97** mutations, exit 0. All saved round-2 pairs and the p = 500 record and CSV were recompared without refitting: **0 differences, 0 non-allowlisted additions**. The drivers now exit non-zero on any failure. `cmp2.R` sha256 5c7ad65c…8b3f, identical in the NOTS job bundle.

## R1. Bit-identity (current v2.2; v2.1 outputs reused after a tree-hash check)

| Case | What it exercises | Status (both versions) | Differing paths |
|---|---|---|---|
| 10 tiny-p datasets (D1–D5 × 2; n 16–30, p 18–20) | SMC branch, binding cap, null, correlated designs | completed | **0** |
| Exact branch (n 30, p 10) | enumeration | exact | **0** |
| y constant; no predictors; seed 0 | early statuses | y_constant; no_predictors; invalid_input | **0** |
| Constant column; duplicated column pair | dropped column; duplicate components | completed | **0** |
| Preflight memory stop; guard stop at the calibration pilot; 10 guard-stop pairs with identical checkpoint sequences (final bridge stages 1, 2, 5; diagnostic stages 1, 4; calibration local search) | `resource_limit` paths | resource_limit | **0** |
| p = 500 dev dataset (S4, r001, c100) through the study adapter | p ≫ n end to end; HLL mode | completed | **0** of 199,750 record paths. The CSV differs only in `run_id`, source hashes, `runtime_s` and timestamps |

Totals: 28 matched comparisons plus the p = 500 record; 0 differences; 0 additions outside the allowlist. The expected-case manifest is complete (0 of 100 files missing).

**Unmatched guard stops.** These were listed and not compared (`work/regression2/REGRESSION2_EVIDENCE.md` §2.1):
- Repetitions at the same tiny allocation: 20 v2.1 runs and 10 v2.2 runs stopped at checkpoint sequences with no partner.
- Single runs: at hours = 6 × 10⁻⁴, v2.1 completed and v2.2 stopped after 64 checkpoints, on a shared laptop.

These are wall-clock effects, as in same-version reruns, and they are the disclosed exception above. Production allocations are thousands of seconds, so only fits within the observer's overhead of their limit can be affected.

## R2. New fields

Round 1: 908 checks on 38 fits, all pass. Round 2 adds 100 checks, all pass:
- **Registry boundaries.**
  - p = 32: exact mode, scored set exported.
  - p = 33: exact mode, no scored set.
  - p = 64: exact.
  - p = 65: HLL, exact fields NA.
  - The same with dropped columns.
  - `keep_scored_set = FALSE` gives no scored set, and the registry stays exact.
- **Scored-set lookup with a dropped column.** It uses retained-position bits, and the HPM key is found.
- **Compatibility.** Old Rcpp call signatures (no registry argument) run and are bit-identical. The registry survives a forced GC.
- **Stops.** On all 25 `resource_limit` fits, `stop` equals the first exceeded checkpoint field by field, and the estimates are absent. A preflight stop has `where = "preflight"` and NA checkpoint fields.
- **Escalation reasons.** The real `finish()` logic was unit-tested on synthetic tier-0 triggers. 324 local fits (135 on the SMC branch) never escalated, so a real escalation is left to the NOTS job.

## R3. Low-p smoke (n = 200; three seeds each; the smoke data are not the campaign generator)

| Fit | Reference | Δ log Ẑ (rel. m₀) | Max \|PIP err\| RB | Max \|PIP err\| plain | HPM, MPM = reference | Scored mass / reference Z | Distinct scored | Largest scored model size |
|---|---|---|---|---|---|---|---|---|
| p20 / 1001 | full 2^20 | −0.0067 | 0.0014 | 0.0039 | yes, yes | 0.99995 | 24,664 | 12 |
| p20 / 1002 | full 2^20 | +0.0050 | 0.0009 | 0.0023 | yes, yes | 0.99995 | 24,932 | 12 |
| p20 / 1003 | full 2^20 | +0.0046 | 0.0018 | 0.0041 | yes, yes | 0.99996 | 27,766 | 13 |
| p30 / 1001 | size ≤ 12 reference | −0.0130 | 0.0017 | 0.0030 | yes, yes | 0.99886 (relative to Z_trunc) | 107,815 | 12 |
| p30 / 1002 | size ≤ 12 reference | +0.0073 | 0.0015 | 0.0018 | yes, yes | 0.99892 (relative to Z_trunc) | 113,123 | 12 |
| p30 / 1003 | size ≤ 12 reference | −0.0035 | 0.0012 | 0.0034 | yes, yes | 0.99891 (relative to Z_trunc) | 111,756 | 12 |

- **Budgets.** All six fits ran `branch_run = "smc"` with the committed budgets: (K, B, ℓ, L, N0, H0, T0) = (20, 4, 8, 8, 2500, 512, 1000) and (30, 5, 8, 8, 2500, 512, 1000). None escalated. Each took 3–5 s.
- **What the p30 numbers mean.** They are relative to the size ≤ 12 reference (1.94 × 10⁸ models). No scored model exceeds size 12, so full-posterior coverage is at most the displayed ratio. The share of mass at sizes ≥ 13 is extrapolated at about 9 × 10⁻⁹; that is not a bound. A full-posterior claim at p = 30 needs a complete enumeration or a certified tail bound; that is LOWP's exact reference.
- **Truth.** The data-generating support was used only after the fits. It was scored in all six fits.

## NOTS identity gate (production platform, escalation): DONE

Job 2455971 (OPS-3), accepted under D20: both units bit-identical on every computed field, including a real E2 tier-1 escalation. Local acceptance after the D20 cmp2 amendment: ACCEPT (`jobs/CONF_NOTS_IDENTITY/ACCEPTANCE_2455971_D20.md`). Original text of this section:


`jobs/CONF_NOTS_IDENTITY/JOB.md` reruns two historical p500 units with v2.2 on NOTS: one not escalated, one escalated by E2. Acceptance is bit-identity with their production RDS under `cmp2.R`, and `escalation$reasons = "E2"`. Cost ≈ 20 min of compute on 1 CPU.

# v2.2.1 regression (CONF-2b, 2026-10-29): v2.2.1 against v2.2 and the retired LOWP fork

**Result: PASS.** Every section has 0 FAIL rows. The identity is the same timing-excluded identity used for v2.2 and for the NOTS gate: timing, memory, provenance and run identity are excluded, and everything else is compared bit for bit by cmp2 (D20 version). It is not whole-file byte identity, because timings are embedded in `fit`.

- An independent verifier (Terra) recomputed the key claims with its own code: `work/v2_2_1_regression/verify/VERIFY_REPORT.md`.
- Harness, logs and outputs are in `work/v2_2_1_regression/`. The mechanical report is `RESULTS.md`, with machine-readable rows in `results/*.csv`.
- The harness was resumable and ran as background shell jobs. It survived a T3 server restart.

**Code.** Private copies of `code/core/v2_2` (25/25 files), `code/core/v2_2_1` (27/27) and a second v2.2.1 core for the fork (21/21) were each verified against their manifests and compiled once. The cores are byte-identical.

The fork (`code/lowp/smc/`, now retired) was copied before retirement and checked with `sha256sum -c` against its full hashes in `code/CODE_LEDGER.md` (LOWP entry): 5/5 OK.

| Part | What | Result |
|---|---|---|
| (a1) | Core cases b, c, a, d2 (17 fits) with v2.2.1, against the saved v2.2 outputs (`work/regression2/out/v22`) and a fresh v2.2 rerun | 0 differing paths and 0 additions of any kind, for all 17 × 2 pairs |
| (a2) | Forced guard stops, hours 5e-05 / 0.0002 / 0.0003 / 0.0006, fresh v2.2 vs v2.2.1 | 4/4 allowed, see below |
| (a3) | p = 500 dev case (`dev_p0500_S4_r001`, c100) through the study adapter: v2.2.1 vs fresh v2.2 and vs the saved v2.2 record | 199,884 record paths, 0 differences, 0 additions, `record$p5` absent, same top-level names. CSV: 88 columns, same order, 0 non-provenance cell differences (only `run_id`, `source_sha256`, `runtime_s`, timestamps differ) |
| (a4) | `smcbvs_case_spec` identity | H: v2.2 = v2.2.1 for 10,080/10,080 ids (the verifier added 9,120 more dev ids, 0 mismatches). L: fork = v2.2.1 for 15,120/15,120 (the verifier added 115,200, 0 mismatches). 24/24 invalid inputs refused; 9/9 CLI refusals exit 1 without creating output |
| (b) | LOWP smoke cases: p0020_S1_r001 c100 and c050; p0030_S4_r050 c100 and c050; p0020_S1_r001 c100 `--repeat 1`; dev_p0020_S2_r003 c100. v2.2.1 `study/run_case.R` vs the fork `run_smc_case.R`, same current core | 6/6: `pip`, `hpm`, `mpm`, `case`, input hashes and all non-timing `fit` content identical; no additions; CSV non-provenance cells identical |
| (b) | vs LOWP's recorded values (`code/lowp/tests/SMC_SMOKE.md`) | 6/6 at the recorded precision: status, HPM, log Z (−85.0870, −192.2569, −107.5142, −214.9098, −85.0776, −126.9532), log Z − log m0, stage rows, tier; seeds 5,221,001 (repeat 1) and 6,230,003 (dev) |
| (c1) | p0020_S1_r001 c100, `--hours 0.00003`: `resource_limit`, then `--p5-retry` | Primary `resource_limit`, stop `runtime_guard/pilot/bridge_stage`. The retry is written to `P5_retry/SMCBVS_p5retry.*` with allocation exactly ×2. `record$p5` reproduces the primary's identity (sha256 lines, allocation and hash, status, stop); same seed; primary files byte-unchanged; the stop phase is on the last stdout line. The retry stopped again: its own `resource_limit` |
| (c2) | Memory preflight: `mem_gb` = 0.75 × the core's own estimate | The primary refuses at preflight; the retry at ×2 **completes** and is valid |
| (c3) | c1 with `--repeat 1` | `SMCBVS_rep1_p5retry.*`; same checks pass |
| (c4) | Regime H, `dev_p0500_S4_r001`, tiny memory | Both records written; stop phases recorded |
| (c5) | Negatives | Refused (exit 1, no files): retry on a completed primary; retry with no primary; allocation ≠ primary's. A second retry is skipped and its files are unchanged |
| (c6) | `tools/p5_scan.R` before and after; `scoring::scan_results()` | Before: 3 units, 2 `resource_limit`, 2 eligible. After: 0 eligible, 2 retried. `scan_results()` returns the 3 primary/repeat units only, never a `P5_retry` file |

**(a2) in detail.** Guard stops depend on the wall clock (D10: not certified identical near a limit).
- At 5e-05 both versions stop at the same checkpoint (`runtime_guard/pilot/bridge_stage`, same tier, iteration, island and stage). The only differing values are the stop record's two wall-clock readings, `instrumentation$stop$elapsed_seconds` and `projected_seconds`. These are classed as timing (`identical_except_stop_timing`), a manager amendment of the harness that the verifier judged sound.
- At 0.0002, 0.0003 and 0.0006 the versions stop at different checkpoints, which is allowed under D10. These pairs prove nothing about the computation beyond the stop.

**Fields.** There are no new or changed `fit` fields. The envelope changes (`adapter_version`, regime-L `case` layout, `record$p5` on rerun records only, the `P5_retry/` layout) are listed in `OUTPUT_FIELDS.md`, section "v2.2.1 changes".

**Not exercised** (as for v2.2): `schedule_limit`, `numerical_failure`, a real escalation-preflight stop, and P5 on NOTS. NOTS identity was shown for v2.2, and the v2.2.1 core is byte-identical to it.

## v2.2.1 after Sol review 1 (CONF-2b, 2026-10-29)

Fixes F1–F7 (`review/CONF2B_REVIEW1_disposition.md`) changed `study/adapter.R` and `tools/p5_scan.R`; the core is unchanged.
- Rerun: the tree copy was refreshed against the new manifest, then **a3 (v2.2.1), a4, (b) merged and c1–c6 were rerun**.
- Kept: a1/a2 are core-only (`run_cases.R` sources only `core/v3.R`). They stay valid, and a2 was reclassified under the hardened rule.
- **Every section has 0 FAIL rows** (`work/v2_2_1_regression/RESULTS.md`), with the same numbers as above: a3 199,884 paths, 0 differences, no additions; (b) 6/6 and 6/6; c1–c6 117 PASS.

**New lane G: tests of the fixes, on scratch copies, with a stub core.**

| Fix | Checks | Result | What the checks show |
|---|---|---|---|
| F1 | 23 | PASS | A unit that another caller commits between the first check and the lock is returned skipped: no core call, files byte-unchanged. Holds on the primary and the P5 paths. New mismatches, a primary changing under a retry and a foreign lock are all refused. |
| F2 | 24 | PASS | H refuses a missing or named-NULL `n`/`kind`/`scales`, as v2.2 does. L is unchanged. |
| F3/F7 | 26 | PASS | Wrong-seed, wrong-primary, wrong-allocation and CSV≠RDS reruns give `invalid_inspect`. Partial artefacts give `incomplete` or `locked`. A clean primary is `launchable`. A primary with CSV≠RDS in either direction makes the scan refuse. The summary line keeps its first six fields. |
| F4 | 22 | PASS | Resumed primaries and reruns print their saved stop phase. |

**F1 mutation check.** The F1 test was run against the pre-fix adapter (`out/mutation_prefix_F1/MUTATION_NOTE.md`). The primary-race checks FAIL there: the core is called again and the unit is rewritten. So the test detects the reported bug.

**F5, a2 rule as amended.**
- The stop-timing exemption needs finite numerics of the same type, length and attributes.
- The different-checkpoint exception needs both sides `resource_limit` with a `runtime_guard` stop, no additions, and a full top-level layout equal to one that v2.2 itself emits in this corpus. A later stop carries more partial-result fields and moves `flags`, so names-equal was too strict for the 0.0003 pair.
- 15/15 negative controls behave as expected.
- All four a2 rows are "timing-excluded / not identity evidence".
