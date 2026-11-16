# BUILD_COMMON — rules for every engine builder (SMC - Engineering Department, 2026-11-15)

**Paths:** the department docs are NOT in your worktree (they are uncommitted in the shared clone). Read them at
`/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/` (absolute path). Your code goes in YOUR worktree, on your
branch created by `git fetch origin && git checkout -b exp/P1M-wp<N>-<short> origin/exp/P1M-engine`.

You build one work package (WP) of the large-p SMC-BVS engine ("v4") for the p = 10⁶ experiment. The p = 10⁶ run is a
top company objective. Read, in this order:
1. this file;
2. your WP brief;
3. `Docs/Experiments/P1M/ENGINEERING_SPEC.md` **§0-v2 first** (it wins over §0–§7), then §1–§7 as reference;
4. `Docs/Experiments/P1M/PROTOCOL.md` (review, tests, labels, rollback);
5. `Docs/Experiments/P1M/INTERFACES.md` once it exists (WP1 writes it; it is the binding contract between WPs).

## Code and git
- Code lives in **`Scripts/SMC_BVS/engine_v4/`** (C++20, CMake; tests in `engine_v4/tests/`; small Python/R tools in
  `engine_v4/tools/`).
- **Never edit `Scripts/SMC_BVS/core/`** (the theorem-covered reference, v3.1 / revision D). Copy the math from it into
  `engine_v4`, citing `core/...:line` in a comment above each copied block.
- Work in your own git worktree on branch `exp/P1M-wp<N>-<short>`, created from `origin/exp/P1M-engine` (the integration
  branch).
  - Commit often; push your branch.
  - When the WP (or a reviewable slice of it) is ready, open a PR **into `exp/P1M-engine`**, never into `main`.
  - No force-push. No history rewrite. Never touch other branches.
- **Build flags**: `-O2 -fno-math-errno -ffp-contract=off` (as `core/cpp/Makevars.v3`) for every kernel that must equal
  the v3 bits; `-march=x86-64-v2` by default. Wider ISA (AVX2/AVX-512) only behind a build option, in kernels whose bit
  tests pass, or for class-A kernels.

## Tests (PROTOCOL §2)
Each PR carries:
- unit tests;
- **golden bit tests** for every function claimed bit-identical to `core/` (compare against the R/C++ reference compiled
  from `core/`, on fixed seeds);
- invariance tests where threads are involved;
- a one-command test runner: `engine_v4/tests/run_tests.sh`.

State in the PR which tests ran, on which machine, with what result. A PR without tests is not reviewed.

## Review
- The Engineering manager starts an **independent reviewer** (a different agent) for each PR, and merges into
  `exp/P1M-engine` only after the review findings are dispositioned.
- Write your PR description for that reviewer: what, why, which spec section, test evidence, known gaps.

## Machines and discipline (owner rules; POLICIES §12)
- **Owls only, for builds and tests.** At most **3 cores** per builder (`make -j3`, `OMP_NUM_THREADS ≤ 3`), always
  `nice -n 19`. Short runs; nothing multi-hour without the manager's OK.
- **Temp files**: `export TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/<YYYYMMDD>-wp<N>`. Never use `/tmp`. Never
  write anything in `/home/fb31` outside your worktree and that tmp folder. Remove your tmp folder when you finish.
- **NOTS**: none by default. If a test truly needs NOTS, ask the manager (one sequential `ssh nots`, never a job
  submission). Never touch `/projects/ml75` or `projects/BVS/Others/`.
- Labels: every performance number is MEASURED (machine, threads, command) or ESTIMATE. No unlabelled numbers.

## Company rules for agents
- Solve technical problems yourself or with the manager. No Fable or other expensive resources.
- Start no sub-agents.
- **Report big problems to the manager at once**: a spec ambiguity that blocks you, a bit test you cannot make pass, a
  design flaw. Say what happened, its impact and what you propose.
- Final message when your WP (or slice) is ready: at most 12 lines: PR link, what is in it, test results, open issues,
  measured numbers.
