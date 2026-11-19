# LEG_PLAN: precision study (Sol F6) + 10⁴ science: plan, cost quote, waves, ops (Engineering, Sonnet plan writer; Thu 2026-11-19)

**Status: reviewed; fixes applied; HQ rulings bd02631e applied; self-release (canary Fri 11-20).** Review: `reviews/PLAN_REVIEW_OPUS.md` (Opus, ACCEPT-WITH-FIXES; every fix in it is applied below, labels R1–R17). HQ rulings Q1–Q6 (HQ_DECISIONS bd02631e): §0. Nothing is deployed or submitted; the Engineering manager commits. Companion: `PREREG.md` (criteria, the pre-declared offset measurement, scripts + sha256).

## Summary (≤ 10 lines)
1. **Frozen binary F (eefcbc4a) can do: m ∈ {1, 4}, I_max ∈ {0, 3}, BLK(20, 0.5), n = 100/400/800, AR-weak. It cannot do N = 10⁴ in V mode (B2: `V_N` is a constant), systematic resampling (B3), or a calibration seed different from the final seed (B1).** Two plan names are also wrong and would have been silent or fatal: `grid_refine_m` (ignored: m = 4 would have run as m = 1) and `partition = exact_linkage` (refused; the engine says `exact`). All verified on an F-equivalent binary (§1).
2. **Scope released now:** 18 precision fits (R′ = 64: m ∈ {1, 4} × 2 replicates × 3 datasets = 12, plus **6 new I_max = 0 arms**) + the 156 science fits (14 overlap V fits reused, none re-run; **if the freeze changes m or I_max they and an A3 pair are re-run**) + two A0 canaries (A3, and an **XB cross-build bit check**). **Held (HQ Q1): the 12 N = 10⁴ fits**, to be run in a separate V-N mini-leg (§0). Science runs **after** the precision freeze, in the frozen configuration (§3).
3. **Offset measurement:** one pre-declared surface δ(N, m, I_max, k) = V − T log Ẑ; R′ (k = 4, 8, 16, 32, 64) comes free from disjoint island blocks of existing and new records; reader validated: reproduces −0.00394 (CI −0.0071…−0.0008). No pass/fail (PREREG §4).
4. **Quote (MEASURED basis): E = 592 core-h released scope (P90 673); 942 with the held arms (P90 1,063), against the plan figure 4,127 → self-release YES** (even m = 4 frozen: E 957, P99 1,262). The manifest's 35 / 141 core-h per precision fit were 3–8× too high (modelled from measurements: 6.3 for m = 1, 12.4 for m = 4 at N = 2,500, R′ = 64; 17 for m = 1 at N = 10⁴).
5. **Stops (HQ Q3 APPROVED):** per fit soft 1.5 × class model = report-and-continue, hard 2.5 × = STOP, **pinned to the committed class table**; per wave 2 × quote; cumulative 1,000 (scope in release); projection ceiling 4,127; arm-identity (settings **and** behaviour), data-identity and build-identity stops. **G-B cost criterion (HQ Q4):** class mean ≤ 1.5 × model AND no single fit > 2.5 × model.
6. **Waves:** A0 canary (4 fits: m = 4, I_max = 0, A3, XB), P1–P4 (precision), FZ (freeze checkpoint), S1–S9 (science), H1–H3 held; ≤ 4 batches and ≤ 150 tasks per batch; **ONE build of the V arm for the whole leg** (H-25).
7. **Timeline:** fixes + commit + canary Fri 11-20; precision Sat 11-21; freeze Sun 11-22; science Mon–Tue; **leg report realistically Wed 11-25** (inside H-14's 11-22..26; a freeze change adds ≈ ½ day) → G-B pilot → 10⁵ from Fri 11-27 if G-B passes.
8. **HQ rulings (bd02631e) applied:** Q1 hold N = 10⁴ + V-N mini-leg (follow-up, out of scope); Q2 one seed per arm, **Q2 stream check (manager, at F): PASS — Philox key = (seed, role<<28 | tier<<26 | iter<<20 | island) (include/v4/rng.h:62-64); calibration islands draw under role R_PILOT / R_DIAG, final islands under R_FINAL (src/island/island_run.h:219,238) → distinct keys, disjoint position-addressed substreams, no stream reuse.**; Q3, Q4 as above; Q5 resampling off, "not tested"; Q6 π₀(S₀) deferred (open item, re-planned with the mini-leg).

## 0. HQ rulings needed before launch (Q1–Q6 as the plan review states them) and HQ's answers (HQ_DECISIONS bd02631e)
| # | item | options (review) | review recommendation | **HQ ruling (bd02631e)** |
|---|---|---|---|---|
| **Q1** | **B2: V cannot run N = 10⁴** (H-25 (3) asked for offset vs N; G-A says freeze N) | (a) hold H1–H3 and freeze N = 2,500 *by default, NOT TESTED*; (b) engine change now, inside this leg: `V_N` → `calibrate --N` (V only, default 2500, same bits at 2500), new binary F′ → breaks H-25 (2) "one build per arm per leg" and touches the owner-signed method freeze (H-17); (c) = (a) for this leg **plus** authorise the small V_N PR now, with its freeze-reproduction check (T3 hashes, goldens, one 10⁵ island hash), and run H1–H3 (≈ 350 core-h) as a separate mini-leg on F′ before G-C; that re-runs the same freeze rule for N and unblocks the 1M N = 5,000 self-check (H-9) and the G-C2 doubling fit, which F also cannot run | (c) | **APPROVED: the 12 N = 10⁴ fits are HELD in this leg.** A separate **V-N mini-leg** runs before 1M (§8): a minimal engine diff on F; default-N outputs bit-identical to F on the overlap fixtures (`identical()` on all fields); one Opus diff review + Sol 6.2; a new freeze tag; a cost quote to HQ before any run. The 10⁴ / 10⁵ freeze record says "N provisional, 2,500" |
| **Q2** | **B1: one seed per arm** (Sol F6 / MANIFEST v0.4: separate calibration and final seeds) | (a) accept: calibration and final islands use distinct Philox roles of one seed, every arm and replicate has its own seed, and the grid vs island variance split stays estimable; (b) engine change to accept a separate calibration seed | (a), recorded as a MANIFEST v0.5 note; the leg report gives the grid/island variance decomposition | **APPROVED with a check:** one seed per arm, valid only if calibration and final stages draw **disjoint position-addressed substreams** of that seed. **Q2 stream check (manager, at F): PASS — Philox key = (seed, role<<28 | tier<<26 | iter<<20 | island) (include/v4/rng.h:62-64); calibration islands draw under role R_PILOT / R_DIAG, final islands under R_FINAL (src/island/island_run.h:219,238) → distinct keys, disjoint position-addressed substreams, no stream reuse.** |
| **Q3** | **V per-fit stop** (plan: soft 1.5× report-and-continue, hard 2.5×; H-23 (3) kept V per-fit = STOP) | (a) literal 1.5× STOP (≈ 3–4 expected halts, mostly in unmeasured classes); (b) the plan as drafted; (c) (b) with the hard 2.5× anchored to the **committed** class table (never re-fitted), 3 soft trips per wave = STOP, each trip reported at once | (c) | **APPROVED (c):** V per-fit soft 1.5× = report-and-continue, hard 2.5× = STOP, pinned to the committed cost table (§5.3) |
| **Q4** | **What "model" means for G-B** ("measured core-h per fit ≤ 1.5× model") | (a) every fit ≤ 1.5× the committed class model (≈ 3.7 expected misses → G-B likely fails on noise); (b) class mean ≤ 1.5× the committed class model, every per-fit exceedance listed | (b), fixed in the PREREG before the commit | **APPROVED (b) with a guard:** G-B cost criterion = class mean ≤ 1.5 × model **AND no single fit > 2.5 × model** |
| **Q5** | **B3: systematic resampling** not testable | (a) frozen OFF, "not tested", D-14 closed by default; (b) an engine switch (new build) | (a); do not fold it into the Q1 PR unless Theory asks | **(a): off, reported "not tested"** |
| **Q6** | **B4: π₀(S₀) / claim C3** | (a) defer, report A3 on outcomes only, keep `setup.bin` of the 30 A3-pair fits (R15); (b) a reader tool now | (a) | **(a): deferred.** Listed as an open item (§8) and re-planned with the V-N mini-leg |
Also for information (review): the overlap T arm ran the truncated partition (§1.2); the 1M budget depends on the m decision (§0-v2.5 "precise" ≈ m = 4); the freeze is efficiency-based because the §0-v2.3 targets are already met at 10⁴ (§8). The cost envelope self-releases (E 592 / P90 673 ≪ 4,127); H-25's "offset vs N" is not fully answerable in this leg (B2): said plainly in PREREG §3.3 and §4.1 (R9).

## 1. Feasibility with the FROZEN binary F (task 1)
**Basis.** F = `eefcbc4a2ab42fdf52ec1e5d318a956bdd07f463` (tag `method-v3.1.1-listpip`). Engine sources read at origin/exp/P1M-engine **b89cba4d** in my worktree `~/SMC_Engineering_Department/tmp/20261119-precplan/wt_b89cba4d` (paths below are `Scripts/SMC_BVS/engine_v4/…`). `git diff eefcbc4a b89cba4d -- src include` is the `xeval` command only, `tools/slurm` differs by the driver PRs #86/#87 (no `src/` effect). **Executable check:** `feasibility_smoke.sh` runs F's engine (an existing Owls build of dc0474eb = F + xeval only; sha256 `b9dc443e66d79ab2…`) on n = 100, p = 400, 2 threads, nice, seconds; output `feasibility_smoke_output.txt`.

| arm parameter / design | F can do it? | evidence (file:line) | smoke result | verdict |
|---|---|---|---|---|
| **grid refinement m ∈ {1, 4}** | **YES**, under the name `refine_m` (calibrate, V only; 1…64) | `src/calib/calib_run.cpp:133` (reads `I_max`, `refine_m` from the manifest params), `:115-116` (V only), `include/v4/calib.h:296` + `include/v4/calib_rules.h:195` (each interval split into m) | `--refine_m 4` → island T = 92 = 4 × 23 | OK. **Plan name `grid_refine_m` is read by nothing** (`tools/slurm/p1m_cells.py:169`): calibrate with `--grid_refine_m 4` gives `refine_m` 1 (silent no-op) → fix **C1** |
| **I_max ∈ {0, 3}** | **YES** (`I_max`, default 3, 0…1000, must be ≤ ℓ) | `calib_run.cpp:133`, `include/v4/calib.h:178-179` | `--I_max 0` → recorded `I_max 0` in `calib.bin.json settings` | OK. The leg's plan carries `I_max` explicitly (**C1/C2**) |
| **N ∈ {2,500, 10⁴}, V mode** | **NO. BLOCKER B2.** V's final N is the compile-time constant `V_N = 2500` | `include/v4/calib_run.h:39,53` (`frozen_N` returns `V_N` for the bounded rule), `src/merge/wp4_io.cpp:336` (merge refuses a V calib.bin with N ≠ 2500), `src/island/island_cmd.cpp:223-224` (island refuses a manifest N ≠ calib's) | `calibrate --N 10000` is ignored (`N_final` 2500); `island --N 10000` → `invalid_input … N differs from calib.bin's frozen N = 2500` | **12 of 24 manifest precision fits cannot run** (and the 1M N = 5,000 self-check has the same constant) |
| **calibration seed ≠ final seed** | **NO. B1.** `calib_seed` is read by nothing; calibrate and island both use the manifest's `seed`, and the island **refuses** a seed different from the calibration's | `p1m_cells.py:244` (placeholder), `src/island/island_cmd.cpp:221-222`, `src/calib/calib_run.cpp:178` | island `--seed 8` after a seed-7 calibration → `invalid_input … differs from the calibration's seed 7` | One seed per arm (§1.2) |
| **systematic resampling** | **NO. BLOCKER B3.** Only multinomial resampling exists; no switch | `src/island/island_run.h:316` (`resample()`, addressed uniforms), `:781` (the one call) | — | Not testable in this leg (§1.2) |
| 10⁴ science: **BLK(20, 0.5)** | YES (defaults b = 20, ρ = 0.5) | `include/v4/gen.h:28`, `src/common/gen.cpp:31` (BLK ρ default 0.5), `:58-60` (truths in distinct blocks); driver `DESIGNS` `p1m_driver.py:70` | gen ran for AR; BLK path is the same CLI | OK |
| **n = 100 / 400 / 800**, AR-weak | YES (`n`, signal `weak` = a 0.6) | `p1m_driver.py:70-71,804-808` (n, signal, amplitude passed to gen), K = min(p, n/2) from data | n = 100 ran end to end; 400 and 800 use the same code path | OK. Cost scaling with n is **unmeasured** (§5) |
| **A3 `partition = exact_linkage`** | **Name wrong.** The engine accepts `truncated` or `exact` | `src/setup/setup_run.cpp:214-217` | `--partition exact_linkage` → rc 13 `invalid_input: setup: partition must be truncated or exact`; `--partition exact` → completed, `partition: exact` | Fix **C3** (`exact`). All 15 A3 fits would have failed at setup |
| params reach the engine | YES, but **every** stage manifest receives all `params` and each command reads only its own keys | `p1m_driver.py:787-790` (`base_params.update(params)`) | — | OK: `refine_m`/`I_max` ride along harmlessly |
| `grid_unconverged`, flags, occ, σ̂, island PIP sd | recorded in `eval.bin.json` | `evidence.sigma_hat`, `fit.meta.occ[M].sd_log_Z_occ_r`, `pip.island_spread.max_sd`, `fit.meta.flags` (read from the 40 overlap records) | — | the §0-v2.3 targets are computable from the collected records |
| exact log π₀(S₀) (C3, A3's π₀ column) | **NO. B4 (reporting gap).** No command or record field | grep of `src include tools` | — | science reports outcomes, PIPs, evidence, d_H; π₀(S₀) deferred (§1.2) |

### 1.1 Plan-side corrections (not engine changes; applied in `make_waves_prec.py`, the generator stays as committed, like the overlap's `make_waves.py` forced the T arm)
- **C1** precision params `{grid_refine_m, calib_seed}` → `{refine_m, I_max: 3}`. **C2** new arms I_max = 0. **C3** A3 `partition` `exact`. **C4** explicit resource shapes (the generator's 1e4 defaults ask 16 CPUs for 15 min per island, 4× over-sized and billing-irrelevant but worst-case-inflating) and `island_throttle`.

### 1.2 Blockers: smallest option each (nothing is designed around silently; HQ rules before launch)
| id | what F cannot do | smallest option | what it costs the science | needs |
|---|---|---|---|---|
| **B1** | an independent calibration seed (k = 20 + a) next to the final seed (k = 10 + a) | **one seed per arm = the final seed (k = 10 + a)**; the unused k = 20 + a stays reserved. Calibration (PILOT/DIAG roles) and final islands are different Philox domains of one seed (`include/v4/rng.h`; `tests/test_rng.cpp:146`: all addresses unique over pilot, diagnostic and final roles), and every arm and replicate has its own seed, so arms and replicates are mutually independent | Sol F6 asked for "independent calibration and final seeds". What is lost: the ability to hold the grid fixed and vary the final seed (not needed by any criterion). Replicate independence is unaffected | **HQ Q2: APPROVED with a stream check** (Q2 stream check: PASS (manager, at F: distinct Philox keys by role — calibration R_PILOT/R_DIAG vs final R_FINAL; include/v4/rng.h:62-64, src/island/island_run.h:219,238; no stream reuse)); MANIFEST v0.5 note |
| **B2** | V at N = 10⁴ (12 precision fits; later the 1M N = 5,000 self-check) | **(a) hold the 12 fits (H1–H3, priced, never submitted) and freeze N = 2,500 (D-1 default), N = 10⁴ recorded as NOT RUN**; or **(b)** an engine change: make `V_N` a `calibrate --N` (V only, default 2500), record it in calib meta, relax `wp4_io.cpp:336` to `N ≥ 1`; same bits at 2500 by construction, but it is **a new binary F′** → HQ ruling against H-25 "no new engine builds", a repeat of the freeze reproduction check (T3 hashes, goldens, one 10⁵ island hash) and a new deploy of the V arm | Without N = 10⁴ the leg cannot say whether doubling-doubling N helps; the V − T offset vs N is then read only from T's own N (10⁴ tier 0, 4 × 10⁴ tier 1: 3 escalated fits) | **HQ Q1: APPROVED — hold; V-N mini-leg follow-up (§8)** |
| **B3** | systematic resampling | **not tested; frozen OFF = the D-14 default** ("off unless the study shows a gain"). The study can neither show nor exclude a gain | D-14's question stays open; flag for Theory/HQ. An engine switch is a new build | **HQ Q5: off, "not tested"** |
| **B4** | π₀(S₀), start-mass lattice (C3; the A3 "π₀(S₀)" comparison) | report A3 on outcomes (HPM = S₀, PIP, log Ẑ, d_H) only; π₀ would need a setup.bin reader (separate tool or build) and the science fits' `setup.bin` kept | claim C3 deferred | **HQ Q6: deferred (§8)**; keep `setup.bin` of the 30 A3-pair fits (R15) |

**I_max and resampling (the manifest's OPEN item), resolved.** I_max = 0 **cannot be read off** the existing arms: it differs in the grid the final islands run on, so it needs final islands on the preliminary grid. It gets **6 arms** (a = 8, 9; N = 2,500, m = 1, 2 replicates × 3 datasets), seeds data_seed + 1800 / 1900, measured cost ≈ 5.8 core-h per fit = **35 core-h in all** (the manifest estimated 106). Resampling: B3.

**Observation (not a blocker).** The overlap's T arm ran with `partition truncated` (`setup.bin.json` of `4-AR-n200-r01-T-s1.T2`: `"partition": "truncated"`; ENGINEERING_SPEC §0-v2.1 says T uses exact complete linkage; law mode defaults to truncated: `include/v4/setup.h:73`, exact only for compat `src/setup/setup_run.cpp:213`). The T-vs-V comparison was therefore truncated-vs-truncated; the A3 pairs in this leg are the only exact-linkage fits. **For information to HQ and Theory, beside the verdict (R14):** every one of the 40 overlap T setups says `truncated`.

## 2. Scope (task 2)
### 2.1 Precision study (datasets: overlap rep 1 of AR-strong, AR-weak, ADJ-OPP; R′ = 64; run ids `4-<AR|ARweak|ADJOPP>-n200-r01-P-<arm>-s1`)
| arm | N | m | I_max | replicates | seed (= data_seed + 100·k, k) | status | fits |
|---|---|---|---|---|---|---|---|
| a0, a1 | 2,500 | 1 | 3 | c1, c2 | k = 10, 11 | **released** (baseline) | 6 |
| a2, a3 | 2,500 | 4 | 3 | c1, c2 | k = 12, 13 | **released** | 6 |
| a8, a9 (**new**) | 2,500 | 1 | **0** | c1, c2 | k = 18, 19 | **released** | 6 |
| a4–a7 | **10,000** | 1, 4 | 3 | c1, c2 | k = 14…17 | **HELD (B2)** | 12 |
Datasets of the precision fits are the **same data** as the overlap's rep 1 (same data seed; `truth.json` X/y sha256 are checked equal to the overlap records, §6.4). Seeds are disjoint from every other fit (`check_seeds` in `p1m_cells.py`; the new k = 18, 19 are asserted free in `make_waves_prec.py`).

### 2.2 10⁴ science, V (156 new fits; **14 overlap V fits reused, not re-run**)
| design | n | fits to run | reused from the overlap | note |
|---|---|---|---|---|
| AR-strong | 100 / 200 / 400 / 800 | 10 / 12 / 10 / 10 | – / **8** (reps 1–4 × s1, s2) / – / – | seed 2 on all 10 reps at n = 200 |
| AR-weak | 100 / 200 / 400 / 800 | 20 / 18 / 10 / 10 | – / **2** (reps 1, 2 s1) / – / – | 20 reps for n ≤ 200 |
| IND | 100 / 200 / 400 | 5 / 4 / 5 | – / **1** / – | |
| BLK(20, 0.5) | 100 / 200 / 400 | 5 / 5 / 5 | – | |
| ADJ-OPP | 200 / 400 | 3 / 5 | **2** / – | mandatory at 10⁴ |
| NULL | 200 | 4 | **1** | null control |
| A3 (`partition exact`) | 200 | 10 AR + 5 BLK = 15 | – | each paired with the default-partition V fit (seed 1) of the same data; the AR pairs on reps 1–4 use the reused overlap fits |
Total 156 + 14 reused = 170 science fits (the 14 are the overlap's V fits: `4-AR-n200-r01..r04-V-s1,s2`, `4-ARweak-n200-r01,r02-V-s1`, `4-ADJOPP-n200-r01,r02-V-s1`, `4-IND-n200-r01-V-s1`, `4-NULL-n200-r01-V-s1`). **Reuse is valid only if the freeze keeps (N 2,500, m 1, I_max 3)**; otherwise they are re-run as tag `VF` (§3).
**Not in this leg:** ablations (482 planned) and competitors (400) on the 10⁴ datasets; the G-B 10⁵ pilot; anything at 10⁵.

## 3. Sequencing: the precision freeze comes first (a dependency the manifest leaves implicit)
ENGINEERING_SPEC §0-v2.6 G-A: "the precision study freezes (N, m, resampling, I_max) → 10⁴ science, then 10⁵". The science fits must therefore run **in the frozen configuration**. Plan: waves A0, P1–P4 first (≈ 150 core-h), **checkpoint FZ** (registered scripts, one Opus check, HQ informed: PREREG §3, §6), then the science waves.
| freeze outcome | science block | reuse of the 14 overlap fits | science E | released-scope E (cumulative stop) |
|---|---|---|---|---|
| (2,500, m 1, I_max 3) (baseline kept) | as quoted | yes | 441 | **592 (1,000)** |
| m = 4 adopted | `refine_m 4` on all science fits, +15 re-runs (14 tag `VF` + the A3 pair, tag `A3F`) | no | 805 | 957 (1,600) |
| I_max = 0 adopted | `I_max 0`, +15 re-runs (14 `VF` + `A3F`) | no | 354 | 505 (900) |
(`make_waves_prec.py --frozen-m / --frozen-I`; `quote_output_freeze_m4.txt`, `quote_output_freeze_i0.txt`.) All three are far inside the plan figure. **R6 (review): the A0 A3 canary and the XB check always run in the baseline configuration; if the freeze changes m or I_max the AR r01 A3 pair is re-run in the frozen configuration as `4-AR-n200-r01-A3F-exactlink-s1` (paired with the `VF` default fit), so no m = 1 A3 fit is ever paired with a frozen-configuration default fit.** **If both m = 4 and I_max = 0 are adopted** the combination was not run in the study (PREREG §3.2): S1 is then released as a one-batch pilot (7 fits) and re-quoted before the rest.

## 4. Waves (≤ 150 array tasks per batch; ≤ 4 batches per wave; every task ≤ 2 h)
Plans: `make_waves_prec.py` (output `make_waves_prec_output.txt`, `waves.json`): driver `--strict` clean, no warnings, 187 fits in 17 waves. Quote per wave from `quote_model.py` (`quote_output.txt`). "Worst" = limit sum (the ledger/admission figure, not a cost estimate). Island arrays are throttled (`%32` precision, `%8` science) so a wave's peak stays < 1,000 CPUs (QOS cap 1,536).
| wave | content | fits | batches / tasks | **E** (P90) | **QUOTE** → wave stop (> 2×) | worst (limit sum) | release |
|---|---|---|---|---|---|---|---|
| **A0** | canary: AR m4-c1 + AR I0-c1 (R′ 64); A3 canary `4-AR-n200-r01-A3-exactlink-s1`; **XB cross-build bit check** `4-AR-n200-r01-V-XB-s1` (the overlap fit re-run with the leg build, baseline config) | 4 | 3 / 176 | 22.8 (26.6) | **25 → 50** | 374 | **self-release (HQ bd02631e): canary Fri 11-20** |
| P1 | AR: m1 c1, c2; m4 c2; I0 c2 | 4 | 2 / 272 | 30.2 (35.0) | 30 → 60 | 557 | self-release after A0 read-back clean |
| P2 | ARweak: m1 c1, c2; m4 c1, c2 | 4 | 2 / 272 | 28.1 (32.3) | 30 → 60 | 557 | self |
| P3 | ARweak I0 c1, c2; ADJ-OPP m1 c1, c2 | 4 | 2 / 272 | 24.5 (28.2) | 25 → 50 | 557 | self |
| P4 | ADJ-OPP m4 c1, c2; I0 c1, c2 | 4 | 2 / 272 | 45.7 (53.9) | 45 → 90 | 557 | self |
| **FZ** | freeze checkpoint (no jobs) | – | – | – | – | – | Opus check + HQ informed |
| S1 | science n = 200: AR-strong 12 + AR-weak 13 + ADJ-OPP 3 | 28 | 4 / 560 | 58.4 (64.8) | 60 → 120 | 1,307 | after FZ |
| S2 | n = 200: AR-weak 5, BLK 5, IND 4, NULL 4 | 18 | 3 / 360 | 31.7 (35.4) | 30 → 60 | 840 | self |
| S3 | A3 (14 remaining: AR 9, BLK 5; setup limit 0:30 from the canary) | 14 | 2 / 280 | 38.7 (43.2) | 40 → 80 | 681 | self |
| S4 | n = 100: AR-strong 10 + AR-weak 18 | 28 | 4 / 560 | 39.9 (48.2) | 40 → 80 | 1,307 | self |
| S5 | n = 100: AR-weak 2, BLK 5, IND 5 | 12 | 2 / 240 | 18.7 (22.9) | 20 → 40 | 560 | self |
| **S6** | **n = 400 pilot**: ADJ-OPP 5, AR-strong 2 | 7 | 1 / 140 | 30.3 (39.5) | 30 → 60 | 467 | self; **re-quote n = 400 from it** |
| S7 | n = 400 rest: AR-strong 8, AR-weak 10, BLK 5, IND 5 | 28 | 4 / 560 | 97.6 (124.6) | 100 → 200 | 1,867 | self if the re-quote ≤ 1.5× this quote, else HQ-informed |
| **S8** | **n = 800 pilot**: AR-strong 7 | 7 | 1 / 140 | 48.5 (66.2) | 50 → 100 | 611 | self; **re-quote n = 800** |
| S9 | n = 800 rest: AR-strong 3, AR-weak 10 | 13 | 2 / 260 | 77.4 (104.0) | 75 → 150 | 1,135 | self (same rule) |
| H1–H3 | **HELD (HQ Q1)**: N = 10⁴: AR, ARweak, ADJ-OPP × (m 1, 4) × (c1, c2) | 12 | 2 / 272 each | 115 / 81 / 153 (138 / 96 / 183) | 115 / 80 / 155 → 230 / 160 / 310 | 557 each | **not in this leg: the V-N mini-leg (§8) re-prices them** (islands limit 0:30 → 1:00 for m = 4 at N = 10⁴, from A0/P2 timings) |
`waves.json` lists every run id. **Submission pacing:** one `submit.sh` per batch (2 + 3 × fits `sbatch` calls: 8 for a precision batch, up to 23 for a science batch; the overlap's W1 batches were 20), the batches of a wave **≥ 5 min apart**, never a burst of the whole wave. If the freeze changes (m, I_max), the 14 `VF` re-runs add a wave S10 (13 fits) and the quotes are re-run with the same script (the scenario table in §3).

## 5. Cost quote (task 4)
### 5.1 Basis: MEASURED V costs (not the manifest's planning values)
- **Measured:** the 20 counted V fits of the overlap (n = 200, N = 2,500, R′ = 16, m = 1, I_max = 3; `measured_V_costs.csv`, from `W*_cost_stages.csv` and the island records): **1.99 core-h mean** (1.7–2.9; NULL 0.5), setup 0.03, calibrate 0.44–1.10, 16 islands 0.9–1.7, merge 0.05, eval 0.03. The manifest priced a precise 10⁴ V fit at **10**.
- **Island cost fit** (OLS on the 18 non-NULL fits): island core-h = 0.0256 + 0.00189 × (T + 12), T = bridging stages of the frozen grid (9–24; the calibrated grid length varies by seed and dataset), 12 = L 8 + Hm 4. **m = 4 multiplies T by 4 (confirmed: 23 → 92 on the F binary)**, so a refined island costs ≈ 2.2–2.9× a coarse one, not the manifest's 1×.
- **Scaling to the leg:** R′ = 64 → islands × 64 and merge × (0.3 + 0.7·R′/16); I_max = 0 → calibration × U(0.2, 0.5). **N = 10⁴ (held):** per-step cost ∝ N (× 4).
- **n-scaling is NOT measured at 10⁴** (every overlap fit is n = 200). Stated assumption: per-step cost × the planning model nf(n) = (3(30 + 60n/200) + 30)/300 = 0.7 / 1.0 / 1.6 / 2.8 for n = 100 / 200 / 400 / 800, lognormal σ 0.2; stage count T(n) = T(200)·(n/200)^g, g ~ U(0, 0.5), shared per n-level. This is why S6 and S8 are one-batch pilots.
- Other unmeasured items, all in the P90: R′ = 64 merge cost and memory (A0 measures), exact-linkage setup at p = 10⁴ (A3 canary), I_max = 0 calibration fraction (A0), BLK (AR pool proxy, extra σ 0.2), infrastructure reruns (3% per fit, doubling the fit).
- Model: `quote_model.py`, 20,000 replicates, fixed seed, `quote_output.txt`.

### 5.2 Result against the plan figure (MANIFEST_CELLS v0.4: precision 2,117 + science 2,010 = **4,127**)
| scope | fits | E | P50 | P90 | P99 | % of 4,127 |
|---|---|---|---|---|---|---|
| precision released (A0 incl. the A3 canary and XB, + P1–P4) | 18 (+ A3 canary, XB) | 151 | 150 | 170 | 190 | 7% of 2,117 |
| science (S1–S9) | 156 (minus the A3 canary in A0) | 441 | 437 | 510 | 584 | 22% of 2,010 |
| **released scope** | 175 | **592** | 588 | **673** | 758 | **14%** |
| held N = 10⁴ (H1–H3; **HQ Q1: not run in this leg**) | 12 | 349 | 346 | 403 | 464 | – |
| **leg with held arms** | 187 | **942** | 936 | **1,063** | 1,187 | **23%** |
P(total > 4,127) = 0.0000 in every scenario (m = 4 frozen: E 957 / P99 1,262; with the held arms 1,306 / 1,677). **Self-release: YES** (H-25 (3): the quote is within CAMPAIGN_PLAN_1117's figure for this leg). Per-fit E by class: `quote_output.txt`. What is NOT in these numbers: ablations, competitors, the G-B pilot, analysis compute.

### 5.3 Stops (the monitor evaluates; any one → stop submitting and tell the manager at once). **Per-fit rule and G-B criterion: APPROVED by HQ (Q3, Q4; bd02631e)**
| rule | threshold |
|---|---|
| **per-fit (soft)** | one fit's billed core-h > **1.5 × its class model** in the **committed class table below** (floor 3.0 core-h): **report-and-continue** (HQ Q3), *provided* the fit completed valid, cost ≤ 2.5 × the committed model, fewer than 3 soft trips in the wave, and no wave/cumulative stop is hit. **Each trip is reported at once** (≤ 3 lines). A re-fit from measured fits (after A0, S6, S8) moves only the soft line and the next-wave quote; **the hard line is never moved** (R10). The model says **3.8 soft trips are expected over the 187 fits** (mostly one shared n-level or m = 4 error) |
| **per-fit (hard)** | > **2.5 × the committed class model** (floor 3.0), or **3 soft trips in one wave**: **STOP** (expected 0.02 hard trips). A hard trip in a pilot class means the committed model was wrong: stop, re-quote, HQ re-pins the table. *(Fallback, if HQ revokes Q3: the literal 1.5× = STOP on the same table, ≈ 4 expected halts.)* |
| **wave** | wave actual (all its batches, billed) > **2 × the wave quote** (table §4) |
| **cumulative** | leg actual > **1.6 × E of the scope in release, rounded up to 100: baseline 1,000** (m = 4 frozen 1,600; I_max = 0 frozen 900; with H waves released: 1,600 / 2,100 / 1,400) |
| **projection ceiling** | spent + (class means × fits left) > **4,127** (the plan figure) → HQ before any further wave |
| failures | any FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (NODE_FAIL / BOOT_FAIL = INFO; one rerun per fit, manager's call); > 2 failed fits in a wave |
| admission / queue | engine `resource_limit` / `OUTCOME` record; pending reason QOS / Assoc / MaxSubmit / Invalid / Limit |
| **arm identity (new), settings AND behaviour** | recorded arm from the fit's own calibration record (`calib_meta.json`: N, `refine_m`, `I_max`, `I_used`; fallback `calib.bin.json settings`) ≠ the plan's arm → STOP (the silent no-op class, §1). **Behaviour (R5; the setting alone is not enough):** m = 4: island T % 4 = 0 **and T ≥ 36** (m = 1 grids can be T = 12, 16, 20, 24, so "multiple of 4" alone does not tell m = 4 from m = 1); I_max = 0: **no `cost/cost_diag_*` files**; I_max = 3: diagnostic rebuild index k in `cost/` = `I_used`. A behaviour miss with a matching record is a flag to the manager (the record is authoritative), not a stop |
| **data identity** | `truth.json` X/y sha256 equal across all fits of a dataset **and equal to the overlap records** for the shared datasets (precision, A3 pairs, reused fits) |
| build identity | every **new** fit's `binary.sha256` = the leg's single build (§6.1); the **14 reused overlap V fits are exempt by their listed shas** (4 builds of F: ba569a33 W0-V2, 72c9109d W1, 1e375b74 W2, 4fecb186 W3), whose equivalence with the leg build is what the XB check in A0 tests (R7) |
**Committed class table** (E per fit from `quote_output.txt`, sha256 in §9; soft stop = max(3, 1.5E); hard = max(3, 2.5E); the hard column is the pinned line):
| class | fits | E | P90 | soft | hard |
|---|---|---|---|---|---|
| prec N2500 m1 I3 / m1 I0 / m4 I3 | 6 / 6 / 6 | 6.28 / 5.76 / 12.36 | 8.12 / 7.43 / 17.81 | 9.4 / 8.6 / 18.5 | 15.7 / 14.4 / 30.9 |
| prec N10⁴ m1 / m4 (held; for the V-N mini-leg) | 6 / 6 | 17.00 / 41.29 | 23.50 / 62.35 | 25.5 / 61.9 | 42.5 / 103.2 |
| A3 n200 | 15 | 2.76 | 3.41 | 4.1 | 6.9 |
| AR (strong) n100 / n200 (incl. XB) / n400 / n800 | 10 / 13 / 10 / 10 | 1.55 / 2.18 / 3.64 / 6.94 | 1.97 / 2.57 / 4.96 / 10.03 | 3.0 / 3.3 / 5.5 / 10.4 | 3.9 / 5.5 / 9.1 / 17.4 |
| ARweak n100 / n200 / n400 / n800 | 20 / 18 / 10 / 10 | 1.36 / 1.87 / 3.05 / 5.67 | 1.68 / 2.17 / 4.04 / 7.88 | 3.0 / 3.0 / 4.6 / 8.5 | 3.4 / 4.7 / 7.6 / 14.2 |
| IND n100 / n200 / n400 | 5 / 4 / 5 | 1.62 / 2.30 / 3.89 | 2.01 / 2.61 / 5.15 | 3.0 / 3.4 / 5.8 | 4.1 / 5.8 / 9.7 |
| BLK n100 / n200 / n400 | 5 / 5 / 5 | 1.58 / 2.22 / 3.72 | 2.19 / 2.99 / 5.44 | 3.0 / 3.3 / 5.6 | 4.0 / 5.6 / 9.3 |
| ADJ-OPP n200 / n400 | 3 / 5 | 2.69 / 4.62 | 3.14 / 6.23 | 4.0 / 6.9 | 6.7 / 11.6 |
| NULL n200 | 4 | 0.51 | 0.50 | 3.0 | 3.0 |
**Pilots re-set the quotes, not the hard line:** after A0, S6 and S8 the manager re-fits the n = 400, n = 800, R′ = 64, m = 4 and I_max = 0 class means from the measured fits (one line each in the read-back); the **soft line and the next-wave quote** move with them; the committed hard line does not. If a re-fitted wave quote is ≤ 1.5× the table's, the next wave self-releases; above that it is reported to HQ first.

**G-B cost criterion (HQ Q4, APPROVED with a guard):** for each class, the **class mean ≤ 1.5 × the committed class model AND no single fit > 2.5 × its committed model**; every per-fit exceedance of 1.5× is listed in the leg report. "Model" is always the committed table, never a re-fitted one.

## 6. Ops (task 5)
### 6.1 ONE build per arm for the whole leg (H-25 (2)); deploy log
The leg has **one arm: V-1M class A, ISA `sapphirerapids`** (the A3 fits are a runtime `partition` setting of the same binary). Build once from `git archive F` (the overlap's `deploy_wave.sh ... build` mechanism, on the login node, nice) **in batch `PL_A0_1`**; record `bin/smcbvs4` sha256, git_commit (= F, no `-dirty`), `island_isa`, libm self-test in **`staging/precision1e4/deploy_leg.log`** (one line per batch: UTC, batch, sha256, home MB, who). Every later batch gets that binary by **`cp -p` + sha256 check** (`COPYBIN` mode of the ops `deploy_wave.sh`, ≈ 15 lines, ops tool, not engine code; `presubmit_check.sh` refuses a batch whose `bin/smcbvs4.sha256` ≠ the leg's recorded sha). No rebuild in any wave; a mismatch is a stop (§5.3). **The 14 reused overlap V fits come from 4 builds of F** (R7; sha256 prefixes in §5.3), builds of F are not bit-reproducible by sha, and the leg's build will be a fifth: hence the **XB cross-build check in A0** (§6.4). *(The overlap rebuilt 4 times per arm: logged deviation F4 of the verdict.)*

### 6.2 Pre-launch ops tasks (Sonnet/Haiku, after the review; no engine change; each reviewed with this plan)
| id | task |
|---|---|
| O-1 | regenerate plans at F with `make_waves_prec.py` (tools from engine head b89cba4d; pin verified by `p1m_cells.py`), commit `plans/` shas in the deploy log |
| O-2 | `COPYBIN` in `deploy_wave.sh`, `leg_deploy.log`, `presubmit_check.sh` sha rule (§6.1) |
| O-3 | `stop_rules_prec.py` + `monitor_probe.sh` for batch ids `PL_*` (the overlap's regexp is `OV_<wave>_(T\|V)2?`), the committed class table, **arm identity from `calib_meta.json` plus the behaviour checks of §5.3** (R5), build identity with the 14 reused fits exempt by sha |
| O-4 | `collect_wave.sh` layout `records/precision1e4/<wave>/<run_id>/`; sha256 per unit as in the overlap; **`calib_meta.json` per fit = `smcbvs4 info calib.bin --meta 1` run on NOTS with the batch `env.sh` (R8)**; `setup.bin` kept for the A3 fits and their default pairs (R15) |
| O-5 | Haiku monitor prompt = `MONITOR_W0_PROMPT.md` with the stop table of §5.3 |
| O-6 | Opus check of the canary read-back checklist (below), including the XB bit comparison |
| O-7 | **F's records do not carry `I_used` and `grid_unconverged` in any collected JSON**: they are in `calib.bin` meta only (`calib.bin.json` has `settings`, `tier_final`, `cal_status`, seconds, not those; checked on the overlap records and on the F-equivalent binary: `info --meta 1` prints `I_used`, `I_max`, `refine_m`, `N`, `flags.grid_unconverged`). O-4's `calib_meta.json` is therefore **required**; until A0 shows it in a record, "`grid_unconverged` / `I_used` frequencies" (PREREG §5 C7) are a field not verified. The freeze rule needs only `N`, `refine_m`, `I_max`, which `calib.bin.json settings` also carries (fallback), so the rule is unaffected; `I_used` and `grid_unconverged` are **reported** per fit beside it |

### 6.3 Monitor, polling, read-back (the overlap's pattern)
Haiku monitor per wave: `monitor_probe.sh <wave>` = **one `ssh nots`, one `squeue` + one `sacct -X`**, ≤ 1 probe per 5 min (normally 20–30), no loops, no scans (POLICIES §12.7, NOTS_FACTS). Reports: every 3rd probe + each state change (≤ 3 lines), immediately on a stop (≤ 6 lines), end of wave (≤ 10 lines). **Read-back per wave (Sonnet):** collect (one rsync stream, nice), `sha256sum -c`, cost files from `p1m_cost.py`, a per-fit table (stage billed core-h, wall, RSS, T, N_final, refine_m, I_max), the stop-rule check, the re-fit of the class models, then self-release the next wave if clean. Home guard 7,900 MB (`home_guard`), jobs write only under `scratch/`. Polling and submission discipline: arrays ≤ 150 tasks, 2 batches per wave typical (≤ 8 `sbatch` calls per batch), waves released serially, one in flight (two only for S-waves whose monitor reports clean).

### 6.4 Canary A0 read-back checklist (what "clean" means for the self-release of P1…)
(1) **4/4 fits delivered**, all stages COMPLETED; (2) recorded arm (`calib_meta.json`: `refine_m 4`; `I_max 0`, `I_used 0`; `N 2500`; rule `bounded`) matches the plan, and the A3 `setup.bin.json` says `"partition": "exact"`; (3) **behaviour (R5):** the m = 4 fit has island T % 4 = 0 **and T ≥ 36**; the I_max = 0 fit has **no `cost/cost_diag_*` files**; an I_max = 3 fit (XB) has diag k = `I_used`; (4) X/y sha256 equal to the overlap rep-1 records (AR) and across the fits; (5) one binary sha256 = the leg's for the 4 new fits; (6) cost ≤ the wave stop and each fit ≤ its soft stop, else re-quote; (7) R′ = 64 merge: wall, RSS (< request 16 G) and time-limit headroom; A3 setup wall and RSS (sets the A3 setup limit for S3); (8) `fit.bin` readable, eval record has `evidence.logZ_r` of length 64 and `fit.meta.occ`; (9) **XB cross-build bit check (R7, ≈ 2.5 core-h):** `4-AR-n200-r01-V-XB-s1` (leg build) against the overlap record `4-AR-n200-r01-V-s1`: all 16 `evidence.logZ_r`, `selection.hpm` and every island `output_hash` (`island_*.bin.json`) **bit-equal**. If not: **STOP**, HQ + Theory (the 14 reused fits, the A3 pairs and the second-seed pairs would straddle builds); if equal, the build-identity exemption of §5.3 is justified.

### 6.5 Records and offload
Layout `records/precision1e4/<wave>/<run_id>/`. **Kept per fit:** `fit.bin`, `eval.bin` + `.json`, `calib.bin.json`, `setup.bin.json`, `island_*.bin.json`, `truth.json`, `run_manifest.json`, `cost/`, `log/`, `manifests/`, `SHA256SUMS`, **`calib_meta.json`** (R8; small) (≈ 25 MB per fit); `law.bin` (150 MB) **only for the 18 precision fits and the A3 fits** (the store-BMA law output of D-8; the science analysis uses the d_H values already in `eval.bin.json`); `setup.bin` is **kept for the 15 A3 fits and their 15 default pairs** (30 units, R15; a later π₀(S₀) reader then needs no re-run); `data.bin` and the other `*.bin` are rebuildable (data from its seed) and **not collected** (a change from the overlap's "keep data.bin"; veto if unwanted). Estimated 8–10 GB on Owls (home has 2.7 TB free). NOTS cleanup only after `crews/offload/desktop_verified.txt` lists the units (tombstone, target ≤ 24 h, hard 7 days). Offload verification is one line to HQ per wave, as in the overlap.

## 7. Timeline (task 6; today Thu 11-19; review R17: the first draft was ≈ 1 day optimistic)
| when | step |
|---|---|
| Thu 11-19 | plan + PREREG drafted, Opus review (ACCEPT-WITH-FIXES), fixes applied, HQ rulings bd02631e |
| Fri 11-20 | the manager commits plan + prereg + scripts with their sha256 (H-25 (3)); ops tools **O-1…O-5, O-7 are written the same day** (COPYBIN, `stop_rules_prec.py`, monitor regexp, collect layout, `calib_meta.json`: none exist yet); build once; **A0 canary submitted** (≈ 23 core-h, 1–2 h wall; self-release per HQ) |
| Fri–Sat 11-20/21 | A0 read-back (incl. XB) → P1–P4 (4 serial waves, ≈ 2–3 h each incl. queue) |
| Sun 11-22 | registered `precision_offset.py` + `precision_freeze.py` on the 18 fits; **FZ**: freeze proposal, one Opus check, CAMPAIGN_FREEZE addendum (N provisional 2,500, m, I_max, resampling off / not tested) |
| Mon–Tue 11-23/24 | science S1–S9: 9 serial waves, 2 pilot-gated (S6, S8 re-quote) |
| **Wed 11-25** | science read-back, leg report (≤ 12 lines) + one Opus review → **G-A closes**; offset surface reported. **If the freeze changes m or I_max:** S10 (+15 fits, ≈ ½ day) → report Wed night / Thu |
| Thu 11-26 (Thanksgiving) | **G-B pilot**: one 10⁵ fit in the frozen configuration (outside this quote; T5 measured 42 core-h at m = 1, I_max 3; ≈ 90–110 if m = 4); HQ G-B decision asynchronous (Q4 cost criterion, §5.3) |
| Fri 11-27 → 11-30 | **10⁵ rung** (H-14), if G-B passes; the slack to H-14's window is ≈ 1 day |
The window H-14 gave the leg (11-22..26) still holds; the overlap ending 11-19 only buys the slack.

## 8. Open items, follow-ups (out of scope here) and notes
**Follow-up legs and tasks (not in this leg's scope or quote):**
1. **V-N mini-leg (HQ Q1), before 1M.** A minimal engine diff on F (`V_N` → `calibrate --N`, V only, default 2500; `wp4_io.cpp:336` relaxed); default-N outputs **bit-identical to F on the overlap fixtures (`identical()` on all fields)**; one Opus diff review + Sol 6.2; a **new freeze tag**; **a cost quote to HQ before any run**. It then runs the 12 held N = 10⁴ fits (H1–H3, priced here at E ≈ 349, P90 403) under the same freeze rule (PREREG §3.2) and the offset measurement's N contrast, and unblocks the 1M N = 5,000 self-check (H-9) and the G-C2 doubling fit. The 10⁴ / 10⁵ freeze record says "N provisional, 2,500".
2. **Open item (HQ Q6): π₀(S₀) and claim C3 (B4)** are deferred. They are re-planned with the V-N mini-leg (a reader of `setup.bin`, or a diff in the same engine change). Until then A3 is reported on outcomes only; the `setup.bin` of the 30 A3-pair fits is kept (§6.5).
3. **Tools PR after the leg (R13):** `p1m_cells.py` still carries `grid_refine_m`, `calib_seed` and `exact_linkage`, adds no I_max arms, and the driver `--strict` does not validate keys inside `params` (how `grid_refine_m` slipped through). A small PR to fix the names, add the I_max arms and a per-stage `params` allowlist; a MANIFEST v0.5 note (names, I_max arms, B1 one seed per arm, A0 canaries). Not a launch blocker: the leg's plans come from `make_waves_prec.py`, which overrides the generated plans, so a regeneration from the unfixed generator would repeat the no-op and must not be used for this leg.
4. **Systematic resampling (HQ Q5):** off, reported "not tested"; D-14 is closed by default. An engine switch would be a new build (not folded into the V-N diff unless Theory asks).
**Notes for the FZ report and the verdict file (information):** the overlap T arm used the truncated partition in all 40 T setups (§1.2); the 1M budget depends on the m decision (§0-v2.5 "precise" ≈ m = 4); at 10⁴ the engine already meets the §0-v2.3 evidence and PIP targets in the one overlap V fit inspected (AR r01: σ̂ 0.025, island PIP max sd 0.0005, log Ẑ_occ sd 0.02; the read-back confirms it for all fits), so the freeze is efficiency-based (relative precision per core-h), not target-based; the offset measurement's power is stated in PREREG §4.5 (a 3-dataset cell cannot resolve −0.004; the realised half-width at df = 2 is itself very variable). The A3 canary and the exact-linkage setup limit (0:30) are guesses until A0. Cost basis: the manifest's 4,127 is ≈ 4–7× the measured-basis quote; no 25 % contingency is added (the quote is measured and the stops sit at 1.6 × E); add it if HQ wants it for the ledger.

## 9. Files and sha256
All under `results/precision1e4/`. Scripts are stdlib python3.9; `python3 -I` for the analysis scripts.
| file | sha256 |
|---|---|
| `precision_offset.py` (registered, PREREG §4; **R11: P2 span contrast + Jensen prediction added**) | `cbbc23012e6900ff7798267cc7325816ad0b8312ec6e26fd09972adc9780d300` |
| `precision_freeze.py` (registered, PREREG §3; **R1, R2 fixed**) | `7cdd69a11f3aaffa7a6615df639aefbe101042e9d37a8d520999ccbdc6279605` |
| `tests/test_precision_offset.py` (5 synthetic cases pass) | `0a9e39be7f0f96482ff7828a4903d277c54c7c4ec9159dddf08dffca2606cc19` |
| `tests/test_precision_freeze.py` (8 synthetic cases pass, incl. R1 and R2) | `3ef4b5b6b652b75459095d2bde036235c2aa976cc55eb0deed87f56a1afacabe` |
| `make_waves_prec.py` (R6, R7) | `3d9b4af6f819c3b7ab6eb6e93d7ca890586d1c815693840a634e619db4985983` |
| `quote_model.py` / `quote_output.txt` | `6cd8a978066618da3fe85de70a3d68891a185615d504d65409ba0e6ab9904cea` / `5fbaed69b972f28fd2bebae317063a6e2e7ff9a6aec0fd1073340b5a6beaf64e` |
| `extract_measured.py` / `measured_V_costs.csv` | `7fe311beaf11b20145683cd1ff1354170cd13a608b1060ba456c939cbc12108d` / `87f17c42681db075645682e8bca4a005640d20559b8ad10581192a0c04a0bee4` |
| `waves.json` / `make_waves_prec_output.txt` | `31cb8cf32d8f85b56e9e99e39bd474a3dd923f061b03cb624c1da5236455bdf3` / `af1f04dabe96c90fe4c5354ea597626af7a546048e562aa04af02eea5cebb792` |
| `waves_freeze_m4.json` / `waves_freeze_i0.json` | `a1af82ff990932dd16d75ee7178cf14858a320e2a2a67d00a5fe3b9c55be317d` / `2837a507b95713713d7b660fe605d94f9a3a3ae4c0a9c0d5b2fc4b15240f7964` |
| `quote_output_freeze_m4.txt` / `quote_output_freeze_i0.txt` | `98c5e38738b04b5abbdb4d7b9a893f3277757a8e75b630dbf2127e8b9f95e6af` / `63d8038f2dd3f2423a61a3bf5ce82e7cf81332337b7723f0ac967aad78fa8d93` |
| `feasibility_smoke.sh` / `feasibility_smoke_output.txt` | `cadbb2a28bde5d6e17e3aec36bc0fb6e7559d954e3b08e211e132b03c7eaabda` / `a36738a20c48ec27844b5f03959df5e4a997cdb3c39516b4bea2b188cf72baff` |
| `reader_check_output.txt` (the offset script's reader against the published −0.00394) | `ce09f01458abb65df0307651044febce8a7ca3845a81bcbdfd85ce6d57f7d6b4` |
`reviews/PLAN_REVIEW_OPUS.md` (the Opus plan review; not edited). The pre-fix draft of this file is kept in the scratch dir `20261119-precplan/LEG_PLAN.before_fixes.md`.
Plan tools, worktree and scratch: `~/SMC_Engineering_Department/tmp/20261119-precplan/` (worktree `wt_b89cba4d`, `gen/`, `mw/`, `smoke/`); nothing under `/tmp`, nothing on NOTS, nothing committed.
