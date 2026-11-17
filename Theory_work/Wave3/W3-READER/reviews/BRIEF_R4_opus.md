# BRIEF R4 — one Opus seat (diff-only re-check, Codex level 1, HQ D101) — W3-READER

You are the single council seat (Claude Opus 5.5, effort high) for the freeze editorial round. The reader text was bound at
council R3 (sol 9.5 FAITHFUL / opus 9.4; MANIFEST_R3 7aebdf2e…) and recorded on main (R3r3 CITATION-ONLY, main fe05ccec).
This round confirms only the edits since then, so that the frozen text is the corrected one.

## Content under review (frozen as `MANIFEST 8d8bcd6f1519d9b6a0851efebff3b32273072a5c998f844ed6e1000470129ac6`, file `Theory_work/Wave3/W3-READER/reviews/MANIFEST_R4.txt`)
**Review only the diff** `Theory_work/Wave3/W3-READER/reviews/R4_diff_R3r3_to_R4.diff` (= `git diff fe05ccec -- <ticket folder>`,
reviews/ and LOG.md excluded; DEPS.tsv is bookkeeping). Read the current files and the cited masters/registry/code as needed to
judge each item in context. You may read that diff file, the R3 reviews (`reviews/R3_council_sol.md`, `reviews/R3_council_opus.md`)
and `reviews/STAGED_B1.md`; nothing else under `reviews/`, nor `LOG.md`, nor `CHECKPOINT_*.md`. Scratch:
`Theory_work/Wave3/W3-READER/reviews/R4_scratch_opus/`. Change no other file; do not commit; start no subagents.

## The edits (each tagged in the text; verify each does what its tag says and nothing else)
| tag | where | change | claimed tag |
|---|---|---|---|
| T14-REP (H5 card 16, AGREED; `W3-AUDIT-AX:REP@1.0.0`, PROVED-CHECKED) | card row 3.1 and its reader note; READER_VERSIONS thm6, thm7 | the integer-limit passage becomes one sentence (IDEAL-W⁺ lifts two integer limits; in the default configuration neither can be reached on any input R can represent, $n,p_{raw}\le2^{31}-1$); caps, $\mathfrak D$, code lines, p_raw, "on $\mathfrak D$ delivery holds under the remaining (S4), without IDEAL-W⁺", and the explicit "other IDEAL-W obligations remain / default configuration only" move to the reader note and reader text. Source: W3-AUDIT `track_A_C/H5_T14_CARD.md` "Consultant edits" (binding; supersede Edit 1/2). Check: no overclaim (representable inputs still carry the other IDEAL-W obligations); the sentence matches `W3-AUDIT-AX:REP` (read with `git show origin/theory/W3-AUDIT:Theory_work/Wave3/W3-AUDIT/track_A_X/T14_REP/STATEMENT.md`; the consultant edits with `git show origin/theory/W3-AUDIT:Theory_work/Wave3/W3-AUDIT/track_A_C/H5_T14_CARD.md`). | STRONGER |
| B2 (GUARD-W wording) | card rows 3.1, 3.2, 3.5, 3.6; thm6, thm7, thm10 + row 3.5 remark | "…a run stopped by its time guard reports status `resource_limit` and returns no estimates; anything else it returns is flagged incomplete and is not covered (`v3_fit.R:84`; `v3_run.R:110-113, 142-146`)" replaces "…and no output". Check against the code lines. | EQUAL |
| AUD-S4 (W3-AUDIT TRACK_B v1.4.1) | card rows 3.1, 2.1 ("Buys"); thm9 Song–Liang comparison (3) | Song–Liang's statements on the sampler's output are limits in the number of iterations at fixed data, for every data set (supplement pp. 12–13, 16–17); ours hold at the coded budget under design conditions; neither implies the other. | EQUAL (concerns their paper) |
| R3-O1, R3-O2 (R3 Opus wording items) | thm10 honest limits; R4 "Not claimed" | comma splice; DLV-0 note (now: its two audit hypotheses are discharged, main fe05ccec) | EQUAL |
| REQUOTE | all rows/sections | every version and status quoted verbatim from `Theory_work/INFRA/registry/claims.tsv` at origin/main fe05ccec (relabel `2676e71f`: Thm-1@1.0.1, POST2 @1.0.6, DIST @1.0.1, SAMP C/TR/LT#/D @…5, PoolZ/R4 @1.0.1; D95 `fe05ccec`: W3-RM2-R RM2-R-plus/RM2-F-plus/RM0-plus/DLV-0/Cont-plus @1.0.1 plain "PROVED-CHECKED; council R3, …", `C-DLV:L2-S3`/`P1-Inventory` "CODE-CHECKED …"). Row 3.6 / Theorem 10 are now conditional on `W1-N1:B`, `W1-N1:F` (R4, `W3-SAMP:C`), which the text states with their own labels; rows 3.1/3.2 carry no open registry condition. Check each quoted status (G4) and that nothing below PROVED-CHECKED is called checked. | EQUAL (statuses only) |
| B1 | — | dropped as moot (no row carries the C-DLV conditions after D95); nothing to review | — |
| narrative | card status notes ("Status refresh", "What blocks"), thm1/thm10 limits, card v1.13 header, update logs | follow the requote | EQUAL |

## Gates (judge on the diff, each PASS or FAIL)
G1 correctness of changed text; G3 faithfulness to the masters (no change claims more than its master; T14-REP exactly as AX:REP
proves it, with the consultant's no-overclaim conditions); D71 interpretive sentences in changed text; G4 statuses verbatim against
`claims.tsv`; G5 no hidden finite-n or scope claims; G6 changed code facts against `Scripts/SMC_BVS/core/`. A change outside the
tagged items (other than bookkeeping) is an F finding.

## Output
Write `Theory_work/Wave3/W3-READER/reviews/R4_council_opus.md`: a per-item table `| tag | ACCEPT/REJECT | note |`; findings tagged
C/S/F/E with file:line and the exact correction; the gates; a score (0.0–10.0, one decimal) on C, S, F only; **exactly one line**
`FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL` on the final reader statements. You must give `gates=FAIL` if you hold a C, S or F
finding. If the round fails on anything beyond wording, the freeze uses the already-recorded R3r3 text and these edits go to the
post-freeze batch.

## Verdict line (mandatory, machine-checked)
End the review with exactly ONE line of its own:
COUNCIL-VERDICT round=R4 manifest=8d8bcd6f1519d9b6a0851efebff3b32273072a5c998f844ed6e1000470129ac6 seat=opus score=<x.y> gates=PASS|FAIL
Write no other line containing that verdict keyword. If you did not review exactly this manifest, write `gates=FAIL`.
