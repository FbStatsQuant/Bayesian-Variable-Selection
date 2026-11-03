# Sol independent review — ANALYSIS-H2, round 1

**Verdict: ACCEPT WITH FIXES.** Five class (i) findings and three class (ii) findings. The recovery tables and reproduction comparisons are sound on the checks below. The must-fixes concern scientific interpretation and one incorrect bound; they do not require rerunning SMC or the full TD audit.

Reviewed locally on Felipe's Windows laptop, 2026-11-02, using Python (`py -3`) and R 4.4.1. No SSH, remote host, fitting run, or modification of deliverables. Only this review and scripts in `review/sol_scratch/` were written. D53: this is the first full round, not a request for an open-ended review cycle.

1. **Class (i), must-fix — T21's discovery term is not identified by the miss partition.**

   **Location:** `EVIDENCE_H.md`, one-line T21 verdict and §4; interpretation of `scripts/evidence_h2.py`'s `miss` field.

   **Evidence:** T21(C1) contains P(Uᶜ, S₀ ∉ 𝒮), without the qualification “though it would have won.” The observed 0 search misses establish only that no completed report has F(S₀) > F(HPM). For each of the 565 reports with F(HPM) > F(S₀), the truth could have been scored or never scored. All 2,400 `truth_scored` values are unavailable, as the report itself explains. HPM provenance certifies scoring of S₀ for the 1,829 hits, not for the 565 posterior misses. Nor is the theorem's posterior-mass expectation evaluated here. Consequently “the discovery term is empirically 0,” “the posterior term binds,” and an unqualified **support** verdict for the displayed inequality overstate the evidence.

   **Concrete fix:** Retain the correct 6/565/0 partition and label it an operational score-based decomposition. Say “0 detected search misses; each completed miss has a scored competitor above truth, so even scoring truth could not make that report a hit.” Mark the actual discovery term unknown (its empirical count among completed fits is between 0 and 565) and the quantitative T21 bound untested/silent. A qualified “consistent with T21's decomposition” is acceptable if distinguished explicitly from testing its probability bound. Do not rename the score-based miss class to imply observed trace membership.

2. **Class (i), must-fix — The finite intensity cutoff is being treated as an asymptotic regime theorem, with contradictory counts.**

   **Location:** `EVIDENCE_H.md`, one-line T22/T27 verdict, §1 findings/verdicts; `scripts/evidence_h2.py` regime definition.

   **Evidence:** The implemented Q_f = 4 N_e(T + 8 + 5), N_e = 2,500/10,000, matches the stated budgets. However, Q_f π₀(S₀) ≥ 1 is a descriptive expected-count threshold, not T22(iii)'s concentration hypotheses, T38(a)'s Q_f π₀(S₀) → ∞, or T27's two-sided cancellation law. `ev_case_derived.csv` has **1 above-threshold completed case and 2,393 below**, with the exception `p0500_S2_r034_c100`, log intensity 0.081779 (intensity approximately 1.085). Thus “Every fit is in the masked regime,” “the masked regime is the only one observed,” and “that regime is not occupied ... neither can explain any recovery” contradict the report's own exception and conflate finite/asymptotic meanings. Two p values at fixed n, with no checked completion-chain ratio law, cannot test T27(i)'s joint n/p mass law. Likewise, π₀(R₂) = 0.25–0.40 is not a demonstrated “break” of π₀(R_d) ≥ b_n when b_n and its required budget scaling have not been specified; it is substantial positive mass.

   **Concrete fix:** Call these “iid intensity below/above 1” bins; report 2,393/2,394 below and one above. Describe tiny start truth mass and its p dependence as qualitative evidence of masking, compatible with T27, while leaving its specific law and T22 hypotheses untested. Remove the universal/no-exception sentences. Report the measured near-truth masses as descriptive eligibility inputs, and replace “breaks” with “lower mass / potential difficulty”; specify b_n before claiming its premise passes or fails. The actual first-delivery conclusion can rest on provenance, independently of these bins.

3. **Class (i), must-fix — Pilot Gibbs provenance does not establish T38(b2)'s delivery premises.**

   **Location:** `EVIDENCE_H.md`, one-line T38 verdict and §3.

   **Evidence:** The provenance counts are correct: all 2,394 completed HPMs were first obtained in the pilot; the 1,829 truth hits split 1,724 Gibbs / 104 neighbour swaps / 1 uniform swap. But T38(b2) requires T24 conditions and an eligible particle at terminal rounds. Provenance at a pilot bridge stage neither checks those conditions nor identifies the repair trajectory or terminal eligibility. An R spot-check, `p0500_S2_r034_c100`, first scores truth at pilot stage 2 with phi = 0.02381287; this is not evidence of terminal-round repair. Reporting only completed fits is descriptive and cannot certify the unconditional asymptotic delivery premise.

   **Concrete fix:** State “observed first truth discovery in the pilot by Gibbs/swaps; motivates a pilot-discovery/T24-type route.” Mark the formal T38(b2) premise unverified/silent; do not say it holds empirically or that the observed mechanism is the theorem's b2 route. Keep the measured provenance and weak descriptive cost scaling. Specify that neither eligibility, T24 conditions, nor asymptotic delivery probability was tested.

