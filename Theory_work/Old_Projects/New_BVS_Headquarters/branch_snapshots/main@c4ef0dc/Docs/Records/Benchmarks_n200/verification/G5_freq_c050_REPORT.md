# c050 independent G5 verification — final assessment

Updated 2026-10-22T14:10:50.317411+00:00. **Overall G5: NOT CERTIFIED. F5 check4 FAIL (search limitation); F1–F4/SCAD checks3/4 PARTIAL (coefficient evidence gap).**

DEFECT — independent same-size search beats 1,477/2,424 F5 path supports across all24 sampled datasets, including109/168 selected-rule rows. Maximum relative RSS improvement is0.4857614783022256. This is a demonstrated ABESS search limitation; the independently recomputed EBIC/SIC choices over the saved candidates still pass. ABESS has no global optimality certificate.

DEFECT — F1–F4/SCAD did not save nonprimary penalised coefficient vectors. Original primary KKT and refits pass on the required samples; support-only convex reproductions do not certify unsaved coefficients. MCP/SCAD refits establish local consistency at raw ebic1 only, including neither K37 nor lam005 coefficient certification.

The lead submitted setup and six refit jobs under label20261022_c050_refit at2026-10-22T14:00:06Z. All seven completed0:0; no job was submitted or resubmitted by the verifier. The old20261021 label was never used. No corrected launch specification is needed for a process failure.

## Per-method verdict

| Method | Production run | 1 EBIC/derived | 2 CV | 3 KKT/consistency | 4 independent refit | 5 integrity | Overall |
|---|---|---|---|---|---|---|---|
| F1 | 20261021T1615Z_bench20261019_prodc050_F1_Lasso | PASS | PASS | PARTIAL | PARTIAL | PASS | PARTIAL |
| F2 | 20261021T1540Z_bench20261019_prodc050_F2_ElasticNet | PASS | PASS | PARTIAL | PARTIAL | PASS | PARTIAL |
| F3 | 20261021T1540Z_bench20261019_prodc050_F3_AdaptiveLasso | PASS | PASS | PARTIAL | PARTIAL | PASS | PARTIAL |
| F4 | 20261021T1604Z_bench20261019_prodc050_F4_MCP_SCAD | PASS | NOT_APPLICABLE | PARTIAL | PARTIAL | PASS | PARTIAL |
| F4_SCAD | 20261021T1604Z_bench20261019_prodc050_F4_MCP_SCAD | PASS | NOT_APPLICABLE | PARTIAL | PARTIAL | PASS | PARTIAL |
| F5 | 20261021T1604Z_bench20261019_prodc050_F5_ABESS | PASS | NOT_APPLICABLE | PASS | FAIL | PASS | FAIL_SEARCH_LIMITATION |

PARTIAL means the measured scope passed with no numerical discrepancy, while required unsaved-vector evidence remains unavailable; it is not a full G5 PASS. The lead’s c050 sample sizes supersede the original brief:30 KKT cases/p and12 refit cases/p, stratified over six scenarios.

## Coverage and numerical maxima

| Method | Cases | Candidates | Original rows | Derived rows | KKT/consistency cases | RSS relative max | Criterion absolute max | KKT/stationarity max | Derived RSS absolute max | Derived criterion absolute max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| F1 | 1200 | 53922 | 4800 | 2400 | 60 | 2.2536727050008174e-15 | 4.092726157978177e-12 | 2.432474682095842e-08 | 1.1368683772161603e-13 | 2.6716406864579767e-12 |
| F2 | 1200 | 53970 | 4800 | 2400 | 60 | 2.1921573603341037e-15 | 4.092726157978177e-12 | 2.608130698911193e-08 | 2.2737367544323206e-13 | 2.7284841053187847e-12 |
| F3 | 1200 | 64773 | 4800 | 2400 | 60 | 2.132821823253096e-15 | 4.092726157978177e-12 | 3.289382611779135e-08 | 1.1368683772161603e-13 | 2.7000623958883807e-12 |
| F4 | 1200 | 73682 | 3600 | 4800 | 60 | 1.0769163338864018e-14 | 5.229594535194337e-12 | 8.05235039083585e-08 | 1.1368683772161603e-13 | 2.7284841053187847e-12 |
| F4_SCAD | 1200 | 77103 | 3600 | 4800 | 60 | 9.373017364602322e-15 | 4.433786671143025e-12 | 9.591331333949626e-08 | 1.1368683772161603e-13 | 2.7284841053187847e-12 |
| F5 | 1200 | 121200 | 3600 | 4800 | 60 | 8.648782167617591e-15 | 4.661160346586257e-12 | 2.41140440948584e-09 | 1.1368683772161603e-13 | 2.6432189770275727e-12 |

F1–F3 KKT maxima in the table are normalized violations (tolerance1e-5); MCP is original-scale and SCAD internal-scale absolute violation (tolerance1e-4). F5 is stationarity divided by the declared master tolerance (must be <=1); all101 points are checked in60 cases,6,060 points. Full absolute/normalized maxima, lambda discrepancies and per-cell evidence are in each saved summary. Check4 measured maxima are reported separately below; historical local-only zero accumulators are unmeasured placeholders.

