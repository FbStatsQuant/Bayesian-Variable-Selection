# BRIEF L04 — re-check of a one-sentence repair (W3-PSHARP-R, lemmas/AE_expectation.md)

You are an independent reviewer (gpt-6.1-sol, reasoning effort high). Work in `/home/fb31/BVS-wt/W3-PSHARP-R`.
A re-check found that two starting indices n₁ in `Theory_work/Wave3/W3-PSHARP-R/lemmas/AE_expectation.md` (end of §4 and
end of §5) were defined as "the least n with …" although the sequences involved need not be monotone; the lead replaced
them, using the reviewer's exact text, by "the least integer m such that, for every integer n ≥ m, …" (marked [L03-S2]).

Read: the finding `Theory_work/Wave3/W3-PSHARP-R/reviews/L03_recheck_sol.md` (finding S2 only); the diff
`Theory_work/Wave3/W3-PSHARP-R/reviews/L04_repair_diff.txt`; the repaired file (Lemma F in §3 and §4–§5); STATEMENT
`Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md` lines 61-72. Do not read anything else under `reviews/`, nor LOG, PLAN or
checkpoints. No scratch files are needed; if you write any temporary files use
`/home/fb31/SMC_Theory_Department/tmp/20261116-W3-PSHARP-R-L04/` and delete it.

Questions: (1) Is S2 resolved (the tail conditions hold for every n ≥ n₁; n₁ exists and depends only on the permitted
parameters)? (2) Does the edit change or break anything else?

Write to `Theory_work/Wave3/W3-PSHARP-R/reviews/L04_recheck_sol.md`: `S2: RESOLVED | NOT-RESOLVED`, `LEMMA AE_expectation:
CORRECT | CORRECT-WITH-FIXES | GAP | WRONG`, and any finding tagged C/S/F/E with file:line and exact fix. Change no other
file; no git operations. Reply with the two verdict lines and counts by tag.
