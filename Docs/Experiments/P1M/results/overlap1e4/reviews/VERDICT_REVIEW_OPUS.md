# VERDICT REVIEW (independent, Opus): 10⁴ T-vs-V overlap rung, HQ H-24 (4)

Reviewer: Opus 5.5 (one independent review per H-24 (4)). Date: 2026-11-19. Scope: `OVERLAP_1e4_VERDICT_DRAFT.md` (Sonnet), checked against `OVERLAP_1e4_PREREG.md`, `PREREG_ADDENDUM_1.md`, `PREREG_ADDENDUM_2.md`, DECISIONS H-18…H-24, both comparison scripts and the raw records under `~/SMC_Engineering_Department/records/overlap1e4/W0..W3/`. No registered, addendum or draft file was edited. Nothing was committed. Scratch: `~/SMC_Engineering_Department/tmp/20261119-verdict-review/` only. No NOTS access.

## Decision

**ACCEPT-WITH-FIXES. Every fix is a documentation fix. None changes an outcome.**

- **Outcome confirmed: CLEAN under v2** (`compare_overlap_v2.py`, which governs per ADDENDUM_1 / H-21). For PREREG §4 rule 5, this review **ACCEPTS** the comparison, code and tables. All 11 criteria pass, and I re-derived each one from the raw records.
- The fixes below concern the wording of the verdict draft. They should be made before the draft becomes the verdict, but they do not gate the CLEAN determination.
- **Registered script:** the correct outcome per PREREG §4 is **INCOMPLETE**. The script prints **MARGINAL** because of a code defect in how it scores S1 (§4 below). Neither label releases anything, and the registered result is informational because v2 governs.

### Fixes (all doc; none changes an outcome)
1. **State the adjudication.** The registered outcome per §4 is INCOMPLETE, and the printed MARGINAL comes from a script defect (finding F1). The draft currently leaves this as "a point for the reviewer".
2. **Re-word the escalation reading (§3b and Summary 4).** Replace "partly" with "not established (suggestive only)". Lead with the within-dataset result, not the fit-level p = 0.011 (finding F2).
3. **Add the dataset-level V−T offset** and recommend a note to the precision-study plan (finding F3).
4. **Move two observations into the deviations log:** "one build per arm not met" and "eval seed = data seed" (findings F4, F5).
5. **Fix the HQ citation for the W0 redo:** LOG.md 2026-11-18 10:59 CST, not H-21 (finding F6).
6. **Add one line on C robustness:** C still passes with the W0 evidence-attempt cost included (finding F7).
7. **Correct the log Ẑ − log Z_T range:** NULL is 0.0066–0.0070 (finding F8).
8. **§7 release:** note that H-19 still requires HQ's GO before the precision study or the 10⁴ science starts (finding F9).

## 1. Reproducibility

| check | result |
|---|---|
| `compare_overlap.py` sha256 | `311bbad886fc61c679ac47d1c30faf8d8897e33681baf5711f1f268472632eea`. Matches the PREREG, and equals the blob at the pre-W0 commit 3148f3af (2026-11-18 08:51 CST). |
| `compare_overlap_v2.py` sha256 | `4f402e5127efd4754cf25e4ade6ad799f697ebc28e1c657ff49f93fd2905b5c6`. Matches ADDENDUM_1, and equals the blob at commit 60e28395 (2026-11-18 20:25 CST). That commit predates the first W1 read-back (23:07 CST snapshot) and all W1 results. |
| PREREG / ADDENDUM_1 / ADDENDUM_2 sha256 | 8b528ced… / 8c4903a6… / 4985833d…. All as the draft states, and git shows none of them modified. |
| tests | `test_compare_overlap.py`: 13/13 PASS. `test_compare_overlap_v2.py`: 18/18 PASS. Test shas match the PREREG and ADDENDUM_1. |
| re-run, full (verdict) mode, both scripts | `python3 -I <script> --records W0 W1 W2 W3 --cost-dir {W0_T2,W0_V2,W1_T,W1_V,W2_T,W2_V,W3_T,W3_V}/cost --cross-file W3_readback/cross_vt_all.json --out …/tmp/20261119-verdict-review/<arm>`. rc 0 for both. |
| **verdict.json sha256 (mine)** | v2 **`b6988ee17a326940b13830df9f62bce96ecfa647641d2b4f3b3efd6721bef367`**, registered **`93c1e33ba435f3e2e38744b34147510199e8ffc63e3f9ccf945668d9e30fce53`**. **Byte-identical to the claimed values.** `per_fit.csv`, `per_dataset.csv`, `verdict.md` and stdout are byte-identical as well. |
| duplicate resolution (W0) | `duplicates_resolved` keeps the `.T2` / `.V2` unit for all 4 W0 run ids. The evidence units are not counted: the AR-T evidence unit has no eval (INCOMPLETE.txt), the ADJ-OPP-T one has none either, and both evidence V evals are older (10:11 vs 11:49 CST). |

