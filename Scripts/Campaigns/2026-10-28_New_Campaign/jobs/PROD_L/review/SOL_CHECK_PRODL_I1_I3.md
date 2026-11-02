# Narrow Sol check: PROD_L I1–I3 (HQ D53)

Reviewer: Sol 6.1. Completed UTC: 2026-10-30T16:23:06Z. Scope is only class-(i) I1, I2 and I3 from `SOL_REVIEW_PRODL_R2.md`, against the binding `R2_FIX_PLAN.md`. Read `R2_RESPONSE.md`, `R2_FIX_NOTES.md`, the four requested code files, JOB.md §5 P5 step and §14, the three regression suites and TESTS.md, and the saved `SUMMARY_r3_final.txt` (14 suites, 1,438 passed, 0 failed). This is the requested narrow check, not a third full review.

Evidence root (`W`): `<PC_TEMP_PATH>`. A byte-identical current-bundle snapshot, before/snapshot hash inventories, copied tests, reproduction diffs, commands/PIDs/timestamps, logs/exit files and generated fixture outputs are retained there. `audit.json` verifies that the campaign bundle was unchanged before this report and that the eight reviewed files match the snapshot. All execution was local, synthetic control-flow testing explicitly requested here: no SSH, NOTS, network, real R, fit, enumeration, simulation or benchmark. Scheduler and R calls used fixture stubs. This does not establish remote execution or Linux filesystem behavior.

## I1 — RESOLVED

`make_p5_list.sh:56,95,106` consumes successful phases, appends only newly eligible units without changing the existing rows, and writes scan hashes and before/after row counts to history. `reconcile_prodl.py:38,265` selects the newest successful recorded scan by job ID and emits `p5_unlisted_eligible`. `make_manifests.sh:60–96` requires a successful final scan newer than every s1_–s4_ fitting job, exact done-unit coverage, listed resource-limit units, verified retries and safe retry states, including zero-expected runs.

Both copied R2 late-primary reproductions now give reconcile **1** and ordinary SMC closure **6**, with no CLOSED marker. The populated-initial-tables reproduction independently confirms this without relying on an empty scan-table format. In the clean P5 suite, L101–107 confirm empty initial inventory → late resource_limit primary → final-eligible refusal; L110–113 repeat it with a nonempty initial list and an already-completed retry. L120–127 confirm extension 1→2, preservation/order of the old row, recorded hashes/history, a second consumption adding nothing, and selection of only the new never-started unit. L128–130 then give reconcile **0** and closure **0** after its retry and final2 job 7030, newer than every fitting job. L140–157 and P505–511 confirm refusal without a final receipt, with old primary/P5/enum job ordering, missing/extra scan coverage, unsafe states, or an invalid/missing retry; the zero-eligible complete-newer-final control closes. JOB.md §5 step 6 states the required rescan/extension sequence after later fitting waves.

Evidence: `W/repro_r2.log`, `W/repro_r2_late_complete_scan.log`, their saved inventories/exceptions, `W/test_p5_clean.log` (L101–172), and `W/test_manifests.log` (P501–511).

## I2 — RESOLVED

`make_manifests.sh:98–106,136` gates on the selected piece's exception rows and saves their hash/count in CLOSED. `reconcile_prodl.py:153–162,276–297` verifies and restores those rows as acknowledged and distinguishes exits 0/1/2/4.

The adapted copied `repro_r2.sh` gives baseline reconcile **0**, unexpected-output reconcile **1**, ordinary enum20 closure **6**, acknowledged closure **0**, post-pull reconcile **4**, and all-pieces-closed/pulled reconcile **4**. The same `UNEXPECTED_UNIT`/`unexpected_output` identity remains in both later `exceptions.tsv` files with `acknowledged=yes`; both inventories say `COMPLETE WITH 1 HQ-ACKNOWLEDGED EXCEPTIONS`. It never becomes a clean exit 0. X08–17 independently cover refusal, hash-bound acknowledgment, pull preservation and tampering/emptying the saved exception file (exit **2**). X20–23 retain the clean close/pull exit-0 control; X30–32 confirm that an unrelated unfinished or exceptional piece does not block a clean selected piece.

Evidence: `W/r2_repros/`, `W/test_manifests.log` (X01–32), and `W/test_reconcile.log` (EX01–06 and strict/malformed-record controls).

## I3 — RESOLVED

`reconcile_prodl.py:146–152` reconstructs one native-status count per done CLOSED unit from the hash-verified inventory detail and aggregates those counts with live pieces.

