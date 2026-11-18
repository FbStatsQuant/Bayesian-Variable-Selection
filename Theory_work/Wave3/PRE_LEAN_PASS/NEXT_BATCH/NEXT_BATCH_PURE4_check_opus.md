PURE check, round 4: MEASD7 (`951d5a66…`) against R6's findings

`python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/ticket Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/MANIFEST_MEASD7.txt` printed `verify: OK MANIFEST 951d5a66c04501d04e39614f6e260c526b8c234b8d9d01d9373cac624419ce5a` and exited 0. All scratch work is under `.rc_tmp/pure4_opus/`. I edited no tracked file, committed nothing and started no subagents. The working tree is clean.

**Baseline.** I took the MEASD6 ticket from `git show 736dea6f:…`. Its three sha256 values (`08c1ed7f…`, `a17058df…`, `8f0a2164…`) match `MANIFEST_MEASD6.txt`. The 21 `#EXTRA` lines and their EXT digests are the same in MEASD6 and MEASD7. The only difference in `MEASD7_EXT.txt` is its title line ("MANIFEST_MEASD7").

## Checks

**(1) Text match by script: PASS**

The script `.rc_tmp/pure4_opus/apply.py` takes every Old/New pair from `R6_council_opus.md` §3, the text between `## 3. Findings` and `## 4. Gates`. It applies each pair to MEASD6 and compares the result with MEASD7.

| edit | file:line (MEASD7) | Old in MEASD6 | Old in MEASD7 | New in MEASD7 |
|---|---|---|---|---|
| F8 | `STATEMENT.md:190` | 1 | 0 | 1 |
| F8 | `lemmas/MEAS_D.md:24` | 1 | 0 | 1 |
| F8 (REPORT form) | `REPORT.md:203` | 1 | 0 | 1 |
| C1 | `lemmas/MEAS_D.md:32` | 1 | 0 | 1 |
| E30 | `lemmas/MEAS_D.md:50` | 1 | 0 | 1 |
| E31 | `lemmas/MEAS_D.md:50` | 1 | 0 | 1 |

- **Nothing else changed.** For each of the three files, MEASD6 with R6's replacements equals MEASD7 byte for byte (True, True, True). `diff` of MEASD6 against MEASD7 changes only `STATEMENT.md` 190, `MEAS_D.md` 24, 32 and 50, and `REPORT.md` 203.
- **The diff file is faithful.** I regenerated it with `diff -u --label R6/… --label R7/…`, and the result is `cmp`-identical to `MEAS-D/R6_to_R7.diff` (51 lines).
- **Hunk count differs from the brief.** The brief asks for "six hunks". The diff has **5 hunks** (`STATEMENT.md @@ -187`, `REPORT.md @@ -200`, `MEAS_D.md @@ -21`, `@@ -29`, `@@ -47`), carrying 6 replacements. E30 and E31 share line 50, so they fall in one hunk. This is a counting slip in the brief; the content is exactly R6's edits and nothing else.
- **Claimed-edit grep.** Every OK row of `MEASD7_CLAIMED_EDITS_GREP.txt` is at its stated file:line (190, 24, 203, 32, 50, 50; inventory 21, 27, 27). Its hash prefixes and line counts are correct. It has no ABSENT row for C1's Old string. My script confirms that string occurs 0 times in MEASD7, so this is an omission in the grep file only.

**(2) E32: PASS**

The script `.rc_tmp/pure4_opus/e32.py` builds the expected file from the 736dea6f inventory. It inserts R6's row, with R6's `` \` `` escapes read as `` ` ``, after the `(C-iii) loss per stage` row, and applies R6's two Old/New replacements. The result equals the current `H_CLAUSE_INVENTORY.md` (True).

- The row is at `H_CLAUSE_INVENTORY.md:21`, and both replacements are at `:27`.
- Each Old string occurs once in the 736dea6f version and 0 times now.
- Nothing else in the file changed. The heading "**Result (MEASD6).**" is untouched, as R6 did not ask for a change there.

**(3) No premise added: PASS**

