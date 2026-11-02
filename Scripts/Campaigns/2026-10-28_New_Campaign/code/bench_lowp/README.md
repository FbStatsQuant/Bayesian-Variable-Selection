# LOWP benchmark runner

**The port has passed local tests; independent review and release gates remain.** F1–F3 code comes from the bench_v2 frozen snapshot `2a8362b2f348`; F3 uses the D42 lasso pilot. F1–F5 schema-v2 records save per-rule penalized and OLS coefficient evidence. A1–A3 retain their existing `beta` and `pip` evidence. See `../bench_v2/lowp_port/` for baseline and verification status.

Run one dataset and scale with a separate output root and an explicit sealed R library:

    Rscript run_bench_case.R --study STUDY --outroot SCRATCH --run-id RUN --case p0030_S4_r050 --scale c100 --methods all --library SEALED_LIB --threads-check

Production IDs require the input manifest and `--library`; package versions are checked and non-base/recommended dependencies must resolve from that library. `--test-library` explicitly permits unsealed and non-pinned libraries for tests, is recorded in every row and RDS, and must not be used for production analysis. The older environment version override is refused unless this flag is present. Development IDs require `--development`; only development IDs may use `--no-manifest`. Methods are all or a comma-separated subset of F1–F5 and A1–A3. Paths with truth or holdout components are refused.

Results are in `SCRATCH/results/RUN/p{pppp}/{dataset_id}_{scale}/{method}.{rds,csv,sha256,done}`. Completed units are skipped only after input, source, package provenance and environment identity checks; partial or inconsistent units are refused. The RDS saves the primary fit, derived rows, source and input hashes, library/build provenance, package-file hashes and environment. Scoring placeholders remain NA. Exit 0 means no failed rules, 2 means a saved or resumed failure, and 1 means infrastructure/input refusal. Thread limits must also be set before starting R in deployment.

For local Windows tests, use `smoke/run_smoke.R` with the specified R library; it explicitly marks its production-layout fixtures as test-library runs. See `smoke/SMOKE_REPORT.md` for the results and limits.
