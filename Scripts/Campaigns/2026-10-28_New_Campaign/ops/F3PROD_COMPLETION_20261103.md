# BENCH_F3_PROD completion report (OPS, 2026-11-03) — run 20261102T1252Z_bench_f3v2_prod

Bundle `bench_audit/jobs/BENCH_F3_PROD` (HQ D64/D65 READY; FINAL ledger `BUNDLE_SHA256SUMS_FINAL`, 63 entries, 90579ad6…7e07; freeze 8905f52e…; upload digest b7d0e36b…). The run is F3 adaptive lasso v2 (lasso pilot, D42) on the 1,200 frozen datasets × {c100, c050}: **2,400 one-CPU fits**. Settings: 30 min and 2 GiB per task (D64), Sapphire Rapids, GCC/14.3.0 + R/4.5.2, GNU time 1.9 (sha256 01dd5765…).

## 1. Submission (four cells, launched one after another, each only once the previous cell was terminal; HQ D65)

| Cell | Job | Array | Submitted (UTC) | Terminal (UTC) | sacct |
|---|---|---|---|---|---|
| p0500_c100 | 2503200 | 1-1199:2%30 | 2026-11-02 18:11 | 18:51 | 600 COMPLETED |
| p0500_c050 | 2504013 | 2-1200:2%30 | 19:11 | 20:03 | 600 COMPLETED |
| p1000_c100 | 2507545 | 1201-2399:2%30 | 20:22 | 21:02 | 600 COMPLETED |
| p1000_c050 | 2509541 | 1202-2400:2%30 | 21:49 | 22:40 | 600 COMPLETED |

Before every launch: the CPU-ceiling check (existing tasks + 30 ≤ 96, i.e. ≤ 192 billed), `launch.py --dry-run` rc 0, and `launch.py`'s own gate (the disk guard plus the frozen-code check). Incidents, each stopped safely with nothing submitted:
- **Cell 1, first attempt (17:28Z):** stage.sh's guard refused at home 9.86 GiB. It launched after the HQ D74 erase.
- **Cell 4, first attempt (21:02–21:07Z):** launch.py's `gate.sh` failed before any submission (CalledProcessError; its output was not captured). The disk guard is gate.sh's first check, and home was ≈ 9.70 GiB by `du` at 21:08Z, over the 9.6 GiB limit. So a guard refusal is the **inferred** cause, not one the log shows directly. The relaunch ran gate.sh on its own first (`GATE_OK`, home 8.22 GB), and was submitted after the HQ D79 clean-up.

The guard was never overridden.

## 2. Terminal accounting, retry and acceptance (JOB.md)
- **Retry dry run:** all 4 cells show `states {'COMPLETED': 600}` and `timeouts_without_valid_result 0`, so **no retry was submitted**. An OPS regex bug in the first collection wrapper (22:45Z) falsely reported "DISPOSITION_NEEDED". It was fixed and the wrapper re-run; the evidence is kept as `ops/evidence/ops8_f3prod_collect_run1_regexbug.txt`.
- **Reconcile** (env.sh sourced; source sha256 3e01c77b…, the same F3 tree hash as the dev run): rc 0, **`integrity_counts={'valid': 2400}`, `rule_status_counts={'ok': 14400}`, `unexpected=0`**. Expected 2,400 = observed 2,400, with no failed or missing unit.
- **Accounting:** **71.98 elapsed core-h / 143.96 allocated (billed) CPU-h**, against the dev-pilot estimate of 66.6 / ≈ 133. By cell (elapsed): p500 c100 15.07, p500 c050 22.96, p1000 c100 14.18, p1000 c050 19.77.
- **Timing** (GNU time, 600 fits per cell; nearest-rank p95):

| Cell | mean wall s | p95 s | max s | max RSS KiB |
|---|---:|---:|---:|---:|
| p500 c100 | 86.4 | 143.9 | 207.4 | 289,420 |
| p500 c050 | 133.5 | 225.2 | 360.0 | 288,700 |
| p1000 c100 | 80.7 | 137.1 | 229.5 | 296,468 |
| p1000 c050 | 114.9 | 197.5 | 321.3 | 296,600 |

  Every fit finished within 20 % of the 30-min wall limit (max 360 s against 1,800 s) and used ≤ 0.29 GiB of its 2 GiB.

## 3. Manifests, download, verification, deletion

File counts exclude `MANIFEST.sha256` itself; the transfer counts in the pull log include it (+1). The Scratch column gives each delete command's **start** time; the whole deletion completed at 2026-11-03T00:04:27Z (`F3_DELETE_DONE`).

| Folder | Files | Bundle MANIFEST sha256 | Local copy (`NOTS Data\New_Campaign\…`) | Scratch (delete started) |
|---|---:|---|---|---|
| results/…/p0500 | 4,800 | e2600c82… | transfer VERIFIED; `sha256sum -c` OK; `manifests.py --verify` rc 0 | deleted 2026-11-02 23:49Z |
| results/…/p1000 | 4,800 | 6b61c4b2… | VERIFIED; OK; rc 0 | deleted 23:55Z |
| logs/20261102T1252Z_bench_f3v2_prod | 4,822 | 5c96e7f6… | VERIFIED; OK; rc 0 (holds reconcile.txt, accounting.tsv, timing.tsv, retry_dryrun.txt, sacct_*.txt, jobs.tsv, resources_used.json, gate/squeue snapshots) | deleted 2026-11-03 00:01Z |
| upload/20261102T1252Z_bench_f3v2_prod | 35 | (transfer manifest 17cb83e6…) | VERIFIED | deleted 00:04Z |

Deletion followed the bundle's own rule. Sol reviewed the exact list and receipts (`ops/F3_DELETION_LIST_20261102.md`; `review/SOL_REVIEW_F3_DELETION_20261102.md`, R1 ACCEPT WITH FIXES, R2 ACCEPT). Each folder was then deleted with `remote_pack.sh delete <folder> <receipt transfer-manifest sha>` (re-hashed on NOTS), after the D79 fail-closed `/proc` scan found 0 references. The F3 dev run's four folders were deleted in the same pass. Both results parents were removed, and the final check found nothing left (`F3_DELETE_DONE` 2026-11-03T00:04:27Z, `ops/CLEANUP_LOG.md`). No `config/<run_id>` folder exists (HQ D64).

## 4. Evidence
`ops/evidence/`:
- launches: `ops8_f3prod_cell1.txt`, `ops8_f3prod_cell2.txt`, `ops8_f3prod_cell3.txt`, `ops8_f3prod_cell4.txt`, and the earlier attempts kept as `ops8_f3prod_cell1_attempt1/2/3*` and `ops8_f3prod_cell4_attempt1_gatefail.txt`;
- monitors: `ops8_f3prod_cell{1..4}_monitor.log`;
- collection: `ops8_f3prod_collect.txt` and `ops8_f3prod_collect_chain.txt`;
- pulls: `ops8_f3prod_pulls.txt`;
- deletion: `ops8_f3_delete.txt`.

Transfer receipts are in `ops/transfer/receipts/`.

## 5. Review and open items
Sol 6.1 (high), 2026-11-03: **ACCEPT WITH FIXES**, no blocking defect (`review/SOL_REVIEW_F3PROD_COMPLETION.md`). Its two should-fixes (the cell-4 cause marked as inferred; delete start times versus completion) and its note (file counts exclude the manifest) are applied above. The run is closed and has no open items.
