# FULL_STUDY_RERUN_PLAN: the full simulation study on the frozen method `method-v3.1.1-listpip` (DEFERRED; Sonnet planner, 2026-11-18)

Planning only: nothing submitted, no NOTS connection, no git change. The owner is not asking for this now.

## Summary (8 lines)
1. **What:** the SMC rows of the paper's two simulation studies: PROD-H (p ≫ n, 2,400 fits) and PROD-L (p ∈ {20, 30}: 2,400 primary + 12,000 repeat fits, exact reference). Benchmarks (F1–F5, A1–A3) are other methods on the same datasets: NOT rerun.
2. **New side only, not paired.** The 242-fit subset gave 120/120 identical legacy fields, 121/121 identical X/y, 0 completed→stopped, runtime ratio 0.975. A paired rerun would add 906 core-h for no new information.
3. **Cost (measured basis): PROD-H ≈ 890 elapsed core-h (1,780 billed); PROD-L ≈ 30 elapsed (≈ 60 billed); total ≈ 920 elapsed ≈ 1,840 billed** (cap 1,000 + 40 elapsed). That is ≈ 6.5% of the 28.3k campaign cap. Paired would be ≈ 3,700 billed.
4. **Arrays (≤ 150 tasks each, 1 CPU, 2G, SPR):** PROD-H 150 + 100 tasks at %25 + %25 = 100 billed CPUs (6.5% of the 1,536 ceiling); PROD-L 96 + 120 tasks at %32. **Wall ≈ 1 day** (PROD-L ≈ 1.5 h first, PROD-H ≈ 18–22 h).
5. **Window:** after the 1M block (≈ 12-08+; submit 12-09, verdict ≈ 12-11), or PROD-L alone any quiet hour (≈ 1.5 h, ≤ 64 billed CPUs). HQ GO per batch.
6. **Comparator:** per-fit legacy-field identity against v2.2.1 records, plus the tables of record regenerated with the existing analysis scripts. Verdict: NO REGRESSION on the pre-registered rules (§5).
7. **Adds over the subset:** all 24 cells × 100 datasets, all 6 stops and the 208 escalated fits, the exact-reference check at v3.1.1 (never rerun at low p), list-PIP fields at full scale, the stop counts, and paper tables on the frozen method.
8. **Limit:** v3.1.1 has no plain-PIP or `instrumentation` fields, so plain-PIP rows of HEADLINE_H/L and instrumentation-based theory measures stay on the v2.2.1 records (disclosed). **Baseline per-seed records are on the desktop only: HQ must extract them (§6).**

## 1. What the paper needs (Docs/PLAN.md §2; CAMPAIGN_PLAN_20261028; Results/…/{H2,L}_20261102/HEADLINE_*.md)
| study | run of record | fits | SMC rows used by the paper |
|---|---|---|---|
| PROD-H | `20261030T0934Z_prodH`, v2.2.1 | 2,400 (p ∈ {500, 1000} × S1–S6 × r 1..100 × c ∈ {1, 0.5}); 2,394 ok + 6 `resource_limit` (all S5; p1000 r030 c100, r044 c100/c050, r064 c100/c050; p500 r088 c100) | recovery /100 and /600 by HPM, MPM (RB), MPM (plain); stops counted as misses; runtime/ev_cost |
| PROD-L | `20261030T1811Z_lowp_prodL` | 2,400 primary + 12,000 repeats (24 cells × 100 r × 5 seeds, seed = data + 4,000,000 + 1,000·m) + 1,200 exact enumerations | Q1 log Ẑ error, Q2 HPM, Q3 PIP error, Q4 recovery, stability, repeat-fit accuracy |
- NOT rerun: BENCH_F3_DEV/PROD (2,400), PROD_L_BENCH (19,200): other methods, datasets unchanged (PLAN §1.6 "benchmarks need no rerun"). After-the-fact theory audits (TD, π₀) read stored outputs.
- Strictly the paper needs only: the subset verdict (v3.1 = v2.2.1 on legacy fields) plus the v2.2.1 tables. The full rerun is the cleaner statement "the tables are produced by the method as frozen" (PLAN principle 2: executed method = written method). Nothing else in the 2026-10-28 campaign folder or PLAN.md is a simulation study.

