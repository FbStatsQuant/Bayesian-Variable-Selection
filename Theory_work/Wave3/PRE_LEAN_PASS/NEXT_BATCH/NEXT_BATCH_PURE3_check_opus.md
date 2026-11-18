PURE check, round 3: both patches are PURE, and the 39-patch stack applies at -F0 with 0 failures.

**Snapshot.** HEAD 2e553f50, and the working tree stayed clean. All scratch work is in `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-215eb534-a080473e9c42fff9/.rc_tmp/nbpure3_r3/`. I changed no tracked file, committed nothing and started no subagent.

**Method.** I used round 2's method.
- **Mechanics:** `mk.sh` runs `patch -p1 -F0` and counts any offset, fuzz or reject as a failure. I checked each `index` line with `git hash-object`.
- **Character diff:** `cdiff.py`.
- **Text match:** `tmatch3.py` applies the addendum's strings to the predecessor state and compares the result with the patched file.
- **Registry effect:** `hashes3.py` runs `bvsreg.claim_hash` with a synthetic MEAS-D row taken from the planned block (`STATEMENT.md:190-192 | premises STATEMENT.md:20-60`). On BASE it reproduces all 66 `claims.tsv` sha256 values that touch the patched files.
- **Sources:** the addendum is `origin/dept/theory:Theory_work/Dept/pre_lean_cards/T9_addendum.md` at c0be15d8, rider 4 (:27-37). It is byte-identical to the copy round 2 used. MEASD4's `STATEMENT.md` is taken from bb94ba61; its sha256 266d0109… matches `MANIFEST_MEASD4.txt`.

---

**NB-C1v2: PURE**
1. **Mechanics.**
   - It applies at -F0 on `MEAS-D_stage_wo_NB-C1.patch`, and the `index` line 9a0d86f2..dc97dca6 matches exactly. The file stays at 192 lines.
   - On the full `MEAS-D_stage.patch`, `patch` reports "Reversed (or previously applied) patch detected", so the "do NOT apply both" rule is enforced mechanically. On BASE alone it fails, as expected.
2. **Byte identity.** wo_NB-C1 + NB-C1v2 + NB-C1r gives a `W3-SAMP/STATEMENT.md` that is `cmp`-identical to two other copies:
   - the one the full `MEAS-D_stage.patch` gives;
   - the real ticket's `MEAS-D/ticket/Theory_work/Wave3/W3-SAMP/STATEMENT.md`.

   Its sha256 is 9f2119a0…, the value `MANIFEST_MEASD5.txt` (968cd72a…) pins. REPORT.md (7ef54ea2…) and `lemmas/MEAS_D.md` (c26d3c9c…) also match the manifest. Otherwise the two stage patches differ only in the `STATEMENT.md` index line, the :36 + line, the final hunk header (+9 vs +11) and the two remark lines.
3. **Character diff.** The only change is an insertion at col 233 of :36, right after "…Lemma MEAS-D (§4, `lemmas/MEAS_D.md`).". It inserts " By erratum E1 (…), 𝒜 and 𝓒 are read throughout as the potential pair (𝒜°, 𝓒°) … (GW-iv, `W3-AUDIT-A:CAL-C`)." No other line changes.
4. **Text match.**
   - The result equals the addendum's theorem-side sentence (rider 4, :33): script True.
   - There is no clock clause. The regex `clock|outer` (case-insensitive) finds nothing in the sentence or anywhere on :36.
   - The text is byte-identical to round 2's :36, so round 2's truth assessment carries over unchanged.
5. **Spans.**
   - Inside the premises span :20-60, only :36 changes, and that is the intended insertion.
   - Nothing in :190-192 changes because of this patch.
   - MEASD4 → wo_NB-C1 changes only :190. That is the F6(b) qualifier: "every bounded h of §2" becomes "every h of §2 whose bound B_h does not depend on the data" (col 711 deletes "bounded ", col 726 inserts the clause). It belongs to MEAS-D, not to these patches.
   - MEASD4 and wo_NB-C1 are identical on :20-60.
