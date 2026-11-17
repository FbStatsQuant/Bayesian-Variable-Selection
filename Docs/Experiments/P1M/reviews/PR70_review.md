# Review of PR #70 (docs only): user README, REPRODUCIBILITY.md, DEV_NOTES.md

| | |
|---|---|
| **Verdict** | **ACCEPT-WITH-FIXES** |
| **Counts** | CRITICAL 0 · **MAJOR 7** · MINOR 14 |
| PR | FbStatsQuant/Bayesian-Variable-Selection #70, head `9c3d56e5`, base `exp/P1M-engine` (merge-base `caa10f0e`; the base has since moved to `eaadbbc6`, which does not touch these three files) |
| Reviewer | independent review sub-agent, read-only on the PR; no sub-agents; Owls, `nice -n 19`, at most 3 threads |
| Scope check | The diff is 3 files, all under `Scripts/SMC_BVS/engine_v4/`: README.md (rewritten), REPRODUCIBILITY.md (new), DEV_NOTES.md (new). `DEV_NOTES.md` equals the old README line for line except a new title and a 3-line preface (checked with `diff`). No file over 50 MB, no hard-coded user paths in the new text. |

Path shorthand: `E4/` = `Scripts/SMC_BVS/engine_v4/`.

**One-paragraph summary.** The documents are good: a newcomer can follow §1 and §3 A literally and get a working fit at p = 2,000 in about 8 minutes. Every timing, the island hash `0x94b566338ba911de` and every row of the same-bits table that I re-ran came out as written. The weak points are (a) the same-bits section promises somewhat more than the tests and measurements show (M1, M2), (b) three statements that are wrong when you try them (M3 mem-budget unit, M4 the SLURM first command, M5 column numbers after `prep`), and (c) two gaps a newcomer hits at once: no flag reference (M6) and no statement of which platforms pass the libm check (M7). All of these are text edits. None needs a code change to ship the guide.

---

## 1. Findings

### MAJOR

**M1. The same-bits table promises more than the tests show on "the node" and on `eval`/`post` across machines.**
Where: `E4/REPRODUCIBILITY.md:3`, `:28`, `:32-37`, `:99`; `E4/README.md:138-139` ("the same build on any machine ... gives the same value").
Evidence:
- Row 28 says changing the node gives "**no**" change, supported by "the double-precision libm was bit-equal on Owls and NOTS" and by an ISA check. The repo's own evidence is narrower. `E4/tests/PMATH_REPORT.md:47-49` says only **7 of 9** libm row hashes were equal between Owls and NOTS: `log1p` and `expm1` **differ**. `E4/include/v4/pmath.h:9-10` repeats it ("Their bits differ between Owls and NOTS").
- The self-test does not cover them (`E4/src/common/provenance.cpp:104-111`, `E4/src/common/pmath_info.cpp:70`), yet `eval` calls `std::log1p` / `std::expm1` directly (`E4/src/eval/dist.cpp:19, 69, 102, 115, 304, 476-477`). So `eval.bin` (and, through the shared code, possibly `law.bin`) non-meta sections are **not** guaranteed equal across Owls and NOTS. Line 3 ("Every command ... is a deterministic function of its input files, its parameters and its binary") and lines 32-37 ("every section of every `.bin` file except `meta`") do not carve this out. A newcomer cannot know that two hosts may disagree in the last bit of an `eval` number.
- I found no recorded run that compares an island, a merge or an eval on two different physical machines. The only cross-build comparison on record is on one node (`Docs/Experiments/P1M/results/T5_1e5.md:31`, NOTS: x86-64-v3 against sapphirerapids, same hash). The compiler also differs between the two machines the guide names (GCC 11.5 on Owls, 14.3 on NOTS, `README.md:32`), and the engine does not compare compiler versions when it admits a merge (`provenance.cpp:85-92` compares flags, libm binding and ISA family only). Compiler independence may well hold, since class A uses explicit FMA, but no document shows it.
- What I could verify (all on Owls) is listed in §3. It supports rows 1, 3, 5, 6, 7 and the resume rows fully, row 2 ("load") by runs made at a machine load average of 14-16, and says nothing about row 4 on another machine.

Fix: reword row 28 to "should be the same when the libm self-test passes; checked on Owls only for islands; **not guaranteed for `eval` and `post` across machines** because `log1p`/`expm1` differ between Owls and NOTS". Say in §1 that "same bits" is proven for `island`, `merge`, and tested by thread-count for `eval`/`post`, and that cross-machine identity of the whole pipeline has not been measured. Change `README.md:138-139` from "on any machine" to "on the same machine type (Owls: ...)". Better still: add a cross-machine measurement (Owls↔NOTS island 1 of the p = 2,000 fit, plus `eval`) to the release checklist and cite it.

