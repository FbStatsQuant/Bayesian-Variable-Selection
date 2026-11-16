# BRIEF L03 — re-check of a repaired lemma (W3-PSHARP-R, lemmas/AE_expectation.md)

You are an independent reviewer (gpt-6.1-sol, reasoning effort high). A line check found one strength defect in an
assembly lemma; the lead repaired it. Check **only the repair** and whether it breaks anything. Work in the checkout
`/home/fb31/BVS-wt/W3-PSHARP-R` (paths relative to it).

## What to read
- The finding (and only this part of the earlier review): `Theory_work/Wave3/W3-PSHARP-R/reviews/L02_line_check_sol.md`,
  section "## Finding" (S1).
- The repair as a diff: `Theory_work/Wave3/W3-PSHARP-R/reviews/L03_repair_diff.txt`; the repaired file
  `Theory_work/Wave3/W3-PSHARP-R/lemmas/AE_expectation.md` (lines marked [L02-S1]: the header, Lemma F in §3, the ends of
  §4 and §5; read enough of §3–§5 to judge them).
- What the lemma must prove: `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md` §3.1 (lines 61-72), in particular the clause on
  what n₀ depends on.
Do not read LOG, PLAN, checkpoints or other review files. Scratch (if any): `Theory_work/Wave3/W3-PSHARP-R/reviews/L03_scratch/`;
temp files: `export TMPDIR=/home/fb31/SMC_Theory_Department/tmp/20261116-W3-PSHARP-R-L03; mkdir -p "$TMPDIR"`, delete after.

## Questions
1. Is S1 resolved: does Lemma F now prove its conclusion from its hypotheses, with n₀ depending only on (ϵ, 𝔭)?
2. In §4 and §5, are the named starting indices n₁ right (every condition the displayed inequality needs before it holds:
   T ≥ 1, x_n ≥ 1, d ≥ 3, 2 log T ≤ d/2, …) and functions of the permitted parameters only? Is the claim
   "ψ_n ≤ ¼ gives 2 log T ≤ √n/2 ≤ (n − 1)/2" correct?
3. Does the diff change anything else, or break any downstream use (§6–§8)?

## Output
Write to `Theory_work/Wave3/W3-PSHARP-R/reviews/L03_recheck_sol.md`: a verdict line `S1: RESOLVED | NOT-RESOLVED`, a line
`LEMMA AE_expectation: CORRECT | CORRECT-WITH-FIXES | GAP | WRONG`, and any finding tagged C/S/F/E with file:line and the
exact fix. Change no other file; no git operations. Reply with the two verdict lines and counts by tag.
