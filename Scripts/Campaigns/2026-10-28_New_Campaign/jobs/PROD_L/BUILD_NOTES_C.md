# Builder C notes

Files: `reconcile_prodl.py`, `bench_hook/README.md`, `JOB.md`, `REUSE.md`, and this record.

Checks on Windows laptop, 2026-10-30:

- `py -3 -m py_compile <absolute bundle path>/reconcile_prodl.py`: exit 0.
- `py -3 <PC_TEMP_PATH>`: exit 0; output: `PASS: done, deferred, timeout, checksum mismatch, native status, P5, repeat path, unexpected folder; exits 0 and 1`. Fabricated inputs, outputs, script and inventory remain under that directory.
- Markdown tables use plain pipe-table syntax; inspected headers and separators in JOB.md and REUSE.md.

No NOTS connection or production computation. Ledger end outcomes other than failed/timeout without a verified result are reported as not_run with the anomalous end in detail; checksum and CSV exceptions appear in INVENTORY.md. A valid sidecar defines done independently of the CSV scientific status, as specified. Reuse entries for files under parallel construction are pending manager reconciliation. Operational commands follow DESIGN; final CLI integration should be verified after the other builders complete.

