# Independent review of CONFORMANCE.md

Reviewer: Sol 6.1, 2026-10-28 (America/Chicago).

**Deliverable verdict: ACCEPT WITH FIXES.** The inspected statistical kernels and orchestration support a qualified executed-run PASS. I found no additional discrepancy in the requested high-risk sampling paths that establishes a need to redeploy the statistical core. However, the categorical statements that every difference is cosmetic/wording and that the method's outputs are unaffected are too strong. The classifications, validation coverage, and several factual statements need the corrections below. No finding below establishes that a different allocation would have completed all six censored fits.

Scope: only the named methodology, baseline core/study files, runner/release/output documents, worker audits and scripts were read. No SSH/network, compilation, simulation, or fitting was performed. Only this review file was written. Read-only saved-output inspection used R 4.4.1 (`Rscript.exe --vanilla -`, code supplied on stdin) on three distinct production RDS files: `p1000_S2_r019_c050`, `p1000_S5_r044_c100`, and `p0500_S5_r088_c100`. The second was reopened to inspect its final guard checkpoints. Production-copy hash identity is supplied provenance, not independently re-established in this review. Original prior-audit documents, original R-1 ruling, PATCHES.md, and D1/D5 decisions were outside the permitted inputs and were not read.

Path convention: `T` = `01_Methodology_and_Theory/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md`; `core/...` and `study/...` are beneath `C/code/core/v2_1_baseline/`; `runner/...`, GO_2400.md and OUTPUTS.md are beneath `ROOT/02_Experiments/H_2026-10-22_smcbvs_v3_deploy/E_ops_claude/`; other audit paths are relative to `C/conformance/`. Citations use the inspected files' current line numbers.

**Independent high-risk code checks.**

- RB recording precedes the coordinate's uniform draw, at the current within-round state (`core/cpp/v3_engine.h:113–131`). Recording is enabled only for the four measured rounds, and divided by particles times measured rounds (`core/cpp/v3_engine.h:342–364`; T:430–437).
- Evidence weights, increment and ESS use incoming particles, before resampling and the move round (`core/cpp/v3_engine.h:317–331`; T:418,439–447).
- All seven calibration triggers feed escalation; E1/E2 use the last iteration, E3/local_limit accumulate within the tier; preflight precedes tier 1 and no second escalation occurs (`core/v3_calib.R:60–61,101–118,141–168`; T:403–416).
- HPM includes fresh scores, with cache hits/held states already represented; island maxima additionally count their own cached/held scores (`core/cpp/v3_ledger.h:82–110`). Calibration stores persist across tiers; their top store contains the calibration HPM under the same size/lex order, is exported, and is rescored into final stores (`core/cpp/v3_core.cpp:398–418,576–581,696–704`; `core/cpp/v3_ledger.h:33–38`; T:426–428). Thus the all-scored HPM rule is supported by code inspection, beyond the weaker saved-output test.
- Final checks only assemble flags; the fit has one final-run call and no diagnostic-driven rerun (`core/v3_run.R:149–156`; `core/v3_fit.R:123–143`; T:418–420). Runner rerun eligibility excludes a finished `.done` unit (`runner/task.sh:35–48`); OUTPUTS.md:10 reports no actual reruns.
- The mandatory exact-branch decision uses the stated threshold and early saturating integer count (`core/v3_preprocess.R:19–32`; `core/cpp/v3_core.cpp:69–81`; T:245–251). It is not exercised by this production arm.
- Gibbs omits infeasible cap additions, records zero and still consumes one uniform; local search skips additions at K and preserves size in swaps (`core/cpp/v3_engine.h:115–131,393–404`; T:226,424,518–519).
- Seed derivation, stream initialization/continuation and final streams agree across adapter, runner and core (`study/adapter.R:88–95,378`; `runner/make_tables.py:35–42`; `core/cpp/v3_util.h:36–60`; `core/cpp/v3_core.cpp:435,562–565,594–595,635–637`). The named Part I does not itself contain the Part II data-seed formula; I did not read beyond its authorized lines to independently verify that citation.

