# NOTS core-hour ledger — SMC - Engineering Department

Envelope: **A + D ≈ 24,600 billed core-h** (HQ, 11-15; DECISIONS H-1).
Rules:
- **Exploratory batches** ≤ ~200 core-h each run on the HQ standing authorisation (11-15). They are logged here and in the
  daily report.
- **Gated stages** and batches above ~200 core-h need HQ's go.
- Billed core-h = allocated CPUs × elapsed (sacct CPUTimeRAW / 3600).
- Admission check before each submission: Σ actual (finished) + Σ worst case (time limit × CPUs, queued and running) +
  this batch's worst case ≤ envelope.

| date | batch | kind | job ids | worst case | actual | status |
|---|---|---|---|---|---|---|
| 2026-11-15 20:53 CST | G0 kernel benchmark (1 SPR node, 96 CPUs, 5 min) | gated (HQ go 11-15) | 2747371 | 8.0 | **0.88** | COMPLETED (33 s; benchmark segfault after the T = 1 offer test, results kept) |
| 2026-11-15 20:53 CST | G0 stage-level re-runs (5k: 16 islands, 7 h limit; 10k: 8 islands, 17.5 h), revision D unmodified | gated (HQ go 11-15) | 2747372_[1-2] | 49.0 | task 1: 0.001 (FAILED in 2 s: invalid `timeout 6h57m`); task 2 running | task 1 failed, task 2 RUNNING |
| 2026-11-15 22:10 CST | G0 stage task 1 rerun (5k, 16 islands; timeout fixed to 417m) | gated (within the G0 approval) | 2747799_[1] | 14.0 (replaces task 1's reservation) | — | submitted |

| 2026-11-15 21:28 CST | pmath bind check (WP1 PR #11 v4_pmath_check on SPR; 1 CPU, 15 min) | exploratory (standing authority) | 2747501 | 0.5 | 0.003 | FAILED (5 s; module load missing Lmod init; no compile) |
| 2026-11-15 21:40 CST | pmath bind check, rerun with the G0 module init | exploratory | 2747524 | 0.5 | 0.001 | FAILED (1 s; CMake 3.27.6 needs GCCcore 13.2; nothing compiled) |
| 2026-11-15 21:52 CST | pmath bind check, rerun 2 (GCC 14.3.0 + CMake 3.31.8) | exploratory | 2747598 | 0.5 | 0.001 | FAILED (2 s; pipefail on `g++ --version \| head`) |
| 2026-11-15 22:00 CST | pmath bind check, rerun 3 | exploratory | 2747666 | 0.5 | 0.04 | COMPLETED (75 s; 7/9 hashes equal; log1p, expm1 differ, unused by core) |

| 2026-11-16 00:2x CST | pmath check 2 (PR #15 5e3d5bf: + expl/logl rows) on SPR | exploratory | 2747875 | 0.5 | 0.05 | COMPLETED (83 s; expl/logl equal; all 8 guarded rows match) |
| 2026-11-16 00:3x CST | WP3 class-A island bench on SPR (820bd30; p = 10⁴ adaptive + geo:30 at 24/48/96 threads; p = 10⁵ at 48/96; 96 CPUs, 12 min) | exploratory | 2747881 | 19.2 | — | submitted |

**Totals:** actual 0.883 · reserved (worst case, open) 49.5 · remaining ≈ 24,543 (admission check: 0 + 57.0 ≤ the G0 cap of 71.5 and ≤ the envelope).