**M2. The "pinned reference value" for class A is only true for the `portable` build, not for the build the README tells you to make.**
Where: `E4/REPRODUCIBILITY.md:150-162` (table `:155-158`), `:160` ("Run it alone ...").
Evidence (measured, my runs, §3): `t3_invariance` in the default test build (no `-DV4_ISLAND_ISA`, what `run_tests.sh` builds, `E4/tests/run_tests.sh:30`) prints bit `44a15bfc6fb8d233` and class A `d2df149413596a19`. The same test built with `-DV4_ISLAND_ISA=x86-64-v3` **and** with `x86-64-v4` prints class A **`e9cc4ab39f8a72db`** (bit form unchanged). The guide's own §3 says FMA and `portable` class-A bits differ by design, and README §1.2 makes `x86-64-v3` the recommended build. A newcomer who builds as told, runs the quoted command with their v3 build tree, and compares with the table sees a mismatch and will think the install is broken. The text "These values must not change in a release" does not say which build.
Fix: give both values and name the build: "class A, `portable` build: `d2df...`; FMA family (`x86-64-v3`, `x86-64-v4`, `sapphirerapids`): `e9cc4ab39f8a72db`" (add the SPR value from NOTS if known), and say how to build the test tree with `-DV4_ISLAND_ISA=...`. Add `run_tests.sh` option or CMake note if the v3 test tree is meant to be a supported path.

**M3. `--mem-budget` is documented as bytes for "every command"; for `setup` it is gigabytes.**
Where: `E4/README.md:404` ("Every command accepts `--mem-budget BYTES` and refuses before allocating ..."), `:412`.
Evidence: `E4/src/setup/setup_run.cpp:224` reads the value into `o.mem_budget_gb`; `:41`, `:55-57` compare it in GB. INTERFACES says bytes (`E4/INTERFACES.md:39`, `:527`). Run: `setup --data data.bin --out s.bin --mem-budget 1` exits 0 (read as 1 GB; at p = 300 it fits). `--mem-budget 0.000001` exits 11 with "accounted setup peak 0.17 GB > mem_budget 0.00 GB". A user who passes `--mem-budget 8000000000` for an 8 GB machine to `setup` gives it 8 billion GB, so there is no protection. Also `gen`, `prep`, `eval` and `post` do not read the flag at all (it is silently ignored, see m13). `island`, `calibrate` and `merge` take bytes (`E4/src/island/island_cmd.cpp:69-75`, `E4/src/calib/calib_run.cpp:118`, `E4/src/merge/wp4_io.cpp:1012-1014`; `--mem-budget-gb` is also accepted).
Fix: in the README, say which commands accept it and the unit of each: "`calibrate`, `island`, `merge`: bytes (or `--mem-budget-gb`); `setup`: **gigabytes**; the others: not used". Also open a code issue: `setup` breaks the INTERFACES contract (§1 line 39, §7 line 527).

**M4. The first SLURM command in §5.2 is refused as written.**
Where: `E4/README.md:253` (`export P1M_TEST_ROOT=$PWD`), `:306-307`.
Evidence: `E4/tools/slurm/p1m_driver.py:734-738` allows a path outside `$HOME/SMC_Engineering_Department` only if `P1M_TEST_ROOT` **and** `TMPDIR` are set and `P1M_TEST_ROOT` lies **inside** `$TMPDIR`; `:750-754` makes `main` print "refusing: --dept ... is outside the department folder" and return 64 otherwise. I did not run the generator (the brief says not to run SLURM sections); I called the pure function `path_allowed` from the module with the README's environment: with `TMPDIR` unset it returns `False`; with `TMPDIR` set to a parent of `$PWD` it returns `True`. So the demo works only if the reader's `$PWD` is under `$TMPDIR`, which the README never says. The generated scripts check only `P1M_TEST_ROOT` (`p1m_driver.py:358`, `:638-639`), so driver and scripts also disagree. §5.5 describes the rule incompletely ("or the directory named by `P1M_TEST_ROOT`").
Fix: in §5.2 write `export TMPDIR=<a scratch directory>; mkdir -p $TMPDIR/demo && cd $TMPDIR/demo; export P1M_TEST_ROOT=$PWD`, or relax the driver. State in §5.5 that `P1M_TEST_ROOT` must be inside `$TMPDIR`.

**M5. Variable numbers in every result are positions in `data.bin`, not columns of the user's `raw.bin`, and the guide never says so.**
Where: `E4/README.md:340` ("0-based columns of `data.bin`"), `:357-358` ("the median-probability model, 1-based"), `:377` ("1-based columns of the MPM"), `:93`.
Evidence: `prep` removes constant columns and renumbers (`E4/src/common/prep.cpp:79-81`); `data.bin` keeps the map in sections `kept` (1-based) and `dropped` (`E4/INTERFACES.md:367`). Run: a hand-made `raw.bin` with constant column 5 gives `p = 299`, `kept = (1, 2, 3, 4, 6, ...)`, `dropped = [5]`. The README's R and Python snippets then print numbers that are off by one for every column after 5, with no warning. For simulated data nothing is dropped, so the examples look right; for the user's own data (the whole point of the guide) the labels are silently wrong.
Fix: add 3 lines to §6.2: "These indexes count the columns that survived `prep`. Map them back with the `kept` section of `data.bin`: `orig <- f_data$get("kept")[pip_index]`", and show it in the R and Python snippets (the Python reader already handles int32 sections). Mention the `dropped` list in `data.bin.json` and in `prep`'s record.

