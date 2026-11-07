> **Archive note.** In this archive, "02a" means `02_theory.md` (final state), "02b" means `02b_theory_campaign_history.md` (campaign history), and "REG-A"/"REG-B" or "registry A/B" mean parts A and B of `ID_REGISTRY.md`. Paths like `branch_snapshots/...` and `transcript/...` are relative to this folder.

# 04. Code and files index: every script, result file, branch, PR, thread, worktree and path

Archive of the T3 thread "New BVS Headquarters" (threadId `5e38497d-7dfd-48f9-88e9-b21895922f58`, environmentId `b18966a3-98dd-4510-a488-d5dfb1650daa`, Owls), 2026-11-02 to 2026-11-04. Cite thread positions as `[pos N]`. Statements marked **UNVERIFIED** could not be checked live; **UNCERTAIN** marks conflicting sources. Facts below were checked by read-only `ssh owls` on 2026-11-04 unless a `[pos N]` is given. No secret values appear in this file.

The thread was first titled "Use Claude Credits for Research Repos" (project GH-Bayesian-Variable-Selection, repo `/home/fb31/BVS_GH/Bayesian-Variable-Selection` on Owls); its memory file `hq-and-credit-plan.md` calls it the "New HQ" [pos 1331]. The Claude Code session id of the thread on Owls is `49b55b9d-cdce-4050-97cf-de8dfe77e168` (visible in its scratchpad path `/tmp/claude-71711/-home-fb31-BVS-GH-Bayesian-Variable-Selection/49b55b9d-.../scratchpad`, e.g. [pos 212, 308, 507]).

