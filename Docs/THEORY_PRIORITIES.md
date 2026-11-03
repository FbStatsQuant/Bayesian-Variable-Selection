# Theory priorities: the frozen paper targets

**Frozen 2026-10-28** by HQ with Felipe, after two independent consultant reviews of HQ's proposal (Fable 5.1 and Astra), both ENDORSE WITH CHANGES. This page is the strategic view: what we will pursue, why, in what order, and through which gates. Written 2026-11-02 for the GitHub handoff. §5 was updated 2026-11-03 with the final empirical evidence. The proof statuses in this repo are unchanged since 2026-11-02. Any results of the theory campaign running elsewhere (D77) are not reflected here.

- **Authoritative record:** `Docs/Theory/PAPER_SELECTION_20261028/FROZEN_LIST.md`.
- **The full inventory** of all 39 items (T01–T36 plus the new T37–T39), with per-theorem one-pagers: `Docs/THEORY.md` and `Docs/Theory/one_pagers/`.
- **Sources** used here, all under `Docs/Theory/PAPER_SELECTION_20261028/`: `PROPOSAL.md`, `FABLE_REVIEW.md`, `ASTRA_REVIEW.md`, `new_conjectures/T37–T39`. Also `Docs/Theory/proofs/LOCKED_PROOFS.md` and `Docs/Theory/INVENTORY_20261028/THEORY_INVENTORY.md`.

**Felipe's premise for the selection.** Every target is assumed provable after restating assumptions, after minor methodology tweaks, or with budget sequences indexed by n. The campaign's job is to prove each target, restate it, or establish that it is false.

**Status words used below (never upgraded):**

| Status | Meaning |
|---|---|
| PROVED-LOCKED | Reviewed, hash-frozen in `LOCKED_PROOFS.md`, **not adopted**. Adoption is Felipe's decision, and he has not taken it yet. |
| CONDITIONAL | Proved, but on hypotheses that are still open. |
| PARTLY PROVED | Only the named parts are locked. |
| CONJECTURE | Not proved. |
| NEW CONJECTURE | Written 2026-10-28; not proved; restatement still expected. |

---

## 1. The story and the selected set

**Story.** What SMC-BVS reports is consistent because the truth gets **scored**, not because the sampler converges. The reported HPM is the best model ever scored. So "right answer" = (a) the posterior favours the truth, and (b) the truth is scored at least once, and (c) the run produces output.

### JRSS-B main text (8 results)

| Paper # | Target(s) | What it establishes | Status today |
|---|---|---|---|
| Thm 1 | **T03** (lemmas T01, T02) | The posterior concentrates on the truth | T01, T02, T03 PROVED-LOCKED (wave 3; external review queued); restatement required |
| Prop 1 | **T07** (+ one sentence of T06(i)) | The HPM is the Bayes rule for exact recovery; a size-only prior cannot fix a same-size swap | PROVED-LOCKED (wave 3; external review queued) |
| Thm 2 | **T22 + T27** | The start: provable mass on or near the truth (favourable regime), and a masking lower bound (masked regime) | PARTLY PROVED: T22(i)(ii)(iv) locked; T22(iii) and T27(i) locked but CONDITIONAL; T22(v) and T27's other clauses not proved |
| Thm 3 | **T37** (NEW); T24 as the alternative | Repair: from any near-truth centre, the production local search reaches and scores the truth; finite-n bound | T37 NEW CONJECTURE; T24 CONJECTURE |
| Thm 4 | **T21** | P(wrong report) ≤ P(no output) + 2E[posterior mass off the truth] + P(truth never scored) | PROVED-LOCKED, CONDITIONAL (route (e) rests on the open H24; exposure and occurrence conditions open) |
| Thm 5 | **T38** (NEW, main) | Consistency of the reported HPM in both regimes, *including delivery* of a near-truth centre, plus a polynomial-cost corollary | NEW CONJECTURE |
| Thm 6 | **T26 (i)–(ii)** | Consistency of the evidence and the PIPs, favourable regime only | CONJECTURE |
| Prop 2 | **T12** (+ T31(i)) | Unbiased evidence; islandwise E[Ẑ_r·PIP̂_rj] = Z·PIP_j; Markov 95% lower bound | T12 PROVED-LOCKED; T31(i) PROVED-LOCKED (wave 1, full review chain); restatement required |