All1,200 cases per method are independently scored with zero-intercept OLS, rank/validity, cap100, null/deduplication and exact criterion/k/ASCII-key ordering. Derived K37 restricts independently scored candidates to k<=37. MCP/SCAD lam005 uses lambda>=0.05*zmax computed from original X and c050 y, and passing occurrences within that segment. F5 SIC uses n*log(RSS/n)+k*log(p)*log(log(n)), with smax19/17. Every derived_from value binds to its source RDS hash; current CSVs authenticate against SHA256SUMS, excluding preserved v1 tables.

Applicable CV means/SEs are independently reconstructed from fold MSE; exact minimum/one-SE choices and F2 alpha/lambda ordering and response scaling are checked. F3 ridge choice, weight arithmetic and sampled independent SVD ridge pilot are included. Raw/derived integrity includes roles, support/k, status, convergence, conditions/codes, scales/seeds/provenance and absent truth placeholders. F2 derived k_path_max is intentionally NA in the saved schema; populated values are checked.

## Size flags

Independently classified 46800 original+derived rule rows. Verified 21600 supplied derived k_gt_K flags; 0 flag/support defects. Original fit rows do not store k_gt_K, so their flags are recomputed from authenticated supports, not claimed to match an absent column. Raw fit-time ebic_at_largest codes remain checked under the unchanged fit specification; the R1 size flag is kept separately. See all_rule_size_flags.csv and size_flags_by_rule_p.csv.


## Check4 measured results

Every method covers24 cases (12/p; exactly2/scenario/p), with the same seed20261019 sample used in the authenticated manifest. F1–F3 independently solve all six raw/derived target problems from zero:144 comparisons each, all supports match. Their24 original cv_min coefficient/objective comparisons pass; the other120 comparisons/method are support-only. MCP/SCAD refine24 raw ebic1 points each, starting at the saved primary vector.

| Method | Job | Cases | Rule comparisons | Fail rows | Max beta difference | Max prediction difference | Max absolute objective gap | Max independent KKT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F1 | 2352136 | 24 | 144 | 0 | 3.2796205026329114e-07 | 6.341936708923234e-07 | 2.653433028854124e-14 | 1.1740707364649161e-09 |
| F2 | 2352137 | 24 | 144 | 0 | 2.9264056275457584e-07 | 6.766743353453603e-07 | 2.5979218776228663e-14 | 1.0053520793640303e-09 |
| F3 | 2352138 | 24 | 144 | 0 | 8.286334276588758e-07 | 1.0293814637771888e-06 | 8.119893646352239e-14 | 9.98160526455294e-10 |
| F4 | 2352139 | 24 | 24 | 0 | 7.759093748217066e-07 | 1.5671458916092997e-06 | 1.6368850719317152e-14 | 9.273559890485283e-09 |
| F4_SCAD | 2352140 | 24 | 24 | 0 | 5.454730786988438e-07 | 2.1505019532434963e-06 | 1.3860440573054689e-13 | 7.492157247657171e-09 |

Differences refer to original primary points; SCAD beta differences use its internal coefficient scale. All solver certifications passed. MCP/SCAD objective gaps are local refinement diagnostics, without a global pass/fail optimality certificate.

### F5 independent search

Job2352135 independently constructs forward OLS supports at sizes0..100 and performs up to three exhaustive single-swap sweeps at the union of selected supports. Every saved/forward/swapped RSS is evaluated with independent SVD least squares (`gelsd`, rank cutoff1e-12). All2,424 witness triples are full rank/evaluable. Beaten means RSS decreases by more than1e-7*max(1,saved_RSS). All24 cases have at least one beaten point.

| Selected rule | Comparisons | Beaten |
|---|---:|---:|
| bic | 24 | 24 |
| bic_K37 | 24 | 22 |
| ebic05 | 24 | 20 |
| ebic05_K37 | 24 | 13 |
| ebic1 | 24 | 10 |
| ebic1_K37 | 24 | 9 |
| sic_smax | 24 | 11 |

Maximum relative improvement witness: `p1000_S4_r092_c050`, k=100; saved RSS=5.176935725518039, forward RSS=2.6621797744147915, swap RSS=4.303989826308687, selected rules=`bic`.

Maximum absolute improvement=24.336820160630083: `p0500_S6_r051_c050`, k=14. Full support keys, SVD ranks, RSS and accepted swaps are in the authenticated witness CSV; every selected-rule comparison is in refits.csv. Cell counts are tabulated in F5_check4_by_cell.csv.

The F5 summary has `check4_status=FAIL`, `search_beaten=1477`, `defect_count=0`, and exit0. The zero defect_count records absence of exceptions/inconsistencies; search limitations are recorded separately. Process success is not scientific success. These witnesses do not establish what selection a globally optimized candidate path would make.

