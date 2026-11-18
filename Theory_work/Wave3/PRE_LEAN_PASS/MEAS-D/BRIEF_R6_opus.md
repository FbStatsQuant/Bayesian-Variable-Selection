# BRIEF R6: one fresh Opus seat (council round R6, diff round R5 -> R6, THE LAST Opus round before Sol-5) for the W3-SAMP lemma MEAS-D

You are the single seat for round R6 (Claude Opus 5.5, effort high, claudeAgent_personal; fresh: you did not see rounds R1-R5). Be skeptical. **Scratch only under `<worktree>/.rc_tmp/`; nothing in /tmp or /tmp/claude-*; no `git worktree add` there.** Write only your review as your final message (no files, change nothing, commit nothing, start no subagents).

**HQ rule for this round.** R6 is the last Opus round; there is no R7. Classify every finding you raise as exactly one of: **WORDING** or **QUALIFIER** (give the exact replacement text, which will be applied as you word it, CORRECTION-ONLY, followed by one PURE check; mark it "apply as written"), or **GENUINE GAP** (a step that does not hold, or an h with no Borel reason in proved text; nothing will be applied and it goes to HQ). Say plainly at the top of §3 which kind(s) you hold.

**Scope: the R5 -> R6 diff.** Read `Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/R5_council_opus.md` (the R5 review: 8.8, gates FAIL on F7; E25-E29) and `R5_to_R6.diff` (same folder), and `H_CLAUSE_INVENTORY.md`.

## What is under review (frozen)
`Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/MANIFEST_MEASD6.txt`, first line `MANIFEST 87dfd9f8258f978affc44879ac3ae01633ff9e481ed65406161091af781c5296` (ticket dir `Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/ticket`, 3 files, plus the same 21 external inputs as R5). First run `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/ticket Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/MANIFEST_MEASD6.txt` and report its output (it must print `verify: OK MANIFEST 87dfd9f8258f978affc44879ac3ae01633ff9e481ed65406161091af781c5296`). Files (under `.../ticket/Theory_work/Wave3/W3-SAMP/`): `lemmas/MEAS_D.md` (96 lines), `STATEMENT.md` (194 lines; claim statement :190-192), `REPORT.md` (REGISTRY :199-206).

## Edits this brief claims, grepped in the REAL ticket files before freezing (HQ rule; each with file:line; all present at freeze)
    OK   ticket/.../W3-SAMP/STATEMENT.md:190  F7 phrase, statement (claim span 190-192)
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:24  F7 phrase, MEAS_D §1 copy of the statement
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:50  F7 phrase, Step 6 first sentence
    OK   ticket/.../W3-SAMP/REPORT.md:203  F7 phrase, REGISTRY conclusion (E26: 'section 2')
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:50  F7 Step 6 sentence 'H_r(h) and pi(h) are Borel'
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:42  F7 Step 5 phrase
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:50  E25 MR weights
    OK   ticket/.../W3-SAMP/STATEMENT.md:194  E27 remark wording
    OK   ticket/.../W3-SAMP/REPORT.md:204  E28 depends_on
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:3  E29 status line (R1 to R6, MEASD6)
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:3  E29 status line: Sol bound to MEASD6
    OK   ticket/.../W3-SAMP/REPORT.md:205  E29 gates pointer R6
    OK   ticket/.../W3-SAMP/STATEMENT.md:36  kept from MEASD5: E1 sentence (NB-C1v2)
    OK   ticket/.../W3-SAMP/STATEMENT.md:194  kept from MEASD5: remark paragraph (NB-C1r)
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:37  kept from MEASD5: E23 bound
    OK   ticket/.../W3-SAMP/STATEMENT.md:0  ABSENT: whose bound B_h does not depend
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:0  ABSENT: whose bound B_h does not depend
    OK   ticket/.../W3-SAMP/REPORT.md:0  ABSENT: whose bound B_h does not depend
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:0  ABSENT: expectation P(𝒜°) ≤ 1 by
    OK   ticket/.../W3-SAMP/STATEMENT.md:0  ABSENT: that is, one intersected with
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:0  ABSENT: MEASD4 digest
    

    file sha256 (first 16) and line counts:
    STATEMENT.md: 08c1ed7fab7b8733 lines=194
    REPORT.md: a17058dfcc61e510 lines=206
    lemmas/MEAS_D.md: 8f0a2164f7337671 lines=96
    RESULT: ALL CLAIMED EDITS PRESENT

