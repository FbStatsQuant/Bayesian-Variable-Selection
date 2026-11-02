# JOB: LOWP pilot on NOTS (dev datasets; sizes the Regime L production runs)

Owner: LOWP thread. Revision 7c, 2026-10-30: GNU time resolution for NOTS (no /usr/bin/time; module binary time/1.9, verified, fail closed for the sizing arms; see section 5, "Environment in every task"). Revision 7, 2026-10-29: SMC step now runs the single frozen tree `code/core/v2_2_1` (staging check against `v2_2_1.SHA256SUMS`; P5 scan reported, never run automatically; details in `CHANGES_v2_2_1.md`; no gate threshold changed). Revision 6 (revisions 3 and 4 fixed the findings of the independent review (5 blocking, 8 should-fix, 2 minor), the charter changes D7/D8, and the final-confirmation findings FC5 to FC9 (shared EXACT validator, cleanup path boundary, benchmark runtime/scaling/wall evidence, exact library and provenance checks); revision 6 closes N1 (memory evidence must be finite and positive; labelled fallbacks; no accepted request <= 0), N2 (coherent fabricated posterior) and N3 (scaling hash/type validation, receipt temp folder); revision 5 closed RC1 (per-unit wall/CPU policy, NOT ACCEPTED labels), RC2 (scaling identity and coverage), RC4 (empty SMC HPM) and RC5 (wording). For OPS via HQ; charter section 6 format. **Needs a fresh independent review before OPS submits.** Nothing here touches production fits; dev datasets are excluded from all counts.

**Status: Gate met (HQ D26, D39, D45), rev 7d, submitted by OPS-4 2026-10-30** (STAMP 20261030T0712Z; jobs 2469168–2469179). Earlier run 20261030T0313Z (jobs 2467487–2467498) stopped at P0a (cross-platform last-bit regeneration differences; `ops/PILOT_FAIL_20261030T0313Z.md`), fixed in revision 7d (HQ D44: B1 P0a cross-platform generator check, B2 unlock when the lock never ran, B3 clean-up from memory). Local evidence: `LOCAL_TEST.md`, section "Revision 7".

Bundle folder: `ROOT/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/pilot/`. NOTS: `HOME = /home/fb31/projects/BVS/New_Campaign`, `SCR = /scratch/fb31/New_Campaign`. Pilot id `PID = <STAMP>_lowp_pilot`, `STAMP = YYYYMMDDTHHMMZ` (UTC, chosen when staging). **OPS reaches NOTS only through the configured `ssh nots` alias (pinned to loginx2, charter section 3, D8), one connection at a time, with batched commands**; no script of the bundle opens ssh.

## 0. Charter limits this bundle respects (section 2, D7)

| Rule | How the bundle complies |
|---|---|
| Campaign footprint in home <= 0.5 GiB (code, manifests, small inputs only) | everything staged sits in ONE folder `HOME/runs/<PID>` (~11.5 MB measured in disk blocks, + compile cache 2 to 5 MB); no logs and no results in home; the only cache in home is the small core `.cpp_cache` built inside that same pilot-owned folder (the enumerator cache is on scratch) |
| Total home < 9.6 GiB | `guard_check.sh` (below) before submission |
| ALL logs and bulky files on scratch | slurm output, unit logs, timing, reports, receipts, truth-lock evidence, accounting: `SCR/logs/<PID>`; results `SCR/results`; caches and TMPDIR `SCR/runs/<PID>_{cache,tmp}`. The only cache in home is the small (2 to 5 MB) core `.cpp_cache` built inside the pilot-owned `runs/<PID>/code/core/...` (removed with it; the enumerator's compile cache is on scratch). The only run bookkeeping in home is `RUN_HOME/JOBIDS.tsv` (< 1 KB, needed by clean-up and recovery) |
| `guard.sh` is OPS-owned | never edited or bypassed; `guard_check.sh` REFUSES unless it enforces the D7 limits (see section 5) |

## 1. Purpose and steps

Replace the local, noisy cost table of `RUN_DESIGN.md` section 2 by NOTS measurements, then size production. All on Sapphire Rapids (`--constraint=sapphirerapids`).

| Step | What |
|---|---|
| P0a | `lowp_verify_nots.R`, a **cross-platform generator check, not an identity check** (revision 7d, HQ D44). It regenerates all 1,200 production + 60 dev datasets. **Exact checks** (what the fits consume, and everything that is not floating point): the manifest grid and every seed field; the `foldid` hash; the file SHA-256 of every truth file (1,200 + 60) and of the six pilot input copies, and the sealed arrays' float64 hashes against the manifests; names, dims, column names and non-float fields. **Tolerance** for regenerated floating-point values against the SEALED values (eps, signal and beta of all 1,260 truth files; X and the five Y columns of the six pilot copies): `|regenerated - sealed| <= 1e-12 * max(1, |sealed|)`, all finite; the observed maxima go to `p0_verify/NOTS_REGEN_MAXIMA.csv` and the report. Why: R's normal draws differ by 1-3 ulp between R 4.4.1/Windows (the seal) and R 4.5.2/Linux (OPS-4: observed max relative 5.5e-16 in eps, about 1e-15 in X, foldid identical). The laptop-sealed files stay canonical and are what the fits read. Exit 0 PASS / 1 MISMATCH (an exact check or the tolerance fails) / 3 INCOMPLETE; **1 or 3 is a STOP** (job fails, all later steps are cancelled) |
| P0c | Linux truth-lock TEST (`code/lowp/tests/test_truth_lock_linux.sh`, ordinary user, home filesystem, on the study copy): lock, check unreadable, unlock, two recoveries. A **gate**; evidence on scratch |
| P0d | **WAVE LOCK**: both staged truth trees set to mode 000 and VERIFIED before any fitting job is released |
| P1 | Exact enumeration: 30 dev datasets at p = 20 (4 threads); the 6 scenarios at p = 30 r1 (16 threads); thread scaling on `dev_p0030_S4_r001`; score/aggregate checks (`R/pilot_bitid.R`) |
| P2 | SMC-BVS v2.2.1 (`code/core/v2_2_1/study/run_case.R`, regime L; core byte-identical to v2.2): 24 dev cases (p in {20,30} x S1..S6 x c in {c100,c050}, r1) + `--repeat 1` on 4 |
| P3 | The 8 benchmark methods on the same 24 cases (R 4.5.2, pinned read-only library, `--library`) |
| P8 | **WAVE UNLOCK** finalizer: truth restored to 755/444 (hashes unchanged) once every fitting job is terminal |
| P9 | collection after the restoration; then OPS runs `final_accounting.sh` (terminal snapshot incl. the collector) |
| P4 | `summarize_pilot.R` on the laptop: ACCEPTS or REJECTS (exit 0 / 2 / 3) |

All CLIs are the production ones on real dev ids with `--development --study <dev root>`. SMC uses the production allocation `--mem-gb 2 --hours 4`.

**Sample coverage (what the timings represent).** Fit-time measurements exist only for: enumeration at p = 20 on 30 datasets (S1..S6 x r1..r5), enumeration at p = 30 on 6 datasets (S1..S6, r1), SMC and the 8 benchmarks on 12 datasets x 2 scales (p in {20,30} x S1..S6, r1), 4 SMC repeat fits. The 60-row regeneration check proves the generator, **not fit cost**. Production extrapolation assumes replicates within a cell cost alike and that rare SMC escalations (none expected in 28 fits) are absent; keep a margin. RUN_DESIGN section 4 already states these subsets.

## 2. Sealing and staging (laptop)

```
Rscript "<CAMP>/code/lowp/R/lowp_seal.R" "<SEALED>"                       # once; ~72 MB, read-only, never overwrites
bash "<CAMP>/code/lowp/pilot/stage_local.sh" --sealed "<SEALED>" --stamp <STAMP> --out "<D>\runs\<PID>\bundle"
```
`--out` should be the DURABLE local run folder (`<D>` = the NOTS Data mirror root): the tar and its sha256 stay there as the source archive of this pilot. The tar has ONE top-level entry, `runs/<PID>/`, containing:

| Staged | Destination (all under `HOME/runs/<PID>/`) |
|---|---|
| `code/core/v2_2_1/{core,study,tools,CHANGES_v2_2_1.md}` (the whole frozen v2.2.1 tree, no `.cpp_cache`) + `code/core/v2_2_1.SHA256SUMS` (its manifest), `code/lowp/{R,enum,pilot,tests/test_truth_lock_linux.sh}`, `code/bench_lowp` | `code/...` (pilot-owned copy: nothing shared is overwritten or deleted) |
| dev inputs and dev manifests (**no dev truth**) | `inputs/lowp_dev/{inputs,manifests}` = the `--study` root of all dev fits |
| study copy: `manifests/`, `dev/manifests/`, all 1,200 `truth/` and 60 `dev/truth/` files, 6 pilot inputs | `study/` (P0a, P0c, wave lock) |
| ownership marker and sha256 list | `OWNER`, `STAGED_SHA256.txt` |

Stage `bench_lowp` and `enum` only when their code is final: the stager copies what is in `code/` at that moment.

**Frozen v2.2.1 (one code tree for the core and the SMC step).** The stager copies the whole `code/core/v2_2_1/` tree (core, study, tools, CHANGES) and its manifest `code/core/v2_2_1.SHA256SUMS`, removes any `.cpp_cache`, and then runs `pilot_check_frozen` (`frozen_check.sh`): `sha256sum -c` against the manifest from inside the staged tree AND a check that no unlisted file is present (exit 4 otherwise). The LOWP fork `code/lowp/smc/` is retired and is not staged. The same check is repeated by `submit_pilot.sh` on NOTS (REFUSED, exit 2, if it fails), by `s0_build` before the compile and by every SMC task before its fit (exit 67), so the pilot provably ran the frozen v2.2.1; the only extra file tolerated is the compile cache `core/.cpp_cache` that `s0_build` creates. The manifest is also copied to `LOG/launch/v2_2_1.SHA256SUMS`. The enumerator keeps its own check that its vendored `v3_score.h` / `v3_util.h` equal the core's (unchanged in v2.2.1).

On NOTS (one connection): `cd HOME && test ! -e runs/<PID> && tar -xf <tar> -C . && sha256sum --quiet -c runs/<PID>/STAGED_SHA256.txt && rm <tar>`. The `test ! -e` makes the destination fresh by construction.

## 3. What OPS fills in: `HOME/runs/<PID>/code/lowp/pilot/pilot.env`

| Variable | Value |
|---|---|
| `MODULES=""` | **must equal CONF's v2.2.1 NOTS build** (the v2.2.1 core is byte-identical to v2.2) (same R and compiler); the scripts `module purge` first, so list the compiler (e.g. `GCC/13.2.0 R/4.4.1`, per NOTS_ENV not yet test-loaded) |
| `R_LIBS_LOWP=""` | library path providing Rcpp and digest as in CONF's build; empty if the modules provide them |
| `R_LIBS_USER_LOWP=""` | optional |
| `MODULES_BENCH=""` | R 4.5.2 + its compiler |
| preset | `R_LIBS_BENCH=/projects/ml75/fb31/BVS/bench20261019/lib/R452` (**read only, benchmark freeze**: only passed as `R_LIBS` and `--library`), `R_LIBS_USER_BENCH` non-existent, the D7 limits |

The final edited `pilot.env`, its sha256, the staged hash list, the lists, JOB.md, the exact `sbatch` argument vectors, the guard receipt and the effective environment are copied to `SCR/logs/<PID>/launch/` at submission, so the run is reproducible from the downloaded evidence.

## 4. Test hooks never reach a real run

`PILOT_DRYRUN, PILOT_SKIP_MODULES, PILOT_LIMIT, PILOT_BENCH_METHODS, PILOT_BENCH_EXTRA, PILOT_TIME_BIN` exist for local tests. `submit_pilot.sh` refuses them unless `--local-test` is given together with `PILOT_LOCAL_TEST=1` and a fake `NC_HOME_ROOT`; every job refuses them again (exit 70); the effective environment is recorded and `summarize_pilot.R` fails a pilot whose record shows one. Benchmark records are also checked after the fact: `test_library = FALSE`, `sealed_library` = the pinned path, every non-base package resolved from it (the benchmark CLI enforces the library location only for production ids, not dev ids).

## 5. Commands, gates and requests (through `ssh nots`, one connection)

```
cd HOME/runs/<PID>/code/lowp/pilot
STAMP=<STAMP> bash submit_pilot.sh --dry-run      # optional
STAMP=<STAMP> bash submit_pilot.sh
```
**Before staging** OPS runs `guard.sh 30` and keeps its line. **At submission** the driver runs `guard_check.sh`, which REFUSES (exit 1, nothing created) unless: no `GUARD_ALLOW_TEST`/`GUARD_TEST_*` in the environment; `guard.sh` itself defines **campaign limit <= 0.5 GiB (524288 KB) and home limit <= 9.6 GiB (10066329 KB)**; a planned add of 513 MB is refused for the campaign limit and an add past 9.6 GiB is refused for the home limit (behavioural probes); the real call with 30 MB exits 0 with status OK and no `TEST_LIMITS`. The receipt (guard sha256, parsed limits, every call and its exit status) is written to `launch/guard_receipt_submit.txt`; the driver sets `TMPDIR=SCR/runs/<PID>_tmp` before its first `mktemp`, so no transient file of the submission is created in the system `/tmp`. If the supplied guard still carries older limits, OPS fixes the guard first; no override is used.

The driver also REFUSES (exit 2, nothing created) when the staged `code/core/v2_2_1` tree does not match `v2_2_1.SHA256SUMS` (see section 2).

Submission is all-or-abort: every `sbatch` is checked, the returned id must be digits, ids are recorded as they come, and on **any failure the driver cancels the already-submitted ids by explicit id** (`scancel <id>`), writes `launch/SUBMISSION_ABORTED.txt` and exits 5. All jobs: `--account=commons --partition=commons --constraint=sapphirerapids`, output to scratch.

| # | Script | Array | CPUs | Mem | Time | Depends on |
|---|---|---|---|---|---|---|
| 1 | `s0_build` (compile core + enumerator, env report) | - | 2 | 4G | 0:40 | - |
| 2 | `s0_verify` (P0a) | - | 1 | 2G | 0:30 | - |
| 3 | `s0_truthlock` (P0c, gate; evidence in `truthlock/evidence/`) | - | 1 | 2G | 0:30 | `afterok` 2 |
| 4 | `s0_lock` (P0d wave lock + verification) | - | 1 | 1G | 0:10 | `afterok` 3 |
| 5 | `s1_enum20` | - | 4 | 4G | 1:00 | `afterok` 1,2,3,4 |
| 6 | `s1_enum30` | 0-5 | 16 | 4G | 1:00 | `afterok` 1,2,3,4 |
| 7 | `s1_scale` | - | 32 | 8G | 1:00 | `afterok` 1,2,3,4 |
| 8 | `s1_bitid` | - | 16 | 8G | 1:00 | `afterok` 1,2,3,4 |
| 9 | `s2_smc` | 0-27 | 1 | 2G | 4:00 | `afterok` 1,2,3,4 |
| 10 | `s3_bench` | 0-23 | 1 | 6G | 2:00 | `afterok` 1,2,3,4 |
| 11 | `s8_unlock` (P8 finalizer) | - | 1 | 1G | 0:15 | `afterany` 4 and 5-10 |
| 12 | `s9_collect` | - | 1 | 1G | 0:15 | `afterany` 1,2,3,11 |

`--kill-on-invalid-dep=yes` on dependents: a STOP at P0a or a failed lock/test cancels every fitting step, the finalizer still runs. **Between jobs 4 and 11 the two truth trees are mode 000.** A `du` of the campaign tree in that window fails closed, so **OPS must not run `guard.sh` on home during the wave** (about 30 to 45 min); wait for job 11. The finalizer refuses to unlock while any recorded fitting job is still active (it then fails and leaves the trees LOCKED, the safe state). **If the lock never ran** (an earlier gate stopped the chain, so the truth-lock test wrote no pre-lock lists), it reports `LOCK_NEVER_RAN` and verifies instead that the trees are open (755/444, 1,200 + 60) and that every truth file equals the staging list `STAGED_SHA256.txt` (exit 0 only if all 1,260 verify; revision 7d, B2). Exactly one pre-lock list present, a changed or missing file, or a missing staging list still FAILS.

Environment in every task: single-threaded BLAS (enumeration sets its OpenMP count), per-task `TMPDIR` on scratch removed on exit, `R_PROFILE_USER`/`R_ENVIRON_USER`/`R_HISTFILE` to `/dev/null`. Per unit GNU time `-f '%e %U %S %M'` (wall, user, sys, max RSS). **GNU time on NOTS (revision 7c, after OPS-4 probe job 2466301):** NOTS has no `/usr/bin/time`; GNU time 1.9 is the module `time/1.9` (GCCcore/13.3.0) at `/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time`. `slurm/common.sh` (`pilot_resolve_time`) tries `/usr/bin/time`, then that path (by absolute path, no `module load`, so the task's R/compiler modules are untouched), and accepts a binary only if `--version` says GNU time AND an `-f`/`-o` format probe writes the four numeric fields. The binary used, its version and sha256 are recorded per task in `LOG/env/time_bin_<arm>_<job>.txt`. **Fail closed:** the arms whose units enter the sizing (enum20, enum30, scale, smc, bench) exit 68 before any unit runs if no verified GNU time exists; infrastructure arms (build, locks, verify, bitid, unlock, collect) continue with wall-only timing, so the truth unlock can never be blocked. OPS pre-check (one connection): `/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time --version` prints `time (GNU Time) 1.9`. If GNU RSS is unusable the summarizer still uses the batch-step MaxRSS from accounting as a **job-level conservative bound** (and says so). No gate threshold changed.

**Requested core-hours (sum over all jobs and array tasks of CPUs x wall limit, from the table above).** Per step: 1: 2 x 0:40 = 1.33; 2: 1 x 0:30 = 0.50; 3: 0.50; 4: 1 x 0:10 = 0.17; 5: 4 x 1:00 = 4; 6: 6 tasks x 16 x 1:00 = 96; 7: 32 x 1:00 = 32; 8: 16 x 1:00 = 16; 9: 28 tasks x 1 x 4:00 = 112; 10: 24 tasks x 1 x 2:00 = 48; 11: 0.25; 12: 0.25. **Total requested = 311.0 core-hours** (12 steps, 67 jobs/array tasks). This is a ceiling that is charged only if every job ran to its limit.

**Expected core-hours (estimate, charged = allocated CPUs x elapsed): about 10 (plausible range 7 to 14), i.e. about 3 % of the request.** How it was estimated, all from local measurements (Windows, not NOTS; NOTS speed is unmeasured, hence the range): enumeration p = 30 about 890 to 1,090 CPU-s per dataset (`enum/VALIDATION.md`, `RUN_DESIGN.md` section 2) on 16 threads, taken as 85 to 100 s elapsed (ideal scaling 56 to 68 s, plus margin) + 30 s start-up, 6 tasks x 16 CPUs = 3.2; enumeration p = 20 about 1.3 s per dataset + about 10 s R start-up, 30 datasets sequentially on 4 CPUs = 0.4; scaling job on 32 CPUs held for the whole job: four 3 % subset runs (about 30 s at 1 thread, 8 s at 8) + full runs at 8, 16, 32 threads (about 110, 60, 35 s from 890 CPU-s) + start-ups, about 8 min = 4.3; bit-identity job (16 CPUs, 2 to 5 min: 2^20-model comparison, 20,000 random models, 2 % of the p = 30 tasks) = 1.0; SMC 14 fits at p = 20 (4.7 to 6.9 s) and 14 at p = 30 (18 to 24 s) (`tests/SMC_SMOKE.md`, no escalation) plus about 60 s per task for start-up and the frozen-tree check = 0.5; benchmarks 24 cases x about 56 s for all 8 methods (`RUN_DESIGN.md` section 2; A3 dominates) plus about 40 s start-up per task = 0.6; build (compile of core and enumerator on 2 CPUs, about 10 min) = 0.3; P0a regeneration (62 s locally) = 0.05; truth-lock test, wave lock, unlock, collection together under 0.1. The sum of the pieces is 10.4. The wait for the first usable result is set by the queue and the build, not by the cores.

## 6. Recovery (OPS) if the wave unlock did not run or failed

Symptoms: job 11 FAILED/CANCELLED/TIMEOUT, or `truthlock/WAVE_UNLOCK.txt` lacks `WAVE_UNLOCK_VERIFIED`, or `HOME/runs/<PID>/study/truth` is not mode 755.
1. `squeue -u fb31` through the alias; if any pilot job is still active, cancel it **by explicit id** from `HOME/runs/<PID>/JOBIDS.tsv` (never by name or user).
2. `bash HOME/runs/<PID>/code/lowp/pilot/recover_truth.sh <STAMP>`. It refuses while a pilot job is active or the scheduler cannot be queried (exit 3); otherwise it reopens both trees without R (directories 755 top-down, files 444) and verifies 1,200 + 60 files and all modes (exit 0 = RECOVERED). The staged trees are copies; the sealed originals are on the laptop.
3. Record the incident in the OPS log; the pilot is then rejected as incomplete (summary verdict "Wave unlock" INCOMPLETE/FAIL) unless HQ decides otherwise.
If the lock job itself failed midway, the same recovery applies (partially locked trees are handled).

## 7. Planned disk

| Location | Amount |
|---|---|
| NOTS home, guard planned add | **30 MB** (staged ~11.5 MB measured + compile cache 2 to 5 MB; limit for the whole campaign 512 MB) |
| NOTS scratch, until pulled | ~60 to 100 MB (results ~35, logs incl. evidence ~10, caches ~3); transient peak <= 300 MB |
| Laptop download | ~50 MB |

## 8. Expected outputs

`SCR/results/<PID>_{enum20,enum30,scale_t08,scale_t16,scale_t32,smc,bench}/p00xx/<unit>/` with `.rds .sha256 .done` (+ `.csv` for SMC and benchmarks): 30, 6, 1, 1, 1, 24 + 4, 24 x 8 units.
`SCR/logs/<PID>/`: `jobids.tsv`, `slurm-*`, `launch/` (receipt), `timing/*.tsv`, `units/*.log`, `env/`, `build/`, `p0_verify/`, `truthlock/` (`TRUTHLOCK_HEADER.txt`, `TRUTHLOCK_AFTER.txt`, `WAVE_LOCK.txt`, `WAVE_UNLOCK.txt`, **`evidence/`**: `run.log`, `final_status.txt`, pre/post sha lists, modes, lock/unlock logs), `bitid/`, `scaling/`, `accounting/` (`sacct_collector.tsv`, `sacct_final.tsv`, `guard_after.txt`, `disk_after.txt`).

## 9. After job 12: terminal accounting, download, summary

```
bash HOME/runs/<PID>/code/lowp/pilot/final_accounting.sh <STAMP>     # sacct for ALL jobs incl. the collector; exit 0 only if every row is terminal
```
(the collector cannot see its own terminal state; this snapshot is part of the evidence). Then pull and delete, one folder at a time with `ops/transfer/nots_pull.py <folder> --delete` (`MSYS_NO_PATHCONV=1`): `SCR/results/<PID>_{enum20,enum30,scale_t08,scale_t16,scale_t32,smc,bench}` and `SCR/logs/<PID>` (this includes `launch/`, `truthlock/evidence/` and `accounting/`). Keep the stage archive under `<D>\runs\<PID>\bundle`. On the laptop:

```
Rscript "<CAMP>/code/lowp/pilot/summarize_pilot.R" --results "<D>\results\<PID>_enum20,...,<D>\results\<PID>_bench" --logs "<D>\logs\<PID>" --out "<CAMP>\code\lowp\pilot\summary_<PID>"
```
Exit 0 = PASS or WARN (accepted); 2 = FAIL; 3 = INCOMPLETE. Only an accepted summary may size production.

**P5 scan (DECISIONS D11, informative).** `summarize_pilot.R` also runs `code/core/v2_2_1/tools/p5_scan.R --run-dir <D>\results\<PID>_smc --out <summary>\pilot_p5_scan.tsv` (default tool location `../../core/v2_2_1`; override `--v221-dir`, `--rscript`), keeps the TSV with the other small summaries, and reports `primary_resource_limit` and `eligible` in `PILOT_SUMMARY.md` (section "P5 scan") and as a verdict row (PASS if both are 0; WARN with the counts otherwise; WARN if the scan could not run). **P5 retries are not run automatically at the pilot**: the SMC allocation is 2 GB / 4 h inside a 4 h Slurm wall, so an in-task retry with doubled allocation is impossible. Any `eligible` unit (primary ended native `resource_limit` and no valid `P5_retry` record) is reported and is a finding for HQ, which decides. The row is not an acceptance gate and changes no threshold (a `resource_limit` unit is already invalid under the SMC native-status check of section 10)

## 10. Acceptance (all computed by `summarize_pilot.R`)

1. Exact unit sets, each VALID: 30 enum20, 6 enum30, 3 scaling, 24 SMC primary, 4 SMC repeat, 192 benchmark units. A unit needs: its files; sha256 sidecar and `.done` marker consistent with the RDS; for SMC and benchmarks the `.done` statuses equal the CSV statuses equal the RDS `rows$status`; a timing row with rc 0; and a record that passes its semantic checks (for SMC units this includes the v2.2.1 consistency check: when the CSV carries a `v3_status` column, which `tools/p5_scan.R` reads, it must equal the RDS native `fit$status` in every row; a disagreement makes the unit invalid, exit 2; a CSV without that column is not affected). **Enumeration records are validated with the shared strict I2 validator `code/lowp/enum/exact_contract.R::lowp_validate_exact(record, c("c100","c050"), input, "sealed")` (staged with the bundle; an empty HPM is legitimate)**: top-level `complete`/`models_expected`, sealed-input binding, retained-column coverage, full exact scope and status per scale, named PIPs, normalised size masses (`size_logjoint` = masses + log Z), 1,000-row top list, zero re-check mismatches; the pilot adds threads, positive re-check coverage and no fallbacks. SMC: regime/study/ids, seed = data seed + 4,000,000 (+1,000 x repeat), native status, runtime guard not exceeded, CSV runtime = RDS runtime. Benchmarks: rule statuses; per-fit runtime from `rows$runtime_s` (the writer has no top-level runtime), equal to the CSV; `test_library` FALSE; the saved environment must show the effective R **4.5.2**, `sealed_library` equal to the pinned path, every non-base package directly inside that exact directory (no sibling or prefix match), with version and a build under R 4.5.x, and the method's own package version equal to the CSV `package_version` (also for dev ids, where the runner does not enforce it). Invalid units never enter the sizing tables.
2. Launch receipt complete (hashes, 12 sbatch vectors, guard receipt `GUARD_CHECK_OK`, no test hook, MODULES filled).
3. P0a PASS; truth-lock test `FINAL_EXIT_STATUS 0`, 0 failed, trees 755/444 after; **wave lock verified; wave unlock verified with file hashes equal to before**.
4. Score/aggregate checks pass: bytes for F, eta, HPM F and top-list F; numerical tolerances for log Z, PIPs and certificate (the enumerator accumulates in a different order from the core, so aggregates are not claimed bit-identical); exact decisions; same-split thread invariance.
5. Thread invariance of the four `dev_p0030_S4_r001` outputs; repeat seeds exactly primary + 1,000.
6. Slurm: all 12 steps and 67 jobs/array tasks COMPLETED with exit 0:0 in the terminal snapshot; memory evidence for every arm and p. **Every required unit has a finite positive process wall time** (missing: the unit is absent evidence, INCOMPLETE, exit 3; zero or negative: invalid, exit 2; no fallback to the in-process time); **CPU policy**: enumeration units also need observed user+sys from GNU time (absence: INCOMPLETE, negative: invalid), single-thread SMC and benchmark units are costed as wall x 1 CPU so their CPU time is informational. **Memory evidence**: a source is usable only if finite and POSITIVE, in the order GNU time, the job's batch MaxRSS (job-level bound), the core's own VmHWM (SMC); a fallback is labelled with its reason (for example `sacct_job_bound (GNU RSS unusable)`); a unit with no usable source is absent evidence (INCOMPLETE), and no accepted memory request can be 0 or negative. Projections and the per-arm table carry `status = accepted` only when the whole pilot is accepted, otherwise `NOT ACCEPTED` and the summary says so. The saved `scaling/scaling_subset.csv` must hold the four rows (1 and 8 threads x 2 repetitions) for `dev_p0030_S4_r001` with full retained coverage (`models_total` = 2^30), the declared split (fraction 0.03, 1,024 tasks, 31 run, `models_scored` = tasks_run x models_total / n_tasks) and one common task subset (`tasks_sha256`: the same 64-hex digest in every row); every row is checked, malformed values (NA, text) are reported as FAIL rather than crashing, and nothing is extrapolated from rows that fail. SMC `fit$hpm` may be empty (the null model) but must be present, integer-valued, strictly increasing and within 1..p.
7. After clean-up: `CLEANUP VERIFIED`.
8. (Informative, not a gate) P5 scan of the SMC results reported: `primary_resource_limit` and `eligible` counts in the summary; a nonzero count is a finding for HQ (section 9).

## 11. Clean-up (nothing may remain; through `ssh nots`)

After section 9: `bash HOME/runs/<PID>/code/lowp/pilot/cleanup_pilot.sh <STAMP>` (dry run) then `--yes`. (Revision 7d, B3: a `--yes` run re-executes itself from memory after `cd /`, so running it from inside `runs/<PID>` no longer leaves an NFS `.nfs*` file that blocks its own verification.) It removes exactly `HOME/runs/<PID>` (the whole pilot-owned folder: code, dev inputs, study copy, ids), `SCR/runs/<PID>_cache` and `SCR/runs/<PID>_tmp`; it never touches `code/`, `inputs/`, `manifests/` or `code/ops`. It first checks: the ownership marker for this STAMP, the **canonical roots** (`readlink -f`, must resolve to New_Campaign folders): each target must equal exactly `canon(campaign home)/runs/<PID>` or `canon(scratch)/runs/<PID>_{cache,tmp}`, with neither `runs/` nor the target a link (a linked ancestor or intermediate directory is refused, exit 4, in the dry run too), results/logs no longer on scratch, and the scheduler: **if `squeue`/`sacct` fail it refuses (exit 4)**; any recorded pilot job active or any `lowp_p*` job queued refuses (exit 3). After removal it runs a residue search and the guard and reports **CLEANUP VERIFIED** (exit 0) or **CLEANUP UNVERIFIED: <reasons>** (exit 1: removal failed, residue search error, residue found, or the guard did not report OK).

## 12. Assumptions

- The pilot does not score (no truth reaches any fitting step); fit quality is not an acceptance criterion.
- The SMC step is the v2.2.1 one-CLI runner (`study/run_case.R`, flags unchanged from the retired LOWP runner: `--case --scale --study --outroot --run-id --core-dir --mem-gb --hours --development [--repeat m]`; output layout `SMCBVS[_rep{m}].*`). `--p5-retry` exists in that CLI but is never passed by the pilot.
- `final_accounting.sh`, `recover_truth.sh` and `cleanup_pilot.sh` run on NOTS through the alias; none of the bundle's scripts opens ssh.
- The enumerator README says memory depends on thread count and task split; the summary checks the 4G request against measured peaks.
