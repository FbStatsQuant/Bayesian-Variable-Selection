# Reproducibility: what "same bits" means, what pins it, how to check it, and how to restart

Given the same input files, parameters and binary, the commands of `smcbvs4` return the same bits whatever the thread
count, the thread schedule or a restart. This document states exactly what that guarantees and **where it has been shown**,
what it does not guarantee, and how to verify it yourself. Examples were run on Owls (a Rice University server: Intel
Xeon Gold 6148, glibc 2.34, GCC 11.5) at p = 2,000, n = 200, mode V, `--seed 1`, one island of R′ = 2; the build used
`-DV4_ISLAND_ISA=x86-64-v3`. The commands run in the directory of [README.md](README.md) §3 A (`run2k`, with `data.bin`,
`setup.bin`, `calib.bin`) and use `B=../build/smcbvs4`.

The binding statements are in `INTERFACES.md` (§5.1 file identities, §6 scorer and libm pin, §7 threads and statuses).

Contents: 1 The guarantees · 2 Threads and schedule · 3 What pins the bits · 4 Verifying hashes · 5 What the engine
refuses · 6 Stopping and restarting an island · 7 What is not guaranteed

---

## 1. The guarantees

For a fixed **build** (same ISA family, flags and libm results, §3) and fixed **inputs** (`data.bin`, `setup.bin`,
`calib.bin` and the parameters in them, the sampler seed, the island index r), on **one machine**:

| you change | the result changes? |
|---|---|
| the number of threads (`--threads`, `OMP_NUM_THREADS`) | **no** |
| the thread schedule or the machine's load | **no** (the engine's loops use fixed schedules; runs at machine load 14–17 agreed) |
| the particle group size `G`, the tile size, the kernel layout, whether store compaction runs serially or in parallel | **no** |
| stopping the island and resuming it from its checkpoint, any number of times, with any thread count | **no** |
| killing the island (SIGKILL) and resuming it from the last checkpoint | **no** |
| the sampler seed, N, the φ-grid, the island index r, the data | **yes**, by design |
| the island ISA family (`portable` against `x86-64-v3`), or `--mode` | **yes**; the engine refuses to mix them (§5) |

"The result" means two things, both compared in §4:

- the island's `output_hash` (record field, and `meta.output_hash` in the file): a hash of everything the island
  computed, its stores and its terminal state;
- the SHA-256 of **every section of every `.bin` file except `meta`**. These are the bits of the science. The `meta`
  section holds execution statistics and the binary block (§4.3), so it is allowed to differ.

**Where this is established, and what is not.**

| claim | evidence |
|---|---|
| `island`, `merge`: same bits for any thread count, schedule, `G`, tile, restart | tests in the suite and the runs below, on one machine (Owls) |
| `merge`, `post`, `eval`: same non-meta sections with 1 and with 3 threads | suite tests (`wp4_tail_threads_vs_serial`, `wp5_dist_metrics_thread_invariance_and_oracle`), one machine |
| the same build on **another machine** gives the same island bits | **not measured.** The double-precision libm functions `exp`, `log`, `lgamma` and the x87 `expl`, `logl` were bit-equal on Owls and on the Rice cluster NOTS (`tests/PMATH_REPORT.md`), and the self-test (§3) refuses a machine where they are not. No island, merge or eval has been compared across two machines. The two machines also used different compilers (GCC 11.5, 14.3), which the engine does not compare |
| `eval.bin` and `law.bin` give the same bits **on another machine** | **not guaranteed.** `eval` (and the code `post` shares with it) calls `log1p` and `expm1` directly. Those two functions differ in bits between Owls and NOTS (`tests/PMATH_REPORT.md`), and the self-test does not cover them |
| the FMA ISA families give the same class-A bits (`x86-64-v3` = `x86-64-v4`) | measured on Owls; the Rice cluster check of `sapphirerapids` against `x86-64-v3` is in `tools/slurm/T5_AND_PILOT.md` |

