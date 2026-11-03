# BENCH_F3 (dev + prod) scratch deletion list — for Sol review (OPS, 2026-11-02)

Bundles: `bench_audit/jobs/BENCH_F3_DEV/JOB.md` and `bench_audit/jobs/BENCH_F3_PROD/JOB.md` § "Download, verify, clean". After every download verifies, Sol reviews the exact deletion list and the receipts. D44 B3: the helper is launched from `/scratch/fb31/New_Campaign`, outside every deleted tree. OPS then runs `bash /home/fb31/projects/BVS/New_Campaign/code/ops/remote_pack.sh delete <exact remote folder> <manifest_sha256 from that folder's VERIFIED transfer receipt>` once per folder. The helper re-hashes the folder and refuses if any byte changed or any fb31 job is queued or running. Each deletion is recorded in `ops/CLEANUP_LOG.md`.

**Nothing else is deleted.** Explicitly not deleted:
- the frozen campaign code (`/home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso`, installed by stage.sh);
- the original study (`/projects/ml75/fb31/BVS/bench20261019/`, which stays frozen until RELOCATION_OK);
- anything on home.

## Runs
- **PROD** `20261102T1252Z_bench_f3v2_prod`: jobs 2503200, 2504013, 2507545, 2509541, all terminal (2,400 COMPLETED).
  - COLLECT_OK at 23:16:26Z. Retry dry run: 0 TIMEOUT units in each of the 4 cells.
  - Reconcile rc 0: `integrity_counts={'valid': 2400}`, `rule_status_counts={'ok': 14400}`, `unexpected=0`.
  - Accounting: 71.98 elapsed core-h, 143.96 billed. Timing rc 0.
  - Manifests: p0500 `e2600c82…`, p1000 `6b61c4b2…`, logs `5c96e7f6…`.
  - Evidence: `ops/evidence/ops8_f3prod_collect.txt`.
- **DEV** `20261030T1855Z_bench_f3v2_dev`: job 2496644, 26/26 COMPLETED, reconcile 26 valid. See `ops/F3_DEV_EVIDENCE_20261102.md`. Manifests: p0500 `bfae02b0…`, p1000 `62d71add…`, logs `976a504e…`.

## Exact list (8 folders)

| # | Remote folder (delete) | Local copy (`NOTS Data\New_Campaign\…`) | Transfer receipt (`ops/transfer/receipts/`) | Files (incl. MANIFEST) | Bytes | Transfer manifest sha256 (delete argument) | Local bundle-manifest check |
|---|---|---|---|---:|---:|---|---|
| 1 | `/scratch/fb31/New_Campaign/results/20261102T1252Z_bench_f3v2_prod/p0500` | `results\20261102T1252Z_bench_f3v2_prod\p0500` | `20261102T231653Z_…__p0500.verify.json` | 4,801 | 55,772,798 | `344d2713c11b651d1b1df3717da014f6f9f50aac5477ce3b2638ff494a324137` | sha256sum -c OK `e2600c82…`; manifests.py --verify rc 0 (4,800) |
| 2 | `/scratch/fb31/New_Campaign/results/20261102T1252Z_bench_f3v2_prod/p1000` | `results\20261102T1252Z_bench_f3v2_prod\p1000` | `20261102T232346Z_…__p1000.verify.json` | 4,801 | 57,104,756 | `d13f0dd38bc58d07f14e8339bef8cc39d1810099951b89a49db861e8c7a77381` | OK `6b61c4b2…`; --verify rc 0 (4,800) |
| 3 | `/scratch/fb31/New_Campaign/logs/20261102T1252Z_bench_f3v2_prod` | `logs\20261102T1252Z_bench_f3v2_prod` | `20261102T233033Z_…logs__20261102T1252Z_bench_f3v2_prod.verify.json` | 4,823 | 2,173,499 | `4f69ac3258e85e431f2f3a0a81b0667454353747a20ecb3f3d48f3cec0a6d1e5` | OK `5c96e7f6…`; --verify rc 0 (4,822) |
| 4 | `/scratch/fb31/New_Campaign/upload/20261102T1252Z_bench_f3v2_prod` | `upload\20261102T1252Z_bench_f3v2_prod` | `20261102T233710Z_…upload__20261102T1252Z_bench_f3v2_prod.verify.json` | 35 | 169,847 | `17cb83e6045f0316e373106cd4da55c462c1e1e3597878dbf599b41a29f0b3fd` | transfer VERIFIED (no bundle manifest in upload) |
| 5 | `/scratch/fb31/New_Campaign/results/20261030T1855Z_bench_f3v2_dev/p0500` | `results\20261030T1855Z_bench_f3v2_dev\p0500` | `20261102T172831Z_…__p0500.verify.json` | 49 | 559,567 | `f79623e9c9d6f4fbaca15c2f88a8548ef573f3e9f5926fb1eb7b3d8596e2dd27` | OK `bfae02b0…` |
| 6 | `/scratch/fb31/New_Campaign/results/20261030T1855Z_bench_f3v2_dev/p1000` | `results\20261030T1855Z_bench_f3v2_dev\p1000` | `20261102T172839Z_…__p1000.verify.json` | 57 | 657,830 | `f40fbe059dcfae37509e73250c79bdc37015a5fa3ed50a4a735379bc71a2a616` | OK `62d71add…` |
| 7 | `/scratch/fb31/New_Campaign/logs/20261030T1855Z_bench_f3v2_dev` | `logs\20261030T1855Z_bench_f3v2_dev` | `20261102T172847Z_…logs__20261030T1855Z_bench_f3v2_dev.verify.json` | 65 | 35,598 | `2b07896a8aa3cf82abddc998d3709bc4ee97006826b7405e91767f91a6a87ae6` | OK `976a504e…` |
| 8 | `/scratch/fb31/New_Campaign/upload/20261030T1855Z_bench_f3v2_dev` | `upload\20261030T1855Z_bench_f3v2_dev` | `20261102T172855Z_…upload__20261030T1855Z_bench_f3v2_dev.verify.json` | 35 | 168,328 | `171118367cd3207bc643a9886d17e528da17ee1c858be7ebeedd51dd7fdf3dfa` | transfer VERIFIED |

After rows 1–2 and 5–6, the now-empty parent folders `results/20261102T1252Z_bench_f3v2_prod` and `results/20261030T1855Z_bench_f3v2_dev` are removed with `rmdir`. That works only if they are empty, and it is checked.

The transfer manifest (column 7) covers every file, including the bundle `MANIFEST.sha256`. That is why it differs from the bundle-manifest hash in column 8. `remote_pack.sh delete` recomputes it on NOTS and refuses unless it is equal.

## Executor
`ops/scaffold/f3_delete_remote.sh`, run detached on the control lane (`remote_bg.sh`) **after** PROD_L_BENCH (2511134–2511136) is terminal, because remote_pack refuses while fb31 jobs run.
1. `cd /scratch/fb31/New_Campaign`; check that `squeue -u fb31` is empty.
2. For each of the 8 rows: `remote_pack.sh delete <folder> <sha>`; record rc and the DELETED line; the folder must no longer exist.
3. `rmdir` the two empty results parents.
4. Print the remaining `results/`, `logs/` and `upload/` entries for these run IDs (must be none).

The script stops at the first failure.
