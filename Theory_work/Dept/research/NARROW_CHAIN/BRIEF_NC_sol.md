# BRIEF — NC: per-row chain verification of today's NARROWed legacy rows (Theory Department, 2026-11-16)
Sol (codex gpt-6.1-sol), effort high, ONE call, fresh, read-only. Your output is read by a tool, so the line format below is exact.
Do not write any file outside the worktree and set no TMPDIR. Scratch only in /home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/, deleted at the end.
Write exactly one file: `Theory_work/Dept/research/NARROW_CHAIN/NC_sol.md` (relative to /home/fb31/BVS-wt/THEORY-DEPT). Change no git state.
First run `git fetch -q origin` and read every file at **origin/main** (`git show origin/main:<path>`), not the working tree.

## Context
Today these registry rows were NARROWED (correctness event): every-n delivery claims about shipped code were restricted to (a) a bounded
domain 𝔇 under IDEAL-W and (b) every n under A:IDEAL-W⁺ (`Theory_work/Dept/research/FUNI_NARROW/A_IDEALW_PLUS.md`), because two shipped
validators can throw (`Theory_work/Dept/research/FUNI_transfer/TR1_sol.md`). Earlier diff reviews: `FUNI_NARROW/DIFF_sol.md` (F-UNI),
`IDEALW_BATCH/DIFF2_sol.md` (the batch). The registry wants, per row, an explicit statement-level verification.

## Task — for each row of `Theory_work/Dept/research/NARROW_CHAIN/rows.tsv` (columns: id, file, lines, stored sha256)
1. Compute the sha256 of the statement span exactly as the registry does (lines joined with "\n", UTF-8, no trailing newline — if your hash
   of a span does not match the stored one, try with a trailing newline and say which convention reproduces the stored hashes; use that one
   for all rows). Report your computed hash.
2. Judge: is the narrowed statement in that span **proved by the row's own existing proof chain** (the lemmas/files it already cites, with the
   delivery step restricted as the narrowing says), with no input that the chain lacks? Cite the chain files:lines. A row whose statement is
   a research target / partial claim (e.g. W2-FAC-XA:X4) is judged on what its span asserts; if it asserts no proved result, say so.

## Output (exact)
For each row where both hold (hash matches stored AND proved by own chain), one line, nothing else on it:
`NARROW-CHAIN-VERIFIED: <claim id> sha256=<64-hex> chain=OWN`
For each row where either fails, one line:
`NARROW-CHAIN-NOT-VERIFIED: <claim id> reason=<short>`
Then ≤ 25 lines of justification (per row: chain files:lines, one clause). Final line: `ROWS: <n verified>/<n total>`.
