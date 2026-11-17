# smcbvs4 — large-p Bayesian variable selection by sequential Monte Carlo

`smcbvs4` does Bayesian variable selection in the Gaussian linear model: it samples the posterior over sets of predictors
(models), under a prior that depends on the model size, with a sequential Monte Carlo sampler, for p from a few thousand
up to 10⁶ predictors. It is one command-line program in C++20 with
OpenMP. The same program runs on a laptop-class node and, through a job-script generator, on a SLURM cluster.

What you get from a fit:

- the highest-posterior model (HPM) and the median-probability model (MPM);
- posterior inclusion probabilities (PIPs) for every variable, from three estimators (`pip_eq`, `pip_Z`, `pip_T`, §6);
- the model evidence log Ẑ with a measure of how well the independent runs agree;
- a stored posterior law over about 40·p models (`law.bin`) for prediction and uncertainty summaries.

Two properties are built in and documented in [REPRODUCIBILITY.md](REPRODUCIBILITY.md): **the same inputs on the same
build give the same bits, whatever the thread count, the schedule or a restart**, and every output file records the
binary, compiler flags and math library that produced it.

> **Status (11-17).** This is the engine in the P1M freeze. The simulation generator (`gen`) is the supported way to
> create data today (§7). Fields marked *(planned)* land later.

Contents: 1 Requirements and build · 2 How a fit is organised · 3 Check the install · 4 A first fit on one node (p = 10⁴) ·
5 The same fit on SLURM · 6 Reading the results · 7 Input data, limits and exit codes · 8 Where to go next

---

## 1. Requirements and build

| need | detail |
|---|---|
| CPU | x86-64 with AVX2 and FMA. Production builds target `x86-64-v3` or newer (§1.2). |
| compiler | GCC ≥ 11 (C++20). Tested with 11.5 (Owls) and 14.3 (NOTS). |
| CMake | ≥ 3.20 |
| OpenMP | required (it ships with GCC). |
| libm | **glibc 2.34**, the FMA variant. The engine binds to glibc's `exp`, `log` and `lgamma` and refuses to run if they do not reproduce the pinned reference results (§1.3). |
| Python 3 | standard library only; needed for the SLURM driver (§5). |
| R (optional) | only to run the golden tests and to read result files with `tools/v4_read.R`. |

No network access is needed at configure or build time.

### 1.1 Build

From the repository root:

```sh
cmake -S Scripts/SMC_BVS/engine_v4 -B build -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA=x86-64-v3
make -C build -j3 smcbvs4
build/smcbvs4 version
```

The build takes about 5 minutes with 3 jobs. `version` prints the *binary block*: git commit, compiler, flags, island ISA
and the libm identity with its self-test. Check these three lines:

```
"island_isa": "x86-64-v3",
"island_fma": true,
"pass": true            (inside "self_test")
```

### 1.2 Choose the island ISA once, and keep it

`-DV4_ISLAND_ISA=<march>` sets the instruction set of the sampler's kernels. **A fit must use one FMA family end to end**:

- Use `x86-64-v3` (AVX2 + FMA) or newer (`x86-64-v4`, `sapphirerapids`). The values from all of these agree bit for bit
  (measured: x86-64-v3 = x86-64-v4 = sapphirerapids).
- Without the option the build is `portable` (no FMA in the kernels). It works, but its results differ from the FMA
  builds *by design*, and the engine refuses to mix them: an island built with `portable` will not run against a
  `calib.bin` made by an `x86-64-v3` build (§5 of REPRODUCIBILITY.md shows the refusal).
- The Rice NOTS production builds use `sapphirerapids`.

### 1.3 The libm pin

Class-A results depend on the last bit of `exp`, `log` and `lgamma`, so the engine does not bundle a math library. It
binds to glibc 2.34's libm (FMA variant) and, at the start of every command except `info` and `version`, runs a
self-test that must reproduce reference hashes. If your system's libm gives other bits, the command stops with
`invalid_input` (exit 13) before doing any work. Details and the measurement are in `tests/PMATH_REPORT.md`.

---

## 2. How a fit is organised

