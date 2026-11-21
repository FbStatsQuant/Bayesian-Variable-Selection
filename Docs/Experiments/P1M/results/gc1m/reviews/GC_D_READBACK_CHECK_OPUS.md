# GC_D_READBACK check (Opus, the one check; read-only; Fri 2026-11-20)

**Under review:** `results/gc1m/GC_D_READBACK.md` sha256 `4a516d8fe63a360fcfa80e03987eb6b3ac61d6f7e48f4b0ae814884252735969` (exp/P1M worktree, uncommitted). The `readback_D/` file hashes match its §13.
**Sources re-read:** GC_PREREG §4, §5, §5.1; GC_PLAN §3 (option D) and `presubmit/memplan_D/pt_AR_n1000.out`; OPS_GC.md; DECISIONS H-46 / H-47; LOG; HQ 6ff8fb9e and cf3bf327 (main). **Records:** `records/gc1m/GC_D` (sacct dump, cost, starts / ends, sidecars, eval / fit json, cost_pilot), `records/gc1m/GC_P`, `records/vn_minileg/V0/4-ADJOPP-n200-r04-V-s2`, and `readback_D/*.json`. **NOTS:** one read-only `ssh nots` (head of `scratch/runs/GC_D/ends.jsonl`, plus `stat` and `ls` of the setup outputs). No job touched, no .bin read, nothing written outside this file.

## Verdict: **ACCEPT-WITH-FIXES**

"VALID" is correct under GC_PREREG §5.1 read with HQ 6ff8fb9e item 3. C1, C2 and C4, the kill rules, the location of the ESS event, the drop-one-island arithmetic, the T 20 / 27 numbers, the merge timeline and the envelope arithmetic all re-derive from the records.

The verdict line **"could hit the n = 200 arm" is the right reading**, and the evidence for it is stronger than the text says (F3, F4). Under H-47 it means **W1 stays stopped until HQ rules.**

One fix is required before commit (F1). The deviation statement repeats a false premise: the setup `ends.jsonl` line is **not** missing. F2–F4 sharpen the H-47 classification without changing it.

## Findings

**F1: MEDIUM-HIGH (fix before commit; the text HQ 6ff8fb9e item 3 requires). The setup `ends.jsonl` line is present.**
- *Evidence:*
  - `records/gc1m/GC_D/_batch_GC_D/ends.jsonl` line 1 reads `{"stage":"setup","run_id":"6-AR-n1000-r01-V-s1","job":"2817052","task":"1","end":"2026-11-20T21:34:45Z"}`. The NOTS original `scratch/runs/GC_D/ends.jsonl` has the same line 1, and the record's SHA256SUMS covers the collected copy.
  - Its format is exactly the last statement of `scripts/stage_setup.sbatch` (l.47, the printf after the `setup` command).
  - `sacct_dump.txt` shows `2817052_1.batch … COMPLETED|6307` (the batch step), with only the job row TIMEOUT.
  - `slurm_out/p1m_GC_D_setup_2817052_1.err` is empty, with no "DUE TO TIME LIMIT" message.
  - Start 19:49:41Z + 6,300 s = 21:34:41Z. The script wrote its end line at 21:34:45Z (6,304 s), and sacct ends at 6,307 s.
  - So the script ran to completion ≈ 4 s past the limit. Slurm marked the job TIMEOUT and, through `afterok`, cancelled the dependants. Nothing was killed mid-command.
- The "missing line" premise came from the ops note of 21:34:46Z: OPS_GC "setup TIMEOUT (STOP)" and the deviation log item (2). It went on into HQ 6ff8fb9e's "New fact" and into read-back §1 item 2 and §4 bullet 1, although the read-back lists `ends.jsonl` among its inputs. A likely cause is an early or stale NFS view 1 s after the write. No tool or log shows a hand edit; the resume script does not write `ends.jsonl`.
- *Fix:*
  - Replace "ends.jsonl setup line missing" in §1.2 and §4 with: "sacct **job** state TIMEOUT (6,307 s against 6,300 s), **batch step COMPLETED**; the stage script ran to its last line and wrote its `ends.jsonl` line at 21:34:45Z; the earlier statement that the line was missing (OPS_GC deviation item 2, HQ 6ff8fb9e) was wrong."
  - Keep the scripted C3 FAIL by the letter. It reads the job state, and that stays TIMEOUT.
  - Send HQ a one-line correction. This is not a re-ruling: it does not change option B or validity, and it strengthens the integrity case. Do not edit HQ's file.

