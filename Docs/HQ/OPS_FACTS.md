# Operational facts: NOTS, Owls, transfers (as of 2026-11-02)

Learned the hard way during campaigns 2 and New Campaign. The binding rules are in `Docs/HQ/RULES.md`; this page holds the facts and gotchas. The OPS tools are under `Scripts/Campaigns/2026-10-28_New_Campaign/ops/`.

## Hosts and access
- **NOTS** (Rice CRC cluster). Use the ssh alias `nots`, pinned to login node **loginx2**, key authentication. Only the OPS thread connects.
  - Felipe's live T3 server runs on that node, and its state lives on NFS. More than one T3 server corrupts it, so keep one pinned node.
- **Owls** (`owls`, a shared stats lab machine) hosts this repo clone at `/home/fb31/BVS_GH`.
  - A separate, older nested clone `/home/fb31/BVS_GH/Bayesian-Variable-Selection` (commit `39db138`) exists. Leave it untouched; it is not this repo's working tree.
- **Route history.** On 2026-10-22, NOTS silently dropped new connections from Owls after a burst, and direct PC → NOTS worked. The Owls → NOTS route must be re-tested at bootstrap, with one connection and no retries in a loop.
- **Burst sensitivity.** About 8 short connections in 3 minutes caused a connect timeout (2026-10-29). After any timeout or reset, back off 15 minutes. Held ssh waits longer than about 1 h get reset.
- **Locking shim.** OPS serialises every ssh through `ops/scaffold/sshlock`: one global lock plus a stall bound.
- **Git Bash path rewriting.** From Git Bash on Windows, `/scratch/...` arguments are rewritten to `C:/Program Files/Git/...`. `nots_pull.py` undoes this; elsewhere set `MSYS_NO_PATHCONV=1`. This does not apply on Owls (Linux).

