Manifest verify printed `verify: OK MANIFEST a08a238a2e84c980ce1b80cd8da237af74d855012f290ff32b99d84d550800f4`. The converter ran on a scratch copy in `.rc_tmp/measd_r3_opus/`. I edited no tracked file, committed nothing and started no subagents. `walks/T9_Thm10.md` is not on this branch, so I read it from `origin/theory/PRE-LEAN-walkB` (commit dc2e7174) into scratch.

# R3 council review (Opus seat): W3-SAMP:MEAS-D

## 1. Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 (W1) | REJECT | The proof never argues that 𝓜_r is Borel (F5). The Islands bullet (`MEAS_D.md:37`) cites Lemma B, but Lemma B's record Φ leaves out the cache and ledger and records only the path (`W1-N1/lemmas/L1_bridge.md:14-20`). 𝓜_r also contains rejected swap proposals, which are scored and then may be dropped (`cpp/v3_engine.h:152-158`, `:172-178`). The only augmentation in the ticket adds the π₀ draws, nothing else (`D_theorem.md:25-26`). No premise is added. |
| 1 (W2) | ACCEPT | P1 (`MEAS_D.md:42`) is correct. Details under §2. |
| 1 (W3) | ACCEPT, with E13 | Proved by Step 6 (`MEAS_D.md:50`). The integrability of 1_{𝒜°}Ẑ uses the joint law of §0 through Step 5. The sentence at `STATEMENT.md:190` puts it before "under the joint law of §0", so it should say so (E13). |
| 2 | ACCEPT | Checked against the code; details below the table. |
| 3 | ACCEPT | (C-v) and (TR-d) are both covered. Each input is used at one fixed island, with no independence across islands. Clause by clause under §2. |
| 4 | ACCEPT, with E15 | The ledger's offers are listed in the note below the table. P2 omits only the LS0 centre S̃₀, which is a data function by Step 2. |
| 5 | ACCEPT | E9, E10, E11, E12, the §3 Mathlib rows, the §4 Theorem 10 line and the §5 κ_n bullet; details below the table. |
| 6 | ACCEPT | See the note below the table. No new C or S. |

**Item 2 detail (Step 6).**
- **The formula.** `cpp/v3_score.h:59` gives log C_n = a₀log(2b₀) + lgamma(a₀ + n/2) − (n/2)log π − lgamma(a₀). `:223` gives logm = logCn − ½(ldH − ldA) − ν log(2b₀ + Q), with H = (n+1)G_S + I and A = G_S + I (`:175-183`). `:60` gives the S = ∅ case: D = 1 and Q = yᵀy.
- **The constants.** a₀ = b₀ = 0.01 are hard-coded (`v3_score.h:14`; also `W3-T03ACC/STATEMENT.md:29`).
- **The bound.** D_S ≥ 1 holds eigenvalue by eigenvalue. Q_S ≥ 0 is Lemma V (`S_one_step.md:7-15`, S = ∅ included). So m(S) ≤ κ_n.
- **κ_n.** κ_n = (2b₀)^{−n/2}Γ(a₀ + n/2)/(π^{n/2}Γ(a₀)). It does not involve p, the data or 𝓒.
- **Z.** ϖ(S) = w(|S|)/W_K, so ϖ sums to 1 over Ω (`v3_score.h:61-70`; T03ACC:27). Hence 0 < Z ≤ κ_n.
- **Ẑ_r.** (MR-b) at h ≡ 1 is E[W_r | 𝓒] = 1 on 𝒜 (`STATEMENT.md:111`). With Step 5's [0, ∞] form this gives E[1_{𝒜°}Ẑ_r] = E[1_{𝒜°}Z] ≤ κ_n.
- **New edges.** Both are correct. `W3-PSHARP:S@proof:Lemma-V` is the existing form: claims.tsv rows `W3-PSHARP:C` and `W3-PSHARP-R:AE` use it. `W3-SAMP:MR@stmt:MR-b` points to MR's span 107-116, which contains (MR-b) at :111. Citation gaps are in E16.

