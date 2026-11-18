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
- Comparator `bundle_src/comparator.R` + `test_comparator.R`: self-test on 24 fabricated pairs with 3 planted differences (log_Z last-bit on a completed fit; completed->stopped; one cell x1.6 runtime) plus 2 benign controls (ls0 HPM gain, stopped->completed; both disclosed not failed), a data-sha mismatch, a missing record and a clean run: ALL 14 CHECKS PASSED.
- Bundle built by `bundle_src/build.sh` -> `/home/fb31/SMC_Engineering_Department/staging/rerun2400/bundle_20261118` (69 files; SHA256SUMS sha256 `db2f9fbf60ea501685bf78fc09d4ffa53a453c1ea91726e57649ef948768af77`). NEW tree = git tree 8ff2d876 (20 files verified blob by blob against the tree; `git archive`, read-only git use). Local dry run of `runner/submit.sh --dry-run` ok.
- **Smoke on Owls** (00:15-00:36 CST, `nice -n 19`, 1 core, TMPDIR in `tmp/20261118-rerun2400/smoke`; the EXACT `runner/task.sh` with LOCAL=1 on a copy of the bundle; p0500_S1_r001 c100, order old then new; host load ~14):
  * both completed: OLD wall 605 s (record runtime 599.9 s), NEW wall 586 s (record 582.9 s; ratio 0.972); peak RSS 211 MB vs 219 MB (1.036).
  * X and y SHA-256 match (x 8e15f8a9..., y 4d193b07...). **log_Z, log_Z_r, hpm, hpm_F, pip_primary, pip_r, status all `identical()`** (non-vacuous: log_Z -69.59122, hpm 14 indices, pip_primary 500, pip_r 500x4). ls0_improved FALSE. Fresh scores 113,092,338 (old) vs 113,126,981 (new): +34,643 = the LS0 scores (0.03%), as the plan expected.
  * comparator on this pair: NO REGRESSION (`smoke/verdict.md`, `smoke/per_fit.csv`).
- **NOTS (via `ssh nots`, the multiplexed master; 3 calls)**: (1) master check, dest free, home quota 8,075M/10,240M (HQ guard 8,192M), no own jobs queued; rsync of the staged bundle to `~/SMC_Engineering_Department/scripts/rerun2400/` (no `.cpp_cache`). (2) `sha256sum -c SHA256SUMS` OK (SHA256SUMS sha256 `db2f9fbf...af77`), `env.sh` on the login node gives R 4.5.2 / GCC 14.3.0, `submit.sh --dry-run` ok, then `submit.sh` (2026-11-18 ~00:37 CST = 06:37Z).
  * RUN_ID `rr2400_20261118T0636Z`; outputs `/scratch/fb31/SMC_Engineering_Department/runs/rerun2400/rr2400_20261118T0636Z/{old,new,meta,slurm}`; run dir `~/SMC_Engineering_Department/scripts/rerun2400/run/`.
  * Jobs: precompile **2773942** (1 CPU, 4G, 1 h); p1000 array **2773943** `1-30%20` (14 h tasks); p500 array **2773944** `1-31%20` (6 h tasks); both afterok:2773942, kill-on-invalid-dep. commons, sapphirerapids, nots_commons, 1 CPU, 2G, --no-requeue, --export=NONE. At most 40 tasks at once (20+20).
