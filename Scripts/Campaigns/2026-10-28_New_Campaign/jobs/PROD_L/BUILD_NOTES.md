# Build notes — INCOMPLETE; do not stage or submit

Built the deterministic inventory generator and `lists/units.tsv`, an initial CPU ceiling checker, and an adapted laptop waiter. Fixture plan, squeue inputs, and ceiling receipts are under `fixtures/`. These are partial work, not an operational job bundle.

## Deviations

- Most required files and all production submission, truth-lock, accounting, staging, and recovery integration remain unimplemented. The requested pilot source review and reuse are incomplete. No inference that these files meet acceptance criteria should be made.
- The two requested submission dry runs were not performed because the driver and its staged prerequisites do not exist. No NOTS connection or NOTS job was made.
- `bash` was not on PATH; the waiter syntax check used `C:/Program Files/Git/bin/bash.exe` instead.

## Smoke checks and outputs

- `py -3 -m py_compile` for both Python files: exit 0, no output.
- `make_lists.py --check`: exit 0: `PASS enum20: 600 unique units, 1 tasks of 600`; `PASS enum30: 600 unique units, 24 tasks of 25`; `PASS smc: 2400 unique units, 96 tasks of 25`; `PASS smcrep: 12000 unique units, 480 tasks of 25`.
- Git Bash `bash -n waiter.sh`: exit 0, no output. No other shell files have been created.
- Ceiling fixture: empty squeue reports `prod_l_peak=132`, `others_peak=0`, `combined=132`, `ADMITTED`; exit 0. The two PROD-H arrays of 50 each report `others_peak=200`, `combined=332` and `REFUSED: PROD-H present with alone profile; global ceiling exceeded`. The PowerShell command wrapper reported exit 1 for that failing native program; the Python code returns 2 on refusal.

## Open work

Complete the specified ordered source review and implementation, perform the two local-test dry runs and all other required checks, and arrange independent acceptance testing before use. Review the partial ceiling checker and waiter against the complete scheduler fixtures as part of that work.
