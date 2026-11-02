# Build notes (PROD_L_BENCH)

**Builder finished (manager completion, 2026-10-30).** Terra (first builder) delivered: lists + `tools/make_lists.py`, `bench_verify.py`, `batch_runner.sh`, `slurm/` (common.sh, s0_verify, s1_bench, s2_benchretry, s9_collect), `R/bench_env_probe.R`, `R/prodl_inputs_check.R` (copy), `stage_local.sh`, `stale_lib.sh`, `clear_stale.sh`, `ceiling_check.py`/`guard_check.sh`/`frozen_check.sh` (copies), `retune_throttle.sh`, `waiter.sh`, `final_accounting.sh`, a partial REUSE.md. It stopped before the driver.

The manager completed: `submit_bench.sh`, `make_resubmit.sh`, `reconcile_bench.py`, `make_manifests.sh`, `cleanup_bench.sh` (PROD_L's, names only), `accept_bench.R`, `JOB.md`, `CORE_HOURS.md`, `tests/live/live_bench.sh`; and fixed staging.

## Deviation resolved: frozen manifest path format
The r2 manifest lists paths WITHOUT `./`; the reused (unchanged) `frozen_check.sh` compares against `find .` output (`./`-prefixed). `stage_local.sh` now writes the staged `code/bench_lowp.SHA256SUMS` as the r2 manifest with `./`-prefixed paths and the SAME hashes, proves the two are identical pair by pair (same count), keeps the original as `code/bench_lowp.r2_manifest_original.txt` and checks its sha256 = `85a18248…a6b7`. Every frozen check (staging, submission, s0_verify, every bench task) runs against the normalized copy. Verified: staging on the real sealed study → 64,379 KB, 1,261 files, frozen check PASS, no truth/holdout/dev.
