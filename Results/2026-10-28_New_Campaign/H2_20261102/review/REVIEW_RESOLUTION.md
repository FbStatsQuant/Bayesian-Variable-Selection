# ANALYSIS-H2: resolution of Sol R1 (ACCEPT WITH FIXES; 5 class (i), 3 class (ii))

All 8 findings were applied on 2026-11-02. No SMC, TD or extraction rerun was needed.

| # | Class | Finding | Resolution |
|---|---|---|---|
| 1 | i | T21 discovery term not identified by the miss partition | **EVIDENCE §4 rewritten** as an "operational, score-based decomposition": 6 no-output, 565 completed misses each with a scored competitor above S₀, and 0 detected search misses. The discovery term is stated as not identified (0–565), and T21's probability bound as untested (silent). Verdict changed from "support" to "consistent with the decomposition; bound silent". The table label "posterior miss" is explained as score-based |
| 2 | i | The Q_f·π₀ ≥ 1 cutoff was treated as the asymptotic regime; "every fit masked" contradicted the 1 exception | **§1:** the cutoff is now a descriptive "iid intensity ≥ / < 1" bin, at 2,393/2,394 below. The exception `p0500_S2_r034_c100` (≈ 1.09) is named; its truth was first scored at pilot stage 2. Masking is "qualitatively consistent with T27". T27(i)'s law and the T22/T38(a) hypotheses are silent. "Breaks" was replaced by "lower mass / potential difficulty". The π₀(𝓡_d) ≥ b_n premise is silent (b_n unspecified) |
| 3 | i | Pilot provenance does not establish T38(b2) | **§3 and the verdict table:** "observed first truth discovery in the pilot by Gibbs/swaps; motivates a pilot-discovery / T24-type route". T38(b2)'s premises are unverified (silent). Eligibility, the T24 conditions and the asymptotic delivery probability are listed as not tested |
| 4 | i | Failure of the TD premise is not a contradiction of the T37 implication | **Verdict scale extended:** failure of a premise ≠ contradiction. T37: "the finite-n TD(0,0) premise holds in 0/196 and fails in all 196 audited cases... T37(i) not contradicted; (ii)–(iii) silent". The mechanism is attributed to the 4 diagnosed cases only. Local search "ran and scanned, but made no improving move". Clause (c) is a necessary, not sufficient, diagnostic |
| 5 | i | The stop bound is 6, not 3 | **§5:** "at most 6 additional recoveries (0.25 points)". Per pool: 1/600, 3/600, 0/600, 2/600. Retry effect unknown. "Innocuous" replaced by "small observed incomplete fraction" |
| 6 | ii | Reproduction wording; "4th of 9" | **HEADLINE:** "all 2,400 records match on the 11 fields, including the stops' unavailable fields; every available estimate reproduces exactly". Rank: "4th; 4th of 8 among the methods with a current headline row" (the earlier 9 included the superseded ridge-pilot aLasso). EVIDENCE header aligned |
| 7 | ii | Pipeline guards and resume instructions | **combine_h2.py:** identical case-id sets across fit, theory and repro; exactly 11 unique repro fields per case; TD rows unique and within the fixed sample, all 196 present; joins `validate="one_to_one"`. **evidence_h2.py:** case-id equality plus a one-to-one merge. **Launchers:** per-worker rc logged; ALL_WORKERS_OK only when every worker exits 0; the header states that ALL_WORKERS_EXITED is not success; absolute paths required. **PROGRESS.md:** stale rows reconciled; absolute invocations and acceptance checks documented. Rerun (logs/combine3.log, evidence3.log): all checks pass; 18 output files byte-identical to before (logs/hashes_before_hardening.txt) |
| 8 | ii | Margin range −7.7 → −7.8; enrichment | **§2:** per-cell (p × c × scenario) median margin range now −12.1 to −7.8. Sentence added: sample percentages are unweighted descriptions of a miss-enriched sample |

Snapshots after the fixes: see `logs/hashes_after_R1.txt`.

## Sol R2 (narrow re-check, D53 final round): ACCEPT WITH FIXES

**Tally:** 7 resolved, 1 partially (#2), 0 not resolved; no numerical or pipeline regression. The 3 residual wording edits were applied:
1. `evidence_h2.py`: the docstring and the assignment comment now say the iid-intensity bins are descriptive, and the legacy labels "favourable"/"masked" are not the theorems' regimes.
2. EVIDENCE §1: the discovery source is attributed to provenance (§3), not to the intensity.
3. This memo: the TD count typo is fixed.

The evidence rerun is unchanged: logs/evidence4.log; the 18 outputs are byte-identical. Final hashes: `logs/hashes_final.txt`. Per D53 there is no further review round.