A fit is a pipeline of separate commands. Each reads files and writes one file plus a JSON *record* (`<out>.json`, same
name with `.json` appended) holding the status, the inputs' hashes, timings and the binary block.

```
gen ──> prep ──> setup ──> calibrate ──> island 1..R′ ──> merge ──> eval ──> (post)
raw.bin  data.bin  setup.bin   calib.bin     island_r.bin      fit.bin    eval.bin    law.bin
```

| command | does | output | cost (p = 10⁴, n = 200, 3 threads; MEASURED on Owls) |
|---|---|---|---|
| `gen` | simulates data (designs IND, AR, BLK, ADJ-OPP) and the truth file | `raw.bin`, `truth.json` | 2 s |
| `prep` | standardises, drops constant and duplicate columns | `data.bin` | a few s |
| `setup` | correlation graph, blocks, the table of models around every variable, the start law | `setup.bin` (97 MB) | 17 s |
| `calibrate` | chooses the tempering ladder (φ-grid) and the offer floor; runs a pilot island | `calib.bin` | 12 min |
| `island` | one independent SMC run (N = 2,500 particles); you run R′ of them | `island_<r>.bin` | 4 min each |
| `merge` | combines the R′ islands: stores, PIPs, evidence, final local search | `fit.bin` | 6 s |
| `eval` | scores the fit against the truth (simulations) | `eval.bin` | 14 s |
| `post` | builds the posterior law from the merged store | `law.bin` | 6 s |

R′ is the number of independent islands. Production uses **R′ = 16**; the examples below use fewer to finish sooner.
The islands are independent, so they are what you spread over cores or over a SLURM job array. Costs grow quickly with
p; `tools/slurm/T5_AND_PILOT.md` has the 10⁵ and 10⁶ commands and their cost estimates.

Every command accepts `--threads k` (default: `OMP_NUM_THREADS`) and `--record path` (override the record's name).
`smcbvs4 info FILE` prints a file's header and section table and verifies every hash; `smcbvs4 info FILE --meta 1`
reads only the header and the meta section (seconds on a multi-GB file).

### Modes

`--mode` selects the method: **`V`** is the engineered sampler used for large p and is what this guide uses; **`compat`**
is bit-identical to the R reference implementation (revision D, serial streams, practical up to about p = 5,000);
**`law`** is the reference method with addressed random streams and threads. `calibrate`, `island` and `merge` must be
given the same mode.

---

## 3. Check the install

Two checks, from fast to thorough.

**A. Smoke test (p = 2,000)**, 3 threads, 4 to 8 minutes in total depending on the machine's load (MEASURED on Owls,
twice: setup 4 s, calibrate 138 s and 308 s, each island 45–48 s, merge 3 s):

```sh
mkdir -p run2k && cd run2k
B=../build/smcbvs4
export OMP_NUM_THREADS=3
$B gen --design AR --n 200 --p 2000 --seed 1 --out raw.bin --truth truth.json
$B prep --in raw.bin --out data.bin
$B setup --data data.bin --out setup.bin
$B calibrate --mode V --data data.bin --setup setup.bin --seed 1 --out calib.bin
$B island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out island_1.bin
$B island --mode V --island 2 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out island_2.bin
$B merge --mode V --Rp 2 --data data.bin --setup setup.bin --calib calib.bin --islands island_1.bin,island_2.bin --out fit.bin
```

Each command exits 0 and writes its `.json` record. The island records contain an `output_hash`; the same build on any
machine, with any thread count, gives the same value (for these inputs on Owls: island 1 `0x94b566338ba911de`; see
REPRODUCIBILITY.md §4).

**B. The test suite** (needs the repository checkout, GCC, CMake, and R with Rcpp, digest, jsonlite for the golden
comparisons against the reference engine):

```sh
export TMPDIR=<a scratch directory>        # the runner refuses to start without it
Scripts/SMC_BVS/engine_v4/tests/run_tests.sh --quick --threads 3
```

It configures and builds into `$TMPDIR/v4_build`, runs about 190 C++ test cases, the SLURM-driver tests and the golden
tests against the reference engine, and exits 0 only if everything passes. `--full` adds the long cases. MEASURED on
Owls with 3 threads: about 25 minutes including the build; 192 C++ cases, 38 driver tests, 540,419 golden checks.
The golden step builds in `$TMPDIR/wp4_golden`; a directory left there by another checkout makes CMake stop with
`does not match the source`, so delete it or use a fresh `TMPDIR`.

