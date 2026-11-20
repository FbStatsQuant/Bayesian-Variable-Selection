# MINILEG_CHECK_OPUS: independent check of the V-N mini-leg N verdict (Opus checker; Fri 2026-11-20)

**Decision: CONFIRMED-WITH-FIXES.** The literal registered outcome is **ADOPT N = 10⁴ at the frozen configuration (m 1, I_max 0)** and **KEEP N = 2,500 at I_max 3**. I reproduced every number that decides it from the raw records with my own reader. The two fixes are documentation only: neither changes a number, the outcome or the §6 row.

Object checked: `results/vn_minileg/MINILEG_READBACK.md` (Sonnet, untracked) and `readback/`. Rules: `MINILEG_PREREG.md` and `MINILEG_PLAN.md` (exp/P1M 5d8c77e8, committed 2026-11-19 23:34:14Z; the first V0 submission was 23:41:23Z). Also `precision1e4/PREREG.md` §3, `CAMPAIGN_FREEZE_ADDENDUM.md` and DECISIONS H-26/28/30/31/33/34. Scratch: `~/SMC_Engineering_Department/tmp/20261120-vncheck-opus/` (my own reader `own/reader.py`, the sacct cross-check `own/sacct_isl.py`, and the script re-runs). Nothing in the repo was edited except this file. No NOTS access, no commits.

## 1. What I re-ran and re-derived