**Item 4 detail (ledger offers in the code).**
- Tables, `v3_core.cpp:384`.
- Inherited models, `:427`. These are coordinates of 𝓒° (`T5_CAL/STATEMENT.md:25, 38`).
- Island evaluations through `eval` (`v3_engine.h:99`; calls at `:122, 153, 174, 186, 291`). `held` (`:104`) never updates the stores (`v3_ledger.h:112`).
- The final local search's scans. Its centre is not emitted (`v3_core.cpp:456`, `false`).
- The LS0 scans, **plus the emitted LS0 centre S̃₀** (`v3_core.cpp:476`, `true`; `v3_engine.h:382`). P2 leaves this one out (E15).
- The re-offer of the inherited HPM inside the `catch` block (`v3_core.cpp:502`) runs only on `numerical_failure`, which cannot happen under EX-A, and the run then has no output.
- There is no exact branch inside `cpp_final_run`. `start_mode` offers nothing to the ledger.
- The cache is new for each run (`:409`), so every model's first evaluation is fresh and is offered.

**Item 5 detail.**
- **E9: ACCEPT.** `v3_core.cpp:474` is the `stop`. `v3_score.h:230` is the `|S| > K` throw. `v3_engine.h:397` skips additions at size K. The swaps at `:401-406` delete one variable and add one. Both centres lie in Ω (E18).
- **E10: ACCEPT.** `MEAS_D.md:48`. The derivation is correct.
- **E11: ACCEPT.** `REPORT.md:203`.
- **E12: ACCEPT.** `REPORT.md:205` now names R3. See E19.
- **Mathlib rows: ACCEPT.** I found `Integrable.of_bound` (IntegrableOn.lean:171, `[IsFiniteMeasure μ]`), `lintegral_mono` (Lebesgue/Basic.lean:84) and `lintegral_iSup` (Lebesgue/Add.lean:36). The checkout is `/home/fb31/lean/packages/v4.35.0-rc2/mathlib` at 06535612. I cannot tell whether that is "the pinned checkout".
- **§4 Theorem 10 line (`MEAS_D.md:89`): ACCEPT.** It matches walk §1 ("Nothing in the reader's conclusion goes beyond (C-v)") and §6 (the TR route). The cited path is not on this branch (E17).
- **§5 κ_n bullet (`:96`): ACCEPT.** `git diff 4676af6 method-v3.1.1-listpip` touches only README, `v3_fit.R` and `v3_run.R`, and `cpp/` is unchanged from 4676af6 to HEAD.

**Item 6 detail.**
- **Scope.** The scope is still the potential objects only (`STATEMENT.md:190`, last sentence).
- **Converter.** It exits 0 and gives one record: W3-SAMP:MEAS-D, lines [190, 192], status_source `lemmas/MEAS_D.md:3`, `gates: correct:PENDING(reviews/R3_council_opus.md)`. All 10 `depends_on` items are present, with no spaces.
- **Bars.** `STATEMENT.md:188-192` has no `|` or `‖`. In the block, `|` appears only as a field separator.
- **Diff from HEAD.** §§0-3 differ from the repo copy only at `:36`.
- **New findings.** The one new F is F5.

## 2. Verdict lines

`(W1) the sets 𝓜_r: NOT PROVED AS WRITTEN, NO NEW PREMISE (F5)`
- Step 4 gives no argument for 𝓜_r.
- The reading it cites, Lemma B's Φ, leaves out the ledger and the rejected swap proposals (`L1_bridge.md:14-20`; `v3_engine.h:153, 174`).
- The only augmentation in the ticket adds the π₀ draws (`D_theorem.md:25-26`). `PC_completed.md:20` relies on it for 𝓜_r and has the same gap.

