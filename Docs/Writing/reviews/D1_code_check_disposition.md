# Disposition of D1_code_check_opus.md (Opus, NOT-CODE-FAITHFUL). Manager, 2026-11-16.

**C (all fixed; confirmed in the code by the manager)**
1. The pre-run check is not memory-only. A new paragraph, "The check before the run", in Stage 1 gives the formula and the 24-hour threshold at n = 200, p = 10⁴; a new table row; a new item in Appendix D. Escalated to HQ for Engineering.
2. Tier 1 uses its own random streams (5–9). Algorithm 1 step 5 is corrected, and a streams row is added.
3. The independence move can change the size. The sentence is corrected: all moves stay in Ω.

**S (all applied)**
- The pilot's and the diagnostic islands' burn-in and measured rounds.
- When E1/E2 and E3/move-cap are evaluated.
- The move-cap semantics: "still improving at the cap". Also fixed in the trigger list.
- The diagnostics list extended.
- What a stop returns, by case.
- The exact case's global certificate (heuristic).

**E (applied):** start mode computed at the end of the run; streams "separately seeded"; self-loop cases of the swaps; grid-failure modes, including the 10⁻¹² snap; the intro's "every model scored anywhere" corrected.
**E (not applied):** the Occam-factor precision (n^{-1/2} vs (n+1)^{-1/2}; "about" kept); the QR detail of the numerics.

**Table:**
- Resampling pin → `v3_engine.h:230-259`.
- E1/E2 pin → `v3_calib.R:101-102`.
- Cache row adds `v3_calib.R:147`.
- Pilot target 1,843.2.
- Added rows: diagnostic islands (4), snap 10⁻¹², global-certificate margin, check before the run, random streams.
- "Every constant" → "the constants".

**Cost sentence:** now "score requests", most answered from the cache.

**Appendix D:**
- Item 1 names both documents.
- Item 3's pin widened to 363-400.
- Seven items added (D4–D14 of the report, grouped).
