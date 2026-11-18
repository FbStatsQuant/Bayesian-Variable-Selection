## A. MEAS-D: coverage, and the exact widening

| Reviewer point | Covered after R1? | What is added |
|---|---|---|
| Astra T9-1, Sol T9-2 (first half): measurability, as the data vary, of the potential calibration record, its success flag, the island records and the evaluated-model sets | Yes (Steps 1–4). The statement did not name the evaluated-model sets. | Statement: name them (W1). |
| Same points: each final stream must be independent of the **pair** (data, streams 0–9) | Used in Step 5 but not derived | Statement: say it (W2). Proof: derive it (P1). |
| Astra T9-3, Sol T9-2 (second half): measurable completion flag and reported model; ledger offers from outside the islands; the clock | Yes for the potential run (𝒪°, ledger, Ŝ of P°) | Proof: name the ledger's offers (P2). Actual runs: the sentence in §B.1. |
| Astra T9-4, Sol T9-3: joint integrability of 1_{𝒜°}Z | **No** | Statement: W3. Proof: new Step 6 (P3). |

**Exact replacements, keyed to MEASD2 and MEASD3:** `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/cards/MEAS-D_R3_texts.md`. They are consistent with Opus R2's F4 and E9–E12: no new text names a route for (C-v) or (TR-d), and none cites `v3_core.cpp:475`. In MEASD3 (43e1b07f) the coordinator has already applied F4, E9–E12 and P1, P2 below; **W1, W2, W3 and P3 are still to apply.**

**Widened statement** (`W3-SAMP/STATEMENT.md:190`; replaces the R1-fixed sentence; the three additions are W1, W2, W3):

> **(MEAS-D) Joint measurability of the potential records.** Fix n, p_raw and the options, and assume EX-A. On the Borel set of valid inputs, the following objects of the potential fit P° (`W3-AUDIT-A:GW`) are Borel functions of (X^r, y^r, U^{(0)}, …, U^{(13)}), the seed entering only as a label: the calibration record 𝓒° and the event 𝒜°; the records of the four final islands, **with the sets 𝓜_r of models they evaluate** [W1]; the final local-search and LS0 archives and the final-run ledger, hence 𝓜, 𝒯, Ŝ and every statistical field of P°'s output; the output event 𝒪°; and Z, π, π₀. **Moreover 0 < Z ≤ κ_n for every valid data set, with κ_n depending on n only, so 1_{𝒜°}Z and 1_{𝒜°}Ẑ are integrable under every law of the data** [W3]. Consequently, under the joint law of §0 (H-U/SI, **:29 and** :35-36, **which together make each final stream independent of the pair (data, streams 0–9)** [W2]), for each island r every identity or bound of §2 about island r stated "given 𝓒 on 𝒜" holds, for the potential pair (𝒜°, 𝓒°), conditionally on (data, 𝓒°); so do the statements obtained from these by finite sums, monotone comparison and union bounds over r, which is all that the joint-law clauses of §2 use; and where a clause assumes IND-T, the same holds for functions of the four final streams jointly. Nothing is claimed about the actual 𝒜, 𝒪 or the guard, which enter only through the pathwise inclusions of `W3-AUDIT-A:GW` (GW-iii), (GW-iv). (Proof: `lemmas/MEAS_D.md`.)

**Proof additions** (`lemmas/MEAS_D.md`):

- **P1** (Step 5, after its first sentence): "Independence from the pair follows from two stated facts: SI holds for each fixed data set, that is, given the data U^{(9+r)} is independent of U^{(0:9)} (`STATEMENT.md:29`); and U^{(9+r)} is independent of the data (`:35-36`). Hence P(U^{(9+r)} ∈ A, U^{(0:9)} ∈ B | data) = P(U^{(9+r)} ∈ A)·P(U^{(0:9)} ∈ B | data)."
- **P2** (Step 4, Ledger bullet, append; already in MEASD3 without the parenthesis "(the sets 𝓜_r)", which W1 adds): "Its offers are the islands' evaluations (the sets 𝓜_r), the block-table models (functions of the data, Step 2), the models inherited from calibration (coordinates of 𝓒°) and the two searches' scans (`W3-SAMP:PC` (iii))."
- **P3** (new step, before "What the proof does not use"; the ∎ moves here):

> **Step 6 (Z is bounded; integrability).** The coded marginal likelihood is m(S) = C_n·D_S^{−1/2}(2b₀ + Q_S)^{−ν}, with C_n = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) depending on n only (`cpp/v3_score.h:59, 223`; `W3-T03ACC/STATEMENT.md:29-30`). Here D_S = det((n+1)G_S + I)/det(G_S + I) = Π_i((n+1)λ_i + 1)/(λ_i + 1) ≥ 1, the λ_i ≥ 0 being the eigenvalues of G_S; and Q_S ≥ 0, because Q_S is the minimum of a sum of two nonnegative quadratic forms (Lemma V, `W3-PSHARP/lemmas/S_one_step.md:7-15`). Hence m(S) ≤ κ_n := C_n(2b₀)^{−ν} for every S and every valid data set. The prior weights sum to 1 over Ω, so 0 < Z ≤ κ_n. Thus 1_{𝒜°}Z is bounded, hence integrable under every law of the data. For the estimates: Ẑ_r ≥ 0 is Borel (Step 4), and Step 5 in its [0, ∞] form with (MR-b) at h ≡ 1 gives E[1_{𝒜°}Ẑ_r | data, 𝓒°] = 1_{𝒜°}Z; so E[1_{𝒜°}Ẑ_r] = E[1_{𝒜°}Z] ≤ κ_n. Each 1_{𝒜°}Ẑ_r, and their mean 1_{𝒜°}Ẑ, is therefore integrable, and the real-valued conditional expectations of §2 and of PoolZ are defined. ∎

Standard facts for Step 6 (Mathlib names verified in the pinned checkout): a bounded measurable function is integrable on a probability space (`Integrable.of_bound`); monotonicity and monotone convergence of the lower integral (`lintegral_mono`, `lintegral_iSup`).

**Registry block:** append to the conclusion "; 0 < Z <= kappa_n with kappa_n depending on n only, so 1_A0 Z and 1_A0 Zhat are integrable under every law of the data"; add to depends_on `W3-SAMP:MR@stmt:MR-b ; W3-PSHARP:S@proof:Lemma-V`.

**PoolZ then needs only a citation** (`W3-READER/STATEMENT.md`, proof, before "taking expectations of"; inside its span, CITATION-ONLY): "(the records are jointly measurable and both sides are finite: `W3-SAMP:MEAS-D`, `W3-SAMP/STATEMENT.md` §4);". Recorder: add `W3-SAMP:MEAS-D` to PoolZ's depends_on.

**Is the integrability proof short and standard? Yes.** It is a data-uniform bound: three inequalities and one application of monotone convergence. Nothing goes to HQ.

**Opus R2 (8.7, gates FAIL; claim ACCEPT):** as author I accept F4 and E9–E12 as the seat wrote them. In particular the routes for (C-v) and (TR-d) are those of F4: (C-iii)'s per-island bound for the Ẑ, log Ẑ and NC_r clauses, (C-iv)'s and (TR-b)'s per-island bounds for the PIP and MPM clauses, with no independence across islands; and the LS0 `stop` is at `v3_core.cpp:474`, with the scorer's size throw at `v3_score.h:230` added to the exit list. R2 also confirms that IND-T "with the data adjoined" is derived, not added. One R3 round takes W1–W3 and P3 on top of what MEASD3 already holds.

