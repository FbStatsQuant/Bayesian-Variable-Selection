# NOTS clean-up plan (OPS, 2026-10-29)

Source: `NOTS_INVENTORY.md`. Evidence:
- NOTS sha256 lists: `evidence/nots_hashes/<name>.sha256`, taken 2026-10-29 00:47–00:56Z;
- laptop comparisons: `evidence/verify/<name>.json`, made with `verify_against_local.py`.

Scope rule from Felipe's brief: nothing outside the BVS paths is deleted without first being listed for him. The BVS paths are `/home/fb31/projects/BVS/`, the BVS folders in `/scratch/fb31/` and `/projects/ml75/fb31/BVS/`.

## Class A: delete without asking

Status: **EXECUTED, 2026-10-29 02:02–02:42Z.**
- Review trail: Sol round 1 rejected the tools (fixes in `review/OPS_RESPONSE_R1.md`); Sol round 2 approved with fixes, and F1–F3 are covered in `review/OPS_RESPONSE_R2.md`.
- Every step is logged in `CLEANUP_LOG.md`.
- A1.3 needed a second pass because 7 files sat in read-only directories. That pass used a residual list authenticated as a subset of the verified list.

Every item is either already verified against a laptop copy by per-file sha256 (A1), or copied by the transfer tool and verified per file before deletion (A2).

**Writer exclusion.** OPS is the only thread allowed to SSH to NOTS (charter §3), and fb31 has no queued or running jobs. Both tools re-check `squeue -u fb31` immediately before deleting, and refuse if it is not empty.

**A1 mechanics: `transfer/verified_delete.sh BASE LIST LIST_SHA [LINKS LINKS_SHA]`.** It deletes nothing unless every check passes:
- BASE is canonical and is one of the three bases hard-coded in the script (A1.1–A1.3). Frozen paths are refused.
- LIST and LINKS are copied to a private temp dir, and their sha256 must equal the values given.
- Line syntax is strict: no backslash names; no empty, `.` or `..` components; no duplicates.
- The set of regular files found under BASE must equal the list exactly. `find` does not follow symlinks, so a list entry that escapes BASE cannot pass.
- The symlinks found under BASE (`name -> target`) must equal the approved link list exactly.
- There are no other entry types, every entry is owned by fb31, and there are no nested mounts.
- `sha256sum -c --strict` passes for every entry.

It then deletes the listed files, then the approved link objects (never their targets), then empty dirs, then BASE. Any residue or command failure exits non-zero (`set -euo pipefail`).

**A2 mechanics: `transfer/nots_pull.py --legacy --delete`, NOTS side `remote_pack.sh`.**
- Only the two A2 folders below are accepted as legacy targets.
- The manifest refuses other entry types, non-fb31 owners, nested mounts, and names containing a newline or backslash.
- The folder is tarred and extracted locally, and every local file is hashed.
- The copy counts as VERIFIED only if:
  - every file matches;
  - the file counts agree;
  - the only tar members skipped are the manifest's own symlinks.
- Deletion requires the remote manifest, recomputed with checks, to be byte-identical to the verified one. Only the manifest's files and symlinks are then removed, followed by empty dirs. Any unexpected leftover is kept, with exit 5.

**Tool tests** (`evidence/tooltest2_raw.txt`, `evidence/tooltest3_raw.txt`, 2026-10-29 01:32Z) refused every case they should:
- no allowlist;
- wrong list sha;
- an extra file;
- an unapproved link, or links omitted;
- a `../` entry;
- changed content;
- a non-allowlisted base;
- a scaffold folder;
- an unapproved legacy path;
- a frozen path;
- a path through a symlink;
- a FIFO;
- a wrong manifest sha.

The good cases deleted cleanly with nothing left, and the dummy end-to-end pull/verify/delete passed twice (OPS_LOG).

