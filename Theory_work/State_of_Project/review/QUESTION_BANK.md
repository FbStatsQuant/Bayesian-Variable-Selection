# SMC-BVS: State of the Project — evaluation question bank (answer key)

Built from primary sources only (the NBH archive, `Docs/HQ/STATUS.md`, the two HEADLINE files). Nothing under `State_of_Project/sections/` or `registry/` was read.

**Path shorthand.** `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`. `TLF` = `NBH/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md`. `M31` = `NBH/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md`. `FFT` = `NBH/branch_snapshots/MEET-THM/FOR_FELIPE_THEOREM_LIST.md`. `HEAD-H` = `Results/2026-10-28_New_Campaign/H2_20261102/HEADLINE_H.md`. `HEAD-L` = `Results/2026-10-28_New_Campaign/L_20261102/HEADLINE_L.md`. `STATUS` = `Docs/HQ/STATUS.md`. `SH` = `NBH/START_HERE.md`. `03` = `NBH/03_results_and_conclusions.md`. `03b` = `NBH/03b_reasoning_and_traces.md`. `05` = `NBH/05_open_questions_and_next_steps.md`. `PXN` = `NBH/branch_snapshots/API-PXNGAP/REPORT.md`. `CONF` = `NBH/branch_snapshots/ABL-CONF/REPORT.md`.

**Scoring hint.** A reviewer answer is correct when it contains the **bold** key items. Qualifiers (hypothesis names, status words, "candidate", "unchecked", regimes) are part of the key. An answer that gives the headline number but drops a flagged qualifier is partial.

**Distribution.** method 5 · empirics 6 · theory statements/hypotheses 8 · proof status/verification 4 · history/reversals/dead ends 4 · open problems/plan 3 = 30.

---

## A. Method (Q01–Q05)

### Q01 — topic: method / target posterior — difficulty: lookup
**Question.** What are the target-posterior settings of SMC-BVS v3.1: the g in the g-prior, the model-size prior, and the cap on model size?
**Key.** **g = n** (unit-information g-prior, with ridge **τ = 1**); variance prior **IG(0.01, 0.01)**; size prior **Beta-Binomial BB(1, p)** (w(k) = ½/C(2p−1, k), normalised over |S| ≤ K); cap **K = min(p, ⌊n/2⌋)**. v3.1 leaves this unchanged from v3.
**Source.** `M31:298-301`; `SH:16`.

### Q02 — topic: method / block start — difficulty: synthesis
**Question.** How does the method build its "local-to-global" start π₀: how are the blocks formed and sized, what is computed exactly inside a block, and how is π₀ sampled? What block size did the 2,400-fit study use?
**Key.** Complete-linkage clustering on 1 − |r|, **cut by node size only (≤ B), no correlation-height threshold**; next-fit packing. Each block's table of **all subsets is enumerated exactly**. π₀ = **product of block tables** (times the global size prior and cap), with exact normaliser Z̄₀, so it is **sampled exactly (iid)**. B = min(⌊√n⌋, ⌊√p⌋, B\*) with **B\* = 16** (a declared compute budget). **B = 14** in all 2,400 study fits.
**Source.** `M31:87`, `M31:180`, `M31:196`, `M31:307-308`.

### Q03 — topic: method / HPM — difficulty: lookup
**Question.** How is the reported HPM defined, and how are ties broken?
**Key.** HPM = **the best-scoring model ever scored** (strict maximum of F over every model scored by the run, including models first scored by LS0), not the most frequent particle model. Ties: **exact equality, then smallest |S|, then lexicographic**. The 10⁻⁹-nat near-tie list is informational only.
**Source.** `M31:94`, `M31:334`; `SH:16`; `TLF:292` (Ŝ⁺ = ≻-maximum under (F, −|S|, lex)).

