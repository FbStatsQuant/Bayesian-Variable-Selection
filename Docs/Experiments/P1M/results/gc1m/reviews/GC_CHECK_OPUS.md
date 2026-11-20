# GC_CHECK_OPUS: the one Opus check of the G-C / 1M plan before HQ's 1M GO (Opus 5.5, Fri 2026-11-20)

**Under check:** `GC_PLAN.md` f1acd249… and `GC_PREREG.md` a4f7e566… (both sha-verified), `gc_identity.py` 49a6e688…, `gc_readback.py` efc0cab9…, `make_gc_plan.py` c19e580a…, the tests, and `presubmit/` (25 plans: `sha256sum -c` gives 25/25 OK). The tests pass when run as scripts (identity 6/6, readback 7/7). Engine diff read: `2cfaa9e5..e993ece2`, 364 commits, C++ sources only. Records read: `records/F1M_pilot`, `records/gb`, `records/hygiene_1117` (T5, P7), `records/precision1e4`, `records/vn_minileg`. Scratch: `~/SMC_Engineering_Department/tmp/20261120-gccheck-opus/` only. No commits, no NOTS, no BNP files, nothing under /tmp.

## Decision: **ACCEPT-WITH-FIXES**

The plan follows H-14, H-34, H-38, H-41 (5), H-42, H-43 and H-44. The memory requests cover the 1.72× under-count, and the arithmetic checks out. Two defects in the identity gate would each give a **certain false FAIL**, which counts as a STOP under GC_PREREG §3. A third defect, the calibration kill line, could plausibly trip a false STOP. All three are cheap text or script fixes, and all three must be made **before the pilot is submitted**. Nothing here needs a re-plan or a change to the quote.

## Findings

