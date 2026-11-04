# THEOREM_REVISION_INPUTS — MEET-v31 → the theorem meeting

Amended by HQ on 2026-11-04 (AMENDMENT_HQ_01.md) after independent review.

**Prepared for the chair of MEET-v31, 2026-11-03.** Input to the **next** meeting, which decides the final theorem list. Reader: the PI, through HQ.

**Status words** follow `theory_campaign/PROTOCOL.md`: PROVED, PROOF SKETCH, COUNTEREXAMPLE, CONJECTURE, OPEN. Registry words and PC verdicts are copied from their sources.
- **Every PROVED here is a candidate** (not reviewed, not adopted). No status is upgraded.
- "Seat-proved, unchecked" = a seat gave an argument that no proof check (PC1/PC2) has covered.

**Sources.**
- `TL` = `origin/theory/THM-SYNTH:theory_campaign/THM-SYNTH/THEOREM_LIST.md` @ fc712e7 (`TL:n` = line).
- `INV` = `origin/theory/THM-INV:theory_campaign/THM-INV/REPORT.md` @ 440a38d. §1 = component × property matrix: rows 1–14; columns **V** validity, **A** accuracy, **C** cost, **F** failure mode, and "Properties with NO theorem".
- Under `theory_campaign/MEET-v31/` on `theory/MEET-v31` @ c13487c: `S1`, `S2`, `S3` = `SYNTH_R1/R2/R3.md` (S3 is authoritative for adopted texts); `R2A…R3C` = seat files; `PC1`, `PC2` = `evidence/2026-11-03_PC1_proof_check.md`, `evidence/2026-11-03_PC2_certificate_card.md`; `AM01` = `evidence/AMEND_01_general_np.md`.

**Meeting state.** All items closed; item 1 closed by the agreed rule as Outcome 2 (§1.B); all seats "R3-7: none". Open method questions: none, **conditional on N9** (running). If N9 fails, the method question reopens before the theorem meeting (§3 N9, a closure gate). Obligations tied to a binding proposal goal (N1, S4, N9) follow the escalation rule stated at N1, S4 and N9 (HQ, 2026-11-04).

---

## 1. Method decisions that matter for theory

### 1.A Closed decisions