**Numbered findings**

1. **[should-fix] S1 changes method-output availability; its authorization, rather than harmlessness, supports PASS. S2 has a different basis.**

   Evidence: CONFORMANCE.md:11–14,64,67,93–96; T:163,182,457,476,570; GO_2400.md:7–10,26; `runner/submit.sh:56,68,76`; `runner/task.sh:20–22,51–53`; `study/adapter.R:99–107,227–257,269–288`; `study/SCHEMA.md:76–86`.

   S1 is an output-affecting study/resource policy: it determines whether the native fit returns `completed` with estimates or `resource_limit` without them. It is inaccurate to say it changes censoring but not the method's outputs. Part I's prose allows a declared allocation that is only *normally* the actual request; its settings table says actual job request. GO_2400 explicitly adopts the per-unit exception, and the runner implements that release policy. Therefore this is not an unauthorized implementation change. Under the requested classification convention, label the difference from the literal master-table allocation as **behavioural at the study/resource-policy level, explicitly authorized by GO_2400**, with a wording correction to reconcile Part I. The abstract guard formula still conforms.

   S2's asymmetry is explicitly documented in the allowed SCHEMA: selected-tier grid status versus local-limit anywhere. The implementation matches it. **Wording/stale OPEN** is defensible relative to that adopted written policy; the original R-1 text was not available for independent confirmation. That rationale should replace any suggestion that diagnostic labels are outside the definition of outputs. No inspected code lets this flag alter HPM/PIP/evidence. The claim that headline analyses do not use it cannot be verified from these inputs.

   Concrete fix: cite GO_2400 C1 and SCHEMA's R-1 definition in the verdict/table; distinguish authorized behavioural policy from a code defect. Remove “not the method's outputs” and the suggestion that a planned future rerun makes the historical verdict/classification immaterial. State the conformance basis for the historical run independently of D5/P5.

2. **[should-fix] D30 is a conditional algorithmic difference, and Gaussianity is not a proof that it cannot fire.**

   Evidence: CONFORMANCE.md:7–11,44,72; `work/A_code_vs_text.md:60,95`; T:128,141; `core/v3_preprocess.R:37–67,119–130`.

   The fallback changes floating-point preprocessing for near-constant nonconstant vectors, applies to both predictors and response, and could change scores and selections. Under the supplied “could change outputs” definition it is **conditional behavioural**, even if inert in the inspected sample. A nondegenerate Gaussian vector has positive probability in a sufficiently small neighborhood of a nonzero constant vector; Gaussianity alone does not exclude the condition. Already centered stored predictors could provide a separate deterministic exclusion argument, but that argument is not supplied here and must cover the response too. Zero occurrences among 86 records does not establish zero among 2,400.

   Concrete fix: classify the implementation/specification difference as conditional behavioural, document the fallback in Part I, and replace “impossible” with the observed sample result. Either qualify the executed-run claim to inspected evidence, or attach a population metadata scan/proof covering all fitted X and y before claiming this path was inactive throughout production. My three spot checks also had no `stable_centering` record.

3. **[should-fix] D03's harmlessness depends on the definition of the timed operation.**

   Evidence: CONFORMANCE.md:60; `work/A_code_vs_text.md:33`; T:182,380–393; `core/v3_calib.R:64–76`; `core/cpp/v3_runtime.h:21–26`.

   The timer includes V rescoring and snapshot work, not just the scalar grid algorithm. If “grid construction” means the narrower operation described in T:393, the extra duration enters the guard projection a second time through `elapsed + operation` and can change stopping/availability near the limit. Calling that merely wording because the difference is seconds does not establish equivalence. If grid construction is explicitly defined to include its preparation/archive work, wording is appropriate. The six actual stops in B occurred at bridge/local checkpoints, so this does not establish a realized grid-checkpoint discrepancy in the six censored fits.

   Concrete fix: state the inclusive timed-operation definition as the interpretation used for conformance, or mark a conditional behavioural resource-guard difference pending that clarification. Do not assert it is intrinsically output-neutral.