**M6. There is no flag reference, and the binary's own usage text covers three commands out of ten.**
Where: whole `E4/README.md` (flags appear only inside examples); `E4/src/cli/main.cpp:19-29` (the usage text lists `gen`, `gen-test`, `prep`, `info` only; `--help` prints it and exits 13 `invalid_input`: run).
Evidence: the flags a user needs after the first fit exist only as source comments: `--N`, `--G`, `--tile`, `--ckpt`, `--ckpt-every-s`, `--stop-after-s`, `--offer-floor`, `--mem-budget-gb` (`E4/src/island/island_cmd.cpp:6-20`), `--n-draws`, `--n-x`, `--n-test`, `--rel-cut`, `--top-k` (`E4/src/eval/README_WP5.md:9-17`), setup's `--partition`, `--tau` (`setup_run.cpp:215-224`). REPRODUCIBILITY §1 names "the particle group size `G`" and "the tile size" as things you may change, but the guide never says that `--G` and `--tile` exist. `gen`'s `--a` and `--b` (in the usage text) are not explained anywhere in the guide (`--rho`, `--s0`, `--sigma` are, `README.md:397-398`). Defaults for `gen` (`rho` 0.6, `s0` 5, `sigma` 1, `b` 20, `a` 1; read from my `truth.json`) are not given either.
Fix: add a "Command reference" table to the README (command, required flags, useful optional flags with default and unit), at least for the seven flags above. Also make `smcbvs4 <cmd> --help` print the flags of that command and exit 0.

**M7. The platform requirement is stated but not qualified, and the failure message does not help.**
Where: `E4/README.md:6` ("runs on a laptop-class node"), `:35`, `:73-76`; `E4/src/common/provenance.cpp:109-110`.
Evidence: every command except `info` and `version` refuses to start unless glibc's `exp`, `log` and `lgamma` reproduce reference bits (`E4/src/cli/main.cpp:69`). The only systems measured are Owls (glibc `2.34-284.el9_8.4`) and NOTS (`E4/tests/PMATH_REPORT.md:6-7, :47`), both RHEL 9 family on Intel. The guide says "glibc 2.34" but never says "tested on RHEL 9-family x86-64 only; other distributions, other glibc versions, AMD and Arm are untested and may stop at `gen`". Reproduced refusal (`GLIBC_TUNABLES=glibc.cpu.hwcaps=-AVX2,-FMA`, exit 13): "libm self-test failed for log, log_near1, exp, exp_pos, lgamma, lgamma_int: bit-form results would differ from the reference (Owls = NOTS) bits (INTERFACES §6)". That text names two internal machines and a document the user does not have, and gives no remedy. Because the check keys on function results, a newer glibc may pass or fail; no document says which.
Fix: add a "Supported platforms" row: "Measured: Rocky/RHEL 9-family, glibc 2.34-284.el9, Intel with AVX2+FMA. If `smcbvs4 version` shows `"pass": false`, this machine cannot run the engine; use such a system or a container of one." Replace "laptop-class node" by "a single multi-core node". Improve the message ("run `smcbvs4 version`; this build needs the glibc 2.34 el9 maths library, see README §1.3").

### MINOR

**m1. Build time.** `README.md:51` says "about 5 minutes with 3 jobs". Measured: configure plus `make -j3 smcbvs4` took **57 s** wall (1 m 39 s CPU) on Owls at `nice -n 19`, machine load about 15. Say "about a minute".

**m2. `prep` does not drop duplicate columns.** `README.md:93` says "drops constant and duplicate columns". `E4/src/common/prep.cpp:79-81` drops constants only; `E4/include/v4/prep.h:31` says it is "without the duplicate check; WP2 computes duplicates in setup" (`E4/src/setup/corr.cpp:1-2`: duplicate *components*, i.e. grouped, not dropped). Fix: "drops constant columns; `setup` finds exactly duplicated columns and treats them as one group".

**m3. The `fit.json` table.** (a) `README.md:325` "When `false`, no field below exists" is wrong: `Rp`, `fit_bin`, `inputs`, `timings`, `island_isa` are always written and `hpm_F` whenever an HPM exists (`E4/src/merge/wp4_io.cpp:825-830`, `:1037`); only `logZ`, `logZ_T`, `R_eff` are conditional (`:830`). (b) `:324` names only `completed`; the other `fit_state` values are `incomplete`, `not_admitted`, `failed` (`E4/include/v4/merge.h:143`). (c) `:327` "estimated as the mean over the R′ islands" reads as the mean of `logZ_r`; the code is `LSE(logZ_r) - log R'`, the **log of the mean** of the island evidences (`merge.h:342`). (d) `max_W` is in the `fit.bin` meta, not the record (`wp4_io.cpp:775`); fine, but then the `R_eff` explanation should not suggest it is in the record. I checked all the other rows against `wp4_io.cpp` and a real `fit.bin.json`: they match.

