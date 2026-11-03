# Sol narrow re-check — ANALYSIS-H2, D53 round 2 (final)

**Verdict: ACCEPT WITH FIXES.** Seven R1 findings are resolved; finding 2 is partially resolved, with only terminology/attribution edits remaining. No numerical or pipeline regression was found. One new documentation typo reverses the TD count in the resolution memo. Exact residual edits are listed below; no SMC, extraction, TD, or numerical-output rerun is needed.

Reviewed locally on Felipe's Windows laptop on 2026-11-02. Scope was limited to R1 findings 1–8 and errors introduced by their fixes. Read all requested revised files, both rerun logs, and both hash manifests. No SSH or remote hosts were used. Deliverables were read-only; only this report and `review/sol_scratch/check_r2.py` were written.

## Per-finding disposition

| R1 | Status | Reason |
|---|---|---|
| 1 | RESOLVED | EVIDENCE §4 preserves 6/565/0 as an operational score decomposition, bounds unknown completed-fit truth non-discovery by 0–565, and leaves the posterior expectation and T21 probability bound untested. |
| 2 | PARTIALLY | EVIDENCE §1 correctly distinguishes descriptive bins from asymptotic hypotheses, reports 2,393 below/1 above, and leaves T27/T22/b_n premises untested; `evidence_h2.py:7,43–52` still calls the bins “iid regime”/“favourable”/“masked,” and EVIDENCE line 60 still attributes discovery-source identification to the intensity. |
| 3 | RESOLVED | EVIDENCE §3 identifies the pilot provenance of all completed HPMs and the 1,829 truth hits, while explicitly leaving T24 conditions, terminal eligibility, repair trajectory, and asymptotic T38(b2) delivery unverified. |
| 4 | RESOLVED | EVIDENCE states the TD premise fails in all 196 audited cases, T37(i) is not contradicted and (ii)–(iii) are silent; diagnosis is limited to four cases, scans made no moves, and clause (c) is necessary rather than sufficient. |
| 5 | RESOLVED | EVIDENCE §5 gives the six-recovery/0.25-percentage-point upper bound and 1/600, 3/600, 0/600, 2/600 pool bounds, with retry effect unknown. |
| 6 | RESOLVED | HEADLINE explicitly distinguishes matching records, including empty stop fields, from available estimates; the historical nine-method rank and current eight-method comparison are distinguished, with adaptive lasso pending and D55 retained. |
| 7 | RESOLVED | Combine now checks case sets, unique expected repro fields and fixed TD sample membership/count, with one-to-one joins; evidence validates its merge; launchers collect worker return codes and condition ALL_WORKERS_OK on zero failures; PROGRESS reconciles stale states and documents absolute-path invocation and acceptance checks. |
| 8 | RESOLVED | EVIDENCE §2 uses −12.1 to −7.8 for the p × c × scenario cell medians and labels percentages as unweighted descriptions of the miss-enriched sample. |

## New error introduced by the fixes

`review/REVIEW_RESOLUTION.md:10`, finding-4 resolution: “the finite-n TD(0,0) premise fails in 0/196” reverses the count. It **holds in 0/196 and fails in 196/196**. EVIDENCE itself has the correct statement. This is a documentation typo, not a changed result.

No new computational error was found in the revised guards or launcher exit aggregation. This conclusion uses source inspection, syntax checks, saved logs and output reconciliation; the launchers were not executed against real workers in this re-check.

## Exact residual edits

1. **Finding 2, storage-label clarification:** in `scripts/evidence_h2.py:7`, replace the “iid regime” definition with: “Descriptive finite-n iid-intensity bins: Q_f*pi0(S0) >= 1 or < 1. Legacy storage labels 'favourable' and 'masked' denote only these bins; they do not assert T22/T27/T38 hypotheses or asymptotic regimes.” Add the same clarification beside the assignment at line 43. The existing CSV/JSON labels can remain for compatibility, preserving the checked numeric artifacts.
2. **Finding 2, attribution:** in `EVIDENCE_H.md:60`, replace “The finite-n iid intensity says final-run iid draws are not how these fits found the truth (see §3)” with “Provenance (§3) identifies pilot SMC as the source of first truth discovery in the 1,829 hits.” A finite expected-count cutoff does not identify an observed discovery mechanism; the inspected provenance does.
3. **New memo typo:** in `review/REVIEW_RESOLUTION.md:10`, replace “the finite-n TD(0,0) premise fails in 0/196” with “the finite-n TD(0,0) premise holds in 0/196 and fails in all 196 audited cases.”

These are narrow wording fixes. No additional review topic or computational workload is requested.

## Validation evidence

- `py -3 -X utf8 <absolute H2>/review/sol_scratch/check_r2.py`: exit 0. SHA-256 recomputation matches **18/18** entries in `hashes_before_hardening.txt` and **17/17** in `hashes_after_R1.txt`. Thus all 18 manifested pre-hardening outputs remain byte-identical, and the revised snapshot matches its manifest.
- Independently checked unique 2,400-case fit/theory tables, equal case-id sets, 26,400 unique reproduction case/field comparisons with the exact 11-field set and all TRUE, a one-to-one merge, and exact equality of the 196 TD case IDs to the fixed sample.
- Saved outputs confirm 2,394 completions; six stops in the stated pools; 1,829 hits/565 completed competitor-above-truth misses/zero detected search misses; 2,393 below-threshold cases and the single above-threshold case `p0500_S2_r034_c100` (log intensity 0.0817787095647197).
- Recomputed TD cell-median margin extrema: −12.1399743671711 and −7.82999496551361; all 196 audits complete, zero strict holds.
- Both revised Python scripts parse; `bash -n` on each revised launcher exits 0. Inspected `combine3.log` and `evidence3.log` agree with the saved counts. Production post-processing was not rerun because it would overwrite deliverables.
- The first scratch invocation completed its substantive checks but exited 1 while printing Unicode through Windows cp1252; the UTF-8 invocation above completed with exit 0.

Verdict: ACCEPT WITH FIXES (the three wording edits above).
Per-finding tally: 7 RESOLVED; 1 PARTIALLY; 0 NOT RESOLVED.
Path: <OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\analysis\H2_20261102\review\SOL_RECHECK_H2_R2.md
