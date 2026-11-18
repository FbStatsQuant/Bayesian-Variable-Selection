# RERUN_2400_PLAN: subset rerun of the 2,400-fit study on the frozen method (v3.1: v3 core + LS0 + list-PIP fields)

Sonnet research helper for Engineering, 2026-11-17. Planning only: nothing submitted, no NOTS connection, no git change.

## Manager decision (proposal to HQ; supersedes the helper's routes where they differ)
- **Simplify: run BOTH cores on the same NOTS SPR nodes, Tier A + the one p500 stop.**
  - The old per-seed v2.2.1 outputs are on the desktop only, and the desktop has no VPN now. So rerun v2.2.1 (its hash-checked tree in the repo) side by side. 11-02 showed v2.2.1 reproduces its stored records exactly (2,400/2,400), so the rerun IS the v2.2.1 reference, on the same machine, toolchain and day: no cross-machine libm doubt, no pull, paired timings.
  - Optional later cross-check: compare against the 126 stored records once the desktop pull resumes.
- **Fits:** 2 × 121 = 242 (Tier A 120 + `p0500_S5_r088_c100`, each on v2.2.1 and on v3.1). Drop the five p1000 24,000 s stops: they cost 33 core-h each side and make the wall 8 h. Tier C (low-p) is out ("keep it simple"; no exact-reference add-on).
- **Core-h:** 2 × (45.3 + 1.75) ≈ 94 elapsed (188 billed). Cap 120 elapsed.
- **Arrays:** v2.2.1 and v3.1 each as p1000 30 tasks + p500 31 tasks = 4 arrays, 122 tasks, %20 each, 80 billed CPUs at most.
- **Wall:** ≈ 4–5 h (a p1000 task = c100 + c050 ≈ 3,200 s median, up to ≈ 8,000 s for S4/S5; 30 tasks at %20 run in 2 waves).
- **Harness:** v2.2.1 = its original study layer unchanged; v3.1 = the `list_pip_ab/ab_run.R` route (generate_prod_dataset → v3_fit; already used on these PROD-H cases), with no patched adapter. Data X/y sha256 are compared across the two sides per fit.
- **Rule** as in §6 minus the low-p row: legacy fields identical on completed fits (any `ls0_improved` HPM gain is disclosed, not failed), 0 completed→stopped, runtime and RSS ratios within the bands.
- **Earliest finish without slipping H-14:** #69 merged and tagged Wed 11-18 → bundle + 2-fit smoke on Owls Wed → submit Thu 11-19 AM after HQ GO → results Thu PM → **verdict Fri 11-20 AM**. It runs in the 10⁴-overlap window on ≤ 80 billed CPUs (1 CPU, 2G tasks), with no overlap on island nodes.
- Staffing: Sonnet (bundle, comparator, smoke), Haiku (submit/poll/collect), manager look, and one Sonnet re-check.

## Summary (10 lines)
1. **Subset (Tier A):** the PROD-H p ≫ n study (n = 200, p ∈ {500, 1000}, S1–S6, c ∈ {1, 0.5}) at the SAME fixed grid as the 2026-11-02 reproduction spot-check: r ∈ {1, 25, 50, 75, 100} → **120 fits (5.0%)**. Tier B adds the **6 known `resource_limit` fits**. Tier C (optional) is a 120-fit low-p arm.
2. **Fit count:** 126 on NOTS (Tier A + B; 66 tasks). Tier C adds 120 fits (0.25 core-h).
3. **Core-h:** about 80 elapsed core-h, 161 billed CPU-h (Tier A 45.3, B 35.1). Planning cap: 120 core-h elapsed.
4. **Wall:** two job arrays, 35 + 31 tasks (≤ 150), throttle %20 + %20 = 80 billed CPUs (5% of the 1,536 ceiling). Run time ≈ 7–8 h, set by the 24,000 s stopped fits. p500 array ≈ 2 h.
5. **Earliest finish:** submit Wed 11-18 evening → results Thu 11-19 early AM. Realistic: submit Thu 11-19 AM → results that evening → verdict Fri 11-20 AM. That is inside the 10⁴ overlap (11-19..22), and it uses no big-node CPUs.
6. **Run on NOTS (SPR).** Owls (≤ 16 cores) is feasible for Tier C and as a fallback only, because the A/B showed admission-time `resource_limit` on loaded Owls and cross-machine bit-identity is unproven.
7. **Comparison:** one table per regime (24 cells, p × c × S1–S6, rolled up to 4 p × c rows). Rule: legacy fields bit-identical to v2.2.1 (`log_Z`, `log_Z_r`, `hpm`, `hpm_F`, RB PIPs, status) + 0 completed→stopped + runtime ratio inside the tolerance (§6).
8. **Staffing:** Sonnet builds the bundle and the comparator; Haiku submits, polls and collects; a manager look plus one Sonnet re-check. No Opus, Codex or Fable needed.
9. **MAIN RISK:** the v2.2.1 per-fit outputs are NOT on Owls (desktop/OneDrive only), so the paired comparison needs a 126-file pull. Fallback: re-run v2.2.1 (tree is in the repo) on the same nodes, +80 core-h.
10. **Second risk:** v3.1 has no plain-PIP/registry/instrumentation fields, and the v2.2.1 study adapter reads `instrumentation`; it needs a 1-fit smoke test on the v3.1 core before the array.

