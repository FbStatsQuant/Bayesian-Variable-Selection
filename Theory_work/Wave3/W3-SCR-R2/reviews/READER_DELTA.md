# READER_DELTA.md — row 3.7 (Theorem 8, certified screening), from W3-SCR-R2 (CP3 package; RIDER_RULES §5, PROTOCOL_v4 H6)

**v2 (leg 3, 2026-11-16), after HQ H5 card 9: AGREED to form (a), plain; conditions binding.** v1 (leg 2, after the R3
bind) is superseded. Diff v1 → v2: `READER_DELTA_v1_v2.diff` (this folder).

Written by the W3-SCR-R2 coordinator, **after** the R3 bind (`bind: OK`, MANIFEST_R3 `19847f54…`, see `../CHECKPOINT_2.md`).
This file is for HQ → W3-READER. Nothing is written in W3-READER's folder, and no W3-SCR file is touched. The frozen
manifests are unaffected (this file is in W3-SCR-R2/reviews/, outside the W3-SCR tree).

**Read-only source.** `/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md`, §8 "Theorem 8 —
Certified screening", row thm8, lines 727–816 (`<!-- ROW thm8 BEGIN/END -->`), section version 0.5, unchanged at
origin/theory/W3-READER 45d39fb4 (file last changed at e20d287f). sha256 of lines 727–816:
`db18fbe1eca2664937bb96762b4475163371470722c03db706fa428eb9188396`. (v1 printed `8b956c02…`, which is the sha of lines
727–818; corrected here.) Card row: `CLAIMS_CARD.md:60` and `:100-104`.
**Masters.** `W3-SCR:A1@1.0.0` (`Theory_work/Wave3/W3-SCR/STATEMENT.md:158-163`) for Theorem 8; `W3-SCR:A-inf@1.0.0`
(`STATEMENT.md:87-90`, definitions at §1 `:49-63`) for Theorem 8′. Both were ACCEPTed by both seats in R2 (MANIFEST_R2
`96488f34…`) and in R3 (MANIFEST_R3 `19847f54…`), with all gates PASS in R3. STATEMENT.md is unchanged between the two
manifests.

## 1. Current reader text (thm8 v0.5): what it already says
- Theorem 8 (A1)–(A3), lines 731–747: the floor κ, signal minimum b₀, ℓ¹ bound M and noise variance σ*² are **named as
  fixed in n**. (A3) includes q_n ∈ {0, …, K−1}. Conclusion: P(output, Ŝ certified, |Ŝ| ≤ q_n, S₀ ⊄ Ŝ) → 0.
  n-varying signals are excluded (open item SCR-R1).
- Placements, lines 749–762: the abstract clause names all four constants as fixed in n, but gives c₁ only by name and
  **omits q_n ≤ K−1**. Forms (a) / (b1) / (b2).
- Theorem 8′, lines 764–782: master A-inf in words. Its form depends on the R2 per-claim table.
- Honest limits, lines 799–802: "None. It is a one-sided guarantee (no false negatives among small certified models)",
  then the SCR-C remark. The parenthesis reads like a guarantee **conditional on certification**, which the master does
  not give (it bounds an intersection probability).

**Fidelity check against the masters** (lines 731–747 and the abstract clause against STATEMENT.md:158–163; Theorem 8′
against :87–90 and :49–63).
- The four fixed-in-n constants, c₁ = κ²b²/(200(M²+σ²)), the conclusion event and the p ≤ n^A consequence match in the
  body. Theorem 8′'s ratio, τ_n² and Γ_n match.
- The abstract clause omits q_n ≤ K−1 (fixed in §3, condition 2).
- One harmless wording point: the reader calls γ(t|S) "the decrease" of the quadratic form, while STATEMENT:54–56 defines
  γ = ((n+1)/n) × that decrease. The factor tends to 1, so the liminf condition is unchanged.

## 2. What changes (form choice, abstract wording, honest limits; no mathematics)
1. **Form (a), plain** (H5 card 9 AGREED). The abstract clause names κ, b, M, σ* as fixed in n. The (b1) label and the
   (b2) option are removed. **Theorem 8′ is plain** (A-inf ACCEPTed in R2 and R3).
2. **c₁ in the abstract** (card 9 condition 1): "with an explicit constant c₁ depending only on κ, b, M, σ*". The
   formula c₁ = κ²b²/(200(M²+σ*²)) stays **in the body only** (Theorem 8 (A3), unchanged). The 200 is a proof artefact.
3. **q_n ≤ K−1** (card 9 condition 2): **stated in the clause** as "q_n below the method's model-size cap min(p, ⌊n/2⌋)".
   This is the master's own hypothesis q_n ∈ {0, …, K−1} with K = min(p, ⌊n/2⌋) (STATEMENT.md:18, :160), so no bridge
   and no new step. (A bridge from the other hypotheses was possible in part, but it is not used, so no line check is
   needed. See §4.)
4. **Honest limits, required** (card 9 condition 3): replace "None" with the two lines in §3. The theorem bounds the
   probability of an **intersection** event. It is not a guarantee conditional on certification, not "the method
   returns a superset w.p. → 1", and a run is not claimed to certify a small model w.p. → 1 (STATEMENT.md:217–218).
