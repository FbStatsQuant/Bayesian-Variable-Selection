# JOB: CONF_NOTS_IDENTITY: code v2.2 reproduces two historical production units on NOTS

Owner: CONF. Route: HQ, then OPS. Review: `conformance/review/` (Sol re-check of this bundle).

**Purpose.** Close two gaps left by the local regression (`conformance/REGRESSION.md`):
1. identity on the production platform (Linux, GCC 14.3.0, R 4.5.2, Sapphire Rapids);
2. a real escalation, which no local fit produced.

**Claim tested (conditional identity).** With the same inputs, seed, allocation, code definitions and numerical environment, v2.2 is expected to reproduce every pre-existing output of these v2.1 production records, adding only the allowlisted v2.2 fields. Excluded are timing, memory, provenance and the run identity, which differ by design.

**Not covered:** `schedule_limit`, `numerical_failure`, a real escalation-preflight stop, and same-allocation stop outcomes near a limit. These stay disclosed as untested in REGRESSION.md.

## Bundle files (upload all to `/home/fb31/projects/BVS/New_Campaign/jobs/CONF_NOTS_IDENTITY/`)

| File | Role |
|---|---|
| `job.sh` | Slurm script, ready to submit |
| `precompile.R` | Job-side precompile: evaluates `core/v3.R` except its final compile line, then compiles with visible compiler output into `compile_<jobid>.log`. The frozen sources are untouched, and both units reuse this fresh cache |
| `env.sh` | Byte copy of the production `runner/env.sh`: GCC/14.3.0, R/4.5.2, one thread, C.UTF-8, module R library |
| `v2_2.SHA256SUMS` | Manifest of the frozen v2.2 tree, verified by `job.sh` before running |
| `compare_identity.R`, `cmp2.R` | Local acceptance (CONF runs these after download) |

## Inputs

- **Code.** `ROOT/02_Experiments/I_2026-10-28_New_Campaign/code/core/v2_2/` (the `core/` and `study/` subfolders). Upload it to `/home/fb31/projects/BVS/New_Campaign/code/v2_2/` without any `.cpp_cache`; it compiles on its first `source`, once.
  - Expected adapter source hashes, recorded in the new RDS: `source_sha256` 2e39575a…8d9c and `v3_source_sha256` c0aebe86…2517.
- **Study inputs.** `/projects/ml75/fb31/BVS/bench20261019`, read only. This respects the benchmark freeze, which allows reading.
- **Units.**

| Unit | Escalated | Production run time | Pinned historical RDS / CSV sha256 |
|---|---|---|---|
| `p0500_S3_r044_c100` | no | 272 s | 27b7c546… / 7389e553… |
| `p0500_S5_r059_c100` | yes, by E2 | 828 s | 83254f90… / 367ee74b… |

The full hashes are pinned in `compare_identity.R`. The historical records carry the v2.1 source hashes b28719e6… and 8d03d364…. These equal the hashes of `code/core/v2_1_baseline/` computed locally by the adapter's own function, which ties the historical records to the audited baseline.

## Command

Pre-check (OPS): the disk guard, and `sinfo -o "%N %f"` shows the `sapphirerapids` feature; if the feature has another name, edit the `--constraint` line.

```
mkdir -p /home/fb31/projects/BVS/New_Campaign/logs/conf_identity /scratch/fb31/New_Campaign/results/conf_identity
sbatch /home/fb31/projects/BVS/New_Campaign/jobs/CONF_NOTS_IDENTITY/job.sh
```

`job.sh`:
1. Sources `env.sh`.
2. Verifies the v2.2 tree against `v2_2.SHA256SUMS` and aborts on mismatch.
3. Records the CPU, GCC, R, Rcpp, threads and locale to `run_env_<jobid>.txt`.
4. Runs both units sequentially with the production CLI (`run_case.R --case … --scale c100 --study … --outroot … --run_id conf_identity --mem_gb 2 --hours 1.75`).
5. Checks each unit's `.done` file and `sha256` file, and exits non-zero on any failure (`set -euo pipefail`).

## Resources

