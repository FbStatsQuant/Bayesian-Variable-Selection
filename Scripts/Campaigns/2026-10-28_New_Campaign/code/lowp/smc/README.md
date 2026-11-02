# RETIRED (2026-10-29, CONF-2b): the LOWP SMC-BVS runner fork

The Regime L runner that used to live here (`adapter_lowp.R`, `run_smc_case.R`, a p ∈ {20, 30} copy of the v2.2 study adapter) has been merged into the single frozen code tree **v2.2.1** (DECISIONS D19):

- runner: `code/core/v2_2_1/study/run_case.R` (both regimes; `--repeat m` for regime L; `--p5-retry`);
- adapter: `code/core/v2_2_1/study/adapter.R` (regime table `smcbvs_regimes()`; regime L keeps the fork's seeds, manifest and record layout);
- changes: `code/core/v2_2_1/CHANGES_v2_2_1.md`; manifest: `code/core/v2_2_1.SHA256SUMS`.

Use v2.2.1 for every SMC-BVS run (pilot, PROD-L, PROD-H). The CLI flags are unchanged from the fork: `--case --scale --study --outroot --run-id --core-dir --mem-gb --hours --development [--repeat m] [--manifest]`. The output layout is INTERFACES I3 (`SMCBVS[_rep{m}].*`).

The retired files' sha256 values are in `code/CODE_LEDGER.md` (LOWP entry). A hash-verified copy, kept as regression evidence only, is at `conformance/work/v2_2_1_regression/trees/fork_lowp_smc/`. Regression (b) there shows that the merged path reproduces the fork exactly.