## 2. New side only vs paired (recommendation: NEW ONLY)
- Same bits is already established on NOTS for the PROD-H legacy fields (`results/RERUN_2400_VERDICT.md`); C-ENG saw 48/48 identical at p = 30 and 3/3 at p = 500. LS0 reads no uniforms and runs after the final search; the paired timing ratio (0.975, worst cell 1.02) is already measured.
- The subset ran v3.1 (tag e9bac478); the full run is the first at v3.1.1 (7100bb3b). The guard changes only the list fields of stopped final runs; completed fits are unaffected (verdict file, last section). The full run confirms that at scale.
- Not recommended: re-running v2.2.1 alongside (+906 elapsed PROD-H, +30 low-p). It stays a fallback for any cell whose table differs.

## 3. Cost from the measured basis (elapsed core-h; billed = 2×)
| piece | basis | estimate |
|---|---|---|
| PROD-H p500 (1,200 fits) | v2.2.1 225.82 × 0.979 (new/old subset runtime sum 42.36/43.26 h) | 221 |
| PROD-H p1000 (1,200 fits, 5 stops × 24,000 s = 33.4 included) | 680.67 × 0.979 | 666 |
| **PROD-H** | v2.2.1 906.49 (`PRODH_COMPLETION:32`); range ×0.95–1.05 | **≈ 890 (860–950)**; 1,780 billed |
| PROD-L primary + 12,000 repeats | `PROD_L_SIZING_20261030` §3: 10.9 + ≈ 50 billed expected (conservative ≈ 95) | **≈ 30 elapsed**; ≈ 61 billed (≤ 100) |
| PROD-L exact reference | reuse stored (§6); fallback re-enumerate 600 × p20 + 600 × p30 at 16 threads: 73.1 + 1.3 billed (`PROD_L_SIZING` §3) | 0 (fallback +75 billed) |
Cap: 1,000 elapsed PROD-H, 60 elapsed PROD-L (+ 40 billed if re-enumerating). Campaign budget: ≤ 28.3k billed; the 1M block is ≈ 18–21k (`HQ_DECISIONS.md:726`), so the margin is ≈ 7–10k.

## 4. Arrays, throttles, wall (NOTS_FACTS §12: be chill; ≤ 150 tasks per array; one multiplexed ssh; poll ≤ 1 per 5 min; scratch only, pull within 7 days)
- Reuse `rerun2400/bundle_src` (new-side route `new_fit.R`: generate → `v3_fit` → record; `task.sh`, `submit.sh`, `precompile.*`, `comparator.R`, `collect.sh`), core tree = tag `method-v3.1.1-listpip` verified blob by blob. Changes needed: (a) a chunk table of all 2,400 PROD-H fits (units.tsv has 2,400 rows, `nots_runner/tables_production/`); (b) a low-p switch in `new_fit.R` using `code/lowp/R/lowp_generate.R` with the repeat-seed rule; (c) low-p comparator mode (vs exact). Same allocations as the 11-02 study (mem 2 G; L500 = 6,300 s; L1000 = 24,000 s; PROD-L as `RUN_DESIGN`/2 G, 4 h), so stops are like-for-like. One precompile job first.
| array | fits | tasks | per task (mean) | task wall | throttle |
|---|---|---|---|---|---|
| H-p1000 | 1,195 + 5 stops | 5 stop tasks (1 fit each, first) + 145 × ≈ 8 fits | ≈ 4.3 h (worst ≈ 11 h) | 16 h | %25 |
| H-p500 | 1,199 + 1 stop | 1 stop task + 99 × ≈ 12 fits | ≈ 2.1 h | 8 h | %25 |
| L-prim | 2,400 | 96 × 25 | ≈ 3 min | 1 h | %32 |
| L-rep | 12,000 | 120 × 100 | ≈ 12 min | 2 h | %32 |
- Wall: PROD-H 887 core-h / 50 concurrent tasks ≈ 18 h + tail (the stop tasks start first, 6.7 h each); ≈ 20 h with queue. At %20 + %20 ≈ 24 h; at %40 + %40 ≈ 12 h (160 billed CPUs, 10% of the ceiling). Recommend %25 + %25 after a first look at tasks 1–4 (heaviest: S4/S5). PROD-L ≈ 1.5 h incl. queue, run FIRST as the scale smoke. Total ≈ 1 day.
- Smoke before submit (Owls, nice 19): 2 p = 20/30 fits (≈ 7 s each; check `branch_run == "smc"`) and 1 p500 c100 fit (≈ 10 min).
- Output ≈ 4 GB PROD-H (1.7 MB/fit) + a few GB low-p; each task also writes a slim digest row per fit (legacy fields, vector hashes, list fields, runtime, RSS, node).

