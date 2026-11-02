# R2 fix notes

Local synthetic control-flow checks only; no R, scientific computation, or NOTS connection. Evidence root: `<PC_TEMP_PATH>`. The copied reproductions use a copied helper redirected to the current bundle and the new evidence root. Their original scripts deliberately continue after refusal and may end nonzero when attempting to read a CLOSED marker that must now be absent.

## I1

`make_p5_list.sh:56` and `:80` consume successful phases and append new rows, with hashes/history at `:104`. `make_manifests.sh:60` requires a newer final scan, coverage, listed resource limits and safe completed retries; `reconcile_prodl.py:265` checks the newest recorded successful phase. `JOB.md:43` describes rescanning after later fits. `repro_r2_late_complete_scan.sh.out`: late resource-limit primary gives reconcile 1 and closure 6. `extra_smoke.sh.out`: extension 0, history 0→1 then 1→1, retry followed by final2 gives closure 0. Missing/old final scan is refused in `repro_r2.sh.out`. Additional nonempty-initial and coverage controls are assigned to the parallel tester.

## I2

`reconcile_prodl.py:154`, `:265`, `:280` and `make_manifests.sh:98`, `:106`, `:136` retain hash-bound per-piece exceptions and status. `repro_r2.sh.out`: unexpected output gives reconcile 1 and closure 6; unrelated enum30 closes 0. `exception_smoke.sh.out`: acknowledged close 0, after pull reconcile 4 with acknowledged row, altered snapshot reconcile 2. The reproduction's unconditional pull after a refused close is not a valid operational pull.

## I3

`reconcile_prodl.py:146` reconstructs native counts from closed inventory. `extra_smoke.sh.out` compares before/after one actual close and pull with a nonempty P5 inventory: smc completed=1, resource_limit=1, smcrep completed=1 on both sides. The parallel tester covers all-piece closure and scientific-failure categories.

## II1

`make_p5_list.sh:4`, `:56`; `JOB.md:116`. `repro_r2_ops.sh.out`: successful r1 consumed (0), absent initial refused (1).

## II2

`JOB.md:117` contains Sol's recovery text verbatim. This is an operator note; no truth recovery was executed locally.

## M1

`retune_throttle.sh:33` includes live non-array jobs in the admission plan and updates arrays only. `repro_r2_ops.sh.out`: other work 64 → 2, 62 → 2, 60 → 0; the saved admitted record contains enum20 and combined=192.

## M2

`REUSE.md:8`, `:19`, `:25`; `DESIGN.md:130`, `:149`, `:153`. The user explicitly reserved all of `B/tests/` to the tester, so the plan's `tests/TESTS.md` and `test_jobmd.sh` edits were not made here.

## Checks and suite handoff

Individual `bash -n` checks passed for the three changed shell scripts; `py -3` py_compile passed for `reconcile_prodl.py` with the bytecode outside the bundle; all seven edited source/doc files were verified LF-only. The isolated Python invocation is exercised by the existing Python suite.

The five requested suites were launched once detached as PID 38864 using `<PC_TEMP_PATH>`; logs, per-suite exit codes and summary are under `<PC_TEMP_PATH>`. They started before two smoke-discovered corrections: reconcile's status variable shadow and refusal before mutating an initial receipt mismatch. Consequently failures from fixture copies made before those corrections are stale and should be checked against the final code by the tester. The append-only contract intentionally replaces the old immutable-inventory expectation; final-scan coverage and exit 4 also change old assertions.

Observed while the detached run was in progress: `test_p5` finished 149 passed / 3 failed: EX13 used the pre-correction initial receipt code; RP01 and RP12 used the pre-correction status variable. The later L125–L172 controls passed extension, idempotence, completed retry, zero-expected final-scan requirement, missing/extra coverage, older scans, and unsafe retry states. `test_manifests` MM72 expects only the old marker, inventory and summary; its failure is the intended new `enum20.exceptions.tsv` snapshot. Inspect the final suite logs and `SUMMARY.txt` for all results; they were still being produced when this note was written.

The initial runner stopped without completing `test_manifests` or starting the final three suites; PID 38864 and its children were absent on inspection. Its partial logs remain untouched. The interrupted manifest suite and the three unstarted suites were launched concurrently detached by `resume_suites.sh`, PID 34156, using separate `w_resume_*` directories and `*_resume.log` / `*_resume.rc` outputs. `RESUME_COMPLETE` marks the end of that runner.

Resumed outcomes: `test_reconcile` 34 passed / 0 failed (exit 0, using `py -3 -I`); `test_retune` 37 passed / 0 failed (exit 0); `test_jobmd` 47 passed / 1 failed, JM67, because DESIGN said “appends” without the literal “append-only”; the wording was corrected after this run. The restarted manifest suite did not finish: its log records Git Bash fork failures, `Resource temporarily unavailable` and Windows errors 299 and 5; PID 34156 is no longer present and no manifest exit file was produced. Its earlier attempt reached MM74 and had the intended MM72 failure described above. No complete manifest-suite verdict is claimed.
