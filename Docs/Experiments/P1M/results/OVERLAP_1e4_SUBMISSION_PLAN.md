# 10⁴ T-vs-V overlap rung: submission plan (Engineering planner, Sonnet; Wed 2026-11-18; PLANNING ONLY, nothing submitted)

Basis: MANIFEST_CELLS v0.4, `p1m_cells.py` / `p1m_driver.py` on origin/exp/P1M-engine af36583f (plans generated and worst cases computed
in a scratch copy, no file in the department tree), LEDGER, T5_1e5.md, CAMPAIGN_PLAN_1117 (H-14). Labels: MEASURED / ESTIMATE / PLANNING VALUE.

## Summary for HQ
1. **40 fits** = 10 datasets (p = 10⁴, n = 200: AR-strong 4, AR-weak 2, ADJ-OPP 2, IND 1, NULL 1) × engine seeds 1, 2 × arms **T** (law mode) and **V**; 20 + 20.
2. **Cost quote:** ≈ **1.0k core-h** expected (V ≈ 0.12k, T ≈ 0.8k; ESTIMATE), range 0.5–2.5k; manifest value 2,500 = the rung's ceiling. No 10⁴ engine fit has been measured: T's coded calibration is the unknown.
3. **Run:** pilot wave W0 (2 T + 2 V; worst 449 + 93, expected ≈ 100) → read back → 3 waves of 6 T + 6 V (Fri, Fri pm, Sat). Five stages per fit via the driver; ≤ 168 queued tasks per wave (two batches, each ≤ 150); peak ≈ 700 CPUs (45% of the QOS cap).
4. **Two plan defects to fix at the freeze (blocking):** the generated T plans are N = 2,500, R′ = 16 with V-sized limits (calibrate 0:45), but the T arm is N = 10⁴, R′ = 4 with coded calibration, so they would TIMEOUT. §1, §2.
5. **HQ decides:** (a) GO after the freeze reproduction check; (b) accept W0's worst 543 as a limit, and a one-off exception to the 2-h task rule (T calibrate 3 h); (c) the pre-registered tolerances (§4), incl. replacing the log Ẑ_occ criterion (deferred by D-21).
6. **Calendar:** Thu 11-19 GO + W0; Fri W1, W2; Sat W3 + analysis; Sun 11-22 independent review + verdict to HQ.
7. **Clean (§4)** = 40/40 delivered, §0-v2.7 tolerances pass incl. predictive Hellinger, the comparison reviewed, cost ≤ 1.5× model → releases the precision study + 10⁴ science.

## 1. Cells and fits
Seeds: data seed = 4·10⁸ + D·10⁶ + 2·10⁴ + rep (D: IND 1, AR 2, AR-weak 3, ADJ-OPP 5, NULL 6); engine seed s1 = data seed, s2 = data seed + 100. T and V share (data seed, engine seed) by design.
Run ids `4-<design>-n200-r<rep>-<T|V>-s<1|2>`:
| cells | reps | fits T / V |
|---|---|---|
| AR-strong (a = 1) `4-AR-…` | r01–r04 | 8 / 8 |
| AR-weak (a = 0.6) `4-ARweak-…` | r01–r02 | 4 / 4 |
| ADJ-OPP `4-ADJOPP-…` | r01–r02 | 4 / 4 |
| IND `4-IND-…`, NULL (a = 0) `4-NULL-…` | r01 each | 2 / 2 each |
These V fits are also 10⁴-science replicates (costed once); precision study + ablations use overlap rep 1.
- **V arm:** N = 2,500, R′ = 16, bounded calibration, `island_isa = sapphirerapids`, class A.
- **T arm (needs decision/fix):** law mode, bit form, N = max(2500, n, p) = 10⁴, R′ = 4 (EXPERIMENT_PLAN A1; coded calibration with escalation, D-26). Version = registry pin v3.1 @ 4676af6 as sent to HQ 11-16, = method-v3.1.1-listpip core tree 61b0a582.
  `p1m_cells.py` emits T with N = 2,500, R′ = 16 (arm `TV2` has no N / islands keys). Fix at freeze: T arm `"N": 10000, "islands": 4`. Confirm with WP4 whether law mode takes N from the plan or sets it.
