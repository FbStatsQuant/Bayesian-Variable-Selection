# Council round 3 — replies as received (2026-11-07) and the lead's actions

## Sol (gpt-6.1-sol, high): SCORE 5.0 (G4 FAIL cap)
GATES: G1 PASS (seed 3; 18 low-coverage flags inspected: formatting/editorial labels) | G2 PASS | G3 PASS | G4 FAIL (03_empirics.tex:548–549 unqualified withdrawn inference) | G5 PASS
DIMENSIONS: fidelity 8.6 | completeness 9.3 | actionability 9.0 | agent-readiness 8.7 | calibration 8.0 | clarity 8.0
QUESTION_BANK: 30/30
ISSUE 1 [major][G4]: 03_empirics.tex:548–549 repeats "no start or search change can fix them" / "a start change can add at most the 6 stopped fits" without marking it withdrawn (contradicts 02_method.tex:913, 05_history.tex:197; NBH/03b:92 "doesn't follow"). -> keep the observed fact; remove the inference or box it as withdrawn (RF164).
STRENGTHS: round-1/2 repairs present; 273/273 coverage; cards, regime map, divergences and frontier strongly support starting theory work.

## Opus (claude-opus-5-5, high): SCORE 8.8 (all gates PASS)
DIMENSIONS: fidelity 8.8 | completeness 9.3 | actionability 9.0 | agent-readiness 8.8 | calibration 8.7 | clarity 8.0
QUESTION_BANK: 30/30 (Q10 thin)
ISSUES (all minor): (1) M1(e)/(f) summarised as unconditional in the map row, TH01 plain box, Layer (ii) and registry TH01.e — they rest on N1. (2) Brief says M1(i) "on W"; card states it for families with osc d ≤ D_* = O_P(1), W is the exhibit. (3) Regime-table LH row and three-layer box pin M5(b1-LH) to the shared LH parametrisation; M5 is stated for general LH with SIZE. (4) TH16 plain box omits that (vii-a) is an unchecked proposal dropped if its route fails, (vii-b) the checked fallback. (5) ABL-CONF entry compresses REPORT.md:9–14. (6) N9 PROOF.md prefix-identity text and L-DIL content still need the archive. (7) 76 overfull boxes (cosmetic).

## Lead's actions after round 3
- Sol 1: the withdrawn inference is now in an UNCERTAIN box citing the withdrawal (pos 1480; NBH/03b:92), cross-referenced to MD01 and reversal H.18; the empirical sentence is limited to "target-mode misses for the existing fits"; the definitional fact LIM07 (MINUTES:92) is kept. No other occurrence of the 6-fit cap in the document.
- Opus 1: "given N1 (PROOF SKETCH; otherwise marginal PIPs only, per the Fallback row)" added to the TH01 map row, the TH01 plain box, Layer (ii) (with the route quote) and registry TH01.e/TH01.f shorts.
- Opus 2: brief now "M1(i) on families with osc d ≤ D_* = O_P(1), under the T03♯ hypotheses and stacking R′_n, exhibited on W".
- Opus 3: regime-table LH row header now distinguishes the shared LH (M3(f), M4(f), M6) from the general LH with SIZE (M5(b1-LH)).
- Opus 4: TH16 plain box now says (vii-a) is an "E proposal unchecked", dropped if its route fails, with (vii-b) the checked fallback (TLF:1343; LP-REST:89).
- Opus 5: ABL-CONF entry now transcribes the per-design results (S5 10/10, p = 0.001, 1,116 s vs 1,639 s; S4 delivery 0/10 vs 9/10, "a delivery result"; S1 8/10, p = 0.055; pre-registered rule) and Claim 2's escalation counts 7/9/8 and 2–4× cost.
- Opus 6: FR04 now quotes N9-KERNEL/PROOF.md:241-244 (invariance ⇒ state before each Gibbs step is γ_φ-distributed; RB identity) and :218-220 (order uniform and state-independent). L-DIL: the notation row (added by the auditor) quotes its only definitions (node name "factorization"; edge "S-TARGET → L-DIL; L-DIL → M3(a–d) | Start normalization and dilution"); its content is the factorisation stated in M3(a)–(d).
- Opus 7: deferred (cosmetic).
- Build: 235 pages, check.py 0 errors, 1,664 citations resolve, coverage 100%.
