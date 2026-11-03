# Independent completion review: BENCH_F3_PROD

**Verdict: ACCEPT WITH FIXES.** The production results and recorded acceptance checks pass. Correct findings 1 and 2 in the completion report before declaring the documentation closed. No blocking result, accounting, transfer, or cleanup defect was found.

Reviewed 2026-11-03, offline. No server connection, job submission, benchmark execution, or full payload rehash. Only this review file was written. Local arithmetic and bounded hash checks used the pulled evidence requested by Felipe. References below are relative to CAMP unless prefixed `DATA`, which means `<PC_NOTS_DATA>\New_Campaign`; `RUN` means `20261102T1252Z_bench_f3v2_prod`.

## Findings

1. **should-fix — qualify the cell-4 incident's cause.** Report section 1 says the first cell-4 gate's guard refused at approximately 9.70 GiB as an established fact. The original failure log preserves only `CalledProcessError` from gate.sh, exit 1, and `launch_rc=1`; it does not preserve that invocation's guard output. OPS_LOG's 21:26:15Z entry correctly calls guard refusal the “near-certain cause,” inferred from the 21:08Z home measurement and gate ordering. The successful standalone gate after D79 is consistent with this diagnosis but cannot prove the earlier failure's cause. Say “gate.sh failed before submission; disk-guard refusal is the strongly supported diagnosis (original gate output unavailable).” The cell-1 refusal is directly evidenced at 17:28:19Z, in `cell1_attempt2_guardrefused`, whereas `cell1_attempt1` was a pull-chain prerequisite stop. Label it “first staging attempt” if retaining “first attempt.” References: `ops/F3PROD_COMPLETION_20261103.md` section 1; `ops/evidence/ops8_f3prod_cell4_attempt1_gatefail.txt`; `ops/OPS_LOG.md` 21:26:15Z and 21:49:30Z entries; `ops/evidence/ops8_f3prod_cell1_attempt{1,2_guardrefused,3_eraserefused}.txt`.

2. **should-fix — distinguish deletion start from confirmed completion.** Section 3's “deleted 23:49Z / 23:55Z / 00:01Z / 00:04Z” values are the timestamps printed immediately before each helper invocation, not timestamped completion receipts. For example, p0500 starts 23:49:50Z and its untimestamped successful return precedes the next start at 23:55:56Z. Rename these as deletion-start times, or report the overall confirmed completion at `2026-11-03T00:04:27Z`. The successful per-folder return codes, absence checks, parent removals and final empty enumeration do establish completed cleanup. References: report section 3; `ops/evidence/ops8_f3_delete.txt`; `ops/scaffold/f3_delete_remote_v2.sh` final deletion loop; `ops/CLEANUP_LOG.md` 00:04:27Z entry.

3. **note — all acceptance counts, accounting and timing tie out.** Four jobs, exactly four unique primary cells in jobs.tsv: 2503200, 2504013, 2507545, 2509541. Each raw sacct file has 600 distinct top-level task records, all COMPLETED / exit 0:0; their combined indices equal exactly 1..2400. Step records were excluded from cost sums. Reconciliation has exactly the expected 2,400 distinct case names, all valid, six ok statuses each (14,400 total), `unexpected=0`, and 2,400 R validator `VALID` messages. Recorded reconciliation rc=0 supports the schema/source/support checks required by JOB.md; this review did not reload every RDS. No failed or missing unit was dropped. References: `DATA/logs/RUN/{jobs.tsv,sacct_*.txt,reconcile.txt,accounting.tsv,timing.tsv}`; `ops/evidence/ops8_f3prod_collect.txt`; JOB.md “Terminal accounting, retry and acceptance.” Independent arithmetic is recorded below.

4. **note — sequential submission, retry disposition and false stop are supported.** Arrays and IDs match the report. Submission confirmations are 18:11:00Z, 19:11:22Z, 20:22:21Z and 21:49:30Z; monitor terminal confirmations are 18:51:42Z, 20:03:48Z, 21:02:31Z and 22:40:03Z. Previous cells were terminal with queued=0 before the next launch. CPU ceiling and dry-run rc=0 are recorded for every successful launch; resources_used.json records 30 minutes / 2 GiB for every cell. Both dry-run attempts show COMPLETED=600 and zero timeout selections in all four cells. Thus no retry submission was warranted; the omitted non-dry-run retry command would have had no selected work. No retry intent or extra jobs.tsv row exists. The 22:45Z wrapper's DISPOSITION_NEEDED / rc=4 contradicts its own all-COMPLETED output, and is honestly identified as an OPS regex false stop; the corrected collection returns zero. Failed gates occur before sbatch/intent creation in launch.py. Nothing in the saved evidence indicates double submission. References: `ops/evidence/ops8_f3prod_cell{1,2,3,4}.txt`, `ops8_f3prod_cell{1,2,3,4}_monitor.log`, `ops8_f3prod_cells_chain.txt`, `ops8_f3prod_collect_run1_regexbug.txt`, `ops8_f3prod_collect.txt`; pulled upload `runner/launch.py` and logs' four primary intents.