---

## 4. A first fit on one node (p = 10⁴)

This is the production pipeline at p = 10⁴ with R′ = 4 islands. It was run end to end on Owls (Xeon Gold 6148, 3
threads); every time below is **MEASURED** and shrinks roughly in proportion to the threads you give it.

```sh
mkdir -p run1e4 && cd run1e4
B=../build/smcbvs4
export OMP_NUM_THREADS=3

# data: AR(0.6) design, n = 200, p = 10,000, five true variables at columns 1000, 3000, 5000, 7000, 9000
$B gen --design AR --n 200 --p 10000 --seed 1 --out raw.bin --truth truth.json     # 2 s
$B prep --in raw.bin --out data.bin                                                # a few s
$B setup --data data.bin --out setup.bin                                           # 17 s

# calibration: one command, one node
$B calibrate --mode V --data data.bin --setup setup.bin --seed 1 --out calib.bin   # 12 min

# the islands: independent, run them one after another here (R' = 4; production uses 16)
for r in 1 2 3 4; do                                                               # 4 min each
  $B island --mode V --island $r --Rp 4 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out island_$r.bin
done

# merge, score, and build the law
$B merge --mode V --Rp 4 --data data.bin --setup setup.bin --calib calib.bin \
         --islands island_1.bin,island_2.bin,island_3.bin,island_4.bin --out fit.bin    # 6 s
$B eval --fit fit.bin --data data.bin --truth truth.json --out eval.bin                  # 14 s
$B post --fit fit.bin --data data.bin --out law.bin                                      # 6 s
```

Total about 30 minutes of wall time at 3 threads, of which 12 are calibration and 16 are islands. Peak memory was
0.3 GB for an island. The result on this data:

```
selection.hpm = [1000, 3000, 5000, 7000, 9000]      (the five true variables; outcome_class "correct")
pip_eq: the five true columns all ≥ 0.9999; the largest PIP of any other column is 0.038
evidence.logZ = -201.57   R_eff = 3.9993 of R' = 4   island spread: max sd of a PIP 0.0005
```

Things to know:

- **More cores.** `--threads k` speeds up every stage. The islands are independent: on a node with 16 cores you can run
  four islands at once with `--threads 4` each (the output does not depend on the thread count, REPRODUCIBILITY.md §2).
- **Seeds.** The sampler `--seed` must be the same for `calibrate` and every `island`; an island run with another seed than
  its `calib.bin` is refused. (`gen --seed` is the data seed, a separate number.)
- **Stopping.** An island can be stopped and resumed (REPRODUCIBILITY.md §6). `setup`, `calibrate` and `merge` have no
  checkpoint and are rerun from the start.
- **Fewer islands.** R′ = 4 gives a usable fit; the quality targets of the experiment (island-to-island spread of a PIP
  ≤ 0.005) are stated for R′ = 16.

---

## 5. The same fit on SLURM

`tools/slurm/p1m_driver.py` turns a small JSON *plan* into the job scripts for the whole pipeline and a `submit.sh`.
It is a **dry-run generator**: it never calls `sbatch`. You read what it wrote, copy the directory to the cluster, and run
`submit.sh` yourself.

```
setup[1..F] ──> calibrate[1..F] ──> islands[1..R′] (per fit) ──> merge ──> eval (+ post)
   array         array (aftercorr)    array (afterok)            task      task (afterok)
```

### 5.1 The plan

`plan_demo_1e4.json`, one fit at p = 10⁴ with R′ = 4 (the example plans in `tools/slurm/examples/` show more keys):

```json
{
  "batch": "demo_1e4",
  "mode": "V",
  "code_commit": "UNSET-for-a-local-demo",
  "binary": "bin/smcbvs4",
  "island_isa": "x86-64-v3",
  "core_h_cap": 200,
  "fits": [
    {"run_id": "demo_AR_n200_p1e4", "design": "AR", "p": 10000, "n": 200, "signal": "strong",
     "data_seed": 20261201, "seed": 1, "Rp": 4, "N": 2500}
  ]
}
```