**m4. The test-suite claim is stronger than the runner.** `README.md:151` says the suite "exits 0 only if everything passes". Without R, `run_tests.sh` skips the golden step and the competitor checks and still exits 0 (`E4/tests/run_tests.sh:51-65`; it prints "R not found: WP4 golden tests NOT RUN"). Also `:142` says R is needed for the golden comparisons, fine, but the exit-code sentence should add "(when R is installed)". I did not run the full suite (about 25 minutes); I ran the engine and the subset in §3.

**m5. "There are no floating-point atomics" (`REPRODUCIBILITY.md:63`) is literally false.** `std::atomic<double>` is used for the monotone store cut-offs (`E4/include/v4/store.h:61`, `E4/include/v4/island/store.h:153`) and `#pragma omp atomic` adds to a `double` timing counter (`E4/src/island/island_lm.h:375-377`, `E4/include/v4/island/island.h:171`). None of these feeds the science (cut-offs are monotone, the counter is a timing statistic in `meta`), which is the point of the rule. Say: "No floating-point *accumulation that enters a result* uses atomics; the store cut-offs are monotone and timing counters are statistics."

**m6. Unsourced number.** `README.md:112`: `compat` is "practical up to about p = 5,000". I found it nowhere in the engine tree or in `Docs/Experiments/P1M/`. Cite it or drop it.

**m7. Jargon and undefined terms in user-facing text.** WP numbers and review IDs are mostly absent, which is good. Remaining:
- `README.md:19` "the P1M freeze", "Status (11-17)" (month-day, no year).
- "Owls" and "NOTS" are used (`:32, :64, :69, :90, :160`) but never explained (Rice machines).
- `:73` "Class-A results" appears before "class A" is defined (only at `REPRODUCIBILITY.md:89`); `:112` and `REPRODUCIBILITY.md:86` "revision D" and "the R reference implementation" are never defined or located (`Scripts/SMC_BVS/core/`).
- `:95-96` "tempering ladder (φ-grid)", "offer floor", "particles" have no definition; `:19`/`:339` "MEASURED" is a marker the reader is never told about.
- `:336` the row "*list-PIP fields* (planned ...)" points at an internal feature the reader has not heard of; either delete it or say in one sentence what it will be.
- `REPRODUCIBILITY.md:28` "the production ISA-check task", `:162` "the freeze check", `:231` "the 10⁵ gate", `:242` "engine v0.1.25", `:174` and `E4/src/common/provenance.cpp:74` "(D-32)", test names `t3_invariance_*` (`:152`) and files `T5_AND_PILOT.md`, `T6_AND_RESTART.md`, `README_WP5.md` (README `:103, :430, :432`) are internal labels.
Fix: a 6-line glossary (SMC, particle, island, φ-grid, offer floor, class A / bit form, HPM, MPM, PIP) near the top of the README, and replace the other labels by what they are.

**m8. The smoke test does not say what success looks like.** `README.md:125-140` ends with "each command exits 0" and one hash. Nothing tells the reader the p = 2,000 fit has found the truth. I ran `eval` (27 s) and `post` (3 s) after the smoke test: `selection.hpm = mpm = [200, 600, 1000, 1400, 1800]`, `outcome_class "correct"`, `R_eff` 1.9995 of 2, island spread max sd 0.0004, `logZ` -200.38. Add these four lines and the two commands. Two smaller points: (i) `version` shows `"flags": "-O2 ... -march=x86-64-v2"` right after the reader chose `-DV4_ISLAND_ISA=x86-64-v3` (`README.md:54-58`); that is correct (the bit-form libraries are always v2, `REPRODUCIBILITY.md:85-87`) but looks wrong, say so in one line. (ii) Every command prints its whole JSON record on stdout (the binary block alone is 25 lines); say that the same text is in `<out>.json` and can be ignored.

**m9. Own data is stated as a gap (good), but the way out is hard.** `README.md:397-400` is plain and honest. However "write a `raw.bin` in the format of §5.1" needs the SHA-256 of the section table and of the header with both hash fields zeroed (`E4/INTERFACES.md:323-345`), and the contract does not give the `dims` of a 1-D or JSON section or say that `meta` is optional (`prep` reads only `X_cm` and `y`: `E4/src/common/prep.cpp:193-200`). I wrote a 25-line Python writer from §5.1 plus two guesses (`y` dims `(n, 0)`, JSON dims `(len, 0)`): `prep` accepted it (exit 0, `p = 300`). Ship that script (e.g. `tools/make_raw.py`, reading a CSV or an `.npy`) and state the dims in INTERFACES §5.1. The README does not need to promise an importer, only to give this recipe.