## 2. Code review

### 2a. Diff registered → v2
`diff compare_overlap.py compare_overlap_v2.py` contains exactly two kinds of change:
- **The ADDENDUM_1 N check.** For a T fit with an integer `fit.meta.tier ≥ 0`, it checks N == 10⁴·4^tier. Otherwise it keeps the registered N.
- **Reporting only.** It adds `tier_final`, `N_final` and `N_expected_at_tier` to `per_fit.csv`, `per_dataset.csv` and `verdict.json` (`fits_tier_N`), plus a docstring.

`PREREG` is byte-identical. No threshold, metric, criterion or outcome line differs, so the diff is ONLY the ADDENDUM_1 change. (The docstring still says "pending HQ approval". That is cosmetic and already disclosed in ADDENDUM_1.)

I also checked `fit.meta.tier` (which the script uses) against `calib.bin.json tier_final`, which the script does not read. They agree in all 40 fits: the 3 tier-1 fits are AR r01 T s1, ARweak r01 T s1 and IND r01 T s2, all at N 40,000. `settings.rule` is `coded` in all 20 T fits and `bounded` in all 20 V fits.

### 2b. Outcome logic vs PREREG §4

| §4 rule | code (`compare()`, v2 lines 715–735) | agrees? |
|---|---|---|
| 1 INVALID if PAIR fails | `PAIR == FAIL → INVALID` | yes |
| 2 NOT CLEAN if hpm_miss ≥ 2, any F_T > F_V, or pred_fail ≥ 2 | `notclean` list. `n_hpm_real_miss` counts only evaluable pairs, including a mismatch in the one evaluable pair of a half-missing dataset. | yes |
| 3 MARGINAL if not (2) and E1, E2, P, S3, S4, a single H miss or C fails | `other_fail` = any criterion with status FAIL other than D and PAIR | **no, for S1 (F1)** |
| 4 INCOMPLETE if D fails or any criterion is NOT_EVALUATED | `incomplete` flag, applied only after `other_fail` | yes |
| 5 CLEAN iff all pass (S1 may have 1 miss) + review ACCEPT | CLEAN only if every status is PASS. S1 PASS at ≥ 9/10. | yes |

**F1 (the registered MARGINAL).** S1 is the only criterion with no NOT_EVALUATED branch: `"PASS" if n_hpm_ok >= 9 else "FAIL"` (v2 lines 669–672; registered lines 655–658). With 3 datasets not evaluable, n_hpm_ok = 7, so S1 = FAIL. The residual `other_fail` then classifies the run MARGINAL. The PREREG reads differently:

- **Rule 3 lists its criteria explicitly:** "E1, E2, P, S3, S4, a single predictive miss, or C". S1 is not among them.
  - That omission is coherent. With all datasets evaluable, S1 can only fail through ≥ 2 HPM mismatches, which rule 2 already handles.
- **The closing sentence of §4 settles it:** "Outcome rules 2–3 count only evaluable data: a dataset with a missing fit is not an HPM mismatch, it is a D failure."
  - In the registered run, S1 is 7/10 only because of the 3 undelivered fits, with 0 real mismatches. So it belongs to D, and through rule 4 it gives **INCOMPLETE**.

**Adjudication: the PREREG outcome of the registered script is INCOMPLETE. The printed MARGINAL is a script defect against the PREREG text** (S1 should be NOT_EVALUATED when fewer than 10 datasets are evaluable and no real mismatches exist). The draft's diagnosis of the cause, the S1-as-FAIL artefact, is correct. Neither label releases anything.

