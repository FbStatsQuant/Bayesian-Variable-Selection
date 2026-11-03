# NOTS environment notes for later phases (probed 2026-10-29 on loginx2)

Raw: `evidence/inv3_raw.txt` (and `evidence/inv4_raw.txt` for the purge check).

## Access
- `ssh nots` → loginx2 (<internal-ip>), key `~/.ssh/id_rice`. Only the OPS thread connects. Batch the commands.
- **Connection limit, HQ D76 (2026-11-02; was "one connection at a time").** At most **two** concurrent connections from this laptop, one per lane, each lane serialised by its own lock in `ops/scaffold/sshlock/`:
  - **bulk**: long transfers (pulls, uploads). Lock `/tmp/nots_ssh.lock`. Used by `with_lock.sh`, whose default lane is bulk.
  - **control**: short commands (squeue/sacct, monitor and waiter checks, starting and polling detached steps, small deletes). Lock `/tmp/nots_ssh_control.lock`. This is the ssh shim's default lane, and the shim bounds every control command at **5 min wall** (`timeout 300`, exit 124).
  - Choose the lane with `NOTS_SSH_LANE=bulk|control`. Re-entrancy is per lane only.
  - Steps that can take longer than 5 min (stage/guard, launch.py, cleanup, BENCH submit) run **detached on NOTS** through `ops/scaffold/remote_bg.sh`. It starts the step with one short control ssh (output in `/scratch/fb31/New_Campaign/upload/ops_bg/<name>.out`, final line `BG_EXIT rc=N`), then polls it with short control calls every 60 s. It never runs the same name twice.
  - Unchanged: the alias `ssh nots` only; the 15-min back-off after any timeout or reset, in both lanes; ServerAliveInterval 30 × 4.
  - Offline test: `ops/scaffold/sshlock/test_lanes.sh` (9/9 PASS 2026-11-02). Live test: a 75 s detached step on the control lane while the bulk pull held its lane (rc propagated).
- 2026-10-29 01:10Z: a connect timeout followed about 8 short connections in 3 minutes, so keep bursts small. After a timeout, back off 15 min.
- From Git Bash, `/scratch/...` arguments get rewritten to `C:/Program Files/Git/...`. `nots_pull.py` undoes this; for other tools, set `MSYS_NO_PATHCONV=1`.

## OS and software
- RHEL 9.4, kernel 5.14. Default login toolchain: GCC 13.2.0 (OpenMPI 4.1.6, FlexiBLAS 3.3.1 loaded by default). R is not on PATH until a module is loaded.
- **R modules:** R/4.2.1, 4.2.2, 4.3.2, 4.3.3, **4.4.1**, 4.4.2, 4.5.2, 4.6.1. R/4.4.1 sits under GCC/13.2.0 (`module load GCC/13.2.0 R/4.4.1`; GCC/13.2.0 is already loaded at login. Not yet test-loaded by OPS; the pilot should confirm it.) and matches the laptop's R 4.4.1. Also available: R-bundle-CRAN/2024.06, R-bundle-Bioconductor/3.19-R-4.4.1, arrow-R.
- **Compilers:** GCC 11.2–15.2 (Core); intel-compilers 2021.2–2025.3.3; toolchains foss/2022a–2026.1 and intel/2023a–2026.1. BLAS: FlexiBLAS 3.3.1, OpenBLAS 0.3.24 (GCC 13.2).
- The earlier campaign used the read-only R library `/home/fb31/projects/BVS/library_portable` (benchmark packages). The v3 core compiles Rcpp code into a `.cpp_cache`, which must stay owner-writable (campaign-2 gotcha).

## Slurm
| Partition | Time limit | Nodes | Notes |
|---|---|---|---|
| commons (default) | 1 day | 142 | mixed: 72 Cascade Lake (80 cores, ~187 GB) + 70 **Sapphire Rapids** (192 cores, ~257 GB, `ib`) |
| long | 3 days | 61 | mostly Sapphire Rapids |
| scavenge | 1 h | 154 | preemptible |
| debug | 30 min | 2 | Sapphire Rapids |
| ea14, deepsC, as143, … | — | — | group partitions; our association has only commons, debug, long, scavenge |

- DefMemPerCPU = 1024 MB on every partition, so always request `--mem` or `--mem-per-cpu`.
- **Sapphire Rapids constraint:** `#SBATCH --constraint=sapphirerapids` (feature name `sapphirerapids`). It is required for timing-comparable runs (charter §3), and the campaign-2 unit limits (L500 = 1500 s, L1000 = 5400 s) were measured on these nodes.
- Account `commons`, QoS `nots_commons`/`nots_long`/`nots_debug`/`nots_scavenge`. No per-user maxjobs/maxsubmit shown by `sacctmgr`.

## Storage
| Path | Quota | Policy |
|---|---|---|
| /home/fb31 | 10 GB hard (nfs1) | shared with Felipe's other work and with tool state (.vscode-server, .codex, .claude, .t3) |
| /projects/ml75 | group quota (~100 GB; 80 GB used) | shared with the ml75 group |
| /scratch/fb31 | no user quota shown; filesystem 82 % full | **purged**; see below |

**/scratch purge age: not documented on the node, and the web search found no Rice page.**
- `/etc/profile.d/crc-settings.sh` only sets `SHARED_SCRATCH=/scratch` and `LOCAL_SCRATCH=/tmp`. `/etc/motd` says nothing about purging.
- Observed: files in `/scratch/fb31` with last access 2026-09-15 (`.claude-science`) and 2026-09-29 (`fsb_deploy*.tar.gz`) still existed on 2026-10-29. So nothing older than about 44 days by atime has been purged yet.
- Working rule: treat scratch as purgeable at any time after about 2 weeks, and never keep the only copy there (charter §2). HQ may ask Rice CRC for the exact policy if it matters.