So: "same bits" is **shown for the island and merge pipeline across threads, schedules and restarts on one machine**.
Across machines it is expected for islands and merges when the self-test passes, and it is **not** claimed for `eval.bin` and
`law.bin`. A cross-machine comparison of a whole fit is on the release checklist, not yet done.

Measured, island 1 of the p = 2,000 fit (`output_hash`):

| run | `output_hash` |
|---|---|
| 3 threads | `0x94b566338ba911de` |
| 1 thread | `0x94b566338ba911de` |
| 2 threads | `0x94b566338ba911de` |
| 3 threads, soft stop after step 6, resumed from step 6 | `0x94b566338ba911de` |
| 3 threads, SIGKILL at 25 s, resumed from step 8 (step 9 in a second run) | `0x94b566338ba911de` |
| soft stop with 3 threads, resumed with **1** thread | `0x94b566338ba911de` |

All 26 non-meta section hashes of the island file were equal in the four re-runs; only `meta` differed. The same
properties are tested in the suite (`t3_invariance_*`, the checkpoint-resume and time-stop-chain tests) on small fixtures.

## 2. Threads and schedule

The rules that make the thread count irrelevant (`INTERFACES.md` §7):

1. **Randomness comes from addresses, never from thread state.** Every uniform is a function of an address
   (seed, role, tier, iteration, island, phase, stage, particle, position, slot) through a counter-based generator
   (Philox 4x32-10), fixed by the control flow before the value is read. Which thread draws it, or in what order,
   cannot matter (`INTERFACES.md` §3).
2. **Fixed chunks.** Work is cut into chunks whose size does not depend on the number of threads (64 items by default).
3. **Ordered reductions.** Floating-point sums that enter a result are formed per chunk and then combined serially in
   chunk order: no atomic floating-point accumulation and no OpenMP floating-point reductions. (Two harmless exceptions
   exist: the stores' admission cut-offs are monotone atomics whose timing only decides which offers are dropped early,
   and timing counters are statistics in `meta`.)
4. **Stores are order-free.** A store keeps the top-c models of everything offered, with the largest value per model; its
   content does not depend on the order or the timing of offers. Thread buffers are absorbed in thread-index order at
   step ends.
5. **The stage barrier** (weights, evidence, resampling) is serial in particle order.

Check it:

```sh
for t in 1 2 3; do
  $B island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin \
        --out island_t$t.bin --threads $t
done
python3 -c "import json; print([json.load(open('island_t%d.bin.json' % t))['output_hash'] for t in (1,2,3)])"
```