- **Plan files** (`p1m_cells.py --plans DIR --only 1e4` writes 41 for 10⁴; the overlap ones are 6, all `kind = gated`, `code_commit = UNSET` until the freeze):
  generated `overlap1e4_p10000_n200_V_N2500_R16_b1..b3` (7/7/6 fits) and `…_law_N2500_R16_b1..b3`.
  Replace by hand-edited wave plans (same generator, then `resources` overrides): `OV_W0_T`, `OV_W0_V`, `OV_W{1,2,3}_{T,V}`. Fits per wave:
  - **W0 pilot:** AR r01 s1 and ADJ-OPP r01 s1, T and V (2 designs; ADJ-OPP is the stress case for escalation).
  - **W1:** IND r01 s1, s2; NULL r01 s1, s2; AR-weak r01 s1, s2, each T and V (designs not yet costed first).
  - **W2:** AR-weak r02 s1, s2; ADJ-OPP r01 s2, r02 s1, s2; AR r01 s2. **W3:** AR r02, r03, r04 × s1, s2 (6 + 6 fits, the best known design last).

## 2. Jobs per fit (driver stages; billed CPUs = allocated threads; SPR `--constraint`, commons / nots_commons)
| stage | V arm (16 isl.) request / limit | T arm (4 isl.) request / limit | expected (ESTIMATE) |
|---|---|---|---|
| setup (gen, prep, setup) | 8 CPU 8G / 0:15 | same | < 1 core-h |
| calibrate | 16 CPU 8G / 0:30 | **48 CPU 16G / 3:00** (pilot; re-size after W0) | V ≈ 1; T 15–100 |
| islands (array R′) | 4 CPU 4G / 0:30 each | 24 CPU 16G / 0:45 each | V ≈ 3; T ≈ 4–10 |
| merge (+ LS0) | 8 CPU 4G / 0:15 | 8 CPU 8G / 0:20 | < 0.5 |
| eval + post | 8 CPU 8G / 0:20 | 8 CPU 8G / 0:30 | < 1 |
| **tasks per fit / worst case** | 20 / **46.7** core-h | 8 / **224.7** core-h | |
- V shapes are the driver's 10⁴ defaults, tightened from 82 to 46.7 worst (islands 4 CPUs: WP3 measured wall flat beyond 24 threads at 10⁴, so few threads waste least; UNVERIFIED at 4). T calibrate at 48 CPUs is sized for the manifest ceiling (115 core-h ≈ 2.4 h); 3 h needs `max_task_hours = 3.0` (default 2.0).
- Tasks are small (≤ 48 CPUs, ≤ 16 GB): memory-aware fragmentation is not binding (NOTS_FACTS: ≥ 19 SPR nodes with ≥ 64 CPUs and ≥ 32 GB free at reading). One `sinfo` check before submission.
- **Arrays and throttle:** a wave = two batches (T: 6 × 8 = 48 tasks; V: 6 × 20 = 120 tasks), each ≤ 150. Islands array per fit has ≤ 16 tasks, so `island_throttle` adds nothing; concurrency is set by the wave size. One wave at a time; T and V batches of a wave go in together (V finishes in ≈ 1 h, before T's islands). Peak ≈ V islands 384 + T calibration 288 = 672 CPUs.
- **Binaries:** build once in W0 on the login node (`nice`, -j3; one build for V with `-DV4_ISLAND_ISA=sapphirerapids`, one default for T), then copy `bin/` unchanged into later waves; record each binary's sha256 in every manifest.
- Restart chain: not used (V islands take minutes; T calibration has stage-boundary checkpoints only, D-21).
- Fits in flight: W0 4, then 12 per wave (6 T + 6 V).

## 3. Core-h, wall, calendar
| arm | fits | MEASURED anchor | per fit (ESTIMATE) | total | worst Σ limits |
|---|---|---|---|---|---|
| V | 20 | none at 10⁴ in the engine; T5 at 10⁵ = 42.18 (islands 28.1 = 67%, calibrate 10.6 = 25%; island cost ∝ p) | 4–10 (central 6; manifest 10) | ≈ 120 (80–200) | 934 |
| T | 20 | B3 10k full fit (coded, 2 CPUs, 1 thread) 20.97; G0 10k final stage 16.87 (8 isl.) | 21–115 (central 40; manifest 52–115) | **≈ 800 (420–2,300)** | 4,494 |
| **rung** | 40 | | | **≈ 0.9–1.0k** (range 0.5–2.5k; manifest 2,500) | |
- **Quote to HQ** (pre-announce in REQUESTS.md, ledger row per batch): expected ≈ 1.0k; ceiling 2.5k; W0 worst 543 (T 449 + V 93.3); later waves' `core_h_cap` = measured-based worst (limits tightened to ≈ 3× the W0 elapsed, never below the stage minimum above), each cap = batch worst rounded up (driver rule: cap ≥ worst).
- Admission check before every wave: Σ actual + Σ worst of open batches + this wave ≤ envelope remaining (≈ 28k, ledger); only the open wave is reserved.
- **Wall:** V fit ≈ 0.5–1 h. T fit ≈ calibrate 1–3 h + islands ≈ 0.3 h + merge/eval 0.2 h ≈ 2–4 h (ESTIMATE; unmeasured). A wave ≈ 4–5 h if the queue is clear.
- **Calendar:** Wed 11-18 plans, pre-reg draft, review. Thu 11-19: freeze check + GO, build, W0 (read back by evening). Fri 11-20: W1 08:00; W2 ≈ 14:00 after W1's costs are read. Sat 11-21: W3 08:00, offload, comparison script on W0–W2 data. Sun 11-22: comparison on 40/40, independent review, verdict. Slack ≈ ½ day (one wave).

## 4. Gates
**Before submission (all required, logged in LOG.md):**
1. Campaign freeze: `code_commit` = the engine freeze commit F; CAMPAIGN_FREEZE.md; reproduction check passed (Owls: T3 hashes + goldens equal 2cfaa9e5's, driver tests; NOTS ≈ 2 core-h: one 10⁵ island hash; bit-form island hash `c4efa909db3fa656` across ISAs, D-32). Plans regenerated at F with `code_commit = F`; `plan.resolved.json` has no warnings; `--strict` passes.
2. T-arm definition fixed (N = 10⁴, R′ = 4; calibration tier rule) and the T limits above; dry run on Owls to a department scripts dir; SHA256SUMS verified after rsync to NOTS (the driver's `submit.sh` verifies them).
3. **Pre-registration** (`results/OVERLAP_1e4_PREREG.md`, sha256 recorded before W0): tolerances, metrics, seeds, designs, the analysis script and evaluator hash. A later change is a logged deviation.
4. HQ GO, with the quote and the W0 worst accepted as a limit. Scratch / home guards read (home < 8,192 MB).
**During (checked at each wave readback; any one → stop submitting, tell HQ, do not resubmit bigger):**
- cost: any T fit > 172 (1.5 × 115) or V fit > 15; cumulative actual > 1.6k, or the projection (measured per-fit cost × fits left) > 2.5k; wave actual > 2× its quote;
- failures: any failed or TIMEOUT stage that is not an infrastructure fault (NODE_FAIL, SIGKILL by Slurm); more than 2 failed fits in a wave; one rerun per fit at most (infra only; a `resource_limit` rerun may re-size memory, same bits, logged);
- admission: any engine `resource_limit` / admission-refusal record, or Slurm QOS / MaxSubmit pending reasons;
- dataset pairing: X, y sha256 must be equal across the 4 fits of a dataset (setup regenerates them per fit).
**After: "clean" (pre-registered, ENGINEERING_SPEC §0-v2.7; yardstick = T's own seed-to-seed spread, pooled over the 10 datasets because 2 seeds give an unstable per-dataset s.e.):**
- delivered: 40/40 complete (G-B needs ≥ 95%; every failure is stated, never dropped);
- HPM(V) = HPM(T) as sets in ≥ 9 of 10 datasets; T never reports a model with higher F than V's; MPM equal;
- max_j |PIP_V − PIP_T| ≤ max(0.01, 3 combined s.e.) for `pip_primary`; also PIP_T and the list-PIP reported;
- |log Ẑ_V − log Ẑ_T| ≤ 3 combined s.e.; the log Ẑ_occ criterion (≤ 0.05) is not available if occupancy diagnostics are deferred (D-21): pre-register log Z_T (deterministic lower bound) instead;
- **predictive:** the Hellinger distance between the store-BMA predictives of V and T (4,000 x draws × 64-node Gauss-Hermite) ≤ 10% of T's distance to f*; also per arm: plug-in h² (HPM, MPM, closed form), posterior law of d_H (quantiles, tail curve), predictive h², KL / log score, test MSE and mean log predictive density on 10⁴ fresh rows, each as a ratio to the oracle, with dataset-clustered intervals (MANIFEST §4); NULL: no model beyond ∅ with PIP > 0.5;
- cost ≤ 1.5× model; an independent review (code + tables) of the comparison reports ACCEPT.
Outcomes: **clean** → precision study (64 islands) + 10⁴ science released. **Marginal** (misses only in evidence or PIP tolerance, HPM ≥ 9/10): the precision study (N 2,500 vs 10⁴, m) is the diagnosis, run first; 10⁵ stays blocked until it explains the miss. **Not clean** (≥ 2 HPM misses, T finds higher F than V, or predictive > 10% on ≥ 2 datasets): stop, HQ + Theory (V is not a faithful variant).

## 5. Monitoring and collection
- **Monitoring:** one Haiku monitor (H-12) over the one multiplexed ssh; one combined `squeue` + `sacct -X` call per check, **≤ 1 per 5 min and normally every 20–30 min** (every 10 min near expected end); it tracks **every** array task, not one job id (the 11-15 lesson). A scheduled readback after each wave (the polling stops when the wave ends). No `watch` loops. Output: wave state, billed core-h so far, stop-rule flags, to the manager.
- **Collection:** every job's epilogue writes `SHA256SUMS` + `OFFLOAD_READY` in `scratch/runs/<batch>/<run_id>/`. The offload crew rsyncs to Owls `SMC_Engineering_Department/records/<batch>/<run_id>/` (`nice`, one stream), verifies `sha256sum -c`, then the desktop pulls. Units of record: `fit.bin`, `law.bin`, eval + post records, `cost/`, manifests, `fit.json`, logs, sacct dump (`p1m_cost.py`); island and setup files are not kept (rebuilt from manifests). Volume ESTIMATE ≤ 10 GB (T5 `fit.bin` 232 MB at 10⁵).
- **Cleanup on NOTS:** run dirs are freed only after Owls + desktop are verified (tombstone `OFFLOADED`); target ≤ 24 h after the wave, hard 7 days (14-day purge on atime, NOTS_FACTS); frozen code and unfinished runs are never freed; `scratch/tmp` is the driver's trap. Ledger rows closed from sacct (CPUTimeRAW / 3600).

## 6. Staffing (H-12, H-15: Sonnet/Haiku default, cap 3 agents)
- **Sonnet A (plans + submission):** wave plans, dry runs, deploy, `submit.sh` only after HQ's GO and the manager's per-batch OK (manager-owned), ledger + pre-announcements.
- **Haiku (monitor + offload + ledger):** polling, sacct, stop-rule flags, offload verification, NOTS cleanup, machines line.
- **Sonnet B (analysis):** comparison script, tables, the pre-reg file; runs on W0 data to debug, frozen before W1 is read as a verdict.
- **Reviewer:** one independent review of the comparison (code + tables): Opus by default (H-13 keeps Codex for P-gate PRs and bit-identity diffs); the manager decides. Opus is also called if a T3 / golden hash differs (H-12).

## 7. Risks and unknowns
1. **T cost and wall are unmeasured** (calibration with escalation; 21 → 115 core-h). W0 prices it; a T fit above 172 stops the rung and goes to HQ with ranked cuts (T on fewer datasets: IND / NULL only 1 seed; the manifest trim "T at the measured lower end" is the other direction).
2. **T arm identity:** the generated plans' N / R′ mismatch (§1); whether law mode at 10⁴ is bit-compatible with revision D / the pin (the 5k anchor covers p ≤ 5k only). Optional: one R-core fit (`method-v3.1.1-listpip`) on AR r01 ≈ 21–40 core-h (B3 basis) ties T(engine) to the pin; not in the 2.5k, HQ decides.
3. **2 seeds per dataset** give a weak per-dataset s.e.: hence the pooled yardstick (pre-register it; a Theory check is cheap).
4. **V thread scaling at 4 CPUs** is unmeasured (WP3: flat beyond 24 threads); W0 checks the wall, the cost impact is small (< 0.2k).
5. **Queue / account:** commons is busy (≈ 900 pending, 11-15); wave starts may slip hours. Home 6.8 / 10 GB (guard 8.2): logs go to scratch only. The account was flagged once: calm submissions, one connection.
6. **Freeze slip:** if F lands after Thu noon, W0 moves to Fri and the calendar loses the ½-day slack; W3 → Sat evening still fits, the verdict Sun.
7. **Merge/eval memory** at 10⁴ is small (≤ 16 GB planned); an unexplained `resource_limit` stops the wave (§4). `eval` predictive objects (n_x 4,000, 64-node GH) are tested only at 10⁵ (T5): W0 is their first 10⁴ run.
