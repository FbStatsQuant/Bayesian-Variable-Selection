# W8-SYNTH brief: where the theory stands (2026-11-02, ~20:40 UTC)

Executive version of `SYNTHESIS.md`. Everything is a **candidate**; nothing is adopted. XF = verified by Astra.

**The story holds.** The reported HPM is right when the posterior ranks the truth first and the run scores the truth.
Thm 4 (T21) turns this into an exact inequality for every n.

**At n = 200 every error is statistical** (`S-ELS`, the actual 2,400 fits):
- 1,829 exact recoveries, 565 posterior misses, **0 search misses**, 6 stopped;
- S₀ was scored in every completed fit, and the final local search never moved.

**Solid (proved, Claude-verified and XF-verified):**
- Thm 1 (T03♯), asymptotic only, thresholds ≈ 2·10⁶;
- EXP′ and the chain-masking law (Thm 2);
- Theorem A, the exact greedy repair, and Theorem B, the Gibbs-path repair (Thm 3);
- Thm 6 Theorem A;
- Prop 1 (T07) and Thm 4 (T21), both locked and formalised in Lean (87 declarations, 0 sorry).

**Main theorem T38 (Thm 5):**
- (0) composition and (a) favourable regime: proved. (c) cost: proved (T32(i), W5-LOCKBOOK, re-checked by W7-SEC).
- Masked regime: fully proved on the LH family **with LS0**, Claude-verified only. The p ≫ n version has an open XF GAP (A-REV3).

**New: masked regime without LS0.** Five candidates on LH: D2-LH (c = 1), B2-LH (under a numerical premise),
BG3 + sketch, F-SHARE F2 (sketch), Prop GU. None is XF reviewed. "No masked theorem without LS0" is out of date, but
"closed without LS0" would overstate.

**Still open:** delivery beyond LH; masked-regime Ẑ/PIP accuracy (only one-sided M1–M3 are proved); anything quantitative at
n = 200; any theorem for the study's actual masking (dilution).

**Errors.** Astra found real errors in about ten Claude results. All have Claude-written repairs except W4-SHARE M(b),
F-DRAFT W2/NM and the A-REV4 bookkeeping items. **None of the repairs has been re-reviewed by Astra.**

**Referee (F-REFEREE): major revision.** Its ask: Thm 5(b) for the algorithm actually run, on LH, with the transition
shown at growing n. Of its 8 major points, 0 are done, 6 in progress, 2 open. W7-SEP undercuts the planned "tempering is
needed" spine: the theory supports "moving off the start is needed".

**Decision 1, LS0.** Approved, conditional on O-LS0 data, **which has not landed**. LS0 cannot fix any study miss.
Recommendation: keep the approval. If the no-LS0 LH routes pass XF review (task 1), make the no-LS0 theorem the
headline and LS0 a remark.

**Decision 2, common-σ² start.** Reject it. O-DILUTE and F-SIGMA show it floods the start in study-like designs. If any
start change is wanted, residualised tables are the candidate (378/480 favourable in a pilot). Run the free post hoc
Step 0 first (task 8).

**Decision 3, n = 200 disclosure.** Use the draft in SYNTHESIS §1, with corrected numbers: beta-min ≥ 43× (not 100×),
threshold ≈ 2·10⁶, 6 stopped fits, 0 search misses. Drop the "favourable from n ≈ …" figure: runs give 590–730,
800–1,600 and 1,050–3,200. Also choose the output convention; strict 𝒪 is recommended.

**Next three tasks:** (1) XF verification of the no-LS0 LH routes; (2) a general proof of LH-lock; (3) finish O-LS0 and
interpret its 5/7 hash mismatches. The ranked list of 10 is in SYNTHESIS §8.
