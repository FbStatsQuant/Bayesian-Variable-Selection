# MINILEG_PLAN: the V-N mini-leg (N = 10⁴ final islands on F2): plan, cost quote, stops, waves, ops (Engineering, Sonnet plan writer; Thu 2026-11-19)

**Status: COMMITTED by the Engineering manager 2026-11-19 before any mini-leg run (HQ H-28 quote approved; H-33 order; manager OK on the seed pairing with the N = 2,500 twins and on precision_freeze_vn.py after a diff check + golden test)** (one Opus plan review recommended first: it adds two scripts that are not the registered files, §3.2). Nothing is deployed, submitted or run; no NOTS access; scratch only under `~/SMC_Engineering_Department/tmp/20261119-vnplan/` (worktree `wt_F2` at e993ece2, `mw/` plans). Companion: `MINILEG_PREREG.md` (the N rule, the 1M consequence, the offset N contrast, scripts + sha256). Basis: HQ H-26 Q1, H-28, H-31, H-33 (HQ_DECISIONS ea106d2b); `results/precision1e4/{VN_MINILEG_NOTE, LEG_READBACK, CAMPAIGN_FREEZE_ADDENDUM, PREREG}.md`; `results/vn_minileg/F2_IDENTITY_CHECK.md`.

**Manager decision on the recommended review (2026-11-19):** no separate Opus review. `precision_freeze_vn.py` was diff-checked by the manager against the registered `precision_freeze.py` (exactly three changes: `--baseline`, `--knob`, skip cost files without `stages`; no threshold, metric, ratio or identity/HPM rule changed) and `tests/test_vn_golden.py` reproduces the registered output on the leg's real FZ records; `vn_offset_contrast.py` is measurement-only (no pass/fail). Owner/HQ token policy: one Opus child only where needed.

