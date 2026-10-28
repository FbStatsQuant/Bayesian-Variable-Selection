# G9 c050 independent recount

Status: FINAL. Strict G9 FAIL.

DEFECT - F1/F2/F3 CV-min and CV-1se size-flag counts are published as NA. PREREG R1 specifies selected k > 37 counted for every rule in the F families. Recovery outcomes and all other requested numerical quantities match. No scoring source or output was edited.

| Run/method | Scale | Production array | G9 | Differing published cells |
|---|---|---:|---|---:|
| F1 | c050 | 2332157 | FAIL | 224 |
| F2 | c050 | 2329049 | FAIL | 224 |
| F3 | c050 | 2329050 | FAIL | 224 |
| F4;F4_SCAD | c050 | 2331186 | PASS | 0 |
| F5 | c050 | 2331188 | PASS | 0 |
| A1;SuSiE-L100 | c050 | 2329051 | PASS | 0 |
| A2;SSL-RS | c050 | 2330288 | PASS | 0 |
| A3 | c050 | 2335200 | PASS | 0 |
| SuSiE-refine | c050 | 2335201 | PASS | 0 |
| SuSiE-refine | c100 | 2335202 | PASS | 0 |

Independent final: 2026-10-21T23:16:09.801755+00:00; local execution local_20261021T231030Z, exit 0. Audit source C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\02_Experiments\F_2026-10-19_benchmark_study_n200\Benchmark_Study_20261019\verify\recount\c050\local_code_20261021T2311Z. Recount job 2339926 from the superseded remote attempt was not used for this verdict. Production IDs are fit arrays, not recount jobs.

Truth: all 1200 production truth_scoring RDS files match the manifest and the independently reconstructed active placement and full beta vectors. Support truth is unchanged across scales. No truth defects. The duplicate truth/p0500 and truth/p1000 tree remained permission-denied and was not copied; the brief's authoritative truth_scoring copy was used. No permissions were changed.

Coverage: 120,000 per-case/rule rows across both scales; every declared dataset/method/rule exactly once, 1,200 datasets per method. Canary reproduction fits and archived derived-rule versions excluded from analytical counts. All requested derived rows are included. 31,240 recount checksum targets, zero failures; additional local preflight checked 24,024 targets including canaries and all 110 baseline-fence files with zero failures. Every downloaded truth_scoring RDS checked against truth_manifest.csv; every downloaded raw and derived sidecar checked. No checksum sidecars existed in the scoring output trees; the final transfer generates source-side SHA-256 manifests of CSV data and verifies every copied file locally.

Independent baseline: relocated own policy_batch_20261020T103833Z (original audit job 2294336), hash fence verified. All five c100 F-derived sets PASS with zero differences; the extra comparison of the original c100 CV rows exposes the same missing flag publication, outside the derived-only subset.

Comparison: 3,960,484 independently mapped scientific cells in 239 table comparisons. All 120,000 case/rule rows, TP/FP/FN, exact/error type, all sel_a01..14, supports, selection sizes, statuses, design/input hashes, and raw roles agree exactly. T1/T2/T3 counts, sums, means and failure/flag counts agree except the documented K37 publication cells. No real-valued precision differences observed; strict tolerance is zero. The separate metadata checks validate all per-run/combined cell copies, paired run IDs/roles and label consistency. Timing, convergence and other diagnostics outside the G9 brief are not newly audited.

Paired analysis: 60,000 dataset_id joins, 700 aggregate rows, 5,600 numerical cells, 0 differences. Joins use dataset_id across scales, never scale-specific case_id; exact recovery contingency cells and no-unpaired counts match.

Differences: 1,344 published cells across 168 unique run/method/rule/p/scenario flag keys (84 c050 and 84 c100 in the initial capture; duplicated across local/global T1, rules_long, caps and T6). Each expected count is nonzero. Example c050 F1 cv_1se p1000 S1: independent 57, scoring NA. Full keys and both values: C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\02_Experiments\F_2026-10-19_benchmark_study_n200\Benchmark_Study_20261019\verify\recount\c050\local_batch_20261021T231030Z\comparisons_verified\differences.csv. Unique original defect table: C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\02_Experiments\F_2026-10-19_benchmark_study_n200\Benchmark_Study_20261019\verify\recount\c050\local_batch_20261021T231030Z\FLAG_PUBLICATION_DEFECTS.csv.

R1 flag scope: K37 applies to the F1-F5 families. Published Bayesian K37 cells are inapplicable NA and are not asserted to be zero. Independent extra Bayesian threshold tallies remain available in metrics_long.csv. Editorial labels/column headings are checked for publication consistency; numerical recovery cells are independently recomputed.

Independence: no real scoring outputs were opened before the complete corrected final fence. Source-side raw inputs and truth only produced the numbers. Scoring capture was opened 2026-10-21T23:16:26Z, after independent finalization. No scoring code was read. The first refinement-registry audit was preserved as an auditor configuration failure, then corrected to pip05/S1 and cslead,bfdr10/S0. All 110 numerical output files are byte-identical before/after that registry correction. Transport timeout/locked-duplicate-truth evidence is retained in FAILED_ATTEMPTS.md and logs/.

Evidence root: C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\02_Experiments\F_2026-10-19_benchmark_study_n200\Benchmark_Study_20261019\verify\recount\c050\local_batch_20261021T231030Z. Independent fence: 040510794641b30a1e5304c16e6dd03c82133b2b9af92cd6a6dadc0349f2eb9a. Environment: Python 3.12.7, numpy 1.26.4, pandas 2.2.2; R 4.4.1 used only as a truth serialization adapter. No simulations or production fits were run locally. All code remains unreviewed; G5/code review is separate.

2026-10-22T14:00:59Z: Lead confirmed: "Use validated truth_scoring". The validated truth_scoring copy is the authoritative truth for this audit. The locked duplicate truth tree is not required. The completed recount already used this source; independent numbers and the strict G9 verdict are unchanged. No remote connection or numerical rerun occurred.
