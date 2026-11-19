# LEG_PLAN: precision study (Sol F6) + 10⁴ science: plan, cost quote, waves, ops (Engineering, Sonnet plan writer; Thu 2026-11-19)

**DRAFT, pending one Opus plan review (H-25).** Nothing is deployed, submitted or committed. Companion: `PREREG.md` (criteria, the pre-declared offset measurement, scripts + sha256).

## Summary (≤ 10 lines)
1. **Frozen binary F (eefcbc4a) can do: m ∈ {1, 4}, I_max ∈ {0, 3}, BLK(20, 0.5), n = 100/400/800, AR-weak. It cannot do N = 10⁴ in V mode (B2: `V_N` is a constant), systematic resampling (B3), or a calibration seed different from the final seed (B1).** Two plan names are also wrong and would have been silent or fatal: `grid_refine_m` (ignored: m = 4 would have run as m = 1) and `partition = exact_linkage` (refused; the engine says `exact`). All verified on an F-equivalent binary (§1).
2. **Scope released now:** 18 precision fits (R′ = 64: m ∈ {1, 4} × 2 replicates × 3 datasets = 12, plus **6 new I_max = 0 arms**) + the 156 science fits (14 overlap V fits reused, none re-run). **Held (B2): the 12 N = 10⁴ fits.** Science runs **after** the precision freeze, in the frozen configuration (§3).
3. **Offset measurement:** one pre-declared surface δ(N, m, I_max, k) = V − T log Ẑ; R′ (k = 4, 8, 16, 32, 64) comes free from disjoint island blocks of existing and new records; reader validated: reproduces −0.00394 (CI −0.0071…−0.0008). No pass/fail (PREREG §4).
4. **Quote (MEASURED basis): E = 591 core-h released scope (P90 673); 940 with the held arms (P90 1,064), against the plan figure 4,127 → self-release YES** (even m = 4 frozen: E 951, P99 1,252). The manifest's 35 / 141 core-h per precision fit were 3–8× too high (modelled from measurements: 6.3 for m = 1, 12.4 for m = 4 at N = 2,500, R′ = 64; 17 for m = 1 at N = 10⁴).
5. **Stops:** per fit 1.5 × class model (soft: report-and-continue up to 2.5×, hard beyond; §5.3), per wave 2 × quote, cumulative 1,000 (scope in release), projection ceiling 4,127; arm-identity and data-identity stops added.
6. **Waves:** A0 canary (3 fits), P1–P4 (precision), FZ (freeze checkpoint), S1–S9 (science), H1–H3 held; ≤ 4 batches and ≤ 150 tasks per batch; **ONE build of the V arm for the whole leg** (H-25).
7. **Timeline:** review + HQ rulings + canary Fri 11-20; precision done Sat 11-21; freeze Sun 11-22; science Sun–Mon; leg report Tue 11-24 (two days inside H-14's 11-22..26) → G-B pilot → 10⁵ from Fri 11-27.
8. **Needs from HQ before launch:** rulings on B1 (single seed per arm), B2 (hold N = 10⁴, or authorise one engine change + new freeze check), B3 (resampling stays off, untested).

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
| **B1** | an independent calibration seed (k = 20 + a) next to the final seed (k = 10 + a) | **one seed per arm = the final seed (k = 10 + a)**; the unused k = 20 + a stays reserved. Calibration (PILOT/DIAG roles) and final islands are different Philox domains of one seed (`include/v4/rng.h`; `tests/test_rng.cpp:146`: all addresses unique over pilot, diagnostic and final roles), and every arm and replicate has its own seed, so arms and replicates are mutually independent | Sol F6 asked for "independent calibration and final seeds". What is lost: the ability to hold the grid fixed and vary the final seed (not needed by any criterion). Replicate independence is unaffected | HQ: manifest v0.5 note |
| **B2** | V at N = 10⁴ (12 precision fits; later the 1M N = 5,000 self-check) | **(a) hold the 12 fits (H1–H3, priced, never submitted) and freeze N = 2,500 (D-1 default), N = 10⁴ recorded as NOT RUN**; or **(b)** an engine change: make `V_N` a `calibrate --N` (V only, default 2500), record it in calib meta, relax `wp4_io.cpp:336` to `N ≥ 1`; same bits at 2500 by construction, but it is **a new binary F′** → HQ ruling against H-25 "no new engine builds", a repeat of the freeze reproduction check (T3 hashes, goldens, one 10⁵ island hash) and a new deploy of the V arm | Without N = 10⁴ the leg cannot say whether doubling-doubling N helps; the V − T offset vs N is then read only from T's own N (10⁴ tier 0, 4 × 10⁴ tier 1: 3 escalated fits) | HQ ruling (a) or (b) |
| **B3** | systematic resampling | **not tested; frozen OFF = the D-14 default** ("off unless the study shows a gain"). The study can neither show nor exclude a gain | D-14's question stays open; flag for Theory/HQ. An engine switch is a new build | HQ note |
| **B4** | π₀(S₀), start-mass lattice (C3; the A3 "π₀(S₀)" comparison) | report A3 on outcomes (HPM = S₀, PIP, log Ẑ, d_H) only; π₀ would need a setup.bin reader (separate tool or build) and the science fits' `setup.bin` kept | claim C3 deferred | HQ note |

**I_max and resampling (the manifest's OPEN item), resolved.** I_max = 0 **cannot be read off** the existing arms: it differs in the grid the final islands run on, so it needs final islands on the preliminary grid. It gets **6 arms** (a = 8, 9; N = 2,500, m = 1, 2 replicates × 3 datasets), seeds data_seed + 1800 / 1900, measured cost ≈ 5.8 core-h per fit = **35 core-h in all** (the manifest estimated 106). Resampling: B3.

**Observation (not a blocker).** The overlap's T arm ran with `partition truncated` (`setup.bin.json` of `4-AR-n200-r01-T-s1.T2`: `"partition": "truncated"`; ENGINEERING_SPEC §0-v2.1 says T uses exact complete linkage; law mode defaults to truncated: `include/v4/setup.h:73`, exact only for compat `src/setup/setup_run.cpp:213`). The T-vs-V comparison was therefore truncated-vs-truncated; the A3 pairs in this leg are the only exact-linkage fits. One line for the paper and the verdict file.

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
| (2,500, m 1, I_max 3) (baseline kept) | as quoted | yes | 442 | **591 (1,000)** |
| m = 4 adopted | `refine_m 4` on all science fits, +14 re-runs (tag `VF`) | no | 800 | 951 (1,600) |
| I_max = 0 adopted | `I_max 0`, +14 re-runs | no | 351 | 500 (800) |
(`make_waves_prec.py --frozen-m / --frozen-I`; `quote_output_freeze_m4.txt`, `quote_output_freeze_i0.txt`.) All three are far inside the plan figure. **If both m = 4 and I_max = 0 are adopted** the combination was not run in the study (PREREG §3.2): S1 is then released as a one-batch pilot (7 fits) and re-quoted before the rest.

## 4. Waves (≤ 150 array tasks per batch; ≤ 4 batches per wave; every task ≤ 2 h)
Plans: `make_waves_prec.py` (output `make_waves_prec_output.txt`, `waves.json`): driver `--strict` clean, no warnings, 186 fits in 17 waves. Quote per wave from `quote_model.py` (`quote_output.txt`). "Worst" = limit sum (the ledger/admission figure, not a cost estimate). Island arrays are throttled (`%32` precision, `%8` science) so a wave's peak stays < 1,000 CPUs (QOS cap 1,536).
| wave | content | fits | batches / tasks | **E** (P90) | **QUOTE** → wave stop (> 2×) | worst (limit sum) | release |
|---|---|---|---|---|---|---|---|
| **A0** | canary: AR m4-c1 + AR I0-c1 (R′ 64) + A3 canary `4-AR-n200-r01-A3-exactlink-s1` | 3 | 2 / 156 | 20.6 (24.2) | **20 → 40** | 327 | after HQ rulings + review |
| P1 | AR: m1 c1, c2; m4 c2; I0 c2 | 4 | 2 / 272 | 30.2 (35.1) | 30 → 60 | 557 | self-release after A0 read-back clean |
| P2 | ARweak: m1 c1, c2; m4 c1, c2 | 4 | 2 / 272 | 28.1 (32.3) | 30 → 60 | 557 | self |
| P3 | ARweak I0 c1, c2; ADJ-OPP m1 c1, c2 | 4 | 2 / 272 | 24.5 (28.2) | 25 → 50 | 557 | self |
| P4 | ADJ-OPP m4 c1, c2; I0 c1, c2 | 4 | 2 / 272 | 45.8 (54.0) | 45 → 90 | 557 | self |
| **FZ** | freeze checkpoint (no jobs) | – | – | – | – | – | Opus check + HQ informed |
| S1 | science n = 200: AR-strong 12 + AR-weak 13 + ADJ-OPP 3 | 28 | 4 / 560 | 58.4 (64.9) | 60 → 120 | 1,307 | after FZ |
| S2 | n = 200: AR-weak 5, BLK 5, IND 4, NULL 4 | 18 | 3 / 360 | 31.6 (35.5) | 30 → 60 | 840 | self |
| S3 | A3 (14 remaining: AR 9, BLK 5; setup limit 0:30 from the canary) | 14 | 2 / 280 | 38.6 (43.2) | 40 → 80 | 681 | self |
| S4 | n = 100: AR-strong 10 + AR-weak 18 | 28 | 4 / 560 | 39.9 (48.2) | 40 → 80 | 1,307 | self |
| S5 | n = 100: AR-weak 2, BLK 5, IND 5 | 12 | 2 / 240 | 18.7 (23.0) | 20 → 40 | 560 | self |
| **S6** | **n = 400 pilot**: ADJ-OPP 5, AR-strong 2 | 7 | 1 / 140 | 30.4 (39.2) | 30 → 60 | 467 | self; **re-quote n = 400 from it** |
| S7 | n = 400 rest: AR-strong 8, AR-weak 10, BLK 5, IND 5 | 28 | 4 / 560 | 97.7 (124.1) | 100 → 200 | 1,867 | self if the re-quote ≤ 1.5× this quote, else HQ-informed |
| **S8** | **n = 800 pilot**: AR-strong 7 | 7 | 1 / 140 | 48.6 (66.3) | 50 → 100 | 611 | self; **re-quote n = 800** |
| S9 | n = 800 rest: AR-strong 3, AR-weak 10 | 13 | 2 / 260 | 77.6 (104.5) | 80 → 160 | 1,135 | self (same rule) |
| H1–H3 | **HELD (B2)**: N = 10⁴: AR, ARweak, ADJ-OPP × (m 1, 4) × (c1, c2) | 12 | 2 / 272 each | 115 / 81 / 153 (137 / 96 / 184) | 115 / 80 / 155 → 230 / 160 / 310 | 557 each | **only after HQ rules on B2** (islands limit 0:30 → 1:00 for m = 4 at N = 10⁴, from A0/P2 timings) |
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
| precision released (A0 prec + P1–P4) | 18 (+1 A3 canary) | 149 | 148 | 168 | 188 | 7% of 2,117 |
| science (S1–S9) | 156 | 442 | 437 | 512 | 585 | 22% of 2,010 |
| **released scope** | 174 | **591** | 586 | **673** | 753 | **14%** |
| held N = 10⁴ (H1–H3) | 12 | 350 | 346 | 405 | 467 | – |
| **leg with held arms** | 186 | **940** | 935 | **1,064** | 1,184 | **23%** |
P(total > 4,127) = 0.0000 in every scenario (m = 4 frozen: E 951 / P99 1,252; with the held arms 1,300 / 1,672). **Self-release: YES** (H-25 (3): the quote is within CAMPAIGN_PLAN_1117's figure for this leg). Per-fit E by class: `quote_output.txt`. What is NOT in these numbers: ablations, competitors, the G-B pilot, analysis compute.

### 5.3 Stops (the monitor evaluates; any one → stop submitting and tell the manager at once)
| rule | threshold |
|---|---|
| **per-fit (soft)** | one fit's billed core-h > **1.5 × its class model** (table below; floor 3.0 core-h). **Pre-declared as report-and-continue** (as ADDENDUM_2 did for T), *provided* the fit completed valid, cost ≤ 2.5 × model, and no wave/cumulative stop is hit; the class model is re-fitted from it. Reason: the class models carry unmeasured scaling (n, m, R′); the model says **3.7 soft trips are expected over the 186 fits** (mostly one shared n-level or m = 4 error, not independent failures) |
| **per-fit (hard)** | > **2.5 × class model** (floor 3.0), or 3 soft trips in one wave: STOP (expected 0.02 hard trips). *If the reviewer prefers the literal "1.5× = hard stop", the same table applies with the soft column as the stop; the cost is ≈ 3–4 halts.* |
| **wave** | wave actual (all its batches, billed) > **2 × the wave quote** (table §4) |
| **cumulative** | leg actual > **1.6 × E of the scope in release, rounded up to 100: baseline 1,000** (m = 4 frozen 1,600; I_max = 0 frozen 800; with H waves released: 1,600 / 2,100 / 1,400) |
| **projection ceiling** | spent + (class means × fits left) > **4,127** (the plan figure) → HQ before any further wave |
| failures | any FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (NODE_FAIL / BOOT_FAIL = INFO; one rerun per fit, manager's call); > 2 failed fits in a wave |
| admission / queue | engine `resource_limit` / `OUTCOME` record; pending reason QOS / Assoc / MaxSubmit / Invalid / Limit |
| **arm identity (new)** | `calib.bin.json settings` (`refine_m`, `I_max`, `N_final`, `rule`) ≠ the plan's arm → STOP (the silent no-op class, §1) |
| **data identity** | `truth.json` X/y sha256 equal across all fits of a dataset **and equal to the overlap records** for the shared datasets (precision, A3 pairs, reused fits) |
| build identity | every fit's `binary.sha256` = the leg's single build (§6.1) |
Per-fit class models (E per fit from `quote_output.txt`; soft stop = max(3, 1.5E); hard = max(3, 2.5E)):
| class | fits | E | P90 | soft | hard |
|---|---|---|---|---|---|
| prec N2500 m1 I3 / m1 I0 / m4 I3 | 6 / 6 / 6 | 6.28 / 5.77 / 12.39 | 8.13 / 7.43 / 17.97 | 9.4 / 8.6 / 18.6 | 15.7 / 14.4 / 31.0 |
| prec N10⁴ m1 / m4 (held) | 6 / 6 | 17.02 / 41.33 | 23.6 / 62.2 | 25.5 / 62.0 | 42.5 / 103.3 |
| A3 n200 | 15 | 2.76 | 3.41 | 4.1 | 6.9 |
| AR n100 / n200 / n400 / n800 | 10 / 12 / 10 / 10 | 1.54 / 2.18 / 3.63 / 6.96 | 1.96 / 2.59 / 4.93 / 10.0 | 3.0 / 3.3 / 5.4 / 10.4 | 3.9 / 5.5 / 9.1 / 17.4 |
| ARweak n100 / n200 / n400 / n800 | 20 / 18 / 10 / 10 | 1.36 / 1.87 / 3.05 / 5.71 | 1.67 / 2.18 / 4.03 / 7.92 | 3.0 / 3.0 / 4.6 / 8.6 | 3.4 / 4.7 / 7.6 / 14.3 |
| IND n100 / n200 / n400 | 5 / 4 / 5 | 1.61 / 2.29 / 3.88 | 2.01 / 2.61 / 5.13 | 3.0 / 3.4 / 5.8 | 4.0 / 5.7 / 9.7 |
| BLK n100 / n200 / n400 | 5 / 5 / 5 | 1.58 / 2.21 / 3.71 | 2.19 / 2.97 / 5.40 | 3.0 / 3.3 / 5.6 | 4.0 / 5.5 / 9.3 |
| ADJ-OPP n200 / n400 | 3 / 5 | 2.68 / 4.61 | 3.14 / 6.20 | 4.0 / 6.9 | 6.7 / 11.5 |
| NULL n200 | 4 | 0.51 | 0.50 | 3.0 | 3.0 |
**Pilots re-set the classes:** after S6 and S8, and after A0, the manager re-fits the n = 400, n = 800, R′ = 64, m = 4 and I_max = 0 class models from the measured fits (one line each in the read-back); if a re-fitted wave quote is ≤ 1.5× the table's, the next wave self-releases; above that it is reported to HQ first.

## 6. Ops (task 5)
### 6.1 ONE build per arm for the whole leg (H-25 (2)); deploy log
The leg has **one arm: V-1M class A, ISA `sapphirerapids`** (the A3 fits are a runtime `partition` setting of the same binary). Build once from `git archive F` (the overlap's `deploy_wave.sh ... build` mechanism, on the login node, nice) **in batch `PL_A0_1`**; record `bin/smcbvs4` sha256, git_commit (= F, no `-dirty`), `island_isa`, libm self-test in **`staging/precision1e4/deploy_leg.log`** (one line per batch: UTC, batch, sha256, home MB, who). Every later batch gets that binary by **`cp -p` + sha256 check** (`COPYBIN` mode of the ops `deploy_wave.sh`, ≈ 15 lines, ops tool, not engine code; `presubmit_check.sh` refuses a batch whose `bin/smcbvs4.sha256` ≠ the leg's recorded sha). No rebuild in any wave; a mismatch is a stop (§5.3). *(The overlap rebuilt 4 times per arm: logged deviation F4 of the verdict.)*

### 6.2 Pre-launch ops tasks (Sonnet/Haiku, after the review; no engine change; each reviewed with this plan)
| id | task |
|---|---|
| O-1 | regenerate plans at F with `make_waves_prec.py` (tools from engine head b89cba4d; pin verified by `p1m_cells.py`), commit `plans/` shas in the deploy log |
| O-2 | `COPYBIN` in `deploy_wave.sh`, `leg_deploy.log`, `presubmit_check.sh` sha rule (§6.1) |
| O-3 | `stop_rules_prec.py` + `monitor_probe.sh` for batch ids `PL_*` (the overlap's regexp is `OV_<wave>_(T\|V)2?`), class table, arm identity (reads `calib.bin.json` through the collected manifests/run dirs) |
| O-4 | `collect_wave.sh` layout `records/precision1e4/<wave>/<run_id>/`; sha256 per unit as in the overlap |
| O-5 | Haiku monitor prompt = `MONITOR_W0_PROMPT.md` with the stop table of §5.3 |
| O-6 | Opus check of the canary read-back checklist (below) |

### 6.3 Monitor, polling, read-back (the overlap's pattern)
Haiku monitor per wave: `monitor_probe.sh <wave>` = **one `ssh nots`, one `squeue` + one `sacct -X`**, ≤ 1 probe per 5 min (normally 20–30), no loops, no scans (POLICIES §12.7, NOTS_FACTS). Reports: every 3rd probe + each state change (≤ 3 lines), immediately on a stop (≤ 6 lines), end of wave (≤ 10 lines). **Read-back per wave (Sonnet):** collect (one rsync stream, nice), `sha256sum -c`, cost files from `p1m_cost.py`, a per-fit table (stage billed core-h, wall, RSS, T, N_final, refine_m, I_max), the stop-rule check, the re-fit of the class models, then self-release the next wave if clean. Home guard 7,900 MB (`home_guard`), jobs write only under `scratch/`. Polling and submission discipline: arrays ≤ 150 tasks, 2 batches per wave typical (≤ 8 `sbatch` calls per batch), waves released serially, one in flight (two only for S-waves whose monitor reports clean).

### 6.4 Canary A0 read-back checklist (what "clean" means for the self-release of P1…)
(1) 3/3 fits delivered, all stages COMPLETED; (2) `calib.bin.json settings` match the plan (`refine_m 4`; `I_max 0`; `N_final 2500`; rule `bounded`) and the A3 `setup.bin.json` says `"partition": "exact"`; (3) island T of the m = 4 fit is a multiple of 4; (4) X/y sha256 equal to the overlap rep-1 records (AR) and across the three fits; (5) one binary sha256 = the leg's; (6) cost ≤ the wave stop and each fit ≤ its soft stop, else re-quote; (7) R′ = 64 merge: wall, RSS (< request 16 G) and time limit headroom; A3 setup wall and RSS (sets the A3 setup limit for S3); (8) `fit.bin` readable, eval record has `evidence.logZ_r` of length 64 and `fit.meta.occ`.

### 6.5 Records and offload
Layout `records/precision1e4/<wave>/<run_id>/`. **Kept per fit:** `fit.bin`, `eval.bin` + `.json`, `calib.bin.json`, `setup.bin.json`, `island_*.bin.json`, `truth.json`, `run_manifest.json`, `cost/`, `log/`, `manifests/`, `SHA256SUMS` (≈ 25 MB per fit); `law.bin` (150 MB) **only for the 18 precision fits and the A3 fits** (the store-BMA law output of D-8; the science analysis uses the d_H values already in `eval.bin.json`); `data.bin` and the other `*.bin` are rebuildable (data from its seed) and **not collected** (a change from the overlap's "keep data.bin"; veto if unwanted). Estimated 8–10 GB on Owls (home has 2.7 TB free). NOTS cleanup only after `crews/offload/desktop_verified.txt` lists the units (tombstone, target ≤ 24 h, hard 7 days). Offload verification is one line to HQ per wave, as in the overlap.

## 7. Timeline (task 6; today Thu 11-19)
| when | step |
|---|---|
| Thu 11-19 | this plan + PREREG drafted |
| Fri 11-20 | **one Opus plan review** → fixes; HQ rulings B1/B2/B3; commit plan + prereg + scripts with their sha256 (H-25 (3)); O-1…O-5; build once; **A0 canary submitted** (≈ 20 core-h, 1–2 h wall) |
| Fri–Sat 11-20/21 | A0 read-back → P1–P4 (4 serial waves, ≈ 2–3 h each incl. queue) |
| Sun 11-22 | registered `precision_offset.py` + `precision_freeze.py` on the 18 fits; **FZ**: freeze proposal, one Opus check, CAMPAIGN_FREEZE addendum (N, m, I_max, resampling) |
| Sun–Mon 11-22/23 | science S1–S9 (pilots S6, S8 re-quote; ≈ 4 waves/day) |
| Tue 11-24 | science read-back, leg report (≤ 12 lines) + one Opus review → **G-A closes**; offset surface reported |
| Wed 11-25 | **G-B pilot**: one 10⁵ fit in the frozen configuration (outside this quote; T5 measured 42 core-h at m = 1, I_max 3; ≈ 90–110 if m = 4) |
| Thu 11-26 (Thanksgiving) | HQ G-B decision (asynchronous) |
| Fri 11-27 → 11-30 | **10⁵ rung** (H-14) |
H-14 had the leg in 11-22..26: this plan finishes it by 11-24 because the overlap ended 11-19. **If B2(b) is chosen:** engine change, new build, repeated freeze check and the H waves add ≥ 1 day and ≈ 350 core-h; the 10⁵ date still holds.

## 8. Points for the Opus reviewer / open items
1. B1: is "one seed per arm" acceptable against Sol F6's "independent calibration and final seeds"? (My argument: Philox domains differ, arms and replicates have distinct seeds.)
2. B2: (a) hold vs (b) engine change. My recommendation: (a) now; the doubling question is needed for the 1M self-check, so **decide (b) before the 1M leg**, not for this leg.
3. The per-fit stop as report-and-continue (§5.3) is a departure from the literal "1.5× = stop"; confirm or revert.
4. The freeze rule (PREREG §3) uses "gain must beat spending the same extra cost on islands" and treats the §0-v2.3 targets as reported; check the thresholds (the limit 1/√c_X is ≈ 0.66 for m = 4 and 0.5 for N = 10⁴ from the cost ratios, measured at FZ; 1.15 / 1.30 for I_max).
5. In the one overlap V fit I inspected (AR r01) the engine already meets the §0-v2.3 evidence and PIP targets (σ̂ 0.025, island PIP max sd 0.0005, log Ẑ_occ sd 0.02; the read-back must confirm it for all fits): the precision study can only freeze on *relative* precision per core-h, not on target misses. Say so in the report.
6. Power of the offset measurement (PREREG §4.5): 3 datasets cannot resolve −0.004 (t(2) half-width ≈ 0.008); the R′ slope on the 10 overlap datasets can. A third replicate of T is not in this leg.
7. A3 canary and exact-linkage setup limit (0:30) are guesses until A0.
8. Cost basis note: the manifest's 4,127 is ≈ 5–7× the measured-basis quote; a 25% contingency (the campaign's rule) is not added here because the quote is measured and the stops sit at 1.6× E; add it if the reviewer wants it for the ledger.

## 9. Files and sha256
All under `results/precision1e4/`. Scripts are stdlib python3.9; `python3 -I` for the analysis scripts.
| file | sha256 |
|---|---|
| `precision_offset.py` (registered, PREREG §4) | `df221026011d0b6b538c65b3dbe5328e9350077e1d417becedacfcb65073c10d` |
| `precision_freeze.py` (registered, PREREG §3) | `f2e0b230c67fc6a7bce286238ab645052b9242bee769b732b857cdff45c301bb` |
| `tests/test_precision_offset.py` (4 synthetic cases pass) | `42155aba770fd960f40964dfb6084203bc85b137eae8ed5d16f4557d702184a6` |
| `tests/test_precision_freeze.py` (3 synthetic cases pass) | `6b0037ed7002ebf19071e23bc4d54a0b3e25a7223dc912b6aed453aaa5545abc` |
| `make_waves_prec.py` | `fa23d264ccabfa9b91fe36c5230ab9ef5817c3085456d14cc7d043e26a499d69` |
| `quote_model.py` / `quote_output.txt` | `ec609671885d215c9a882ec8ee384dee4e14488d80a0fd30b4ddfabbcee6dc8d` / `9cc7e48d4041b1b4c1e65fb639ddddd34abc46f37104d847a688a4a7e30b7295` |
| `extract_measured.py` / `measured_V_costs.csv` | `7fe311beaf11b20145683cd1ff1354170cd13a608b1060ba456c939cbc12108d` / `87f17c42681db075645682e8bca4a005640d20559b8ad10581192a0c04a0bee4` |
| `waves.json` / `make_waves_prec_output.txt` | `a27394a53cbfc07027dc6e74e7f01a39d120914efe84277559c4b4f9a9bec627` / `a34dd69c9bf90077ed4b178357c7a93307c85e568f1f3f8d3fc9674fdfa14543` |
| `waves_freeze_m4.json` / `waves_freeze_i0.json`; `quote_output_freeze_m4.txt` / `_i0.txt` | `141c684a…` / `19c1992f…`; `192a0da2…` / `eb7a8e32…` |
| `feasibility_smoke.sh` / `feasibility_smoke_output.txt` | `cadbb2a28bde5d6e17e3aec36bc0fb6e7559d954e3b08e211e132b03c7eaabda` / `a36738a20c48ec27844b5f03959df5e4a997cdb3c39516b4bea2b188cf72baff` |
| `reader_check_output.txt` (the offset script's reader against the published −0.00394) | `a335df40290ecdd02370054c192f266b4d88053db57595c0db6199d498645a3c` |
Plan tools, worktree and scratch: `~/SMC_Engineering_Department/tmp/20261119-precplan/` (worktree `wt_b89cba4d`, `gen/`, `mw/`, `smoke/`); nothing under `/tmp`, nothing on NOTS, nothing committed.
