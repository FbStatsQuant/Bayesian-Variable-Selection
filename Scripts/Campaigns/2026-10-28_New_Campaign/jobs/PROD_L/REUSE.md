# Reuse inventory (PROD-L from the accepted pilot rev 7d)

Paths are relative to CAMP. Source SHA-256 computed 2026-10-30. "Unchanged" = byte-identical after CRLF→LF normalisation (checked with `diff`). New files without a reused source are listed at the end.

| Source path | Source SHA-256 | PROD-L file | Diff summary |
|---|---|---|---|
| `code/lowp/pilot/pilot.env` | `981c418abc8550c493d7a7aaa66874125690e9a5e3de11ba8ea10662d7a3a743` | `prodl.env` | Same structure; MODULES prefilled with the pilot's accepted values (OPS confirms); D47 ceilings; deadline constants; per-piece table (wall, budget, CPUs, memory, threads, throttles); RID `<STAMP>_lowp_prodL`, per-piece run ids; `PILOT_DIR` = staged `code/prod_l` |
| `code/lowp/pilot/slurm/common.sh` | `a2c2316a755c4b60409e7f0caef5d9fc0f1250365bc8343141b56c8eb2207a06` | `slurm/common.sh` | Adds PROD-L hooks, restart guard before initialization, GNU time for `smcrep` and `p5`, and job-tagged unit logs. |
| `code/lowp/pilot/R/pilot_build.R` | (pilot file) | `R/pilot_build.R` | Unchanged |
| `code/lowp/pilot/slurm/s0_build.sbatch` | `0d61274a4c5c2371d1859bd5c7034671dc6c2fd371cc361b1b1f993a396cf659` | `slurm/s0_build.sbatch` | Same steps; sources prodl.env from the PROD-L run folder; `WAVE` required; `PRODL_T0` recorded |
| `code/lowp/pilot/slurm/s0_verify.sbatch` | `0c8a384362daa517ff9ad6fc38ace2aafcb599a4fdf4aa3f5f2618dde3d0db00` | `slurm/s0_verify.sbatch` | P0a `lowp_verify_nots.R` unchanged (rev 7d tolerance gate); adds P0b `R/prodl_inputs_check.R` (exact sha256 of all 1,200 staged inputs vs the manifest); job fails if either fails |
| `code/lowp/pilot/slurm/s0_truthlock.sbatch` | `7597ff084089ad8bbdaa23ba1c0e66574b97d6868add6cbcb5823caf769d2227` | `slurm/s0_truthlock.sbatch` | Evidence per wave: `LOG_RUN/truthlock/<wave>/evidence` |
| `code/lowp/pilot/slurm/s0_lock.sbatch` | `80d02fcf29553f42e7e2c6f4e70c3d38dbdb8186ba91f2297e155cbadff4aa55` | `slurm/s0_lock.sbatch` | Lock record per wave |
| `code/lowp/pilot/slurm/s1_enum20.sbatch` | `eafddcff5d91857b6af5043bd0eb70f55073d0c4cf7c79517bab8a8d962c1d6c` | `slurm/s1_enum20.sbatch` | Production ids (no `--development`); 1 GiB; units through `batch_runner.sh` (deadline rule, ledger) |
| `code/lowp/pilot/slurm/s1_enum30.sbatch` | `32c421f5238c79c69769dc7237dd586cb3b57004af973186c86c25abb01ad5d1` | `slurm/s1_enum30.sbatch` | 25 datasets per task via `batch_runner.sh`; 1 GiB / 45 min |
| `code/lowp/pilot/slurm/s2_smc.sbatch` | `2db4e09376fd3df32d71958e36224d46d3f3db99f5f73a4e7ddd3345ca42a70f` | `slurm/s2_smc.sbatch` | 25 fits per task via `batch_runner.sh`; task wall 5 h; core allocation `--mem-gb 2 --hours 4` unchanged; frozen check per task kept |
| same | same | `slurm/s3_smcrep.sbatch` | As s2 with `--repeat m` (arm `smcrep`) |
| same | same | `slurm/s4_p5.sbatch` | One unit per task, `--p5-retry`, primary allocation passed (adapter doubles), 4 GiB / 9 h, noclobber attempt record |
| `code/lowp/pilot/slurm/s8_unlock.sbatch` | `adb19dd8212fc94e9da1d9705cf54b61c5d6a370a937b71e205b702e0643bf44` | `slurm/s8_unlock.sbatch` | Checks fitting jobs of ALL waves (`s1_`–`s4_`); fail-closed queue inspection and complete terminal accounting; wave evidence and B2 never-locked path. |
| `code/lowp/pilot/slurm/s9_collect.sbatch` | `a0943672da2b9cc97b6e8281e66027fd45c4b34e2b505b7fe9ed561e77f5e4c5` | `slurm/s9_collect.sbatch` | Accounting snapshot per wave; guard after unlock; disk-footprint table dropped |
| `code/lowp/pilot/frozen_check.sh` | `ae1aacc23c1ff7c9cea7b9c0016872e805f415c1a839163abe2a9665c9ebbf72` | `frozen_check.sh` | Unchanged |
| `code/lowp/pilot/guard_check.sh` | `3625033365a168dd4e255f4a74453a46378aaf5bfcdcb160ef614923d9232384` | `guard_check.sh` | Unchanged |
| `code/lowp/pilot/truth_lib.sh` | `a4b4ddcd5b8b680cda3c8b30738949cab46a6baaba267e3dccb9acdd6c2436ae` | `truth_lib.sh` | Unchanged |
| `code/lowp/pilot/truth_wave.sh` | `0fd6b1c80dcefca4b6ab37f1a9b4242cb4ebe46d2102ab3945a42a692ea24e5d` | `truth_wave.sh` | Unchanged (B2 path included) |
| `code/lowp/pilot/recover_truth.sh` | `add6cd10ff0c12611340b4e5e4a90d6545dff2a7d0aa57e474d3f702c280e75e` | `recover_truth.sh` | Run folder `_lowp_prodL`; job-id column 3 (wave column added); name pattern `^lowpL_` |
| `code/lowp/pilot/submit_pilot.sh` | `dd64f303f0f392c78ebe9f2f8b14422f862278b685c6e7f1eb6afd6ce7bddb09` | `submit_prodl.sh` | Rewritten around waves and profiles; adds truth-open and run-idle checks, ceiling check, CLOSED-piece refusal, and `--no-requeue` submission. Retains hook refusal, guard, staged/frozen checks, launch record and all-or-abort cancellation. |
| `code/lowp/pilot/final_accounting.sh` | `58ac5727f3e3960e3d980f8cb76fae5dcd70857793950ce746ad31b0b4c7783e` | `final_accounting.sh` | All waves; adds `ElapsedRaw` and `accounting/core_hours.tsv` (billed core-h per step and total) |
| `code/lowp/pilot/cleanup_pilot.sh` | `5871c669e4a1b178d2276544695df8fd606f04afdf2aef7394b9d61e6c69554f` | `cleanup_prodl.sh` | Names adapted (`_lowp_prodL`, `^lowpL_`, OWNER `lowp_prodL`); refuses while any `results/<STAMP>_lowp_*` or the logs remain; residue search `<STAMP>_lowp_*`; `--receipt FILE` outside the removed tree (operational-closure receipt); B3 re-exec from memory kept |
| `code/lowp/pilot/stage_local.sh` | `7ae2eb2d2d9c6c2f715ac8c7463320edf59b0111357ade1967a2e65c0b24ebfe` | `stage_local.sh` | Stages the whole sealed study and the bundle as `code/prod_l` (no tests/review/fixtures/notes); no bench_lowp; same frozen, truth-separation and hash-list checks; tar `prodL_bundle_<STAMP>.tar` |
| `code/lowp/pilot/JOB.md` | `7ff0d3885bea3634d2b3fb77ad9c927bae269474113695166658cda3f3b07dd8` | `JOB.md` | Rewritten for production waves, per-piece closing and evidence |
| `ops/scaffold/pilot_monitor.sh` (v2) | `fa4413e3ea7823e421c2c837c05a3c92edf84e259c86486cf80806f9432aa82c` | `waiter.sh` | Prefix `lowpL_`; wakes on any non-COMPLETED terminal state incl. CANCELLED variants; empty squeue with PENDING sacct rows is not terminal |

New files (no reused source): `batch_runner.sh` (deadline rule, ledger, inventory), `ceiling_check.py`, `retune_throttle.sh`, `make_resubmit.sh`, `clear_stale.sh`, `make_p5_list.sh`, `make_manifests.sh` (per-piece CLOSED), `reconcile_prodl.py`, `R/prodl_inputs_check.R` (P0b), `tools/make_lists.py` + `lists/units.tsv`, `bench_hook/README.md`, `DESIGN.md`, `CORE_HOURS.md`.
