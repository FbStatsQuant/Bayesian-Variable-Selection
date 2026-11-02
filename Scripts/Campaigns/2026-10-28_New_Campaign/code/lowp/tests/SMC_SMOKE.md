# LOWP SMC smoke test (local, Windows)

Run 2026-10-28 on the local PC (R 4.4.1 ucrt, Rtools g++, `Makevars.v3` flags via `v3_compile`). Study root `TMP\study` (sealed by `R/lowp_seal.R`), outputs `TMP\smoke\results\<run_id>\…`, `TMP` = `C:\Users\felip\AppData\Local\Temp\lowp_work\gen`. Adapter `smc/adapter_lowp.R` (SHA-256 `3d0c836e…2362060`, before README/CHANGES were added) and `smc/run_smc_case.R`; core = a copy of `code/core/v2_2/core` in `TMP\core_copy` (so nothing under `code/core/` was written; its `.cpp_cache` already held a matching Windows build, so the table runs needed no compile; afterwards the copy's cache was deleted and one fit (p0020_S1_r001 c100, run `smoke4_compile`) rebuilt it through `v3_compile` with `Makevars.v3`: wall 48.8 s in total, and `log_Z` and `pip` are bit-identical to the cached-build run); core source hash `v3_source_sha256 = 8c8c7413208a382fc68b9493bc2ba6babc55f42f0bfae0975a20425849e7fe99`. Allocation 8 GB, 24 h (the CLI default).

## Table (run_id `smoke2`, one process per fit, `Rterm.exe --file=run_smc_case.R`)

| Case | Scale | Rep | Status (native / rows) | runtime_s | Stages: stage_table rows (final-bridge per island) | Escalated | HPM | log Z (full) | log Z − log m0 | Peak WS MB (paged MB) | Wall s (R start + load + fit) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| p0020_S1_r001 | c100 | – | completed / warning,warning | 5.57 | 9 (1) | no (tier 0) | 3;7;14;16 | −85.0870 | 204.2378 | 106.8 (195.7) | 40.2 |
| p0020_S1_r001 | c050 | – | completed / warning,warning | 4.74 | 9 (1) | no | 3;7;14;16 | −192.2569 | 97.0680 | 107.5 (195.5) | 46.6 |
| p0030_S4_r050 | c100 | – | completed / warning,warning | 17.98 | 189 (15) | no | 3;7;14;16;25 | −107.5142 | 181.8106 | 184.6 (206.7) | 70.2 |
| p0030_S4_r050 | c050 | – | completed / warning,warning | 23.53 | 121 (14) | no | 3;9;14;16;22 | −214.9098 | 74.4150 | 187.2 (209.0) | 86.6 |
| p0020_S1_r001 | c100 | 1 | completed / warning,warning | 6.87 | 9 (1) | no | 3;7;14;16 | −85.0776 | 204.2472 | 107.3 (195.7) | 53.4 |

- All five fits: branch `smc`, final tier 0, 4 islands, `diag_codes = cut_group` (informational), exit code 0, `.done` written. `status = warning` on both rules is the Windows `/proc/self/status` warning of the core (`v3_fit.R` line 3), not a fit problem; it will not occur on Linux.
- Stages: `fit$stage_table` rows over all phases (pilot, diagnostic, final bridge); in brackets the final-bridge stages per island (rows / 4 islands).
- **Peak memory** = high-water mark `PeakWorkingSet64` (and `PeakPagedMemorySize64`, commit) of the `Rterm.exe` process, polled every 100 ms from PowerShell (`Start-Process -PassThru`) until exit (`scr/run_one.ps1`, not kept in CAMP). Reading the property after exit returned 0, hence the polling; the value is a lower bound within one polling interval. It excludes the PowerShell parent. `peak_memory_kb` of the core is NA (Linux-only).
- Repeat 1 of p0020_S1_r001 c100: seed 5,221,001 (primary 5,220,001), files `SMCBVS_rep1.*` beside `SMCBVS.*`, log Z −85.0776 versus −85.0870, same X/y hashes, rows carry `method_seed = 5221001`.

## Extra checks

- **Truth separation.** A study copy that contains only `inputs/p0020/p0020_S1_r001.rds` and `manifests/` (no `truth/` directory at all) was fitted for p0020_S1_r001 c050 (run `smoke3_notruth`): success, and `log_Z`, `pip` and `hpm` are bit-identical to the run from the full study. The adapter source contains the word `truth` only in comments and in the path refusal; `smcbvs_safe_path` refuses any `truth`/`holdout` path component (tested: error raised).
- **Dev path.** `dev_p0020_S2_r003` c100 with `--development --study …\study\dev` (run `smoke3_dev`): completed, method seed 6,230,003, HPM 3;7;14;16, log Z −126.9532, runtime 10.37 s, 164 stage rows, peak WS 123 MB.
- **Guards tested without the core:** ids `p0500_…` rejected; `dev_` id without `--development` rejected; `--repeat 6` rejected; scale c075 rejected; id/scale mismatch rejected; seeds of `p0020_S3_r007` and `p0030_S6_r100` for repeat none/1/5 equal data + 4,000,000 (+1,000·m); a finished unit is skipped on rerun (primary and repeat); a changed allocation on a finished unit stops with `saved unit identity mismatch (allocation_sha256); use a new run_id`.
- Timing is a Windows desktop figure, not NOTS timing; use it only as an order of magnitude (seconds per fit at p = 20–30).