| key | meaning |
|---|---|
| `batch` | name of this set of jobs (letters, digits, `_ . -`) |
| `mode`, `island_isa` | as in §1.2. A `V` plan must name an FMA ISA, otherwise the driver refuses it |
| `code_commit` | the frozen commit the binary is built from (recorded in every manifest) |
| `core_h_cap` | refuse to generate if the worst-case billed core-hours exceed this |
| `fits[]` | one entry per fit: design, `p`, `n`, `signal` (`strong`, `weak`, `null`), `data_seed`, sampler `seed`, `Rp` (= R′), `N` |
| `resources` (optional) | override CPUs, memory and time limit per stage; the defaults are tabulated by rung (10⁴, 10⁵, 10⁶) in `DEFAULT_RES` |
| `restart` (optional) | `{"attempts": 3, "margin_s": 600}`: resubmit islands that hit their time limit (REPRODUCIBILITY.md §6) |

### 5.2 Generate and read

```sh
export P1M_TEST_ROOT=$PWD     # lets the driver write under this directory (§5.5)
python3 Scripts/SMC_BVS/engine_v4/tools/slurm/p1m_driver.py --plan plan_demo_1e4.json \
        --out $PWD/dept/scripts/demo_1e4 --dept $PWD/dept
```

```
dry run: wrote 22 files to .../dept/scripts/demo_1e4; 1 fits, 8 tasks, worst case 34.0 billed core-h. Nothing was submitted.
```

The directory holds `stage_*.sbatch` (one per stage), `submit.sh`, `build.sh` and `env.sh` (compile the pinned binary
on the cluster), `manifests/` (one JSON per command, with the input hashes filled in at run time), `ledger_row.md` (the
worst-case cost line), `SHA256SUMS` (`submit.sh` verifies them first) and `plan.resolved.json` (the plan with every
default filled in: **read this before submitting**; it holds the CPUs, memory and time per stage).

The worst case is Σ(CPUs × time limit) over all tasks, i.e. what you would be billed if every task ran to its limit.

### 5.3 Run

On the cluster:

```sh
cd <scripts>/demo_1e4
mkdir -p code && git -C <clone> archive <code_commit> | tar -x -C code
bash build.sh                  # configures with -DV4_ISLAND_ISA=<island_isa>, builds smcbvs4, prints `version`
CONFIRM=yes bash submit.sh     # setup -> calibrate -> islands -> merge -> eval, with dependencies
```

Each stage writes into `<dept>/scratch/runs/<batch>/<run_id>/` (`data.bin`, `setup.bin`, `calib.bin`, `island_<r>.bin`,
`fit.bin`, `eval.bin`, `law.bin`, `cost/`, `log/`, `manifests/`) — the same files as §4, produced by the same commands.

### 5.4 Run the generated scripts without SLURM

The stage scripts are plain bash; SLURM variables are the only thing they need from the scheduler. The driver's own tests
run them this way, and it is the way to check a plan on one machine before submitting. For a small plan (p = 2,000):

```sh
S=$PWD/dept/scripts/<batch>                      # the generated directory
mkdir -p $S/bin && cp build/smcbvs4 $S/bin/smcbvs4 && echo true > $S/env.sh   # no module system needed
mkdir -p $PWD/dept/scratch/{slurm_out,tmp,runs/<batch>}
export SLURM_JOB_ID=1 SLURM_CPUS_PER_TASK=3
SLURM_ARRAY_TASK_ID=1 bash $S/stage_setup.sbatch
SLURM_ARRAY_TASK_ID=1 bash $S/stage_calibrate.sbatch
for r in 1 2; do SLURM_ARRAY_TASK_ID=$r bash $S/stage_islands.sbatch 1; done    # argument: the fit's index
bash $S/stage_merge.sbatch 1 && bash $S/stage_eval.sbatch 1
```

### 5.5 What is specific to the Rice NOTS cluster

The driver was written for one cluster and says so in its scripts. Before using it elsewhere, know that:

- every `.sbatch` hard-codes `--account=commons --partition=commons --qos=nots_commons --constraint=sapphirerapids`
  (in `p1m_driver.py`, the `#SBATCH` header block);
- `env.sh` loads the NOTS modules `GCC/14.3.0` and `CMake/3.31.8` and checks the compiler version;
- all paths must be inside a *department folder* (`$HOME/SMC_Engineering_Department`, or the directory named by
  `P1M_TEST_ROOT`, as in §5.2). The driver itself never calls `sbatch`; only the generated `submit.sh` does.

On another cluster, edit those three places in the generated scripts (or in `p1m_driver.py`), and keep one rule from §1.2:
every task of a fit runs the same binary, built once.

---

## 6. Reading the results

### 6.1 The records and `fit.json`

Every command writes `<out>.json`. The merge's record, `fit.bin.json` — called `fit.json` in the documents — is short:
scalars and hashes only. The full content, including the PIP vectors, is in `fit.bin`.

| field | meaning |
|---|---|
| `status` | `completed` or a failure name (§7). **Check this first**; no estimate is written unless the status is `completed`. |
| `fit_state`, `reason` | `completed`, and an empty `reason`, unless something went wrong (`reason` then names the file, the value and the limit) |
| `estimates_available` | `true` if the fit has estimates. When `false`, no field below exists |
| `Rp` | number of islands merged |
| `logZ` | log of the model evidence, estimated as the mean over the R′ islands |
| `logZ_T` | log of the evidence of the *stored* models only: a **deterministic lower bound** on log Z. Never an upper bound |
| `R_eff` | effective number of islands, 1/Σ W_r². Close to R′ means all islands agree on the evidence; far below means a few islands dominate |
| `hpm_F` | log posterior (unnormalised) of the highest-posterior model found |
| `fit_bin` | SHA-256 content hash of `fit.bin` |
| `inputs` | content hash of every input file (`data.bin`, `setup.bin`, `calib.bin`, each `island_r.bin`) |
| `island_isa` | the ISA family of the merge binary (§1.2) |
| `timings` | seconds: `merge_tail_seconds` (whole command), `merge_islands_seconds`, `tail_local_seconds` (final local search), `ls0_seconds`. Execution statistics, not part of the result |
| `binary` | git commit, compiler, flags, libm identity and self-test of the program that wrote the record |
| *list-PIP fields* | *(planned: the PIP list fields land with the list-PIP output; this table will name them.)* |

### 6.2 Posterior inclusion probabilities

`fit.bin` has three PIP vectors, each of length p (indexes are **0-based** columns of `data.bin`; `eval` and
`truth.json` report 1-based):

| section | estimator |
|---|---|
| `pip_eq` | **primary.** Mean of the R′ islands' Rao–Blackwell PIPs, equal weights. The median-probability model is `pip_eq > 0.5` |
| `pip_Z` | the same islands weighted by their evidence (W_r = Z_r / Σ Z_r) |
| `pip_T` | from the merged store alone: Σ over stored models of w·1[j ∈ S], with w ∝ e^F normalised over the store |
| `pip_r` | R′ × p: each island's own vector (for spread checks) |
| `hpm_S`, `mpm` | the HPM and the MPM (`pip_eq > 0.5`) |
| `mode_S` | the start law's mode model (from `setup`) |

Reading them in R:

```r
source("Scripts/SMC_BVS/engine_v4/tools/v4_read.R")
f   <- v4_read("fit.bin")
pip <- f$get("pip_eq")
which(pip > 0.5)               # the median-probability model, 1-based
f$get("hpm_S") + 1L            # the HPM, 1-based
```

Or in Python without dependencies. A `.bin` file is a 128-byte header, then one 128-byte entry per section (name,
dtype, dims, offset, length, SHA-256), then the data (`INTERFACES.md` §5.1; little-endian):

```python
import struct
raw = open("fit.bin", "rb").read()
secs = {}
for i in range(struct.unpack_from("<I", raw, 20)[0]):
    b = 128 + 128 * i
    name = raw[b:b + 48].split(b"\0")[0].decode()
    dtype = struct.unpack_from("<I", raw, b + 48)[0]                 # 1 = float64, 2 = int32, 9 = JSON
    off, length = struct.unpack_from("<QQ", raw, b + 72)
    secs[name] = (dtype, off, length)
dtype, off, length = secs["pip_eq"]
pip = struct.unpack("<%dd" % (length // 8), raw[off:off + length])
print([j + 1 for j, v in enumerate(pip) if v > 0.5])               # 1-based columns of the MPM
```

