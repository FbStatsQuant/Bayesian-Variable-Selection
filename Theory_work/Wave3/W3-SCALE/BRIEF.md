# W3-SCALE — track 3 (scaling), leg A → CP1

Owner goal (Felipe, 2026-11-10, binding): SMC-BVS must be feasible at p where sequential methods break (1k–10k+, later
far beyond), on NOTS. Expect a massive re-engineering; efficiency in EVERY component (scoring, start tables, SMC stages,
calibration, searches, memory, I/O). The paper's theory must stay valid for whatever ships: output-preserving changes
first; anything output-changing goes through the registry/lifecycle. The final theory must cover the parallel
(many-island, merge) method.

Read first: Theory_work/Pause_2026-11/SCALING_DESIGN_v0.md (limits, measured speedups, 16 theory obligations),
Theory_work/Pause_2026-11/RERUN_SPEC.md (A1–A8, PROD-H), Theory_work/Pause_2026-11/scaling_scratch/,
Wave3/PROTOCOL.md, Wave3/HOLDS.md. Production code: Scripts/SMC_BVS/core (v3.1).

Leg A (HQ-approved 2026-11-11 with consultant advice; Felipe delegated). Order matters:
1. PROFILE FIRST (submit to NOTS early, code while it runs): v3.1 time + peak memory by phase at p = 1k, 5k (full
   fits); at most ONE full fit at 10k, admitted only after the 5k measurement; 20k as a single island with N ≤ 2,500.
   Measure the stage count T (unverified in v0).
2. v3.2-dev, bit-identical speedups only: incremental-Cholesky block tables, neighbour graph, LS0 preflight delivery
   fix (v3_fit.R:44 scan-size refusal from p≈2.3k), Gram speedup. NOT in leg A: Gram-free scoring (needs the Phase 2
   per-particle factor cache; Gram still fits at 20k).
3. BIT-IDENTITY ON NOTS: on the PROD-H node type and toolchain, ≈24 PROD-H units (one per cell) under RERUN_SPEC A1–A8,
   v3.1 vs v3.2-dev, covering the fallback score routes, escalated fits, the exact branch and tie cases. This doubles
   as track 1's gate 0.
4. FREE TASK (no compute): tabulate sd(log Ẑ_r) by p from the 2,394 PROD-H records and the P6 runs (evidence for the
   island-degeneracy question).
5. DESIGN_v1.md LAST, from measured numbers: islands, evidence-weighted merging + effective-number-of-islands
   diagnostic, O(np) memory, the parallel-SMC theory obligations. If CW runs short, DESIGN_v1 slips to leg B.

NOTS budget, leg A: hard cap 150 task-hours (≈300 billed core-h at 2 CPUs/task). Keep an admission ledger in LOG.md
(worst case admitted before each submission, sacct actuals after). Commons/scavenge only. W3-P6 keeps queue priority
(do not crowd its jobs). Check HOLDS.md before every submission; a `HOLD SCALE` line stops submissions.

Reserved for Felipe — do NOT decide, only frame with numbers in CP1: (i) p = 1M via fixed N per island (reverses the
v3.1 "never split N_e" ruling); (ii) switching the primary PIP from equal-weight (v3_run.R:162) to evidence-weighted.

Reviews: Sol (codex gpt-6.1-sol, high) code review of the bit-identity claims and test coverage; Astra (codex
gpt-6-astra, high) break review of DESIGN_v1 if written. Claude agents: Claude Work (claudeAgent) only, effort ≤ high;
never the claude-personal provider. Parallelism: lead + its reviewers.

Stop at CHECKPOINT_1.md (profile tables, bit-identity verdict, ledger, sd(log Ẑ_r) table, DESIGN_v1 or its slip,
leg-B proposal with cost). HQ audits. Leg B may be HQ-approved only while it stays bit-identical.