## Summary (≤ 10 lines)
1. **What runs (15 fits, 8 batches, 3 waves, F2 only):** 6 N = 10⁴ fits at the **FROZEN configuration** (m 1, I_max 0) = the decision arm; 6 N = 10⁴ fits at I_max 3 (the held arms that the registered script scores verbatim; also the fallback configuration of HQ H-30); XB2 (an N = 2,500 R′ = 64 identity re-run of a leg fit on F2); the **r04 check** (I_max 3 twin of `4-ADJOPP-n200-r04-V-s1` + a seed-2 I_max 0 fit; report-only). **The held arms were m ∈ {1, 4} × 2 replicates × 3 datasets at I_max 3** (LEG_PLAN H1–H3): the 6 m = 1 arms are kept as they were; the 6 m = 4 arms are **not run** (m is frozen at 1, KEEP) and are replaced by the 6 frozen-configuration arms. **Paired seeds:** each N = 10⁴ fit takes its N = 2,500 twin's seed, so the calibration grid is bit-identical and the contrast isolates the islands' N (§2).
2. **Quote (MEASURED twins): E = 248 core-h (P90 280, P99 312) against the approved ≈ 440 + r04 ≈ 4 (cap 600): self-release YES.** Waves V0 / V1 / V2 quoted 50 / 75 / 125 (stops 100 / 150 / 250); cumulative stop 400; projection ceiling 600; per-fit class table committed (soft 1.5× / hard 2.5×, hard pinned).
3. **(a) N rule:** the registered rule, per configuration: I_max 3 by `precision_freeze.py` (sha 7cdd69a1…) **unedited**; the frozen configuration by `precision_freeze_vn.py` (a parameterised copy: baseline and knob as arguments; **identical on the leg's real FZ records**, proven by test); no new threshold. (b) **1M consequence:** all-N = 10⁴ at 1M does **not** fit (35.7k with 25 % reserve, 29.0k without, vs 28.3k); the pre-declared ladder, with numbers, is in PREREG §6 (default S2: 17.3k). (c) The N contrast of the offset measurement is pre-declared as the one measurement, no pass/fail.
4. **Open for the manager/HQ:** the paired-seed design and the dropped m = 4 arms (§2), the two non-registered scripts (§3.2), and the ledger total (**spent 2,450.40**: the "2,041 + 462 + 1.99" in the brief counts the 55.09 of A0 + P1 twice).

## 0. Facts used (all read from the files named)
| item | value | source |
|---|---|---|
| F2 | tag `p1m-freeze-F2` = e993ece226b355058e26400f05f9faad6daf16ca (F + #85–#88); V binary **sha256 da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a**, built ONCE on NOTS (`BUILD_F2`, `staging/vn_minileg/deploy_F2.log`); default-N identity **PASS** (AR r01 s1: 16/16 `logZ_r`, HPM, 16/16 island hashes, 24 sidecars, fit/eval sections) | `F2_IDENTITY_CHECK.md` |
| the N feature | V's final N is a `calibrate` parameter (manifest `params.N`, default 2,500, whole number in [1, 2²⁴]); merge/island read it from `calib.bin`; the driver refuses a top-level N ≠ `params.N` | e993ece2: `include/v4/calib_run.h:40`, `src/calib/calib_run.cpp:120-123`, `src/merge/wp4_io.cpp:329,340`, `src/island/island_cmd.cpp:224`, `tools/slurm/p1m_driver.py:405` |
| N = 10⁴ island cost | same-machine **3.85×** the N = 2,500 island (range 3.4–4.6; effectively linear in N); calibration is N-independent (H = 512; same seed → same grid, `calib.bin` sections identical, meta differs in N only) | `VN_MINILEG_NOTE.md` §1, §1.1 |
| frozen configuration | N 2,500 (provisional), m 1, I_max 0, resampling off "not tested", π₀(S₀) deferred | `CAMPAIGN_FREEZE_ADDENDUM.md` §1 |
| measured baseline fits (N 2,500, m 1, R′ 64, F build d0c30b65) | I_max 0: 5.55 / 5.34 (AR), 4.09 / 4.13 (AR-weak), 5.51 / 5.42 (ADJ-OPP); I_max 3: 5.72 / 6.14, 5.01 / 5.90, 7.24 / 6.14 core-h; islands = 80–95 % | `twin_costs.csv` (from the leg's cost files) |
| ledger | spent **2,450.40** = 975.5 (closed to 11-18 10:05) + 1,010.43 (overlap) + 462.48 (leg, 194 fits) + 1.99 (VN_ID_1); envelope 28,300; remaining 25,850. **The LEDGER's "≈ 2,041" already contains A0 + P1 = 55.09 of the 462.48** | `LEDGER.md`, `LEG_READBACK.md` §6 |

## 1. Scope, and how the held arms map (task: "state whether the held arms were m ∈ {1,4} and how they map now")
**Held arms (LEG_PLAN §2.1 / §4, H1–H3):** N = 10⁴ × m ∈ {1, 4} × 2 replicates × 3 datasets (AR-strong, AR-weak, ADJ-OPP; overlap rep 1) = 12 fits, **I_max 3**, R′ = 64, independent seeds k = 14–17.
| arm (new run ids) | fits | N | m | I_max | seed | role |
|---|---|---|---|---|---|---|
| `4-<ds>-n200-r01-P-N10000-m1-I0-c{1,2}-s1` | 6 | 10⁴ | 1 | **0** | the N 2,500 I_max-0 twin's (k = 18, 19) | **decision arm at the frozen configuration** (replaces the 6 m = 4 held arms) |
| `4-<ds>-n200-r01-P-N10000-m1-c{1,2}-s1` | 6 | 10⁴ | 1 | **3** | the N 2,500 I_max-3 twin's (k = 10, 11) | the held m = 1 arms, kept: scored **verbatim** by the registered script; the fallback configuration if the G-B I_max rule reverts 10⁵/1M to I_max 3 (H-30) |
| `4-AR-n200-r01-P-N2500-m1-I0-XB2-s1` | 1 | 2,500 | 1 | 0 | the leg's AR c1 I_max-0 seed (k = 18) | **XB2**: F2 vs F bit check at R′ = 64 (§6.3) |
| `4-ADJOPP-n200-r04-VI3-s1`, `4-ADJOPP-n200-r04-V-s2` | 2 | 2,500 | 1 | 3 / 0 | data seed (s1), data seed + 100 (s2) | **r04 check** (H-33 (1)), R′ 16, report-only |
| *m = 4 held arms* | *6* | 10⁴ | 4 | 3 | – | **NOT RUN**: m is frozen at 1 (KEEP at N 2,500; r(M1) 1.007, r(M2) 1.037 against the bar 0.656). Priced in VN_MINILEG_NOTE at ≈ 310 core-h; saved |
15 fits; seeds and run ids in `waves_vn.json` (`make_waves_vn.py`). The r04 pair is the check HQ asked for: the original fit (I_max 0, F build, σ̂ 1.088, one final-merge E2, log Ẑ 0.123 below log Z_T) has no I_max-3 twin and no second seed.

## 2. Design choices that need confirmation (flagged, not silent)
- **D1. Paired seeds (a change from the manifest's "every arm its own seed").** An N = 10⁴ fit uses the engine seed of its N = 2,500 twin from the precision leg. Calibration depends on H = 512, not on N (D-26), so at the same seed `calib.bin` and the frozen grid are bit-identical (VN_MINILEG_NOTE §1.1); the contrast then isolates the islands' N and removes the grid-to-grid variability, which is a large part of the per-fit spread of the freeze metrics (M3 sd of log 0.27 at R′ = 16, PREREG R3). The two replicates of a cell stay independent of each other. Verified at the verdict, not assumed: **pairing identity** (the twin's `calib_meta.json` section hashes, all sections except `meta`, equal: the `grid` section sha256 equal) is a stop condition (§5.3). The rule's thresholds do not change; paired noise is smaller, so the rule is, if anything, sharper (PREREG §3.4 gives the operating characteristics for both noise levels). **If the manager prefers independent seeds** (generator seeds k = 14–17), change two lines of `make_waves_vn.py`; the operating characteristics then use the wider noise.
- **D2. The m = 4 arms are dropped** (above). If HQ wants m = 4 at N = 10⁴ anyway: +6 fits, E ≈ 310 (VN_MINILEG_NOTE), still inside the approved 440.
- **D3. Two replicates per cell**, as the registered rule evaluates (it requires exactly 2 delivered replicates per dataset and cell). More replicates would need a change of the rule; not proposed.
- **D4. Unspent approved budget:** E 248 against ≈ 444 approved. Not spent on more N = 10⁴ cells (the rule's resolution is limited by the bar, not the count: PREREG §3.4).

## 3. Feasibility on F2 (nothing here needs a code change)
- **N = 10⁴ in V:** supported by F2 as a manifest parameter; the plans carry `N: 10000` once as the top-level fit N (the driver, which copies it into `params.N`, refuses any disagreement). Plans resolved with the F2 driver `--strict`: no warnings (`make_waves_vn_output.txt`). Owls check of the feature: one N = 10⁴ island 270.5 / 274.4 s on 4 threads against 70.7 s at N = 2,500 (NOTE §1).
- **Island time limits explicit (PR #88 F7):** `resources.islands` = **0:45** for the N = 10⁴ batches (measured ≈ 4.5–5 min at T = 20 on 4 CPUs; AR and ADJ-OPP grids reach T ≈ 23–30, so 9–10 min worst; ≥ 4.5× margin; ≤ 2 h); the driver's `DEFAULT_RES` (0:15) is not used. XB2 batch islands 0:30, r04 batch the overlap V shapes. Other stages as the precision leg (calibrate 0:20, merge 16G 0:20, eval 0:15).
- **Identity of the pooled baseline.** The N = 2,500 twins ran on F (d0c30b65); the N = 10⁴ fits run on F2. F2 reproduces F bit for bit at default N (`F2_IDENTITY_CHECK`: PASS at R′ = 16); XB2 repeats it at R′ = 64 and I_max 0 on a leg fit, and the pairing identity (§5.3) compares the calibration grids. Pooling is justified only if both hold.
- **Registered scripts and N arms** (task (a)): `precision_freeze.py` keys its cells by `(N, m, I_max)` from the run id and scores the knobs `m=4`, `N=10000 (m=1)`, `N=10000 (m=4)`, `I_max=0` against the fixed baseline (2500, 1, 3): the **(10⁴, 1, 3) arms are scored verbatim; the (10⁴, 1, 0) cell has no knob and baseline (2500, 1, 0) is not selectable**, so the frozen-configuration arm cannot be scored without editing it. `precision_offset.py` builds its N contrast only for I_max 3, and **its per-fit CSV has a header without the `src` column its rows carry** (every column after `I_max` is shifted by one; `offset.json` is unaffected): a defect named here, the registered file is not edited. Handling: §3.2.
### 3.2 Two scripts that are NOT the registered files (registered by the mini-leg PREREG with sha256 before any run)
| script | what it is | proof |
|---|---|---|
| `precision_freeze_vn.py` | the registered file with three differences: `--baseline N,m,I` (default the registered 2500,1,3), `--knob NAME:N,m,I:up\|down` (default the registered four knobs), and cost files without a `stages` key skipped (the named `cost_batch.json` defect). No threshold, metric, ratio, identity, HPM or cost rule changed | `tests/test_vn_golden.py`: **on the leg's real FZ records** identity / decisions / detail / targets equal the registered script's (`m=4` KEEP, `I_max=0` ADOPT); synthetic: ADOPT / KEEP / INCOMPLETE for the frozen N arm, `cost_batch.json` skipped |
| `vn_offset_contrast.py` | the N contrast (and any cell pair) from the registered `offset_per_fit.csv`, with the registered formulas and t table, reading the CSV by position (both layouts); prints the H0 and H-N reference values | `tests/test_vn_offset_contrast.py`: its I_max-3 contrast equals the registered script's own N contrast |
Both are small; a diff against the registered file is reproduced in MINILEG_PREREG §3.2. 5 self-tests pass.

## 4. Waves (≤ 150 array tasks per batch; every task ≤ 2 h; gate-paced)
Plans: `make_waves_vn.py` (tools from F2, `--code-commit` e993ece2, pin verified by `p1m_cells.py`; sha256 in §8). `COPYBIN`: ONE build = the F2 binary `da0cf85b…` (BUILD_F2), sha-checked into every batch by the leg's `deploy_wave.sh copybin` / `presubmit_check.sh` (derived tool copies, V-O2); nothing is rebuilt. Submission pacing: one `submit.sh` per batch, batches ≥ 5 min apart. Island arrays throttled `%32` (R′ 64) / `%8` (R′ 16): peak ≤ 768 CPUs (QOS cap 1,536). "Worst" = limit sum (ledger admission, not an estimate).
| wave | batches | content | fits | tasks | **E** (P90) | **QUOTE → wave stop (> 2×)** | worst (limit sum) | release |
|---|---|---|---|---|---|---|---|---|
| **V0 (canary)** | `VN_V0_1` | AR N 10⁴ I_max 0 c1 + AR N 10⁴ I_max 3 c1 | 2 | 136 | | | 407 | after the manager's commit |
| | `VN_V0_2` | **XB2** (N 2,500, R′ 64, I_max 0, AR c1 seed) | 1 | 68 | | | 139 | |
| | `VN_V0_3` | r04 pair (R′ 16) | 2 | 40 | | | 93 | |
| | wave | | **5** | **244** | **51.0 (56.8)** | **50 → 100** | **639** | |
| **V1** | `VN_V1_1`, `_2` | AR c2 (I_max 0, 3); AR-weak N 10⁴ I_max 0 c1, c2 | 4 | 272 | **73.3 (84.6)** | **75 → 150** | 813 | self-release after the V0 checklist (§5.4) is clean |
| **V2** | `VN_V2_1`, `_2`, `_3` | AR-weak I_max 3 c1, c2; ADJ-OPP I_max 0 c1, c2; ADJ-OPP I_max 3 c1, c2 | 6 | 408 | **124.0 (142.2)** | **125 → 250** | 1,220 | self-release after V1 clean |
| **VZ** | – | the registered scripts + one Opus check + the verdict | – | – | – | – | – | gate to HQ |
**Total: 15 fits, 8 batches, 3 waves; E 248.3 (P10 219, P50 247, P90 280, P99 312); P(> 444) = 0, P(> 600) = 0** (`vn_quote_output.txt`). Gate-paced order: commit → V0 → V0 read-back (canary checklist) → V1 → V2 → registered scripts + Opus check → verdict to HQ → the G-B plan finalises with N* (H-33 (3)). Wall time is queue-bound: a wave is a few hours; the whole mini-leg is of the order of one working day plus the verdict check; no calendar dates are promised.

## 5. Cost quote and stops
### 5.1 Basis (MEASURED twins, not planning values)
Each N = 10⁴ fit is priced from its N = 2,500 twin's measured stage costs (same seed, data, grid, T): setup, calibrate, merge, eval unchanged; **islands × f, f = 3.85** (lognormal median 3.85, σ 0.09 so ±2σ = 3.2–4.6, one systematic draw per replicate; per-fit noise σ 0.04; calibration ±10 %); 3 % chance a fit is re-run (cost doubles). r04: the measured r04 seed-1 fit (1.54) for the seed-2 I_max-0 fit, × 1.5 for the I_max-3 twin (14 VF 1.35 vs 2.02). XB2 = its twin (5.55). Model `vn_quote_model.py` (20,000 replicates), output `vn_quote_output.txt`. **The only physical datum for f is one grid (T = 20) on Owls**; V0 re-measures it on NOTS before V1 is released (§5.4).
### 5.2 Result
| | E | P90 | P99 | against |
|---|---|---|---|---|
| 6 N 10⁴ I_max 0 + 6 N 10⁴ I_max 3 + XB2 + r04 pair | **248.3** | 279.7 | 312.2 | approved ≈ 440 (P90 510) + r04 ≈ 4; cap 600 |
(VN_MINILEG_NOTE priced the original 12 held fits, with 6 m = 4 arms, at 440 / P90 510. Dropping m = 4 and replacing it with the cheap frozen-configuration arms is what lowers the quote.)
### 5.3 Stops (the monitor evaluates; any one → stop submitting, tell the manager at once; per-fit rule as HQ H-26 Q3)
| rule | threshold |
|---|---|
| **per-fit soft** | one fit's billed core-h > **1.5 × its class model** (committed table below; floor 3.0): report-and-continue, each trip reported at once; 3 soft trips in one wave = STOP |
| **per-fit hard** | > **2.5 × the committed class model** (floor 3.0): STOP; the hard line is **pinned to the committed table and never re-fitted** (a re-fit after V0 moves only the soft line and the next-wave quote) |
| wave | wave actual (billed) > 2 × the wave quote (§4) |
| cumulative | mini-leg actual > **400** (1.6 × E rounded up to 50) |
| projection ceiling | spent + class means × fits left > **600** (the approved cap) → HQ |
| failures / admission | FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage = STOP (NODE_FAIL / BOOT_FAIL = INFO, one rerun per fit); > 2 failed fits in a wave; engine `resource_limit` / `OUTCOME`; pending reason QOS / Assoc / MaxSubmit / Invalid / Limit |
| **arm identity** | recorded arm from `calib_meta.json` (N, `refine_m`, `I_max`, `I_used`, rule) ≠ the plan's → STOP; **N = 10,000 for every N 10⁴ fit, 2,500 for XB2 and r04**; behaviour: I_max 0 → no `cost/cost_diag_*` files; I_max 3 → diag k = `I_used` |
| **pairing identity (new)** | every section of the N 10⁴ fit's `calib.bin` except `meta` (`calib_meta.json` `sections[].sha256`) equals its N 2,500 twin's; the `grid` section above all. A mismatch → STOP (the contrast would not isolate N; HQ + manager) |
| data identity | `truth.json` X / y sha256 equal across all fits of a dataset and equal to the overlap / leg records |
| build identity | every fit's `binary.sha256` = `da0cf85b…` (BUILD_F2) |
Per-fit class models (committed; E / P90 per fit; soft = max(3, 1.5E), hard = max(3, 2.5E)):
| class | fits | E | P90 | soft | **hard** |
|---|---|---|---|---|---|
| vn N10⁴ m1 I_max 0 | 6 | 19.06 (per fit 15.4–21.0) | 22.67 | 28.6 | **47.6** |
| vn N10⁴ m1 I_max 3 | 6 | 20.68 (16.8–24.8) | 24.79 | 31.0 | **51.7** |
| XB2 (N 2,500, R′ 64, I_max 0) | 1 | 5.71 | 5.87 | 8.6 | **14.3** |
| r04 pair (R′ 16) | 2 | 1.99 (1.6–2.4) | 2.56 | 3.0 | **5.0** |
Expected soft trips 0.01, hard 0.000 under the model. Note the old VN_MINILEG_NOTE table (E 21.2 / 51.7 for m = 1 / m = 4 at I_max 3, hard 53.0 / 129.3) is **superseded** by this one (no m = 4 class; I_max-0 class added). **G-B cost criterion for this mini-leg's classes (HQ Q4):** class mean ≤ 1.5 × the committed model and no single fit > 2.5 × it; every exceedance of 1.5× listed.
### 5.4 V0 canary read-back checklist (what "clean" means for the self-release of V1 and V2)
(1) 5/5 fits delivered, all stages COMPLETED; (2) recorded arm = plan for every fit (§5.3), `I_used` 0 for the I_max-0 fits; (3) **pairing identity** for the AR N 10⁴ I_max-0 and I_max-3 fits against their leg twins (sections equal); (4) **XB2 bit check** (`xb_check.py` as in F2_IDENTITY_CHECK) against the leg record `4-AR-n200-r01-P-N2500-m1-I0-c1-s1`: 64/64 `evidence.logZ_r`, `selection.hpm`, 64/64 island `output_hash`, sidecars, fit/eval sections equal outside provenance; **a difference → STOP** (F2 ≠ F at R′ 64: the pooled baseline is not valid; HQ + Theory); (5) **f measured**: the two N 10⁴ islands' wall and billed core-h against their twins on NOTS; if the measured f is outside 3.2–4.6, re-quote V1 / V2 (soft lines and quotes move, hard lines do not); (6) merge wall and RSS at R′ 64, N 10⁴ (request 16 G); (7) cost ≤ the wave stop and each fit ≤ its soft stop; (8) X/y sha256 equal to the leg's; one binary sha; (9) `fit.bin` readable, `evidence.logZ_r` length 64, `fit.meta.occ` present.

## 6. Ops (derived from the precision leg's tools; no engine change; each reviewed with the commit)
| id | task |
|---|---|
| V-O1 | regenerate plans at F2 with `make_waves_vn.py` (tools from e993ece2); record plan shas in the deploy log |
| V-O2 | `deploy_wave.sh copybin` / `presubmit_check.sh` with the master binary = BUILD_F2 (`da0cf85b…`, from `staging/vn_minileg`); batch ids `VN_V<w>_<i>`; one `deploy_vn.log` line per batch (UTC, batch, sha256, home MB) |
| V-O3 | `stop_rules_vn.py` + probe: the class table above pinned by its sha256, §5.3 rules, pairing identity (reads the twin's `calib_meta.json` from `records/precision1e4`) |
| V-O4 | `collect_wave.sh` layout `records/vn_minileg/<wave>/<run_id>/`; per unit one `SHA256SUMS`; **`calib_meta.json` per fit** (`smcbvs4 info calib.bin --meta 1`, with the batch `env.sh`); kept per fit as in the leg (`fit.bin`, `eval.bin(.json)`, sidecars, `truth.json`, `cost/`, `log/`, `manifests/`); `law.bin` for the 12 N 10⁴ fits and XB2; `setup.bin` not needed |
| V-O5 | a clean per-run cost directory for the freeze (symlinks to the per-run `cost_<run_id>.json` only; the leg's baselines + the mini-leg's) |
| V-O6 | Haiku monitor prompt = the leg's `MONITOR_PREC_PROMPT.md` with this §5.3 table; cadence ≤ 1 probe per 5 min; read-back per wave (Sonnet): collect, `sha256sum -c`, per-fit table, stops, quote re-fit |
Home guard 7,900 MB; jobs write only under `scratch/`; polling and submission per POLICIES §12.7. Offload and cleanup as the leg (verification line per wave to HQ).

## 7. What is not in this mini-leg
ablations and competitors; the G-B pilot and its I_max-3 twin (G-B plan, `results/gb/`); anything at 10⁵ or 10⁶; π₀(S₀) (HQ Q6, deferred, re-planned after the mini-leg); systematic resampling (HQ Q5, off, "not tested"); m = 4 at N = 10⁴; the m × I_max interaction. **Note for the G-B plan** (`GB_PLAN.md` §1 row "I_max of the mini-leg's N = 10⁴ arms"): the frozen combination (N 10⁴, I_max 0) **is** run here (6 fits), so the G-B pair is not its first test at 10⁴.

## 8. Files and sha256 (`results/vn_minileg/`)
| file | sha256 |
|---|---|
| `precision_freeze_vn.py` (registered by MINILEG_PREREG) | `114f7e7847dc9efef111c6888feb2f6616edd24ba18244062332cfba84e4cf73` |
| `vn_offset_contrast.py` (registered by MINILEG_PREREG) | `89725c169f8231bc6b6b37c9f20e5a9af88b4cced22f13200dbc599afb3a2655` |
| `tests/test_vn_golden.py` (4 cases) / `tests/test_vn_offset_contrast.py` (1 case) | `22c1bd6bacce9715901ef4d282c586848fdd2d302fee5aad03718ed99cd966e3` / `9ef9b9e73e30f84b9def13e24a34dc690156389d1ed417b8a228a0f2ab9a1331` |
| `make_waves_vn.py` / `waves_vn.json` / `make_waves_vn_output.txt` | `e82404c74da3d36a706ce122f68f7a579cb272c20967ee6cc4d88805fa6057ac` / `21a9679ff28261f5ef0963a9714ca07bdf6f93498f30b783ab193dbfc28491e7` / `9e09419fcd91ebea7acb8b90267a990fcbc02ecba227e1894b70782a5df521ce` |
| `vn_quote_model.py` / `vn_quote_output.txt` | `408bf9a4e260542efb041de155cef4b57c75b5779792338bfc4db27dccddc104` / `f18b1b3286ac8c65592b0c0973f011cff99be418ff99677ddcfcbab17d1f06d4` |
| `vn_budget.py` / `vn_budget_output.txt` | `35591b2ba2fc05cb0a1a29a381e00757b41670b3f5371911003f29c852adff8a` / `40b9367d4718e906bcc7e93cdd60b6b82299e3a5f978c969578e81281e27effd` |
| `extract_twin_costs.py` / `twin_costs.csv` | `d4d23ec62cfaa21f6f8d42c863d9ee1f7a8232891b72384dcf8b72f3dd6d762a` / `30507874e7650975c0a88f1bb5310f62acf2a1f52178c04b6ee1e63da70de3be` |
| registered, unedited | `precision_freeze.py` `7cdd69a11f3aaffa7a6615df639aefbe101042e9d37a8d520999ccbdc6279605`; `precision_offset.py` `cbbc23012e6900ff7798267cc7325816ad0b8312ec6e26fd09972adc9780d300` |
