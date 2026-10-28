# Thread B verdict on frozen A v2

**FAIL ? G1 remains closed for this artifact.** All original v1 reproducers pass, including both rescoring-containment repairs. An additional hand canary confirms that **B-N1 is only partially repaired**: stable centering fails above the new conditional fallback threshold. No contract exception is assumed.

A archive `v2.tar.gz`: SHA-256 `17bdd21a719f3c7c4d876b21e926aeac4ba447ec71634e5ba20242068661e1ff`. All24 production files match the handoff. B's full-production digest is `b2abaea2dd13e9ecccb19c9b86821941f2c51ccd60a15c372c40e83b0b207ded`; its recipe and file identities are in `A_V2_IDENTITY.json`. A's32/32 regression claim does not replace B evidence.

## Residual B-N1-R2 and minimal reproducer

Frozen `core/v3_preprocess.R:37?67` retains ordinary subtraction when the centered maximum exceeds sqrt(eps). On this finite, nonconstant represented vector it does not select its stable fallback:

```r
source("a_code/core/v3_preprocess.R")
x <- c(1, 1, 1 + 2^-24 + 2^-52, 1)
z <- v3_standardise(x)$z
print(z, digits=17)
max(abs(z - c(-.5, -.5, 1.5, -.5)))
mean(z)
```

Writing the positive represented contrast as d, the exact mean is1+d/4 and sample SD is d/2. Therefore the exact standardized vector is `(-.5,-.5,1.5,-.5)`, independently of any numerical oracle.

| Quantity | Expected | Observed for both X and y |
|---|---|---|
| Standardized vector | (-.5,-.5,1.5,-.5) | (-0.49999999813735474,-0.49999999813735474,1.5000000018626451,-0.49999999813735474) |
| Maximum coordinate error | <=2e-12 | 1.8626452602532595e-9 |
| Mean | zero within prepared-data tolerance | 1.862645232497684e-9 |
| Stable fallback map | accurate centering required | NULL; fallback not selected |
| Q and affine log-m difference | Q=2.85; difference<=1e-9 | PASS; difference0 |

The coordinate error is about931 times the unchanged prepared-data tolerance (`test_score.py:38`, frozen before A inspection). This is a centering contract failure under Part I and R-5; **no likelihood or selection error is claimed on this particular case**.

The independent v2 reviewer proposed this additional input and exact answer before its execution. It is an added repair-completeness check, not falsely labelled a pre-A fixture. The original one-ULP canary passes. No tolerance was changed.

Full command: `Rscript --vanilla v2_nearconstant_R5.R a_code fresh_output`. Saved laptop evidence: `phase2_v2_containment_20261022/evidence/nearconstant_R5/actual.json` and `actual.rds`. Command and worker exit1. Preserve v2 and route this reproducer to A; B made no production repair.

## Every v1 reproducer and R-5 item

