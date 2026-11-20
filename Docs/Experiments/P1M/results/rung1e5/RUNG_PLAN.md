# RUNG_PLAN: the 10⁵ rung at (F2, N 10⁴, m 1, I_max 0): the remaining 10 fits, the 2 continuity twins, the forced-kill restart test (T6), the D1–D3 evaluation (Engineering, Sonnet plan writer; Fri 2026-11-20)

**Status: final; COMMITTED by the Engineering manager 2026-11-20 before any rung run (HQ H-40)** (HQ H-40: G-B PASS, I_max 0 stands, 10⁵ rung GO, option D adopted verbatim, rep 1 = (b)). Nothing here is committed, submitted or run on NOTS. Companions: `GB_PLAN.md` / `GB_PREREG.md` (committed, 26ef4abc; the rung inherits their conventions), `GB_READBACK.md`. Plan tools: `tools/`; pre-submit outputs: `presubmit/`. Scratch (Owls only): `~/SMC_Engineering_Department/tmp/20261120-rung/`.

## Summary (≤ 12 lines)
1. **Fits:** the 12 MANIFEST rung fits are AR n200 ×5, AR n400 ×3, IND n200 ×2, ADJ-OPP n200 ×2. **Two are the G-B pilots and are done** (AR n200 r01 = `GB_G1a`, 76.39; ADJ-OPP n200 r01 = `GB_G2a`, 65.65). **The 10 remaining** run at F2 `da0cf85b…`, N 10⁴, m 1, I_max 0, R′ 16: AR n200 r02–r05, AR n400 r01–r03, IND n200 r01–r02, ADJ-OPP n200 r02. Plus the **2 continuity twins** (N 2,500, same data and seeds as the two pilots; report-only).
2. **Plans (driver from e993ece2, `--strict`, no warnings; explicit N / refine_m / I_max asserted in the run, setup, calibrate, island and merge manifests of every fit; regenerated three times, byte-identical):** `RG_1a` `8afd032b…`, `RG_1b` `fced26b3…`, `RG_2a` `5b02cead…`, `RG_2b` `475e81a9…`, `RG_3a` `dd2a8da0…`, `RG_3b` `2387b19c…`, `RG_T6` `91e53f90…` (+ the fallback `RG_T6b` `536a1e69…`). 12 fits + 1 T6 task, 241 tasks, every batch ≤ 150 tasks, every task ≤ 2 h (islands 1:00 at most, T6 1:30): **no exception**.
3. **Restart test (G-C item):** one **T6 task** (`RG_T6`, 48 CPUs, 24 G, 1:30) on the **G-B pilot's own inputs** (AR r01, N 10⁴, I_max 0): inside the job `p1m_t6.py` runs an uninterrupted reference island, **SIGKILLs by PID** a second island process after its second checkpoint generation, SIGKILLs a resumed process **in the middle of a checkpoint write**, resumes a third time and completes. PASS = every `p1m_t6` check **and** the resumed `output_hash` = the reference's = the G-B pilot's own island 1 (`0x4e4fd6a2e6135cfb`). ≈ **12 core-h** (P90 ≈ 20; worst 72).
4. **Waves:** R1 (n400 pilot `RG_1a` + twins `RG_1b` + T6) quote **150** → wave stop 300; R2 (AR n200 ×4 + AR n400 ×2) **460** → 920; R3 (IND ×2 + ADJ-OPP r02) **220** → 440. **Total ≈ 824** (HQ's 813 = 10 fits 753 + twins 60; **+ T6 11 = 824**; P90 ≈ 1.1k); cumulative stop **1,400**; projection ceiling **1,326** (the S2 rung figure, counting the two G-B pilots' 142).
5. **D1–D3 (option D, verbatim, judged at the read-back):** the AR-strong fits n200 r01–r05 and n400 r01–r03; D1 ≥ 4/5 and 3/3 HPM = S₀; D2 mean π̂(S₀) n400 ≥ n200 with **no tolerance**, reported with a Welch t-interval and a cluster bootstrap; D3 budget. Script `rung_d123.py`.
6. **Envelope:** closed 2,984.56 + 824 = **3,809**; S2 (b) ends at ≈ 13.7k (16.1k with reserve), with the H-34 seeds ≈ 20.0k (24.0k).