**F2: MEDIUM. The census mixes N, and the reassuring clause over-claims.**
- *Evidence* (`eval_flags_all.json`):
  - All 8 TRUE fits are at **N 2,500** (8 of 225 records). At N ≥ 10,000 the count is **0 of 48**.
  - F2 at n 200 is 1 of 7 at N 2,500 and 0 of 23 at N 10,000.
  - "None of the 17 fits at n 200 with p ≥ 10⁵" (§5.7) counts 11 N 10,000 rung / G-B fits. At the frozen N 2,500 it is **0 of 6 records**: T5_1e5, RG_1b AR / ADJ-OPP VN25, and three 1M records (F1M_pilot twice plus GC_P), which are **one dataset**.
  - The §5.4 table also compares D with eight N 10,000 fits. A single dominant particle weighs ¼ as much there.
- *Fix:* stratify §5.4 / §5.7 by N. State that the frozen arm's N is the only N at which the flag has ever appeared. Replace "1 of 30 F2 at n 200" with "1 of 7 F2 at N 2,500, n 200 (0 of 23 at N 10,000)".

**F3: MEDIUM. The n = 200 precedent is on the exact frozen arm, and its harm is under-described.**
- *Evidence:*
  - `V0/4-ADJOPP-n200-r04-V-s2` `calib_meta.json`: N 2,500, `refine_m` 1, I_max 0, `I_used` 0, rule bounded, F2. Same build, same arm, same n as W1; p is 10⁴.
  - Its two flagged islands are the two evidence extremes (island 11, the highest at −225.12; island 13, the lowest at −231.05; median **−227.98**, not −227.9).
  - It had E2 TRUE and σ̂ 1.34 (robust 0.94), R_eff 3.4, max W 0.52.
  - **Every C2 gate would still pass:** M1 0.0094, M2 0.00049, gap 0.31 ≤ bound 1.01, `local_certified`, `eq_T_target_met`, HPM = S₀.
  - The read-back's "a larger effect because that design is harder" / "large for its own reasons" is not shown by anything in the records.
- *Fix:* say so plainly. At n = 200 on the frozen arm, the flag has co-occurred with σ̂ 1.34 (2.7× the 0.5 goal) while selection, PIPs and all registered gates held. Whether the ESS event caused the spread is not determined. "Harmless at n = 200" is therefore **not** established, and that is what makes "could hit" the correct H-47 branch.

**F4: MEDIUM. HQ asked about the step-size mechanism ("fewer, larger tempering steps"); the records answer it, and the read-back does not use them.**
- *Evidence* (`ess_D.json`, `ess_others.json`, `ess_local.json` grids):
  - Both flagged events are at **stage 3 with Δφ ≈ 0.095**: D 0.0949 (φ 0.487 → 0.581); precedent 0.0958, with a first step of 0.174 and T 23.
  - The 1M n = 200 AR pilot's early steps are ≤ 0.047 (0.041, 0.042, 0.0002, 0.046 …), and its minimum ESS is 0.667 N.
  - In the one-particle model, the incremental weight is exp(Δφ · gap). The same ≈ 54-unit outlier gives w ≈ 167 (ESS 0.093 N) at Δφ 0.095, but only w ≈ 9 (ESS ≈ 0.975 N) at Δφ 0.041.
- *Reading:* the exposure is a large early tempering step. That is a grid-shape property; n = 1,000 makes it likely here through the start law (§6a). It is **not n = 1,000-specific**, because a frozen-arm n = 200 fit had the same shape.
  - For W1, the AR-strong 1M n = 200 grid seen so far has small steps, which is lower exposure.
  - ADJ-OPP r01 is the precedent's design: the 10⁵ G-B ADJ-OPP fit had early steps of 0.119 / 0.117, though at N 10,000.
  - This rests on two events. It is an inference, not a test.
- *Fix:* add this to §5.4 as a descriptive observation, with that caveat.

**F5: LOW. "Recovered at once (stage 4 ESS 2,499.7)" uses a non-diagnostic stage.**
- Stage 4 has Δφ 0.0066, so all 16 islands read 2,499.1–2,499.9 there, and resampling resets the weights by construction.
- The real evidence of recovery is that island 6 at stages 5–20 lies within the other 15 islands' range. It is marginally below their minimum at stage 9 (2,269.6 against 2,273.3) and stage 15 (2,239.4 against 2,243.2). The distinct-particle counts also support recovery.
- *Fix:* reword §1.3 / §5.3 accordingly.