**m10. Discoverability and reuse.** The guide never says how to get the code (no clone URL, no branch or tag, no commit); `README.md:43` starts "From the repository root". The repository's root `README.md` does not mention `engine_v4` or `smcbvs4`, and there is no `LICENSE` file at the root, so a newcomer finds neither the entry point nor the terms of use. Suggest: a "Get the code" line (`git clone ... && git checkout <tag>`), a pointer in the root README, a LICENSE, and a citation line.

**m11. The foreign-checkpoint rule is stated plainly only in REPRODUCIBILITY.** `README.md:203-204` ("An island can be stopped and resumed (REPRODUCIBILITY.md §6)") does not say that a checkpoint written by another binary, even a rebuild of the same commit, is refused. Reproduced: stop with the `x86-64-v3` build (exit 22), resume with a different binary: exit 13, `invalid_input: checkpoint island_f.ckpt belongs to another configuration or binary` (`E4/src/island/island_run.h:631`). REPRODUCIBILITY states it well (`:181`, `:198-203`, `:236-243`). Add one sentence to README §4 "Stopping": "resume with the **same binary file** that started the island; another build is refused with `invalid_input` (exit 13). Delete the `.ckpt.a/.b` files to start over."

**m12. Error texts carry internal labels and give no remedy.** `provenance.cpp:74` ends "(D-32)"; `provenance.cpp:109-110` ends "(Owls = NOTS) bits (INTERFACES §6)"; `island_run.h:631` says "belongs to another configuration or binary" without saying what to do. The guide quotes the first one verbatim (`REPRODUCIBILITY.md:174`). Rewrite the messages and quote the new text.

**m13. Unknown flags are silently ignored (product gap, outside this PR).** `smcbvs4 gen ... --bogusflag 3` exits 0 (run). A mistyped `--mem-budgt`, `--thread 3` or `--Rp` has no effect and no warning (all arguments go into one JSON object, `E4/src/cli/main.cpp:53-66`). This combines badly with M3 and M6. The guide should warn in one sentence; a follow-up issue should make each command reject keys it does not read.

**m14. `git archive` builds record `git_commit: "unknown"` (by reading, not run).** §5.3 (`README.md:275`) builds from a `git archive` tree; `E4/cmake/git_version.cmake:3, 6-7` writes `"unknown"` when no `.git` is found (my own test was inside a git tree, so it found one and printed the commit; I could not test outside a repo without leaving my worktree). `REPRODUCIBILITY.md:107` says the commit is recorded; the manifests carry `code_commit` from the plan instead. State which one is authoritative on the SLURM path.

---

## 2. Usability walk-through (README followed literally, from a fresh clone)

Method: `git clone` of the PR head into `.rc_tmp/fresh`, then the README commands verbatim (`nice -n 19`, 3 threads, `TMPDIR=.rc_tmp/tmp`). Skipped as instructed: §4 (p = 10⁴), §5 (SLURM; read only, except the pure path check in M4).

| step | README | result |
|---|---|---|
| configure + build | §1.1 | works first time; 0 warnings; **57 s** (the text says 5 min, m1) |
| `smcbvs4 version` checks | §1.1 | `island_isa "x86-64-v3"`, `island_fma true`, `self_test.pass true`: as written. `flags` shows `-march=x86-64-v2` (m8) |
| `gen` / `prep` / `setup` | §3 A | exit 0; 1 s, 2 s, 4 s |
| `calibrate` | §3 A | exit 0; **308 s** (README: 138 s and 308 s) |
| `island` 1, 2 | §3 A | exit 0; 45 s, 46 s (README 45-48 s) |
| `merge` | §3 A | exit 0; 3 s |
| island 1 `output_hash` | §3 A | **`0x94b566338ba911de`**, equal to the README on a fresh build and a fresh clone |
| read the fit | §6.2 R and Python snippets | both work as written and print `[200, 600, 1000, 1400, 1800]` (the R one needs `../` in the path because `run2k` is a subfolder; the README writes the path from the root) |
| `eval`, `post` | §4 lines | exit 0; 27 s and 3 s at p = 2,000 |
| `info --meta 1`, section compare | REPRODUCIBILITY §4.1, §4.2 | both work as written; 27 sections, 26 non-meta |

Places where I had to guess (each is a finding above or here):
1. How to get the code and which branch (m10).
2. What a good smoke test looks like, and that `eval` is the check (m8).
3. Why `flags` says x86-64-v2 (m8).
4. Which flags exist besides the ones in the examples, their defaults and units (M6, M3).
5. That the column numbers are not the raw column numbers (M5).
6. What to do when the libm check fails, and which systems are supported (M7).
7. How to make a `raw.bin` (m9).
8. The R snippet's path assumes the working directory is the repository root, while the smoke test leaves you in `run2k`: use `source("../Scripts/...")`. One-word fix: say "from the repository root" in §6.2.
9. §3 B needs `TMPDIR` set; the README says so (good), but `$TMPDIR` is also where the build tree goes, which is not obvious from the sentence (`:150`).

