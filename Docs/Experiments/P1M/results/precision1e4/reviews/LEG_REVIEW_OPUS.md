# LEG_REVIEW_OPUS: the one Opus review of the precision study + 10⁴ science leg read-back (PREREG §6.3)

**Reviewer:** Opus 5.5 review child, Thu 2026-11-19 (evening). **Under review:** `LEG_READBACK.md` (Sonnet draft) + `leg_readback/` incl. the late `cross_vf.{json,md}`.
**Method:** everything below was re-derived from the records with my own readers or by re-running the registered tools. Scratch: `~/SMC_Engineering_Department/tmp/20261119-legreview-opus/` (`reader.py` f99be2b0…, `sci.py` 98691f5d…, `a3.py` 9b2c6f2c…, `cross_mixed.json` d9a3dad0…; outputs `off_out/`, `out_mixed_full/`, `out_vf_wc/`, `xcross/`). Read-only on the records and on every registered or committed file. No commit, no NOTS, no BNP file.

## Decision: **ACCEPT-WITH-FIXES**
- **G-A closes: YES.** Precision COMPLETE (HQ 5a44e163), science **170/170** re-derived, frozen configuration recorded by hash and present in every science fit.
- **ADDENDUM_2_VF: COMPLETE, carry-over confirmed on the 14 pairs.** With the late cross values, H is no longer only screened. It passes 14/14. The registered scorer, run by me in full mode on `mixed40` with the merged cross file, returns **CLEAN, 11/11 PASS**. The read-back's "H screened only" text must be replaced (F1).
- **Three statements in the read-back are wrong** (F1–F3). None changes a gate. F2 and F3 change descriptive science lines that HQ will read.
- **Flags.** `ADJOPP-n200-r04` is an evidence-precision outlier with selection intact. It has no bearing on the freeze, and it goes to HQ as a flag. The M2 misses are report-only misses, correctly disclosed, but they need one scope correction (F10).

## 1. G-A closing (PREREG §6.3)

| condition | my check | result |
|---|---|---|
| Precision COMPLETE | FZ_CHECK_OPUS (CONFIRMED-WITH-FIXES, counted as the ACCEPT) + HQ 5a44e163 / H-30; `precision_freeze.py` and `precision_offset.py` HEAD blob sha = registered (7cdd69a1…, cbbc2301…) | **MET** |
| Science ≥ 95 % | Own reader over all 194 units: exactly one `SHA256SUMS`, `sha256sum --strict -c` OK; `eval.bin.json` status and fit_status `completed`; setup / calib / fit sidecars `completed`; R′ island sidecars all `completed`; `logZ_r` of length R′ and finite; `fit.bin` present. **194/194 clean, 0 problems; science S1–S10 = 170/170** (155 V/VF + 15 A3/A3F) | **MET (100 %)** |
| Frozen config by hash | `CAMPAIGN_FREEZE_ADDENDUM.md` sha256 **0b9890835ff36e4c…0f201491** = the blob added in **e627b547** (2026-11-19 10:30 CST, commit message lists the same sha) and unchanged at today's HEAD. ADDENDUM_2_VF 8c70fc53… and PREREG 3f2daf76… are likewise committed in e627b547. **Binary:** the union of every `binary.sha256` in every JSON of a unit is exactly {d0c30b65…} in 192 units and {09249230…} in the 2 B1 T units. **calib_meta:** all 170 science units read (N 2,500, refine_m 1, I_max 0, I_used 0, rule bounded); triggers = {grid_unconverged} in 155/155 | **MET** |

ADDENDUM_2_VF was committed at 16:30:22Z, before the first S1 submit at 16:32:37Z (OPS_PREC). The pre-declaration holds.

## 2. ADDENDUM_2_VF

**Scoring as pre-declared?** Yes, after F1 is applied. The scorer is `compare_overlap_v2.py` sha 4f402e51…, unchanged (verified). It was run in `--wave-check` mode and with `--cross-file`, as the addendum says. I re-ran the registered wrapper `vf_wrapper.py` f64cc97e… into my scratch. I merged a cross file: the VF seeds from `cross_vf.json`, and the 6 un-twinned I_max = 3 seeds from `overlap1e4/W3_readback/cross_vt_all.json`. Then:
- **`mixed40` full mode: CLEAN, all 11 criteria PASS** (D, PAIR, S1–S4, P, E1, E2, H 10/10 with a cross value, C).
- `--wave-check` on `vf_pairs` with `cross_vf.json`: 14/14 pairs scored.

