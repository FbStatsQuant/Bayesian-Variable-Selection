# LC1, LC2 — dispositions (lead, 2026-11-15)

## LC1 (`reviews/LC1_line_check_sol.md`): PASS, no findings
R1_VIS, R2_NEC: PASS. Statement-change check of the four v1.5 changelog rows: all confirmed (STRONGER, EQUAL ×3). The
changelog column "check" now points to LC1. Nothing to repair.

## LC2 (`reviews/LC2_line_check_sol.md`): PASS WITH FIXES
| # | tag | disposition | where |
|---|---|---|---|
| 1 | S | Accepted. "For n large" thresholds that use the envelope of (D4) may depend on n_H (the index from which log H̄_n ≤ κ_H√log n holds); constants do not. N̄_n bound stated for n ≥ n_H; n_R's dependence includes n_H. The asymptotic conclusions are unaffected. [R-10] | `lemmas/R3_RATE.md` R3.0, N̄_n paragraph, R3.4 |
| 2 | E | Accepted: "and S₀ ⊆ H_l" deleted; explanation as proposed. | `lemmas/R3_RATE.md` R3.3, last paragraph |
| 3 | E | Accepted: "iff" replaced by "which tends to zero when A > 3/4". | `lemmas/R5_EX.md` R5.2 |
Also: three path-only header citations in `lemmas/R4_TRANSFER_COR.md` (lines 8-9) given their BASE/PARENT prefix (citecheck form).

**Process note.** At 21:58, two minutes after LC2 was launched, the lead made citation-form edits in R3–R5 (explicit
BASE/PARENT paths in place of short citations whose continuation was ambiguous; no mathematical text). LC2 may have read
either version. The repair re-check RC1 therefore covers: the diff `reviews/RC1_repair.diff` (snapshot 68f470b0, which
contains the 21:58 edits, → current) and every explicit-path citation of R3–R5 (citecheck output).

Re-check: RC1 (Sol, new agent), brief `reviews/BRIEF_RC1_sol.md`.

## Re-checks
* RC1 (first agent; reported stalled, completed late; `reviews/RC1_recheck_sol_late.md`) and RC1b (relaunch, re-check of
  record; `reviews/RC1_recheck_sol.md`): LC2 findings 1–3 resolved; R3 PASS, R4 PASS; R5 FAIL on one E finding (four short
  citations at R5:17, :64, :73 continued the wrong file). Accepted; replaced by explicit BASE `lemmas/L11_EXAMPLES.md`
  citations (`reviews/RC2_repair.diff`).
* RC2 (`reviews/RC2_recheck_sol.md`): R5 PASS, no findings.