Credit where due: the known gaps are stated plainly: no importer for your own data (`README.md:399`), the driver is specific to NOTS (`:299-310`, an explicit list of the three hard-coded places), and a foreign checkpoint is refused (REPRODUCIBILITY, m11 for the README side). The text is also free of WP numbers and review IDs except for the few places in m7.

---

## 3. Accuracy: claims checked against the source

Twenty-three claims; the ones that failed are findings above.

| # | Claim (document) | Source | Result |
|---|---|---|---|
| 1 | exit 0, `10 + status`; 11-16 names; 20/21/22 (`README.md:407-419`) | `E4/include/v4/status.h:11-12, 20`; `E4/src/cli/main.cpp:129-138` | ✓ |
| 2 | self-test runs before every command except `info`/`version` (`README.md:74`, `REPRODUCIBILITY.md:96`) | `main.cpp:69`; run with `GLIBC_TUNABLES` → exit 13 | ✓ |
| 3 | `portable` island refused against an `x86-64-v3` `calib.bin` (`README.md:66-68`, `REPRODUCIBILITY.md:174`) | `provenance.cpp:71-75`; run: exit 13, text equal | ✓ (text has "D-32", m12) |
| 4 | sampler seed, N, inputs must match `calib.bin` (`REPRODUCIBILITY.md:175-177`, `README.md:201-202`) | `island_cmd.cpp:222, 224, 246`; run with `--seed 2`: exit 13 | ✓ |
| 5 | foreign checkpoint → `invalid_input` (`REPRODUCIBILITY.md:181, 198-203`) | `island_run.h:631`; run: exit 13 | ✓ |
| 6 | checkpoint files `.ckpt.a/.b`, `--ckpt-every-s` default 600, `--ckpt 0` | `island_cmd.cpp:261-265` | ✓ |
| 7 | resume removes leftover `.tmp.<pid>` files | `island_run.h:592-598` | ✓ |
| 8 | soft stop: exit 22, `status completed`, `island_status interrupted_resumable`, no `island_bin` (`REPRODUCIBILITY.md:212-215`) | `main.cpp:135`; run: `stopped_after_step 6`, no island file | ✓ |
| 9 | `pip_eq`, `pip_Z`, `pip_T`, `R_eff = 1/ΣW²`, `logZ_T` lower bound, MPM = `pip_eq > 0.5` (`README.md:329, 345-349`) | `E4/include/v4/merge.h:340-364` | ✓ (`logZ` wording, m3) |
| 10 | `fit.json` fields (`README.md:321-336`) | `E4/src/merge/wp4_io.cpp:825-830, 1037`; real `fit.bin.json` | ✓ except the sentence at `:325` (m3) |
| 11 | container layout and dtype codes; Python snippet (`README.md:362-378`) | `E4/include/v4/format.h:17-31`; snippet run | ✓ |
| 12 | `K = min(p, n/2)` (`README.md:402`) | `E4/src/common/data.cpp:12` | ✓ |
| 13 | fixed chunks of 64 (`REPRODUCIBILITY.md:61`) | `E4/include/v4/threads.h:10` | ✓ |
| 14 | thread buffers absorbed in thread-index order; stage barrier serial (`REPRODUCIBILITY.md:65-67`) | `E4/include/v4/ledger.h:3, 69`; `INTERFACES.md:315, 577` | ✓ |
| 15 | `schedule_limit` is `compat`/`law` only (`README.md:417`) | `status.h:11-12` | ✓ |
| 16 | `prep` drops duplicates (`README.md:93`) | `prep.cpp:79-81`, `prep.h:31` | ✗ m2 |
| 17 | `--mem-budget BYTES` on every command (`README.md:404`) | `setup_run.cpp:224` | ✗ M3 |
| 18 | `P1M_TEST_ROOT=$PWD` suffices (`README.md:253`) | `p1m_driver.py:734-738` | ✗ M4 |
| 19 | "no floating-point atomics" (`REPRODUCIBILITY.md:63`) | `store.h:61`, `island_lm.h:375-377` | ✗ m5 (harmless in effect) |
| 20 | pinned class-A hash `d2df...` (`REPRODUCIBILITY.md:158`) | built and run | ✗ for FMA builds, M2 |
| 21 | cost example: 8 tasks, worst case 34.0 core-h (`README.md:259`) | `p1m_driver.py:60-67, 269, 284-294`: 8 + 12 + 16 + 2 + 1.33 + 2.67 | ✓ by arithmetic (generator not run); "22 files" not checked |
| 22 | SLURM facts: three `#SBATCH` lines, module load, `margin_s` default `max(300, 15%)`, 150-task cap (`README.md:303-305`, `REPRODUCIBILITY.md:257-261`) | `p1m_driver.py:54, 262, 313-321, 347` | ✓ |
| 23 | data example: five true variables at p/10, 3p/10, ... (`README.md:168`) | my `truth.json` at p = 2,000: 200, 600, 1000, 1400, 1800 | ✓ (so 1000 ... 9000 at 10⁴) |