| # | Decision | Consequence for theory | Source |
|---|---|---|---|
| M1 | **v3 unchanged as a statistical method** (target, prior, cap K, blocks, bridge, move round, calibration law, budgets). Changing counts, order or kernel of the move round is WORKHORSE. C8 (split N_e), C9 (shorter calibration), C10 (particle-parallel kernel) rejected. | Every v3 theorem stays about the shipped method. C10 would break R5(b2), BG3, V5. | dossier §2; S1 item 3; R1_B:64 |
| M2 | **LS0 in the shipped core, after the final local search.** Reads no uniforms; own provenance and `ls0_improved` flag; no E3; an LS0 stop (operational interruption) = no complete output (OP-LS0); a completed LS0 capped at `local_limit` still returns output, with L1 = "n/a". Island outputs, Ẑ, PIPs unchanged; scored set nested; best score cannot fall; **𝒯_new = top_c(𝒯_old ∪ 𝒮_added), not a superset**; HPM unchanged in 2,394/2,394. Tie-aware DP on truncation (e4). | T38(b1)/(b1-LH), LS-score about the shipped method (TL:41, 686; INV row 11). | S1 item 2; S2 D3c, P-9 e4 |
| M3 | **HPM is the only decision rule.** MPM reported per named PIP; no HPM-vs-MPM flag; `local_certified` = 1-flip/swap local certificate only. | R2/R4/R5 stay the selection theorems; MPM results descriptive. | S1 item 2 |
| M4 | **Ẑ-weighted PIP primary; equal-weight named secondary.** Both MPMs reported; R_eff = (ΣW)²/ΣW² per fit. POST HOC. | V3(ii), A1 are about the **primary**; A4 about the secondary. | S2 D5 |
| M5 | **Parallel layer (a)–(h).** (a) Final islands as **process** workers, Lemma S merges (Prop W). (b) Concurrent diagnostic islands (W-cal); no "bitwise" for (b) until executed. (c) Parallel scans. (h) Block-table stage = explicit parallel local step. "Bitwise" = one binary (`Makevars.v3`), single-thread BLAS, process workers, unchanged fp summation order. Threads need private counters merged deterministically (`cpp/v3_score.h:20–21, 231–236`). | V2 scopes; D1 depth at this level. | S1 item 3; S2 D3e–f |
| M6 | **GUARD-W: "any worker stop, LS0 stop or guard stop ⇒ no output".** Lemma RO stays as recorded (XF VERIFIED). GUARD-W in the v3.1 worker, merge and LS0 code is a **new code-audit obligation** (engineering, class (iv)), not a method question. | Premise (i) of every output-event statement and of card G2; N2(e). | S3 R3-5(ii) |
| M7 | **Stacking.** R′ = 4 default; optionally R′ = 4k at **unchanged N_e**, declared before stream 10, on streams 10..9+R′. **N_e never split.** **Extra local search from the R = 4 centre c₄ kept.** Baseline record (islands 1–4, baseline HPM and search) and expanded flags over all R′ islands; **one certificate card per reported record**. | PC1 claim 6: with the extra search, nesting and HPM(R′) ⪰ HPM(4); without it COUNTEREXAMPLE. No listed theorem needs monotonicity. | S2 D3a–b; PC1 `:159–202`; S3 R3-1 |
| M8 | **Calibration unchanged, with a contract.** 𝓒 frozen before final randomness; validity conditional on any frozen 𝓒; Theorem G cap; ≤ ℓ rebuilds per tier (≤ 2ℓ with escalation); restricted ESS on V only; statuses distinguished. Cost wording counts calibration (single tier: 0.0512 + 0.2048·I of final trajectory work; seat-derived). | Rebuild convergence, P(S₀ ∈ V), P(schedule_limit) are **OPEN obligations, not inherent**. | S1 item 4; S2 D4; R2A D4 |
| M9 | **D7 estimator spec (adopted).** 𝓗 = finite list of bounded model-space functions. Default, fixed from (X, y): model-size indicators; joint inclusion on neighbour-graph edges (≤ 2pB pairs). A user may declare h **measurable in (X, y, 𝓒)** (fixed before stream 10); N1, conditional on the frozen 𝓒, covers it. An h defined from other calibration information is covered only if that information is included in 𝓒 before freezing (enlarge 𝓒 when necessary). H_r(h) = (4N_e)⁻¹ Σ_q Σ_i h(S_rqi) after each complete measured round (φ = 1, equal weights after multinomial resampling; B checked the code). Report μ̂(h) = Σ_r Ẑ_r H_r(h)/Σ_r Ẑ_r and the equal-weight version. **Joint h: plain averages (c_h = 0). RB only for marginal PIPs**; no RB joint estimator ships (v3.2 at most; the kernel computes no pair conditionals, `cpp/v3_engine.h:349–364`). Products of marginal RB-PIPs are not joint estimates. **HPM terminal frequency dropped from 𝓗**: descriptive diagnostic, no theorem, printed next to e^{F(Ŝ)}/Ẑ. Optional archive (key → count multiset); an h chosen after the run does not inherit the fixed-h guarantee. Continuous parameters: h̄(S) = E[h \| S, X, y]. ADDITIVE; no re-run; no joint claims for the 2,400 fits. | Defines A1's estimator; A1's RB clause restricted to marginal PIPs. Identity = N1. | S3 R3-3 |
| M10 | **Certificate card (adopted), POST HOC** = PC2's minimal card: G1, G2, L1, L2, L3 always; R optional (declared U-rule, node budget, τ printed). Additions (S3 R3-1): **(A)** one declared budget (scores, B&B nodes) covers L1, L2, R; "unresolved" on exhaustion; a failed certificate never changes the fit's status. **(A)** L1 is evaluated on the finally returned Ŝ, from whichever search ended on it (final local search or LS0); a completed LS0 that ends on its move cap (`local_limit`) gives L1 = "n/a" (an operational LS0 interruption gives no output, GUARD-W). **(B)** G2 premise (i) = "Lemma RO (XF VERIFIED) plus GUARD-W … a code-audit obligation, not a mathematical gap". **(B)** One card per reported record (baseline, expanded), each with its own 𝒯 and Z_𝒯. **(C)** G2 is joint with output, never conditional on completion; rigorous fp coverage needs validated SC and VAL-FP. Label "numerical implementation of an exact-arithmetic certificate", η printed. Exclusions per PC2. Z_𝒯 and MASKZPIP C1 ship; E1–E3, ESS, grid flags stay triggers / labelled heuristics. No feedback into calibration. | A2, A3; N6, N7. | S3 R3-1; PC2 `:194–235` |
| M11 | **Output convention.** Guarantees for the potential run and as **P{𝒪, ·}**, never P(· \| 𝒪). Allocation = class (c), decides delivery only. Every estimate on 𝒪 is a function of (X, y, seed, binary). `fit$log_Z` = NA on stopped fits. | V4, R4, R5, N6, the card. | dossier §2(g); S2 P-9 e8 |
| M12 | **Item-9 table (adopted).** No setting is class (e) in the method's law. **e1** B* = 16 a (c) table budget; W7-PART's g_max ≤ B < 2g_min a theorem hypothesis; g = 5 ⇒ N8. **e2** 10⁻⁹ list kept, η(Ŝ) printed, heuristic list at max(10⁻⁹, 2η(Ŝ)); exact pairwise margin η(S) + η(Ŝ), but the store keeps only (F, S), so 2η(Ŝ) is the labelled proxy. **e3** n = 2 admitted (K = B = 1, exact branch; a proposed extension: current preprocessing still rejects n < 3 and raw p = 0). Spec sentence (R3B's, **seat-derived, unchecked**): "At n = 2 every centred non-constant column is proportional to (1, −1), so all singleton models have exactly equal F. The exact output is ∅, or the lexicographically smallest singleton with a p-fold exact tie, reported as such." Duplicates are **kept** (spec §4 rule 5, `cpp/v3_core.cpp:715–728` only report them; chair-checked); that code check is not a proof of the n = 2 output. `degenerate_n` (n = 1), `no_predictors`; n = 0 rejected. **e4** tie-aware DP on truncation; invariant OPEN (N3). **e5** `global_certified` heuristic. **e6/e7** engineering. **e8** allocation (c). **w1** r_n = √(2 log p/n); **w2** all p at n ≤ 5; **w3** 1-NN fallback if p > e^{n/2}; **w4** "the ℓ² term exceeds 1,000 exactly when n + p ≥ 2³¹" (inclusive); **w5** size cut only; **w6** comment → 16; **w7** streams 10..9+R′. **ESS 0.90: (c)**, a declared one-step dispersion budget; B's caveat: "defines the law of 𝓒; carried by the theorems as a hypothesis (Theorem G needs the same threshold for pilot and grid)". **Remaining constants** (R3C text): (c) budgets with (b) formulas; 60 halvings (d); one-nat thresholds (c) diagnostic criteria; conventions, not optima; not automatically law-preserving to change. No p ≪ n / p ≫ n rule. | N3, N8, N12; Theorem G; IND-T for streams 10..9+R′. | S3 R3-4 |
| M13 | **Declared v3.2 path.** C6 (per-particle counter streams, LAW-PRESERVING) implemented and law-checked **iff** paper 1 claims particle-parallel depth **or** demonstrates any fit with p > 2,500. This is HQ's disposition: the union of the two recorded conditions (Seats A/B: any p > 2,500, R2A:23, R2B:21, R3B:44; Seat C: a particle-parallel depth claim); the narrower trigger was not unanimously adopted. Felipe decided (2026-11-03) that paper 1 claims island-level depth only, and the study has p ≤ 1,000, so neither trigger currently fires. C7 (Gram-free scorer, LAW-PRESERVING in exact arithmetic). Island-parallel results reportable with actual cost. "Free of N, H, R" dropped for v3.1. C11 clustering, neighbour graph, grid bisection, convolution, pooling → cost account. | D1(c), D3(b) restated. | S2 D3d, D3e |
| M14 | **Limitation wordings.** (i) **Adopted D6(i)** (verbatim in I2). (ii) Literal "no run can upper-bound Z" is false. State only what is proved: T31(c) (positivity and unbiasedness of Ẑ alone yield no upper bound on Z; a non-implication, not a data-specific impossibility) and PC1 claim 1's analytic bound (N17; gap to Z data-dependent). The blanket "no *useful* upper bound from the run's record alone" is withdrawn as an inherent limitation (HQ amendment 01). (iii) "Markov gives the assumption-free probabilistic lower bound; max{Z_𝒯, 0.05Ẑ} keeps 95%". Sharper bounds need information beyond positivity and the mean; Markov sharpness is seat-derived, unchecked (§4.B). (iv) Masked weight variance: mechanism PROVED in kind; severity on the production grid OPEN (V11). | §4. | S3 R3-2; S2 D6; PC1 claims 1–2 |

Engineering actions (cannot change a decision): W-cal executed, integrated-LS0 replay, GUARD-W audit, IND-T for streams 10..9+R′ (S3 R3-7). R3A's D5 reversal criterion is for HQ to read against the full PIP rescoring; if it fires, it is a report to Felipe, not a re-run.

### 1.B Item 1 (block start)

**Item-1 outcome: Outcome 2 (keep, reframe).** 9 of 12 designs were complete for arms A–C; all 9 were inconclusive under the > 1 nat clause because arm C (prior start) was 2.6–13.3 nats below A and B. So the rule never compared A and B head to head. Certified count: arm C's log Ẑ is below the best score found by any arm on 10/12 designs, so Ẑ < Z in exact arithmetic; arms A and B on 0 (`evidence/item1_scripts/HQ_NOTE_v2.md`). Descriptively, B agreed with A's log Ẑ within 0.24 nats (agreement, not certified accuracy) and cost more (rebuilds ≥ A on 9/9; three B fits unfinished after 3–4 h vs 10–28 min for A). Source: `ITEM1_ABL_START.md`. Theorem consequence: the Outcome-2 row below. N18 is **not** opened. A confirmatory A-vs-B / A-vs-C test is an optional HQ action, which could later license a depth claim and then open N18.

Rule (S2 §2) committed before any arm-C or S4/S5 result was read; some arm-A/B results were already filed (S1 r001 c100 in `evidence/2026-11-03_pip_rescore/REPORT.md`, a240857; arm A's bitwise check, S2 §0.3). **v3.1 ships the block start under every outcome**; HPM counts are reported but do not decide. Conventions adopted before results (S3 R3-6, all ACCEPT):
- a design on which any of arms A–C did not finish or has no complete output, or whose pooled log Ẑ disagree by > 1 nat, is **inconclusive** and counts toward neither Outcome 1's nor Outcome 3's 9/12; an arm-A stop is a delivery event (e8, R6), not a start-quality signal;
- fewer than 9 conclusive designs ⇒ **Outcome 2**;
- fewer than 12 completed designs ⇒ the same proportions on the completed designs, and both S4 and both S5 designs are still required for Outcome 3;
- executable rule: the committed v1 script (`evidence/item1_scripts/apply_rule.py`) lacked the absolute 9-design gate. HQ's corrected `apply_rule_v2.py` enforces need = max(9, ⌈0.75·complete⌉), so the absolute gate is kept alongside the proportional sentence; it reproduces Outcome 2 (`HQ_NOTE_v2.md`, commit 8f6051b);
- no outcome reopens item 1 in this meeting; Outcome 3's follow-up goes to HQ. Arm D is v2 evidence only.

| Outcome | Condition (S2 §2) | Theorem-list consequences |
|---|---|---|
| **1: keep, depth claim allowed** | Arm A: T ≤ min(T_B, T_C) and rebuilds ≤ min on ≥ 9/12; accuracy not worse than B or C by > σ_r on ≥ 9/12. | S1, S2 as written; the paper may say the block start buys depth, but **no TL theorem compares A₀ or T across starts**: D2(c)'s T* = log₂A₀ + O(1) (ideal grid) predicts only ≈ 1–1.2 stages saved (`SYNTH_R1.md:17`; Seat B: any advantage comes from the bulk spread of d(S)). The claim is **empirical** (12 designs × 1 seed), or **N18** is opened (OPEN). |
| **2: keep, reframe** (also if inconclusive) | Accuracy not worse on ≥ 9/12; depth condition fails. | S1, S2 framed as "the exactly computable, theorem-bearing local step plus the parallel table stage (h)". **No depth or speed claim for the start**; D2(c), D3(b) keep A₀ as a property of the shipped start only. C1(e) stands. No new obligation. |
| **3: real issue flagged; block start still ships** | B or C beats A on accuracy by > σ_r on ≥ 9/12, incl. both S4 and both S5, and is not worse on depth on any S4/S5 design. | Paper 1: as Outcome 2, plus the ablation as a disclosed weakness and a ≤ 20-seed paired check on the two worst designs. If it confirms, a **WORKHORSE v2 candidate** goes to Felipe; v2 must re-prove for the new start everything using π₀: S1(a)–(d), S2, D2(c)'s A₀, C1(d), above all **R5(b1)/(b1-LH)** ((M1) needs P₀(π₀(S°) > ½) → 1 for the block start). Paper-1 theorems unchanged. Helper's reading (E5): DIL-E ("any data and partition", TL:432–433) may cover arm B as B = 1; arm C is not a block product. |

---

## 2. Per item of THEOREM_LIST.md (in order)

"Current" is copied from TL. Actions: keep / restate / drop / split / merge / new hypothesis.

### G1. Validity under parallel execution

| ID | Current (TL) | What the decisions change | Action | Source |
|---|---|---|---|---|
| **V1** Thm V | (a),(b) T12, T31(i) PROVED-LOCKED; (c) ADRAFT-ThmA PROVED (Astra only), Prop P(ii) PROVED (candidate); (d) Prop 2(c) PROVED-LOCKED / Prop P(iv) PROVED (candidate); V5 no registry row. v1. (TL:21, 55–94) | (1) "R declared" → "R′ = 4k, N_e, 𝓒 declared before stream 10; streams 10..9+R′"; EX-S/IND-T for the extended map. (2) V1(a) is stated for general bounded h, but the locked identity covers Ẑ and the RB marginal PIP only (INV row 8). (3) (b) in output-event form: P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜), same event as max{Z_𝒯, 0.05Ẑ} (PC1 claim 2). (4) Hypotheses GUARD-W, process workers. (5) (c) = consistency of the **primary** estimator. | **Split (S3 R3-5(i)):** (a1) Ẑ, RB marginal PIP, locked; (a2) general bounded h at the M9 accumulation point, **PROOF SKETCH = N1**. **New hypotheses** (stream map, GUARD-W). **Restate** (b). V5 → N9. | S3 R3-5; PC1 `:41–76, :98` |
| **V2** Prop W / W-cal / Lemma S / Cor W-R | Lemma S PROVED; Prop W PROVED (code reading), executed "1/1 design + smoke"; W-cal PROVED (code reading), not executed. v1, supplement. (TL:22, 96–121) | (1) Executed: **smoke + 3/3 study designs**; 1.9× on 2 cores, **no 4-core figure**. (2) Scope per M5. (3) LS0: "island outputs bitwise", **not** "stores nested"; 𝒯_new = top_c(𝒯_old ∪ 𝒮_added) (R2C D3c, seat-proved, unchecked); no E3. (4) Cor W-R as written **PROVED** (PC1 claim 6), amended: E3 and `local_certified` on islands 1–4 match only on the search from c₄. **Cor W-R(b)**: with the extra search, post-search nesting and HPM(R′) ⪰ HPM(4) (PROVED); without it FALSE (COUNTEREXAMPLE `c6_ls.py`). | **Restate**; **add** Cor W-R(b). Prop W stays a code-audit fact (TL:119). | S2 D3a–c, D3f; PC1 `:159–202` |
| **V3** Prop P | PROVED (candidate, elementary). v1. (TL:23, 123–149) | (1) (ii) about the **primary** PIP. (2) **PC1 claim 3**: P(\|μ̂ − μ\| > ε) ≤ min{1, 4(M−1)/R + 4M/(Rε²)}, PROVED, W_r ≥ 0 stated, E[W_r H_r] = μ a premise. (3) (v) covers R′ = 4k. (4) E[W²\|𝓒] may be exponential (V11 OPEN). (5) R = 32 × 312 runs split N_e: not stacking evidence. | **Keep**; "secondary" → "primary"; **add** PC1 claim 3 as (iii′); merge (iii) into A1. | S2 D5; PC1 `:79–100`; R2C `:236` |
| **V4** Lemma RO + GUARD + CEX-guard | Lemma RO PROVED, XF VERIFIED (A-REV6); GUARD fact HOLDS (literal ERROR); CEX-guard COUNTEREXAMPLE. v1, supplement. (TL:24, 151–168) | (1) **Resolved (S3 R3-5(ii)):** Lemma RO stays as recorded (XF VERIFIED conditional implication). PC1/PC2's "unreviewed" refers to GUARD-W in the v3.1 worker, merge and LS0 code (API-AUDIT covered the serial v3 guard only). (2) OP-LS0. (3) Allocation (c); Lemma RO makes "estimates are a function of (X, y, seed, binary)" true. (4) `fit$log_Z` = NA. | **Split:** Lemma RO (keep) + GUARD-W (**code-audit obligation N2(e)**), premise (i) of N6/N7 and card G2. Do not downgrade the lemma or certify the new code (R3C). | S3 R3-5(ii); PC1 `:63–69`; PC2 `:64` |

### G2. Posterior accuracy

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **A1** Thm H (NEW-SYNTH) | PROOF SKETCH; NEW-COMP; v1. (TL:25, 174–218) | (1) Estimator = M9 (plain averages, Ẑ-weighted primary). (2) **TL A1(i)'s RB clause ("RB version when h is a product of inclusion indicators") is restricted to marginal PIPs; c_h = 0 for joint h** (S3 R3-3(b)). (3) h ∈ 𝓗, measurable in (X, y, 𝓒); 1{S = Ŝ} is out of 𝓗. R3B (unchecked): an h fixed by streams 0–9, e.g. 1{S = best model of the calibration store}, is covered by N1, if a theorem-bearing mode frequency is wanted, provided 𝓒 is enlarged to include the information defining h (measurability in streams 0–9 need not imply measurability in the compressed 𝓒); no final-run selection. (4) Add PC1 claim 3 (\|μ̂ − π(h)\|) beside Maurer/Hoeffding (b). (5) Simultaneous bounds over q_n summaries need multiplicity. (6) h̄ for continuous functionals. (7) No claims for the 2,400 fits. (8) Crux = **N1**. | **Restate** around M9; **new hypothesis** h measurable in (X, y, 𝓒); **drop** RB-joint for v3.1 (no status change). If N1 fails, A1 shrinks to marginal PIPs and the binding §13.1 goal goes to HQ escalation (N1). | S3 R3-3; R2C D7; PC1 claim 3 |
| **A2** Thm Z | (i) T12/T31(i) PROVED-LOCKED; (ii) O-PW2 Thm A PROVED, XF VERIFIED; (iii) E1/E2 PROVED (candidate); (iv) MASKZPIP C1 PROVED; (v) T26-ThmA PROVED, XF VERIFIED*. Two-sided masked: v2. (TL:26, 220–255) | (1) **PC1 claim 4:** TL:26 and TL:236 "errs/can only fail downward" are **literally false** (COUNTEREXAMPLE; formal (iii) not refuted); use `PC1:124–126`. (2) Remark **PC1 claim 1**: Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}, PROVED (N17). (3) max{Z_𝒯, 0.05Ẑ} coverage in (i), output-event form, joint (card G2). (4) (iv) = card G1. (5) Masked severity OPEN (V11). | **Restate** (mandatory wording); **add** two PROVED clauses. | PC1 claims 1, 2, 4; PC2 C1 |
| **A3** Thm Z𝒯 | MASKZPIP P3 PROVED (candidate, deterministic). v1. (TL:27, 257–271) | (1) **PC1 claim 5 (amended, PROVED):** S₀ ∈ 𝒯 and **δ₁ < ½ ⇒ MPM^𝒯 = S₀**, ½ sharp; Seat B's "δ₁ < ⅓" FALSE. (2) **Retention** on {δ₁ < ½}: S₀ ∈ 𝒮 ⇔ S₀ ∈ 𝒯 (𝒯 = top_{40p+1}(𝒮) via Lemma S + calibration re-offer, `v3_core.cpp:409–419`); unqualified retention false. (3) Holds under LS0 (card L3 premise). (4) PIP^𝒯 labelled "restricted". (5) fp: numerical until SC. | **Restate:** MPM^𝒯 clause + retention lemma (N13); compose with R5. | PC1 `:130–155`; PC2 `:22–25` |
| **A4** Thm PIP (equal-weight) | P1 PROVED; P2 PROVED (composition, LH fixed p); Thm R PROVED as composition, CONDITIONAL on DELIV-POP (OPEN). P1 v1, Thm R v2. (TL:28, 273–292) | Equal-weight is the **secondary** (M4); A4 explains why it does not improve with R. | **Keep;** supplement (recommendation). Thm R v2. | S2 D5 |

