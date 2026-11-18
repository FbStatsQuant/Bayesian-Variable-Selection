# READER editorial round: brief (HQ GO 2026-11-17 night; token-lean)

**Role.** You are the Sonnet editor, on claudeAgent_personal. You make **editorial edits only** to the READER files: `Theory_work/Wave3/W3-READER/` (CLAIMS_CARD.md, READER_VERSIONS.md, NOTATION.md, REPORT.md as needed). You change no theorem and no claim's mathematics. Branch: `theory/W3-READER-ED`, created from **origin/main** (main is authoritative; the recorder has requoted the card there). Never push to main, and never edit registry files.

## Items (sources: `Theory_work/Dept/QUEUE.md` on origin/dept/theory, lines ~52–66, and DECISIONS D115/D120/D121)
1. **H5 card 17 text.** This is the joint card swap the consultant AGREED with changes (D120, D121):
   - row 1.2: Thm2X coexists, tag **MIXED/incomparable**, and **Thm2SG becomes the presented Theorem 2** (class-1 anchor NH14 only; SL Cond 1 is a factual remark);
   - row 3.1L for Cor 6L, with clauses (a)/(b)/(c) per `Theory_work/Dept/H5_CARD_PUSH_2026-11-17.md`. The 6L ↔ Cor 9C wording is "pathwise; the probability form needs the raw-scale bridge (open)" (D121). **Cor 6L is not yet recorded** (W3-D5P waits for IMPL-LIST), so mark its row **"pending recording"**, and do not present it as a software statement.
   - **Cor-FAMC reader line** (recorded 8b4d3101). Use the faithfulness-checked 4-line text in `Theory_work/Dept/writing_answers/FAMC_NOTE_2026-11-17.md` on dept/theory. Do not paraphrase it.
   - **This card text goes to the manager first.** HQ takes it to the consultant. Do not apply the card swap to the files until the manager confirms.
2. **R4 premise pointer.** W3-READER:R4's pointer (:28-32) is stale after the v1.13 re-anchor (R4 kept @1.0.1).
3. **R5's 3 minor editorial items.** See `Theory_work/Wave3/W3-READER/reviews/R5_council_opus.md`.
4. **Card 15 B batch** (QUEUE line 60):
   - (1) rows 3.1/3.2: say which clause C-DLV:L2-S3 / P1-Inventory attach to;
   - (2) GUARD-W wording;
   - (3) compress row 3.1's integer-limit passage to one sentence, only if T14 is recorded. Check the registry; if T14 isn't recorded, skip this.
5. **Post-freeze editorial** (QUEUE line 63): Opus R3's 2 wording items, and the [AUD-S4] SL sampler-output sentence, using the **v1.4** wording from WRITING_DELTA_v1.4.
6. **Stale narrative bullets:** anything in the card or reader text that no longer matches main's registry statuses after today's landings (W3-D2/D3, V, MF, FAMC, RM2: Ex-PolyR/BC/IR now PC). List each one with file:line.
7. **W3-RM2-R READER_DELTA:** the F-UNI cap sentence still carries the error that READER corrected as R1-F6. This is editorial. If the file belongs to W3-RM2-R and isn't a READER file, list it for the manager instead of editing it.

## Process
- **Inventory first.** Make a table: item | file:line | current text | proposed text | kind (editorial / statement-substance). Send it to the manager.
- **Anything that changes a statement's wording in substance** needs one Sol 6.2 check. Ask the manager first, and run the ingest converter locally before that check. Editorial items need no Sol check.
- **Apply the edits.** Then run the READER citecheck and the ingest converter, and freeze the next READER manifest with manifest.py v2 (no registry files or live logs).
- **At the end, one Opus faithfulness check** of the whole diff against the registry and the sources. Run it on a fresh subagent, explicitly on claudeAgent_personal, Opus at high.
- **Report to the manager** in 10 lines or fewer at each step. The recorder's dry run then goes to HQ before LAND=yes.

## Budget
Token-lean. Sonnet does the edits; spend Opus only on the final faithfulness check. Use no Fable, and no other subagents unless they are mechanical. Every subagent must be explicitly on claudeAgent_personal.