5. **Certification frequency** (card 9 condition 4): a line next to the row, and a qualifier on the card's "holds
   where 3.1–3.2 may fail" (§5).
6. **Gating** (unchanged from v1): changes 1–5 apply **only after acceptance**, that is once HQ accepts the R3 result and
   the recorder replaces the INTERIM LABEL on `W3-SCR:A1` and `W3-SCR:SCR-G`. Until then row 3.7 stays in form (b1). The
   status string stays verbatim from the registry ("PROVED-CHECKED"; the label sits in the evidence field).

## 3. New reader text (proposed, to apply after acceptance)
**Abstract clause (form (a), plain):** *"Certified screening: if the design has a sparse eigenvalue floor κ on models
of size q_n+s₀, the true coefficients satisfy θ*_min ≥ b and ‖θ*‖₁ ≤ M, the constants κ, b, M and the noise variance
σ*² are fixed in n, q_n is below the method's model-size cap min(p, ⌊n/2⌋), and (q_n+1) log p + log n ≤ c₁n with an
explicit constant c₁ depending only on κ, b, M, σ*, then the probability that a run produces output, certifies a
reported model of size at most q_n, and that model misses a true predictor tends to zero — with no visibility,
leakage, start or block condition."*

**Theorem 8 (body):** keep lines 731–747 unchanged. (A2) names the four constants as fixed in n; (A3) gives the
formula for c₁ and q_n ∈ {0, …, K−1}.

**Placements block (replaces lines 749–762):**
- **Abstract:** the clause above, form (a), plain (second SCR council round passed: R2 + diff round R3, MANIFEST_R3
  `19847f54…`, both seats PASS; H5 card 9; HQ acceptance of <date>).
- **Body:** Theorem 8′ (n-varying signals; master `W3-SCR:A-inf`), plain.

**Theorem 8′:** keep lines 764–778. Replace the "Form dependency" paragraph (lines 779–782) with: *"Reviewed together
with Theorem 8 in the second SCR council round; A-inf ACCEPTed by both seats (stated plain)."*

**Honest limits (replaces line 800's "None. It is a one-sided guarantee (no false negatives among small certified
models);" and keeps the SCR-C remark that follows, starting "exact recovery from the certificate needs …"):**
- *"The bound is on the probability of an intersection: a run produces output, certifies a small model, **and** that
  model misses a true predictor. It is not a guarantee conditional on certification, and it does not say that the
  method returns a superset of the true model with probability tending to one."*
- *"A run is not claimed to certify a small model with probability tending to one (STATEMENT:217-218); how often it does
  is reported from numerics (see the certification-frequency line)."*
- *"It is one-sided: certified small models are not shown to equal the true model;"* followed by the kept SCR-C remark.

**Certification-frequency line (next to the row; text in §5).**

**Update log line:** `v0.6 <date>: [W3-SCR-R2 CP3; H5 card 9] form (a) for row 3.7, plain (second SCR council round
passed, R3 bind OK 19847f54…); Theorem 8′ plain (A-inf ACCEPT); abstract: c₁ by name only (formula in body), q_n below
the cap min(p, ⌊n/2⌋) stated; honest limits: intersection event, certification not claimed w.p. → 1;
certification-frequency line (EQUAL).`

## 4. Bridges needed
None.
- Theorem 8 is the master A1 with the floor named in standard terms. Theorem 8′ is A-inf in words.
- The abstract's q_n condition is the master's own hypothesis, restated. It is not derived from the others.
- The changelog tag is EQUAL: no hypothesis or conclusion moves. Adding the q_n cap to the clause removes an omission;
  it does not change the theorem.
- *Bridge not used (for the record):* the other hypotheses give q_n + 1 ≤ ⌊n/2⌋ (κb ≤ M, `lemmas/L7_master.md:103-104`, gives c₁ < 1/200), but
  they do not give q_n < p. That gap could be closed only by a separate reduction (if q_n ≥ p = K, the size-K model is
  [p] ⊇ S₀). This would be a new step needing a Sol line check, which is why the clause states the cap instead.

## 5. Certification frequency (card 9 condition 4)
**Finding.** In every existing study with a certification field, the method certified a small reported model in
essentially every completed run, strong-factor designs included. Certification is therefore almost never the binding
event. Theorem 8's content is in its hypotheses. At these constants (A3) requires n ≳ 1,450: κb ≤ M
(`W3-SCR/lemmas/L7_master.md:103-104`) gives c₁ < 1/200, so (A3) gives log n < n/200; the studies below have n ≤ 200.