### G3. Parallel work and depth

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **D1** Thm D | Prop D PROVED (counting); T32(i) PROVED, rate GAP. v1. (TL:29, 298–333) | (1) v3.1 is island-parallel: D1(b), depth N_e(T+L+4)(p+B+2) sequential elementary-step slots (not scorer operations or seconds; tier e uses H_e; R′ above the worker count runs in waves) plus score costs, setup, calibration, grid, reductions and finite-worker scheduling. **"Free of N, H, R" (TL:29, 309) and the TL:29 summary formula are particle-parallel, v3.2 only (C6).** (2) Terms: (h) tables, LS0, extra search (≤ ℓ+1 scans), R′ = 4k width. (3) Calibration on the critical path: single tier 0.0512 + 0.2048·I of final trajectory work (R2A, seat-derived; predicted 0.46/0.67/1.69 vs observed 0.45/0.62/1.76); ≤ ℓ rebuilds per tier, ≤ 2ℓ with escalation; depth (1+I_e)·H_e (R2B). (4) No 4-core speed-up. (5) Superiority over sequential MCMC is **empirical**, needs a comparator. | **Restate** (b) as the v3.1 theorem; (c) a v3.2 remark iff C6; fix TL:29. | S2 D3d, D3e, D4 |
| **D2** Thm STG | Theorem G PROVED; STG-F PROVED; STG-M PROVED (ideal two-state grid), XF VERIFIED*; families PROOF SKETCH; as-coded masked T_n Conjecture P OPEN. v1 ideal grid + T_e cap; as-coded v2. (TL:30, 335–370) | (1) T ≤ T_e is the as-coded guarantee; Conjecture P in N5(b3). (2) Ideal stage laws ≠ laws of the realised rebuild process. (3) Theorem G carries ESS 0.90 (same for pilot and grid) as a hypothesis. (4) A₀ of the block start vs others: item 1. | **Keep;** wording; state the ESS hypothesis. | S3 R3-4; R1_C:235–241 |
| **D3** Thm CD | Assembly; weakest links A1, C1 (PROOF SKETCH), as-coded T_n (OPEN). v1 in REPORT §3 scope. (TL:31, 372–398) | (b) "free of N, H, R" (TL:378) → island-level depth; (b) "costs depth through A₀" is outcome-dependent; (a) uses the M9 estimator; (c) adds PC1 claim 3 and stacking at N_e; (d) uses R5(b1-LH) for the shipped method. | **Restate** (b), (d); conditional on item 1. | S2 D3d; §1.B |
| **D4** Cor V | PROOF SKETCH. v2. (TL:32, 400–415) | Never splitting N_e and stacking at fixed N_e are shipped; Cor V motivates them. The R = 32 × 312 runs bear on Cor V, not on stacking. | **Keep v2;** v1 states Prop P(i)/(ii) plus the decision. | S1 item 3; R2C §2 |

