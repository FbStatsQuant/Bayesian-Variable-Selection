# A0_CHECK_OPUS: independent check of the A0 canary read-back (O-6; Opus checker; Thu 2026-11-19)

**Decision: CLEAN-WITH-FIXES. No fix is needed before P1, so P1–P4 may self-release.** I re-derived every row of the LEG_PLAN §6.4 checklist from the records, the plans and the engine source, and every row passes. The XB bit check does what it claims, and my rerun reproduces it bit for bit. `grid_unconverged = True` is structural under the bounded rule and is not a reason to hold. The fixes below fall due at later waves: F1 before P2, F2 before P4, F3 and F4 before S1. F5–F7 are text or low-priority changes.

Material checked: draft `A0_READBACK.md`; LEG_PLAN §5.3 and §6.4; PREREG §2, §3 and §5; PLAN_REVIEW R5, R7 and R8; OPS_PREC; DECISIONS H-25 and H-26. Plan commit a6037ab0. The registered shas still match: `precision_offset.py` cbbc2301…, `precision_freeze.py` 7cdd69a1…, `make_waves_prec.py` 3d9b4af6…, `quote_model.py` 6cd8a978…, and `waves.json` 31cb8cf3… (identical in staging). Engine source was read at b89cba4d in the worktree `tmp/20261119-precplan/wt_b89cba4d` (read-only). My scratch is `~/SMC_Engineering_Department/tmp/20261119-o6check/` (`rederive.py`, `dropped.py`, `xb_rerun.txt`, synthetic probes `p1–p4.txt`). I did not touch /tmp or NOTS, made no commit, and edited no draft or plan file.

## 1. Checklist §6.4, re-derived (my own script `rederive.py`; not the draft's tools)
| # | item | my evidence | verdict |
|---|---|---|---|
| 1 | 4/4 delivered, all stages COMPLETED | `sacct_dump.txt`: 528/528 rows COMPLETED. The dump covers the whole wave and is identical in all 3 batch units (sha e7528fd7…); each batch's cost files filter their own jobs. Per-fit `cost_*.json`: every stage `["COMPLETED"]`; island tasks 64/64/16/16. `eval.bin.json` `status` and `fit_status` are completed ×4 | PASS |
| 2a | arm = plan (`plan.resolved.json` vs `calib_meta.json`) | m4: plan `{I_max 3, refine_m 4}`, N 2500 → recorded N 2500, m 4, I_max 3, I_used 3, bounded. I0: plan `{0, 1}` → 2500 / 1 / 0 / 0 / bounded. A3: `{partition exact}` → 2500 / 1 / 3 / 3 / bounded. XB: `{}` → the same. `calib.bin.json settings` agree (fallback source). I_used ≤ I_max in every fit | PASS |
| 2b | A3 `partition: exact` | `setup.bin.json`: A3 `exact`; the other 3 `truncated` | PASS |
| 3 | behaviour (R5) | m4: 64/64 islands have T = 84 (84 % 4 = 0, ≥ 36). **Stronger check, from `calib_meta.json` section dims:** T = dims(grid) − 1 = refine_m × (dims(grid_unrefined) − 1), i.e. 84 = 4 × 21, and it holds exactly for all 4 fits (I0 23, A3 21, XB 20). I0: `cost/` has 1 file and 0 `cost_diag_*`; `grids_all_labels` = [preliminary]. m4, A3, XB: 12 diag files, k ∈ {1, 2, 3}, max = I_used = 3 | PASS |
| 4 | X/y sha256 = overlap rep 1 and across fits | `truth.json` X e67d7051…, y 577c5682… in all 4 fits, equal to `overlap_refs.json["4-AR-n200-r01"]` and to the overlap record's own `truth.json` | PASS |
| 5 | one binary sha = the BUILD line | Every `binary.sha256` (walked recursively, including `eval.bin.json fit.meta.binary` and `calib_meta.json` meta and top level) in all JSON of the 4 fits (26/74/74/26 occurrences) = d0c30b65…, the `deploy_leg.log` BUILD line. COPYBIN lines PL_A0_2/3 carry the same sha | PASS |
| 6 | cost ≤ wave stop; each fit ≤ soft | 14.01 / 5.55 / 2.63 / 2.64 against soft 18.5 / 8.6 / 4.1 / 3.3; wave 24.83 against stop 50. `stop_rules_prec.py` rerun on both A0 probes: "no stop rule fired", table sha c0fcd139 pinned | PASS |
| 7 | R′ = 64 merge; A3 setup | merge 62 s / 83 s, MaxRSS 1,677,640K / 1,660,556K (1.72 / 1.70 GB) against 16G and 0:20. A3 setup 14 s, 0.86 GB against 0:30 and 16G | PASS |
| 8 | fit.bin readable, logZ_r length, occ | `logZ_r` length 64/64/16/16, all finite; `fit.meta.occ` present ×4. M1 / M2 / M3 all meet the §0-v2.3 targets (e.g. m4: 0.016 / 0.00054 / 0.012). `info` on fit.bin succeeds (my XB rerun) | PASS |
| 9 | XB cross-build bit check | §2 below: rerun by me, PASS on all 6 checks | PASS |