The copied zero-P5 reproduction retains smc completed=1 and smcrep completed=1 before and after all four actual closures/pulls. The copied nonempty-P5 reproduction retains smc resource_limit=1 and smcrep resource_limit=1 across live → smc closed/pulled → both SMC pieces closed/pulled, with both saved P5 units still done. N301–309 independently exercise nonempty P5, committed scientific failures (`status=failed`, native resource_limit), multiple native categories and one-count-per-unit behavior: **smc complete=1, smc resource_limit=2, smcrep complete=3**, invariant across live, one SMC piece pulled, both SMC pieces pulled, and all four pieces pulled. Operational unit coverage also remains unchanged.

Evidence: the reproductions' `INVENTORY.md` files, `W/suite/test_manifests/rec_n0` through `rec_n3`, and `W/inspection.json` (direct equality checks of the saved native tables).

**I1–I3 RESOLVED: PROD_L may be declared READY for OPS**

## Independent reruns and adaptations

The three suites ran one at a time against the current snapshot, with Bash `C:/Program Files/Git/bin/bash.exe`; Python reconcile tests used `py -3 -I`. Copied suite/helper sources differ only by the literal `prodl_tests` → `prodl_sol`; `vec_check.py` is byte-identical. No operational source was edited.

| Suite | Passed | Failed | Exit |
|---|---:|---:|---:|
| test_p5.sh (clean rerun) | 152 | 0 | 0 |
| test_manifests.sh | 124 | 0 | 0 |
| test_reconcile.py | 34 | 0 | 0 |
| Total independently rerun | 310 | 0 | |

The first P5 attempt is preserved separately as `test_p5.log`/`.rc` and `suite/test_p5`: 141 passed, one harness failure because I omitted the copied `vec_check.py`. I restored that unchanged dependency and reran the whole suite into `test_p5_clean.log` and `suite/test_p5_clean`, without edits during the clean run. This was not a bundle defect. The supplied 14-suite summary was inspected; only the three requested suites were independently rerun.

Copies of all three historical scripts were rerun; originals and historical evidence were untouched. Exact diffs are `W/repro_r2*.sh.diff`. Adaptations were limited to:

- Redirecting the evidence root/helper paths and using `PRODL_B_SRC` for the current snapshot.
- In `repro_r2.sh`, adding a successful final baseline scan (job 7004 > fitting job 7002), then explicitly closing enum20 with `--allow-incomplete` only after recording the ordinary closure refusal, so its subsequent pull is valid. Post-pull exit **4** is the required new contract.
- In `repro_r2_closed_p5.sh`, adding the now-required header-only, hash-bound exceptions snapshot to its pre-existing synthetic empty-enum CLOSED fixtures. Its actual SMC closures, P5 inventory, pulls and manifest checks are unchanged. This small fixture does not claim actual enum closure; the four-piece reproduction and manifest suite cover that.

The two late-primary scripts end with exit **1** because their original final `cat` attempts to read the CLOSED marker that is now correctly absent; their inspected reconcile/closure exits are **1/6**. The nonempty-P5 script ends **0**: real SMC closures and post-pull reconciliations, final accounting, logs closure, downloaded-manifest verification and cleanup all return 0. Raw exit files and inspection assertions are retained. No new class-(i) defect introduced by the I1–I3 fixes was found.

noted, out of scope: TESTS.md's trailing “Not encoded” paragraph and the manifest suite's P503 label retain obsolete wording; the executed fixture does include the required final scan.

## SHA-256 (current bundle; matches tested snapshot)

```text
615b054bf3b324625541706a47b28adc3959355a6fbe4af8c88375ac30e56bd2  make_p5_list.sh
4539bd21edc6a20754cc673fc815a92b0053f47390caebab603f89d1a5a182eb  make_manifests.sh
ed7b8ea5f3a65d62c81be02b6f5635ec7fc5ef2d0fb2829f5519af63c3b8d850  reconcile_prodl.py
73079e42dc8d914b3c112822512b1aa368b240f6df1f0b7816c04f2a4ef5ce55  prodl_verify.py
aba9ed2234fd835c469a072f3427f907204c4f36409894be57e89c1a119fa5ba  JOB.md
e8f90690e7ef1461345517d2bf9bfb394ec25eb28260c991a58ffb76dece7c8b  tests/test_p5.sh
07c613092a6e8c6e14a99c1f028fd73ce55996dbfee27361fed256b43bf4e270  tests/test_manifests.sh
90b07ccf8ab1aa3081c481097f3c92f42dbe5c54176072b3d9cfec62386596f5  tests/test_reconcile.py
```
