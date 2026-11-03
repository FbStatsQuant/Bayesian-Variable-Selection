# BENCH_F3_DEV evidence summary (OPS, 2026-11-02) — run 20261030T1855Z_bench_f3v2_dev, job 2496644

Bundle `bench_audit/jobs/BENCH_F3_DEV` (ledger BUNDLE_SHA256SUMS_FINAL, 28 entries; the `_R2REVIEWED` ledger was the pre-R2-4 state; freeze 8905f52e…), F3 adaptive lasso v2 (lasso pilot, D42), 26 one-CPU fits: 24 dev cases (p500/p1000 × S1–S6 × r001 × c100/c050) + production p1000 S4/S6 r001 c050. Sapphire Rapids, GCC/14.3.0 + R/4.5.2, glmnet 5.1, GNU time 1.9 (absolute path, sha256 01dd5765…). Submitted 2026-11-02 03:34Z (`1-26%13`, 75 min / 4 GiB per task) after the PROD-L truth unlock (HQ D59).

## Outputs valid
- Slurm: **26/26 COMPLETED**, 0 failed/timeout/OOM (sacct; `retry.py --dry-run`: `{'COMPLETED': 26}`, timeouts without valid result 0, so no retry).
- `reconcile.py` (kind dev, source sha256 3e01c77b…): **26/26 rows `valid`**, every row's six rules `ok,ok,ok,ok,ok,ok`; exit 0 (rerun with `env.sh` sourced; see note).
- Manifests (`manifests.py`, all three folders, `--verify` rc 0): p0500 48 files `bfae02b0…`, p1000 56 files `62d71add…`, logs 64 files `976a504e…`.
- Failures: **none**.

## Cost and resources
- Accounting: **0.757 elapsed core-h (1.514 allocated/billed CPU-h)**; per cell: p500 c100 0.131, p500 c050 0.206, p1000 c100 0.134, p1000 c050 0.287 (elapsed core-h).
- Per-fit GNU time: wall **37–192 s**, max RSS **≤ 291 MiB** (291,268 KiB).

| Cell | n | mean wall s | p95 (nearest rank) s | max RSS KiB | pilot-rule time | pilot-rule memory | est. PROD core-h (600 fits) |
|---|---:|---:|---:|---:|---:|---:|---:|
| p500 c100 | 6 | 75.3 | 124.3 | 285,300 | 10 min | 2 GiB | 12.5 |
| p500 c050 | 6 | 120.8 | 190.7 | 285,324 | 10 min | 2 GiB | 20.1 |
| p1000 c100 | 6 | 77.6 | 105.8 | 291,044 | 10 min | 2 GiB | 12.9 |
| p1000 c050 | 8 | 126.2 | 192.3 | 291,268 | 10 min | 2 GiB | 21.0 |
| **Total** | 26 | | | | | | **66.6** (≈ 133 billed) |

(HQ D64 then set the production wall to 30 min / 2 GiB in every cell.)

## Operational notes (OPS)
1. First submission attempt (2026-10-30 18:57Z) refused safely at `stage.sh`'s disk guard: `du` could not read PROD-L's mode-000 truth trees during PROD-L's main wave; staged and launched after the verified unlock (D59).
2. The first `reconcile.py` run crashed before its summary (`Rscript` not on PATH): OPS had sourced `runner/env.sh` only inside the retry subshell. The crashed output is kept as `logs/<run>/reconcile_partial_20261102T114827Z.txt`, and the logs manifest written too early as `MANIFEST.sha256.superseded_20261102T114827Z` (both inside the logs folder); reconcile was rerun with `env.sh` (rc 0) and the manifests regenerated over all three folders (the script preflights them together). `env.sh` switches on errexit: run it in a subshell or as the last step of a script.
3. Raw evidence: `ops/evidence/ops7_f3dev_20261030T1855Z_{prepare,scp,launch,launch2}.txt`, `ops/evidence/ops_finish_h_f3_20261102.txt`, `ops/evidence/ops_f3fix_prodl_close_20261102.txt`, `ops/evidence/ops_f3manifest_prodl_close_20261102.txt`, `ops/evidence/ops7_f3dev_monitor.log`. The three folders (+ upload) are being pulled to `NOTS Data\New_Campaign\` (copy only); scratch deletion after Sol reviews the exact deletion list (JOB.md).