### Q04 — topic: method / islands, R′ and stacking — difficulty: lookup
**Question.** What is the default number of final islands R′? What does optional stacking change, and what must be true about it?
**Key.** Default **R′ = 4** final islands (the 2,400-fit study is R′ = 4). Optional stacking uses **R′ = 4k at unchanged N_e** (N_e is never split across more islands), **declared before final randomness (before stream 10)**. With R′ > 4, an **extra local search runs from the islands-1–4 centre c₄**. Two records are kept (expanded, baseline), each with its own certificate card. An optional growth configuration R′_n = 4⌈log₂(n+p+1)⌉ exists; the default stays 4.
**Source.** `M31:142`, `M31:315`, `M31:425`.

### Q05 — topic: method / LS0 — difficulty: synthesis
**Question.** What is LS0, and what did it do to the study's outputs? Was it in the production code that produced the 2,400 fits?
**Key.** LS0 = **one extra local search (flip/swap rules) started from the start mode S̃₀ = argmax γ₀**, computed exactly by the block DP, run after the final local search. It reads no uniforms; its scored models join the all-scored set (provenance `ls0`, flag `ls0_improved`); an LS0 improvement does not fire E3. In the O-LS0 test export it **changed the HPM in 0 of 2,394** completed fits. The **production code of the study had no LS0** (it existed only in a test export); the integrated/merged-LS0 replay is still pending.
**Source.** `M31:48`, `M31:150`, `M31:399`; `03:188-191`.

---

## B. Empirics (Q06–Q11)

### Q06 — topic: empirics / low-p regime — difficulty: synthesis
**Question.** In the low-p regime (n = 200, p ∈ {20, 30}, exact posterior by enumeration), how accurate is Ẑ, how often does the SMC HPM equal the exact HPM, and where does SMC-BVS rank on pooled exact recovery?
**Key.** **log Ẑ error RMSE 0.012** (bias −0.0002); the 0.05·Ẑ lower bound covered Z in **100%** of fits. **SMC HPM = exact HPM in 2,400/2,400** (and 12,000/12,000 repeat fits); HPM = truth in **92.3%**; every miss is a miss of the exact posterior (0 search misses). Pooled recovery /2,400: **SSL 2,251 > SMC-BVS HPM 2,216 > SuSiE 2,183** > adaptive lasso 2,066 > MCP 2,061 > ABESS 2,051 > horseshoe 2,028 > lasso 1,852 > EN 1,692.
**Source.** `HEAD-L:7-10`, `HEAD-L:125-137`; `STATUS:26-45`.

### Q07 — topic: empirics / high-p accounting — difficulty: lookup
**Question.** Decompose the 2,400 high-p fits (n = 200, p ∈ {500, 1000}) by outcome. How many were exact recoveries, posterior misses, search misses, and stopped fits? What are the stopped fits?
**Key.** **1,829 exact · 565 posterior misses · 0 search misses · 6 stopped** (= 2,400). The 6 are **`resource_limit` stops, all in scenario S5**, counted as misses (P5 retry not run). Design: scenarios S1–S6 × 100 replicates × c ∈ {1, 0.5}, true support size 14, B = 14, K = 100. A "posterior miss" means a model scoring strictly above the truth exists (F(S₀) < F(Ŝ)).
**Source.** `03:157-168`; `HEAD-H:140-145`; `STATUS:61-66`.

### Q08 — topic: empirics / rankings by signal scale — difficulty: synthesis
**Question.** At high p, how does SMC-BVS (HPM) rank against the benchmarks at c = 0.5 versus c = 1?
**Key.** **c = 0.5:** exact recovery **370/600 (p500), 340/600 (p1000)**; first or tied-first in **11 of 12 cells**; ahead of the best benchmark (spike-and-slab lasso) by **67 datasets (p500) and 85 (p1000)**. **c = 1:** 559/560 of 600; **ranks 4th of 9**, behind **SuSiE, SSL and the horseshoe** (≈ 93% vs 95–97%); almost every miss adds variables to the truth; it beats the adaptive lasso (493/512) in 24/24 cells. The project's pitch: best at weak signal, slightly behind at strong signal; "do not claim to beat everything".
**Source.** `HEAD-H:129-136`; `STATUS:57-66`; `03:181`.

