# Brief — Sol diff check v2 of the IDEAL-W⁺ batch NARROW (19 claims) and errata, after one repair

Prepared 2026-11-16 by the Theory Dept implementation sub-agent (Claude Opus 5.5). Reviewer: gpt-6.1-sol, reasoning high.
This is a fresh review of the whole batch: the first review returned FAIL, and the batch has been repaired once.

## Rules
- You are a **fresh, read-only** reviewer. Edit no file except your one reply file below. Do not commit to, or touch,
  any other worktree. Do not change the registry. Do not apply the patches to the real files.
- **D62 (verbatim):** "Do not write any file outside the worktree and set no TMPDIR. Scratch only in /home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/, deleted at the end."
- Write your reply to `Theory_work/Dept/research/IDEALW_BATCH/DIFF2_sol.md` (inside the worktree `/home/fb31/BVS-wt/THEORY-DEPT`).
  Last line: `DIFF: PASS` or `DIFF: FAIL`. Use FAIL only for a concrete defect in the batch, and give a concrete same-line-count
  repair with it.

## Inputs
- Everything listed in `BRIEF_DIFF_sol.md` (same folder): patches, TR1, the A:IDEAL-W⁺ definition, the code and the F-UNI
  precedent. Its questions (a)–(f) and the per-claim table also apply here.
- The first review: `DIFF_sol.md` (same folder; FAIL). Read it, but judge independently. Do not assume its PASS findings.

## What changed since DIFF_sol.md
- **R1**, applied verbatim from DIFF_sol.md. In `patches/W2-FAC-XA__STATEMENT.md.patch`, the appended note's first
  physical line (target line 112) now says that X4 remains a research target, that X2's discovery argument is open, and
  that the edit strengthens only the proposed delivery premises. The in-span edit at `:86` is unchanged.
- **R2**, applied verbatim from DIFF_sol.md. In `patches/ERRATUM__C-DLV__INVENTORY.md.patch`, target line 80 (the
  Summary) now excludes X7–X8 by A:IDEAL-W⁺ or on 𝔇 *before* the "only random no-output path" sentence at :81.
  Line 81 is unchanged.
- **Editorial changes in `LINES_CHECK.md`:**
  - "19 batch rows" is now "17 batch rows";
  - W2-FAC-B:L5 and W2-FAC-S5:L5 are now "UNCHANGED; keep 1.0.0; delivery metadata correction only";
  - W2-FAC-XA:X4 is now "WEAKER target only; retain PARTIAL";
  - the whole-file after-hashes of the two repaired files are refreshed.

No other patch changed (`git diff 4b7150fe -- Theory_work/Dept/research/IDEALW_BATCH/patches` shows only these two files).
R1 changes an appended note and R2 changes an unregistered line, so no registered span or claim hash changes.

## Questions
(a)–(f) as in `BRIEF_DIFF_sol.md`, over the whole batch as it now stands. Also answer:

(g) Do R1 and R2 fully repair DIFF_sol's two defects, and do they introduce any new defect?
(h) Do you accept the tag corrections: UNCHANGED for FAC-B:L5 and S5:L5, and "WEAKER target only, retain PARTIAL" for XA:X4?

Include a per-claim table (id | (a) true & proved? | (b) scope OK? | (c) tag). End with the single line `DIFF: PASS` or `DIFF: FAIL`.
