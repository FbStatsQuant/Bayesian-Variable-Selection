# Errors, statuses and exit codes of `smcbvs4` and its SLURM driver

This is the catalogue of how the engine and its job scripts fail, what each failure means and what to do about it. It is
written from the source at commit `c8a30d39`. Every message below is quoted as the program prints it, with the source
file and line that produces it; the ones marked **(run E17)** were triggered for real on Owls and their actual output is in
Appendix A. Line numbers drift with the source: the companion file [ERRORS_ALL_SITES.md](ERRORS_ALL_SITES.md) lists all 496
`throw` sites and the non-throw reasons, generated from the same commit, so you can look up a message that is not here.

Contents: 1 Reading an error · 2 Exit codes · 3 Statuses and their causes (3.1 resource_limit · 3.2 numerical_failure ·
3.3 invalid_input · 3.4 io_error · 3.5 internal_error · 3.6 schedule_limit · 3.7 completed with exit 20, 21, 22) ·
4 Driver and script exits · 5 Failures the engine cannot report · 6 Messages to improve · Appendix A Real runs ·
Appendix B How the real runs were made

Paths are relative to `Scripts/SMC_BVS/engine_v4/`.

---

## 1. Reading an error

Every `smcbvs4` command ends the same way (`src/cli/main.cpp:117-139`):

1. It prints its **record** (a JSON object) on stdout and writes the same text to `<out>.json`. On failure the record
   has `"status"` (a name such as `invalid_input`) and `"reason"` (the message). The message always starts with the status
   name and a colon: `invalid_input: cannot open nonexistent.bin`.
2. It exits with **0** for `completed`, **10 + status number** for a failure (§2), or 20, 21, 22 for three outcomes that
   are not failures.
3. For a command-line mistake it also prints the usage text on stderr (only for no arguments and an unknown command, E01
   and E02). Nothing else is written to stderr.

So: **test the exit code first, then read `reason` in the record.** A failed command writes no output file of its own
(`fit.bin`, `calib.bin`, …), only `<out>.json`; no estimate is ever written for a failed fit ("GUARD-W", the rule that a
fit that did not complete carries no estimates). The one exception is an `island` that is *not admitted* by
`--mem-budget`: it writes an island file with the status `resource_limit` and no estimate sections
(`src/island/island_cmd.cpp:284-292`).

The record is the place to look for details the one-line message omits: `binary` (which build ran), `inputs` (hashes of
the files it read), `mem_plan` for admission refusals.

Three things people trip over:

- **`status` is not enough.** For exit 20, 21 and 22 the record says `"status": "completed"`; only the exit code and the
  fields `prep_status` / `island_status` tell them apart from success (§3.7).
- **An unknown flag is silently ignored** (`gen … --bogusflag 3` exits 0). A typo such as `--thread 3` or `--mem-budgt`
  changes nothing and says nothing; see the flag table in README.md §7.
- **Opening a missing file for reading is `invalid_input` (13); creating a file that cannot be created is `io_error` (14).**
  The status follows what the code was doing, not what the operating system said (E05, E07).

---

## 2. Exit codes

| exit | name | where it comes from | meaning |
|---:|---|---|---|
| 0 | `completed` | engine | success (or a fit-level outcome the record explains: check `fit_state`, README §6.1) |
| 1 | — | `tools/slurm/*.py`, generated isa-check script | a Python tool failed: an uncaught exception (for example D07: a missing plan file prints a traceback), a `SystemExit` with a message (`p1m_manifest.py`, D13), or a comparison that found a difference (`p1m_stage_cost.py isa`, `p1m_t6.py`, the generated ISA check, `tools/slurm/p1m_driver.py:550`) |
| 2 | — | `tests/run_tests.sh:9,17` | the test runner was started wrongly: no `TMPDIR`, or an unknown option (D14) |
| 11 | `resource_limit` | engine | not admitted by the memory budget, out of memory, or a graph too large (§3.1) |
| 12 | `numerical_failure` | engine | a model's score could not be computed (§3.2) |
| 13 | `invalid_input` | engine | the command line, a file or a combination of files was refused (§3.3). By far the most common failure: 384 of the 496 throw sites |
| 14 | `io_error` | engine | a file could not be created, written, flushed or renamed (§3.4) |
| 15 | `internal_error` | engine | an internal check failed (§3.5). Report it |
| 16 | `schedule_limit` | engine | calibration of the `compat`/`law` modes found no grid; never raised by mode V (§3.6) |
| 20 | `completed` | `smcbvs4 prep` | `prep_status` = `no_predictors`: every predictor is constant; no `data.bin` is written (E30) |
| 21 | `completed` | `smcbvs4 prep` | `prep_status` = `y_constant`: the response is constant; no `data.bin` is written (E29) |
| 22 | `completed` | `smcbvs4 island` | `island_status` = `interrupted_resumable`: a soft stop wrote a checkpoint (`--stop-after-s`); not a failure; rerun the same command to resume (E26) |
| 64 | — | `p1m_driver.py:755`, generated `submit.sh`, `build.sh` | **refusing to run**: a path is outside the department folder, or `CONFIRM=yes` is not set (D08, D09, D12) |
| 65 | — | `p1m_driver.py:764` | **plan error**: the plan JSON failed validation (D01–D04, D06) |
| 66 | — | generated scripts | **FATAL precondition**: scripts differ from `SHA256SUMS`, a binary or a scratch directory is missing, GCC 14.3.0 is not loaded (D10, D11) |
| 137 | — | the operating system | the process got SIGKILL: the SLURM memory limit (out-of-memory kill), `scancel`, or the time limit (§5) |
| 143 | — | the operating system | SIGTERM: `scancel` or the scheduler stopping the job |
| 139 | — | the operating system | SIGSEGV: a crash. This is a bug; keep the input files and report it |

Mapping for the engine: `exit = 10 + status` (`include/v4/status.h:17`), with the status numbers
`resource_limit` 1, `numerical_failure` 2, `invalid_input` 3, `io_error` 4, `internal_error` 5, `schedule_limit` 6
(`status.h:14`). A failure while writing the record itself turns a `completed` run into `io_error`
(`src/cli/main.cpp:137-138`).

In the SLURM stage scripts, an island task repeats the engine's exit code; with the `restart` plan key a finished island
is skipped, a failed one repeats its code (and is not retried), and exit 22 means "attempt ended cleanly, resume next"
(`tools/slurm/p1m_driver.py:413-429`).

---

## 3. Statuses and their causes

For every cause: the message as printed (`…` is a value filled in at run time), where it comes from, what it means, and
what to do.

### 3.1 `resource_limit` (exit 11): not enough memory, or refused up front

The engine plans its memory before allocating. Over budget it stops **before** any allocation, writes the record and
exits 11, so nothing is half-written. The budget flag is `--mem-budget` with a **different unit per command** (README §7):
bytes for `calibrate`, `island`, `merge`; **gigabytes** for `setup`; not read by `gen`, `prep`, `eval`, `post`.