`(W2) the pair (data, streams 0–9): PROVED, NO NEW PREMISE`
- **The two facts.** SI given the data (fixed-data premise, `:64-66`, read conditionally on the data by `:29`) gives P(U∈A, V∈B | D) = P(U∈A | D)·P(V∈B | D). Independence of U from the data (`:35-36`) gives P(U∈A | D) = P(U∈A). So the identity displayed in P1 is correct.
- **To independence.** Integrate over {D ∈ C}. Rectangles {V∈B, D∈C} form a π-system that generates σ(D, V), so U ⊥ (D, V). Since 𝓒° = Ψ(D, seed, V) (CAL-b), U ⊥ (D, 𝓒°).
- **What the frozen slot needs.** U^{(9+r)} must be iid U[0,1) (H-U; its law is unchanged because it is independent of the data). It must be independent of (data, 𝓒°), which W2 gives. The integrand must be jointly Borel, which Steps 2-4 give. For bounded g, the display is the freezing lemma that Lemma F's proof invokes, which in Mathlib is `condExp_indep_eq`.
- **Caveat.** Lemma F's own integrand bound depends on the data (`L3_freezing.md` Boundedness), so Ẑ-type integrands go through the [0, ∞] form and Step 6 (E14).
- **Premise.** No new premise: this is the same fixed-data-premise reading that R2 accepted for IND-T.

`(W3) 0 < Z ≤ κ_n and integrability: PROVED, NO NEW PREMISE` (the wording needs E13)

`(Step 6): CORRECT`

`(F4) (C-v): COVERED`
- **Ẑ/Z.** E[|W_r − 1| | 𝓒] ≤ β (C-iii) and |Ẑ/Z − 1| ≤ ¼Σ_r|W_r − 1| give P(𝒜° ∩ {|Ẑ/Z − 1| > ε}) ≤ E[1_𝒜 min(1, 2δ̄/ε)].
- **log Ẑ.** Through |x − 1| ≥ 1 − e^{−u}.
- **NC_r.** P(W_r < η | 𝓒) ≤ β/(1 − η), per island.
- **O_P(r_n).** By the same Markov step.
- **PIP and MPM.** (C-iv)'s per-island bound g + β/2 depends on the data only. {MPM ≠ S₀} ⊆ {‖pip_primary − 1_{S₀}‖_∞ ≥ ½} is correct: a missed j ∈ S₀ has pip ≤ ½, and a false j has pip > ½.
- **Ŝ.** It comes from P(S₀ ∉ 𝓜_r | 𝓒) ≤ δ̄ at one fixed r, (LT-d) with PC (𝓜 ⊇ 𝓜_r; the event {δ ≥ ½} depends on the data only), and GW-iv.

`(F4) (TR-d): COVERED`
- (TR-b)'s per-island bound g + e_L is σ(data, 𝓒)-measurable. 1_𝒜 g ≤ 21·1_𝒜 o₁ → 0, and 1_𝒜 e_L ≤ e^{−L/M} → 0 under P-OVL∞.
- MPM uses the same inclusion.
- Ŝ comes from (TR-c)'s P(S₀ ∉ 𝓜_r | 𝓒) ≤ δ + e_L, (LT-d) with PC, and GW-iv.

`(Text P2): MISSING OFFER — the LS0 centre S̃₀, emitted at cpp/v3_core.cpp:476 (emit_centre = true; cpp/v3_engine.h:382); otherwise complete and correct (E15)`

## 3. Findings

