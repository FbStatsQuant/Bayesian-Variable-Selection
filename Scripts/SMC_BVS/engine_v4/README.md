# smcbvs4 — large-p Bayesian variable selection by sequential Monte Carlo

`smcbvs4` does Bayesian variable selection in the Gaussian linear model. It samples the posterior over sets of predictors
(models) with a sequential Monte Carlo (SMC) sampler, for p from a few thousand up to 10⁶ predictors. The model is that of
the R reference implementation SMC-BVS v3 (a g-prior slab and a Beta-Binomial BB(1, p) prior on the model size). It is one
command-line program in C++20 with OpenMP. The same program runs on a single multi-core node and, through a job-script
generator, on a SLURM cluster.

What you get from a fit:

- the highest-posterior model (HPM) and the median-probability model (MPM);
- posterior inclusion probabilities (PIPs) for every variable, from three estimators (`pip_eq`, `pip_Z`, `pip_T`, §6);
- the model evidence log Ẑ, with a measure of how well the independent runs agree;
- a stored posterior law over about 40·p models (`law.bin`) for prediction and uncertainty summaries.

Two properties are built in and documented in [REPRODUCIBILITY.md](REPRODUCIBILITY.md): **the same inputs on the same
build give the same bits, whatever the thread count, the schedule or a restart**, and every output file records the
binary, compiler flags and math library that produced it. What is and is not guaranteed across *machines* is stated there
exactly.