### Q09 — topic: empirics / N200 prediction — difficulty: synthesis
**Question.** What does the N200 account predict for the number of wrong reported models at n = 200, how does it compare with the observed count, and what status does the prediction rest on?
**Key.** Pooled over the 2,400 fits: **predicted ≈ 558.1 wrong reports vs 571 observed** (571 = 6 stopped + 565 posterior misses). By signal: c = 1 predicted 81.8 vs 81 observed; c = 0.5 predicted 476 vs 490. The prediction is U + ΣP̂₀(L|X): a **lower bound plus a measured term** Π(X); **a finite-n upper bound on Π(X) is OPEN** (future work FW14). Theorem N200 itself is PROVED (elementary, any n), author-only.
**Source.** `03:193-208`; `SH:51`.

### Q10 — topic: empirics / ABL-CONF — difficulty: synthesis
**Question.** What did the confirmatory start test (ABL-CONF) find about the prior start and about the block start's cost? Which claim is licensed and which is not?
**Key.** 118 fits, 3 designs (S1, S4, S5) × 10 seeds, rule pre-registered. **Claim 2 (accuracy) LICENSED:** at equal declared budgets the **prior start underestimates the evidence on all three designs**, median log Ẑ error **−13.4 (S1), −10.8 (S4), −5.7 (S5) nats** (6–13 nats), every test fit below arm A; it escalated to tier 1 in 7/9/8 of 10 fits and cost 2–4× the block start. **Claim 1 (cost) INCONCLUSIVE overall** (licensed only if it holds on every design): **S5** block start cheaper in 10/10 pairs (~30% less cost, equal accuracy); **S4** singleton factors did not deliver within the 75-min cap in 10/10 fits vs block start 9/10 (a delivery result, not equal accuracy); **S1** no significant difference (8/10, p = 0.055). The paper may state per-design results, not a general cost claim.
**Source.** `CONF:9-14`, `CONF:26-29`; `03:243-253`.

### Q11 — topic: empirics / "0 search misses" at high p — difficulty: synthesis
**Question.** The study reports "0 search misses". Is that an identified fact at high p (p = 500, 1000), or is it qualified? How does it differ at low p?
**Key.** **Low p:** 0 search misses is established against the **exact reference** (full enumeration). **High p:** 0 search misses were **detected**, but **whether the truth was ever scored is not identified for the 565 completed misses**, and the **T21 probability bound is silent there**; there is no exact reference at high p (BVS compared against the truth only). So "0 search misses" is not fully identified at high p.
**Grader note (source tension, do not penalise either reading if flagged).** `03:168` (S-ELS) additionally reports that S₀ was found in the 20,001-model top store in all 2,394 completed fits; `STATUS:75` is the more cautious wording and is the key.
**Source.** `STATUS:75`; `03:168`.

---

## C. Theory statements and hypotheses (Q12–Q19)

### Q12 — topic: theory / M5(0) composition bound — difficulty: lookup
**Question.** M5(0) states a bound on P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) involving a term D_n. State the bound and say exactly what D_n means.
**Key.** **P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2·E₀δ₁ + D_n**, with δ₁ = 1 − π(S₀) (posterior mass off the truth; read pointwise in the deterministic clause: if S₀ ∈ 𝒮⁺ and 1 − π(S₀) < ½ then Ŝ⁺ = S₀). **D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺})** in potential-run notation: the probability that the run produces output **and the true model was never scored (not in the all-scored set 𝒮⁺)** — the discovery/search-miss term. The overbar denotes the potential (uninterrupted) run, not set complement. Holds at every n, for any X.
**Source.** `TLF:86`, `TLF:282`, `TLF:292`.