| # | Path (NOTS) = BASE | Size | Files | Reason | Verification |
|---|---|---|---|---|---|
| A1.1 | `/scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_p0500_20261023T1227Z/results` | 1,097,537,311 B | 4,800, 0 symlinks | Campaign-2 production outputs; Felipe authorised deletion once hashes are re-verified | List `evidence/nots_hashes/prod_p0500_results.sha256` (sha256 `fa82a53f…ad56`) was taken by `cd BASE; find . -type f …` (`evidence/inv3.sh`), so its paths are BASE-relative. `results/` itself holds a nested `prod_p0500_20261023T1227Z/p0500/<case>/` folder; the whole-deploy list `evidence/nots_hashes/scr_smcbvs_deploy_all.sha256` shows this (4,800 lines `./claude/prod_p0500_…/results/prod_p0500_…/p0500/…`). Laptop base: `NOTS_BVS\smcbvs_v3_deploy_20261022\claude` (OUTPUTS.md). `evidence/verify/prod_p0500.json`: 4,800/4,800 match, 0 mismatch, 0 missing. |
| A1.2 | `…/claude/prod_p1000_20261023T1227Z/results` | 2,905,373,304 B | 4,800, 0 symlinks | same | List sha256 `e1c84805…dcf0d`. `evidence/verify/prod_p1000.json`: 4,800/4,800 match. |
| A1.3 | `/home/fb31/projects/BVS/Others` | 321,924,368 B (457 M on disk) | 55,024 + 34 symlinks | Legacy experiments (D6: out of scope); the largest BVS item on the 10 GB home | List sha256 `3205717b…b9f7`. Approved links: `evidence/nots_hashes/home_BVS_Others.symlinks` (sha256 `42f3bb5b…c597`). Of the 34 links, 24 are absolute links to `/scratch/fb31/Experiments_October_14*` and `/scratch/fb31/BVS_Paired_October_14` and 7 point to `/home/fb31/projects/BVS/Experiments_October_14*`; all those targets are gone (checked 01:35Z). The other 3 are relative links inside `Experiments_oct_13` (`../data`, `../code`) that resolve to folders within Others, whose files are in the verified list. Only the link objects are removed. Laptop copy `NOTS_BVS\NOTS_home\projects\BVS\Others` (relocation copy of 2026-10-21): **55,024/55,024 match**. Afterwards one line is appended to the existing `/home/fb31/projects/BVS/README.md` (no new file). |
| A2.1 | `/scratch/fb31/smcbvs_v3_deploy_20261022` (the remainder after A1.1–A1.2) | ≈ 123 MB (123,303,115 B in the 00:52Z list) | ≈ 13,453 + 3 symlinks | Finished jobs' logs and test outputs: prod `attempts/` and `slurm/` of the completed arrays 2365494/2365495; readiness/test runs rdy_A, rdy_B, tinyp, smoke, c4test, e2e; A_build n0 logs; n0_20261023; `claude_readiness_evidence.tar.gz`; `.transfer*` bookkeeping. The 3 links are test aliases inside rdy_A. | Pulled whole to `NOTS_BVS\smcbvs_v3_deploy_20261022\nots_scratch_remainder_20261029\` and verified per file. Deleted only through the manifest re-check. Receipt in `transfer/receipts/`. |
| A2.2 | `/projects/ml75/fb31/BVS/v3_profiling_20261020` | 70,317,604 B (113 M on disk) | 16,436 + 5 symlinks | v3 profiling (Oct 20–22). Its code is already copied to `SMC_BVS_v3/` (`COPIED_TO_SMC_BVS_v3.md`); the laptop holds only `partC`. It sits on the shared ml75 group quota. The 5 links point to `/scratch/fb31/v3_profiling_20261020/…`, which was relocated on 2026-10-22 (`scr_v3prof_MOVED.md`). | Pulled whole to `NOTS_BVS\NOTS_projects_ml75\BVS\v3_profiling_20261020\`, verified, then deleted through the manifest re-check. A `v3_profiling_20261020_MOVED.md` pointer is left in `/projects/ml75/fb31/BVS/`, as the earlier relocation did. |
| A3 | `/tmp/fb31_ops_20261028/` and `/tmp/fb31_ops_20261028.tgz` on loginx2 | 3.7 MB tgz | 23 list files | OPS's own temporary hash bundle, created by `evidence/inv3.sh` at 00:56Z | **Already removed** at 01:09Z by the explicit `rm -rf /tmp/fb31_ops_20261028 /tmp/fb31_ops_20261028.tgz` in the scaffold command (no wildcard). Its contents survive locally as `evidence/nots_hashes/` (23 files). |

Expected effect on the home quota: about −0.46 GB (A1.3 only); every other item is on scratch or projects.

## Class B: needs Felipe's OK (listed only; nothing done)

**Home (the 10 GB quota stands at 9.30 GiB; the campaign guard refuses everything above 9 GB):**
| Path | Size | Why it matters / suggestion |
|---|---|---|
| `~/.vscode-server` | 4.9 G | VS Code remote server. The four old `code-*` builds (126 M) and old `cli/servers/*` versions are regenerable caches; deleting the whole folder only forces a re-download at the next VS Code connect. **Largest single win.** |
| `~/.codex/packages`, `~/.codex/db-backups`, `~/.codex/cache` | 931 M + 165 M + 53 M | Codex CLI install packages and DB backups. Re-installable; the backups are Felipe's call. |
| `~/.claude/remote` | 900 M | Claude CLI remote state. Felipe's call. |
| `~/archive_control` (2026-10-14, 2026-10-15) | 673 M | Unknown project (not BVS by its path). Felipe's call. |
| `~/R` (library 152 M, Dynamic_BQTF_libs 61 M) | 212 M | Personal R libraries, probably for Quant_Reg/BQTF. Keep unless Felipe says otherwise. |
| `~/.cache/pip` | 128 M | pip cache, regenerable. |
| `~/backups/*.tar.gz` | 46 M | Quant_Reg package snapshots of 2026-10-21/22. |
| `~/.t3-recovery/diagnostic-20261022T153145Z` | 12 M | Old T3 diagnostic. |
| `/home/fb31/projects/BVS/SMC_BVS_v3` | 54 M | Code of the v3 deployment. No verified laptop copy (the laptop holds the equivalent sources under `02_Experiments/H_…`, but not byte-checked). Small; keep until CONF says it is not needed. |
| `/home/fb31/projects/BVS/releases` | 4.6 M | Hash-addressed releases; laptop copy VERIFIED 432/432 (`evidence/verify/home_BVS_releases.json`), but negligible and possibly referenced by older code paths; keep. |

**Scratch / projects (not BVS, or the paused relocation):**
| Path | Size | Note |
|---|---|---|
| `/scratch/fb31/qr_data/` | 195 G | Quant_Reg data: inner_individual 121 G (chunks c01–c05, c08–c19 not relocated), inner_individual_S_b0001 71 G, extreme_joint 3.3 G, air_sim_lap 28 M. What remains of the paused relocation; possible partial copies on the laptop are unverified (see RELOCATION_LOG / memory). Scratch purge will eventually remove it. |
| `/scratch/fb31/_relocation_manifests/` | 136 M | Relocation checksum lists and chunk indexes; needed if the qr relocation is resumed. |
| `/scratch/fb31/` loose files (≈ 25, < 1 MB) | — | Sept 29–30 scripts/logs/deploy tarballs (fsb, h1v1, air, k2, sqrtn, uext, spod) and 4 relocation scripts. Not BVS by name. |

## Class C: never touch
- `/projects/ml75/fb31/BVS/bench20261019/` and `/home/fb31/projects/BVS/Benchmarks/`: frozen until `RELOCATION_OK.md` exists (charter §3).
- `/home/fb31/projects/BVS/library_portable/`: read-only R library the frozen benchmark code loads.
- `~/.t3`: the live T3 server's state, shared over NFS by all login nodes. `~/.ssh`, `~/.claude.json`, dotfiles, `~/bin`, `~/lib`, `~/.local`, `~/.config`.
- `/home/fb31/projects/Quant_Reg`, `/home/fb31/projects/Large Prior_ Sims`: Felipe's other projects.
- Every `*_MOVED.md` pointer (relocation bookkeeping).
- `New_Campaign/` scaffolds.
- Other users' files, and anything outside `/home/fb31`, `/scratch/fb31`, `/projects/ml75/fb31`.