The read-back should save this run (or its own equivalent) under `leg_readback/vf/`, and state the cross-file merge as input plumbing.

**Wrapper sha before any output?** Yes. File mtimes in the worker's scratch `20261119-legrb/`:
- `vf_wrapper.sha256` (v1) 16:31:13 CST;
- `vf_wrapper.sha256.v2` 16:31:31.28;
- input trees built from 16:31:31.7;
- the first scorer outputs at 16:32:05.

**v1 → v2 is clean.**
- The diff is the mirroring of run dirs only: a real dir of symlinks instead of a symlinked dir. No field, filter or pairing changed.
- The v1 output was not kept (F8). I therefore checked what it could have contained, from the scorer's code (`compare_overlap_v2.py:752-765`): with no T run found, a `wave_check` row carries only the V side's `reasons`, `core_h`, `tier` and `flags`. No V − T quantity and no S₀ quantity is printed.
- "Read nothing scored" is therefore true.

**Re-derived pairs.**

| pair | quantity | read-back | mine |
|---|---|---|---|
| ADJ-OPP r02 s1 (worst H) | xeval `cross` re-run (same b89cba4d build afef0e46…) | h² 1.2409258745e-06, ratio 0.0136 | **bit-identical h²**; d_H 0.001114 / d_H(T,f\*) 0.08163 = **0.01365** |
| AR r01 s1 (worst E1 pair; T = `.T2`) | xeval `cross` | h² 3.5233e-07 | **bit-identical** |
| NULL r01 s1 | xeval `cross` | h² 7.7222e-09 | **bit-identical** |
| AR r01 (dataset, mixed40) | E1 \|Δlog Ẑ\| / combined s.e. | 1.382 | **1.3815** (I_max 3: 1.6388) |
| AR r04 (dataset) | E1 | 1.184 (I_max 3: 1.761) | **1.1836 / 1.7612** |
| ADJ-OPP r02 (dataset) | P worst ratio | 0.0379 | **0.0378** (I_max 3: 0.0381) |
| `vf` offset row | δ(k = 16), 10 datasets | −0.00300, 7/10 negative | **−0.00300, 7/10** (own reader, newest T dup) |

**"I_max = 0 V agrees with T as I_max = 3 did."** This is fair and not over-read, provided the read-back's own qualifier stays in the same sentence: 14 pairs, p = 10⁴, n = 200, single-seed pairs, and no "validated" claim.

There is one point HQ should see. VF and its I_max = 3 twin share the data and the engine seed, and differ only in the temperature grid. The near-equality of the two columns is therefore a direct measurement of the grid change, which is what was asked. But it says nothing about rare heavy-tailed island spreads, which these 14 pairs did not contain. The one such case is the un-twinned ADJ-OPP r04 (§4).

## 3. Science section against PREREG §5

**Coverage.** Every §5 row is reported, or explicitly marked unavailable:
- C2 and C4, including the reliability curve with bin counts, active counts and the cluster bootstrap;
- C5, including the slope bootstrap and the posterior quantiles of d_H;
- C7, A3, the second seed, the null control, cost, and the G-B inputs.

Two availability statements are now stale because `law.bin` exists for the 14 VF units:
- **V − T Hellinger for VF** (§3.9): now available, passes (F1).
- **d_H between partitions** (§3.5 / §3.9): now computable for the **4 A3 pairs whose default is VF** (AR r01–r04). At 15 s per xeval run, compute them or say "computable for 4/15, not done" (F9).

**Spot checks from the eval records** (own reader, `selection.*`, `pip.eq.*`, `fit.bin` `pip_eq` read with section-hash verification on):

| claim | mine |
|---|---|
| P(HPM = S₀) AR-weak n 100 / 200 / 400 / 800 = 0.00 / 0.50 / 1.00 / 0.90 | **0.00 (20 ds) / 0.50 (20) / 1.00 (10) / 0.90 (10)**; all 17 cells agree |
| 112 / 150 non-NULL recover S₀; 38 misses all `posterior`; 34 strict subsets; 4 with one FP; AR-weak n 100 HPM empty 13 / S₀ not in store 11; n ≥ 200: 98 / 110 | **all reproduced**; min F(HPM) − F(S₀) over the misses +0.31 nats |
| NULL: HPM empty 5/5; `n_null_gt_0.5` 0 in 5/5; largest null PIP 0.0157 | **reproduced** (sup 0.0080–0.0157) |
| A3: HPM identical 15/15; max \|ΔPIP\| 2.50e-4; second seed max 8.67e-4 | **15/15; 2.502e-4; 8.667e-4**; per-pair Δlog Ẑ agrees to 5 decimals |
| Wilson bounds (n = datasets) | reproduced: (0.30, 0.70), (0.72, 1.00), (0.60, 0.98), (0.00, 0.16), (0.38, 0.96) |
| final-merge flags (155 fits) | **E2 1, low_empirical_ESS 6, checks_passed_final 148, all others 0** |

