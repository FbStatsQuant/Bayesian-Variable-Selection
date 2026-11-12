# W3-P6 — DESIGN notes (pre-declarations; additions to DESIGN.md v2, which is unchanged)

## N1. Stage-1 outcome rules — pre-declared 2026-11-12 10:45 CT, before any stage-1 task is submitted or any stage-1 outcome is seen
Source: HQ_DECISIONS "W3-P6 CP1 ACCEPTED" (commit 703a6b2), on CHECKPOINT_1.md.

1. **Failure:** a completed fit whose HPM under the MR1 cap (method as coded: ℓ_n + |S̃₀|) ≠ S₀. Both classes count
   (posterior, search).
2. **Censored:** a fit stopped by the 22.5-h in-fit runtime guard (status `resource_limit`). It is neither a failure nor
   a success. It stays in the denominator and is reported by the bounds of DESIGN §6: [k/sched, (k + sched − e)/sched].
3. **Infeasibility:** ≥ 3 censored fits among the 10 stage-1 seeds of a cell is an infeasibility finding. Stop releasing
   that cell and return to HQ.
4. **Slurm kills** (TIMEOUT, node failure; no RDS): one rerun, same seed, new RUN_ID, at 24:00:00. The rerun reserves
   48 core-h and passes the same admission check before release. A Slurm kill is not a failure.
5. **Stage 2 (reps 11–20) is conditional.** It runs only on cells with 1–3 failures among reps 1–10, and only within
   budget. Otherwise HQ asks the owner.
6. **Admission before every release:**
   - L = CPUTimeRAW of finished `w3p6_` allocations since 2026-11-09 + Σ(time limit × 2) over queued and running tasks.
     Release only if L ≤ 1,896.
   - Projected total (finished + measured median × 2 for every running, queued and remaining stage-1 task) must be
     ≤ 1,700. Otherwise stop and return to HQ.
   - Read HOLDS.md before each release.
7. **Stage-1 schedule** (CHECKPOINT_1 §3, as amended by HQ):
   - **Wave 1:** d1, h1, h2, c, b, b1r (all 21).
   - **Later waves, in this order:**
     - d2, after d1;
     - h1b / h2b, after h1 / h2, at 1.5 × measured max;
     - e = (100,100) reps 1–10, limit 04:00:00, after b1r;
     - g1, then g2;
     - f1, then f2.