| message | source | cause and action |
|---|---|---|
| `resource_limit: admission: accounted setup peak 0.04 GB > mem_budget 0.00 GB (C = …, J = …, B_blocks = …)` | `src/setup/setup_run.cpp:55-58` **(run E13)** | `setup` needs more than `--mem-budget` (**GB**). Raise it, give more memory to the job, or use `--count-only 1` to see the needed amount first |
| `resource_limit: admission: exact partition needs 8 p^2 = … GB > limit … GB (use partition=truncated)` | `setup_run.cpp:40-45` | `--partition exact` builds a dense p×p matrix. Use the default truncated partition for large p |
| `resource_limit: calibrate not admitted: calibration state … B >= --mem-budget` | `src/calib/calib_run.cpp:160,168` **(run E14)** | the calibration's resident state alone does not fit in `--mem-budget` (**bytes**). Raise it; `calibrate --plan-only 1` prints the plan |
| `resource_limit: calibration island not admitted (N-1): resident + island plan … B > --mem-budget` | `calib_run.cpp:163,174` | the state plus one calibration island does not fit. Raise the budget |
| `resource_limit: mem_budget: predicted peak 59 MiB > budget 0 MiB [inputs=… x_tiles=… store=… worker_bufs=… … total=59MiB (G=1, k=8.000000)]` | `src/island/island_cmd.cpp:281-292`, `island_run.h:375,994` **(run E15)** | the island's plan (the bracket lists every term) exceeds `--mem-budget` (**bytes**). Raise the budget or lower `--G` (fewer particles per group); an `island_<r>.bin` with status `resource_limit` is written. `island --plan-only 1` prints the plan without running |
| `resource_limit: merge not admitted: estimated peak … B > --mem-budget … B` | `src/merge/wp4_io.cpp:1093,1134` **(run E16)** | the merge's plan exceeds the budget. Raise `--mem-budget` (bytes) or `--mem-budget-gb`; at p = 10⁶ the merge is the largest task (README §8) |
| `resource_limit: correlation_pass: more than max_edges edges (hub design); raise max_edges` | `src/setup/corr.cpp:120,159` | one variable (a "hub") is correlated with a huge number of others, so the correlation graph is too large. Pass a larger `--max-edges`, or check the design for duplicated or near-duplicated columns |
| `resource_limit: correlation tiles: out of memory`, `edges_by_filter: allocation failed` | `src/setup/tiles.h:111`, `src/setup/account.cpp:228` | `setup` ran out of memory inside its tile or filter step. Give the job more memory |
| `resource_limit: out of memory` | `src/cli/main.cpp:121-122`, `island_run.h:859,862`, `setup_run.cpp:72` | a `std::bad_alloc` anywhere. The operating system refused an allocation. Give the job more memory, or set `--mem-budget` so that the engine refuses up front with a message that names the plan |
| `… out of memory inside a parallel region` | `src/island/island_pm.h:150` | the same, inside the sampler's parallel loop (the island ends with status `resource_limit`) |
| `resource_limit: runtime guard after the final local search`, `… after LS0` | `include/v4/merge.h:356,369` | the merge's memory guard tripped late. Raise the budget |

An out-of-memory *kill* by SLURM looks different: the process just disappears with exit 137 (§5).

### 3.2 `numerical_failure` (exit 12)

A model's marginal likelihood could not be computed even after the engine's three fallbacks (Cholesky, refactor,
augmented QR). It depends on the data, not on the command line. It has not been triggered here (the engine is built to
avoid it: infeasible models are never scored).

| message | source | cause and action |
|---|---|---|
| `numerical_failure: score failed after Cholesky, refactor and augmented QR for a model of size …` | `src/common/score.cpp:166` | the design matrix of that model is numerically singular. Look for exactly or nearly duplicated or collinear columns, a degenerate response, extreme scaling. Keep the record and the input files |
| `numerical_failure: <phase> <stage>, particle …, position …: Gibbs label …: score failed after Cholesky, refactor and augmented QR` | `src/island/island_run.h:196-206` | the same, inside an island; the message names the stage, particle and variable, which the developers need |
| `numerical_failure: NaN score in the local search` | `include/v4/tail.h:131,149` | the final local search of `merge` scored a model as NaN. Same advice |

### 3.3 `invalid_input` (exit 13): the input is refused

The commonest status. It means "fix the command, the files or their combination, then rerun"; nothing was run. The causes
group as follows.

#### 3.3.1 The command line

| message | source | cause and action |
|---|---|---|
| (usage text on stderr) and exit 13 | `src/cli/main.cpp:39` **(run E01)** | no command given. The usage lists only `gen`, `prep` and `info`; see README §7 for all commands |
| `invalid_input: unknown command …` + usage | `main.cpp:117` **(run E02)** | misspelled command. Commands: `gen gen-test prep setup calibrate island merge eval post info version` |
| `invalid_input: bad argument …` | `main.cpp:55` **(run E03)** | a flag with no value, or a value without `--` before it. Flags are `--name value` pairs |
| `invalid_input: json: missing key seed` | `src/common/json.cpp:24` **(run E04)** | a required flag is missing; the message names the key but not the command or the flag. For `gen` the required flags are `--design --n --p --seed --out` |
| `invalid_input: json: not a number` | `json.cpp:36` **(run E36)** | a flag that must be a number got text (here `--n abc`). The message does not say which flag |
| `invalid_input: unknown design XYZ` | `src/common/gen.cpp:21` **(run E37)** | `--design` must be `IND`, `AR`, `BLK` or `ADJ-OPP` |
| `invalid_input: gen: rho must be in [0, 1)`, `gen: s0 in 0..min(5, p)`, `gen: need n >= 3, p >= 1, seed in [1, 2^31-1]`, `gen: b >= 1`, `gen: ADJ-OPP needs s0 >= 2 and p >= 10`, `gen: truths do not fit in p columns` | `gen.cpp:36-40,62` **(runs E38, E39)** | a `gen` parameter out of range; the message gives the allowed range, not the value you passed |
| `invalid_input: calibrate: --threads must be a whole number in [1, 4096]`, `island: --G must be a whole number in [0, 256]`, `island: --stop-after-s must be a number > 0`, `merge: --mem-budget must be a number`, `setup: partition must be truncated or exact` | `calib_run.cpp:48-51`, `island_cmd.cpp:54-57,306`, `wp4_io.cpp:1053` (budget parsing), `setup_run.cpp:217` **(runs E40–E44)** | a numeric or choice flag outside its range. Each message names the flag and the range |
| `invalid_input: calibrate: --mode must be compat, law or V`, `island: --mode must be compat, law or V`, `merge: mode not given (--mode or the manifest's mode)` | `calib_run.cpp:112`, `island_cmd.cpp:103`, `wp4_io.cpp:1024` **(runs E35, E48)** | `--mode` is required by `calibrate`, `island` and `merge` and must agree across the three |
| `invalid_input: calibrate: --seed is required (a whole number in [1, 2^31 - 1])`, `island: --seed is required (…)`, `island: the island index is required (--island r, …)` | `calib_run.cpp:179`, `island_cmd.cpp:211-213` **(run E21)** | a required flag is missing |
| `invalid_input: calibrate: --I_max / --refine_m apply to the bounded rule (mode V) only` | `calib_run.cpp:116` **(run E34)** | these two flags only exist in mode V |
| `invalid_input: eval: --fit, --data, --truth and --out are required`, `post: --fit, --data and --out are required` | `src/eval/run.cpp:102`, `src/post/law.cpp:173` **(run E32)** | missing required flags |
| `invalid_input: info: the file is required (info FILE, or --in FILE)` | `main.cpp:92` **(run E46)** | `info` needs a file |
| `invalid_input: give --mem-budget or --mem-budget-gb, not both` | `island_cmd.cpp:70`, `wp4_io.cpp:1052` | choose one of the two spellings |
| `invalid_input: island: --role must be final (pilot and diagnostic islands run inside calibrate)` | `island_cmd.cpp:128` | `--role` is only for the driver; leave it out |
| `invalid_input: run_island: stop_after_s needs a checkpoint path and a final island` | `island_run.h:969` **(run E28)** | `--stop-after-s` with `--ckpt 0`. A soft stop needs checkpoints; drop `--ckpt 0` |
| `invalid_input: run_island: G must be in 0..256 …`, `run_island: the offer floor …`, `run_island: compat mode needs … 1 thread …` and the other `run_island:` checks | `island_run.h:952-984` | the island's own configuration checks; most can only be reached through a manifest or the test hooks. Read the message; it names the rule |

#### 3.3.2 Files: missing, damaged, of the wrong kind