**Could the same logic mis-classify under v2?** Not on these data. D = 40/40 makes S1 evaluable on all 10 datasets (10/10 equal, 0 mismatches). Every other criterion is PASS, with its "all evaluated" condition met (E1/E2 10/10, P 10/10, S3 20/20, S4 4/4, H 10 with a cross value and 0 pending, C 0 without a cost record). The only path to CLEAN is "every status PASS", and that is what holds. The S1 defect is dormant whenever D passes. It matters only for a successor script (for example a 10⁵ rung), where it should be fixed under its own pre-registration.

### 2c. Other things that could flip a criterion: checked, none found
- **E1.** The pooled variance is s_A² = mean_d (Δ_A,d)²/2, and v_A,d = max(s_A²/2, (se²_s1 + se²_s2)/4). The island s.e. is sd(Z_r/Ẑ)/√R′ (delta method). All of this matches PREREG §3.4.
- **P.** Uses a per-column threshold max(0.01, 3·se_j), with se_j from the `pip_r` island matrix (ddof 1, /√R′) and the 2-seed variance /4. Matches §3.3.
- **E2.** Checks (i), (ii) and (iii) as in §3.5. (i) and (ii) use the 2-seed mean of log Z_T, a reasonable reading of "log Z_T,A".
- **H.** Uses mean_s √h²_cross ≤ 0.10 · mean_s √h²_T, which matches §3.6. Any FAIL gives H = FAIL, and `pred_fail` drives rules 2 and 3.
- **Robustness of the input plumbing (info, F10).** Both points worked correctly in this run, and neither is a criterion bug:
  - **Duplicates** are resolved by the newest eval mtime.
  - **Cost files** are looked up in the run dir first, then in each `--cost-dir` in the order given. The W0 evidence and T2 batches both hold a `cost_4-AR-n200-r01-T-s1.json` (42.11 vs 110.12), so the cost read depends on which dirs are passed. `verdict.json` records neither the cost dirs nor a per-fit cost source.

## 3. Tables: independent re-derivation from the raw records

My own script (`tmp/20261119-verdict-review/indep_check.py`; it does not import the comparison scripts) covers all 40 counted units. It reads `eval.bin.json`, `truth.json`, `calib.bin.json`, the per-fit `cost_<run_id>.json`, and `fit.bin` through its own section parser with every section sha256 verified. Output is in `indep_check.out` and `indep_check.json`. The required spot-checks (escalated T fit AR r01 T s1, AR r04, and others) are part of the full sweep.

