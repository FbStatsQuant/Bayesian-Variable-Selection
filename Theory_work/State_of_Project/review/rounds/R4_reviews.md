# Council round 4 — replies (2026-11-07) and the lead's actions

## Sol (gpt-6.1-sol, high): SCORE 5.0 (G4 FAIL cap)
GATES: G1 PASS | G2 PASS | G3 PASS | G4 FAIL (03_empirics.tex:117–118 field attribution) | G5 PASS
DIMENSIONS: fidelity 8.7 | completeness 9.3 | actionability 9.0 | agent-readiness 8.8 | calibration 8.8 | clarity 8.0
QUESTION_BANK: 30/30
ISSUES: (1) [major][G4] 03_empirics.tex:117–118 said every reported PIP, incl. plain, is the core's `pip_primary`; plain PIPs are `pip_plain` (v3_run.R:167–169). (2) [minor][calibration] 04_theory.tex:838 three-layer box still pinned the reported-model statement to "groups of nine, p ≈ n^{1/3}".

## Opus (claude-opus-5-5, high): SCORE 8.9 (all gates PASS)
DIMENSIONS: fidelity 9.0 | completeness 9.3 | actionability 9.0 | agent-readiness 8.8 | calibration 8.9 | clarity 8.0
QUESTION_BANK: 30/30 (Q26 thin)
ISSUES (minor): (1) same as Sol 2; (2) TH02 overview row "continuously in cross-block correlation" vs (b8) step-function stage count and grid premises for (b5)/(b6); (3) derived ranking shows only FR04 for wave 1; M3 and LP-FOUND missing; (4) N1 route text (R2C :200–204, R3A) and the M3 / D_* sketch texts only cited, not transcribed or pointed to; (5) 05_history.tex:88 cites 03b:280-281, phrase at :282; (6) GR4/GR8 drop "not the main driver" and "re-run at the end only if needed"; (7) overfull boxes (cosmetic).

## Lead's actions after round 4
- Sol 1: the §3 divergence box now says all study PIPs use equal-weight island pooling: RB = `pip_primary` (v3_run.R:126-129), plain = `pip_plain` (v3_run.R:167-168); equal-weight pooling is the v3.1 secondary PIP. Field names elsewhere (02_method.tex:802, 820, 1021) already consistent.
- Sol 2 / Opus 1: three-layer box now: M5(b1-LH) is stated for a general LH (exact Gram, p ≤ n−1, c linked pairs, group size g, ρ, |ψ| < ρ, fixed β) with SIZE, under T03♯ hypotheses on LH and the implementation premises (N3 OPEN); the shared groups-of-nine exhibit is one instance (matches TLF:292).
- Opus 2: TH02 row now "bounds continuous in ε ((b7)); the integer stage count is a step function that can jump ((b8)); (b5)/(b6) need the grid premises".
- Opus 3: derived priority table has a wave-1 row for the M3 START assembly and LP-FOUND (TH10–TH12) with the charters' first-lemma text (M3.md:93; LP-FOUND.md:111).
- Opus 4: FR04 now quotes the N1 route sketch (MEET-v31/R2_C.md:200-204) and Seat A's own reading (MEET-v31/R3_A.md:38, labelled as its reading); FR09 gained a "Starting material" paragraph (M2 charter first lemma M2.md:117; Seat C's D_* bounds MEET-THM/R2_C.md:65, :261; PC2 evidence folder).
- Opus 5: citation corrected to 03b:280-282.
- Opus 6: GR4 now quotes "Parallel computing is the final goal but it is not the main driver, …"; GR8 adds "it is re-run at the end only if needed" (DOSSIER.md:14, :18).
- Opus 7: deferred (cosmetic).
- Before round 5, an exhaustive Sol G4 sweep (all non-stmt factual sentences, code citations, registry short/regime) was run; its findings and the lead's fixes are in `R4_sweep.md`.
- Build: 236 pages; check.py 0 errors; 1,673 citations resolve; coverage 100%.
