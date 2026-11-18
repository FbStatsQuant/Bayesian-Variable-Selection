# rerun2400 RUN_LOG (Sonnet builder, 2026-11-18)

Task: paired subset rerun of the p >> n 2,400-fit study; 121 datasets x scales = 242 fits (OLD v2.2.1 and NEW v3.1 on the same NOTS node). Plan: `../RERUN_2400_PLAN.md`
(manager decision at the top is binding). Scripts: `bundle_src/` (this folder); staged bundle: `/home/fb31/SMC_Engineering_Department/staging/rerun2400/bundle_20261118`.

## Log
- Read plan, NOTS_FACTS, PROD_H JOB runner (env.sh, task.sh, precompile), old adapter/run_case.R, `list_pip_ab/{ab_run.R,ws_common.R}` (from `origin/core/v3.1-listpip`; they are not in the working tree).
- Checks: git tree 8ff2d876... = `Scripts/SMC_BVS/core` of `origin/core/v3.1-listpip` (8bd779be); old v2_2_1 tree matches its manifest (27 files OK). Git state unchanged (only the pre-existing W3-DIST/LOG.md modification; only read-only git commands used).
- Design decisions (all inside the plan; no science or cost change):
  * Old side = unchanged study layer (`run_case.R`), fed by `gen_inputs.R` (frozen generator -> inputs .rds + a one-row inputs manifest, as gen_prod_data.R::main) because the original `inputs/` tree is not on Owls/NOTS-accessible here. The adapter verifies file and array hashes against that manifest as before.
  * New side = `new_fit.R` (ab_run route: generate_prod_dataset -> v3_fit(X, y, method_seed, allocation) with default ls0 = TRUE -> save). It regenerates the data in its own process, so X/y SHA-256 agreement across the two sides is a real check.
  * Allocation numbers identical on both sides: mem 2, hours via the same awk `%.10g` string (1.75 / 6.666666667). Per-fit hard kill L+300 s as in PROD_H.
  * Task = one dataset: 4 fits sequential; first side alternates with task parity (odd: old first). Task walls: p1000 14:00:00, p500 06:00:00 (typical p1000 task 2 x ~3,200 s x ... ~2 h; worst plausible < 8 h).
  * Peak RSS: `fit$peak_memory_kb` (VmHWM at the end of v3_fit, same code in both cores) + sacct step MaxRSS (each fit is its own srun step named `<side>_<case>`).
  * Runtime for the verdict: `record$runtime_s` = wall around v3_fit (old: adapter; new: new_fit.R), i.e. including the list-PIP fields that v3.1 adds after `finish()`.
  * In-task admission guard: a fit returning `resource_limit` in < 5 s makes the task stop and write `ALERT_admission_*` in the run folder.
