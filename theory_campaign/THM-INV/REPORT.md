# THM-INV: inventory of the method and its theory, against the goal and the literature

Branch `theory/THM-INV`. Run on 2026-11-03 (Opus 5.5; digest workers Sonnet). **No new proofs.** This is a stock-take.
Every status below is copied from its source and is never upgraded. "Candidate" means AI-proved, not reviewed for adoption, and not adopted.
Working material is in `digests/`: REG (registry, T38, architecture), API (nine API reports), AREV (Astra A-REV5..9), LIT (five LIT reports + API-POS), SL (Song–Liang 2015), LITGAP (new primary-source pass).
Those digests were written by worker agents and spot-checked by me, not line-checked. Where this report and a digest differ, the source branch file is authoritative.

## 0. Headline

1. **Selection accuracy has the most theory.**
   - The statistical half is PROVED-LOCKED, but only asymptotically: T01–T03, plus T03♯ VERIFIED cross-family.
   - The composition is PROVED-LOCKED: T21 (CONDITIONAL), with Thm N200 PROVED for the algorithm as run at every n.
   - The masked-regime consistency of the *reported* HPM has two verified routes:
     - with LS0 (Thm 5(b1), A-REV8 VERIFIED), which is a method change absent from the production core;
     - with no LS0, but only on an exact-Gram LH subfamily (B2-LH + STAB-LH, A-REV7 + API-VSTAB VERIFIED).
   - Neither covers the study's generator (groups of 5), finite n, or P(no output) → 0.
2. **Posterior accuracy (objective 1) is thin.**
   - Ẑ has unbiasedness, the islandwise identity and the Markov lower bound. These are PROVED-LOCKED, but the LIT reports say they are textbook (KNOWN—CITE).
   - Ẑ's relative accuracy is a CONJECTURE (favourable regime only); in the masked regime only a lower-tail mechanism is PROVED.
   - PIP accuracy is CONJECTURE (T26) or holds only on LH at fixed p.
   - **Joint inclusion probabilities and general posterior expectations E_π[h(S)] as n grows have no theorem at all.** Proposal §13.1 asks for exactly this.
3. **Parallel scalability (objective 2) has no theorem.**
   - There are cost bounds: T32(i) gives a polynomial score count, and Theorem G and O-STAGES bound the stage count.
   - There is no statement of work/depth versus p and correlation, no island-count theory beyond standard pooling, and no comparison of depth with sequential MCMC.
   - **The thesis sentence ("correlation costs only depth and particles, never correctness") is not a theorem yet.** Its "never correctness" half is fixed-data Monte Carlo validity (KNOWN—CITE), and its "costs only depth" half is unproved.
4. **Against Song–Liang we exceed on every theorem type except the parallel-cost analysis (§6), which we lack in comparable form.** We also lack their weak-condition posterior contraction in Hellinger distance.
5. **Literature.**
   - Of the proposal's five themes, *composite likelihood / posterior calibration* and *diagnostics for scalable computation* had no LIT coverage.
   - A primary-source pass (10 works, all verified) finds no precedent for using a composite/block-product posterior as an *SMC start that is then corrected exactly*.
   - Chatterjee–Diaconis (2018) supplies the right cost scale exp(KL(π‖π₀)) for a one-shot correction.

## 1. Component map

Legend: **V** = validity (the target is right / the estimator is unbiased or invariant), **A** = accuracy (error → 0 or bounded), **C** = cost, **F** = failure-mode characterisation.
Status words as in the sources (registry/REG digest, API, AREV). **NONE** = no theorem of any status. "Idealised" = holds for a variant (frozen calibration, iid final draws, LS0, exact Gram, fixed p, ideal grid), not the production run.

