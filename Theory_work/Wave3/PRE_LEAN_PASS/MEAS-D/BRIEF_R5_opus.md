# BRIEF R5: one fresh Opus seat (council round R5, diff round R4 -> R5) for the W3-SAMP lemma MEAS-D

You are the single seat for round R5 (Claude Opus 5.5, effort high, claudeAgent_personal; fresh: you did not see rounds R1-R4). Be skeptical. **Scratch only under `<worktree>/.rc_tmp/`; nothing in /tmp or /tmp/claude-*; no `git worktree add` there.** Write only your review as your final message (no files, change nothing, commit nothing, start no subagents).

**Scope: the R4 -> R5 diff.** Read `Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/R4_council_opus.md` (the R4 review: 8.7, gates FAIL on F6; E21-E24) and `R4_to_R5.diff` (63 lines) in the same folder. Also `H_CLAUSE_INVENTORY.md` and `R5_CLAIMED_EDITS_GREP.txt` (same folder).

## What is under review (frozen)
`Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/MANIFEST_MEASD5.txt`, first line `MANIFEST 968cd72a718ffe0d68d8e6fd364bcc200c855a7824ffbdfeefd657a6a0dd4f43` (ticket dir `Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/ticket`, 3 files, plus 21 external inputs: the 20 of R4 and `Theory_work/Wave1/W1-N1/STATEMENT.md` (E24)). First run `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/ticket Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/MANIFEST_MEASD5.txt` and report its output (it must print `verify: OK MANIFEST 968cd72a718ffe0d68d8e6fd364bcc200c855a7824ffbdfeefd657a6a0dd4f43`).
Files (under `.../ticket/Theory_work/Wave3/W3-SAMP/`): `lemmas/MEAS_D.md` (96 lines), `STATEMENT.md` (194 lines; claim statement :190-192), `REPORT.md` (REGISTRY :199-206).

## Edits this brief claims, grepped in the REAL ticket files before freezing (HQ rule; each with file:line; all present at freeze)
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:50  F6(a) bounded-h paragraph (R4 F6(a), R4_council_opus.md:58), Step 6
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:50  F6(a) H_r(h) is Borel
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:50  F6(a) MR weights expectation P(𝒜°) ≤ 1
    OK   ticket/.../W3-SAMP/STATEMENT.md:190  F6(b) qualifier, statement (claim span 190-192)
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:24  F6(b) qualifier, MEAS_D §1 copy of the statement
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:50  F6(b) qualifier, Step 6 first sentence
    OK   ticket/.../W3-SAMP/REPORT.md:203  F6(b) qualifier, REGISTRY conclusion
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:38  E21 exit-list sentence
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:37  E22 notation
    OK   ticket/.../W3-SAMP/lemmas/MEAS_D.md:37  E23 evaluation bound
    OK   ticket/.../W3-SAMP/STATEMENT.md:36  NB-C1v2 E1 theorem-side sentence (line 36)
    OK   ticket/.../W3-SAMP/STATEMENT.md:194  NB-C1r remark (new final paragraph)
    OK   MEASD5_EXT.txt:30  E24 W1-N1/STATEMENT.md pinned (EXT file)
    OK   MANIFEST_MEASD5.txt:46  E24 W1-N1/STATEMENT.md in the manifest
    OK   lemmas/MEAS_D.md:0  ABSENT: for every bounded h of §2
    OK   STATEMENT.md:0  ABSENT: for every bounded h of §2
    OK   REPORT.md:0  ABSENT: for every bounded h of section 2
    OK   lemmas/MEAS_D.md:0  ABSENT: u_κ
    

    file sha256 (first 16) and line counts:
    STATEMENT.md: 9f2119a092efb8c9 lines=194
    REPORT.md: 7ef54ea28fa2c4bf lines=206
    lemmas/MEAS_D.md: c26d3c9c1d344450 lines=96
    RESULT: ALL CLAIMED EDITS PRESENT

(If any claimed edit is not where this table says, or the verify digest differs, write gates=FAIL and say so.)