## 1. The study's design (what the 2,400 are)
"The 2,400" is ambiguous in the repo: **two** v2.2.1 studies have 2,400 primary fits. I read it as PROD-H (the p ≫ n headline, `Results/2026-10-28_New_Campaign/H2_20261102/HEADLINE_H.md:1-3`) and add the low-p study as a cheap Tier C. HQ should confirm.

| item | p ≫ n study (PROD-H, Tier A/B) | low-p study (PROD-L, Tier C) |
|---|---|---|
| grid | p ∈ {500, 1000} × S1–S6 × r = 1..100 × c ∈ {1, 0.5} = 2,400 (`Docs/Records/SMC_BVS_v3_deploy/AUDIT_SUMMARY.md:31`; `BRIEF_CLAUDE.md:5`) | p ∈ {20, 30} × S1–S6 × r = 1..100 × c ∈ {1, 0.5} = 2,400, plus 12,000 repeat fits (`Results/.../L_20261102/HEADLINE_L.md:3`) |
| n | 200 | 200 |
| sparsity / signal | 14 active variables (`HEADLINE_H.md:3`). Nominal SNR c²β′Σβ = 24.6 (c = 1), 6.2 (c = 0.5); S5 17.4 / 4.4 (`Docs/Records/STATUS_BRIEFING_20261028/BRIEFING.md:60`) | same families; the truth size at p = 20/30 is in `Scripts/Campaigns/2026-10-28_New_Campaign/code/lowp/RUN_DESIGN.md` (not read) |
| correlation (all S) | S1 independent; S2 AR(1) 0.5^\|j−k\|; S3 0.7 in blocks of 5; S4 0.85 in blocks; S5 0.7 in blocks + 0.3 between blocks; S6 block ρ cycling 0.4–0.9 (`BRIEFING.md:52-57`) | same |
| seeds | data seed = 1,410,000 (p500) / 1,510,000 (p1000) + 10,000·s + r; method seed = data seed + 4,000,000 (`Scripts/Data_generators/gen_prod_data.R:6-8`; table `Scripts/SMC_BVS/nots_runner/tables_production/units.tsv`, 2,400 rows) | LOWP's scheme (not read) |
| replicate structure | 1 dataset = 1 X + 1 noise draw; c100 and c050 share X and noise (`gen_prod_data.R` `generate_prod_dataset`). One fit per (dataset, c). No repeat seeds. | primary fits + 5 extra seeds on r = 1..20 |
| code | v2.2.1 (`Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/`, manifest sha256 d880afdb…13e1, `conformance/SUMMARY.md`) | v2.2.1 |

The 10-23 production (v2.1) and the 11-02 rerun (v2.2.1) agree exactly on all 2,400 records (`H2_20261102/repro/repro_summary.csv`; `ops/PRODH_COMPLETION_20261102.md:55`). So **the study is deterministic given the seed** on NOTS.