### Q13 — topic: theory / T03♯ (target consistency) — difficulty: synthesis
**Question.** State the T03♯ conclusion (rate) and its main hypotheses.
**Key.** Conclusion: **1 − π(S₀) = O_P(√(log n / n))**; exact HPM and MPM are consistent (without beta-min, PIPs of the large-signal set J_n(c) converge to 1). Hypotheses: **fixed-design triangular array, fixed s₀ ≥ 1, p ≤ n^A (A fixed), s₀ ≤ K eventually**; **G** (Gaussian noise, fixed σ²); ‖μ‖² ≤ Mn and normalised truth-Gram eigenvalue ≥ φ₀²; **anchored eigenvalue conditions SE_λ(j₀) and SE_w(m_n♯; g₀)**; **beta-min BM-∞ or BM(c > c₀)**. Repairs: no expectation rate inferred from O_P, **no universal onset n₀**, no random-design or growing-sparsity extension. Status: PROVED; same-family VERIFIED, cross-family VERIFIED (A-REV2); T01–T03 locked set is SAME-FAMILY-ONLY.
**Source.** `TLF:448-451`, `TLF:462-464`.

### Q14 — topic: theory / T03♯ onset disclosure — difficulty: lookup
**Question.** At what sample size do the proof thresholds of the asymptotic selection theorem (T03♯) begin to apply, how does that compare with the study, and what is disclosed about the beta-min condition?
**Key.** Proof thresholds start near **n ≳ 2·10⁶** (an earlier W1 figure of ≈1.2·10⁵ was corrected), versus the study's **n = 200**. The beta-min constant is **at least 43× above the signals actually executed** (the earlier "about 100×" was corrected to 43×). The theory is asymptotic; N200 supplies the finite-n account. A hostile-referee simulation flagged this gap as major point (1).
**Source.** `TLF:478`, `TLF:489`; `03:102`, `03:308`; `03b:346`.

### Q15 — topic: theory / SIZE hypothesis and the study generator — difficulty: synthesis
**Question.** Which hypothesis excludes the study's own generator (groups of 5) from the LH-iid result (Theorem 5(b1) with LS0, p ≫ n included)? Why does it fail?
**Key.** The partition hypothesis **(SIZE): g_max ≤ B < 2·g_min** (group size ≤ block size bound < twice the group size). With the study's **groups of 5 and B = 14, 2g ≤ B**, so the partition **packs ≥ 2 groups per block** and **LH masking is not available**; the theorem does not describe the study's generator. This is obligation **PART-pairing (N8, = FW25), OPEN**; the g = 5 design is not the LH exhibit.
**Source.** `PXN:17-20`; `M31:180`, `M31:367`; `TLF:302`; `05:94`.

### Q16 — topic: theory / LH family — difficulty: lookup
**Question.** Define the "LH" design family used by the masked-regime theorems: group size, correlations, cross-group links, coefficients, noise, and how p grows with n.
**Key.** **p = 9⌊n^{1/3}/9⌋** (so p grows like n^{1/3}); **groups of nine**, within-group correlation **0.4**; **two disjoint cross-group links** with correlation **0.2** (all other cross-group correlations 0); each linked pair has coefficients **(1, −0.2)**, all others 0 (support size four); **σ² = 1**; exact Gram (n−1)Σ; λ_min(Σ) ≥ 0.4, p < n. For **n ≥ 9⁶** the actual blocks equal the groups (9 ≤ B ≤ 16 < 18). Two true coordinates have zero population marginal covariance with the response (masking).
**Source.** `TLF:69-70`.

### Q17 — topic: theory / W family — difficulty: lookup
**Question.** Define the "W" reporting exhibit family (used for M1(i) and M2) and contrast it with LH.
**Key.** Same p = 9⌊n^{1/3}/9⌋ and **groups of nine**; **within-group correlation 1/4**; **every cross-group correlation ε_n = 1/(np) > 0** (a stronger checked exhibit uses ε_n = n^{−1/2}/p); **two coefficients n^{−1/4} in different groups**, others 0; σ² = 1. Actual blocks = groups for n ≥ 9⁶; D_\* = O_P(1). (LH has exactly zero cross-group correlation except two links and fixed O(1) signals; W has all-pairs small positive cross-group correlation and decaying signals.)
**Source.** `TLF:71`, `TLF:178`.

