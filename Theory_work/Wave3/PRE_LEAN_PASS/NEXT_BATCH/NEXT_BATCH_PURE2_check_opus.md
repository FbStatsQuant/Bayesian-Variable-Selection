PURE check, round 2, of the NEXT_BATCH patches (fresh Opus seat). Three of the six patches under test are PURE: NB-C1v2, NB-C1r and NB-F3. Three are NOT-PURE: NB-C4r, NB-C5log and NB-C6err. In all three the inserted text is right; the errors are in the header or the `NEXT_BATCH.md` table. The corrected headers of NB-C3 and NB-C4 are now right, and the full 41-patch stack applies at -F0 with 0 failures.

**Snapshot.** HEAD moved from 56811bb1 to ff688c92 while I worked. The only changes there that touch this brief are the first (`#`) line of NB-F3's header and NB-F3's row in `NEXT_BATCH.md` ("Kept, not droppable"). I rebuilt the NB-F3 tree and the full stack at ff688c92, and both came out byte-identical to the earlier runs.

**Method.** All work is in `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-215eb534-a080473e9c42fff9/.rc_tmp/nbpure2_r2/`. No tracked file was changed, nothing was committed and no subagent was started.
- **Mechanics:** `patch -p1 -F0`; any fuzz, offset or reject counts as a failure. Each patch's `index` line was checked with `git hash-object` on the pre- and post-images.
- **Character diff:** `cdiff.py`, line by line and then character by character.
- **Text match:** `tmatch.py` applies the addendum's strings (and the card's, for NB-C3 and NB-F3) to the predecessor state and compares the result with the patched file.
- **Registry effect:** `hashes.py` runs `bvsreg.claim_hash` over the 66 rows of `claims.tsv` that touch any patched file. On BASE it reproduces all 66 `sha256` values.
- **Sources:** "Addendum" means `origin/dept/theory:Theory_work/Dept/pre_lean_cards/T9_addendum.md` (c0be15d8), rider 4.

---

**NB-C1v2: PURE**
1. **Mechanics.** It applies at -F0 on `MEAS-D_stage.patch`, and fails without it (checked). The `index` line 95351f2b..19dfad9b matches exactly. Only `W3-SAMP/STATEMENT.md:36` changes, and the file stays at 192 lines.
2. **Character diff.** A pure insertion at col 233 of :36, right after "…`lemmas/MEAS_D.md`).". It inserts " By erratum E1 (…), 𝒜 and 𝓒 are read throughout as the potential pair … (GW-iv, `W3-AUDIT-A:CAL-C`)."
3. **Text match.** Equal to the addendum's theorem-side sentence (script True). It deliberately differs from card v2 §B.1, which still carries the clock clause; the addendum supersedes that.
4. **Truth: true.**
   - No clock clause (the regex `clock|outer` finds nothing in the inserted text).
   - GW-iii (`W3-AUDIT/track_A/T1_GW/STATEMENT.md:80-83`): on 𝒪 the fields of 𝓒 equal P°'s.
   - GW-iv (:85-91): 𝒪 ∩ A ⊆ 𝒪° ∩ A°, and 𝒜 = 𝒜° ∩ G ⊆ 𝒜°.
   - No new hypothesis.
   - Round 1's note still applies: for the actual 𝒜, the inclusion that does the work is 𝒜 ⊆ 𝒜° (:87), and the cited GW-iv contains it.
5. **Registry effect.**
   - Eight hashes change: `W3-SAMP:` PC, MR, ST, D, LT#, LT#(f), C and TR. These are the same 8 that MEAS-D already changes, and nothing else. This matches the header and the table.
   - **Recorder note 1 (not an error against `claims.tsv`).** MEAS-D's planned registry block (`MEAS-D/ticket/.../REPORT.md:200`) has premises `STATEMENT.md:20-60`, and :36 lies inside it. A synthetic MEAS-D row's hash changes under NB-C1v2 (8e253bb9 → 0766f78a). If NB-C1v2 lands after MEAS-D is recorded, 9 claims are rehashed, not 8.
   - **Recorder note 2.** `MANIFEST_MEASD3.txt` (a08a238a) pins `W3-SAMP/STATEMENT.md` at sha256 a2e0ee76…. NB-C1v2 makes it 3a23a84b…. So landing "WITH MEAS-D" means re-freezing MEASD3.