Also confirmed: 38 driver tests (`grep -c "def test_" E4/tools/slurm/test_p1m_driver.py` = 38); 188 `TEST` cases in the C++ sources (the README says 192 measured: plausible, tagged and generated cases); links `T5_AND_PILOT.md`, `T6_AND_RESTART.md`, `PMATH_REPORT.md`, `README_WP5.md`, `tools/v4_read.R` all exist.

### The same-bits table, row by row (`REPRODUCIBILITY.md:21-30`, `:39-50`)

All "my run" results: Owls, p = 2,000, n = 200, island 1 of R′ = 2, seed 1, `calib.bin` from the smoke test.

| row | tests in the repo | my run | verdict |
|---|---|---|---|
| threads 1 / 2 / 3 | `t3_invariance_*` (1-3 threads, small fixture; passes) | `output_hash 0x94b566338ba911de` for all three; times 112 / 60 / 46 s (doc: 111 / 60 / 45) | ✓ promise = evidence |
| schedule, machine load | none directly | all my runs were at a machine load of 14-16 and agree | ✓ for load; "schedule" is not tested (the engine uses fixed `schedule(...)` clauses, so the row is true by construction but not by test) |
| `G`, tile, kernel layout | `t3_invariance_*` (7 configurations) | `--G 16 --tile 64 --threads 2`, `--G 1 --tile 128 --threads 3`, `--G 7 --tile 256 --threads 1`: same hash | ✓ |
| serial or parallel store compaction | `store_parallel_compaction_any_flush_order` (passes) | not separately run on a real island | ✓ by test |
| soft stop and resume, any number of times | `t6_restart_bit_identical`, `time_stop_chain_equals_uninterrupted` (pass) | stop at step 6, resume with 3 threads and with **1** thread: same hash; 26 non-meta section hashes equal, only `meta` differs | ✓ |
| SIGKILL and resume | `t6_kill_during_write_resubmit_and_refusal` (pass) | `kill -9` at 25 s (exit 137), resume from step 9: same hash, 26 non-meta sections equal | ✓ |
| node, if build and libm results agree | none | not testable by me (one machine) | ✗ **overclaimed, M1** |
| other seed, N, grid, r, data, ISA family, mode: changes | `merge_refuses_mixed_fma_families` (pass) | portable island vs v3 `calib.bin`: refused, exit 13 | ✓ |
| claim "x86-64-v3 = x86-64-v4 = sapphirerapids" (`README.md:64-65`) | `Docs/.../T5_1e5.md:31` (v3 vs SPR on NOTS) | x86-64-v4 build: island 1 hash `0x94b566338ba911de` against the v3 `calib.bin`; `t3_invariance` class A `e9cc4ab39f8a72db` in both v3 and v4 | ✓ (and shows M2) |
| "the five runs have five different content hashes" (`:148`) | n/a | my seven files have seven different content hashes | ✓ |
| "every command is a deterministic function" (`:3`) | `wp4_tail_threads_vs_serial`, `wp5_dist_metrics_thread_invariance_and_oracle` (pass) | `merge`, `post`, `eval` with `--threads 1` vs 3: **all non-meta sections equal** (fit 41, law 16, eval 4; and the eval JSON blocks `selection`, `pip`, `evidence`, `store`, `dist` are equal) | ✓ for thread count on one machine; across machines not shown (M1) |

The 26-section figure, the 0.04 s `--meta` reading time on a 2 GB file (`REPRODUCIBILITY.md:120`, not checked: no such file here) and the p = 10⁴ numbers (`README.md:160-195`, skipped by instruction) are unverified.

---

## 4. Completeness and honesty: other gaps

Besides M5-M7 and m9-m14:
- **What the engine cannot do is not listed in one place.** A short "Limits" box would help: x86-64 with AVX2/FMA only; one libm family; no importer; `compat` mode small p only; `merge` needs all R′ island files; a rebuilt binary orphans every checkpoint; exit 22 is not an error but also writes no `island_<r>.bin`.
- **Script-writers will trip on exit 22 and exit 20/21**: `status` is `completed` in the record for both (`main.cpp:129-135`), so a script that tests only `status` will miss them. The exit-code table says so (good); add one sentence "test the exit code, not only `status`".
- **No data-size or disk guidance.** The p = 2,000 smoke test left 165 MB in `run2k` after my extras (about 54 MB for the README commands alone); p = 10⁴ `setup.bin` is 97 MB, but the guide gives no table of disk and memory against p, n and R′ beyond one line (`README.md:402-406`).
- **`--threads` default** is `OMP_NUM_THREADS` (`README.md:105`); if neither is set OpenMP uses every core. On a shared node that matters; say so.
- **Reproducibility of the guide itself.** The README numbers are tagged MEASURED on Owls; add the engine commit they were measured at, so a later reader can tell whether they are stale.