## What to check (every item gets a line)
1. **F6(a)** (Step 6, `MEAS_D.md:50`): the paragraph is R4's own correction text (`R4_council_opus.md:58`) with ONE added phrase in its first sentence (the F6(b) qualifier). Confirm that diff is the only difference (diff it yourself), that the paragraph is correct (|H_r(h)| <= B_h; H_r(h) Borel; the two integrability bounds with κ_n·B_h; (N1) integrates by Step 5's positive/negative split; (MR-a)-(MR-c) likewise, **their weights having expectation P(𝒜°) <= 1 by the same identities at h = 1**: check that last claim against `STATEMENT.md:107-116`), and adds no premise. Verdict: `(F6a) PROVED, NO NEW PREMISE | <problem and exact correction>`.
2. **F6(b)**: the same words "for every h of §2 whose bound B_h does not depend on the data" in the statement (`STATEMENT.md:190`), `MEAS_D.md:24`, Step 6 (`:50`) and the REGISTRY conclusion (`REPORT.md:203`); the qualifier narrows the h-clause (CORRECTION-ONLY + WEAKER) and is what N1's "deterministic bound" means. Check the inventory (`H_CLAUSE_INVENTORY.md`): is it right that no h used by a clause that MEAS-D serves has a data-dependent bound (read `STATEMENT.md:107-116`, `lemmas/MR_identities.md:25, 62`, `lemmas/LT_theorem.md:26, 37`, `lemmas/C_theorem.md:28, 47`)? Verdict: `(F6b) qualifier: CORRECT AND CONSISTENT | <problem>` and `(inventory): RIGHT | <h with a data-dependent bound, file:line>`.
3. **E21-E24 against R4's own findings** (`R4_council_opus.md` §3): E21 (`MEAS_D.md:38`: three-item list readable), E22 (`:37`: no u_κ), E23 (`:37`: the bound N_e[1 + (p + B + 2)(T + L + 4)] equals what R4 derived, with the cited lines `cpp/v3_engine.h:72, 113-192, 331, 345, 355`: check them), E24 (`W1-N1/STATEMENT.md` pinned, manifest verify). One line each ACCEPT/REJECT.
4. **NB-C1v2 and NB-C1r folded in (wording outside MEAS-D's span).** `STATEMENT.md:36` gained the E1 sentence and `STATEMENT.md:194` the remark (new final paragraph after :192). Confirm from `R4_to_R5.diff` that **nothing inside MEAS-D's claim span :190-192 moved except the F6(b) qualifier**, that §§0-3 differ from main only at :36, that the E1 sentence has no clock clause, that the remark says "not part of any claim", and that neither adds a premise or claim (GW-iii, GW-iv at `Theory_work/Wave3/W3-AUDIT/track_A/T1_GW/STATEMENT.md`). Verdict: `(NB-C1) outside the span, NO NEW PREMISE | <problem>`.
5. **Nothing else moved:** scope remains the potential objects only; the converter exits 0 on a scratch copy of the staged REPORT.md (under `.rc_tmp/`); no `|x|` bars in the block or the statement (the registry block uses `§`; check the converter accepts it); claim span `STATEMENT.md:190-192`; `depends_on` has 11 items without spaces; no new C/S/F from the R5 edits. If you find anything beyond wording, say so explicitly.

## Output (your final message; it will be saved as `PRE_LEAN_PASS/MEAS-D/R5_council_opus.md`)
1. A per-item table `| # | ACCEPT/REJECT | note |` for items 1-5, with file:line.
2. The verdict lines of items 1, 2 and 4 exactly as given.
3. Findings tagged C / S / F / E with file:line and the exact correction; say explicitly whether any finding is more than wording.
4. Gates, each PASS or FAIL: G1 correctness, G3 faithfulness and scope, G4 statuses and pins, G5 registration form. `gates=FAIL` if you hold any C, S or F.
5. A score (0.0-10.0, one decimal) on C, S, F only.
6. The claim table: `| id | decision |` then `| W3-SAMP:MEAS-D | ACCEPT |` or `REJECT`.
7. The last line, alone and the only line containing the keyword:
`COUNCIL-VERDICT round=R5 manifest=968cd72a718ffe0d68d8e6fd364bcc200c855a7824ffbdfeefd657a6a0dd4f43 seat=opus score=<x.y> gates=<PASS|FAIL>`