| study (code) | design | fits | certified | certified, small | small and ⊇ S₀ |
|---|---|---|---|---|---|
| 2,400-fit production study (v2.2.1 core; flag = final search only) | n = 200, p ∈ {500, 1000}, s₀ = 14, S1–S6 (S5 = 0.7 within / 0.3 between blocks; no one-factor design), c ∈ {1, 0.5} | 2,400 (2,394 completed, 6 `resource_limit`, all S5) | **2,394/2,394 completed** | no per-fit size; mean 13.9–14.1; ≤ 28 = 2s₀ provable for 2,194 | ⊇ S₀ in 1,996/2,394 (all sizes) |
| W3-P6 strong-factor (main 2252d57, both searches) | cs(ρ) x = √ρ f + √(1−ρ) e, ρ ∈ {.3,.5,.7}; fac2; s5; n = 40–150, p up to 10n, s₀ ∈ {4, 8} | 376 | **376/376** | 376 (|HPM| ≤ 2s₀, max 8) | 275/376; p ≥ 2n: 165/234; cs ρ ≥ .5, p ≥ 2n: **109/172** |
| SCR N1 (main 2252d57) | n = 100, p = 400, s₀ = 4; independent, AR(.7), equicorrelated .5, 3-factor; strong / weak | 80 (71 finished) | **71/71 finished** | 71 (size ≤ 5) | strong 32/32, weak 2/39 |

Sources (file:line):
- **Production study.**
  - `Theory_work/Old_Projects/New_BVS_Headquarters/03_results_and_conclusions.md:168`: "In all 2,394 completed fits … `local_certified = TRUE`".
  - `Results/2026-10-28_New_Campaign/H2_20261102/HEADLINE_H.md:140`: 2,394 completed + 6 `resource_limit`.
  - `Results/SMC_BVS_v3_production/p0500/smc_flag_rates.csv` and `p1000/smc_flag_rates.csv`, column
    `n_local_certified_false`: 6 in total, all S5. Those 6 are listed at
    `Scripts/Campaigns/2026-10-28_New_Campaign/ops/PRODH_COMPLETION_20261102.md:15-26`.
  - Containment and sizes: `p*/exact_recovery_long.csv`, rows SMCBVS/hpm (err_* counts, tp/fp means).
  - Scenarios: `Docs/Records/STATUS_BRIEFING_20261028/BRIEFING.md:52-57`.
- **W3-P6.** Per-fit field `local_certified` in the NOTS record copies
  `/home/fb31/SMC_Theory_Department/records/theory_w3/*/raw/fits.jsonl` (15 runs). I recounted 376/376 certified,
  376 small and 275 containing S₀. The repo copies `Theory_work/Wave3/W3-P6/reviews/R02_inputs/*_derived.jsonl` lack the
  field. Designs: `Theory_work/Wave3/W3-P6/DESIGN.md:13-14`.
- **SCR N1.** `Theory_work/Wave3/W3-SCR/REPORT.md:87-100` (table and totals) and `numerics/SUMMARY_N1_N2.md:18`. The
  equicorrelated and 3-factor strong cells are conditional on finishing (5/10 and 7/10 finished, `REPORT.md:95, 97, 108-111`).
- Search notes: `CERT_FREQ_SEARCH.md` (this folder; helper Sonnet 5.5, read-only search; W3-P6 and production counts
  re-checked by the coordinator).

**Worst strong-factor cells (W3-P6, n = 50; all certified and small):**
- cs ρ = .5, p = 250, s₀ = 8: 0/20 contain S₀.
- cs ρ = .7, p = 250, s₀ = 4: 4/20.
- cs ρ = .5, s₀ = 4: p = 250 10/21; p = 500 11/21.
- At n ≥ 75 and p ≥ 188: 49/51 contain S₀.

**Certification-frequency line for the reader (next to row 3.7; numerics, not a theorem):** *"In existing numerics the
method certified a small reported model in essentially every completed run (2,394 of 2,394 in the 2,400-fit study at
n = 200; 376 of 376 in the strong-factor experiment with n ≤ 150 and p up to 10n; 71 of 71 in the screening study at
n = 100). On strong-factor designs (equicorrelation ρ ≥ 0.5) at n = 50 and p ≥ 2.5n, the certified small model missed a
true predictor in 61 of 122 fits. Theorem 8 holds asymptotically under (A1)–(A3); at these constants (A3) requires
n ≳ 1,450."*

**Consequence for the card (W3-READER decides the wording).**
- `CLAIMS_CARD.md:60` says row 3.7 "holds where 3.1–3.2 may fail (strong factors, masking)". As a theorem statement
  this is true, because its hypotheses involve no visibility condition.
- Scope statement for the card (neutral wording, owner rule):
  "asymptotically, under (A1)–(A3), row 3.7 holds where 3.1–3.2 may fail", with the certification numbers above
  stated as facts next to the row (H5 card 11).
- No small-run proposal is drafted, because data exist (card 9 condition 4 asks for one only if no data has it).
- Gaps, if HQ wants them closed: the production study has no per-fit HPM size, and no strong-factor run has n ≥ 200.

## 6. Not part of this delta
- SCR-R1 (dropping "fixed"): stays a post-freeze rider. `../SCR_R1_NOTE.md` answers YES (a short corollary of SCR-A with
  one side condition); it is not proved here.
- A1° (beta-min at rate σ√(𝐋_n/n)): a separate claim with different hypotheses (STATEMENT:165–169), kept out of
  Theorem 8.
- The registry INTERIM LABEL itself: the recorder replaces it after HQ acceptance, not this file.
