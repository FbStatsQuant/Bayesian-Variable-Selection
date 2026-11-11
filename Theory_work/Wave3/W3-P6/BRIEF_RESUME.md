# W3-P6 resume — lead brief, leg A (HQ, 2026-11-11)

You are the **lead** of W3-P6 (Claude Opus 5.5, effort high, Claude Work). Worktree `C:/Users/felip/BVS-wt/W3-P6`
(branch `theory/W3-P6`); folder `Theory_work/Wave3/W3-P6/`. **Change no git state** (HQ commits). Effort never above high.

## Read first
`Theory_work/Wave3/PROGRAM.md` (Decision D1), `Theory_work/Wave3/PROTOCOL.md` (all; **rule 10 "Compute tickets"**: CP0 smoke
manifest, CP1 smoke gate, batch release, 1,400 core-hour ceiling with worst-case admission; rules 11–16), this ticket's
`DESIGN.md`, `LOG.md`, `reviews/`, and `Theory_work/Pause_2026-11/RESUME_PLAN.md` §2 (W3-P6 state at the pause:
b1 298/320, b2 0/240 cancelled; preliminary reading at n = 50).

## This leg: CP0 only — NOTHING is submitted on NOTS
NOTS use in this leg is **read-only** (ls, cat, sacct, squeue, reading result files) and only under
`/home/fb31/projects/BVS/theory_w3` and `/scratch/fb31/theory_w3`. Never touch `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/`
or `/projects/ml75`. Never run sbatch, scancel, or anything that writes on NOTS.

1. Reconcile the state: what finished in b1/b2/probes (read back from NOTS), which tasks remain, which scripts are frozen
   for each (sha256), and the core-hours already used by every w3p6_ job since 2026-11-09 (sacct CPUTimeRAW).
2. Write `CP0_SMOKE_MANIFEST.md`: the **smallest representative smoke set** — covering both driver versions (b1 v2,
   b2 v3), each n level, and the most expensive calibration regimes (largest p per n) — with, per task: cell, seeds,
   scripts sha, Slurm time limit × cores, and the **worst-case admission** total (Σ time limit × cores + core-hours used),
   which must be ≤ 1,400. Also give the projected release plan after the smoke (batches, worst-case and expected cost
   each) and what you would report at CP1.
3. **CP0:** write `CHECKPOINT_0.md` (state reconciliation, smoke manifest summary, admission arithmetic, risks) and **end
   your run** with that content as your final message. HQ (and the owner) approve before anything is submitted.

LOG.md heartbeat at every step (timestamp in real local time; agents started: model, provider, role). Read
`C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave3/HOLDS.md` before each step; a `HOLD P6` line stops you.
No subagents in this leg. Keep replies short; details in files.
