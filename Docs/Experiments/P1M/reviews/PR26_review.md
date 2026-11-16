# PR #26 review: WP3 slice 3 (per-round counters, socket mode, G = 256 with budget, near-stationary 10⁶, products blocking)

Reviewer: Opus 5.5 (high), independent of the author. Date: 2026-11-16.
- Branch: `exp/P1M-wp3-island4` @ `32b11a91`. Reviewed diff: `exp/P1M-wp3-island3` (`9466489d`)..`32b11a91`, 5 files,
  +143/−27.
- Commits: `efc0dfd0` (slice 3), `c6dd554d` (bench env order and socket check), and a merge of `9466489d`.
- Contract: INTERFACES v0.1.9. Design: WP3_DESIGN. Spec: §0-v3.
- Read-only: detached worktrees under the department tmp folder (removed after). Nothing was pushed or commented.

## Verdict: **FIX FIRST** (one small fix in the bench script; the engine change is mergeable as it stands)

**The products blocking is bit-identical.**
- By reading: every lane does the same sequence of additions.
- By a randomised check: 440,256 entries are bit-equal to the old loop and to a scalar reference, at x86-64-v2 and
  x86-64-v4.
- In the island: block 1 and block 4 give the same output hash in both forms, at 1 and 3 threads.

**Tests: 69 of 69 pass** at `32b11a91`.

**One MAJOR finding:**
- **B1.** The scripted `g256` mode is refused by the admission at p = 10⁶ from this head. MEASURED: status 3, plan
  99,491 MiB > 60 GiB. The G = 256 lever therefore cannot be measured from this commit.

**One performance surprise (B2):** block 4 is the new default for every build, and it is **slower** in the default
x86-64-v2 build (+17 %). It is faster only with AVX-512 (−27 %).

Counts: CRITICAL 0 · MAJOR 1 · MINOR 3 · nits 3.

## Test runs (Owls, Xeon Gold 6148, load 21–30, gcc 11.5.0, `nice -n 19`, ≤ 3 threads)
1. **`tests/run_tests.sh --build-dir …/b4`**: **69 test cases, 0 failed**, exit 0. `git_commit` = `32b11a91…`.
   - T3 hashes are unchanged: bit `44a15bfc6fb8d233`, A `d2df149413596a19` (default build).
   - The PR body says "65 of 65", which is stale; the #24 merge brought 69.
2. **Unit bit check of `tile_products`** (reviewer `chk/tp.cpp`):
   - Inputs: 400 random cases with n ∈ [1, 260], nA ∈ [1, 13] (every nA mod 4 remainder) and Bk ∈ {64, …, 256}. Values
     span 10^±20 and include −0, denormal_min, 1e308 (overflow to inf) and NaN.
   - Block 1, block 4 and a scalar `s = s + x_a[i]·x_j[i]` loop are compared bit by bit.
   - Result: **0 mismatches in 440,256 entries**, built with `-O2 -ffp-contract=off` at `-march=x86-64-v2` and at
     `-march=x86-64-v4`.
3. **Island A/B through the bench** (`v4_bench_island island 20000 300 1,3 {A,bit} lm 64 128 geo:4 1 1`,
   `V4_PRODUCTS_BLOCK` = 1 vs 4):

   | build | form | block 1 hash (threads 1, 3) | block 4 hash (threads 1, 3) | products ns per pair, block 1 → 4 (thread-time) |
   |---|---|---|---|---|
   | default (x86-64-v2) | A | `9153c1f05c8ef1e8` ×2 | `9153c1f05c8ef1e8` ×2 | 190 → 223; repeat 196 → 231 |
   | default (x86-64-v2) | bit | `f9c6272ed1ffbae5` ×2 | `f9c6272ed1ffbae5` ×2 | 181 → 221 |
   | `V4_ISLAND_ISA=x86-64-v4` | A | `263474601a55acb1` ×2 | `263474601a55acb1` ×2 | 44 → 32; repeat 44 → 32 |

   MEASURED. The hashes are identical within each build. Class A differs across ISAs, as already known.