| # | sev | area | finding (evidence) | fix | when |
|---|---|---|---|---|---|
| **1** | **BLOCKER** | identity I1 | `raw_content_sha256` is the hash of the whole raw.bin file, and that file's `meta` section embeds `binary_block()` (`src/common/gen.cpp:171-190`; the code itself says "data identity (independent of the binary block in meta): the section hashes of X_cm and y"). It therefore differs whenever the binary differs, and here 2197fd5b ≠ da0cf85b. On the records it already differs for the same data: P7 `1a1c6c59` vs the 11-17 fit `2e8550be` (same X `5174f8b3`, same code); T5 `db9f887f` vs G-B `7152ee1c` (same X `2cdfff22`). → **I1 FAILs for certain.** | Gate I1 on `X_sha256` and `y_sha256`, plus equality of the truth's `generator`, `spec`, `S0` and `beta`, and the run params. Report `raw_content_sha256` only. `gen.cpp` is unchanged in the diff, so X and y are expected to be equal. | before the pilot |
| **2** | **BLOCKER** | identity I3 | Five of the gated "trajectory" counters measure **execution structure, not state**. They are `passes`, `act_cols`, `act_cols_per_pass`, `pairs` and `supports`. WP6 K5 (4c1e0f60, "rolling admission", **default on** in F2, absent at 2cfaa9e5) changes the pass composition by design: its commit says "passes 298 → 199", and per-pass support dedup moves `supports` and `pairs` too. **Cross-build control** (absent from `tools/identity_controls/`, whose pairs are all same-build): T5 (04d8d2b5, an ancestor of 2cfaa9e5) vs G-B G1a (F2), same data and seed at 10⁵. `gc_identity.py` gives I3 FAIL with **160 differences, every one in those 5 counters**, in all 32 active rows. M, mean_S, phi, sweeps, particle_rounds, store_size, store_mean_k and slow_supports are **equal in 34/34 rows** (e.g. step 1: passes 22 vs 16, pairs 100.8 M vs 99.8 M, while M, mean_S, phi and sweeps are bit-equal). → **I3 FAILs for certain at 1M.** | Move the 5 counters to "reported". Gate on the state counters (M, mean_S, phi, sweeps, particle_rounds, store_size, store_mean_k, slow_supports, kind, step, segment) and on the header. Add T5-vs-G1a as a cross-build control test with expected PASS under the new set. Log this as a pre-commit change (no 1M F2 data exists yet, so no tuning). | before the pilot |
| **3** | **MAJOR** | kill rule K1 | The calibrate model E 16 equals P7's pilot-island task (14.96) + 1. That disagrees with the plan's own expected wall: "≈ 12–15 min" × 96 CPUs = **19–24 core-h**. It also disagrees with G-B's measured I_max-0 ratio (14–21 % of the I_max-3 calibration), which gives **19–29**. The 11-17 calibrate also spent 278 s outside the calibration proper (7.4 core-h of task overhead), plus the 9.8 GB calib.bin export. K1 at 32 core-h fires at **20 min** of wall, only 1.1–1.7× the realistic value, so a false STOP of G-C is plausible. The clause "or elapsed > 30 min" is looser than the billed clause and never fires first. | Re-base calibrate E to **24** (P90 29) before the commit, and set K1 = 2 × 24 = **48 core-h ≈ 30 min**, which matches the elapsed clause already written. The unit becomes ≈ 325 and C1 ≈ 488. P90 360, the block and the envelope change by < +200 (already covered by the Opus G-B F4 sensitivity). The alternative is to keep 317 and justify K1 on the 24 figure; either way the model and K1 must agree. | before the pilot |
| 4 | minor | C3 at option D | C3 is judged on sacct MaxRSS, which counts page cache (MERGE_MEM: the 11-17 merge was "reclaim-capped" at 75.1 of 80 GiB with a process of ≈ 34 GiB). At the pilot the margins are fine: merge ≈ 26–34 GiB process + ≈ 59 GB of files in 128 G; islands ≈ 27 + ≈ 21 GB mapped in 64 G. At D, the islands (42.9 GiB plan + ≈ 22 GB of inputs mapped in 64 G) and the merge can read ≈ the request with no OOM risk. That is a false C3 and a wasted stage rerun. | For C3, judge the process peak (`peak_rss_kb` / VmHWM), report sacct alongside it, and count an OOM only on state OUT_OF_MEMORY. | before D |
| 5 | minor | D eval memory | D's eval is "as the pilot" (16 G), but eval reads `data.bin` (11-17 eval inputs), and that file is 8 GB at n = 1,000 vs 1.6 GB. Eval is the only unplanned stage at D. | Request 32 G for D's eval (memory is not billed) or plan it. | before D |
| 6 | minor | D sequencing text | H-44: D runs "only AFTER the G-C2 pilot is clean". GC_PLAN §3 and GC_PREREG §5 release D "after the pilot is read back clean", while the §9 timeline says "right after the ruling". | Release D on **HQ's G-C2 ruling**, the same trigger as W1, but before W1. | before the pilot (text) |
| 7 | nit | K2 | ENGINEERING_SPEC says "island > 2× at 50 % progress". K2 uses elapsed > 2 × the *slowest* 11-17 island (1,584 s) "while the others have finished". That is looser than 2 × the mean (1,260 s) and fires at completion, not at 50 %. The 1:00 limit and K3 (≈ 30 min for 16 uniformly slow islands) bound the cost, so the risk is low. | Disclose it as the implementation of the spec rule, or drop the "others finished" clause. | later |
| 8 | nit | stop overlap | The pilot's wave stop (> 630 = 2 × 315) falls inside C1's soft band (476–793, "re-quote, HQ rules, not a stop"). D likewise: 2,170 vs 2,718. | State that for a one-fit wave the per-fit lines govern, or that 630 stops submission only. | later |
| 9 | nit | spec §pilot acceptance | ENGINEERING_SPEC l. 399-400 also requires "T3 hash check repeated on the pilot's first stage with two thread counts". It is not listed in C1–C4. | HQ point: discharged by H-14's freeze reproduction check, or waived. | HQ |
| 10 | nit | retention text | V5's parenthetical "(so a lost fit.bin would cost a re-merge)" reads backwards: after deletion a re-merge is impossible. The §5 desktop total (≈ 170 GB) is incremental; the current desktop use is not stated. | Re-word, and state current use vs the 700 GB cap. | later |