The draft's tables match my numbers. I found two textual inaccuracies (F5, F7); neither changes a verdict.

## 2. XB: does `xb_check.py` compare what it claims? (sha 12132b50…, imports `overlap1e4/tools/cross_check_V.py` d95522b4…)
**Rerun:** `xb_check.py --a …/A0/4-AR-n200-r01-V-XB-s1 --b …/W0/4-AR-n200-r01-V-s1 --info-bin <b9dc443e…> --show-dropped --tmp <my scratch>` gives rc 0. logZ_r 16/16 bit-equal, HPM equal, 16/16 island `output_hash` equal, 24 sidecars with 0 differences, fit.bin 44 sections and eval.bin 4 sections equal.

**Code read:** the five checks are implemented as described. `output_hash` is FNV-1a over every law output of the island (`island.h:283`), and execution statistics are excluded by design (`:202`). The JSON comparison takes the union of keys and the union of files, so a key or file present on one side only is caught. I listed every dropped key that is not under `binary.*`, with its A and B values (`dropped.txt`):
- **Every dropped key is provenance:** input/output file hashes, `calib_bin` / `fit_bin` / `island_bin` / `content_sha256` (container hashes that embed the binary block), `mem_plan` / `mem_estimate` (two values differ by 64 bytes of input size), RSS, walls, paths, and `threads`.
- **Dropped although substantive:** only `eval.bin.json data.{n, p, K, p_raw}` (equal) and `params.threads` (equal). Nothing that carries a result was dropped.

**Not compared directly (residuals; all are covered transitively):**
- **The calibration.** `calib_meta.json` is excluded, and the overlap unit has none. `calib.bin` is collected on neither side, and its hash differs by the binary block. The frozen grid is still covered: islands with identical `init_hash` and `output_hash`, identical T and bit-equal logZ_r cannot come from different grids.
- **The other containers.** The `setup.bin` and `data.bin` contents are covered by `init_hash` and the X/y hashes. `law.bin` is covered by its sidecar and by fit.bin's section shas (law.bin is not collected for XB).
- **Empty containers.** `flat()` ignores empty dicts and lists. That is cosmetic.

**Sufficiency for the 14 reused fits (R7):**
- **What XB proves directly.** One fit is bit-identical across 3 different binary shas of F: the leg build d0c30b65, W0-V dd5af0cd (git "unknown") and W0-V2 ba569a33. So binary-sha differences between builds of F with this toolchain are shown to be non-functional.
- **Which builds the reused fits come from.** The 14 fits come from 4 builds, which I read from their eval `binary` blocks:
  - dd5af0cd: AR r01 s1, ADJOPP r01 s1 (2 fits);
  - 72c9109d: ARweak r01 s1, IND r01 s1, NULL r01 s1 (3 fits);
  - 1e375b74: AR r01 s2, ARweak r02 s1, ADJOPP r02 s1 (3 fits);
  - 4fecb186: AR r02–r04 s1 and s2 (6 fits).
- **The doc slip in §5.3.** LEG_PLAN §5.3 lists **ba569a33 (W0-V2)** for W0. The reused units named by run id (`EXEMPT_RUNS`) are the W0 **V** units, built by **dd5af0cd**. XB covers both W0 builds, so there is no gap, only a doc slip (F7).
- **What rests on inference.** 12 of the 14 fits (W1–W3 builds) are **not directly tested**. For them, git commit F, compiler g++ 14.3.0, flags, ISA, FMA and libm sha256 are identical to the leg build; I checked every build block field except the sha.
- **My judgement.** This is sufficient under the plan's own rule (§6.4 (9): if equal, the exemption is justified), and I agree it is adequate evidence. The residual risk is small and does not touch P1–P4: the precision waves use only leg-build fits. If HQ wants direct evidence, F4 gives a cheap option.

