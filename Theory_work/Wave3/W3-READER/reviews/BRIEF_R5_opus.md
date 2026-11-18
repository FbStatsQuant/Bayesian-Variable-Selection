# BRIEF R5 — one Opus seat (diff-only re-check of the R4 fixes; Codex level 1) — W3-READER

You are the single seat. Round R4 (one Opus seat, MANIFEST_R4 8d8bcd6f…) scored 7.9, gates FAIL, FIDELITY: FAITHFUL; its only
gate failure was one status quote (F1); the rest were wording. All findings were applied in commit 7405a463. This round checks
only those fixes (and that nothing else changed).

## Content under review (frozen as `MANIFEST 9f1104743b12c1358bc5b2bbb8266c7bac345fe81f4d6bf213f25b052b80df52`, file `Theory_work/Wave3/W3-READER/reviews/MANIFEST_R5.txt`)
**Review only the diff** `Theory_work/Wave3/W3-READER/reviews/R5_diff_R4_to_R5.diff` (= `git diff b4123f62 7405a463 -- <ticket
folder>`, reviews/ and LOG.md excluded; DEPS.tsv is bookkeeping). You may read that diff, your own R4 review
(`reviews/R4_council_opus.md`) and the R4 brief (`reviews/BRIEF_R4_opus.md`); nothing else under `reviews/`, nor `LOG.md`, nor
`CHECKPOINT_*.md`. Read the current files, the registry (`Theory_work/INFRA/registry/claims.tsv`) and the code as needed. Scratch:
`Theory_work/Wave3/W3-READER/reviews/R5_scratch_opus/`. Change no other file; do not commit; start no subagents.

## The R4 findings and what was done (verify each fix is correct and complete)
| R4 finding | fix claimed |
|---|---|
| F1 (G4) card row 4.1 quoted `W3-SAMP:LT#` as plain "PROVED-CHECKED" | now `W3-SAMP:LT#@2.0.5` "PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1, …"; status cell "proved (LT-d; conditional on W1-N1:B, W1-N1:F); PoolZ PROVED-CHECKED"; "What blocks" (2) names rows 3.6, 4.1, 2.1 |
| E1 broken sentence at READER_VERSIONS thm1 master block | replaced by "…`W3-POST:Thm-1@1.0.1` now carries the label above and no open condition (relabel, main 2676e71f)" |
| E2 stale quotes in R4 header, R4 :12, REPORT:46 | R4 header gives Thm-1@1.0.1 "PROVED-CHECKED; council C3, …"; stray "(main 33e1f0f5)" dropped; REPORT depends on `W3-POST:Thm-1@1.0.1` |
| E3 old dated history lines had been rewritten | restored byte-for-byte from main fe05ccec (card v1.9, v1.10 lines, Status-refresh bullet for 14892123; reader update-log lines for thm2 v0.4, thm6 v0.5, v0.9, thm10 v0.8, v1.1). Verify that no history line differs from fe05ccec except the new FRZ-B lines and the v1.13 header. |
| E4 "What blocks" still listed the C-DLV audits | replaced by a sentence that they are discharged (main fe05ccec) |
| E5 AUD-S4 for Theorem 9 / Corollary 9C | adds "(and, for Corollary 9C, given that the returned list carries posterior mass at least $n^{-cM/2}$)" and cites "supplement pp. 9–10, 12–13, 16–17" (card rows 3.1, 2.1; Theorem 9 (3)) |
| E6 B2 code citation | `v3_fit.R:84-85`; `v3_run.R:110-113, 142-147` (card rows 3.1, 3.2, 3.5, 3.6; thm6, thm7, thm10) |

## Gates (judge on the diff; each PASS or FAIL)
G1 correctness of changed text; G3 faithfulness (no change claims more than its master); D71 interpretive sentences in changed
text; G4 statuses verbatim against `claims.tsv`; G5 no hidden scope claims; G6 changed code facts against `Scripts/SMC_BVS/core/`.
A change outside the table above (other than bookkeeping) is an F finding.

## Output
Write `Theory_work/Wave3/W3-READER/reviews/R5_council_opus.md`: a per-finding table `| R4 finding | ACCEPT/REJECT | note |`; findings
tagged C/S/F/E with file:line and the exact correction; the gates; a score (0.0–10.0, one decimal) on C, S, F only; **exactly one
line** `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL`. You must give `gates=FAIL` if you hold a C, S or F finding. If the round
fails on anything beyond wording, the freeze uses the recorded R3r3 text.

## Verdict line (mandatory, machine-checked)
End the review with exactly ONE line of its own:
COUNCIL-VERDICT round=R5 manifest=9f1104743b12c1358bc5b2bbb8266c7bac345fe81f4d6bf213f25b052b80df52 seat=opus score=<x.y> gates=PASS|FAIL
Write no other line containing that verdict keyword. If you did not review exactly this manifest, write `gates=FAIL`.