## NOTS software
- RHEL 9.4. The default toolchain is GCC 13.2.0, with FlexiBLAS 3.3.1 loaded.
- **R:** not on PATH until loaded: `module load GCC/13.2.0 R/4.4.1` (it matches the PC's R 4.4.1). The campaign bundles record the R and module versions they used; follow each `JOB.md`.
  - R 4.5.2 on Linux and R 4.4.1 on Windows differ by 1–3 ULP in `rnorm`/`qnorm`. Cross-platform generator checks therefore use exact checks on the fit-consumed bytes, plus a tolerance of 1e-12·max(1, |x|) on regenerated floats (D44).
- **Modules on compute nodes** must be initialised explicitly in batch scripts.
- **GNU time:** there is no `/usr/bin/time`. Use module `time/1.9` by absolute path (D27).
- **Python:** the system python3 is too old; use 3.13 (module).
- **Benchmark packages** come from the read-only R library `/home/fb31/projects/BVS/library_portable`.
- **Rcpp compile cache:** `.cpp_cache` must stay owner-writable, with one cache per process (a compile race exists).
- `make` may print a clock-skew warning on NFS; it is harmless.

## Slurm
| Partition | Limit | Notes |
|---|---|---|
| commons (default) | 1 day | 72 Cascade Lake (80 cores) + 70 **Sapphire Rapids** (192 cores) |
| long | 3 days | mostly Sapphire Rapids; 384 CPUs / 1 TB per job possible |
| scavenge | 1 h | preemptible |
| debug | 30 min | — |

- **Memory.** DefMemPerCPU is 1024 MB, so always request `--mem`. Use the measured request plus a margin, and run a memory pilot before enumerations.
- **Timing-comparable runs:** `--constraint=sapphirerapids`.
- **Accounting.** Account `commons`. There is no allocation balance, but heavy use lowers fair-share. A 1-CPU request bills as 2.
- **Campaign ceilings.** At most 192 billed CPUs and at most 96 array tasks campaign-wide when throttles are raised (D47/D49/D50).
- **`squeue -u fb31` shows ALL of Felipe's jobs**, including other projects. Throttle and cancel by explicit job ID only.
- **Escalated SMC fits (~8.7%) need the long unit limits:** L500 = 6,300 s, L1000 = 24,000 s (v2.1 production). The v2.2.1 bundles carry their own limits; use the bundle's `JOB.md`.
- **Waiters and watchers** must detect terminal states correctly and wake on STOP/FAILED lines. A broken poll once left a thread idle for 8 h (D43, D69).

## Storage
| Path | Quota | Use |
|---|---|---|
| `/home/fb31` | 10 GB hard, shared with Felipe's tool state | campaign ≤ 0.5 GiB, total < 9.6 GiB (D7) |
| `/home/fb31/projects/BVS/New_Campaign/` | — | the only campaign home folder; code, manifests, small inputs |
| `/scratch/fb31/New_Campaign/` | none shown; filesystem ~82% full | bulky transient outputs + logs; **purgeable** (no documented age; treat it as purgeable after about 2 weeks) |
| `/projects/ml75` | ~100 GB group quota, shared | no hefty data |
| Owls `/home/fb31` | about 1.36 TB free of the user quota (2026-10-29), shared with Felipe's other work | the repo; bulk data in git-ignored `_data/` |

- **Home on 2026-11-02** was about 9.49 GiB. Growth comes mostly from Felipe's own `~/.codex` releases and `~/.vscode-server` (both kept, by policy).
- **Disk-quota truncation is silent.** Always audit expected against analysed counts, and rerun with the same seeds.
- **The disk guard's `du` fails while truth trees are locked** (mode 000). Serialise guarded staging after each truth unlock (D59).
- **Clean-up must run from outside the tree it deletes**, because NFS leaves `.nfs*` files (D44 B3).

## Transfers
- **Speed.** NOTS → PC runs at about 3–10 MB/s, so long pulls must survive outages. Use one driver per disjoint unit list.
- **Tools.** `ops/transfer/nots_pull.py` (pull + manifest verify + receipt), `remote_pack.sh` and `verified_delete.sh`. The pull refuses to merge into a non-empty local destination; pull into a fresh sibling folder (D69).
- **Windows tar** does not recreate symlinks, so symlink "FAIL" lines in relocation checks are false alarms.
- **Destinations.**
  - Until cutover, the campaign data mirror is on Felipe's PC (OneDrive "NOTS Data/New_Campaign").
  - After cutover, bulk data lands on Owls `/home/fb31/BVS_GH/_data/` (git-ignored).
  - Earlier campaigns' data is in the PC archive "NOTS_BVS". Its relocation manifests are durable there; the NOTS copies are purgeable.
  - An always-on retrieval route that does not need the PCs must be tested before the new HQ takes authority (`ASTRA_HANDOFF_PLAN.md` §D).

## Failure modes seen (and the fix)

| Incident | Fix |
|---|---|
| OAuth/credential expiry killed HQ and workers (watchdog runs failed; D24, D25, D60) | A human re-login. The PC recipe uses the Claude Personal config dir with `claude auth login` / `claude auth status`; the Owls equivalent is to be determined at bootstrap. The new HQ needs an out-of-band alert |
| Laptop sleep / T3 restarts (D57, D60: 31 h outage) | NOTS jobs continue; every thread resumes from its `PROGRESS.md`. Never trust a watcher, only file timestamps and rc files |
| Bash permission prompts block agents silently (D37/D38) | Approval-safe tooling (`RULES.md` §4); the watchdog checks pending approvals |
| A provider-error rerun sat queued for 6 h (D21) | `task_cancel` and relaunch |
| A hard-coded 30-min scan limit timed out (D63) | Limits scale with the work: max(2 h, 600 s + 2 s/record) |

- **Watchdog cadence** used: a check every 30 min; foreground polls ≤ 10 min; nudge after 45 min with no file change.
- **Rice CRC help:** the Rice research-computing help desk (see the CRC website).