4. **Class (i), must-fix — Separate failure of TD as a finite-n premise from contradiction of the conditional/asymptotic T37 statements.**

   **Location:** `EVIDENCE_H.md`, verdict scale, one-line T37 verdict and §2 verdicts.

   **Evidence:** The TD audit is a valuable negative finding: strict TD(0,0) holds in 0/196 sampled cases; both variants have identical violation counts. The four move diagnoses show truth-for-truth swaps dominate the competing moves. T37(i), however, says **if** strict TD holds and the move budget suffices, repair follows. Violating its antecedent does not refute that implication. T37(ii) is a union probability bound, and (iii) is an asymptotic claim under G/R/SE/BM-∞; neither has been tested at a single n. The supplied verdict scale defines contradict as refuting the statement as worded, so the present labeling risks handing the theory phase a false theorem-refutation verdict. Also the mechanism diagnosis was done on four cases, not all 196. Local search did run and scan; it made no improving moves, which is more precise than “never exercised.”

   **Concrete fix:** Preserve the negative headline as “finite-n TD premise fails in all 196 audited cases; truth-for-truth swaps explain the four diagnosed examples.” Explicitly state T37(i) is not contradicted and T37(ii)/(iii) remain untested/silent. Do not generalize the four-case mechanism diagnosis to every case. Say “repair by improving moves was not exercised; searches terminated without a move.” Treat clause (c) as a necessary local-optimality diagnostic, not a sufficient operative condition for a hit (three sampled posterior misses satisfy it).

5. **Class (i), must-fix — The maximum recovery effect of completing six stops is six, not three.**

   **Location:** `EVIDENCE_H.md` §5, final verdict.

   **Evidence:** The six primaries all count as nonrecoveries. Three stopped supports already equal truth, but their exclusion from primary counts does not bound how many of the other three could recover after further computation. No P5 retry was run (D62). Thus “at most 3 recoveries would change” is unsupported and conflicts with the preceding 0.25% bound (6/2,400).

   **Concrete fix:** Replace with “at most six additional recoveries overall (0.25 percentage points of 2,400); observed retry effect unknown.” At the p × c pooled level the maximum gains are 1/600, 3/600, 0/600, 2/600 for p500 c1, p1000 c1, p500 c0.5, p1000 c0.5. Qualify “innocuous” as a small observed completion fraction, rather than a verified theorem assumption or a measured retry effect.

6. **Class (ii), should-fix/minor — Reproduction wording should distinguish matching absent outputs from reproduced estimates; current rank uses the historical nine-method set.**

   **Location:** `HEADLINE_H.md` opening reproduction bullet and §5; `repro/repro_summary.csv`.

   **Evidence:** All 26,400 saved comparisons are genuinely identical. For stopped cases, some fields are NULL in both records (R spot-check `p0500_S5_r088_c100`: log_Z, island log_Z, pooled/island RB PIPs and MPM have length 0). This is correct record reproduction, not 2,400 reproduced numeric estimates. Also “4th of 9” includes a method whose current headline is pending.

   **Concrete fix:** Say “all 2,400 records match on the 11 fields, including matching unavailable fields at stops; all available estimates reproduce exactly.” Qualify the nine-method rank as the historical comparison with the superseded aLasso pilot, or state the rank among the eight methods with available current headlines. Keep the pending aLasso row and D55 last-grid caveat.

7. **Class (ii), should-fix/minor — Pipeline acceptance guards and resume instructions are weaker than the resulting checked artifacts.**

   **Location:** `scripts/combine_h2.py`, `scripts/evidence_h2.py`, `scripts/launch_*.sh`, `PROGRESS.md`.

   **Evidence:** The current files pass one-to-one reconciliation, but combine checks counts/duplicates only for fit/theory, not the expected 11 unique repro fields per case, TD uniqueness/completeness/sample membership, or equality of the actual case-id sets before left joins. The evidence merge has no `validate='one_to_one'`. Launchers use bare `wait` and always print ALL_WORKERS_EXITED without preserving individual worker return codes; errors require checking .err and output completeness independently. Documented launch arguments are relative and the launcher does not resolve them against H2. PROGRESS still says TD RUNNING / EVIDENCE TODO and a tie-out attempt RUNNING beside later DONE entries.

   **Concrete fix:** At minimum document the independent final acceptance checks and absolute invocation paths, state that ALL_WORKERS_EXITED is not success, and reconcile stale progress entries. For reusable scripts, add explicit expected id/field sets, join validation, TD sample checks, and worker exit aggregation. These are hardening/documentation items for this round: no current missing/duplicate record was found and no new workload is required.

