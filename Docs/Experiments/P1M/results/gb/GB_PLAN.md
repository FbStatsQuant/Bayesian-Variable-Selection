# GB_PLAN: gate G-B, the 10⁵ pilot on F2, its I_max = 3 twin, the 1M rep-1 options, and what follows (Engineering, Sonnet plan writer; Thu 2026-11-19)

**Status: DRAFT; finalised after the V-N mini-leg verdict (H-33).** Nothing here is submitted, built, committed or run on NOTS. Every `N*` below is a placeholder that the mini-leg verdict fixes (`N* ∈ {2,500, 10⁴}`); every number is given for both. Companion: `GB_PREREG.md` (the pre-declared I_max rule for the pair, the registered criteria, operating characteristics, disclosures). The Engineering manager commits both with the sha256 of the registered scripts **before the pilot is submitted** (H-30, H-25 (3), the L-8 carry rule). Plan tools: `tools/` (`pair_ratios.py`, `gb_quote.py` + outputs). Scratch: `~/SMC_Engineering_Department/tmp/20261119-gbplan/`.

## Summary (≤ 10 lines)
1. **Pilot:** `5-AR-n200-r01-V-s1` (p = 10⁵, n = 200, AR-strong, data seed = engine seed 502020001: the T5 dataset and rung fit 1), F2 binary `da0cf85b…`, frozen config m = 1, **I_max = 0**, N = N*, R′ = 16. **E ≈ 30 core-h** (T5 measured 39.9 without the isa_check; I_max = 0 saves ≈ 9.5 of calibration).
2. **Twin:** same data, same engine seed, same build, **I_max = 3**. E ≈ 40 (HQ's ≈ 42 includes the 2.2 isa_check allowance). **Pair ≈ 70 core-h** (P90 ≈ 95); at N* = 10⁴ ≈ 230.
3. **Rule on the pair (pre-declared in `GB_PREREG.md` §2):** the registered rule of `precision_freeze.py` / PREREG §3.2 read literally: r_k = M_k(I_max 0) / M_k(I_max 3) ≤ 1.15 for each of M1, M2, M3, and the HPM identical. With one dataset the two bars collapse and **1.15 binds**. R′ = 16 (production), one seed per arm shared by both arms (no replicates, no R′ = 64).
4. **What one pair can decide (honest version):** a gross failure (HPM differs, M3 ratio ≫ 1.15, a grid-construction failure, a final E2). It **cannot** show non-inferiority within 15 %: measured on the 13 non-NULL same-seed 10⁴ pairs, the M3 ratio has sd(log) 0.12 (12/13 ≤ 1.15), so P(pass | true ratio 1.13) ≈ 0.56 and P(pass | true 1.30) ≈ 0.16. Same-seed M1 and M2 ratios were 1.000 ± 0.001 in 14/14 pairs at 10⁴, so those two metrics may not discriminate at all. **Recommended upgrade: one more dataset (ADJ-OPP r01; +≈ 49, the I_max = 3 twin only, because the I_max = 0 fit is a rung fit anyway)**: the rule then applies as registered (geometric mean ≤ 1.15, each ≤ 1.30). R′ = 64 is not recommended (+≈ 172 for one dataset).
5. **G-B (`§4`):** cost ≤ 1.5× the committed class model (31 / 40; a class of one fit, so the 2.5× guard is the STOP line); precision targets M1 ≤ 0.05, M2 ≤ 0.005, evidence within 3 s.e., HPM certified; peak RSS < request in every stage. Cost, precision and memory are judged on the fit of the **winning** configuration.
6. **1M rep 1 (§5):** manager's recommendation **(b) now** (cost 0), decide after the twin. The budget does not separate the options (every option ends at 12–15k of 28.3k at N* = 2,500). (a) costs ≈ 317 (not 440), because I_max = 0 saves ≈ 121 per 1M fit.
7. **Quotes (§6), N* = 2,500:** G-B pair 70; 10⁵ rung (11 more fits) 352; 1M block ≈ 8.8k. **Envelope position:** closed 2,450 (the 11-19 ledger total 2,041 already holds 55.09 of the 462.48 leg: do not add 462 again), + mini-leg 444 = 2,894, + pair → 2,964, + rung → 3,316, + 1M → ≈ 12.1k (≈ 14.3k with 25 % on the 1M block) of 28.3k.

## 1. Dependencies and placeholders (the mini-leg verdict supplies these)
| item | placeholder | supplied by |
|---|---|---|
| **N\*** | 2,500 or 10⁴ (default 2,500 = the D-1 value, "provisional") | the mini-leg's `precision_freeze.py` N rule (PREREG §3.2, c_X measured) and HQ's acceptance |
| committed class models (§4) | `E_I0`, `E_I3` for the chosen N* | §4 gives both columns; pinned in the commit |
| I_max of the mini-leg's N = 10⁴ arms | they were designed at I_max = 3 against baseline B (LEG_READBACK §8.4) | mini-leg PREREG; if N* = 10⁴ the frozen combination (N 10⁴, I_max 0) was **not run at 10⁴**, so the pair is its first test (stated in `GB_PREREG.md` §7) |
| the ADJ-OPP r04 attribution pair (≈ 3–4 core-h, H-33 (1)) | "folded into the next batch" = the mini-leg's batch | if it did not ride there, it rides in the G-B batch (+4, not a criterion) |
| mini-leg 1M consequence (H-33 (2)(b)) | which N is feasible at 1M | mini-leg PREREG; §6 here gives the capacity at N* = 10⁴ for context only |
| F2 identity | PASS (VN_ID_1, 1.99 core-h; `results/vn_minileg/F2_IDENTITY_CHECK.md`) | done; F2 = `p1m-freeze-F2` e993ece2, binary sha256 `da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a` |
Finalisation = replace `N*`, pin the class table, commit with shas, report once to HQ (the plan is then the launch document). **G-B works for either N\*** (the pair carries `N` in its params; cost scales on islands only, calibration H = 512 is N-independent).

## 2. The G-B pilot
### 2.1 Specification
| item | value |
|---|---|
| fit (pilot) | **`5-AR-n200-r01-V-s1`**: p = 10⁵, n = 200, AR-strong (s₀ = 5, a = 1), data seed **502020001** = R·10⁸ + D·10⁶ + (n/100)·10⁴ + rep with R 5, D 2, rep 1; engine seed 1 = the data seed (k = 0). The T5 dataset (T5 fit: HPM = MPM = S₀ = {10000, 30000, 50000, 70000, 90000}, log Ẑ −233.27, 42.18 core-h, pre-freeze code 04d8d2b5, I_max 3). It is **rung fit 1** of the 10⁵ AR n = 200 cell in MANIFEST_CELLS, so it is not an extra fit |
| config (frozen, H-30) | `refine_m 1`, **`I_max 0`**, `N N*`, R′ 16, bounded calibration (D-26), resampling off ("not tested"), π₀(S₀) deferred, class A, `island_isa sapphirerapids` (D-32) |
| engine | **F2** (H-31): one binary, `cp -p` + sha256 check (the leg's COPYBIN rule), never rebuilt; every sidecar's `binary.sha256` must equal it |
| explicit params | **`I_max`, `refine_m` and `N` written in every plan** (the generated 10⁵ plans from `p1m_cells.py` carry no `I_max`, so the engine default 3 would run silently, the C1 / C2 class of the precision leg's LEG_PLAN §1.1); a small `make_gb_plan.py` writes `GB_P1` (pilot) and `GB_P2` (twin), driver `--strict` clean |
| arm identity | recorded arm from `calib_meta.json` (`smcbvs4 info calib.bin --meta 1`: N, refine_m, I_max, I_used, rule) ≠ plan → STOP; behaviour: I_max 0 → no `cost/cost_diag_*` files; I_max 3 → diagnostic index = `I_used` |
| data identity | `truth.json` X / y sha256 equal across the pair; compared with T5's record if its NOTS run dir still exists (informational) |
| T5 cross-check (informational, free) | the twin (I_max 3, same data, same seed) may reproduce T5's island hashes (island 1 `0xc4fb97717604869d`) if T5's calibration used the same seed and the calibration code is unchanged; **untested** (the freeze check reproduced the island stage from T5's own inputs only). Equal = a 10⁵ cross-build identity for the whole I_max = 3 pipeline; unequal = not a failure |

### 2.2 Run sheet (stages, resources, limits; every task ≤ 2 h, **no exception needed**)
Basis: T5's shapes and measured times (setup 0:46, calibrate 9:54, islands 1:52–2:33, merge 2:47, eval 0:30); driver `DEFAULT_RES["1e5"]` memory except the merge (the 10⁶ merge peaked at 75 GiB against a plan of 43.7: no 10⁵ merge RSS exists, so it gets 24 G). Memory is not billed; the request being checked is the one the rung will use.
| stage | tasks | CPUs | mem req | limit (N* 2,500 / 10⁴) | expected wall | E core-h, pilot I_max 0 (twin I_max 3) |
|---|---|---|---|---|---|---|
| setup (gen + prep + setup) | 1 | 32 | 16 G | 0:30 | ≈ 1 min | 0.41 (0.41) |
| calibrate | 1 | 64 | 16 G | 0:30 (pilot) / 1:00 (twin) | pilot ≈ 1–2 min, twin ≈ 10–15 | **≈ 1.1** (10.56) |
| islands | 16 | 48 | 8 G | 0:20 / 0:45 | 2–2.5 min (N* 10⁴: 8–10) | 28.10 (28.10) |
| merge (+ tail, LS0) | 1 | 16 | 24 G | 0:30 | ≈ 3 min | 0.74 (0.74) |
| eval + post | 1 | 8 | 16 G | 0:45 | ≈ 0.5 min | 0.07 (0.07) |
| **fit total (N\* 2,500)** | 20 | | | | ≈ 20 min per fit | **30.4 (39.9)** |
| N\* 10⁴ (islands × 3.85, ONE Owls datum) | | | | | | **110 (120)** |
- **Worst case** (limit sum, the admission figure): ≈ 318 (pilot) + 350 (twin) = **≈ 670 core-h**; this is not an estimate. Island arrays throttled to `%8` per fit so the pair peaks at 768 CPUs (QOS cap 1,536).
- **I_max = 0 calibration cost** is the pilot island plus grid construction (at 10⁶ the P7 pilot island was 14.96 core-h against 135.63 for the I_max = 3 calibration): the 1.1 here is 0.10 × T5's calibration, measured at 10⁴ only (a guess at 10⁵; the soft stop absorbs 1–3).
- **Optional +2.2:** the D-32 isa_check (not run by default; the freeze check already reproduced a 10⁵ island on F).
- **Batches and pacing:** two batches (`GB_P1` pilot, `GB_P2` twin), 20 tasks each (≤ 150), ≥ 5 min apart; the twin is submitted after the pilot's setup and calibrate are clean and inside 2× their E (so a pilot identity or cost failure does not spend the twin).
- **Ops:** deploy = `cp -p` + sha256 (`presubmit_check.sh` refuses a mismatch); home guard 7,900 MB; jobs write only under `scratch/`; pre-announce one ledger row (quote 70, worst ≈ 670, stop 140).

### 2.3 Stops (the monitor evaluates; any one → stop submitting, tell the manager)
| rule | threshold |
|---|---|
| per-fit soft (report-and-continue, H-26 Q3) | > 1.5 × class E: pilot 46.5, twin 60 (N* 10⁴: 165 / 180) |
| per-fit hard (**STOP**, pinned, never re-fitted) | > 2.5 × class E: pilot 77.5, twin 100 (N* 10⁴: 275 / 300) |
| wave / cumulative | wave > 2 × quote = 140; cumulative 150 (covers one infrastructure rerun) |
| failures | any FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (a rerun of the stage is the manager's call; an OOM is also a G-B memory finding, §4) |
| arm / data / build identity | as §2.1 |
| admission | engine `resource_limit` / `OUTCOME` record |
| informational | any task > 80 % of its limit; pilot island wall outside 72–124 s (T5) |
Monitor: the overlap's Haiku pattern (one `ssh nots`, one `squeue` + one `sacct -X`, ≤ 1 probe per 5 min, `START` line, `WAVE STATE: ENDED` stop).

### 2.4 Read-back
Sonnet worker: collect (one rsync stream, nice) → `sha256sum -c` → cost files from `p1m_cost.py` → the **registered** `gb_imax_rule.py` and `gb_readback.py` (§2.5) → one table per fit (stage billed core-h, wall, MaxRSS against request, T, I_used, flags) → the §4 criteria → ≤ 10 lines to HQ. Then **one Opus child** re-derives M1–M3, the ratios and the decision from the raw eval records (H-20 (3): the twin verdict is a deep-judgment item). **Items the read-back must carry** (LEG_READBACK §8.5): calibration E1 / E2 reported **NOT EVALUATED** at I_max = 0 (never 0 %), `grid_unconverged` / `I_used` as constants outside any quality aggregate, and instead the final-merge E1–E3, `low_empirical_ESS`, `checks_passed_final`, sd(log Ẑ_r) > 1 (the E2 analogue), `occ_inhomogeneous`; M3 = sd(log Ẑ_r) (the PREREG erratum). Records: `records/gb/<run_id>/` with `fit.bin`, `eval.bin(.json)`, `calib.bin.json`, **`calib_meta.json`**, `setup.bin.json`, `island_*.bin.json`, `truth.json`, `run_manifest.json`, `cost/`, `log/`, `SHA256SUMS`, and `law.bin` + `data.bin` for both fits (so a pair cross-Hellinger stays possible: L-12); offload per the tombstone rule.
### 2.5 Scripts registered BEFORE submission (not just before the first read)
`gb_imax_rule.py` (the §2 rule of `GB_PREREG.md`; `fit_metrics` copied verbatim from the registered `precision_freeze.py` 7cdd69a1…, which cannot be run on 10⁵ ids because its run-id regex is the precision leg's, and which has the `cost_batch.json` glob defect, L-4: the new script reads eval records only) and `gb_readback.py` (tables, criteria). stdlib, `python3 -I`, deterministic, synthetic self-tests (PASS, FAIL, NOT_EVALUATED, n = 1 and n = 2 forms, HPM mismatch, zero denominator). **sha256: to be recorded at finalisation.**

## 3. The I_max = 3 twin and the pre-declared rule (full text: `GB_PREREG.md` §2–§3)
- **Twin:** `5-AR-n200-r01-VI3-s1`, same data seed and engine seed, same F2 binary, `I_max 3`, R′ 16; E ≈ 40 (approved ≈ 42). One seed per arm (H-30 "same dataset and seed"); **no second seed**: the rule's unit is the dataset (PREREG §4.5), so a second seed on the same dataset is not an independent unit.
- **Rule (literal):** r_k = M_k(I0) / M_k(I3), k = 1, 2, 3 (M1 = `fit.meta.occ[M = 1000].sd_log_Z_occ_r`, M2 = `pip.island_spread.max_sd`, M3 = `evidence.sigma_hat` = sd(log Ẑ_r)); **PASS iff all three r_k ≤ 1.15 and `selection.hpm` is identical in the two fits**; otherwise FAIL. With one dataset the geometric mean over datasets is the ratio itself, so the per-dataset 1.30 clause can never bind: **1.15 binds**.
- **What one pair can and cannot decide:**

| | statement | basis |
|---|---|---|
| can | a gross failure: HPM differs; r3 well above 1.15; r1 or r2 diverging; a grid-construction failure (`grid_fallback`) at I_max 0; a final E2 | one paired draw |
| scope | nothing about 10⁵ is assumed from 10⁴: the pair is the first measurement at 10⁵ | FZ addendum §3 |
| cannot | non-inferiority within 15 % | M3 pair-ratio sd(log) 0.123 on 13 non-NULL same-seed 10⁴ pairs: P(pass \| true ratio) = 0.87 at 1.00, **0.56 at 1.13** (the 10⁴ R′ = 64 estimate), 0.16 at 1.30, 0.02 at 1.50 |
| cannot | a false FAIL is unlikely but real: 1 of 13 non-NULL 10⁴ pairs (AR r04 s2, r3 = 1.37) would have failed although I_max = 0 was adopted on that population | `tools/pair_ratios_output.txt` |
| cannot | detect an I_max effect on M1 and M2 if the arms stay identical on a same-seed pair (ratios 1.000 ± 0.001 in 14/14 at 10⁴; cause not examined) | same |
| cannot | design dependence: AR-strong is the easiest design; ADJ-OPP had the one σ̂ outlier at I_max = 0 (r04 s1, no I_max = 3 twin) | LEG_REVIEW_OPUS §4 |
- **Does the pilot need R′ = 64 or replicates?** *R′ = 64: no.* The rule is applied at the production R′ = 16 (what the 1M fits use; G-B's targets are R′ = 16 targets); R′ = 64 shrinks the island-sd noise but costs **+≈ 86 per fit (+≈ 172 for the pair)** and needs the driver to extend the fit's islands 17–64 from the same calibration (**not verified**); a fresh R′ = 64 fit repeats islands 1–16. *Replicates: more datasets, not more seeds.* Priced (N* = 2,500, E):

| design | extra over the approved pair | rule form | why / why not |
|---|---|---|---|
| **A. one pair, AR r01, R′ 16 (approved, H-30)** | 0 (pair 70) | literal, 1.15 binds | the baseline; coarse (above) |
| **B. + ADJ-OPP r01 pair, R′ 16 (recommended)** | **+49** (twin only: I_max 3 ≈ 49; its I_max 0 fit ≈ 37 is rung fit 1 of the ADJ-OPP cell) | **as registered**: geometric mean ≤ 1.15 **and** each ≤ 1.30, HPM identical in both; n = 2 datasets × 1 replicate | the registered rule's two bars then do different work; covers the design with the 10⁴ tail flag; simulated P(pass): 0.93 / 0.55 / 0.07 / 0.00 at true ratio 1.00 / 1.13 / 1.30 / 1.50 (sd 0.123, assumption) |
| C. A + a second seed (s2) on AR r01 | +70 | not a new unit | rejected: one dataset |
| D. A at R′ = 64 | +172 | literal | rejected: +172 for one dataset; M1 / M2 uninformative |
| E. B at R′ = 64 | +≈ 430 | as B | not recommended |
HQ approved only design A (H-30); B is **the plan's request for HQ's decision at the commit** (0.2 % of the envelope). The rule text is pre-declared for both forms, so either choice is fixed before anything runs.
- **Decision table (H-30; full wording `GB_PREREG.md` §4):**

| outcome | 10⁵ rung and 1M | the 10⁴ science | the pair's fits |
|---|---|---|---|
| **PASS** | I_max = 0 (frozen) | stands | the pilot is rung fit 1 (AR r01); the twin is reported |
| **FAIL** | **I_max = 3** | stands as run (I_max 0), **reported per configuration** | **the twin is rung fit 1** (so its cost is not wasted); the pilot is reported; cost and memory criteria move to the twin |
| NOT EVALUATED (a field missing, zero denominator) or INCOMPLETE (a fit undelivered after one rerun, an identity failure) | no default: to HQ with the priced options | stands | rerun or hold |
FAIL costs ≈ 9.5 per 10⁵ fit and ≈ 121 per 1M fit (≈ 2.5k over 20 replicates, ≈ 9 % of the envelope): affordable, which is why a coarse test with a conservative FAIL is acceptable. No post-hoc override either way (H-30, the FZ precedent).

## 4. G-B criteria: exact pass conditions and what a miss does
Evaluated on the **winning configuration's fit** (the pilot if the rule PASSES, the twin if it FAILS); both fits are reported. All thresholds are registered in `GB_PREREG.md` §5 and written into `gb_readback.py` before the pilot is submitted.
| # | criterion | pass condition | on a miss |
|---|---|---|---|
| **C1** | **cost** ≤ 1.5× model (H-26 Q4) | fit billed core-h ≤ 1.5 × the committed class model: **pilot 46.5** (E 31), twin 60 (E 40); N* 10⁴: 165 / 180. A class of one fit, so "class mean" is the fit and the **2.5× guard is the STOP line** (77.5 / 100; 275 / 300). Also listed beside it, not a criterion: the ratio to the manifest planning value (96) | 1.5×–2.5×: **not a stop; G-B cost FAIL**: per-stage comparison with T5 (which stage), the 10⁵ rung and the 1M block **re-quoted from the measured fit**, HQ releases the rung only if the re-quoted total still fits 28.3k. > 2.5×: STOP, HQ re-pins the table |
| **C2** | **precision targets met** (ENGINEERING_SPEC §0-v2.3, at R′ = 16) | all of: **M1 ≤ 0.05**; **M2 ≤ 0.005** (engine `target_met` True); **\|log Ẑ − log Ẑ_occ(M = 1,000)\| ≤ 3 √(se_Z² + se_occ²)** (PREREG §3.1); **merged HPM certified by the final local search** (`local_certified`); PIP agreement max_j \|PIP_eq − PIP_𝒯\| ≤ 0.01 + (1 − π̂(𝒯)) **if the field exists at F2 (not verified)**. **Reported, not gating:** M3 ≤ 0.5 (goal), `occ_inhomogeneous`, E1–E3, sd(log Ẑ_r) > 1 | **G-B precision FAIL; the rung is not auto-released.** Report to HQ with priced options: (i) accept and report as a miss (§0-v2.3 "reported per fit; never used to switch estimators"; the 10⁴ n = 100 misses are the precedent); (ii) more islands for the rung (R′ = 32 ≈ +28 per fit, ≈ +340 for 12 fits; D-6 set R′ = 16, so HQ's call); (iii) hold. **Never an estimator switch.** The "same best model in 16 of 16 islands" target is not computable (no per-island HPM in the records, PREREG §3.1) |
| **C3** | **memory < request** | MaxRSS (sacct) and the O2 `peak_rss` **< the stage's request in all 5 stages** (setup 16 G, calibrate 16 G, islands 8 G, merge 24 G, eval 16 G). Advisory flag at > 80 %. Also recorded: peak RSS < 50 % of a node (EXPERIMENT_PLAN G-B), trivially true at ≈ 4.5 GB per island (T5) | a stage ≥ its request or OOM: **G-B memory FAIL, not a halt**: re-size that request to 1.3 × the measured peak, rerun that stage only (cost ≤ that stage), re-evaluate; recorded as "PASS after resize"; the rung uses the re-sized requests |
| **C4** | **completion** | both fits delivered (status and fit_status completed, `evidence.logZ_r` of length 16 and finite, `fit.bin` section hashes verified), one build sha256 = F2's, arm identity verified | one infrastructure rerun per fit; then INCOMPLETE to HQ |
| **C5** | **E2 recorded** (EXPERIMENT_PLAN G-B, input to OD-2) | reported as in §2.4 (the final-merge flags and sd(log Ẑ_r) > 1; the calibration E1 / E2 as NOT EVALUATED at I_max 0) | n/a (recording) |
| **C6** | **I_max rule evaluated** | one of PASS / FAIL / NOT EVALUATED / INCOMPLETE recorded with M1–M3, r_k, HPM and the form (n = 1 or 2) | per §3 table |
**G-B passes iff C1–C4 pass (after any resize) and C6 is PASS or FAIL.** Pass → HQ releases the rung in the winning configuration. Science check, not a criterion: the pilot's HPM should equal S₀ (T5 did); a different HPM is flagged to HQ as a science finding (C2 of the study is the rung's job).

## 5. 1M rep 1: options for HQ's ruling (at G-B, after the twin is read)
**What rep 1 is:** `6-AR-n200-r01-V-s1`, 437.44 core-h MEASURED (setup 15.25, calibrate 135.63 with **3 rebuilds**, islands 269.25, merge 16.91, eval 0.40), HPM = MPM = S₀, code 2cfaa9e5 (**pre-F2**), N 2,500, I_max 3. Under I_max = 0 it is not in the frozen configuration.
| option | what | cost now |
|---|---|---|
| **(a)** re-run rep 1 frozen | same data and seed, F2, I_max 0, N*; the fit becomes replicate 1; it is also the **same-seed I_max 0 partner of the pre-F2 I_max 3 pilot at 1M** (the only 1M I_max pair) once an F2-vs-2cfaa9e5 identity statement at 1M is made | **≈ 317** (437.44 − 135.63 + P7's pilot island 14.96 = 316.8; P90 ≈ 360), **not 440**: I_max = 0 saves ≈ 121 per 1M fit. At N* 10⁴: ≈ 1,084 |
| **(b)** report rep 1 as a separate configuration | pilot evidence ("I_max 3, pre-F2, one seed"); replicates 2–20 are frozen; the self-check moves to a frozen replicate's data | **0** |
| (c) a 21st replicate (fresh data) | rep 1 stays separate, 20 frozen replicates | ≈ 317 (1,084) |
**Manager's recommendation: (b) now; decide among (a), (c) and "accept 19" after the 10⁵ twin is read** (the Opus review endorses this with two corrections). Reasoning: I_max = 0 at p ≫ 10⁴ is untested (the coded rule's grid kept changing for 13–15 rebuilds at p ≥ 5k), so (a) may spend ≈ 317 on a configuration the twin rejects; if the twin FAILS, 1M runs at I_max = 3 and rep 1 is already in-configuration for I_max. **Caveats (stated, not softened):**
1. Rep 1 is one fit, one seed, **pre-F2** (H-31 makes F2 the 1M engine) and has **no same-seed I_max 0 partner**: it is not "exactly the I_max 3 arm" of a 1M I_max comparison. It becomes one only with an F2 identity statement at 1M (one island on F2 from rep 1's retained `calib.bin` / `setup.bin`, ≈ 17 + 15 if they are retained, **retention not verified**; otherwise the identity needs a re-run) **and** a paired I_max 0 fit.
2. HQ approved **20** AR-strong replicates (H-14): under (b) **19** are frozen unless a 21st is run.
3. **MANIFEST_CELLS §1 pilot rule (Sol F7):** "the pilot is replicate 1 only if the frozen configuration is unchanged after it; otherwise it is kept as pilot evidence and a fresh replicate 1 is run". If the twin PASSES the configuration did change, so **(b) departs from the registered pilot rule and needs HQ's explicit ruling**; (a) and (c) follow it.
4. The 1M N = 5,000 self-check was planned on rep 1's data (H-9 L4). Under (b) it moves to a frozen replicate's data (no extra fit; its partner is a planned replicate). Under (a) it stays on rep 1's data and can reuse the N-independent calibration (H = 512).

**Decision by twin outcome (the plan's suggestion):** twin PASS → (a) if HQ wants the 1M I_max pair and 20 on-rule replicates (≈ 317, 1.1 % of the envelope), else (b) with 19; twin FAIL → keep rep 1 under (b) (in-configuration for I_max) after the F2 identity statement, a re-run would cost 437.
**Budget table against the 28.3k envelope** (N* = 2,500; position after the mini-leg + pair + rung = 3,316; unit costs measured as in §6; competitors and ablations ≈ 475; option D ≈ 1,087; self-check ≈ 586):
| option | 1M block (I_max 0) | envelope position after everything | with 25 % contingency on the 1M block | share of 28.3k |
|---|---|---|---|---|
| (b) 19 frozen reps | 8,799 | **12,116** | 14,315 | 43 % / 51 % |
| (a) re-run, 20 reps | 9,116 | 12,432 | 14,711 | 44 % / 52 % |
| (c) 21st rep, 20 reps | 9,116 | 12,432 | 14,711 | 44 % / 52 % |
| if the twin FAILS (I_max 3, unit 437): keep rep 1 (b′) | 12,009 | 15,400 (rung +114) | 18,400 | 54 % / 65 % |
| if N* = 10⁴ (unit 1,084; self-check and D re-scoped by the mini-leg) | the position before 1M is ≈ 4.4k, leaving **≈ 23.9k = 22 fits at 1,084 with no reserve, ≈ 17 with a 25 % reserve** | | | the 20-replicate plan does not fit; the mini-leg plan (H-33 (2)(b)) states what runs |
**The budget does not separate (a), (b) and (c) at N\* = 2,500** (differences of 317 = 1.1 %); the science and the pilot rule do. At N* = 10⁴ (a) costs ≈ 1,084 and (b) is the realistic choice.

## 6. After G-B: the 10⁵ rung and the 1M start (gate-paced; dates are earliest-feasible, not commitments; the owner works daily, no calendar padding)
**Measured bases:** T5 10⁵ fit 42.18 (39.9 without isa_check); 1M rep 1 437.44; P7 pilot island 14.96; N* = 10⁴ islands × 3.85 (ONE Owls same-machine datum). Costs below are E (P90 in brackets) at **N\* 2,500, I_max 0** unless stated; `tools/gb_quote_output.txt` reproduces them.
| step | content | E (P90) core-h | N* 10⁴ | position after (E) |
|---|---|---|---|---|
| closed to date | ledger 2,041.0 (11-19 08:45; holds 55.09 of the leg) − 55.09 + 462.48 (precision + science leg, 194 fits) + 1.99 (F2 identity) | **2,450** | | 2,450 |
| V-N mini-leg | 12 N = 10⁴ fits ≈ 440 (P90 510, cap 600) + ADJ-OPP r04 check ≈ 4 | 444 (514) | same | **2,894** |
| **G-B pair** | pilot 30.4 + twin 39.9 (design A); + ADJ-OPP twin 49 (design B) | **70 (95)**; B: 119 | 230 | **2,964** (B: 3,013) |
| 10⁵ rung | 12 fits: AR n200 ×5 (rep 1 = the pilot), AR n400 ×3, IND n200 ×2, ADJ-OPP n200 ×2; remaining 11 | **352 (540)**; 12 fits 382 (568); at I_max 3 **+114** | 1,279 (≈ 1,950) | **3,316** |
| T6′ (optional) | the forced-kill restart (G-C) re-run on F2: one island, T6 cost 3.23 | 3.2 | 3.2 | |
| 1M start | 2 fits at a time, each batch pre-announced; per fit **317 (360)** at I_max 0, 437 at I_max 3; ≈ 2.2 h wall per fit, 4–6 fits per day | block 8.8k | | **≈ 12.1k** (14.3k) |
- **Rung detail.** Data seeds (R·10⁸ + D·10⁶ + (n/100)·10⁴ + rep): AR n200 `502020001…05`, AR n400 `502040001…03`, IND n200 `501020001…02`, ADJ-OPP n200 `505020001…02`; run ids `5-<design>-n<n>-r<rep>-V-s1`; one seed per fit (the second seed is not in the rung). Unit costs: AR n200 30.4; AR n400 1.0× (10⁴ measured 0.77×; the planning model 1.6× is the P90); IND 1.05×, ADJ-OPP 1.23× (the committed 10⁴ class table's ratios). The plan figure was 1,325: the measured basis is ≈ 29 % of it. n-scaling at 10⁵ is **not measured**; the rung's first batch (AR n400 ×1) re-quotes the rest, as S6 / S8 did.
- **Option D gate (H-1, conditional on the π̂(S₀) trend):** the registered form is not in the sources I read, so **a proposal to pre-declare in the rung plan, not a decision**: D (AR-strong n = 1,000, ≈ 1,087 at N* 2,500) is released iff the mean π̂(S₀) over the AR datasets is non-decreasing from n = 200 (5 fits) to n = 400 (3 fits), and P̂(HPM = S₀) at n = 200 is ≥ 4/5. OWNER_SHEET's guess (π(S₀) ≈ 0.3–0.45 at n = 200, 0.45–0.6 at n = 500) is the "expected" band; π̂(S₀) at F2 needs the store law's mass on S₀ (D-8 `law.bin`, **field not verified**; π₀(S₀) is a different, deferred quantity).
- **G-C-type conditions before the replicates (H-14):** 10⁵ ≥ 90 % complete (≥ 11 of 12), restart tested at 10⁵ (T6 PASS on 96137399, pre-freeze; T6′ optional), configuration and evaluator frozen by hash (the FZ addendum + this plan's commit), competitors frozen; kill rule 2× model at 50 % progress (the 1M model = 317 / 437).
- **1M quotes at N\* = 10⁴:** per fit ≈ 1,084 (I_max 3: 1,205); the islands run ≈ 35–53 min at 96 CPUs (< 2 h; no exception).
- **Gate-paced order:** mini-leg → verdict → finalise + commit this plan → pilot pair (≈ 2 h wall) → read-back + Opus check → HQ G-B → rung (≈ 12 fits, ≈ 1 day wall, 2 at a time under the CPU cap) → rung read-back + option D gate → 1M replicates (from ≈ 12-01 in H-14; earlier if the gates clear).

## 7. Open items and things not verified (to settle at finalisation)
1. The mini-leg verdict (N*), its class table, and whether the ADJ-OPP r04 attribution pair rode with it.
2. `make_gb_plan.py`, `gb_imax_rule.py`, `gb_readback.py` and their self-tests do not exist yet (registered before submission).
3. The F2 flag for calibrate `--N` and the manifest `I_max` for the 10⁵ plan: checked by a driver dry run (`--strict`), not by me.
4. Whether the driver can extend a fit's islands from R′ 16 to 64 on the same calibration (only design D / E need it).
5. Eval field names at F2 for the PIP_𝒯 agreement check and `local_certified` at 10⁵; the field for π̂(S₀).
6. 10⁵ merge, setup and eval RSS have no measurement (T5 reports islands and calibration only): the requests above are guesses; this pilot measures them.
7. The I_max = 0 calibration cost at 10⁵ (0.10× is a 10⁴ figure); the 10⁵ n-scaling; the retention of T5's and rep 1's run dirs on NOTS scratch (the T5 cross-check, the F2 identity at 1M).
8. The 10⁴ twin statistics rest on 14 pairs, the same-seed pairs of the precision leg (R′ 16, p 10⁴, n 200); disclosed in `GB_PREREG.md` §6.
9. The ledger arithmetic: the brief's "≈ 2,041 closed + 462 leg" double-counts 55.09 (the leg's A0 and P1 are already in the 2,041).

## 8. Files
`results/gb/GB_PLAN.md`, `results/gb/GB_PREREG.md`, `results/gb/tools/` (`pair_ratios.py` sha256 `16d96ed5b10cb894…`, `gb_quote.py` `cb8a019e758f9d7f…`, and their outputs `pair_ratios_output.txt`, `gb_quote_output.txt`). Nothing committed; nothing on NOTS; nothing under `/tmp`; no BNP file touched.