**F6: LOW. Two items are missing from the deviation account.**
- (a) The registered §5 failure stop ("any … TIMEOUT / CANCELLED stage") **did fire**: ops logged "setup TIMEOUT (STOP)", and HQ 6ff8fb9e cleared it. "No kill rule tripped" is true, but the stop should be named in §3 / §4.
- (b) §1 item 1's "C4 delivered" should carry "(setup: job TIMEOUT, item 2)" inline, per 6ff8fb9e item 3. The §3 table already does.

**F7: LOW. HQ item 3 asks for "setup counts equal to the plan"; the text sits in §3.1, not §4.**
- The counts are verified: sidecar J 78,286, B 16, B_blocks 14, against `memplan_D/pt_AR_n1000.out` J 78,261, B 16, max_block 14.
- *Fix:* move or cross-reference these into §4 and say plainly "not exactly equal: J +25 (+0.03 %, the plan used the WP2 count-only sizes), B and B_blocks equal; the clean pilot shows the same kind of offset (+8)".

**F8: LOW. Some of the registered script's output blocks use the pilot's lines.**
- `gc_readback.json` `kill` evaluates K1 at 48 core-h and K2 at 1,584 s. Its `stages` block uses the pilot's requests (setup 48, eval 16 → 68.9 % / 68.7 %).
- The read-back correctly applies D's lines (70 core-h / 45 min / 3,600 s / 2,718) and the C3 block's D requests. It should say once that the script's kill and stages blocks are at the pilot's values. They are stricter, and D passes both, so no reader should mistake them.

**F9: LOW. §5.6 registration note.**
- HQ cf3bf327 already calls `low_empirical_ESS` "registered as reported, not gating". The read-back's literal point stands: GC_PREREG §4 names it in neither list.
- *Fix:* cite cf3bf327, and propose a GC_PREREG §10 deviation-log line so the registration text matches HQ's reading. Do not decide it in the read-back.

**Nits.**
- §4 "1.53× the bottom-up 69 min": 6,304–6,306 / 4,140 = 1.52.
- §1 item 6 gives "15,220"; §10 gives 15,221.
- In §10, label the row "+ H-34 seeds" as "position + seeds (no reserve)". It is not cumulative on the reserve row: 13,047 + 6,194 = 19,241.
- §9 "the cost per step is n-independent" should read "≈ equal in this pair (0.858 / 0.872 = 0.98)".
- §6a "the pilot bridges in 14 steps" should say "the **calibration** pilot".
- "25 of 25 sidecars" is 24 run-dir JSONs (23 `*.bin.json` + `calib_meta.json`) plus `bin_version.json`; name them.
- The NOTS `/tmp` slip broke POLICIES §14. It was disclosed and removed; it is noted here for the manager's record only.

## Verified (re-derived; no change needed)
- **C1:** the sacct dump sums to 389.249 (job rows), equal to the cost record's 389.248 and `prior_after_D.json` 389.25. That is 0.358 × 1,087, below soft 1,631, hard 2,718 and the wave line 2,174.
- **C2** (`eval.bin.json` = `gc_readback.json`):
  - M1 0.011692 and M2 0.00011390 (`target_met`).
  - Gap 0.002527 ≤ 0.024883. I re-computed it from `logZ_r`: σ̂/4 and M1/4 give a bound of 0.024883.
  - `local_certified` True.
  - eq − T 0.000623 ≤ 0.060923, which gives π̂(𝒯) 0.9491 = exp(−0.05227).
