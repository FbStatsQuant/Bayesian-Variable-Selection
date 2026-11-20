# GB_PLAN: gate G-B, the 10⁵ pilot set on F2 at N* = 10⁴, the I_max rule on two pairs, continuity twins, the 10⁵ rung, option D, 1M rep 1 (Engineering, Sonnet plan writer; Fri 2026-11-20)

**Status: FINAL; COMMITTED by the Engineering manager 2026-11-20 before any G-B run (HQ H-38, H-39)** (supersedes the 11-19 draft; HQ H-38 and H-39 applied; the G-B set is released at ≈ 501 after the dry run + commit). Nothing here is submitted or run on NOTS. Companion: `GB_PREREG.md` (the pre-declared I_max rule, the registered criteria, operating characteristics, disclosures). The manager commits both with the sha256 of the registered scripts **before the pilot set is submitted**; then the G-B pilot set self-releases (H-38). Plan tools: `tools/`. Scratch: `~/SMC_Engineering_Department/tmp/20261120-gbfinal/`.

## Summary (≤ 12 lines)
1. **Pilot set (4 fits, 2 pairs, all F2 `da0cf85b…`, explicit `N 10000 / refine_m 1 / I_max` in every plan):** AR r01 `5-AR-n200-r01-V-s1` (I_max 0, data seed 502020001) + its I_max 3 twin `…-VI3-s1`; ADJ-OPP r01 `5-ADJOPP-n200-r01-V-s1` (data seed 505020001) + `…-VI3-s1`. Same data, same seed, same build within a pair. R′ 16.
2. **Quotes at N 10⁴ (f = 3.768 measured, T5 = 42 at N 2,500):** AR pair 108 + 118 = **226**; ADJ-OPP pair 133 + 142 = **275**; **set ≈ 501** (P90 ≈ 650). Note: HQ's "+49" was the ADJ-OPP twin at N 2,500 (46.5); at N 10⁴ it is **≈ 142**. Two waves: G1 (AR pair) then G2 (ADJ-OPP pair), ≤ 150 tasks per batch, every task ≤ 2 h.
3. **Rule (`GB_PREREG.md` §2):** the registered I_max rule (`precision_freeze.py` 7cdd69a1…, PREREG §3.2) on the 2 pairs, scored by **`gb_imax_rule.py`, sha256 `76927ae2faadc095e9353050eae3ef626ad439d88b92a7bf7cb9f313dab91012`** (a three-change copy: the registered scripts cannot ingest 10⁵ ids or one replicate per arm; golden test = the registered output on the leg's real FZ records, 7/7 tests pass). PASS iff geometric mean of the two datasets' ratios ≤ 1.15 on each of M1, M2, M3, each dataset ≤ 1.30, HPM identical.
4. **What 2 pairs can decide:** gross failure and structural change, not non-inferiority within 15 %: P(pass) ≈ 0.93 if truly equivalent, 0.55 at 1.13, 0.07 at 1.30 (M3 pair-ratio sd 0.123 measured at N 2,500; unknown at N 10⁴). On the 10⁴ records at N 10⁴ the same rule gives PASS (1.043 / 1.027 / 0.948).
5. **Consequences (pre-declared):** PASS → rung and 1M at I_max 0 (N 10⁴ rung; the pilots are rung fits 1 of AR and ADJ-OPP). **FAIL → I_max 3 AND N 2,500** (the mini-leg's I_max-3 verdict is KEEP, MINILEG_PREREG §3.3), rung 12 fits at (N 2,500, I_max 3) ≈ 495, the continuity twins are dropped, the 10⁴ science stands reported per configuration.
6. **G-B criteria (§4):** cost ≤ 1.5× the committed class model (H-26 Q4 guard), precision targets M1 ≤ 0.05 / M2 ≤ 0.005 / evidence / HPM certified, peak RSS < request; judged on the winning configuration's fit (on FAIL, on a confirmation fit of the rung).
7. **Rung (§6), waits for the I_max verdict:** PASS: 12 fits at N 10⁴ ≈ **1,360** (P90 ≈ 1.9k), 10 remaining after the pilots ≈ 1,119; **continuity twins** (2 fits, N 2,500, same data and seeds as AR r01 and ADJ-OPP r01) ≈ **67**, run with the rung.
8. **Option D gate (§6):** proposed wording: HPM = S₀ at the 10⁵ premise (≥ 4/5 at n 200, 3/3 at n 400) **and** mean π̂(S₀) at n 400 ≥ at n 200, with the continuity twins' N effect on π̂(S₀) reported; HQ rules at G-B.
9. **1M rep 1 (§5):** manager recommends (b); at S2 + H-34 (a) and (b) cost the same (the 20-seed block's seed 1 **is** the frozen re-run of rep 1), and the N 10⁴ 1M fit wants that same-seed N 2,500 partner.
10. **Envelope (§6), from closed 2,686.91 (VN_ID_1 counted once):** + G-B set 501 + rung/continuity 1,186 → 4,374; + 1M S2 → **≈ 14.2k (b) / 14.5k (a)**, 16.7k / 17.1k with 25 % on the unspent 1M items, **+ H-34 20 seeds → 20.6k (24.6k with reserve)** of 28.3k. FAIL branch: 16.1k; with H-34 at I_max 3 it does **not** fit with the reserve (24.9k without, 30.4k with).

**HQ notes (H-39), part of the registered text:**
1. **The two pairs detect only a GROSS I_max failure (P(pass) 0.93 / 0.55 / 0.07 at true ratio 1.00 / 1.13 / 1.30); HQ noted the low power.**
2. **The FAIL consequence (rung + 1M at I_max 3 AND N 2,500) is accepted by HQ as pre-declared. If FAIL makes the conditional 20 seeds (H-34) bust the 25 % reserve, the seeds give way, decided then** (§5: FAIL + H-34 at I_max 3 is 24.9k without and 30.4k with the reserve).
3. **Option D: HQ rules on the D1–D3 wording at G-B** (§6); the wording below is a proposal, not a decision.

## 1. Fixed by the mini-leg and HQ (no placeholders left)
| item | value |
|---|---|
| **N\*** | **10⁴** at the frozen configuration (m 1, I_max 0): ADOPT by the pre-declared rule, margin on M2 0.0019 (c_X 3.7496, f billed 3.768). The I_max-3 arm said **KEEP** (M3 0.572 > bar 0.514): a FINDING, no veto (MINILEG_PREREG §3.3); no override (H-38) |
| S2 (H-38) | 10⁵ rung at N 10⁴; 1M replicates at N 2,500 + ONE N 10⁴ 1M fit on the rep-1 data; the conditional 20 seeds (H-34) at N 2,500 |
| engine | F2 = `p1m-freeze-F2` e993ece226b355058e26400f05f9faad6daf16ca, binary sha256 `da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a`; default-N identity PASS (VN_ID_1) and **XB2 bit-identical** at R′ 64, I_max 0 (the pooled baselines are valid) |
| mini-leg arms | both I_max arms **were** run at N 10⁴ (6 + 6 fits); (N 10⁴, I_max 0) has 10⁴ evidence. The draft's statement that it "was not run at 10⁴" is withdrawn |
| closed | **2,686.91** = 975.5 + 1,010.43 + 462.48 + 1.99 + 236.51 (the 2,041 ledger total already held 55.09 of the leg; VN_ID_1 is inside 2,450.40: no double count). Remaining 25,613 |
| r04 | the oddity repeats at I_max 3 and at seed 2: a property of that dataset, not of I_max or the seed; **ADJ-OPP r01 is a different dataset and is not expected to reproduce it** |
| gates before any N 10⁴ run above 10⁴ (pre-declared by the mini-leg) | the `--plan-only` memory plan at 10⁵ for N 10⁴ (0 core-h) before the pilot; at 10⁶ before the 1M N 10⁴ fit; one 10⁵ N 10⁴ fit before any 1M fit (this set) |

## 2. The G-B pilot set
### 2.1 Fits (all F2, R′ 16, `refine_m 1`, `N 10000`, bounded calibration, class A, `island_isa sapphirerapids`, resampling off "not tested", π₀(S₀) deferred)
| fit | run id | data seed = engine seed | I_max | role |
|---|---|---|---|---|
| (a) pilot AR | `5-AR-n200-r01-V-s1` | 502020001 (R·10⁸ + D·10⁶ + (n/100)·10⁴ + rep; the T5 dataset) | **0** | frozen configuration; rung fit AR r01 on PASS |
| (b) twin AR | `5-AR-n200-r01-VI3-s1` | 502020001 | **3** | the registered rule's comparison arm |
| (c1) pilot ADJ-OPP | `5-ADJOPP-n200-r01-V-s1` | **505020001** (MANIFEST §1: D 5; the rung's ADJ-OPP rep 1) | 0 | rung fit ADJ-OPP r01 on PASS |
| (c2) twin ADJ-OPP | `5-ADJOPP-n200-r01-VI3-s1` | 505020001 | 3 | comparison arm |
- **Explicit params:** `N`, `refine_m` and `I_max` written in every fit of every plan. The generated 10⁵ plans (`p1m_cells.py`) carry no `I_max` (engine default 3, silently) and no N: `make_gb_plan.py` (to write; sha recorded) emits `GB_G1.json` and `GB_G2.json`, driver `--strict` clean, **dry run before submit**.
- **Identity:** recorded arm from `calib_meta.json` (N, refine_m, I_max, I_used, rule) ≠ plan → STOP; behaviour: I_max 0 → no `cost/cost_diag_*` files, I_max 3 → diag k = `I_used`; `truth.json` X / y equal inside each pair; one binary sha256 = F2's in every sidecar. **Calibration is N-independent (H = 512)**: the pilot's grid equals what N 2,500 would build at the same seed (the mini-leg's pairing identity).
- **Build:** **one build, F2**: `cp -p` + sha256 (COPYBIN) from the recorded F2 build; never rebuilt; `presubmit_check.sh` refuses a mismatch.
- **T5 cross-check (informational, free):** the AR twin is at N 10⁴, so it cannot reproduce T5's islands (N 2,500). The continuity twin (§3) at I_max 3 could; not planned.
### 2.2 Run sheet (every task ≤ 2 h; **no exception needed**)
Shapes from T5; islands wall from T5 (2–2.5 min at N 2,500) × the mini-leg's wall factor 3.9 (≈ 8–10 min; **one ADJ-OPP island task at 10⁴ took 7.2× its twin's wall**, so the ADJ-OPP limit is wider). Memory not billed; the checked request is the one the rung will use.
| stage | tasks | CPUs | mem req | limit AR / ADJ-OPP | expected wall | E core-h pilot (I_max 0) / twin (I_max 3) |
|---|---|---|---|---|---|---|
| setup | 1 | 32 | 16 G | 0:30 | ≈ 1 min | 0.41 / 0.41 |
| calibrate | 1 | 64 | 16 G | 0:30 pilot, 1:00 twin | pilot ≈ 1–2, twin ≈ 10–15 min | ≈ 1.1 / 10.56 |
| islands | 16 | 48 | **12 G** | 0:45 / 1:00 | 8–10 min | **105.9** / 105.9 (28.10 × 3.768) |
| merge (+ tail, LS0) | 1 | 16 | 24 G | 0:30 | ≈ 3 min | 0.8 / 0.8 |
| eval + post | 1 | 8 | 16 G | 0:45 | ≈ 0.5 min | 0.07 / 0.07 |
| **AR fit** | 20 tasks | | | | ≈ 30 min | **108.2 / 117.7** |
| **ADJ-OPP fit** (islands × 1.23, the committed 10⁴ class ratio) | 20 | | | | ≈ 35 min | **133.0 / 142.5** |
- **Worst case** (limit sum; the admission figure, not an estimate; **driver dry run, §2.6**): AR pilot 638.0, AR twin 670.0, ADJ-OPP pilot 830.0, ADJ-OPP twin 862.0: **wave G1 1,308, G2 1,692, set 3,000** (the ADJ-OPP islands limit is 1:00). Island arrays `%8` per fit, so a wave peaks at 768 CPUs (QOS cap 1,536).
- **Waves: two** (cumulative stop covers both). **G1** = batches `GB_G1a` (pilot AR) and `GB_G1b` (twin AR): 20 tasks each, ≥ 5 min apart; the twin is submitted after the pilot's setup and calibrate are clean and inside 2× their E. **G2** = `GB_G2a` / `GB_G2b` (ADJ-OPP), released after G1's read-back is clean (so a hard trip does not spend a second pair). One build, one binary.
- **Wall:** ≈ 1–2 h per wave plus queue; read-back after each wave.
### 2.3 Committed class table and stops (E per fit from `tools/gb_quote_output.txt`; soft = 1.5E, hard = 2.5E; the hard line is never re-fitted)
| class | fits | E | soft (report-and-continue) | **hard (STOP)** |
|---|---|---|---|---|
| 10⁵ AR n200 N 10⁴ I_max 0 | 1 | 108 | 162 | **270** |
| 10⁵ AR n200 N 10⁴ I_max 3 | 1 | 118 | 177 | **295** |
| 10⁵ ADJ-OPP n200 N 10⁴ I_max 0 | 1 | 133 | 200 | **333** |
| 10⁵ ADJ-OPP n200 N 10⁴ I_max 3 | 1 | 142 | 213 | **355** |
| continuity twins, N 2,500 I_max 0: AR / ADJ-OPP (§3) | 1 / 1 | 30 / 37 | 45 / 56 | **75 / 93** |
| rung classes (§6) | | set at the verdict from these | | pinned in the rung addendum |
Wave stop: wave actual > 2 × its quote (**G1 450, G2 550**); cumulative **800** (1.6 × 501, rounded). Failures: any FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (an OOM is also a C3 finding); arm, data and build identity as §2.1; admission (`resource_limit`). Informational: a task > 80 % of its limit; pilot island wall outside 4 × (72–124 s). Monitor: the Haiku pattern (one `ssh nots`, one `squeue` + one `sacct -X`, ≤ 1 probe per 5 min, `START` line, `WAVE STATE: ENDED`).
### 2.4 Read-back and records
Sonnet worker: collect → `sha256sum -c` → cost files (`p1m_cost.py`) → the registered `gb_imax_rule.py` and `gb_readback.py` → one table per fit (stage billed, wall, MaxRSS vs request, T, I_used, flags) → §4 criteria → ≤ 10 lines to HQ; then **one Opus child** re-derives M1–M3, ratios and the decision from the raw records. Carry the leg's items (LEG_READBACK §8.5): calibration E1 / E2 = **NOT EVALUATED** at I_max 0 (never 0 %); `grid_unconverged` / `I_used` as constants outside any quality aggregate; the final-merge E1–E3, `low_empirical_ESS`, sd(log Ẑ_r) > 1 as the quality items; M3 = sd(log Ẑ_r). Records `records/gb/<batch>/<run_id>/` (keyed by batch: the pilot and a later same-id rung fit cannot collide): `fit.bin`, `eval.bin(.json)`, `calib.bin.json`, `calib_meta.json`, `setup.bin.json`, `island_*.bin.json`, `truth.json`, `run_manifest.json`, `cost/`, `log/`, `SHA256SUMS`, plus `law.bin` and `data.bin` for all four fits (L-12).
### 2.5 Scripts registered BEFORE submission (not only before the first read)
| file | sha256 |
|---|---|
| `gb_imax_rule.py` | **`76927ae2faadc095e9353050eae3ef626ad439d88b92a7bf7cb9f313dab91012`** |
| `tests/test_gb_imax_rule.py` (7 tests: golden on the real FZ records + synthetic) | `7c85ebfab0145fb9140ee8887b725190bf40220a4bc9bed9bf070c5bfdd19018` |
| `tests/test_gb_readback.py` (7 tests: synthetic, **T5-shaped** (T5's measured stage costs and RSS), continuity twin, and a parse check on a **real** mini-leg eval record) | `b131ca93f028bb1e2091e3d147c7693f75878a221f16cbaccfedae0b4fd9d149` |
| `gb_readback.py` (tables, §4 criteria, continuity-twin report; no decision content beyond §4's thresholds) | **`870a610adb8663c02d431126ae14bfc63f5ea256093ea2ab2e1699a23d6d1589`** |
| `make_gb_plan.py` | **`a6aaac5d54910c4aeee2313064799635c65ed58bce5d9a1b768a0b83b5b79068`** |
| the four plans `presubmit/plans/` (driver from e993ece2, `--strict`, no warnings; regenerated twice, byte-identical) | `GB_G1a` `51af3e68f7051f09f96ecc796288f46ded8482baa2d44a81b858dac4792a1b48`; `GB_G1b` `b5d8438b984f057b442ee2075b41add57f23324277c6b1ab299915ef35ff564a`; `GB_G2a` `98c7d2e81c65a6a95ce2c51922fbc19b548f1700d535bc32ddfcfbd452915704`; `GB_G2b` `5d4b9e30cc39eb76e7260d764456c79d4d99402250995a31a014084c97900648` |

### 2.6 Pre-submit results (Owls only, no NOTS; 2026-11-20)
- **Plans and dry run.** `make_gb_plan.py` (the generator `p1m_cells.py` is not modified) builds the four plans from the F2 worktree (`e993ece226b355058e26400f05f9faad6daf16ca`); each goes through `p1m_driver.py --plan … --strict`: **no warnings, 20 tasks per batch (80 in all), "Nothing was submitted"**, each scripts tree's `SHA256SUMS` verifies. **Explicit arm verified:** after the driver run the script reads back the run manifest and the **setup, calibrate, island and merge stage manifests** of every fit and asserts `N = 10000`, `refine_m = 1` and the planned `I_max` (0 for `…-V-s1`, 3 for `…-VI3-s1`) in each: 4 / 4 fits pass (a missing key would fail the build); `gen`, `eval` and `post` manifests do not take them. Output `presubmit/make_gb_plan_output.txt`, `presubmit/waves_gb.json`.
- **Memory plan at 10⁵ N 10⁴ (real 10⁵ inputs generated on Owls with an F2 build): every request clears its plan.** `presubmit/memory_vs_request.md`: calibrate admitted at G = 256 with a plan of 8.33 GiB in a 14.4 GiB budget (T5 measured 8–11 GB: ≤ 69 % of 16 G); final island 3.53 GiB at G = 256 (N 10⁴ adds 1 MiB; T5 peak 4.5 GB, 35 % of 12 G); **merge plan 4.22 GiB against 24 G: even with the 1M under-count (× 1.72, 75.1 measured vs 43.7 planned) it is 7.3 GiB = 30 %**; setup measured 1.43 GiB (16 G). Eval at 10⁵ is unplanned and unmeasured. No request changes.
- **Read-back script.** `gb_readback.py` reads the eval, calibration and cost records and prints C1–C5 per fit (verdicts OK / SOFT / HARD, PASS / FAIL / ADVISORY, the I_max rule JSON for C6, the continuity-twin report); tested on synthetic, a T5-shaped record and a real eval record. **Field names verified on a real eval record** (the 11-19 open item 3 is closed): `pip.eq_T_target_met` / `pip.max_abs_eq_minus_T` (the PIP_𝒯 agreement), `fit.meta.local_certified`, `evidence.logZ_occ.M1000`, `fit.meta.mem_estimate.sacct_upper` (the engine's own merge estimate).

## 3. The I_max rule on the two pairs and the continuity twins (full text `GB_PREREG.md` §2–§4, §6)
- **Rule:** the registered rule applied to the pairs (AR r01, ADJ-OPP r01), 2 datasets × 1 replicate: PASS iff geometric mean ≤ 1.15 for M1, M2 and M3, each dataset ≤ 1.30, `selection.hpm` identical in all four fits. One seed per arm, shared inside a pair; R′ 16; no R′ 64.
- **Decision table (H-30, H-38; MINILEG_PREREG §3.3):**

| outcome | rung + 1M | 10⁴ science | pair fits | continuity twins |
|---|---|---|---|---|
| **PASS** | **I_max 0, N 10⁴ rung**; 1M N 2,500 I_max 0 + ONE N 10⁴ 1M fit (S2) | stands | the two I_max 0 pilots are rung fits (AR r01, ADJ-OPP r01); twins reported | run with the rung |
| **FAIL** | **I_max 3 and N 2,500** (the I_max-3 N rule is KEEP): rung 12 fits at (2,500, 3) ≈ 495 (all new); 1M at (2,500, 3), N 5,000 self-check (the KEEP row) | stands (I_max 0), **reported per configuration** | all four fits reported only; the N 10⁴ I_max 3 twins are not rung fits | **dropped** (the rung is at N 2,500) |
| NOT EVALUATED / INCOMPLETE | HQ decides (rerun or hold); no default | stands | none is a rung fit until HQ rules | held |
- **What two pairs can and cannot decide:** see `GB_PREREG.md` §3. In short, they detect gross failures (HPM differs, an M3 ratio far above 1.15, M1 / M2 leaving ≈ 1, a grid-construction failure, a final E2) and cover two designs (AR-strong, ADJ-OPP: not AR-weak or IND); they **cannot** show non-inferiority within 15 %. A FAIL costs ≈ 9.5 per 10⁵ fit and ≈ 121 per 1M fit, so a coarse test with a conservative FAIL is affordable. No post-hoc override (H-30).
- **Continuity twins (HQ addition (1), report-only, ≈ 67 core-h):** `5-AR-n200-r01-VN25-s1` (30.4) and `5-ADJOPP-n200-r01-VN25-s1` (36.9): **10⁵, N 2,500, I_max 0, same data and seeds as the two N 10⁴ pilots/rung fits**, so they connect the N 2,500 thread (10⁴ science → 1M) with the N 10⁴ thread. They run **with the rung**, after the G-B verdict says PASS, on F2, same shapes (islands 0:20). Calibration is identical by pairing (they may reuse the pilot's `calib.bin` if the driver allows: −1.1 each, unverified). What is reported (no threshold, no pass/fail): HPM equality and HPM = S₀; max_j |ΔPIP_eq| and Δ of the active / null PIPs; Δ log Ẑ (N 10⁴ − N 2,500) in island s.e.; log Ẑ − log Z_T; M1–M3 ratios r_N beside the mini-leg's 1/√c_X reference at the measured 10⁵ c_X; the measured **f at 10⁵** (billed islands ratio) against 3.77; π̂(S₀) at both N; d_H between the two store laws if `law.bin`, `data.bin` and the cross-evaluator build exist at 10⁵ (**not verified**).

## 4. G-B criteria: exact pass conditions and what a miss does
Judged on the **winning configuration's fit**: on PASS the I_max 0 pilots; on FAIL the config is (N 2,500, I_max 3), for which no fit exists at G-B, so **the rung's first fit (`5-AR-n200-r01`, N 2,500, I_max 3, ≈ 40) is the confirmation fit**: C1–C3 are evaluated on it before the other 11 rung fits are released. Both pairs are reported either way. Thresholds are registered in `GB_PREREG.md` §5.
| # | criterion | pass condition | on a miss |
|---|---|---|---|
| **C1 cost** | ≤ 1.5× model, H-26 Q4 guard | per fit ≤ 1.5 × the committed class model (§2.3): **AR pilot ≤ 162, ADJ-OPP pilot ≤ 200** (FAIL branch: confirmation fit ≤ 60). The class has one fit, so the class mean is the fit and **the 2.5× guard is the STOP line**. Listed beside it, not a criterion: the ratio to the manifest planning value (96 at N 2,500) | 1.5×–2.5×: **G-B cost FAIL, not a stop**: per-stage comparison with T5 and the mini-leg's f, rung and 1M **re-quoted from the measured fit**, HQ releases only if the re-quoted total fits 28.3k. > 2.5×: STOP, HQ re-pins |
| **C2 precision** | §0-v2.3 at R′ 16 | **M1 ≤ 0.05; M2 ≤ 0.005 (`target_met`); \|log Ẑ − log Ẑ_occ(M 1,000)\| ≤ 3√(se_Z² + se_occ²); HPM certified by the final local search**; PIP agreement ≤ 0.01 + (1 − π̂(𝒯)) if the field exists (not verified). Reported, not gating: M3 ≤ 0.5, `occ_inhomogeneous`, E1–E3, sd(log Ẑ_r) > 1; "same best model in 16 of 16 islands" not computable | **G-B precision FAIL; the rung is not auto-released**; priced options to HQ: accept as a reported miss (§0-v2.3: never an estimator switch; the 10⁴ n = 100 misses are the precedent); more islands for the rung (R′ 32: +≈ 106 per fit at N 10⁴); hold |
| **C3 memory** | < request | MaxRSS and O2 `peak_rss` < request in all 5 stages (setup 16 G, calibrate 16 G, islands 12 G, merge 24 G, eval 16 G); advisory > 80 %; peak < 50 % of a node recorded | a stage ≥ its request / OOM: **memory FAIL, not a halt**: re-size to 1.3 × the measured peak, rerun that stage, re-evaluate ("PASS after resize"); the rung uses the re-sized requests. The `--plan-only` plan at 10⁵ N 10⁴ is checked first (0 core-h) |
| **C4 completion** | all four fits delivered, one sha = F2's, arm identity verified, `logZ_r` length 16 and finite | one infrastructure rerun per fit, then INCOMPLETE → HQ |
| **C5 E2 recorded** | per §2.4 | recording only |
| **C6 I_max rule** | PASS / FAIL recorded with the form (2 datasets × 1 replicate) | per §3 |
**G-B passes iff C1–C4 pass (after any memory resize) and C6 is PASS or FAIL.** The pilots' HPM should equal S₀ (T5, AR r01: {10000, 30000, 50000, 70000, 90000}); otherwise a flag to HQ, not a criterion.

## 5. 1M rep 1: options for HQ's ruling at G-B
**Rep 1** = `6-AR-n200-r01-V-s1`, 437.44 core-h measured (calibrate 135.63 with **3 rebuilds**), HPM = MPM = S₀, **pre-F2** code 2cfaa9e5, N 2,500, I_max 3. Under I_max 0 it is not in the frozen configuration.
| option | what | cost now |
|---|---|---|
| **(a)** re-run rep 1 frozen | same data and seed, F2, I_max 0, N 2,500: replicate 1, **same-seed partner of the 1M N 10⁴ fit** (S2) and of the pre-F2 I_max 3 pilot (the only 1M I_max pair, after an F2-vs-2cfaa9e5 identity statement at 1M) | **≈ 317** (437.44 − 135.63 + P7's pilot island 14.96; P90 ≈ 360) |
| **(b)** report rep 1 as a separate configuration | pilot evidence ("I_max 3, pre-F2, one seed"); replicates 2–20 frozen | **0** |
| (c) a 21st replicate on fresh data | rep 1 stays separate | ≈ 317 |
**Manager's recommendation: (b) now; HQ rules at G-B after the I_max verdict.** The review's caveats stand: rep 1 is one fit, one seed, pre-F2, no same-seed I_max 0 partner (it becomes an I_max 3 arm only with an F2 identity statement at 1M, ≈ 17 + 15 if its `calib.bin` / `setup.bin` are retained, **retention not verified**); under (b) 19 of the 20 approved replicates are frozen unless a 21st runs; and **the MANIFEST §1 pilot rule ("kept as pilot evidence, a fresh replicate 1 is run") makes (b) a departure from the registered rule on PASS** that needs HQ's explicit ruling.
**New since the draft (H-34, H-38):** (i) **if the 20-seed block (H-34) is released on the rep-1 data at the frozen configuration, its seed 1 is the frozen re-run of rep 1: (a) then costs nothing extra** (the totals below are equal). (ii) S2's ONE N 10⁴ 1M fit on the rep-1 data is paired in the mini-leg's sense (same seed, same grid) with an N 2,500 I_max 0 fit on that data, which only (a) or the seed block provides. (iii) On FAIL the configuration is (N 2,500, I_max 3) and rep 1 is in-configuration for I_max (after the identity statement); a re-run would cost 437.
**Envelope table** (from closed 2,686.91; unit costs MEASURED as §6; ablations + competitors 1,052 and option D 1,087 are plan values; `tools/gb_quote_output.txt`):
| scenario | 1M items | position (no reserve) | with 25 % on the unspent 1M items | share of 28.3k |
|---|---|---|---|---|
| S2, (b): 21 frozen fits (19 AR + ADJ-OPP + AR-weak), ONE N 10⁴ fit 1,062, D 1,087 | 9,853 | **14,228** | 16,691 | 50 % / 59 % |
| S2, (a)/(c): 22 frozen fits | 10,170 | 14,544 | 17,087 | 51 % / 60 % |
| S2 + **H-34 20 seeds** (6,335; ≈ 6.4k), (a) = (b) | + 6,335 (− 317 under (a)) | **20,563** | **24,610** | **73 % / 87 %** |
| **FAIL branch** (N 2,500, I_max 3; 21 × 437, N 5,000 self-check 707, D 1,510) | 12,455 | 16,138 | 19,501 | 57 % / 69 % |
| FAIL + H-34 at I_max 3 (20 × 437 = 8,749) | | 24,887 | **30,437: does not fit with the reserve** | 88 % / 108 % |
The budget does not separate (a), (b), (c) (a difference of 317 = 1.1 %); on FAIL the H-34 block at I_max 3 needs HQ's decision (it fits only without the reserve).

## 6. After G-B: the rung, option D, the 1M start (gate-paced; dates are earliest-feasible, not commitments)
**Steps and quotes** (E; N* 10⁴ and I_max 0 unless stated; measured bases: T5 = 42.18 at N 2,500; f = 3.768; 1M pilot 437.44; P7 pilot island 14.96):
| step | content | E (P90) core-h | position after |
|---|---|---|---|
| closed | 975.5 + 1,010.43 + 462.48 + 1.99 + 236.51 | **2,686.91** | 2,687 |
| **G-B set** | AR pair 226 + ADJ-OPP pair 275 | **501 (≈ 650)** | 3,188 |
| **I_max verdict, G-B read-back** | HQ | | |
| 10⁵ rung (waits for the verdict) | 12 fits at N 10⁴: AR n200 ×5, AR n400 ×3, IND n200 ×2, ADJ-OPP n200 ×2; **10 remaining** after the two pilots. Unit: AR n200 108.2; n400 1.0× (10⁴ measured 0.77×, planning model 1.6× is the P90); IND 1.05×, ADJ-OPP 1.23× | 12 fits **1,360 (1.94k)**; remaining 10: **1,119 (1.70k)** | |
| continuity twins | 2 fits, N 2,500, I_max 0 | **67** | **4,374** |
| 1M (S2) | 21–22 frozen fits at **317** (P90 360) + ONE N 10⁴ fit **1,062** + option D **1,087** + ablations / competitors 1,052 | 9,853–10,170 | **14.2–14.5k** |
| H-34 seeds (conditional) | 20 seeds on ONE 1M dataset, N 2,500, I_max 0 | **6,335** (≈ 320 each) | **20.6k** |
Rung data seeds (R·10⁸ + D·10⁶ + (n/100)·10⁴ + rep): AR n200 `502020001…05`, AR n400 `502040001…03`, IND n200 `501020001…02`, ADJ-OPP n200 `505020001…02`; run ids `5-<design>-n<n>-r<rep>-V-s1`; one seed per fit. The rung's first batch (AR n400 ×1) re-quotes the rest (n-scaling at 10⁵ is **not measured**; the leg's regression says "consider T"). The rung is the first 10⁵ evidence of N 10⁴ beyond the pilots: the mini-leg's gate "one 10⁵ N 10⁴ fit before any 1M fit" is met by the pilots.
- **Option D (H-1; HQ rules at G-B): proposed gate wording.** AR-strong n = 1,000 at 1M, N 2,500, I_max per the verdict (≈ 1,087), is released iff **all** hold on the 10⁵ rung (AR-strong, n 200 × 5 and n 400 × 3, in the winning configuration): **(D1)** the theorem premise holds at 10⁵: P̂(HPM = S₀) ≥ 4/5 at n 200 and 3/3 at n 400; **(D2)** the expected trend: the mean over datasets of **π̂(S₀)** (**field verified**: π̂(S₀) = exp(`selection.F_S0` − `evidence.logZ`), the estimated posterior probability of S₀, with the terminal occupancy `fit.meta.occ[M = 1].occ` beside it (S₀'s when HPM = S₀) and the store-law omitted mass reported) at n 400 is ≥ the mean at n 200 (OWNER_SHEET's expected band: 0.3–0.45 at n 200, rising; reported with the dataset-clustered interval, **not a significance test**: 5 against 3 datasets); **(D3)** the budget check: position + D ≤ 28.3k at the re-sized unit cost. Reported beside it, with **no numeric threshold and a flag to HQ if the N effect looks large**: the continuity twins' π̂(S₀) at N 2,500 against N 10⁴ (the trend is measured at N 10⁴, D runs at N 2,500). π₀(S₀) is a different, deferred quantity.
- **G-C-type conditions before the 1M replicates (H-14):** 10⁵ rung ≥ 90 % complete (≥ 11 of 12); restart tested at 10⁵ (T6 PASS on pre-freeze code 96137399; an optional T6′ on F2, one island, ≈ 3.2); configuration, evaluator and competitors frozen by hash (the FZ addendum, the mini-leg verdict, this plan's commit); kill rule 2× model at 50 % progress (1M model 317, or 437 at I_max 3); 2 fits at a time, each batch pre-announced; the 1M memory plan at N 10⁴ (`--plan-only`) before the N 10⁴ 1M fit.
- **Order:** commit this plan → pilot set G1 → G2 → read-back + Opus check → HQ G-B + rep-1 ruling + option-D wording → rung + continuity twins (PASS) / confirmation fit then rung (FAIL) → rung read-back → 1M from ≈ 12-01 (earlier if the gates clear).

## 7. Open items and things not verified (settle before the first submit)
1. **Closed 11-20 (§2.6):** `make_gb_plan.py` and `gb_readback.py` written and tested; the driver dry run (`--strict`) clean with the arm explicit in every manifest; the 10⁵ N 10⁴ `--plan-only` memory plan run on real 10⁵ inputs; the eval field names verified.
2. Still before the first submit: the manager's commit with these shas; `cp -p` of the F2 binary and the presubmit check on NOTS (not mine); the stage-shape request for ADJ-OPP merge is the AR one (same dimensions).
3. Eval at 10⁵ has no plan and no measurement; the first eval measures it.
4. Merge and eval RSS at 10⁵ have no measurement (T5 reports islands and calibration only); merge is covered by the plan (4.22 GiB, × 1.72 = 7.3 GiB in 24 G), eval is not. Setup was measured on Owls (1.43 GiB). Island RSS at N 10⁴ at 10⁵ is inferred from the plan (+1 MiB over N 2,500).
5. I_max 0 calibration at 10⁵ (0.10×) is a 10⁴ figure; merge cost at N 10⁴ (0.8) is extrapolated from the 10⁴ residual; ADJ-OPP factor 1.23 is the committed 10⁴ class ratio.
6. Retention of rep 1's `calib.bin` / `setup.bin` and of T5's run dir on NOTS scratch.
7. The ADJ-OPP island wall outlier (×7.2 at 10⁴) is unexplained: the 1:00 limit covers a repeat.
8. The two-pair characteristics rest on same-seed pairs at **N 2,500**; the M3 pair-ratio noise at N 10⁴ is unknown (disclosed, `GB_PREREG.md` §6).
9. The mini-leg's ADOPT is fragile (M2 margin 0.0019, within the noise of c_X): the rung at N 10⁴ is spent only after the I_max verdict holds I_max 0, as the check recommends.

## 8. Files
`results/gb/GB_PLAN.md`, `GB_PREREG.md`, `gb_imax_rule.py`, `gb_readback.py`, `make_gb_plan.py` (shas in §2.5), `tests/` (`test_gb_imax_rule.py`, `test_gb_readback.py`), `presubmit/` (`plans/`, `plans.sha256`, `waves_gb.json`, `make_gb_plan_output.txt`, `memory_vs_request.md`, `memplan/`), `tools/` (`gb_quote.py` sha256 `854ba5ba42eb1c38…`, `gb_quote_output.txt`, `imax_at_N1e4_output.txt`, `pair_ratios.py`, `pair_ratios_output.txt`). Nothing committed, nothing on NOTS, nothing under `/tmp`, no BNP file touched.