### Q18 — topic: theory / M6 one-shot obstruction — difficulty: synthesis
**Question.** In M6(b), how many iid draws from the block start π₀ are needed to discover the true model on LH, and what happens on either side of that scale? What does this result NOT cover?
**Key.** **Q\*_n = p²n.** Under LH, if **Q_n/Q\*_n → 0 the probability that S₀ is absent from all draws → 1**; if **Q_n/Q\*_n → ∞ it → 0** (probability over data and draws). Underlying fact: π₀(S₀) = p^{−2}n^{−1}e^{O_P(1)} → 0 while π(S₀) → 1. One-shot evidence correction inherits a second-moment obstruction (1+χ² ≥ b²/a). **Not** a lower bound for production SMC, start-plus-search, or every one-shot estimator; "tempering is needed" is NOT claimed.
**Source.** `TLF:326-334`, `TLF:254`.

### Q19 — topic: theory / M1(d) output-event certificate — difficulty: synthesis
**Question.** What probability statement does M1(d) (and the certificate card) make about the evidence lower bound 0.05·Ẑ, and what reading is explicitly NOT licensed?
**Key.** **P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05**: a probability **joint with the output event 𝒪**; the card version uses max{Z_𝒯, 0.05Ẑ}. It is **never conditional on 𝒪** (completion): P(B | 𝒪, 𝒞) ≤ α does not follow — the guard counterexample **CEX-guard**; adaptive R′ or conditioning on completion need not preserve the bounds. The sentence "claims hold with probability ≥ 95% given the run reports" is **not proved and struck**. Premises include Lemma RO and **GUARD-W (stop-only guard), whose code audit is still open**.
**Source.** `TLF:111`, `TLF:253`; `M31:168-169`, `M31:232`.

---

## D. Proof status and verification level (Q20–Q23)

### Q20 — topic: proof status / N1 and M1 general-h — difficulty: synthesis
**Question.** What blocks M1's accuracy statement for general bounded summaries h (as opposed to marginal PIPs)? Give its status and the fallback if it fails.
**Key.** **Lemma N1**: the measured-round island identity **E[Ẑ_r·H_r(h) | 𝒞] = Z·π(h)** for the plain measured-endpoint average H_r and general bounded h. Status **PROOF SKETCH, unchecked** (numerically true-as-written); PC1's claim 3 takes it as a premise. It is the crux of the **binding proposal goal §13.1**. The locked Rao–Blackwell marginal-PIP identity does **not** need it. Fallback: ship (a), (c), (d) plus (e)–(i) **for marginal PIPs only**; if N1 is not closed after one HQ wave, ship the fallback and **escalate §13.1 to HQ/Felipe — never silently dropped**. N1 is the "longest pole" and starts first in wave 1.
**Source.** `TLF:111`, `TLF:115`, `TLF:124`; `05:87`; `M31:159` (N1 PROOF SKETCH).

### Q21 — topic: proof status / API-PXNGAP — difficulty: lookup
**Question.** What is the status and cross-check level of API-PXNGAP, and what does it claim?
**Key.** **PROVED (candidate)**: "not reviewed, not adopted"; **not cross-checked by another model family** ("needs cross-family review"); a campaign-era repair candidate outside the final theorem list. Claim: Thm 5(b1) with LS0 holds on **LH-iid for every polynomial p ≤ n^A (p ≫ n included)** with premises discharged on the random design, **given** locked T22(i),(ii), T03, classical concentration, and W7-PART Theorem B (itself a candidate). It is **asymptotic**, excludes the study's groups of 5, and does **not** claim P(U) → 0, the no-LS0 method, or masked PIP/evidence accuracy.
**Source.** `PXN:3-22`, `PXN:54-58`; `SH:48`; `03:337`.

### Q22 — topic: proof status / Lean coverage and card certification — difficulty: synthesis
**Question.** What does the Lean library certify, and is any main theorem card Lean-certified?
**Key.** Lean library: **101 declarations, 0 `sorry`**. It covers the **T21 inequality** (`t21_C1`: P(U ∨ Ŝ≠S₀) ≤ P(U) + 2Eδ₁ + P(Uᶜ, S₀∉𝒮)), **T07**, **T11(iii)** (iid miss probability), and **Theorem A / T37(i)**; T12 is only partial (the resample–move recursion `hstep` is an explicit hypothesis). The T21 inequality and Theorem A are cores of M5. **No main card is Lean-certified as a whole**; each card has a "Lean core" still to be written. Lean files are abstract finite versions, not certificates of M1–M8. All checks are AI-based (two model families + Lean for finite cores); no external human proof review.
**Source.** `SH:44-46`; `03:22`, `03:143-147`, `03:340`.