| Item | V2 disposition | Evidence |
|---|---|---|
| B-N1 original X/y | PASS original; FAIL repair completeness | Original one-ULP coordinates/Q/affine score pass. Additional failure above. |
| B-N2 shapes | PASS | Vector X and row/column-matrix y invalid_input; all13 input/seed/precedence checks pass. |
| B-O1 cache500p | PASS | Actual p30 final setting15000; calibration500p independently source-reviewed. |
| B-O2 timing | PASS | All200 supports have exactly k*=7 at n28,p14,K14. Actual sink bit-identical to sequential scorer sum, -9286.326293893027. Separate operator replay passes. |
| B-O5 provenance | PASS | Actual exact fit records phase=exact, mechanism=enumeration. |
| B-A1 roles | PASS | hpm primary; pip05 S0; fixed adopted policy. |
| B-A2 conditions/status | PASS | Successful exact/completed records become warning on captured conditions; failed stays failed. |
| B-A3 early statuses | PASS | y_constant/no_predictors failed; support/k NA; returned empty HPM retained as empty audit string. |
| B-A4 diagnostics | PASS within fixtures/source review | R-1 quality OR and codes on both rows, including failures; informational codes never alter status/selection. |
| B-A5 failure audit/PIPs | PASS | Returned support retained for audit; unavailable PIPs remain NA. Conditional supplied-PIP fixture distinguished from actual early returns. |
| B-A6 folds | PASS | fold_seed/fold_sha256 and converged NA despite stale design values. |
| B-A7 verbatim conditions | PASS within handler/writer scope | Actual extracted handlers preserve message `verbatim \| message\n\n` and warning `verbatim warning\n` through mapper, CSV and RDS. The backslash before the table delimiter here is Markdown escaping; it is not part of the tested message. |
| Inherited-final rescoring | PASS controlled faults | Real scorer failure before best is rescored and after best/before later model: numerical_failure, original HPM/F/provenance retained, completed calibration retained, no final estimates. |
| Candidate-V rescoring | PASS controlled faults | Preliminary/rebuilt V failures return normal status without partial V vectors; completed pilot/diagnostic/grid/snapshot records and last completed E1/E2 retained. |

All90 I.8 clauses, I.6 record obligations and R-1 fields are covered in `CLAUSE_REVIEW_v2.md`; `v2_review.md` independently reviews the complete production-only diff with current source references. Seven executable files changed. Scorer, engine, start, blocks, ledger and RNG implementation files remain byte-identical. Source-review PASS is not exhaustive runtime certification.

## Full battery and smoke results

The main Owls worker completed all10 commands with exit0. Seven independent reference suites pass: scorer including hand/80-digit mpmath checks, start, moves, semantics, protocol, protocol-extra and adapter. A-versus-B comparisons pass251/251 across six fixtures and94 feasible models, covering log m/BF/prior/F/Q, exact evidence/PIPs/HPM ordering, blocks/tables/convolution and feasible pi0 probabilities.

The first and only v2 A start-law family passes: four pooled joint G-tests,100000 draws each, seeds2026102201..04,stream200. Pools use expected mass only with minimum expected count5. Holm familywise alpha=.001; p-values .33201321351974555,.9577686717683933,.377939562351717,.5231406803094012; all adjusted p-values1. Raw draws/hashes precede p-value computation. No statistical retry, retuning or seed change occurred.

Actual elementary move matrices pass the unchanged B oracle on four tiny state spaces at phi=0,.37,1: all14 verifier groups pass. Seven resampling boundary cases and p1 actual whole rounds pass. Ten native semantics cases cover HPM/primary pip05/cut_group/certification predicates. All36 valid adapter fixtures pass; the historical invalid synthetic completed/global-certified fixture remains excluded and NOT TESTED. The actual-handler/writer supplement passes13/13 checks.

Both v2 smoke bundles were identity-verified and rescored from saved c100 inputs and reported original HPM indices, without truth or regenerated inputs:

| p / HPM size | B log m | B log prior | Stored A F | Absolute F error |
|---|---|---|---|---|
| 500 /15 | -7.037691418512907 | -76.28958013640866 | -83.32727155492012 | 1.4495071809506044e-12 |
| 1000 /14 | -6.975123116563736 | -81.86193309502984 | -88.83705621159417 | 5.968558980384842e-13 |

Both pass1e-8. A stores F, not direct HPM log m. The comparison is B log m+B prior against A F, equivalently A F minus B prior against B log m. This is not a separate stored-likelihood measurement or global-optimum certificate. Input/output/array hashes and HPM indices are in main `evidence/auxcheck/smoke_comparison.json` and `SMOKE_INPUT_IDENTITIES.json`.

## Containment, adaptations and limits