## 3. `grid_unconverged = True` in all 4 fits
- **What it means at F** (`include/v4/calib.h:217-246`, `:289`):
  - **The flag.** Under the bounded rule the driver runs up to I_max (diagnostic → rebuild) iterations. If no rebuild yields a grid **bitwise identical** to its predecessor, `grid_unconverged` is set. The last grid is then frozen anyway (D-26), with no escalation; the flag also sets `checks_passed_calibration` to false.
  - **I_max = 0.** The loop never runs, so the flag is **True by construction**.
  - **I_max = 3 at p = 10⁴.** The candidate set V grows at every rebuild (XB: 399,226 → 399,369 → 399,381 → 399,386; m4 and A3 grow the same way). The rebuilt grid therefore essentially never repeats bitwise, and True is the expected state on signal data.
  - **It does discriminate.** The 2 NULL overlap V fits stopped after rebuild 1 (4 diag files, k = 1 only), which means they converged.
- **Effect on the freeze and the criteria: none.**
  - `precision_freeze.py` takes identity from N, m, I_max, rule and I_used ≤ I_max (lines 104-114). It only *reports* `grid_unconverged` per fit (line 170).
  - It is not part of D (PREREG §2) or of any pass/fail rule.
  - PREREG §5 C7 and the G-B "flag frequencies" input will show ≈ 100 % on signal datasets. The FZ and leg reports must say that this is structural under the bounded rule at p = 10⁴, not a warning.
- **The 40 overlap fits.** The flag was not recorded there: it lives only in calib.bin meta, which was not collected (R8). What can be inferred:
  - **AR r01 V-s1: True.** XB reproduces it bit for bit, and the calibration is deterministic.
  - **The other 17 non-NULL V fits: 3 rebuilds each** (12 diag files, k1–k3). The flag is therefore True unless rebuild 3 happened to equal rebuild 2, which the records cannot show.
  - **The 2 NULL V fits: False** (converged at rebuild 1).
  - **The 20 T fits** use the coded rule, where the flag is an escalation trigger. That is not comparable.
  - So "True in all 40" is not the case, and "True in every non-NULL V fit" is the most likely reading.
- **Hold P1–P4? No.**

## 4. Costs, and the inputs to the class re-fit (the hard line never moves; HQ Q3)
| fit | measured | committed E | ratio |
|---|---|---|---|
| m4 | 14.01 | 12.36 | 1.13× |
| I0 | 5.55 | 5.76 | 0.96× |
| A3 | 2.63 | 2.76 | 0.95× |
| XB | 2.64 | 2.18 | 1.21× |
| **A0 wave** | **24.83** | quote 22.8 | 1.09× |

- **I_max = 0 calibration.** Measured 0.107 core-h against 1.08–1.25 for I_max = 3: a fraction of ≈ 0.10, where the quote assumed U(0.2, 0.5).
  - Effect on the quote: ≈ −0.25 core-h per I0 fit, ≈ −1.5 over the leg.
  - The m4 excess adds ≈ +1.6 per fit, ≈ +10 over the 6 fits.
  - So each P-wave re-quote moves by less than 10 %, well inside the 1.5× self-release band. **Nothing material for P1–P4.**
- **For the FZ report (R4).** At the production R′ = 16, calibration is ≈ 41 % of a fit (XB: 1.08 of 2.64), and I_max = 0 removes ≈ 90 % of it. That is a ≈ 37 % saving per fit, larger than the plan assumed. HQ should see this beside the I_max decision.
- **The pooled class table matters for P4 (→ F2).**
  - The committed class `prec N2500 m4 I3` is pooled over datasets (E 12.36, soft 18.5). The P4 wave quote, which is dataset-specific, is 45.7 for ADJ-OPP m4 ×2 + I0 ×2.
  - Overlap ADJ-OPP fits cost ≈ 1.2× AR fits (`measured_V_costs.csv`: 2.60 vs 2.10).
  - With the A0 m4 ratio of 1.13, an ADJ-OPP m4 fit is expected at ≈ 17–18 core-h, at or just under the soft line. Two soft trips in P4 are therefore likely, and a third (an ADJ-OPP I0 fit above 8.6) would STOP the wave on a pooling artefact.
  - The hard line (30.9) and the wave stop (90) are far away. This is friction, not risk.

