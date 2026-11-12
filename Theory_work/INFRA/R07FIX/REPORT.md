# INFRA R07 — addendum supersedes body — REPORT (2026-11-12, HQ decision 2)

Implementer: Claude Opus 5.5 (high). Worktree `C:/Users/felip/BVS-wt/INFRA-R07`, branch `infra/R07-accept-form`
(HEAD 4a68a2a). **Uncommitted; no git state changed** (HQ commits). Changed: `tools/bvsreg.py`,
`tools/test_lifecycle.py`, `LIFECYCLE.md`. New files: `R07FIX/BRIEF_sol2.md`, `R07FIX/R07_sol2.md`, this report.
History (withdrawn design): `BRIEF_sol.md`, `R07_sol.md`.

## Decision 1 (withdrawn)
The first R07 design, an anchored `accepted [with non-blocking remarks] [(…)]` form, is **reverted**. The three files
were restored to HEAD before the new work. With no addendum, the R06 strict reader is unchanged (same code, now
`_seat_table_strict`).

## Decision 2 (implemented)
- `seat_table` splits the raw review at its first `COUNCIL-VERDICT` line.
- A **valid addendum** is at least one per-claim table after that line, with no table-level malformation under R06.
  When there is one:
  - The addendum, read strictly, is the seat's decision table.
  - Body tables are read only for negatives. A body row whose **decision column** (2nd cell; never Basis or other
    columns) contains `not accepted`, `reject`, `withdraw`, `not examined`, `not-examined`, `refus` or `fail`
    (case-insensitive) refuses that id ("listed with contradictory decisions").
  - A body id missing from the addendum is refused.
  - Everything else in the body is ignored.
- Without a valid addendum (no verdict line, no table after it, or a malformed addendum header), the whole file is
  read by R06 as before.
- **Fail-closed additions beyond the literal ruling** (they can only add refusals; please confirm):
  - The substring test normalises the cell first: NFKC; invisible format characters dropped; emphasis and code marks,
    backslashes, every Unicode dash or connector (Pd, Pc, U+2212) and all whitespace read as one space; case folded.
  - A term also matches with its spaces removed (`NOTACCEPTED`).
  - LF and every line or paragraph separator end a body line.
  - A body line that is not a row with an id (a continued or split row) is scanned whole, and a hit refuses the
    previous row's id.
- LIFECYCLE §"Seat tables by addendum" now has a paragraph *Addendum supersedes body*.

## Results
- **Branch re-read** (`git show`, old vs new reader):
  - W3-START R2: Opus 17 → **21/21**, Sol 0 → **21/21**. Both seats accept all 21, including the 4 Opus remark cells
    and Sol's Basis column.
  - PSHARP R2 4/4 and 4/4, MISR R2 7/7 and 7/7, RM2 C_R1 astra 18/18 and Opus 16/18. **Unchanged.**
- **Staged acceptance** (disposable clone of main 07ee8b0 + merge of theory/W3-START e3bc846, new bvsreg):
  `ingest.py claims CHECKPOINT_3.md --staged` → **PASS, 0 acceptance ERROR** (431 claims, 0 ERROR).
- **Tests (+3 results).**
  - Direct (`R07 addendum supersedes body`):
    - Accepted: the 4 real Opus cells; a Basis column holding negative words; free text and extra columns.
    - Refused: 22 negative spellings; split, continued, U+2028 and escaped-pipe rows; a body id missing from the
      addendum.
    - Sol regressions: the 9 separators at header level, all Unicode Pd dashes, and separator-made blank lines.
  - No valid addendum (`R07 without a valid addendum`): the 4 remark cells and `accepted (withdrawn)` are still
    refused when there is no addendum, a malformed addendum, or no verdict line before it.
  - Staged checkpoint (`R07 staged checkpoint`): Basis + remark bodies + addenda → PASS. Body `accepted (withdrawn)`
    → REFUSED (A). Body `rejected` → REFUSED (B). Body id missing from the addendum → REFUSED (B).
  - All R06 suites (95 + 116 Sol cases, whitelist, staged variants, separators) are unchanged and contain no addendum.
- **Suite:** **172/172 PASS, exit 0** (169 R06 + 3 R07), final run after the Sol fixes. `check.py --quiet`: 406 claims, **0 ERROR** (184 WARN, 217 INFO).
- **Sol check** (codex gpt-6.1-sol high, mode wait; `R07_sol2.md`): 4 findings (2 MAJOR, 1 MINOR, 1 NOTE). Fixed
  once:
  - F1 MAJOR: body lines were split on separators only after header detection, so a header and rows joined by
    U+2028 etc. were missed. Separators now split logical lines first.
  - F2 MAJOR: only some Unicode dashes were normalised (e.g. `not⸺accepted` passed). All Pd and Pc characters now
    read as a space.
  - F3 MINOR: a blank line made of separators did not end the table. Fixed by the same split.
  - NOTE: by design these remain accepted: HTML entities, synonyms (`declined`, `denied`), Cyrillic look-alikes, a
    word split across rows, misaligned pipes, ids spelled differently in body and addendum (e.g. `_C_`), and header
    styles the inherited lenient detector misses.
  - Not re-checked by Sol (one round, as briefed).
- Other: a stopped earlier suite run of mine left no process. Sandboxes `sb-xebkym10` and `sb-lk1f0gyf` belong to
  another session's running tests and were not touched.