| check | how | result |
|---|---|---|
| Registered material unchanged | `sha256sum` of the 4 scripts and 2 tests; `git log 5d8c77e8..HEAD` and `git diff HEAD` on PREREG, PLAN, the scripts, `tests/` and `vn_budget.py` | shas = PREREG §1 (except the test-sha typo, F1); **0 commits and 0 working-tree changes since 5d8c77e8**; the PREREG was committed 7 min before the first submission |
| Self-tests | `python3 -I tests/test_vn_golden.py`, `test_vn_offset_contrast.py` (`PREC_TEST_TMP` set to the scratch dir) | 4 OK + 1 OK |
| Frozen rule, exact PREREG §3.2 command | own clean cost dir (35 per-run links, no `cost_batch.json`, **no duplicate run id across batches**: asserted) → `precision_freeze_vn.py --baseline 2500,1,0 --knob "N=10000 (m=1,I0):10000,1,0:up"` | **ADOPT**, 0 identity failures; `decisions`, `detail`, `targets_per_fit` and `identity` equal to the read-back's `freeze.json` |
| Registered rule verbatim (I_max 3) | `precision_freeze.py` (7cdd69a1…) | **`N=10000 (m=1)` KEEP**; it also reproduces `m=4` KEEP (c_X 2.326 = ADDENDUM), `I_max=0` ADOPT and `N=10000 (m=4)` NOT_RUN; equal to the read-back |
| M1–M3 per fit, per dataset, HPM, recorded arm | **own reader** straight from `eval.bin.json` / `calib_meta.json` / the batch cost files (not the scripts' `find`) | all 24 fits `completed`, R′ 64, recorded (N, m, I_max, I_used, rule) = plan; HPM identical within each dataset across X ∪ B at both I_max; ratios below |
| Islands billed core-h | own sum of `CPUTimeRaw` over the island array tasks in every batch's `sacct_dump.txt` (mapped via `submissions.jsonl`) against the `cost_<run_id>.json` used by the rule | max abs difference 4e-5 core-h; 64/64 tasks COMPLETED for every fit |
| Δ_N | (a) the registered `precision_offset.py` + `vn_offset_contrast.py` re-run: outputs **byte-identical** to the read-back's `offset.json`, `offset_per_fit.csv` and `vn_offset_contrast.json`; (b) **own derivation from raw `logZ_r`** (the k = 64 block = lse(logZ_r) − log 64; the T reference cancels in the paired contrast) | **+0.00062 [−0.00087, +0.00210]** (I_max 0; per dataset +0.00024 / +0.00031 / +0.00130) and **+0.00089 [−0.00073, +0.00251]** (I_max 3), identical |
| XB2 | own comparison of the XB2 record with the leg's A0 `…-I0-c1-s1` | `logZ_r` 64/64 equal, HPM equal, island `output_hash` 64/64 equal, the whole `evidence` and `pip` blocks equal |

**Rule inputs, frozen configuration (own reader = script):**

| metric | AR | AR-weak | ADJ-OPP | r (geo. mean) | bar 1/√c_X = 0.516428 | margin |
|---|---|---|---|---|---|---|
| M1 | 0.4968 | 0.5248 | 0.4934 | 0.50481 | ≤ ✓ | 0.0116 |
| M2 | 0.5099 | **0.5856** | 0.4562 | **0.514556** | ≤ ✓ | **0.001872** |
| M3 | 0.4798 | 0.4807 | 0.4778 | 0.47943 | ≤ ✓ | 0.0370 |

c_X = 105.972 / 28.263 = **3.749560** (islands billed, X 6 fits / B 6 fits). Every per-dataset ratio is < 1, and HPM is identical. → **ADOPT.**
At I_max 3: c_X 3.7896, bar 0.5137; r = 0.4704 / 0.4666 / **0.5719 (M3 fails by 0.058)** → **KEEP**.

## 2. Is c_X unambiguous? Yes, for every reading the text allows

PREREG §3.1 (and leg PREREG §3, the script docstring): "c_X = mean billed **islands** core-h of the arm's fits / the baseline's (cost files; calibration excluded; …)". It names the quantity (billed, islands stage), the source (the cost files) and the fits (the arm's fits and the baseline's, both defined in §3.2 and PLAN §1). There is no fit selection to make, since every one of the 6 + 6 fits is pooled. The cost directory leaves no freedom either: there is exactly one cost file per run id. XB2 and r04 are excluded by the run-id pattern and by PREREG §2 ("XB2 and r04 are not rule inputs").

The only textual latitude is "mean of X / mean of B" against "mean of the per-pair ratios". The docstring says "mean over the fits of … (X) / the same for B", i.e. a ratio of means, which is what the script does. I tested every variant (break-even c_X for M2 = 1/0.514556² = **3.7769**):

| c_X reading | c_X | bar | outcome |
|---|---|---|---|
| **islands billed, ratio of means (registered)** | **3.7496** | **0.5164** | **ADOPT** |
| islands billed, mean of the 6 pair ratios | 3.7432 | 0.5169 | ADOPT |
| islands billed, geo. mean of pair ratios / of dataset ratios | 3.7400 / 3.7439 | 0.5171 / 0.5168 | ADOPT |
| whole-fit billed (calibration incl.; **excluded** by the text) | 3.611 | 0.526 | ADOPT |
| islands + calibrate billed (**excluded** by the text) | 3.698 | 0.520 | ADOPT |
| islands **wall** (max task; not "billed") | 4.07–4.26 | 0.484–0.496 | KEEP |
| the quote's c_X 3.85 (not measured; §3.1 says measured) | 3.85 | 0.5097 | KEEP |

Only readings that the text rules out flip the verdict: wall time instead of billed core-h, or the quoted c_X instead of the measured one. Every reading of "billed islands core-h" that the text admits gives ADOPT. One more option the text leaves open is metric pairing: the geometric mean of per-seed-pair ratios instead of ratios of replicate means. That gives M2 = 0.5151, which still passes. **The prereg is unambiguous.**

## 3. Governing configuration, and whether anything was chosen post hoc

PREREG §3.3, verbatim: "**N\*(configuration) = 10⁴ iff that configuration's run returns ADOPT** … The two configurations decide independently; **there is no AND and no veto** … **The frozen configuration governs the plan** (it is the one currently frozen); the I_max-3 result is what is used if the G-B rule reverts 10⁵/1M to I_max 3." Also: "If the two configurations disagree, the disagreement is **reported as a finding** … each still decides its own configuration." And: "Judgement is not substituted for the rule after the data are seen."

Every input was fixed before the data existed:
- **Baseline cells:** (2,500, 1, 0), as written in §3.2.
- **Knob string and command:** verbatim from §3.2.
- **Pooling:** all 6 + 6 fits, as in §3.1.
- **Pairing:** by seed (PLAN D1, committed), and verified by the read-back (pairing identity 12/12).
- **Baselines:** the leg's F-build twins, validated by XB2, which I confirmed.

**ADOPT is a literal application, with no post-hoc choice.** The read-back's c_X = 3.85 sensitivity is labelled descriptive and is not used. That is correct.

## 4. The 1M consequence and the closed spend

- **The row is the pre-declared one.** PREREG §6, "ADOPT (default, self-releasable within S2's 17.3k only after HQ accepts N\* at the verdict)":
  - 10⁵ rung at N 10⁴ (12 fits);
  - 1M at N 2,500 frozen for the 22 approved fits, plus ONE N 10⁴ fit on the rep-1 data in place of the N 5,000 self-check;
  - option D at N 2,500.

  The read-back quotes this row correctly.
- **The numbers are right.** Pre-declared S2: 17,261 (`vn_budget_output.txt`, sha = PLAN §8). I re-ran `vn_budget_rebase.py` and its output is byte-identical: **17,122** at measured f 3.768 (17,187 at 3.85; 17,425 at the maximum f 4.15). My recomputed f is 3.768 (3.50–4.15). S1b (all at N 10⁴) is 34.9k, which does not fit.
- **Closed spend 2,686.91 is correct, with no double counting:**
  - 975.5 to 11-18 10:05 ("≈" in LEDGER l.46);
  - 1,010.43 overlap (LEDGER l.48);
  - 462.48 leg: `staging/precision1e4/prior_after_S10.json`, 194 rows, identical to the results copy; it does **not** contain VN_ID_1 `4-AR-n200-r01-V-s1`;
  - 1.99 VN_ID_1: `F2_ID/…/cost_4-AR-n200-r01-V-s1.json` = 1.9923;
  - 236.51 mini-leg: `staging/vn_minileg/prior_after_V2.json`, 15 rows, identical copy, no overlap with S10 and no VN_ID row.

  Cross-check: the LEDGER's 2,041 − 55.09 (A0 + P1, already inside 462.48) + 462.48 + 1.99 = 2,450.40, and 2,450.40 + 236.51 = 2,686.91. The read-back is right that "2,450.40 + 236.51 + 1.99" would count VN_ID_1 twice. Remaining: 25,613.

## 5. The two defects (both confirmed; both documentation-level)

| # | defect | confirmed | effect | how to log |
|---|---|---|---|---|
| F1 | PREREG §1 prints `9ef9b9e7…417becedacfcb65073c10d` for `tests/test_vn_offset_contrast.py`. That string is **65 hex characters, not a valid sha256**. The committed blob (`git show 5d8c77e8:…`) and the working file both hash to `…417b8a228a0f2ab9a1331`, which is the value in PLAN §8. | yes | none. The test file is unchanged since the commit and passes. No rule script is involved. | Do **not** edit the committed text silently. Add a dated entry to PREREG §10 (Deviation log), "erratum, documentation only: correct sha256 of test_vn_offset_contrast.py = 9ef9b9e7…a9a1331 (= PLAN §8, = blob at 5d8c77e8); file unchanged", and one LOG line. |
| F2 | The registered `precision_offset.py` drops `4-ADJOPP-n200-r04-V-s2`. Its id matches the overlap-V pattern `-(V)-s<seed>`, so the script expects (2,500, 1, 3) and the record says I_max 0 → ARM_MISMATCH. | yes (`dropped fits` in my re-run) | **None, for two independent reasons.** (i) r04 is not a precision dataset, so it is in no N cell. (ii) The overlap records have no r04 fit, so r04 has no T reference and could not enter any δ. The overlap cell still has 20 fits / 10 datasets and reproduces −0.00394 [−0.00712, −0.00076]. `…-VI3-s1` does not match the pattern at all. | Classify it as a **run-id naming collision** in the mini-leg's report-only fits, with the registered identity guard **working as designed**: it is not a defect of the registered script. Note it in the read-back §6 and OPS_VN. Rule for future plans: give report-only fits ids outside the registered patterns. Had this fit been at I_max 3, it would have entered the `ovl` cell **silently**, since r04 has no T reference only by luck of the overlap design. |

## 6. The r04 reading

**Supported.** I read the three records:
- σ̂ = sd(log Ẑ_r): 1.0880 (original I_max 0, S1), 1.1033 (I_max-3 twin), 1.3415 (seed 2, I_max 0).
- `fit.meta.flags.E2` is True in all three, and HPM = MPM = S₀.

The PREREG §7 guide is literal:
- The twin is elevated, so the cause is "a property of the dataset / seed, not of I_max".
- The seed-2 fit is also elevated, so the I_max-0 elevation repeats at another seed.

"Dataset-specific" is therefore the guide's own conclusion, with no attribution beyond it.

**On read-back point 7:** M1 and M2 are bit-identical between the original and the I_max-3 twin, while the island `output_hash`, `logZ_r` and 40 calib sections differ. M1 and M2 are occupancy-based: computed from exact marginals over the visited model sets. At the same seed both runs visit the same top-1,000 sets, so `logZ_occ` is identical at every M. GB_PLAN summary item 4 found the same thing on other datasets ("same-seed M1 and M2 ratios 1.000 ± 0.001 in 14/14 pairs at 10⁴"). The elevation sits in the importance weights (log Ẑ_r), not in model discovery. This is my reading and it does not change the r04 line.

## 7. Findings

| # | severity | finding |
|---|---|---|
| 1 | — | Both rule outputs, c_X, the per-dataset ratios, HPM, identity, XB2, Δ_N, f, the §6 row and the closed spend are reproduced exactly. |
| 2 | fix (doc) | F1: the sha typo in PREREG §1. Log it as a §10 deviation-log erratum. |
| 3 | fix (wording) | F2: in the read-back, call it a run-id collision caught by the identity guard, with zero effect, rather than a script defect. |
| 4 | note | The ADOPT is thin. The margin is 0.0019 on r, which is +0.027 (0.7 %) on c_X. That is well inside the noise of both inputs (§8). |
| 5 | note | `GB_PLAN.md` §1 row "I_max of the mini-leg's N = 10⁴ arms" still says (N 10⁴, I_max 0) "was **not run at 10⁴**". MINILEG_PLAN already flags this. Update it when G-B is finalised. |
| 6 | note (for HQ) | H-34 (20-seed 1M block, +6.4k at N 2,500, dated 11-20) postdates the §6 table. S2 17,122 plus 1.25 × 6.4k ≈ **25.1k**, which fits. S4 (27.0k) plus H-34 does **not** fit. |

## 8. What HQ must hear

1. **The registered outcome is ADOPT N = 10⁴ at the frozen configuration. It stands, with no override in either direction.** The prereg is unambiguous: every reading of "billed islands core-h" the text admits gives ADOPT, and the I_max-3 KEEP is a FINDING, not a veto (§3.3). This is the same posture as H-30's I_max = 0 freeze: accepted as the rule reads it, and fragile.
2. **What ADOPT means here.** N = 10⁴ is *not worse per core-h* than spending the same core-h on more N 2,500 islands. It does not mean "better". All nine ratios at I_max 0 sit at ≈ 0.48–0.59, which is plain 1/√N scaling, exactly the knife-edge that PREREG §3.4 predicted (P(ADOPT) ≈ 0.25–0.46 at a true ratio of 0.50). Across both configurations, the evidence says N = 10⁴ is roughly cost-equivalent to islands at p = 10⁴, n = 200.
3. **How fragile it is, honestly stated:**
   - The margin is 0.0019 on M2, and M2's per-dataset log-ratios have sd ≈ 0.12. So the geometric mean carries roughly ±7 % (1 se) against a 0.36 % margin.
   - c_X needs only +0.027 to flip it. Billed island cost of *identical* work varies by about 10 % between runs: XB2 is bit-identical to its F twin but billed 5.73 against 5.19 core-h.
   - That same datum suggests that the F2 / time-of-run mix inflates c_X, which works **against** ADOPT. If XB2's cost replaced its twin's, c_X would be 3.68 and the bar 0.521 (descriptive only; not a rule input).
   - So the build mix does not manufacture the ADOPT, but the call is within noise. A repetition could plausibly KEEP.
4. **The two configurations disagree** (I_max 3: M3 0.572 > 0.514). This goes as the pre-declared FINDING to HQ + Theory: at I_max 3, N buys less on σ̂. If G-B's I_max twin rule reverts 10⁵/1M to I_max 3, N\* is 2,500 for that configuration.
   - **Sequencing consequence:** run the 1.3k core-h 10⁵ N = 10⁴ rung only after the G-B I_max verdict holds I_max 0, so the spend cannot become moot.
   - The G-B finalisation should state at which N the I_max-3 twin runs. Under N\* = 10⁴ its pair tests I_max at N 10⁴, while the fallback configuration's own N\* is 2,500.
5. **1M under the pre-declared ADOPT row (S2):**
   - 10⁵ rung at N 10⁴ (12 fits);
   - 1M at N 2,500 frozen for the 22-fit set, plus ONE N 10⁴ fit on the rep-1 data (≈ 1,061–1,083);
   - option D at N 2,500.

   Total **17,122** with reserve (re-based; 17,261 pre-declared) against 28,300. Closed: **2,686.91**. It self-releases only after HQ accepts N\*. All-N 10⁴ at 1M (34.9k) does not fit. The H-34 20-seed block must stay at N 2,500 (≈ 25.1k total with S2).
6. **Caution on S5** (R′ 4 at N 10⁴, "budget-neutral"). PREREG §3.1 says an ADOPT makes it "available", but its equal-precision premise rests on this 0.0019 margin. R′ 4 would also cripple the island-spread diagnostics themselves (M1–M3 and σ̂ estimated from 4 islands). HQ should not read the ADOPT as evidence for S5 without the D-6 ruling weighing that.
7. **Fixes before the manager commits the read-back:** the F1 erratum (PREREG §10 + LOG) and the F2 wording. Neither touches a result.