**Clustering.** The dataset is the unit, as MANIFEST §4 asks:
- t intervals over datasets;
- Wilson intervals with n = datasets;
- a cluster bootstrap for the reliability curve and the slopes;
- the two AR n = 200 seeds averaged within each dataset (10 datasets, 20 fits).

The unclipped t intervals for bounded quantities are disclosed. Acceptable.

**Reliability curve.** It is labelled a repeated-sampling diagnostic under a fixed truth, both in the conventions and under the table. OK.

**Over-reading and errors:**
- **F2: false statement.** §3.4 says log Ẑ − log Z_T is "positive in every fit". It is **negative in 1 of 155**: `4-ADJOPP-n200-r04-V-s1`, log Ẑ −227.811 against the deterministic lower bound log Z_T −227.688, a gap of **−0.123**. The SMC estimate sits below a known lower bound on Z. This belongs in the flag description too (§4).
- **F3: false summary line.** §1 line 5 says "store-BMA d_H² reaches the oracle's by n = 400 (ratio ≤ 1.40 AR-weak, ≤ 1.04 elsewhere)". The read-back's own §3.3 table contradicts it:
  - IND n = 400: **1.255** [0.85, 1.66];
  - AR-weak n = 800: **1.582** [0.30, 2.87].

  Suggested text: "At n ≥ 400 the BMA/oracle ratio is 1.02–1.04 in AR-strong, BLK and ADJ-OPP. It stays above 1 where HPM misses remain: AR-weak 1.40 / 1.58 (n 400 / 800), IND n 400 1.26 (the r01 fit with one extra variable)."
- Nit (F14): §6 says "the 10⁵ / 1M re-size should use T, not nf(n)". This comes from a post-hoc regression at p = 10⁴, and the stage count T at 10⁵ is unknown. Write "consider T" instead.
- Nit (F13): §5 bolds "−0.00690 (m1·I0)" and the sentence "only the I_max = 0 cell's interval excludes 0". PREREG §4.3 fixes three headline lines, and this is not one of them. Un-bold it and keep the number in the table.
- Nit (F17): A3 is "closer than seed-to-seed on every outcome". A same-seed pair against a different-seed spread is expected to come out closer. The caveat is printed; leave it.
- Nit (F5): the §3.4 header "sigma-hat of Z_r" should read "σ̂ = sd(log Ẑ_r)".

## 4. Flags

### `4-ADJOPP-n200-r04-V-s1`

**What it is.** From the record:

| quantity | value |
|---|---|
| sd(log Ẑ_r) = `sigma_hat` | 1.0880 (identical to machine precision) |
| robust σ̂ | 1.003 |
| R_eff / R′ | 0.42 |
| max − median of log Ẑ_r | 1.96 |
| log Ẑ − log Z_T | **−0.123** |

The 16 log Ẑ_r spread from −2.07 to +1.96 about their median. Four islands sit at least 0.8 nats below it and one sits 1.96 above it. Some islands under-sample posterior mass, and the mean is carried by a few others (max weight 0.32).

Selection and PIPs are unaffected:
- HPM = MPM = S₀, F(HPM) = F(S₀) to 6e-14, certified `both`;
- M1 0.0136, M2 0.00055;
- `occ_inhomogeneous` False.

It is the only fit in the leg with σ̂ > 0.46, and no other fit at n = 200 exceeds 0.1. The 20 overlap V fits (I_max 3) and the 18 precision fits all stay ≤ 0.1. With 1 of 155 against 0 of 38, no attribution is possible.

**Does it matter for the freeze? No.**
- The freeze is the registered rule's output, and HQ ruled "no post-hoc override" (H-30).
- §0-v2.3 targets never switch estimators.
- The flag concerns the precision of log Ẑ, not selection.

**To HQ? Yes, as a flag, not a criterion.** It is the only per-fit hint that I_max = 0 might fatten the Ẑ_r tails on a hard design. The 10⁵ I_max twin remains the decisive test.