| quantity | my value | draft / script | |
|---|---|---|---|
| D | 40/40. Status completed ×4 fields in all 40. N/R′/mode: V 2500/16/V/sapphirerapids; T 10⁴·4^tier / 4 / law / portable. | 40/40 | ✓ |
| PAIR | X/y sha equal across the 4 fits of every dataset; X sha distinct across the 10 datasets | PASS | ✓ |
| S1 HPM | equal in both seed pairs in 10/10 datasets | 10/10 | ✓ |
| S2 | max F_T − F_V = 0 (0 or −1e-13 … −3e-14 in all 20 pairs) | PASS | ✓ |
| S3 MPM | equal in 20/20 pairs | 20/20 | ✓ |
| S4 NULL | `n_null_gt_0.5` = 0 in 4/4. Recomputed from fit.bin `pip_eq`: 0 columns > 0.5 in all 4. | PASS | ✓ |
| pip_eq = row mean of pip_r | max abs diff ≤ 2.2e-16 in all 40 | (PREREG check) | ✓ |
| P max abs ΔPIP / worst ratio | 3.81e-4 (ADJ-OPP r02) / 0.038 vs 1 | 3.8e-4 / 0.038 | ✓ |
| log Ẑ = log mean exp(logZ_r) | reproduced from `logZ_r` to ≤ 5.7e-14 in all 40 | | ✓ |
| pooled s_V / s_T (10 df each) | 0.005817 / 0.003244 | 0.005817 / 0.003244 | ✓ |
| **E1 AR r01** | Δ = −0.009635, se_comb 0.005879 (both arms at the island floor), **ratio 1.639** ≤ 3 | 1.64 | ✓ |
| **E1 AR r04** | Δ = −0.011863, se_comb 0.006735 (v_V = s_V²/2 = 1.69e-5; v_T = island floor 2.84e-5), **ratio 1.761** ≤ 3 | 1.76 | ✓ |
| E1, the other 8 datasets | 0.009 – 1.31; worst of all 10 = 1.761 | 0.01 – 1.76 | ✓ |
| E2 | consistent in 10/10. Smallest margin: NULL 0.0074 (log Z_T sits 0.0066–0.0070 below log Ẑ, against 3·se_isl ≈ 0.0007). Others 0.107–0.228. | PASS | ✓ |
| **H d_H(V,T)/d_H(T,f\*)** | AR r04 0.0125, ADJ-OPP r02 0.0136, AR r01 0.0073, NULL 0.0034; all 10 in 0.0034–0.0136, vs 0.10 | 0.0034–0.0136 | ✓ |
| H cross-file provenance | All 20 cells: `law_a`/`law_b` = the counted V/T `law.bin` by engine identity (header bytes 64–96 = `law.bin.json outputs`), with xeval seed = the eval's x seed. The W0 cells use the bypass build 066b70f8; the re-check with PR #87 (afef0e46, guard on) gives bit-equal h² and se. | | ✓ |
| **C per fit** | T max 143.96 (IND s2) ≤ 172.5; V max 2.91 ≤ 15. Per-fit billed = Σ stages in every file. | PASS | ✓ |
| C, batch reconciliation | Per-fit sums plus evidence = the sacct wave totals (CPUTimeRAW/3600, parent rows): W0 254.74 (T2 158.40 + V2 4.84 + evidence 91.50), W1 277.90, W2 221.15, W3 256.64 | | ✓ |
| rung total | billed **1,010.43**; counted 918.93 (T 879.08 + V 39.85); evidence 91.50 | 1,010.43 / 918.92 / 91.51 | ✓ (0.01 rounding) |
| evaluator params | identical in all 40 (n_x 4000, n_gh 64, n_draws 10⁴, n_test 10⁴, rel_cut 1e-12, top_k 1000, tail_r 1000, tail_groups 8, block_rows 500, threads 8), apart from `seed` | identical | ✓ |
| builds | 4 builds per arm (one per wave). All have git_commit eefcbc4a, g++ 14.3.0, flags `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`, libm sha 98677841; ISA portable (T) / sapphirerapids (V) | 4 per arm | ✓ |

## 4. The draft's own claims

| claim | verdict |
|---|---|
| Criteria table (§2), both columns | Correct. Every v2 cell was reproduced from the raw data. Registered column: D 37/40, S1 "7/10", S3/P/E1/E2/H NOT_EVALUATED, C/PAIR/S2/S4 PASS, as printed. |
| §4 step-by-step, v2 | Correct: rule 1 no, rule 2 no (hpm_miss 0, F_T − F_V ≤ 0, pred_fail 0), rule 3 no, rule 4 no, rule 5 CLEAN given this ACCEPT. |
| §4 step-by-step, registered | Correct, but the draft leaves the conclusion open. Adjudicated above: **INCOMPLETE** (F1). |
| "v2 governs" | Correct. ADDENDUM_1 was HQ-approved (H-21 (2)), and the diff is only that change. Conditions are met: (i) commit before any W1 read-back (60e28395 at 20:25 CST vs the first W1 read-back at 23:07); (ii) both outputs shown in the W1, W2 and W3 read-backs; (iii) the registered sha reproduces (verified here). The change can only re-classify escalated fits as delivered, and those fits follow the registered T method (D-26). |
| E1 strictly by rule: PASS, worst 1.76, AR r01 1.64 | Correct (§3). No miss, so no MARGINAL. |
| E1 escalation analysis | The numbers reproduce from my own gaps: diff −0.00890; Welch t −3.67, p 0.027, CI −0.01606 … −0.00175; exact permutation 12/1,140 = 0.0105. **The reading needs a fix (F2).** |
| Deviations log vs H-18…H-24 | Mostly complete: H-18 (b) and (c) are in the PREREG; H-21 (2) is item 1; H-23 (2) and (3) are items 2–3; H-24 (1) is item 6; e8aab325 is item 5. **Missing or misplaced: F4, F5, F6.** H-19, H-20/20a and H-22 are staffing and home rulings with no protocol effect; omitting them is fine. |
| Cost section | Correct (§3). Add the C robustness line (F7). |
| Tooling notes | (a) The 1-ulp miss reproduces: engine h² 0.007346601991972124 vs xeval …235, a difference of 1.1e-16 = 1 ulp of the affinity (≈ 0.9927). The compiler and libm differences are reported honestly as unconfirmed, as H-24 (2) asked. (b) All 10 `_batch_*/bin_version.json` hold the CXXABI_1.3.15 loader error; confirmed. (c) Guard history confirmed, and the W0 re-check is bit-equal. |
| "One build per arm" | A real deviation from SUBMISSION_PLAN §2 ("build once in W0 … then copy `bin/` unchanged into later waves") and from the PREREG header ("the two binary sha256"). It should be logged; it does not matter for the outcome (F4). |