---

## 5. Clarity

Mostly good: short sentences, a contents line, one pipeline picture, a cost table, tables for fields and exit codes. Problems: m7 (jargon list), the order of definitions (class A is used in §1.3 and defined in REPRODUCIBILITY §3), the `§` references to INTERFACES (the guide sends the newcomer to a 600-line contract for basic facts such as the container layout), and the fact that REPRODUCIBILITY.md assumes the reader has just run README §3 A in `run2k` (`:5-7`), so its commands do not run elsewhere (say so in the heading of each example, or use a variable `RUN=`).

---

## 6. Tests and commands I ran

| what | result |
|---|---|
| build, README §1.1 (`smcbvs4`) | OK, 57 s |
| README §3 A, all seven commands | OK, exit 0 each; island 1 hash as documented |
| `eval`, `post` on the smoke fit | OK |
| REPRODUCIBILITY §2 loop (1, 2, 3 threads) | hashes equal to README; section hashes equal |
| REPRODUCIBILITY §4.1, §4.2 snippets | work as written |
| REPRODUCIBILITY §6.2 soft stop and resume (3 → 3 and 3 → 1 threads), §6.3 SIGKILL at 25 s | hashes equal, `resumed_from_step` 6 / 6 / 9, 26 non-meta sections equal |
| refusal checks: portable vs v3 `calib.bin`; wrong seed; foreign checkpoint; libm mask | all exit 13 with the quoted texts |
| `merge`, `post`, `eval` at 1 vs 3 threads | non-meta sections equal |
| x86-64-v4 build of `smcbvs4`: island 1 against the v3 `calib.bin` | same hash, 16 s |
| `v4_tests` (portable, v3, v4 builds), filters `t3_invariance`, `store_parallel_compaction`, `t6_restart_bit_identical`, `t6_kill_during_write`, `time_stop_chain`, `merge_refuses_mixed_fma`, `checkpoint_of_the_older`, `checkpoint_checksum`, `wp4_tail_threads_vs_serial`, `wp5_dist_metrics_thread`, `leader_stores_deferred` | all PASS; class-A reference `d2df...` (portable) vs `e9cc...` (v3, v4) |
| hand-written `raw.bin` (25-line Python) → `prep`, with and without a constant column | OK; `kept`/`dropped` as in M5 |
| `path_allowed` of `p1m_driver.py` with the README environment | `False` unless `P1M_TEST_ROOT` is inside `TMPDIR` (M4) |
| NOT run (by instruction or cost) | §4 (p = 10⁴), the SLURM generator and stage scripts, `run_tests.sh --quick` (about 25 min), `--full` |

Build trees, run directories and logs are in `<worktree>/.rc_tmp/` (`fresh/`, `own/`, `tmp/`, `*.log`, `repro_run.sh`).

---

## 7. Sandbox compliance

- All writes under `<worktree>/.rc_tmp/`; `TMPDIR` = `.rc_tmp/tmp`; builds in `.rc_tmp/fresh/build` and `.rc_tmp/tmp/v4_build*`; nothing in the main clone or the department folder. Nothing was deleted.
- Every compute command ran under `nice -n 19`, at most 3 threads (`OMP_NUM_THREADS=3`, `make -j3`), one compute job at a time. A background repro script (`.rc_tmp/repro_run.sh`) ran alone while I read source.
- Things I did outside the worktree files, for transparency: `git fetch origin` and `git fetch origin pull/70/head` (this writes remote refs and `FETCH_HEAD` in the shared `.git`); my worktree branch `t3/review-pr70-engine-docs` is now **detached at `9c3d56e5`**; I read, read-only, the project docs under `/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/` (`results/T5_1e5.md`) and the template from a t3 checkpoint ref, because `Docs/Experiments/P1M/briefs/REVIEW_PR_template.md` is not in the PR head or in `origin/exp/P1M-engine`.
- No push, no GitHub comment, no merge, no sub-agents, no NOTS.

## 8. Suggested order of fixes

1. M2, M3, M4, M5 (each a few lines; they are plainly wrong or misleading today).
2. M1 (reword the node row and the `eval` caveat; schedule a cross-machine measurement if the claim is wanted).
3. M6, M7 (command reference, supported platforms).
4. m8, m10, m11 (what success looks like, where to get the code, the checkpoint rule in the README).
5. The rest, together with the code follow-ups: `setup --mem-budget` unit (M3), reject unknown flags (m13), clearer error texts (m12), per-command `--help` (M6).
