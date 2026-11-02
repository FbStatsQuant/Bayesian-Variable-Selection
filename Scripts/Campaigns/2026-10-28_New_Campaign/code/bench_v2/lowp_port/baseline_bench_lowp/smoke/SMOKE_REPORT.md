# LOWP benchmark smoke — review fixes, 2026-10-28

The final source was run locally using Windows R 4.4.1 and `<PC_TEMP_PATH>`, with `--test-library` explicitly recorded on all production-layout fixtures. This was a test environment, not sealed-library or remote deployment certification. The previous smoke predates LA-4 and its results are historical; the interrupted review-fix attempts remain in temp.

| Check | Result |
|---|---|
| Eight methods × three production-layout cases × two scales | 48/48 completed, six invocation exits 0; 228/228 saved rows `ok`, zero diagnostic flags |
| Smoke driver, checksums, development case, resume, tamper, forced error, identity refusal and restoration | 60/60 passed; driver exit 0 |
| Derived-rule aliases, unscored columns and one-primary invariant over all 48 units | 122/122 passed; K37 and cap data identical for p=20 and p=30 |
| Independently reconstructed from input and saved paths | F4 `ebic1_lam005` and F5 `sic_smax` supports and criteria match on p0020_S1_r001_c100 |
| Eight-method forced failures, complete registry/schema, outer conditions; A3 km2-only warning/message; production manifest bypass | 12/12 passed |
| Wrong glmnet pin without test flag / explicit test override | refused with exit 1 / completed with flag recorded |
| Resume with changed library identity | refused with exit 1 |
| F4 and F5 derived fit-gate failure | missing selection and preserved support audit verified; unrelated original-rule error not inherited by successful F4 derived row |
| F3 ridge grid | exact equality with `10^seq(3,-6,length.out=61)` |

The main run, per-invocation logs, output artifacts, `validation.csv`, `derived_checks.csv`, independent path and audit logs, and a source snapshot are under `<PC_TEMP_PATH>`. Eight-method targeted records and logs are in `bench_fix_targeted_v5/`; version and environment probes are in `bench_version_v5/` and `bench_resume_env_v5/`. Each RDS records the command line, source/input hashes, seeds, UTC fit times, package runtime-file hashes, build metadata, library paths and environment identity. Process IDs were not captured by this smoke driver. The sealed-study fixtures and their manifest predate this run. Windows R startup reported locale warnings outside method capture. The tests do not establish NOTS threading, production performance, scoring, cross-scale RNG reconciliation, or the separate D3 commitment for LA-1–LA-3.

## Post-recheck fixes (2026-10-29, manager)

RECHECK_c N1–N3 fixed (see `code/review/RECHECK_c_disposition.md`). Rerun into `<PC_TEMP_PATH>`: smoke3 60/60, derived_checks 122/122; LA-4 present on every F1–F5 row.
