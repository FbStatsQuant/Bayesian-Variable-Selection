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
