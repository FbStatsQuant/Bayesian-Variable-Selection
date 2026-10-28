# F_analysis_claude: STATUS

Lead: Claude Opus 5.5 (Campaign 2 ANALYSIS). Contract: ../BRIEF_CLAUDE.md. Protocol: miscellaneous operations.
Updated: 2026-10-23 ~02:00Z.

## Phase
**Phase 1 COMPLETE.** Waiting for `E_ops_claude/OUTPUTS.md` to start Phase 2. Nothing is running.

## Phase 1 results
1. **Takeover.** D's pipeline was copied to `pipeline/` and hash-verified identical before editing (`D_PIPELINE_COPY_SHA256.txt`). D_analysis was not written to. The diff is in `DIFF_vs_D_pipeline.patch`; the reasons are in `README.md`.
2. **D-F1 fixed** (`pipeline/native_contract.R`). The heuristic-bound label is required only when `global_certified` is TRUE, and A's native label `heuristic (not a validated interval bound)` is accepted. Two new mock regressions:
   - certified and unlabelled → rejected;
   - uncertified and unlabelled → passes every native/R-1 check.
3. **D-F2 closed for completed fits** (`phase1_devsmoke/`).
   - The real A v2 bundles `smoke_v2_20261022T2315Z` (dev_p0500/p1000_S4_r001, c100) were scored end to end: `smc` mode, R-1 profile, assessment mode, unchanged `score.R`. Exit 0.
   - Dev truth comes from the unchanged `gen_dev_data.R`. The stored input file, X and Y hashes match the dev manifest. The regenerated X, Y and noise agree to ≤ 5.3e-15; bit equality is not expected across BLAS builds. The active set and β use no RNG.
   - p500: hpm and pip05 **exact** (14 TP, 0 FP, 0 FN), diag_flag FALSE.
   - p1000: hpm and pip05 **extra_only** (14 TP, 1 FP = index 834 with PIP 0.557, 0 FN), diag_flag TRUE (`final_check_E2;cut_group`).
   - An independent recount from the raw RDS and the truth, without benchmark code: **38 checks, 0 mismatches**.
4. **Relocatable, one command:** `python pipeline/score_campaign2.py --smc-results <results/<run_id>> --ops-outputs <OUTPUTS.md> --work <dir>`. All paths are arguments.
5. **Regression:** the mock suite passes **245/245** (D's 241 plus 4 D-F1 checks), exit 0, on the final bytes. Evidence: `C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\F_analysis\validation\local_20261023T015327_862358Z`.
6. **Full-design dry run** through the wrapper (1,200 datasets × 2 scales, no SMC output), in 3 min:
   - 120,000 benchmark rule rows joined, with hash and key checks;
   - the combined `rules_long` reproduces the published tables cell-for-cell at c100 and c050;
   - spot cells equal the published SUMMARY (A2 569/582, F5 365/323, A3 574/575 with 32 flagged at p1000);
   - every SMC cell counts 100/100 (600/600) missing.
   - Output: `...\F_analysis\wrapper_test_20261023T014810Z\`. That run used the pre-LF-normalisation bytes of `run_pipeline.py` and `prepare_assessment_config.py`, which differ only in line endings.

## Phase 2 plan (on OUTPUTS.md)
1. Run `score_campaign2.py` on the pulled results. Every bundle is validated (sidecars, provenance, seeds, hashes, R-1, native) before any truth is opened. A bundle that fails validation stops the run; I report it, and never drop it silently.
2. Read RESULTS_TABLES.md and the figures. Check reconciliation: 2,400 fits = scored + failed + missing (timeouts recorded as non-recovery).
3. ONE independent Sonnet agent recomputes ≥ 40 random cells from the raw SMCBVS.csv/rds plus the truth RDS, without the pipeline, across all table types (exact counts, error types, TP/FP/FN, flag rates, recovery-given-flag, runtime, paired wins/losses), with planted canary cells whose answers I know.
4. Write `RESULTS.md` in plain language for Felipe, covering every scenario, including the ones SMC-BVS loses.

## Known residuals (not blocking)
- No real *failed* SMC fit exists, so the failed-row path is covered only by the mock suite. When the ops thread's real e2e production fit (p1000_S4_r001 c050) lands, I will also score it through the wrapper as a real production-case check, if HQ wants that before the 2,400.
- D's round-3 review finding (hollow stream entries / all-NA stage identity accepted by `native_contract.R`) is still open. It concerns validator strictness only, not scores.
- Headline comparator rules are each method's registry `primary` rules. Post-hoc and c050-preregistered K37 variants are labelled; all rules are in the long CSV.

## Requests to HQ
1. Please confirm the comparator set for the headline: the registry's primary rule for each of the 8 methods (A1–A3, F1–F5), with SuSiE-L100, SSL-RS, SCAD and SuSiE-refine (S1 arms) as supplementary rows. This is my default unless told otherwise.
2. When the ops thread writes OUTPUTS.md, please have it state the laptop results root(s) and run ID(s), plus any units rerun for infrastructure reasons, so that exactly one bundle per unit is scored.

## Agents
None spawned (0 Haiku, 0 Sonnet, 0 Opus, 0 Fable). One Sonnet is planned for Phase 2.