(Measured: 111 s, 60 s, 45 s; all three hashes equal, and equal to the README's island 1.)

## 3. What pins the bits

Two arithmetic forms exist, and they are pinned differently.

**The bit form** (the theory path: `compat` and `law` modes, the scorer used in `merge`, the tail local search and the
evaluator). Its results are, bit for bit, those of the R reference implementation (revision D of the code in `Scripts/SMC_BVS/core/`). It is built with
`-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2` in every build, so compiler fusing of multiply-adds is off.

**Class A** (the engineered sampler, mode V): vectorised kernels with fused multiply-add. Its bits depend on:

- **The island ISA family.** Class A uses a true FMA wherever the build has one and `a*b + c` otherwise, so FMA builds
  agree with each other and differ from `portable` by design. Measured: `x86-64-v3` = `x86-64-v4` on Owls (§4.4);
  `x86-64-v3` = `sapphirerapids` in a NOTS run recorded in `Docs/Experiments/P1M/results/T5_1e5.md`. A fit is run with **one** family end to end (`-DV4_ISLAND_ISA=...`, README §1.2).
- **The libm.** `exp`, `log` and `lgamma` come from glibc, which is *not* correctly rounded and picks its routine by CPU
  features at load time. The engine therefore binds to glibc 2.34's FMA variant and runs a self-test at the start of every
  command (except `info` and `version`): `log`, `exp` and `lgamma` on fixed argument sets, plus the x87 `expl` and `logl`,
  must reproduce reference hashes, or the command stops with `invalid_input` (exit 13). It keys on function results, not
  on the library file, so two distributions with the same results are interchangeable. Evidence and the measurement:
  `tests/PMATH_REPORT.md`; the double-precision functions were bit-equal on Owls and on NOTS.

Both are recorded in the **binary block**, written into every record and every file's `meta`:

```sh
$B version        # compiler, flags, island_isa, island_fma, git_commit, libm {path, sha256, glibc, self_test}
```

`git_commit` is the 40-hex HEAD, with `-dirty` appended if tracked files differ from it, and is refreshed at every build.
A build from a `git archive` tree has no `.git` and reports `unknown`; on the SLURM path the plan's `code_commit`, recorded
in every manifest, is then the authoritative record of the code.

## 4. Verifying hashes

### 4.1 The island hash

Every `island` record has `output_hash`, and so does the file's meta:

```sh
$B info island_1.bin --meta 1 --record info.json > /dev/null
python3 -c "import json; r = json.load(open('info.json')); print(r['verified'], r['meta']['output_hash'])"
```

(`--meta 1` reads only the header, the section table and `meta`; it takes about 0.04 s on a 2 GB island file. Without
`--meta`, `info` recomputes every section hash.)

### 4.2 The sections

`smcbvs4 info FILE` lists every section with its SHA-256. To compare two files or two machines, compare every section
except `meta`:

```python
import json, subprocess

def sections(path, binary="../build/smcbvs4"):
    subprocess.run([binary, "info", path, "--record", path + ".info.json"], check=True, stdout=subprocess.DEVNULL)
    return {s["name"]: s["sha256"] for s in json.load(open(path + ".info.json"))["sections"]}

a, b = sections("island_t1.bin"), sections("island_t3.bin")
print("differing non-meta sections:", [k for k in a if k != "meta" and a[k] != b[k]])    # → []
```

`info` also verifies the file: header and table hash, every section hash, and the file size; a corrupted or truncated
file is refused.

### 4.3 Why `content_sha256` differs between equal runs

`content_sha256` hashes the header and the section table, which holds every section hash, `meta` included. `meta` holds
execution statistics (thread count, timings, the per-step cost rows) and the binary block, so the content hash changes
with the thread count, the machine's speed and the binary. **Never use it to compare results.** Use it as a file's
*identity* (manifests and the merge use it to check that an island belongs to this `data.bin`, `setup.bin` and
`calib.bin`). Measured: the five runs of §1 have five different content hashes and identical non-meta sections.

### 4.4 The pinned reference values

The test `t3_invariance_*` runs one fixed island (n = 100, p = 300) through the particle-major reference and many
label-major configurations, 1 to 3 threads, and checks that all hashes agree. Its reference hashes, which **depend on
the build** (§3):

| form | build | reference hash |
|---|---|---|
| bit form | any | `44a15bfc6fb8d233` |
| class A | `portable` (no `-DV4_ISLAND_ISA`; what `tests/run_tests.sh` builds) | `d2df149413596a19` |
| class A | FMA family: `x86-64-v3`, `x86-64-v4` | `e9cc4ab39f8a72db` |

(MEASURED on Owls, `logZ` equal to 15 digits in both class-A builds. `sapphirerapids` is the same FMA family and is
expected to give `e9cc4ab39f8a72db`; no test tree has been built with it here.)

Run it for the build you use. The default (`portable`) test tree:

```sh
export TMPDIR=<a scratch directory>
Scripts/SMC_BVS/engine_v4/tests/run_tests.sh --quick        # builds $TMPDIR/v4_build/v4_tests (and runs the suite)
$TMPDIR/v4_build/v4_tests t3_invariance
```

and a test tree for the FMA build:

```sh
cmake -S Scripts/SMC_BVS/engine_v4 -B $TMPDIR/v4_build_v3 -DCMAKE_BUILD_TYPE=Release -DV4_ISLAND_ISA=x86-64-v3
make -C $TMPDIR/v4_build_v3 -j3 v4_tests
$TMPDIR/v4_build_v3/v4_tests t3_invariance
```

The test prints `reference hash …` for each form, and each configuration's hash. These values must not change in a release
that does not intend to change the science; the project's pre-release check compares them. If your values differ from the
row for your build, the install is not producing the reference bits.

`v4_pmath_check` (built by the suite) is the libm measurement tool: it prints a SHA-256 of `log`, `exp`, `log1p`,
`expm1` and `lgamma` on fixed argument sets, to compare across machines or `GLIBC_TUNABLES` settings, the number of results
that are not correctly rounded against 113-bit references, and the time per call.

## 5. What the engine refuses

A refusal is `invalid_input` (exit 13) with a `reason` that names the files or values involved, before any work starts.

| situation | message (excerpt) |
|---|---|
| island ISA family differs between `calib.bin` and this binary | `island: calib.bin vs this binary: island ISA families differ (x86-64-v3 vs portable): class-A bits differ (D-32)` (measured; D-32 is the project's number for this rule) |
| island sampler seed ≠ the calibration's | `--seed … differs from the calibration's seed …` |
| N ≠ calib.bin's frozen N | `N differs from calib.bin's frozen N = …` |
| `data.bin` or `setup.bin` is not the one `calib.bin` was made from | `calib.bin's meta.inputs differ from the data.bin / setup.bin in use` |
| `--mode` differs from the file's mode or the manifest's | `--mode differs from …` |
| a manifest names an input whose hash differs from the file | the job refuses to start (INTERFACES §5.3) |
| merge of islands of two FMA families, or of islands from other `calib.bin`s | refused by the merge's binary and input checks |
| restart from a checkpoint made by another binary, other inputs or other parameters | `checkpoint … belongs to another configuration or binary` (§6) |
| the libm does not reproduce the pinned results | `invalid_input` before any work (§3) |

## 6. Stopping and restarting an island

Only `island` checkpoints. `setup`, `calibrate` and `merge` take minutes to an hour; if one is killed, rerun it. A final
island at large p runs for hours, so it checkpoints.

### 6.1 Files and flags

- The checkpoint is written to `<out without .bin>.ckpt.a` and `.ckpt.b`, alternately; the newest valid generation wins
  and the other survives a crash during a write. The island removes them when it completes. For
  `--out island_s.bin` they are `island_s.ckpt.a` and `island_s.ckpt.b`.
- `--ckpt-every-s S` is the checkpoint interval in seconds (default 600). `--ckpt 0` turns checkpointing off. A write
  goes to `.tmp.<pid>`, is flushed and renamed, so a killed process leaves either the old generation or the new one, never
  half of one.
- The checkpoint holds the sampler's complete state, the per-step cost rows, and a **fingerprint**: seed, island, tier,
  N, the φ-grid, L, Hm, B, the store capacity, n and p, the offer floor, the hashes of the three input files, and the
  binary block. On start the island looks for a checkpoint. If a valid one has the same fingerprint it resumes; if the
  only valid ones have another fingerprint it **refuses** (`invalid_input`, `checkpoint … belongs to another
  configuration or binary`) rather than start over silently; with none it starts fresh. Threads, `G`, tile and kernel
  are not part of the fingerprint: **you may resume with another thread count.** To start over on purpose, delete the
  `.ckpt.a` and `.ckpt.b` files.

### 6.2 Soft stop (`--stop-after-s`)

```sh
$B island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin \
      --out island_s.bin --threads 3 --ckpt-every-s 5 --stop-after-s 12 ; echo "exit $?"        # exit 22
```

At the first step boundary after 12 s the island writes a checkpoint and exits with code **22**. This is not a failure: the
record has `status` `completed`, `island_status` `interrupted_resumable`, `stopped_after_step`, no `island_bin` and no
island file. (Measured: it stopped after step 6, about 15 s after the start.) Rerun the same command without `--stop-after-s`:

```sh
$B island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin \
      --out island_s.bin --threads 3 --ckpt-every-s 5                                          # exit 0
```

The record then says `resumed_from_step` 6, and the `output_hash` equals the uninterrupted run's (§1). Resuming with
`--threads 1` instead gives the same hash. The soft stop needs
checkpoints on (`--ckpt 0` or S ≤ 0 is `invalid_input`). Choose S below your job's time limit by a margin that covers the
step in flight and the checkpoint write.

### 6.3 Hard kill

A job killed at its time limit, a node failure or `kill -9` loses at most the work since the last checkpoint. The next run
of the same command resumes from it; if the dead process left a `.tmp.<pid>` file, the resume removes it. (Measured:
SIGKILL at 25 s with `--ckpt-every-s 5`, resumed from step 8 and from step 9 in two runs, same `output_hash`.) The kill-and-resume test used for the
p = 10⁵ release gate kills a real island twice, once during a checkpoint write, and compares the final output with an uninterrupted
run: see `tools/slurm/T6_AND_RESTART.md` (MEASURED there at p = 2,000: both kills survived, output hash equal).

### 6.4 The rule: finish on the binary that started

The fingerprint contains the binary block, whose `sha256` and git commit identify the executable. A checkpoint written by
one build is refused by another. In practice:

- Build once; run every task of a fit, and every retry, with that binary (`bin/smcbvs4`).
- Do not upgrade the code between a stop and its resume. The `restart` chain below uses the same `bin/smcbvs4` for all
  attempts.
- Layouts change too: version 0.1.25 of the engine contract (`INTERFACES.md` changelog) added a column to the per-step cost
  rows stored in the checkpoint, so a chain started on an older binary could not have been continued on the newer one even
  without the fingerprint.

### 6.5 On SLURM: the `restart` key

```json
"restart": {"attempts": 3, "margin_s": 600}
```

- `submit.sh` submits the islands array `attempts` times; attempt k+1 starts after attempt k, whatever its outcome
  (`afterany`). Merge, eval and any ISA check wait (`afterok`) for the last attempt.
- Each attempt's task passes `--stop-after-s = time limit − margin − seconds already used`, skips an island that has
  finished (`island_<r>.done`), repeats the exit code of one that failed for real (`island_<r>.failed`: a failure is not
  retried), and otherwise runs the island, which resumes from its checkpoint.
- An island still unfinished after the last attempt ends with exit 22, and merge does not start.
- `margin_s` defaults to `max(300 s, 15% of the limit)`; it must cover the step in flight and the checkpoint write.
- **Cost:** the driver counts every retry array at its limit in the worst case (Σ CPUs × limits) because it cannot know
  which islands will need one, so a `core_h_cap` set for one attempt refuses a chain. A finished island's retry task
  costs seconds, so the billed cost is the cost of the work. A chain adds `R′ × (attempts − 1)` queued tasks per fit
  (the driver caps a batch at 150 tasks).
- Without the key the plan is unchanged: one array, no soft stop.

## 7. What is not guaranteed

- **Wall time, speed, memory use, cost rows and every timing.** They vary with the machine and the load. They live in
  `meta` and in the records' `timings` and `cost` fields, and are never hashed into the science.
- **`content_sha256`** across runs (§4.3).
- **Bits across ISA families or modes.** `portable` and FMA builds differ in class A; V, `law` and `compat` are
  different methods. Neither is a bug.
- **`eval.bin` and `law.bin` across machines** (§1): they use `log1p` and `expm1`, which differ between Owls and NOTS.
- **Whole-fit identity across machines.** Not yet measured (§1).
- **Bits on an unpinned libm.** A system whose `exp`/`log`/`lgamma` give other bits is refused (§3), not silently
  accepted. A node without AVX2 and FMA would select a different glibc routine and fail the self-test.
- **Resuming across code versions** (§6.4).
- **Anything the manifest and the file hashes say differs.** If an input file changes, its hash changes and the dependent
  commands refuse it.
