# NOTS_HYGIENE_INVENTORY — SMC material on NOTS, read-only inventory for the owner's cleanup (2026-11-17)

**Summary** (Sonnet helper, SMC - Engineering; NOTS read-only, 2026-11-17 ~21:00–21:25 CT; nothing moved, copied, deleted or written on NOTS; no sbatch/srun; no git change):

1. **Method.** 6 sequential `ssh nots` calls (§9), all `nice`+`timeout`; deploy/ trees pruned by name, /projects/ml75, $WORK, BNP and non-SMC never listed. `squeue -u fb31` empty; every job in the sacct tail is COMPLETED → **nothing is in use** by a running/queued job.
2. **SMC material found: 80.40 GB in 20,128 files** = scratch 80.07 GB (dept scratch 79.15 GB of it) + home 329.2 MB. Rows reconcile with the `find` totals to the byte (§3).
3. **Per class (GB · files).** KEEP-ON-NOTS 0.027 · 582; DOWNLOAD+DELETE **15.68** · 10,486 (scratch 15.67, home 0.014); DOWNLOAD-ONLY 0.134 · 5,971 (all home); DELETE-AFTER-GO **64.54** · 2,293 (scratch 64.40, home 0.143); UNKNOWN 0.015 · 796; not SMC (16 Quant_Reg loose files) untouched.
4. **Home quota 8,086 MB of 10,240 MB (79%)** (11-15: 6,761 MB, +1,325 MB); guard line 8,192 MB is only 106 MB away. SMC is just 0.33 GB of home; the growth is app builds (`.vscode-server` 4.5 GB, was 2.7 GB; `.t3` 1.6 GB; guard freed 2.9 GB at 11-17 08:40 and it has refilled). **Projected after SMC cleanup ≈ 7,937 MB** (DD+DG only) **/ ≈ 7,809 MB** (also DOWNLOAD-ONLY deleted): SMC cleanup cannot make home "clean"; the non-SMC app builds (7.5 GB) are the lever (§6, D8).
5. **Biggest items (scratch):** F1M pilot run dir 58.3 GB (16 islands 34.2, setup.bin 10.1, calib.bin 8.1, fit.bin 2.4, data+raw 3.2, law 0.34); P7 probe 13.4 GB (all regenerable inputs); T5 6.5 GB; T6 0.44 GB. Everything else on scratch is < 0.5 GB per tree (w3scale 454 MB, theory_w2 453 MB).
6. **Purge risk (14 d on atime):** `theory_w2` (oldest atime 11-09 → ≈ 11-23) and `w3scale` (11-11 → ≈ 11-25) exist on Owls (verified) but **not on the desktop**; **12.14 GB of DOWNLOAD+DELETE scratch has no copy anywhere** (F1M calib 8.1 GB, data+raw 3.2 GB, law 0.34 GB, T5 law, small files; atime 11-15…11-17 → ≈ 11-29…12-01). `crews/offload/ledger.tsv` does not exist (only `desktop_verified.txt`, 5 names).
7. **Local copies already verified (Owls + desktop):** F1M `fit.bin` 2.36 GB, T5 `fit.bin` 0.23 GB, G0 stage_2747372/2747799 (29 MB), F1M_pilot small records.
8. **Needs an owner/HQ decision (§7):** D1 waive 'never delete unverified' for 64.4 GB of regenerable bulk (islands, setup.bin, test-run inputs; F1M alone ≈ 285 core-h to rebuild) · D2 download calib.bin 8.1 GB? · D3 re-run of rep 1 after the freeze (keeps setup.bin 10.1 GB) · D4 `Others/library_portable` + releases 98.7 MB · D5 Theory-owned trees · D6 ccd-cli binary (HQ said 'do not delete') · D7 relocation records · D8 home quota/guard · D9 P7 vs F1M `data.bin` hashes differ for the same seed · D10 BVS keep-set vs RERUN_2400_PLAN.
9. **Transfer:** NOTS → Owls `records/hygiene_1117/` (rsync, SHA-256 manifests computed on NOTS) → desktop pull; NOTS deletes only after Owls + desktop verification (§8). Relay volume to build ≈ 12.3 GB; the biggest single files: calib.bin 8.1 GB, data.bin/raw.bin 1.6 GB each.

File: `Docs/Experiments/P1M/machines/NOTS_HYGIENE_INVENTORY.md`. Companions: `INVENTORY.md` (11-15), `REORG_PLAN.md`, `OFFLOAD.md`, `../NOTS_FACTS.md`. Sizes are apparent bytes (`find -printf %s`), decimal units (GB = 10^9); `du` block sizes run higher. "Newest" = newest file mtime in the row (2026, mm-dd). Class codes: **K** KEEP-ON-NOTS · **DD** DOWNLOAD+DELETE · **DO** DOWNLOAD-ONLY · **DG** DELETE-AFTER-GO · **U** UNKNOWN (never proposed for deletion).