## 2. Where the v2.2.1 results are (reachable from Owls?)
- **Repo (Owls, git):** only aggregates: `Results/2026-10-28_New_Campaign/H2_20261102/tables/{headline_h2_long.csv (480 rows, cell × S counts), ev_cost.csv (runtime median/p90, fresh scores per p × c), ev_*.csv}`, `repro/repro_summary.csv`, and the low-p tables `L_20261102/tables/{Q1_logZ,Q2_hpm,Q3_pip,Q4_recovery,stability,repeat_fit_accuracy}.csv`. No per-seed value.
- **Per-fit outputs (`SMCBVS.{rds,csv,sha256,done}`, whole native `fit` in `record$fit`; format `Scripts/SMC_BVS/study/SCHEMA.md`):** the desktop's OneDrive `NOTS Data/New_Campaign/results/20261030T0934Z_prodH` (manifests p0500 7893396c…, p1000 a0196198…) and `Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/claude/prod_p{0500,1000}_20261023T1227Z` (10-23); the low-p and per-fit CSVs (`smc_h2_per_fit.csv`, `case_theory*.csv`) too (`Docs/Records/DATA_INDEX.md`). `/home/fb31/BVS_GH/_data` is absent on Owls; `SMC_Engineering_Department/records/` holds no study fit (checked: F1M_pilot, fitbin_1117, G0, W3-SCALE only).
- **NOT reachable from Owls: the per-seed v2.2.1 `log_Z`, `hpm`, `pip_primary`, `status`, `runtime_s`, `peak_memory`.** Missing exactly: the 126 `SMCBVS.rds` (≈ 1.7 MB each, ≈ 4 GB / 2,394 files per `PRODH_COMPLETION:53`, so ≈ 0.2 GB) plus `.sha256`. Route: HQ's desktop→Owls offload (`Docs/Experiments/P1M/offload/`), one batch of 126 files, sha256 vs the manifests. This is a request to HQ, not mine to do.
- **Inputs:** regenerable deterministically from `Scripts/Data_generators/gen_prod_data.R` (used by the Owls A/B for the 24 PROD-H cases, `Scripts/SMC_BVS/tests/list_pip_ab/ws_common.R:67-90`). The frozen input manifest (x/y sha256) is NOT on Owls (A/B `manifest_match` = NA), so data identity across machines is unverified. The original `inputs/*.rds` may still sit under `/projects/ml75/fb31/BVS/bench20261019` on NOTS (referenced by `nots_runner/runner/submit.sh`; INFERRED, unchecked).

## 3. Cost of v2.2.1 (NOTS) and the estimate for v3.1
- **Machine:** `commons`, `sapphirerapids` constraint, QoS `nots_commons`, **1 CPU per fit, `--mem=2G`** (MaxRSS 297 MB p500, 466 MB p1000), billed 2× (hyperthread). One task = one dataset = c100 then c050. Limits L500 = 6,300 s, L1000 = 24,000 s (`conformance/jobs/PROD_H/JOB.md:12-19`; `ops/PRODH_COMPLETION:32`).
- **Total:** **906.49 elapsed core-h (1,812.98 billed)**: p500 225.82, p1000 680.67 (`PRODH_COMPLETION:32`). Mean per fit: p500 = 225.82·3600/1200 = **678 s**; p1000 = 680.67·3600/1200 = **2,042 s**. (The 10-23 run was extrapolated at ≈ 1,120 core-h, `HQ_CAMPAIGNS_20261023-28.md:50`.)
- **By regime** (`H2_20261102/tables/ev_cost.csv`): median / p90 runtime s: p500 c100 565 / 964; p500 c050 607 / 826; p1000 c100 1,550 / 3,839; p1000 c050 1,616 / 2,369. Median fresh scores 1.4·10⁸ (p500 c100) to 3.3·10⁸ (p1000 c050). S4–S6 and escalated fits are the slow ones (Owls r001 A/B: S4 p1000 c100 4,128 s vs S1 1,781 s).
- **Stops:** 6 fits ran to the limit: p1000_S5_r030_c100 (24,001 s), r044_c100 (24,000), r044_c050 (24,016), r064_c100 (24,011), r064_c050 (24,015); p0500_S5_r088_c100 (6,307) (`PRODH_COMPLETION:17-24`).
- **v3.1 vs v2.2.1 per-fit cost (INFERRED, no direct v3.1-vs-v2.2.1 timing exists):**
  - v3.1 = v3 core + LS0 (default on), e4 tie-aware start-mode DP, GUARD-W NA fields, `grid_fallback` (only fires on a calibration failure), an LS0 charge in the preflight, list fields added last (`Scripts/SMC_BVS/core/README.md:37-68` on `origin/core/v3.1-listpip`).
  - LS0 costs ≤ 1 + (ℓ+1)·max_k[p + k(p−k)] scores (`Theory_work/INFRA/registry/claims.tsv`, W1-PXN (K)). Measured at p = 500 (S1/S4/S5): 59,290 / 51,297 / 37,994 scores (`Theory_work/Wave1C/C-ENG/REPORT.md:c2`) against ≈ 1.4·10⁸ fresh scores per fit. That is **≈ 0.04%**; at p = 1000 the bound ≈ 1.7·10⁵ against 2.9–3.3·10⁸, **< 0.1%**. List fields run after `finish()` (core README:68), so they add no scoring work.
  - The v2.2.1 instrumentation/registry (extra bookkeeping) is NOT in v3.1, so v3.1 is, if anything, cheaper. **Estimate: v3.1 = v2.2.1 × 1.00 (range 0.95–1.05), memory the same (≤ 0.5 GB; request 2G as before).**
  - Owls A/B timings (core before/after the list-PIP change, both with LS0; `SMC_Engineering_Department/tmp/20261117-listpip/ab/log_{old,new}.txt`, a read-only citation) are 1.2–1.5× slower than NOTS medians on a loaded host (load ≈ 21/80): p500 S1 c100 691 s; p1000 S1 c100 1,781 s. They are not a v3.1-vs-v2.2.1 comparison.