## 1. Memory at 1M: **covered; no plausible OOM at the pilot**
- **Merge 128 G.** The 75.1 GiB was sacct page cache at the 80 G limit. The process was ≈ 34 GiB before PR #65 and the plan after it is 26.2 GiB. MERGE_MEM's `sacct_upper`, with every file cached, is 82.6 GiB < 128 G, so the 1.72× under-count was an accounting artefact and the request covers even the fully cached case. I_max 0 does not grow the merge: the inherited models are 2c, set by the store cap and not by I_max, and calib.bin is at most the 11-17 size.
- **Calibrate 128 G.** At I_max 0 there are no diagnostic islands (those peaked at 53–55 GB). The P7 pilot island peaked at 48.7 GB, against a plan of 71.6 GiB.
- **Islands 64 G.** Measured 26–27 GB, plan 33.8 GiB.
- **Setup 48 G.** Process 13.5 GB, sacct 23.7 GB.
- **Eval 16 G.** Completed at 11-17.
- **Option D.** The plan-only values (island 42.9 / 64, calibrate 82.0 / 128, merge 58.0 / 128) clear. At n = 200 the same tool over-counts the island (31.1 vs 26–27 measured) and the calibrate (71.6 vs ≤ 55). The only exposure at D is findings 4 and 5, which are false-C3 and eval risks rather than real OOMs.
- **Setup reshape at D.** 48 CPUs and 1:45 is sound. The correlation pass does not scale with threads: 897 s at 3 threads vs 780 s at 48 for n = 200. So n = 1,000 ≈ 4,069 × 780 / 897 ≈ 59 min, plus ≈ 10 min for the rest ≈ 69 min, giving 1.5× margin. The kill rule at D's own model (calibrate > 70 / 45 min, island > 60 min, fit > 2,718) is consistent with the 21–51 and 380–920 ranges.

## 2. The G-C2 pilot
- **Quote 317 (P90 360).** The method (437.44 − 135.63 + 14.96 + 1) is sound, except that the calibration term is ≈ 5–13 low (finding 3). The real saving is ≈ 107–117, not ≈ 121, and that sits inside P90. The islands (269.25) assume the same T = 27 on the preliminary grid; at 10⁵, T was equal in all G-B pairs. The pilot measures it.
- **Stage limits.** All are ≤ 2 h, with margins of 2.4× (setup), ≥ 6× (calibrate), 4.5× (islands), 2.8× (merge) and 20× (eval). No exception is needed.
- **Pass criteria.** C2 follows §0-v2.3 at 10⁶ to the letter: M1, M2, evidence within 3 s.e., HPM certified, PIP_eq vs PIP_𝒯. The one exception, "same best model in 16 of 16 islands", is disclosed as not computable. C1 = 1.5× matches the spec's pilot acceptance and the 2.5× guard matches H-26 Q4. The spec's T3 two-thread-count item is missing (finding 9).
- **F2 identity statement: the code expectation holds; the gate as written does not.**
  - Setup and data-generation sources are **unchanged** from 2cfaa9e5 to e993ece2. No setup or `gen.cpp` C++ appears in the diff. `p1m_driver.py` changes plan plumbing (N, I_max, T6) only.
  - The calibrate changes are N-parameter plumbing (`v_N`, default 2,500) and `release_tables()`.
  - The island kernel changes all declare "same bits" and are tested: K2 (Philox AVX-512 multiply, I-proposals in the order phase), K5 (rolling admission), O3 (deferred leader compaction) and O4 (checkpoint checksum).
  - So the same data, setup and pilot trajectory are expected. The 10⁵ cross-build control confirms it: the state counters are bit-equal across a build that is older still.
  - The *counter* identity is not expected, because of findings 1 and 2. As registered, the gate FAILs for certain, a false STOP of G-C.
  - With fixes 1 and 2 the gate is meaningful. Per-row M, mean_S, phi and sweeps at full double precision over 34 rows are a strong trajectory fingerprint, so the risk of a false PASS is low.
  - The final-island stage stays untested at 1M, as the plan already discloses.

