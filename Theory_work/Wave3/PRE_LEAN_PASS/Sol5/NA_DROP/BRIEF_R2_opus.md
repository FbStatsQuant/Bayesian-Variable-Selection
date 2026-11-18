# BRIEF: Opus diff seat on NA_DROP v1.2 -> v1.3 (round R2; one fresh seat, claudeAgent_personal, effort high)

You are a fresh seat; you did not see the Opus statement-change check on v1.2 (`W3-D5P/reviews/post_cp3/NA_DROP/NA_check_opus.md`) or the Sol 6.2 read (`Sol5/NA_DROP_council_sol_R1.md`, 8.6, gates FAIL, points b-1 to b-4). Be skeptical. **Scratch only under `<worktree>/.rc_tmp/`; nothing in /tmp or /tmp/claude-*; no `git worktree add` there.** Change no tracked file, commit nothing, start no subagents; your final message is the review.

**Scope: v1.2 -> v1.3 only.** v1.2 (the prepared NA_DROP statement change: clause (o) "every output run prints pip_list, mpm_list and a finite log_Z_list"; exact-branch row read as "from fit$exact$top"; qualifiers dropped) is manifest `Sol5/NA_DROP/MANIFEST_NADROP_v1.2.txt` (first line `MANIFEST 2443df8545d11cf93ab49f591306122bbfa85cdacfcb0fffcf413c8bda24501d`, ticket `Sol5/NA_DROP/v1.2_ticket`). v1.3 = the four Sol points applied: `Sol5/NA_DROP/MANIFEST_NADROP13.txt`, first line `MANIFEST 8fb12543d716f3878e0a23fbd3e36072bc27b59dcf602f1d4918c21e5c067eee` (ticket `Sol5/NA_DROP/ticket`, 5 staged files + 32 external inputs: the core files at method-v3.1.1-listpip etc.). First run `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/PRE_LEAN_PASS/Sol5/NA_DROP/ticket Theory_work/Wave3/PRE_LEAN_PASS/Sol5/NA_DROP/MANIFEST_NADROP13.txt` and report its output (it must print `verify: OK MANIFEST 8fb12543d716f3878e0a23fbd3e36072bc27b59dcf602f1d4918c21e5c067eee`). The diff: `Sol5/NA_DROP/NADROP_v1.2_to_v1.3.diff`; the claimed-edit grep: `Sol5/NA_DROP/NADROP13_CLAIMED_EDITS_GREP.txt`. The staged files are under `Sol5/NA_DROP/ticket/Theory_work/Wave3/W3-D5P/`: `STATEMENT.md` (168 lines), `lemmas/L3_listR.md` (129), `REPORT.md` (72), `CARD.md` (23), `READER_DELTA.md` (45).

## Edits this brief claims, grepped in the REAL staged files before freezing (HQ rule; all present)
    OK   ticket/.../W3-D5P/lemmas/L3_listR.md:36  b-1 (0.5) lists the three stop() rows with reasons
    OK   ticket/.../W3-D5P/lemmas/L3_listR.md:41  b-1 (0.5) count mismatch reason (:251)
    OK   ticket/.../W3-D5P/lemmas/L3_listR.md:41  b-1 (0.5) duplicate row (:253)
    OK   ticket/.../W3-D5P/lemmas/L3_listR.md:42  b-1 (0.5) out-of-set column reason (:263)
    OK   ticket/.../W3-D5P/lemmas/L3_listR.md:37  b-1 (0.5) byte-identical at 61b0a582 and the tag
    OK   ticket/.../W3-D5P/lemmas/L3_listR.md:54  b-1 Step 0' row list
    OK   ticket/.../W3-D5P/lemmas/L3_listR.md:0  b-1 ABSENT: 'only through SPEC §4's duplicate-model row'
    OK   ticket/.../W3-D5P/CARD.md:10  b-2 CARD row 3.1L: p>=2 on the rate
    OK   ticket/.../W3-D5P/CARD.md:13  b-2 CARD Option B: p>=2 for the rate
    OK   ticket/.../W3-D5P/READER_DELTA.md:30  b-2 READER_DELTA: p>=2 on the rate
    OK   ticket/.../W3-D5P/CARD.md:10  b-3 CARD: IMPL-LIST discharged
    OK   ticket/.../W3-D5P/CARD.md:0  b-3 ABSENT (CARD): 'until Engineering's method commit is code-read'
    OK   ticket/.../W3-D5P/REPORT.md:19,64  b-3 REPORT status (LIST-R table row and REGISTRY status line)
    OK   ticket/.../W3-D5P/REPORT.md:0  b-3 ABSENT (REPORT): 'conditional on IMPL-LIST'
    OK   ticket/.../W3-D5P/REPORT.md:0  b-3 ABSENT (REPORT): 'method commit pending'
    OK   ticket/.../W3-D5P/REPORT.md:66  b-4 REPORT conclusion: (o) its own clause, finite log_Z_list
    OK   ticket/.../W3-D5P/REPORT.md:0  b-4 ABSENT: 'log_Z_list is never NA on an output run' inside the data-event sentence
    OK   ticket/.../W3-D5P/STATEMENT.md:168  changelog row v1.3 (outside every claim span)
    OK   ticket/.../W3-D5P/STATEMENT.md:1  header v1.3
    

    file sha256 (first 16) and line counts:
    STATEMENT.md: c968e0715f97303f lines=168
    lemmas/L3_listR.md: e81a564b5de1bcd9 lines=129
    REPORT.md: a649e9a2eda86981 lines=72
    CARD.md: 46be38145525e830 lines=23
    READER_DELTA.md: a3fd959d97c48c7f lines=45
    RESULT: ALL CLAIMED EDITS PRESENT