| message | source | cause and action |
|---|---|---|
| `invalid_input: cannot open nonexistent.bin` | `src/common/format.cpp:104` (container), `src/common/prep.cpp:153` **(runs E05, E45)** | the path does not exist or cannot be read. Check the path and the working directory |
| `invalid_input: data.bin is not a raw file`, `… is not a data file`, `…: not a calib file`, `…: not a setup file`, `…: not an island file`, `…: not a fit.bin (kind != 6)`, `…: not a law.bin (kind != 7)` | `prep.cpp:195,124`, `island_cmd.cpp:139,228`, `wp4_io.cpp:323,715,704`, `island_file.cpp:85`, `src/eval/io.cpp:15`, `src/post/law.cpp:129` **(runs E06, E33, E47)** | the file is a valid engine file of the wrong kind: the arguments are in the wrong order or point at the wrong stage's output. The pipeline is `raw.bin → data.bin → setup.bin → calib.bin → island_<r>.bin → fit.bin` |
| `invalid_input: file too short: err.txt` | `format.cpp:108` **(run E08)** | not an engine file at all (shorter than the 128-byte header) |
| `invalid_input: bad magic: …`, `unsupported format version: …` | `format.cpp:116-117` | not an engine file, or one written by an incompatible version |
| `invalid_input: file size mismatch (truncated?): truncated.bin` | `format.cpp:118` **(run E09)** | the file is shorter than its header says: an interrupted copy or a full disk. Copy it again; regenerate it if the original is damaged |
| `invalid_input: section table hash mismatch: …`, `header hash mismatch (header altered): …` | `format.cpp:124,126` **(run E11)** | the header or the section table was altered or damaged. Do not use the file; regenerate it |
| `invalid_input: section hash mismatch: terminal_S in corrupt.bin` | `format.cpp:143,149` **(run E10)** | one section of the file was damaged (the name tells which). A single flipped byte is caught. Regenerate the file |
| `invalid_input: section out of range: …` | `format.cpp:132` | the section table points outside the file; same advice |
| `invalid_input: merge refused (GUARD-W): 0 missing, 1 invalid, 0 failed island(s) [corrupt.bin: invalid_input: …]` | `include/v4/merge.h:278` **(run E12)** | `merge` refuses to pool anything if any island file is missing, invalid (damaged, or from other inputs) or failed. The bracket names the island and its own error. Fix or rerun that island; no subset is ever merged |
| `invalid_input: prep: non-finite entry in X or y` | `prep.cpp:74-75` **(run E31)** | NaN or Inf in the data. Remove or impute them before `prep` |
| `invalid_input: data.bin: stored constants differ from the recomputed ones (libm or binary mismatch)` | `prep.cpp:145` | `data.bin` was made on a system whose math library gave other bits, or by another binary. Make it again with this build |

#### 3.3.3 Files that do not belong together

The commands check that the files they read were produced from one another (by content hash), that the mode, seed and
build agree. All of these mean "rerun the earlier stage, or pass the right file".

| message | source | cause and action |
|---|---|---|
| `invalid_input: island: setup.bin was built from another data.bin`, `calibrate: setup.bin was built from another data.bin` | `island_cmd.cpp:244`, `calib_run.cpp:143` **(run E24)** | the `--data` and `--setup` do not match (different data, even with the same p). Use the `data.bin` that `setup` read |
| `invalid_input: island: calib.bin's meta.inputs differ from the data.bin / setup.bin in use` | `island_cmd.cpp:246` | `calib.bin` was made from other inputs |
| `invalid_input: island: --seed 2 differs from the calibration's seed 1` | `island_cmd.cpp:222` **(run E18)** | the island's sampler seed must equal `calibrate`'s |
| `invalid_input: island: N differs from calib.bin's frozen N = …` | `island_cmd.cpp:224` | N is fixed by `calibrate`; drop `--N` |
| `invalid_input: island: calib.bin's mode is V, not law` | `island_cmd.cpp:216` **(run E19)** | `--mode` must match the mode `calibrate` ran in |
| `invalid_input: island: island r = 3 > R' = 2` | `island_cmd.cpp:125` **(run E20)** | the island index exceeds `--Rp` |
| `invalid_input: island: calib.bin vs this binary: island ISA families differ (x86-64-v3 vs portable): class-A bits differ (D-32)` | `src/common/provenance.cpp:74` **(run E17)** | the binary was built with another `-DV4_ISLAND_ISA` family than the one that made `calib.bin`. The two give different bits by design, so the engine refuses to mix them. Rebuild with the original ISA, or redo `calibrate` with this binary (README §1.2). The same check refuses a `merge` of islands from two families |
| `invalid_input: merge: 2 island files for R' = 3 (no subset is ever pooled)` | `wp4_io.cpp:1018` **(run E22)** | `--Rp` and the list of `--islands` disagree. Give exactly R′ distinct island files |
| `invalid_input: merge: an island path appears twice` | `wp4_io.cpp:1014` **(run E23)** | one island listed twice |
| `invalid_input: merge: --Rp differs from the manifest's params.Rp`, `merge: --islands differs from the manifest's island inputs`, `merge: --mode differs from the manifest's mode` | `wp4_io.cpp:970,1015,1022` | an explicit flag that disagrees with the driver's manifest. The manifest wins; drop the flag |
| `invalid_input: … content hash differs from the manifest` | `wp4_io.cpp:1105`, `src/eval/run.cpp:108` | a file changed after the driver recorded its hash. Rerun the stage that produced it |
| `invalid_input: calib.bin mode differs from the merge mode`, `…: meta.inputs differ from the data / setup in use`, `…grid differs from calib.bin's frozen grid` | `wp4_io.cpp:1108,342,493` | the merge's inputs do not belong to one fit |
| `invalid_input: libm self-test failed for log, log_near1, exp, exp_pos, lgamma, lgamma_int: bit-form results would differ from the reference (Owls = NOTS) bits (INTERFACES §6)` | `provenance.cpp:109` **(run E25)** | this machine's math library does not reproduce the reference bits (here forced with `GLIBC_TUNABLES`). Only RHEL 9-family systems are measured. Run `smcbvs4 version` and look at `self_test.pass`; use a RHEL 9-family system or a container of one (README §1.3). `info` and `version` still run |
| `invalid_input: binary blocks incompatible: …` | `provenance.cpp:101` | the merge found two files written by incompatible builds (flags, libm, ISA family) |

#### 3.3.4 Checkpoints

| message | source | cause and action |
|---|---|---|
| `invalid_input: checkpoint island_c.ckpt belongs to another configuration or binary` | `island_run.h:632` **(run E27)** | a checkpoint exists for this output but was written under a different fingerprint: another binary (even a rebuild of the same commit), other inputs, another seed or N, or another setting such as `--offer-floor`. The island **refuses rather than start over silently**. Rerun with the binary and flags that wrote it; or delete `island_<r>.ckpt.a` and `.ckpt.b` to start from scratch (the message names `…ckpt`, the files are `….ckpt.a/.b`) |
| `invalid_input: checkpoint … is of the older format (serial checksum, before WP7 O4): remove it or finish the run with the binary that wrote it` | `island_run.h:609` | a checkpoint from an older engine version. Remove it or finish with that binary |

#### 3.3.5 Inputs found inconsistent by the readers

Most of the roughly 300 remaining `invalid_input` sites check that a file's internal tables are consistent (a model larger than K, an
index outside [0, p), offsets that do not cover the pool, a store that is not sorted, a grid that is not increasing,
`hpm_ev … out of range`). They fire only for a **damaged or hand-edited file** that still passes its hashes, or for a
file from an incompatible engine version. The action is always the same: regenerate the file with this build. They are in
[ERRORS_ALL_SITES.md](ERRORS_ALL_SITES.md) under `src/merge/wp4_io.cpp`, `include/v4/island/setup_load.h`,
`src/island/island_file.cpp`, `src/eval/io.cpp`, `src/setup/*`; many are worded for developers (§6).

### 3.4 `io_error` (exit 14): the file system said no

| message | source | cause and action |
|---|---|---|
| `io_error: cannot create /…/g.bin.tmp.<pid>` | `src/common/format.cpp:79` **(run E07)** | the output directory does not exist, is not writable, or the disk is full. Outputs are written to `<out>.tmp.<pid>`, flushed and renamed, so a failure leaves no half-written `<out>` |
| `io_error: write failed: …`, `fsync failed: …`, `rename failed: …`, `directory fsync failed: …` | `format.cpp:51,90,93,98`, `src/common/json.cpp:177-178` | the write did not complete: full disk, quota, a file-system fault. Free space and rerun |
| `io_error: mmap …`, `fstat …` | `format.cpp:106,111` | the input file could not be mapped; low address space or a network file system problem |
| `io_error: cannot open …` | `src/common/sha256.cpp:74` | a file to hash could not be read |
| `io_error: short read of section …` | `wp4_io.cpp:694` | a read returned fewer bytes than the section length: a file being rewritten while read, or a network file system fault |
| `io_error: cannot open checkpoint …`, `checkpoint write failed: …`, `directory fsync failed for …` | `island_run.h:568,579,583` | the island could not write its checkpoint. A full disk is the usual cause; the island stops rather than run unprotected |
| `io_error: calibrate: cannot create --cost-dir …: …` | `calib_run.cpp:194`, `include/v4/island/pilot_only.h:86` | the directory given to `--cost-dir` cannot be created |

### 3.5 `internal_error` (exit 15): a check inside the engine failed