## 4. Proposed subset
**Tier A (120 fits, the comparison set):** p ∈ {500, 1000} × S1–S6 × r ∈ {1, 25, 50, 75, 100} × c ∈ {1, 0.5}, the SAME seeds (data seed = base + 10,000·s + r, method seed + 4,000,000). Why this grid:
- It is the fixed grid already used and accepted for the 11-02 v2.2.1 reproduction check (`PRODH_COMPLETION:53`, script `ops/scaffold/prodh_repro_check.R`), hard-coded before any result, so no cherry-picking. Reuse it.
- Every design family and regime is covered: all 6 correlation structures × both p × both signal sizes = 24 cells, 5 fits each. 5.0% sits inside the 5–10% target.
- Per-fit comparison is paired and (expected) bit-identical, so rate precision is not the point; coverage of regimes and the slow/escalated tails (S4–S6, p1000) is.

**Tier B (+6 fits):** the six known stopped fits (above). The stop count (6/2,400) is a study metric that a 5% sample cannot estimate (expected 0.3 stops), and LS0 plus the new `ls0` guard checkpoint can change a wall-clock stop (§7). They cost 35.1 core-h, almost all the 5 × 24,000 s p1000 fits. HQ may drop the 5 p1000 stops (saves 33.4 core-h; wall falls to ≈ 3 h) and keep p0500_S5_r088_c100 (1.75 core-h).