## Job accounting and evidence paths

Remote base: `/projects/ml75/fb31/BVS/bench20261019/verify/G5_freq/c050`. Local collected evidence: `collected_check4_20261022/`. Each method’s `evidence/<method>_refit_<job>/` contains job.log, exit_status.txt, self-check logs and audit/{summary.json,environment.json,refits.csv,search_witnesses_svd.csv,defects.csv}. Setup is evidence/environment_2352134/.

| Job | Role | State / exit | Elapsed | Allocated CPUs | Requested memory | Batch MaxRSS | Node |
|---|---|---|---|---:|---|---|---|
| 2352134 | environment | COMPLETED / 0:0 | 00:00:34 | 2 | 3G | 540064K | bb2u13c1 |
| 2352135 | F5 | COMPLETED / 0:0 | 00:00:15 | 4 | 10G | 463384K | bb2u13c1 |
| 2352136 | F1 | COMPLETED / 0:0 | 00:00:06 | 4 | 10G | 439916K | bb2u18c1 |
| 2352137 | F2 | COMPLETED / 0:0 | 00:00:07 | 4 | 10G | 468796K | bb2u19c1 |
| 2352138 | F3 | COMPLETED / 0:0 | 00:00:07 | 4 | 10G | 379800K | bb2u22c1 |
| 2352139 | F4 | COMPLETED / 0:0 | 00:00:05 | 4 | 10G | 674904K | bb2u22c1 |
| 2352140 | F4_SCAD | COMPLETED / 0:0 | 00:00:06 | 4 | 10G | 650984K | bb2u22c1 |

Scheduler dates in sacct.txt are cluster local time; job UTC timestamps in logs/environment identify2026-10-22T14:00–14:01Z. Accounting was collected once at14:07:47Z after the ten-minute check interval; download/verification followed serially. Setup requested1 CPU, but accounting reports2 allocated. Refits used4 CPUs/10G, F5 limit6h and others8h; no larger job was requested.

## Authentication and reproducibility

Downloaded archive SHA256=`888dfafd19832a3979abd4885f63151e576421f4a9de846900328e3b01db14a1`; all95 collected files were independently rehashed. Job IDs, exact sample coverage, rule registries, CSV row counts/maxima, source hashes and manifest bindings were cross-checked against saved outputs. See collected_check4_20261022/{authentication.json,inspection.json}, collection_20261022/files.sha256 and collection_20261022/sacct.txt.

Sample manifest SHA256=`a5a9276198520415d932997399c9c26e553226c05b14de1494d43a3a026e5188`. Input manifest SHA256=`1a42b91913091c0da0fe95841340aea19667f4a4be05599a77405cf895cb682c`. Executed refit_only.py SHA256=`7d169e16edf67b48a6739a517c39576c6a0755f390ea6d7bad569009b986fe8e`; immutable source snapshot is snapshots/20261022_c050_refit/. The lead’s receipt is submissions/20261022_c050_refit.txt. Original sample RDS/CSV files were authenticated against sidecars and audited source bindings before staging; each job rechecked those hashes and c050 y hashes.

NOTS Python3.11.5/GCC13.2.0, numpy2.4.6, scipy1.17.1, rdata1.1.0; complete pip_freeze saved for setup. Every refit job ran the saved synthetic checks (10 OLS/search assertions,13 convex/MCP/SCAD assertions, plus c050 restriction boundaries). Four workers and one BLAS/OpenMP thread each. Local saved-output analyses used Python3.12.7/Anaconda, numpy1.26.4, scipy1.12.0, rdata1.1.0, pandas2.2.2, xarray2023.6.0. Commands, environments, source snapshots, starts/finishes and exits are preserved.

Local checks1/2/3/5 used the explicit lead exception for analysis of saved relocated outputs. Re-fits ran only in lead-submitted NOTS jobs. Nothing under C:/Users/felip/Documents/NOTS_BVS/ was written; no truth file was read and no production result/source was changed. Derived metadata archive SHA256=`dcc51a9dce8f18b8ca2b9fc7555c93cfc097dccb0a7b3fe3ba05337e01030220`.

Successful local audit paths: evidence/local_full_round2/{F1,F2,F5}/audit/ and evidence/local_full_round2_corrected/{F3,F4,F4_SCAD}/audit/. Their summary.json, cell summaries, candidate/rule/derived comparisons and artifact tables support checks1/2/3/5. The explicit audit_overrides.json and original failed evidence are retained. Executed local source snapshots are source_snapshots/{local_full_round2,local_full_round2_corrected}/, with driver launch_record.json in the corresponding evidence root.

Original local summaries remain unchanged as historical analyses; their NOT_RUN_LEAD_SUBMISSION fields and zero refit accumulators are superseded only by combined_final_summary.json and this report. Corrected local audit overrides remain explicit. FAILED_ATTEMPTS.md preserves resolved verifier failures; parent LEDGER_ENTRY.md records authored source as unreviewed.