(If a claimed edit is not where this table says, or the verify digest differs, write gates=FAIL and say so.)

## What to check (every item one line)
1. **b-1 (mandatory).** L3 (0.5) now says the new computation can end the fit with an error only through the three `stop()` rows of `v3_list_fields` (`v3_run.R:251` count mismatch, `:253` duplicate model, `:263` column outside the retained set) and gives each a reason why it cannot fire on an output run. Verify each reason against the code of record: (i) `store_to_list` (`cpp/v3_core.cpp:358-362`; callers `:366` for the sampler store and `:565` for the exact store) builds the model list and value vector in one pass over the same set, so length(F) = m; (ii) distinctness (L2 (iii), (iv)); (iii) `to_orig` (`cpp/v3_core.cpp:38-42`) gives original indices of retained columns and `orig` passed to `v3_list_fields` is that same vector (`ctx$orig` from `pre$kept`, `v3_fit.R:118, 176`; `v3_run.R:160, 220`). Check the claim "these three lines are byte-identical at the core tree 61b0a582 and at method-v3.1.1-listpip (7100bb3b)": `git show 61b0a582:v3_run.R | sed -n '251p;253p;263p'` against `git show 7100bb3b:Scripts/SMC_BVS/core/v3_run.R | sed -n '251p;253p;263p'` and the working tree (the coordinator got the same sha256 prefix 8af9f9b7653c0ef0 for all three). Are there any other `stop()` or error paths in `v3_list_fields`, `v3_add_list_fields` or the two call sites (`v3_fit.R:176`, `v3_run.R:220`) that (0.5) now misses? Does the Step 0′ list of NA rows (line :54) remain complete? Verdict: `(b-1) (0.5) COMPLETE AND CORRECT | <missing row or wrong reason, file:line>`.
2. **b-2:** the eventual p ≥ 2 qualifier restored on the rate in CARD (row 3.1L and Option B) and READER_DELTA, equal to STATEMENT (C3)(ii) "Rate (p ≥ 2 for all large n)". **b-3:** IMPL-LIST presented as discharged at method-v3.1.1-listpip (7100bb3b) in CARD and REPORT (all places: REPORT :9, :19, :26, :64, :70), with the v1.2/v1.3 statement-change review status kept separate (no claim that v1.3 is reviewed). **b-4:** the REPORT registry conclusion has (o) as its own clause covering all three fields and a finite log_Z_list on every admissible output run, and the data-event sentence no longer carries the non-NA statement. One line each ACCEPT/REJECT.
3. **What the fixes introduce:** line pointers in REPORT (statement spans :100-128, premises :29-64: did the +1 changelog row in STATEMENT or the 7 added lines in L3 shift any pointer?), the changelog row v1.3 (tag EQUAL: proof completion and derived-text corrections, no statement change: is that right?), the `ingest.py convert` result (the coordinator got exit 0, 3 records), `[NA-b1]`/`[NA-b4]` markers, any statement of (o) or of the rate that is now inconsistent across STATEMENT, L3, REPORT, CARD, READER_DELTA. Does clause (o) still hold and is Step 0′ still proved?
4. **Classification (HQ rule):** for every finding say WORDING (give exact replacement text, "apply as written"), QUALIFIER, or GENUINE GAP (a step that does not hold). Say plainly at the top of your findings which kinds you hold.

## Output (final message; saved as `Sol5/NA_DROP_R2_council_opus.md`)
A per-item table `| # | ACCEPT/REJECT | note |` (file:line), the verdict line of item 1, findings tagged C / S / F / E with file:line and exact corrections and their classification, gates (G1 correctness, G3 faithfulness and scope, G4 statuses and pins, G5 registration form; each PASS or FAIL; `gates=PASS` allowed if your only findings are WORDING/QUALIFIER to be applied as written), a score (0.0-10.0) on C, S, F, and the last line, alone and the only line containing the keyword:
`COUNCIL-VERDICT round=R2 manifest=8fb12543d716f3878e0a23fbd3e36072bc27b59dcf602f1d4918c21e5c067eee seat=opus score=<x.y> gates=<PASS|FAIL>`
