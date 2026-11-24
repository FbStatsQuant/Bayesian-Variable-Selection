# Campaign freeze: the engine and the method for the p = 10⁶ campaign

Frozen 2026-11-18 (HQ order, H-14). This file is the manifest: what is frozen, how to rebuild it, and the reproduction
check that was run on the freeze tree. Binding companions: [README.md](README.md) §1 (build), [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
(what "same bits" means), [TESTING.md](TESTING.md) (the suites).

Contents: 1 The method · 2 The engine freeze commit · 3 Tree hashes · 4 Binary build and ISA · 5 Reference hashes and golden counts ·
6 Reproduction check, Owls · 7 Reproduction check, NOTS · 8 Generating the campaign plans · 9 Reproduce it

## 1. The method (what the campaign samples with)

| item | value |
|---|---|
| method tag | `method-v3.1.1-listpip` (annotated tag object `15a6d841c57fa9b66bfa46223336ebbec61f8049`) |
| method commit | `7100bb3b5a341aed5cbcd3b03fa5851a6345f0dd` (main) |
| method source | `Scripts/SMC_BVS/core/`, git tree `61b0a5822019b2737fe415ff15625e410f3227b2` |
| the same tree is on | main, the tag, `origin/exp/P1M-engine` at `af36583f8f64aba8e8d2e3c67d972960e17c0603`, and every engine commit after it |
| fixtures' reference | `tests/fixtures/MANIFEST.json`: core commit `32c90ac1…`, 20 pinned core files (the test `fixtures_pinned_reference_matches_core`) |

The tag's commit is **not** an ancestor of `exp/P1M-engine` (the branches diverged; the engine branch carries the same core
tree), so the pin is the **tree hash**, which is what the method is: `p1m_cells.py` checks the tag and the code commit both carry
tree `61b0a582…` (§8). Any later change under `Scripts/SMC_BVS/core/` changes the tree and is refused at plan generation.

## 2. The engine freeze commit

The engine freeze commit **F** is the merge commit of PR `exp/P1M-freeze` into `exp/P1M-engine` (the head of `exp/P1M-engine` that
the freeze PR to main carries). F contains this file, so F's own SHA cannot be written in it. F is recorded in the freeze PR body
to main, in the PR that creates it, and in the report to HQ; it is the **`code_commit` of every campaign plan**:

    p1m_cells.py --plans DIR --code-commit <F>      # resolves F to 40 hex, verifies the pin, writes it into all 47 plans

`git archive <F>` is what the NOTS scripts unpack and build (README §5.3), so the binary's `version.git_commit` is `unknown` and the
plan's `code_commit` is the authoritative record (REPRODUCIBILITY §3). If main squash-merges the freeze PR, F stays valid as the
commit on `exp/P1M-engine`; the trees are identical, and the content hashes of §3 identify the code whatever the merge style.

## 3. Tree hashes (git trees, `git rev-parse <commit>:<path>`)

| path | tree (first 12) | note |
|---|---|---|
| `Scripts/SMC_BVS/core` | `61b0a5822019` | the method (§1); identical at the base, F and main's tag |
| `Scripts/SMC_BVS/engine_v4/src` | `95f28676980d` | unchanged by the freeze branch |
| `Scripts/SMC_BVS/engine_v4/include` | `9deef1152baa` | unchanged by the freeze branch |
| `Scripts/SMC_BVS/engine_v4/tests` | `88fa7a5dc775` | unchanged by the freeze branch |
| `Scripts/SMC_BVS/engine_v4/CMakeLists.txt` (blob) | `3a682d988b0b` | unchanged |
| `Scripts/SMC_BVS/engine_v4/tools` | base `ef9da50a5f87` → freeze `7925c7c65921` | the freeze branch: `p1m_cells.py` (pin), `p1m_driver.py` (keys), `test_p1m_driver.py`, `slurm/freeze_check_1e5.sh` |
| `Scripts/SMC_BVS/engine_v4` | base `9476d02fc0a7` → engine_v4 at F differs by `tools/` and this file only | |

Base = `exp/P1M-engine` `af36583f`. So the freeze changes **no engine source, header, test or CMake file**: the C++ is the code
of #81 (v3.1.1 list-PIP guard, `core/` tree 61b0a582), with the plan generator and the driver extended to record the freeze
(`code_commit`, `method_tag`, `core_tree`).

## 4. Binary build and ISA