Optional attribution check (≈ 3–4 core-h): an I_max = 3 twin of r04 s1 (same data and engine seed) plus an I_max = 0 s2, folded into the next NOTS batch (the V-N mini-leg or the G-B pilot batch), with no wave of its own. HQ's call.

### M2: 14/155 fits above 0.005 (13 at n = 100)

**Count and identities reproduced.** The engine's own `pip.island_spread.target_met` is False in exactly these 14. The two I_max = 3 AR-weak n = 100 fits in the leg (B1 r91 V s1, s2) sit at 0.0027 and 0.0029, but they are a different dataset and not twins.

**Not a precision-target failure in the gate sense.** ENGINEERING_SPEC §0-v2.3 states these as "precision targets at 10⁶ (reported per fit; never used to switch estimators)", and PREREG §3.1 says "a target miss is reported as a miss". The read-back does exactly that, so the disclosure is correct.

**One correction (F10).** `CAMPAIGN_FREEZE_ADDENDUM.md` §2 says "at 10⁴ every fit meets the §0-v2.3 targets by 3–54×". That sentence covers only the 18 precision fits at R′ = 64 and n = 200.

The leg report should say so beside the production-R′ result: at R′ = 16, M2 is missed in 14/155 fits (13 at n = 100) and M3 in 1/155. The I_max decision used M2 only at R′ = 64 and n = 200.

## 5. Deviations

### L-8: science analysis script not registered

**How serious.** Moderate as a procedural breach, nil for any gate:
- The only gate quantity in §5 is completion, which I derived independently.
- The descriptive conventions (dataset clustering, Wilson intervals, the reliability-curve form, the bootstrap) are the ones PREREG §5 and MANIFEST §4 fixed in advance, and the script follows them.
- The script has no thresholds.

**Timeline, from mtimes.** The final `science.py` (7c5c7fee…) has mtime 16:37:26, and its first output 16:37:35, which is consistent with the sha being recorded first. The sha chain itself is self-attested, because the sha file was last written at 16:41:46 when the extras were appended.

**The note's claim needs qualifying.** The note says "no science value had been read in this task". Before 16:37:07 the VF scorer outputs (16:32) and `vf_offset` / `costs` (16:33) already existed. Those are V-vs-T and log Ẑ values for 14 of the 155 science fits, though no C2–C5 quantity.

**How to log it.** Add a dated deviation entry to PREREG §8 (append-only, new sha recorded in the commit), containing:
- the facts;
- the sha chain 9a2cc1cb → 3b3b1254 → 7c5c7fee;
- the post-read extras (`science_extras*.py`) and the post-hoc shas of `vf_offset.py` and `costs.py`;
- the qualifier above;
- the G-B carry rule: register before the first read.

### E1 / E2 wording

**Confirmed in the source at F** (`git show eefcbc4a:Scripts/SMC_BVS/engine_v4/include/v4/merge.h`, byte-identical to b89cba4d):
- `merge.h:473` sets E1 (island best < HPM − 1);
- `:474` sets **E2 = R ≥ 2 && sd(log Ẑ_r) > 1**;
- `:486` sets low ESS;
- `:487` sets `checks_passed_final`.

None of these depends on I_max. The calibration E1 / E2 (`calib.h:228-233`) sit inside the loop `for it = 1..cap`, with `cap = I_max` for the bounded rule (`:221`), so they never run at I_max = 0.

**Correction line**, for the leg report and as a PREREG §8 erratum referenced from CAMPAIGN_FREEZE_ADDENDUM §2(i) and PREREG §7 (last bullet) and §8 (third entry):
> *Erratum (2026-11-19, leg review): "E1 and E2 are not evaluated at I_max = 0" applies to the **calibration-stage** triggers only (`calib.h:221-246`). The **final-merge** flags `fit.meta.flags.{E1, E2, E3, low_empirical_ESS, checks_passed_final}` are computed at every I_max (`merge.h:473-487` at F) and are reported as frequencies. The final E2 is exactly sd(log Ẑ_r) > 1, i.e. the "E2 analogue" of §2(iii). At 10⁴: E2 1/155, E1 0, E3 0.*

**Add to the same erratum (F5).** PREREG §3.1 describes M3 as the "island sd of Ẑ_r / Ẑ". The field `evidence.sigma_hat` is sd(log Ẑ_r): for r04 both equal 1.088026, while sd(Ẑ_r / Z̄) is 1.205. ENGINEERING_SPEC already writes σ̂(log Ẑ_r). The freeze rule is unaffected, because it reads the field.

### Also log (F7)

