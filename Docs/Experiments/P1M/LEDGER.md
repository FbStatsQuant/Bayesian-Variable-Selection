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
| — | (none yet) | | | | | |

**Totals:** actual 0 · reserved (worst case, open) 0 · remaining ≈ 24,600.