### Q23 — topic: proof status / what the study cannot claim — difficulty: lookup
**Question.** Which v3.1 outputs can NOT be claimed for the 2,400-fit study without further work?
**Key.** (i) **Joint posterior summaries** (pair inclusions, size distribution): measured-round populations were not saved — no claims. (ii) The **Ẑ-weighted (now primary) PIPs and MPM_Ẑ** on the full study: only **3 designs rescored** so far (max|ΔPIP| ≤ 1.3·10⁻³, MPMs never differ); equal-weight PIPs/MPM_eq remain valid as **secondary**. (iii) **Any stacking (R′ > 4) result**. (iv) A **4-core speed-up** (the 1.9× is a 2-core measurement). (v) "Bitwise" for concurrent calibration until W-cal runs. (vi) The **certificate card** wherever the top store was not saved. (vii) Any **depth/speed claim for the block start**.
**Source.** `M31:52-61`.

---

## E. History, reversals and dead ends (Q24–Q27)

### Q24 — topic: history / literal T37 — difficulty: synthesis
**Question.** Why was the literal T37 (truth dominance ⇒ greedy repair) abandoned, and what replaced it?
**Key.** Literal T37 was **REFUTED as written: false for d ≥ 1 on any design (Prop1-TD) and false even at d = 0 without positivity**; data agreed (1 of 2,394 fits favourable; local search repaired 0). Replaced by **Theorem A = refined T37(i): greedy repair holds exactly when TD′ holds, with positivity** (TD′ on the lattice; plus Theorem B and Theorem W/PGD). Theorem A is Lean-checked (sorry-free) and is a core of M5.
**Source.** `03b:268-272`, `03b:344`; `03:127`, `03:144`; `STATUS:76`.

### Q25 — topic: history / the "tempering is needed" spine — difficulty: synthesis
**Question.** What happened to the claim that tempering (the bridge) is needed for the method to succeed?
**Key.** **Refuted on LH** (W7-SEP Prop GU, greedy universality): start-only plus local search **does** reach S₀ on LH. Replaced by "**moving off the start is needed** (and v3's moves do that)". The retained theorem is M6: iid start-only discovery needs ~p²n draws, one-shot correction needs polynomially many draws; honest scope: masking is a property of the start, and **no published BVS example has MCMC provably slow while SMC succeeds**.
**Source.** `03b:96-101`, `03b:296-300`; `03:81`; `TLF:334`.

### Q26 — topic: history / backfit (residualised) start — difficulty: synthesis
**Question.** Why was the backfit/residualised start rejected for paper 1, and which earlier argument was withdrawn?
**Key.** Rejected because it is a **WORKHORSE change** (changes the method's law): it needs a **full re-run**, **no exact sampler with a known normaliser exists so Ẑ would not be unbiased**, and **there is no theorem** for it. The earlier rationale "gain capped at 6 of 2,400 fits" was **withdrawn (does not follow: a changed start does not nest scored sets)**. Recorded as future work/unproven candidate (pilot: favourable in ≈ 79% of regenerated fits).
**Source.** `03b:89-94`; `M31:273`; `03:214-215`.

### Q27 — topic: history / "no upper bound on Z" and "Ẑ fails only downward" — difficulty: synthesis
**Question.** Which two statements about Ẑ were corrected during the method meeting, and what is the corrected wording?
**Key.** (1) "**Ẑ can only fail downward**" was **literally false**; the corrected wording: Ẑ underestimates Z with high probability, the rare complementary event carries compensating overestimates of the same total mean, Markov caps them (P(Ẑ > 20Z) ≤ 0.05), and the certificate Ẑ < Z_𝒯 detects underestimation only. (2) The limitation "**no useful upper bound on Z**" was **not proved**: what is proved is that the properties behind the 95% bound imply **no two-sided relative-error bound** (T31(c)); an analytic bound Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} exists (PROVED).
**Source.** `03b:360-361`; `M31:173`.