- **F8 only narrows.** At `STATEMENT.md:190` it inserts "(for Lemma MR, with h as in the preceding sentence)". The preceding sentence on the same line is the existing h-clause ("every h of §2 that is a Borel function of (data, S, c) with a bound B_h …"). The "Consequently" clause is therefore restricted to the class that Step 5 proves, which is CORRECTION-ONLY and WEAKER. The REPORT form at :203 points to "the preceding clause" in the same way.
- **C1 is proof text** at `MEAS_D.md:32`. It cites `W3-AUDIT-A:BLK` (BLK-c), and `W3-AUDIT-A:BLK@stmt` is already in `depends_on` (`REPORT.md:204`).
- **E30 and E31 are proof wording** at `MEAS_D.md:50`.
- **Claim span.** It is still `STATEMENT.md:190-192`, and only line 190 changed inside it.
- **Line counts.** 194 / 206 / 96, as required.
- **Converter.** `ingest.py convert` on a scratch copy of the staged `REPORT.md` exits 0. It gives 1 record, with lines [190, 192], status_source `lemmas/MEAS_D.md:3` and 12 `depends_on` items. No item contains a space.
- **No bars or "§".** The conclusion has no `|`, no `‖` and no `§`. `STATEMENT.md:188-194` has no bars. The block `REPORT.md:199-206` has 5 `|`, all of them field separators, and no `§`.

**(4) NEXT_BATCH: PASS**

- **Two routes give the ticket.** On HEAD's `W3-SAMP` files, `MEAS-D_stage_wo_NB-C1.patch` + NB-C1v2 + NB-C1r at `patch -p1 -F0` (rc 0 each) gives a `STATEMENT.md` that is `cmp`-identical to the ticket's. It is also identical to what `MEAS-D_stage.patch` gives alone (rc 0). `REPORT.md` and `MEAS_D.md` are identical to the ticket on both routes.
- **39-patch stack: 39/39 at -F0, 0 failures, no offset and no fuzz.** I applied it to a scratch copy of the 23 touched files, in this order:
  - the 28 BATCH_READY_v2 files (T8-SA2 included), in the order of `BATCH_READY_v2.md:6`;
  - then `MEAS-D_stage.patch`;
  - then NB-C2, C3, C4, C4r, C5log, C6err, INT, T10-1, T10-2, F3.
- **Stack result.** The resulting `W3-SAMP` `STATEMENT.md`, `REPORT.md` and `MEAS_D.md` are `cmp`-identical to the MEASD7 ticket. Line counts: ERRATA 11, STATEMENT 194, REPORT 206, W3-DIST 500, `MEAS_D.md` 96.
- **NB-C1r remark.** The remark line that NB-C1r adds `cmp`-matches `ticket/.../STATEMENT.md:194`. It contains R5's E27 correction verbatim: "that is, an event of the statistical state intersected with {completed}, or a potential or calibration-time event intersected with the actual 𝒜 (§0, :33-34),".
- **NB-C1r and NB-C1v2 were rebuilt, not rewritten.** Their +/- text lines are identical to the 736dea6f versions. Only the `index` lines and NB-C1r's context line :190 changed, which is the F8 version.
- **NB-C6err is unchanged in text.** It does not change from 736dea6f to a2e3a9f1 (empty diff). Its +/- body is also identical to the PURE round 3 version (`ba95b56c`); at 736dea6f only its header comment and `index` line changed.

**(5) Errata date: PASS**

`Theory_work/Wave3/ERRATA_W3-SAMP.md:3` reads "… HQ GO real run (task W2, W1-N1:B/F discharge, track A_W, 2026-11-17))". The file was created in `20d01e52`, which is dated 2026-11-17 15:25 -0600. It does not change from 736dea6f to a2e3a9f1.

## Notes (no correction needed for purity)

- The brief's "six hunks" in (1) should read "5 hunks (6 replacements; E30 and E31 share `MEAS_D.md:50`)".
- `MEASD7_CLAIMED_EDITS_GREP.txt` could add an ABSENT row for C1's Old string, "and d(S) are continuous, and so are the finite sums Z, Z̄₀ and the ratios π, π₀.". Its absence is confirmed by script.

PURE-VERDICT: PURE