| Item | Value |
|---|---|
| CPU, memory | 1 CPU, 2 GB (as production) |
| Wall | 03:40:00. This covers the worst case of two units at their full 6,300 s allocation (L500) plus compilation; the expected total is ≈ 20 min |
| Disk | < 10 MB scratch; < 1 MB home (code and logs) |

## Expected outputs and transfer

Outputs:
- `/scratch/fb31/New_Campaign/results/conf_identity/results/conf_identity/p0500/<unit>/SMCBVS.{rds,csv,sha256,done}`;
- the Slurm log `logs/conf_identity/<jobid>.out`;
- `run_env_<jobid>.txt`.

Transfer (audit trail first, then deletion):
1. After the job ends, save `sacct -j <jobid> --format=JobID,State,ExitCode,Elapsed,NodeList,MaxRSS -P` to `sacct_<jobid>.txt`.
2. Download to `<PC_NOTS_DATA>\New_Campaign\results\conf_identity\`:
   - the two unit folders;
   - the Slurm log `<jobid>.out`;
   - `run_env_<jobid>.txt`, `compile_<jobid>.log` and `sacct_<jobid>.txt`;
   - the submitted bundle files, whose hashes are recorded at the top of `run_env`.
3. Verify the unit sha256 files and the bundle hashes.
4. CONF runs the acceptance command below on the downloaded copy, and saves its stdout, stderr and exit status as `ACCEPTANCE_<jobid>.log` in this bundle folder.
5. Only then delete from scratch, and record the deletion in OPS_LOG.

## Acceptance (CONF, local)

```
Rscript compare_identity.R "<downloaded …/results/conf_identity/results/conf_identity>" "<downloaded run_env_<jobid>.txt>"
```
The first argument is the folder that directly contains `p0500/`; the second is the job's environment record. It exits **0 and prints ACCEPT only if every criterion holds**, and otherwise exits 1 listing the failed criteria. The criteria:
- all four files present for both units, and each `SMCBVS.sha256` lists exactly `SMCBVS.rds` and `SMCBVS.csv`, both verifying;
- historical files match the pinned sha256, and carry the v2.1 source hashes;
- new records carry the pinned v2.2 source hashes and adapter 2.2-R1;
- the new records' numerical environment *equals the historical one*: exact R version string, the loaded-module list, session lines (platform, OS, FlexiBLAS OPENBLAS and LAPACK, Rcpp 1.1.0), all five thread variables = 1, and RNGkind;
- same input sha256, seeds and allocation as the historical units;
- both runs `completed` on the SMC branch;
- S3 not escalated, with empty reasons;
- S5 escalated to tier 1, with `instrumentation$escalation$reasons == "E2"`, matching the tier-0 triggers in both records, and not blocked;
- the required new fields are present and sane: fit plain PIPs (500 retained names, [0,1], island mean, MPM); the record's original-index `pip_plain` and `mpm_plain`; all instrumentation subfields, version v2.2, HLL mode; record instrumentation = fit instrumentation;
- `cmp2.R`: 0 differing pre-existing paths and 0 non-allowlisted additions;
- CSV: same columns, and every non-provenance cell identical;
- populated instrumentation, checked against the fit: best before/after the local search, the after-calibration HLL report, stages per tier, `cut_group_large`, escalation;
- the job record shows:
  - a Sapphire Rapids CPU (`amx_tile`), gcc 14.3.0, R 4.5.2 and Rcpp 1.1.0;
  - exactly one header, one end and one `final_status 0`, and `failed_case none`;
  - one launch command and one `exit 0` line per unit;
  - a fresh compile (cache key and shared-object hash).

**Fresh-run rules (enforced by `job.sh`).** The job aborts, without deleting anything, if the uploaded tree has a `.cpp_cache` or if the output location already exists. An EXIT trap writes the failed case, the end time and the final status to `run_env_<jobid>.txt`, which also records the bundle file hashes and every launch command.

**Dry runs (local, `DRYRUN_negative_controls.log`).** The historical v2.1 outputs posing as new, with an emptied checksum manifest and a wrong environment record, fail 30 criteria and exit 1. A job record with a conflicting second `final_status` is also rejected.

**If the units stop at the allocation** (`resource_limit`) or exceed the wall, the gate is **INCOMPLETE**, not passed. Report to CONF; do not retry automatically.