- **Biometrika cut (5).** Thm 1 (T03), Thm 2 (T22, with T27 as a remark), Thm 3 (T37 or T24), Thm 4 (T21), Thm 5 (T38). T07, T26 and T12 become remarks.
- **Contingency.** **T39** (Astra's C37): independent scoring-only repair tracks with an explicit budget. Use it only if T38(b) cannot be proved for the original method. It is a method extension and would need new validation runs.
- **Supplement.** Lemmas T01, T02, T09, T10, T11, T13, T14, T15, T20, T23, T32. Remarks T04, T05 (a disclosed negative: the g-prior + BB(1,p) HPM loses a √log n factor to the oracle under orthogonal design), T06, T33, T34. The other eleven conjectures are dropped from the paper (see `FROZEN_LIST.md`).
- **Rejected as targets** (both reviewers): comparative superiority over SuSiE or SSL; PIP calibration; robustness to misspecification; minimax optimality.

### Common setting for every target (restatement notes)
- A triangular array with s₀ **fixed** (14 in our study), p_n ≤ n^A and B ≤ 16. The generator's growing rule s₀ = ⌊√n⌋ is **not** covered.
- Keep the *potential uninterrupted run* separate from the *output-available* event, and never condition on observed completion. This is the `resource_limit` caveat: 6 of 2,400 fits stopped.
- **Prove compatible premises jointly.** One statistical family must satisfy every premise used in T38, not each conditional statement separately (Astra).

---

## 2. The results, one by one

### Thm 1: T03 selection consistency (with T01 contrast reduction, T02 dimension control)
- **Statement.** Under G, R, SE and beta-min (BM-C or BM-∞), the posterior mass outside S₀ is O_P(√(log n / n)). PIPs are within that distance of the 0/1 truth, and the HPM and MPM of the *true posterior* equal S₀ with probability → 1. Without beta-min, the large signals still get PIPs → 1.
  - T01 makes the standardised-data posterior an exact contrast-model posterior.
  - T02 makes large models and strict supersets of S₀ negligible.
- **Intuition.** With enough data, the marginal likelihood penalises both missing signal and spurious extras, and the BB(1,p) prior penalises extras further.
- **Why it matters.** It is the statistical half of the story: the target is right. Without it, scoring the truth would not help.
- **Status.** All three PROVED-LOCKED (wave 3: Opus lead + 2 Opus xhigh reviewers; **external review queued**); not adopted.
- **Key premises.** G, R, SE, BM-C or BM-∞, s₀ fixed, H-T02 (closed by T02(i)).
- **Crux / open obligation.** The restatement:
  - replace T02(i)'s 2^−m size tail by the exact BB(1,p) tail, which cuts m_n from about 200 to s₀ + O(s₀ log n / log p);
  - restrict SE to the comparison unions actually used;
  - replace M* by BM-∞ or an unnamed constant.
- **Risk.** At n = 200, SE is *impossible* (rank ≤ 199 against subsets of 215–229 columns), and beta-min fails by about 100× in squared signal. The theorem explains the mechanism, not the n = 200 numbers. Restating does not yield a useful finite-n error rate. The risk to *validity* is low; the risk to *relevance* at n = 200 is accepted and must be disclosed.
- **Fallback.** Present it as asymptotic, stated informally in the main text.

### Prop 1: T07 size-prior ceiling and Bayes decisions (+ T06(i) ties)
- **Statement.** For the true posterior:
  - the HPM minimises 0-1 loss (exact recovery), and the MPM minimises Hamming loss;
  - PIP error bounds the excess MPM risk;
  - no size-only prior can repair a within-size ranking error.
  - T06(i): the score functions of two supports agree for every standardised response iff X_S X_Sᵀ = X_S′ X_S′ᵀ. Equal column spans alone do not suffice with this ridge prior; under G, observed exact ties almost surely have equal outer products. Such ties are a ceiling for every method.
- **Why it matters.** It justifies reporting the HPM, and it names the within-size *look-alike swap* as the only error that re-tuning BB(1,p) cannot fix.
- **Status.** PROVED-LOCKED (wave 3; external review queued); not adopted.
- **Risk.** Low. Astra judged its standalone novelty modest and would demote it to a remark; that is what the Biometrika cut does.

### Thm 2: T22 + T27, the start (upper and lower bounds)
- **Statement.**
  - **T22(i)(ii)(iv)**, deterministic:
    - the composite block start puts mass ≥ (1−q)^{s+1}/(1+e)^s on a reference model;
    - the odds from a reference to the truth are exact;
    - the tempering bridge never loses mass on S₀ below the smaller endpoint mass.
  - **T22(iii)**, favourable regime: under EXP′, VIS, NL_η and NL_avg(κ), 1 − π₀(S₀) = O_P(2^B √(log n) n^{−κ}).
  - **T27(i)**, masked regime: for a chain of c masked feasible additions satisfying H2/H3, π₀(S₀) = p^{−c} n^{−c/2} e^{O_P(1)}. Whether iid discovery fails depends on Q_f·π₀(S₀). The locked part proves the mass law, not a discovery failure; enough draws can still find the truth.
- **Intuition.** The start concentrates on the truth when the blocks see it. When true variables cancel, the start gives the truth only polynomially vanishing mass, so the iid draws alone may not find it within the budget. That is the motivation for the sampler.
- **Why it matters.** It is the motivation for the SMC machinery, in two sentences, and an input to T38's delivery step.
- **Status.**
  - T22(i)(ii)(iv): PROVED-LOCKED (wave 1, full chain).
  - T22(iii) and T27(i): PROVED-LOCKED, CONDITIONAL (wave 2):
    - T22(iii) rests on EXP′, VIS, NL_η, NL_avg (open);
    - T27(i) rests on H2, H3 (open statistical inputs).
  - Never combine T22(iii) and T27(i) on one sequence: they describe different regimes.
- **Open obligation.**
  - Prove EXP, visibility and leakage for the actual X-dependent partition.
  - Replace T27's assumed ratio law by a bounded-leakage condition along the chain: a two-sided law with a controlled multiplier.
  - For T38(b), use T22's deterministic reference bound, where the reference may differ from S₀.
- **Risk.** Medium. The T22(iii) rate is vacuous at n = 200 (≥ 2,667). Fable warns that a restricted T22 regime with uncheckable hypotheses must not eat the repair theorem's time.
- **Fallback.** Keep T22's deterministic clauses plus T27 as a route-specific remark. T27 bounds iid start draws only, not the hybrid sampler.

### Thm 3: T37 truth dominance and greedy repair (primary), T24 terminal repair (alternative)
- **Statement (T37).**
  - **(i), deterministic.** Assume truth dominance TD(d, 0) with strict inequalities, and a move budget ℓ ≥ |S Δ S₀|. Then the production local search moves from any centre S in the near-truth region 𝓡_d (subsets of S₀ plus at most d extras) monotonically to S₀ in exactly |S Δ S₀| moves, never leaving 𝓡_d, and scores and certifies S₀.
  - **(ii), finite n.** Under G and for fixed X, P₀(TD(d, m) fails) is bounded by a sum of explicit one- or two-dimensional non-central Gaussian events.
  - **(iii), n-indexed.** Assume s₀ and d are fixed, ℓ_n = ⌈log₂(n+p+1)⌉ ≥ s₀ + d eventually, and G, R, SE and BM-∞ hold. Then the bound in (ii) → 0.
- **Intuition.** Adding a missing true variable captures its full signal, while its look-alike captures only the r² share. Once S₀ ⊆ S, extras only pay the size penalty. So the greedy order is "truths in, then extras out". The margin (n−1)θ²(1−r²)/(2σ²) is also the proposed mechanism behind the correlated-design advantage.
- **Why it matters.** It is the paper's one genuinely finite-n statement, and the repair step T38 needs. It replaces the open GAIN_d, LK_d and EXIT_d codes.
- **Why T24 was singled out first, and why T37 now leads.**
  - The 2026-10-28 briefing ranked T24 the "top open target" and "the single result that would lift the paper's tier". It would replace T21's assumed event H24 with a bound, (1−a)^H + Hη, on not scoring the truth.
  - Fable then showed T24's repair constant 1/(s₀+d+B+2)! = 1/31! at s₀ = 14 is useless, and that LK_d fails in correlated designs.
  - Hence T37 became primary, and **whichever closes first becomes Thm 3**.
- **Status.** T37 NEW CONJECTURE; T24 CONJECTURE.
- **Crux.**
  - The 2^{s₀} union bound in (ii) is loose at s₀ = 14; a bound along the actual greedy path is the research part.
  - ℓ = 10 < s₀ + d = 15 at n = 200, so use the extra-scan rule or a closer centre.
  - T37 does not deliver an eligible centre; that is T38's job.
- **Risk.** **High on the literal wording; see §5.** The final evidence shows the literal TD premise fails in every audited case at both low and high p. The "toward S₀" form has no counterexample at p ≤ 30 as a sufficient condition.
- **Fallback.**
  - Restate TD ("toward S₀" variant, or a path-wise condition).
  - Or T24, restated:
    - evaluate LK only at states containing S₀;
    - charge look-alike additions to d;
    - prove progress of one correct step per round instead of a full-ordering constant.
  - Or, failing both, T39.

### Thm 4: T21 HPM composition
- **Statement.** P(U or Ŝ ≠ S₀) ≤ P(U) + 2E₀δ₁ + P(truth not scored). Routes (a)–(f) bound the last term: iid final draws, Gibbs, swaps, tables and scans, terminal repair, exact enumeration.
- **Why it matters.** It is the bridge between the statistical and computational halves, and the core of the story.
- **Status.** PROVED-LOCKED (wave 2: Astra lead, Sol ×2, Astra xhigh, Claude audit); not adopted. **CONDITIONAL:**
  - route (e) needs H24 (T24's inputs, unproved);
  - also H03, H10, and the occurrence and exposure conditions;
  - "scored" includes rejected proposals.
- **Open obligation.** Wire Thm 3 into it. Fable proposes (C1) with routes (a), (d) and (e′ = T37). How T37 enters T21's routes is not yet written, so record it as an obligation, not a fact. Report P(U) empirically.
- **Risk.** Low for the inequality; the content lives in its inputs.

### Thm 5: T38 two-regime consistency of the reported HPM (main theorem)
- **Statement.** P(Ŝ = S₀) → 1 − limsup P(U). The discovery term vanishes:
  - **(a)** in the favourable regime, by T22(iii) + T11(iii) (iid final draws score S₀);
  - **(b)** in the masked regime: the start puts mass π₀(𝓡_d) ≥ b_n near the truth (T22(i)), and then
    - **(b1)** T37 repairs from an eligible local-search centre, or
    - **(b2)** T24 repairs at the terminal rounds;
  - **(c)** cost corollary: polynomially many score evaluations (via T32).
- **Why it matters.** It explains the method's *design* (start, bridge, moves, local search), not just its output. The masked regime is where SMC-BVS beats the coordinate-wise competitors at c = 0.5. It replaces T26(iii), which needed no sampler at all.
- **Status.** NEW CONJECTURE. Not claimed:
  - masked-regime evidence or PIP accuracy;
  - results for completion-selected fits;
  - comparative superiority.
- **Crux.**
  - **Eligibility:** show that the best-scored model, or the start mode with tweak **LS0** (local search also from the start mode; deterministic, about ℓ·p extra scores, addable after the fact), lands in 𝓡_d.
  - **Compatibility** of T22(i) with T27 on one family.
  - ℓ_n < s₀ + d at n = 200.
- **Risk.** High; this is the hole (§3).
- **Fallback.** T39.

### Thm 6: T26 (i)–(ii) evidence and PIP consistency (favourable regime)
- **Statement.** Under the favourable-start premises, Ẑ/Z → 1 and the PIPs → the 0/1 truth, at the actual n-indexed budgets.
- **Why it matters.** The method reports Ẑ and PIPs, and this is their consistency statement.
- **Status.** CONJECTURE. Demoted to a favourable-start result by both reviewers.
- **Premises.**
  - (T_n+1)Δ_n → 0 and (L_n+4)ρ*_n → 0;
  - EXP named as a hypothesis;
  - SE (impossible at n = 200);
  - remove the secondary PIP;
  - no masked-regime claims.
- **Risk.** Medium-high: the longest hypothesis list in the pool.
- **Fallback.** A remark; Regime L supplies the empirical PIP and Ẑ accuracy.

### Prop 2: T12 frozen-run identities (+ T31(i))
- **Statement.** For the frozen calibrated run, E[Ẑ] = Z, and the *islandwise* product is unbiased: E[Ẑ_r·PIP̂_rj] = Z·PIP_j. This is **not** an identity for pooled Ẑ × pooled PIP, and the normalised PIP is not claimed unbiased. T31(i): 0.05·Ẑ is a 95% lower bound on Z.
- **Why it matters.** It makes Ẑ meaningful, and the reported 95% bound valid.
- **Status.** Both PROVED-LOCKED (wave 1, full review chain incl. Fable + Astra campaign review); not adopted.
- **Open obligation (bookkeeping).**
  - Freeze everything before the final randomness.
  - Use the islandwise wording.
  - Drop the secondary-PIP clause.
  - State the potential-uninterrupted-run / output-available split.
  - Validate floating point separately.
- **Risk.** Low.

### Contingency: T39 independent repair tracks
- **Statement.** M scoring-only tracks, each from an exact π₀ draw, run h rounds at φ = 1. Then P(S₀ never scored) ≤ (1 − b_n s_n)^M, with explicit h and M, and the cost is polynomial if b_n and a_n decay polynomially.
- **Status.** NEW CONJECTURE (contingency).
- **Risk.**
  - It is a **method change**: the 2,400 fits did not run it, so it needs validation runs under the investment rule.
  - The research content lies in the inputs b_n and a_n.
  - If the tracks explain all the gain, the paper must say what tempering contributes.

---

## 3. The hole, and how it is filled

Both consultants independently found the same hole: **a guarantee that a near-truth particle is *delivered* and then *repaired* within an explicit, finite budget.** T24 and T26 alone do not give it. T24 repairs an eligible particle but does not deliver one; T26 needs start concentration, which is exactly the regime where the sampler is unnecessary.

| Step | Supplied by | Status |
|---|---|---|
| Delivery: start mass near the truth, b_n | T22(i) with a reference S° ∈ 𝓡_d (S° ≠ S₀ allowed) | Deterministic bound locked; its statistical inputs are open |
| Eligibility: some local-search centre in 𝓡_d | T38(b1), or the LS0 tweak | Open (the crux) |
| Repair: centre → S₀ scored | T37 (primary) / T24 (alternative) | Open |
| Report: scored truth + π(S₀) > ½ ⇒ Ŝ = S₀ | T21 + T03 | Locked, conditional |
| Fallback if (b) fails for the original method | T39 (method extension) | Open; needs new runs |

---

## 4. Pursuit order and gates

**Order** (FROZEN_LIST, both reviewers agreeing):
1. **T37**: cheap and finite-n; feeds Thm 3 and T38.
2. **T02(i) tail sharpening and the T03 restatement.**
3. **T22(i)/(iii) and T27 on one compatible family.** Start with EXP in the block-orthogonal benchmark.
4. **T38**: composition plus eligibility.
5. **T24 only if T37 fails; T39 only if T38(b) fails.**
6. **Bookkeeping restatements:** T12, T21, T26(i)–(ii), T07, the T05 remark, plus the potential-uninterrupted-run / output-available split for T11(iii), T12, T14, T15, T23, T25, T31 (and T34).

**Gates** (campaign plan phases P4–P8; see `Docs/PLAN.md`):

| Phase | Name | What happens |
|---|---|---|
| P4 | Let the data talk | EVIDENCE_H and EVIDENCE_L say, per target, support / contradict / silent |
| P5 | Theory layer 1 | The bookkeeping restatements above. Opus-led, Sol review |
| P6 | Believed versions | **Fable 5.1 leads statement refinement** of each hard target (T37, T22+T27, T38, T26(i)–(ii); T24 and T39 as fallbacks). It produces a **confidence card** per target: the refined statement, the data evidence, exact small-case tests at p ≤ 30, the proof skeleton with its crux isolated, Astra's attack and Sol's review, the risk, and whether a method change is needed |
| G3 | Felipe's gate | **Felipe's green light per card. No proof swarm before it** |
| — | If a card fails | A method-change proposal under the **investment rule**: change the method and rerun *only if* (1) with the change, all or most of the key results are provable, **and** (2) a pilot gives strong evidence that the method still performs well. One redeploy carries all changes together. No large runs on gambles |
| P7 | Proof swarm | Opus-managed, worker-heavy, Sol and Astra reviews, Fable only on cruxes |
| P8 | Lean, last | Every accepted proof is formalised. The exact finite results (T07, T21, T11(iii), T12, T37(i)) first |

Adoption of the 21 locked entries is a separate, still unanswered decision for Felipe (`Docs/HQ/DECISIONS.md`, Pending).

---

## 5. What the data says (final, 2026-11-03)

**Sources.** The accepted final reports:
- `Results/2026-10-28_New_Campaign/H2_20261102/EVIDENCE_H.md` (p ≫ n: 2,400 fits, p ∈ {500, 1000});
- `Results/2026-10-28_New_Campaign/L_20261102/EVIDENCE_L.md` (p ∈ {20, 30}: 2,400 cases + 12,000 repeat fits, exact posterior by enumeration).

Both have Terra tie-outs and Sol acceptance (D78, D87, D94). The extraction plan is `Docs/Campaigns/2026-10-28_New_Campaign/THEORY_EXTRACTION_STRATEGY.md`.

**How to read the verdicts.** They describe what one n = 200 design can show:
- **support** means consistent with the statement, not a proof of it;
- a failed finite-n *premise* of a conditional theorem is **not** a contradiction of the implication;
- **silent** means the data cannot speak to it here.

| Target | p ≫ n (EVIDENCE_H) | p ≤ 30 (EVIDENCE_L) |
|---|---|---|
| **T22 + T27** (Thm 2), start mass | **Masking qualitatively consistent with T27.** The iid start intensity Q_f·π₀(S₀) is below 1 in 2,393/2,394 completed fits. The cell medians of π₀(S₀) are 10^−12.4 to 10^−25.6 and fall by 2–4 orders of magnitude from p = 500 to 1000. Pooled near-truth medians: π₀(𝓡₀) = 0.20, π₀(𝓡₂) = 0.81 (lower in S4). T27's law and T22(iii)'s hypotheses: **silent** | **Support:** a tiny start mass on the truth does not stop the SMC from delivering the exact HPM. Rates: **silent** |
| **T37** (Thm 3), truth dominance and repair | The finite-n premise TD(0, 0) **fails in all 196 audited cases** (literal and "toward" coincide at d = 0). Truth-for-truth swaps explain the violations in the cases diagnosed. The final local search never made an improving move. T37(i), as an implication: **not contradicted**; (ii)–(iii): **silent** | The literal premise fails in all 2,400 cases; that limits **applicability** and is not a refutation. The **"toward S₀" wording has no counterexample as a sufficient condition** (1,511 cases at d = 1), but it is not necessary (705 hits violate it) |
| **T38** (Thm 5), delivery + consistency + cost | **First discovery of the truth happens in the pilot SMC, by Gibbs flips and swaps, in every completed hit.** This motivates a pilot-discovery / T24-type route. T38(b2)'s formal premises: **silent**. Cost is descriptively consistent with polynomial growth (two values of p) | **Support delivery:** SMC HPM = exact HPM in 2,400/2,400 primary and 12,000/12,000 repeat fits. Asymptotic consistency and the cost rate: **silent** |
| **T21** (Thm 4), decomposition | **Consistent.** 6 no-output fits + 565 completed misses, each with a scored competitor above the truth; 0 detected search misses. The discovery term is not identified at p ≫ n (no per-model trace), so it lies between 0 and 565 | **Support, but loose:** every HPM truth-recovery error is a posterior error, the search contributes none, and the mass-off-truth term dominates |
| **Resource stop vs complete run** | 2,394/2,400 completed. The 6 guard stops (S5) could change at most 6 recoveries. The P5 retry was not run (D62) | **Silent:** all 14,400 units completed |
| **T03 / T07** (Thm 1, Prop 1) | T03: **silent** (asymptotic); concentration is visibly incomplete at c = 0.5. **T07: support.** 207 of 565 completed misses (37%) are same-size wrong supports, which no size-only prior can repair | **Support both mechanisms:** supersets dominate at strong signal, same-size swaps at weak signal |
| **T26(i)–(ii), T12** (Thm 6, Prop 2) | **Silent** by design (D22). The RB and plain MPMs agree in 2,391/2,394 fits | **Support T12:** the mean relative error of Ẑ is −0.00011 (SE 0.00010) over 14,400 fits. **Support T26(i)–(ii) as finite-setting accuracy:** log Ẑ RMSE 0.012; mean per-fit max PIP error 0.0005 (RB) / 0.0020 (plain) |

**Implications for P6** (what the statement refinement must absorb; these are not new decisions):
1. **T37 must be restated before any proof effort.** The literal TD premise never holds in this design. The "toward S₀" form is the data-supported candidate (sufficient in every low-p case, not necessary), and it needs its own assumptions and proof.
2. **Delivery runs through the SMC moves.**
   - **At high p:** first discovery in the completed hits is in the pilot by Gibbs flips and swaps, and the final local search made no improving move in any of the 2,394 completed fits.
   - **At low p:** every first truth score is also in the pilot, mostly from initial draws or Gibbs flips. EVIDENCE_L notes that this attribution neither tests local-search repair nor rules out a later local-search role.
   - So T38's eligibility and delivery step should be argued through the bridge, Gibbs and swap moves (a T24-type or pilot-discovery route, or LS0). The masked regime is the default case.
3. **The open work in the error budget looks statistical rather than computational.**
   - At low p there are 0 search misses against the exact reference.
   - At p ≫ n there are 0 *detected* search misses: every completed miss has a better-scoring competitor, but whether the truth was ever scored in those 565 fits is unidentified, and the T21 probability bound is silent there.
   - That points to T03/T02 (supersets at strong signal) and T07 (same-size swaps at weak signal).
4. **Exactness claims rest on the low-p study.** Ẑ unbiasedness (T12) and PIP accuracy (T26) are supported at p ≤ 30 only; at p ≫ n they are silent by design.
