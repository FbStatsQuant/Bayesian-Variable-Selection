# NOTS facts (read by Felipe on loginx3, 2026-11-15; pasted to the Exp thread). Read-only commands.

- commons: Sapphire Rapids, 70 nodes × 192 CPUs (60 × 257 GB, 10 × 515 GB, 1 of them drained); Cascade Lake, 72 × 80 CPUs, 187 GB.
  At reading: no SPR node fully idle (64 mixed, 5 allocated); 19 Cascade Lake idle.
- SPR node bb2u24c1: 2 sockets × 48 cores, ThreadsPerCore = 2, CPUTot = 192, CfgTRES billing = 192
  → billing is per hardware thread; a single-thread task = 1 core = 2 billed CPUs.
- QOS (sacctmgr):
  - nots_commons: MaxWall 1-00:00:00, **MaxTRESPU cpu=1536, mem=2304G**, MaxSubmitPU 5000.
  - nots_long: 3-00:00:00, cpu=384, mem=1T per user.
  - nots_scavenge: 01:00:00, MaxJobsPU 300, MaxSubmitPU 5000.
- Association (fb31): commons/debug/long/scavenge, no extra MaxJobs/MaxTRES/GrpTRES.
- Consequences:
  1. Per-user ceiling = 1,536 CPUs = 768 physical cores, and **2.3 TB of memory summed over running jobs**.
     → one multithreaded process per island (shared X, tables, store), not many single-thread processes.
  2. "billed core-h = 2 × thread-h" in the plan holds for one thread per core. Hyperthreads could buy 10–30% (UNVERIFIED).
  3. Ceiling throughput ≈ 36.9k billed CPU-h per day.
- Billing confirmed (sacct 2692690_1, the 5k profile fit): ReqCPUS 1 → AllocCPUS 2, AllocTRES billing=2,cpu=2,mem=12G;
  CPUTimeRAW 88,060 = 2 × ElapsedRaw 44,030.
- Load at reading (sinfo %C, A/I/O/T): Sapphire Rapids 8,270 / **4,978 idle** / 192 / 13,440; Cascade Lake 2,400 / 3,360 / 0 / 5,760.
  934 jobs pending in commons, yet ~5k SPR CPUs idle → most pending jobs are probably held by per-user limits or constraints.
  Our 1,536 cap fits inside the idle pool today; the open question is fragmentation (free CPUs per node).
- `scontrol show partition` takes a single name (the three-name form errors); not needed.
- Storage (quota -s, df):
  - **home: 10,159M used of 10,240M quota (99%; ~80 MB left)**, 115k files.
  - Group allocation data191:/rhf/allocations/ea14: **16,384G used, limit 16,384G (asterisk = at or over quota)**, 4.05M files.
  - /scratch (VAST, shared): 887T, 761T used, 127T free (86%); no per-user quota shown; purge policy unknown.
  - → All P1M I/O goes to /scratch. Nothing is written to home or the allocation. FLAG to HQ: home and allocation are full now
    (risk to any running job that writes logs or caches there).
- Free CPUs per SPR node at reading: 41 nodes with ≥ 64 free, 25 with ≥ 96, 4 with ≥ 128, 7 with 0.
  → 16 tasks × 64 CPUs (1,024) or 16 × 96 (1,536 = cap) would fit by CPU count today.
  Caveat: bb2u24c1 showed 104 idle CPUs but AllocMem 253,952 of 257,124 MB → free CPUs can come with no free memory.
  Memory per node to be checked (sinfo -O AllocMem).
- UPDATE (HQ, 18:52 CST): home = 6,770 MB of 10,240 MB (66%), from `quota -s | grep -A1 export/nots/home | tail -1`; guard 8,192 MB.
  No action on home. Our earlier 10,159M was read from the `nfs1:/export/nots/home` row of the owner's screenshot, so it was the
  home line at that moment. The ~3.4 GB difference is most likely space freed between the two readings, or quota reporting lag.
  ea14 (16 TB, at limit) is a separate project allocation. Plan outputs go to /scratch only (unchanged).
- **Direct read-only access from Owls (`ssh nots`) is live** (HQ, 11-15; POLICIES §5 220b4901). Submission still needs HQ's go per batch.
- First own read (11-15 ~21:20 CT, loginx3), memory-aware fragmentation: 70 SPR nodes. With ≥ 32 GB of *unallocated*
  memory: 19 have ≥ 64 free CPUs and **only 10 have ≥ 96 free CPUs**.
  → Free memory, not CPUs, binds. 16 island tasks of 96 CPUs + 32 GB would not all start now; 64-CPU tasks (19 nodes) would.
  Default island task: 64 CPUs (32 cores) + 32 GB; 96 only when available. Load: SPR 8,742 / 4,506 idle / 192 / 13,440.
- B3 jobs (sacct, REQUESTS R5): 5k 15:30:05 elapsed, MaxRSS 1.22 GB (ReqMem 16G); 10k 10:29:18, 2.38 GB (20G);
  20k 15:29:51, 6.64 GB (36G). All 2 CPUs. The 20k RSS includes the Gram (p² doubles = 3.2 GB).
- **Usage discipline (owner, POLICIES §12 rule 7, "be chill, do not swarm"; the account was flagged two weeks ago).**
  - SSH multiplexing on Owls for host `nots` (ControlMaster auto, ControlPath ~/.ssh/cm-%r@%h:%p, ControlPersist 10m;
    configured 11-15 by Engineering; backup ~/.ssh/config.bak-20261115-2021). Verified: `ssh -O check nots` → Master running.
  - One connection per session; no parallel logins; polling ≤ 1 squeue/sacct per 5 minutes; batches as job arrays only
    (≤ 150 tasks); no scans or unusual tools.
  - Owls: ramp gradually, ≤ 16 cores.
  - Anything that might look odd to Rice IT → ask HQ first.
- **Scratch purge policy (Rice CRC KB, read 2026-11-15).**
  - https://kb.rice.edu/147975 ("CRC Data and Quotas", updated 2026-11-09): `$SHARED_SCRATCH` = /scratch, quota None,
    VAST, **purge policy 14 days**. "Staff may periodically delete files from the $SHARED_SCRATCH file system even if files
    are less than 14 days old." "$SHARED_SCRATCH is to be used only for job I/O. Delete everything you do not need for
    another run at the end of the job or move to $WORK for analysis."
  - https://kb.rice.edu/147979 (2025-01-31): "may be subject to catastrophic data loss!" "A "cp" will update the access
    time on files whereas a move "mv" will preserve the access time … our periodic cleaning mechanism may purge files where
    the access time is maintained via the "mv" command." So the purge keys on **access time** (inferred), and a `mv`
    keeps the old atime.
  - https://kb.rice.edu/108229 (Retention, 2026-09-24): "Backup and archival of data remains the sole responsibility of the
    end user." No backups of scratch.
  - Observed: reading files does not refresh atime here (census_p5000.rds atime 2026-11-12 after reads on 11-15).
  - **Consequences.**
    - Scratch is for in-flight job I/O only. Nothing of record stays idle there longer than **7 days** (half the window,
      HQ rule).
    - The department `scratch/archive/` is **not** an archive. Results of record leave scratch within 7 days of creation
      (to the laptop route, or interim staging on Owls).
  - `$WORK` = /storage/hpc/work (256 TB, 13% used). No user directory exists for fb31; there is a group directory
    `/storage/hpc/work/ml75` (group ml75). Not touched: it is the advisor group's space; HQ or the owner decides.