### 6.3 The evaluator's record (simulations)

`eval.bin.json` scores a fit against `truth.json` (schema `smcbvs4.eval/1`):

| block | contents |
|---|---|
| `selection` | HPM and MPM against the truth: exact match, Hamming distance, TP/FP/FN, and `outcome_class`: `correct`, `posterior` (the HPM scores higher than the truth: the posterior prefers another model), `search` (the truth scores higher than the HPM: the sampler missed it), `tie`. Also where the HPM came from (`prov_*`) |
| `pip` | for each estimator: largest PIP over true-null variables, smallest over true variables, Brier score, 20 reliability bins; island spread (`island_spread.max_sd`; the target is ≤ 0.005) |
| `evidence` | log Ẑ, per-island log Ẑ_r, their spread, `R_eff`, a Markov lower confidence bound (`logZ_lower95`, never an upper bound) |
| `store` | stored-model count, `logZ_T`, the dropped mass, and an honest label: π̂(T) is a noisy ratio, not a bound |
| `dist` | Hellinger-distance summaries of the HPM, the MPM and the store law against the oracle; prediction error; held-out test MSE and log predictive density |


---

## 7. Input data, limits and exit codes

**Data.** `gen` creates simulated designs (IND, AR, BLK, ADJ-OPP; `--rho`, `--s0`, `--sigma` set the correlation, the
number of true variables and the noise). Real data enters as a `raw.bin` (sections `X_cm`, a column-major n×p `float64`
matrix, `y` and `meta`; the container format is in `INTERFACES.md` §5.1). **No importer for your own data ships yet.**
Until one does, use `gen`, or write a `raw.bin` in the format of §5.1.

**Sizes.** K, the largest model size, is min(p, n/2). The sampler stores about 40·p models, so memory grows with p: at
p = 10⁴ an island needs about 0.3 GB; at p = 10⁶ the planned task sizes are tens of GB (`DEFAULT_RES["1e6"]` in the driver,
and `tools/slurm/T5_AND_PILOT.md`). Every command accepts `--mem-budget BYTES` and refuses *before* allocating if its plan
does not fit (exit 11).

**Exit codes.** Exit `0` is success and `10 + status` is a failure, with the same words in the record's `status` and `reason`:

| exit | status | meaning |
|---|---|---|
| 0 | `completed` | |
| 11 | `resource_limit` | not admitted by `--mem-budget`, or out of memory |
| 12 | `numerical_failure` | a score failed numerically; the reason names the step |
| 13 | `invalid_input` | bad argument, missing or wrong-mode file, hash mismatch, binary/libm mismatch |
| 14 | `io_error` | cannot read or write a file |
| 15 | `internal_error` | an invariant was violated: report it |
| 16 | `schedule_limit` | `compat`/`law` calibration only |
| 20 / 21 | `completed` | `prep` found no usable predictors / a constant response; no `data.bin` is written |
| 22 | `completed` | an island stopped on `--stop-after-s` and wrote a checkpoint: not a failure, rerun to resume |

---

## 8. Where to go next

| file | for |
|---|---|
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | what "same bits" guarantees, the ISA and libm pins, how to verify hashes, the restart guide |
| [INTERFACES.md](INTERFACES.md) | the binding contract: file formats, record fields, statuses, the changelog |
| [tools/slurm/T5_AND_PILOT.md](tools/slurm/T5_AND_PILOT.md) | the 10⁵ and 10⁶ commands, ISA rules, cost tables |
| [tools/slurm/T6_AND_RESTART.md](tools/slurm/T6_AND_RESTART.md) | the restart chain and the kill-and-resume test |
| [DEV_NOTES.md](DEV_NOTES.md) | the component table (WP1), fixtures, test inventory |
| `src/eval/README_WP5.md` | everything `eval` and `post` compute |