### G4. Why the bridge

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **S1** Thm 2 (start) | T22(i)(ii)(iv) PROVED-LOCKED; T22(iii) PROVED-LOCKED CONDITIONAL; T27(i) PROVED-LOCKED CONDITIONAL, Thm3/4-EXP XF VERIFIED; DIL-E/E1/R/N PROVED, XF VERIFIED. v1. (TL:33, 423–455) | Framing per item-1 outcome; content unchanged for paper 1. W7-PART's g_max ≤ B < 2g_min is a theorem hypothesis (e1); study g = 5 outside it (N8). | **Keep;** framing per outcome; state the SIZE hypothesis where W7-PART is used. | S2 §2, P-9 e1 |
| **S2** Thm SEP + Lemma KL | SEP-A/B PROVED, XF VERIFIED; Lemma KL PROOF SKETCH (NEW-SYNTH); (d) PROVED (candidate). v1. (TL:34, 457–492) | Outcome-independent. SEP-B is the mechanism behind M14(iv). (d): "moving off the start is needed", not "tempering is needed". | **Keep.** Lemma KL into the next proof-check batch. | S2 D6; R1_C:241 |
| **S3** Prop M | Dropped. (TL:35, 494–499) | No change. | **Keep dropped.** | — |
| **S4** Weight stability | Supplement remark; v2. (TL:501–509) | §5.3 needs a theorem for the **actual** block product incl. common noise integration: **OPEN, not inherent**. | **Keep v2;** list as OPEN. If it fails, the binding goal is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change (proposal §5.3, binding). | R2C `:259` |

### G5. Correlation robustness vs split-and-merge

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **C1** Thm SL (NEW-SYNTH) | COUNTEREXAMPLE (numerical) + PROOF SKETCH. v1 on exact-Gram LH; LH-iid v2. (TL:36, 515–581) | (1) (d) is about the shipped method (R5(b1-LH) applies). (2) (d)'s "joint inclusions satisfy A1" holds only via M9 plain averages (c_h = 0), for declared pairs, conditional on N1. (3) Name clash: E2. | **Keep;** **restate** (d). | M2, M9 |

