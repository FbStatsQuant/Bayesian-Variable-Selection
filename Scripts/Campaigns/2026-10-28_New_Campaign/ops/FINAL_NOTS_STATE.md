# FINAL NOTS STATE — New Campaign (OPS, 2026-11-03 14:00Z) — OPS CLOSED

Raw evidence:
- `ops/evidence/ops_final_state_20261103.txt` (13:59:12Z, read-only);
- `ops/evidence/ops_final_delete.txt`;
- `ops/CLEANUP_LOG.md`.

**Jobs:** `squeue -u fb31` is empty. No job of ours is queued or running.

## Footprint
- **Home:** guard reads `home 8.42 GB of 10.00 GB | campaign_home 0.00 GB | campaign_scratch 0.00 GB | OK`. `du /home/fb31` is 8,675,228 KB. The non-campaign remainder is Felipe's VS Code server, Codex, Claude and T3 installs. Their caches and old versions were cleaned under HQ D74 and D79; the live installs are kept.
- **Campaign home** `/home/fb31/projects/BVS/New_Campaign`: **2,432 KB**.
  - `README.md`;
  - `code/core` (frozen SMC-BVS v2.2.1 core) and `code/v2_2`;
  - `code/bench_v2` (frozen F3 install);
  - `code/ops` (guard.sh, remote_pack.sh);
  - empty `inputs/` and `manifests/`.

  Why kept: small and reusable (HQ D92). The same trees are archived locally in `nots_home_final\code\`.
- **Scratch:** `/scratch/fb31/New_Campaign` **no longer exists**. The receipts and detached-step logs were archived first (`nots_scratch_final\`).
- **Untouched throughout:** the benchmark freeze (`/projects/ml75/fb31/BVS/bench20261019/`, `/home/fb31/projects/BVS/Benchmarks/`), `~/.claude/remote`, `~/.t3-recovery`, and everything else outside the campaign.

## Runs: all closed (local data root `<PC_NOTS_DATA>\New_Campaign\`)

| Run | Jobs | Outcome | Local data (bundle MANIFEST sha256) |
|---|---|---|---|
| PROD-H `20261030T0934Z_prodH` | 2469859–2469861 | 2,394 ok + 6 resource_limit; repro vs 2026-10-23 IDENTICAL (882/882); P5 not run (D62); F1 deviation accepted (D92); report `ops/PRODH_COMPLETION_20261102.md` | `results\…\p0500` 7893396c…, `p1000` a0196198…, `logs\…` 8048e0b8…, home summary `runs\…\home_summary` (HOME_MANIFEST ca245339…; also `nots_home_final\runs\…`) |
| PROD-L `20261030T1811Z_lowp_prodL` | main wave 2474408–… | 14,400 units completed; closed under D63 (P5 scan incomplete) | `results\…_enum20` d0a0fc14…, `_enum30` 98b8e95a…, `_smc` 394f7dd0…, `_smcrep` 7c5baa69…, `logs\…` a9b01c2a…, `runs\…\home_summary` |
| BENCH_F3_DEV `20261030T1855Z_bench_f3v2_dev` | 2496644 | 26/26 valid | `results\…\p0500` bfae02b0…, `p1000` 62d71add…, `logs\…` 976a504e…, `upload\…` |
| BENCH_F3_PROD `20261102T1252Z_bench_f3v2_prod` | 2503200, 2504013, 2507545, 2509541 | 2,400 valid / 14,400 ok / 0 unexpected; 71.98 core-h; Sol ACCEPT WITH FIXES; report `ops/F3PROD_COMPLETION_20261103.md` | `results\…\p0500` e2600c82…, `p1000` 6b61c4b2…, `logs\…` 5c96e7f6…, `upload\…` |
| PROD_L_BENCH rev 2 `20261102T2309Z_lowp_bench` | 2511134, 2511135, 2511136 | 98/98 COMPLETED; reconcile CLEAN; **accept_bench ACCEPTED 19,200/19,200** (D54.3 ABESS exact-size check deferred, disclosed); 21.85 core-h | `results\…_benchres` 0dd8ced3…, `logs\…` 0b8bc30d…, `runs\…\home_summary`, `runs\…\accept\ACCEPT_BENCH.md` |
| PROD_L_BENCH rev 1 (failed, D82) `20261102T1311Z_lowp_bench` | 2510090 (FAILED), 2510091 (CANCELLED), 2510092 | bundle probe defect; fixed in rev 2 | `logs\20261102T1311Z_lowp_bench` (evidence; transfer manifest e38e7a28…) |
| LOWP pilots and the conformance identity gate (OPS-4, earlier) | — | closed before PROD | `logs\20261030T0313Z_lowp_pilot`, `logs\20261030T0712Z_lowp_pilot`, `logs\conf_identity` |

Every scratch deletion followed a VERIFIED copy, with the remote manifest re-checked or the hash gated (receipts in `ops/transfer/receipts/`). Each clean-up script that has a receipt reported `CLEANUP VERIFIED`.

## Archived to the laptop over the campaign
- **D31** (archive, then erase): `~/backups` (2 Quant_Reg tarballs) → `NOTS Data\NOTS_home_archive\backups_20261030\`; ~/.codex db-backups (89 folders) → `NOTS Data\NOTS_home_archive\codex_db_backups_20261030\`.
- **D92 final sweep:** `NOTS Data\New_Campaign\nots_home_final\` (code trees, CONF_NOTS_IDENTITY staging, PROD-H home run folder, README) and `nots_scratch_final\` (detached-step logs, clean-up receipts, README).
- **Erased without archive** (regenerable, HQ-authorised):
  - D74: VS Code VSIX cache, 561 MB;
  - D79: pip and matplotlib caches, the VSIX cache, T3 runtime 0.1.6, three old VS Code servers and their CLI binaries, 2,017.8 MB.

## Open items for HQ
None for OPS. Two items stay on record for disclosure:
- the PROD-H P5 sensitivity was not run (D62);
- the PROD_L_BENCH ABESS exact-size check is deferred (D54.3).

OPS-4 is closed for this campaign. No further SSH unless HQ asks.