- **C3:** `not_completed: ["setup"]` is the only cause of the FAIL. Process peaks: setup 18,551 MB = 18.12 GiB (< 64 G) and merge 25,848,300 kB = 24.65 GiB (< 128 G). `process_over_request` is empty and there is no ADVISORY. The islands ran at 80 G with a 44.98 GiB sacct peak; this is disclosed.
- **C4:** every sidecar carries `da0cf85b…`. The recorded arm (2,500 / 1 / 0 / `I_used` 0 / bounded) equals the plan, and `logZ_r` has 16 finite values.
- **Kill rules:** calibrate 17.84 core-h and 669 s; slowest island 738 s; fit 389.25. No trip.
- **Setup integrity** (OPS_GC / LOG): `info --verify 1` gives `content_sha256` fd873022… = the sidecar's outputs hash, size 9,217,428,672, and 37 of 37 sections verified. Calibrate, every island and the merge record `inputs.setup.bin` = fd873022…. The 84.09 core-h is counted once.
- **H-47 location:** 320 values. The single value below 1,250 is island 6, stage 3, **232.76 (0.093 N)**. The next lowest is 2,001.2 (island 7, stage 19). The other islands at stage 3 read 2,470.9–2,483.1. The grid is identical across islands.
- **One-particle inference:** w₁ = 167.5 and log((N − 1 + w₁)/N) = 0.0645, against an observed stage-3 excess of 0.0637 (others' sd 0.0021). That is ≈ 54 units at Δφ 0.0949. It is labelled as an inference, correctly.
- **Effect on the evidence:** dropping island 6 moves log Ẑ by +0.00541; σ̂ goes 0.03105 → 0.02380; z = +3.51; W₆ 0.0676 is the maximum; the gap without island 6 is 0.0029. **Evidence and PIPs are unaffected at D**, and that claim is supported.
- **Census counts as printed:** n 100: 5 / 44; n 200: 1 / 170 (no basename duplicates within n 200); n 400: 0 / 38; n 800: 1 / 20; n 1,000: 1 / 1. The pilot's minimum is 1,666.9 (0.667 N). The precedent's minimum is 859.1 at island 11, stage 3; E2 is TRUE and σ̂ 1.3415.
- **§6a:** `cost_pilot` step 0 `mean_S` 6.4277 against 3.4609. First φ 0.30070 against 0.04089 (×7.35). Kind-1 step counts 14 against 20. `calib_meta` L 10 / 8, Hm 4 / 4. Grid T 20 / 27. The explanation is sound as measured, with its stated limit (φ = 0 only).
- **§6b:** the engine `before_write` is at 1,005.6 s for D and 1,026.5 s for the pilot; writes take 12.1 and 11.3 s. 3,027 − 1,006 − 12 = 2,009 and 1,566 − 1,027 − 11 = 528. The stage script runs only manifest fill, then `merge`, then the end printf; `manifests/merge.json` was written 2 s after the start. So the excess is inside the `merge` process, before its first phase record; the 9.0 / 9.9 GB HWM at "start" is consistent with that. "Located, not explained" is the right claim.
- **§9 ratios:** ×6.83, ×1.10, ×0.858, ×1.93, ×2.68, and ×1.126 overall (pilot 345.6355). The deltas are +71.8, −43.1, +13.4 and +1.6.
- **§10 envelope:**
  - Spent 4,353.02. Unspent at the committed classes: 7,642 + 1,052 = 8,694, which places the position at **13,047 (46.1 %)**. With the re-fit: 8,132.2 + 1,052 → **13,537 (47.8 %)**.
  - With the 25 % reserve: 15,220.5 / 15,833.3. Position + seeds: 19,241 / 20,104.
  - With 25 % on everything unspent: 4,353.02 + 1.25 × 14,888 = **22,963 (81.1 %)**, and 4,353.02 + 1.25 × 15,751.4 = **24,042 (85.0 %)**.
  - The previous column, 13,725, is consistent with the pilot at its class value of 326. Net −678.

## What the classification means for W1
H-47's branch is **"could hit the n = 200 frozen arm" → stop, HQ**, and the records support that branch.
- The flag has occurred on the identical build and arm (F2, N 2,500, m 1, I_max 0) at n = 200.
- Every occurrence ever recorded is at N 2,500.
- At n = 200 it co-occurred with σ̂ 1.34. The registered gates do not catch that, because σ̂ and E2 are reported, not gating.

In both events, **selection and PIPs held**: HPM = S₀, M2 ≤ 0.0005. The exposure for W1 is therefore the **precision of the evidence**, not selection. The expected incidence is low: 1 of 7 at F2, N 2,500, n 200. It is plausibly tied to large early Δφ steps. The AR-strong 1M n = 200 grid seen so far has small steps; ADJ-OPP r01 is the precedent's design.

The following is for HQ, not a ruling: an option consistent with "no engine or schedule change" is to release W1 with the flag kept reported-not-gating and two additions.
- A mandatory per-fit locate whenever the flag is TRUE: island, stage, min ESS / N, Δφ, and the drop-one-island log Ẑ shift.
- A pre-declared escalation: if the flag is TRUE together with E2 or σ̂ > 0.5, report to HQ before the next wave.
