# PR #42 review — WP3 mechanical split of `island_impl.h` (run / pm / lm + lm_state)

Reviewer: independent (Opus 5.5, high), 2026-11-16. Design: WP3_ARCH_REVIEW §4.
- **Final head: 4cb0ebc2** = the split commit 24e13309 + the merges 88a3d6c4 / 4cb0ebc2 of `exp/P1M-wp3-calib`
  (#39, now fcdcd2c0).
- `git diff 24e13309 4cb0ebc2 -- src/island/` is **empty**.
- `git diff fcdcd2c0 4cb0ebc2` is exactly the six split files. So the PR adds nothing beyond the split, and
  everything below applies to the final head.

## Verdict: **MERGE** (ACCEPT)

The split is purely mechanical. No statement changed, and the compiled island code is **byte-for-byte identical**
to its base. Counts: **0 CRITICAL, 0 MAJOR, 1 MINOR** (process; it does not block the merge), plus 1 INFO.

## What I verified
1. **Statements: the concatenation diff, modulo moves.** I compared the old `island_impl.h` at 6bb89fc5 with the
   five new files, normalising leading and trailing whitespace.
   - **As a multiset of lines,** the difference is only:
     - out-of-class signatures (`template <Arith A>`, `IslandEngine<A>::`);
     - the four in-class declarations (`step_nongibbs`, `draw_order`, `pm_round`, `lm_group`);
     - `using GroupBuf = LmGroupBuf;` and `struct GroupBuf` → `struct LmGroupBuf`;
     - includes, `#pragma once`, namespace lines and header comments.
   - **As sequences, block by block:**

     | block | lines |
     |---|---|
     | `step_nongibbs` | 52 |
     | `draw_order` | 28 |
     | `pm_round` | 40 |
     | `lm_group` | 278 |
     | `GroupBuf` / `LmGroupBuf` | 11 |

     Each block's body is **identical in order**.
   - The remainder of the old file, against `island_run.h`, differs only by one added include and the five
     declaration / alias lines.
   - `LmGroupBuf` uses only namespace-scope names (`Particle`, `SupportCache`, `avec`). `IslandEngine` has no
     class-scope alias that a name could have bound to, so moving the struct out of the class changes no name
     lookup.
2. **Object code.**
   - I compiled `island_bit.cpp` and `island_a.cpp` from 6bb89fc5 and from 24e13309 with the same CMake Release
     flags (default build).
   - `size`: text 255,339 / 247,337 bytes in both.
   - `objdump -d` is **identical instruction for instruction**. The only differences are the symbol / section name
     `IslandEngine<A>::GroupBuf::~GroupBuf` → `LmGroupBuf::~LmGroupBuf`.
   - So the loss of the implicit `inline` on the moved member functions changed no inlining decision either. There is
     no performance risk.
   - Only `island_bit.cpp` and `island_a.cpp` include `island_impl.h`, so no other translation unit is affected.
3. **Tests (Owls, gcc 11.5, `nice -n 19`, 3 threads, fresh build of 24e13309):** v4_tests **114 test cases, 0 failed,
   0 check failures**.
   - T3 hashes are unchanged on every kernel / thread / G / tile row: bit `44a15bfc6fb8d233`, A
     `d2df149413596a19`.
   - All island goldens vs core pass: final, compat, and calibration compat / law / failure prefix.
   - The R golden and the WP5 extras were not re-run on this head, because the island object code is identical to
     6bb89fc5. They ran on #39 (528,081 / 0) and on the merged stack in the #43 review.
4. **Stacking.** The final head 4cb0ebc2 contains #39's head fcdcd2c0, and GitHub reports MERGEABLE / CLEAN.
   - The #39 commits after 6bb89fc5 (e8bef8b0: the WP4 merge; fcdcd2c0: the N-1 admission) do not touch
     `island_impl.h`, so the identical-object-code result carries over.
   - The whole stack, #43 head 8d584649 (which contains 4cb0ebc2), ran the full `run_tests.sh` in the #43 review
     (see PR43_review.md).

## Findings

### MINOR-1 — ownership comment vs §4 table
- WP3_ARCH_REVIEW §4 gives `island_pm.h` to "the reference". The PR puts the shared U / N / I steps and the round
  order there as well.
- Builder 6's K2 package (Philox multiply, inverse-only orders, I-step proposals in the order phase) edits exactly
  `draw_order` / `step_nongibbs`. That is in `island_pm.h`, which is not in builder 6's §4 file list.
- The PR body says so ("builder 6 edits `draw_order` / `step_nongibbs` for K2"), but the README table and the §4 table
  do not.
- **Fix:** one line in the README ownership column, and the manager tells builders 6 and 7 at the 08:00 start.

### INFO-1 — the `lm_group` banner stayed with the struct
- The comment `// --- label-major round for the particles [g0, g0 + gN) ---` sits above `struct LmGroupBuf` in
  `island_lm_state.h:9`, as it sat above `struct GroupBuf` in the old file (line 368). The move is faithful.
- `lm_group` in `island_lm.h` therefore has no banner. Cosmetic; builder 6 may add one.

## Discipline
- Everything is under `engine_v4/src/island/` plus the README. No path is hard-coded.
- `island_bit.cpp` and `island_a.cpp` are unchanged, and `island_impl.h` remains the single include point.