| # | Component (METHODOLOGY_v3 §) | V | A | C | F | Properties with NO theorem |
|---|---|---|---|---|---|---|
| 1 | Target posterior (§5; g = n, IG(.01,.01), BB(1,p), cap ⌊n/2⌋) | Reduction V1 / T01 PROVED-LOCKED | T02, T03 PROVED-LOCKED; T03♯ PROVED, XF A-REV2 VERIFIED; asymptotic (onset n ≳ 2·10⁶; SE impossible at n = 200). N200 Prop 2: lower bracket on Π(X) PROVED | — | T07 (size-only prior cannot fix a same-size swap) PROVED-LOCKED; API-POS Prop U (no underfitted local modes on LH) PROOF SKETCH | **Finite-n upper bound on Π(X)** (OPEN, API-N200); posterior contraction / coefficient rates (V3) NONE; growing s₀ NONE |
| 2 | Exact branch (§6.2) | by construction (enumeration) | V2–V4 apply directly | branch threshold is explicit | W2-T26 exact-branch remark ERROR (A-REV5) | — |
| 3 | Blocks / partition (§6.3: complete linkage, cut, next-fit packing) | — | W7-PART Thm B (partition = groups on SIZE g ≤ B < 2g, LH-iid) PROVED, VERIFIED* A-REV6/A-REV9; explicit constants GAP | tables ≤ p·2^B/B scores (by count) | PART-CE2: unequal groups not merged (COUNTEREXAMPLE) | **Partition law for the study's packing (groups of 5, 2g ≤ B)** NONE (A-REV6); correlation-adaptive blocking; random/overlapping partitions NONE |
| 4 | Composite start π₀ (exact Z̄₀, iid draws) | exact sampler and normaliser: by construction (V5 target; no registry theorem found (?)) | T22(i)(ii)(iv) PROVED-LOCKED (deterministic mass on a reference); T22(iii) favourable rate CONDITIONAL (EXP′ PROVED, XF VERIFIED* fixed design); FAV-ThmB PROVED (author only) | — | T27(i) masking law PROVED-LOCKED, CONDITIONAL (Thm3/4-EXP XF VERIFIED); DIL-E/E1/R/N (dilution, the study's actual mechanism) PROVED, XF VERIFIED; SEP-A/B (start-only / one-shot reweighting needs p^c n^{c/2} draws) PROVED, XF VERIFIED | Start quality for random designs with adaptive packing; backfit start (API-RESID) NONE |
| 5 | Bridge γ_φ = γ₀e^{φd} and schedule (§6.3, 6.6) | each stage targets γ_φ exactly (by construction) | T22(iv) (bridge never loses S₀ mass below the smaller endpoint) PROVED-LOCKED; OWS weight-stability WS1–WS8 PROVED (no review), W(a–f) XF VERIFIED under H-ORTH | Theorem G (stage count = pilot + ⌈log₂1/η⌉) PROVED, deterministic, as-run rule (API-T26BUD, candidate); STG-M (log₂A₀ stages for a crossing, ideal two-state grid) PROVED, XF VERIFIED*; one-stage regime Thm 1 PROVED (favourable only) | Lemma J (an ESS-0.9 step cannot be blind to a mode) PROVED | **Realised stage count T_n in the masked regime** (O_P(1) OPEN; Conjecture P); depth as a function of correlation NONE |
| 6 | Move kernel (Gibbs, swaps, neighbour swaps, independence; random order) | reversibility and self-adjointness: by construction, consultant-checked (V5), no registry row (?) | Masked discovery: Thm B-T24 PROVED (vacuous at n = 200); BG3 PROVED, XF VERIFIED (fixed p); B2-LH PROVED-UNDER STAB-LH, XF VERIFIED (exact-Gram LH subfamily, no LS0) | — | General LH locking FALSE (A-REV7 counterexample); H24 retired (CE1/CE2 COUNTEREXAMPLE) | **Mixing / spectral gap of the φ = 1 round (V10)** NONE; YWJ/ZYVR do not apply to the paper's prior (API-POS PROOF SKETCH; LIT-MCMC Prop OB sketch) |
| 7 | Calibration, candidate set V, grid rebuilds, tiers, escalation (§6.7–6.9) | final run independent of calibration (frozen before final randomness): T12 frozen-run identities; IND-T PROVED, XF VERIFIED* (A-REV1 only) | Masked Ẑ lower tail decided by the crossing temperature: MASKZPIP E1/E2 PROVED (candidate); "resolved grid ⇒ O_P(√(T/N))" (V11) CONJECTURE, OPEN for c ≥ 2 | Theorem G; Rule CAP (method change) PROVED | E1c: island agreement uninformative when the grid is blind (PROVED) | **Rebuild-loop convergence** NONE; probability of `schedule_limit` / `grid_unconverged` NONE; whether V contains the competing pair NONE |
| 8 | Islands and pooling (R = 4 final; independent streams) | Prop 2(a,b,d,e) islandwise E[Ẑ_r PIP̂_rj] = Z·PIP_j PROVED (XF A-REV4 GAP on output Markov wording); Prop 2(c) pooled product is not an identity PROVED; IND-T audit HOLDS | Ẑ-weighted pooling is consistent as R → ∞ at fixed N: standard (Dai et al. 2022; LIT-PAR TH2) | — | — | **Parallel speed-up / work–depth theorem** NONE; choice of R vs N NONE; island variance vs correlation NONE |
| 9 | Ẑ and 0.05·Ẑ lower bound (§6.12) | T12 E[Ẑ_r] = Z PROVED-LOCKED; T31(i) Markov bound PROVED-LOCKED; OPW2-ThmA/B relative variance PROVED, XF VERIFIED* (frozen calibration) | Favourable: T26-ThmA/B PROVED / PROVED-UNDER (realised T_n not controlled); Thm 6 overall CONJECTURE. Masked: only the lower-tail mechanism E1/E2; top-store Z_T sandwich P3 PROVED | — | Ẑ underestimates by the log-odds overshoot of a late switch (E1a PROVED); per-fit certificate Ẑ < Z_T ⇒ underestimate (C1 PROVED) | **Two-sided relative accuracy of Ẑ in the masked regime** NONE (an upper bound on Z is impossible from a run, MASKZPIP); floating point: VAL-FP MEASURED at p ≤ 40 only |
| 10 | PIPs (Rao–Blackwellised; equal-weight primary, Ẑ-weighted secondary), MPM (§6.11) | islandwise identity (T12/Prop 2); ADRAFT-ThmA/uniPIP (fixed-data N → ∞ consistency) PROVED (Astra author, Astra check) | T26(ii) CONJECTURE (favourable); MASKZPIP P1 (bias ≤ TV) PROVED; P2 composition PROVED (needs locking, LH fixed p); P3 top-store PIP^T PROVED (deterministic) | — | O-CERT: π(S₀) ≤ 0.37 even on correct fits at n = 200 (empirical) | **Joint inclusion probabilities** NONE; **equal-weight PIP accuracy at fixed R** NONE; credible-set / coverage NONE (rejected as a target) |
| 11 | HPM (best ever scored), near ties, decision (§6.10) | T07 Bayes rules PROVED-LOCKED; T21(C1) PROVED-LOCKED, CONDITIONAL; N200 (every n, as run) PROVED | T38(0) composition PROVED, XF VERIFIED; Thm 5(a) PROVED-UNDER (favourable, iid draws); (b1) LS0 PROVED-UNDER, XF VERIFIED; (b1-LH-iid) p ≫ n PROVED (candidate), XF GAP; (b2-LH) no LS0 PROVED-UNDER STAB-LH, XF VERIFIED | T32(i) polynomial score count PROVED (XF GAP on qualification) | N200 lower bound; OSWAP posterior-miss theory (T4, P5 PROVED; P1–P3 XF GAP) | **P(U) → 0 (output delivered)** NONE; **finite-n discovery bound for the Gibbs route** OPEN; study generator (groups of 5) NONE |
| 12 | Local search, `local_certified` (§6.10) | Theorem A (exact greedy repair) PROVED, XF VERIFIED*, Lean sorry-free; LS-score (with LS0) PROVED, XF VERIFIED* | ThmB-T37(incl) finite-n union bound PROVED; ThmW PROVED (candidate) | ≤ (ℓ+1)(p + K(p−K)) scores (count) | Literal T37/TD fails generically (Prop1-TD, CEX1/2); region-form Theorem W fails on masked LH c ≥ 2; data: 0 moves in 2,394/2,394 | Meaning of `local_certified` beyond "no improving neighbour" (V12) NONE positive; LS0 absent from production (API-AUDIT) |
| 13 | Flags and diagnostics (E1–E3, ESS, grid flags) | — | — | — | V12 (checks fail to fire with non-crossing kernels) is the only theory, all negative; MASKZPIP E1c; O-CERT C1–C6 per-fit certificates (some XF ERROR) | **Any positive power result (a flag fires when the output is wrong)** NONE; ESS/k̂/coupling diagnostics not analysed (§4) |
| 14 | Resource limits, statuses, GUARD, numerics (§2, §6.13, §8) | Lemma RO run/output split PROVED, XF VERIFIED; GUARD implementation fact HOLDS (literal "every output equals" ERROR, A-REV8) | — | T32(i); Cost-T38 PROVED-UNDER | CEX-guard COUNTEREXAMPLE (path-dependent stopping biases Ẑ); `fit$log_Z` hazard on stopped fits (API-AUDIT) | **P(resource_limit), P(schedule_limit), P(numerical_failure)** NONE (V13); floating-point error theorem NONE |

**Observations.**
- Nearly every positive theorem about the *algorithm* (rows 5–12) is either idealised or about a design the study did not use. The idealisations are a frozen calibration, iid final draws, an ideal grid, LS0, exact-Gram LH and fixed p. The study's designs (groups of 5, p ≫ n) are uncovered.
- The only results that hold for the algorithm exactly as run, at every n, are bookkeeping:
  - T07, T21(C1), N200 Lemma 1 and Thm N200, Theorem G;
  - the T12/T31 identities, given the frozen calibration;
  - Lemma RO and the per-fit certificates.

## 3. Coverage against the goal

### 3a. Proposal theory targets (Local-to-Global proposal §5, §13.1)

| Proposal target | What we have | Verdict |
|---|---|---|
| §5.1 / Prop 1: exactness under MH correction (π invariant) | Each move reversible for γ_φ; the random-order round is self-adjoint. This is by construction (METHODOLOGY_v3 §6.5, V5) and checked by three consultants; I found no registry row for it (?). It is standard (proposal: "standard detailed balance") | **MATCH** (textbook; state it, cite it) |
| §5.2: SMC consistency as N → ∞ for the specified local-to-global sequence | ADRAFT-ThmA/CorA1 (fixed-data convergence of SMC estimators) PROVED, Astra author with Astra check only. T12/T31 unbiasedness PROVED-LOCKED. All standard (Del Moral et al. 2006; LIT-SMC/LIT-PAR call T12/T31 KNOWN—CITE) | **MATCH** (needs a cross-family check of ADRAFT-ThmA, or just cite) |
| §5.3: weight stability under weak cross-block dependence (Thm 1 "possible direction") | O-WSTAB WS1–WS8 PROVED (no review), W(a–f) XF VERIFIED under H-ORTH, ideal grid; WS6e CONJECTURE, WS8d OPEN. FD-W(a) PROVED-UNDER, (b) PROOF SKETCH, (c) CONJECTURE. T22(iii)/EXP′ (favourable start) is the selection-side analogue | **PARTLY MATCHED** (orthogonal-type idealisation only; nothing for the actual partition) |
| §5.4: approximation error when exact correction is unavailable (KL, TV, PIP and joint-PIP error) | Inverted in our design: correction is always exact, so the "approximation" is π₀ itself. T27(i), DIL-*, SEP-A/B quantify how far π₀ is from π (π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}). FD-NM (naive merge fails) ERROR, repair pending (A-REV4/A-REV6) | **EXCEEDED in kind** (lower bounds on the merge's error); the naive-merge proposition itself is still unrepaired |
| §13.1: estimates of E_π[h(θ)] converge to the truth | Fixed data, N → ∞: ADRAFT-ThmA (standard). Truth as n → ∞ at n-indexed budgets: only h = 1{S = S₀} (T38/N200), h = Z (T26(i), favourable, CONJECTURE), and h = 1{j ∈ S} (T26(ii) CONJECTURE; P1–P3 on LH at fixed p). General h (joint inclusion, β-functionals, predictions) NONE | **LACK** (the single most visible gap against the proposal) |
| §4.4 / §8.2: diagnostics (ESS, local–global discrepancy) as a new device | Only negative results (V12, E1c); no positive diagnostic theorem | **LACK** |

### 3b. Song & Liang (2015) theorem types (digest `SL.md`)

| SL result (type) | SL scope | Our counterpart | Verdict |
|---|---|---|---|
| Thms 1–2, Cor 1, eq. (16): posterior consistency (Hellinger contraction, rates) | exact full posterior; bounded predictors; P_n < e^{Cn^α} | T03/T03♯: selection consistency, 1 − π(S₀) = O_P(√(log n / n)), with p ≤ n^A. Coefficient/prediction contraction (V3) NONE | **MATCH for selection; LACK for contraction rates and p up to e^{Cn^α}** (we have p ≤ n^A only) |
| Thm 3: sure screening of identifiable true predictors (marginal inclusion → 1) | exact posterior | T03 ("large signals get PIPs → 1 without beta-min") PROVED-LOCKED | **MATCH** (about the exact posterior; our estimated PIPs are only covered in the favourable regime, T26 CONJECTURE) |
| Thm S (supplement): MAP consistency | exact posterior | T03 (HPM/MPM of the true posterior) **plus** the reported HPM of the algorithm: T38(0)/(a)/(b1)/(b2-LH), N200 | **EXCEED**: SL never prove anything about the merged output ("SAM is consistent" is informal; SL digest §2) |
| Thm 4, Cor 2: misspecified-subset posterior concentrates on the KL projection | fixed subset, n → ∞ | Our blocks *are* misspecified subset posteriors. T22 and T27 and DIL-* describe exactly when the block-product start does and does not hold the truth (a lower bound: π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} under masking), and the SMC removes the dependence | **EXCEED** (we quantify the failure, and correctness does not depend on it); their Condition 5 (|cov(x_t, y)| > 0) is exactly what masking violates |
| §6: complexity, K_n = O(√P_n), parallel O(P_n^{(1+α)/2}) + O(nP_n) | heuristic, no accuracy trade-off | T32(i) total score count (polynomial, 2.7·10¹¹ at (200, 500)); Theorem G; STG-M; table cost p·2^B/B, embarrassingly parallel | **LACK of a comparable parallel-cost statement**: we have total work, not work/depth/speed-up versus p, R and correlation |
| UQ of the merged output | none (SL: "only provides an approximate quantification of uncertainty") | Fixed-data exactness (T12, ADRAFT-ThmA); n-indexed accuracy only favourable/LH | **EXCEED at fixed data; LACK as n grows in correlated (masked) designs** |

### 3c. The three objectives (Felipe, 2026-11-03)

| Objective | Covered by | Missing |
|---|---|---|
| (1) Posterior accuracy: Ẑ | T12, T31(i) (KNOWN—CITE); OPW2 Thm A/B (relative variance, frozen; possibly Cérou et al. 2011, unchecked); T26(i) favourable CONJECTURE; masked E1/E2 lower tail | two-sided masked-regime accuracy; finite-n precision at study budgets |
| (1) PIPs | Prop 2 islandwise; T26(ii) CONJECTURE; P1–P3 (LH, fixed p) | equal-weight pooled PIP accuracy; masked p ≫ n |
| (1) Joint inclusion | — | **everything** |
| (2) Parallel scalability | T32(i) total work; table cost; Theorem G / STG-M stage counts (sequential depth, favourable or ideal) | work–depth theorem; islands-vs-particles trade-off; "correlation costs depth, never correctness" |
| (3) Selection accuracy | T03, T07, T21, N200, T38(0)/(a)/(b1)/(b2-LH) | study generator; P(U) → 0; finite-n discovery; upper bound on Π(X) |