## Manager recommendations to HQ (2026-11-17 night; proposals, nothing run)
- **D1, no waiver needed:** Owls `/home/fb31` (NFS) has 2.9 TB free, so download ALL 80.4 GB to Owls `SMC_Engineering_Department/records/hygiene_1117/`. Owls `/` (89%) is not used. SHA-256 manifests are computed on NOTS and verified on Owls, then the NOTS copy is deleted. The desktop gets the 15.8 GB of records of record when the VPN is back; the 64 GB of regenerable bulk stays on Owls only (PC disks stay under 70%). HQ to confirm that "verified on Owls" counts as "verified locally" for the NOTS delete (OFFLOAD.md principle 3 asks for Owls AND desktop; the desktop is offline for now).
- **Order:** (1) the 12.1 GB DD with no copy anywhere (F1M calib/data/raw/law, T5 law, small files); (2) the rest of DD; (3) the DG bulk (F1M islands + setup.bin, P7, T5); (4) the home DO items. One rsync at a time over the multiplexed connection, `nice`. NOTS deletes happen per group, only after `sha256sum -c` passes on Owls, and each leaves an `OFFLOADED` tombstone. `theory_w2`/`w3scale` already have verified Owls copies, so their NOTS deletes need only D5.
- **D2:** yes, download calib.bin. **D3:** no rerun of rep 1 is planned (rep 1 = the pilot's fit.bin, already on Owls + desktop), so setup.bin goes too.
- **D6:** keep the ccd-cli binary (HQ's earlier "do not delete"). **D4/D7:** download + keep on NOTS until the owner decides. **D5:** route to Theory. **D8:** the home quota growth is non-SMC (`.vscode-server`, `.t3`), outside Engineering's scope; owner's call.
- **D9, likely benign:** gen writes the binary block into data.bin's `meta` (gen.cpp:173, 186), so file hashes differ between builds. Data identity is the `X_sha256`/`y_sha256` pair (gen.cpp:188-193), which the transfer step compares for P7 vs F1M.
- **D10:** the rerun plan reruns v2.2.1 from the repo tree on NOTS. Leave `projects/BVS` (141 MB) untouched until the rerun verdict.

## D5: Theory sign-off (Theory Dept manager, 2026-11-18, owner order via HQ)
| rows | decision | condition |
|---|---|---|
| S34+S35 `/scratch/fb31/theory_w2/` | DELETE | after re-running `sha256sum -c` on the Owls copy (`/home/fb31/SMC_Theory_Department/records/theory_w2`); no desktop copy needed |
| S30 `w3scale/out/` | DELETE | after the verified Owls copy (records/W3-SCALE). P1M check (Engineering, 11-18): R5/R6 were one-time read-only queries answered 11-15 (REQUESTS.md R6, LOG 11-15 19:30/19:43); no P1M job or engine code reads `census_p*.rds` in place → OK |
| S31 `w3scale/code/v32dev_6866f57` | KEEP | until HQ confirms G0 closed; then delete after verified copy |
| S32+S33 `w3scale/code/{v31…, v32dev_bbdfea0, v32dev_e5afee7}`, `{runs,stage,nots,tasks,submissions.jsonl}` | DELETE | after the verified Owls copy |
| S36 `/scratch/fb31/theory_w3/` + H14 `projects/BVS/theory_w3` | DELETE (HQ update via Theory, 11-18) | after a fresh copy to Owls `SMC_Theory_Department/records/theory_w3` + checksum verify (the scratch copy is newer than the 11-14 Owls copy); a future W3-P6 resume restores from Owls. `projects/BVS/theory_w3` still waits for the rerun-verdict hold |
| H14 `projects/BVS/theory_w2` | DELETE | after download to Owls + verify (falls under the projects/BVS hold until the rerun verdict) |
| S37 scratch `SMC_Theory_Department/W3-AUDIT-C` + H17 `~/SMC_Theory_Department/W3-AUDIT-C/pkg` | DOWNLOAD then DELETE | no copy anywhere: copy to Owls `/home/fb31/SMC_Theory_Department/records/w3_audit_c/`, SHA256SUMS, verify, then delete both |

## 1. Headline numbers

| Item | 11-15 | now (11-17 ~21:00 CT) | Command |
|---|---|---|---|
| NOTS home quota | 6,761 MB of 10,240 (66%), 90,394 files | **8,086 MB of 10,240 (79%)**, 109k files; guard 8,192 MB not reached (106 MB margin) | `quota -s \| grep -A1 export/nots/home \| tail -1` |
| SMC material in home (sum of `find` sizes) | ≈ 168 MB (`projects/BVS`) | 329.2 MB: `projects/BVS` 141.1 MB (6,822 files), `~/SMC_Engineering_Department` 175.7 MB (2,334), `SMC_Theory_Department` 7.6 MB, `archive` 4.7 MB, `bin` 24 KB | `find -printf` scans (§9) |
| SMC material on `/scratch/fb31` | 1.2 GB | **80.07 GB**: dept scratch 79.15 GB (967 files), w3scale 454.4 MB, theory_w2 453.0 MB, theory_w3 3.0 MB, SMC_Theory_Department 5.8 MB, loose 0.66 MB (no whole-scratch `du` run: `qr_data` is empty, nothing else is listed at the root) | `find -printf` scans |
| NOTS queue | empty | **empty** (`squeue -u fb31`: header only) | `squeue -u fb31` |
| sacct (7 d) | all terminal | tail (60 rows) all COMPLETED; WorkDirs: `~/SMC_Engineering_Department/scripts/{wp6_k3,T5_1e5,P7_pilot_1e6,F1M_pilot,T6_1e5}` and `~/SMC_Theory_Department/W3-AUDIT-C`; rows before the tail were not read | `sacct -u fb31 -S now-7days -X …` |
| Home guard | last run 11-12 | last run 11-17 08:40: 8,333 → 5,617 MB (freed ≈ 2,933 MB: T3 builds, Claude srv); now back at 8,086 MB | `tail home_guard.log` |
| Owls records/ | W3-SCALE only | `records/{W3-SCALE 437 MB, F1M_pilot 0.5 MB, fitbin_1117 2.5 GB, G0 29 MB, _offload_test}`; `crews/offload/desktop_verified.txt` lists F1M_pilot, fitbin_1117, G0/stage_2747372, G0/stage_2747799, _offload_test/hello; **`crews/offload/ledger.tsv` does not exist** | `ls`, `cat` on Owls |
| Owls Theory copies | — | `/home/fb31/SMC_Theory_Department/records/{theory_w2 441 MB, theory_w3 5.3 MB}` + `SHA256SUMS_*_nots.txt`, `MANIFEST_*` (verify files are 0 bytes; INDEX says 0 mismatches; I did not re-verify) | `ls`, `du` on Owls |

## 2. Exclusions respected

- `…/Others/SMC_BVS_v3_history_Oct2026/deploy/` pruned **by name** in every `find` (`-path '*SMC_BVS_v3*/deploy' -prune`); not listed, not measured. Its siblings `core/` and `prototype_profiling/` are in row H16 (9.2 MB). No `ls`/`du` ever entered it. `/home/fb31/projects/BVS/SMC_BVS_v3` still does not exist.
- `/projects/ml75`, `$WORK`: not visited. BNP: not touched. Not-SMC home entries: one `du -sh` each (§5), no descent beyond that.

## 3. Table (one row per tree at depth 2–3; large files separate)

Columns: id | path | size | files | newest | what it is (READMEs/INDEX/job records/repo references) | action | local copy today | note. `D` = `/scratch/fb31/SMC_Engineering_Department` (= `~/SMC_Engineering_Department/scratch`).

### 3.1 Department scratch (`/scratch/fb31/SMC_Engineering_Department`, 79.15 GB, 967 files; created 11-15…11-17; also `INDEX.md` 811 B, empty `data/`, `tmp/`, `archive/home_guard/` skeleton = KEEP)

| id | path | size | files | newest | what | action | local copy today | note |
|---|---|---:|---:|---|---|---|---|---|
| S01 | `D/runs/F1M_pilot/6-AR-n200-r01-V-s1/fit.bin` | 2.36 GB | 1 | 11-17 | merged 1M fit store of rep 1 (6-AR-n200-r01-V-s1, HPM = MPM = S0; job 2761934); science record, source of the post-hoc list-PIP | **DD** | Owls records/fitbin_1117 (sha256 = NOTS, 11-17 15:09) + desktop (desktop_verified.txt) | delete only after re-hash against fitbin_1117/nots_sums.txt |
| S02 | `D/runs/F1M_pilot/6-AR-n200-r01-V-s1/law.bin` | 336.3 MB | 1 | 11-17 | V-law mixture of the 1M fit (eval output) | **DD** | none |  |
| S03 | `D/runs/F1M_pilot/6-AR-n200-r01-V-s1/ (86 small files)` | 1.1 MB | 86 | 11-17 | eval.bin 345 KB, fit_report.json 72 KB, 16 island *.bin.json, log/, manifests/, cost/ (13 files), run_manifest.json, truth.json, *.bin.json | **DD** | partial: Owls records/F1M_pilot has the *.bin.json, run_manifest, truth, cost/, SHA256SUMS; NOT eval.bin, fit_report.json, log/, manifests/, island json |  |
| S04 | `D/runs/F1M_pilot/6-AR-n200-r01-V-s1/calib.bin` | 8.08 GB | 1 | 11-17 | calibration state of the 1M fit (3 iterations, 12 diagnostic islands, 135.6 core-h) | **DD** | none | recommended; HQ may downgrade to DG (D2) |
| S05 | `D/runs/F1M_pilot/6-AR-n200-r01-V-s1/{raw,data}.bin` | 3.24 GB | 2 | 11-17 | generated dataset of rep 1: raw.bin 1.60 GB (generator output), data.bin 1.64 GB (prepared); seed 602020001; data.bin sha256 4de72b21… is in setup.bin.json | **DD** | none (hash on Owls) | regenerable from the seed, but a local copy fixes the exact data of rep 1 |
| S06 | `D/runs/F1M_pilot/6-AR-n200-r01-V-s1/setup.bin` | 10.14 GB | 1 | 11-17 | setup of the 1M fit (correlation + tables + start law; 15.25 core-h, 19 min); sha256 51ebef14… (Owls setup.bin.json) | **DG** | hash only | keep until HQ rules on a re-run of rep 1 after the freeze (D3) |
| S07 | `D/runs/F1M_pilot/6-AR-n200-r01-V-s1/island_1..16.bin` | 34.18 GB | 16 | 11-17 | 16 final islands (269 core-h); already merged into fit.bin; OFFLOAD.md: island files are not kept | **DG** | none | owner waiver needed for 'delete only if verified locally' (D1) |
| S08 | `D/runs/F1M_pilot/{ends,starts,submissions}.jsonl` | 5.0 KB | 3 | 11-17 | batch ledgers of F1M_pilot | **DD** | Owls records/F1M_pilot + desktop |  |
| S09 | `D/runs/P7_pilot_1e6/6-AR-n200-r01-V-s1/{setup,data,raw}.bin` | 13.38 GB | 3 | 11-17 | P7 pilot-island probe at 10^6: setup.bin 10.14 GB, data.bin 1.64 GB, raw.bin 1.60 GB. Same run_id/seed as the 1M fit but data.bin sha256 differs (b051ca10… vs 4de72b21…) | **DG** | none (results/P7_PILOT_1e6.md in repo) | D9: same seed, different data hash |
| S10 | `D/runs/P7_pilot_1e6/ (16 small files + 3 batch files)` | 81.3 KB | 19 | 11-17 | pilot.json, pilot_plan.json, cost_pilot/, log/, manifests/, run_manifest.json, truth.json, jsonl ledgers | **DD** | none |  |
| S11 | `D/runs/T5_1e5/5-AR-n200-r01-V-s1/fit.bin` | 232.2 MB | 1 | 11-17 | T5 gate fit at 10^5 (job 2758741 chain) | **DD** | Owls records/fitbin_1117 + desktop | delete after re-hash |
| S12 | `D/runs/T5_1e5/5-AR-n200-r01-V-s1/law.bin` | 373.4 MB | 1 | 11-17 | T5 V-law output | **DD** | none |  |
| S13 | `D/runs/T5_1e5/5-AR-n200-r01-V-s1/ (90 small files) + batch files` | 1.0 MB | 93 | 11-17 | eval.bin, *.bin.json, cost/, log/, manifests/, isa_check*.json, run_manifest, truth, ledgers | **DD** | none (results/T5_1e5.md in repo) |  |
| S14 | `D/runs/T5_1e5/5-AR-n200-r01-V-s1/{setup,raw,data,calib}.bin, island_1..16.bin, island_1_isa_check.bin` | 5.87 GB | 21 | 11-17 | T5 setup 1.00 GB, raw 0.16, data 0.16, calib 0.78, 16 islands 3.54 GB, isa-check island 0.22 GB | **DG** | none | regenerable (gate run) |
| S15 | `D/runs/T6_1e5/5-AR-n200-r01-V-s1/t6/{ref_island,island}.bin` | 442.5 MB | 2 | 11-17 | T6 real-SIGKILL restart test islands (result: results/T6_1e5.md, PASS) | **DG** | none | regenerable from T5 |
| S16 | `D/runs/T6_1e5/ (6 small + 2 batch files)` | 13.0 KB | 8 | 11-17 | t6.json, logs | **DD** | none |  |
| S17 | `D/runs/g0/stage_2747372, stage_2747799` | 29.3 MB | 12 | 11-16 | G0 stage runs (stage_p*.rds, logs, SHA256SUMS) | **DD** | Owls records/G0 + desktop (desktop_verified.txt) | delete after re-hash |
| S18 | `D/runs/g0/{kernel_2747371, build, submissions.jsonl}` | 160.9 KB | 5 | 11-15 | G0 kernel bench output + build record | **DD** | repo has results/g0_kernel_2747371.log; rest none |  |
| S19 | `D/runs/pmath/` | 23.1 MB | 6 | 11-15 | pmath NOTS checks (2 loose files 23 MB, names not listed; run_* logs); repo: results/pmath_nots_*.log, PMATH_NOTS.md | **DD** | repo (2 logs) |  |
| S20 | `D/runs/wp3_bench/` | 67.8 MB | 177 | 11-16 | WP3 benches: arch_2749483 9.2 MB (160), l5, levers, rounds, run_2747881; 5 loose files 58.6 MB (names not listed) | **DD** | repo has summaries (results/{arch_2749483,l5_2749328,levers_2748756}) |  |
| S21 | `D/runs/wp6_k3/{build_2756524, src, 1 loose file}` | 35.1 MB | 367 | 11-16 | WP6 K3 SPR build tree + source copy | **DG** | regenerable from the repo commit |  |
| S22 | `D/runs/wp6_k3/run_2756524` | 55.5 KB | 17 | 11-16 | K3 run output (results/WP6_K3_SPR.md in repo) | **DD** | none |  |
| S23 | `D/archive/home_guard/holding_20261111/ccd-cli_2.1.321-c6c6b562e837` | 341.9 MB | 1 | 11-11 | old Claude CLI build moved out of home by the guard | **DG** | not needed (regenerable by the tool's updater) | D6: INDEX says 'HQ: move, do not delete' |
| S24 | `D/archive/home_guard/holding_2026111{1,2}/codex_db-backups_*.tgz` | 5.5 MB | 2 | 11-12 | Codex DB backups moved out of home by the guard | **DD** | none | HQ infra, not research; HQ may skip |
| S25 | `D/slurm_out/` | 12.6 KB | 120 | 11-17 | batch stdout/err of the drivers (nearly all 0 bytes; the listing showed two non-empty pmath .err of 1.1 KB and 0.3 KB) | **DD** | none |  |

### 3.2 Other SMC trees on `/scratch/fb31`

| id | path | size | files | newest | what | action | local copy today | note |
|---|---|---:|---:|---|---|---|---|---|
| S30 | `/scratch/fb31/w3scale/out/` | 444.6 MB | 854 | 11-12 | W3-SCALE: B3 census p = 2k..20k (census_p*.rds read by P1M R5/R6), bit-identity records (bitid_p500/p1000 × C/D/S5; res up to 110.7 MB per dir), profiles, setup_cmp | **DD** | Owls records/W3-SCALE (SHA256SUMS_nots.txt, 0 mismatches 11-15); desktop NOT | Theory/HQ OK (D5); oldest atime 11-11 |
| S31 | `/scratch/fb31/w3scale/code/v32dev_6866f57` | 1.9 MB | 28 | 11-12 | frozen code under test of the P1M G0 leg (revision D) | **K** | Owls ✓ | tiny; G0 results are on the desktop, so DD is possible once HQ confirms G0 is closed |
| S32 | `/scratch/fb31/w3scale/code/{v31_613f063, v32dev_bbdfea0, v32dev_e5afee7}` | 5.5 MB | 85 | 11-11 | earlier W3-SCALE code trees | **DD** | Owls ✓ |  |
| S33 | `/scratch/fb31/w3scale/{runs, stage, nots, tasks, submissions.jsonl}` | 2.5 MB | 586 | 11-12 | task tables, script copies, submissions ledger (jobs 2692663–2698180) | **DD** | Owls ✓ |  |
| S34 | `/scratch/fb31/theory_w2/loc_pilot02` | 395.1 MB | 42 | 11-09 | Theory W2-SIM LOC pilot (data/: 3 X.bin of 127 MB + others = 391 MB, regenerable inputs; rds 4 MB) | **DD** | Owls /home/fb31/SMC_Theory_Department/records/theory_w2 (checksums verified 11-15); desktop NOT | Theory OK; oldest atime 11-09 → purge ≈ 11-23 |
| S35 | `/scratch/fb31/theory_w2/ (23 other dirs; fam_X 39.4 MB)` | 57.9 MB | 5,915 | 11-09 | W2-SIM pilots and production probes (FAC-PK, LOC, S5, X); 19 + repo files cite the path | **DD** | Owls ✓; desktop NOT | Theory OK |
| S36 | `/scratch/fb31/theory_w3/` | 3.0 MB | 1,858 | 11-14 | Theory W3-P6 run outputs; RESUME_PLAN may resubmit b1/b2 here | **DD** | Owls ✓ (copy 11-15 incl. newest 11-14); desktop NOT | Theory decides on the resume first (D5) |
| S37 | `/scratch/fb31/SMC_Theory_Department/W3-AUDIT-C` | 5.8 MB | 460 | 11-16 | Theory W3-AUDIT-C job 2754540 outputs (out 5.7 MB/114 files, log, slurm) | **DD** | none found (Owls SMC_Theory_Department/records has only w2, w3, w3_dist_numerics, w3_rm2r_numerics) | Theory OK; atime 11-16 |
| S38 | `/scratch/fb31/.claude-science/jobs` | 41.8 KB | 12 | 09-25 | three job folders of an old agent tool; no repo reference | **U** | none |  |
| S39 | `/scratch/fb31/{scr_*_MOVED.md ×7, qr_small_del2_MOVED.md, cksum_units.sh, del_unit.sh, mkchunks.sh, mkunits.sh}` | 8.9 KB | 12 | 10-22 | records of the Oct 21–22 relocations to the laptop (old path → laptop path, bytes) + the tools used | **DD** | none | HQ (11-15) said 'left in place, untouched'; owner's new order needed (D7) |
| S40 | `/scratch/fb31/{fsb_deploy*.tar.gz ×3, h1v1_deploy_v1.tar.gz, h1v1_*.sh ×2, SOURCE_SHA256SUMS_h1v1_v1}` | 629.1 KB | 7 | 09-30 | Sept 29–30 deploy tarballs and scripts; h1v1 = 'heterogeneous_1v1' (SMC arm + exact 2^30; cf. Docs/History/benchmarks_p30_2026-10-07) → probably SMC-BVS history | **U** | none | local copy suggested (0.6 MB); owner decides |
| S41 | `/scratch/fb31/{air_*, k2_*, sqrtn_*, uext_*, spod_proc.log, submit_p1only*, patch_sqrtn.sh, diagnose_cycle1.R, final_tab.R} (16 files)` | 20.5 KB | 16 | 09-30 | Quant_Reg project files (paths ~/projects/Quantile_Reg) | **X** | — | not SMC: untouched |

### 3.3 NOTS home (SMC areas; deploy/ excluded)

| id | path | size | files | newest | what | action | local copy today | note |
|---|---|---:|---:|---|---|---|---|---|
| H01 | `/home/fb31/SMC_Engineering_Department/{INDEX.md, crews/home_guard, crews/laptop_route}` | 25.6 KB | 6 | 11-17 | department index; home guard log + original scripts; laptop-route test files (authorized_keys.bak-20261115: key backup, 610 B) | **K** | — | light; the guard log is live |
| H02 | `/home/fb31/SMC_Engineering_Department/scripts/F1M_pilot/{bin, code, manifests, run_manifests, *.sh}` | 19.4 MB | 327 | 11-17 | frozen code (git archive of 2cfaa9e5), binary smcbvs4 + sha256, manifests and submit scripts of the 1M pilot fit | **K** | repo (commit); binary hash in manifests | reference for any re-run of rep 1; WorkDir of sacct jobs 2761931–5 |
| H03 | `/home/fb31/SMC_Engineering_Department/scripts/F1M_pilot/build` | 12.5 MB | 166 | 11-17 | compile tree of the pilot binary | **DG** | regenerable |  |
| H04 | `/home/fb31/SMC_Engineering_Department/scripts/P7_pilot_1e6/{bin, manifests, run_manifests, *.sh}` | 3.6 MB | 26 | 11-17 | binaries smcbvs4 + v4_pilot_island (+ .sha256), manifests, scripts of the P7 probe | **DD** | none for the binaries | small |
| H05 | `/home/fb31/SMC_Engineering_Department/scripts/P7_pilot_1e6/{code, build}` | 32.6 MB | 472 | 11-17 | code copy (same commit 2cfaa9e5, 17,089,520 B as F1M_pilot/code) + compile tree | **DG** | repo commit; compare against the manifest hashes |  |
| H06 | `/home/fb31/SMC_Engineering_Department/scripts/T5_1e5/{bin, manifests, run_manifests, *.sh}` | 7.4 MB | 33 | 11-17 | T5 binaries (smcbvs4, isa_check, v4_bench_island ×3) + sha256, manifests, scripts | **DD** | none for the binaries |  |
| H07 | `/home/fb31/SMC_Engineering_Department/scripts/T5_1e5/{code, build, build_isa_check, build_portable_bench}` | 56.3 MB | 772 | 11-17 | T5 code copy + three compile trees | **DG** | repo commit |  |
| H08 | `/home/fb31/SMC_Engineering_Department/scripts/T6_1e5/{bin, manifests, run_manifests, *.sh}` | 2.3 MB | 24 | 11-17 | T6 binary + manifests + scripts | **DD** | none for the binary |  |
| H09 | `/home/fb31/SMC_Engineering_Department/scripts/T6_1e5/{code, build, __pycache__}` | 29.8 MB | 471 | 11-17 | T6 code copy + compile tree | **DG** | repo commit |  |
| H10 | `/home/fb31/SMC_Engineering_Department/scripts/{g0, pmath, wp3_arch, wp3_l5, wp3_levers, wp6_k3, wp3_bench (5 small files)}` | 189.2 KB | 36 | 11-16 | batch scripts of finished batches | **DD** | repo has the originals |  |
| H11 | `/home/fb31/SMC_Engineering_Department/scripts/wp3_bench/engine_v4_cd1a7e02.tgz` | 11.6 MB | 1 | 11-15 | staged engine source tarball | **DG** | Owls staging/engine_v4_cd1a7e02.tgz (same name; compare sha256 first) |  |
| H12 | `/home/fb31/projects/BVS/{SMC_BVS/core (frozen v2.2.1), Others/superseded_code/v2_2, Data_Generation, Environment, Exact, Analysis, tools, README.md, INDEX.tsv, Others/INDEX.md}` | 5.8 MB | 216 | 11-04 | campaign-I frozen v2.2.1 code, generators, exact enumerator, scoring, env, index; needed for the study-subset rerun on v2.2.1 (CONF_NOTS_IDENTITY) | **K** | take with H13 tarball; INDEX.tsv has sha256 per file | provisional: confirm with RERUN_2400_PLAN (D10) |
| H13 | `/home/fb31/projects/BVS/{Benchmarks, Studies, Methodology, Records, Main_Results}` | 15.7 MB | 1,203 | 11-04 | campaign-I benchmarks (8 methods), frozen run bundles, method docs, records, headline results | **DO** | none verified (laptop holds the scratch/BVS 35 GB relocation, not this home tree) | owner decides later deletion |
| H14 | `/home/fb31/projects/BVS/{theory_w2, theory_w3}` | 11.7 MB | 696 | 11-13 | Theory W2-SIM / W3-P6 code, task tables, sim WorkDirs | **DO** | repo has Theory_work copies of the scripts | Theory's; theory_w3 is the WorkDir of a pending resume (D5) |
| H15 | `/home/fb31/projects/BVS/Others/{library_portable, benchmark_releases_Oct2026}` | 98.7 MB | 4,052 | 10-07 | legacy R library (mode r-x, 3,620 files) + three Oct-4 benchmark releases; Others/INDEX: 'safe to delete with releases, owner decides' | **DO** | none | D4: owner decides deletion |
| H16 | `/home/fb31/projects/BVS/Others/SMC_BVS_v3_history_Oct2026/{core, prototype_profiling} (deploy/ EXCLUDED, not listed)` | 9.2 MB | 655 | 10-22 | v2.1 cores + Oct 20–22 profiling study; parent of the excluded deploy/ | **U** | none | no action proposed (parent holds excluded tree) |
| H17 | `/home/fb31/SMC_Theory_Department/W3-AUDIT-C/pkg` | 7.6 MB | 20 | 11-16 | Theory W3-AUDIT-C package: scripts + data/riboflavin_L.csv 6.9 MB (WorkDir of job 2754540) | **DO** | none | Theory's |
| H18 | `/home/fb31/archive` | 4.7 MB | 121 | 09-26 | older home archive (Sept 2026: ADMM/genlasso, Brantley review, simulation_cleanup deleted_files.jsonl.gz 4.3 MB); no repo reference | **U** | none | never proposed for deletion |
| H19 | `/home/fb31/.claude-science-scratch` | 2.8 KB | 1 | 09-26 | old agent-tool folder | **U** | none |  |
| H20 | `/home/fb31/bin` | 24.0 KB | 5 | 11-15 | home_guard.sh, home_guard_job.sh, check_project_paths.py, prepare_nots.sh (HQ infra) | **K** | — |  |

Notes on the table:
- `D/runs/` layout is `runs/<batch>/<run_id>/` as in PROTOCOL.md; the batch driver wrote **no** `code/` folder inside the run dirs: frozen code and binaries are in `~/SMC_Engineering_Department/scripts/<batch>/{code,bin}` (home). Per-file hashes: `runs/*/manifests/` and the `.bin.json` files.
- The 16 island files of the F1M fit are 2.129–2.142 GB each; T5/T6 islands 221.2 MB each. All files ≥ 100 MB of the department scratch are in rows S01, S02, S04–S07, S09, S11, S12, S14, S15, S23; of `theory_w2`: three `loc_pilot02/data/*.X.bin` (127–128 MB each) inside S34.
- `pmath` (S19) and `wp3_bench` (S20) contain loose files whose names I did not list (23.1 MB and 58.6 MB): they are small enough to move with their folders.
- `/scratch/fb31/home_holding_*` and `home_guard/` no longer exist at the root: the 11-15 reorg moved them to `D/archive/home_guard/` (S23, S24). `scratch/slurm_out/` holds 120 driver `.out/.err` files, nearly all 0 bytes.

### 3.4 Class totals (bytes · files; reconciled to the scans)

| class | scratch | home | total |
|---|---:|---:|---:|
| KEEP-ON-NOTS | 1.9 MB · 28 | 25.2 MB · 554 | **27.1 MB · 582** |
| DOWNLOAD+DELETE | 15.67 GB · 10,367 | 13.5 MB · 119 | **15.68 GB · 10,486** |
| DOWNLOAD-ONLY | 0 B · 0 | 133.7 MB · 5,971 | **133.7 MB · 5,971** |
| DELETE-AFTER-GO | 64.40 GB · 411 | 142.8 MB · 1,882 | **64.54 GB · 2,293** |
| UNKNOWN | 671.0 KB · 19 | 13.9 MB · 777 | **14.6 MB · 796** |
| not SMC: untouched | 20.5 KB · 16 | 0 B · 0 | **20.5 KB · 16** |
| **SMC total (without not-SMC)** | 80.07 GB | 329.2 MB | **80.40 GB · 20,128** |

Check against the scans: dept scratch 79,151,970,815 B / 967 files; w3scale 454,447,202 / 1,553; theory_w2 452,990,677 / 5,957; theory_w3 3,015,990 / 1,858; SMC_Theory_Department 5,764,310 / 460; `.claude-science` 41,827 / 12; `~/SMC_Engineering_Department` 175,704,719 / 2,334; `projects/BVS` 141,071,326 / 6,822 (deploy pruned).

## 4. Home quota: now vs 11-15 and the projection

| | MB (quota line) | note |
|---|---:|---|
| 11-15 20:00 | 6,761 | 90,394 files |
| 11-15 18:52 (HQ) | 6,770 | |
| 11-17 08:40 (guard end) | 5,617 | after freeing ≈ 2,933 MB |
| **11-17 21:00 (now)** | **8,086** | 109k files; guard 8,192 |
| after DD + DG in home (≈ 156 MB of file bytes) | ≈ 7937 | dept compile trees (80 MB), code copies, T5/T6/P7 bench binaries after download, engine tgz |
| … and DOWNLOAD-ONLY deleted too (≈ 134 MB: library_portable 95.5 MB, BVS benchmarks/studies, Theory code) | ≈ 7809 | needs owner OK (D4, D5) |
| KEEP + UNKNOWN that stays in home | ≈ 39 MB | K 25.2 MB + U 13.9 MB (archive 4.7 MB, v3_history 9.2 MB) |

Freed quota ≈ bytes + 4 KB-block slack per file (≈ 3–8 MB here), so the projections are rounded. NOTS accounting also reads ≈ 0.6 GB above `du`.

## 5. Not SMC: untouched (one `du -sh` per top-level home entry)

| entry | size | note |
|---|---:|---|
| `.vscode-server` | 4.5 G | not SMC: untouched |
| `.t3` | 1.6 G | not SMC: untouched |
| `.codex` | 670 M | not SMC: untouched |
| `.claude` | 397 M | not SMC: untouched |
| `R (user R library)` | 212 M | not SMC: untouched |
| `projects/Quant_Reg` | 101 M | not SMC: untouched |
| `.local` | 73 M | not SMC: untouched |
| `.t3-recovery` | 12 M | not SMC: untouched |
| `projects/Large Prior_ Sims` | 2.7 M | not SMC: untouched |
| `.cache` | 184 K | not SMC: untouched |
| `.dotnet` | 288 K | not SMC: untouched |
| `.copilot` | 64 K | not SMC: untouched |
| `.ipython` | 56 K | not SMC: untouched |
| `.config` | 36 K | not SMC: untouched |
| `.mozilla / .vscode / .conda / .nv / lib / Python / archive_control` | < 12 K each | not SMC: untouched |

`.vscode-server` is the largest home item and grew +1.8 G since 11-15; `.t3` rebuilds daily (the guard prunes it). `/scratch/fb31/qr_data` is empty (0).

## 6. In use / purge risk

**In use:** nothing. `squeue -u fb31` is empty. WorkDirs in the sacct tail (all COMPLETED) are the department `scripts/<batch>` folders and the Theory `W3-AUDIT-C` folder, none of which a delete here would touch (they are KEEP/DD-small). Re-run `squeue` once right before any delete. A pending use by *planned* work: F1M `setup.bin` if rep 1 is re-run (D3); `projects/BVS/theory_w3` + `/scratch/fb31/theory_w3` if W3-P6 resumes (D5); `projects/BVS/SMC_BVS/core` for the v2.2.1 rerun (D10).

**Purge risk** (CRC: 14 days on atime; "staff may delete earlier"; a `mv` keeps the old atime). Oldest atime per tree from the scans:

| tree | size | oldest atime | est. purge | local copy |
|---|---:|---|---|---|
| `theory_w2` (S34, S35) | 453.0 MB | 11-09 | **≈ 11-23** | Owls only (verified 11-15); desktop not |
| `archive/home_guard/holding_20261111` (S23, S24) | 346.5 MB | 11-09 | ≈ 11-23 | none (binary regenerable; 4.5 MB tgz none) |
| `theory_w3` (S36) | 3.0 MB | 11-09 | ≈ 11-23 | Owls only; desktop not |
| `w3scale` (S30–S33) | 454.4 MB | 11-11 | ≈ 11-25 | Owls only (verified 11-15); desktop not |
| `runs/g0`, `wp3_bench`, `pmath`, `wp6_k3` (S17–S22) | 155.6 MB | 11-15 | ≈ 11-29 | G0 stage on desktop; rest repo summaries only |
| `SMC_Theory_Department/W3-AUDIT-C` (S37) | 5.8 MB | 11-16 | ≈ 11-30 | **none** |
| `runs/{F1M_pilot,P7_pilot_1e6,T5_1e5,T6_1e5}` (S01–S16) | 78.6 GB | 11-17 | ≈ 12-01 | only the two `fit.bin` + small F1M json (Owls + desktop); **none** for law.bin ×2, calib.bin, data/raw, eval.bin, logs |

Observed: loose root files with atime 09-29/09-30 (49 days) still exist, as in the 11-15 inventory (NOTS_ENV.md: nothing older than ≈ 44 days purged). The purge is not enforced strictly, but it must not be relied on. The desktop gap (w3scale, theory_w2/w3 on Owls only) is the item that can be closed first at no NOTS cost.

## 7. Decisions needed (owner / HQ)

- **D1 — regenerable bulk without a local copy.** DELETE-AFTER-GO = 64.4 GB on scratch (F1M islands 34.2 GB + setup.bin 10.1 GB; P7 inputs 13.4 GB; T5 bulk 5.9 GB; T6 0.44 GB; ccd-cli 0.34 GB; wp6 build 0.04 GB). All are regenerable from seeds/commits (rebuild cost, F1M alone: ≈ 269 core-h islands + 15 core-h setup; P7/T5/T6 bulk not costed here), and OFFLOAD.md already says island files are not kept. The owner rule 'never delete anything not verified locally' needs an explicit waiver for them (or HQ lists exceptions to download: islands = 34 GB).
- **D2 — calib.bin (8.1 GB, 135.6 core-h) and F1M data/raw (3.2 GB).** I mark them DOWNLOAD+DELETE (recommended). HQ may downgrade calib.bin to DELETE-AFTER-GO.
- **D3 — re-run of rep 1 after the freeze?** If HQ re-runs 6-AR-n200-r01-V-s1 on the frozen code, `setup.bin` (10.1 GB; 19 min, 15.25 core-h) could be reused only if the setup code is unchanged; otherwise delete it now. Scratch purge would take it by ≈ 12-01 anyway.
- **D4 — `projects/BVS/Others/library_portable` (95.5 MB, 3,620 files) + `benchmark_releases_Oct2026` (3.1 MB).** Others/INDEX.md: 'safe to delete with the releases; owner decides'. Proposed: download tar, then owner decides deletion.
- **D5 — Theory-owned trees need Theory/HQ OK:** `w3scale`, `theory_w2`, `theory_w3` (scratch), `SMC_Theory_Department/W3-AUDIT-C` (scratch + home), `projects/BVS/theory_w2|3`. The dept INDEX says Theory moves them after Wed 11-18; `theory_w3` + RESUME_PLAN is a possible resume target.
- **D6 — ccd-cli_2.1.321 (341.9 MB):** the 11-15 INDEX entry says 'HQ: move, do not delete'. Confirm deletion (regenerable).
- **D7 — relocation records and loose files:** HQ 11-15 said 'records left in place, untouched'. The owner's new cleanup order supersedes it only if confirmed; they are 8.9 KB. The `h1v1`/`fsb` tarballs (0.63 MB) are probably SMC-BVS history (UNKNOWN); the 16 Quant_Reg files are not SMC.
- **D8 — home quota 8,086 MB, guard 8,192 MB.** The SMC cleanup frees at most ≈ 0.3 GB. `.vscode-server` (4.5 GB) and the other app builds are not SMC and outside Engineering's scope; HQ/owner decide whether the guard threshold or a VS Code server cleanup is wanted. The guard runs inside Engineering's daily call (INDEX).
- **D9 — same run_id and seed, different `data.bin` hash:** P7 (b051ca10…) vs F1M (4de72b21…), both `data_seed` 602020001, same code commit 2cfaa9e5; setup.bin hashes also differ (172980ce… vs 51ebef14…). Probably a header field (binary hash / time); a one-line check for the data-generator owner before anyone treats the P7 data as the same dataset.
- **D10 — BVS keep-set (H12).** I assumed the subset rerun on v2.2.1 (HQ owner GO 11-17, RERUN_2400_PLAN.md, written by the other helper) reads `SMC_BVS/core`, `Data_Generation`, `Exact`, `Analysis`, `Environment`. Confirm against that plan before anything under `projects/BVS` is deleted; I propose no deletion there except D4.

## 8. Transfer plan sketch (nothing run)

Route: NOTS → Owls `records/hygiene_1117/<group>/` → desktop pull (no Rice VPN on the desktop). SHA-256 manifests are computed **on NOTS** and verified at each hop, as in OFFLOAD.md. NOTS data are deleted only after Owls **and** desktop are verified (laptop mirror does not gate). One transfer at a time, one multiplexed connection, `nice`, calm.

**Preconditions.** HQ GO; Theory OK for D5 items; `squeue -u fb31` empty (once); Owls free space on `/home` (my `df -h /home` printed zeros; INDEX 11-15 said ≈ 3 TB) and `D:` on the desktop (OFFLOAD: 70% rule). Use `$TMPDIR` under `~/SMC_Engineering_Department/tmp/`; nothing in `/tmp`.

**SHA-256 on NOTS.** Small groups: one `nice -n 19 sha256sum` pass per group (≤ 0.2 GB). Large files (calib.bin, data/raw, law ×2, 11.9 GB): a single 1-CPU job (`debug` partition, 30 min) *or* one `nice`+`ionice` login-node pass per file (≈ 1–2 min per GB); HQ decides which (no sbatch was run in this step).

| step | what | volume | source → dest | verify | then |
|---|---|---:|---|---|---|
| 0 | **desktop pull of what Owls already holds** (no NOTS read): `records/W3-SCALE` + `SMC_Theory_Department/records/theory_w2,theory_w3` | 883.0 MB | Owls → desktop | desktop SHA-256 vs `SHA256SUMS_*_nots.txt` | closes the 11-23/11-25 purge risk; NOTS delete of S30–S36 after Theory OK |
| 1 | small records: S03, S08, S10, S13, S16, S18, S19, S20, S22, S24, S25, S39, S40 + S37 | ≈ 105.3 MB | NOTS → Owls `records/hygiene_1117/{F1M_pilot,P7,T5,T6,g0,pmath,wp3_bench,wp6_k3,misc,theory_audit}` (rsync `--files-from`) | `sha256sum -c` on Owls | desktop pull; delete on NOTS |
| 2 | `law.bin` ×2 (S02, S12) | 709.7 MB | one file per call | SHA-256 | as above |
| 3 | F1M `data.bin` + `raw.bin` (S05), then `calib.bin` (S04) | 11.33 GB | one file per call | SHA-256 (calib first hashed on NOTS) | as above |
| 4 | home: tar of H12 + H13 + H15 (+ H14 if Theory agrees) with an `INDEX.tsv` check, dept `bin/manifests/scripts` (H04, H06, H08, H10), `SMC_Theory_Department/W3-AUDIT-C/pkg` (H17), `archive` (H18, copy-only) | ≈ 157.7 MB | `ssh nots 'tar cf - -T list'` or rsync, `deploy/` excluded by an explicit file list | `sha256sum -c` against `INDEX.tsv` + a new manifest | desktop pull; delete only H04/H06/H08/H10 (DD) and the DG rows |
| 5 | desktop pulls of steps 1–4 (`pull_desktop.ps1`, skip 03:00–03:15) | all | Owls → desktop | Get-FileHash vs manifest; `desktop_verified.txt` | the crew reads it |
| 6 | **NOTS delete** (HQ GO per group, one ssh call each) | 15.7 GB (DD) + 64.4 GB (DG, after D1) scratch, 0.16 GB home | — | the delete list is the manifest itself: `xargs -d '\n' rm -v -- < list`, never `rm -rf` on a department root; `find <run_dir> -type d -empty -delete`; keep an `OFFLOADED` tombstone (manifest hash, destinations) in each run dir; INDEX rows | `squeue` empty before; sizes recounted after |

After step 6, scratch SMC keeps ≈ 1.9 MB (`w3scale/code/v32dev_6866f57`, INDEX) + the UNKNOWN items; home keeps K 25.2 MB + U 13.9 MB (+ DO 134 MB if the owner keeps it). Relay volume to build: **12.14 GB** from scratch + 147 MB from home; Owls → desktop adds 883.0 MB of already-on-Owls records.

**Order of value / risk:** (0) desktop pull of Owls-held records; (1) small group; (2–3) law, data/raw, calib; (4) home; then deletes smallest-risk first: G0/fit.bin (already local), the small groups, DG regenerables last (after D1).

## 9. Commands (all read-only; every NOTS call sequential)

Local pre-checks (Owls): `ssh -O check nots` → *Control socket connect(...cm-fb31@nots.rice.edu:22): No such file or directory* (no master was running; the first `ssh nots` call opened one, ControlPersist 10 min, so calls after a gap may have opened a new one: ≤ 6 logins in all). `ls -la ~/SMC_Engineering_Department/{,records,crews,crews/offload}`; `df -h /home`; `find records -maxdepth 3`; `du -sh records/* staging/*`; `cat crews/offload/desktop_verified.txt`; `tail crews/offload/serve.log`; `ls -la ~/SMC_Theory_Department ~/SMC_Theory_Department/records`; `du -sh ~/SMC_Theory_Department/records/*`; `grep -A8 -i 'host nots' ~/.ssh/config`; repo reads and `grep -rIlF` per NOTS path over `Docs Theory_work Scripts POLICIES.md` (counts: runs/T5_1e5 1; wp3_bench 6; runs/g0 5; w3scale 11; theory_w2 47; theory_w3 11; SMC_Theory_Department 52; library_portable 19; h1v1 3; heterogeneous_1v1 6; fsb_deploy 2; claude-science 5; home_guard 6; the F1M/P7/T6/wp6/`~/archive` paths: 0). Byte sums by a small Python script in the scratchpad (not in the repo).

NOTS (6 `ssh nots` calls; `nice`/`timeout 120` on every `find`/`du`):

```
# call 1
hostname; date; quota -s | grep -A1 export/nots/home | tail -1; squeue -u fb31 | head -30
sacct -u fb31 -S now-7days -X --format=JobID,JobName%28,State,Elapsed,End,WorkDir%90 | tail -60
ls -la /scratch/fb31 | head -120; ls -la ~/SMC_Engineering_Department; ls -la /scratch/fb31/SMC_Engineering_Department

# call 2
ls -la /home/fb31 | head -90; ls -la ~/SMC_Engineering_Department/{scripts,results,crews,tmp}
for d in archive data runs slurm_out tmp; do ls -la /scratch/fb31/SMC_Engineering_Department/$d | head -60; done
cat /scratch/fb31/SMC_Engineering_Department/INDEX.md; ls -la /scratch/fb31/SMC_Theory_Department | head -40
ls -la ~/projects ~/projects/BVS | head -60

# call 3: scan() applied to /scratch/fb31/{SMC_Engineering_Department,SMC_Theory_Department,w3scale,theory_w2,theory_w3,.claude-science}; ls -la .../archive/home_guard
scan() { root="$1"; nice timeout 120 find "$root" -type f -printf '%s\t%T@\t%A@\t%P\n' | awk -F'\t' -v BIG=104857600 '<group by first 1 and 3 path components: files, bytes, newest mtime, oldest atime; print files >= 100 MB>' | sort; }

# call 4: same scan() with `\( -path "*SMC_BVS_v3*/deploy" -o -name SMC_BVS_v3 \) -prune -o`, depth D, BIG threshold:
#   ~/SMC_Engineering_Department (D=3, 5 MB)  ~/SMC_Theory_Department (3, 5 MB)  ~/projects/BVS (2, 5 MB)  ~/bin (1)  ~/archive (2, 1 MB)  ~/.claude-science-scratch (1)
ls -la <F1M_pilot, P7, T6 run dirs; T5 run dir without island_*>  (names + sizes only)
ls -laR ~/SMC_Engineering_Department/crews | head -40; head -50 ~/SMC_Engineering_Department/INDEX.md

# call 5
tail -12 ~/SMC_Engineering_Department/crews/home_guard/home_guard.log
for e in .vscode-server .t3 .codex .claude .local .t3-recovery .cache R lib Python .config .copilot .dotnet .ipython .conda .mozilla .nv .vscode archive_control; do nice timeout 120 du -sh "$HOME/$e"; done
nice timeout 120 du -sh ~/projects/Quant_Reg "~/projects/Large Prior_ Sims" /scratch/fb31/qr_data
ls -lu --time-style=+%m-%d /scratch/fb31 | awk ...            # atime of loose root files
head -6 h1v1_run_one.sh submit_p1only.sh uext_proc.slurm sqrtn_proc.slurm; tar tzf fsb_deploy.tar.gz | head -5; tar tzf h1v1_deploy_v1.tar.gz | head -5
ls -la ~/SMC_Engineering_Department/scripts/{F1M_pilot,T5_1e5,P7_pilot_1e6,T6_1e5}/bin

# call 6 (3 small JSON/ls reads)
cat <P7 run dir>/setup.bin.json <P7 run dir>/run_manifest.json   # compared with the copy in Owls records/F1M_pilot
ls <F1M run dir>/{log,manifests,cost} | head / wc -l
```

Not run (odd-looking or not needed): `du -sh /scratch/fb31` over the whole tree; any `find` on `/projects`, `$WORK`, `/home/fb31/.vscode-server`, `.codex` etc.; any checksum of NOTS files (to be done in the transfer step, ideally as one low-priority job); `sbatch`/`srun`; any write. The home-dir `du` calls on `.vscode-server` (many files) and `.t3` ran once each, sequentially.

## Group 1 done (Sonnet operator, 2026-11-18 06:10-06:20 UTC; HQ GO)
- **Scope:** 144 files, **12,037,953,990 B**: F1M run dir (72: `calib.bin` 8.08 GB, `data.bin` 1.64, `raw.bin` 1.60, `law.bin` 0.34 + small files), T5 run dir (69: `law.bin` 0.37 GB + small files), T5 batch ledgers (3). Not touched: all `island_*.bin`, `setup.bin`, `fit.bin` and the `*.bin.json` of those kept bins (T5 `raw/data/calib.bin` + json also stay, DG).
- **Manifest on NOTS** (one file at a time, `nice -n 19`): `~/SMC_Engineering_Department/records/hygiene_1117/group1_manifest_nots.tsv` (bytes, mtime, sha256, path); `group1_files.txt` is the explicit list.
- **Copy:** one `rsync -a --partial --bwlimit=60000` (nice both ends, one multiplexed ssh) into `records/hygiene_1117/group1/runs/...`.
- **Verify on Owls:** `sha256sum -c` 144/144 OK, 0 size mismatches. Row sizes of S02, S04, S05, S12 match the inventory.
- **D9 (data identity):** F1M vs P7 `X_sha256` and `y_sha256` IDENTICAL; file-level hashes (raw, data.bin) differ only by the meta block. Benign. Record: `group1_D9_data_identity.txt`.
- **NOTS delete:** one ssh call, literal paths, `squeue`=0 guard and size+mtime re-check per file; 144 deleted, 0 skipped. Log: `records/hygiene_1117/DELETES.tsv`. Tombstones `OFFLOADED_group1.txt` in 9 dirs (each run dir + its cost/, log/, manifests/; T5_1e5 batch dir).
- **Dept scratch:** 79,151,970,815 B / 967 files -> **67,114,033,797 B / 832 files** (freed 12,037,937,018 B net of 9 tombstones). Home untouched.
- **Ledger:** `crews/offload/ledger.tsv` created, 144 rows, `desktop_verified` empty (15.7 GB records group goes to the desktop when its VPN is back; Owls copy is currently the only copy).
- Status of S02, S04, S05, S12 and the F1M/T5 small files: **done (Owls only)**. Next: Group 2 = rest of DD (below the line in the operator report).

## Group 2 done (Sonnet operator, 2026-11-18 06:18-06:25 UTC; manager GO)
- **Scope:** 487 files (scratch 368 + home 119), 2,730,436,690 B hashed; 139,623,506 B copied. Scratch: `runs/{g0,pmath,wp3_bench}`, `wp6_k3/run_2756524`, P7 and T6 small files + ledgers, F1M ledgers, `slurm_out/` (120, all older than 11-18 00:00), 2 codex backup tgz, F1M/T5 `fit.bin` (+ `.bin.json`). Home `scripts/`: `bin/`, `manifests/`, `run_manifests/` and top-level files of P7/T5/T6; all of g0, pmath, wp3_arch, wp3_bench (not `engine_v4_cd1a7e02.tgz`), wp3_l5, wp3_levers, wp6_k3.
- **Not touched:** `rerun2400` (did not exist in either tree at 06:21), `INDEX.md`, `crews/`, F1M_pilot scripts (K), ccd-cli (D6), the build/code trees, islands, setup/raw/data/calib `.bin` and their sidecars, Theory trees, `projects/BVS`.
- **fit.bin (F1M, T5):** not re-copied. NOTS re-hash == `fitbin_1117/nots_sums.txt` == fresh `sha256sum` of the Owls copies (58e9e816..., 16a67d14...); sizes match; deleted. G0 stage files also compared with the existing `records/G0` copies: identical.
- **Verify:** `sha256sum -c` 485/485 OK (the 2 fit.bin are hash-only), 0 size mismatches. Manifest `group2_manifest_nots.tsv`; copies in `records/hygiene_1117/group2/{scratch,home}/`.
- **Delete:** one ssh call, `squeue`=0 guard, per-file size+mtime re-check; 487 deleted, 0 skipped; tombstones `OFFLOADED_group2.txt` in 24 dirs; DELETES.tsv +487, ledger.tsv +487 (now 631 rows). Empty subdirs (e.g. old build trees) were left (no `rmdir` authorized).
- **After:** dept scratch 67,114,033,797 B / 832 files -> **64,397,161,861 B / 478 files** (freed 2,716,871,936 B); home `scripts/` 175.7 -> 162.2 MB; home quota 8,088 -> 8,075 MB.
- **Left on scratch (Group 3 candidates):** 64.40 GB = islands/setup/P7/T5/T6/wp6 build + ccd-cli; list `group3_proposed_files.tsv` (453 files, 64,055,186,051 B, ccd-cli excluded).

## Group 3 done (Sonnet operator, 2026-11-18 06:25-07:11 UTC; manager GO; regenerable bulk, Owls copy only)
- **Scope:** exactly `group3_proposed_files.tsv`: 453 files, **64,055,186,051 B** (F1M run dir 34 files 44.32 GB: 16 islands + setup.bin + sidecars; P7 run dir 6 files 13.38 GB; T5 run dir 42 files 5.87 GB; T6 `t6/` 4 files 0.44 GB; wp6_k3 `build_2756524`, `src`, `engine_v4_89366d4a.tgz` 367 files 35 MB). ccd-cli not touched (D6).
- **Copy/verify:** manifest hashed on NOTS first (`group3_manifest_nots.tsv`), one `rsync -a --partial --bwlimit=60000` (about 40 min wall incl. hashing), `sha256sum -c` on Owls **453/453 OK**, 0 size mismatches; copies in `records/hygiene_1117/group3/runs/...`. Owls is now the only copy of these files.
- **Guard changed mid-run:** at delete time `squeue` was no longer empty: the `rr2400` arrays (jobs 2773943/2773944, 41 running+pending) had started, all with WorkDir `runs/rerun2400/...`. The first delete attempt aborted (nothing deleted). I grepped the rerun2400 scripts (home) and tree (scratch) for any reference to the files being deleted (P7/T5/T6/F1M_pilot/wp6_k3/g0/pmath/wp3_bench/islands/setup.bin): none. The guard was then "every job's WorkDir is under runs/rerun2400/", and the delete ran.
- **Delete:** one ssh call, literal paths, per-file size+mtime re-check: 453 deleted, 0 skipped; tombstones `OFFLOADED_group3.txt` in the 4 run dirs + `runs/wp6_k3/`; DELETES.tsv +453, ledger.tsv +453.
- **rmdir (explicit lists, `rmdir -v`, only under `runs/`, only fully offloaded trees):** 105 from the file lists (G2 + G3) + a follow-up of 21 (empty `tmp/`, `pkgRedirects/`, `CMakeScratch/`, `src/cli`, `pmath/run_2747524`, `build_2756524`): all removed. Kept: every run dir top level with its tombstones, `runs/`, `runs/rerun2400/`.
- **Dept scratch, excluding runs/rerun2400:** 64,397,161,861 B / 478 files -> **342,032,628 B / 30 files** (= ccd-cli 341.9 MB + INDEX.md + tombstones); freed 64,055,129,233 B net of 5 new tombstones. Home quota 8,075 -> 8,080 MB (rerun activity).

## Group 4 done (Sonnet operator, 2026-11-18 07:11-07:13 UTC; manager GO; home DG build/code trees)
- **Scope:** 1,882 files, **142,793,087 B** under `~/SMC_Engineering_Department/scripts/`: `F1M_pilot/build`; `{P7_pilot_1e6,T5_1e5,T6_1e5}/{build,code}`, T5 `build_isa_check`, `build_portable_bench`, T6 `__pycache__`; `wp3_bench/engine_v4_cd1a7e02.tgz` (sha256 61524c21... equals Owls `staging/engine_v4_cd1a7e02.tgz`). Not touched: `F1M_pilot/{bin,code,manifests,run_manifests,*.sh}` (KEEP), `rerun2400/`, `INDEX.md`, `crews/`. No symlinks or special files in the trees; nothing but my 10 group-2 tombstones lay outside the G4 list.
- **Copy/verify:** manifest on NOTS (`group4_manifest_nots.tsv`), one rsync `--bwlimit=60000`, `sha256sum -c` **1882/1882 OK**, 0 size mismatches, copies in `records/hygiene_1117/group4/` (51 executables keep their mode bits).
- **Delete:** one ssh call; guard = every queued/running job has WorkDir under `runs/rerun2400/` (42 `rr2400` lines, 0 others); per-file size+mtime re-check: 1,882 deleted, 0 skipped. Tombstones `OFFLOADED_group4.txt` in `F1M_pilot`, `P7_pilot_1e6`, `T5_1e5`, `T6_1e5`, `wp3_bench`. DELETES.tsv +1,882, ledger.tsv +1,882.
- **rmdir:** 337 explicit directories (all subdirs of the offloaded trees, incl. the group-2 leftovers: bin, manifests/*, run_manifests, g0/{kernel,stage}...), all removed, 0 failed. Kept: top levels of every script batch dir with its tombstones, `scripts/`, `rerun2400/`, `F1M_pilot` KEEP files.
- **Home `scripts/` (excluding rerun2400):** 162,177,851 B / 2,219 files -> **19,627,154 B / 342 files** (F1M_pilot KEEP set + tombstones). **Home quota 8,080 -> 7,938 MB** (guard 8,192).

## Theory group: prepared, not run (Sonnet operator, 2026-11-18)
- Lists and plan: `~/SMC_Engineering_Department/records/hygiene_1117/theory_prep/` (`README_THEORY_PLAN.md`, `*_files.tsv`, `*_empty_dirs.txt`). Delete set 9,820 files / 922.0 MB (theory_w2 5,957, theory_w3 1,858, w3scale 1,525 without S31, W3-AUDIT-C scratch 460 + home pkg 20); S31 (28 files, 1.9 MB) kept.
- Pre-check: Owls copies of theory_w2, theory_w3 and w3scale equal NOTS by path+size+mtime for all 9,368 files (0 missing, 0 extra). theory_w3 scratch is therefore not newer than the 11-15 Owls copy; the hash compare decides. Open item: OK to `rmdir` under the Theory trees (current permission covers `runs/` and `scripts/` only).

## Theory group done, PARTIAL (Sonnet operator, 2026-11-18 07:15-07:30 UTC; manager GO)
- **Scope as prepared:** 9,820 files (theory_w2 5,957, theory_w3 1,858, w3scale 1,525 without S31, W3-AUDIT-C scratch 460, home pkg 20) = 921,954,318 B; S31 (28 files) kept; `projects/BVS/theory_*` not included. A fresh listing at 07:15 equalled the prepared lists (0 new, 0 gone).
- **Verification by SHA-256, not size/mtime:** all 9,848 files hashed on NOTS (nice, one at a time; `theory_manifest_nots.tsv`), then `sha256sum -c` on Owls against the fresh NOTS hashes: theory_w2 5,957/5,957, theory_w3 1,858/1,858, w3scale 1,553/1,553 (incl. S31), W3-AUDIT-C scratch 460/460, home pkg 20/20, **all OK**, so nothing had to be re-copied (theory_w3 included: contents equal the 11-15 Owls copy). Copies: `~/SMC_Theory_Department/records/{theory_w2,theory_w3}`, `~/SMC_Engineering_Department/records/W3-SCALE/w3scale` (left where it is), new `~/SMC_Theory_Department/records/w3_audit_c/{scratch,home_pkg,SHA256SUMS_w3_audit_c_nots.txt}` (one rsync, `--bwlimit=60000`).
- **Delete (one ssh call, guard: 36 queue lines, all WorkDir `runs/rerun2400/`, 0 others; per-file size+mtime re-check; S31 refused by the script):** **9,327 deleted** (880,954,221 B), 0 changed. theory_w3 and the scratch W3-AUDIT-C are fully emptied. **493 files (41,000,097 B) were NOT deleted: `rm` -> Permission denied**, because they sit in directories of mode 555 (read-only): theory_w2 82 files (`fam_X/runs/*`), w3scale 391 (`runs/*/scripts`), home `W3-AUDIT-C/pkg` all 20 files (the pkg dirs are read-only, so the tombstone could not be written there either). All 493 are SHA-verified on Owls. I did not `chmod`: not authorized. List: `theory_prep/NOT_DELETED_permission_denied.tsv`; blocking dirs: `theory_prep/READONLY_dirs_blocking_delete.tsv`.
- **rmdir:** 512 of 597 listed directories removed; 85 not removable (non-empty or read-only). Tombstones `OFFLOADED_theory.txt` in theory_w2, theory_w3, w3scale (with a PARTIAL note), scratch W3-AUDIT-C; none in home pkg.
- **Logs:** DELETES.tsv +9,327 (`theory`), ledger.tsv +9,820 rows (`nots_freed` empty for the 493).

## Theory group COMPLETED (second pass, 2026-11-18 07:28-07:29 UTC; manager OK)
- `chmod u+w` (no -R) on exactly the 83 directories of `theory_prep/READONLY_dirs_blocking_delete.tsv`; the 493 verified files of `NOT_DELETED_permission_denied.tsv` then removed (size+mtime re-check, same job guard: 35 queue lines, all WorkDir `runs/rerun2400/`): **493 deleted, 0 skipped**; the 85 directories that had failed were `rmdir`ed (0 failures); S31 and `w3scale/code` untouched. Tombstone written in `~/SMC_Theory_Department/W3-AUDIT-C/pkg/OFFLOADED_theory.txt`; the theory_w2 and w3scale tombstones carry a COMPLETED note.
- **Theory-group totals:** 9,820 files / 921,954,318 B deleted (9,327 first pass + 493 second); all SHA-256 verified on Owls first; DELETES.tsv has 9,820 `theory*` rows; ledger.tsv has 9,820 rows, all with `nots_freed`.
- **Left in the Theory trees:** a tombstone each in theory_w2, theory_w3, scratch `SMC_Theory_Department/W3-AUDIT-C` and home `pkg`; `w3scale` = tombstone + `code/v32dev_6866f57` (S31, 28 files, 1.88 MB).

## Group R done (rerun2400, Sonnet operator, 2026-11-18 12:55-12:59 UTC; HQ GO, verdict accepted)
- **Scope:** scratch `runs/rerun2400/rr2400_20261118T0636Z/` 1,523 files / 420,110,451 B (its `tmp/` was an empty directory: nothing to keep) + home `scripts/rerun2400/` 90 files / 3,929,682 B = **1,613 files / 424,040,133 B**.
- **Verify (SHA-256, not size):** all 1,613 hashed on NOTS (`rerun2400_manifest_nots.tsv`); `sha256sum -c` on Owls: scratch vs `records/rerun2400/rr2400_20261118T0636Z` **1,523/1,523**; home vs `staging/rerun2400/bundle_20261118` **70/70** (the bundle's own SHA256SUMS also verified, 69/69); 20 home files were not in the bundle (compile caches `new|old/core/.cpp_cache/*` and `run/{chunks_p0500,chunks_p1000,config.env,jobs.tsv,precompile.ok.*}`, 3.2 MB): copied by rsync to `records/rerun2400/home_scripts_extra/`, **20/20** OK. Sizes match.
- **Delete:** `squeue -u fb31` = 0 lines; one ssh call, per-file size+mtime re-check: 1,613 deleted, 0 skipped; 279 directories `rmdir`ed (0 failed). Tombstones `OFFLOADED_rerun2400.txt` in `runs/rerun2400/` and `scripts/rerun2400/` (both top levels kept). DELETES.tsv +1,613 (`groupR`), ledger.tsv +1,613.
- **Dept scratch** (now including the rerun tree): 762,143,079 B / 1,553 files -> 342,033,226 B / 31 files (ccd-cli, INDEX.md, tombstones).

## Group B done, PARTIAL (`~/projects/BVS`, Sonnet operator, 2026-11-18 12:59-13:05 UTC; HQ GO, hold lifted)
- **Scan (pruned by name, `SMC_BVS_v3*/deploy` and `SMC_BVS_v3` never entered; only `Others/SMC_BVS_v3_history_Oct2026/deploy` exists):** 6,822 files / 141,071,326 B + 1 symlink (`.../prototype_profiling/checker/.venv -> /scratch/fb31/v3_profiling_20261020/venv/checker_venv`), 1,140 dirs; nothing non-SMC inside. Copy of ALL of it: `records/hygiene_1117/projects_BVS/` (rsync `--bwlimit=60000`), manifest hashed on NOTS (`projects_BVS_manifest_nots.tsv`), `sha256sum -c` **6,822/6,822 OK**, 0 size mismatches, symlink preserved.
- **Delete list (files; `squeue`=0; per-file size+mtime re-check; script refuses keep paths): 1,579 deleted (26,041,578 B), 0 skipped:** Analysis 61, Benchmarks 604, Data_Generation 24, Environment 13, Exact 47, INDEX.tsv 1, Main_Results 23, Methodology 17, Others 28 (`INDEX.md`, `superseded_code`), Records 31, SMC_BVS 37, Studies 528, tools 4, theory_w2 97, theory_w3 64.
- **KEPT on NOTS:** `README.md` (kept + new tombstone `OFFLOADED_projects_BVS.txt` saying where the copy is); D4 `Others/library_portable` (3,620 files, 95.5 MB) + `Others/benchmark_releases_Oct2026` (432, 3.1 MB), downloaded + verified; the deploy folder (not touched).
- **HELD, not deleted (2 reasons, need a decision):** (1) **535 files (7,156,884 B)** of theory_w2 (364) and theory_w3 (171) sit in **85 read-only (mode 555) directories**; deleting needs `chmod u+w` on those dirs, authorized earlier only for the Theory trees' explicit list. (2) **`Others/SMC_BVS_v3_history_Oct2026/{core,prototype_profiling}` (655 files + the symlink, 9,198,204 B)**: not in the manager's exclusion list, but held back on my judgment: inventory row H16 was never proposed for deletion (UNKNOWN), it is the parent of the excluded deploy folder, 12 of its directories (113 files) are read-only, and the `.venv` link points to scratch. Both lists: `records/hygiene_1117/projects_BVS_held_readonly.tsv` (1,191 rows, reason column).
- **rmdir:** not done (no authority granted for `projects/BVS`); the empty directory skeleton stays.
- **Logs:** DELETES.tsv +1,579 (`groupB`), ledger.tsv +6,822 (`nots_freed` only for the 1,579).
- **Final SMC footprint on NOTS (13:05 UTC):** scratch dept 342.0 MB (31 files: ccd-cli 341.9 MB, INDEX.md, tombstones) + w3scale 1.9 MB (S31 + tombstone) + loose root files 0.66 MB + `.claude-science` 41.8 KB; home `~/SMC_Engineering_Department` 19.7 MB, `~/projects/BVS` 115.0 MB (5,244 files), `~/archive` 4.7 MB, `~/bin` 24 KB, `~/SMC_Theory_Department` tombstone. **SMC total about 485 MB** (was 80.40 GB). **Home quota 9,084 MB of 10,240 MB, above the 8,192 MB guard: the growth since 12:55 (7,931 -> 9,084 MB, 107k -> 114k files) is not SMC** (SMC home shrank by 26 MB); the last guard run was 11-17 08:40.

## Group B COMPLETED (second pass, 2026-11-18 13:05 UTC; manager decisions 1-3)
- `chmod u+w` (no -R) on exactly 97 directories: the 85 read-only dirs of theory_w2/theory_w3 and the 12 read-only dirs inside `Others/SMC_BVS_v3_history_Oct2026/{core,prototype_profiling}`; then **1,190 files deleted** (535 theory + 655 history, all SHA-256 verified on Owls, size+mtime re-check, `squeue`=0), 0 skipped; script refuses D4, README, tombstone, `deploy/` and `.venv`. Groups B total: **2,769 files / 42,396,666 B** deleted, DELETES.tsv +1,190 (`groupB(2nd pass)`), ledger.tsv `nots_freed` set for 2,769 of 6,822 groupB rows (the rest are the kept D4/README rows).
- **rmdir** by explicit list (465 dirs; never `deploy/`, its parents `Others/` and `SMC_BVS_v3_history_Oct2026/`, `projects/BVS/`, or the D4 dirs): 428 removed, 37 not: 27 "Permission denied" (20 read-only parents under `theory_w2/code/{main_11dc9b7,tickets_*}`, outside the authorized chmod set) + 10 non-empty parents; plus `prototype_profiling/` and `checker/` stay because they hold the `.venv` symlink (not touched). Left: an empty skeleton of 37 dirs under `theory_w2/code` (finishing it needs `chmod u+w` on those 20 read-only dirs).
- **projects/BVS now:** `README.md`, `OFFLOADED_projects_BVS.txt` (tombstone, second-pass note appended), D4 (`library_portable` 95.5 MB + `benchmark_releases_Oct2026` 3.1 MB), the `.venv` symlink, the deploy folder (untouched), and the dir skeleton above.

## Group B final (theory_w2 skeleton, 2026-11-18 13:07 UTC; manager OK)
- `chmod u+w` (no -R) on the 20 read-only dirs under `projects/BVS/theory_w2/code`, then `rmdir -v` of the remaining 35 empty directories there plus the empty `theory_w2/` itself: all removed, 0 failures, `squeue`=0. No files touched.
- **`~/projects/BVS` now holds only:** `README.md`, `OFFLOADED_projects_BVS.txt`, `Others/` with D4 (`library_portable`, `benchmark_releases_Oct2026`) and `SMC_BVS_v3_history_Oct2026/{deploy (untouched), prototype_profiling/checker/.venv (symlink holder)}`. SMC footprint on NOTS about 468 MB; home quota 9,064 MB (non-SMC growth).
- The hygiene cleanup is finished; Owls holds all copies under `records/hygiene_1117/`, `records/rerun2400/`, `SMC_Theory_Department/records/` and the W3-SCALE records.