## 5. Findings

| # | severity | claim / location | evidence | fix |
|---|---|---|---|---|
| F1 | **Medium** (code defect; registered label only) | Registered script prints MARGINAL; draft §2 leaves it open | S1 has no NOT_EVALUATED branch (v2 l. 669–672, registered l. 655–658). §4 rule 3 does not list S1, and §4's closing sentence says a missing fit is a D failure, not an HPM mismatch. | **Doc:** state "registered outcome per §4 = INCOMPLETE; the printed MARGINAL is a script defect (S1 scored FAIL on non-evaluable datasets)". Do not edit the registered script. Fix S1 in any successor script under its own pre-registration. No effect on v2: the defect is dormant when D = 40/40. |
| F2 | Low–Medium (interpretation; doc) | Summary 4 and §3b: "Escalation link: partly", headlined by CI −0.0161…−0.0018 and p 0.011 | The fit-level tests treat the 20 fits as exchangeable, but seeds share data and there are clear dataset effects (AR r04 has the largest gap at tier 0). The design-respecting test is the within-dataset sign-flip: 3/3 contrasts negative gives one-sided p = 1/8 = 0.125 (paired t p 0.11, CI −0.0199…+0.0044). The grouping was chosen after all 3 escalated fits had been seen (W0–W1; H-24 came at the W2 read-back), and W2–W3 added 0 escalated fits, so there is no out-of-sample test. | **Doc:** answer HQ plainly: "**Not established.** The escalated fits have the more negative gaps, but within dataset the effect is indistinguishable from zero (n = 3, p ≈ 0.11–0.125), a tier-0 fit has the largest gap, and the non-escalated fits are also offset negative." Keep the fit-level numbers, labelled as descriptive and optimistic (they ignore clustering). Replace "partly". No rescue and no over-reading: E1 passes by rule, and this note does not alter that. |
| F3 | Low (doc; answers the draft's point 3) | Draft gives the 20-fit mean −0.0039 (t on non-independent pairs) | At the dataset level (10 independent Δ_d): mean −0.00394, t(9) = −2.80, p = 0.021, 95 % CI −0.0071 … −0.0008; 7 of 10 negative. A systematic V < T offset of ≈ 0.004 nats (≈ 0.7 se_comb) is detectable at rung level, while every dataset is inside its own 3-s.e. bound. | **Doc:** add these numbers as a post-hoc observation (not a criterion), and recommend one line in the precision-study plan: measure the V−T log Ẑ offset against N and R′. |
| F4 | Low (deviation log) | §6 observation (ii): "one build per arm not met" | SUBMISSION_PLAN §2 says build once in W0 and copy `bin/` unchanged; the PREREG header binds "the two binary sha256". In fact there are 4 builds per arm, each wave rebuilt from shared worktrees (OPS_W0 §93). Mitigation (verified): same commit, compiler, flags and libm in all 40; W0 V vs V2 (two V builds) bit-identical outside provenance. | **Doc:** move it into the deviations log as an unapproved operational deviation, with the mitigation and its scope. Every criterion pairs V and T built in the same wave. Only the pooled E1 yardstick mixes builds, across seeds of AR r01 and ADJ-OPP r01 (W0 vs W2), and a build effect there could only widen s_A. No outcome effect. Report it to HQ. |
| F5 | Low (deviation log) | §6 observation (i): eval seed = data seed | PREREG §2 says "`eval` seed = the fit's engine seed". In all 40 fits, `params.seed` = the data seed (s2: e.g. 402020004, not 402020104). Effect: s1 and s2 evals of a dataset share x draws. V and T stay paired, and xeval used the same seed (20/20 verified). E1, P and S do not depend on eval randomness; H passes with ≥ 7× margin. | **Doc:** log it as a deviation from the PREREG §2 text, with "no effect on any criterion". |
| F6 | Low (doc) | Deviation item 4: "HQ id for the re-submission not stated …; counted-unit rule fixed at the W0 checkpoint, H-21" | The HQ GO is in LOG.md 2026-11-18 10:59 CST: rebuild both arms from the git clone of F and resubmit OV_W0_T2/V2, with OV_W0_V kept as a cross-check. The cause was GUARD-W (T merge invalid_input, git commit "unknown"; LOG 10:58). H-21's DECISIONS row does not state the counted-unit rule. | **Doc:** cite LOG 10:58 and 10:59 (the W0 incident and HQ GO). State that this is the "one infrastructure rerun per fit" of §4 for the 4 W0 fits, and that AR-T2 then had a stage-level rescue (e8aab325). |
| F7 | Low (doc) | §4 cost: C PASS | If the W0 first-attempt cost is charged to the same fit: AR r01 T s1 = 110.12 + 42.11 = 152.24, and ADJ-OPP r01 T s1 = 48.28 + 44.93 = 93.20. Both stay ≤ 172.5. | **Doc:** add one line saying C passes under either accounting. |
| F8 | Nit (doc) | §3b(iv): "log Z_T lower bounds sit 0.09–0.22 below both" | NULL is 0.0066–0.0070; non-NULL 0.093–0.216 | **Doc:** correct the range. Also 918.92 / 91.51 → 918.93 / 91.50 (or say "± 0.01 rounding"). |
| F9 | Low (doc) | §7: "CLEAN … releases the precision study and the 10⁴ science" | True per PREREG §4 rule 5. However, H-19 says the "precision study plan, 10⁵ and everything else wait for HQ's GO after the overlap verdict". | **Doc:** add "start still subject to HQ GO (H-19)". |
| F10 | Info (tooling) | Input plumbing | Duplicates are resolved by eval mtime, and the cost file depends on the `--cost-dir` order. `verdict.json` records neither the cost dirs nor a per-fit cost source. Correct in this run (verified). | Optional doc: give the exact command line in draft §1 (it lists the dirs already). Tooling, later: record the cost dirs and source in `verdict.json` and pin the unit list explicitly. |

No finding changes a criterion or the outcome.

## 6. Answer to task 5: is "CLEAN under v2" correct?

**Yes.**
- **ADDENDUM_1 makes v2 the operative script.** It was HQ-approved, it is a pure N-check change, and its conditions were met.
- **ADDENDUM_2 leaves C unchanged.** Its report-and-continue rule never triggered: max T 143.96, and 152.24 even under the stricter accounting.
- **Under v2:** D, PAIR, S1–S4, P, E1, E2, H and C all PASS, each re-derived here from the raw records. Rules 1–4 do not apply. Rule 5's review condition is met by this ACCEPT.
- **Outcome: CLEAN.** It releases the precision study (64 islands) and the 10⁴ science, subject to HQ's GO under H-19. **10⁵ stays gated by G-B.**
- **Registered script:** INCOMPLETE per §4 (it prints MARGINAL, F1). Informational only.

## 7. Files (reviewer scratch, `~/SMC_Engineering_Department/tmp/20261119-verdict-review/`)
- **Re-runs:** `v2/`, `registered/`, `*_stdout.txt`. All byte-identical to `W3_readback/final/`.
- **Independent derivation:** `indep_check.py`, `indep_check.out` and `indep_check.json` (all 40 fits, all criteria).
- **Supporting checks:**
  - `cross_prov.out`: cross-file law identity, 20/20.
  - `e1_esc_indep.out`: escalation statistics recomputed.
  - `cost_indep.out`: sacct reconciliation, plus the dataset-level offset test.
