# Council round 1 — summary for round-2 reviewers

| Reviewer | Score | Gates | QB |
|---|---|---|---|
| Sol (gpt-6.1-sol, high) | 5.0 (capped: G4 FAIL) | G1 PASS, G2 PASS, G3 PASS, G4 FAIL, G5 PASS | 30/30 |
| Opus (claude-opus-5-5, high) | 8.8 | all PASS | 30/30 |

## Findings and what the lead changed (all accepted; no objections)

Sol
1. [major][G4] `sections/04_theory.tex:31` overview row of TH05 said the reported HPM is S₀ jointly with output "w.p. → 1" — stronger than the card (delivery unproved).
   → Fixed: the row now states P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, hence liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n); "delivery (P(𝒪) → 1) is not claimed".
2. [minor][calibration] PR #1 "unmerged" without temporal qualifier vs UNCERTAIN elsewhere.
   → Fixed with a new fact: the lead queried GitHub on 2026-11-07 (`gh pr view 1`): OPEN, not merged, last updated 2026-11-02. Recorded as `sources/PR1_status_2026-11-07.json` and cited in §5 (H.4), §6 (DEC09) and Appendix C; registry DEC09 status now "OPEN (PR open, unmerged on 2026-11-07)".
   → Lead also found and fixed a related G4 problem: Appendix C credited commit 21ebc28 to an archive file that predates it; now cited to `sources/git_log_main_2026-11-07.txt`.

Opus
1. [minor][G4] approval of 2026-11-07 uncited → new source `sources/approval_2026-11-07.md` (Felipe's verbatim words, scope, exclusions); cited in §4 Approval paragraph, the agent brief and the changelog.
2. [minor][calibration] 5/318 counterexample design not qualified → EMP25 (§3), FR06 (§6) and the §5 do-not-retry row now say the LIT-PAR design's masked variable is a singleton (group size 1, not the g-prior's g; CE213 at ID_REGISTRY:1309, CE214 at :1310), not the LH family.
3. [minor][agent-readiness] EMP12 registry status looked reviewed → now "UNCERTAIN (repo: not identified, 0 to 565; S-ELS: S0 in the top store in all 2,394 completed fits; unreconciled). Repo half: …; S-ELS half: no tie-out".
4. [minor][contradiction] N9 7 vs 8 sub-claims → §2 invariance paragraph now marks the count UNCERTAIN (7 at pos 1550, 8 at pos 1593) and points to the uncertain boxes under TH12 and OB09.
5. [minor][agent-readiness] "101 sorry-free theorems" → brief now: 101 declarations, 0 sorry; abstract finite cores; T12 core partial (`hstep` hypothesis); no main card Lean-certified as a whole; no external human review (all checks AI + Lean), cited to NBH/03_results_and_conclusions.md:22, :340.
6. [minor][actionability] frontier not ranked → new table "Priority of the frontier problems (derived)" in §6 (label sec:open:frontier-rank), explicitly derived only from binding goals (COVERAGE_MATRIX:16,23) and the wave order (MINUTES:110–113); scope extensions and scouts listed as unordered.
7. [minor][clarity] overfull boxes → td0 header wrapped; `\emergencystretch` and breakable underscores added; overfull warnings 157 → 75, worst 66 pt → 40 pt.

Build after fixes: 232 pages; check.py 0 errors; 1,633 citations resolve; coverage 100% (273/273); tables regenerate identically.
