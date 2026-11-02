# Scoring tests: report

Run: 2026-10-30 07:44 UTC. R 4.4.1. Enumerator library (lowp_enum.R): loaded, C++ lowp_td exercised.
Fixture: p in {8, 10}, S1-S2, 3 replicates, c100/c050 = 24 cases, 12 exact posteriors by brute force (2^p models), 30 mock SMC records (24 main + 6 repeat seeds), 68 benchmark rule rows. Assertions: 195, passed 195, failed 0, skipped 0.

| Group | Assertions | PASS | FAIL | SKIP | Verdict |
|---|---|---|---|---|---|
| G1 extract_smc | 11 | 11 | 0 | 0 | PASS |
| G2 log Z | 5 | 5 | 0 | 0 | PASS |
| G3 PIP | 3 | 3 | 0 | 0 | PASS |
| G4 HPM | 5 | 5 | 0 | 0 | PASS |
| G5 stability | 4 | 4 | 0 | 0 | PASS |
| G6 flag x error | 2 | 2 | 0 | 0 | PASS |
| G7 selection | 6 | 6 | 0 | 0 | PASS |
| G7b H4 recovery | 3 | 3 | 0 | 0 | PASS |
| G8 headline H1-H3 | 7 | 7 | 0 | 0 | PASS |
| G9 theory | 10 | 10 | 0 | 0 | PASS |
| G10 TD audit | 26 | 26 | 0 | 0 | PASS |
| G11 run_theory_H | 6 | 6 | 0 | 0 | PASS |
| G12 CLI | 4 | 4 | 0 | 0 | PASS |
| G13 missing main fit (finding 1) | 5 | 5 | 0 | 0 | PASS |
| G14 roster (finding 5) | 6 | 6 | 0 | 0 | PASS |
| G15 empty supports (finding 2) | 5 | 5 | 0 | 0 | PASS |
| G16 dropped truth (finding 3) | 5 | 5 | 0 | 0 | PASS |
| G17 evidence validity (finding 4) | 4 | 4 | 0 | 0 | PASS |
| G18 duplicates (finding 6) | 5 | 5 | 0 | 0 | PASS |
| G19 exact PIP map (finding 7) | 3 | 3 | 0 | 0 | PASS |
| G20 extraction safety (finding 8) | 5 | 5 | 0 | 0 | PASS |
| G21 passing-only recovery (finding 9) | 2 | 2 | 0 | 0 | PASS |
| G22 EXACT readiness (finding 10) | 6 | 6 | 0 | 0 | PASS |
| G23 repeat seeds (finding 11) | 3 | 3 | 0 | 0 | PASS |
| G24 TD above K (finding 12) | 2 | 2 | 0 | 0 | PASS |
| G25 review notes | 4 | 4 | 0 | 0 | PASS |
| G26 registry derived from bench_lowp (N1) | 7 | 7 | 0 | 0 | PASS |
| G27 exact-branch evidence (N2) | 4 | 4 | 0 | 0 | PASS |
| G28 PIP index validation (N3) | 9 | 9 | 0 | 0 | PASS |
| G29 duplicate identity (finding 6 residual) | 5 | 5 | 0 | 0 | PASS |
| G30 EXACT completeness (finding 10 residual) | 13 | 13 | 0 | 0 | PASS |
| G31 unknown seeds (finding 11 residual) | 2 | 2 | 0 | 0 | PASS |
| G32 EXACT consistency (RC3) | 6 | 6 | 0 | 0 | PASS |
| G33 EXACT PIP feasibility (FC3 N2) | 2 | 2 | 0 | 0 | PASS |

## Every assertion

