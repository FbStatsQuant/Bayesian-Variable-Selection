# R06FIX — parser correctness test (Sol) — brief

Context: a software-correctness test of one small text parser in a research-project bookkeeping tool (a Python
registry of mathematical claims). The parser reads Markdown tables in which two reviewers record, per claim, whether
they accept it. No security testing is involved; the task is to check that the parser's output matches its written
specification on every input you can construct.

You are an independent tester (Codex GPT-6.1 Sol, effort high). The code is in the worktree
`C:/Users/felip/BVS-wt/INFRA-R06` (branch `infra/R06-eol`, last commit 4952705 plus uncommitted changes). **Read that
worktree only; change no git state anywhere**; work in a disposable clone under a short temp path (copy the
uncommitted files over it: `git -C C:/Users/felip/BVS-wt/INFRA-R06 status --short`). Start no subagents. Write only
your output file (below).

## Specification under test (HQ ruling, 2026-11-12)
`Theory_work/INFRA/tools/bvsreg.py`: `decision_value`, `decision_accepts`, `seat_table`, `seat_decisions`,
`_row_problems`, and their two callers `checkpoint_problems` (part (b)) and `seat_table_problems`. Documented in
`Theory_work/INFRA/LIFECYCLE.md` §4.1 item 2 of "Checkpoint status source" and in the comment above
`DECISION_ACCEPT`. In short:
1. A per-claim table starts at a header row whose first cell is `id` / `claim` / `claim id` and second `decision` /
   `disposition` (case-insensitive) and runs to the first blank line.
2. The decision cell, trimmed of surrounding spaces / tabs and the table pipes and nothing else, must equal exactly
   `ACCEPT` (or, for legacy tables, exactly `accepted` / `Accepted` / `ACCEPTED`) to read as accepted; exactly
   `NOT-EXAMINED` reads as not accepted; anything else reads as NOT accepted with a problem naming the claim.
3. Every line inside the table must be a complete row: starts and ends with `|`, no escaped pipe, no line or
   paragraph separator character (CR, VT, FF, FS/GS/RS, NEL, U+2028, U+2029), the header's number of cells, and every
   cell after the decision empty. A row continued or split (an incomplete line, a row with an empty id, a separator
   character) makes that row's claim and the previous row's claim NOT accepted. An id listed twice with different
   readings is NOT accepted.
4. Fail closed: when in doubt the output must be "not accepted"; a checked label for that claim is then refused
   (acceptance check A4) with a clear message.
The previous tester's 95 inputs are in `Theory_work/INFRA/R06FIX/decision_cases.json` (exact table texts, Sol's
original expectation `sol_expected`, and `expected` under this specification: 13 of Sol's positive controls with
remarks or other spellings now read as not accepted by design — that is intended, not a defect).

## Do
1. Re-run the 95 cases (`seat_decisions(text, "REV")[0].get("REV:A", False)`) and confirm each equals `expected`.
2. Construct new inputs and compare the output with the specification: other whitespace and Unicode (NBSP, zero-width
   characters, BOM, combining marks, full-width or look-alike letters), case, Markdown emphasis or code, HTML entities
   or tags in the cell, escaped characters, leading / trailing pipes doubled, separator-row variants, header variants,
   blank lines with spaces, tables inside code fences or block quotes, several tables in one file (body plus dated
   addendum), duplicate and contradictory rows in either order, local vs full ids, ids with emphasis, rows without a
   leading pipe, a table directly followed by text. Report every input where the output says "accepted" although the
   specification says "not accepted" (an acceptance error), and separately every input wrongly read as "not
   accepted" (a fail-closed false negative; report but rate MINOR unless it breaks the documented ACCEPT / NOT-EXAMINED
   addendum workflow).
3. End-to-end: for a few acceptance errors (if any) and for a plain ACCEPT control, show the effect through
   `python -B Theory_work/INFRA/tools/ingest.py claims <carrier.jsonl> --staged` (two seat reviews, each with one
   `COUNCIL-VERDICT` line and the table; a frozen manifest covering the statement and status files; the carrier in
   `reviews/`). The suite's block "INFRA R06" in `Theory_work/INFRA/tools/test_lifecycle.py` has a ready fixture
   (ticket `R06T`).
4. Run the full suite once in a fresh clone with the changes and no other probes:
   `python -B Theory_work/INFRA/tools/test_lifecycle.py` (expected all PASS; record the Python exit code directly).

## Output
`C:/Users/felip/BVS-wt/INFRA-R06/Theory_work/INFRA/R06FIX/R06FIX_parser_sol.md`: a verdict line first (PARSER MATCHES
SPEC / MATCHES WITH MINOR FINDINGS / ACCEPTANCE ERRORS FOUND); the 95-case result; a table of your new inputs (input,
spec reading, actual reading, OK / mismatch); findings with severity (MAJOR = an acceptance error; MINOR = a false
negative or message issue), exact reproduction and a fix direction; the staged results; the suite result; scratch
paths. Keep it factual and compact. End your run with a ≤ 5-line summary.