(If any claimed edit is not where this table says, or the verify digest differs, write gates=FAIL and say so.)

## What to check (every item gets a line)
1. **F7 in all four places** (`STATEMENT.md:190`, `MEAS_D.md:24`, `MEAS_D.md:50`, `REPORT.md:203`): the phrase is R5's own ("that is a Borel function of (data, S, c) with a bound B_h that does not depend on the data"); the registry copy says "section 2" for "§2" (E26). Check the three companion edits: Step 6's "H_r(h) and π(h) are Borel (h is Borel in (data, S, c), 𝓒° is Borel by Step 3, and the S_{rqi} are coordinates of the island record, Step 4)" (`MEAS_D.md:50`) and Step 5's "(for (MR) and (N1), g is Borel when h is Borel in (data, S, c))" (`MEAS_D.md:42`): do they now make the Step 5 display and the Step 6 paragraph correct, with no premise added, for every h the clause covers? Verdict: `(F7) PROVED, NO NEW PREMISE | <problem and exact text>`.
2. **The inventory** (`H_CLAUSE_INVENTORY.md`): for each h used by a clause MEAS-D serves, is the Borel-in-(data, S, c) reason right from proved text (functions of S alone; f_t of `lemmas/C_theorem.md:37-40` via d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b) at `STATEMENT.md:24`, MEAS-D Step 2 for d, CAL-c / Step 4 for the grid Δ_t) and B_h = 1? Is anything missing (grep the W3-SAMP statement and lemmas for every use of MR with an h)? Verdict: `(inventory) RIGHT AND COMPLETE | <h with no Borel reason in proved text: file:line>`. A missing Borel reason for a used h is a GENUINE GAP.
3. **E25** (`MEAS_D.md:50`: "at most P(𝒜°) ≤ 1 … exactly P(𝒜° ∩ {T ≥ t}) for (MR-a)"): correct against `STATEMENT.md:107-116` and `lemmas/MR_identities.md:27-30`? **E26** (registry "section 2"; the converter exits 0 with 12 depends_on items, none with spaces). **E27** (`STATEMENT.md:194`, the remark's scope: "an event of the statistical state intersected with {completed}, or a potential or calibration-time event intersected with the actual 𝒜 (§0, :33-34)"; check against `Theory_work/Wave3/W3-AUDIT/track_A/T5_CAL/STATEMENT.md:47-52` and `T1_GW/STATEMENT.md:80-102`: it is now true and adds nothing to any claim). **E28** (depends_on: `W3-SAMP:MR@stmt:MR-a,MR-b,MR-c` and `W1-N1:Thm-N1@stmt`: both ids in claims.tsv; each used by Step 5/6). **E29** (status line `MEAS_D.md:3` names R1-R6 and MEASD6, Sol bound to MEASD6; gates pointer `reviews/R6_council_opus.md`). One line each ACCEPT/REJECT.
4. **Nothing else moved** (R5's accepted items stay as they were): the claim span is :190-192 and `R5_to_R6.diff` changes inside it only the F7 phrase; §§0-3 differ from main only at :36; scope still potential-only; the converter exits 0 on a scratch copy of the staged REPORT.md under `.rc_tmp/`; no `|x|` bars in the block or the statement; Steps 1-6 and F4, E9-E24 unchanged since R5 (confirm from the diff).

## Output (your final message; it will be saved as `PRE_LEAN_PASS/MEAS-D/R6_council_opus.md`)
1. A per-item table `| # | ACCEPT/REJECT | note |` for items 1-4, with file:line.
2. The verdict lines of items 1 and 2 exactly as given.
3. Findings tagged C / S / F / E with file:line and the exact correction, each classified WORDING, QUALIFIER or GENUINE GAP as above ("apply as written" where you give text).
4. Gates, each PASS or FAIL: G1 correctness, G3 faithfulness and scope, G4 statuses and pins, G5 registration form. `gates=FAIL` if you hold any C, S or F that is not purely WORDING/QUALIFIER (if your only findings are wording you may still write gates=PASS, saying that applying them as written is the only condition).
5. A score (0.0-10.0, one decimal) on C, S, F only.
6. The claim table: `| id | decision |` then `| W3-SAMP:MEAS-D | ACCEPT |` or `REJECT`.
7. The last line, alone and the only line containing the keyword:
`COUNCIL-VERDICT round=R6 manifest=87dfd9f8258f978affc44879ac3ae01633ff9e481ed65406161091af781c5296 seat=opus score=<x.y> gates=<PASS|FAIL>`