## 5. `starts.jsonl` / `ends.jsonl`
- **The loss is larger than the draft says.** PL_A0_1 should hold 136 start records (2 setup, 2 calibrate, 128 islands, 2 merge, 2 eval).
  - Only 111 `"stage"` tokens are present: 107 parseable lines plus 3 broken lines. So **≈ 25 records are lost outright**, not "1 glued line and 2 fragments".
  - `ends.jsonl` has 135 of 136 records: one I0 island end is missing. The draft does not mention this.
  - Cause: non-atomic `printf >>` from many nodes onto the shared scratch filesystem.
- **It is harmless for cost and records.** No stop, cost or freeze tool reads these files:
  - `p1m_cost.py` uses sacct plus `submissions.jsonl` (that file is intact: 8/5/5 lines all parse);
  - `stop_rules_prec.py` uses squeue and sacct;
  - `precision_freeze.py` uses `cost_*.json`;
  - the driver's restart-mode end records are not used in this leg (the plans have no `restart`).
- **The only consumer** is `a0_facts.py`, for the "calibrate task → fit" table. That mapping is fixed independently by the plan order (`RUNS[FIT-1]`) and by each run dir's own `calib_meta.json`.
- **Expect the same loss in P batches** (136 tasks each). Treat the files as non-authoritative (F5).

## 6. Stop-rule tool and monitor for P1–P4
- **Batches of ≤ 150 tasks.** Each P plan has 136 tasks with island throttle %32.
  - Setup and calibrate array tasks map to fits through `runs[b][task−1]`, and islands, merge and eval through `submissions.jsonl`.
  - A pending array row (`…_[33-128%32]`) is handled.
  - Every run id in `waves.json` for A0 and P1–P4 resolves to a committed class, and every precision dataset (AR, ARweak, ADJOPP r01) has an `overlap_refs` entry. `test_stop_rules_prec.py`: 26/26 pass (run with `PREC_TEST_TMP` in my scratch).
- **The `%k` throttle INFO fix.** It is correct and narrow; I tested it with synthetic probes:
  - `JobArrayTaskLimit` on `…_[33-128%32]` → INFO, no stop;
  - the same reason on an expanded id with no `%k` → STOP;
  - `QOSMaxCPUPerUserLimit` on a `%k` array → STOP.
  - Cosmetic: the line prints "INFO INFO".
- **The squeue scope (F6).** The probe's squeue is `-u fb31`, so it sees **every** job of the account. A foreign pending job (for example another leg) with a QOS, Assoc or Limit reason gives a **false STOP**; I confirmed this with a synthetic probe. It is conservative, not unsafe.
- **PRIOR and the cumulative stop (F3).**
  - `--prior {run_id: core_h}` adds the cost of earlier waves to the cumulative and projection rules, but **no tool writes that file**. Without it, the cumulative counts only the current wave.
  - For P1–P4 this is immaterial (A0 + P ≈ 150 against 1,000), and the projection is conservative because unstarted A0 fits count as "left".
  - If a prior file also contained the current wave's run ids, they would be double-counted. Build it from earlier waves only.
- **Behaviour rule for m = 4 (F1).**
  - The overlap ARweak r01 m = 1 grids have T = 9 and 10, so an ARweak m4 fit in P2 lands at T = 36–40. An unrefined grid of 8 intervals gives T = 32, which raises a false "FLAG behaviour".
  - It is a flag, not a stop, and `precision_freeze.py` does not use it for identity, so the freeze is unaffected.
  - The exact check (§1 row 3) is available from `calib_meta.json` at read-back.

