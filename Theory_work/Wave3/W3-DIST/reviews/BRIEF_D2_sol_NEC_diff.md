# W3-DIST — diff check D2 (re-check of three presentation amendments to `lemmas/NEC.md`) — gpt-6.1-sol, codex, reasoningEffort high

You are an independent checker, new to this ticket. Repo clone `/home/fb31/Bayesian-Variable-Selection`; ticket folder
`Theory_work/Wave3/W3-DIST/` (paths below are relative to it). **Read-only except your one output file
`reviews/D2_sol_NEC_diff.md`.** Run no git command that changes state; start no agents; no cluster jobs; any computation
small and `nice`. Any temporary file goes under `/home/fb31/SMC_Theory_Department/tmp/20261115-W3-DIST-D2/` (never `/tmp`);
remove it when done. This is a short task.

A line check (`reviews/L7_sol_NEC.md`) verified Proposition NEC and Corollary NEC in `lemmas/NEC.md` v0.1 and raised
three presentation findings (L7-01 MINOR, L7-02 NIT, L7-03 MINOR). The lead applied three amendments (v0.2).
The exact diff is `reviews/DIFF_D2_NEC.patch`. Read the three findings, the diff and the amended passages in
`lemmas/NEC.md` (with as much of the surrounding text as you need; the statements referred to are Lemma X′ and display
(1.2) in `STATEMENT.md` §1 and §3). Decide, hunk by hunk:
1. Does the amendment resolve its finding, and is the amended text correct as it now reads?
2. Does the diff contain any change beyond the three amendments and the version line? Does any hunk alter the
   Proposition, the Corollary, a constant or a proof step?
3. L7-02: recompute 2/√(πβ) at β = 256 and confirm that the chain of inequalities on that line still gives ≤ 0.08p
   eventually, as the surrounding argument uses it.
Also confirm that the statement of Proposition NEC in `STATEMENT.md` §3 (the paragraph starting "**Proposition NEC**")
agrees with `lemmas/NEC.md` §0 as amended, and does not repeat the error of L7-01 (the radius attributed to (1.2)).

Output (`reviews/D2_sol_NEC_diff.md`): first line `D2 diff check — lemmas/NEC.md sha256 <first 16 hex>`. Findings with id
(D2-xx), severity (CRITICAL / MAJOR / MINOR / NIT), place, the error in full, minimal repair. Verdict per hunk
(RESOLVED / NOT RESOLVED) and for the file as it now stands (VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED).
Final line: overall verdict. Do not soften findings; say exactly what you could not check.