ADDENDUM_2_VF placed the VF scoring "at the read-back of the wave that holds the VF fits (S1 / S2)". Three things happened instead:
- It ran only at the leg read-back.
- H became possible only after `law.bin` and `data.bin` were fetched from NOTS scratch. The collection plan kept `law.bin` only for `-P-` and A3 fits, although the addendum pre-declared `--cross-file`.
- 14 record units were amended:
  - files moved in;
  - content hashes checked against the fit's own `law.bin.json`, 28/28;
  - `SHA256SUMS` rewritten, with the old file kept as `.prev`;
  - `sha256sum -c` OK; my reader confirms all 194.

Nothing failed, so the addendum's "report to HQ at once" clause was never triggered. Log one deviation line, and keep OPS_PREC's desktop re-sync heads-up for the 14 units.

## 6. Offset (final) and cost

**Offset.**
- I re-ran `precision_offset.py` (cbbc2301…, verified) on W0–W3 + A0, P1–P4.
- `offset_report.md` and `offset_per_fit.csv` are **byte-identical** to `fz/` and to `leg_readback/offset/`, and `offset.json` is equal apart from paths.
- P1 −0.00394 reproduced.
- The knob contrasts are m +0.00010 [−0.00183, +0.00204] and I_max −0.00089 [−0.00398, +0.00220]. **No FINDING.** The N contrast is not computable.

**Cost.**
- The ledger `staging/…/prior_after_S10.json` is identical to the copy in the folder: 194 fits, **462.48**.
- With the pinned class table (sha c0fcd139… verified in `stop_rules_prec.py`) and the unchanged `klass`, **21/21 classes PASS**: class mean ≤ 1.5 E and no fit > 2.5 E.
- **0 fits above 1.5 E**; the largest single fit is **1.358×** (IND n100 r05). The 2 B1 T fits have no class (report line 172.5).
- Only immaterial 2nd-decimal rounding differs from the read-back table (AR n100 max/E 1.34 vs 1.33; IND n400 mean 1.06 vs 1.07).
- The caveat that the science E is the I_max = 3 baseline table is correct and stays.

## 7. 1M rep 1: recommendation (b)

**The reasoning is sound.**
- (b) costs nothing now.
- It preserves option value. If I_max = 0 fails the 10⁵ twin, 1M runs at I_max = 3 and rep 1 is then already in-configuration for I_max. Option (a) would have bought ≈ 440 core-h of a configuration HQ might drop.

**Two corrections before it goes to HQ:**
1. "Rep 1 at I_max = 3 is exactly the I_max = 3 arm a later 1M I_max comparison needs" over-states it. Rep 1 is:
   - one fit with one seed;
   - on a pre-F2 build (the 11-17 pilot), whereas H-31 makes F2 the engine for 1M;
   - without a same-seed I_max = 0 partner.

   It could serve as one arm only with an F2 identity statement at 1M and a paired I_max = 0 fit.
2. HQ approved **20** AR-strong 1M replicates (H-14). Under (b), only 19 replicates are in the frozen configuration unless a 21st is run (≈ 440). So (b) defers the cost rather than removing it, unless HQ accepts 19.

**Recommend:** (b) now, and decide between (a), a 21st replicate, or 19 after the 10⁵ I_max twin is read.

## 8. Findings

