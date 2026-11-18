# BRIEF L05 — line check of one bridge (W3-PSHARP-R, post-CP3)

You are an independent reviewer (gpt-6.1-sol). Check one short proof line by line and try to break it. Work in the
checkout `/home/fb31/BVS-wt/W3-PSHARP-R` (paths relative to it).

Rule D62: do not write any file outside the worktree and set no TMPDIR; scratch (if any) only in the git-ignored folder
`/home/fb31/BVS-wt/W3-PSHARP-R/.rc_tmp/` at the worktree root, deleted at the end. Never write inside
`Theory_work/Wave3/W3-PSHARP-R/` except your output file. No git operations; start no subagents.

## Read
- Under check: `Theory_work/Wave3/W3-PSHARP-R/reviews/post_cp3/BRIDGE_orth_thm1.md`.
- What it relies on: the reader's Theorem 1 and Theorem 3 text, `git show e20d287f:Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
  (lines 84-112 for Theorem 1 and (S1)/(S2) at its lines 1-30; lines 314-345 for Theorem 3), and its notation
  `git show e20d287f:Theory_work/Wave3/W3-READER/NOTATION.md` (line 46); the master lower bound
  `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md` lines 39-92 (Setting-E, (W-orth-E), Proposition A-E, Corollary A1-E);
  the parent remark `Theory_work/Wave3/W3-PSHARP/lemmas/A_log_factor.md` lines 134-145.
Do not read other files under `Theory_work/Wave3/W3-PSHARP-R/reviews/`, nor LOG or checkpoints.

## Check
1. Each of (A1)–(A6) of Theorem 1, with the constants chosen, holds on the stated design for every p with
   s₀ + 1 ≤ p ≤ n − 1 and n ≥ 2s₀ + 2 (incl. the meaning of R̂_S, (S2), the second form of (A6)).
2. Theorem 3(b)'s hypotheses and those of Corollary A1-E hold (incl. s₀ + 1 ≤ K, (W-orth) with all nulls, (log p)² = o(n)).
3. The arithmetic: (s₀ + 1)f_p ≥ 2 for s₀ ≥ 1, p ≥ s₀ + 1; ℓ_n ≥ ½ log n; the two constants c; the passage from
   liminf E/Λ^E ≥ 1 to "for n large".
4. The claim in item 3 that both bounds hold "for every such sequence p_n" with the stated dependence of constants, and
   that Remark (ii) is right that the Gaussian witness is not covered in expectation by the reader's Theorem 2.

## Output
Write `Theory_work/Wave3/W3-PSHARP-R/reviews/post_cp3/L05_bridge_sol.md`: a verdict line
`BRIDGE B3.8: CORRECT | CORRECT-WITH-FIXES | GAP | WRONG`, then findings tagged C/S/F/E with file:line and the exact fix.
Reply with the verdict line and counts by tag.