4. **[should-fix] D12's “Realised: none” is contradicted by an inspected saved fit.**

   Evidence: CONFORMANCE.md:65; `work/A_code_vs_text.md:45`; `work/B_outputs.md:38`; `core/cpp/v3_engine.h:335–360`; `core/cpp/v3_core.cpp:657–660`. Direct binary evidence: `prod_p1000_20261023T1227Z/p1000/p1000_S5_r044_c100/SMCBVS.rds`, `fit$runtime_guard$checkpoints` and the last tier's last diagnostic iteration.

   At tier 1, iteration 7, island 4, the last bridge checkpoint (stage 51) has elapsed about **23,970.09 s**, projected **23,972.82 s**, and `exceeded=FALSE`. That island then records **22.07246070 s burn-in + 10.83688344 s measured rounds** without a guard. The next local-search operation takes only **0.01429666 s**; its checkpoint has elapsed **24,003.014702624 s** against allocation **24,000.0000012 s**, and stops. An unguarded terminal stretch did cross the allocation. Zero external timeouts does not imply zero internal allocation overshoots.

   Concrete fix: say “No external timeout; at least one terminal stretch exceeded the fit allocation and was caught by the following local-search checkpoint.” Keep the classification “consistent with Part I/residual operational risk”; this is a factual correction, not evidence of an extra required checkpoint or a sampler defect.

5. **[should-fix] The claimed escalation biconditional and frozen-grid validation exceed the actual test.**

   Evidence: CONFORMANCE.md:33; `work/B_outputs/audit.R:53–55`; `core/v3_calib.R:145–168`.

   The check asserts `escalated == (frozen$tier == 1)` and **escalated implies some tier-0 trigger**. It does not assert the reverse: an erroneous completed tier-0 run with a stored trigger would pass. It also trusts stored triggers instead of recomputing them from the calibration archives. Final schedule checking compares lengths only; different temperature values of the same length would pass.

   Concrete fix: for completed fits assert `escalated == any(tier0_triggers)`, allowed tier values, one/two attempted tiers with matching IDs, and the appropriate tier budgets. Compare each island's actual `phi` vector with `grid[-1]` and the frozen grid. Describe trigger-storage consistency separately from independent trigger recomputation, unless the latter is added. The static code check above independently supports the actual escalation rule.

6. **[note] Several B checks are sound assembly checks, but do not independently validate the underlying mechanism.**

   Evidence: CONFORMANCE.md:29–35; `work/B_outputs/audit.R:33,41–57`; `work/B_outputs.md:62`; `core/cpp/v3_ledger.h:87–110`.

   HPM versus the saved top store is a valid consistency check, not a replay of “every model scored”: HPM and top store share the same ledger update path. A model omitted from both would escape it. CONFORMANCE's explicit top-store wording is appropriately narrower. Similarly, PIP versus saved RB accumulators tests normalization, not before-draw timing; evidence versus saved increments tests assembly, not incoming-particle timing. The diagnostic check calls the actual production `smcbvs_diagnostics` helper, so it is independent of neither that policy implementation nor its mistakes. B discloses that reuse; it usefully checks RDS-to-CSV consistency and is not a vacuous comparison of a value with itself. The seed/stream check compares a fit seed to CSV and a static `stream_map` to `0:13`, not actual stream execution or draw consumption.

   Concrete fix: retain these checks with those explicit limits, and cite code inspection for timing, coverage and RNG implementation. For a stronger saved-output cross-check, compare final HPM against calibration HPM and inherited HPM, and inspect actual island stream metadata. The directly inspected completed fit had equal calibration/inherited/final HPM F, streams 10–13, 31 stages in each island, and zero RB-normalization error; its final low-ESS flag did not cause another escalation.