**NB-C1r: PURE**
1. **Mechanics.** It applies at -F0 on MEAS-D stage + NB-C1v2. The `index` line 19dfad9b..ca7f1b88 matches exactly. The file goes from 192 to 194 lines: a blank :193 and the remark at :194, at end of file, with no earlier line shifted.
   - It also applies without NB-C1v2, because its context is :190-192. The declared stacking is stronger than needed, which does no harm.
   - Forward note: the MEAS-D R3 review (d33f220d) asks for E13, an edit at `STATEMENT.md:190`. If the stage patch is re-issued with E13, this patch's context breaks and it must be rebuilt.
2. **Character diff.** The two added lines are exactly a blank line and "*Remark (actual runs; not part of any claim).* … corresponding potential event.". Nothing else changes.
3. **Text match.** Equal to the addendum's remark sentence (script True).
4. **Truth: true.**
   - It says "not part of any claim", and :193-194 lie outside every claim span, including MEAS-D's planned 190-192 and premises 20-60.
   - The clock clause is GW "Not claimed" (`T1_GW/STATEMENT.md:99-101`).
   - Note for the Fable: "intersected with the actual 𝒜" is true here because on 𝒜 W3-SAMP's events concern potential quantities (`STATEMENT.md:33-34`) or the calibration-time state (CAL-d). `T5_CAL/STATEMENT.md:51-52` says that actual final-run events transfer only on 𝒪.
5. **Registry effect.** No hash changes; this matches the header and the table. It does change the MEASD3-pinned file digest (to e0ce4a56…), so the same re-freeze note applies as for NB-C1v2.

**NB-C4r: NOT-PURE (header registry statement; the text is PURE)**
1. **Mechanics.** It applies at -F0 on BASE, independently of the other patches; NB-C5log, NB-C4r and NB-C4 in any order also apply cleanly. The `index` line b8f3015d..5e7c4eb3 matches. Only `READER_VERSIONS.md:1322` changes, and the file stays at 1458 lines.
2. **Character diff.** Insertion at col 336 of :1322, after "[GUARD-W]", of " *Remark (the time guard).* … for the uninterrupted run."
3. **Text match.** Equal to the addendum's reader remark (script True).
4. **Truth: true.**
   - GW-iii (:80) supports "a completed run coincides with the uninterrupted one".
   - The outer-probability reading and the bound are GW :99-101. On 𝒜 the estimates come from the uninterrupted records (:1303-1304), so the bound also holds through 𝒜 ⊆ 𝒜°.
   - :1322 is outside every claim span; no row has `READER_VERSIONS.md` as its claim file.
5. **Registry effect: misstated.** :1322 lies inside `W3-READER:R1`'s premise span 1283-1388, and the R1 hash changes. The header says "prose, no registry span", which is wrong. The table row ("R1 span 1283-1388 (same R1 bump)") is right.
6. **Minimal correction.** In the header, replace "prose, no registry span" with "inside `W3-READER:R1`'s premise span READER_VERSIONS.md:1283-1388: R1 rehash, same R1 bump as NB-C4, NB-C5log and BATCH_READY_v2".