8. **Class (ii), should-fix/minor — Correct one rounded range and make sample enrichment visible beside TD percentages.**

   **Location:** `EVIDENCE_H.md` §2 clause-(a) margin range and TD sample discussion.

   **Evidence:** Direct grouping of the 196 cases by p × c × scenario gives cell-median add-true minimum margins from **−12.139974 to −7.829995**, i.e. approximately −12.1 to −7.8, rather than −12.1 to −7.7. The saved `ev_td0.csv` additionally stratifies by sample_reason, which is not the same aggregation. The sampling rule is disclosed correctly, but includes every strong-signal miss; aggregate violator shares and hit/miss associations are therefore sample descriptions, not population estimates. The numerical 0/196 finding remains valid.

   **Concrete fix:** Use −7.8 for the per-cell range, or explicitly name the different grouping if −7.7 was intended. Add one sentence that enriched-sample percentages are unweighted/descriptive. Keep the fixed five replicates per cell and all-miss enrichment explicit; no additional TD audit is requested.

## Validation and scope of acceptance

- Read the requested charter/decisions (including D35), theory strategy, previous headline, frozen list, T37/T38, and T21/T22/T27/T03/T07/T26/T12. Reviewed the specified H2 extraction/build/combination/evidence/launch scripts and scoring definitions/DP/TD implementation. Terra's completed tie-out was not rerun.
- `review/sol_scratch/check_r1.py` ran locally with exit 0. It checks unique 2,400-case tables and one-to-one joins; recomputes all three selection-exact flags from saved supports and truth; checks all 26 numeric main-headline markdown rows against the long table and all SMC scenario counts against per-fit records; verifies 26,400 unique case/field reproduction comparisons with all identical flags and numeric maximum difference 0. It also prints the TD, miss-shape, start-mass, provenance, cost and PIP summaries for inspection.
- Main pooled counts confirmed: HPM 559/560/370/340; RB MPM 559/561/338/321; plain MPM 559/561/338/320 (p500 c1, p1000 c1, p500 c0.5, p1000 c0.5). Sensitivity totals match the prior table; EN alpha 0.9 in 2,399/2,400, one alpha 0.5 at p500 S4 c0.5. D35/D42 switch and post-hoc c1 choice are disclosed; aLasso pending and future last-grid disclosure are appropriate.
- Evidence counts, shapes, cost ratios, TD counts, diagnosis percentages, gaps, PIP agreement, ledger shares and stop details were inspected against their saved tables. Confirmed 565 posterior misses, 207 same-size misses, minimum positive gap 0.004869 nats, 23 gaps below 0.1, 39.292% below 1; 0 local moves in all 2,394 completed fits; 196 complete enum TD audits; 2,391 matching RB/plain MPMs; no exact-reference truth-mass/coverage/HPM or truth-trace fields populated at high p. T07's within-size ranking interpretation is valid; “same-size swap” here denotes equal-size wrong supports, not necessarily a single-variable swap. T03/T26/T12 silence is appropriately disclosed.
- `review/sol_scratch/spot_r1.R` ran locally with exit 0 on four old/new RDS pairs (above-threshold case, plain-MPM recovery disagreement, completed tier-1 case, and stop). Nonempty stored arrays agree, RB threshold selection agrees where available, local fields/provenance are consistent, and tier budgets/L = 8 confirm the Q_f constants. R emitted Windows locale startup warnings; checks completed. This is a spot-check of the raw reproduction, not a second all-RDS rerun.
- No high-p Z-hat accuracy or PIP-vs-exact accuracy is presented. Reproduction and RB/plain agreement are appropriately distinguished from accuracy. HLL/scored-mass unavailability, sampled d=0 TD, absent d=1 audit, and unrun P5 are explicitly disclosed. The weak two-p cost comparison is descriptive, not proof of polynomial asymptotic complexity.

Reviewed snapshot SHA-256:

| File | SHA-256 |
|---|---|
| HEADLINE_H.md | 959f4de8bb6ba2c7e3d90abbec8794c7290e148057335702f1880f8d4aa9d773 |
| EVIDENCE_H.md | ac36538c1a1760143f0705d604ad5e50ea49cee5c0471d048b1d8f0b9cdc7a2f |
| case_theory_H.csv | 8a6bbc32b2e807dd653f4c63fb3186281ce45d0d82735a7e51414a3f21ea9207 |
| scripts/evidence_h2.py | 33f6d3222d291a32eee427daee1be706b4e0ece2ca8c691db762715d4076c1de |
| scripts/extract_h2.R | 8212d66199a2794ae7231f9f8b2bf3f2a1932256080aa15632e2153ed858d594 |