### G6. Selection accuracy

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **R1** Thm 1 (T03♯) | T01–T03 PROVED-LOCKED; T03♯ PROVED, SF + XF VERIFIED. v1 (asymptotic; disclose n ≳ 2·10⁶). (TL:37, 587–604) | Scope sentence: p ≤ n^A comes from the **target theory** (Felipe's prior, proof technique), not the sampler. Song–Liang's e^{Cn^α} cannot be imported; whether our prior admits it is **OPEN, not impossible**. | **Keep;** add the scope sentence (N12). | S2 P-9 theory scope |
| **R2** Prop 1 (Bayes rules) | PROVED-LOCKED; XF VERIFIED*. v1 remark. (TL:38, 606–613) | No change (true posterior). PC1 claim 5(a) is about the reported HPM and belongs in R4. | **Keep.** | PC1 `:132–138` |
| **R3** Thm 3 (Theorem A, LS-score) | Theorem A PROVED, XF VERIFIED*, Lean sorry-free; LS-score PROVED, XF VERIFIED (A-REV8); Lemma M PROVED, XF VERIFIED. v1. (TL:39, 615–634) | LS-score is about the shipped method. **New hypotheses:** (1) LS0 centre = prescribed smallest-size lexicographic start mode, tie-aware DP on truncation (e4; DP invariant OPEN, N3); (2) ℓ ≥ max{Φ(S°) − 1, 0} (N11); (3) completed scans / OP-LS0. | **Keep;** **new hypotheses** (1)–(3). | S3 R3-4 e4; R2B row 7 |
| **R4** Thm 4 (T21(C1), T38(0), N200, RO) | T21(C1) PROVED-LOCKED; T38(0) PROVED, XF VERIFIED; N200 PROVED (author only); Π(X) upper bound OPEN. v1. (TL:40, 636–656) | (1) Output-event form (M11). (2) **Add PC1 claim 5(a)**: Ŝ = S₀ if S₀ ∈ 𝒮 and δ₁ < ½, sharp (PROVED). (3) "0/2,394 S₀ ∉ 𝒮" transfers to R′ > 4 **only because the extra search from c₄ is kept** (PC1 `:197–201`). (4) Lemma RO under GUARD-W. | **Keep;** add (2) and the transfer caveat. | PC1 claims 5, 6 |
| **R5** Thm 5 (T38) | (0) PROVED, XF VERIFIED; (a) PROVED-UNDER (F); (b1) PROVED-UNDER (M1)–(M3), XF VERIFIED; (b1-LH) PROVED (candidate), XF VERIFIED; (b2-LH) PROVED-UNDER STAB-LH; (b1-LH-iid) XF GAP; (c) PROVED-UNDER T32(i). v1: (0),(a),(b1-LH),(b2-LH),(c). (TL:41, 658–692) | (1) M2 answers TL:686: **headline (b1-LH) for v3.1**, (b2-LH) the no-LS0 corollary; shipped-code status via N3. (2) Routes carry to any R′ by nesting. (3) (c) cost: LS0, extra search. (4) Scope: exact-Gram LH needs p ≤ n − 1, g_max ≤ B < 2g_min; LH-iid XF GAP; study generator N8. (5) Outcome 3 → v2: re-prove (M1). | **Restate** headline; **new hypotheses** OP-LS0, e4, SIZE, GUARD-W. | TL:686; PC1 `:181–193` |
| **R6** Delivery P(U) → 0 | NONE; "limitation in v1 … ≈ 4× headroom". (TL:42, 694–700) | (1) **OPEN, not inherent**; only "a fixed allocation cannot support unrestricted growth" is definitional (V13). (2) **"≈ 4× headroom" is not measured** (1.9× on 2 cores). (3) Replaying the 6 stopped fits is optional and cannot establish a theorem. (4) Allocation (c); an ABL-START arm-A stop is a delivery event. | **Restate** "OPEN (delivery)"; report 6/2,400 with the allocation; **remove the 4× sentence.** | S2 D8, e8; S3 R3-6 |
| **R7** Π(X) upper bound | OPEN. v2. (TL:43, 702–708) | No change. | **Keep v2.** | — |
| Cited lemmas (TL:45–49) | — | No change. INV D9's citation clashes need a primary-source check before printing. | **Keep.** | INV §2 D9 |

---

## 3. New theorem obligations

Each: statement; hypotheses; status; decision supported; if it fails; INV §1 cell(s), row × column.

**N1. Measured-round island identity for general bounded h (Theorem H crux; V1(a2)).**
- *Statement.* Conditional on a successful frozen 𝓒, for each final island r and each h ∈ 𝓗 with 0 ≤ h ≤ 1, measurable in (X, y, 𝓒): E[Ẑ_r·H_r(h) \| 𝓒] = Z·π(h), with H_r(h) as in M9.
- *Hypotheses.* EX-A, EX-S, CAL, V5 (each φ = 1 round π-invariant), multinomial resampling, R′ declared before stream 10.
- *Route* (R2C `:200–204`): the finite-state resample–move recursion gives E[Ẑ_r η_{r,T}(f)] = Zπ(f); terminal rounds preserve π, so the identity holds at each measured endpoint and for their average. R3A (unchecked): the base case of the locked terminal-round lemma.
- *Status:* **PROOF SKETCH**; PC1 claim 3 takes it as a premise.
- *Supports:* M9, A1, C1(d) joint clause, D3(a) for general h.
- *If it fails:* the binding goal is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change (proposal §13.1, binding). Until that decision: μ̂(h) carries no theorem; A1 shrinks to marginal PIPs (locked); M4 survives (Prop P(ii) for PIPs).
- *Cell:* row 8 × V (islandwise identity, extended); row 10 × "NONE: joint inclusion probabilities".

**N2. Integrated v3.1 core: Prop W, W-cal, LS0, stacking, GUARD-W.** Code-audit facts plus executed replays, not mathematical theorems (TL:119).
- *Statement.* For fixed (X, y, seed, binary), process workers, Lemma S merges: (a) final islands bitwise equal to serial (Prop W); (b) the 4 diagnostic islands, with persistent per-worker stream state, bitwise equal to serial (W-cal); (c) LS0 leaves island outputs, Ẑ, PIPs bitwise unchanged, gives 𝒯_new = top_c(𝒯_old ∪ 𝒮_added), fires no E3; (d) R′ = 4k with the extra search leaves islands 1–4 unchanged and nests the post-search scored set; (e) **GUARD-W:** v3.1 worker, merge and LS0 code satisfy "any worker, LS0 or guard stop ⇒ no output" (an LS0 stop is an operational interruption; a completed capped LS0 returns `local_limit`) (new code-audit obligation, class (iv); S3 R3-5(ii)).
- *Status.* Lemma S PROVED. (a) PROVED by code reading, executed on smoke + 3/3 designs. (b) PROVED by code reading, **not executed**. (c) not in the production core. (d) PROVED (PC1 claim 6, deterministic). (e) **not audited** (API-AUDIT covered the serial v3 guard only).
- *Supports:* M2, M5, M6, M7, card G2 premise (i), "the 2,394 study fits' saved sampler estimates are reusable as v3.1" (full v3.1 records pending: LS0 integration and flags, NA interface, certificates, primary rescoring).
- *If it fails:* (b) → LAW-PRESERVING, wall-clock claims capped at the D4 table, "bitwise" claims narrow; (e) → CEX-guard applies to v3.1 (N6); fixes are engineering; decisions survive.
- *Cell:* row 8 × V; row 7 × V; row 12 × "NONE: LS0 absent from production"; row 14 × V.

**N3. LS0-based T38(b1-LH) about the shipped method; e4 tie-DP invariant.**
- *Statement.* For v3.1 with LS0, on LH exact Gram (p ≤ n − 1, c linked pairs, g_max ≤ B < 2g_min): P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, with no open statistical hypothesis. Sub-obligation: on truncation the tie-aware DP returns the prescribed smallest-size, lexicographically smallest maximiser.
- *Hypotheses.* EX-A, EX-S, CAL, SR, GUARD + GUARD-W, (P), (M1)–(M3) (verified on LH), **OP-LS0**, the **LS0 centre rule** (e4), **ℓ ≥ max{Φ(S°) − 1, 0}** (N11).
- *Status.* (b1-LH) PROVED (candidate), XF VERIFIED (A-REV8) for "v3 + LS0"; bridge to code = N2(c), not done. DP invariant **OPEN**. R3A and R3B sketch the same route (unchecked): greedy choice j = 1..p, keeping j iff some size-k_min maximiser consistent with earlier choices contains j, each test a max-plus feasibility DP over (block, remaining size) (`v3_start.h:179–200`); polynomial, no tie enumeration. Study: 0/2,400 truncated; all had one tie.
- *Supports:* M2, M12 e4.
- *If it fails:* headline falls back to (b2-LH) on STAB-LH without LS0; M2 survives (ADDITIVE; HPM unchanged 2,394/2,394) without theorem motivation.
- *Cell:* row 11 × A; row 12 × V/A.

**N4. Finite-R accuracy of the Ẑ-weighted PIP and μ̂(h); the constant M under masking (V11).**
- (i) PC1 claim 3: P(\|μ̂ − μ\| > ε) ≤ min{1, 4(M−1)/R + 4M/(Rε²)}, M = E[(Ẑ_r/Z)² \| 𝓒]. **PROVED**, given N1 for general h or the locked identity for PIPs.
- (ii) Prop P(iii) with M1 (PROVED, candidate): regime-free distance to 1{j ∈ S₀}.
- (iii) **Obligation:** an upper bound on M on the production grid through a masked crossing (V11, "resolved grid ⇒ O_P(√(T/N))": CONJECTURE, OPEN for c ≥ 2). Known lower bound M ≳ 1/P_𝓒(cross), PROOF SKETCH (TL A1(v)); do not cite F-MASKPIP M3 (XF ERROR).
- *Supports:* M4; M7's R′ guidance; R_eff reporting.
- *If (iii) fails:* M4 survives (R-consistency holds; equal-weight has none); the paper claims correctness, not efficiency.
- *Cells:* row 10 × A; row 9 × "NONE: two-sided relative accuracy of Ẑ (masked)"; row 8 × "NONE: island variance vs correlation"; row 7 × A.

**N5. Calibration contract.**
- *(a) Validity for any frozen 𝓒:* every final-run identity (V1, N1, N6) holds conditional on any successful 𝓒 on streams 0–9, final streams ≥ 10 independent. Status: assembly of T12/T31(i) (PROVED-LOCKED, conditional on 𝓒), IND-T (PROVED, XF VERIFIED*, A-REV1 only), Lemma RO; IND-T for streams 10..9+R′ is a code-audit item. ESS 0.90 (pilot = grid) is a hypothesis.
- *(b) OPEN* (all NONE in INV row 7 and §5 item 9): (b1) rebuild-loop convergence within ≤ ℓ rebuilds; (b2) P(S₀ ∈ V), "V contains the competing pair"; (b3) P(schedule_limit), P(grid_unconverged) → 0, incl. as-coded masked T_n (Conjecture P).
- *If (b) fails:* M8 **survives** (validity conditional on any frozen 𝓒); only delivery and efficiency suffer. Each is stated OPEN beside the POST HOC tabulation of rebuilds, tier, T, convergence.
- *Cells:* row 7 × V (a); row 7 × "NONE" (b1–b3 stay empty); row 14 × "NONE: P(schedule_limit)"; row 5 × "NONE: realised T_n".

**N6. Output-event coverage statements.**
- (a) P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05; {L > Z} = {0.05Ẑ > Z}.
- (b) Card level: P(𝒪 ∩ {some G2, L or R item false}) ≤ 0.05·P(SMC ∩ 𝒜).
- (c) Every result is joint with 𝒪, never conditional on it: "the probability that a run returns a card with a false claim is at most 5%".
- *Hypotheses* (PC1 claim 2): (i) Lemma RO + GUARD-W; (ii) successful 𝓒 with E[Ẑ̄ \| 𝓒] ≤ Z; (iii) CAL, EX-S; (iv) Ẑ = Z on the exact branch; plus EX-A and distinct store entries. Rigorous fp coverage also needs validated SC and VAL-FP (N16).
- *Status:* (a) **PROVED** (potential run; output form CORRECT WITH AMENDMENT). (b) **PROVED modulo premise (i)**, whose GUARD-W part is the code-audit obligation N2(e).
- *Supports:* M10, M11.
- *If premise (i) fails:* CEX-guard applies and the output-event statements fail for v3.1; fix is engineering.
- *Cells:* row 9 × V; row 14 × V.

**N7. Certificate card G1/G2/L/R (PC2 verdicts; card as adopted in M10).**
- *By item:* **G1** (C1(a) amended, excl. Ŝ) PROVED, deterministic. **G2** (C1(b)) PROVED, output event, joint. **L1** (C3(a); empty maxima +∞; fp margin 2η_F) CORRECT WITH AMENDMENT; on the finally returned Ŝ. **L2** (C3(b)) PROVED. **L3** (C3(c), realised 𝒮, \|𝒯\| ≥ 2) amended form PROVED; premise holds under LS0. **R** (C4 + Lemma M) PROVED with amendments (drop \|L\| > K leaves; S ⊆ U, \|S\| ≤ K; SC covers Φ and M); C4(b) PROVED as written (isolating {Ŝ} is sharpness only; R3C withdrew). Card bound (C6) PROVED modulo premise (i). C6′ PROVED.
- Budget and per-record clauses: as M10.
- *FALSE or not a theorem:* C1(a) third clause; C1(b) "unscored mass" (COUNTEREXAMPLE `t4b`); the conditional C6 reading; "SC checkable by replay"; rigorous `global_certified` (η uses a *lower* condition-number estimate); the C4 cost remark.
- *Excluded from the output:* C2 (conditional on PW2), C5 (needs S₀; a study-level item).
- *Open sub-obligation:* SC(η_F) by validated arithmetic and VAL-FP(η, ε) at production size (N16); until then, labelled numerical.
- *Supports:* M10. *If SC is never validated:* the label stays (POST HOC).
- *Cells:* row 13 × F (per-fit certificates, **not** flag power); row 9 × F; row 12 × "NONE: meaning of `local_certified`" (L1, deterministic); row 11 × F.

**N8. PART-pairing for the study generator g = 5 (2g ≤ B).**
- *Statement (as far as sources go):* a partition law for complete linkage + size cut + next-fit packing with equal groups 2g ≤ B (study g = 5, B = 14): which groups are co-blocked, and does that remove masking (Prop Q)?
- *Status:* **OPEN**; Prop Q **PROOF SKETCH** (R2B row 6′); W7-PART CE2 COUNTEREXAMPLE (unequal groups not merged).
- *Supports:* M12 e1. *If it fails:* e1 survives (changing B or the cut is WORKHORSE); the study generator is disclosed as outside every selection theorem.
- *Cells:* row 3 × "NONE: partition law for the study's packing"; row 11 × "NONE: study generator".

**N9. V5: kernel reversibility, self-adjointness, exact start sampler.**
- *Statement:* each elementary move (Gibbs flip, uniform swap, neighbour swap, independence move with π₀ proposal) is γ_φ-reversible; a uniformly random order of reversible kernels is self-adjoint; the start sampler draws exactly from π₀ with exact Z̄₀.
- *Status:* by construction, consultant-checked, **no registry row** (INV §5 item 12; TL:77); one-page route (TL V1(v)).
- *Closure gate (HQ, 2026-11-04):* N9 is a closure gate, not an ordinary obligation; it is being checked against the code (branch `theory/N9-KERNEL`). Open method questions: none, **conditional on N9** (running). If N9 fails, the method question reopens before the theorem meeting. Status words above unchanged.
- *Supports:* M1, V1, N1, rejection of C10. *If it fails:* V1 fails; the method question reopens before the theorem meeting. The binding goal (proposal §5.1) is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change.
- *Cells:* row 6 × V; row 4 × V.

**N10. V10: L versus t_mix.**
- *Statement:* do L = max(4, ⌈log₂(n+1)⌉) terminal φ = 1 rounds give populations close to π?
- *Status:* **NONE / OPEN** (INV row 6); YWJ/ZYVR route blocked as stated (INV §2 D1). Validity (V1, N1) holds at any L; L affects accuracy and variance.
- *Supports:* M1. *If it fails:* theorems needing mixing carry L as a hypothesis.
- *Cell:* row 6 × "NONE: mixing / spectral gap".

**N11. ℓ versus the moves needed.**
- *Statement:* ℓ = ⌈log₂(n+p+1)⌉ ≥ max{Φ(S°) − 1, 0} (moves LS0 needs, LS-score), and the caps on the final local search and rebuilds are not binding w.p. → 1.
- *Status:* on LH with c ≤ s₀ fixed, "eventually true" (R2B row 7; elementary, unchecked); growing s₀: **OPEN**.
- *Supports:* M2. *If it fails:* R3/R5 carry ℓ as a hypothesis; growing support would need a bigger budget (method-induced).
- *Cells:* row 12 × C/A; row 7 × C (rebuild cap).

**N12. General (n, p) scope, per regime** (S2 P-9 theory scope; R2A–R2C §4).

| Regime | What theory may claim | Cause of any restriction |
|---|---|---|
| Tiny n | No asymptotic claim. n ≤ 5 exact for **all p** (chair-checked). n = 2 extension (e3, proposed; current code rejects n < 3): PROOF SKETCH (R2C E1); its p-fold-tie output statement (M12) is R3B's, elementary, **seat-derived, unchecked**; duplicates kept (chair-checked), which is a code fact, not a proof of the n = 2 output. n = 1 → `degenerate_n`; zero predictors → `no_predictors`; n = 0 rejected. | None from the method. |
| Fixed p, n → ∞ | Eventually exact dispatch (R2C §4.4, seat-proved, unchecked), so V2–V4 apply. | — |
| Growing p ≪ n | Polynomial-p target results under their assumptions; logarithmic L, ℓ may be short (N10, N11). | Method budgets (theorem hypotheses). |
| p ≈ n | Exact-Gram LH needs p ≤ n − 1; centred designs have rank ≤ n − 1. | Proof family's geometry, not the target. |
| Polynomial p ≫ n (p ≤ n^A) | T03/T03♯; T38(b1-LH-iid) XF GAP; study generator N8. | **Prior and proof technique** (INV §3b), not the sampler. |
| p ≤ e^{Cn^α} | No theorem; whether our prior admits it is **OPEN**, not impossible. | — |
| Joint growth | Budgets polynomial; by-definition limits: fixed allocation, Θ(p) round; w4 boundary n + p ≥ 2³¹. | Method-induced: K excludes s₀ > K; fixed B limits whole-group recovery to g ≤ B ("recovery as a single block", R3C); bounded stores; log ℓ and L; N₀ ≥ p. |

w1 and w3 affect proposal efficiency only; validity rests on the Hastings ratio.
- *Cells:* row 1 × A and row 1 × "NONE: growing s₀"; INV §3b "p up to e^{Cn^α}: LACK".

**N13. Retention lemma.** If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 = top_{40p+1}(𝒮), and the HPM and MPM^𝒯 certificates are equivalent.
- *Status:* **PROVED** (PC1 claim 5; R2C D7); premises Lemma S and the inheritance merge (PC2 code facts). Unqualified retention stays false.
- *Supports:* A3 ∘ R5, card L3, M2's eviction wording. *Cell:* row 11 × A.

**N14. Stacking statements.**
- (a) Cor W-R(b): post-search nesting, HPM(R′) ⪰ HPM(4) with the extra search. PROVED (PC1 claim 6).
- (b) Every listed bound holds per run for any R′ declared before final randomness (PC1 claim-6 table).
- (c) IND-T for streams 10..9+R′: code audit, not done.
- (d) One certificate card per record (M7, M10).
- *Supports:* M7. *Without the extra search:* PC1's three uses (monotonicity, D_n(R′) ≤ D_n(4), transfer of R = 4 measurements) go; no listed theorem affected.
- *Cell:* row 8 × V; row 8 × "NONE: choice of R vs N" (D4 PROOF SKETCH, v2).

**N15. Work and depth at the implemented level** (D1(b) restated).
- *Statement:* depth and work for island-parallel v3.1: setup, (h) tables, calibration ((1+4I_e)·H_e work and (1+I_e)·H_e depth per tier; ≤ ℓ rebuilds per tier, ≤ 2ℓ with escalation), final run N_e(T+L+4)m sequential step slots (not scorer operations or seconds; add score costs and finite-worker scheduling; R′ above the worker count runs in waves), LS0, extra search, population reductions.
- *Status:* Prop D PROVED (counting); calibration share seat-derived (R2A, R2B), not proof-checked.
- *Supports:* M5, M8, M13. *If it fails:* recount.
- *Cells:* row 8 × "NONE: work–depth theorem" (filled as counting; speed-up vs sequential MCMC stays empty, empirical); row 7 × C; row 5 × "NONE: depth vs correlation" (ideal grid via A₀ only).

**N16. Floating-point contract.** Validated SC(η_F) for scores, Φ, M, Z_𝒯⁻, and VAL-FP(η, ε) for Ẑ at production size.
- *Status:* **OPEN.** VAL-FP MEASURED at p ≤ 40 only; η a documented heuristic (`v3_score.h:240`); PC2's exact-rational test found no violation in 60 cases (max \|error\|/η = 0.069): not a proof.
- *Supports:* M10 labels, G2 fp coverage, e2, e5. *If never done:* labels stay "numerical".
- *Cells:* row 14 × "NONE: floating-point error theorem"; row 9 × "VAL-FP MEASURED at p ≤ 40 only".

**N17. Analytic bounds on Z and π(Ŝ).** Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}; equivalently π(Ŝ) ≥ e^{F(Ŝ)}(2b₀ + yᵀy/(n+1))^{ν}/C_n.
- *Status:* **PROVED** (PC1 claim 1; PC2 C1(c)). Its gap to Z is data-dependent: the ≈ 530-nat figure at n = 200 compares against m(∅), not against Z, and is not a universal looseness (n = 200, p = 1, y = x₁ gives log(U/Z) = 3.83; review check, SOL1 #27). Supports M14(ii).
- *Cell:* row 9 × "NONE … an upper bound on Z is impossible from a run": **INV's wording is literally false**; correct to what is proved (T31(c)'s non-implication plus this bound), not to a blanket "no useful upper bound".

