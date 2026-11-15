# R07FIX — cell grammar correctness test (Sol) — brief

Context: a software-correctness test of one small text-matching function in a research-project bookkeeping tool (a
Python registry of mathematical claims). Reviewers record per claim, in a Markdown table, whether they accept it. No
security testing is involved; the task is to check that the function's output matches its written grammar on every
input you can construct.

You are an independent tester (Codex GPT-6.1 Sol, effort high). The code is in the worktree
`C:/Users/felip/BVS-wt/INFRA-R07` (branch `infra/R07-accept-form`, last commit 4a68a2a plus uncommitted changes in
`Theory_work/INFRA/tools/bvsreg.py`, `tools/test_lifecycle.py`, `LIFECYCLE.md`). **Read that worktree only; change no
git state anywhere and edit no file in it except your output file.** For experiments, import the module read-only
(`sys.path.insert(0, "C:/Users/felip/BVS-wt/INFRA-R07/Theory_work/INFRA/tools"); import bvsreg`) or copy it to a temp
folder. Do NOT run `test_lifecycle.py` (it is long and already run). Start no subagents. Keep it narrow: about 30–45
minutes.

## Grammar under test (INFRA R07, HQ ruling 2026-11-12)
`bvsreg.decision_value(cell)` (and through it `seat_table`) returns `"accept"` for a decision cell iff, after trimming
surrounding spaces / tabs only, the cell is in the R06 whitelist (`ACCEPT`, `accepted`, `Accepted`, `ACCEPTED`) OR
matches exactly the one anchored R07 form

    <accepted | Accepted | ACCEPTED> [" with non-blocking remarks"] [" (" <text> ")"]

- single spaces between parts, the remark phrase in lower case exactly as written;
- at most ONE parenthetical, at the very end, with non-blank content, whose parentheses are balanced (nesting
  allowed: the opening `(` must close exactly at the cell's last character), nothing after it;
- no line / paragraph separator anywhere in the cell;
- the parenthetical's content is NOT interpreted (by design, no keyword heuristics: `accepted (withdrawn)` reads as
  accepted — that is intended, not a defect).
Everything else is `"unknown"` (or `"not-accept"` for exactly `NOT-EXAMINED`), i.e. NOT accepted. Row-level rules
(complete `|`-bounded rows, no extra non-empty cells, split / continued rows, contradictory duplicate ids) are
unchanged from R06 and must still apply when the cell has the R07 form.
Spec text: comment above `DECISION_ACCEPT` and `_accept_remark_form` in `bvsreg.py`; `LIFECYCLE.md` paragraph
"*Accepted with remarks*".

## Do
1. Confirm the four real cells read `"accept"`:
   - `accepted with non-blocking remarks (Issue 5: the η = 0 sentence is read under the premise of F1(ii))`
   - `accepted with non-blocking remarks (Issue 3)`
   - ``accepted with non-blocking remarks (Issue 2: wording of the P-OVL row in `STATEMENT.md` §4, not of OVL itself)``
   - `accepted (F-1, F-2, F-3, G-1, G-2 verified; UNI-0 and AR(1) correctly not claimed)`
2. Construct inputs that the grammar says are NOT accepted and check none reads `"accept"`: extra words before /
   after, commas, `except`, `conditional on`, blocking remarks, `not accepted (…)`, text after the parenthetical,
   two parentheticals, unbalanced / empty / whitespace-only parentheses, parentheses that close early and reopen,
   other case of the remark phrase, other spacing (double space, tab, NBSP, other Unicode spaces, zero-width
   characters, BOM), look-alike letters, emphasis / code marks, separators (CR, LF, VT, FF, FS/GS/RS, NEL, U+2028,
   U+2029) inside the cell or parenthetical, `ACCEPT (…)`, and the form inside split / continued rows or with a
   remarks column (use `seat_table`).
3. Construct inputs the grammar says ARE accepted (nested balanced parentheses, Unicode text inside, long text) and
   check they read `"accept"`.
4. Any regex / backtracking cost issue on long inputs (e.g. 100k characters)?

## Output
Write `C:/Users/felip/BVS-wt/INFRA-R07/Theory_work/INFRA/R07FIX/R07_sol.md`: the inputs you tried (grouped; exact
reprs for any mismatch), every mismatch with the grammar as a numbered finding (severity MAJOR = a non-grammar cell
reads accepted; MINOR = a grammar cell reads not accepted, or doc / message issue), and a last line
`R07-SOL: <n> findings (<m> MAJOR)`.