**Tier C (optional, 120 fits, Owls):** low-p, p ∈ {20, 30} × S1–S6 × c × r ∈ {1, 25, 50, 75, 100}. SMC ≈ 7.5 s/fit (`ops/PROD_L_SIZING_20261030.md`, §2) → **0.25 core-h**. It is the only place with an exact reference (full enumeration: p = 30 ≈ 27 s × 16 threads/dataset → ≈ 3.7 core-h for the 30 p = 30 datasets, ≈ 0.1 for p = 20). It checks Ẑ/PIP/HPM against the exact posterior (study's headline: log Ẑ RMSE 0.012, HPM = exact in 100%).

**Arithmetic (elapsed core-h; billed = ×2):**
| piece | fits | mean s/fit | core-h |
|---|---|---|---|
| A p500 | 60 | 678 | 60·678/3600 = 11.3 |
| A p1000 | 60 | 2,042 | 60·2,042/3600 = 34.0 |
| B p500 stop | 1 | 6,307 | 1.75 |
| B p1000 stops | 5 | 24,009 | 120,043/3600 = 33.4 |
| **total** | **126** | | **80.4 elapsed = 160.8 billed** |
The grid is a 5-rep sample of a heavy-tailed cost (p90/median 1.4–2.4), so Tier A could be 35–60 core-h; v3.1 ×1.00 ±0.05. **Planning cap 120 core-h elapsed (240 billed).** Compare: PROD-H 906 core-h; the NOTS ceiling ≈ 36.9k billed CPU-h/day (`NOTS_FACTS.md`, ceiling-throughput line).

## 5. How it is run
- **Entry:** the original study ran `Scripts/SMC_BVS/study/run_case.R --case pPPPP_Ss_rRRR --scale c100|c050 --mem-gb 2 --hours 1.75|6.667` (one fit per call, calls `v3_fit(X, y, method_seed, allocation)`), submitted by `conformance/jobs/PROD_H/runner/{submit.sh,task.sh}` (precompile job → p1000 array → p500 array; `JOB.md:15-19, 155-166`). Chunk/unit tables: `tables/{chunks.tsv,units.tsv}` (columns task, dataset, p, scales; one row per dataset; `scales` may list a single scale).
- **Plan:** reuse that bundle (v2.2.1 study layer, `code/core/v2_2_1/study/`) with its `core/` swapped for `Scripts/SMC_BVS/core/` at the tag `method-v3.1-listpip` (after #69 lands), and new chunk tables.
  - **Tasks:** p1000 array = 30 grid datasets (c100 then c050) + 5 single-scale stop tasks = **35 tasks**; p500 array = 30 + 1 = **31 tasks**. Both ≤ 150. Stop tasks first in the table, one scale per task, so no task is longer than ≈ 6.7 h.
  - **Resources:** unchanged (1 CPU, 2G, SPR, `--no-requeue`), same allocations L500 = 6,300 s, L1000 = 24,000 s so that stops are like-for-like. Task wall: p500 3:52:00; p1000 13:42:00 (the old values).
  - **Throttle:** %20 + %20 = 80 billed CPUs. One precompile job first (core build on a compute node). One submission, polling ≤ 1 `squeue`/`sacct` per 5 min over the single multiplexed ssh (`NOTS_FACTS.md`, usage discipline; arrays ≤ 150; Owls ≤ 16 cores). Outputs on `/scratch` only; pull within 7 days (14-day purge).
  - **Fallback harness:** `Scripts/SMC_BVS/tests/list_pip_ab/ab_run.R` shows the no-adapter route (`generate_prod_dataset` → `v3_fit`, save the fit), and is what the A/B used for these same PROD-H cases.
- **Comparator (new, small R script):** reads old `SMCBVS.rds` (`record$fit`) and new, per fit: `identical()` on `log_Z`, `log_Z_r`, `hpm`, `hpm_F`, `pip_primary`, `pip_r`, native status; plus runtime/RSS from the record and sacct. It should mirror `ops/scaffold/prodh_repro_check.R` (the 126-case, 882-comparison precedent). Output: one CSV per fit, one table per regime.
- **Does not run alongside the 10⁴ overlap competitively:** 80 billed CPUs and 2 GB per task; the overlap uses multi-thread island tasks (64 CPUs + 32 GB by default, `NOTS_FACTS.md`), so there is no memory conflict.

## 6. The comparison (one table) and the no-regression rule
One row per regime = p × c (4 rows; S1–S6 detail in the CSV, 24 cells × 5 fits). For each metric: v2.2.1 value | v3.1 value | delta.

| metric (the study's own) | v2.2.1 / v3.1 / Δ | pass criterion |
|---|---|---|
| exact recovery by HPM (count of 30; study's primary metric) | n / n / Δ | Δ = 0 in every cell; any change must come with `ls0_improved` TRUE |
| exact recovery by MPM (RB PIP > 0.5) | n / n / Δ | Δ = 0 |
| log Ẑ: max \|Δ\| over fits | – / – / max\|Δ\| | = 0 (identity); fallback ≤ 2·sd(`log_Z_r`) of the same v2.2.1 fit |
| F(HPM) (`hpm_F`) | – / – / Δ | new ≥ old (LS0 only adds scored models) |
| RB PIPs: max \|Δ\| (`pip_primary`) | – / – / max\|Δ\| | = 0; fallback ≤ 0.05 and MPM set identical |
| status counts ok / resource_limit / other | n / n / Δ | 0 fits completed→stopped; each stopped fit stops again OR completes with finite estimates |
| escalated count (`diag`) | n / n / Δ | Δ = 0 (escalation is calibration-only) |
| runtime: cell median s, p90 s | m / m / ratio | cell median ratio ≤ 1.25; pooled per p (n = 60) ≤ 1.10 |
| peak RSS (max) | MB / MB / ratio | ≤ 1.2 |
| low-p (Tier C): log Ẑ error RMSE vs exact; HPM = exact; max\|PIP−exact\| | 0.012 / – / – ; 100%; 0.0005 | ≤ 0.015; 100% (identical HPM set); ≤ 0.002 |
Not compared: plain PIP (the v2.2 registry/plain-PIP fields are not in v3.1), `instrumentation`, `pip_list*` (new, no baseline; the list-PIP gate covers them), SHA/hash fields that include the code identity.

**Tolerance justification.** The study's own Monte Carlo spread is the within-fit island spread (`log_Z_r`, 4 islands) and, at low p, seed-to-seed sd(log Ẑ) = 0.005–0.027 (max over cells) and max PIP sd 1·10⁻⁴–3·10⁻³ (`L_20261102/tables/stability.csv`). The fallback tolerances sit at that scale. They matter only if bit-identity fails (e.g. a different machine); on NOTS the prior reruns gave max |diff| = 0 (882/882). The runtime band follows the cell p90/median of 1.4–2.4 (`ev_cost.csv`): a median of 10 fits moves ±15–25% by chance. Since LS0 adds < 0.1% of scores, a larger shift is not explained by the method. These are proposals for HQ to accept.

**Overall verdict:** NO REGRESSION = all pass criteria met on Tier A + B. Otherwise list the failing fits with their diagnosis. Disclose, do not fail, any `ls0_improved` HPM gain (O-LS0 saw 0/2,394 changes; C-ENG 0/48 at p = 30 and 0/3 at p = 500, `C-ENG/REPORT.md:161-165`).

**Determinism / bit-identity expectation (INFERRED, to be tested).** The v2.2.1 core = v2.2 core = v2.1 numerics, and v2.2 is "bit-identical to the old fields whenever the same operations run" (`conformance/SUMMARY.md` open item 6). C-ENG showed LS0-off == old on every field except timings (48/48) and LS0-on == old on stages, Ẑ, PIPs, MPM, streams (48/48), because LS0 reads no uniforms and runs after the final search (core README:42-44). So, for completed fits on NOTS, I expect `log_Z`, `log_Z_r`, `hpm`, `hpm_F`, RB PIPs, MPM **bit-identical** to v2.2.1 (`pip_r` too). Exceptions to flag: (a) `ls0_improved` HPM change; (b) the top store / near-ties (LS0 adds models; not compared); (c) wall-clock stops (the guard is wall-time, not certified identical, and LS0 adds a checkpoint). **A difference in a legacy field on a completed fit is a finding, not noise** (candidate causes: e4 start-mode change, `grid_fallback`, tool-chain or libm difference, a data mismatch). Check data identity first (x/y sha256).

## 7. Timeline (H-14, `DECISIONS.md:104`; H-15 `:105`)
- H-14: freeze 11-18/19 → 10⁴ T-vs-V overlap 11-19..22 → precision study + 10⁴ science → 10⁵ rung 11-27..30 → 1M replicates from ≈ 12-01.
- Prerequisites: #69 merged + tag (Wed 11-18; its cite-CI is red as of the last log entry); the bundle; the 1-fit adapter smoke; the 126-file pull; HQ's go for the batch (`NOTS_FACTS.md`: submission needs HQ's go).
- **Earliest:** submit Wed 11-18 evening → finish Thu 11-19 ≈ 06:00 (p500 array ≈ 2 h, p1000 ≈ 7–8 h). **Realistic:** submit Thu 11-19 AM → finish Thu 11-19 ≈ 20:00 → verdict Fri 11-20 AM. Add queue wait (unknown on `commons`).
- Slip: none. It overlaps 11-19..22 on 80 billed CPUs; the precision study and 10⁴ science start 11-22. The sign-off (verdict ≈ 11-20) lands ≈ 1 day after the 11-18/19 freeze: HQ chooses (a) freeze provisional, sign-off on pass, or (b) sign-off first.
- If the p1000 stops are dropped: wall ≈ 3 h (p1000 grid max ≈ 2 × 4,000 s, plus the long tail).
- **Owls instead?** Only the p500 half and Tier C. p500 Tier A + stop ≈ 13 core-h NOTS-equivalent ≈ 18 core-h on Owls (×1.4) → ≈ 2–3 h at 8–12 cores. The p1000 half ≈ 67 NOTS core-h ≈ 95 on Owls ≈ 6 h at 16 cores, with the 24,000 s stops on the tail: overnight, on a loaded shared host. Not recommended as the main route: (1) 3 of the first 9 A/B units hit `resource_limit` at 0.7–0.8 s (admission preflight; INFERRED from `log_new.txt` `wall=0.7-0.8s`, and the rerun list used `hours = 48`), (2) cross-machine bit-identity is not established (`#70` review: libm differences Owls vs NOTS), (3) `nice 19` plus 16 cores means ≈ 2× the wall.

## 8. Staffing (Sonnet/Haiku only)
- **Sonnet #1 (bundle + comparator):** v2.2.1 study layer on the v3.1 core, chunk tables for Tiers A/B (and C), adapter smoke on 2 p = 30 fits on Owls (7 s each), the comparator, a unit test on fabricated old/new pairs with 3 planted differences.
- **Haiku (ops, per the JOB.md runbook):** stage, `sha256` check, submit after HQ's go, poll ≤ 1/5 min, collect, checksum, pull, scratch cleanup.
- **Review:** manager diff look + one Sonnet re-check of the comparator and the verdict table. No Codex/Sol gate needed unless a regression is reported. Pace follows H-15 (cap 3 agents, `claudeAgent_personal`).

## 9. Risks and unknowns
1. **Old per-seed outputs not on Owls** (§2): 126 `SMCBVS.rds` must come from the desktop. If that fails: re-run the v2.2.1 tree (`code/core/v2_2_1/`, hash-checked; a copy may still be in NOTS `~/projects/BVS/New_Campaign/code/core/v2_2_1`, INFERRED from `DATA_INDEX.md`) on the same SPR nodes: +80 core-h, same arrays, gives paired same-machine timings. The prior reproduction supports that old and rerun agree.
2. **"Same seed" comparability:** data regenerate from `gen_prod_data.R`, but there is no frozen-manifest hash on Owls; the NOTS `inputs/*.rds` are the safest source. Rule: compare X/y sha256 first (the `manifest` route of `ws_prodh`). The core's RNG is seeded per stream (SplitMix64/xoshiro256**, core README:22), so it is seed-deterministic on a fixed tool chain.
3. **Adapter on the v3.1 core:** v2.2.1's `study/adapter.R` expects v2.2 fields (`fit$instrumentation$stop`, P5 retry, plain PIP) that v3.1 lacks (`CHANGES_v2_2_1.md`; `README` v3.1 §GUARD-W). It may need a patched study layer, which is code not covered by any freeze, or the `ab_run.R` route. A 1-fit smoke settles it before any array.
4. **Stops are wall-clock events:** LS0 adds an `ls0` guard checkpoint, and GUARD-W makes an LS0 stop produce no output (`core/README.md:46`); the preflight now charges the LS0 worst case (`ef33f91c`). At L = 24,000 s a fit that was just inside may now stop, or vice versa. Classification differences on the 6 stops are reported, not failed (§6).
5. **Admission refusal:** if the new preflight (with LS0's worst case) projects more than the allocation, a fit returns `resource_limit` in < 1 s. On NOTS SPR with the old L values I expect admission, but the first 2 tasks (p1000 S4/S5, the heaviest) should be watched before the array widens (precedent: the 200-unit stop rule, `GO_2400.md` C3).
6. **Ambiguity of "2,400":** Tier A/B is p ≫ n; the low-p study is only Tier C. If HQ meant low-p, swap the weights (low-p is ≈ 0.3 core-h for 120 fits, or ≈ 5 core-h for all 2,400, plus enumeration).
7. **Timeline coupling:** the sign-off lands after the freeze unless the start is Wed evening. Home/scratch: outputs ≈ 0.2 GB; all on `/scratch`.
8. **A/B state:** The Owls A/B (`ab_run`, 39 units, still running at my read; old core vs new core, both with LS0). It tests list-PIP additivity, not v3.1 vs v2.2.1, so it does not substitute for this rerun.

## Result (2026-11-18)
NO REGRESSION, accepted by HQ: see `results/RERUN_2400_VERDICT.md`.
