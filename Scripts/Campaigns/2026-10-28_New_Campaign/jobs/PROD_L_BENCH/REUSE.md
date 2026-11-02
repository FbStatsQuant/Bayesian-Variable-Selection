# Reuse inventory (PROD_L_BENCH from PROD_L)

Sources are in `CAMP/jobs/PROD_L` unless stated; "unchanged" = byte-identical copy. PROD_L itself derives from the accepted pilot rev 7d (see `PROD_L/REUSE.md`).

| PROD_L_BENCH file | Source | Change |
|---|---|---|
| `bench.env` | `prodl.env` | benchmark modules/library only; RID `<STAMP>_lowp_bench`; result run id `<STAMP>_lowp_benchres` for bench and benchretry; pieces bench (1 h / 600 s) and benchretry (1 h / 1,200 s); D57 `PLANNED_HOME_MB_STAGE` 75 / `PLANNED_HOME_MB_MAIN` 5; `V221_DIR`/`V221_SUMS` point at the frozen benchmark tree so the reused `pilot_require_frozen` checks it |
| `slurm/common.sh` | `slurm/common.sh` | hook `PRODL_BENCH_EXTRA`; `benchretry` among the arms that require GNU time; frozen-check messages name the checked tree |
| `slurm/s0_verify.sbatch` | `slurm/s0_verify.sbatch` | frozen check of `code/bench_lowp`, P0b (unchanged script), `R/bench_env_probe.R`; no P0a (no truth staged) |
| `slurm/s1_bench.sbatch`, `slurm/s2_benchretry.sbatch` | `slurm/s2_smc.sbatch` | benchmark modules (`pilot_modules bench`), piece constants |
| `slurm/s9_collect.sbatch` | `slurm/s9_collect.sbatch` | no unlock receipt (no truth); requires an accounting row for every predecessor id before the guard |
| `batch_runner.sh` | `batch_runner.sh` | benchmark unit command (`run_bench_case.R --methods all --library … --threads-check`); CLI exit 2 (committed failed rule) = ok with `cli_status=failed_rules`; skipped when all 8 methods say skipped; no P5 branch |
| `submit_bench.sh` | `submit_prodl.sh` | waves main / rN only; no truth-lock steps; no-truth check; refusal while PROD-L fitting jobs are active (`--allow-concurrent-prodl` for HQ); D57 single reservation + `stage_on_disk_kb` in the guard receipt; job names `lowpB_` |
| `make_resubmit.sh` | `make_resubmit.sh` | one call per round; routing bench / benchretry (one doubled-time retry) / exceptions; `bench_verify.py` |
| `bench_verify.py` | `prodl_verify.py` | case = all 8 method units valid (exact sidecar, done marker, CSV columns and statuses, identity) |
| `reconcile_bench.py` | `reconcile_prodl.py` | one piece of 2,400 cases; ledgers of bench + benchretry; rule-status table per method; no P5; the closing `MANIFEST.sha256` is not an unexpected output |
| `make_manifests.sh` | `make_manifests.sh` | pieces bench / logs; no P5 gates; logs not scanned for stale artefacts |
| `stale_lib.sh`, `clear_stale.sh` | same | benchmark artefact kinds: `*.lock` dirs, the CLI's hidden `.<M>.<ext>…` temp files, incomplete method units |
| `cleanup_bench.sh` | `cleanup_prodl.sh` | names only (run folder, OWNER text, job prefix, env path) |
| `stage_local.sh` | `stage_local.sh` | benchmark tree + `./`-normalized r2 manifest (proven identical; original kept and hash-checked) + inputs-only study; no truth, dev or truth manifest |
| `waiter.sh`, `retune_throttle.sh`, `final_accounting.sh` | same | job prefix / run identity / pieces |
| `guard_check.sh` | `guard_check.sh` | identical to PROD_L's post-D57 version (home probe against the guard's own limit) |
| `ceiling_check.py`, `frozen_check.sh`, `R/prodl_inputs_check.R` | same | unchanged |
| `R/bench_env_probe.R`, `accept_bench.R`, `tools/make_lists.py`, `lists/units.tsv` | — | new |