**NB-C5log: NOT-PURE (header registry statement, and the table's dependency column; the text is PURE)**
1. **Mechanics.** It applies at -F0 independently. The `index` line b8f3015d..54ce6b5b matches. Only :1387 changes, and the file stays at 1458 lines.
2. **Character diff.** Insertion at col 298 of :1387, at the end of the last bullet of "#### Update log (thm10)" (:1360), before `<!-- ROW thm10 END -->` (:1388). It inserts " PL-T9 2026-11-18: [E1-TEXT] … CORRECTION-ONLY (EQUAL)."
3. **Text match.** It is equal to the addendum's log line with two differences, neither stated in the header:
   - The addendum's "- " bullet marker is dropped, as the addendum's own line-stability note says to do.
   - The inner quotes 'in the run taken as if uninterrupted' become double quotes. This is the un-nesting of the addendum's quotation, and it matches the double quotes already used on :1387.

   The script confirms equality once those two differences are applied, and gives False verbatim. I count this as a rendering difference and report it; no change is needed.
4. **Truth: true.**
   - It describes only NB-C4 ("in Theorem 10's preamble", :1301-1302) and NB-C4r ("added to the row 3.5 remark", :1322).
   - §11 stays at :1412, and no line count changes.
5. **Registry effect: misstated.** :1387 is inside R1's span 1283-1388, and the R1 hash changes. The header says "Prose; no registry span", which is wrong. The table is right.
6. **Minimal correction.**
   - In the header, replace "Prose; no registry span." with "Inside `W3-READER:R1`'s premise span READER_VERSIONS.md:1283-1388 (R1 rehash, same R1 bump)."
   - In the table's "apply after" column, change "none" to "NB-C4, NB-C4r (describes them; lines independent)". This agrees with the header's own "Depends on NB-C4 and NB-C4r".

**NB-C6err: NOT-PURE (landing dependency; the text is PURE)**
1. **Mechanics.** It applies at -F0. The `index` line e17a5895..b6786664 matches. `ERRATA_W3-SAMP.md` goes from 9 to 11 lines, appended at the end: a blank :10 and the paragraph at :11, under E1, the file's only section.
2. **Character diff.** The only additions are the blank line and "Applied to text 2026-11-18 (…): … E1's substance is unchanged."
3. **Text match.** Equal to the addendum's errata line (script True).
4. **Truth: true once its six patches are in.** The files are exactly the four touched by NB-C1v2, NB-C1r, NB-C2, NB-C3, NB-C4 and NB-C4r.
   - The line ranges are the spans of the aligned sentences: R4 :17-18, READER STATEMENT :15-16 and READER_VERSIONS :1301-1302. The bytes actually change only on :18, :16 and :1302, and the ranges are the card's own pins.
   - NB-C1r is given only as "after §4". It is in fact §4's last paragraph, at :194.
   - **The error:** the table says "apply after: none". If NB-C6err landed before NB-C1v2 and NB-C1r, which are held for MEAS-D, then "`W3-SAMP/STATEMENT.md:36` now states the potential-pair reading" would be false.
5. **Registry effect.** No hash changes, and no MANIFEST lists the errata file (`git grep`). This matches the header and the table.
6. **Minimal correction.**
   - Header: add "Describes NB-C1v2 and NB-C1r (held for MEAS-D): lands with or after them, with NB-C2, NB-C3, NB-C4, NB-C4r."
   - Table "apply after" column: "NB-C1v2, NB-C1r, NB-C2, NB-C3, NB-C4, NB-C4r (describes them). **Lands with or after MEAS-D.**"
   - Add NB-C6err to the "lands WITH or AFTER MEAS-D" landing rule.

**NB-F3 (rebuilt): PURE**
1. **Mechanics.** It applies at -F0 on Sol2-S2-2 + NB-T10-1 + NB-T10-2. It fails without NB-T10-1/NB-T10-2 and fails without S2-2 (both checked). The `index` line 762e1a50..4bedd9eb matches. Only `CLAIMS_CARD.md:76` and :97 change, and the file stays at 181 lines.
   - Its −/+ lines are identical to round 1's rebuild; only the header and the hunk-header trailing text differ.
2. **Character diff.**
   - :76: "the printed evidence" becomes "$\exp$ of the printed field `log_Z` (not `log_Z_list`, row 3.1L)".
   - :97: "the printed evidence" becomes "$\exp$(`log_Z`), the printed pooled evidence,".
3. **Text match.** Equal to the card's row F3 (§C) (script True).
4. **Truth: true.** `Scripts/SMC_BVS/core/v3_run.R:154` (also at 4676af6) sets `out$log_Z <- v3_log_sum_exp(logZr) - log(R)`, so exp(log_Z) = Ẑ. `log_Z_list` is the 3.1L field (:236).
5. **Registry effect.** None (no hash changes), which matches the header and the table. In the full stack, :76, :78 and :97 equal this tree.

**Corrected headers of NB-C3 and NB-C4: correct.**
- NB-C3: "inside `W3-READER:R4`'s registered span 1-48; premises :25-29 untouched; … rehashes R4". The hash check shows exactly R4 changing.
- NB-C4: "Inside `W3-READER:R1`'s premise span 1283-1388: R1 rehash/bump". The hash check shows exactly R1 changing.
- Both table rows agree. Their text is unchanged from round 1 (character diffs: :18 col 53 and :1302 col 36), and still matches the card.

**Full 41-patch stack: 41/41 at -F0, 0 failures, no offset or fuzz**, re-run at ff688c92. The order is the 28 BATCH_READY_v2 files (T8-SA2 included), then `MEAS-D_stage.patch`, then the 12 NB patches in table order.
- **Line counts:** ERRATA 9 → 11 and W3-SAMP STATEMENT 186 → 194 (MEAS-D +6, NB-C1r +2). The rest are as in round 1: W3-DIST 499 → 500, REPORT 194 → 206, MEAS_D.md new at 96 lines.
- **Hashes:** 33 change, and the NB share is exactly the table's summary: PoolZ (C2, INT), R4 (C3), R1 (C4, C4r, C5log), and the 8 W3-SAMP claims (C1v2). Not hashed: C1r, C6err, T10-*, F3.

PURE-VERDICT: NOT PURE: NB-C4r, NB-C5log, NB-C6err
