# NOTS inventory (read-only), 2026-10-29 00:39Z

Taken by OPS over `ssh nots`. Raw outputs: `evidence/inv1_raw.txt`, `evidence/inv2_raw.txt`, `evidence/inv3_raw.txt`; per-file sha256 lists in `evidence/nots_hashes/`.

Note: `Host nots` now resolves to **loginx2** (<internal-ip>), not loginx3. The `~/.ssh/config` header says it was re-pinned on 2026-10-28 to follow the only live T3 server. OPS used `ssh nots` as configured and did not change it.

## Quotas
| Filesystem | Used | Limit | Note |
|---|---|---|---|
| /home (nfs1) | **9,519 MB = 9.30 GiB** | 10,240 MB | `quota -s`; `du` gives 9.2 G. Already above the campaign's 9 GB home line. |
| /scratch (vast) | 199 G (fb31) | no per-user quota shown | FS 82 % full (947T/1.2P) |
| /projects/ml75 | 80 G for the group (fb31: 3.6 G) | about 100 G group quota (memory, 2026-10-21) | |

## /home/fb31: top level (disk blocks, `du -sh`)
| Folder | Size | What it is | BVS? |
|---|---|---|---|
| .vscode-server | 4.9 G | VS Code remote server: cli 2.8 G, extensions 1.5 G, data 570 M, 4 old `code-*` builds 24–34 M each | no |
| .codex | 1.2 G | Codex CLI: packages 931 M, db-backups 165 M, cache 53 M, plugins 49 M | no |
| .claude | 921 M | Claude CLI: remote 900 M | no |
| projects | 728 M | BVS 624 M, Quant_Reg 101 M, "Large Prior_ Sims" 2.7 M | partly |
| archive_control | 673 M | 2026-10-14 (92 M), 2026-10-15 (581 M) | unknown, likely not BVS |
| .t3 | 530 M | **live T3 server state** (runtime 363 M, userdata 114 M, ssh-launch 54 M) | no, never touch |
| R | 212 M | R/library 152 M, Dynamic_BQTF_libs 61 M | no |
| .cache | 129 M | pip 128 M | no |
| backups | 46 M | two Quant_Reg package tarballs (Oct 21–22) | no |
| .t3-recovery | 12 M | T3 diagnostic of 2026-10-22 | no |
| archive | 5.1 M | Sept 2026 maintenance archives | no |
| .local | 4.1 M | user Python bits | no |
| others | < 1 M | dotfiles, .ssh, bin, lib, README.md | no |

## /home/fb31/projects/BVS (624 M)
| Folder | Size | Contents | Status |
|---|---|---|---|
| Others/ | 457 M (322 MB apparent; 55,024 files, 34 symlinks) | legacy experiments: Experiments_October_14_Mixture 172 M, _WeakSignals 91 M, _Benchmarks 81 M, Experiments_oct_13 67 M, Experiments_October_14 45 M, Benchmarks_old 3.3 M | laptop copy at `NOTS_BVS\NOTS_home\projects\BVS\Others` (relocation of 2026-10-21) |
| library_portable/ | 102 M | read-only R library (abess, glmnet, susieR, SSLASSO, Rcpp*, ggplot2 …) used by the benchmark code | benchmark dependency |
| SMC_BVS_v3/ | 54 M (2,816 files) | core 3.3 M, deploy 44 M, prototype_profiling 7.4 M | code of the v3 deployment; no full laptop copy |
| Benchmarks/ | 7.4 M | F1–F5, A1–A3, _shared | **frozen** (charter §3) |
| releases/ | 4.6 M | three hash-addressed releases | laptop copy in NOTS_home |
| README.md | 4 K | layout note of 2026-10-23 | |
| New_Campaign/ | new | scaffold created by OPS 2026-10-29 | campaign |

## /scratch/fb31 (199 G)
| Item | Size | Status |
|---|---|---|
| qr_data/ | 195 G | **Quant_Reg (not BVS)**: inner_individual 121 G, inner_individual_S_b0001 71 G, extreme_joint 3.3 G, air_sim_lap 28 M, two empty dirs. What remains of the paused relocation. |
| smcbvs_v3_deploy_20261022/ | 3.9 G | Campaign-2 production `claude/prod_p0500_…` 1.1 G and `prod_p1000_…` 2.8 G (results + attempts + slurm), plus readiness/test runs (rdy_A 40 M, rdy_B 20 M, tinyp, smoke, c4test, e2e), A_build n0 logs, n0_20261023 (≈ 12 M), `claude_readiness_evidence.tar.gz` 31 M |
| _relocation_manifests/ | 136 M | checksum lists and chunk indexes of the paused relocation |
| *_MOVED.md (8) | < 4 K each | pointers left by the relocation |
| loose files (≈ 25) | < 1 M total | Sept 29–30 scripts, logs and `*_deploy*.tar.gz` (fsb, h1v1, air, k2, sqrtn, uext, spod: not BVS by name) and four relocation scripts |
| .claude-science/ | 44 K | tool state |
| New_Campaign/ | new | scaffold created by OPS |

## /projects/ml75/fb31 (3.6 G)
| Item | Size | Status |
|---|---|---|
| BVS/bench20261019/ | 3.5 G | **frozen** (inputs 1.4 G, results 757 M, verify 696 M, scoring 331 M, lib 166 M, derived 78 M, logs 70 M, runs 46 M, …); `DO_NOT_RELOCATE.md` present, no `RELOCATION_OK.md` |
| BVS/v3_profiling_20261020/ | 113 M (70 MB apparent, 16,436 files, 5 dangling symlinks) | v3 profiling code/data/results; laptop holds only `partC` |
| BVS/*_MOVED.md (4) | 4 K each | relocation pointers |

## Jobs
`squeue -u fb31`: **no running or queued jobs** (2026-10-29 00:39Z).

## After class-A clean-up (2026-10-29 02:42Z; `evidence/final_state_raw.txt`)
- **Home:** 9,063 MB = 8.85 GiB of 10 GiB, down from 9,519 MB = 9.30 GiB. That leaves only about 150 MB of headroom below the 9 GB guard line until class-B items are cleared.
- **/home/fb31/projects/BVS:** 168 M. `Others/` is gone; Benchmarks, library_portable, releases, SMC_BVS_v3, README.md and New_Campaign remain.
- **/scratch/fb31:** 195 G, of which qr_data accounts for nearly all. `smcbvs_v3_deploy_20261022/` is gone.
- **/projects/ml75/fb31:** 3.5 G, the frozen bench20261019 only. `v3_profiling_20261020/` is gone, replaced by a MOVED pointer.
- **Jobs:** none.