7. **[should-fix] Some reported test coverage is missing from the saved script.**

   Evidence: CONFORMANCE.md:23,36–37; `work/B_outputs/audit.R:34–39,65`; `work/B_outputs.md:11,59–60`.

   The resource test asserts only an exceeded checkpoint exists and both study statuses are failed. It does not independently recompute the guard inequality, assert primary `support` is unavailable, or compare `support_audit` with the returned HPM. Budgets L/ell/H0/T0 are recorded, but the script explicitly marks their definition check unperformed; CONFORMANCE presents all budgets as one passed test. The formulas are available in `core/v3_preprocess.R:19–30` and T:151–159, and I find those definitions correct. Manager checks may supplement the worker, but their commands/assertions are not in the supplied B scripts.

   Concrete fix: separate recorded values, worker assertions and supplemental manager verification. Preserve the supplemental assertions/output, including the sample basis. Add a direct `projected = elapsed + operation`, `projected > allocation` check and support/audit-label assertions, or narrow the resource-test wording. My two resource spot checks do preserve HPM only in `support_audit`, with `support=NA` and no reported estimates; that independently confirms two cases, not six.

8. **[should-fix] D41 is incorrectly grouped as an L0-only issue, and that table row is malformed.**

   Evidence: CONFORMANCE.md:63,85; `work/A_code_vs_text.md:69`; T:447,551; `core/v3_run.R:121–124`; `core/v3_fit.R:99`.

   A explicitly cites the current master requirement for relative-scale lower-bound reporting. The output has a full-scale lower bound and relative evidence, but no separately reported relative lower-bound field. Marking L0 superseded does not resolve that Part I reporting question. It is derivable without a fit change as `log_Z_rel_m0 + log(0.05)`; a reporting/wording resolution is reasonable, but it is not an L0-only mismatch. The grouped row also contains six cells beneath a five-column header (`as found` is an extra cell), obscuring class/action.

   Concrete fix: give D41 its own row, explicitly resolve whether a derived relative bound meets the reporting contract or add it in output assembly, and repair the five-column table. This does not require numerical rerunning of completed fits.

9. **[should-fix] Correct the audit count and qualify population/prior-audit claims.**

   Evidence: CONFORMANCE.md:19,39–44,81–89; `work/A_code_vs_text.md:31–79,143,152–154,165–166`; `work/B_outputs/audit.R:42,53`; `work/B_outputs.md:4,68–80`.

   A has **31 D-rows**, not 36: D01–07, D10–21, D30–32, D40–45, D50–52. Its 33 equal rows are correctly counted. “E1 and E3 never fired” is established at population scale for **final checks on 2,394 completed fits**, with six missing values; calibration trigger counts are only sampled here. The final-stage median/range appears under “Population facts,” although the supplied stage checks cover only 80 completed sampled RDS records, not all 2,394 completed fits. A describes B.1 as spot-checked and flags some inventory statements as not re-verifiable or arithmetic-only. “Verified prior audits” should not imply independent wholesale recertification of all S_A/S_B/S_C/SN findings. R-1's original text was also explicitly unavailable to A.

   Concrete fix: use 31 rows; label all final-check counts and their denominator; label the stage summary `n=80 sampled completed fits` unless a population source is supplied; describe selected prior-audit claims as cross-checked with amendments and distinguish direct code, sampled-output, population-CSV, and inherited audit evidence. Retain the supported population totals: 2,394 completed, six resource limits, 208 escalations, and 2,398 cut-group flags.

**Ten-line summary**

1. Deliverable verdict: ACCEPT WITH FIXES.
2. The requested high-risk statistical code paths conform on independent inspection.
3. No inspected finding establishes a need to redeploy the statistical core.
4. S1 is an authorized, output-affecting resource policy; reconcile it with Part I.
5. S2 matches the written SCHEMA policy; update the master's stale OPEN item.
6. D30 is conditional behavioural; D03 needs an explicit timed-operation interpretation.
7. One inspected terminal stretch actually exceeded its allocation; correct D12.
8. B mostly validates saved-output assembly; strengthen or narrow its escalation/coverage claims.
9. Separate D41, repair the table, correct 36 to 31, and qualify sample/population claims.
10. Retain a qualified historical PASS based on the declared release policy and inspected evidence.