Contents: 1 Machines and roots; 2 GitHub (repo, PR #1, main commits, every `origin/theory/*` branch, local-only branches); 3 Threads; 4 Scripts and infrastructure the HQ wrote; 5 Result and data files; 6 Credentials and billing facts.

---

## 1. Machines and roots

### 1.1 Owls (`owls.stat.rice.edu`, user `fb31`, 80 cores, shared lab machine)
The HQ thread ran here. Owls is shared and heavily loaded (load average about 600 at the time) [pos 479, 601]; the compute budget for fb31 is at most 8 cores (see 4.3).

| Path | What it is | Notes |
|---|---|---|
| `/home/fb31/BVS_GH/Bayesian-Variable-Selection` | The thread's ORIGINAL working directory (every command in the transcript runs here, e.g. [pos 189, 277, 334]); nested clone, at commit `39db138` per `Docs/HQ/OPS_FACTS.md` [pos 449] | **NO LONGER EXISTS** (`ls /home/fb31/BVS_GH` fails on 2026-11-04). The `/home/fb31/BVS_GH/Docs/...` tree (older pre-campaign docs, [pos 96]) is gone too. How and when it was removed or moved is **UNVERIFIED**. The Claude memory folder keeps the old key `-home-fb31-BVS-GH-Bayesian-Variable-Selection`. |
| `/home/fb31/Bayesian-Variable-Selection` | CURRENT repo clone (220 MB), `main` at `d46ebed`, `origin` = `https://github.com/FbStatsQuant/Bayesian-Variable-Selection` | Holds all local `theory/*`, `t3/*` branches and all T3 worktrees (git metadata in `.git/worktrees/`). `Docs/HQ/OPS_FACTS.md` and `RULES.md` live here (POLICY.md points to it). |
| `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/*` | T3 worktrees of delegated agents and threads | 29 worktrees listed in 1.2. |
| `/home/fb31/.config/bvs-hq/` (764 KB, mode 700) | HQ private config and tools | `launch_cloud.sh` (1,597 B), `launch_api.sh` (1,989 B), `cloud_sessions.log` (23 lines = 23 cloud sessions), `gh_token` (secret, 93 B), `api/anthropic_key` (secret, 106 B), `inputs/Local_to_Global_draft.pdf` + `.txt` (Felipe's first draft, "Local-to-Global Bayesian Computation", [pos 484]), `owls/` (below). File names only were listed; contents of secrets were not read. |
| `/home/fb31/.config/bvs-hq/owls/` | OWLS-STEWARD guardrails | `owls_run` (3.4 KB), `owls_guard.sh` (1.2 KB), `owls_tool.py` (14.6 KB), `POLICY.md` (5.2 KB), `env.sh`, `status.json`, `guard.log` (294 KB), `jobs.log` (136 KB), `guard.pid`, `running/`, lock files. |
| `/home/fb31/.claude-personal/projects/-home-fb31-BVS-GH-Bayesian-Variable-Selection/memory/` | HQ memory files (Claude Personal config) | `MEMORY.md`, `hq-and-credit-plan.md` [pos 36], `autonomy-after-target-approval.md` [pos 160, 165], `owls-resource-rules.md` [pos 473], `agent-account-model-defaults.md` [pos 810], `agent-meeting-format.md`, `biometrika-first-target.md`, `control-over-speed.md`, `per-theorem-hq-architecture.md`, `project-objective-parallel.md`, `provable-or-nothing.md`. Sibling dirs under `.claude-personal/projects/` belong to worktrees (`...t3-<hash>`) and to `-home-fb31-fresh-eyes-fable`. |
| `/home/fb31/api_workers` (2.1 GB) | Agent SDK worker area | `sdk_worker.py`, `.venv/`, `.claude-api-config/`, `launches.log` (20 lines), per-task git worktree `<ID>/`, `<ID>.log`, `<ID>.prompt` (+ `.resume.*`) for ABL-START, API-AUDIT, API-FAVIID, API-MASKZPIP, API-N200, API-POS, API-PXNGAP, API-RESID, API-T26BUD, API-VSTAB, LIT-MCMC, LIT-PAR, LIT-SMC, LIT-STAT, LIT-VENUE, METH-AUDIT, THM-INV, THM-SYNTH; also `METH-AUDIT-designs23.out`, `sdktest/`. |
| `/home/fb31/ablconf_work` (104 MB) | ABL-CONF confirmatory fits | `checkout/` (detached worktree at `7e12cf5`), `core_abl/`, `claims/`, `fits/` (107 files), `launch/` (job .out files, `launches.log`), `logs/`, `progress.log`, `killed.log`, `status/`, `DEVIATIONS.md`, `smoke_A.rds`, `tmp/`. |
| `/home/fb31/abl_work` (9.7 MB) | ABL-START (ablation) fits and chair queues | `fits/` (33 files), `core_abl/`, `backfit/`, `chair_q*.out`, `chair2_q*.out`, `chair_queue_*.txt`, `chair2_queue_*.txt`, `owls_q*.out`, `smoke_{A,B,C}.rds`, `progress.log`. |
| `/home/fb31/ls0_work` (2.8 GB) | O-LS0 run on the 2,400 regenerated study datasets | `core_ls0/`, `dev/`, `full/` (jobA, p0500, p1000 shards), `full_lat/`, `pilot/`, `smoke/`, `study/`, `study_mt/`, `agg_final/` (`ls0_per_fit.csv`, `paired_per_fit.csv`), `sels_ledger_per_fit.csv`, `gen_dev_data.R`, `launch.sh`, `run2.sh`, `verify_prod_data_noOct14.R`. |
| `/home/fb31/ma_work` (1.8 MB) | METH-AUDIT core | `core_ma/`. |
| `/home/fb31/hq_reviews` (112 KB) | Sol 6.1 reviewers' output [pos 1409, 1578] | `SOL1_proof_check.md`, `SOL2_audit.md`, `HQ_DISPOSITIONS.md` (written by the HQ, file_change [pos 1475]), `sol1_scripts/` (`check_claims.py`, `check_results.json`), `sol2_scripts/`. |
| `/home/fb31/fresh_eyes` (980 KB) | Isolated folders for the fresh-eyes round 0 [pos 1386, 1394, 1568] | `packet/` (BRIEF.md, METHOD_v3.md, METHOD_v3.1_ADDITIONS.md, code/), `fable/` and `astra/` (each: BRIEF.md, METHOD_v3.md, METHOD_v3.1_ADDITIONS.md, code/, THEORY_PLAN.md). `packet/BRIEF.md` and `packet/METHOD_v3.1_ADDITIONS.md` were written by the HQ (file_change [pos 1389, 1391]). |
| `/home/fb31/api_audit_work` (15 MB) | API-AUDIT code-audit scratch | `core_fp/`, `core_ld/`, compile and run logs, `thr_table.csv`. |
| `/home/fb31/campaign_inbox` (133 MB) | Transfer inbox from the laptop crew (GH-PACK / OPS), seen at [pos 376] | `Lean/`, `_lean_work/`, `projects/`. |
| `/home/fb31/campaign_transfer` (1.3 MB) | Transfer manifest and watchers | `filelist.txt`, `MANIFEST.sha256`, `push_retry.sh`, `seen_*.txt`, `update1/`, `wait_*.sh`. |
| `/home/fb31/theory_campaign` (25 MB) | Stray directory with subfolders `A-REV3 A-REV4 A-REV5 A-REV7 A-REV8` (probably working copies of Astra reviews written outside git) | Purpose **UNVERIFIED**. |
| `/home/fb31/OWLS_BVS_MOVED.md` | Note dated 2026-10-22/23: "BVS project moved off Owls ... lives on NOTS only; the laptop holds the full archive" [pos 376] | Old `~/smcbvs_v3_deploy_20261022/` (9,559 files, 757,608,226 B) and `~/BVS/` (203,658 files) were deleted from Owls after sha256 verification; copies on the laptop at `C:\Users\felip\Documents\NOTS_BVS\Owls_home\...`, code/scripts on NOTS at `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/`. |
| `/home/fb31/Bayesian-Nonparametric-Lean-Library`, `/home/fb31/lean`, `/home/fb31/.elan` | Separate Lean project clone and toolchain (the old Lean campaign). The only SSH key on Owls (`id_ed25519_bnp_deploy`) is a deploy key for that Lean repo, not for BVS [pos 205] | Not part of this campaign. |
| `/tmp/claude-71711/...` | HQ scratch (prompts, NEXT_TASKS copy, cloud test output) | Ephemeral. |

### 1.2 Owls worktrees (`git worktree list` in `/home/fb31/Bayesian-Variable-Selection`, 2026-11-04)
Root `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/`:

| Worktree dir | Branch (tip) | Task |
|---|---|---|
| `campaign` | `theory/campaign` (401a613) | HQ ledger worktree |
| `t3-0e18a33f` | `theory/LH-LOCK` (581e4ba) | LH-LOCK (failed) |
| `t3-147b528e` | `theory/O-SWAP` (5adb21a) | O-SWAP (Owls copy) |
| `t3-2138bde7` | `theory/S-REGISTRY` (1540bb3) | S-REGISTRY |
| `t3-2c070586` | `theory/O-LS0` (d9b3d31) | O-LS0 |
| `t3-2c50ca8d` | `theory/A-DRAFT` (dbf47f7) | A-DRAFT |
| `t3-3b32d183` | `theory/A-REV1` (26815e8) | A-REV1 |
| `t3-4173f9f8` | `theory/S-PAPER` (556be30) | S-PAPER |
| `t3-58e249fb` | detached at `c20059d` | N9-KERNEL (its session jsonl is under `~/.claude/projects/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-t3-58e249fb/`, [pos 1524]) |
| `t3-5b84b7ab` | `theory/F-SHARE` (e05b832) | F-SHARE (Owls copy) |
| `t3-76b20e33` | `t3/refine-theory-confidence-cards-1` (db708ca) | F-REFINE |
| `t3-82162602` | `theory/MEET-THM-REG` (b160085) | registrar |
| `t3-82988d67` | `theory/F-DRAFT` (4de6e4c) | F-DRAFT |
| `t3-8660d5af` | `theory/O-CERT` (ff42c70) | O-CERT (Owls copy) |
| `t3-95809045` | `o-ls0-wrap` (02348e2) | O-LS0-WRAP |
| `t3-b2362d00` | `theory/F-REFINE` (e05b832) | F-REFINE |
| `t3-b8c44b19` | `t3/b8c44b19` (e05b832) | unnamed early T3 branch |
| `t3-c3e3cc0e` | `theory/ABL-CONF` (c0730fe, local) | ABL-CONF |
| `t3-c4af14f4` | `t3/review-smc-bvs-proofs` (00c7b34) | A-REV1/A-REV2 era |
| `t3-cb149a9d` | `theory/A-REV2` (09dc230) | A-REV2 |
| `t3-ce42a416` | `theory/T38-RECORD` (c785bc0) | T38-RECORD |
| `t3-d52f81e9` | `theory/O-BGIBBS` (432fb12, local) | O-BGIBBS (Owls copy) |
| `t3-d5a7a1ad` | `t3/masked-delivery-theorem-1` (56b401f) | F-SHARE |
| `t3-de01d90c` | `o-ls0` (2471709) | O-LS0 |
| `t3-ebcba51c` | `theory/F-PXN` (e05b832) | F-PXN (cancelled) |
| `t3-ebd7fab9` | `theory/O-WSTAB` (e309e14) | O-WSTAB (Owls copy) |
| `t3-f88c0e0b` | `theory/E-SPINE` (cec1680) | E-SPINE (PR #1) |
| `theory-MEET-THM` | `theory/MEET-THM` (37b4d2b) | theorem meeting chair worktree |
| `theory-MEET-v31` | `theory/MEET-v31` (e82e097) | method meeting chair worktree |

Worktrees of the same repo outside `.t3`: `/home/fb31/ablconf_work/checkout` (detached `7e12cf5`) and `/home/fb31/api_workers/<ID>` for the API-credit workers (the first nine were printed by `git worktree list`: ABL-START, API-AUDIT, API-FAVIID, API-MASKZPIP, API-N200, API-POS, API-PXNGAP, API-RESID, API-T26BUD; my output was cut after that, so API-VSTAB, LIT-*, METH-AUDIT, THM-INV, THM-SYNTH are expected to be listed too, **UNVERIFIED**).

### 1.3 Laptop (T3 environment `Felipe_Bedoya`, environmentId `07f21594-c641-48b4-bc5c-855d308c3a55`)
- Felipe's Windows PC, linked to the Owls HQ as `Felipe_Bedoya` (`t3_environment_links`: reachable [pos 133], unreachable [pos 609]; link expires 2026-11-29; access full-access).
- T3 project "GH-Bayesian-Variable-Selection", projectId `6166e65d-e15a-44a5-8b37-6f52805b50e4`, workspaceRoot `C:\Users\felip\OneDrive - Rice University\Bayesian-Variable-Selection` [pos 628]. All 28 laptop agent threads (3.2) use it.
- Other laptop T3 projects seen [pos 628]: "SMC_BVS" (`a0e5df41-d3c9-402c-a6b7-f3cc36a6fb9f`, `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian`; the old HQ's project; holds `00_Admin/OWLS_MIGRATION.md` [pos 376]), "Lean_4", "Large Prior", "Quantile Regression", "(Old) GH-Bayesian-Nonparametric-Lean-Library".
- Archives on the laptop: `C:\Users\felip\Documents\NOTS_BVS\Owls_home\...` (the pre-2026-10-23 Owls home), the PC copy of study data "OneDrive NOTS Data/New_Campaign" (OPS_FACTS [pos 449]), and the per-island `pip_r`/`log_Z_r` study bundles needed for the full PIP rescoring [pos 1249].
- The Owls environment has its own project also called GH-Bayesian-Variable-Selection, projectId `58858238-933d-4ae9-bac2-213d20df8897` (used by the two meeting launches [pos 1197, 1576, 1600]).

### 1.4 NOTS (Rice CRC cluster, user `fb31`)
Reached only through the PC (the PC's T3 server connects over ssh to login node `loginx2`; the HQ on Owls has no working `nots` alias, ssh fails host-key verification [pos 1179, 1208]). A T3 link request to NOTS was sent [pos 1193, `t3_environment_link` hint `nots`, status pending]; Felipe was told to Cancel it as impossible [pos 1208]. Paths named in the thread:
- `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/` (code/scripts, 1,555 files) [pos 376]; `/home/fb31/projects/BVS/library_portable` (read-only R library) [pos 449]; planned `/home/fb31/projects/BVS/LS0_20261102/` (Slurm, not used) [pos 474].
- `/scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_*/results/` (per-island `pip_r`, `log_Z_r` of the 2,394 completed fits) [pos 1249]; `/scratch/fb31/New_Campaign/` (bulk output, purgeable) [POLICY.md].
- Facts and rules: `Docs/HQ/OPS_FACTS.md` (printed [pos 449]): ssh alias `nots`, one connection at a time, back off 15 min after a timeout; Slurm partitions `commons` (1 d), `long` (3 d), `scavenge`, `debug`; always `--mem`; `module load GCC/13.2.0 R/4.4.1`. `squeue -u fb31` shows all of Felipe's jobs, so cancel by job id. The `OPS` thread (on the PC) is the only thread meant to connect to NOTS.

### 1.5 Cloud sessions (claude.ai/code, Felipe's Personal account)
- Cloud environment id `env_01FmvuGCAsZuzPTGX6T1Qyjv` (every `RemoteTrigger` create [pos 70, 220-231]); repo source `https://github.com/FbStatsQuant/Bayesian-Variable-Selection`.
- Routines page: https://claude.ai/code/routines [pos 296]. Routine sessions have a lightning prefix in the title and do not show in the normal sidebar list.
- Session URLs (waves 2-8 are in `~/.config/bvs-hq/cloud_sessions.log`; wave 1 URLs only in [pos 296]):

| Wave | Task | Session URL | Pos |
|---|---|---|---|
| 1 (routine) | W1-T03R | https://claude.ai/code/session_01PQxfr1MSAv7byTHr3nX3sG | 296 |
| 1 | W1-T24G | https://claude.ai/code/session_01PQxfqzmXEyVnKma3aUtjfU | 296 |
| 1 | W1-EXP | https://claude.ai/code/session_01PQxfr2kvLVPmtcwd1xMrKb | 296 |
| 1 | W1-T38E | https://claude.ai/code/session_01PQxfqyZuDC99AbQujAFeVW | 296 |
| 1 | W1-T37R | https://claude.ai/code/session_01PQxfqzF8dSxCm6GLU47j4y | 296 |
| 2 | W2-VT24G | https://claude.ai/code/session_01PQxfqySzkCD7fJxcQ16eHT | 334 |
| 2 | W2-VT03R | https://claude.ai/code/session_01PQxfr3wMBDPm1AJwRgZsmz | 334 |
| 2 | W2-PREM | https://claude.ai/code/session_01PQxfr1ST3w5Mbz1YDufpUz | 334 |
| 2 | W2-T26 | https://claude.ai/code/session_01PQxfr1MVeeqhgqNtppfaVU | 334 |
| 2 | W2-BOOK | https://claude.ai/code/session_01PQxfr2ZraGSVTmp9m1RxzE | 334 |
| 3 | W3-VT37R | https://claude.ai/code/session_01PQxfqzxWYPwNVkWrHY35WD | 352 |
| 3 | W3-VT38E | https://claude.ai/code/session_01PQxfr2yPS6HtgeUMUXxxxW | 352 |
| 3 | W3-VEXP | https://claude.ai/code/session_01PQxfqzbTFigWzgzVLBarjG | 352 |
| 3 | W3-PXN | https://claude.ai/code/session_01PQxfqzMRuTfx7CzfyBXYqN | 352 |
| 3 | W3-PGD | https://claude.ai/code/session_01PQxfqzyBxybg1PmiQ8ArGV | 352 |
| 4 | W4-T38FULL | https://claude.ai/code/session_01PQxfr1cL8HeqHFQByyL3d6 | 364 |
| 4 | W4-SHARE | https://claude.ai/code/session_01PQxfr1KEij3VZnXo21EK9P | 364 |
| 5 | W5-VMASK | https://claude.ai/code/session_01PQxfr1UkxivwQGK29oMVyD | 508 |
| 5 | W5-VPGD | https://claude.ai/code/session_01PQxfr123rsxcuwsq46tiKG | 508 |
| 5 | W5-B2ENV | https://claude.ai/code/session_01PQxfqyi9pEcG1APKEWPpTD | 508 |
| 5 | W5-FAVIID | https://claude.ai/code/session_01PQxfqzyQrh7CJxBJDd6AoC | 508 |
| 5 | W5-LOCKBOOK | https://claude.ai/code/session_01PQxfqzKN8LGwTayhPKe8TW | 508 |
| 6 | W6-FIXREV1 | https://claude.ai/code/session_01PQxfr1AFEQQ4ctNTFVtCz7 | 558 |
| 6 | W6-FIXREV2 | https://claude.ai/code/session_01PQxfr36hxCXHP5YNXXdt98 | 569 |
| 7 | W7-SEP | https://claude.ai/code/session_01PQxfr3ARxEeXaZdMPqhPcD | 711 |
| 7 | W7-PART | https://claude.ai/code/session_01PQxfr4EZmFdDcjRdFzmmfA | 711 |
| 7 | W7-SEC | https://claude.ai/code/session_01PQxfr11GDzaEEnADmjHJWJ | 711 |
| 8 | W8-SYNTH | https://claude.ai/code/session_01PQxfr3bmCnTyRbCZY8m9EC | 756 |

  Wave 1 sessions came from routines (`RemoteTrigger`, plan-billed); waves 2-8 were launched with `launch_cloud.sh` via `claude --cloud` (credit-billed). The Pos column is where the URL first appears in an HQ command or message.
- Routine objects: smoke test `trig_01TdWXN5cb4qFMoyjMquAnrs` (created [pos 70], fired twice, e.g. sessions `cse_01PQxfr1MEmWpAdAZ9DtWMjX` [pos 104] and `cse_01PQxfr12c6wzLXX8rTK8ZpU` [pos 217]; branch `theory/smoke-test`, ledger says "delete later"); Wave 1: `trig_0182js57bVQZahQ16SryUbwB` (W1-T37R, [pos 220]), `trig_01WtU11nXb4xuqiFMothspbW` (W1-T24G [226]), `trig_018hmxt6dY6i2rtYjwsxn2Co` (W1-T38E [229]), `trig_013YamuSQR6U3vJGbe9xqP5Z` (W1-T03R [230]), `trig_01NVzjRNzdF3a2T8Gt5vz8f2` (W1-EXP [231]).
- Stray cloud branch `origin/claude/w2-vt24g-research-fdvfkg` (tip `dba6ff4`, same as `theory/W2-VT24G`): auto-created by the W2-VT24G cloud session; no separate snapshot.
- T3 scheduled task created by the HQ: `scheduled-task:874a5a46-925f-4636-b4b5-16e27708be6e`, "HQ wake-up: ABL-CONF fits due + check fresh-eyes threads", once at 2026-11-04T11:30:00Z [pos 1485].

---

## 2. GitHub

### 2.1 Repo and PR #1
- Repo: `FbStatsQuant/Bayesian-Variable-Selection` (public), https://github.com/FbStatsQuant/Bayesian-Variable-Selection. Commits by Felipe/the HQ carry author FelipeBedoyaR1991 `fb31@rice.edu`; cloud sessions commit as "Claude".
- **PR #1**: https://github.com/FbStatsQuant/Bayesian-Variable-Selection/pull/1, head branch `theory/E-SPINE` (tip `cec1680`; two commits over `c4ef0dc`: `dd0ec8a` "Theory docs: replace 'tempering is needed' with 'moving off the start is needed'; record 2026-11-02 decisions", `cec1680` "Amendments note: record campaign-branch commit SHAs"). The spine correction: 7 files, +160/-14: `Docs/PLAN.md`, `Docs/THEORY.md`, `Docs/THEORY_PRIORITIES.md`, `Docs/Theory/AMENDMENTS_20261102.md` (new, 131 lines), `Docs/Theory/one_pagers/{T27,T38,T39}.md`. Snapshot: `branch_snapshots/E-SPINE/`. The HQ linked it with `link_pull_request` [pos 848] and told Felipe "It isn't merged" [pos 850]. On 2026-11-04 `theory/E-SPINE` is NOT an ancestor of `origin/main` and `Docs/Theory/AMENDMENTS_20261102.md` is absent from main (ssh check), so it is still unmerged; the live PR state on GitHub is **UNVERIFIED** (no `gh` on Owls; the stored token was deliberately not used).
- `origin` currently holds 89 refs (`git ls-remote`).

### 2.2 Main commits
| Commit | Date | Message | Role |
|---|---|---|---|
| `aa6099a` | before 2026-10-28 | Repo test | initial commit |
| `39db138` | | Add SMC-BVS v3 scripts, benchmark scripts, papers and Others | state of the old nested clone [pos 449] |
| `eb75737` | | Add results, docs, papers and remaining SMC-BVS/benchmark tooling | `main` when the thread started [pos 34] |
| `c4ef0dc` | 2026-11-02 | Transfer | GH-PACK transfer landed [pos 260-263, 277]; adds `Docs/THEORY_PRIORITIES.md`, `Docs/THEORY.md`, `Docs/PLAN.md`, `Docs/Theory/...`, `Docs/HQ/*` (vs `eb75737`: 1283 files, 146,071 insertions [pos 262]). Snapshot `branch_snapshots/main@c4ef0dc/Docs/`. |
| `d46ebed` | 2026-11-03 10:31 -06:00 | "GH-PACK: reviewed doc fixes + pre-push scanner; post-campaign refresh (final results, records D1-D94, PROD_L_BENCH rev2, analysis scripts)" | current `origin/main` (278 files vs `c4ef0dc`); pushed outside this HQ (the string `d46ebed` never appears in the thread). |

### 2.3 Every `origin/theory/*` branch (84 branches including `campaign`)
Tips/dates fetched live from Owls on 2026-11-04 and equal to `SNAPSHOT_MANIFEST.txt` tips for every branch except `MEET-THM-REG` (no snapshot dir). Dates are the last commit in UTC. Agent/model/account come from the ledger (`branch_snapshots/campaign/LEDGER.md`), the `delegate_task`/`t3_thread_launch` inputs and HQ messages. Account key: CP = Claude Personal (provider instance `claudeAgent_personal` on Owls), CW = Claude Work (`claudeAgent` on Owls, `claudeAgent_claude_work` on the laptop); "Agent SDK" = API promotional credit (section 6). Per-file hashes: `SNAPSHOT_MANIFEST.txt`. Families: W1-W8 = cloud Opus waves; F-/O-/A-/S-/L-/E-/T38- = plan-funded agents; API-/LIT-/METH-AUDIT/THM-/ABL-START = Agent SDK workers; MEET-*, N9-KERNEL, ABL-CONF = subscription (CW) method/theorem-meeting work. Costs in parentheses are ledger readings, not independently verified.

| ID | tip (origin) | last commit (UTC) | agent / model / account | what it produced | key files (under `branch_snapshots/<ID>/`) |
|---|---|---|---|---|---|
| campaign | `401a613` | 11-04 11:31Z | HQ (Opus 5.5 thread, Owls) | shared campaign branch: PROTOCOL.md, LEDGER.md, tasks/*.md specs, HQ/SR_AUDIT.md, inputs/ PDFs; tip is the last ledger commit | `LEDGER.md`, `PROTOCOL.md`, `HQ/SR_AUDIT.md`, `tasks/ABL-CONF.md`, `tasks/ABL-START.md` (+47 more md/tex) |
| A-DRAFT | `dbf47f7` | 11-02 18:57Z | GPT-6 Astra high (Codex), Owls | novelty, E[h] consistency, naive-merge failure for the first draft | `REPORT.md` |
| A-REV1 | `26815e8` | 11-02 18:44Z | GPT-6 Astra high (Codex), Owls | cross-family review of Theorem B, T38(b)-R, D2 | `REVIEW.md` |
| A-REV2 | `09dc230` | 11-02 18:45Z | GPT-6 Astra high (Codex), Owls | cross-family review of T03-sharp, refined T37, EXP-prime | `REVIEW.md`, `SOURCES.md` |
| A-REV3 | `522d83d` | 11-02 19:29Z | GPT-6 Astra high, laptop mcp:launch:2b9ff443 | review of W3-PXN, W4-SHARE, Prop M | `REVIEW.md`, `snapshots/EXP_PROOF.md`, `snapshots/T37_PROOF.md`, `snapshots/T38_PROOF.md`, `snapshots/W3_PROOF.md` (+2 more md/tex) |
| A-REV4 | `b95948c` | 11-02 19:25Z | GPT-6 Astra high, laptop mcp:launch:787f113a | review of T26, Prop 2/Lemma RO, draft results | `REVIEW.md`, `snapshots/A-DRAFT_REPORT.md`, `snapshots/COLLECTED_PROOFS_v2.tex`, `snapshots/LOCKED_PROOFS.md`, `snapshots/W2-BOOK_PROOF.md` (+19 more md/tex) |
| A-REV5 | `189770c` | 11-02 21:19Z | GPT-6 Astra high, laptop mcp:launch:382beca1 | re-review of repairs to A-REV1/2 findings; LOCKABLE list | `REVIEW.md`, `REV1_CHECK.md`, `REV2_CHECK.md` |
| A-REV6 | `02d6a4a` | 11-02 21:17Z | GPT-6 Astra high, laptop mcp:launch:7620de24 | re-review of repairs to A-REV3/4 findings | `REVIEW.md`, `sources/A-DRAFT__REPORT.md`, `sources/A-REV3__REVIEW.md`, `sources/A-REV3__snapshots__EXP_PROOF.md`, `sources/A-REV3__snapshots__T37_PROOF.md` (+90 more md/tex) |
| A-REV7 | `70eadf3` | 11-02 21:20Z | GPT-6 Astra high, laptop mcp:launch:e0a5f1f8 | review of no-LS0 masked routes (BG3, F1/F2, D2-LH/B2-LH, Prop GU); STAB-LH certificate | `REVIEW.md` |
| A-REV8 | `6417192` | 11-02 21:24Z | GPT-6 Astra high, laptop mcp:launch:3602f479 | review of the LS0 masked route | `REVIEW.md`, `sources/A-REV1__REVIEW.md`, `sources/A-REV3__REVIEW.md`, `sources/LOCKED_PROOFS.md`, `sources/O-LS0__REPORT.md` (+15 more md/tex) |
| A-REV9 | `bbadda3` | 11-02 21:23Z | GPT-6 Astra high, laptop mcp:launch:c9dc46bd | review of the new supplement results | `REVIEW.md`, `sources/F-MASKPIP_REPORT.md`, `sources/O-CERT_REPORT.md`, `sources/O-DILUTE_REPORT.md`, `sources/O-PW2_REPORT.md` (+15 more md/tex) |
| ABL-CONF | `7e12cf5` | 11-04 11:31Z | Opus 5.5 high, CW (delegate_task pos 1431) | pre-registered confirmatory start test; 118 fits; PREREG, RUNBOOK, REPORT | `PREREG.md`, `REPORT.md`, `RUNBOOK.md` |
| ABL-START | `0cc3789` | 11-03 17:30Z | Opus 5.5, Agent SDK, $12 cap | block start vs singleton blocks vs prior start ablation (Owls); worker exited early, HQ/chair ran the remaining fits | `REPORT.md` |
| API-AUDIT | `966e713` | 11-02 23:28Z | Opus 5.5, Agent SDK, $12 (+ resume) | code audit of SR, GUARD, emit_centre, scan-before-limit, IND-T | `REPORT.md`, `AUDIT.md`, `NOTES.md` |
| API-FAVIID | `4a1835d` | 11-02 21:32Z | Opus 5.5 high, Agent SDK, $15 | audit of favourable-rate claims | `REFEREE_HANDOFF.md`, `REPORT.md`, `W5-FAVIID_REPORT_AMENDED.md` |
| API-MASKZPIP | `1200e63` | 11-02 21:53Z | Opus 5.5, Agent SDK, $15 | two-sided masked-regime Z-hat / PIP accuracy | `PROOF.md`, `REPORT.md` |
| API-N200 | `453117a` | 11-02 21:42Z | Fable 5.1, Agent SDK, $25 | Theorem N200 vs the study's n=200 counts | `PROOF.md`, `REPORT.md`, `results/n200_table.md` |
| API-POS | `4819b93` | 11-02 21:41Z | Opus 5.5, Agent SDK, $10 | positioning vs rapid-mixing literature | `REPORT.md`, `NOTES.md`, `results/cond1_lh.md` |
| API-PXNGAP | `c535beb` | 11-02 21:57Z | Fable 5.1, Agent SDK, $25 | Thm 5(b1) with LS0 on LH-iid incl. p >> n | `PROOF.md`, `REPORT.md`, `PLAN.md` |
| API-RESID | `66e1da7` | 11-02 23:40Z | Opus 5.5 high, Agent SDK, API credit, $15 cap (+ resume run, $6 cap) | start tables recomputed from saved fits (RESID-STEP0) | `REPORT.md`, `results/extra_tables.md`, `results/sweeps_tables.md`, `results/tables.md` |
| API-T26BUD | `2ac43ac` | 11-02 21:56Z | Opus 5.5, Agent SDK, $12 | Theorem G (stage count), T26 with proved stage count | `PROOF.md`, `REPORT.md`, `results/realised_T_summary.md` |
| API-VSTAB | `ba9507f` | 11-02 21:50Z | Opus 5.5, Agent SDK, $12 | Claude check of A-REV7 STAB-LH certificate | `REPORT.md` |
| E-SPINE | `cec1680` | 11-02 21:16Z | Opus 5.5 high, CW, Owls | PR #1: "tempering is needed" -> "moving off the start is needed" in Docs | `Docs/PLAN.md`, `Docs/THEORY.md`, `Docs/THEORY_PRIORITIES.md` |
| F-DRAFT | `4de6e4c` | 11-02 18:57Z | Fable 5.1 high, CP, Owls | crosswalk of Felipe's first draft; NEW_TARGETS.md | `CROSSWALK.md`, `NEW_TARGETS.md` |
| F-MASKPIP | `dbe45fa` | 11-02 20:00Z | Fable 5.1 high, CP, laptop thread mcp:launch:96085453 | what Z-hat and PIPs mean in masked regime | `REPORT.md`, `HELPER_BRIEF_SIM.md`, `results/SIM_NOTES.md`, `results/summary.md` |
| F-REFEREE | `fae6b7f` | 11-02 19:51Z | Fable 5.1 high, CP, laptop thread mcp:launch:04ab8d7c | hostile JRSS-B referee report + response plan | `REFEREE_REPORT.md`, `RESPONSE_PLAN.md` |
| F-REFINE | `450df6e` | 11-02 21:16Z | Fable 5.1 xhigh, CP, Owls | CARDS.md, ARCHITECTURE.md, NEXT_TASKS.md (P6 believed versions) | `CARDS.md`, `ARCHITECTURE.md`, `NEXT_TASKS.md` |
| F-SHARE | `13bc665` | 11-02 20:06Z | Fable 5.1 xhigh, Claude Personal (CP); Owls delegate, then laptop thread mcp:launch:1306a77e | delivery theorem for route (b2) in masked regime | `PROOF.md`, `REPORT.md`, `BRIEF.md` |
| F-SIGMA | `e2a3481` | 11-02 19:54Z | Fable 5.1 high, CP, laptop thread mcp:launch:00e29d07 | theory of the common-sigma^2 start | `REPORT.md` |
| L-LEAN | `cfa78ed` | 11-02 20:35Z | Opus 5.5, CW, laptop mcp:launch:3734388b | Lean 4 formalisation (ledger: 101 declarations, 0 sorry) | `REPORT.md`, `ADVISER_DECISIONS.md`, `ASSUMPTIONS.md`, `DECL_STATUS.md`, `FAILED_ATTEMPTS.md` (+9 more md/tex) |
| LIT-MCMC | `8f12b8e` | 11-02 23:38Z | Opus 5.5, Agent SDK, $8 | BVS-MCMC mixing literature | `REPORT.md`, `NOTES.md`, `results/ob_check.md`, `results/rz_lh.md` |
| LIT-PAR | `cf4a9d9` | 11-03 13:19Z | Opus 5.5, Agent SDK, $10 | tries to falsify the "parallel + robust + guaranteed" gap claim | `REPORT.md`, `notes/01_local_papers.md`, `notes/02_feature_splitting.md`, `notes/03_parallel_smc_depth.md`, `notes/04_datasplit_scalable_bvs.md` (+5 more md/tex) |
| LIT-SMC | `c10f0ad` | 11-02 23:36Z | Opus 5.5, Agent SDK, $8 | SMC-sampler literature vs our results | `REPORT.md`, `NOTES.md` |
| LIT-STAT | `61caccc` | 11-02 23:37Z | Opus 5.5, Agent SDK, $8 | statistical literature (concentration, selection) | `REPORT.md`, `notes/00_PLAN.md`, `notes/01_CSvdV_YWJ.md`, `notes/02_JR_SBJ_Rossell_NH.md`, `notes/03_decision_sizeprior.md` (+2 more md/tex) |
| LIT-VENUE | `294717d` | 11-02 23:37Z | Opus 5.5, Agent SDK, $8 | venue/novelty survey | `REPORT.md`, `NOTES.md` |
| MEET-THM | `37b4d2b` | 11-04 05:29Z | Chair Opus 5.5 CW (thread "Theorems - Final meeting", second launch) + seats | theorem meeting: THEOREM_LIST_FINAL.md, MINUTES, NOTATION, FUTURE_WORK, HQ_CHARTERS | `MINUTES.md`, `REGISTRY_PAPER1.md`, `THEOREM_LIST_FINAL.md`, `AMENDMENT_HQ_02_DEFINITIONS.md`, `CHAIR_BRIEF.md` (+55 more md/tex) |
| MEET-THM-REG | `b160085` | 11-04 01:03Z | Sonnet 5.5 registrar, CW (delegate_task pos 1446) | inherited-results index for MEET-THM (ledger: 24 draft entries, 166 cited IDs) | (no snapshot dir) |
| MEET-v31 | `e82e097` | 11-04 11:31Z | Chair Opus 5.5 high CW (thread "Methodology - Final meeting") + seats; later HQ amendments | method meeting: METHOD_v3.1_FINAL.md, MINUTES, evidence/ | `METHOD_v3.1_FINAL.md`, `MINUTES.md`, `AMENDMENT_HQ_01.md`, `AMENDMENT_HQ_02.md`, `AMENDMENT_HQ_02_DEFINITIONS_from_MEET-THM.md` (+22 more md/tex) |
| METH-AUDIT | `96464ae` | 11-03 13:53Z | Opus 5.5, Agent SDK, $15 cap (ledger: cost $5.89) | is v3 parallel-friendly; concurrency re-runs | `PROOFS.md`, `REPORT.md` |
| N9-KERNEL | `c20059d` | 11-04 01:33Z | Opus 5.5 high, CW (delegate_task pos 1457) | kernel reversibility / round self-adjointness / exact start sampler vs production code | `PROOF.md`, `REPORT.md`, `CHECK.md`, `HQ_NOTE.md` |
| O-BGIBBS | `55679ee` | 11-02 19:54Z | Opus 5.5, CP, Owls then laptop mcp:launch:ac5a82ce | bridge-Gibbs discovery: Theorems BG1-BG3 (no-LS0 masked, LH) | `REPORT.md` |
| O-CERT | `332bf3e` | 11-02 20:45Z | Opus 5.5, CP, Owls then laptop mcp:launch:f68ac0f9 | a-posteriori finite-n certificates | `REPORT.md` |
| O-DILUTE | `abedf99` | 11-02 19:57Z | Opus 5.5, CP, Owls then laptop mcp:launch:31d5000e | finite-n theory of start masking (dilution) | `REPORT.md`, `THEORY.md` |
| O-LS0 | `02348e2` | 11-02 20:24Z | Opus 5.5 xhigh/light, CP, Owls (+ O-LS0-WRAP Opus CW) | LS0 local-search check on the 2,400 regenerated study fits; ledger: PASSED (0/2,394 HPM changes) | `REPORT.md`, `results/report_tables.md`, `results/tables.md` |
| O-MIX | `26b7708` | 11-02 19:35Z | Opus 5.5, CP, laptop mcp:launch:19eacc2b | LS0 vs mixture of block starts vs common sigma^2 | `REPORT.md` |
| O-PW2 | `e685ead` | 11-02 19:37Z | Opus 5.5, CP, laptop mcp:launch:a36022e6 | PW2-free relative-variance bound for Z-hat | `REPORT.md` |
| O-STAGES | `8d3c142` | 11-02 19:52Z | Opus 5.5, CP, laptop mcp:launch:a029f4b2 | realised stage count T_n of the ESS-adaptive grid | `REPORT.md` |
| O-SWAP | `5b9b506` | 11-02 20:03Z | Opus 5.5, CP, Owls then laptop mcp:launch:a9c92fa5 | finite-n theory of posterior-miss rates | `REPORT.md`, `out/TABLES_local.md` |
| O-VCERT | `839bed5` | 11-02 19:50Z | Opus 5.5, CP, laptop mcp:launch:00adbb05 | same-family verification of O-CERT | `REPORT.md` |
| O-WSTAB | `2ec3099` | 11-02 19:59Z | Opus 5.5, CP, Owls then laptop mcp:launch:7fd33c90 | weight stability of the composite start (Theorem W, W-prime) | `PROOF.md`, `REPORT.md`, `review/CHECK_SEP_W.md` |
| S-ELS | `90423b1` | 11-02 19:58Z | Sonnet 5.5, CW, laptop mcp:launch:6fe801ba | E_LS ledger extraction from the fit archive | `REPORT.md` |
| S-PAPER | `e073b69` | 11-02 21:15Z | Sonnet 5.5, CW, Owls | theory_section.tex skeleton with STATUS comments | `theory_section.tex`, `README.md` |
| S-REGISTRY | `3d88da6` | 11-02 19:42Z | Sonnet 5.5, Claude Work (CW), Owls then laptop mcp:launch:06e271c4 | claims REGISTRY.md + LOCKABLE.md | `LOCKABLE.md`, `REGISTRY.md` |
| T38-RECORD | `c785bc0` | 11-02 21:36Z | Opus 5.5 high, CW, Owls | one statement of record for Thm 5 (T38_STATEMENT.md) + REGISTRY_v2 / LOCKABLE_v2 | `LOCKABLE_v2.md`, `REGISTRY_v2.md`, `REPORT.md`, `T38_STATEMENT.md` |
| THM-INV | `440a38d` | 11-03 13:42Z | Opus 5.5, Agent SDK, $12 cap (ledger: cost $7.99) | component-to-theorem inventory | `REPORT.md`, `NOTES.md`, `digests/API.md`, `digests/AREV.md`, `digests/LIT.md` (+3 more md/tex) |
| THM-SYNTH | `fc712e7` | 11-03 16:52Z | Fable 5.1, Agent SDK, $25 cap (ledger: cost $8.4) | 19-item theorem list G1-G6, HQ_PLAN | `REPORT.md`, `HQ_PLAN.md`, `THEOREM_LIST.md` |
| W1-EXP | `722bd18` | 11-02 17:12Z | Opus 5.5, cloud routine, Wave 1 | EXP-prime compatible family carrying T22+T27 | `PROOF.md`, `REPORT.md`, `BRIEF.md` |
| W1-T03R | `7e14d6f` | 11-02 16:56Z | Opus 5.5, cloud routine, Wave 1 | exact BB(1,p) tail in T02(i), restated T03 | `PROOF.md`, `REPORT.md`, `BRIEF.md`, `NOTES.md` |
| W1-T24G | `9e210a3` | 11-02 17:39Z | Opus 5.5, cloud routine, Wave 1 | Gibbs-path terminal repair, restated T24 (Theorem B) | `PROOF.md`, `REPORT.md`, `BRIEF.md`, `NOTES.md` |
| W1-T37R | `3bcc429` | 11-02 17:36Z | Opus 5.5, cloud routine (plan-billed), Wave 1 | restated T37 (truth dominance / greedy repair): Theorem A, TD-prime; Theorems B/C | `PROOF.md`, `REPORT.md`, `BRIEF.md`, `results/exp1_p20_summary.md`, `results/exp1_p25_summary.md` (+2 more md/tex) |
| W1-T38E | `436a712` | 11-02 17:10Z | Opus 5.5, cloud routine, Wave 1 | delivery and eligibility for T38(b); composition | `PROOF.md`, `REPORT.md`, `BRIEF.md` |
| W2-BOOK | `57eb3d0` | 11-02 17:35Z | Opus 5.5, `claude --cloud` (credit) | bookkeeping restatements T12, T31(i), T07, T21; run/output split | `PROOF.md`, `REPORT.md`, `NOTES.md`, `STATEMENTS.tex` |
| W2-PREM | `988c5f5` | 11-02 18:02Z | Opus 5.5, `claude --cloud` (credit) | discharging the premises of Theorem B | `PROOF.md`, `REPORT.md`, `NOTES.md`, `results/lh_table.md` |
| W2-T26 | `0e4f1e7` | 11-02 17:49Z | Opus 5.5, `claude --cloud` (credit) | T26(i)-(ii) evidence and PIP consistency, favourable regime | `PROOF.md`, `REPORT.md`, `results/premise_summary.md` |
| W2-VT03R | `b9f6d9b` | 11-02 17:40Z | Opus 5.5, `claude --cloud` (credit) | adversarial verification of W1-T03R | `REPORT.md`, `NOTES.md` |
| W2-VT24G | `dba6ff4` | 11-02 17:42Z | Opus 5.5, `claude --cloud` (credit) | adversarial verification of W1-T24G | `PROOF.md`, `REPORT.md`, `NOTES.md` |
| W3-PGD | `fdeaec3` | 11-02 21:04Z | Opus 5.5, `claude --cloud` (credit) | PGD / LD asymptotic hypotheses of refined T37 | `PROOF.md`, `REPORT.md`, `PLAN.md` |
| W3-PXN | `4aebea3` | 11-02 18:13Z | Opus 5.5, `claude --cloud` (credit) | p >> n joint family carrying T38(b) premises | `PROOF.md`, `REPORT.md`, `PLAN.md` |
| W3-VEXP | `7970fa0` | 11-02 17:50Z | Opus 5.5, `claude --cloud` (credit) | referee report on W1-EXP | `REPORT.md`, `NOTES.md`, `REPAIRS.md` |
| W3-VT37R | `4988b96` | 11-02 17:49Z | Opus 5.5, `claude --cloud` (credit) | verification of W1-T37R | `REPORT.md`, `REPAIRS.md`, `results/prod_scale_summary.md` |
| W3-VT38E | `3e4b732` | 11-02 17:55Z | Opus 5.5, `claude --cloud` (credit) | verification of W1-T38E | `REPORT.md`, `NOTES.md` |
| W4-SHARE | `0d3f3fe` | 11-02 18:34Z | Opus 5.5, `claude --cloud` (credit) | delivery to terminal rounds, route (b2) | `PROOF.md`, `REPORT.md`, `NOTES.md` |
| W4-T38FULL | `a0f9cb5` | 11-02 18:15Z | Opus 5.5, `claude --cloud` (credit) | main theorem T38 assembled, paper-ready | `REPORT.md`, `T38_PROOF.md`, `T38_STATEMENT.md`, `NOTES.md` |
| W5-B2ENV | `053511d` | 11-02 19:30Z | Opus 5.5, `claude --cloud` (credit) | no-method-change masked theorems on LH | `PROOF.md`, `REFEREE.md`, `REPORT.md`, `NOTES.md` |
| W5-FAVIID | `31695b1` | 11-02 20:24Z | Opus 5.5, `claude --cloud` (credit) | 2^B-free favourable-regime start rate on iid designs | `PROOF.md`, `REPORT.md`, `PLAN.md` |
| W5-LOCKBOOK | `a65392b` | 11-02 19:00Z | Opus 5.5, `claude --cloud` (credit) | lock the low-risk half (LOCKABLE bookkeeping) | `PROOF.md`, `REPORT.md`, `AUDIT.md`, `NOTES.md`, `STATEMENTS.tex` |
| W5-VMASK | `4e41b97` | 11-02 19:11Z | Opus 5.5, `claude --cloud` (credit) | verification of masked-regime instance of T38 | `REPORT.md`, `PLAN.md`, `REPAIRS.md` |
| W5-VPGD | `8e2bbc4` | 11-02 20:44Z | Opus 5.5, `claude --cloud` (credit) | verification/completion of Theorem W (Thm 3(iii)) | `REFEREE.md`, `REPORT.md`, `PLAN.md`, `REPAIRS.md`, `STAR.md` (+1 more md/tex) |
| W6-FIXREV1 | `a7833f3` | 11-02 19:06Z | Opus 5.5, `claude --cloud` (credit) | applies A-REV1 findings to Theorem B / T38 package | `REPORT.md`, `T38_PROOF.md`, `T38_STATEMENT.md`, `CONSOLIDATED.md` |
| W6-FIXREV2 | `be2d456` | 11-02 19:07Z | Opus 5.5, `claude --cloud` (credit) | applies A-REV2 findings to T03-sharp, Theorem A, EXP-prime, Lemma U | `REPORT.md`, `NOTES.md`, `STATEMENTS.md` |
| W7-PART | `b2aa940` | 11-02 20:21Z | Opus 5.5, `claude --cloud` (credit) | partition-recovery lemma, iid Gaussian designs | `PROOF.md`, `REPORT.md` |
| W7-SEC | `7e33e8a` | 11-02 19:55Z | Opus 5.5, `claude --cloud` (credit) | secondary lemmas T05, T33, T32(i) | `PROOF_T05.md`, `PROOF_T33.md`, `REPORT.md`, `NOTES.md` |
| W7-SEP | `858004e` | 11-02 20:21Z | Opus 5.5, `claude --cloud` (credit) | separation theorem: what the tempering bridge buys | `PROOF.md`, `REPORT.md`, `NOTES.md` |
| W8-SYNTH | `6876a9a` | 11-02 20:29Z | Opus 5.5, `claude --cloud` (credit; last credit session) | campaign SYNTHESIS.md + BRIEF.md | `REPORT.md`, `SYNTHESIS.md`, `BRIEF.md`, `README.md`, `SNAPSHOT.md` (+5 more md/tex) |

Notes on the table: (a) MEET-THM-REG (tip `b160085`, 2026-11-03 19:03 -06:00 = 2026-11-04 01:03Z) is on origin but has no snapshot dir; its registrar output (24 draft entries, 166 cited IDs, 37 conflicts per the ledger) is only summarised in `branch_snapshots/campaign/LEDGER.md`. (b) The ABL-CONF row's tip is the final results commit; local `theory/ABL-CONF` is `c0730fe` (RUNBOOK commit), an ancestor. (c) For `MEET-v31` the ledger quotes `c3e18ee` (close), `791e5e3` (AMENDMENT_HQ_01) and `6a80fe5` (AMENDMENT_HQ_02) as intermediate commits; the snapshot is at `e82e097`. For `MEET-THM` the ledger quotes `514c8fc` (close) and `37b4d2b` (Felipe summary); snapshot at `37b4d2b`. (d) `campaign` is the shared base: every task spec lives at `theory_campaign/tasks/<ID>.md` there and API/cloud launchers read the spec from it (`launch_cloud.sh`, `launch_api.sh`).

### 2.4 Local-only and diverged branches on Owls (`/home/fb31/Bayesian-Variable-Selection`)
`git branch --contains` / `merge-base --is-ancestor` checked on 2026-11-04. Nothing below carries content that is not in `origin`, except the two cancelled/failed branches which carry no commits of their own.

| Local branch | Local tip | Status | Where its content lives |
|---|---|---|---|
| `o-ls0` | `2471709` | local only; 3 commits over `theory/campaign` ("O-LS0: aggregator ...") | contained in `origin/theory/O-LS0` |
| `o-ls0-wrap` | `02348e2` | local only; 4 commits ("O-LS0: report (wrap-up by O-LS0-WRAP)") | identical to the tip of `origin/theory/O-LS0` (`02348e2`) |
| `theory/O-LS0` (local) | `d9b3d31` | ancestor of origin | `origin/theory/O-LS0` |
| `theory/F-PXN` | `e05b832` | local only, 0 commits of its own (ledger: cancelled "superseded by W3-PXN" [pos 474]) | ledger-only; the substance is W3-PXN (+ API-PXNGAP) |
| `theory/LH-LOCK` | `581e4ba` | local only, 0 commits of its own: the Fable CW run failed on a 64K-output-token API error before its first commit (ledger 21:55 UTC); not relaunched because A-REV7 refuted general LH locking | ledger-only; successor route API-VSTAB |
| `t3/*` (27 branches: `t3/3b32d183`, `t3/abl-conf`, `t3/aggregate-ls0-report`, `t3/audit-n9-kernel`, `t3/b8c44b19`, `t3/bridge-gibbs-discovery`, `t3/build-claims-registry`, `t3/draft-theory-crosswalk`, `t3/draft-theory-section`, `t3/evaluate-ls0-study`, `t3/finite-fit-certificates`, `t3/finite-n-posterior-miss-rates`, `t3/high-dimensional-joint-theorem`, `t3/ls0-study-datasets`, `t3/masked-delivery-theorem`, `t3/masked-delivery-theorem-1`, `t3/posterior-consistency-audit`, `t3/prove-lh-lock-bg3-theorem`, `t3/prove-start-posterior-divergence`, `t3/refine-theory-confidence-cards`, `t3/refine-theory-confidence-cards-1`, `t3/replace-tempering-necessity-claim`, `t3/review-smc-bvs-proofs`, `t3/review-smc-bvs-proofs-1`, `t3/t38-theorem-record`, `t3/theorem-registry-index`) | various | auto-named T3 worktree branches; every one is contained in some `origin/theory/*` branch (checked with `git branch -r --contains`) | e.g. `t3/refine-theory-confidence-cards-1` (db708ca) in `origin/theory/F-REFINE`; `t3/masked-delivery-theorem-1` (56b401f) in `origin/theory/F-SHARE`; `t3/prove-lh-lock-bg3-theorem` and `t3/t38-theorem-record` (581e4ba) in the A-REV8/A-REV9 history |
| `theory/ABL-CONF` `c0730fe`, `theory/N9-KERNEL` `3338896`, `theory/O-BGIBBS` `432fb12`, `theory/O-CERT` `ff42c70`, `theory/O-SWAP` `5adb21a`, `theory/O-WSTAB` `e309e14`, `theory/F-REFINE` and `theory/F-SHARE` `e05b832`, `theory/S-PAPER` `556be30`, `theory/S-REGISTRY` `1540bb3` | older than origin | strict ancestors of the same-named `origin/theory/*` branch | origin tip (use the table in 2.3) |
| `theory/campaign-base` | not present on 2026-11-04 | transient local branch created [pos 189] to stage the campaign files, replaced by `theory/campaign` [pos 277] | n/a |
| `main` | `d46ebed` | equals `origin/main` | |

Remote-only extra: `origin/claude/w2-vt24g-research-fdvfkg` (see 1.5). Smoke-test branch `theory/smoke-test` is no longer on origin (not in the 2026-11-04 listing).

---

## 3. Threads

### 3.1 The HQ and the old HQ
| Thread | IDs and links exactly as in the transcript | Positions |
|---|---|---|
| This HQ ("New BVS Headquarters", originally "Use Claude Credits for Research Repos") | threadId `5e38497d-7dfd-48f9-88e9-b21895922f58`, environmentId `b18966a3-98dd-4510-a488-d5dfb1650daa` (Owls) | whole thread |
| Old "SMC_BVS Headquarters" (superseded HQ; on the laptop) | thread `mcp:5e4b26e1-e27b-4f82-a11e-f0b274127549`, environment `07f21594-c641-48b4-bc5c-855d308c3a55` (Felipe_Bedoya). Link `<t3-thread://v2/07f21594-c641-48b4-bc5c-855d308c3a55/mcp:5e4b26e1-e27b-4f82-a11e-f0b274127549>`; context ref `t3-context://v1/thread/thread_mcp-5e4b26e1-e27b-4f82-a11e-f0b274127549-072d63595627ee8a` | Felipe names it [pos 12]; first lookup fails [pos 24]; found on the laptop environment [pos 137, 139]; `t3_thread_read` result too large [pos 141]; read for the handoff [pos 142-150]; Felipe relays its NOTS reorganisation [pos 1673]; baseline-rule reference [pos 1155, 1162] |
| GH-PACK crew and OPS / OPS-4 threads (laptop/PC) | named by the old HQ, no ids in this thread. GH-PACK = Opus manager + two Sonnet agents + Haiku copier + Sol reviewer, writes `Docs/THEORY.md`, `Docs/PLAN.md`, `Docs/HQ/` into the repo (decision D70) and screens for secrets before the public push; OPS-4 closed out the p >> n rerun (about 907 core-hours) | [pos 142, 150, 449, 1179] |

### 3.2 Laptop agent threads (environment `07f21594-c641-48b4-bc5c-855d308c3a55`, project `6166e65d-e15a-44a5-8b37-6f52805b50e4`, `t3_thread_launch` with worktree strategy on branch `theory/<ID>` start-from-origin)
The first attempt used `delegate_task` with worktree isolation and failed for all (error: "isolation 'worktree' is not supported there ... use t3_thread_launch with environmentId") [pos 646-652]. `t3_thread_launch` worked [pos 657-658]. Link format: `<t3-thread://v2/07f21594-c641-48b4-bc5c-855d308c3a55/mcp:launch:HEX>`. 23 threads:

| Launch pos | Title (as launched) | Model / account | Full threadId |
|---|---|---|---|
| 657 | F-SHARE (laptop): route b2 delivery crux | Fable 5.1 high, CP | `mcp:launch:1306a77e2a3c9ac297942435f6d03f8f6c2a3304628b0520f5c617e9f1a2a109` |
| 659 | O-WSTAB (laptop): weight stability theorem | Opus 5.5 high, CP | `mcp:launch:7fd33c908496c6bc6f8ed3e1cd3869f1ed4c17dac8378c9e49ad9fd82c546dda` |
| 660 | O-CERT (laptop): finite-n certificates | Opus, CP | `mcp:launch:f68ac0f9cde1deeacba93ac710afbc715385f90aa719be42b64978627857d46d` |
| 661 | O-SWAP (laptop): predict the posterior-miss rates | Opus, CP | `mcp:launch:a9c92fa5046ab8ea8c3cf741fc89dfffbe9f9e341f7b4ccaafeb46457fd97fc5` |
| 662 | O-BGIBBS (laptop): bridge-Gibbs discovery | Opus, CP | `mcp:launch:ac5a82cebf0022aa717598e69e116aa9c6e4147399286323cfd1553d2b6e020f` |
| 663 | O-DILUTE (laptop): finite-n theory of the start masking (base `theory/campaign`) | Opus, CP | `mcp:launch:31d5000e090ea1feb0e30c6c9a479e0f662d436e292fc30e88b1318b75eaa7a2` |
| 664 | S-REGISTRY (laptop): claims registry + LOCKABLE | Sonnet 5.5 high, CW (`claudeAgent_claude_work`) | `mcp:launch:06e271c4f16674916ca49931ceb30a76f7052454fc8deac7adb81e47816f4676` |
| 673 | O-PW2 (laptop): evidence variance bound PW2 | Opus, CP | `mcp:launch:a36022e620f91c13a84e776ab7c618ae84c206d0b45e2593532cd56aef03f0f8` |
| 674 | O-MIX (laptop): mixture of block starts as an alternative to LS0 | Opus, CP | `mcp:launch:19eacc2b761606392e67685287c3e1ccfd7147a5da7515243fc897951d2fc8cd` |
| 675 | F-MASKPIP (laptop): evidence and PIP accuracy in the masked regime | Fable 5.1 high, CP | `mcp:launch:96085453fe4ce0b4533d0757f9c37ee5d2b75a0a68503b11910ced0d728ad3b5` |
| 676 | A-REV3 (laptop): Astra review of W3-PXN, W4-SHARE, Prop M | GPT-6 Astra (Codex) high | `mcp:launch:2b9ff44377dfa769a3f6c880450be97b9c0fe1ba0167d173fbac7741822bd690` |
| 677 | A-REV4 (laptop): Astra review of T26, Prop 2/Lemma RO, draft results | Astra high | `mcp:launch:787f113a02c820a08111b707113fa03943b411eb08c18824b98f9d447cba5247` |
| 714 | L-LEAN (laptop, CW): Lean 4 formalisation of the exact finite results | Opus 5.5, CW | `mcp:launch:3734388bedb9fbe14096ca5662e3fc66ba300f355442417264c49bf24816f15f` |
| 715 | S-ELS (laptop, CW): E_LS ledger extraction from the fit archive | Sonnet 5.5, CW | `mcp:launch:6fe801baeb3a7be93172fd74058a5cd1c2e2e28b504e8d36fe878f2c07206a1d` |
| 726 | F-REFEREE (laptop): adversarial JRSS-B referee report on the theory | Fable 5.1 high, CP | `mcp:launch:04ab8d7c8d3cee8286cb0ad5527009c0642db54f520f787cb2f9918b55ade61c` |
| 727 | F-SIGMA (laptop): theory of the common-sigma^2 start tables | Fable, CP | `mcp:launch:00e29d07f8f87d92d1fdf44ebc597e3d854c024674c53097ff53be1ae8cf99d4` |
| 728 | O-STAGES (laptop): the realised stage count T_n of the ESS-adaptive grid | Opus, CP | `mcp:launch:a029f4b2ff19b62bd32bce79360471e0878dfd5c6d28aed0038b2a50f7a04f6c` |
| 729 | O-VCERT (laptop): adversarial verification of O-CERT | Opus, CP | `mcp:launch:00adbb0a5437bc93f35b490be04e1e9df2a39d93bbafa9a447634f984e0a9317` |
| 801 | A-REV5 (laptop): Astra re-review of repairs to A-REV1/A-REV2 findings | Astra high | `mcp:launch:382beca1e066d8d9e36eb1e0c10091e093494596501deee92feaee64f52f046f` |
| 802 | A-REV6 (laptop): Astra re-review of repairs to A-REV3/A-REV4 findings | Astra high | `mcp:launch:7620de24a202b05e4532ac64c41c01a68005255b4c4d96a9cd0b57897ababa54` |
| 803 | A-REV7 (laptop): Astra review of the no-LS0 masked routes | Astra high | `mcp:launch:e0a5f1f8b9cd1eddb91844943f700046b3d96ae85e55ef5f929382ff71323445` |
| 829 | A-REV8 (laptop): Astra review of the LS0 masked route | Astra high | `mcp:launch:3602f4796a12d0a2eab34032f40f58e9b2f364d8b7341ed6e66ef0978723159e` |
| 830 | A-REV9 (laptop): Astra review of the new supplement results | Astra high | `mcp:launch:c9dc46bd7278df5d75707af46a04f8949a659d0df065623efb15aeff811864be` |

Permission message "you MAY spawn Claude Personal helper agents" was sent with `t3_thread_send` (mode steer) to the first seven threads [pos 684-690].

### 3.3 Owls-side delegated tasks (`delegate_task`, children run in `~/.t3/worktrees/...`)
About 45 `delegate_task` calls on Owls (positions 393-835, 1410-1476); several were retried after T3 restarts (`clientRequestId` e.g. `a-rev2-retry-1`, `a-rev1-restart-1/2`, `a-rev2-restart-4`, `f-share-xhigh-1`, `f-refine-xhigh-1`, `o-ls0-light-1`, `o-dilute-1` twice). The early Fable/Opus/Astra tasks have no recorded threadId in my extraction (ids are in the items of `activity_all.json`). Child thread ids recorded for the late and key tasks:

| Task | Pos | childThreadId |
|---|---|---|
| OWLS-STEWARD (Sonnet 5.5, CW) | 458 | `thread:delegated-task:command%3Amcp%3A9249c83d-25ae-4fbb-beab-04d05421a45c%3Adelegate-task%3Aowls-steward-1` |
| O-LS0-WRAP (Opus, CW) | 759 | `thread:delegated-task:command%3Amcp%3Abab9a58d-6921-43e4-825e-2f7b77608dd4%3Adelegate-task%3Ao-ls0-wrap-1` |
| E-SPINE (Opus, CW) | 804 | `thread:delegated-task:command%3Amcp%3A1be49f2e-413e-4c7b-8bc6-d8424ca41efb%3Adelegate-task%3Ae-spine-1` |
| LH-LOCK (Fable, CW; failed) | 818 | `...%3A1be49f2e-413e-4c7b-8bc6-d8424ca41efb%3Adelegate-task%3Alh-lock-1` |
| T38-RECORD (Opus, CW) | 820 | `...%3A1be49f2e-413e-4c7b-8bc6-d8424ca41efb%3Adelegate-task%3At38-record-1` |
| Sol 1 proof check of MEET-v31 (GPT-6.1 Sol) | 1410 | `thread:delegated-task:command%3Amcp%3A69497215-3f14-4b45-b283-0c24f706e0a3%3Adelegate-task%3Ab88de747-8715-4e43-95f5-72169ab94cad` |
| Sol 2 audit of MEET-v31 (Sol) | 1412 | `...%3Adelegate-task%3A6fed5a13-0154-4d90-a9c4-be982dc711f9` |
| ABL-CONF (Opus, CW) | 1431 | `...%3Adelegate-task%3Aab0b8728-8bfd-4d43-af06-8102701fc070` |
| Registrar for MEET-THM (Sonnet, CW) | 1446 | `...%3Adelegate-task%3Aa2a4b5a3-3d8d-4c7a-b545-0ddbde4b2700` |
| N9 kernel validity (Opus, CW) | 1457 | `...%3Adelegate-task%3A559fe794-7d03-4372-8e6e-0390b621ccb9` |
| MEET-v31 amendment editor (Opus, CW) | 1476 | `...%3Adelegate-task%3A23948a37-98e7-4753-88d0-6401c300ef61` |
(`...` = prefix `thread:delegated-task:command%3Amcp%3A69497215-3f14-4b45-b283-0c24f706e0a3` for 1410-1476 and `thread:delegated-task:command%3Amcp%3A1be49f2e-413e-4c7b-8bc6-d8424ca41efb` for 804-820.)

### 3.4 Meeting threads and fresh-eyes threads (Owls environment, project `58858238-933d-4ae9-bac2-213d20df8897` unless noted)
| Thread | Link / id exactly as in the transcript | Pos |
|---|---|---|
| "Methodology - Final meeting" (chair Opus 5.5 high, CW; worktree branch `theory/MEET-v31` from `theory/campaign`) | `<t3-thread://v2/b18966a3-98dd-4510-a488-d5dfb1650daa/mcp:launch:d8b9d7a2b3d1902cd8fac11f4301638e39b000164c2fd3ffca0ed0de482c17f2>` | launched [1197], described [1201, 1212, 1251, 1584] |
| "Theorems - Final meeting", FIRST launch (FAILED, never started: the worktree setup used base `theory/MEET-THM`, a branch that existed only on the remote) | `<t3-thread://v2/b18966a3-98dd-4510-a488-d5dfb1650daa/mcp:launch:4dcb66569f85b6a04c0f829a2d74bfb36aec53bdabf62d0f46652fdc39dec8b1>`, renamed "(failed launch - ignore) Theorems - Final meeting" with `t3_thread_update` | launched [1576], failure noted [1597], renamed [1605, 1606] |
| "Theorems - Final meeting", SECOND launch (the real meeting; base `origin/theory/MEET-THM`, chair Opus CW) | `<t3-thread://v2/b18966a3-98dd-4510-a488-d5dfb1650daa/mcp:launch:df98ff6d90c04ddb6a8838890c91ad7916abbfa7bc904b4c59cace039b5491d0>` | launched [1600], reported [1606] |
| Project "Fresh-eyes Fable" | projectId `mcp:ebb3e2f0-ec05-40ab-bdc7-5403d7451a71`, workspaceRoot `/home/fb31/fresh_eyes/fable` | created [1395] |
| Project "Fresh-eyes Astra" | projectId `mcp:ba6b106e-7c21-4733-a6c2-6a8bd34ecd8f`, workspaceRoot `/home/fb31/fresh_eyes/astra` | created [1396] |
| Thread "Fresh-eyes theory plan (Fable)" (Fable 5.1 high, CP, instance `claudeAgent_personal`) | `<t3-thread://v2/b18966a3-98dd-4510-a488-d5dfb1650daa/mcp:launch:a636656f46d312431211c48bba49de2c36cc3fc12bcd39d6a8328707f8019110>` | launched [1405] after two failed `delegate_task` attempts [1401, 1402] ("A local task runs in this thread's project") |
| Thread "Fresh-eyes theory plan (Astra)" (GPT-6 Astra, Codex, high) | `<t3-thread://v2/b18966a3-98dd-4510-a488-d5dfb1650daa/mcp:launch:e2da471067686dfea3d80fd8e497a9ce20569dd141022357088ac08c2665997c>` | launched [1406] |

Fresh-eyes outputs: R0_D.md (Seat D, 72 items) and R0_E.md (Advisor E, 44 packages) under `theory_campaign/MEET-THM/` (`branch_snapshots/MEET-THM/R0_D.md`, `R0_E.md`); working folders `/home/fb31/fresh_eyes/{fable,astra}` (THEORY_PLAN.md).

### 3.5 Other T3 objects the HQ created
- Link request to NOTS: turnItemId `turn-item:link-request:5e38497d-7dfd-48f9-88e9-b21895922f58:1dd6d348-8e63-46fa-bafe-16a1a62903be:link-nots-meet-v31` (pending, then told to cancel) [pos 1193, 1208].
- Secret requests (private cards): [pos 250] GitHub token cancelled; [272] GitHub token saved; [860] Anthropic API key cancelled; [871] Anthropic API key saved.
- Attachments: Felipe's PDF uploads under `/home/fb31/.t3/userdata/attachments/5e38497d-...-pdf.pdf` (e.g. `...-e1629524-1b8c-4924-8c50-b9d98903c127-pdf.pdf` = the first-draft PDF copied to `~/.config/bvs-hq/inputs/Local_to_Global_draft.pdf` [pos 484]).

---

## 4. Scripts and infrastructure the HQ wrote

### 4.1 Cloud launcher: `~/.config/bvs-hq/launch_cloud.sh` (1,597 B)
Written [pos 334]; `bash launch_cloud.sh TASK_ID`. Checks out `theory/campaign` in `/home/fb31/BVS_GH/Bayesian-Variable-Selection` (spec `theory_campaign/tasks/$T.md` must already be pushed), opens a detached tmux session `cc_$T` with `env CLAUDE_CONFIG_DIR=/home/fb31/.claude-personal claude --cloud "<prompt>"` (a pseudo-terminal is required: plain `claude --cloud` with piped stdout fails with "--cloud requires an interactive terminal" [pos 308]), auto-answers the trust dialog (Down + Enter), scrapes `https://claude.ai/code/session_...` and appends `<UTC time> <TASK> <URL>` to `~/.config/bvs-hq/cloud_sessions.log`. The cloud prompt tells the run to read `theory_campaign/PROTOCOL.md` and its task spec, create branch `theory/$T`, write only under `theory_campaign/$T/`, push after every step, finish with `REPORT.md`, open no PR and never touch main. Used for waves 2-8 [pos 334, 352, 364, 508, 558-569, 711, 756]; retired when credits ran out (ledger 20:35 UTC). Wave 1 used `RemoteTrigger` routines instead (plan-billed, see section 6).

### 4.2 API launcher: `~/.config/bvs-hq/launch_api.sh` (1,989 B, mode 700) and `/home/fb31/api_workers/sdk_worker.py`
- First version [pos 831]; changed to a hard dollar cap [pos 835] (`--max-budget-usd`, default 15); rebuilt on the Claude Agent SDK [pos 888-891] after the Claude Code CLI was refused on the promotional credit ("Credit balance is too low", `claude -p ... --max-budget-usd 0.10` [pos 875]); the Agent SDK test cost $0.002 [pos 890]. Final text printed [pos 1032].
- Usage: `launch_api.sh TASK_ID [MODEL] [MAX_USD] [EFFORT]` (default model `claude-opus-5-5`, cap 15, effort high). Per task: `git worktree add -B theory/$T /home/fb31/api_workers/$T origin/theory/campaign`, writes `$T.prompt`, runs `nohup env -u CLAUDE_CODE_OAUTH_TOKEN -u CLAUDECODE nice -n 10 /home/fb31/api_workers/.venv/bin/python /home/fb31/api_workers/sdk_worker.py <cwd> <model> <cap> <effort> <promptfile> > $T.log`, appends to `/home/fb31/api_workers/launches.log`. The worker prompt requires: read PROTOCOL.md and `tasks/$T.md`; write only under `theory_campaign/$T/`; commit/push each step; commit trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; run any computation through `~/.config/bvs-hq/owls/owls_run -j 2 -- <cmd>`; hard spend cap; write long proofs across several files (single responses are capped at 64K output tokens); finish with `REPORT.md`; no PR, no main. Resume runs: `$T.resume.prompt` / `.resume.log` (API-RESID, API-AUDIT).
- `sdk_worker.py` (written [pos 888]): `claude_agent_sdk.query` with `ClaudeAgentOptions(cwd, model, max_budget_usd, effort, permission_mode="bypassPermissions", env={ANTHROPIC_API_KEY (read from ~/.config/bvs-hq/api/anthropic_key), CLAUDE_CONFIG_DIR=/home/fb31/api_workers/.claude-api-config}, setting_sources=["project"])`; prints `[assistant]` text and a final JSON line with `total_cost_usd`.
- Launch log (`/home/fb31/api_workers/launches.log`, 20 lines): first lines `2026-11-02T21:25:37Z API-RESID model=claude-opus-5-5 cap_usd=15 effort=high` and `...21:25:42Z API-FAVIID`; `API-PXNGAP` (Fable, cap 25) 21:29:58Z. Launch positions: [pos 891] (first two), then 897-909, 966-974, 996, 1079-1105 (METH-AUDIT/THM-INV), 1121, 1185.
- Caps used: Opus $15/$12/$10/$8, Fable $25, from the ledger table (section 2.3). Org has no payment method and a monthly spend limit of $195 (section 6).

### 4.3 Owls guardrails: OWLS-STEWARD, `owls_run`, `owls_guard.sh`, `POLICY.md` (all in `~/.config/bvs-hq/owls/`)
- Built by the delegate task OWLS-STEWARD (Sonnet 5.5, CW) launched [pos 458], finished [pos 476]; summary [pos 474]. Why: Owls was at load about 600-700 and Felipe's ssh collapsed after about 34 cores of multithreaded R; Felipe asked to "be very mindful with Owls usage" (memory `owls-resource-rules.md` [pos 473]).
- `owls_run -j N -- cmd ...` (default N=2, hard max 8): nice 19 + ionice idle, sources `env.sh` (single-threaded BLAS/OpenMP/MKL/FlexiBLAS, `MC_CORES=1`), pins to the N least-loaded cores with `taskset`, admission control under `flock` on `admit.lock` (refuses with exit 75 / `REFUSED` if fb31 compute + request would exceed 8 cores or 3 jobs already run), logs START/RUNNING/END/REFUSED to `jobs.log`. Env: `OWLS_BUDGET_CORES` (8), `OWLS_MAX_JOBS` (3).
- `owls_guard.sh start|run|status|resume|stop`: 60 s sampler writing `status.json` and `guard.log`; compute over 8 cores is reniced; over 16 cores for 3 consecutive samples the newest offenders get SIGSTOP (listed in `STOPPED`) and are auto-resumed after a 5 min cool-down once under 75% of budget.
- Persistence: first a crontab `@reboot ... owls_guard.sh start` [pos 479]; at [pos 601] no guard process was found running (empty pid file), so [pos 605] restarted it as `systemd-run --user --unit=owls-guard --description="Owls fb31 compute guard" -p Restart=always -p RestartSec=30 .../owls_guard.sh run` plus an `@reboot systemd-run ...` crontab line [pos 601-605]. Unit `owls-guard.service` was active on 2026-11-02 13:04.
- `POLICY.md` (5,207 B): rules (8 cores total, 2 per job, 3 concurrent jobs, everything through `owls_run`, refusal is an answer, never kill t3/claude/codex/sshd/tmux; `cpulimit`/`systemd-run --scope -p CPUQuota` do not work for this user, `taskset` is the enforcement); big work goes to NOTS (one ssh connection at a time via `ops/scaffold/sshlock`, back off 15 min); how to read `status.json`/`guard.log`.
- **systemd-run lesson** (added to POLICY.md by the HQ, 2026-11-04) [pos 1533, 1541, 1584]: every T3 agent runs inside its own systemd scope (`app-t3code-agents.../t3code-*.scope`); when the agent's session ends T3 stops the scope and kills every process in it, including `setsid nohup ... &` children. This caused every rc=143 kill on 2026-11-03/04 (ABL-START arm-B S4 fits; ABL-CONF's first launch at 01:25 UTC). Fix: launch long jobs as `systemd-run --user --unit=<name>-$(date +%Y%m%d-%H%M%S) --collect --quiet --working-directory="$PWD" -p StandardOutput=file:... -p StandardError=file:... $HOME/.config/bvs-hq/owls/owls_run -j 2 -- <cmd>`. HQ verified that a `systemd-run --user` unit lands in its own cgroup (`app.slice/hq-escape-test.service`) [pos 1533].

### 4.4 ABL-CONF scripts and RUNBOOK (`theory/ABL-CONF`, work dir `/home/fb31/ablconf_work`)
Task spec `theory_campaign/tasks/ABL-CONF.md` (written by the HQ, file_change [pos 1429]); launched [pos 1431]; agent finished with a hand-off [pos 1432]. Branch content (`branch_snapshots/ABL-CONF/`): `PREREG.md` (commit 1, rule frozen before any fit), `RUNBOOK.md` (commit `c0730fe`; exact commands to check progress, relaunch and finalize), `REPORT.md`, `results/final/rule_verdict.txt`, `results/queue.txt`, `results/schedule_estimate.txt`, `results/dryrun/**` (synthetic rule dry runs: expected, reversed, no_difference, B_fails_badly, C_fails_badly, guard_fails; 31 csv files). Scripts under `theory_campaign/ABL-CONF/scripts/`: `abl_core.R`, `abl_exports.cpp`, `abl_fit.R`, `abl_start_table.py`, `apply_rule.py` (the pre-registered decision rule), `dryrun.sh`, `finalize.sh`, `launch.sh` (patched by the HQ to systemd units at 01:29 UTC; original kept as `launch_setsid_orig.sh`), `make_queue.py`, `make_synthetic.py`, `progress.sh`, `relaunch.sh`, `report_tables.py`, `run_queue.sh`, `summarise.R`. Work dir contents: `fits/` (107 files; 118/118 terminal at the end: 107 completed, 11 capped), `launch/`, `logs/`, `progress.log`, `killed.log`, `DEVIATIONS.md` ("not rule changes": the rc 143 kill and the systemd relaunch). Related earlier ablation: `theory/ABL-START` with `scripts/{abl_core.R, abl_exports.cpp, abl_fit.R, backfit_tables.R, block_stats.cpp, check_armA_bitwise.R, run_queue.sh, summarise.R}` and chair queues in `/home/fb31/abl_work`. Positions: relaunch/progress [1519, 1530-1541, 1632, 1653-1665]; finalised result [1651, 1670]; scheduled wake-up [1485].

### 4.5 N9 harness (`theory/N9-KERNEL`)
Task N9 (kernel reversibility, round self-adjointness, exact start sampler against production code) delegated [pos 1457]. Files (`branch_snapshots/N9-KERNEL/`): `PROOF.md`, `CHECK.md`, `REPORT.md` (agent's own), `HQ_NOTE.md` (HQ's note; the HQ first overwrote the agent's report, then restored it [pos 1590, 1593]). Non-text files: `scripts/n9_harness.cpp` (28,780 B), `scripts/n9_order.cpp`, `scripts/build.sh`, `scripts/run_all.sh`, `scripts/summarise.py`, `results/{A_n20_p6_ar1.txt, B_n20_p8_factor.txt, C_n10_p8_factor_capK5.txt, order.txt, summary.txt}`. Result: PROVED (candidate) with exact checks on the production headers and failing negative controls; tip `c20059d` (local branch at `3338896`). Positions [1457, 1517, 1551, 1555, 1588-1593].

### 4.6 METH-AUDIT scripts (`theory/METH-AUDIT`, work dirs `/home/fb31/api_workers/METH-AUDIT`, `/home/fb31/ma_work`)
Launched through `launch_api.sh` (Opus, $15) [pos 1068-1103]. Scripts (`theory_campaign/METH-AUDIT/scripts/`): `ma_core.R`, `ma_exports.cpp`, `ma_fit.R`, `run_owls.sh` (3 designs sequentially via `owls_run -j 2`), `summarise.R`, `nots_10designs.slurm` (a 10-design NOTS job, not run from Owls). Results: `results/fit_p0500_S1_r001_c100.rds`, `run_owls.log`, `smoke.rds` (gitignored data, on Owls only). The worker exited early with a "3/3 bitwise" headline that the ledger calls an overclaim; the HQ re-ran designs `p0500_S4_r001` (c050) and `p0500_S5_r002` (c100) itself with `nohup ~/.config/bvs-hq/owls/owls_run -j 2 -- bash -c 'for spec in ...; Rscript scripts/ma_fit.R ...'` [pos 1093-1098]; concurrency log in `theory_campaign/MEET-v31/evidence/2026-11-03_concurrency_runs.md`. Ledger: S4_r001 bitwise PASS (serial 672 s vs 352 s); full 3/3 stands in the meeting record [pos 1251].

### 4.7 PIP rescoring
Script `theory_campaign/MEET-v31/evidence/2026-11-03_pip_rescore/pip_rescore.R` (5,390 B, blob `8980cfc`), with `partA_per_island_subset.csv`, `partB_cell_counts_2400.csv`, and `REPORT.md` (commit a240857). Purpose: Z-hat-weighted PIP (now primary in v3.1) vs equal-weight PIP over the study fits. Status: only 3 designs could be rescored on Owls (PIPs moved by at most 0.0013, MPM never changed [pos 1251]); the full POST HOC rescoring of all 2,394 completed fits needs the per-island `pip_r`/`log_Z_r` from NOTS (`/scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_*/results/`) and the laptop, and was handed to "a thread on your PC" [pos 1251]; METHOD_v3.1_FINAL.md lists it as open item 8. No completed full rescoring appears in the thread (**UNVERIFIED**).

### 4.8 Other scripts and files written by the HQ itself
- Campaign skeleton on `theory/campaign`: `theory_campaign/PROTOCOL.md` (file_change [pos 193]), `LEDGER.md` [pos 234 and many appends], `tasks/*.md` (task specs written by heredoc, e.g. [pos 201, 328, 352, 364, 508, 558]; THM-SYNTH [1102], ABL-START [1184], ABL-CONF [1429]), `HQ/SR_AUDIT.md` [pos 542, 551].
- Meeting dossiers: `MEET-v31/DOSSIER.md` [1182], `MEET-v31/evidence/AMEND_01_general_np.md` [1220, 1227], `MEET-v31/FOR_FELIPE_FINAL_METHOD.md` [1581], `MEET-THM/DOSSIER.md` [1442], `MEET-THM/CHAIR_BRIEF.md` [1573, 1585], `MEET-THM/FOR_FELIPE_THEOREM_LIST.md` [1643, 1644], `hq_reviews/HQ_DISPOSITIONS.md` [1475], `fresh_eyes/packet/{BRIEF.md, METHOD_v3.1_ADDITIONS.md}` [1389, 1391].
- Memory files (Owls, Claude Personal config): see section 1.1 [pos 36, 160, 165, 473, 810].
- Git facts: the HQ committed with trailer `Co-Authored-By: Claude Opus 5.5 ...` using a repo-local credential helper that reads `~/.config/bvs-hq/gh_token` (set [pos 274]; value never printed).
- Branch-state polling idiom used throughout: `git fetch -q origin; for b in $(git branch -r | grep -E 'theory/(W4|F-|O-|A-)'); do echo "$b: $(git log -1 --format=%cd ...) $(git rev-list --count origin/theory/campaign..$b)c"; done` [pos 284, 346, 358, 412, 421, 500, 545].
- PR/Git: `link_pull_request` for PR #1 [pos 848]; no other PRs.

---

## 5. Result and data files

The branch snapshots hold text (`.md/.tex/.lean`) verbatim; everything else (1,645 files) is indexed in `branch_snapshots/NONTEXT_INDEX.tsv` (columns `ref  path  bytes  git_blob`), where the real bytes can be fetched with `git show <blob>` on Owls (`/home/fb31/Bayesian-Variable-Selection`). The index contains: `main@c4ef0dc` 21 files (14 PDFs, 5.7 MB) and one file group per `theory/<ID>@tip`. The largest groups by bytes are A-REV5 (289 files, 12.0 MB; 127 `.py`, 62 `.json`, 87 `.txt`), O-DILUTE (22, 6.5 MB), API-RESID (14, 5.8 MB), W1-T37R (4.7 MB), W1-EXP (4.5 MB), F-MASKPIP (3.8 MB, 25 `.jsonl`), A-REV3 (3.6 MB, `.npz`), `theory/campaign` (2 PDFs, 1.3 MB: `inputs/Local_to_Global_proposal.pdf`, `inputs/SongLiang2015.pdf` [pos 1073]).

Grouping of the non-text files:
- Scripts (`.py`, `.R/.r`, `.sh`, `.cpp`, `.h`, `.slurm`): by far the majority; they are the reproduction code of each branch (e.g. `A-REV1/sources/...` copies of verification scripts, `ABL-CONF/scripts`, `N9-KERNEL/scripts`, `MEET-THM/**` 34 `.py` + 9 `.h` + 3 `.cpp`).
- Numerical results (`.csv`, `.json`, `.jsonl`, `.npz`): table below.
- Logs (`.log`, `.err`, `.out`, `.txt`): outputs of runs.
- PDFs: `main@c4ef0dc` (COLLECTED_PROOFS_v2.pdf, MASTER_Methodology_and_Plan.pdf, THEORY.pdf, delmoral_doucet_jasra SMC paper, etc.), `S-PAPER` (compiled theory section), `theory/campaign` inputs.

Per branch: file counts and the three largest data files (csv/json/jsonl/npz/pdf/png/svg/rds; scripts and logs excluded from "data"). Blobs are the first 10 hex chars of the git blob id.

| ref@tip | non-text files / data files (by type) | data bytes | largest data files (path : bytes : git blob) |
|---|---|---|---|
| main@c4ef0dc | 21 / 15 (14 .pdf, 1 .out) | 5707848 | `proofs/COLLECTED_PROOFS_v2.pdf` : 1377981 : `8d638f4618`; `MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.pdf` : 562685 : `cd74b1bd5f`; `THEORY.pdf` : 489533 : `07e391dcc0` |
| theory/A-DRAFT@dbf47f7 | 8 / 4 (1 .png, 1 .svg, 1 .csv, 1 .json) | 160176 | `results/naive_merge.png` : 93184 : `306e7becbe`; `results/naive_merge.svg` : 65645 : `ae09e67ac0`; `results/naive_merge.csv` : 1171 : `e873656630` |
| theory/A-REV1@26815e8 | 89 / 18 (18 .json) | 252522 | `sources/W1-T24G/results/designs_n200.json` : 75553 : `0dc3f34880`; `sources/W1-T24G/results/distance_one.json` : 25259 : `bb3581d65c`; `sources/W2-VT24G/results/ce1_recheck.json` : 21660 : `60e17f9657` |
| theory/A-REV2@09dc230 | 5 / 1 (1 .json) | 6553 | `results/checks.json` : 6553 : `06d763da5e` |
| theory/A-REV3@522d83d | 26 / 7 (3 .npz, 3 .json, 1 .jsonl) | 3475674 | `results/data_1.npz` : 1154564 : `ef8f4f0101`; `results/data_2.npz` : 1154502 : `16756204a4`; `results/data_0.npz` : 1154388 : `39e554658c` |
| theory/A-REV4@b95948c | 61 / 5 (5 .json) | 210693 | `results/nm_raw.json` : 197515 : `0100819a35`; `ARTIFACT_HASHES.json` : 8347 : `e3d6687b28`; `SOURCE_MANIFEST.json` : 2047 : `e8393418f9` |
| theory/A-REV5@189770c | 289 / 62 (62 .json) | 11213982 | `sources/W1-T37R/results/exp1_p20_pm1.json` : 1763538 : `5e9bc91235`; `sources/W1-T37R/results/exp1_p20_pm0.json` : 1681850 : `dfc2916ab4`; `sources/W1-EXP/results/fam_A85_gram.json` : 1101343 : `4bc66f2318` |
| theory/A-REV6@02d6a4a | 3 / 2 (2 .json) | 29550 | `SOURCE_MANIFEST.json` : 28566 : `beff0794be`; `AUDIT.json` : 984 : `2bc2a0a055` |
| theory/A-REV7@70eadf3 | 90 / 3 (3 .json) | 8898 | `remote/results.json` : 6428 : `31e90c23c5`; `AUDIT.json` : 1614 : `98226ce516`; `sources/refs.json` : 856 : `dc34d12e3b` |
| theory/A-REV8@6417192 | 53 / 17 (12 .npz, 4 .json, 1 .csv) | 71541 | `results/failed_serialization/population.json` : 16551 : `d5502cb08d`; `results/population.json` : 16551 : `d5502cb08d`; `sources/manifest.json` : 5271 : `3d9ef24cea` |
| theory/ABL-CONF@7e12cf5 | 60 / 31 (31 .csv) | 158555 | `results/final/per_fit.csv` : 46984 : `c4a86a20e4`; `results/dryrun/input/abl_start_item1_per_fit.csv` : 17881 : `1d385db836`; `results/dryrun/synthetic/no_difference/per_fit.csv` : 10662 : `68db44358e` |
| theory/API-AUDIT@966e713 | 20 / 7 (7 .csv) | 25031 | `results/valfp_seeds.csv` : 10898 : `a71c1a0376`; `results/index_draw_flips.csv` : 4229 : `21101b1c8a`; `results/valfp_table.csv` : 3083 : `f2152ac120` |
| theory/API-MASKZPIP@1200e63 | 17 / 8 (8 .jsonl) | 104517 | `results/check_masked_n640_N500.jsonl` : 31701 : `b55ab5391f`; `results/check_masked8_n5120_N500.jsonl` : 22006 : `dfe07718d1`; `results/check_masked8_n640_N500.jsonl` : 20883 : `292d4ee299` |
| theory/API-N200@453117a | 30 / 25 (25 .csv) | 1366668 | `data/oswap/local_p1000_S1.csv` : 84183 : `4fe62db241`; `data/oswap/local_p500_S1.csv` : 84140 : `49e6461537`; `data/oswap/local_p500_S2.csv` : 83840 : `c9f28191c2` |
| theory/API-PXNGAP@c535beb | 15 / 1 (1 .jsonl) | 29108 | `results/route.jsonl` : 29108 : `d3dd1c53e5` |
| theory/API-RESID@66e1da7 | 14 / 6 (6 .csv) | 5818319 | `results/per_fit.csv` : 2468063 : `e938ce5756`; `results/per_fit_shard1.csv` : 1238429 : `6fde7a6434`; `results/per_fit_shard2.csv` : 1238045 : `8c7c40cda0` |
| theory/API-T26BUD@2ac43ac | 9 / 1 (1 .jsonl) | 39430 | `results/realised_T.jsonl` : 39430 : `3981cef79c` |
| theory/API-VSTAB@ba9507f | 4 / 1 (1 .json) | 2465 | `scripts/vstab_check.json` : 2465 : `a9518bba6f` |
| theory/F-MASKPIP@dbe45fa | 33 / 25 (25 .jsonl) | 3775376 | `results/masked_sim.jsonl` : 1887688 : `439e24671e`; `results/raw/masked_n5120_N50_G2.jsonl` : 105237 : `5f8e02db5d`; `results/raw/masked8_n5120_N50_G2.jsonl` : 104901 : `4a290779d6` |
| theory/F-SHARE@13bc665 | 17 / 5 (5 .json) | 726125 | `results/f1_exact_lh.json` : 381964 : `dcc9b1f1a9`; `results/f2_sim_lh.json` : 164887 : `d40ab9ec0c`; `results/f2_sim_lh_LH16.json` : 125695 : `136c24cf72` |
| theory/L-LEAN@cfa78ed | 10 / 1 (1 .json) | 3231 | `SmcBvs/lake-manifest.json` : 3231 : `2d46424328` |
| theory/MEET-THM@37b4d2b | 77 / 8 (8 .json) | 82448 | `evidence/W2_PC1/scripts/verdict_rows.json` : 58703 : `78d1da010b`; `evidence/W2_PC1/scripts/new_checks.json` : 6500 : `c56cf4881f`; `evidence/W1_PC1/scripts/seat_a_d_reconstruction.json` : 6155 : `08a25bf57f` |
| theory/MEET-v31@e82e097 | 22 / 4 (4 .csv) | 25713 | `evidence/item1_per_fit.csv` : 17881 : `1d385db836`; `evidence/item1_rule_table.csv` : 3460 : `ebe72daa13`; `evidence/2026-11-03_pip_rescore/partA_per_island_subset.csv` : 3082 : `87ebdbef21` |
| theory/O-DILUTE@abedf99 | 22 / 6 (6 .jsonl) | 6484631 | `results/study_a.jsonl` : 2171708 : `2303a12b2e`; `results/study_d.jsonl` : 1090234 : `42070f7e1c`; `results/study_c.jsonl` : 1082690 : `6a321e887b` |
| theory/O-LS0@02348e2 | 18 / 3 (3 .csv) | 12139 | `results/cell_summary.csv` : 9260 : `315f916077`; `results/paired_cell_summary.csv` : 1752 : `912f6efd6f`; `results/data_hash_check.csv` : 1127 : `05d62657e7` |
| theory/O-PW2@e685ead | 13 / 6 (6 .json) | 27316 | `results/pw2_p8_rho0.95_gibbs1_thr0.9.json` : 5658 : `aace39700b`; `results/pw2_p8_rho0.9_indep_thr0.9.json` : 4821 : `6be2f33e77`; `results/pw2_p6_rho0.9_gibbs1_thr0.9.json` : 4716 : `1b128d1ffe` |
| theory/O-SWAP@5b9b506 | 37 / 24 (24 .csv) | 1361953 | `out/local_p1000_S1.csv` : 84183 : `4fe62db241`; `out/local_p500_S1.csv` : 84140 : `49e6461537`; `out/local_p500_S2.csv` : 83840 : `c9f28191c2` |
| theory/O-WSTAB@2ec3099 | 20 / 2 (2 .json) | 719261 | `results/sweep_link.json` : 414039 : `4f29994ae3`; `results/sweep_link_part1.json` : 305222 : `19f449b6c6` |
| theory/S-ELS@90423b1 | 15 / 12 (11 .csv, 1 .json) | 1269238 | `tables/ledger_per_fit.csv` : 1121558 : `de03d21e1f`; `tables/c541_cases.csv` : 144652 : `9a259447ab`; `tables/strict_same_size_misses.csv` : 772 : `027ad82b68` |
| theory/S-PAPER@e073b69 | 2 / 1 (1 .pdf) | 527178 | `theory_section.pdf` : 527178 : `6a28f22e73` |
| theory/W1-EXP@722bd18 | 15 / 6 (6 .json) | 4451165 | `results/fam_A85_gram.json` : 1101343 : `4bc66f2318`; `results/fam_A_gram.json` : 1097487 : `f64e93f2be`; `results/fam_A_random.json` : 1092760 : `558e7758dd` |
| theory/W1-T24G@9e210a3 | 26 / 8 (8 .json) | 176189 | `results/designs_n200.json` : 75553 : `0dc3f34880`; `results/distance_one.json` : 25259 : `bb3581d65c`; `results/compare_cprime.json` : 18965 : `8588a68db6` |
| theory/W1-T37R@3bcc429 | 10 / 4 (4 .json) | 4702972 | `results/exp1_p20_pm1.json` : 1763538 : `5e9bc91235`; `results/exp1_p20_pm0.json` : 1681850 : `dfc2916ab4`; `results/exp1_p25_pm1.json` : 953173 : `bc4eb889b8` |
| theory/W2-PREM@988c5f5 | 17 / 1 (1 .json) | 18719 | `results/lh_premises_all.json` : 18719 : `0161842778` |
| theory/W2-T26@0e4f1e7 | 13 / 4 (3 .csv, 1 .jsonl) | 68573 | `results/premise_scan.csv` : 47065 : `48861a4c34`; `results/premise_scan_large.csv` : 13800 : `8fb971ae40`; `results/smc_sim.jsonl` : 6840 : `62e9e33474` |
| theory/W2-VT24G@dba6ff4 | 19 / 7 (7 .json) | 44341 | `results/ce1_recheck.json` : 21660 : `60e17f9657`; `results/p1_repair.json` : 10194 : `4058799521`; `results/ce1_scaling.json` : 5057 : `4f153694c0` |
| theory/W3-PGD@fdeaec3 | 15 / 8 (8 .json) | 1344203 | `results/n200_p500_S4.json` : 238583 : `84225e1146`; `results/n200_p500_S5.json` : 205817 : `db27311e30`; `results/n200_p500_S2.json` : 202834 : `bf2d00a357` |
| theory/W3-PXN@4aebea3 | 20 / 6 (6 .jsonl) | 1146414 | `results/study_n200.jsonl` : 540867 : `d1cd4645a2`; `results/study_nsweep.jsonl` : 320437 : `e8f54d6705`; `results/lh_P.jsonl` : 91736 : `70c10f19a9` |
| theory/W3-VEXP@7970fa0 | 32 / 9 (9 .json) | 33616 | `results/study_exp_1_2_3_4_5_6.json` : 16765 : `8791b067f7`; `results/study_check.json` : 6207 : `5098796ebf`; `results/study_exp_3_n200_c1.0_4.0.json` : 1845 : `5bc0a630ce` |
| theory/W3-VT37R@4988b96 | 17 / 2 (2 .json) | 315032 | `results/prod_scale.json` : 183595 : `07f3167056`; `results/exhaust_theoremA.json` : 131437 : `fb8dfe2c8a` |
| theory/W5-FAVIID@31695b1 | 18 / 2 (2 .jsonl) | 1747835 | `results/sweep.jsonl` : 1701469 : `269e7e3457`; `results/pilot.jsonl` : 46366 : `4bbc3ffc72` |
| theory/W5-LOCKBOOK@a65392b | 10 / 1 (1 .csv) | 16182 | `results/premise_indep.csv` : 16182 : `66644c52af` |
| theory/W5-VMASK@4e41b97 | 31 / 7 (7 .jsonl) | 190332 | `results/lh_A.jsonl` : 40270 : `7341ac4220`; `results/lh_B.jsonl` : 39440 : `9080498a19`; `results/lh_ADV_PSI.jsonl` : 36814 : `ae6c186fad` |
| theory/W5-VPGD@8e2bbc4 | 35 / 5 (3 .json, 2 .jsonl) | 51883 | `results/realised.jsonl` : 41366 : `4d08238f70`; `results/study_pop_A.json` : 7190 : `05fd7fe62b`; `results/study_pop_C.json` : 1410 : `658aef965d` |
| theory/W6-FIXREV1@a7833f3 | 11 / 4 (4 .json) | 12896 | `results/lemmaS_lemmaU_check.json` : 8841 : `cb71605c08`; `results/ce1_sequence.json` : 2349 : `c9400307a4`; `results/propU_check.json` : 1150 : `1024261aab` |
| theory/W6-FIXREV2@be2d456 | 12 / 3 (3 .json) | 3949 | `results/lemmaU_checks.json` : 1827 : `788a338a3c`; `results/t37_checks.json` : 1371 : `292ff488ec`; `results/t37_extra.json` : 751 : `9647da5a19` |
| theory/W7-PART@b2aa940 | 22 / 1 (1 .jsonl) | 10980 | `results/sim_partition.jsonl` : 10980 : `665b69fd9e` |
| theory/W7-SEP@858004e | 26 / 4 (4 .jsonl) | 338788 | `results/sep_C3_gram.jsonl` : 126576 : `643ab6fa93`; `results/sep_V2_gram.jsonl` : 118485 : `bf234ecfde`; `results/sep_B2_gram.jsonl` : 61588 : `8835c983ad` |
| theory/campaign@401a613 | 2 / 2 (2 .pdf) | 1325534 | `SongLiang2015.pdf` : 1102387 : `596eba6dec`; `Local_to_Global_proposal.pdf` : 223147 : `b0aab4d48c` |

Full list of non-text files: `branch_snapshots/NONTEXT_INDEX.tsv`. Branches with no data files (only scripts/logs/text) are omitted from the table, e.g. F-DRAFT, LIT-*, METH-AUDIT, N9-KERNEL (txt/py/cpp only), O-VCERT, S-REGISTRY, THM-SYNTH. Some headline data sets named in reports but NOT in git: the 2,400 regenerated study datasets and fits (`/home/fb31/ls0_work/{full,study,agg_final}`, laptop/NOTS bundles), ABL-CONF fits (`/home/fb31/ablconf_work/fits`, 107 files), ABL-START fits (`/home/fb31/abl_work/fits`, 33 files); small summaries of them are committed (O-LS0 `results/*.csv`, ABL-CONF `results/dryrun/**`).

---

## 6. Credentials and billing facts (no secret values)

### 6.1 Credentials stored on Owls
| Item | Where | Facts | Positions |
|---|---|---|---|
| GitHub fine-grained personal access token "owls-hq" | `~/.config/bvs-hq/gh_token` (mode 600, 93 bytes; installed with `install -m 600` from the T3 secrets store) | Scope: repo `FbStatsQuant/Bayesian-Variable-Selection` only, contents/PRs; 90-day lifetime, **expires Dec 2**; used by a repo-local git credential helper `x-access-token`; verified push access via API without printing it; Owls had no other GitHub credential (only the Lean deploy key). The first request card was cancelled, the second saved. | request cancelled [250], saved [272]; installed + credential helper [274]; "It expires Dec 2" [280]; creation walk-through [msgs around 236-262] |
| Anthropic API key "owls-hq" (Felipe's Individual Org) | `~/.config/bvs-hq/api/anthropic_key` (mode 600, 106 bytes); read by `/home/fb31/api_workers/sdk_worker.py` | Covered by the $200 promotional credit (6.2). First request cancelled, second saved. Used only through the Agent SDK worker (config dir `/home/fb31/api_workers/.claude-api-config`). | cancelled [860], saved [871]; first CLI test [875]; SDK test [888-890] |
| Claude subscription logins | `~/.claude-personal` (Claude Personal, "CP") and `~/.claude` (Claude Work, "CW") on Owls; T3 provider instances `claudeAgent_personal` / `claudeAgent` (Owls) and `claudeAgent_claude_work` (laptop) | Native subagents and `delegate_task` children on CP draw on Felipe's Ultra plan weekly usage (no `ANTHROPIC_API_KEY` in the environment) [pos 289]. Account-balancing rule: split work across CW and CP, weight toward the one with more weekly headroom [pos 165, memory `autonomy-after-target-approval.md`]; from the CP reset window on 2026-11-02, new agents default to CW [pos 810, memory `agent-account-model-defaults.md`]. | |
| Owls ssh keys | `~/.ssh/id_ed25519_bnp_deploy(.pub)`, `authorized_keys`, `config`, `known_hosts` | `id_ed25519_bnp_deploy` is the deploy key of the Lean repo only; `git@github.com` is denied for BVS [pos 205]. No NOTS key on Owls [pos 1208]. | |

### 6.2 Credit pools and what billed them
| Pool | Amount and expiry | What it paid for | What it did NOT pay for | Positions |
|---|---|---|---|---|
| Cloud-session credit (Personal account) | $245 at the start; expires 2026-11-05 07:59 UTC (1:59 AM CST) (ledger header; first message says "Nov 5, in about 3 days") | `claude --cloud` sessions (claude.ai/code): waves 2-8 and W8-SYNTH, launched by `launch_cloud.sh`. Verified by a 7-second test session: credit $245 -> $244 while plan usage stayed at 71%. Readings: $245 (16:00), $244 (17:19), $239 (about 17:22 after wave 2), about $21 of $250 left at 20:35 UTC ("CREDITS EXHAUSTED") per Felipe's reading. | **Routines** (`RemoteTrigger` / triggers API) are EXCLUDED from the cloud credit and bill the weekly plan: Wave 1 (5 runs) and the smoke test moved Personal plan usage 65% -> 71% while the credit stayed at $245. | initial table [pos 7]; billing doubt [305]; finding [342]; ledger BILLING note [337]; exhaustion (ledger 20:35 UTC) |
| API promotional credit (Felipe's Individual Org) | $200.00, **expires 2026-11-17**; no payment method on the org; monthly spend limit $195 | API calls and the **Agent SDK** (all `launch_api.sh` workers). Measured costs from the ledger: API wave about $31 for 7 runs with a cost line; literature phase about $17.0 (LIT-SMC $2.81, LIT-MCMC $3.56, LIT-STAT $4.01, LIT-VENUE $2.78, API-RESID resume $2.41, API-AUDIT resume $1.47); balance $160.34 before the literature phase, est. about $143 after; METH-AUDIT $5.89, THM-INV $7.99, THM-SYNTH $8.4; about $115 left at [pos 1201]. | The **Claude Code CLI** (`claude -p` with the API key returned "Credit balance is too low"). | page read [867]; CLI refusal [875, 880]; Agent SDK works ($0.002) [890]; summary to Felipe [894]; hard per-run caps [835, 891] |
| Second API credit | a new $200 "arrives 2026-11-15, also for theory" (Felipe, via the ledger); the very first message described API credits as "$200/month ... next credit Nov 15" | planned for per-theorem HQs | | [pos 7, 989, 1059]; **UNCERTAIN:** monthly renewal [pos 7] vs one-off promotion [pos 867]; no evidence of the Nov 15 credit arriving within the thread |
| Claude subscriptions (CP/CW weekly usage) | CP weekly usage 65% on 2026-11-02 morning, 71% after wave 1, 84% by 20:35 UTC (resets about 21:00 UTC); CW had headroom | local Fable/Opus/Sonnet agents, laptop threads, meeting seats and chairs (spend $0 credit) | | [pos 342, 810]; ledger 18:02, 18:50, 20:35 UTC |
| Console daily rate limits | Fable 100K / Opus 400K output tokens per day on the API org | held API-UMODEL and API-T03CONST for 2026-11-03 | | ledger 21:30 UTC |

A 64K-output-token single-response cap killed LH-LOCK's first attempt (Fable CW) and shaped the "write long proofs across several files" rule in `launch_api.sh` [ledger 21:55 UTC, pos 1032].

---

## 7. Paths I could not verify (and why)
- Live state of PR #1 on GitHub (no `gh`; stored token deliberately not used). Branch evidence says unmerged.
- How/when `/home/fb31/BVS_GH` was removed or moved to `/home/fb31/Bayesian-Variable-Selection` (no transcript hit; git worktree metadata already points to the new path).
- NOTS paths (`/home/fb31/projects/BVS/...`, `/scratch/fb31/...`): taken from transcript outputs, not listed live (NOTS is unreachable from Owls).
- Laptop paths (`C:\Users\felip\...`): taken from `t3_project_list` and the Owls move note; not listed live.
- The Wave 1 routines' sessions (`session_...` ids from [pos 296]) and the cloud sessions generally: URLs copied from the transcript; not opened.
- Intermediate commits quoted in the ledger (`c3e18ee`, `791e5e3`, `6a80fe5`, `514c8fc`, `db708ca`, `3338896`) were not each checked against `git cat-file` on Owls (only the current tips were).
- Worktrees for API-VSTAB, LIT-*, METH-AUDIT, THM-* under `/home/fb31/api_workers/` (listing was cut off); directories exist per `ls`.
- Credit-test session URL (`claude --cloud` 7-second test) is not recorded in my extraction.