6. **Registry effect.**
   - :36 lies inside the premises span 20-60 of exactly 8 `claims.tsv` rows: `W3-SAMP:` PC, MR, ST, D, LT#, LT#(f), C and TR. It also lies in the synthetic MEAS-D row's premises.
   - From wo_NB-C1 to wo + NB-C1v2, 9 hashes change: those 8 plus the synthetic MEAS-D row (6b3acbd6 → 1b1f411f).
   - From BASE to wo_NB-C1, the same 8 change, plus MEAS-D's row coming into existence. So these are the 8 that MEAS-D already rehashes.
   - `W3-SAMP:CC` (premises :38-51) is untouched.
   - No other row moves.

**NB-C1r: PURE**
1. **Mechanics.**
   - It applies at -F0 on wo_NB-C1 + NB-C1v2, and the `index` line dc97dca6..44b553c2 matches exactly.
   - The file goes from 192 to 194 lines. :193 is blank and :194 is the remark; no earlier line shifts.
   - It also applies at -F0 on wo_NB-C1 alone, because its context is :190-192. The declared stacking is stronger than needed, which does no harm.
   - Its context is the F6(b) version of :190, so it is correctly rebuilt on MEASD5.
2. **Byte identity.** See NB-C1v2, item 2: the combined result `cmp`-matches both the full stage and the ticket.
3. **Character diff.** The only additions are the blank :193 and :194, "*Remark (actual runs; not part of any claim).* The guard's clock is not modelled … corresponding potential event." Nothing else changes.
4. **Text match.** wo + NB-C1v2, plus a blank line and the addendum's remark (rider 4, :37), equals the patched file (script True). :193 is blank, :194 is the remark, and the file ends there. The text is byte-identical to round 2's :193-194.
5. **Spans.** Nothing in :190-192 or :20-60 changes. In the span inventory, :193 and :194 lie inside no statement span and no premises span:
   - not in any `claims.tsv` row (the largest W3-SAMP statement span ends at :177);
   - not in MEAS-D's planned 190-192 / 20-60.
6. **Registry effect.** From wo + NB-C1v2 to wo + NB-C1v2 + NB-C1r, 0 hashes change, synthetic MEAS-D row included.

**39-patch stack: 39/39 at -F0, 0 failures, no offset or fuzz.**
- **Order:** the 28 BATCH_READY_v2 files (T8-SA2 included), then `MEAS-D/MEAS-D_stage.patch`, then NB-C2, C3, C4, C4r, C5log, C6err, INT, T10-1, T10-2, F3.
- **Files:** every file the stack touches is in the scratch file list.
- **Output:** the resulting `W3-SAMP/STATEMENT.md` is `cmp`-identical to the ticket's.
- **Line counts:**
  - ERRATA 9 → 11
  - W3-SAMP STATEMENT 186 → 194
  - REPORT 194 → 206
  - W3-DIST 499 → 500
  - `MEAS_D.md` new, at 96 lines
- **Hashes:** 33 `claims.tsv` hashes change, plus the synthetic MEAS-D row. That is the same set as round 2's 41-patch stack.
- **Agreement with round 2:** only the three W3-SAMP files differ from round 2's full tree, which is expected, since MEASD5 differs from the stage round 2 used.

**Note on `NEXT_BATCH.md` (outside the two patches under test).** Its header line 3 still says "the 12 patches below, **41 patches in the order below, 0 failures**". With the fold-in, that 41-patch order no longer applies: NB-C1v2 is refused on top of `MEAS-D_stage.patch` as already applied.
- **Suggested correction:** "the BATCH_READY_v2 patches (T8-SA2 included), `MEAS-D/MEAS-D_stage.patch` (MEASD5, NB-C1v2/NB-C1r folded in), and the 10 other patches below, **39 patches, 0 failures** (PURE round 3)".
- This does not affect either patch's verdict.

PURE-VERDICT: ALL PURE