**N18 (only under item-1 Outcome 1). Depth comparison between starts.** Under stated conditions, the block start's A₀ (or realised T) ≤ that of the singleton or prior start.
- *Status:* **OPEN**, no route in the sources. *If not attempted:* the depth claim stays empirical.
- *Cells:* row 4 × "NONE"; row 5 × "NONE: depth vs correlation".

**Carried over unchanged (already in TL):** DELIV-POP (A4, OPEN); Conjecture P (in N5(b3)); Π(X) upper bound (R7); LH-iid XF GAP (R5); S4 weight stability (§5.3).

**Not obligations:** the HPM terminal frequency (descriptive, M9); an RB joint estimator (not shipped; as a v3.2 option it would need its own identity, R3A/R3B).

---

## 4. Inherent limitations, and what is NOT inherent

### 4.A Inherent: PROVED impossible, or true by definition

| # | Limitation (narrow wording) | Why inherent | Source |
|---|---|---|---|
| I1 | Each move round has m = p + B + 2 sequential steps per particle. | Definition of the single-site, full-coordinate round: inherent **to the kernel, not to SMC or BVS**. Changing it is C10 (WORKHORSE). | Prop D remark; S1 item 3; R2C §3 row 8 |
| I2 | **Adopted D6(i):** "A full-coordinate move round visits all p coordinates and requires scoring access to every predictor, through X or sufficient statistics (8np bytes for X). That access may be local, shared or distributed; its computation and communication costs must be counted. Neither a private copy of all X nor a private 8p² Gram matrix per worker is inherent. C7 is the declared Gram-free scoring path, law-preserving in exact arithmetic, with floating-point fidelity checked separately." | Definition of a full-coordinate round. | S3 R3-2 |
| I3 | The product-of-blocks start is masked under T27(i)'s hypotheses (H2, H3; verified on LH): π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}. | PROVED-LOCKED, CONDITIONAL (H2, H3); on LH no open hypothesis. Scope: this construction and design class; it does not say every product start is masked on every design. | TL S1(c) |
| I4 | On LH with exact Gram and cancellation depth c, under TL S2's specified discovery and IS losses and its asymptotic Q/Q* regimes, one-shot importance correction from π₀ needs ≈ Q* = p^c n^{c/2} draws. | SEP-A/B PROVED, XF VERIFIED; Chatterjee–Diaconis 2018 Thms 1.1/1.2. About one-shot IS under these hypotheses; the reason the bridge exists. Not a universal cost lower bound for arbitrary targets, summaries or one-shot algorithms. | TL S2 |
| I5 | No diagnostic from the observed record (the run's own weights or island agreement) has a universal detection guarantee for never-visited modes. | MASKZPIP E1c PROVED; V12; Chatterjee–Diaconis 2018 Thm 2.1. Positive one-sided certificates (e.g. Ẑ < Z_𝒯, card G1) can still detect some failures. | INV rows 7, 13 |
| I6 | At n = 200 the exact posterior often misses S₀: 565 strict competitor defeats among the 2,394 completed fits (six stops) certify at least 565 target-mode misses, not the exact count on all 2,400 data sets. | Thm N200 PROVED (author only); Π(X) lower bracket PROVED. Data facts, not a universal rate. | TL R4 |
| I7 | T31(c): positivity and unbiasedness of Ẑ alone yield no upper bound on Z (a non-implication from the estimator's law; not a data-specific impossibility; it excludes neither structural nor record-based bounds). | Proved: T31(c) (PROVED-LOCKED, as cited by R2A D6(ii)) and PC2 C1(c) (PROVED relative to T31(c)). Literal "no upper bound" is **false** (N17). The blanket "no *useful* upper bound on Z from the run's record alone" is withdrawn ("useful" undefined; not proved) and listed in 4.B. | PC1 claim 1; PC2 C1(c) |
| I9 | Definitional limits: (a) K excludes s₀ > K; (b) groups larger than B are not returned intact as one block; (c) bounded stores (40p+1) can omit mass; (d) restriction to V does not inspect its complement; (e) a fixed allocation cannot support unrestricted growth (V13); (f) with a clock guard, *delivery* depends on hardware; (g) no finite scored set certifies the global mode without excluding better unscored scores, by a maximum-score envelope or a sufficient mass bound (R supplies one on [∅, U]). | By definition. | S2 theory scope; R2C §3 row 6; PC2 C4 |
| I10 | The equal-weight PIP keeps the single-island bias for every R. | Prop P(i) PROVED (candidate); property of the **secondary** estimator (why M4 holds). | TL V3 |
| I11 | Calibration rebuilds are sequential, so calibration depth grows with I ≤ ℓ. | Definition of the kept rebuild rule. | R2B D4; S2 D4 |

**I8 moved to 4.B** (HQ amendment 01): Markov sharpness is seat-derived, unchecked, so it does not meet the PROVED-or-by-definition rule.

**Proposed as inherent, no basis filed (do not print):** R1_C §7's "finite-budget universal posterior accuracy without overlap/mixing/weight-moment conditions is unavailable"; no proof or citation filed.

### 4.B NOT inherent: OPEN, never present as limitations

**I8 (moved from 4.A, seat-derived, unchecked):** "without further assumptions, Markov is the only assumption-free probabilistic lower bound on Z; sharp given only nonnegativity and the mean (two-point law)": Seat C's argument, **not covered by PC1** (R2C D6(iii)). If used: sharper bounds need information beyond positivity and the mean (not necessarily a variance hypothesis); Z_𝒯 keeps 95% (PC1 claim 2, PROVED) · the blanket "no *useful* upper bound on Z from the run's record alone" (withdrawn from I7; only T31(c) and N17 stand) · N5(b) rebuild convergence, P(S₀ ∈ V), P(schedule_limit), P(grid_unconverged), as-coded T_n (Conjecture P) · R6 delivery P(U) → 0 (only I9(e) is definitional) · N4(iii) masked-variance severity, two-sided masked Ẑ (V11) · A4 DELIV-POP, Thm R · N1 general-h identity (binding §13.1: escalation rule) · N10, N11 mixing of the φ = 1 round, ℓ and L for growing support · N8 study generator; R5 LH-iid (XF GAP) · N12 p up to e^{Cn^α} · R7 finite-n Π(X) upper bound · S4 weight stability (binding §5.3: escalation rule) · N16 fp contract · INV row 13 positive flag power · I2 private copy of X / private Gram (C7) · §1.B start depth advantage; speed-up vs sequential MCMC (empirical) · engineering: e4 DP invariant, W-cal executed, integrated-LS0 replay, GUARD-W audit, IND-T for streams 10..9+R′ (N2, N3, N14).

---

## 5. Mapping: THM-INV §1 cells → what fills them after this meeting

"Filled" = by a TL item or obligation, at its status; "empty" = no theorem planned (reason given).

| INV row | V | A | C | F | "NO theorem" column after the meeting |
|---|---|---|---|---|---|
| 1 Target | T01 (R1) | T03♯ (R1) + N12 | — | T07 (R2) | Π(X) upper bound → **R7 OPEN** (v2). Contraction rates → **empty** (not a v1 target). Growing s₀, e^{Cn^α} → **N12 OPEN** |
| 2 Exact branch | by construction | V2–V4 | threshold; n ≤ 5 all p (w2); eventual exactness (N12, seat-proved) | W2-T26 remark ERROR | n = 2 extension (e3) PROOF SKETCH; n = 1 / zero-predictor statuses |
| 3 Blocks | — | W7-PART Thm B (S1/R5 hypothesis, e1) | tables ≤ p2^B/B; (h) stage (N15) | PART-CE2 | study packing → **N8 OPEN**. Adaptive partitions → **empty** (WORKHORSE) |
| 4 Start π₀ | exact sampler → **N9** | T22 (S1) | — | T27(i), DIL, SEP (S1, S2) | backfit start → **empty** (rejected for paper 1; recorded as future work). Start depth comparison → **N18 only under Outcome 1** |
| 5 Bridge / schedule | by construction | T22(iv) | Theorem G, STG-M (D2); ESS 0.90 as hypothesis | Lemma J | as-coded masked T_n → **N5(b3) OPEN**. Depth vs correlation → D3(b) on the ideal grid; as-coded OPEN |
| 6 Kernel | → **N9** | B2-LH etc. (R5) | m = p + B + 2 (I1) | A-REV7 | mixing → **N10 OPEN** |
| 7 Calibration | → **N5(a)** | V11 → **N4(iii)** | Theorem G; calibration share (N15) | E1c (I5) | rebuild convergence, P(schedule_limit), V coverage → **N5(b) OPEN, stay empty** |
| 8 Islands / pooling | Prop 2 + **N1** + **N2** + **N14** | Prop P(ii)/(iii) + PC1 claim 3 (V3, A1, N4) | D1(b) restated (**N15**) | — | work–depth → N15. R vs N → D4 (v2). Island variance vs correlation → **N4(iii) OPEN**. Speed-up vs MCMC → **empty** (empirical) |
| 9 Ẑ | T12/T31 + **N6** (output event, joint) | T26; P3 (A3); **N17** | — | E1a; C1 → card G1 (**N7**) | "upper bound impossible" → **corrected by N17**. Two-sided masked → **OPEN (V11, v2)**. fp → **N16 OPEN** |
| 10 PIPs (Ẑ-weighted primary) | islandwise identity (V1(a1), locked); N1 for general h (V1(a2)) | Prop P(iii), PC1 claim 3, A1; P3 + MPM^𝒯 at δ₁ < ½ (A3) | — | O-CERT empirical | joint inclusion → **A1 + N1 (PROOF SKETCH; plain averages, c_h = 0; declared 𝓗; new runs only)**; RB for marginal PIPs only. Equal-weight → A4 (secondary). Credible sets → **empty** (rejected) |
| 11 HPM | T07, T21, N200 | R5 with LS0 → **N3**; **N13**; PC1 claim 5(a) (R4) | T32(i) + LS0 + extra search | N200; OSWAP | P(U) → **R6 OPEN**. Finite-n Gibbs-route discovery → **empty** (no route). Study generator → **N8**. HPM frequency → descriptive |
| 12 Local search | Theorem A, LS-score (R3) | ThmB-T37 | ≤ (ℓ+1)(p + k*(p − k*)), k* = min(K, ⌊p/2⌋); **N11** | literal T37 fails | `local_certified` → card L1 on the returned Ŝ (deterministic gaps, **N7**). LS0 absent from production → **M2 + N2(c)/N3** |
| 13 Flags | — | — | — | V12, E1c; card G/L/R as certificates (**N7**) | positive power → **empty** (labelled heuristics) |
| 14 Resources, GUARD, numerics | Lemma RO (as recorded) + GUARD-W (**N2(e)** code audit; N6 premise (i)) | — | T32(i) | CEX-guard; `log_Z` hazard → fixed by M11 | P(resource_limit), P(schedule_limit), P(numerical_failure) → **R6 / N5 OPEN**. fp theorem → **N16 OPEN** |

INV §3a targets: §5.1 → N9; §5.2 → V1; §5.3 → S4 (OPEN); §5.4 → S1/S2; §13.1 → A1 + N1 (PROOF SKETCH); diagnostics → the card (positive certificates, not power). These goals are binding (ground rule 7): if an obligation whose failure would leave one unmet fails (N9 → §5.1; S4 → §5.3; N1 → §13.1), the goal is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change.

---

## 6. Conflicts in the earlier draft: resolution

1. V1(a) scope → split (a1)/(a2) (S3 R3-5(i)). 2. Lemma RO vs "unreviewed" → Lemma RO as recorded; GUARD-W = N2(e) (R3-5(ii)). 3. "Free of N, H, R" → v3.2 only (S2 D3d). 4. R6 "≈ 4×" → removed. 5. INV row 9 "upper bound impossible" → N17; INV row 10 "equal-weight primary" → M4. 6. HPM frequency in 𝓗 → dropped, descriptive (R3-3(a)). 7. A1 RB-joint → marginal PIPs only, c_h = 0 (R3-3(b)). 8. C4(b) "isolate {Ŝ}" → sharpness only; withdrawn (R3-1). 9. R2B "stores nested" → top_c wording (S2 D3c). 10. ESS 0.90 (a) vs (c) → (c) with caveat (R3-4). 11. R3A "duplicates collapsed" → wrong; kept (R3-4).

### Editorial items for the theorem meeting (not method questions)

- **E1. "BASIN"** (R2B §3, "ℓ versus the moves BASIN needs") is not defined in any file read; N11 is stated without it.
- **E2. "C1" names three results** (Thm SL = TL C1; MASKZPIP C1 = TL A2(iv) / card G1; O-CERT C1 = PC2). Rename for the paper.
- **E3. Seat-level results not proof-checked; statuses preserved, none upgraded:** calibration ratio 0.0512 + 0.2048·I, single tier, rounded 0.05 + 0.2·I (R2A); eventual exact dispatch for fixed p and the n = 2 extension (R2C); the n = 2 p-fold-tie statement (R3B); the store-eviction identity (R2C); Markov sharpness (R2C); Lemma KL (TL); the e4 greedy-DP route (R3A, R3B); "N1 is a short extension of the locked lemma" (R3A); "h fixed by streams 0–9 is covered by N1" (R3B).
- **E4. M14 scope:** keep PC1's precise scope; do not turn "useful" or "Markov-only" into unrestricted impossibility claims (R3C).
- **E5. Helper's reading, not a source statement:** S1(a),(d) may cover ABL-START arm B as the B = 1 partition (§1.B, Outcome 3).
- **E6. Item 1** was filled by the chair in §1.B (Outcome 2, `ITEM1_ABL_START.md`).
