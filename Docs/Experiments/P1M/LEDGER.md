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
| 2026-11-15 20:53 CST | G0 stage-level re-runs (5k: 16 islands, 7 h limit; 10k: 8 islands, 17.5 h), revision D unmodified | gated (HQ go 11-15) | 2747372_[1-2] | 49.0 | — | submitted |

**Totals:** actual 0.88 · reserved (worst case, open) 49.0 · remaining ≈ 24,543 (admission check: 0 + 57.0 ≤ the G0 cap of 71.5 and ≤ the envelope).
