# RT2: red team of the Phase-2 results (2026-10-13)

Read-only R scripts: Owls `/tmp/fb31_rt/`. No simulations were rerun.

## 1. BB product Ẑ outliers
**Verdict: no bug found. The likely cause is higher estimator variance in the BB particle system on S. The exact mechanism is uncertain.**
- The outliers go both ways: of 25 BB-S datasets with |e| > 5 %, 10 are negative and 15 positive. Mean e is −0.096 % against a standard error of about 0.13 %. A wrong start or wrong Z₀ would bias every dataset.
- The effect is limited to S. SD of the product log error is 0.037 for BB-S and 0.014 for Bern-S. On W the engines match (0.0068 vs 0.0077).
- BB starts with fewer distinct models: median after stage 1 is 976 vs 2,398 on S.
- S5_r005 is the extreme case:
  - Under BB it has 371 distinct models at stage 1 (2nd percentile) and the largest first jump: φ from 0 to 0.314, 270 nats in one stage.
  - Under Bern it goes from 0 to 0.079 (68 nats) and ends at e = +0.67 %.
- S4_r065 and S4_r014 look ordinary. No stored diagnostic predicts |e|: Spearman correlation is −0.02 with the within-scenario rank of φ₁ and −0.02 with the rank of distinct₁.
- **What would settle it:** rerun S5_r005, S4_r065, S4_r014, S4_r013 and S4_r092 under BB with 3 extra seeds each. If the errors do not recur it is variance. If they recur, the bridge fails on those datasets.
- **Gating on the hybrid Ẑ** is defensible, but Amendment 1 names no estimator, so it was our interpretation. The product estimator fails the 1e-3 median gate under both engines (Bern-S median |log err| is 0.0071–0.0106).
- **Action: report as a caveat.** Show the product numbers too: BB-S product RMSE is 1.17–5.16 % vs 1.05–1.74 % for Bern, and the product seed-SD ratio BB/Bern is 1.03–1.29.

## 2. Is the Plan-2 rule unfair to BB?
**Verdict: holds.**
- **W truths are correct.** Replaying spec steps 1–3 for 6 W datasets (W1_r003, W2_r050, W3_r077, W5_r012, W6_r100, W1_r041) reproduces the stored truth exactly. Signals match `per_variable_omission.csv`. HPMs recomputed from `top_by_size` match `per_dataset_decisions.csv`.
- **Truth size does not disadvantage BB.** Prior mass on sizes 2–4 is 0.22 under BB(1,30) and 0.245 under Bern(0.2). On S the gap runs against BB (P(5) = .014 vs .172), yet BB wins there.
- **The cause is the cost of each inclusion.** Adding a variable to a size-k model costs log((1+k)/(59−k)) under BB, from −4.08 to −2.40 for k = 0–4. Under Bern it is always −1.39. W puts t at about 2.5–4.5, where a stricter prior must lose. The opposite failure was not tested.
- **The margins are large.** R1 is −28 against −10 (discordant pairs 2 vs 30). R2 is +0.685 against +0.3. R3 fires in W1 (−17) and W5 (−15) under either reading.
- **Action: report as a caveat** that W covers only the omission side.

## 3. "BB engine at least as accurate"
**Verdict: flawed as worded. It is an artefact of the target, not the engine.**
- The hybrid advantage tracks the outside share f. Median BB/Bern ratio of f is 0.37–0.61 on S and 0.09–0.12 on W. The restricted-MAE ratios follow it: 0.64–0.83 on S, 0.35–0.39 on W.
- Normalising by √(PIP(1−PIP)) leaves the ratios at 0.30–0.83, so PIP spread is not the cause.
- Particle-only estimates are worse under BB:
  - RB-PIP restricted-MAE ratio is 0.96–1.85 (S4 1.85, just under the 2× gate);
  - product Ẑ is worse (finding 1);
  - BB has 2.5–5× fewer distinct particles.
- **Action: fix the wording before reporting.** Suggested: "BB passes every gate. Its visited-set estimates are more accurate because its posterior is more concentrated. Its particle-only estimates are 1.0–1.9× less accurate."

## 4. Bookkeeping
**Verdict: holds.**
- **Main runs:** for 1,200 cases × 2 engines, case_id, seeds, X/y, active set and prior type all match the data (0 mismatches).
- **Duplicates:** no duplicate dataset hashes and no duplicate y.
- **Enumeration merge:** `enum_strat` case_id and data_sha256 match the manifests for all 1,200 (430 Owls + 770 NOTS).
- **Seed files:** all 200 have the correct smc seed (data + 2e5 + 5e4·s) and seed_offset_index. All 200 symlinks point to the right file. The analysis reads only the `__s` names, so nothing is counted twice.
- **Second launcher:** same code hash (1ee964c4…). `smc_bern` holds exactly 1,400 entries with no partial files. Old vs new runs agree to ≤ 8e-13 on 550 pairs, with the same |V| and stage counts.
- **Minor:**
  - The `smc_bern_b` manifest.json lacks host, seeds, status and output checksums. **Fix the provenance.**
  - "C3 FAIL" is a rounding difference of 2.98e-12. **Explain it.**

## 5. Headline recommendation
**Verdict: the decision holds, but three phrases need correcting.**
- The figures 400, 382, 128, 104 and 431 are correct.
- "SMC = exact in 100 % of HPM decisions" is true for both priors (2,400/2,400).
- **(a) "BB-HPM is best only for strong signals" is mislabelled.**
  - BB's gain on S is real (discordant pairs 46 vs 15) and comes from fewer false inclusions: FP is .03 vs .13 in S1 and .07 vs .21 in S2.
  - BB omits more true variables in every signal bin: S 4–5 .17 vs .13; W 3–4 .60 vs .38.
  - Suggested wording: "BB-HPM trades omissions for fewer false inclusions. It wins only where supersets are the main failure (S1, S2, S5)."
- **(b) HPM over median is not supported on S1–S5:** discordant pairs there are 18 vs 14. The gain comes from S6 (15 vs 1) and W (27 vs 3).
- **(c) Bern(0.2)+HPM is the existing baseline** (FAILED_ATTEMPTS). Plan 2 means the proposed change is withdrawn; say so plainly. Also note that BFDR5 beats it in S1–S2 (93/87 vs 87/81).
- **Scope caveat:** p = 30 and n = 100 only, and S has one fixed truth per scenario.
- **Action: fix the wording before reporting.**