> **Status.** Numbers marked **MEASURED** were obtained by running the command shown, on the Rice machine "Owls", with the
> engine at commit `caa10f0e` (later changes to this guide's base are driver-only and do not affect them). The simulation
> generator `gen` is the supported way to create data; for your own data see §8. Fields marked *(planned)* land later.

Contents: 1 Requirements and build · 2 How a fit is organised · 3 Check the install · 4 A first fit on one node (p = 10⁴) ·
5 The same fit on SLURM · 6 Reading the results · 7 Command reference · 8 Input data, limits and exit codes ·
9 Where to go next

**Words used in this guide.**

| term | meaning |
|---|---|
| particle, island | a particle is one candidate model with a weight (N = 2,500 per island). An **island** is one independent SMC run; a fit merges R′ of them |
| φ-grid, offer floor | the tempering ladder the sampler climbs, and the score below which candidate models are not stored; both are chosen once by `calibrate` |
| HPM, MPM, PIP | highest-posterior model; median-probability model (variables with PIP > 0.5); posterior inclusion probability of one variable |
| bit form, class A | the two arithmetics. The **bit form** reproduces the R reference implementation (`Scripts/SMC_BVS/core/`, "revision D") bit for bit. **Class A** is the vectorised, fused-multiply-add arithmetic of the large-p sampler (mode V); its bits depend on the build (§1.2) |
| mode | `V` (the large-p sampler, used here), `law` (the reference method with addressed random streams and threads) or `compat` (bit-identical to the reference's serial streams; per the engineering spec it is feasible up to about p = 5,000 and it is not measured here) |
| Owls, NOTS | Rice University machines: Owls is a shared Intel Xeon Gold 6148 (Skylake) server used for development; NOTS is Rice's SLURM cluster (Sapphire Rapids nodes) |

---

## 1. Requirements and build

| need | detail |
|---|---|
| CPU | x86-64 with AVX2 and FMA. |
| operating system | **Measured: RHEL 9-family Linux (glibc 2.34, el9) on Intel CPUs** (Owls: Xeon Gold 6148; NOTS: Sapphire Rapids). Other distributions, other glibc versions and AMD or Arm CPUs are untested and may be refused at the first command (§1.3). |
| compiler | GCC ≥ 11 (C++20). Tested with 11.5 (Owls) and 14.3 (NOTS). |
| CMake | ≥ 3.20 |
| OpenMP | required (it ships with GCC). |
| Python 3 | standard library only; needed for the SLURM driver (§5) and the snippets below. |
| R (optional) | only for the golden tests and for reading result files with `tools/v4_read.R`. |

No network access is needed at configure or build time.

### 1.1 Get the code and build

```sh
git clone https://github.com/FbStatsQuant/Bayesian-Variable-Selection.git && cd Bayesian-Variable-Selection
git checkout exp/P1M-engine          # or the release tag, once there is one
cmake -S Scripts/SMC_BVS/engine_v4 -B build -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA=x86-64-v3
make -C build -j3 smcbvs4
build/smcbvs4 version
```

The build takes about a minute with 3 jobs (MEASURED: 57 s). `version` prints the *binary block*: git commit, compiler,
flags, island ISA and the libm identity with its self-test. Check these three lines:

```
"island_isa": "x86-64-v3",
"island_fma": true,
"pass": true            (inside "self_test")
```

Do not worry that `"flags"` ends in `-march=x86-64-v2`: the bit-form libraries are always built for x86-64-v2, and the
island ISA you chose applies to the class-A sampler kernels only (§1.2).

### 1.2 Choose the island ISA once, and keep it

`-DV4_ISLAND_ISA=<march>` sets the instruction set of the sampler's kernels. **A fit must use one FMA family end to end**:

- Use `x86-64-v3` (AVX2 + FMA) or newer (`x86-64-v4`, `sapphirerapids`). Class-A values from these agree bit for bit
  (MEASURED: x86-64-v3 = x86-64-v4 on Owls; a Rice NOTS run found `sapphirerapids` = `x86-64-v3`, recorded in
  `Docs/Experiments/P1M/results/T5_1e5.md`). REPRODUCIBILITY.md §4.4 gives the reference hash of each build.
- Without the option the build is `portable` (no FMA in the kernels). It works, but its class-A results differ from the
  FMA builds *by design*, and the engine refuses to mix them: an island built with `portable` will not run against a
  `calib.bin` made by an `x86-64-v3` build (REPRODUCIBILITY.md §5 shows the refusal).
- The Rice NOTS production builds use `sapphirerapids`.

### 1.3 The libm pin, and what to do when it refuses

Class-A results depend on the last bit of `exp`, `log` and `lgamma`, so the engine does not bundle a math library. It
binds to glibc 2.34's libm (FMA variant). At the start of every command except `info` and `version` it runs a self-test
that must reproduce reference results; otherwise the command stops with `invalid_input` (exit 13) before doing any work.

Only RHEL 9-family systems have been measured. The test keys on function results, not on the library file, so another
system may pass or fail, and nobody has checked which. **To see whether your machine can run the engine, run
`smcbvs4 version` and look at `"pass"`.** If it is `false`, the machine cannot run the engine: use a RHEL 9-family system
(Rocky Linux 9, AlmaLinux 9) or a container of one on an AVX2+FMA CPU. When the refusal fires the record says
`libm self-test failed for log, exp, …: bit-form results would differ from the reference (Owls = NOTS) bits (INTERFACES §6)`;
"Owls = NOTS" means the two Rice machines the reference bits were measured on. `tests/PMATH_REPORT.md` has the
measurements.

---

## 2. How a fit is organised

A fit is a pipeline of separate commands. Each reads files and writes one file plus a JSON *record* (`<out>.json`, the same
name with `.json` appended) holding the status, the inputs' hashes, timings and the binary block. Every command also
prints that record on stdout; the text is the same as `<out>.json` and can be ignored (`> /dev/null`).

```
gen ──> prep ──> setup ──> calibrate ──> island 1..R′ ──> merge ──> eval ──> (post)
raw.bin  data.bin  setup.bin   calib.bin     island_r.bin      fit.bin    eval.bin    law.bin
```

| command | does | output | cost (p = 10⁴, n = 200, 3 threads; MEASURED) |
|---|---|---|---|
| `gen` | simulates data (designs IND, AR, BLK, ADJ-OPP) and the truth file | `raw.bin`, `truth.json` | 2 s |
| `prep` | standardises the columns and drops constant ones | `data.bin` | a few s |
| `setup` | correlation graph, blocks, the table of models around every variable, the start law; finds exactly duplicated columns and treats them as one group | `setup.bin` (97 MB) | 17 s |
| `calibrate` | chooses the φ-grid and the offer floor; runs a pilot island | `calib.bin` | 12 min |
| `island` | one independent SMC run (N = 2,500 particles); you run R′ of them | `island_<r>.bin` | 4 min each |
| `merge` | combines the R′ islands: stores, PIPs, evidence, final local search | `fit.bin` | 6 s |
| `eval` | scores the fit against the truth (simulations) | `eval.bin` | 14 s |
| `post` | builds the posterior law from the merged store | `law.bin` | 6 s |

R′ is the number of independent islands. Production uses **R′ = 16**; the examples below use fewer to finish sooner.
The islands are independent, so they are what you spread over cores or over a SLURM job array. Costs grow quickly with
p; `tools/slurm/T5_AND_PILOT.md` has the 10⁵ and 10⁶ commands and their cost estimates.

**Threads: pass `--threads` yourself.** The defaults differ by command: `setup` and `island` use `OMP_NUM_THREADS` (every
core if it is unset), but **`calibrate`, `merge`, `eval` and `post` use one thread unless you pass `--threads`** (an
unthreaded `calibrate` at p = 2,000 took 308 s against 138 s with 3 threads). The examples below set `T=3` and pass
`--threads $T` to all of them. `smcbvs4 info FILE` prints a file's header and section table and verifies every hash;
`smcbvs4 info FILE --meta 1` reads only the header and the meta section (seconds on a multi-GB file).

---

## 3. Check the install

Two checks, from fast to thorough.

**A. Smoke test (p = 2,000)**, 3 threads, about 4 minutes (MEASURED on Owls: setup 4 s, calibrate 138 s, each island
45–48 s, merge 3 s, eval and post a few seconds each):

```sh
mkdir -p run2k && cd run2k
B=../build/smcbvs4; T=3
$B gen --design AR --n 200 --p 2000 --seed 1 --out raw.bin --truth truth.json
$B prep --in raw.bin --out data.bin
$B setup --data data.bin --out setup.bin --threads $T
$B calibrate --mode V --data data.bin --setup setup.bin --seed 1 --out calib.bin --threads $T
$B island --mode V --island 1 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out island_1.bin --threads $T
$B island --mode V --island 2 --Rp 2 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out island_2.bin --threads $T
$B merge --mode V --Rp 2 --data data.bin --setup setup.bin --calib calib.bin --islands island_1.bin,island_2.bin --out fit.bin --threads $T
$B eval --fit fit.bin --data data.bin --truth truth.json --out eval.bin --threads $T
python3 -c "import json; r = json.load(open('eval.bin.json')); print(r['selection']['hpm'], r['selection']['outcome_class'], r['evidence']['R_eff'])"
```

**What success looks like.** Every command exits 0 and writes its `.json` record, and the last line prints

```
[200, 600, 1000, 1400, 1800] correct 1.9995...
```

that is, the highest-posterior model is exactly the five true variables (`truth.json` lists them), `outcome_class` is
`correct`, and `R_eff` is close to R′ = 2. For these inputs on Owls the island records also carry
`output_hash` `0x94b566338ba911de` (island 1); the same build gives the same value with any thread count
(REPRODUCIBILITY.md §4).

**B. The test suite** (needs the repository checkout, GCC, CMake, and R with Rcpp, digest and jsonlite for the golden
comparisons against the reference implementation):

```sh
export TMPDIR=<a scratch directory>        # the runner refuses to start without it; the build goes to $TMPDIR/v4_build
Scripts/SMC_BVS/engine_v4/tests/run_tests.sh --quick --threads 3
```

It builds, runs the C++ test cases, the SLURM-driver tests, the competitor-harness checks and the golden tests, and ends
with one summary line that gives PASS, FAIL or SKIPPED and the time for each suite. It exits 0 only if every suite ran and
passed. **Without R the golden and competitor suites are SKIPPED and the exit status is 3** (a failure is 1); pass
`--allow-skip` to accept that on purpose. `--list` names the suites, `--only a,b` runs some of them, `--full` adds the long
cases. MEASURED on Owls with 3 threads: about 25 minutes for `--quick` including the build (198 C++ cases, 55 driver tests,
540,419 golden checks), about 2 hours for `--full`. A build or golden directory left in `TMPDIR` by another checkout is now
reported as such (`was configured for another checkout`) instead of CMake's `does not match the source`. What each suite
covers, the timings, what to do when a pinned reference moves and the other traps are in [TESTING.md](TESTING.md).

---

## 4. A first fit on one node (p = 10⁴)

This is the production pipeline at p = 10⁴ with R′ = 4 islands. It was run end to end on Owls (Xeon Gold 6148, 3
threads); every time below is **MEASURED** and shrinks roughly in proportion to the threads you give it.

```sh
mkdir -p run1e4 && cd run1e4
B=../build/smcbvs4; T=3

# data: AR(0.6) design, n = 200, p = 10,000, five true variables at columns 1000, 3000, 5000, 7000, 9000
$B gen --design AR --n 200 --p 10000 --seed 1 --out raw.bin --truth truth.json     # 2 s
$B prep --in raw.bin --out data.bin                                                # a few s
$B setup --data data.bin --out setup.bin --threads $T                              # 17 s

# calibration: one command, one node
$B calibrate --mode V --data data.bin --setup setup.bin --seed 1 --out calib.bin --threads $T   # 12 min

# the islands: independent, run them one after another here (R' = 4; production uses 16)
for r in 1 2 3 4; do                                                               # 4 min each
  $B island --mode V --island $r --Rp 4 --seed 1 --data data.bin --setup setup.bin --calib calib.bin --out island_$r.bin --threads $T
done

# merge, score, and build the law
$B merge --mode V --Rp 4 --data data.bin --setup setup.bin --calib calib.bin \
         --islands island_1.bin,island_2.bin,island_3.bin,island_4.bin --out fit.bin --threads $T   # 6 s
$B eval --fit fit.bin --data data.bin --truth truth.json --out eval.bin --threads $T                # 14 s
$B post --fit fit.bin --data data.bin --out law.bin --threads $T                                    # 6 s
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
- **Stopping.** An island can be stopped and resumed (REPRODUCIBILITY.md §6). Resume with **the same binary file** that
  started the island: a checkpoint written by another build, even a rebuild of the same commit, is refused with
  `invalid_input` (exit 13, `checkpoint … belongs to another configuration or binary`); delete the `.ckpt.a` and `.ckpt.b`
  files to start over. `setup`, `calibrate` and `merge` have no checkpoint and are rerun from the start.
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
| `code_commit` | the frozen commit the binary is built from. **On this path it is the authoritative record of the code**: a binary built from a `git archive` tree has no `.git` and reports `git_commit` `unknown` in `version` |
| `core_h_cap` | refuse to generate if the worst-case billed core-hours exceed this |
| `fits[]` | one entry per fit: design, `p`, `n`, `signal` (`strong`, `weak`, `null`), `data_seed`, sampler `seed`, `Rp` (= R′), `N` |
| `resources` (optional) | override CPUs, memory and time limit per stage; the defaults are tabulated by rung (10⁴, 10⁵, 10⁶) in `DEFAULT_RES` |
| `restart` (optional) | `{"attempts": 3, "margin_s": 600}`: resubmit islands that hit their time limit (REPRODUCIBILITY.md §6) |

### 5.2 Generate and read

The driver only writes inside a *department folder*. Outside the Rice setup that means a directory under a scratch
directory named by **`TMPDIR`**, with `P1M_TEST_ROOT` set to a directory inside `$TMPDIR` (the driver refuses with
`refusing: --dept … is outside the department folder` and exit 64 if `TMPDIR` is unset or `P1M_TEST_ROOT` is not inside it):

```sh
REPO=<the clone>                                   # the directory that contains Scripts/
export TMPDIR=<a scratch directory>
mkdir -p $TMPDIR/demo && cd $TMPDIR/demo           # save the plan of §5.1 here as plan_demo_1e4.json
export P1M_TEST_ROOT=$PWD
python3 $REPO/Scripts/SMC_BVS/engine_v4/tools/slurm/p1m_driver.py --plan plan_demo_1e4.json \
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
run them this way, and it is the way to check a plan on one machine before submitting. In the directory of §5.2, for a
small plan (p = 2,000, the §5.1 plan with `"p": 2000` and `"Rp": 2`), after the generator has written
`dept/scripts/<batch>`:

```sh
S=$PWD/dept/scripts/<batch>                      # the generated directory
mkdir -p $S/bin && cp $REPO/build/smcbvs4 $S/bin/smcbvs4 && echo true > $S/env.sh   # no module system needed
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
- all paths must be inside a *department folder*: `$HOME/SMC_Engineering_Department`, or a `P1M_TEST_ROOT` that lies inside
  `$TMPDIR` (§5.2). The generated scripts check `P1M_TEST_ROOT` only. The driver itself never calls `sbatch`; only the
  generated `submit.sh` does.

On another cluster, edit those three places in the generated scripts (or in `p1m_driver.py`), and keep one rule from §1.2:
every task of a fit runs the same binary, built once.

---

## 6. Reading the results

### 6.1 The records and `fit.json`

Every command writes `<out>.json`. The merge's record, `fit.bin.json` — called `fit.json` in the documents — is short:
scalars and hashes only. The full content, including the PIP vectors, is in `fit.bin`.

| field | meaning |
|---|---|
| `status` | `completed` or a failure name (§8). **Check this first**; no estimate is written unless the status is `completed` |
| `fit_state`, `reason` | `fit_state` is `completed`, `incomplete` (the merge refused its inputs), `not_admitted` (over `--mem-budget`) or `failed`; `reason` is empty unless something went wrong, and then names the file, the value and the limit |
| `estimates_available` | `true` if the fit has estimates. When `false`, `logZ`, `logZ_T` and `R_eff` are absent (the fields below them marked * are always written) |
| `Rp` * | number of islands merged |
| `logZ` | log of the model evidence: the log of the **mean** of the R′ island evidences, log((1/R′) Σ e^{logZ_r}) |
| `logZ_T` | log of the evidence of the *stored* models only: a **deterministic lower bound** on log Z. Never an upper bound |
| `R_eff` | effective number of islands, 1/Σ W_r² with W_r the islands' evidence shares. Close to R′ means the islands agree on the evidence; far below means a few dominate (the largest share, `max_W`, is in the `meta` section of `fit.bin`) |
| `hpm_F` | log posterior (unnormalised) of the highest-posterior model found; present whenever a model was found |
| `fit_bin` * | SHA-256 content hash of `fit.bin` |
| `inputs` * | content hash of every input file (`data.bin`, `setup.bin`, `calib.bin`, each `island_r.bin`) |
| `island_isa` * | the ISA family of the merge binary (§1.2) |
| `timings` * | seconds: `merge_tail_seconds` (whole command), `merge_islands_seconds`, `tail_local_seconds` (final local search), `ls0_seconds`. Execution statistics, not part of the result |
| `binary` | git commit, compiler, flags, libm identity and self-test of the program that wrote the record |
| *list-PIP fields* | *(planned: the PIP list fields land with the list-PIP output; this table will name them.)* |

### 6.2 Posterior inclusion probabilities, and which column is which

`fit.bin` has three PIP vectors, each of length p:

| section | estimator |
|---|---|
| `pip_eq` | **primary.** Mean of the R′ islands' Rao–Blackwell PIPs, equal weights. The median-probability model is `pip_eq > 0.5` |
| `pip_Z` | the same islands weighted by their evidence (W_r = Z_r / Σ Z_r) |
| `pip_T` | from the merged store alone: Σ over stored models of w·1[j ∈ S], with w ∝ e^F normalised over the store |
| `pip_r` | R′ × p: each island's own vector (for spread checks) |
| `hpm_S`, `mpm` | the HPM and the MPM (`pip_eq > 0.5`) |
| `mode_S` | the start law's mode model (from `setup`) |

**Which column is "column j".** Every index in `fit.bin`, `law.bin` and the islands is a position in `data.bin`, not a column
of your `raw.bin`. `prep` removes constant columns and renumbers the rest, so after it a variable's position can be
smaller than its place in your matrix. Positions in the sections are **0-based**; `eval` and `truth.json` report 1-based
numbers (and `truth.json` in terms of the raw columns). `data.bin` keeps the map in its `kept` section: `kept[i]` is the
1-based raw column of data position i (0-based i), and `dropped` lists the removed raw columns (also in the `prep`
record). With no constant column, `kept` is 1, 2, …, p and nothing shifts; that is why the simulated examples look
unshifted. Example: raw column 5 is constant, so `p_raw` = 300, p = 299, `dropped` = [5] and `kept` = (1, 2, 3, 4, 6, 7, …):
the variable that sits at 0-based position 5 of `pip_eq` is raw column 7.

A reader for both files, in Python without dependencies (a `.bin` file is a 128-byte header, then one 128-byte entry per
section — name, dtype, dims, offset, length, SHA-256 — then the data; `INTERFACES.md` §5.1; little-endian):

```python
import struct

def read_bin(path):
    """Return {section name: list of numbers} (float64 and int32 sections; JSON sections as bytes)."""
    raw, out = open(path, "rb").read(), {}
    for i in range(struct.unpack_from("<I", raw, 20)[0]):
        b = 128 + 128 * i
        name = raw[b:b + 48].split(b"\0")[0].decode()
        dtype = struct.unpack_from("<I", raw, b + 48)[0]                 # 1 = float64, 2 = int32, 9 = JSON
        off, length = struct.unpack_from("<QQ", raw, b + 72)
        data = raw[off:off + length]
        out[name] = (struct.unpack("<%dd" % (length // 8), data) if dtype == 1 else
                     struct.unpack("<%di" % (length // 4), data) if dtype == 2 else data)
    return out

fit, data = read_bin("fit.bin"), read_bin("data.bin")
mpm = [j for j, v in enumerate(fit["pip_eq"]) if v > 0.5]                # 0-based positions in data.bin
print("MPM, raw columns (1-based):", [data["kept"][j] for j in mpm])
print("HPM, raw columns (1-based):", [data["kept"][j] for j in fit["hpm_S"]])
```

The same in R, from the repository root with the files' paths adjusted (`tools/v4_read.R` reads `float64`, `int32` and JSON sections):

```r
source("Scripts/SMC_BVS/engine_v4/tools/v4_read.R")
fit <- v4_read("fit.bin");  dat <- v4_read("data.bin")
kept <- dat$get("kept")                              # raw column (1-based) of each data position
kept[which(fit$get("pip_eq") > 0.5)]                 # the MPM, as raw columns
kept[fit$get("hpm_S") + 1L]                          # the HPM, as raw columns
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

## 7. Command reference

Flags are written `--name value`. A flag a command does not know is **silently ignored**, so a misspelling (`--thread 3`,
`--mem-budgt`) has no effect and no warning: check spelling against this table. Every command accepts `--record path`
(the record's name, default `<out>.json`); the commands that read `--manifest m.json` (the SLURM driver's form) take
their inputs and parameters from it, and an explicit flag that disagrees with the manifest is refused.

**Threads and memory budget, per command** (the two flags most often misunderstood):

| command | `--threads` default | `--mem-budget` |
|---|---|---|
| `gen`, `prep` | `OMP_NUM_THREADS` | not used (ignored) |
| `setup` | `OMP_NUM_THREADS` | **gigabytes**, a decimal number (`--mem-budget 8` = 8 GB); admission check on the setup's accounted peak. A value in bytes gives it billions of GB, i.e. no protection |
| `calibrate`, `island`, `merge` | `calibrate`: 1; `island`: `OMP_NUM_THREADS`; `merge`: 1 | **bytes** (whole number, 0 = off), or `--mem-budget-gb G` for `island` and `merge`. It is the whole task's memory. Over budget the command stops before allocating, with exit 11 |
| `eval`, `post` | 1 | not used (ignored) |

| command | required | useful optional flags (default) |
|---|---|---|
| `gen` | `--design IND\|AR\|BLK\|ADJ-OPP`, `--n`, `--p`, `--seed`, `--out raw.bin` | `--truth truth.json`; `--rho` (0.6; 0.5 for BLK), `--s0` number of true variables, 0–5 (5), `--sigma` noise sd (1), `--a` signal amplitude (1 strong, 0.6 weak, 0 null), `--b` block size of BLK (20). `--seed` is the data seed |
| `gen-test` | the `gen` spec, `--ntest M`, `--cols 1,5,9`, `--out test.bin` | test rows for the given columns (used by `eval`) |
| `prep` | `--in raw.bin --out data.bin` (or `--from-r DIR`) | exits 20 (no usable predictors) or 21 (constant response) without writing `data.bin` |
| `setup` | `--data data.bin`, `--out setup.bin` | `--threads`, `--mem-budget` (GB), `--count-only 1` (report the accounting without building tables), `--file-mode compat\|law\|V` (law), `--partition truncated\|exact` (truncated), `--tau`, `--B` (advanced: leave the defaults) |
| `calibrate` | `--mode compat\|law\|V`, `--data`, `--setup`, `--seed` (1…2³¹−1), `--out calib.bin` | `--threads` (1), `--mem-budget` (bytes), `--cost-dir DIR` (per-island cost logs), `--plan-only 1` (with `--n --p`: print the memory plan, run nothing), `--I_max` (3) and `--refine_m` (1), both V mode only |
| `island` | `--mode`, `--island r`, `--seed`, `--data`, `--setup`, `--calib`, `--out island_r.bin`; `--Rp R′` (optional: checks that r ≤ R′) | `--threads`, `--mem-budget` (bytes) or `--mem-budget-gb`, `--G` particles per group (0 = the largest ≤ 256 that fits), `--tile` (128, 64…4096), `--ckpt 0\|1` (1), `--ckpt-every-s` (600), `--stop-after-s` (soft stop, exit 22), `--offer-floor 1\|0` (1; 0 = no floor, same merged science), `--plan-only 1` |
| `merge` | `--mode`, `--Rp R′`, `--data`, `--setup`, `--calib`, `--islands i1,…,iR′`, `--out fit.bin` | `--threads` (1), `--mem-budget` / `--mem-budget-gb`, `--chunk` (2048 items per parallel chunk) |
| `eval` | `--fit fit.bin`, `--data`, `--truth truth.json`, `--out eval.bin` | `--threads` (1), `--n-draws` (10,000), `--n-x` (4,000), `--n-test` (10,000), `--n-gh` (64), `--rel-cut` (1e-12), `--top-k` (1,000), `--tail-r` (1,000), `--tail-groups` (8), `--block-rows` (500), `--law law.bin`, `--seed`; details in `src/eval/README_WP5.md` |
| `post` | `--fit`, `--data`, `--out law.bin` | `--threads` (1), `--rel-cut` (1e-12), `--max-models` (1,000,000), `--draws`, `--seed` |
| `info` | `FILE` (or `--in FILE`) | `--meta 1` (header + section table + meta only), `--verify 0\|1` |
| `version` | — | prints the binary block |

`--N` on `island` is an assertion only: it must equal the N frozen in `calib.bin`.

---

## 8. Input data, limits and exit codes

**Data.** `gen` creates simulated designs. Your own data enters as a `raw.bin`: sections `X_cm` (a column-major n×p
`float64` matrix), `y` (n `float64`) and `meta`; the container format is in `INTERFACES.md` §5.1. **No importer ships
yet**, but a `raw.bin` is easy to write. This stdlib-only Python function writes one from p lists of n numbers (it was
tested with `prep` and a full fit):

```python
import array, hashlib, json, struct

def write_raw(path, cols, y):
    """Write a raw.bin for `smcbvs4 prep`. cols: p lists of n floats (one per predictor); y: n floats."""
    n, p = len(y), len(cols)
    meta = json.dumps({"source": "write_raw.py"}).encode()
    secs = [("X_cm", 1, n, p, array.array("d", [v for c in cols for v in c]).tobytes()),   # float64, n x p, column-major
            ("y", 1, n, 0, array.array("d", y).tobytes()),                                 # float64, n
            ("meta", 9, len(meta), 0, meta)]                                               # dtype 9 = JSON
    pad = lambda x: (x + 63) // 64 * 64                                                    # sections start on 64-byte offsets
    offsets, table, off = [], b"", pad(128 + 128 * len(secs))
    for name, dtype, d0, d1, data in secs:
        offsets.append(off)
        table += struct.pack("<48sIIQQQQ32s8s", name.encode(), dtype, 2 if d1 else 1, d0, d1, off, len(data),
                             hashlib.sha256(data).digest(), b"")
        off = pad(off + len(data))
    header = lambda t, c: struct.pack("<8sIIIIQ32s32s32s", b"SMCBVS4", 1, 1, 0, len(secs), off, t, c, b"")  # kind 1 = raw
    table_sha = hashlib.sha256(table).digest()
    content_sha = hashlib.sha256(header(bytes(32), bytes(32)) + table).digest()   # header with both hashes zeroed + table
    with open(path, "wb") as f:
        f.write(header(table_sha, content_sha) + table)
        for (_, _, _, _, data), o in zip(secs, offsets):
            f.write(bytes(o - f.tell()) + data)
        f.write(bytes(off - f.tell()))
```

A worked example with a **constant column**, which `prep` drops (n = 100, p = 300; the signal is in raw columns 4, 7 and
250; column 5 is constant):

```python
import random
random.seed(7)
n, p = 100, 300
cols = [[random.gauss(0, 1) for _ in range(n)] for _ in range(p)]
cols[4] = [1.0] * n                                   # raw column 5 (1-based) is constant
y = [2.0 * cols[3][i] - 1.5 * cols[6][i] + 1.0 * cols[249][i] + random.gauss(0, 1) for i in range(n)]
write_raw("raw.bin", cols, y)
```

```sh
$B prep --in raw.bin --out data.bin > /dev/null       # data.bin.json: "p_raw": 300, "p": 299, "dropped": [5]
```

then run `setup`, `calibrate`, the islands and `merge` as in §3 A with this `data.bin`. `read_bin` of §6.2 then maps the
result back: the MPM printed by the snippet is raw columns 4, 7 and 250, while the same variables sit at 0-based
positions 3, 5 and 248 of `pip_eq`. Everything in `fit.bin` counts positions in `data.bin`, so always map through `kept`.

**Sizes and disk.** K, the largest model size, is min(p, n/2). The sampler stores about 40·p models, so memory grows with
p: at p = 10⁴ an island needs about 0.3 GB; at p = 10⁶ the planned task sizes are tens of GB (`DEFAULT_RES["1e6"]` in the
driver, and `tools/slurm/T5_AND_PILOT.md`). Disk: the p = 2,000 smoke test writes about 53 MB; at p = 10⁴ `setup.bin` alone
is 97 MB and each island file several MB (MEASURED). Use `--mem-budget` (§7, mind the unit) to make a command refuse
instead of being killed.

**Exit codes.** Exit `0` is success and `10 + status` is a failure, with the same words in the record's `status` and `reason`.
[ERRORS.md](ERRORS.md) catalogues every status and exit code, the typical messages with what to do, and the driver's exits.
**Test the exit code, not only `status`**: for exits 20, 21 and 22 the record says `completed`.

| exit | status | meaning |
|---|---|---|
| 0 | `completed` | |
| 11 | `resource_limit` | not admitted by `--mem-budget`, or out of memory |
| 12 | `numerical_failure` | a score failed numerically; the reason names the step |
| 13 | `invalid_input` | bad argument, missing or wrong-mode file, hash mismatch, binary/libm mismatch, a foreign checkpoint |
| 14 | `io_error` | cannot read or write a file |
| 15 | `internal_error` | an invariant was violated: report it |
| 16 | `schedule_limit` | `compat`/`law` calibration only |
| 20 / 21 | `completed` | `prep` found no usable predictors / a constant response; no `data.bin` is written |
| 22 | `completed` | an island stopped on `--stop-after-s` and wrote a checkpoint: not a failure, no `island_<r>.bin`; rerun to resume |

**Limits at a glance.** x86-64 with AVX2 and FMA; one libm family (RHEL 9 / glibc 2.34 measured); no importer for your own
data (the writer above is the recipe); `merge` needs all R′ island files (no subset is ever pooled); a rebuilt binary
orphans every checkpoint of the old one; the SLURM driver is specific to Rice NOTS (§5.5).

---

## 9. Where to go next

| file | for |
|---|---|
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | what "same bits" guarantees (and where), the ISA and libm pins, how to verify hashes, the restart guide |
| [ERRORS.md](ERRORS.md) | every status and exit code of the engine and the SLURM driver: meaning, typical messages, what to do |
| [INTERFACES.md](INTERFACES.md) | the binding contract: file formats, record fields, statuses, the changelog |
| [tools/slurm/T5_AND_PILOT.md](tools/slurm/T5_AND_PILOT.md) | the 10⁵ and 10⁶ commands, ISA rules, cost tables |
| [tools/slurm/T6_AND_RESTART.md](tools/slurm/T6_AND_RESTART.md) | the restart chain and the kill-and-resume test |
| [TESTING.md](TESTING.md) | the test suites: what each covers, how long it takes, what a pass means, updating pinned references, the traps |
| [DEV_NOTES.md](DEV_NOTES.md) | the component table (WP1), fixtures, test inventory |
| `src/eval/README_WP5.md` | everything `eval` and `post` compute |
