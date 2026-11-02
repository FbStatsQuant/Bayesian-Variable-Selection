# Builder B build notes

Local checks on 2026-10-30. No NOTS connection was made; the manager's independent `tests/` were not run.

## Syntax

Git Bash `bash -n` passed for every top-level shell file (batch_runner, cleanup_prodl, clear_stale, final_accounting, frozen_check, guard_check, make_manifests, make_p5_list, make_resubmit, recover_truth, retune_throttle, stage_local, submit_prodl, truth_lib, truth_wave and waiter). `py -3 -m py_compile ceiling_check.py` passed.

## Ceiling fixtures

| Capture | Profile | Result |
|---|---|---|
| empty | alone | ADMITTED: L 132, others 0, combined 132 |
| empty | withH | ADMITTED: L 68, others 0, combined 68 |
| two PROD-H pending arrays at %50 | withH | REFUSED, exit 2: L 68 + others 200 = 268 |
| two PROD-H pending arrays at %31 | withH | ADMITTED: L 68 + others 124 = 192 |
| PROD-H present | alone | REFUSED, exit 2: PROD-H present and combined 256 |

Receipts are in `<PC_TEMP_PATH>`. PowerShell's reported wrapper status for a nonzero native program was 1; explicit `$LASTEXITCODE` confirmed native exit 2.

## Driver dry runs

Both profiles passed and emitted ten sbatch vectors, retained verbatim in `<PC_TEMP_PATH>` and `dry_withH.txt`. They used a staged tree extracted from the real-study staging test under the temporary fake root; the source study remained read-only. The test used stubs for sbatch, squeue, sacct, stat and guard, and a Python shim to translate Git Bash process-substitution paths to Windows Python. No job was submitted.

| step | CPU | memory | time | array alone / withH | dependency (dry-run IDs) |
|---|---:|---|---|---|---|
| s0_build | 2 | 4G | 00:40:00 | — | — |
| s0_verify | 1 | 2G | 00:30:00 | — | — |
| s0_truthlock | 1 | 2G | 00:30:00 | — | afterok:1001 |
| s0_lock | 1 | 1G | 00:10:00 | — | afterok:1002 |
| s1_enum20 | 4 | 1G | 01:00:00 | — | afterok:1000:1001:1002:1003 |
| s1_enum30 | 16 | 1G | 00:45:00 | 0-23%4 / 0-23%2 | afterok:1000:1001:1002:1003 |
| s2_smc | 1 | 2G | 05:00:00 | 0-95%32 / 0-95%16 | afterok:1000:1001:1002:1003 |
| s3_smcrep | 1 | 2G | 05:00:00 | 0-479%32 / 0-479%16 | afterok:1000:1001:1002:1003,afterany:1006 |
| s8_unlock | 1 | 1G | 00:15:00 | — | afterany:1003:1004:1005:1006:1007 |
| s9_collect | 1 | 1G | 00:15:00 | — | afterany:1000:1001:1002:1008 |

## Real sealed-study staging

`stage_local.sh --sealed .../inputs/lowp_study --stamp 20261030T1202Z --out <PC_TEMP_PATH>` succeeded. Output: frozen v2.2.1 tree verified, 27 files; archive 70,120 KB, 2,608 files plus hash list; staged footprint 74,766 KB. SHA-256: `a1d5ca57fbe2dc79b5316b0161295c361b8959779d0b699d74ed713ecaf04845`. The archive is a test snapshot; cleanup_prodl.sh was subsequently edited to fix the memory re-exec with receipts, so restage for an actual deployment.

The first staging attempt exposed Git tar treating a Windows drive-letter archive path as remote; stage_local.sh now converts the arguments with cygpath and the retry succeeded.

## Deviations and limitations

- The design calls main enum20 a non-array job even though the general instruction says array jobs use the list range. The driver follows the explicit main-wave table; later enum20 resubmission waves use arrays.
- For `--p5-scan` without a profile, withH is used as the conservative default; section 6 shows that invocation without a profile while section 5 requires one.
- Dry-run verification used a copy of the sealed study instead of dummy contents, with a local shim for Windows Python. It did not exercise a real scheduler, scheduler failures, submission rollback, recovery, accounting, manifests or cleanup. These require the manager's independent suite and review before production use.
- The pilot's guard checker writes each receipt line both through tee and to stdout; using /dev/stdout for the driver's no-file dry run duplicates lines in its captured guard text.
- An attempted removal of the temporary failed first staging tree was rejected by the environment's automatic policy. It was left in place; the successful staging used a fresh temporary directory.
