# R07FIX (rule 2) — table-reading correctness test (Sol) — brief

Context: a software-correctness test of one small Markdown-table reader in a research-project bookkeeping tool (a
Python registry of mathematical claims). Reviewers record per claim, in Markdown tables, whether they accept it. No
security testing is involved; the task is to check that the reader's output matches its written rule on every input
you can construct.

You are an independent tester (Codex GPT-6.1 Sol, effort high). The code is in the worktree
`C:/Users/felip/BVS-wt/INFRA-R07` (branch `infra/R07-accept-form`, last commit 4a68a2a plus uncommitted changes in
`Theory_work/INFRA/tools/bvsreg.py`, `tools/test_lifecycle.py`, `LIFECYCLE.md`). **Read that worktree only; change no
git state anywhere and edit no file in it except your output file.** Experiment by importing the module read-only
(`sys.path.insert(0, "C:/Users/felip/BVS-wt/INFRA-R07/Theory_work/INFRA/tools"); import bvsreg`), calling
`bvsreg.seat_table(text, "T")` → `({"T:<id>": accepted?}, [problems], n_tables)`. Do NOT run `test_lifecycle.py` (long,
already run). Start no subagents. Keep it narrow: about 30–45 minutes. (An earlier, different rule was tested in
`R07_sol.md`; it has been withdrawn — ignore it.)

## Rule under test (INFRA R07, HQ ruling 2026-11-12)
Spec text: the comment block above `_BODY_NEG_TERMS` and the functions `_neg_norm`, `_neg_hit`, `_split_at_verdict`,
`_body_scan`, `seat_table` in `bvsreg.py`; `LIFECYCLE.md` paragraph "*Addendum supersedes body*". In short:
1. A review text is split at its FIRST line that (after an optional opening backtick) starts with `COUNCIL-VERDICT`.
   The part after it is the addendum part.
2. The addendum is VALID iff the addendum part has at least one per-claim table and no table-level malformation under
   the unchanged strict R06 reader (`_seat_table_strict`: exact header `| id | decision |` with delimiter row; rows
   `ACCEPT` / `NOT-EXAMINED`; legacy `accepted` / `Accepted` / `ACCEPTED`).
3. With a valid addendum, the addendum (strict reading) is the decision table. The body (before the verdict line) is
   read only for negatives: per-claim tables found by a lenient header (first two cells id / claim / claim id and
   decision / disposition); a body row's DECISION column (2nd cell) containing, case-insensitively, any of `not
   accepted`, `reject`, `withdraw`, `not examined`, `not-examined`, `refus`, `fail` → that id NOT accepted. Normalisation
   for this test only (fail closed): NFKC, Cf characters dropped, Markdown emphasis / code marks, backslash, dashes,
   underscores and all Unicode whitespace → one space, casefold; a term also matches with spaces removed. Separators
   (CR, VT, FF, FS/GS/RS, NEL, U+2028/9) split body lines; a body line that is not a `|`-row with a non-empty id is
   scanned WHOLE and a hit refuses the previous row's id (and the line's first segment as an id). A body id absent from
   the addendum → NOT accepted. Text in other body columns (e.g. `Basis`) and free text are ignored.
4. Without a valid addendum (no verdict line, no table after it, or a malformed addendum table) the whole text is read
   by the strict R06 reader exactly as before.

## Do
1. Positives (must be accepted): body with the four real cells below + addendum ACCEPT; a 3-column body
   `| Id | Disposition | Basis |` whose Basis cells contain words like failed / rejected / withdrawn, + addendum ACCEPT.
   - `accepted with non-blocking remarks (Issue 5: the η = 0 sentence is read under the premise of F1(ii))`
   - `accepted with non-blocking remarks (Issue 3)`
   - ``accepted with non-blocking remarks (Issue 2: wording of the P-OVL row in `STATEMENT.md` §4, not of OVL itself)``
   - `accepted (F-1, F-2, F-3, G-1, G-2 verified; UNI-0 and AR(1) correctly not claimed)`
2. Try to construct a body whose decision column says, to a human reader, one of the listed negatives (or
   NOT-EXAMINED), yet the id still reads accepted with an addendum ACCEPT: spelling / Unicode / emphasis / HTML
   entity or tag / escaped characters / split or continued rows / separators / column misalignment (extra or missing
   pipes, escaped pipes, leading pipe missing) / several body tables / tables in code fences or block quotes /
   header variants that the lenient detector misses but a human reads as the per-claim table / an id spelled
   differently in body and addendum (emphasis, prefix `T:`). Report which are outside the rule (e.g. a synonym not
   in the closed list is by design NOT a negative) and which are real misses of the rule as written.
3. Verdict-line split: a COUNCIL-VERDICT mention in prose before the real line; the body table after the verdict
   line; two addenda; a malformed addendum (must fall back to strict R06 for the whole file).
4. Body id missing from the addendum → NOT accepted; addendum rows other than ACCEPT stay not accepted.

## Output
Write `C:/Users/felip/BVS-wt/INFRA-R07/Theory_work/INFRA/R07FIX/R07_sol2.md`: the inputs tried (grouped; exact reprs
for any mismatch), each mismatch with the rule as written as a numbered finding (MAJOR = an id reads accepted that
the rule says is NOT accepted; MINOR = the reverse, or a doc / message issue; NOTE = outside the rule by design), and
a last line `R07-SOL2: <n> findings (<m> MAJOR)`.