## 3. Option D
H-44 is implemented: D was released, sits at the ≥ 317 floor with ≈ 1,087 kept in the envelope, comes after a clean G-C2, has the n = 1,000 plan-only gate (sizes-only `v4_plan_tables` on WP2 counts, which I accept as that gate, with the engine's own `--mem-budget` admission still on), and runs alone with no other 1M batch in flight. The setup reshape and the kill rule at D's own model are sound (§1). Fix the release trigger wording (finding 6), the C3 basis (finding 4) and the eval request (finding 5).

## 4. Retention and island deletion (H-41 (5)): **V1–V5 are sound for deletion; one residual risk for HQ**
- V1–V5 together prove three things: the merge consumed exactly these 16 files (V4: sidecar sha and size = `fit.meta.inputs`, and the merge hashes every island itself), the fit and eval are complete and valid, and the record of record is desktop-verified (V5). The first-fit full re-hash is a good control.
- Later readers covered without the islands:
  - `listpip` (fit.bin, plus regenerable data).
  - re-eval (fit.bin + data, regenerable by `gen`).
  - the seed scoring (`logZ_r` and `pip_eq` in fit.bin).
  - d_H (law.bin, kept).
  - π₀(S₀) (A+ setup.bin).
- **Residual risk:** once the islands are deleted and calib.bin is purged (class B, 14 days), *any* re-merge costs a full re-run (≈ 317 per fit). Re-merge triggers would be a merge, tail or LS0 bug found later, or a new merge-side statistic such as the per-island HPM that §0-v2.3 asks for and the plan calls "not computable".
- This is exactly what happened with the 11-17 fit: its islands are gone, which is why the I_max 3/0 pair cannot be compared at the final stage now.
- **Recommendation (HQ):** keep a re-merge reference for the **pilot** on the desktop until the block read-back: islands 34.2 GB + calib.bin ≈ 8–10 GB (setup.bin is already A+), ≈ +44 GB. Optionally do the same for D, ≈ +45 GB. The desktop total becomes ≈ 215–260 GB, still ≪ 700.
- **Totals:** per-fit A ≈ 2.8 GB × 43 ≈ 120 GB, plus A+ 47 GB, ≈ 170 GB on the desktop; Owls staging ≤ 15 GB; the 7-day and 12-day alarms precede the 14-day atime purge. All of these respect the caps. State current desktop use (finding 10).
- The split itself is a deviation from H-41 (5)'s keep set, which includes setup for every fit, so it needs HQ's ruling. The plan says so. The island-deletion fence is new and also needs approval.

## 5. The block and the envelope: **arithmetic verified**
- 8,849 = 317 + 6,023 + 330 + 317 + 775 + 1,087; × 1.6 = 14,158 → **14,200**.
- Seeds: 6,023 × 1.6 = 9,637 → **9,700**.
- S2 = 8,849 + 1,052 = **9,901**; closed + S2 = 13,519; + 25 % on the unspent items = 15,994.
- Seeds: 19,542 without the reserve, 23,523 with it.
- P90 S2 = 11,610. Worst stack = (11,610 + 6,746 + 470) × 1.25 + 3,618 = **27,150 ≤ 28,300**, a thin margin of 1,150 that is still inside.
- Waves: 2 fits at a time, each pre-announced, serial, `%16`, and the QOS cap = one fit's islands. All consistent with H-14.
- **The N 5,000 adjudication: the plan's reading is correct.** MINILEG_PREREG §6, the ADOPT row: "N 2,500 for the approved replicate set (22 fits) + **ONE N 10⁴ fit on the rep-1 data (1,083) in place of the N 5,000 self-check** + option D at N 2,500: S2". The S2 row of the table reads: "1M at N 2,500 + ONE N 10⁴ self-check; option D at N 2,500". H-38 adopted S2 "as declared". The N 5,000 self-check is therefore outside S2; keeping it as an HQ-only +470 option is consistent.

## 6. Open items
- **Competitors frozen by hash.** ENGINEERING_SPEC §0-v2.6 lists it as a G-C *entry* item ("configuration, evaluator and competitors frozen by hash → the 1M pilot alone"). It has no effect on any 1M fit. The code exists on the engine branch (`tools/competitors/`: `ACCEPTANCE.md`, `p1m_competitors.R`, `competitor_packages.tsv`). The cheapest way to meet the letter of G-C is to record the sha of `tools/competitors/` at a named commit, plus the package-version TSV, in the plan's commit. Otherwise HQ moves the item to "before the competitor runs". This blocks the literal G-C wording, not the pilot's science. **HQ point.**
- **`gc_seeds.py` not registered.** This blocks only the release of the conditional seed block (H-34). It is not a 1M GO blocker.

## Points HQ must rule on
1. Accept fixes 1–3 as pre-commit changes to GC_PREREG §3/§4 (identity gate sets, calibrate E 24 and K1 48), logged as made before any 1M F2 data existed.
2. The competitors' freeze: record the hash now, or move it to before the competitor runs.
3. The retention split (classes A, A+, B, C) as a deviation from the H-41 (5) keep set, the new island-deletion fence, and the recommended pilot re-merge reference (+≈ 44 GB on the desktop).
4. The T3 two-thread-count pilot item (spec l. 399): discharged or waived.
5. D's release trigger: HQ's G-C2 ruling (recommended).

## Path
1. Make fixes 1–3 and 6 (script + PREREG/PLAN text), and add the T5-vs-G1a cross-build control test.
2. Re-run the identity tests. Expected: T5 vs G1a PASS under the new set; FAIL still on different data and on a mutated `M` or `mean_S`.
3. Manager commit with the shas, plus the competitors hash if HQ chooses that route.
4. HQ 1M GO, then the pilot alone, then the read-back with `gc_identity.py` and the Opus child re-derivation, then HQ's G-C2 ruling.
5. D runs alone, with fixes 4–5 in place before D. Then W1 onwards.
