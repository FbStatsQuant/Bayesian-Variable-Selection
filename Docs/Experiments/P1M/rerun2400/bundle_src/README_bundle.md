# rerun2400 bundle -- paired subset rerun of the p >> n 2,400-fit study (PROD-H), OLD v2.2.1 vs NEW v3.1

**What.** 121 datasets (Tier A: p in {500,1000} x S1-S6 x r in {1,25,50,75,100} x c in {c100,c050} = 120 fits, plus `p0500_S5_r088_c100`), each fit
run on BOTH cores = 242 fits, in ONE Slurm array task per dataset (same node, same minute): OLD c100, NEW c100, OLD c050, NEW c050, with the
first side alternating by task parity (odd task: old first, even task: new first). p1000: 30 tasks, p500: 31 tasks.

| side | code | harness |
|---|---|---|
| OLD | `old/` = SMC-BVS v2.2.1 tree unchanged (hash-checked by `old.SHA256SUMS` = the repo's `v2_2_1.SHA256SUMS`) | its own study layer `old/study/run_case.R`; X/y from `runner/gen_inputs.R` (frozen generator, writes the input .rds and a one-row manifest like gen_prod_data.R) |
| NEW | `new/core/` = git tree 8ff2d876c6a5667edfeeebd00305f02388b736fd (`Scripts/SMC_BVS/core` of `origin/core/v3.1-listpip` 8bd779be), by `git archive`, verified blob by blob (`NEW_PROVENANCE.txt`) | `runner/new_fit.R` = the `tests/list_pip_ab/ab_run.R` route: `generate_prod_dataset` -> `v3_fit` -> save; no adapter |

Seeds as the original: data seed = 1,410,000 (p500) / 1,510,000 (p1000) + 10,000 s + r; method seed = data seed + 4,000,000 (generator; `tables/units.tsv`
is checked against the formula by `tables/` build). Allocation as the original: `--mem-gb 2`, hours 1.75 (p500) / 6.666666667 (p1000), 1 CPU, 2G, commons,
sapphirerapids, `nots_commons`, `--no-requeue`. Both sides get the identical allocation numbers. X/y SHA-256 are recorded on both sides (old: record$input,
new: record$x_sha256) and compared.

**Layout.** `old/ new/ gen/ runner/ tables/ analysis/ smoke/ SHA256SUMS NEW_PROVENANCE.txt`. On NOTS the bundle lives in
`~/SMC_Engineering_Department/scripts/rerun2400/` (copy without any `.cpp_cache`), the run directory `run/` is created by `runner/submit.sh`, outputs in
`/scratch/fb31/SMC_Engineering_Department/runs/rerun2400/<RUN_ID>/{old,new,meta,slurm}`.

**Run (NOTS, after `sha256sum -c SHA256SUMS`).** `bash runner/submit.sh --dry-run`, then `bash runner/submit.sh`: precompile job (both trees, 1 h limit) -> p1000
array `1-30%20` (14 h tasks) and p500 array `1-31%20` (6 h tasks), both `afterok` on the precompile: at most 40 tasks at once. A task NEVER compiles. If a fit
returns `resource_limit` in < 5 s (admission refusal) the task stops and writes `ALERT_admission_*` in the run folder.

**Collect + compare (Owls).** `bash analysis/collect.sh <RUN_ID>` (one ssh for the accounting, one rsync, then `analysis/comparator.R --expect-grid`).
`Rscript --vanilla analysis/test_comparator.R` is the self-test (3 planted differences).

**Pass rule (RERUN_2400_PLAN section 6):** legacy fields (`log_Z log_Z_r hpm hpm_F pip_primary pip_r status`) `identical()` on completed fits (an `ls0_improved` HPM gain
is disclosed, not failed); 0 completed -> stopped; runtime ratio of medians <= 1.25 per cell (p x c x S) and <= 1.10 pooled per p; peak RSS ratio <= 1.2.
