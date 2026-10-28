# Campaign 2 brief (Claude): SMC-BVS v3 on all 2,400 benchmark units (HQ, 2026-10-23)

This supersedes the OpenAI-era BRIEF.md where they conflict. Background: AUDIT_CLAUDE/AUDIT_SUMMARY.md, RULINGS_LEAD.md (R-1 adapter mapping; R-5; R-6 relabelled as a waiver), G1_PASSED.md (with its correction), C_ops/PILOT.md and C_ops/DATA_CHECK.md.

**Goal (Felipe):** empirical evidence of SMC-BVS v3 against the benchmarks. That means 100 seeds per scenario per p (S1–S6 × p ∈ {500, 1000} × r = 1..100 = 1,200 datasets), each at c100 and c050: 2,400 fits, on EXACTLY the benchmark study's inputs and seeds. Report how often each method recovers the true model, plus the error breakdown, against all benchmark methods.

## Fixed: no changes allowed
- The method: master Part I, implemented by A's frozen v2 core (`A_build/snapshots/v2`, archive SHA 17bdd21a…e1ff). Never retune.
- Seeds: method seed = data seed + 4,000,000, with data seeds from master §II.7.
- R-1 output mapping.
- The sealed holdout and truth are never read by fitting code.

## Places
- **Local.** This deployment folder. New Claude work goes in `E_ops_claude/` (ops thread) and `F_analysis_claude/` (analysis thread). The OpenAI folders A_build, B_verify, C_ops and D_analysis are READ-ONLY inputs.
- **NOTS code home.** `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/`. A reorganisation in progress is moving the copied infrastructure there; until it lands, the copy sits at `/home/fb31/projects/BVS/SMC_BVS_v3_deploy/`. Read 00_Admin/OWLS_MIGRATION.md "Phase 3" for its status.
  - Put new Claude code in `.../SMC_BVS_v3/deploy/claude/`.
  - Home quota is 10 GB: code only.
- **Outputs.** `/scratch/fb31/smcbvs_v3_deploy_20261022/`. When the run finishes, pull them to `C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\` (copy → sha256 → delete on NOTS). Never keep hefty data on NOTS.
- **Inputs.** `$STUDY` = /projects/ml75/fb31/BVS/bench20261019, `inputs/` and `manifests/` are READ-ONLY. Never write under $STUDY: a freeze is active.
- **Owls.** Not used; it is being cleared.

## Required fixes and readiness (AUDIT_SUMMARY decisions 1–4)
1. **v2.1 study-layer freeze** (the core is untouched): A-CODE F1, F3, F5 (F2 optional), and D-F1 handled on the analysis side.
   - An independent review is required: HQ arranges one Opus reviewer on the other account. Write the diff summary in `E_ops_claude/HANDOFF_v2_1.md`.
2. **Runner fixes:**
   - no GNU time; use R/proc VmHWM plus `sacct`;
   - explicit `module` initialisation in Slurm scripts (compute nodes lack /etc/profile.d/z00_lmod.sh);
   - resource kills count as infrastructure (rerun with the same seed);
   - unit limits derived from the NOTS smokes: 3× the observed whole-process wall time, rounded up to 5 minutes;
   - the in-run `--hours` equals the external unit limit.
3. **NOTS readiness, written up in `E_ops_claude/NOTS_READINESS.md`:**
   - build (GCC/14.3.0, R/4.5.2);
   - A's 32-seed regression (must be 32/32);
   - B's battery (unchanged scripts);
   - tiny-p SMC versus exact: (n, p) chosen so v3 takes the SMC branch but enumeration is feasible (for example p = 18–20, n ≈ 30). At least 5 seeds; compare log Ẑ and PIPs with B's exact oracle, and report the errors.
   - the 2 dev smokes;
   - ONE real fit end to end through the production runner and transfer.
4. **HQ GATE:** HQ (with an independent reviewer) reads NOTS_READINESS.md and writes `E_ops_claude/GO_2400.md`. No production array runs before it.

## Production, after GO_2400
- **Array:** one Slurm array over dataset-keyed chunks (each task runs its c100 then its c050 unit). Frozen snapshot plus manifest.json, rows in RUNS.md.
- **Resources:** 1 CPU and 2 GB per task. Throttle at most %100 (NOTS commons is large; be a good citizen).
- **Monitoring:** poll at most every 10 minutes, with one ssh connection at a time.
- **Reruns:** only for infrastructure failures, with the same seeds. Timeouts are recorded, never extended.
- **Pull** to the laptop with verification, then write `E_ops_claude/OUTPUTS.md`.

## Rules
- **Models:** Opus leads. Use Sonnet freely and Haiku for mechanical work; plant canaries in Haiku batches. Workers never verify their own work.
- **SSH:** batch commands, never connection bursts; back off 15 minutes after a timeout.
- **Usage limits:** pause and resume; never abandon.
- **Status:** keep `<your folder>/STATUS.md` current (phase, job IDs, blockers, Requests to HQ, resume point, agent counts).
- **Ledger:** stage CODE_LEDGER candidates in your folder; HQ merges them.
- **Never fabricate.** Report failures plainly.
- **Writing:** simple language in summaries; Felipe is new to the field.
