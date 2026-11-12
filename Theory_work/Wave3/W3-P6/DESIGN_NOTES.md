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

## N2. Reference hardware and hardware reruns — 2026-11-12 15:05 CT, HQ decision on the 13:23 return (consultant concurs), before any affected outcome is seen
1. **Reference hardware:** NOTS commons `sapphirerapids` nodes (bb*, feature `sapphirerapids,ib`). The allocation was
   costed on these nodes (smoke S1–S5).
2. **Hardware rerun.** On non-reference hardware (`cascadelake`, bc12*), any time-dependent stop is a hardware rerun:
   the 22.5-h runtime guard, a preflight stop, an escalation refusal, or a Slurm time-limit kill.
   - It is neither a failure nor censoring.
   - It is applied mechanically, whatever the HPM so far.
   - The slow-node record is kept and logged, but never pooled.
3. **Valid on cascadelake:** a fit that completes on cascadelake with no such stop is valid.
4. **How a hardware rerun runs:**
   - new RUN_ID, same seed, `--constraint=sapphirerapids`;
   - it does not use the rerun-once allowance for a genuine Slurm failure (N1.4).
   - Tasks cancelled by HQ decision for this reason (s1_c 1–9, s1_b 1–9, s1_d1 4–5) are hardware reruns.
5. **Node type for every fit:** sacct NodeList mapped to the node feature, recorded for all `w3p6_` fits (b1, probes,
   smoke, stage 1).
6. **All further P6 releases** use `--constraint=sapphirerapids`.
7. **Budget for stage 1:**
   - The projection stop moves from 1,700 to the 1,896 ceiling; the cause is hardware loss. The HQ watchdog line is 1,880.
   - If the ledger does not fit, cut in this order: (75,75) first, then (100,100), then reps 6–10 of the two breadth cells
     (h1b/h2b).
   - The four D1 cells are never cut.
