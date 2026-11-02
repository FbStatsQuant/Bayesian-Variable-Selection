# Local bundle checks

Run by implementation worker. These are script/unit checks on synthetic inputs, not benchmark fits. No SSH, Slurm job or remote workload was run.

## Round 3 (historical)

- Python unittest discovery: **16/16** production tests and **2/2** dev sizing tests passed. The mapping checks exhaustively cover 2,400 distinct production units and 26 pilot units. CLI dry-runs output four 600-unit %30 production arrays and one 26-unit %13 pilot array.
- Mock `squeue`, `sbatch`, and `sacct` exercise sequential cell submission, a 100-task guard including all fb31 arrays, refusal above that ceiling, terminal vs live vs failed-query handling, all four accounting cells, incomplete accounting refusal, one timeout-only retry at double time, and a second-attempt refusal. A simulated sbatch client failure after acceptance retains the intent and blocks a duplicate. FAILED/OOM do not enter the retry.
- Reconciliation fixture: 26 valid synthetic four-file units; missing file, damaged data, duplicated checksum entry and an extra case are detected. Frozen-tree checks reject an extra file, changed content and wrong source hash; synthetic prepare/upload and folder-manifest checks reject changed bytes.
- R validator: one positive and four negative in-memory object controls; two positive and four negative saved RDS/CSV CLI controls. The positives include an empty support. Negatives remove coefficients, alter beta support, change schema version, or change source hash. Windows R emitted locale warnings; exit status was zero and expected nonzero negative-control subprocess warnings were observed.
- Git Bash guard fixture: **2/2** refusal checks passed (campaign home above 0.5 GiB and total home above 9.6 GiB). GNU time checks accepted a working stub and rejected a lying stub and a relative path. `bash -n` passed for six runner shell scripts.

Run the Python suites with absolute paths:

```text
py -3 -B -m unittest discover -s "<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/tests" -p "test_*.py" -v
py -3 -B -m unittest discover -s "<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_DEV/tests" -p "test_*.py" -v
```

## Sol review 1 rerun

- **19/19** production Python tests and **2/2** DEV Python tests passed. These include real-freeze prepare, simulated stage/repeated verification, copied-upload verification, real single-case reconciliation through R, retry fsync ordering and retained intent on client failure.
- R: one complete real frozen-runner RDS/CSV record plus its actual frozen dev input and manifest passed. **10/10** Sol corruptions and **4/4** earlier plus **3/3** additional OLS/weight/both-copy coefficient corruptions failed with asserted reason strings. Selected-point coefficient mutation of both copies was rejected by KKT.
- Test commands use at most two R/Python processes at once. Windows R locale warnings were observed, as before.

## Frozen-runner branch fixtures

- **3/3** complete RDS/CSV/SHA-256/done saved-record positives pass: a genuine zero-predictor pilot, a genuine singleton pilot, and a genuine whole-fit failure. The same saved-record validation rejects **6/6** branch-specific corruptions with individually asserted reasons; each is also checked through the object validator.
- The original failed run's zero runtime is rejected by the frozen validator; it remains saved as evidence. A second runner-written failure uses a documented 50-ms test-wrapper delay to ensure the unchanged frozen failure records a positive elapsed time. The wrapper normalizes read.csv's all-NA `k` column from logical to integer before calling the unchanged frozen validator. The original 10 Sol corruptions, 4 earlier controls and 3 further controls still pass.

The actual NOTS task, full 26/2,400-unit reconciliation, remote module gate, and OPS transfer helper require OPS and real remote outputs. Independent review is pending; no claim of release readiness is made.

## Sol review 2 — implementation checks

- **14/14** rehashed saved-record controls pass, with distinct reasons listed in `REVIEW2_FIXES.md`: three seeds, four null contracts, the CV primary substitution, incorrect EBIC criterion, wrong EBIC minimizer, later occurrence, weighted grid, candidate table and CV diagnostics.
- **3/3** additional whole-fit-failure seed controls are rejected before the failure return. The real, null, singleton and whole-failure positives remain valid; the six prior saved branch corruptions still fail as intended. The earlier 17 real-record controls continue to pass.
- Python suites rerun: **19/19** production and **2/2** DEV. At most two local R/Python processes were used. No fitting or remote execution.

## 2026-11-02, HQ D64 resource fill (manager)

- `runner/resources.json` = 30 min / 2 GiB in all four cells; `tests/test_workflow.py` expected wall-time literal updated to match (30 ×4).
- Python suites: **19/19** production, **2/2** DEV; `tests/test_guard.sh` with `ops/guard.sh`: **2/2** refusals PASS; `launch.commands('prod', …)` gives `--array=…%30 --time=30 --mem=2G` for the 4 arrays (2,400 tasks); `frozen.py check` FROZEN_OK. Logs: `code/bench_v2/review/manager/d64_{prod,dev}_tests.log`.
- Authoritative ledgers rewritten and verified: PROD 63/63 (90579ad6…5e07), DEV 26/26 (3353b6f6…64ed); historical ledgers in `archive_ledgers/`.
