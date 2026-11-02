# CONF thread: summary for HQ (2026-10-29)

## Deliverables

| File | Content | Review |
|---|---|---|
| `CONFORMANCE.md` | Verdict: **PASS, qualified**. No unauthorized behavioural deviation. S1, the per-unit allocation, is behavioural but authorized by GO_2400 C1. D03 and D30 are conditional and never fired. | Sol: ACCEPT WITH FIXES; all 9 fixes adopted (`review/CONFORMANCE_REVIEW_*`) |
| `PATCHES.md` | P1–P6, with costs and markings | Sol, 3 rounds: fixes adopted |
| `OUTPUT_FIELDS.md` | Every output field the LOWP metrics pipeline consumes | Sol: ACCEPT |
| `code/core/v2_2/` | v2.2 = v2.1 + plain PIPs + scored-model registry + instrumentation; `v2_2.diff`, `v2_2.SHA256SUMS`, `code/CODE_LEDGER.md` | Sol: ACCEPT |
| `REGRESSION.md` | Pre-existing outputs bit-identical (hardened comparator, 101 asserted mutations); new fields sane; low-p smoke against enumeration | Sol: ACCEPT WITH FIXES; the fixes were applied in round 3 and the F4 repair |
| `jobs/CONF_NOTS_IDENTITY/` | NOTS gate: production platform plus a real escalation (2 historical p500 units, ≈ 20 min of compute) | Sol: ACCEPT WITH FIXES; the fixes are applied (`review/GATE_CONFIRM_disposition.md`); ready to submit |

## Review trail (`review/`)

- `CONFORMANCE_REVIEW_sol.md`, then `CONFORMANCE_REVIEW_disposition.md`.
- `REGRESSION_REVIEW_sol.md` (16 findings), then `REGRESSION2_REVIEW_sol.md` (re-check; 7 resolved, 9 partial).
- `FINAL_CHECK_sol.md` (13/16 resolved; bundle rejected).
- `GATE_CHECK_sol.md` (bundle ACCEPT WITH FIXES), then `GATE_CONFIRM_sol.md` (ACCEPT WITH FIXES; its one remaining fix is applied: `GATE_CONFIRM_disposition.md`). The bundle is ready to submit.

## Open items for HQ

1. **P5, stop policy (BEHAVIOURAL).** One rerun at doubled allocation, same seed, for `resource_limit` fits. Cost ≈ 70 core-h and ≈ 13.5 h wall if the same 6 p ≫ n units stop again.
2. **P3(b), replay with a watch list at p ≫ n.** Optional; ≈ ½ day to build, plus one fit per replayed unit.
3. **P4, a discriminating cut_group variant.** Optional; ≈ 1 h of work.
4. **P6, low-p study adapter and runner.** They reject p ∈ {20, 30}. This needs LOWP's seed and input scheme; route to CONF (as v2.2.1) or LOWP.
5. **Part I wording reconciliations:** S1 allocation, D03, D30, D41, §I.7 (R-1).
6. **Contract wording.** v2.2's guarantee is conditional: no random numbers drawn, no decision inputs, bit-identical whenever the same operations run. Wall-clock guard stop points near a limit are not certified identical; same-version reruns vary too. Accepting this in place of the brief's literal "no decision changes" is HQ's call.
7. **Not exercised locally:** `schedule_limit`, `numerical_failure`, a real escalation-preflight stop.

# CONF-2b (2026-10-29/30): v2.2.1 frozen; pilot and PROD-H bundles released

| Deliverable | State | Evidence |
|---|---|---|
| Code tree **v2.2.1** (`code/core/v2_2_1/`), one tree for every SMC-BVS run | **FROZEN.** `v2_2_1.SHA256SUMS` sha256 d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1 (27 files); core byte-identical to v2.2; diff 527 lines | Sol reviews 1–3 (`review/CONF2B_REVIEW{1,2,3}_*`); `REGRESSION.md`, v2.2.1 sections |
| D20 cmp2 amendment | ACCEPT on job 2455971; controls and self-test pass | `jobs/CONF_NOTS_IDENTITY/ACCEPTANCE_2455971_D20.md` |
| Regression a/b/c (+ lane G tests of the review fixes) | 0 FAIL in every section; Terra verification; F1 mutation check | `work/v2_2_1_regression/RESULTS.md` |
| LOWP fork `code/lowp/smc/` | retired (README pointer) | `code/CODE_LEDGER.md` |
| LOWP pilot bundle `code/lowp/pilot/` | **READY for OPS (rev 7d)** | `review/PILOT7D_SOL.md`, `PILOT7D_disposition.md`; `code/lowp/pilot/LOCAL_TEST.md` |
| PROD-H bundle `jobs/PROD_H/` | **REVIEWED; for HQ, then OPS** (Sol reviews 2–7, HQ D48/D49) | `jobs/PROD_H/REVIEW{2..7}_FIXES.md`, `BUNDLE_SHA256SUMS` |