---

## F. Open problems and plan (Q28–Q30)

### Q28 — topic: open / Song–Liang separation — difficulty: synthesis
**Question.** What is the status of the claimed separation from Song–Liang split-and-merge, what evidence exists, and what did HQ recommend?
**Key.** **NOT proved** (future work FW21/CJ21). The meeting could not get a sound analytic proof that split-and-merge loses true predictors under correlation; the key step (an **iteration-uniform null-BF/prior-odds claim about their algorithm**) was rejected by both check waves. The paper **compares with** Song–Liang (Theorems 1, 2, 4 and §6) and cites a **numerical counterexample as labelled evidence**: at β = 1 the exact posterior recovers S₀ in **20/20** datasets, split-and-merge recovers it in **5/318** random splits that separate the linked pair (0/318 at β = 0.6), on an LH-like design with p = 16. Our side (validity under any correlation, M1) is proved. HQ recommended **one small scout HQ** alongside wave 1; if it lands it becomes a ninth main theorem.
**Source.** `FFT:48`; `05:20`, `05:67`; `03:263`; `SH:50`.

### Q29 — topic: plan / approval state and wave order — difficulty: synthesis
**Question.** What is the approval state of the paper-1 theorem list (at the end of the archive, and now)? What are the planned next steps and wave order, and what safeguard applies to binding goals?
**Key.** At the end of the archive **Felipe had NOT approved the list** ("I will take a look … later"); HQ had approved it. **Felipe approved it on 2026-11-07** (recorded in this document; approval does not change any proof status — lead's update to the key, source: State of Project changelog). The list: **8 main cards + 12 supplement cards**; future work FW1–FW27, drops DR01–DR06. Plan after approval, per-theorem HQs each looping to a **refereed proof plus a Lean certificate for its finite core**: **wave 1 = M1, M3, LP-FOUND**; wave 2 = M2, M7, M6, LP-IDENT; wave 3 = M5, M4, M8, LP-AUDIT; wave 4 = LP-REST, LP-REP. Safeguard: if a theorem behind a binding goal (**§5.1–5.4, §13.1**; also N9 kernel validity, S4 weight stability §5.3) fails, it **comes back to Felipe for method reconsideration or explicit scope change — never silently dropped**. Target venue Biometrika.
**Source.** `SH:27`, `SH:57`; `FFT:57-66`; `05:15-19`; `M31:7`; `03:331`.

### Q30 — topic: open / M2 scale and stage-count scope — difficulty: synthesis
**Question.** What are the honest scope limits of M2 (the §5.3 weight-stability package): at what cross-block correlation scale are its constants useful, and what is and is not claimed about the stage count?
**Key.** Constants are **O(1) only for very weak cross-block correlation, ε ≲ n^{−1/2}/p** (signal energy O(√n)) on the exhibited family; at fixed ε, D_\* grows and the domain fails. The **stage count T(ε) is a step function** that can jump (example n = 40, p = 2, B = 1: baseline counts {2, 4}, T = 3 at ε = 10⁻⁵); "stable stage count" means **only the two-sided sandwich**, not continuity. The literal **one-shot reading is false** (proved). A **sharp necessity statement for the ε-scale is future work (FW22)**; all three seat forms were counterexamples. Part (a)'s D_\* route is only a PROOF SKETCH.
**Source.** `TLF:158-164`, `TLF:176`; `FFT:51`; `05:68`.

---

## Coverage check against the brief's required items

D_n → Q12 · SIZE/groups-of-5 → Q15 · N1 → Q20 · T37 → Q24 · "0 search misses" → Q11 · API-PXNGAP → Q21 · T03♯ → Q13 · onset → Q14 · N200 → Q09 · LH and W → Q16, Q17 · default R′ → Q04 · HPM → Q03 · g/size prior → Q01 · c = 0.5 vs 1 → Q08 · ABL-CONF → Q10.
