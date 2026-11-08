# Common brief for W1-PXN item reviewers (read first)

You are an independent cross-family reviewer (Codex) for ticket W1-PXN, repo C:\Users\felip\Bayesian-Variable-Selection.
Read-only except for your ONE output file. No git state changes. No subagents. You may run small local Python checks
(C:/Users/felip/anaconda3/python.exe has numpy/scipy) if useful; keep them under a few minutes; put any script you write
under Theory_work/Wave1/W1-PXN/numerics/reviewer_<your item>/.

Paths: NBH = Theory_work/Old_Projects/New_BVS_Headquarters/ ; PROOF = NBH/branch_snapshots/API-PXNGAP/PROOF.md (the
candidate proof under review, Claude-authored) ; the locked target statement is Theory_work/Wave1/W1-PXN/STATEMENT.md
(read §1-§3 for setting, notation and how A enters). Score/target definitions: STATEMENT §1 and
NBH/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/STATEMENT.md §1.

Standard: check every step of your assigned part line by line: hypotheses used = hypotheses stated, constants and
quantifiers correct, the range of every cited lemma covers the use, no hidden assumption, the dependence on the fixed
exponent A (p <= n^A, A > 1 allowed) tracked. Re-derive; do not trust the text's own claims of verification.

Output format (write to the file named in your item brief, and return the same content as your final message):
- First line: "VERDICT: VERIFIED | VERIFIED WITH MINOR FIXES | GAP | ERROR" for the item as a whole.
- A table: claim / step (with path:line) | verdict (VERIFIED / MINOR / GAP / ERROR) | reason.
- Numbered findings: severity (ERROR = false statement; GAP = unjustified step that may be true; MINOR = typo/constant
  slip not affecting the conclusion), evidence path:line, and the exact repair you would accept.
- A line "A-dependence:" stating whether the part holds for every fixed A >= 1 (A > 1 included) and how its
  constants/onset depend on A.
Be concise; do not restate the documents.