| id | where | finding | label |
|---|---|---|---|
| F1 | LEG_READBACK §1.1, §1.4, §4 (H row, "Why H cannot be completed", "INCOMPLETE solely because H"), §3.9, §8.5(iv), §9.1 | H is now evaluated: d_H(VF,T)/d_H(T,f\*) 0.0034–0.0136 (≤ 0.10), 14/14 (I_max 3 max 0.0136). The registered scorer on `mixed40` + merged cross file gives **CLEAN 11/11**. Replace "screened only" everywhere; add the run under `leg_readback/vf/` | **changes a conclusion** (VF section: INCOMPLETE → CLEAN) |
| F2 | §3.4 bullet 3; §3.4 table | "log Ẑ − log Z_T positive in every fit" is false: ADJ-OPP r04 −0.123 (1/155). Add the minimum column and put it in the flag text | **changes a conclusion** (descriptive C7) |
| F3 | §1 line 5 | "BMA reaches the oracle by n = 400; ≤ 1.04 elsewhere" is false (IND n400 1.26, AR-weak n800 1.58). Use the suggested text in §3 | **changes a conclusion** (descriptive C5 summary) |
| F4 | CAMPAIGN_FREEZE_ADDENDUM §2(i), PREREG §7, §8 | E1 / E2 erratum: the calibration-stage flags are not evaluated, the final-merge flags are (`merge.h:473-487`). Correction line in §5 above | doc |
| F5 | PREREG §3.1 (M3); LEG_READBACK §3.4 header | σ̂ = sd(log Ẑ_r), not sd(Ẑ_r/Ẑ). Same erratum | doc |
| F6 | §7 L-8; `science_script.sha256` note | Log in PREREG §8 with the sha chain; qualify "no science value read" (VF outputs and `vf_offset` existed at 16:32–16:33) | doc |
| F7 | §7 (new line) | ADDENDUM_2_VF timing deviation + the `law.bin` / `data.bin` amendment of 14 record units | doc |
| F8 | §4 provenance, L-9 | The v1 wrapper output was not kept. State that cleanliness rests on the scorer's code path (`compare_overlap_v2.py:752-765`), which I confirm | doc |
| F9 | §3.5, §3.9 | The partition d_H is now computable for 4/15 A3 pairs: compute or re-word | doc |
| F10 | §3.4 / §8.5(ii); CAMPAIGN_FREEZE §2 | Say that "targets met by 3–54×" covers the R′ = 64 precision fits only; at R′ = 16, M2 is missed in 14/155 and M3 in 1/155. Engine `target_met` agrees (14/14) | doc |
| F11 | §1.6, §3.4 flag text | Complete the r04 description (log Ẑ < log Z_T; island spread; selection intact) and add the optional ≈ 3–4 core-h attribution pair for HQ | doc |
| F12 | §2 table | "e627b547 = HEAD": HEAD is now the auto-snapshot d1407386, but the blob is unchanged; say "committed in e627b547, unchanged at HEAD" | doc |
| F13 | §5 | Un-bold the I_max = 0 δ cell and its "excludes 0" remark (not a §4.3 headline) | doc |
| F14 | §6 n-scaling | "should use T" → "consider T (post hoc at p = 10⁴)" | doc |
| F15 | §6 class table | 2nd-decimal rounding only | doc (nit) |
| F16 | `leg_readback/science/science_tables.md` (S4) | Annotate the wrong sentence about final flags (L-10), since the file ships | doc |
| F17 | §3.5 yardstick | A same-seed A3 pair vs a different-seed spread; the caveat is printed. Leave as is | nit |
| F18 | §8.3 | 1M rep 1: soften "exactly the I_max = 3 arm"; add the 19-vs-20 replicate implication (§7 above) | doc |

## 9. What must go to HQ in the leg report

1. **G-A closes.**
   - Precision COMPLETE (5a44e163).
   - Science 170/170, re-derived independently (194/194 units clean).
   - Freeze addendum sha 0b989083… (e627b547), binary d0c30b65… in all 192 V fits, refine_m 1 / I_max 0 / I_used 0 / bounded in 170/170.
2. **ADDENDUM_2_VF complete.**
   - All overlap v2 criteria pass for the 14 VF pairs, **including H** (max 0.0136 against 0.10); the registered scorer gives CLEAN 11/11 on `mixed40`.
   - Scope: 14 pairs, p = 10⁴, n = 200.
   - Deviations: scored late, and 14 units amended with content-verified `law.bin` / `data.bin`.
3. **Flag `ADJOPP-n200-r04`** (σ̂ 1.09, final E2, log Ẑ 0.12 below log Z_T, HPM = S₀).
   - Not attributable, and no bearing on the freeze.
   - Offer the optional ≈ 3–4 core-h I_max 3 / seed-2 pair for HQ to decide.
4. **Production-R′ precision.** M2 missed in 14/155 (13 at n = 100) and M3 in 1/155. These are report-only §0-v2.3 misses, but they correct the "every fit meets the targets" reading of the freeze addendum.
5. **Deviations / errata.**
   - L-8: unregistered science script (PREREG §8 entry).
   - The E1 / E2 erratum and the σ̂ label.
   - The ADDENDUM_2_VF timing.
6. **Offset:** no FINDING; reproduced byte-identical; the N contrast awaits the V-N mini-leg.
7. **Cost:** 462.48 core-h (11.2 % of plan); G-B cost criterion PASS 21/21 (max single 1.36×).
8. **1M rep 1:** (b) now, with the two corrections of §7 (build and pairing; 19 vs 20 replicates). HQ rules at G-B, after the 10⁵ twin.
9. **Corrected science summary lines (F2, F3)**, plus the G-B items of §8 (I_max twin rule on one pair, the V-N arms' I_max, register the analysis script first).