## 5. Comparator and verdict (pre-register; extends `rerun2400/bundle_src/comparator.R`, whose self-test had 14 checks)
1. Per fit vs v2.2.1: X/y SHA-256 match; `identical()` on `log_Z`, `log_Z_r`, `hpm`, `hpm_F`, `pip_primary`, `pip_r`, status for both-completed fits; 0 completed→stopped; each v2.2.1 stop stops again or completes finite (disclosed); `ls0_improved` HPM gains disclosed, not failed.
2. Tables of record regenerated with the existing scripts (`Scripts/Campaigns/2026-10-28_New_Campaign/analysis/{H2,L}_20261102/scripts`) and diffed: `headline_h2_long.csv` counts, `ev_cost.csv` (median/p90 runtime within ×1.25 per cell, pooled ≤ 1.10), `Q1_logZ`, `Q2_hpm`, `Q3_pip` (RB only), `Q4_recovery`, `stability`, `repeat_fit_accuracy`. Counts identical, rates to the table's rounding.
3. Low p vs exact: log Ẑ RMSE ≤ 0.015 (v2.2.1: 0.012), HPM = exact HPM in 100%, max |PIP − exact| mean ≤ 0.001.
4. RSS ≤ 1.2× (v2.2.1 max 477 MB at the stops).
**Verdict:** NO REGRESSION if 1–4 hold; else list the failing fits and diagnose (check data identity first). New descriptive gates (list-PIP, no baseline): list fields present on every completed fit and NA on stopped ones (v3.1.1 guard); `pip_list` ∈ [0, 1]; counts of `list_full`/`pip_list_flag`; max |pip_list − pip_primary| and `mpm_list` = `mpm` rates per cell; at low p, `pip_list` and `log_Z_list` against the exact posterior (new table, secondary).

## 6. Offload and baseline
- **Baseline (needed):** the v2.2.1 per-fit records exist only on the owner's desktop (`NOTS Data/New_Campaign/results/20261030T0934Z_prodH`, the low-p run, ≈ 4 GB + 2–3 GB; `Docs/Records/DATA_INDEX.md`); Owls holds aggregates only. Ask HQ for ONE extraction on the desktop: a file with, per fit (2,400 + 14,400 rows), the legacy fields at full precision (pip vectors included, ≈ 100 MB) and the 1,200 exact-enumeration results (≈ 120 MB), via the existing offload route (`Docs/Experiments/P1M/offload/`), sha256-checked. Without it, steps 2–3 of §5 still run (tables of record are in the repo) but step 1 (bit identity) does not.
- Records of the new run: pull from `/scratch` to `~/SMC_Engineering_Department/records/fullstudy/<run>/` within 7 days (14-day purge; Owls has 2.8 TB free); clean scratch after checksum; the data mirror copy goes through HQ's desktop route.

## 7. What it adds over the 242-fit subset
- Coverage: 100% of the 24 PROD-H cells (the subset was 5%: r ∈ {1, 25, 50, 75, 100}), including all 6 stops (subset: 1) and all 208 escalated fits; the stop COUNT is a study metric a 5% sample cannot estimate.
- Low p: never rerun on v3.1 (the plan's Tier C was dropped). Gives the exact-reference accuracy and the 12,000-fit stability tables on the frozen method.
- List-PIP fields at full scale, with their gates (the subset comparator never read them), and the v3.1.1 stopped-run guard on real stops.
- Paper tables (HEADLINE_H/L, ev_cost, stability) regenerated from the frozen method, minus the plain-PIP rows (§1, item 8).

## 8. Staffing and open choices
- Sonnet: bundle changes, low-p mode, comparator, smoke, regenerated tables; Haiku: submit/poll/collect per the RUN_LOG runbook; manager look + one Sonnet re-check. No Sol/Codex unless a regression appears.
- HQ/owner choices: (a) run at all vs keep the subset verdict plus v2.2.1 tables; (b) tiers: PROD-L only (≈ 60 billed, 1.5 h), + PROD-H (+1,780 billed, ≈ 20 h); (c) throttle %25 vs %20; (d) the desktop extraction (§6); (e) window (after the 1M block, or PROD-L in a quiet hour).
- Risks: baseline records unreachable (§6); PROD-H stops are wall-clock events and may differ (reported, not failed); queue wait on `commons` unknown; R 4.5.2 / GCC 14.3 on NOTS must match the earlier runs (the subset did).
