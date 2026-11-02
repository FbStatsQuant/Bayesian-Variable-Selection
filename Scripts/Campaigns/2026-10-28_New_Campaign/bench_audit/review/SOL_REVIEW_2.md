# SOL review 2 — benchmark audit v2

**ACCEPT WITH FIXES.** The exact-pilot evidence repairs the principal evidentiary gap, and the whole-arm PROD-L gate is corrected. The substantive conclusions survive independent checks. This accepts the audit conditionally, not the unimplemented replacement wrapper or a benchmark release. Resolve R2-1–R2-3 before describing the deployment contract as complete; correct R2-4–R2-5 in the audit.

Scope: independent Sol 6.1 review; local only, no SSH. Existing audit, evidence, study code and results were unchanged. Only this review is retained; the temporary read-only check script was removed. Paths below are relative to `bench_audit/` unless stated otherwise.

| Round-1 finding | Status | Assessment / remaining work |
|---|---|---|
| 1. Exact recommended pilot not tested | Resolved for audit evidence | New experiment actually reads stored F1 `cv_min` beta, covers all four cells and uses the registered second-stage engine. Frozen-wrapper identity, separate development data at both regimes, timing and acceptance remain explicit pre-rerun gates, not completed validations. |
| 2. Partial PROD-L release | Resolved | §6 correctly holds the entire benchmark arm under D36.2/D36.4, exempts enumeration/SMC and does not certify F4/A1–A3. |
| 3. F3 contract/tests incomplete | Partly | Failure propagation, screening, full-p EBIC, floor declaration and test coverage are substantially improved; stable normalization and fully specified edge/schema outputs remain (R2-1–R2-2). |
| 4. Low-p exact OLS reference absent | Resolved in audit | New code and measured cost are explicitly required; comparison conventions and the implement-or-HQ-defer gate are stated. The reference itself is still unimplemented. |
| 5. ABESS overstatement/polish scope | Partly | Settings, suboptimality, c100/S1/S4 scope and the S1 counterexample are corrected; polish tolerance/cap/ties still differ from or omit the evidence algorithm (R2-3). |
| 6. Numbers/scopes/verdict language | Resolved, with minor corrections | FP ranges, path counts, F3 9/600, qualified ORGANIC, alpha sensitivity and low-p uncertainty are corrected. See R2-4 for new scope wording. |
| 7. F5 chain/evidence checklist | Resolved | W6 supplies both-scale accounting, hashes, environment and 96-cell recount; §5 lists the required redeployment evidence. Its hash-to-manifest and saved-candidate checks retain the limitations W6 states; they do not freshly authenticate every input or certify global search. |
| 8. Runtime provisional | Resolved | 75–90 core-h is a reasonable planning allowance: historical F1 73.2 plus 2–4 estimated second-stage core-h and margin. Local seconds are not measured NOTS throughput; dev <2 core-h and the stored-beta shortcut are also estimates. The required pilot must replace all estimates. |

## Findings and exact fixes

**R2-1 — SHOULD-FIX: §3 still gives an unstable weight normalization.** Finite positive raw weights do not make `m*w/sum(w)` safe: `b=c(1e-308,1e-308)` gives finite `w=c(1e308,1e308)` but normalized weights `NaN,NaN`. Fix: scale first, e.g. `r=w/max(w); v=m*(r/sum(r))`, then assert every v is finite and strictly positive and its sum is m within tolerance. Declare failure for unrepresentable reciprocals or underflowed factors; never silently floor/drop them. Add overflow-of-sum and underflow fixtures beyond the current 1e-12 example.

**R2-2 — SHOULD-FIX: §3 is mathematically sound in ordinary cases but not yet a complete output/edge contract.** A genuine empty pilot should yield the null; the singleton soft-threshold solver is appropriate; failed/nonfinite/KKT-failing pilots must fail the fit. However, specify m=0 outputs: every registered row, empty support/k=0, p-vector zeros, zero predictions, RSS=sum(y^2), and explicit lambda/index/path/diagnostic sentinels. Specify the singleton full-data and training-fold Gram denominators and check both CV choices against an independent scalar solution. The new evidence has m=35–163; its `m<2` fallback simply returns keep and does not validate either proposed edge implementation.
Fix the schema explicitly: enumerate retained/new rule IDs and roles (including the existing `ebic05` and K37 companions), define coefficient-vector provenance for each EBIC-selected path occurrence versus its OLS scoring refit, retire ridge-only diagnostics (`ridge`, `ridge_resid_max`, `ridge_fold_mse`) and obsolete floor fields/code (`eps_floor`, `n_floored`, `floored_selected`), and update consumers as well as config/metadata. Add negative controls for nonpositive/nonfinite RSS and second-stage selected-point KKT failure. These are preimplementation specifications/tests, not failures observed in the 120 ordinary cases.

