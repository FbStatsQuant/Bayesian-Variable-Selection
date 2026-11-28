# COUNCIL BRIEF — round 3 (scoped fix-verification; TH-SONG-ASSUMPTIONS)

You are one seat of a three-seat review council (Opus, Neon, Sol). Effort: high. This round follows the HQ owner ruling
(POLICIES §1b): **Round 2+ is scoped fix-verification, NOT a cold re-review.** Do not re-read or re-review the package
from scratch.

## Inputs (read only these, plus the exact passages they point to)
1. The prior-round findings: `council/R2_<SEAT>.md` for all three seats (and `council/R1_<SEAT>.md` where an R2 point
   refers back to R1).
2. The Task Lead's point-by-point response: `council/RESPONSE_R2.md` (one-line reasons for declined points included).
3. The diff of the revised sections: `council/R2_TO_R3.diff`. You may open the full files only to read the context of a
   changed passage.

Folder: `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/song_assumptions/`.

## Charter (strict)
Check ONLY:
- (a) whether every prior-round **substantive/blocking** issue was genuinely fixed (not papered over); and
- (b) whether the edits in the diff introduced any **new substantive flaw or regression**.

**No new stylistic nitpicks.** Do not raise points about unchanged text unless the change makes that text wrong. The gate
clears when (a) holds for every issue and (b) finds nothing.

## Rules
- Read-only. Write ONLY `council/R3_<SEAT>.md` (≤ 120 lines). Never delete files. Do not commit. Do not spawn subagents.
- Scratch only under `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/` (never /tmp, never outside the worktree). Never read or write
  under `/home/fb31/Bayesian-Variable-Selection/_local/engineering/`. No cluster jobs.
- For any Python/R: `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`, run under `nice -n 10`.

## Output
`council/R3_<SEAT>.md` must contain:
1. a table with one row per prior-round substantive/blocking issue: **fixed / not fixed**, plus a one-line reason;
2. a list of new substantive flaws or regressions introduced by the diff, each with a location and a fix (or "none");
3. the gate verdict: **CLEAR** or **NOT CLEAR**;
4. optionally, scores 0–10 for D and R on the assumptions touched by the diff.

Then reply with a summary of at most 10 lines.