| where | recipe | ISA |
|---|---|---|
| **NOTS (production)** | `git archive <F> \| tar -x -C code`; modules `GCC/14.3.0` `CMake/3.31.8`; `cmake -S code/Scripts/SMC_BVS/engine_v4 -B build -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA=sapphirerapids`; `make -C build -j3 smcbvs4` (the driver's `build.sh`, plan key `island_isa`) | `sapphirerapids` (FMA family) on every V-mode task, `--constraint=sapphirerapids` |
| Owls (checks) | `cmake -S Scripts/SMC_BVS/engine_v4 -B build -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA=x86-64-v3`; GCC 11.5.0, CMake 3.31.8, glibc 2.34 | `x86-64-v3` = `x86-64-v4` = `sapphirerapids` bits (REPRODUCIBILITY §1) |
| test tree (`tests/run_tests.sh`) | default (`portable`, no FMA) | `portable`: class-A bits differ by design |

Bit form: `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2` in every build. libm: glibc 2.34 FMA variant,
`/lib64/libm.so.6` sha256 `c8933ed54328b293c8b005fe44161d1c73c09f96abc6d781a6c31230368d1120`; the self-test at the start of every
command must pass (`smcbvs4 version` → `self_test.pass: true`). A fit uses one binary and one FMA family end to end.

## 5. Reference hashes and golden counts

T3 reference hashes (REPRODUCIBILITY §4.4; test `t3_invariance_*`, n = 100, p = 300 fixed island):

| form | build | hash |
|---|---|---|
| bit form | any | `44a15bfc6fb8d233` |
| class A | `portable` | `d2df149413596a19` |
| class A | `x86-64-v3` / `x86-64-v4` (and `sapphirerapids`, expected) | `e9cc4ab39f8a72db` |

Smoke island (README §3 A, p = 2,000, n = 200, island 1, R′ = 2, v3 build): `0x94b566338ba911de`.
T5 10⁵ island 1 (`5-AR-n200-r01-V-s1`, sapphirerapids = x86-64-v3): `0xc4fb97717604869d` (26 non-meta sections), T5_1e5.md.

Golden counts (TESTING §2): quick suite, `tests/run_tests.sh --quick --threads 3`: **207 C++ cases** (`v4_tests`; 6 more are `full`-only), **60 driver tests**, **23 install checks**, **568,269 R golden checks** (WP4 golden vs `core/`, 0 failures), competitors harness PASS (packages missing here are normal). TESTING.md's 198 / 55 / 540,419 predate #68, #81 and the later driver tests.

## 6. Reproduction check, Owls (freeze tree; CAMPAIGN_PLAN_1117 §3 pilot rule)

Owls (owls.stat.rice.edu, Xeon Gold 6148, GCC 11.5.0, CMake 3.31.8, glibc 2.34; load average 15–32), 2026-11-18, `nice -n 19`, 3 threads, `TMPDIR` in the
department folder, freeze-branch tree (the C++ trees `src`, `include`, `tests` and `CMakeLists.txt` are identical to `exp/P1M-engine` `af36583f`, §3).

| check | result |
|---|---|
| `tests/run_tests.sh --quick --threads 3` | **SUMMARY: PASS** build 108 s · cpp 1,063 s (207 cases, 0 failed, 0 check failures) · driver 14 s (60 tests) · competitors 45 s · install 15 s (23 checks) · golden 445 s (568,269 checks, 0 failures) · total 1,690 s · exit 0 |
| driver suite again on the final tree (`--only driver`) | PASS, 60 tests (includes the freeze pin and the overlap T-arm tests) |
| T3, bit form (`v4_tests t3_invariance`, portable tree) | `44a15bfc6fb8d233` = §5 |
| T3, class A, `portable` | `d2df149413596a19` = §5 |
| T3, class A, `x86-64-v3` (own test tree, `-DV4_ISLAND_ISA=x86-64-v3`) | `e9cc4ab39f8a72db` = §5; 2 test cases, 0 failed |
| the freeze pin on the real repository | `p1m_cells.py --plans … --code-commit HEAD` verified tag, method commit and core tree 61b0a582; the 47 plans resolve `--strict` through `p1m_driver.py` |
| theory-ci `cite` step on the merge of `exp/P1M-engine` into `origin/main` | see the freeze PR to main (run before opening) |

The three T3 hashes equal the pinned REPRODUCIBILITY §4.4 values, which were measured before the pilot's code (2cfaa9e5) and have not moved; a build
of 2cfaa9e5 itself was not re-run here (its T3 values are those pinned ones). The golden suite compared the engine with the live `core/` (tree
61b0a582) bit for bit: 0 failures in 568,269 checks.

## 7. Reproduction check, NOTS (≈ 2 core-h; HQ GO 11-18; submitted by the manager, not by this branch)

`tools/slurm/freeze_check_1e5.sh` re-runs **one 10⁵ island** (island 1 of the T5 fit `5-AR-n200-r01-V-s1`) with the freeze binary on
the T5 inputs, and compares `output_hash` with the literal T5 value `0xc4fb97717604869d` and every non-meta section with the stored
`island_1.bin` (26). With `PILOT_COMMIT=2cfaa9e5…` it also runs the pilot-code binary on the same inputs (+ ≈ 2 core-h). Cost: one
island, 48 CPUs, 1:52–2:33 in T5 → ≈ 2 core-h (the limit allows 24; the builds run on the login node, not billed).

```sh
# login node (no job; needs a clone with F and, optionally, 2cfaa9e5 fetched)
CLONE=<clone> bash Scripts/SMC_BVS/engine_v4/tools/slurm/freeze_check_1e5.sh build <F> [2cfaa9e5...]
sbatch Scripts/SMC_BVS/engine_v4/tools/slurm/freeze_check_1e5.sh run        # the only billed step
cat ~/SMC_Engineering_Department/scratch/runs/FREEZE_CHECK_1e5/freeze_check.json     # verdict PASS / FAIL
```

Result: **not run** (HQ's GO covers it; the manager submits). A PASS makes the 1M pilot (2cfaa9e5) replicate 1 of the campaign; a FAIL
keeps it as pilot evidence and a fresh replicate 1 is run (MANIFEST_CELLS §1). What it does not cover: setup and calibration are
not redone (≈ 12 core-h more); the Owls golden suite covers their code against `core/`.

## 8. Generating the campaign plans

```sh
cd Scripts/SMC_BVS/engine_v4/tools/slurm
git fetch --tags origin
python3 p1m_cells.py --tsv fits.tsv --plans PLANS --code-commit <F>       # exit 65 and no files if the pin fails
python3 p1m_driver.py --plan PLANS/<plan>.json --out <dept>/scripts/<batch> --strict     # each of the 47 resolves clean
```

Expected (MANIFEST_CELLS v0.4, with the T-arm fix below): 259 fits (`fits.tsv` 260 lines, sha256
`60f36503647ae80f5f9d0bfb881dfe911a4cf1bd0772f80bb7f06d80b3476839`), **47** plans of 239 fits (v0.4 said 48: see below); every plan has
`code_commit` = F, `method_tag` = `method-v3.1.1-listpip`, `core_tree` = `61b0a582…`, `core_h_cap` = its worst case rounded up. The plan set is
deterministic: the digest of the 47 files with `code_commit` masked is `e764ec622ef0973c96408a7504bd7201870916cf866eb4ceb43a650011e86625` (printed
by `p1m_cells.py --plans`, whatever F is). The driver copies `code_commit`, `method_tag` and `core_tree` into every run manifest.

**The 10⁴ overlap T arm (blocking fix at the freeze; OVERLAP_1e4_SUBMISSION_PLAN §1–2).** v0.4 emitted the 20 T fits (law mode) as N = 2,500,
R′ = 16 with V-sized limits. The T arm is **N = N0 = max(2500, n, p) = 10⁴, R′ = 4, coded calibration** (EXPERIMENT_PLAN A1, D-26). The engine
sets N itself in theory mode (`calibrate`: `Budgets::N0`, tier 1 = 4·N0 on escalation; `island` and `merge` read N from `calib.bin`, an explicit
different `--N` is refused, the manifest's N is not read), so N in the plan is the tier-0 record and `expand()` asserts it (`check_theory_arms`);
R′ = 4 does change the work (4 island tasks, 4 merge inputs). The T plans now carry the T limits (setup 8 CPU/8G/0:15, calibrate 48/16G/**3:00**,
islands 24/16G/0:45, merge 8/8G/0:20, eval 8/8G/0:30; `max_task_hours = 3.0`, a one-off exception to the 2-h rule that needs HQ's acceptance) and the V
overlap plans the V shapes (setup 8/8G/0:15, calibrate 16/8G/0:30, islands 4/4G/0:30, merge 8/4G/0:15, eval 8/8G/0:20): worst case 224.7 core-h per T
fit and 46.7 per V fit. The planning cost of the rung is unchanged (T = 115 per fit, 2,500 for the 40 fits). Because a T fit is now 8 tasks, 18 fits per
150-task batch, so T is 2 plans (18 + 2 fits) and the campaign is 47 plans, not 48. Other blocks keep the driver's default shapes. Test
`test_overlap_t_arm_and_shapes`.

## 9. Reproduce the freeze check

```sh
export TMPDIR=/home/$USER/SMC_Engineering_Department/tmp/freeze          # inside the department folder; no "scratch" in the path
nice -n 19 Scripts/SMC_BVS/engine_v4/tests/run_tests.sh --quick --threads 3     # §6: all six suites PASS (≈ 26–40 min on a loaded Owls)
cmake -S Scripts/SMC_BVS/engine_v4 -B $TMPDIR/v4_build_v3 -DCMAKE_BUILD_TYPE=Release -DV4_ISLAND_ISA=x86-64-v3
make -C $TMPDIR/v4_build_v3 -j3 v4_tests && $TMPDIR/v4_build_v3/v4_tests t3_invariance      # class-A FMA reference e9cc4ab39f8a72db
```