These should not happen. They mean the engine found a violated internal rule, and **a bug is the likely explanation**:
keep the record, the input files and the command, and report them. 57 sites raise it explicitly; any C++ exception that is
not an engine error is also reported as `internal_error` (`main.cpp:123-124`). Examples:

| message | source | meaning |
|---|---|---|
| `internal_error: store: a NaN value was offered (INTERFACES v0.1.3)`, `leader store: a NaN value was offered` | `island_run.h:343,347` | a score was NaN where the sampler must never produce one |
| `internal_error: store invariant I1 violated (…)` | `island_run.h:396` | the island's store was found unsorted or with a duplicated model at a check |
| `internal_error: score: |S| > K (infeasible model; callers never pass these, R1)` | `score.cpp:160` | an infeasible model reached the scorer |
| `I5: address used twice`, `I5: address not increasing in the serial order`, `slot index >= 2^28` | `include/v4/rng.h:58-67,164-168` | the random-number address rules were broken (`compat` mode checks); a plain exception, reported as `internal_error` |
| `internal_error: write_setup_bin: setup did not complete (GUARD-W)` | `setup_run.cpp:98` | an attempt to write `setup.bin` after a failed setup |

### 3.6 `schedule_limit` (exit 16)

Raised only by the `compat` and `law` modes' calibration when the first tier's grid construction fails and the reference
method has no fallback. It cannot arise in mode V. Nothing in this catalogue triggers it. If you see it in `compat`/`law`,
the data may need a larger tier budget or more tempering; this is the reference method's own limit, not a defect.

### 3.7 `completed` with exit 20, 21, 22: not failures, but not plain success

| exit | record fields | what happened | what to do |
|---:|---|---|---|
| 20 | `prep_status: "no_predictors"` | every predictor column is constant (E30) | check the data. The fit has no estimate by definition (empty HPM) |
| 21 | `prep_status: "y_constant"` | the response is constant (E29) | check the data |
| 22 | `island_status: "interrupted_resumable"`, `stopped_after_step`, `reason: "interrupted after checkpoint (stop_after_s: resumable)"` | `--stop-after-s` elapsed; a checkpoint was written; no `island_<r>.bin` (E26) | rerun the same command (same binary, same flags) to resume; REPRODUCIBILITY.md §6 |

The SLURM driver treats 20 and 21 as data outcomes (`OUTCOME` file, the pipeline for that fit ends) and 22 as "resume in
the next attempt" (`tools/slurm/p1m_driver.py:402-405,413-429`).

---

## 4. Driver and script exits

These come from `tools/slurm/p1m_driver.py` (the plan checker and generator, Python 3) and from the scripts it writes
(`submit.sh`, `build.sh`, `stage_*.sbatch`). The driver never calls `sbatch`; `submit.sh` does, and only with
`CONFIRM=yes`.

| exit | message | source | cause and action |
|---:|---|---|---|
| 64 | `refusing: --dept … is outside the department folder (POLICIES §12)` | `p1m_driver.py:750-755` (D08) | `--dept` or `--out` lies outside `$HOME/SMC_Engineering_Department` or a `P1M_TEST_ROOT` that is inside `$TMPDIR`. Set both (README §5.2) |
| 64 | `refusing: set CONFIRM=yes (the manager's submission, after HQ's go)` | `submit.sh`, generated at `p1m_driver.py:645` (D09) | `submit.sh` submits jobs and so requires an explicit `CONFIRM=yes` |
| 64 | `refusing: … is outside the department folder` | generated `submit.sh`/`build.sh`, `p1m_driver.py:360,641` (D12) | the scripts repeat the path check; `P1M_DEPT` or the script directory is outside the allowed folder |
| 65 | `plan error: a V-mode plan needs island_isa with FMA (one of …; D-32); got ''` | `p1m_driver.py:133` (D01, D02) | add `"island_isa": "x86-64-v3"` (or another FMA ISA) to the plan (README §5.1) |
| 65 | `plan error: worst case 34.0 billed core-h exceeds the plan's core_h_cap 5.0` | `p1m_driver.py:304` (D03) | raise `core_h_cap` or shrink the plan (fewer islands, shorter limits) |
| 65 | `plan error: batch 'bad batch!': use letters, digits, _ . - (max 64)` | `p1m_driver.py:110` (D04) | rename the batch or run id |
| 65 | `plan error: mode must be compat, law or V` | `p1m_driver.py:120` (D06) | fix `mode` |
| 65 | other `plan error:` lines (44 in `resolve`: bad time limit, task cap of 150, QOS wall of 24 h, duplicate `run_id`, `restart` and `t6`/`pilot` combinations…) | `p1m_driver.py:103-470` | each names the key and the limit |
| 66 | `FATAL: scripts differ from SHA256SUMS` | generated `submit.sh`, `p1m_driver.py:647` (D10) | a generated file was edited after generation. Regenerate, do not edit; or run `sha256sum -c SHA256SUMS` to see which |
| 66 | `FATAL: binary …/bin/smcbvs4 missing` | `p1m_driver.py:648,670,684` (D11) | run `build.sh` first (or copy the binary to `bin/`) |
| 66 | `FATAL: scratch/slurm_out or scratch/tmp missing` | `p1m_driver.py:649` | create the two scratch directories |
| 66 | `FATAL: env.sh: GCC 14.3.0 not loaded` | `p1m_driver.py:351` | the NOTS module environment did not load (on another cluster, edit `env.sh`, README §5.5) |
| 66 | `FATAL: …/data.bin missing (run the source batch first)` | `p1m_driver.py:499` | a restart or T6 batch needs the inputs of a finished batch |
| 1 | `p1m_manifest: cannot read the producer record …: refusing to start`; `…: section table hash mismatch: refusing to start`; `…: has status 'invalid_input': refusing to start` | `tools/slurm/p1m_manifest.py:39-96` (D13) | a stage found its input missing, corrupt or produced by a failed stage; the next stage refuses to start. Look at the producer's record under `log/` and `<out>.json` |
| 1 | `D-32 isa check FAILED (isa_check*.json)` | `p1m_driver.py:550` | the comparison build's island differs from the production build's: the two builds are not in one FMA family. Do not merge; see `isa_check.json` |
| 1 | a Python traceback (for example `FileNotFoundError` for a missing `--plan`) | D07 | the driver does not catch a missing or malformed plan file; fix the path or the JSON |
| 2 | `run_tests.sh: set TMPDIR (department tmp folder; never /tmp)`, `unknown option …` | `tests/run_tests.sh:9,17` (D14) | set `TMPDIR` to a scratch directory (it also holds the build) |

A gap found while making this catalogue: the driver does **not** validate `Rp` or `N` (a plan with `"Rp": 0` generates
without complaint, D05); `p1m_driver.py:239` only sets defaults. See §6.

---

## 5. Failures the engine cannot report

When the process is killed from outside it cannot write a record. You then have an exit code and a stale or missing
`<out>.json`.

