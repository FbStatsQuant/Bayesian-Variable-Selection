# THEOREM_MAP.md — ranks, dependencies and recommended proof order

Every item is a conjecture about METHODOLOGY_v3.0 (SHA-256 93043758…8019c). Files are in `theorems\`; each must be given to proof.md together with `theorems\00_COMMON.md`, `THEORY_BRIEF.md` and the method file (by path). Ranks are the judge's (PROPOSAL_v3) as ruled in RULINGS.md; "clause ranks" give the within-file ranks where they differ.

## Index

| File | Label (v3 / v1) | Title | Headline rank | Clause ranks |
|---|---|---|---|---|
| T01_A0_contrast_reduction | A0 = T1 | Contrast reduction and mixed-rate transfer | core (lemma) | |
| T02_A1_dimension_supersets | A1 = T2 | Dimension control and exclusion of strict supersets | core (lemma) | |
| T03_A2_selection_consistency | A2 = T3 | Selection, screening, PIPs and the global HPM | core | BM-C constant provisional |
| T04_A3_contraction | A3 = T4 | Contraction without beta-min | core | (i) double-log fallback secondary |
| T05_A4_orthogonal_threshold | A4 = T5-S | Orthogonal threshold and benchmark gap | secondary | |
| T06_A5_identifiability_ties | A5 = T-ID | Identifiability and exact ties | core (proposition) | |
| T07_A6_size_prior_ceiling | A6 = T5-C | Size-only ranking ceiling and Bayes decisions | core (proposition) | |
| T08_A7_oracle_BvM | A7 = T6 | Oracle joint Bernstein–von Mises limit | optional | |
| T09_T7_kernel_validity | T7 | Exact start, invariant kernels, whole-round minorisation | core (proposition) | |
| T10_T11_addition_hazard | T11 | Feasible-addition hazards and ordered paths | core (lemma) | |
| T11_LLED_scoring_ledger | L-LED/T14-D | Unified scoring and discovery ledger | core (lemma) | |
| T12_T8_frozen_run_identities | T8 | Frozen-run evidence and recorded-RB identities | core | |
| T13_T10_restricted_ESS | T10 | Restricted ESS and omitted-mass identity | core (lemma) | |
| T14_LFM_first_moment_evidence | L-FM | First-moment evidence consistency | core (lemma) | (iii) general set conditional |
| T15_LOCC_occupancy | L-OCC | Occupancy from an evidence lower tail | core (lemma) | |
| T16_T9_frozen_limits | T9 | Frozen-particle and independent-island limits | secondary | |
| T17_LRC_reflection_coupling | L-RC | Reflection with output-specific coupling | core (lemma) | |
| T18_BRP_reflected_pair | B-RP | Reflected single-flip pair benchmark | secondary (lemma) | |
| T19_T12_working_set_bounds | T12 | Conservative working-set bounds | optional | new judge conjecture, unvalidated |
| T20_T15_local_search | T15 | Local-search semantics and conditional repair | core | (i)–(ii) core; (iii) ORTH secondary; (iv) COH optional |
| T21_T14H_HPM_composition | T14-H | Composition theorem for the reported HPM | core | route (e) medium confidence |
| T22_T16_start_aggregation | T16 | Aggregate start bounds and conditional concentration | core | (i),(ii),(iv) core; (iii),(v) secondary |
| T23_T18_basin_prefix | T18 | Basin-to-output guarantee with recording-prefix control | core | (i)–(iv) core; (v) instances secondary |
| T24_T18p_terminal_repair | T18′ | Conservative terminal repair, fixed extra budget | secondary | |
| T25_T19_crossing_evidence | T19 | Conditional evidence bounds through a crossing | secondary | (i)–(iii) secondary; (iv) PW2 open/optional |
| T26_T17_no_switch_consistency | T17 | No-switch consistency at the actual budgets | secondary (corollary) | |
| T27_T20C_cancellation_budget | T20-C | Sequential cancellation and the iid-discovery budget | secondary (corollary) | |
| T28_T21E_evidence_loss | T21-E | Evidence loss under avoidance and evidence coupling | core | |
| T29_T21H_HPM_PIP_loss | T21-H | HPM loss needs scoring avoidance; PIP loss needs reward control | secondary | (iv) accessibility sub-conjecture |
| T30_T21X_pilot_discovery | T21-X | Pilot discovery under the terminal-repair hypotheses | optional | lead's ruling 61 |
| T31_T22_certificates | T22 | What the reported checks and certificates establish | core (proposition) | |
| T32_T23C_resource_counts | T23-C | Branch-specific arithmetic and storage counts | core (proposition) | |
| T33_T23N_numerical_margins | T23-N | Numerical margins on a common scored set | secondary (lemma) | |
| T34_T23S_statuses | T23-S | Statuses and allocation-dependent guarantees | core (proposition) | |
| T35_T23R_bisection_obstruction | T23-R | Mass-qualified bisection obstruction; discrepancy range | optional | |
| T36_RT13_pilot_finite_comparison | R-T13 | Pilot limit as a finite-comparison rule | secondary | remark-level |

Counts by headline rank: core 22 (T01, T02, T03, T04, T06, T07, T09, T10, T11, T12, T13, T14, T15, T17, T20, T21, T22, T23, T28, T31, T32, T34); secondary 10 (T05, T16, T18, T24, T25, T26, T27, T29, T33, T36); optional 4 (T08, T19, T30, T35). Total 36.

Remarks without files (recorded in DROPPED.md): R-T20(i) fixed-p start masses (counterfactual component); R-T20(iii) cap crowd-out (open construction).

## Dependency graph (A → B: B uses A)

Authority note: this graph lists logical inputs. The "Used by" lines inside the theorem files also cite interpretive uses (a result that informs the reading of another without being a premise), so they are not mirrored one-to-one by the "Builds on" lines; where the two disagree, this graph governs (operator check of 2026-10-20: all cross-reference tokens valid; 36 non-mirrored "Used by" citations, all interpretive).

- Method identities → T01, T06 (structural identity), T07, T09, T10, T11, T32, T33(i), T34, T35.
- T01 → T02 → T03; T01 + T02 → T04; T01 + T02 → T05; T01 + T03 + T04 → T08; T03 → T06 (strict-mode clause).
- T09 → T10, T12, T13, T17, T18, T19, T23, T25, T28, T29, T36.
- T10 → T11, T17, T21, T22 (deterministic), T24, T27, T28, T29, T30.
- T11 → T20, T21, T24, T27, T28, T29, T30, T31.
- T12 → T14, T15, T16, T17, T19, T25, T28, T31.
- T13 → T18, T25, T28, T31, T35.
- T14 → T15 (lower tail), T25 (first-moment alternative), T26.
- T15 → T23, T24, T26.
- T17 → T18, T19, T25, T28, T29, T31.
- T18 → T23 (pair instance), T25.
- T19 → T25 (alternative comparator bound), T26 (optional alternative).
- T03 → T20, T21, T22 (endpoint), T23, T24, T26, T28 (consequences), T30, T31, T33.
- T20 → T21, T24, T31.
- T22 → T21, T26, T27.
- T23 → T24, T26, T31.
- T24 → T21 (route e), T29 (iv), T30.
- T25 → T15/T23 (per-island lower tails), T31.
- T26 → T31. T27 → T31. T28 → T30, T31. T29 → T31. T30 → none. T31 → none.
- T32 → T34; T33 → T34; T36 → T34; T34 → T21, T26.

Acyclicity: T25 does not derive particle stability from a later occupancy consequence; T15 precedes its applications; T23 assumes its basin inputs; T30 and the open constructions have no outgoing edges; discovery of truth is never an input silently substituted for evidence accuracy.

## Recommended order of proof.md runs

1. Exact foundations: T01, T09, T10, T11, T32, T33, T34.
2. Finite-particle identities: T12, T13, T14, T15, T17, T18; then T16 and T36.
3. Target transfer: T02, T03, T06, T07 (with the explicit BM-C constants and margins); T04.
4. Start and no-switch composition: T22 deterministic clauses first; EXP before its statistical clause; then T20 (i)–(ii), T21 (routes a, d, f), T26.
5. Repair and crossing: T23, T24, T19, T25 (BW2 part); PW2 and the primitive statistical verification of LK/EXIT/GAIN are separate tasks.
6. Limits and certification: T27, T28, T29, T31; then full operational integration (T21 routes c, e; T34).
7. Secondary and optional extensions: T05, T20 (iii)–(iv), T08, T30, T35, T19.

## Files

Process files: THEORY_BRIEF.md, RULINGS.md, STATUS.md, FAILED_ATTEMPTS.md, DROPPED.md, this file; council\, review\, judge\ (judge\sol1, judge\sol2 hold the Sol scripts and evidence; no ledger rows); THEORY.tex with the PDF in build\.