5. **note — download/verify/delete chain and retained artifacts satisfy the specification.** All four VERIFIED production receipts precede deletion (last verification 23:37:15Z). Bundle verification rc=0 for both results folders and logs is saved in the collection-chain evidence; upload uses its transfer authority as JOB.md specifies. The deletion review R2 accepts v2; its literal production path/hash arguments agree with the receipts. Runtime evidence records the D79 scan (49 processes, 10 tolerated helpers, zero references/incomplete), successful helper returns for all eight reviewed dev/prod targets, both parent removals, and final empty enumeration / rc=0. The process scan retains the accepted same-node/helper limitations disclosed in the deletion review; it is not an unrestricted proof about every NFS client. Logs preserve raw sacct, retry dry run, reconciliation, cost, timing, resources, intents, gate/squeue snapshots, 2,400 Slurm logs and 2,400 timing files. Upload preserves the immutable source/runner snapshot. No separate production sizing.tsv or config folder is required by JOB.md/HQ D64. No additional required run artifact was found missing. References: `ops/evidence/ops8_f3prod_{collect_chain,pulls}.txt`, `ops8_f3_delete.txt`; `review/SOL_REVIEW_F3_DELETION_20261102.md` R2; `ops/scaffold/f3_delete_remote_v2.sh`; `ops/CLEANUP_LOG.md`; `ops/transfer/receipts/*RUN*.verify.json`.

6. **note — clarify manifest-member versus transferred-file counts.** The report's 4,800 / 4,800 / 4,822 numbers count bundle-manifest members, excluding MANIFEST.sha256 itself. Actual local/transfer totals are 4,801 / 4,801 / 4,823; upload is 35. All memberships match, with no missing member and only MANIFEST.sha256 outside each bundle's member list. Consider labelling the table column accordingly. All three full bundle-manifest digests match the report and collection evidence. References: report section 3; `DATA/{results/RUN/p0500,results/RUN/p1000,logs/RUN}/MANIFEST.sha256`; `ops/evidence/ops8_f3prod_pulls.txt`.

## Independent numerical tie-out

Raw sacct arithmetic, ordered as in the report:

| Cell | Tasks | Elapsed core-h | Allocated CPU-h |
|---|---:|---:|---:|
| p0500_c100 | 600 | 15.0736111111 | 30.1472222222 |
| p0500_c050 | 600 | 22.9563888889 | 45.9127777778 |
| p1000_c100 | 600 | 14.1822222222 | 28.3644444444 |
| p1000_c050 | 600 | 19.7655555556 | 39.5311111111 |
| Total | 2400 | 71.9777777778 | 143.9555555556 |

These round to every reported cost value. The 66.6 / approximately 133 pilot forecast is documented in JOB.md; it is an estimate, not an acceptance ceiling.

Recomputed from all 2,400 timing.tsv observations (600 per cell, all attempt=1); p95 is sorted observation 570:

| Cell | Mean wall s | p95 wall s | Max wall s | Max RSS KiB |
|---|---:|---:|---:|---:|
| p0500_c100 | 86.4408667 | 143.87 | 207.37 | 289420 |
| p0500_c050 | 133.5290833 | 225.16 | 360.00 | 288700 |
| p1000_c100 | 80.6884333 | 137.09 | 229.54 | 296468 |
| p1000_c050 | 114.9390333 | 197.48 | 321.33 | 296600 |

All report table entries round correctly. Maximum wall is exactly 20% of 1,800 s; maximum RSS is 0.28286 GiB, consistent with the stated <=0.29 GiB.

## Bounded integrity checks

- Independently hashed all three production bundle manifests: p0500 `e2600c82887fc176f129ca7a0ae33831da311aff4b062ad890201e711b5a06b9`; p1000 `6b61c4b2257bf71bc59f3a8f6e499e9ab2c90cc724e7904f43c12ec0915f6a8e`; logs `5c96e7f65086c99b3c81536f1bfbf93845054415c486307f4bb8cb45b949f7da`.
- Enumerated complete local file membership, without rehashing all payloads. Spot hashes passed for six distinct members per results folder (first case's CSV/done/RDS/sha256, midpoint CSV, last sha256) and eleven log members (accounting, jobs, reconciliation, resources, retry dry run, four raw sacct files, timing.tsv, and midpoint Slurm output).
- Read all four production VERIFIED receipts: no mismatches, missing members, skipped members or symlinks. Their transfer hashes are `344d2713…4137`, `d13f0dd3…7381`, `4f69ac32…d1e5`, `17cb83e6…b3fd`, matching pulls and reviewed delete arguments. These are distinct from the bundle manifests.
- The FINAL ledger has 63 entries and independently hashes to `90579ad6a592916f2a87e5be614a468901884610421ab0c4809ae86666875e07`. The pulled upload's UPLOAD_SHA256.txt hashes to `b7d0e36bec8ada2fd991e706da8b895a2bd2a579d9f64aaa4916355284b15424`. freeze.json records manifest `8905f52e…0373` and source `3e01c77b…f42c`, agreeing with prepare/collection evidence. This is a bounded completion review, not a fresh verification of every source-ledger or payload entry.

Closure remaining: correct the two report statements above and attach this independent tie-out. No rerun, retry or additional deletion is indicated by the inspected evidence.