4. **`g256` admission at 10⁶** (B1): `V4_MEM_BUDGET_GB=60 v4_bench_island island 1000000 2500 3 A lm 256 128 steps:1 2 2`,
   run under `timeout` and `ulimit -v`. It printed `status=3`, the plan `… store=90170MiB … total=99491MiB (G=256,
   k=114.288654)`, and exited with rc 0. The data build took ≈ 40 s; nothing was allocated for the island.

## Products blocking: bit-identity proof (focus item)

`kernel.h` `tile_products`, block 4:
- For each group of 4 active columns and each 32-label chunk, there are 16 `v8d` accumulators. Each starts at `bc(0)` and
  is updated as `a_rc = a_rc + b_r * x_c` for i = 0..n−1 in order. Here `b_r = bc(x_r[i])` and `x_c = load8(rp + 8c)`,
  the same tile row as the old loop.
- Per lane (column a, label j), the operation sequence is s₀ = 0, then s ← s + (x_a[i] · x_j[i]) for i = 0..n−1. This is
  exactly the old block-1 loop's sequence: `s0 = s0 + xi * load8(rp)` with `xi = bc(xa[i])`.
- The vector multiply and add are lane-wise IEEE operations. `-ffp-contract=off` is set in `V4_BIT_FLAGS` and `V4_A_FLAGS`
  (`cmake/flags.cmake`), and the `V4_ISLAND_ISA` override only changes `-march`. No FMA contraction or reassociation is
  possible.
- Only *which* lanes share a register and the loop nesting change. The values and their order per lane do not.
- Edges:
  - Bk is always a multiple of 64 (`Bk = max(64, ⌈tile/64⌉·64)`), so the 32-label chunks tile it exactly.
  - The nA mod 4 remainder falls through to the unchanged block-1 loop.
  - The output layout `P[a·Bk + jj]` is the same, and padding lanes of the last tile multiply zeros, as before.
  - `products_block` is not in the fingerprint or the checkpoint. That is correct, because it does not change outputs.
- So the blocked products are **bit-identical** for every input, NaN payloads included (check 2).

## Findings

### MAJOR

**B1. From this head, `nots_bench_island4.sh g256` is refused at p = 10⁶, so the G = 256 lever produces no measurement.**
- Where: `tools/nots_bench_island4.sh` (`g256)  V4_MEM_BUDGET_GB=60 run_single … 256`), `tools/bench_island.cpp`
  (`V4_MEM_BUDGET_GB` now applied, no `k_store`), and `run_island`'s `k_est = max(8, 2·E_π₀|S| + 2)`.
- Evidence (MEASURED, test run 4):
  - The bench's stand-in π₀ at 10⁶ gives k_est = 114.3.
  - With #24's upper-bound plan, the store term alone is 88 GiB, and the plan is 97.2 GiB at 3 threads (it is larger at
    96).
  - Result: `status=3`, refused before allocation. The script continues, and the exit code is 0.
  - At the true stored size (k ≈ 7, job 2748105), the same plan is **21.7 GiB** (G = 256, 96 threads), well inside the
    budget.