Six cases pass: healthy control, inherited-before, inherited-after, preliminary V, rebuilt V, and rebuilt V after completed E1/E2 failures. The harness executes actual frozen production bodies with B-only tiny internal budgets at n8,p3,seed2026102205. Internal z corruption forces the real Cholesky/refactor/augmented-QR failure chain, then restores data. The last case additionally changes only completed diagnostic summaries to make retention checks nonvacuous. Actual native records and production mapper/writer envelopes are saved. This checks the ruled handlers; it does not show that valid study inputs naturally reach these faults or validate production budgets.

The executed containment snapshot predates the author's final addition of the same centering canary. `v2_containment_final_addition.patch` records the difference. The six-case executed source remains in `runs/phase2_v2_containment_20261022/`; the parent separately executed the reviewer-specified hand canary. The final combined author file is not claimed executed.

The first supplemental handler harness failed on an R AST missing formal argument before assertions. The independent operator added only a missing-argument guard, retained original source/log/failure, and ran the repaired13-check supplement once. This is a B harness defect, not A evidence. `v2_independent_execution.md` details it. Actual handlers and mapper/writer were exercised, not condition injection through the full study input/fitting/resume pipeline.

The provenance assertion was transparently strengthened to exact enumeration under R-5. It implies the former non-null predicate; both requirements pass. No statistical reference formula, tolerance or family changed. General p>=2 exact whole-round matrices, every rare path, full2^20 enumeration and bitwise prototype parity remain outside B's dynamic certification. The tiny p3 healthy control is not a whole-round transition proof. Synthetic assembly uses identical island PIPs and cannot distinguish alternative pooling weights; equal pooling remains source-reviewed.

## Identity, retention and disposition

B's reference receipt remains SHA `86158e437f194f77f9ea09864d264830123fdb384d4ebe205d793a37f761b62a`; criteria remain SHA `234bcd705a5152c1caa190c39b979066f9bd161fc1c0faadec11af6b7884ec03`. No prototype, A test/reference source, truth or holdout was read. B edited only its own folder. V1 evidence remains preserved.

All numerical execution occurred on Owls: persistent workers, nice19, one CPU, threads1,2GiB address-space limit, load/memory admission, one B SSH at a time. No NOTS or SSH-config edits. Both authorized Sol high delegates are complete; no jobs remain.

Laptop root: `C:/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/B_verify/`.

| Archive | SHA-256 | Verified files |
|---|---|---|
| phase2_v2_main_20261022.finished.tar | 05c68c8c3c522caa7d587d2754a7d4d45a9a353d3077a2a29271e4db632f733a |194 |
| v2_independent_execution_20261022T2208Z.finished.tar | b1ab5057b5ea41e6883ec7443c0945423d4beec7e7be55fc13eab4c5e1c44bb5 |105 including manifest |
| phase2_v2_containment_20261022.finished.tar | dee7d949ff998862217baffd5f46275f435e9fc445794185356a1be8deecc26c |146 |

Archive and every-file hashes verified. Selected remote bytes matched before removal at22:12:30Z. `ARCHIVES_v2.json`, `CLEANUP_RECEIPT_v2.json` and `RUNS_CANDIDATES.md` retain paths, commands/PIDs, seeds, environments, timing/RSS, exits and receipts. Remote sources/manifests remain. B-scoped ledger audit90/90 matching, zero missing/mismatched/unledgered files in audited directories; root files untouched, candidates await lead merge under R-2.

Verification labels remain scoped: administrative tooling and reusable fixture/export plumbing (adapter/smoke exporters, repaired handler harness, separate canary serializer) remain labelled unverified where full separate-author execution verification was not completed. Their output bytes, actual production source and exact hand-answer checks are inspectable; they are not publication-approved reusable core. Frozen oracle/comparison units and separately authored/executed containment units carry their own verification evidence. This verdict is a deployment rejection, not production approval.

**Lead action:** preserve frozen v2; route residual B-N1-R2 and its minimal reproducer to A; keep fixed criteria and G1 closed. B stops after this verdict. A later NOTS deployment still requires the instructed one-time backend rerun after the lead opens it.

Issued UTC: 2026-10-22T22:19:01.052991+00:00