## 7. Findings
| # | sev | finding | when | fix |
|---|---|---|---|---|
| F1 | M | The m = 4 behaviour rule "T ≥ 36" is not dataset-proof: ARweak r01 m = 1 T is 9–10, so an m4 fit with T = 32 is possible and would be a false FLAG in P2/P4 | **before P2** (read-back level; no stop involved) | Judge m4 behaviour by the exact identity T = dims(grid) − 1 = refine_m × (dims(grid_unrefined) − 1) from `calib_meta.json` sections (verified on all 4 A0 fits); keep T ≥ 36 only as a monitor hint |
| F2 | M | The post-A0 soft-line re-fit (LEG_PLAN §5.3) **cannot be applied** in `stop_rules_prec.py`: the soft column sits inside the sha-pinned TABLE and there is no override, so editing it gives "STOP table altered". P4 ADJ-OPP m4 is expected near the pooled soft line of 18.5 (2 trips likely; 3 = STOP on an artefact) | **before P4** | Add `--soft CLASS=value` (only the soft column changes; TABLE and the hard column stay pinned; overrides printed), set from the A0 re-fit (m4 E′ ≈ 14.0 → soft ≈ 21). Or the manager accepts the committed soft lines and pre-declares that a P4 3-trip STOP is cost-benign. Manager's call; the hard line does not move |
| F3 | L | No tool produces the `PRIOR` JSON, so the cumulative stop counts only the current wave | before S1 (immaterial for P1–P4) | At each read-back, write `staging/precision1e4/prior_after_<wave>.json` from the collected `cost_*.json` (earlier waves only) and pass `PRIOR=` in the monitor prompt |
| F4 | L | XB directly covers 2 of the 4 builds behind the reused fits (dd5af0cd, and ba569a33 too). 12 of the 14 reused fits (72c9109d, 1e375b74, 4fecb186) rest on identical-toolchain evidence plus the 3-build reproducibility shown | before S1 / FZ (not P1–P4) | Say it in the read-back as a stated limit. Optional, HQ or manager: one more cross-build fit against a W3 record (e.g. `4-AR-n200-r02-V-s1`, 4fecb186, 6 of the 14) in S1, ≈ 2.6 core-h |
| F5 | L | Draft §8(b) understates the jsonl loss: ≈ 25 of 136 start records lost, and `ends.jsonl` 135/136 | with the read-back | Correct the line; record "starts/ends.jsonl non-authoritative" in OPS_PREC. A per-task record file is for a later driver PR (the driver is pinned in this leg) |
| F6 | L | The monitor's squeue scope is the whole account: a foreign job pending on QOS/Assoc/Limit gives a false STOP. Also "INFO INFO" | later (conservative) | Keep only SQUEUE rows whose base job id is in the wave's submissions |
| F7 | L | LEG_PLAN §5.3 / draft: the W0 exempt build is dd5af0cd (W0-V, git "unknown"), not ba569a33 (W0-V2) | with the FZ / leg report (do not edit the committed plan now) | Note it as a correction line. Both W0 builds are bit-identical to the leg build (XB vs V-s1 and vs V-s1.V2) |
| info | – | `grid_unconverged` is structural (bounded rule; True by construction at I_max = 0; V grows every rebuild at I_max = 3); its C7 / G-B frequency will be ≈ 100 % on signal data | FZ / leg report | Report it as such; it is not a defect |
| info | – | The I_max = 0 saving at R′ = 16 is ≈ 37 % of a fit (the calibration fraction is ≈ 0.10, not 0.2–0.5) | FZ (R4) | Put it beside the I_max decision |

## 8. Answers to the brief (one line each)
1. Checklist §6.4: **all rows re-derived and PASS** (arm, behaviour and partition, data, build, cost, merge and setup, fit/eval, XB).
2. XB: **the check is real and complete for result-bearing fields; my rerun gives the same PASS.** It is sufficient for the exemption under the plan's rule. 12 of the 14 reused fits rest on toolchain identity (F4); P1–P4 do not depend on it.
3. `grid_unconverged`: structural under the bounded rule. It does not affect the freeze or any criterion. In the overlap it was not recorded: likely True in the 18 non-NULL V fits (certain for AR r01 s1) and False in the 2 NULL fits. It is **not** a reason to hold.
4. Costs: A0 runs at 1.09× its quote; the I0 fraction is ≈ 0.10. The P-wave quotes move by less than 10 %, and the hard line is unchanged. The pooled m4 soft line is a P4 friction point (F2).
5. jsonl: harmless for cost and records, because no tool depends on these files; the loss is larger than the draft says (F5).
6. Stop tool and monitor: correct for P1–P4; the `%k` fix is correct. Items: F1 before P2, F2 before P4, F3 and F6 later.