- The submitted batch 2748756 (built at `efc0dfd0`, with the pre-#24 formula) is ESTIMATE-admitted: its plan at
  k = 114.3 and 96 threads is **59.60 GiB vs a 60 GiB budget**, a margin of 0.4 GiB.
  - So that batch should run G = 256.
  - Any re-run from `32b11a91` or later will not.
  - If the batch had used 192 threads, its plan would be 65.1 GiB, and it would be refused.
- Fix (small):
  - Add `V4_K_STORE` to the bench (→ `IslandConfig::k_store`) and set it in the `g256` mode, for example `V4_K_STORE=8`
    (the stored mean |S| measured at 10⁶ is 6–8). Alternatively, size the budget from the printed plan.
  - Make the bench return non-zero when `status != 0`, so that a refusal fails the step visibly.
  - See also PR24_recheck r1, the engine-side version of this issue.

### MINOR

**B2. `products_block = 4` is the default in every build, but it is slower in the default x86-64-v2 build.**
- Where: `island.h:56` (`int products_block = 4`) and `kernel.h` `tile_products`.
- Evidence (MEASURED, test run 3):
  - Default build: 190 → 223 and 196 → 231 ns per pair, about +17 %.
  - `x86-64-v4` build: 44 → 32 ns per pair, about −27 %.
- Cause: 16 `v8d` accumulators plus 4 row and 4 broadcast vectors need about 24 vector registers. AVX-512 has 32 zmm
  registers, while SSE4.2 has 16 xmm registers holding 2 doubles each, so x86-64-v2 spills.
- The PR's "118 → 77 ns" does not name its build. The NOTS script builds `sapphirerapids`, so production is not
  affected.
- Fix: default `products_block` to 4 only `#if defined(__AVX512F__)` in the island translation unit, else 1. Or keep 4,
  but state the ISA dependence in the field comment and the PR, and name the build next to every ns figure.

**B3. Robustness gaps in the socket mode.**
- `[[ -z "$h1" || "$h1" == "$h2" ]]` does not catch an empty `h2`. If island 2 printed no hash, the check reports
  "distinct". Add `-z "$h2"`.
- `for pid in "${pids[@]}"; do wait "$pid"; done` under `set -e` exits at the first failed island. The other island is
  left running in the allocation, and the logs are not printed. Collect the exit codes, wait for both, print both logs,
  then fail.
- A refused or failed island (status 2 or 3) exits 0 and still prints an "output hash", so the distinct-hash check can
  pass on two refusals. Grep `status=0` too.

**B4. The script does not enforce the NOTS path rules.**
- Verified: there is no `/tmp` and no hard-coded path.
- But the script neither sets nor checks `TMPDIR`. gcc's temporaries during the in-job build go to the node's default
  (`/tmp`), which is against the department rule "TMPDIR via the scratch link" (WP5 brief item 4, BUILD_COMMON).
- The logs are written as siblings of an arbitrary build directory (`$build.cmake.log`, `$build.socket<id>.log`).
- Fix:
  - Refuse unless `TMPDIR` is set and the build directory lies under `~/SMC_Engineering_Department/` or
    `/scratch/fb31/SMC_Engineering_Department/`, as `run_tests.sh` does for TMPDIR.
  - Or `export TMPDIR="$build.tmp"`, create it, and remove it at exit.
  - Put the logs inside `$build/`.

### Nits
- The `[round]` line labels `pairs/steps·m/p` as "per step". That value is pairs per (particle-round · p), the same
  quantity as the summary's "pairs per particle-round / p". Rename the label.
- PR body: "65 of 65" should read 69 of 69 at `32b11a91`. Also name the build next to "118 → 77 ns".
- `bench_kernel` reads `V4_PRODUCTS_BLOCK` into a function-local `static` (once per process), while the island path
  reads it per run. This is harmless, but the two should be read the same way.

## Other checks
- Merge integrity:
  - `9466489d..32b11a91` touches only `island.h` (+1 field), `kernel.h` (+`tile_products`), `island_impl.h` (the call
    and the verbose block), the bench and the new script.
  - All #24 fixes are intact (69/69, T3 unchanged).
- Per-round counters: the deltas come from `ks_prev`, and compaction time from `top.t_compact`. These are verbose-only,
  and outputs are unaffected.
- Socket mode logic:
  - Socket groups come from `sched_getaffinity` ∩ `lscpu -p`, and the mode refuses unless there are exactly 2 groups.
  - `V4_ISLAND_ID` is applied after the defaults (`c6dd554d`), so the address keys differ.
  - Binding uses `OMP_PLACES` per CPU, `taskset`, and `numactl` when present.
  - A function-prefixed `V4_PRODUCTS_BLOCK=1 run_single` is exported to the child (bash; checked).
- The near-stationary mode uses `steps:1` (φ: 0 → 1 in one stage), then L = 2 and Hm = 2. This matches the brief.
- Discipline: all changes are under `engine_v4/`, `core/` is untouched, and there are no large files. The cost
  estimates in the script header are labelled ESTIMATE.
