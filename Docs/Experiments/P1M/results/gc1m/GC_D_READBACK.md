GC_D (OPTION D) READ-BACK VERDICT: **VALID, two items reported with it.** (1) Setup ended with sacct state **TIMEOUT** with complete, verified outputs (HQ 6ff8fb9e item 3): the scripted C3 reads FAIL on that state alone; every other criterion passes. (2) **`low_empirical_ESS` = TRUE: one island-stage, island 6 stage 3, ESS 232.8 = 0.093 N; harmless here; H-47 VERDICT: "could hit the n = 200 arm"** (an n = 200 F2 fit has had it: ADJ-OPP r04 at p 10⁴). **Cost 389.25 core-h = 0.358 × the plan value 1,087** (below the bottom-up range 490–1,060).

# GC_D_READBACK: option D, `6-AR-n1000-r01-V-s1` at 1M (F2, N 2,500, m 1, I_max 0, R′ 16, seed 602100001) (Engineering, Sonnet worker; Fri 2026-11-20)

**Status: ready for Opus check; pending manager commit.** Per GC_PREREG §5.1 (option D, registered) and GC_PLAN §3. The registered scripts ran **unedited** (`gc_readback.py` `63767ad3312ef580…`, importing `gb_readback.py` `870a610a…`; run with `--records` scoped to `records/gc1m/GC_D` ONLY, one fit found: Opus B1). Descriptive, unregistered helpers (all in `readback_D/`, sha §13): `pip_read.py`, `ess_read.py`, `ess_many.py`, `sec_any.py`, `ess_summary.py`. **NOTS use (read-only, as the manager's message allowed):** only `ssh nots` seek-reads of small sections (`st_ess`, `st_phi`, `st_inc`, `st_distinct_*`) of island files (the 16 D islands and 9 other fits' islands, `nice -n 19`, each section hash-verified); no job touched, no full verify, nothing written to `scratch/` or the runs. **One slip, disclosed:** my first ssh call also wrote my own 1 KB script to NOTS `/tmp/ess_read_fb31.py`; I removed it at once (checked: absent). Scratch (Owls) `~/SMC_Engineering_Department/tmp/20261120-gcdrb/`, removed at the end.
Inputs: `records/gc1m/GC_D/{6-AR-n1000-r01-V-s1,_batch_GC_D}` (sha-verified by ops: 2 units, 0 problems; 12 GB), `staging/gc1m/prior_after_D.json` (389.25), `_batch_GC_D/{sacct_dump.txt,ends.jsonl,starts.jsonl,cost/}`, `OPS_GC.md`; the pilot `records/gc1m/GC_P/` (islands included), the 11-17 fit `records/hygiene_1117/group3/runs/F1M_pilot/…` (islands), and for the ESS comparison the islands of nine more fits on NOTS `scratch/runs/` (§5.4). Engine source: tag `p1m-freeze-F2` (e993ece2), `include/v4/merge.h`, `src/island/island_run.h`.

## 1. Summary for HQ (≤ 12 lines)
1. **Option D completed and reads VALID.** C1 **389.25** core-h (0.358 × 1,087; soft 1,631, hard 2,718, wave line 2,174); C2 PASS (M1 0.01169, M2 0.000114, evidence gap 0.0025 ≤ 0.0249, HPM certified, PIP agreement 0.0006 ≤ 0.0609); C4 delivered (F2 `da0cf85b…` in 25 of 25 sidecars; arm 2,500 / 1 / 0 / `I_used` 0 / bounded); no kill rule tripped (calibrate 17.84 ≤ 70, 669 s ≤ 45 min; slowest island 738 s ≤ 3,600 s). **C3: the script says FAIL on one reason only: setup's sacct state TIMEOUT** (§3, §4); process peaks merge 24.65 GiB (of 128), setup 18.12 GiB (of 64), no OOM.
2. **Setup deviation (HQ 6ff8fb9e item 3):** TIMEOUT at 6,307 s (limit 1:45) with `status: completed` outputs written 1 s earlier; `ends.jsonl` setup line missing; `info --verify 1` by the manager: `content_sha256 fd873022…` = sidecar, 37 of 37 sections verify; calibrate accepted it (§4).
3. **H-47, low_empirical_ESS TRUE:** from the island section `st_ess` (merge.h l.346 / l.486): **one island-stage of 320 below 0.5 N = 1,250: island 6, stage 3 (φ 0.488 → 0.581), ESS 232.8** (0.093 N). It **recovered at once** (stage 4 ESS 2,499.7, distinct-after-move 543 against 577 in island 5). Effect on the fit: island 6's log Ẑ_r is the highest of 16 (+0.08, 3.5 sd of the other 15): it moves log Ẑ by +0.0054 and σ̂ from 0.0238 to 0.0310; |log Ẑ − log Ẑ_occ| 0.0025, M2 0.000114: not material. **Not n = 1,000-specific:** an n = 200 F2 fit (ADJ-OPP r04, p 10⁴) has two island-stages below 0.5 N (min 0.344 N) with E2 and σ̂ 1.34; the flag census: n 100 5 of 44, **n 200 1 of 170**, n 400 0 of 38, n 800 1 of 20, n 1,000 1 of 1 (§5). **Verdict: could hit the n = 200 arm.** The pilot's own islands: minimum ESS 0.667 N, none below.
4. **n-scaling of cost (D / pilot):** setup ×6.83 (84.09 vs 12.32; the correlation pass 5,591 s vs 626 s), calibrate ×1.10, **islands ×0.86 (259.81 vs 302.93)**, merge ×1.93, eval ×2.68; total ×1.126. The islands are cheaper because the final grid has **T 20 not 27** (+ L 10, Hm 4: 34 steps against 39): D's start law is already at posterior size (mean |S| 6.43 at φ = 0 against 3.46 at n 200) so the pilot bridges in 14 steps, not 20 (§6a). The merge's own timeline is the same as the pilot's (1,006 vs 1,027 s); the extra ≈ 1,500 s of stage wall sits **before the engine's timeline starts** (§6b, not resolved).
5. **π̂(S₀) 0.663** (terminal occupancy 0.663), HPM = MPM = S₀, the five true PIPs 1.0 to double precision, max null PIP **0.0165** (eq) / 0.0158 (T) at column 100,526, null counts above 0.1: 0 / 0 / 0; log Ẑ −767.4737; σ̂ 0.0310 (§7).
6. **Envelope re-based on D's measured cost (§10):** spent 4,353.02; position **13,047 (46.1 %)** at the committed class values, **13,537 (47.8 %)** if the unit is re-fit from the pilot; with the 25 % reserve on the unspent 15,220 / 15,833; with the seeds 19,241 / 20,104; the worst stack with reserve on everything unspent **22,963 (81.1 %) / 24,042 (85.0 %)** ≤ 28,300.
7. **Next steps (stated, not started):** HQ's classification of the ESS flag; the two-thread-count check (GC_T2THR job 2820415, submitted 23:50:29Z, result pending); W1 after HQ's classification; D's optional A++ exception (islands and `calib.bin` still on NOTS) is HQ's choice.