## 1. Fits
| # | fit | data seed = engine seed | status / batch | role |
|---|---|---|---|---|
| 1 | `5-AR-n200-r01-V-s1` | 502020001 | **G-B pilot, done** (`GB_G1a`, 76.39) | rung fit; D1 / D2 n 200; T6 source |
| 2 | `5-ADJOPP-n200-r01-V-s1` | 505020001 | **G-B pilot, done** (`GB_G2a`, 65.65) | rung fit |
| 3–6 | `5-AR-n200-r02 … r05-V-s1` | 502020002 … 05 | `RG_2a` | D1 / D2 n 200 |
| 7 | `5-AR-n400-r01-V-s1` | 502040001 | `RG_1a` (**the n-scaling pilot of R1**) | D1 / D2 n 400; the fallback T6 source |
| 8–9 | `5-AR-n400-r02, r03-V-s1` | 502040002, 03 | `RG_2b` | D1 / D2 n 400 |
| 10–11 | `5-IND-n200-r01, r02-V-s1` | 501020001, 02 | `RG_3a` | rung fits |
| 12 | `5-ADJOPP-n200-r02-V-s1` | 505020002 | `RG_3b` | rung fit |
| twin | `5-AR-n200-r01-VN25-s1` | 502020001 | `RG_1b` | continuity twin of fit 1 (N 2,500) |
| twin | `5-ADJOPP-n200-r01-VN25-s1` | 505020001 | `RG_1b` | continuity twin of fit 2 (N 2,500) |
Seeds: R·10⁸ + D·10⁶ + (n/100)·10⁴ + rep (MANIFEST §1); one seed per fit; the engine seed equals the data seed. All 10 new rung fits and both twins: F2, m 1, **I_max 0**, R′ 16, bounded calibration, class A, `island_isa sapphirerapids`, resampling off ("not tested"). N 10⁴ for the 10 rung fits, **N 2,500 for the twins** (the arm tag `VN25` keeps the report-only fits outside every registered id pattern, the mini-leg's r04 lesson). No I_max 3 fit is in the rung (the G-B pairs did that).
- **Explicit arm (silent-default guard).** `make_rung_plan.py` writes `N` (top level), `refine_m 1` and `I_max 0` in every fit and, after the driver runs, reads back the **run manifest and the setup, calibrate, island and merge stage manifests of every fit** and asserts N (10⁴ or 2,500), `refine_m 1`, `I_max 0` (`presubmit/waves_rung.json`: all asserted; a missing key would fail the build). The generated 10⁵ plans of `p1m_cells.py` carry neither (engine default I_max 3, N 2,500): they must not be used.
- **One build, F2:** `cp -p` + sha256 (COPYBIN) of the recorded F2 build `da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a` into each of the 7 batches; never rebuilt; every sidecar's `binary.sha256` must equal it.
- **Calibration identity of the twins:** the calibration is N-independent (H = 512): the twin's grid equals its pilot's at the same seed (mini-leg pairing identity); the read-back checks `calib.bin` section equality (all but `meta`).

## 2. Run sheet (every task ≤ 2 h; no exception)
| batch | fits | tasks | setup | calibrate | islands (limit; throttle) | merge | eval | worst case (limit sum) |
|---|---|---|---|---|---|---|---|---|
| `RG_1a` | AR n400 r01 | 20 | 32 CPU 16 G 0:30 | 64 CPU 16 G 0:30 | 48 CPU **12 G** **1:00**; %8 | 16 CPU **24 G** 0:30 | 8 CPU 16 G 0:45 | 830 |
| `RG_1b` | the 2 twins (N 2,500) | 40 | same | same | 48 CPU 12 G **0:20**; %8 | same | same | 636 |
| `RG_2a` | AR n200 r02–r05 | 80 | same | same | 48 CPU 12 G **0:45**; %12 | same | same | 2,552 |
| `RG_2b` | AR n400 r02–r03 | 40 | same | same | 48 CPU 12 G 1:00; %8 | same | same | 1,660 |
| `RG_3a` | IND n200 r01–r02 | 40 | same | same | 48 CPU 12 G 1:00; %8 | same | same | 1,660 |
| `RG_3b` | ADJ-OPP n200 r02 | 20 | same | same | 48 CPU 12 G 1:00; %8 | same | same | 830 |
| `RG_T6` | the T6 task (§4) | 1 | – | – | **48 CPU 24 G 1:30** (one task) | – | – | 72 |
Worst cases are limit sums (the admission figure, not an estimate): **8,240 for the 6 fit batches + T6** (`RG_T6b` is an alternative, not additional). The limits rest on G-B: islands wall 396–447 s at 48 CPUs (one ADJ-OPP island took 7.2× its twin at 10⁴, hence 1:00 for ADJ-OPP, n400 (unmeasured) and IND (unmeasured)); calibrate I_max 0 85–102 s; merge ≤ 195 s; eval ≤ 41 s. **Island arrays are throttled per batch** so a wave peaks at 816 (R1), 960 (R2) and 768 (R3) island CPUs, under the QOS cap of 1,536. Batches of a wave ≥ 5 min apart; waves serial.
**Memory against the requests** (islands 12 G, calibrate 16 G, merge 24 G, setup 16 G, eval 16 G; pre-submit `--plan-only` on real inputs generated on Owls with an F2 build, plus G-B's measured sacct peaks):
| stage (request) | AR n200 (G-B measured) | AR n400 (plan, real setup) | IND n200 (plan, real setup) | verdict |
|---|---|---|---|---|
| setup (16 G) | 2.5 GiB sacct (1.43 on Owls) | 1.52 GiB (Owls setup, 3:33 wall at 8 threads) | 1.67 GiB (Owls setup, 2:33 wall; `setup.bin` 1.23 GB) | PASS |
| calibrate (16 G) | 5.55–5.74 (I_max 0) | 8.54 admitted at G = 256 (53 %) | 8.77 admitted at G = 256 (55 %) | PASS |
| islands (12 G) | 3.54–3.70 | 3.80 (32 %; N 10⁴ and N 2,500 identical) | 3.74 (31 %) | PASS |
| merge (24 G) | process 2.06 (sacct 4.97–6.86 incl. page cache) | 4.25 plan (18 %) | 4.84 plan (20 %) | PASS |
| eval (16 G) | 1.67–1.72 | (as G-B) | (as G-B) | PASS |
**Ops:** deploy = COPYBIN + `presubmit_check.sh` (sha rule); `home_guard` 7,900 MB; jobs write only under `scratch/`; one ledger row per batch (quote, worst); the Haiku monitor of the G-B pattern (one `ssh nots`, one `squeue` + one `sacct -X`, ≤ 1 probe per 5 min, `START` line, `WAVE STATE: ENDED`), batch ids `RG_*`; monitor map = the quotes of §3.

## 3. Waves, quotes, committed class table, stops
**Quotes (E, core-h; measured bases: G-B AR n200 76.39, ADJ-OPP 65.65 at N 10⁴, I_max 0; `tools/rung_quote_output.txt`):** n400 at 1.0× AR (**unmeasured at 10⁵**; the plan's 1.6× is the P90), IND at 1.0× AR (**assumption**; the 11-19 plan used 1.05×, −8), twins from the I_max 0 stage costs with the island factor 2.53 implied by T5, T6 from the G-B islands wall × T6's measured ratio at N 2,500.
| wave | batches | content | E | **quote** → wave stop (> 2×) | release |
|---|---|---|---|---|---|
| **R1** | `RG_1a`, `RG_1b`, `RG_T6` | AR n400 r01 76.4 (**the n-scaling pilot**); twins 31.9 + 27.9 = 59.8; T6 11.4 | 147.7 | **150 → 300** | self-release on the commit (HQ H-40) |
| **R2** | `RG_2a`, `RG_2b` | AR n200 r02–r05 305.6; AR n400 r02–r03 152.8 | 458.3 | **460 → 920** | after R1's read-back is clean and **R1 re-quotes n400**: self if the re-fitted R2 quote ≤ 1.5× this table's (690), else HQ first |
| **R3** | `RG_3a`, `RG_3b` | IND n200 ×2 152.8; ADJ-OPP r02 65.7 | 218.4 | **220 → 440** | after R2 clean (IND is unmeasured: R2's n400 result and R3's first IND fit re-fit the class means; the hard line never moves) |
| rung total | | 10 new fits 753.2 + twins 59.8 + T6 11.4 | **824** (P90 ≈ 1.1k) | | HQ's 813 = fits + twins; T6 is +11 (1.4 %) |
P90 (assumption stated): AR n200 and ADJ-OPP × 1.2, n400 × 1.6 (the plan's per-n factor), IND × 1.3, twins × 1.2, T6 20 → ≈ 1,100.
**Committed class table (E per fit; soft = max(3, 1.5E) report-and-continue; hard = max(3, 2.5E) STOP; the hard line is pinned and never re-fitted; H-26 Q3 / Q4 form):**
| class | fits | E | soft | **hard** |
|---|---|---|---|---|
| 10⁵ AR n200 N 10⁴ I_max 0 | 4 (+ the pilot) | 76 | 114 | **190** |
| 10⁵ ADJ-OPP n200 N 10⁴ I_max 0 | 1 (+ the pilot) | 66 | 99 | **165** |
| 10⁵ AR n400 N 10⁴ I_max 0 (unmeasured) | 3 | 76 | 114 | **190** |
| 10⁵ IND n200 N 10⁴ I_max 0 (assumption) | 2 | 76 | 114 | **190** |
| continuity twin AR n200, N 2,500 | 1 | 32 | 48 | **80** |
| continuity twin ADJ-OPP n200, N 2,500 | 1 | 28 | 42 | **70** |
| T6 restart test (N 10⁴, one task, 48 CPUs) | 1 | 12 | 18 | **30** |
**Stops (the monitor evaluates; any one → stop submitting, tell the manager):** per-fit soft = report-and-continue **provided** the fit is valid, ≤ the hard line, < 3 soft trips in the wave; per-fit **hard = STOP** (a hard trip in a pilot class means the committed model was wrong: HQ re-pins the table); **wave** actual > 2 × its quote (300 / 920 / 440); **cumulative: 1.6 × 824 = 1,319 → 1,400** (new spend of this plan); **projection ceiling: 1,326** (the S2 rung figure, counting the two G-B pilots' 142.04, i.e. **1,184 of new spend**): spent + class means × fits left > ceiling → HQ before any further wave; failures: any FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (a T6 kill is **not** a failure: the SIGKILLs are by PID inside one COMPLETED job; the job itself failing is); **arm identity** (recorded arm from `calib_meta.json` ≠ plan → STOP; I_max 0 → no `cost/cost_diag_*` files); **data identity** (`truth.json` X / y equal inside a twin pair and equal to the pilot's); **build identity** (`binary.sha256` = F2's); admission (`resource_limit` / `OUTCOME`). Informational: a task > 80 % of its limit; a G-B-class island wall > 4× 447 s.
**G-B cost criterion carried (H-26 Q4):** per class, mean ≤ 1.5× the table's E and no fit > 2.5× (listed in the read-back); n400 and IND classes are re-fit from R1 / R3 for the soft line and the next quote only.

## 4. The forced-kill restart test at 10⁵ (G-C item), on ONE rung fit
**What it tests.** The island checkpoint / restart of F2 at 10⁵, N 10⁴, I_max 0, by REAL SIGKILLs: a killed island resumes from its checkpoint and the resumed island is **bit-identical** (output hash and every non-meta section) to an uninterrupted one. It follows T6 (`results/T6_1e5.md`: 11-17, N 2,500, code 96137399, 3.23 core-h, PASS, 11/11 checks) and the driver's `t6_only` machinery (`T6_AND_RESTART.md`, `p1m_t6.py`).
**The fit and the inputs.** Rung fit 1, `5-AR-n200-r01-V-s1` (the G-B pilot, N 10⁴, I_max 0), island 1, on **its own** `data.bin`, `setup.bin` and `calib.bin` in `scratch/runs/GB_G1a/5-AR-n200-r01-V-s1/` (the stage script refuses to start if one is missing, exit 66). **Retention of those files on NOTS scratch is not verified by me (Owls only): the manager checks `ls` before releasing R1; if they are gone, submit the fallback `RG_T6b`** (source `RG_1a` = AR n400 r01, after its calibrate has finished: the task reads only data / setup / calib, so it may run while that fit's islands run; the pre-declared third hash is then that fit's own island 1, read after).
**How the kills are done (scheduled in the job script, no manual `scancel`).** `stage_t6.sbatch` (generated by the driver) runs one task (48 CPUs, 24 G, `--mem-budget` 0.9 × 24 G, `--time 1:30`) that executes `p1m_t6.py --island 1 --kills 2 --ckpt-every-s 60 --max-seconds 5100`:
1. **reference:** the island uninterrupted, `--ckpt 0` → `ref_island.bin` (≈ 7.5 min at 48 CPUs, G-B's island wall at N 10⁴);
2. **kill 1:** the same island with `--ckpt 1 --ckpt-every-s 60` starts as a child process; the script polls `island.ckpt.{a,b}` and, when **both generations** exist (the second checkpoint was written), sends **SIGKILL to that PID** (`os.kill`); it must die with return code −9 and leave no `island.bin`;
3. **kill 2:** the identical command is started again (it **resumes** from the surviving checkpoint); the script waits for the writer's temporary file `island.ckpt.{a,b}.tmp.<pid>` **of that process** and SIGKILLs it at once, i.e. **in the middle of a checkpoint write** (the earlier complete generation must survive);
4. **final run:** the identical command resumes from the checkpoint and completes; `island.bin` is written and the checkpoints are removed.
Only processes started by the script are killed, by PID (POLICIES: never `pkill` by pattern). **The only manual act is `CONFIRM=yes bash submit_t6.sh`** (one `sbatch`).
**The reference** is the uninterrupted island of step 1 (a same-job twin island run, same binary, inputs, seed, island, threads) **and**, independently, the G-B pilot's own island 1 for the same inputs (`island_1.bin.json` `output_hash` **`0x4e4fd6a2e6135cfb`**, T 30, N 10⁴, status completed, seed 502020001).
**Pass rule (pre-declared).** **PASS iff** (a) `p1m_t6.py` returns `ok`, i.e. **every** check is true: `reference_completed`; `kill_1_sigkill` and `kill_2_sigkill` (return code −9); `kill_1_no_island_file`, `kill_2_no_island_file`; `final_completed`; `resumed` (`resumed_from_step ≥ 1`); `status_completed`; `output_hash_equal` (resumed = reference); `ckpt_removed`; `sections_equal` (every non-meta section hash of the two island files equal, via `smcbvs4 info --meta 1`); **and** (b) the resumed `output_hash` equals `0x4e4fd6a2e6135cfb` (skipped for the fallback source). **INVALID, not FAIL:** an island that ends before a kill condition (`p1m_t6` says "lower --ckpt-every-s"): one rerun at `ckpt_every_s 30` (+≈ 12). **FAIL:** any other false check, or a hash difference: STOP, HQ + Theory (a restart that changes the output would also change every resumed 1M island).
**Cost.** E ≈ **11–12 core-h** (wall ≈ 14 min at 48 CPUs: the reference 7.5 min + 2 killed runs + the resumed run + 4 checkpoint loads; T6's measured ratio at N 2,500 is 4:02 for a 1:52–2:33 island; the 60-s cadence and the larger N 10⁴ state add ≈ 15 %), **P90 ≈ 20, worst 72** (48 × 1.5 h); the class table's hard line is 30. It runs inside R1 beside `RG_1a`, `RG_1b` (separate task, separate workdir, inputs read-only).
**Not tested here (stated).** The Slurm-level `restart` chain (soft stop, `afterany` attempts): the rung plans do **not** use it (island limits are ≥ 2.2× the observed wall); T6 tests the checkpoint mechanism it relies on. T6 at N 2,500 on F2 (the 1M main configuration) is not repeated here (it passed pre-freeze at N 2,500 on the same code path; F2 = F at default N, VN_ID_1); an optional T6′ on the N 2,500 twin's inputs costs ≈ 3.2 core-h if HQ wants it.

## 5. D1–D3 at the rung read-back (option D, adopted verbatim: GB_PLAN §6; HQ H-40 (c))
**The verbatim wording** is GB_PLAN §6 "Option D"; this section fixes only which fits enter and how the quantities are computed (`rung_d123.py`, registered with the commit; synthetic self-test 7/7, incl. the t-quantile against textbook values and a real G-B record).
- **Fits that enter D1 / D2 (AR-strong only):** **n 200: `5-AR-n200-r01 … r05-V-s1`** (r01 is the G-B pilot, read from `records/gb`); **n 400: `5-AR-n400-r01 … r03-V-s1`**, each with recorded arm (N 10⁴, m 1, I_max 0). **ADJ-OPP, IND, the I_max 3 twins and the continuity twins do not enter.** Each fit has its own dataset: the dataset is the independent unit. If fewer than 5 + 3 are delivered the evaluation is NOT EVALUABLE (to HQ), never computed on a subset.
- **D1 (the theorem premise at 10⁵):** P̂(HPM = S₀) from `selection.hpm_eq_S0`; **PASS iff ≥ 4 of 5 at n 200 and 3 of 3 at n 400.**
- **D2 (the expected trend):** π̂(S₀) = exp(`selection.F_S0` − `evidence.logZ`) per fit (the estimated posterior probability of S₀; the terminal occupancy `fit.meta.occ[M = 1].occ` and the store-law omitted mass are printed beside it); **PASS iff mean π̂(S₀) at n 400 ≥ mean at n 200: a comparison of means with NO tolerance (5 against 3 datasets; a difference of −10⁻¹² or more counts as equal: floating-point roundoff only).** **Reported, not gating:** the difference n400 − n200 with **(a)** the Welch 95 % t-interval for two independent means (Welch–Satterthwaite df) and **(b)** a percentile **cluster bootstrap** (the datasets are resampled within each n level, 10,000 draws, seed 20261120), plus every per-dataset value. With small samples the intervals will be wide: stated in advance.
- **D3 (budget):** position + D ≤ 28.3k at the re-sized unit cost: computed by the read-back's budget script, **not** by `rung_d123.py`. The re-sizing is pre-declared: D = 317 × ρ^(log₂ 5), with ρ the measured per-fit cost ratio (AR n400 mean / AR n200 mean) at 10⁵ (cost ∝ n^g, g = log₂ ρ, so n 1,000 = 5 × n 200 costs ρ^(log₂ 5)), floored at 317 and printed beside the plan value 1,087. With the position ≈ 3.8k after the rung, D3 is far from binding.
- **Beside (no threshold; a flag to HQ if the N effect looks large):** the continuity twins' π̂(S₀) at N 2,500 against N 10⁴ (AR r01, ADJ-OPP r01). The trend is measured at N 10⁴, D runs at N 2,500, and there is no N 2,500 link at n 400 (stated for HQ).
- **First evidence (G-B, n 200, two datasets):** π̂(S₀) 0.387 (AR), 0.340 (ADJ-OPP); HPM = S₀ in both. OWNER_SHEET's 0.3–0.45 is the expert's p = 10⁶ draw, not a 10⁵ band.
- **What the read-back reports to HQ:** D1 PASS / FAIL with the counts, D2 PASS / FAIL with the means and both intervals, D3 with the re-sized D; the release of option D is HQ's.

## 6. Read-back
**After each wave:** the manager's one-line report (H-40) and the Haiku probe verdicts. **After R3 (the rung read-back):** the Sonnet worker runs, in this order (all registered by the commit, **before the first submission**: L-8 carry rule): `rung_readback.py` (per-fit C1–C5 with the rung class table, the G-C completion count, the T6 check), `gb_readback.py` (the registered G-B script, unedited, for the continuity-twin report), `rung_d123.py` (D1 / D2) and the budget arithmetic (D3, the re-sized 1M units). Then **one Opus child** re-derives the completion count, the D1–D3 quantities, the T6 verdict and the twin report from the raw records, and the read-back goes to HQ with the G-C plan.
- **Per fit (as G-B):** C1 cost against the §3 class table (OK / SOFT / HARD), C2 precision (M1 ≤ 0.05, M2 ≤ 0.005, evidence within 3 s.e., HPM certified, PIP agreement; reported per fit, a miss is a target miss and never an estimator switch), C3 peak RSS < request in all 5 stages (and the merge **process** peak `peak_rss_kb` beside sacct, which counts page cache), C4 completion, C5 flags (calibration E1 / E2 NOT EVALUATED at I_max 0, `grid_unconverged` True and `I_used` 0 as constants, final E1–E3, sd(log Ẑ_r) > 1).
- **G-C items:** completion ≥ 11 of 12 rung fits (the two G-B pilots count) — **PASS / FAIL with the missing ids**; **T6 PASS** (§4); the 1M cost re-sized from the measured rung (AR n200, n400, IND, ADJ-OPP unit costs; the n-scaling at 10⁵ measured); the configuration, evaluator and competitors frozen by hash (the FZ addendum, the mini-leg and G-B read-backs, the commits).
- **Continuity twins, pre-declared outputs (GB_PLAN §3, unchanged; report-only; no threshold; no pass / fail):** per pair (N 10⁴ pilot vs N 2,500 twin, same data and seeds): HPM equality and HPM = S₀; the change of the sup of null PIP and the min of active PIP (the **max_j |ΔPIP_eq|** needs the `fit.bin` reader and is computed there if available, else "not computed"); Δ log Ẑ (N 10⁴ − N 2,500) in combined island s.e.; log Ẑ − log Z_T for both; M1–M3 ratios r_N beside the mini-leg's reference 1/√c_X at the **measured 10⁵ c_X**; the **measured island factor f at 10⁵** against 3.77 and the 2.5–2.9 inferred from T5; π̂(S₀) at both N; d_H between the two store laws only if `law.bin`, `data.bin` and the cross-evaluator build exist at 10⁵ (not verified; otherwise "not computed"); stage costs and wall.
- **Records:** `records/rung1e5/<batch>/<run_id>/` (keyed by batch): `fit.bin`, `eval.bin(.json)`, `calib.bin.json`, `calib_meta.json`, `setup.bin.json`, `island_*.bin.json`, `truth.json`, `run_manifest.json`, `cost/`, `log/`, `SHA256SUMS`; **`law.bin` and `data.bin` for the two twins and the two pilots** (the pair cross-check, L-12); the T6 task: `t6.json`, `t6/` logs and the island hash files (not the 1 GB island files). Offload per the tombstone rule.

## 7. Quote and envelope position
| item | core-h |
|---|---|
| closed after G-B | **2,984.56** (2,686.91 + 297.65) |
| R1 (n400 pilot 76.4 + twins 59.8 + T6 11.4) | 147.7 |
| R2 (AR n200 ×4 305.6 + AR n400 ×2 152.8) | 458.3 |
| R3 (IND ×2 152.8 + ADJ-OPP r02 65.7) | 218.4 |
| **rung total** | **824** (P90 ≈ 1.1k); position **≈ 3,809** (13.5 %) |
| then S2 (b) (21 frozen 1M fits + ONE N 10⁴ + D + comp) | 9,854 → **13.7k** (48 %); +25 % on the unspent 1M items 16.1k (57 %) |
| + H-34 20 seeds (6,335) | 20.0k (71 %); 24.0k (85 %) |
HQ's 813 is the 10 fits + the twins; the restart test is the only addition (+11). The rung quote does **not** depend on the island factor f: it is the measured N 10⁴ per-fit cost; the **twins at 60 use f = 2.53 (the conservative side)**. n400 and IND are unmeasured at 10⁵; R1's n400 pilot re-quotes the rest before R2.

## 8. Open items and things not verified
1. **NOTS retention** of `scratch/runs/GB_G1a/5-AR-n200-r01-V-s1/{data,setup,calib}.bin` (T6's inputs): not checkable from Owls; the fallback `RG_T6b` is generated and verified.
2. **n 400 and IND costs at 10⁵ are unmeasured** (n400 = 1.0× AR, IND = 1.0× AR): R1's `RG_1a` and R3's first IND fit re-fit the soft lines and the next quotes; the hard lines (190) are pinned. The 10⁴ leg measured n400 at 0.77× and BLK at 1.31× its n200 cost, so a 1.3× surprise is possible and covered by the P90.
3. **T6's cost and wall are an estimate** (T6's measured ratio at N 2,500 scaled to the G-B islands wall); N 10⁴ checkpoint size and write time are not measured at 10⁵. The 60-s cadence is a guess that must produce ≥ 2 checkpoint generations before ≈ 440 s and a later write: INVALID (not FAIL) if the island ends first.
4. IND's setup tables are larger than AR's (WP3's 10⁶ table: setup inputs 8.86 vs 6.78 GiB); measured at 10⁵ on Owls with real inputs: `setup.bin` 1.23 GB (AR n200 1.00, AR n400 0.95), setup RSS 1.67 GiB, and the plans for IND (island 3.74, calibrate 8.77, merge 4.84 GiB) clear the requests (§2). The 10⁵ **runs** of n400 and IND are the first measurements of their peaks.
5. `rung_d123.py` D2 compares means of 5 and 3 independent datasets with no tolerance: close to a coin flip for a small true rise (Opus G-B F2 note); HQ ruled it verbatim.
6. The G-C kill rule (pilot calibration > 2× its model; an island > 2× at 50 %) belongs to the 1M plan; the rung's hard lines are the 2.5× of §3.
7. Scripts to record at the commit (below): `make_rung_plan.py`, `rung_d123.py`, `rung_readback.py` and their tests; the G-B scripts are unchanged.

## 9. Files and sha256
`results/rung1e5/`: `RUNG_PLAN.md`, `make_rung_plan.py`, `rung_d123.py`, `rung_readback.py`, `tests/` (`test_rung_d123.py`, `test_rung_readback.py`), `presubmit/` (`plans/`, `plans.sha256`, `waves_rung.json`, `make_rung_plan_output.txt`, `memplan/`), `tools/` (`rung_quote.py`, `rung_quote_output.txt`). Unchanged and registered: `results/gb/gb_readback.py` `870a610a…`, `gb_imax_rule.py` `76927ae2…` (not used by the rung).
| file | sha256 |
|---|---|
| `make_rung_plan.py` | `963ac386acc7294999e8d9e6022cbd423faa4b457d61ff1f3b308755381be54b` |
| `rung_d123.py` | `d80545da6ed5f26b0db87839fc10780428df7c099f747dd577f3bfc645e1c036` |
| `rung_readback.py` | `2c8c883a5f911b7ed4a64def3c926e4ab734b428aea4afb64176497ee94a5aff` |
| `tests/test_rung_d123.py` | `96bd013a6c878ca230c938d94c7b5582acc033cf562c472d2d9d45381b01e8ac` |
| `tests/test_rung_readback.py` | `f8578a619c1f1011c687792f9b25276d539b06b667e15e8aed1ccfa4be12a338` |
| `tools/rung_quote.py` | `a161b742ad53f36900209d44a2d6be4da2ed6c9465c2ac007098ae00b2e806fa` |
| `tools/rung_quote_output.txt` | `a69d7c9fb4a94d97ca39ae0f05706a9c9a7a2c769f94569fa19a5472d1755193` |
| `presubmit/plans.sha256` | `5c1810e6fa12c112e837787770e9efc1e466b34163d4cc8ebb85634c0a9f65d4` |
| `presubmit/waves_rung.json` | `b1295a87af7e13c341706c9f0406621f61f60bc28a5bf42ac60c0c1c814924b3` |
| `presubmit/plans/RG_1a.json` | `8afd032be857e4594b7f41e0373b4e6f8b47abd32bb58f0058215dc6a8fbc169` |
| `presubmit/plans/RG_1b.json` | `fced26b338d20e627df33ac7abb2b377f8356ebf8c4ff0e321987db517674bf5` |
| `presubmit/plans/RG_2a.json` | `5b02cead1e29dbfb2225cda7680b49c1622cccf84dd9efa1525b96be3be98572` |
| `presubmit/plans/RG_2b.json` | `475e81a94ad7f9c55821ce56c9f0fc4e152ae43fc3b0381e1f0b4c8a9ca1c3ad` |
| `presubmit/plans/RG_3a.json` | `dd2a8da0da3e6978eb5774c56cdb1f8522d09fea085dfa86816f29915a3a050d` |
| `presubmit/plans/RG_3b.json` | `2387b19c2935328198edb24ac7edcd27fac5963675b09e47ca0fe11b51d6a719` |
| `presubmit/plans/RG_T6.json` | `91e53f900d8ffe7a798a1025bbb652941b20cb73309c72fcd0aa6d2ade86b527` |
| `presubmit/plans/RG_T6b.json` | `536a1e698b82866823eb9eb68b9f4ad8ade0f20bce791c6dd7821c1675f789ff` |
Nothing committed, nothing on NOTS, nothing under `/tmp`, no BNP file touched.