| Group | Assertion | Result | Note |
|---|---|---|---|
| G1 extract_smc | ids and ok | PASS |  |
| G1 extract_smc | log_Z, island log Z, lower95 | PASS |  |
| G1 extract_smc | RB and plain PIP full length | PASS |  |
| G1 extract_smc | flags | PASS |  |
| G1 extract_smc | min ESS uses final rows only (diag row ess = 1 ignored) | PASS |  |
| G1 extract_smc | score counts and tier | PASS |  |
| G1 extract_smc | registry log mass and distinct count | PASS |  |
| G1 extract_smc | failed fit: not ok, estimates NA/NULL, HPM audit kept | PASS |  |
| G1 extract_smc | absent v2.2 fields give NA / NULL (log_mass_scored, scored_set, plain PIP) | PASS |  |
| G1 extract_smc | retained-only PIP expanded with zeros for dropped columns | PASS |  |
| G1 extract_smc | FIELD_MAP covers every name used and statuses are code/provisional | PASS |  |
| G2 log Z | every fit (24 main + 6 repeat rows): log Z exact, e, relative error, island errors, lb coverage, SE, within 2 SE | PASS | 0 mismatching fits |
| G2 log Z | hand value, case A: e = log mean exp(0, .2, .4, .6) | PASS |  |
| G2 log Z | hand value, case B: e ~ 4 so the 0.05 lower bound is violated | PASS |  |
| G2 log Z | failed fit (case D) has NA metrics but a row | PASS |  |
| G2 log Z | coverage of scored set = injected fraction (0.999; 0.5 for the Fc case) | PASS |  |
| G3 PIP | RB and plain: max, mean, true/null split, per island, island mean (all fits) | PASS | 0 mismatches |
| G3 PIP | hand values, case A (p=8, S0={2,6}; +/-0.05 on vars 1,2 RB; 0.10 on var 1 plain) | PASS |  |
| G3 PIP | MPM = exact MPM (RB, plain), exact MPM = truth, SMC MPM = truth | PASS |  |
| G4 HPM | SMC HPM = exact HPM, exact HPM = truth, SMC HPM = truth, score gap, truth mass, truth-vs-HPM scores, miss class | PASS | 0 mismatches |
| G4 HPM | the injected wrong HPMs are detected (B second-best, C below truth, rep2 of A) | PASS |  |
| G4 HPM | both miss classes occur in the fixture | PASS |  |
| G4 HPM | native hpm_F shift 0.001 injected in case E is measured | PASS |  |
| G4 HPM | exact F from the stored top list equals the scorer F for the true model (consistency) | PASS |  |
| G5 stability | only the three cases with repeat seeds have a stability row, 3 attempted / 3 completed fits each | PASS |  |
| G5 stability | sd of log Z-hat across seeds | PASS |  |
| G5 stability | HPM agreement = 1/3 for A, B, C (main and repeat 1 share an HPM, repeat 2 differs; 2 distinct HPMs) | PASS |  |
| G5 stability | max PIP sd = 0.5 max/delta/ (PIP scaled by 1, 1.5, 2 across seeds) | PASS |  |
| G6 flag x error | 2x2 counts, sensitivity, specificity for all 36 flag x event pairs | PASS | 0 mismatches |
| G6 flag x error | the table has 9 flags x 4 events | PASS |  |
| G7 selection | row count: 24 cases x (LASSO 2 rules + SUSIE 1 + SMC 2 + EXACT 2) = 168 | PASS |  |
| G7 selection | LASSO/SUSIE: TP, FP, FN, exact, error type per row (exact, extra_only, missed_only, mixed, failed/timeout/not_run) | PASS | 0 cases mismatch |
| G7 selection | timeout and not_run rows are present as failed non-recovery (denominator) | PASS |  |
| G7 selection | SMC hpm / pip05 rows: exact recovery matches the injected supports; failed fit (case D) is a failed row | PASS |  |
| G7 selection | EXACT reference rows: exact HPM / exact MPM recover the truth iff they equal S0 | PASS |  |
| G7 selection | repeat-seed fits add no selection rows (only the main fit is scored for selection) | PASS |  |
| G7b H4 recovery | per-scenario and pooled recovery counts for LASSO cvmin and SUSIE (p x c) | PASS |  |
| G7b H4 recovery | H4 contains primary rules, SMC pip05 and the EXACT references; S0-role rules of benchmarks (ebic1) excluded from H4 only via role | PASS |  |
| G7b H4 recovery | H4 n_failed counts failed/timeout/not_run | PASS |  |
| G8 headline H1-H3 | H1 (n, failed, bias, RMSE, median/e/, 90th pct /e/, lower-bound coverage) for 12 cells | PASS |  |
| G8 headline H1-H3 | H2 (% SMC HPM = exact, % exact = truth, % SMC = truth; failed counted as not equal) for 12 cells | PASS |  |
| G8 headline H1-H3 | H3 (RB and plain mean/p90 of max error, true/null mean error, % MPM = exact MPM) for 12 cells | PASS |  |
| G8 headline H1-H3 | failed fit (D, p=10 S2 c100) stays in the denominator | PASS |  |
| G8 headline H1-H3 | HEADLINE.md has exactly the four questions H1-H4 and nothing else at level 2 | PASS |  |
| G8 headline H1-H3 | HEADLINE.md H4 shows LASSO cvmin pooled count for p=8, c100 | PASS |  |
| G8 headline H1-H3 | all output files written | PASS |  |
| G9 theory | one case_theory row per case | PASS |  |
| G9 theory | pi0(S0) and pi0(R_d), d = 0, 1, 2: DP equals brute-force summation of v3_start_logmass (24 cases); pi0(S0) via tables; monotone in d | PASS |  |
| G9 theory | blocks_match: TRUE except case E (blocks altered in the record) | PASS |  |
| G9 theory | scored-set coverage in case_theory equals the injected fraction | PASS |  |
| G9 theory | truth trace from the scored set: scored iff injected or the HPM equals the truth; first phase 'pilot' | PASS |  |
| G9 theory | truth vs HPM score and miss class in case_theory | PASS |  |
| G9 theory | p = 20 (n = 200, B = 4, 6 blocks): DP equals brute-force sum over R_d for d = 0, 1, 2 | PASS | -3.2112975 -1.1251570 -0.3966282 |
| G9 theory | p = 20: pi0(S0) from v3_start_logmass equals the table product | PASS |  |
| G9 theory | p = 20: log varpi(k) read from the scorer equals ctx$log_w - ctx$log_W_K | PASS |  |
| G9 theory | true variable dropped by preprocessing (duplicate column): S0_retained FALSE and pi0 = 0 (or the duplicate handled) | PASS |  |
| G10 TD audit | p0008_S1_r001_c100 d=1: R stand-in equals independent reference (literal and toward: centres, violations, ties, min margins; truth-in-swap diagnosis) | PASS |  |
| G10 TD audit | p0008_S1_r001_c100 d=1: lowp_td (C++) literal and toward equal the independent reference | PASS | engine: enum |
| G10 TD audit | p0008_S1_r001_c100 d=2: R stand-in equals independent reference (literal and toward: centres, violations, ties, min margins; truth-in-swap diagnosis) | PASS |  |
| G10 TD audit | p0008_S1_r001_c100 d=2: lowp_td (C++) literal and toward equal the independent reference | PASS | engine: enum |
| G10 TD audit | p0008_S2_r002_c050 d=1: R stand-in equals independent reference (literal and toward: centres, violations, ties, min margins; truth-in-swap diagnosis) | PASS |  |
| G10 TD audit | p0008_S2_r002_c050 d=1: lowp_td (C++) literal and toward equal the independent reference | PASS | engine: enum |
| G10 TD audit | p0008_S2_r002_c050 d=2: R stand-in equals independent reference (literal and toward: centres, violations, ties, min margins; truth-in-swap diagnosis) | PASS |  |
| G10 TD audit | p0008_S2_r002_c050 d=2: lowp_td (C++) literal and toward equal the independent reference | PASS | engine: enum |
| G10 TD audit | p0010_S1_r003_c100 d=1: R stand-in equals independent reference (literal and toward: centres, violations, ties, min margins; truth-in-swap diagnosis) | PASS |  |
| G10 TD audit | p0010_S1_r003_c100 d=1: lowp_td (C++) literal and toward equal the independent reference | PASS | engine: enum |
| G10 TD audit | p0010_S1_r003_c100 d=2: R stand-in equals independent reference (literal and toward: centres, violations, ties, min margins; truth-in-swap diagnosis) | PASS |  |
| G10 TD audit | p0010_S1_r003_c100 d=2: lowp_td (C++) literal and toward equal the independent reference | PASS | engine: enum |
| G10 TD audit | p0010_S2_r001_c050 d=1: R stand-in equals independent reference (literal and toward: centres, violations, ties, min margins; truth-in-swap diagnosis) | PASS |  |
| G10 TD audit | p0010_S2_r001_c050 d=1: lowp_td (C++) literal and toward equal the independent reference | PASS | engine: enum |
| G10 TD audit | p0010_S2_r001_c050 d=2: R stand-in equals independent reference (literal and toward: centres, violations, ties, min margins; truth-in-swap diagnosis) | PASS |  |
| G10 TD audit | p0010_S2_r001_c050 d=2: lowp_td (C++) literal and toward equal the independent reference | PASS | engine: enum |
| G10 TD audit | K < p (n = 10, p = 8, K = 5), d = 2: stand-in equals reference (swaps feasible at /S/ = K) | PASS |  |
| G10 TD audit | K < p, d = 2: lowp_td (C++) equals reference (swaps feasible at /S/ = K) | PASS |  |
| G10 TD audit | K < p (n = 10, p = 8, K = 5), d = 3: stand-in equals reference (swaps feasible at /S/ = K) | PASS |  |
| G10 TD audit | K < p, d = 3: lowp_td (C++) equals reference (swaps feasible at /S/ = K) | PASS |  |
| G10 TD audit | TD restricted null pool: d = 1 with a pool of 3 nulls equals the reference with that pool | PASS |  |
| G10 TD audit | TD margin parameter: a margin above every observed margin makes every centre violate (both variants) | PASS |  |
| G10 TD audit | TD max_scores stops the stand-in with complete = FALSE | PASS |  |
| G10 TD audit | literal fails when a truth-in swap exists and the diagnosis counts it (p0008_S1_r001_c100, d = 1) | PASS |  |
| G10 TD audit | case_theory TD columns (td{d}_literal_*, td{d}_toward_*, truth-in-swap counts) agree with the reference for d = 1, 2 | PASS |  |
| G10 TD audit | scorer F equals lowp_score_models F (same arithmetic) | PASS | max abs diff 0 |
| G11 run_theory_H | p = 60 record: pi0(S0), pi0(R_0), pi0(R_1) equal brute force; coverage NA (no exact Z) | PASS |  |
| G11 run_theory_H | blocks of the record equal the recomputed blocks; HPM = truth gives a hit | PASS |  |
| G11 run_theory_H | TD d = 0 (all nulls) and opt-in restricted d = 1 (union of core neighbour lists, columns td1r_*) are labelled | PASS |  |
| G11 run_theory_H | restricted d = 1 TD equals the R stand-in with the same pool | PASS |  |
| G11 run_theory_H | default p >> n run: TD d = 0 only (no d = 1 columns, no restricted columns) | PASS |  |
| G11 run_theory_H | CLI Rscript run_theory_H.R writes case_theory row | PASS |  |
| G12 CLI | Rscript run_scoring.R runs and writes the headline files | PASS |  |
| G12 CLI | CLI output equals the in-process output (accuracy table) | PASS |  |
| G12 CLI | HEADLINE.md is identical between runs | PASS |  |
| G12 CLI | CSV round trip keeps NA vs empty support in selection table (failed rows have NA k) | PASS |  |
| G13 missing main fit (finding 1) | absent main (repeats still present): n_cases stays 3, n_smc_missing = 1, n_evidence = 2 | PASS |  |
| G13 missing main fit (finding 1) | H2 divides by 3 expected cases (not 2 observed): pct = hits / 3 | PASS |  |
| G13 missing main fit (finding 1) | H1, H2, H3 and H4 agree on the cell sizes | PASS |  |
| G13 missing main fit (finding 1) | the repeat-only case keeps its repeat rows in case_smc_accuracy but no main row | PASS |  |
| G13 missing main fit (finding 1) | no SMC output at all: H1-H3 and HEADLINE still produced, every case counted missing | PASS |  |
| G14 roster (finding 5) | a manifest dataset with no result at all is counted (4 cases: 1 missing SMC); the changed manifest SHA-256 invalidates the sealed EXACT records bound to the old manifest (all 4 count as no exact, reason logged) | PASS |  |
| G14 roster (finding 5) | a registry method with no result file anywhere reports 0/n per scenario and 0/n pooled | PASS |  |
| G14 roster (finding 5) | a rostered dataset without a truth file is a scoring-completeness error (not a smaller denominator) | PASS |  |
| G14 roster (finding 5) | no manifest: error in production mode; partial mode lists inputs/ and labels HEADLINE as partial | PASS |  |
| G14 roster (finding 5) | production mode checks the planned grid (6 scenarios x 100 replicates) | PASS |  |
| G14 roster (finding 5) | an unknown id in the case subset is an error | PASS |  |
| G15 empty supports (finding 2) | parse_support: integer(0) and numeric(0) stay empty; '' is empty; NA / NULL / character(0) are unavailable | PASS |  |
| G15 empty supports (finding 2) | exact_scale keeps the integer(0) HPM and MPM from the real API (not NA) | PASS |  |
| G15 empty supports (finding 2) | empty truth, empty exact HPM / MPM: two successful empty selections with exact recovery (k = 0), support text '' | PASS |  |
| G15 empty supports (finding 2) | non-empty truth with an empty exact MPM: successful selection, missed_only (not failed) | PASS |  |
| G15 empty supports (finding 2) | CSV round trip keeps '' distinct from NA | PASS |  |
| G16 dropped truth (finding 3) | a constant true column is dropped by preprocessing (kept = 1:8 without 6) | PASS |  |
| G16 dropped truth (finding 3) | no error with a completed fit; S0_retained FALSE, n_true_dropped 1, status labelled, F_truth NA, miss_class NA | PASS |  |
| G16 dropped truth (finding 3) | pi0(S0) = 0 (infeasible truth) but pi0(R_d) is the mass of the FEASIBLE retained region, not zero | PASS |  |
| G16 dropped truth (finding 3) | TD is undefined for a dropped truth and labelled so (no TD columns, no silent zeros) | PASS |  |
| G16 dropped truth (finding 3) | blocks are matched through original indices on the dropped-column design | PASS |  |
| G17 evidence validity (finding 4) | completed record with log_Z = NA: ok, HPM usable, evidence unavailable | PASS |  |
| G17 evidence validity (finding 4) | two-island record: no SE, no island statistic (four valid islands required) | PASS |  |
| G17 evidence validity (finding 4) | H1 reports n_evidence = 1 and every statistic is finite (consistent NA handling); coverage defined on those fits | PASS |  |
| G17 evidence validity (finding 4) | the unavailable evidence does not invalidate the HPM: H2 unchanged | PASS |  |
| G18 duplicates (finding 6) | identical copies in two roots are merged: same accuracy rows, same H2, duplicates logged | PASS |  |
| G18 duplicates (finding 6) | conflicting copies are refused | PASS |  |
| G18 duplicates (finding 6) | explicit precedence 'first_root' keeps the first root and records the conflict | PASS |  |
| G18 duplicates (finding 6) | conflicting benchmark rows are refused (no silent last-wins) | PASS |  |
| G18 duplicates (finding 6) | repeat fits that share a method seed are refused | PASS |  |
| G19 exact PIP map (finding 7) | retained PIPs named by original index are expanded: (.8, 0, 0, .2), kept = {1, 4} | PASS |  |
| G19 exact PIP map (finding 7) | SMC and exact PIP errors are 0 (not NA) on the dropped-column design; kept maps agree | PASS |  |
| G19 exact PIP map (finding 7) | exact PIP names that disagree with the retained-column map are rejected | PASS |  |
| G20 extraction safety (finding 8) | a named partial PIP that does not cover every retained variable is unavailable (no invented zeros) | PASS |  |
| G20 extraction safety (finding 8) | a stage table with no final rows gives min_ess = NA (no fallback to calibration) | PASS |  |
| G20 extraction safety (finding 8) | all-NA ESS and score counts stay NA (not Inf / 0) | PASS |  |
| G20 extraction safety (finding 8) | unavailable exact HPM / MPM: exact-vs-truth equalities are NA (not FALSE), like the SMC-vs-exact ones | PASS |  |
| G20 extraction safety (finding 8) | out-of-range PIPs are rejected | PASS |  |
| G21 passing-only recovery (finding 9) | a flagged exact success is in the all-saved count but not the passing-only count; same fixed denominator; NA flag counts as not flagged | PASS |  |
| G21 passing-only recovery (finding 9) | HEADLINE H4 shows both versions in each cell | PASS |  |
| G22 EXACT readiness (finding 10) | complete, hashed, status exact: ready | PASS |  |
| G22 EXACT readiness (finding 10) | no .done marker: refused (no_done_marker) | PASS |  |
| G22 EXACT readiness (finding 10) | sidecar hash differs from the RDS: refused | PASS |  |
| G22 EXACT readiness (finding 10) | status partial / incomplete subset run: refused even with valid hashes (validator reasons logged) | PASS |  |
| G22 EXACT readiness (finding 10) | missing sha256 sidecar: refused; envelope of another dataset: refused | PASS |  |
| G22 EXACT readiness (finding 10) | end to end: an uncommitted EXACT unit is not used (no_done_marker in exact_diagnostics, both scales count as no exact reference, EXACT rows not_run) | PASS |  |
| G23 repeat seeds (finding 11) | one completed main + one failed repeat: no SD / agreement is reported (>= 2 eligible seeds required), counts shown | PASS |  |
| G23 repeat seeds (finding 11) | ragged fields: each statistic reports its own seed count (3 evidence, 2 PIP vectors) | PASS |  |
| G23 repeat seeds (finding 11) | two completed seeds baseline: SD of log Z, agreement 1, PIP SD | PASS |  |
| G24 TD above K (finding 12) | p = 4, n = 4 (K = 2), S0 = {1, 2}, d = 1: no error, 3-variable centres skipped and counted | PASS |  |
| G24 TD above K (finding 12) | the C++ audit and the stand-in agree on the feasible centre set | PASS |  |
| G25 review notes | PPV = P(event / flag) is asserted too | PASS |  |
| G25 review notes | miss classes: hit, search_miss (F(S0) > F(HPM)), posterior_miss (F(S0) <= F(HPM), including an exact tie) | PASS |  |
| G25 review notes | a tied wrong HPM: support unequal to the truth, truth-minus-HPM score exactly 0 | PASS |  |
| G25 review notes | master tie order (lexicographic on original indices): {1,4} precedes {2,3} (fixture key) | PASS |  |
| G26 registry derived from bench_lowp (N1) | 42 rows: SMCBVS 2 + EXACT 2 + 38 benchmark rules; in_h4 = the 8 primaries + SMC hpm/pip05 + EXACT hpm/mpm | PASS |  |
| G26 registry derived from bench_lowp (N1) | primary rules: F1-F3 cv_min, F4/F5 ebic1_K37, A1 pip05, A2 ssl_final, A3 ci95 | PASS |  |
| G26 registry derived from bench_lowp (N1) | LA-4 roles: cap rows secondary (F4/F5 ebic1, ebic05, bic; F1-F3 ebic1, ebic05); K37 companions and ebic1_lam005 / sic_smax S0; cslead, bfdr10, km2, cv_1se S0 | PASS |  |
| G26 registry derived from bench_lowp (N1) | derived rule set equals the 38 (method, rule, role) rows of the real benchmark smoke output (p = 20 and 30, both scales) | PASS |  |
| G26 registry derived from bench_lowp (N1) | H4 reports ebic1_K37 as the F4/F5 primary (F4 1/1, F5 0/1) and never the cap rows; missing F4/F5 K37 rows would be not_run | PASS |  |
| G26 registry derived from bench_lowp (N1) | an observed role that disagrees with the registry is an error | PASS |  |
| G26 registry derived from bench_lowp (N1) | default run uses the derived registry (registry_used.csv = build_registry()); absent benchmark methods are 0/n in H4; the SMC and EXACT rows are scored | PASS |  |
| G27 exact-branch evidence (N2) | exact branch: ok, pooled evidence kept (finite log Z), no islands, no plain PIPs | PASS |  |
| G27 exact-branch evidence (N2) | error, relative error and lower-bound comparison are retained (e = 0, covered); island errors and SE stay unavailable | PASS |  |
| G27 exact-branch evidence (N2) | a completed (non-exact) record without islands still has no evidence | PASS |  |
| G27 exact-branch evidence (N2) | H1 keeps the exact-branch fit as an evidence contributor (n_evidence 3 of 3 in its cell) | PASS |  |
| G28 PIP index validation (N3) | full vector with names 4,3,2,1 is reordered to the canonical original-index order | PASS |  |
| G28 PIP index validation (N3) | duplicate names, unknown names and out-of-range values are rejected | PASS |  |
| G28 PIP index validation (N3) | confirmed dropped columns must carry 0: a nonzero entry for a column outside `kept` is rejected, zero accepted | PASS |  |
| G28 PIP index validation (N3) | end to end: a permuted adapter vector gives the same canonical PIPs and the same error against the exact reference | PASS |  |
| G28 PIP index validation (N3) | exact PIP 1.8 rejected | PASS |  |
| G28 PIP index validation (N3) | exact PIP NaN rejected | PASS |  |
| G28 PIP index validation (N3) | exact PIP Inf rejected | PASS |  |
| G28 PIP index validation (N3) | exact PIP -0.2 rejected | PASS |  |
| G28 PIP index validation (N3) | exact log Z must be finite | PASS |  |
| G29 duplicate identity (finding 6 residual) | copies that differ only in diag_flag are a conflict (not 'identical copies merged') | PASS |  |
| G29 duplicate identity (finding 6 residual) | copies that differ only in diag_codes are a conflict | PASS |  |
| G29 duplicate identity (finding 6 residual) | bit-identical benchmark copies are merged | PASS |  |
| G29 duplicate identity (finding 6 residual) | explicit first_root precedence resolves the flag conflict and records it in duplicates.csv | PASS |  |
| G29 duplicate identity (finding 6 residual) | case_base() asserts a unique main-fit row per case | PASS |  |
| G30 EXACT completeness (finding 10 residual) | extra$complete NULL with top-level FALSE: refused | PASS |  |
| G30 EXACT completeness (finding 10 residual) | completeness unspecified at both levels: refused | PASS |  |
| G30 EXACT completeness (finding 10 residual) | top-level TRUE but extra missing: refused; extra TRUE but top-level missing: refused | PASS |  |
| G30 EXACT completeness (finding 10 residual) | a scale marked partial / restricted_to_scored_models under an exact envelope: refused (status and scope reasons) | PASS |  |
| G30 EXACT completeness (finding 10 residual) | models_scored differing from models_expected, or extra$complete FALSE: refused | PASS |  |
| G30 EXACT completeness (finding 10 residual) | FC4: both counts missing: refused (missing top-level fields) | PASS |  |
| G30 EXACT completeness (finding 10 residual) | FC4: 0/0 counts: refused (expected count not the derived sum, not positive) | PASS |  |
| G30 EXACT completeness (finding 10 residual) | FC4: absent requested scale c050: refused | PASS |  |
| G30 EXACT completeness (finding 10 residual) | FC4: extra$models_expected missing, wrong K, truncated top list, unnormalised size_logmass, wrong input_mode: each refused | PASS |  |
| G30 EXACT completeness (finding 10 residual) | input binding: the matching X / input file hash / manifest hash pass | PASS |  |
| G30 EXACT completeness (finding 10 residual) | input binding: another input matrix (retained columns differ), a wrong input hash or a wrong manifest hash is refused | PASS |  |
| G30 EXACT completeness (finding 10 residual) | a requested scale beyond those in the record (c075) is refused when asked for | PASS |  |
| G30 EXACT completeness (finding 10 residual) | the untouched unit is still ready | PASS |  |
| G31 unknown seeds (finding 11 residual) | two completed records with NA method_seed: excluded (n_completed 0, n_unknown_seed 2), no SD or agreement | PASS |  |
| G31 unknown seeds (finding 11 residual) | one unknown among three: the two known distinct seeds are used | PASS |  |
| G32 EXACT consistency (RC3) | reversed_size_logjoint: refused by the shared validator (reason logged) | PASS | scale c100: size_logjoint[k] != size_logmass[k] + log_Z (max abs error 48.5) |
| G32 EXACT consistency (RC3) | reversed_size_logjoint: end to end, the record never reaches the tables (no exact reference for p0008_S1_r001; its cases count as no_exact and give no e, EXACT rows not_run) | PASS |  |
| G32 EXACT consistency (RC3) | hpm_vs_top: refused by the shared validator (reason logged) | PASS | scale c100: hpm differs from the support of the best entry of top / scale c100: hpm_size differs from top$size[1] / scale c100: hpm differs from top$mask[1] |
| G32 EXACT consistency (RC3) | hpm_vs_top: end to end, the record never reaches the tables (no exact reference for p0008_S1_r001; its cases count as no_exact and give no e, EXACT rows not_run) | PASS |  |
| G32 EXACT consistency (RC3) | logZ_below_hpm_F: refused by the shared validator (reason logged) | PASS | scale c100: size_logjoint log-sum-exp differs from log_Z / scale c100: size_logjoint[k] != size_logmass[k] + log_Z (max abs error 10.4) / scale c100: log_Z (-96.014189) is below the mass of one contained model, hpm_F (-86.014189) / scale c100: log_Z is below the total mass of the listed top models / scale c100: PIP_j below the posterior share of the listed top models containing j (j = 1,2,3,4,5,6,7,8) |
| G32 EXACT consistency (RC3) | logZ_below_hpm_F: end to end, the record never reaches the tables (no exact reference for p0008_S1_r001; its cases count as no_exact and give no e, EXACT rows not_run) | PASS |  |
| G33 EXACT PIP feasibility (FC3 N2) | all PIPs 1 and MPM = all variables (impossible for the stored posterior): refused by the shared validator, reason logged | PASS | scale c100: PIP_j above the share of the listed models plus the unlisted mass 1 - sum(listed) = -4.441e-15 (j = 1,3,4,5,7,8) / scale c100: sum(PIP) = 8 != sum_k k exp(size_logmass[k]) = 2.3885434 |
| G33 EXACT PIP feasibility (FC3 N2) | end to end: the record never reaches the tables (no exact reference, no e for the dataset, EXACT rows not_run, cell n_evidence 2 of 3) | PASS |  |
