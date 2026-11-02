# R1 implementation and check notes

No NOTS connection or R computation was used. Smoke fixtures and scheduler stubs are under `<PC_TEMP_PATH>`. The detached existing suite is under `<PC_TEMP_PATH>`; process ID 15328. Its tests were being edited concurrently and its scripts copy the bundle at different times, so it is not an immutable snapshot of this final revision.

All touched shell files were individually checked with Git Bash `bash -n` (exit 0); both Python files passed `py -3 -m py_compile`. Targeted fixtures do not establish NOTS behaviour.

## F1
`slurm/s8_unlock.sbatch:21` and `recover_truth.sh:17` query the full queue, reject active IDs and require complete terminal accounting. Stub smoke: mixed scheduler error, earlier active fit, and missing accounting each refused (exit 1); see `work/f1*.out`. The suite's S8-01 and S8-11 all-terminal unlock controls passed; its unlock suite had four failures from older recovery exit-code/queue fixtures.

## F2
Phase submission and scanner output: `submit_prodl.sh:8`, `slurm/s5_p5scan.sbatch:14`; expected inventory and wave lists: `make_p5_list.sh:2`; reconciliation and closure: `reconcile_prodl.py:91`, `make_manifests.sh:58`. Smoke: absent expected inventory produced reconcile exit 1; `p5_smoke.sh` created an initial inventory and one never-started unit, then listed the attempted unit as an exception without a new unit list. The interrupted-attempt, phase reuse, final scan and zero-eligible end-to-end cases still require regression validation.

## F3
`submit_prodl.sh:88` adds no-requeue; `slurm/common.sh:67` and `batch_runner.sh:4` reject restart; `batch_runner.sh` uses noclobber start. Stub restart smoke exited 71 (`work/f3.out`). A same-ID second run exited 1, reported start_record_exists, and preserved start/end SHA-256 hashes. The driver's D17 vector checks report no-requeue present.

## F4
`slurm/s9_collect.sbatch:21` writes accounting and gates guard on receipt and modes. Stub without receipt exited 1 and wrote GUARD_SKIPPED; verified receipt with open trees ran the stub guard and exited 0 (`work/f4_verified.out`).

## F5
`stale_lib.sh:3`, used by `clear_stale.sh:20`, `make_resubmit.sh:35`, and `make_manifests.sh:44`. Stub smoke found five fixtures: .lock directory and four real temp naming patterns. Moving and terminal-gate controls remain to be checked.

## F6
`prodl_verify.py:16` shares exact validation with reconciliation and resubmission. `verify_smoke.py` accepted a committed scientific failure and rejected one-line and duplicate sidecars, malformed marker and one-row CSV; missing output was rejected in `work/f6.out`. A synthetic unexpected result directory made reconciliation exit 1.

## F7
`make_manifests.sh:118` records inventory hashes; `reconcile_prodl.py:97` verifies and reads closed inventories, including P5 snapshots. A one-unit synthetic closed inventory with scratch absent reconciled exit 0; a tampered hash exited 2. The full close/pull/reconcile integration remains untested.

## F8
`JOB.md:35` documents waiter, one-submit-per-round, absolute transfer paths and home folder commands; `final_accounting.sh` copies JOBIDS into manifests. Manual read against `nots_pull.py`; no network action. End-to-end command sequence not tested. The plan's instructions conflict for a permanently failed job: F10 requires exit 3 whenever a failed row is present, while F8 requires a later waiter exit 0 for those same IDs. The current waiter will continue to exit 3; HQ must resolve that policy before operating.

## F9
`retune_throttle.sh:6` adds plan admission, confirmation and drain check; `JOB.md:39` documents drain. Stub admission with live enum30 and SMC plus 70 other billed CPUs refused (exit 2); drain checks at 70/68 billed CPUs returned 1/0; applying a lower throttle and confirming the stub's updated pending array returned 0.

## F10
`waiter.sh:9` requests delimited accounting and `waiter.sh:19` requires all IDs. `waiter_smoke.sh` returned 2 for partial accounting, 0 for complete terminal accounting, and 3 for a failure row. Existing old-format waiter fixture failed.

## F11
`make_manifests.sh:50` writes diagnostics under scratch. Syntax and static path inspection only.

## F12
`CORE_HOURS.md:19` and `JOB.md:69` distinguish 16 nominal, 16.2 wrapper and 18 requested. Checked wording against constants.

## F13
`batch_runner.sh:12` derives scheduler end, defers without it in production and records source; `DESIGN.md:61` documents it. Production-mode stub exited 1 with `reason=no_scheduler_end_time` and `end_source=missing`. The initial suite ran before correction of the empty scheduler response parse, so its deadline failures cannot validate the final code.

## Suite status
The one detached run finished: lists 20/0, ceiling 26/0, waiter 22/47, deadline 75/200, resubmit 79/17, manifests 53/38, cleanup 43/0, unlock 56/4, reconcile 3/24, driver 324/0 (passed/failed): **701 passed, 330 failed**. See `SUMMARY.txt` and per-suite logs at the path above.

Failures include intentional changes to waiter format and strict validation, but the initial run also exposed the now-corrected F13 empty-response bug and P510's missing P5 exception detail in CLOSED (added after that test captured its bundle). The Windows `sha256sum` in the VE12/VE13 fixtures emitted binary-marker lines (`hash *name`), whereas the binding adapter contract requires two spaces. The reconcile test's copied bundle omitted the new `prodl_verify.py`, causing ModuleNotFoundError. Concurrent test edits produced at least one `?: command not found` in `test_resubmit.log`; do not assume all failures are expected or use this run as acceptance evidence.
