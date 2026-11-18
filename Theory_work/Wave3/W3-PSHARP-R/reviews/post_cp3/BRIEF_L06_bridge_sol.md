# BRIEF L06 — re-check of a repaired bridge (W3-PSHARP-R, post-CP3)

You are an independent reviewer (gpt-6.1-sol, reasoning effort high), new to this ticket. Check one short proof line by
line and try to break it. Work in the checkout `/home/fb31/BVS-wt/W3-PSHARP-R` (paths relative to it).

Rule D62: do not write any file outside the worktree and set no TMPDIR; scratch (if any) only in the git-ignored folder
`/home/fb31/BVS-wt/W3-PSHARP-R/.rc_tmp/` at the worktree root, deleted at the end. Never write inside
`Theory_work/Wave3/W3-PSHARP-R/` except your output file. No git operations; start no subagents.

## Read
- Under check: `Theory_work/Wave3/W3-PSHARP-R/reviews/post_cp3/BRIDGE_orth_thm1.md` (repaired), with the repair diff
  `Theory_work/Wave3/W3-PSHARP-R/reviews/post_cp3/BRIDGE_L05_to_L06.diff` and the earlier informal read that triggered it,
  `Theory_work/Wave3/W3-PSHARP-R/reviews/post_cp3/L05_bridge_sol.md`.
- Pinned reader sources, extracted as files (read-only copies of commit e20d287f of the W3-READER branch):
  - `Theory_work/Wave3/W3-PSHARP-R/reviews/post_cp3/sources/READER_VERSIONS_e20d287f.md`
    sha256 3353d8e115e906fa934052de157c2d1201fa3467d0c323855cff0c9218ff62b0 — (S1)/(S2) near the top (lines 1-30),
    Theorem 1 (lines 84-112, its assumptions (A1)–(A6) and expectation display), Theorem 2 (lines 250-270), Theorem 3
    (lines 314-345);
  - `Theory_work/Wave3/W3-PSHARP-R/reviews/post_cp3/sources/NOTATION_e20d287f.md`
    sha256 ca6c6e516278521b3e93899a5e620220be824efeb53b100f62c9da2f88fe4faa — line 46 (R̂_S, G_S), and the model section.
- The master lower bound: `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md` lines 39-92 (Setting-E, (W-orth-E),
  Proposition A-E incl. what n₀ depends on, Corollary A1-E); the parent remark
  `Theory_work/Wave3/W3-PSHARP/lemmas/A_log_factor.md` lines 134-145.
Do not read other files under `Theory_work/Wave3/W3-PSHARP-R/reviews/`, nor LOG or checkpoints. Verify the two sha256
values first (sha256sum is allowed; it is not a git operation).

## Check
1. Each of (A1)–(A6) of Theorem 1, with the constants chosen, holds on the stated design for every p with
   s₀ + 1 ≤ p ≤ n − 1 and n ≥ 2s₀ + 2 (incl. R̂_S, (S2), the second form of (A6), the role of σ*²).
2. Theorem 3(b)'s hypotheses and those of Corollary A1-E / Proposition A-E hold (s₀ + 1 ≤ K, orthogonal witness with all
   nulls, (log p)² = o(n) with the common envelope (log n)²/n).
3. The arithmetic: (s₀ + 1)f_p ≥ 2 for s₀ ≥ 1; ½ log n ≤ ℓ_n ≤ (3/2) log n; the two constants c; the common-threshold
   argument via Proposition A-E with ϵ = ¼.
4. Claim 3 (both bounds for every admissible p_n, constants depending only on s₀, θ*, σ*²) and Remark (ii) (the Gaussian
   witness is not covered in expectation by the reader's Theorem 2).
5. Whether each L05 point is resolved.

## Output
Write `Theory_work/Wave3/W3-PSHARP-R/reviews/post_cp3/L06_bridge_sol.md`: a verdict line
`BRIDGE B3.8: CORRECT | CORRECT-WITH-FIXES | GAP | WRONG`, the status of each L05 point, then findings tagged C/S/F/E with
file:line and the exact fix. Reply with the verdict line and counts by tag.