## 2. Verification of the inputs
| item | check | result |
|---|---|---|
| scripts | `gc_readback.py` `63767ad3312ef580…`, `gc_identity.py` `6842354256c47a49…`, `gb_readback.py` `870a610a…` = GC_PREREG §1 | ✓, run unedited |
| records | one SHA256SUMS per unit; ops verified 2 units, 0 problems; run unit 77 files; sidecar `inputs` hashes are consistent (islands' `setup.bin` `fd873022…` = setup sidecar = the manager's verify) | ✓ |
| ledger | my sum of `sacct_dump.txt` / the cost record: 84.0933 + 17.84 + 259.8133 + 26.9067 + 0.5956 = **389.2489**; `prior_after_D.json` 389.25 | ✓ |
| fits found | `gc_readback.py --records records/gc1m/GC_D --cost-dir records/gc1m/GC_D/_batch_GC_D/cost`: **1 fit** (the identity step is not run, §3.1) | ✓ |
| engine | `st_ess` section and rule re-read in the F2 tag source (merge.h l.313 `ess_all`, l.346 insert of `I.ess`, l.486 flag; island_run.h l.779 the ESS) | ✓ |

## 3. The option-D verdict (GC_PREREG §5.1)
`readback_D/gc_readback.json` / `.md`. **Valid iff** all five stages COMPLETED, C2 as §4, C3 on the process basis, C4, no kill trip (the setup state: §4).
| # | criterion | registered condition | measured | verdict |
|---|---|---|---|---|
| **C1** | cost | soft 1,631 · hard 2,718 (E 1,087; wave line 2,174) | **389.25** (ratio **0.358**) | **OK** |
| **C2** M1 | ≤ 0.05 | `fit.meta.occ[M 1,000].sd_log_Z_occ_r` | **0.011692** | PASS |
| M2 | ≤ 0.005 (`target_met`) | `pip.island_spread.max_sd` | **0.00011390** (2.3 % of the bar; `target_met` true) | PASS |
| evidence | \|log Ẑ − log Ẑ_occ\| ≤ 3√(se_Z² + se_occ²) | | **0.002527** ≤ **0.024883** (10 % of the bound) | PASS |
| HPM certified | `local_certified` | True, certified by both | PASS |
| PIP agreement | max_j \|PIP_eq − PIP_𝒯\| ≤ 0.01 + (1 − π̂(𝒯)) | **0.000623** ≤ **0.060923** (π̂(𝒯) = 0.9491) | PASS |
| reported | M3 = σ̂ = sd(log Ẑ_r) (goal ≤ 0.5) | **0.031049** (robust 0.023053; R_eff / R′ 0.99907; max − median 0.0856; max W 0.0676) | met |
| **C3** | process basis: no OOM, no stage not COMPLETED, process peak < request | script: **FAIL**, `not_completed: ["setup"]` (sacct TIMEOUT; §4). Process peaks: merge **24.65 GiB** < 128 G, setup **18.12 GiB** < 64 G; `process_over_request` empty; sacct ≤ 70.3 % of any request (islands, against the original 64 G; 56 % of the 80 G actually requested), no ADVISORY ≥ 80 % | **FAIL by the letter (setup state), no OOM, peaks far below the requests** |
| **C4** | delivered | 4 stage groups COMPLETED + the setup (TIMEOUT, §4); `logZ_r` length 16, finite; `binary.sha256` = `da0cf85b…` in **25 of 25** sidecars; recorded arm N 2,500, `refine_m` 1, I_max 0, `I_used` 0, rule bounded (`calib_meta.json`) = plan | holds |
| kill rule (D, §5.1) | calibrate billed > 70 core-h or > 45 min; an island > 60 min while the others have finished; fit > 2,718 | calibrate **17.84** core-h, **669 s**; slowest island **738 s**; fit **389.25** | **no trip** |
Final flags: E1 / E2 / E3 False, `occ_inhomogeneous` False, `sd_logZ_r > 1` False, `final_local_limit` False, **`low_empirical_ESS` TRUE ⇒ `checks_passed_final` FALSE** (§5); calibration `grid_unconverged` True and `I_used` 0 (as the pilot's). The `low_empirical_ESS` / `checks_passed_final` flags are **not named** in GC_PREREG §4's gating or "reported, not gating" lists (§5.6).
### 3.1 Identity
Option D is a **new dataset with no reference fit**, so `gc_identity.py` (which needs `--old`) was **not run**, and the monitor reported no data reference hash. The data content is recorded (`truth.json`): `X_sha256` **`7e0107aea7fae9de82d9f8930052db07a8bbec0b96d4e35cc6d3cf0f59eb4f0d`**, `y_sha256` **`28ed3a2e6fc542bed5ebbc458161f0014978a4e324afb0fb71580200fe27dc7a`**, generator `smcbvs4.gen/1`, spec AR ρ 0.6, b 20, s₀ 5, a 1, σ 1, n 1,000, p 10⁶, seed 602100001; S₀ {100000, 300000, 500000, 700000, 900000}, β (1, −0.8, 0.9, −0.7, 0.6); raw content hash `6870040b…`; `data.bin` `e190e64d…`. Setup counts (sidecar): J **78,286**, C **692,367,872**, B 16, B_blocks 14, mode_size 6, partition truncated, file_mode V. The sizes-only memory plan used WP2 count-only sizes J 78,261 and B 16: **B equal, J +25 (+0.03 %)** (the pilot's analogue: 74,726 → 74,734). The same data and setup entered all 16 islands (their `inputs` hashes are identical).

## 4. The setup deviation (HQ 6ff8fb9e item 3; reported with every "all stages COMPLETED" line)
- **What happened (from `OPS_GC.md`, `starts.jsonl`, `ends.jsonl`, the sacct dump):** setup 2817052_1 (48 CPU, 64 G, limit 1:45) started 19:49:41Z and was killed by its limit at **6,307 s** (billed 302,736 CPU-s = **84.09 core-h**, sacct state **TIMEOUT**). Its work was complete 1 s before the kill: `log/setup.log` status completed, `setup.bin` 9,217,428,672 B and `setup.bin.json` (status completed, binary sha256 = F2) written 21:34:45Z; the sidecar's stage seconds sum to 5,972 s (correlation **5,591.5**, tables 294.7, start_law 70.4, partition 12.7, start_mode 2.9) plus data generation and write. **The closing `ends.jsonl` line for setup is missing** (written after the `setup` command); Slurm cancelled the four dependants (0 core-h).
- **Integrity check (the manager's):** the F2 binary `smcbvs4 info setup.bin --verify 1` on NOTS: `verified: true`, rc 0; `content_sha256` **fd8730222abd4ddeed1af04e00a7b75ff5ba5570e395a06332b8fabd9ab2abc8** = the sidecar's `outputs` hash; header `file_bytes` = the on-disk size 9,217,428,672 B; all 37 section sha256s verify. (The sidecar hash covers the header and the section table; the whole-file sha256 `046e0137…` is not comparable.)
- **How D continued (option B, HQ-approved):** `gc_resume_after_setup.sh` resumed the same batch from `setup.bin`: calibrate 2819032 → islands 2819033 (16 tasks) → merge 2819034 → eval 2819035, the same stage scripts and graph as `submit.sh`, with the HQ limits as sbatch overrides (calibrate 2:00, islands 2:30 and **80 G**, merge 3:00, eval 1:00). **Calibrate accepted `setup.bin`** (`calib_meta.json` `inputs.setup.bin` = `fd873022…`; every island and the merge the same).
- **How it is counted:** the 84.09 core-h of the TIMEOUT setup is **in** the fit total 389.25 (one setup, no re-run, no double count); the cost record keeps `states: ["TIMEOUT"]` for setup.
- **Consequence for the criteria:** the scripted C3 reads FAIL only because setup's sacct state is TIMEOUT (`not_completed: ["setup"]`); C4's "all 5 stage groups COMPLETED" is met for four and, for setup, by the deviation above. **The deviation does not touch the science:** the setup output is hash-identical to its sidecar and every downstream artefact records the same hash. The need for the deviation is the 1:45 limit: the measured setup work was ≈ 6,306 s, i.e. 1.00× the limit and 1.53× the bottom-up 69 min (§6): the limit was set from the WP2 count-only estimate (4,069 s at 3 threads).

## 5. H-47: `low_empirical_ESS` = TRUE (checks_passed_final FALSE): locate and classify
### 5.1 Where the flag comes from (engine, tag F2)
`low_empirical_ESS` is set in `include/v4/merge.h` l.486: `for (double e : ess_all) if (e < 0.5 * ms.N) out.low_ESS = true;` (N = the island's particle count, 2,500, so the line is **1,250**). `ess_all` (l.313) collects `I.ess` of every island as it is merged (l.346): **one value per island per bridge stage**, read from the island file's section **`st_ess`** (`island_run.h` l.779: at bridge stage t the incremental weights are w_i = exp(Δφ_t · d_i) over the N particles **before** the resample, and ESS_t = (Σw)² / Σw²; the stage is then resampled and moved). The island loader rejects any value outside [0, N]. The flag is therefore *any single island-stage whose weights, before resampling, were more concentrated than ESS 0.5 N*. `checks_passed_final = !(E1 || E2 || E3 || low_ESS)`.
### 5.2 Which island(s), which stage(s), the minimum (all 16 D islands × 20 stages = 320 values; `readback_D/ess_D.json`)
- **Exactly one value is below 1,250:** **island 6, stage 3** (φ 0.4866 → 0.5814, Δφ 0.0949), **ESS 232.8 = 0.093 N** (the ESS sequence of island 6: 2,202, 2,431, **233**, 2,500, 2,495, 2,268, …). The other 319 values: minimum **2,001** (0.80 N, island 7 stage 19), the 15 other islands at stage 3 lie in 2,471–2,483; the typical stage sits at ≈ 2,250 (the 0.9 N the grid is built to).
- **What it is (inference from the stored numbers; the particle weights are not stored):** the stage-3 incremental log-evidence of island 6 is 24.5276 against 24.4639 (the mean of the 15 others, sd 0.0021): +0.0637. One particle of weight w₁ against N−1 of weight 1 gives ESS = (N−1+w₁)²/(N−1+w₁²) = 232.8 for **w₁ ≈ 167** and a log-evidence excess of log(1 + w₁/N) = **0.0645** (observed 0.0637): **one dominant particle, ≈ 6.3 % of the stage's weight, ≈ 54 deviance units above the rest at Δφ 0.095** (a rare, better model found by one particle at that stage), consistent with both numbers.
### 5.3 Did the next resample-move recover it? **Yes, at once.**
Resampling resets the weights: stage 4 of island 6 has ESS **2,499.7**, stage 5 2,495.4; the distinct-particle counts after the stage-3 resample / after the move are 331 / 564 in island 6 against 375 / 583 in island 5 (and 331 → 344 → 356 over the next stages): the clone group (≈ 6 % of the particles) is re-diversified by the moves; nothing persists in the later stages. The grid is fixed, so a stage's ESS depends only on that stage's particle cloud.
### 5.4 Is it specific to n = 1,000? **No.** Evidence (`readback_D/ess_summary.txt`; ESS from the `st_ess` sections; N 2,500 except the 10⁵ fits, N 10,000)
| fit (build) | islands × T = stages | min ESS (min / N), where | island-stages < 0.5 N |
|---|---|---|---|
| **GC_D** 1M n 1,000, N 2,500 (F2) | 16 × 20 = 320 | 232.8 (0.093), island 6 stage 3 | **1** |
| GC_P pilot, 1M n 200 (F2) | 16 × 27 = 432 | 1,666.9 (0.667), island 11 stage 22 | 0 |
| 11-17 fit, 1M n 200 (I_max 3) | 16 × 27 = 432 | 1,668.2 (0.667), island 11 stage 22 | 0 |
| **`4-ADJOPP-n200-r04-V-s2` (V-N V0), p 10⁴, n 200, N 2,500 (F2)** | 16 × 23 = 368 | **859.1 (0.344)**, island 11 **stage 3** | **2** (island 11 stage 3: 859; island 13 stage 18: 1,227) |
| eight 10⁵ F2 fits (AR n 200 ×2, ADJ-OPP n 200 ×2, IND n 200 ×1, AR n 400 ×3), N 10,000 | 8 × 16 islands, 2,096 stages | 0.60–0.85 (IND 0.602; the rest 0.80–0.85) | 0 |
- **The n = 200 precedent in detail** (`V0/4-ADJOPP-n200-r04-V-s2`, F2 build `da0cf85b`, 10⁴): `low_empirical_ESS` TRUE **and E2 TRUE**, σ̂ **1.34** (robust 0.94), R_eff 3.4 of 16, max W 0.52, log Ẑ −227.23 against log Ẑ_occ −227.54; HPM = S₀. Its two low-ESS islands are the two **extremes** of the evidence (island 11 log Ẑ_r −225.12, the highest; island 13 −231.05, the lowest; the median −227.9). The mechanism is the same as D's (island 11, **stage 3** again, ESS 859), but that fit is a hard design (ADJ-OPP) whose between-island evidence spread is large for its own reasons (E2).
- **Census of the flag over all 273 `eval.bin.json` under `records/`** (all builds; some fits appear in more than one directory, e.g. the 11-17 fit three times): n 100: **5 of 44** (older build `d0c30b65`: AR-weak ×3, IND ×2); **n 200: 1 of 170** (p 10⁴ 1 of 153, p 10⁵ 0 of 14, p 10⁶ 0 of 3); n 400: 0 of 38; n 800: 1 of 20 (older build); **n 1,000: 1 of 1**. F2 build only: 2 of 34 fits, **1 of 30 at n 200**. No monotone trend in n; the flag is rare, appears at n 100, 200, 800 and 1,000, and not at n 400 (38 fits).
### 5.5 Are the evidence or the PIPs affected? **No, not materially (D).**
- σ̂ **0.0310**; the 15 islands without the event: sd **0.0238**. Dropping island 6 moves log Ẑ from −767.4737 to −767.4791 (the event shifts it by **+0.0054** = 0.7 of the fit's s.e. σ̂/√16 = 0.0078). |log Ẑ − log Ẑ_occ(M 1,000)| **0.0025** (the bound 0.0249); M1 **0.0117**; **M2 0.000114** (the largest island-to-island PIP sd over the 10⁶ variables; the bar 0.005); the PIP agreement 0.0006; HPM certified, = S₀.
- Island 6's log Ẑ_r (−767.396) is the highest of the 16 (z = +3.5 against the other 15): a heavy right tail of one island's estimate, which the combination Ẑ = mean over islands absorbs (weight W₆ 0.0676 against the 1/16 = 0.0625 average).
### 5.6 Registration note (for HQ's ruling, not applied)
GC_PREREG §4 gates C2 on M1, M2, the evidence gap, HPM certification and the PIP agreement, and lists "final E1–E3, `occ_inhomogeneous`, sd(log Ẑ_r) > 1" as reported, not gating; **`low_empirical_ESS` and `checks_passed_final` are in neither list** (`gc_readback.py` reports them in its C5 block). On the evidence above the clean reading is **reported, not gating, judged by σ̂, the evidence gap and M2** (as in §5.5). Stating that line for W1 and the block is HQ's call.
### 5.7 VERDICT LINE (H-47)
**"could hit the n = 200 arm."** (It is not n = 1,000-specific: an n = 200 F2 fit has had it, at the same stage 3, with a larger effect because that design is harder; the rate at n = 200 is 1 of 170 fits (1 of 30 on F2); at 1M n = 200 the two fits so far (pilot, 11-17) have a minimum ESS of 0.667 N, and none of the 17 fits at n 200 with p ≥ 10⁵ has had it. W1 contains an ADJ-OPP fit at n = 200, the design of the precedent. At D it changed neither the evidence (+0.005) nor the PIPs (M2 0.0001).) The flag stays reported with D and is not dropped.

## 6. The two HQ notes
### (a) Final-island T = 20 against 27: why
- **The measured cause is the start law.** At φ = 0 the calibration pilot's mean model size is **6.43 at n = 1,000 against 3.46 at n = 200** (cost files, step 0; the posterior size at φ = 1 is 5.4 and 6.3). The adaptive pilot targets the same ESS at every step (island stage 1 ESS 2,236 at n 1,000, 2,260 at n 200; both ≈ 0.9 N), but at n = 1,000 the first step is **Δφ 0.301 against 0.041 (7.4×)**: the start law π₀ (built in `setup.bin` from the screening: `start_law` 70 s) already concentrates the particles on models of the final size, so the weights' spread is small and the pilot reaches φ = 1 in **14 steps instead of 20** (the pilot's bridge-step counts: 14 / 20). The final grid has 21 points against 28: **T 20 against 27**, with burn-in L 10 against 8 and Hm 4 in both: **34 island steps against 39**.
- This is a data-dependent (n-dependent) schedule, not a build or configuration change: the same F2 build, `refine_m 1`, I_max 0, `H` 512, `ell` 20 and the same `rule bounded` / `grid_label preliminary` / `grid_unconverged` as the pilot's. The island cost scales with the 34 / 39 = 0.87 (measured islands ratio 0.858). **No check was made beyond these numbers** (the data-dependence of π₀ at other n is not examined).
### (b) Merge 50.5 min against 22–30: why (NOT resolved; located)
- Stage wall: D **3,027 s (50.5 min)**, pilot **1,566 s (26.1 min)** (ratio 1.93). **The engine's own phase timeline is the same:** from its `start` to `before_write` D 1,006 s, pilot 1,027 s (`eval.bin.json` `cost.fit_timings`: `merge_islands_seconds` 667 / 716, `merge_tail_seconds` 1,006 / 1,027; the 16 island merges 23–30 s each in both; `write_fit_seconds` 12.1 / 11.3). The merge's process peak is 24.65 / 20.88 GiB (`peak_rss_kb`).
- **So the excess wall is outside that timeline:** stage elapsed − (timeline + write) ≈ **2,009 s at D against ≈ 528 s at the pilot** (the timeline's `start` row already shows an 8.6 GiB (D) / 9.4 GiB (pilot) high-water mark: a pre-timeline phase of the process, before the first phase record). The manifest `fill` step took 2 s in both (`manifests/merge.json` mtime 2 s after the stage start), so it is not the python wrapper. Candidate contributors, **none verified**: the pre-timeline input read / check of `data.bin` (8.04 GB at D, 1.64 GB at the pilot), the shared-filesystem read rate at 22:24–23:14Z for the 61 GB of inputs (D) against 56 GB (pilot) at 16:55–17:21Z, and node differences. The eval stage shows the same shape (stage 268 s against 100 s; its engine timeline 66.8 against 30.1 s), which points the same way (the 8 GB `data.bin`).
- **Cost of it:** merge 26.91 core-h against the model's 17: +9.9; it does not move any line. Resolving it would need a re-run or a timestamped log; not proposed.

## 7. Science (descriptive; `readback_D/pip_D.json`, `eval.bin.json`)
| quantity | D (n 1,000, 1M) | pilot (n 200, 1M) |
|---|---|---|
| HPM / MPM | = S₀ {100000, 300000, 500000, 700000, 900000} (both) | = S₀ |
| F(HPM) − F(S₀); S₀ store rank; outcome | 0; 0; "correct" | 0; 0; "correct" |
| HPM found in | pilot phase, φ 0.3007, island 0, `gibbs_flip` | pilot phase, φ 0.0409 |
| log Ẑ; log Ẑ_occ (M 1,000); log Z_T | **−767.4737**; −767.4762; −767.5260 | −245.1099; −245.0946; −245.3878 |
| log Ẑ − log Z_T; π̂(𝒯) = Z_T/Ẑ | +0.0523; **0.949** | +0.2779; 0.757 |
| **π̂(S₀)** = exp(F_S₀ − log Ẑ) (terminal occupancy) | **0.6630** (0.6635) | 0.3203 (0.3174) |
| the five true PIPs (eq) | **1.0 (to double precision) for all five** | ≥ 0.99999982 |
| PIP_T on the true variables | 1.0000000000000338 (the unclipped ratio estimator) | ≥ 0.99999989 |
| max null PIP eq / T / Z (column) | **0.01647 / 0.01585 / 0.01647** (100,526) | 0.1064 / 0.0877 / 0.1064 (398,205) |
| null PIPs > 0.5 (eq / T / Z) | 0 / 0 / 0 | 0 / 0 / 0 |
| null PIPs > 0.1 (eq / T / Z) | 0 / 0 / 0 | 1 / 0 / 1 |
| Σ PIP eq / T; Brier eq | 5.421 / 5.330; 4.85 × 10⁻¹⁰ | 6.373 / 5.783; 1.68 × 10⁻⁸ |
| M1 / M2 / M3 (σ̂) | 0.01169 / 0.000114 / 0.03105 | 0.01707 / 0.00312 / 0.02830 |
| E1–E3, occ_inhomogeneous | False | False |
| `low_empirical_ESS` | **TRUE** (§5) | False |
| plug-in h² of HPM = MPM = oracle | 3.403 × 10⁻⁴ (ratio 1); store-law predictive h² 0.9954× the oracle's; test mse ratio 1.0001; store dropped mass 0.0225 | 5.22 × 10⁻³; 1.037× |
**π̂(S₀) 0.663 against the 10⁵ trend and the pilot.** The 10⁵ means at n 200 → 400 are 0.349 → 0.546 (RUNG_READBACK / GC_PREREG §5.1); the 1M pilot at n 200 is 0.320; **D at n 1,000 is 0.663**: the occupancy of the true model rises with n along both axes of the data (10⁵: n 200 → 400; 1M: n 200 → 1,000), as the option-D question asked. One dataset per point, p differs between the two series, no claim of a trend from these points. Alongside it the store captures more of the mass (π̂(𝒯) 0.949 against 0.757) and the null PIPs are an order of magnitude smaller (0.016 against 0.106).

## 8. Memory on the process basis (GC_PREREG §4 C3)
| stage (request) | **process peak** (where recorded) | sacct MaxRSS (page cache included) | % of request (sacct) | plan-only / pilot |
|---|---|---|---|---|
| setup (64 G) | **18.12 GiB** (`setup.bin.json` `peak_rss_mb` 18,551) | 33.07 GiB | 51.7 % | pilot 13.25 GiB process; WP2-based plan ≈ 13.5 |
| calibrate (128 G) | calibration-pilot high-water **58.8 GiB** (`cost_pilot` `hwm_kb`) | 58.94 GiB | 46.0 % | **plan-only 82.0** (0.72×); sidecar mem_plan 49.1 GB; pilot sacct 48.5 |
| islands (80 G, raised from 64 G) | not recorded | **44.98 GiB** (max of 16) | 56.2 % of 80 G (70.3 % of the original 64 G) | plan-only 42.9 (sidecar 42.8 GiB): **1.05×** by sacct (page cache counted); pilot 37.5 |
| merge (128 G) | **24.65 GiB** (`fit.bin.json` `peak_rss_kb` 25,848,300) | 71.73 GiB | 56.0 % | **plan-only 58.0** (0.43×); pilot process 20.88 GiB |
| eval (32 G) | not recorded | 10.99 GiB | 34.4 % | pilot 3.54 GiB (the 8 GB `data.bin`) |
**No OOM; every recorded process peak is far below its request; no sacct value at or above 80 % of the request actually used.** The merge process peak at n = 1,000 is 1.18× the pilot's (24.65 vs 20.88 GiB), so the 128 G request has 5.2× headroom and the 48 G fallback (90 % budget 43.2 GiB) 1.75×. The island sacct peak is the one near its plan (1.05×) and the reason the 80 G request mattered (the 64 G original would have been 70 %). C2 precision as §3.

## 9. n-scaling of cost by stage, D against the pilot (billed core-h from the cost records)
| stage | D billed / max wall | pilot billed / max wall | D / pilot | D bottom-up (GC_PLAN §3) | note |
|---|---|---|---|---|---|
| setup (48 CPU) | **84.09** / 6,307 s (TIMEOUT, work done) | 12.32 / 924 s | **×6.83** | ≈ 55 (69 min) | the correlation pass 5,591.5 s vs 625.9 s (×8.9): it does not scale with threads; measured 1.53× the bottom-up |
| calibrate (96 CPU) | 17.84 / 669 s | 16.24 / 609 s | ×1.10 | 30–60 | the calibration pilot reaches φ = 1 in 14 steps (20 at n 200) |
| islands (16 × 96 CPU) | **259.81** (16.24 mean; billed 13.6–19.7) / elapsed 509–738, mean 609 s | 302.93 (18.93; 15.6–29.3) / 584–1,097, mean 710 s | **×0.858** | 380–920 (269 × 1.4–3.4) | T 20 vs 27, L 10 vs 8: 34 vs 39 steps (×0.87); **the cost per step is n-independent**, the planning model's 1.4–3.4 was not seen |
| merge (32 CPU) | 26.91 / 3,027 s | 13.92 / 1,566 s | ×1.93 | ≈ 22 | engine timeline equal (§6b); extra wall pre-timeline |
| eval (8 CPU) | 0.596 / 268 s | 0.222 / 100 s | ×2.68 | ≈ 1 | reads the 8 GB `data.bin` |
| **fit** | **389.25** | **345.64** | **×1.126** | **490–1,060** (plan value 1,087) | **0.358 × the plan value**; below the bottom-up floor, because the islands (and calibrate) did not scale as the planning factor |
**Reading.** From n 200 to n 1,000 the fit cost grows 12.6 %: the setup (+71.8 core-h), the merge and eval (+13.4) and calibrate (+1.6) grow, the islands shrink (−43.1); a **second n = 1,000 fit on the same data would not pay the setup again** (if the same `setup.bin` is reused: 389.25 − 84.09 = 305.2). All five D stages are inside the committed lines (soft 1,631, hard 2,718); no stage was near its own K line (calibrate 25 % of 70; islands 20 % of 3,600 s).

## 10. The envelope re-based on D's measured cost (GC_PLAN §7; arithmetic only, nothing applied)
Closed 3,618.13 + pilot 345.64 + D 389.25 = **4,353.02 spent** (`prior_after_D.json` 734.89 = the two). Remaining items: AR replicates 2–20 (19), ADJ-OPP r01, AR-weak r01 (gated), the ONE N 10⁴ fit, ablations + competitors 1,052 (plan values); the seeds 19 × unit. **Reserve now applied to the unspent items only** (the previous table applied it to the whole S2 block).
| | committed classes (326 / 339 / 326 / 783) | re-fit from the pilot only (345.64 / 359.4 / 345.64 / 860; `readback/refit_sensitivity.txt`) | the previous table (D at 1,087) |
|---|---|---|---|
| unspent S2 items + ablations | 7,642 + 1,052 = 8,694 | 8,132 + 1,052 = 9,184 | |
| **position** | **13,047 (46.1 %)** | **13,537 (47.8 %)** | 13,725 (48.5 %) |
| + 25 % on the unspent | 15,221 (53.8 %) | 15,833 (55.9 %) | 16,252 (57.4 %) |
| + H-34 seeds (19 × unit) | 19,241 (68.0 %) | 20,104 (71.0 %) | 19,919 (70.4 %) |
| + 25 % on all unspent incl. the seeds | **22,963 (81.1 %)** | **24,042 (85.0 %)** | 23,994 (84.8 %) |
All ≤ 28,300. D came in 697.8 below its plan value; the pilot was 19.6 above its class value; net **−678** at the committed classes. The projection ceiling and the cumulative lines (S2 14,500, seeds 9,900) are untouched. **Not applied:** the class-mean re-fit (soft line 518 for the AR unit, W1 quote ≈ 705, wave stop ≈ 1,410: §4 of GC_P_READBACK), the S2 / hygiene accounting, any retention change. A D-based n-scaling is **not** a class mean for the n 200 block (D is one fit at another n).

## 11. Next steps (stated, not started)
1. **HQ's classification of the ESS flag (§5.7) and the registration line for `low_empirical_ESS` (§5.6)**; W1 (AR r02 + ADJ-OPP r01; committed quote 665, stop 1,330; the §10 / GC_P_READBACK §4 re-fit is the manager's call) waits on it.
2. **The two-thread-count check** (GC_T2THR, HQ H-47; report-only): job 2820415 (one pilot island at 48 threads against the pilot's 96, bit-for-bit), submitted 23:50:29Z, running; the result is **pending** (`tools/gc_t2thr_compare.py` → `records/gc1m/T2THR/t2thr.json`); a FAIL is reported, not a stop.
3. **D's retention:** classes A + A+ kept (fit, eval, law, `setup.bin` 8.6 GB, sidecars); the 16 island files (35.3 GB), `calib.bin` (8.5 GB) and `data.bin` (8.0 GB) remain on NOTS; whether D takes the optional A++ exception (island files and `calib.bin` kept until the block read-back) is HQ's choice. `gc_seeds.py` after W2's read-back (sha frozen before any seed-block fit).

## 12. Not done / limits
No NOTS job touched, no full verify of any island, no engine run; the `st_ess` reads on NOTS are small seeks (one stray `/tmp` file of mine on NOTS removed, §header). The identity gate was **not** run (no reference for the new dataset); the particle-level cause of the stage-3 ESS dip is an inference from `st_ess` and `st_inc` (weights not stored); the merge's pre-timeline excess is located, not explained (§6b); the start-law explanation of T 20 is measured at φ = 0 (mean |S|), not tested at other n; the ESS census is over the fits on this desktop (273 `eval.bin.json`, with duplicates), not over every fit ever run, and the n 100 / 800 events are older builds; one dataset, one seed. The registered test failure (`test_real_11_17_record_parse`) of the pilot read-back is unchanged and unrelated (this run's `--records` is scoped to `records/gc1m/GC_D`).

## 13. Files and sha256
`results/gc1m/readback_D/` (not committed): `gc_readback.json`, `gc_readback.md`, `gc_readback_stdout.txt`, `pip_read.py`, `pip_D.json`, `ess_read.py`, `ess_many.py`, `sec_any.py`, `ess_summary.py`, `ess_summary.txt`, `ess_D.json`, `ess_others.json`, `ess_local.json`, `sec_sel.json`, `eval_flags_all.json`.
| file | sha256 (first 16) |
|---|---|
| `gc_readback.json` | `8b8a9f72d28b3de9…` |
| `gc_readback.md` | `61908596dd22b23c…` |
| `gc_readback_stdout.txt` | `f631f47460205497…` |
| `pip_read.py` | `0a93d61a827d580b…` |
| `pip_D.json` | `72711878ff77a402…` |
| `ess_read.py` | `81282d38c1145fc4…` |
| `ess_many.py` | `a0df52b723c3ae83…` |
| `sec_any.py` | `f623935064075d96…` |
| `ess_summary.py` | `9631f46deedb8e88…` |
| `ess_summary.txt` | `3a793d6c8ea66db5…` |
| `ess_D.json` | `56dbe3f68e47cdb8…` |
| `ess_others.json` | `8066ce6a2c1d65c5…` |
| `ess_local.json` | `f81381294d821713…` |
| `sec_sel.json` | `847441ce7213a645…` |
| `eval_flags_all.json` | `5385c0be59100fb2…` |
Commands: `python3 -I gc_readback.py --records ~/SMC_Engineering_Department/records/gc1m/GC_D --cost-dir ~/SMC_Engineering_Department/records/gc1m/GC_D/_batch_GC_D/cost --out readback_D`; `python3 -I readback_D/pip_read.py <fit.bin> <truth.json> readback_D/pip_D.json` (the registered reader `compare_overlap_v2.py` `4f402e51…`, unedited); ESS: `ssh nots 'cd ~/SMC_Engineering_Department/scratch/runs && nice -n 19 python3 -I - <island files>' < readback_D/ess_read.py` and `ess_many.py <run dirs>` (stdin script; seeks only); `python3 -I readback_D/ess_summary.py > ess_summary.txt`.

## 14. Points for the Opus checker
1. **The verdict:** re-derive C1 (sacct dump sum 389.2489), C2 (`eval.bin.json`: M1, M2, gap and bound, `local_certified`, `eq_T_target_met`), C3 on the process basis and **the reason the script says FAIL** (`not_completed: [setup]` only), C4 (25 of 25 sidecars F2), the kill rule at D's lines (70 core-h / 45 min / 3,600 s / 2,718).
2. **The setup deviation text** against `OPS_GC.md` (TIMEOUT 6,307 s, 84.09, the missing `ends.jsonl` line, the manager's verify, option B), and that the 84.09 is counted once.
3. **H-47:** the F2 source lines (merge.h l.313 / 346 / 486, island_run.h l.779); the single value 232.8 at island 6 stage 3 (re-read `st_ess` of `island_6.bin` on NOTS); the one-particle arithmetic (w₁ ≈ 167, +0.0645 vs 0.0637, an inference); the recovery at stage 4; the effect numbers (+0.0054, σ̂ 0.0238 → 0.0310); the V0 ADJ-OPP precedent (859 at stage 3, E2, σ̂ 1.34); the census counts (273 evals, duplicates) and the verdict line "could hit the n = 200 arm".
4. **§6 (a)/(b):** the step-0 mean |S| (6.43 vs 3.46), first Δφ 0.301 vs 0.041, 14 vs 20 pilot steps; the merge timeline equality and the pre-timeline arithmetic (3,027 − 1,006 − 12 = 2,009 vs 1,566 − 1,027 − 11 = 528).
5. **§9–§10:** the n-scaling ratios and the envelope arithmetic (spent 4,353.02; 13,047 / 13,537).
6. **§3.1:** no identity reference for D (the `gc_identity.py` run is not possible), and the J +25 against the sizes-only plan.
7. **Not done:** §12.