**R2-3 — SHOULD-FIX: §4 does not state the exact polish algorithm claimed in §7.** `work_abess/scripts/lib.R:52–69` uses maxit=200 and accepts `cand < best - 1e-9*max(1,best)`, a relative tolerance, with first-encountered winners in its numeric scan; it does not implement support-key tie breaking. The recommendation says only “tolerance 1e-9 on RSS; iteration cap stated; ties broken by key.” Fix: give the actual numeric cap, relative acceptance rule and scan/tie policy if reproducing W5; otherwise label a changed prospective companion and validate it separately. Keep the stored-path-versus-refit transfer check. The frozen ABESS keep/disclose conclusion is unaffected.

**R2-4 — MINOR: tighten the new experiment's scope.** Its r011–r015 inputs/results are from the production archive, not the study's separately sealed `holdout/` manifest (study `RUNS.md`, held-out-generation row). Replace unqualified “held-out” with “production replicates held out from the earlier pilot exploration,” retaining the outcome-informed caveat. Label 23/30 versus SCAD's published 76% as a descriptive, unequal-sample comparison, not equivalence/generalization evidence. The §3 test diagnostic “dev S1 ... 13/30 ... 29/30” is pooled p500/c100 S1–S6, not S1; name that cell and cite W4 for the ridge truth-on-path count.

**R2-5 — MINOR: correct F3 c100 job time.** §3 associates job 2279914 with 21:57Z. Study `RUNS.md` records submission at 22:19Z on 2026-10-19; 21:57Z is the snapshot/run-ID time. Correct the distinction (also documented by W3).

## Independent checks rerun

Four cases, one per p × c cell; entries below give new support sizes for `cv_min / cv_1se / ebic1_K37` and EBIC exactness new/ridge:

| Case | Pilot k | New k | EBIC exact new/ridge |
|---|---:|---|---|
| p0500_S5_r014_c100 | 86 | 76 / 66 / 15 | FALSE / TRUE |
| p1000_S4_r013_c100 | 85 | 68 / 49 / 14 | TRUE / FALSE |
| p0500_S1_r011_c050 | 71 | 63 / 56 / 14 | TRUE / FALSE |
| p1000_S6_r015_c050 | 58 | 52 / 47 / 14 | TRUE / FALSE |

- **12/12 case-rule records match** every numerical/logical CSV field except timing, which is machine/run dependent: pilot size, truth inclusion, KKT flag, truth-on-path, new/ridge sizes and exactness. The CSV does not store new support keys or coefficient vectors, so it cannot establish their byte-level reproduction.
- **Pilot binding:** read `F1.rds$beta`; checked its nonzeros against stored `cv_min` support, CV-min index against stored CV curve, lambda and common folds. Independent local full-path F1 refits retain identical supports; maximum beta differences are 1.13e-14, 1.38e-14, 1.92e-15 and 1.09e-14 respectively. Cross-version bit identity is neither claimed nor needed for this saved-beta experiment.
- **Independent second stage:** direct glmnet calls with thresh=1e-16/maxit=1e7, manual fold predictions, weighted MSE/SE and CV choices; independently computed KKT and OLS EBIC. Compared with the study engine using the documented local argument override: full coefficient paths identical and CV summaries within 1e-12. Maximum relative KKT across the four cases: 3.23e-8 (tolerance 1e-5).
- **Full-p EBIC:** independently used original p=500/1000, null plus distinct mapped supports, cap37, no-intercept OLS, rank/RSS checks and criterion/k/key ordering. Negative control using screened m changes p500/c050 from the correct size14 truth to size16, and p1000/c050 from size14 truth to size20. The manager script also explicitly passes original p.
- **Aggregate tie-out:** all 360 rows comprise exactly 120 cases × 3 rules. All summary counts reconcile, including K37 new/ridge 23/13, 23/8, 13/2, 9/0; paired-only gains/losses, truth inclusion/path and zero KKT failures agree. F2 table internally totals 2,399/2,400 alpha=.9 and one .5 in p500/c050/S4. W6 comparison CSV has 96/96 agreements; this round inspected its script/report, not a fresh all-F5 recount.
- **Citation:** supplied ZvB text §2.1 and Remark 2.4 supports a lasso initial estimator and explicitly distinguishes its max{1/|b|,1} weights from Zou's inverse-power weights. V2 discloses the unadopted floor. It does not establish F1 prediction-CV/EBIC tuning as the paper's theoretical tuning; retain the narrower literature-motivated claim.

Command: `& 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' --vanilla '<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/review/scripts/sol_review_2_checks.R'` (temporary script, removed after inspection).
Final run: 2026-10-30 03:26:31–03:27:45 UTC, exit 0; Windows 11, R 4.4.1, glmnet 4.1-10, Matrix 1.7-4. Script SHA-256 `7d2afcf5a2a2d9b1bb70261fcbd741305a7731d9ee08eb422b5f3f5d4bdf75f1`. Initial attempt stopped on named-versus-unnamed index comparison; corrected before the final run. Only startup locale/package-build warnings occurred in the completed run.
