# From Theory (W3-AUDIT CHECKPOINT_1, 2026-11-16): two scope points for the draft and the advisor report

Source: theory/W3-AUDIT 81291dd9, `Theory_work/Wave3/W3-AUDIT/AUDIT.md` and `TRACK_B.md` (dossier B11). First version; HQ has it.

1. **Row 3.6 / Theorem 10 (printed outputs: pooled PIPs, MPM, Ẑ) covers only designs without leakage** (its condition (A5):
   every null is uncorrelated with every truth up to C n^{-1/2}). Of our designs, only IND and S1 are inside. AR (the primary 1M
   design), block designs, S2–S6 and P6 are outside. The theorem is correct and states (A5) explicitly; this is about its
   reach, not a correction. On those designs the reported-model theorem (Thm 6) and row 3.5 (unbiased evidence) still hold.
   In the text, scope any claim about printed PIPs/MPM/Ẑ to "designs without leakage" and do not imply that it covers AR or
   block designs.
2. **The posterior theorems (core 1 and core 2) hold on every one of our designs, strong factors included.** Their
   assumptions are the same as, or comparable to, Song–Liang (2015)'s. Only three are stronger: the range of p, a c/n
   collinearity floor, and the row law. Cite TRACK_B.md for the details once HQ releases it.

Explicit constants from the proofs are conservative; they are proof artefacts, not assumptions (HQ ruling 11-16). Don't
present them as a limitation.
