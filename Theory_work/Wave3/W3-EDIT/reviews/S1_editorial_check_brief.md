# S1: Sol "editorial only" diff check, W3-EDIT (PROTOCOL_v4 §5.3)

Reviewer: Codex `gpt-6.1-sol`, reasoningEffort high, fresh thread. Read-only on the git worktree
`/home/fb31/BVS-wt/W3-EDIT` (branch `theory/W3-EDIT`). Write your reply to
`Theory_work/Wave3/W3-EDIT/reviews/S1_editorial_check_sol.md` and nothing else. Do not commit or change git state.

## Context
W3-EDIT is the Theory Department's editorial pass. It applies, in place, wording, citation and typo fixes that
councils, sweeps and blind audits found and called non-blocking. PROTOCOL_v4 §0 (`Theory_work/Wave3/PROTOCOL_v4.md`)
gives the rule: a review blocks only on correctness, strength or faithfulness; everything else is editorial. §5.3 says
editorial items are applied in one batch with one "editorial only" diff check. That check is this review.

## Inputs
- The whole diff against the branch base `1478808`, without the ticket's own folder:
  `Theory_work/Wave3/W3-EDIT/reviews/S1_diff.patch` (17 files). Regenerate it with
  `git diff 1478808 HEAD -- . ':(exclude)Theory_work/Wave3/W3-EDIT'`.
- The ledger `Theory_work/Wave3/W3-EDIT/LEDGER.tsv`, columns
  `id | claim | file:line | finding (source) | class | before | after | route`. Rows with route `IN-PLACE` are the ones
  in the diff. Each row names the finding that motivated it (council review, sweep, audit result file); open those
  sources as needed.
- The rest of the repository, to check each edit against what it describes: cited files, code, numerics outputs.

## Questions
For each hunk of the diff:
1. Does it change mathematics: a hypothesis, a conclusion, a quantifier, a constant, a proof step, or what a cited
   result is used for? Or is it wording, citation or typo only?
2. Is the new text correct? Check re-pointed line numbers against the cited file as it is now, quoted numbers against
   their source output, and statements about code against the code. Check that it does not claim more than the source
   supports (strength) and that it is faithful to the source.
3. Does it match the ledger row's "after" column and the finding it implements?

Also look for edits in the diff with no ledger row, and for IN-PLACE ledger rows with no edit in the diff.

## Reply format
1. A table `| ledger id | file:line | EDITORIAL / CHANGES-MATH / INCORRECT | one-line reason |`, with one row per
   IN-PLACE ledger row.
2. Findings. Tag each **C** (correctness), **S** (strength), **F** (faithfulness) or **E** (editorial; wording that
   could be better but is not wrong). Give the file:line, what fails, and the exact fix.
3. One final line, on a line of its own:
   `EDITORIAL-CHECK verdict=PASS|FAIL rows=<n checked> changes_math=<n> incorrect=<n>`.
   Give FAIL if any hunk changes mathematics or is incorrect, or if you hold any C, S or F finding of your own.