**F5 (W1 has no proof step). `MEAS_D.md:37`.**
- **Problem.** The statement now names the sets 𝓜_r (W1), but Step 4 never shows they are Borel. The record that Lemma B makes Borel (B-d) leaves out the cache and ledger contents and keeps only each particle's path. Rejected uniform-swap and neighbour-swap proposals are scored through `eval` and then may be dropped (`cpp/v3_engine.h:152-158, 172-178`). The ticket's only augmentation, `D_theorem.md:25-26` (C1 Opus #1), adds the π₀ draws only.
- **Exact correction.** Append to the Islands bullet:
  > "The set 𝓜_r of models island r passes to `eval` (`cpp/v3_engine.h:122, 153, 174, 186, 291`: initial draws, Gibbs flips, both swap proposals and independence proposals, accepted or not) is not a coordinate of Lemma B's record (`W1-N1/lemmas/L1_bridge.md:14-20`). Each such model is nevertheless computed by the same control flow from (grid values, data constants, u₁, …, u_κ) (B-0), (B-d), as for the π₀ draws in `lemmas/D_theorem.md:25-26`. So, on each cell, 𝓜_r is a Borel map into the finite set 2^Ω, the number of evaluations being bounded by a function of (p, T, N_e, L)."
- **Also.** Add "𝓜_r," to the list "So the island records, …" at `:40`.

**E13 (W3 wording). `STATEMENT.md:190`, `MEAS_D.md:24`, `REPORT.md:203`.**
- **Problem.** The integrability of 1_{𝒜°}Ẑ needs Step 5, that is, the joint law of §0.
- **Correction.** Replace "integrable under every law of the data" with "integrable under the joint law of §0, for every law of the data". In the REGISTRY, use "integrable under the joint law (H-U/SI), for every law of the data".

**E14 (Step 5, frozen slot). `MEAS_D.md:42, 46`.**
- After "(`:35-36`)." add: "Integrating over {data ∈ C} and applying the π-λ theorem to the rectangles gives independence from the pair."
- After "by monotone convergence" add: "; a signed integrand dominated by B_h Ẑ_r is split into positive and negative parts, each finite by Step 6".

**E15 (P2). `MEAS_D.md:39`.**
- Replace "and the two searches' scans" with "the two searches' scans and LS0's emitted centre S̃₀ (`cpp/v3_core.cpp:476`; a function of the data, Step 2)".
- Optionally add "the inherited-model `stop` (`cpp/v3_core.cpp:425`) is a further branch on a Borel predicate".

**E16 (Step 6 citations). `MEAS_D.md:50`.**
- After "depending on n only (" add `cpp/v3_score.h:14` (a₀ = b₀ = 0.01).
- After "The prior weights sum to 1 over Ω" add "(`cpp/v3_score.h:61-70`; `W3-T03ACC/STATEMENT.md:27`)".

**E17 (walk path). `MEAS_D.md:89`.**
- `walks/T9_Thm10.md` is not on theory/PRE-LEAN at d432ca4f. Write "`walks/T9_Thm10.md` (theory/PRE-LEAN-walkB, dc2e7174)". The content checks out.

**E18 (E9 sentence). `MEAS_D.md:38`.**
- After "swaps keep the size" add ", and both centres lie in Ω (the running best by CC5, S̃₀ by TDP)".

**E19 (records). `MEAS_D.md:3`, `REPORT.md:205`.**
- The status line still names R1 and MANIFEST_MEASD. Update it to R3 and MANIFEST_MEASD3.
- `reviews/R3_council_opus.md` will resolve only if this record (saved at `PRE_LEAN_PASS/MEAS-D/R3_council_opus.md`) is copied into `W3-SAMP/reviews/` when it is recorded.

**E20 (optional edge). `REPORT.md:204`.**
- P2 uses `W3-SAMP:PC` (iii) as the source of the ledger's offers. Consider adding `W3-SAMP:PC@stmt:PC-iii`.

## 4. Gates

- **G1 correctness: FAIL.** F5: the clause W1 has no proof step. W2, W3, Step 6, F4 and E9-E12 are correct.
- **G3 faithfulness and scope: PASS.** The scope is potential-only, and no premise is added. E13 is wording.
- **G4 statuses and pins: PASS.** All pins were checked: `v3_core.cpp:474`, `v3_score.h:14/59/223/230/237`, `v3_engine.h:397`, `S_one_step.md:7-15`, T03ACC:29-30. Both new edges are in claims.tsv in the existing form.
- **G5 registration form: PASS.**

## 5. Score

**8.7.** There is one F (F5), which a single added sentence fixes. There is no C or S.

## 6. Claim table

| id | decision |
|---|---|
| W3-SAMP:MEAS-D | ACCEPT |

COUNCIL-VERDICT round=R3 manifest=a08a238a2e84c980ce1b80cd8da237af74d855012f290ff32b99d84d550800f4 seat=opus score=8.7 gates=FAIL