| symptom | cause | what to do |
|---|---|---|
| exit 137, no record, `sacct` shows `OUT_OF_MEMORY` or `MaxRSS` at the request | the SLURM memory limit killed it (page cache counts toward a cgroup's limit) | raise `--mem`; set `--mem-budget` so that the engine refuses up front; the drivers use 90% of the allocation as the budget |
| exit 137 or 143, state `TIMEOUT` or `CANCELLED` | the time limit or `scancel` | for islands use the `restart` plan key (REPRODUCIBILITY.md §6): the last checkpoint survives |
| exit 139 | a crash | report with the command and inputs |
| the record is from an earlier run | the command died before writing; `<out>.json` was not refreshed | trust the exit code and the timestamps, not an old record |
| an island leaves `island_<r>.ckpt.a/.b` | killed or soft-stopped: expected | rerun to resume; delete the files to start over |

---

## 6. Messages to improve

The goal of P-3 part 2 is that every message names **the file, the value and the limit**, and uses no internal labels.
This table lists the messages that fall short. **No code was changed** for this catalogue. The `reason` column says what
is wrong; the last column is a suggested replacement. "Internal label" means a name the reader of the output cannot know
(Owls, NOTS, D-numbers, PR and review numbers, `GUARD-W`, `I1`–`I7` invariant names, `WP7 O4`, INTERFACES and file
references into `core/`).

### 6.1 Internal labels

| source | message as written | problem | suggested |
|---|---|---|---|
| `src/common/provenance.cpp:109` | `libm self-test failed for …: bit-form results would differ from the reference (Owls = NOTS) bits (INTERFACES §6)` | Owls, NOTS, INTERFACES; no remedy | `the math library of this machine does not reproduce the reference results for log, exp (…): the engine cannot run here. Run 'smcbvs4 version' for details; use a RHEL 9 / glibc 2.34 system (README §1.3)` |
| `src/common/provenance.cpp:74` | `… island ISA families differ (x86-64-v3 vs portable): class-A bits differ (D-32)` | D-32 | `…: they give different results by design. Rebuild with -DV4_ISLAND_ISA=x86-64-v3 or rerun calibrate with this binary` |
| `include/v4/merge.h:261` | `R' < 1: nothing to merge (review PR20 C-1)` | review id; no value | `merge: --Rp is 0; give at least one island` |
| `include/v4/merge.h:262` | `manifest R' != number of islands` | no numbers | `the manifest says R' = 16 but 15 island files were found` |
| `include/v4/merge.h:278,315-333` | `merge refused (GUARD-W): 0 missing, 1 invalid, 0 failed island(s) […]`, `… island 3 has leader stores (INTERFACES v0.1.7)` | GUARD-W, INTERFACES | `merge refused: 1 of 2 island files is invalid (island 1: …). Fix or rerun it; no subset is merged` |
| `include/v4/merge.h:301` | `merge refused: the pre-island ledger has leader stores (final-run ledgers need leaders = false, INTERFACES v0.1.7)` | internal vocabulary | say which file and what to do (it is a calibration-run output given as a final island) |
| `include/v4/merge.h:488` | `a non-finite estimate at assembly (internal check)` | no value, no file | name the estimate and island |
| `src/island/island_run.h:609` | `checkpoint … is of the older format (serial checksum, before WP7 O4): remove it or …` | WP7 O4 | `checkpoint … was written by an older engine version: delete it or finish the run with that version` |
| `src/island/island_run.h:347,396` | `store: a NaN value was offered (INTERFACES v0.1.3)`, `store invariant I1 violated (…)` | INTERFACES, I1 | describe the failed rule in words and add `this is a bug: please report it with the command and inputs` |
| `src/island/island_run.h:954-984` | `run_island: calibration tier < 4 and iteration < 64 (INTERFACES §3)`, `grid not strictly increasing (I3)`, `the bit-form label-major kernel is test-only (D-21, manager Q1)`, `G must be in 0..256 (0 = chosen by mem_budget; manager Q3)`, `an offer floor … (D-29)` | D-numbers, "manager Q1/Q3", I3, no values | rewrite each as `<flag> = <value> is not allowed: <rule>`; most are unreachable from the command line |
| `src/island/island_file.cpp:89`, `src/merge/wp4_io.cpp:271,293,296,336,468` | `…: an offer floor outside V mode (D-29)`, `…: tau_cal is not the c-th best F of the distinct inherited models (D-29)`, `…: a V calib.bin must have the bounded rule, tier 0 and N = 2500 (D-1, D-26)` | D-numbers; jargon (`tau_cal`, "inherited") | say in words which file is inconsistent and what it was expected to contain |
| `src/common/store.cpp:195`, `src/eval/io.cpp:26,40`, `src/merge/wp4_io.cpp:100,512` | `…the same model appears twice (I1)`, `fit.bin: top store not sorted (I1; re-merge with the current engine)`, `store …: not a valid sorted store (I1)` | I1; some lack the file path | `<file>: the stored models are not in the required order: the file is damaged or was written by another version; regenerate it` |
| `include/v4/island/setup_load.h:52,249,261`, `include/v4/island/setup_load.h:106` | `size_cum differs from the island's rebuild of the start law (core/cpp/v3_start.h)`, `… (D-31)`, `no section … (the admission plan needs it; INTERFACES §5.1)` | references into `core/`, D-31, INTERFACES | `setup.bin <path> is inconsistent: regenerate it with this build`; for a missing section name the file |
| `src/setup/setup_run.cpp:98`, `src/merge/wp4_io.cpp:758` | `write_setup_bin: setup did not complete (GUARD-W)`, `write_setup_min: code_ptr must have J + 1 entries … (INTERFACES v0.1.19)` | GUARD-W, INTERFACES | these are internal-error paths; add `please report` |
| `src/setup/partition.cpp:222`, `src/setup/start.cpp:291` | `partition: B outside 1..16 (core/cpp/v3_core.cpp:180)`, `start_mode: the e4 tie-aware fallback requires cap >= 2 (C-PACK MR2)` | source and review references | state the value and the limit; drop the references |
| `include/v4/calib.h:177,179` | `bounded calibration has no tier escalation: tier0 must be 0 (D-26)`, `… requires 0 <= I_max <= ell (D-26)` | D-26; no values | `--I_max = 5 is not allowed: it must be between 0 and 14 in mode V` |
| `include/v4/rng.h:58-168` | `slot index >= 2^28`, `address key field out of range`, `I5: address used twice` | internal invariant names; thrown as plain exceptions (so exit 15) | internal; add `this is a bug: please report it` |
| `tools/slurm/p1m_driver.py:133`, `p1m_driver.py:550` | `a V-mode plan needs island_isa with FMA (…; D-32)`, `D-32 isa check FAILED` | D-32 | `the plan's island_isa must be an FMA ISA: one of …` and `the ISA comparison failed: the two builds are not in one FMA family` |
| `tools/slurm/p1m_driver.py:645` | `refusing: set CONFIRM=yes (the manager's submission, after HQ's go)` | "the manager", "HQ" | `submit.sh submits jobs: set CONFIRM=yes to proceed` |
| `tools/slurm/p1m_driver.py:750-755`, `:360,641`, build.sh | `refusing: … is outside the department folder (POLICIES §12)` | "department folder", POLICIES | `… is not under $HOME/SMC_Engineering_Department or under P1M_TEST_ROOT inside $TMPDIR (README §5.2)` |
| `tools/slurm/p1m_driver.py:254` | `exceeds max_task_hours = %.2f (§0-v2.5: no job longer than 2 h)` | spec reference | drop the reference |
| `tests/run_tests.sh:9` | `set TMPDIR (department tmp folder; never /tmp)` | "department" | `set TMPDIR to a scratch directory` |

### 6.2 The value, the file or the limit is missing

| source | message as written | problem | suggested |
|---|---|---|---|
| `src/common/json.cpp:24` | `json: missing key seed` (E04) | does not say which command or flag | `gen: --seed is required` |
| `src/common/json.cpp:28-43` | `json: not a number`, `json: not an integer`, `json: bad array index` (E36) | no flag, no value | `gen: --n must be a number, got 'abc'` |
| `src/cli/main.cpp:55` | `bad argument --n` (E03) | does not say the value is missing | `--n needs a value` |
| `src/common/gen.cpp:36-40` | `gen: rho must be in [0, 1)`, `gen: s0 in 0..min(5, p)`, `gen: need n >= 3, p >= 1, seed in [1, 2^31-1]` (E38, E39) | gives the limit, not the value | `gen: --rho 1.5 is outside [0, 1)` |
| `src/calib/calib_run.cpp:112`, `src/island/island_cmd.cpp:103` | `--mode must be compat, law or V` (E35) | does not give the value received (and is also the message for a *missing* `--mode`) | `--mode is missing` / `--mode 'fast' is not one of compat, law, V` |
| `src/island/island_cmd.cpp:57`, `calib_run.cpp:51` | `--G must be a whole number in [0, 256]` (E41) | limit but not the value | `--G 999 is outside [0, 256]` |
| `src/island/island_cmd.cpp:306` | `--stop-after-s must be a number > 0` (E42) | no value | `--stop-after-s -3 must be > 0` |
| `src/island/island_run.h:969` | `run_island: stop_after_s needs a checkpoint path and a final island` (E28) | names an internal function, not the flag | `--stop-after-s needs checkpoints: remove --ckpt 0` |
| `src/calib/calib_run.cpp:160,168` | `calibrate not admitted: calibration state 38880243 B >= --mem-budget` (E14) | does not give the budget | `calibrate needs 38,880,243 B but --mem-budget is 1,000 B` |
| `src/island/island_cmd.cpp:281`, `island_run.h:375,994` | `predicted peak 59 MiB > budget 0 MiB` (E15) | rounds a budget under 1 MiB to 0; does not say the flag | `predicted peak 59 MiB > --mem-budget 1,000 B` |
| `src/setup/setup_run.cpp:55-58` | `accounted setup peak 0.04 GB > mem_budget 0.00 GB` (E13) | rounding to 0.00; the unit differs from the other commands | print more digits and say `(--mem-budget is in GB for setup)` |
| `src/island/island_run.h:632` | `checkpoint island_c.ckpt belongs to another configuration or binary` (E27) | says nothing about what differs or what to do; the named file does not exist (`.ckpt.a/.b`) | `…island_c.ckpt.a was written by another binary or with other settings; rerun with those, or delete island_c.ckpt.a/.b to start over` |
| `src/common/format.cpp:108` | `file too short: err.txt` (E08) | does not say it is not an engine file | `err.txt is not an smcbvs4 file (12 bytes; the header alone is 128)` |
| `src/common/format.cpp:118` | `file size mismatch (truncated?): truncated.bin` (E09) | no sizes | `… the header says 4,516,928 bytes, the file has 2,258,464` |
| `src/common/format.cpp:79` | `cannot create …/g.bin.tmp.205791` (E07) | names the temporary file and not the reason | `cannot create /…/g.bin: the directory does not exist (or: permission denied, disk full)` using `errno` |
| `src/common/format.cpp:104`, `prep.cpp:153` | `cannot open nonexistent.bin` (E05, E45) | no reason (`errno`), and `invalid_input` where `io_error` fits a permission problem | `cannot open nonexistent.bin: No such file or directory` |
| `src/eval/io.cpp:15` | `island_1.bin: not a fit.bin (kind != 6)` (E33) | prints a kind number | `island_1.bin is an island file, not a fit.bin` |
| `src/island/island_cmd.cpp:139`, `prep.cpp:195` etc. | `data.bin: not a calib file` (E47), `data.bin is not a raw file` (E06) | does not say what it is | `data.bin is a data file, not a calib file` (the reader knows the kind) |
| `src/eval/run.cpp:108`, `src/merge/wp4_io.cpp:1105` | `truth.json: content hash differs from the manifest`, `…: content hash differs from the manifest` | no hashes, no manifest path | print both hashes |
| `src/eval/io.cpp:20-25,40`, `src/merge/wp4_io.cpp:485-561` | `fit.bin: top_off size`, `hpm_ev xph out of range`, `pip_r: not in [0, 1]`, `inconsistent top store sections` | literal `fit.bin` instead of the path; terse field names; no values | `<path>: section top_off has 12 entries, expected 14` |
| `src/common/prep.cpp:145` | `data.bin: stored constants differ from the recomputed ones (libm or binary mismatch)` | literal `data.bin`, no values | name the file, the constant and both values |
| `src/common/score.cpp:166` | `score failed after Cholesky, refactor and augmented QR for a model of size …` | does not name the variables | list the model's columns (as raw columns, README §6.2) |
| `include/v4/merge.h:262`, `src/merge/wp4_io.cpp:1018` | `manifest R' != number of islands`, `2 island files for R' = 3` | (the second is good; the first has no numbers) | add the numbers |
| `src/island/island_run.h:955-961` | `calibration islands have no checkpoints`, `a final island is r >= 1` | no values | add the value |
| `src/setup/setup_run.cpp:152,160`, `src/merge/wp4_io.cpp:724-743` | `setup.bin: scalars missing`, `blk / pos / blk_members length != p`, `block size outside 1..20` | no values, literal file names | name the file, the value and the limit |
| `tools/slurm/p1m_driver.py:756` | traceback for a missing or malformed `--plan` file (D07) | unhandled exception | `cannot read plan nonexistent.json: …`, exit 65 |
| `tools/slurm/p1m_driver.py:239` | `Rp` and `N` are not validated: `"Rp": 0` is accepted (D05) | a plan error is missed, so the generated scripts are wrong | `plan error: fit demo: Rp must be an integer ≥ 1, got 0` |
| `src/cli/main.cpp:51-66` (argument parsing) | unknown flags are silently ignored (E-note in §1) | a typo changes nothing and says nothing | `warning: unknown flag --thread (ignored)`, or an error |

### 6.3 The status does not fit

| source | situation | problem | suggestion |
|---|---|---|---|
| `src/common/format.cpp:104`, `prep.cpp:153` | opening a missing or unreadable input is `invalid_input` (13) | a permission error or an I/O fault is not an invalid input; scripts cannot tell "wrong path" from "disk problem" | `invalid_input` for a missing file, `io_error` for permission or I/O errors |
| `include/v4/rng.h:58-168` | internal address checks throw plain exceptions | the status is `internal_error` only by the catch-all in `main.cpp:123` | throw `Error(Status::internal_error, …)` explicitly |
| `src/cli/main.cpp:19-29` | `--help` is treated as an unknown command: it prints a usage text that lists three commands out of ten, and exits 13 | `--help` should exit 0 and every command should have its own help | polish item P-4 |

---

## Appendix A. Real runs

Each case below was run on Owls (`nice -n 19`, 3 threads) against the p = 2,000 fit of README §3 A (`data.bin`,
`setup.bin`, `calib.bin`, `island_1.bin`, `island_2.bin`, `fit.bin`, `truth.json` in the working directory), with the
x86-64-v3 build of `smcbvs4` at commit `c8a30d39` (`smcbvs4-portable` is the build without `-DV4_ISLAND_ISA`). The output is
exactly what the program printed, reduced to `exit`, `status` and `reason` (the full record also holds the `binary` block);
paths of the working directories are shortened. "stderr" lines are the usage text. How they were produced: Appendix B.

### A.1 The engine: E01–E48

**E01 no arguments**

```
$ smcbvs4
exit 13

stderr:
usage: smcbvs4 <command> [--key value ...]   or   smcbvs4 <command> --manifest m.json
commands: gen prep setup calibrate island merge eval post info version
  gen   --design AR|IND|BLK|ADJ-OPP --n N --p P --seed S [--rho R --b B --a A --s0 K --sigma s] --out raw.bin [--truth truth.json]
  gen-test  (same spec) --ntest M --cols 1,5,9 --out test.bin
  prep  --in raw.bin --out data.bin    |   prep --from-r <dir> --out data.bin
  info  file.bin | --in file.bin       (header, sections, verified hashes: every section)
  … (the usage text continues: see README §7)
```

**E02 unknown command**

```
$ smcbvs4 frobnicate
exit 13
status: invalid_input
reason: invalid_input: unknown command frobnicate
stderr:
usage: smcbvs4 <command> [--key value ...]   or   smcbvs4 <command> --manifest m.json
commands: gen prep setup calibrate island merge eval post info version
  gen   --design AR|IND|BLK|ADJ-OPP --n N --p P --seed S [--rho R --b B --a A --s0 K --sigma s] --out raw.bin [--truth truth.json]
  gen-test  (same spec) --ntest M --cols 1,5,9 --out test.bin
  prep  --in raw.bin --out data.bin    |   prep --from-r <dir> --out data.bin
  info  file.bin | --in file.bin       (header, sections, verified hashes: every section)
  … (the usage text continues: see README §7)
```

**E03 flag without a value**

```
$ smcbvs4 gen --design AR --n
exit 13
status: invalid_input
reason: invalid_input: bad argument --n
```

**E04 missing required flag (--seed)**

```
$ smcbvs4 gen --design AR --n 50 --p 100 --out g.bin
exit 13
status: invalid_input
reason: invalid_input: json: missing key seed
```

**E05 input file does not exist**

```
$ smcbvs4 prep --in nonexistent.bin --out d.bin
exit 13
status: invalid_input
reason: invalid_input: cannot open nonexistent.bin
```

**E06 wrong kind of file (data.bin given as raw)**

```
$ smcbvs4 prep --in data.bin --out d.bin
exit 13
status: invalid_input
reason: invalid_input: data.bin is not a raw file
```

**E07 cannot write the output (directory missing)**

```
$ smcbvs4 gen --design AR --n 50 --p 100 --seed 1 --out /home/fb31/no_such_dir_p3/g.bin
exit 14
status: io_error
reason: io_error: cannot create /home/fb31/no_such_dir_p3/g.bin.tmp.<pid>
```

**E08 a file that is not an engine file**

```
$ smcbvs4 info err.txt
exit 13
status: invalid_input
reason: invalid_input: file too short: err.txt
```

**E09 truncated file**

```
$ smcbvs4 info truncated.bin
exit 13
status: invalid_input
reason: invalid_input: file size mismatch (truncated?): truncated.bin
```

**E10 one flipped byte inside a section**

```
$ smcbvs4 info corrupt.bin
exit 13
status: invalid_input
reason: invalid_input: section hash mismatch: terminal_S in corrupt.bin
```

**E11 one flipped byte in the header**

```
$ smcbvs4 info badheader.bin
exit 13
status: invalid_input
reason: invalid_input: section table hash mismatch: badheader.bin
```

**E12 merge given the corrupt island**

```
$ smcbvs4 merge --mode V --Rp 2 --data data.bin --setup setup.bin --calib calib.bin --islands corrupt.bin,island_2.bin --out f_c.bin --threads 3
exit 13
status: invalid_input
reason: merge refused (GUARD-W): 0 missing, 1 invalid, 0 failed island(s) [corrupt.bin: invalid_input: section hash mismatch: terminal_S in corrupt.bin]
```

**E13 setup over its memory budget (GB)**

```
$ smcbvs4 setup --data data.bin --out s_x.bin --mem-budget 0.000001
exit 11
status: resource_limit
reason: resource_limit: admission: accounted setup peak 0.04 GB > mem_budget 0.00 GB (C = 1484804 codes, J = 155, B_blocks = 14)
```

**E14 calibrate over its memory budget (bytes)**

```
$ smcbvs4 calibrate --mode V --data data.bin --setup setup.bin --seed 1 --out c_x.bin --mem-budget 1000
exit 11
status: resource_limit
reason: calibrate not admitted: calibration state 38880243 B >= --mem-budget
```

**E15 island over its memory budget (bytes)**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out i_x.bin --mem-budget 1000
exit 11
status: resource_limit
reason: mem_budget: predicted peak 59 MiB > budget 0 MiB [inputs=16MiB x_tiles=3MiB store=15MiB worker_bufs=16MiB rb=0MiB orders=0MiB rows=0MiB gram_rows=0MiB supports=0MiB lm_scratch=0MiB particles=0MiB ckpt=2MiB headroom=4MiB total=59MiB (G=1, k=8.000000)]
```

**E16 merge over its memory budget (bytes)**

```
$ smcbvs4 merge --mode V --Rp 2 --data data.bin --setup setup.bin --calib calib.bin --islands island_1.bin,island_2.bin --out f_x.bin --mem-budget 1000
exit 11
status: resource_limit
reason: merge not admitted: estimated peak 73376745 B > --mem-budget 1000 B
```

**E17 ISA mismatch: portable binary, x86-64-v3 calib.bin**

```
$ smcbvs4-portable island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out i_p.bin --threads 3
exit 13
status: invalid_input
reason: invalid_input: island: calib.bin vs this binary: island ISA families differ (x86-64-v3 vs portable): class-A bits differ (D-32)
```

**E18 island seed differs from the calibration's**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --seed 2 --data data.bin --setup setup.bin --calib calib.bin --out i_s.bin --threads 3
exit 13
status: invalid_input
reason: invalid_input: island: --seed 2 differs from the calibration's seed 1
```

**E19 island mode differs from calib.bin's**

```
$ smcbvs4 island --mode law --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out i_m.bin --threads 3
exit 13
status: invalid_input
reason: invalid_input: island: calib.bin's mode is V, not law
```

**E20 island index above R'**

```
$ smcbvs4 island --mode V --island 3 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out i_r.bin --threads 3
exit 13
status: invalid_input
reason: invalid_input: island: island r = 3 > R' = 2
```

**E21 island without --seed**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --data data.bin --setup setup.bin --calib calib.bin --out i_n.bin --threads 3
exit 13
status: invalid_input
reason: invalid_input: island: --seed is required (a whole number in [1, 2^31 - 1])
```

**E22 merge with the wrong number of islands**

```
$ smcbvs4 merge --mode V --Rp 3 --data data.bin --setup setup.bin --calib calib.bin --islands island_1.bin,island_2.bin --out f_r.bin --threads 3
exit 13
status: invalid_input
reason: invalid_input: merge: 2 island files for R' = 3 (no subset is ever pooled)
```

**E23 merge with the same island twice**

```
$ smcbvs4 merge --mode V --Rp 2 --data data.bin --setup setup.bin --calib calib.bin --islands island_1.bin,island_1.bin --out f_d.bin --threads 3
exit 13
status: invalid_input
reason: invalid_input: merge: an island path appears twice
```

**E24 setup.bin built from another data.bin**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --seed 1 --data data2.bin --setup setup.bin --calib calib.bin --out i_d.bin --threads 3
exit 13
status: invalid_input
reason: invalid_input: island: setup.bin was built from another data.bin
```

**E25 libm self-test failure (AVX2/FMA masked)**

```
$ env GLIBC_TUNABLES=glibc.cpu.hwcaps=-AVX2,-FMA smcbvs4 gen --design AR --n 50 --p 100 --seed 1 --out g2.bin
exit 13
status: invalid_input
reason: invalid_input: libm self-test failed for log, log_near1, exp, exp_pos, lgamma, lgamma_int: bit-form results would differ from the reference (Owls = NOTS) bits (INTERFACES §6)
```

**E26 soft stop (exit 22, resumable)**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out island_c.bin --threads 3 --ckpt-every-s 3 --stop-after-s 8
exit 22
status: completed
reason: interrupted after checkpoint (stop_after_s: resumable)
island_status: interrupted_resumable
stopped_after_step: 4
resumed_from_step: -1
```

**E27 resume with another configuration (--offer-floor 0): foreign checkpoint**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out island_c.bin --threads 3 --offer-floor 0
exit 13
status: invalid_input
reason: invalid_input: checkpoint island_c.ckpt belongs to another configuration or binary
```

**E28 --stop-after-s without checkpoints**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out island_z.bin --ckpt 0 --stop-after-s 5
exit 13
status: invalid_input
reason: invalid_input: run_island: stop_after_s needs a checkpoint path and a final island
```

**E29 prep: constant response (exit 21)**

```
$ smcbvs4 prep --in yconst.bin --out d_y.bin
exit 21
status: completed
reason: (empty)
prep_status: y_constant
```

**E30 prep: no usable predictor (exit 20)**

```
$ smcbvs4 prep --in nopred.bin --out d_p.bin
exit 20
status: completed
reason: (empty)
prep_status: no_predictors
```

**E31 prep: NaN in X**

```
$ smcbvs4 prep --in nanx.bin --out d_n.bin
exit 13
status: invalid_input
reason: invalid_input: prep: non-finite entry in X or y
```

**E32 eval without --truth**

```
$ smcbvs4 eval --fit fit.bin --data data.bin --out e_x.bin
exit 13
status: invalid_input
reason: invalid_input: eval: --fit, --data, --truth and --out are required
```

**E33 eval with a fit.bin of the wrong kind**

```
$ smcbvs4 eval --fit island_1.bin --data data.bin --truth truth.json --out e_k.bin
exit 13
status: invalid_input
reason: invalid_input: island_1.bin: not a fit.bin (kind != 6)
```

**E34 calibrate --mode compat with a V-only flag**

```
$ smcbvs4 calibrate --mode compat --data data.bin --setup setup.bin --seed 1 --I_max 2 --out c_c.bin
exit 13
status: invalid_input
reason: invalid_input: calibrate: --I_max / --refine_m apply to the bounded rule (mode V) only
```

**E35 calibrate without a mode**

```
$ smcbvs4 calibrate --data data.bin --setup setup.bin --seed 1 --out c_n.bin
exit 13
status: invalid_input
reason: invalid_input: calibrate: --mode must be compat, law or V
```

**E36 non-numeric value**

```
$ smcbvs4 gen --design AR --n abc --p 100 --seed 1 --out g.bin
exit 13
status: invalid_input
reason: invalid_input: json: not a number
```

**E37 unknown design**

```
$ smcbvs4 gen --design XYZ --n 50 --p 100 --seed 1 --out g.bin
exit 13
status: invalid_input
reason: invalid_input: unknown design XYZ
```

**E38 rho out of range**

```
$ smcbvs4 gen --design AR --n 50 --p 100 --seed 1 --rho 1.5 --out g.bin
exit 13
status: invalid_input
reason: invalid_input: gen: rho must be in [0, 1)
```

**E39 s0 out of range**

```
$ smcbvs4 gen --design AR --n 50 --p 100 --seed 1 --s0 9 --out g.bin
exit 13
status: invalid_input
reason: invalid_input: gen: s0 in 0..min(5, p)
```

**E40 calibrate --threads 0**

```
$ smcbvs4 calibrate --mode V --data data.bin --setup setup.bin --seed 1 --threads 0 --out c_t.bin
exit 13
status: invalid_input
reason: invalid_input: calibrate: --threads must be a whole number in [1, 4096]
```

**E41 island --G 999**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out i_g.bin --G 999
exit 13
status: invalid_input
reason: invalid_input: island: --G must be a whole number in [0, 256]
```

**E42 island --stop-after-s -3**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out i_g.bin --stop-after-s -3
exit 13
status: invalid_input
reason: invalid_input: island: --stop-after-s must be a number > 0
```

**E43 merge --mem-budget abc**

```
$ smcbvs4 merge --mode V --Rp 2 --data data.bin --setup setup.bin --calib calib.bin --islands island_1.bin,island_2.bin --out f_a.bin --mem-budget abc
exit 13
status: invalid_input
reason: invalid_input: merge: --mem-budget must be a number
```

**E44 setup --partition foo**

```
$ smcbvs4 setup --data data.bin --out s_f.bin --partition foo
exit 13
status: invalid_input
reason: invalid_input: setup: partition must be truncated or exact
```

**E45 post: fit.bin missing**

```
$ smcbvs4 post --fit nonexistent.bin --data data.bin --out l.bin
exit 13
status: invalid_input
reason: invalid_input: cannot open nonexistent.bin
```

**E46 info without a file**

```
$ smcbvs4 info
exit 13
status: invalid_input
reason: invalid_input: info: the file is required (info FILE, or --in FILE)
```

**E47 island: calib.bin is not a calib file**

```
$ smcbvs4 island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib data.bin --out i_k.bin
exit 13
status: invalid_input
reason: invalid_input: data.bin: not a calib file
```

**E48 merge: --mode missing**

```
$ smcbvs4 merge --Rp 2 --data data.bin --setup setup.bin --calib calib.bin --islands island_1.bin,island_2.bin --out f_m.bin
exit 13
status: invalid_input
reason: invalid_input: merge: mode not given (--mode or the manifest's mode)
```


### A.2 The driver and its scripts: D01–D14

**D01 V plan without an FMA island_isa**

```
$ python3 tools/slurm/p1m_driver.py --plan plan_noisa.json --out WORK/dept/scripts/x_noisa --dept WORK/dept
exit 65
plan error: a V-mode plan needs island_isa with FMA (one of cascadelake, icelake-server, sapphirerapids, skylake-avx512, x86-64-v3, x86-64-v4; D-32); got ''
```

**D02 V plan with island_isa portable**

```
$ python3 tools/slurm/p1m_driver.py --plan plan_portable.json --out WORK/dept/scripts/x_portable --dept WORK/dept
exit 65
plan error: a V-mode plan needs island_isa with FMA (one of cascadelake, icelake-server, sapphirerapids, skylake-avx512, x86-64-v3, x86-64-v4; D-32); got 'portable'
```

**D03 worst case above core_h_cap**

```
$ python3 tools/slurm/p1m_driver.py --plan plan_cap.json --out WORK/dept/scripts/x_cap --dept WORK/dept
exit 65
plan error: worst case 34.0 billed core-h exceeds the plan's core_h_cap 5.0
```

**D04 bad batch name**

```
$ python3 tools/slurm/p1m_driver.py --plan plan_name.json --out WORK/dept/scripts/x_name --dept WORK/dept
exit 65
plan error: batch 'bad batch!': use letters, digits, _ . - (max 64)
```

**D05 Rp = 0**

```
$ python3 tools/slurm/p1m_driver.py --plan plan_rp.json --out WORK/dept/scripts/x_rp --dept WORK/dept
exit 0
dry run: wrote 22 files to WORK/dept/scripts/x_rp; 1 fits, 4 tasks, worst case 18.0 billed core-h. Nothing was submitted.
```

**D06 unknown mode**

```
$ python3 tools/slurm/p1m_driver.py --plan plan_mode.json --out WORK/dept/scripts/x_mode --dept WORK/dept
exit 65
plan error: mode must be compat, law or V
```

**D07 plan file missing**

```
$ python3 tools/slurm/p1m_driver.py --plan nonexistent.json --out WORK/dept/scripts/x --dept WORK/dept
exit 1
Traceback (most recent call last):
  File "tools/slurm/p1m_driver.py", line 771, in <module>
    sys.exit(main())
  File "tools/slurm/p1m_driver.py", line 756, in main
    with open(a.plan) as fh:
FileNotFoundError: [Errno 2] No such file or directory: 'nonexistent.json'
```

**D08 output outside the department folder**

```
$ env -u TMPDIR python3 tools/slurm/p1m_driver.py --plan plan_ok.json --out /home/fb31/notdept_p3/s --dept /home/fb31/notdept_p3
exit 64
refusing: --dept /home/fb31/notdept_p3 is outside the department folder (POLICIES §12)
```

**D09 submit.sh without CONFIRM=yes**

```
$ bash submit.sh
exit 64
refusing: set CONFIRM=yes (the manager's submission, after HQ's go)
```

**D10 submit.sh after a script was edited (SHA256SUMS)**

```
$ env CONFIRM=yes SBATCH=/bin/false bash submit.sh
exit 66
stage_merge.sbatch: FAILED
sha256sum: WARNING: 1 computed checksum did NOT match
FATAL: scripts differ from SHA256SUMS
```

**D11 submit.sh with the binary missing**

```
$ env CONFIRM=yes SBATCH=/bin/false bash submit.sh
exit 66
FATAL: binary WORK/dept/scripts/demo_1e4/bin/smcbvs4 missing
```

**D12 build.sh outside the department folder**

```
$ env -u P1M_TEST_ROOT P1M_DEPT=/home/fb31/notdept_p3 bash build.sh
exit 64
refusing: /home/fb31/notdept_p3 is outside the department folder
```

**D13 p1m_manifest fill: input missing**

```
$ python3 tools/slurm/p1m_manifest.py fill --template man_t.json --out man_o.json
exit 1
p1m_manifest: cannot read the producer record WORK/nonexistent.bin.json ([Errno 2] No such file or directory: 'WORK/nonexistent.bin.json'): refusing to start
```

**D14 run_tests.sh without TMPDIR**

```
$ env -u TMPDIR bash engine_v4/tests/run_tests.sh --quick
exit 2
run_tests.sh: set TMPDIR (department tmp folder; never /tmp)
```


---

## Appendix B. How the real runs were made

- Inputs: the smoke test of README §3 A (`gen`, `prep`, `setup`, `calibrate`, two islands, `merge`; p = 2,000, `--seed 1`),
  copied to a working directory. `data2.bin` is `gen --seed 2` + `prep` (E24). `truncated.bin`, `corrupt.bin` (one byte
  flipped 3,000 bytes before the end of an island file) and `badheader.bin` (one byte flipped in the header's hash field)
  were made from `island_1.bin` with a short Python snippet. `yconst.bin`, `nopred.bin` and `nanx.bin` (E29–E31) were
  written with the `write_raw` function of README §8.
- E26 and E27 are one pair: `island … --ckpt-every-s 3 --stop-after-s 8` (soft stop, exit 22), then the same command with
  `--offer-floor 0` added (a different configuration, so the checkpoint is foreign).
- E25 masks AVX2 and FMA with `GLIBC_TUNABLES=glibc.cpu.hwcaps=-AVX2,-FMA`, which makes glibc choose other `log`/`exp`
  routines.
- The driver cases ran in a directory under `$TMPDIR` with `P1M_TEST_ROOT` set to it. D08 and D12 use a path outside the
  department folder; the driver refuses before writing anything. `submit.sh` was always run with `SBATCH=/bin/false` and
  never reached a submission (D09 stops at the `CONFIRM` check, D10 and D11 at the next checks).
- Not triggered here: `numerical_failure` (12), `internal_error` (15), `schedule_limit` (16), a real out-of-memory kill
  (137) and the `io_error` causes other than an unwritable directory; they need a damaged design, a bug, the reference
  method's calibration limit, an undersized SLURM job or a failing disk.
